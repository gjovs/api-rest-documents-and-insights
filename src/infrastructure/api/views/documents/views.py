from dependency_injector.wiring import inject, Provide
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from infrastructure.containers import Container
from infrastructure.persistence.models import Document
from infrastructure.api.serializers import DocumentSerializer
from application.documents import CreateDocumentUseCase


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    @inject
    def create(self, request, create_document_use_case: CreateDocumentUseCase = Provide[Container.create_document_use_case], *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            document = create_document_use_case.execute(
                name=validated_data.get('name'),
                company=validated_data.get('company'),
                user=request.user,
                file_url=validated_data.get('file_url'),
                signers_data=validated_data.get('signers_data')
            )

            if document is None:
                return Response({"error": "Falha na comunicação com o serviço externo."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            response_serializer = self.get_serializer(document)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
