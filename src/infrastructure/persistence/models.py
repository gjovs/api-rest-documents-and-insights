from django.db import models
from django.contrib.auth.models import User
import uuid

from encrypted_model_fields.fields import EncryptedCharField


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    api_token = EncryptedCharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='documents')
    zapsign_open_id = models.CharField(
        max_length=255, blank=True, null=True)
    zapsign_token = models.CharField(
        max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='draft')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Signer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='signers')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    # O token aqui se refere ao 'signer_token' específico para o signatário no documento
    zapsign_signer_token = models.CharField(
        max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"{self.name} ({self.email})"


class DocumentInsight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, related_name='insight')
    content = models.JSONField(null=True, blank=True)
    # PENDING, PROCESSING, COMPLETED, FAILED
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insights for {self.document.name}"
