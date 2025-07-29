from domain.documents.repositories import IDocumentRepository
from domain.signers.repositories import ISignerRepository


class ProcessZapSignWebhookUseCase:
    def __init__(self, doc_repo: IDocumentRepository, signer_repo: ISignerRepository):
        self.doc_repo = doc_repo
        self.signer_repo = signer_repo

    def execute(self, payload: dict):
        event_type = payload.get('event_type')
        if not event_type:
            print("Webhook recebido sem 'event_type'. Ignorando.")
            return

        if event_type == 'doc_signed':
            signer_who_signed = payload.get('signer_who_signed')
            if signer_who_signed and signer_who_signed.get('token'):
                signer_token = signer_who_signed.get('token')
                signer_status = signer_who_signed.get('status', 'signed')
                
                signer_in_db = self.signer_repo.find_by_zapsign_token(signer_token)
                if signer_in_db:
                    self.signer_repo.update_status(signer_in_db, signer_status.upper())
                    
                    print(f"Status do signatário {signer_in_db.id} atualizado para {signer_status.upper()}")

            # 3. Atualiza o status geral do documento
            document_token = payload.get('open_id')
            document_status = payload.get('status')
            if document_token:
                doc_in_db = self.doc_repo.find_by_zapsign_id(document_token)
                if doc_in_db:
                    self.doc_repo.update_status(doc_in_db, document_status.upper())
                    print(f"Status do documento {doc_in_db.id} atualizado para {document_status.upper()}")

