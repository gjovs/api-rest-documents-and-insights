import requests
from domain.documents.services import IZapSignService
from zapsign_project.settings import APIS


class ZapSignService(IZapSignService):
    def create_document(self, payload: dict, api_token: str) -> dict | None:
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {api_token}'}

        url = f"{APIS['ZAP_SIGN']}/api/v1/docs/"

        print(payload);

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao se comunicar com a API da ZapSign: {e}")
            return None
