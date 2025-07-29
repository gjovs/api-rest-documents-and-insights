from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, DocumentViewSet, SignerViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'signers', SignerViewSet, basename='signer')

urlpatterns = [
    path('', include(router.urls)),
]
CompanyViewSet