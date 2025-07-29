from domain.signers.repositories import ISignerRepository

from zapsign_project.settings import APIS

ZAPSIGN_API_URL = APIS['ZAP_SIGN_APP']


class GetSignerSigningUrlUseCase:
    def __init__(self, repository: ISignerRepository):
        self.repository = repository

    def execute(self, signer_id: str) -> str | None:
        signer = self.repository.get_by_id(signer_id)
        if not signer or not signer.zapsign_signer_token:
            return None
        return f"{ZAPSIGN_API_URL}/verificar/{signer.zapsign_signer_token}"


