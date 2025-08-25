import base64
import os
import shutil
import uuid

import util.shell_util as shell_util
import util.ssl_util as ssl_util
import util.template_util as template_util
from configuration.logging_configuration import logger as log
from dto.certificate_dto import GenerateCertificateRequest, GenerateCertificateResponse
from persistence.model.certificate_entity import CertificateEntity
from persistence.repository.certificate_repository import CertificateRepository
from service import CAService


class CertificateService:
    def __init__(self, certificate_repository: CertificateRepository,
                 certificate_authority_service: CAService):
        self.certificate_repository = certificate_repository
        self.certificate_authority_service = certificate_authority_service

    def get_certificate(self, certificate_id):
        log.info(f"Retrieving certificate with ID {certificate_id}")
        return self.certificate_repository.get_certificate(certificate_id)

    def get_certificates_by_ca(self, ca_id: str):
        log.info(f"Retrieving certificates for CA ID {ca_id}")
        return self.certificate_repository.find_certificates_by_ca(ca_id=ca_id)

    def create_certificate(self, certificate_data: GenerateCertificateRequest):
        log.info(f"Creating certificate for domain {certificate_data.domain}")
        log.info("Checking if certificate already exists...")
        existing_certificate = self.certificate_repository.find_certificate_by_domain(certificate_data.domain)
        if existing_certificate:
            log.info("Certificate already exists, returning existing certificate.")
            return GenerateCertificateResponse(
                certificate_id=existing_certificate.certificate_id,
                domain=existing_certificate.domain,
                crt=existing_certificate.crt,
                key=existing_certificate.key
            )
        log.info(f"Creating certificate for domain {certificate_data.domain}...")
        return self.__do_generate_certificate(certificate_data=certificate_data)

    def __do_generate_certificate(self, certificate_data: GenerateCertificateRequest):
        # Download CA certificate and key
        log.info("Retrieving CA...")
        ca = self.certificate_authority_service.get_ca_by_id(ca_id=certificate_data.ca_id)
        os.makedirs(ca.domain, exist_ok=True)
        with open(f'{ca.domain}/{ca.domain}.crt', 'w') as ca_crt_file:
            content = base64.b64decode(ca.crt).decode('utf-8')
            ca_crt_file.write(content)
        with open(f'{ca.domain}/{ca.domain}.key', 'w') as ca_key_file:
            content = base64.b64decode(ca.key).decode('utf-8')
            ca_key_file.write(content)

        # Build configuration file
        log.info("Generating configuration files...")
        os.makedirs(f"{ca.domain}/{certificate_data.domain}", exist_ok=True)
        cert_conf = template_util.generate_cert_conf(domain=certificate_data.domain)
        csr_conf = template_util.generate_csr_conf(country=certificate_data.country,
                                                   state=certificate_data.state,
                                                   location=certificate_data.location,
                                                   organization=certificate_data.organization,
                                                   organization_unit=certificate_data.organization_unit,
                                                   domain=certificate_data.domain)
        with open(f'{ca.domain}/{certificate_data.domain}/cert.conf', 'w') as cert_conf_file:
            cert_conf_file.write(cert_conf)
        with open(f'{ca.domain}/{certificate_data.domain}/csr.conf', 'w') as csr_conf_file:
            csr_conf_file.write(csr_conf)

        # Generate certificate server key
        log.info("Generating certificate files...")
        shell_util.run_command(f"openssl genrsa -out \"{ca.domain}\"/\"{certificate_data.domain}\"/server.key 2048")

        # Generate Sign Request
        shell_util.run_command(
            f"""openssl req -new -key \"{ca.domain}\"/\"{certificate_data.domain}\"/server.key \
-out \"{ca.domain}\"/\"{certificate_data.domain}\"/server.csr \
-config \"{ca.domain}\"/\"{certificate_data.domain}\"/csr.conf""")

        # Generate certificate signed by CA
        shell_util.run_command(
            f"""openssl x509 -req \
-in \"{ca.domain}\"/\"{certificate_data.domain}\"/server.csr \
-CA \"{ca.domain}\"/\"{ca.domain}\".crt -CAkey \"{ca.domain}\"/\"{ca.domain}\".key \
-CAcreateserial -out \"{ca.domain}\"/\"{certificate_data.domain}\"/server.crt \
-days 365 \
-sha256 -extfile \"{ca.domain}\"/\"{certificate_data.domain}\"/cert.conf""")

        # Save all
        encoded_crt, encoded_key = self.__get_encoded_crt_and_key(ca_domain=ca.domain,
                                                                  certificate_domain=certificate_data.domain)
        entity = CertificateEntity(certificate_id=uuid.uuid4().__str__(),
                                   ca_id=ca.ca_id,
                                   domain=certificate_data.domain,
                                   crt=encoded_crt,
                                   key=encoded_key)
        log.info("Saving certificate to database")
        entity = self.certificate_repository.save(certificate_data=entity)
        shutil.rmtree(ca.domain)
        return GenerateCertificateResponse(certificate_id=entity.certificate_id,
                                           domain=certificate_data.domain,
                                           crt=entity.crt,
                                           key=entity.key)

    def __get_encoded_crt_and_key(self, ca_domain: str, certificate_domain: str) -> tuple[str, str]:
        crt_command = f'cat "{ca_domain}"/"{certificate_domain}"/server.crt | base64 -w 0'
        key_command = f'cat "{ca_domain}"/"{certificate_domain}"/server.key | base64 -w 0'
        _, encoded_crt = shell_util.run_command(crt_command)
        _, encoded_key = shell_util.run_command(key_command)
        return encoded_crt, encoded_key

    def delete_certificate(self, certificate_id):
        log.info(f"Deleting certificate with ID {certificate_id}")
        self.certificate_repository.delete_certificate_by_id(certificate_id=certificate_id)

    def renew(self, certificate_id: str):
        log.info(f"Renewing certificate with ID {certificate_id}")
        entity = self.certificate_repository.get_certificate(certificate_id=certificate_id)
        dictionary = ssl_util.parse_certificate(entity.crt)
        return self.__do_generate_certificate(certificate_data=GenerateCertificateRequest(ca_id=entity.ca_id,
                                                                                          domain=entity.certificate_data.domain,
                                                                                          country=dictionary["country"],
                                                                                          location=dictionary[
                                                                                              "location"],
                                                                                          state=dictionary["state"],
                                                                                          organization=dictionary[
                                                                                              "organization"],
                                                                                          organization_unit=dictionary[
                                                                                              "organization_unit"]))
