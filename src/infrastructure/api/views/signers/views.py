from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from infrastructure.api.serializers import SignerSerializer
from infrastructure.persistence.models import Signer

from dependency_injector.wiring import inject, Provide
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from infrastructure.containers import Container
from application.signers import GetSignerSigningUrlUseCase


class SignerViewSet(viewsets.ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = SignerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='start-signing-process')
    @inject
    def start_signing_process(
        self,
        request,
        pk=None,
        use_case: GetSignerSigningUrlUseCase = Provide[Container.get_signer_signing_url_use_case]
    ):
        """
        Inicia o processo de assinatura para um signatário, retornando sua URL única.
        """
        signing_url = use_case.execute(signer_id=pk)

        if not signing_url:
            return Response(
                {"error": "Signatário não encontrado ou token de assinatura indisponível."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({"signing_url": signing_url}, status=status.HTTP_200_OK)
