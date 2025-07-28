# backend/tests/api/test_webhooks_api.py
import pytest
from django.urls import reverse
from infrastructure.persistence.models import Company, Document, Signer
import json

pytestmark = pytest.mark.django_db

# Fixture para criar uma configuração base de Documento e Signatário
@pytest.fixture
def doc_and_signer(db):
    company = Company.objects.create(name="Empresa Webhook")
    doc = Document.objects.create(
        name="Doc para Webhook",
        zapsign_token="doc-token-123",
        company=company
    )
    signer = Signer.objects.create(
        document=doc,
        name="Signer Webhook",
        zapsign_signer_token="signer-token-456"
    )
    return doc, signer

def test_webhook_updates_status(client, doc_and_signer):
    """
    Testa se o webhook da ZapSign atualiza o status do documento e do signatário.
    """
    doc, signer = doc_and_signer

    # Garante que o status inicial seja o padrão
    assert doc.status == "draft"
    assert signer.status == "pending"
    
    webhook_payload = {
        "event_type": "doc_signed",
        "token": "doc-token-123", # Token do Documento
        "status": "signed",
        "signer_who_signed": {
            "token": "signer-token-456", # Token do Signatário
            "status": "signed"
        }
    }

    url = reverse('zapsign-webhook')
    response = client.post(
        url,
        data=json.dumps(webhook_payload),
        content_type='application/json'
    )
    
    assert response.status_code == 200

    # Pega os objetos atualizados do banco de dados
    doc.refresh_from_db()
    signer.refresh_from_db()

    # Verifica se os status foram alterados
    assert doc.status.upper() == "SIGNED"
    assert signer.status.upper() == "SIGNED"