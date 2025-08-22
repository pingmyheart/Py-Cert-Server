from typing import List

from persistence.model.certificate_entity import CertificateEntity


class CertificateRepository:
    def __init__(self, mongo_client):
        self.__collection = mongo_client.certs

    def find_certificates_by_ca(self, ca_id: str) -> List[CertificateEntity]:
        """
        Retrieve all certificate for a given CA
        :param ca_id: certification authority id
        :return: list of certificates
        """
        return [CertificateEntity.model_validate(model) for model in self.__collection.find({"ca_id": ca_id})]

    def get_certificate(self, certificate_id: str):
        """
        Retrieve a certificate by its ID.
        :param certificate_id: The ID of the certificate to retrieve.
        :return: The certificate data if found, otherwise None.
        """
        entity = self.__collection.find_one({"certificate_id": certificate_id})
        if entity:
            return CertificateEntity.model_validate(entity)
        return None

    def get_certificate_by_domain(self, domain: str):
        """
        Retrieve a certificate by its domain.
        :param domain: The domain of the certificate to retrieve.
        :return: The certificate data if found, otherwise None.
        """
        entity = self.__collection.find_one({"domain": domain})
        if entity:
            return CertificateEntity.model_validate(entity)
        return None

    def save(self, certificate_data: CertificateEntity):
        """
        Create new certificate record
        :param certificate_data: entity
        :return: saved entity
        """
        self.__collection.insert_one(certificate_data.model_dump())
        return certificate_data

    def delete_certificate_by_id(self, certificate_id):
        """
        Delete a certificate by its ID.
        :param certificate_id: The ID of the certificate to delete.
        :return: The result of the delete operation.
        """
        return self.__collection.delete_one({"certificate_id": certificate_id})
