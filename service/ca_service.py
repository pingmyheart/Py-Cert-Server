import os
import shutil
import uuid

import util.ssl_util as ssl_util
from configuration.logging_configuration import logger as log
from dto.ca_dto import GenerateCertificateAuthorityResponse, GenerateCertificateAuthorityRequest
from persistence.model.ca_entity import CAEntity
from persistence.repository.ca_repository import CARepository
from util.shell_util import run_command


class CAService:
    def __init__(self, ca_repository: CARepository):
        self.ca_repository = ca_repository

    def get_ca(self, ca_domain: str):
        log.info(f"Retrieving CA with domain {ca_domain}")
        return self.ca_repository.find_ca_by_domain(ca_domain)

    def get_ca_by_id(self, ca_id: str) -> CAEntity:
        log.info(f"Retrieving CA with ID {ca_id}")
        return self.ca_repository.find_ca_by_id(ca_id)

    def delete_ca_by_id(self, ca_id: str):
        log.info(f"Deleting CA with ID {ca_id}")
        return self.ca_repository.delete_ca_by_id(ca_id)

    def create_ca(self, ca_data: GenerateCertificateAuthorityRequest) -> GenerateCertificateAuthorityResponse:
        log.info(f"Creating CA with domain {ca_data.domain}")
        return self.__idempotent_create_ca(ca_data)

    def __idempotent_create_ca(self,
                               ca_data: GenerateCertificateAuthorityRequest) -> GenerateCertificateAuthorityResponse:
        """
        Create a CA if it does not already exist.
        """
        log.info("Checking if CA already exists...")
        existing_ca = self.ca_repository.find_ca_by_domain(ca_domain=ca_data.domain)
        if existing_ca:
            log.info("CA already exists, returning existing CA.")
            return GenerateCertificateAuthorityResponse(domain=existing_ca.domain,
                                                        crt=existing_ca.crt,
                                                        ca_id=existing_ca.ca_id)
        log.info(f"Creating CA with domain {ca_data.domain}...")
        return self.__do_create_ca(ca_data=ca_data)

    def __do_create_ca(self, ca_data: GenerateCertificateAuthorityRequest) -> GenerateCertificateAuthorityResponse:
        # Generate CA certificate and key
        log.info("Generating CA certificate and key")
        self.__generate_ca_crt_and_key(domain=ca_data.domain,
                                       country=ca_data.country,
                                       location=ca_data.location)
        encoded_crt, encoded_key = self.__get_encoded_ca_crt_and_key(ca_domain=ca_data.domain)
        entity = CAEntity(ca_id=uuid.uuid4().__str__(),
                          domain=ca_data.domain,
                          crt=encoded_crt,
                          key=encoded_key)
        log.info("Saving CA to database")
        entity = self.ca_repository.save(ca_data=entity)
        shutil.rmtree(ca_data.domain)
        return GenerateCertificateAuthorityResponse(domain=ca_data.domain,
                                                    crt=entity.crt,
                                                    ca_id=entity.ca_id)

    def __generate_ca_crt_and_key(self, domain: str,
                                  country: str,
                                  location: str) -> None:
        os.makedirs(domain, exist_ok=True)
        command = f"""openssl req -x509 \
-sha256 -days 365 \
-nodes -newkey rsa:2048 \
-subj "/CN={domain}/C={country}/L={location}" \
-keyout "{domain}"/"{domain}".key -out "{domain}"/"{domain}".crt"""
        # Execute the command to generate CA certificate and key
        run_command(command)

    def __get_encoded_ca_crt_and_key(self, ca_domain: str) -> tuple[str, str]:
        crt_command = f'cat "{ca_domain}"/"{ca_domain}".crt | base64 -w 0'
        key_command = f'cat "{ca_domain}"/"{ca_domain}".key | base64 -w 0'
        _, encoded_crt = run_command(crt_command)
        _, encoded_key = run_command(key_command)
        return encoded_crt, encoded_key

    def find_all(self) -> list[CAEntity]:
        return self.ca_repository.find_all()

    def renew(self, ca_id: str):
        log.info(f"Renewing CA with ID {ca_id}")
        dictionary = ssl_util.parse_certificate(self.get_ca_by_id(ca_id=ca_id).crt)
        return self.__do_create_ca(ca_data=GenerateCertificateAuthorityRequest(domain=dictionary["domain"],
                                                                               country=dictionary["country"],
                                                                               location=dictionary["location"]))
