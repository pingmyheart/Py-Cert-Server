from typing import List

from persistence.model.ca_entity import CAEntity


class CARepository:
    def __init__(self, mongo_client):
        self.__collection = mongo_client.ca

    def find_all(self) -> List[CAEntity]:
        """
        Find all CA entities in the database.
        :return: List of CAEntity
        """
        return [CAEntity.model_validate(model) for model in self.__collection.find()]

    def find_ca_by_domain(self, ca_domain) -> CAEntity | None:
        """
        Find a CA entity by its domain.
        :param ca_domain: The domain of the CA.
        :return: CAEntity if found, otherwise None.
        """
        entity = self.__collection.find_one({"domain": ca_domain})
        if entity:
            return CAEntity.model_validate(entity)
        return None

    def find_ca_by_id(self, ca_id: str) -> CAEntity | None:
        """
        Find a CA entity by its ID.
        :param ca_id:
        :return:
        """
        entity = self.__collection.find_one({"ca_id": ca_id})
        if entity:
            return CAEntity.model_validate(entity)
        return None

    def save(self, ca_data: CAEntity):
        """
        Save a CA entity to the database.
        :param ca_data: CAEntity to be saved.
        :return: The saved CAEntity.
        """
        self.__collection.insert_one(ca_data.model_dump())
        return ca_data

    def delete_ca_by_id(self, ca_id):
        """
        Delete a CA entity by its ID.
        :param ca_id: The ID of the CA to be deleted.
        :return: The result of the delete operation.
        """
        return self.__collection.delete_one({"ca_id": ca_id})
