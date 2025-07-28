from dependency_injector.wiring import inject, Provide
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from infrastructure.containers import Container
from application.webhooks import ProcessZapSignWebhookUseCase


class ZapSignWebhookView(APIView):
    # parser_classes = [JSONParser]
    permission_classes = [AllowAny]

    @inject
    def post(self,
             request,
             use_case: ProcessZapSignWebhookUseCase = Provide[
                 Container.process_zapsign_webhook_use_case],
             *args, **kwargs):

        use_case.execute(payload=request.data)
        
        return Response(status=200)
