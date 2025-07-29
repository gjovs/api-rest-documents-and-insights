import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def test_user(db):
    """Cria um usuário de teste simples no banco de dados."""
    user = User.objects.create_user(username='testuser', password='testpassword123')
    return user

@pytest.fixture
def api_client(test_user):
    """
    Cria e retorna um cliente de API já autenticado como o test_user.
    Isso nos economiza de ter que fazer login em cada teste.
    """
    client = APIClient()
    token_url = reverse('token_obtain_pair')
    response = client.post(token_url, {'username': 'testuser', 'password': 'testpassword123'})
    token = response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client