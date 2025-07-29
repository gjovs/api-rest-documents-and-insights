from abc import ABC, abstractmethod
from infrastructure.persistence.models import Document


class IDocumentRepository(ABC):
    @abstractmethod
    def create(self, **data) -> Document:
        pass

    @abstractmethod
    def find_by_zapsign_id(self, zapsign_id: str) -> Document | None:
        pass

    @abstractmethod
    def update_status(self, document: Document, new_status: str):
        pass
