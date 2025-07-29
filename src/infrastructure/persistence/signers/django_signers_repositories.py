from typing import List
from domain.signers.repositories import ISignerRepository
from infrastructure.persistence.models import Signer, Document


class DjangoSignerRepository(ISignerRepository):
    def get_by_id(self, signer_id: str) -> Signer | None:
        return Signer.objects.filter(id=signer_id).first()

    def bulk_create_from_list(self, signers_list: List[dict], document: Document):
        signers_to_create = [Signer(document=document, **data)
                             for data in signers_list]
        Signer.objects.bulk_create(signers_to_create)

    def find_by_zapsign_token(self, zapsign_token: str) -> Signer | None:
        return Signer.objects.filter(zapsign_signer_token=zapsign_token).first()

    def update_status(self, signer: Signer, new_status: str):
        signer.status = new_status
        signer.save(update_fields=['status'])
