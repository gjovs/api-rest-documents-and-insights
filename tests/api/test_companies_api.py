# backend/tests/api/test_companies_api.py
import pytest
from django.urls import reverse
from infrastructure.persistence.models import Company

pytestmark = pytest.mark.django_db


def test_unauthenticated_user_cannot_list_companies(client):
    url = reverse('company-list')
    response = client.get(url)
    assert response.status_code == 401


def test_authenticated_user_can_crud_company(api_client):
    """Testa o fluxo completo de CRUD para Company."""
    list_url = reverse('company-list')

    # 1. CREATE
    create_data = {'name': 'Nova Empresa', 'api_token': 'token123'}
    response = api_client.post(list_url, data=create_data, format='json')
    assert response.status_code == 201
    assert response.json()['name'] == 'Nova Empresa'
    company_id = response.json()['id']

    # 2. RETRIEVE
    detail_url = reverse('company-detail', kwargs={'pk': company_id})
    response = api_client.get(detail_url)
    assert response.status_code == 200
    assert response.json()['name'] == 'Nova Empresa'

    # 3. LIST (Verifica se está na lista)
    response = api_client.get(list_url)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 4. UPDATE (PATCH)
    update_data = {'name': 'Empresa Atualizada'}
    response = api_client.patch(detail_url, data=update_data, format='json')
    assert response.status_code == 200
    assert response.json()['name'] == 'Empresa Atualizada'

    # 5. DELETE
    response = api_client.delete(detail_url)
    assert response.status_code == 204

    # Verifica se foi deletado
    response = api_client.get(detail_url)
    assert response.status_code == 404
