from domain.documents.services import IZapSignService, IQueueService
from domain.documents.repositories import IDocumentRepository
from domain.signers.repositories import ISignerRepository
from infrastructure.persistence.models import Document, DocumentInsight, Company
from django.contrib.auth.models import User
import os


class CreateDocumentUseCase:
    def __init__(self,
                 zapsign_service: IZapSignService,
                 queue_service: IQueueService,
                 document_repository: IDocumentRepository,
                 signer_repository: ISignerRepository):
        self.zapsign_service = zapsign_service
        self.queue_service = queue_service
        self.document_repository = document_repository


        self.signer_repository = signer_repository

    def execute(self, name: str, company: Company, user: User, file_url: str, signers_data: list) -> Document:
        api_token = company.api_token
        if not api_token:
            raise ValueError("Empresa sem token de API.")

        zapsign_payload = {
            "name": name, "signers": signers_data, "url_pdf": file_url
        }

        zapsign_response = self.zapsign_service.create_document(
            zapsign_payload, api_token)
        if not zapsign_response:
            return None

        document = self.document_repository.create(
            company=company, name=name, created_by=user,
            zapsign_open_id=zapsign_response.get('open_id'),
            zapsign_token=zapsign_response.get('token'), status='sent_to_zapsign'
        )

        response_signers_map = {
            s['email']: s for s in zapsign_response.get('signers', [])}
        signers_to_create = []

        for signer_data in signers_data:
            signer_info = response_signers_map.get(signer_data['email'])
            signer_token = signer_info.get('token') if signer_info else None
            signers_to_create.append(
                {**signer_data, 'zapsign_signer_token': signer_token})

        self.signer_repository.bulk_create_from_list(
            signers_to_create, document)

        DocumentInsight.objects.create(document=document, status='PENDING')

        task_payload = {"doc_id": str(document.id), "file_url": file_url}

        self.queue_service.publish_analysis_task(task_payload)

        return document
