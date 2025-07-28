from domain.documents.repositories import IDocumentRepository
from infrastructure.persistence.models import Document

class DjangoDocumentRepository(IDocumentRepository):
    def create(self, **data) -> Document:
        return Document.objects.create(**data)

    def find_by_zapsign_id(self, zapsign_id: str) -> Document | None:
        return Document.objects.filter(zapsign_open_id=zapsign_id).first()

    def update_status(self, document: Document, new_status: str):
        document.status = new_status
        document.save(update_fields=['status'])
