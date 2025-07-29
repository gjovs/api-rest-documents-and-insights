from django.apps import AppConfig


class InfrastructureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infrastructure'

    def ready(self):
        from . import containers

        container = containers.Container()
        container.wire(modules=[
            "infrastructure.api.views.documents.views",
            "infrastructure.api.views.signers.views",
            "infrastructure.api.views.company.views",
            "infrastructure.api.views.webhooks.views",
        ])
