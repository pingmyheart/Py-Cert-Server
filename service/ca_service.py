import os
import shutil
import uuid

from dto.ca_dto import GenerateCertificateAuthorityResponse, GenerateCertificateAuthorityRequest
from persistence.model.ca_entity import CAEntity
from persistence.repository.ca_repository import CARepository
from util.shell_util import run_command


class CAService:
    def __init__(self, ca_repository: CARepository):
        self.ca_repository = ca_repository

    def get_ca(self, ca_domain: str):
        return self.ca_repository.find_ca_by_domain(ca_domain)

    def get_ca_by_id(self, ca_id: str) -> CAEntity:
        return self.ca_repository.find_ca_by_id(ca_id)

    def create_ca(self, ca_data: GenerateCertificateAuthorityRequest) -> GenerateCertificateAuthorityResponse:
        return self.__idempotent_create_ca(ca_data)

    def __idempotent_create_ca(self,
                               ca_data: GenerateCertificateAuthorityRequest) -> GenerateCertificateAuthorityResponse:
        """
        Create a CA if it does not already exist.
        """
        existing_ca = self.ca_repository.find_ca_by_domain(ca_domain=ca_data.domain)
        if existing_ca:
            return GenerateCertificateAuthorityResponse(domain=existing_ca.domain,
                                                        crt=existing_ca.crt,
                                                        ca_id=existing_ca.ca_id)
        # Generate CA certificate and key
        self.__generate_ca_crt_and_key(domain=ca_data.domain,
                                       country=ca_data.country,
                                       location=ca_data.location)
        encoded_crt, encoded_key = self.__get_encoded_ca_crt_and_key(ca_domain=ca_data.domain)
        entity = CAEntity(ca_id=uuid.uuid4().__str__(),
                          domain=ca_data.domain,
                          crt=encoded_crt,
                          key=encoded_key)
        entity = self.ca_repository.save(ca_data=entity)
        shutil.rmtree(ca_data.domain)
        return GenerateCertificateAuthorityResponse(domain=ca_data.domain,
                                                    crt=entity.crt,
                                                    ca_id=entity.ca_id)

    def __generate_ca_crt_and_key(self, domain: str,
                                  country: str,
                                  location: str) -> None:
        os.makedirs(domain, exist_ok=True)
        command = f'openssl req -x509 -sha256 -days 356 -nodes -newkey rsa:2048 -subj "/CN={domain}/C={country}/L={location}" -keyout "{domain}"/"{domain}".key -out "{domain}"/"{domain}".crt'
        # Execute the command to generate CA certificate and key
        run_command(command)

    def __get_encoded_ca_crt_and_key(self, ca_domain: str) -> tuple[str, str]:
        crt_command = f'cat "{ca_domain}"/"{ca_domain}".crt | base64 -w 0'
        key_command = f'cat "{ca_domain}"/"{ca_domain}".key | base64 -w 0'
        _, encoded_crt = run_command(crt_command)
        _, encoded_key = run_command(key_command)
        return encoded_crt, encoded_key
