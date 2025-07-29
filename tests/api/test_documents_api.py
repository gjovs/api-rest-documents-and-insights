# backend/tests/api/test_documents_api.py
import pytest
from django.urls import reverse
from infrastructure.persistence.models import Company, Document
from unittest.mock import Mock
import uuid

pytestmark = pytest.mark.django_db

@pytest.fixture
def company(db):
    return Company.objects.create(name="Empresa para Documentos", api_token="fake_token")

def test_create_document_with_mocks(api_client, company, mocker):
    """
    Testa a criação de um documento, mockando as classes de serviço
    no momento em que a view as importa.
    """
    # 1. Mock da classe ZapSignService onde a view a utiliza
    mock_zapsign_class = mocker.patch('infrastructure.services.zap_sign.zap_sign_client.ZapSignService')
    mock_zapsign_instance = mock_zapsign_class.return_value
    mock_zapsign_instance.create_document.return_value = {
        'open_id': '123',
        'token': str(uuid.uuid4()),
        'signers': []
    }

    # 2. Mock da classe RedisQueueService onde a view a utiliza
    mock_redis_class = mocker.patch('infrastructure.queue.redis_service.RedisQueueService')
    mock_redis_instance = mock_redis_class.return_value

    # 3. Prepara os dados da requisição
    url = reverse('document-list')
    doc_data = {
        "name": "Contrato de Teste",
        "company": str(company.id),
        "file_url": "http://example.com/doc.pdf",
        "signers_data": [{"name": "Signatário Mock", "email": "mock@email.com"}]
    }

    # 4. Faz a requisição
    response = api_client.post(url, data=doc_data, format='json')

    # 5. Verifica os resultados
    assert response.status_code == 201, f"A criação falhou: {response.data}"
    
    # Verifica se as classes foram instanciadas e os métodos chamados
    mock_zapsign_class.assert_called_once()
    mock_zapsign_instance.create_document.assert_called_once()
    mock_redis_class.assert_called_once()
    mock_redis_instance.publish_analysis_task.assert_called_once()