from rest_framework import serializers
from ..persistence.models import Company, Document, Signer, DocumentInsight


class SignerInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = '__all__'


class DocumentInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentInsight
        fields = ['status', 'content', 'updated_at', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    signers = SignerSerializer(many=True, read_only=True)
    insight = DocumentInsightSerializer(read_only=True)

    file_url = serializers.URLField(write_only=True, required=True)
    signers_data = SignerInputSerializer(
        many=True, write_only=True, required=True)

    class Meta:
        model = Document
        fields = list(f.name for f in Document._meta.get_fields()
                      ) + ['file_url', 'signers_data', 'insight']
        read_only_fields = ['zapsign_open_id',
                            'zapsign_token', 'status', 'created_by']
        extra_kwargs = {
            'company': {'write_only': True},
            'created_by': {'read_only': True}
        }
        


class CompanySerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['created_at', 'last_updated_at']
        extra_kwargs = {
            'api_token': {'write_only': True}
        }
