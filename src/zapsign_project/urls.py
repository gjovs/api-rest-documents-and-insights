from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from infrastructure.api.views import document_stream_view
from infrastructure.api.views.webhooks import ZapSignWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    # API principal (que ainda vamos criar)
    path('api/v1/', include('infrastructure.api.urls')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    path('api/v1/webhooks/zapsign/',
         ZapSignWebhookView.as_view(), name='zapsign-webhook'),

    path('api/v1/documents/<uuid:document_id>/insights/stream/',
         document_stream_view, name='document-stream'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),



]
