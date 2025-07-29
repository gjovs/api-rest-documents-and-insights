from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from infrastructure.api.serializers import CompanySerializer
from infrastructure.persistence.models import Company


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
