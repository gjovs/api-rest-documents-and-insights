from abc import ABC, abstractmethod
from typing import List
from infrastructure.persistence.models import Signer, Document


class ISignerRepository(ABC):
    @abstractmethod
    def get_by_id(self, signer_id: str) -> Signer | None:
        pass

    @abstractmethod
    def bulk_create_from_list(self, signers_list: List[dict], document: Document):
        pass

    @abstractmethod
    def find_by_zapsign_token(self, zapsign_token: str) -> Signer | None:
        pass

    @abstractmethod
    def update_status(self, signer: Signer, new_status: str):
        pass
