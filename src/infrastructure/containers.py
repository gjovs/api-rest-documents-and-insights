
from dependency_injector import containers, providers
from infrastructure.persistence.documents import DjangoDocumentRepository
from infrastructure.persistence.signers import DjangoSignerRepository

from application.documents import CreateDocumentUseCase
from application.signers import GetSignerSigningUrlUseCase
from application.webhooks import ProcessZapSignWebhookUseCase

from infrastructure.services.zap_sign import ZapSignService
from infrastructure.queue.redis_service import RedisQueueService


class Container(containers.DeclarativeContainer):
    """
    Container de Injeção de Dependência para o projeto.

    Ele centraliza a criação de instâncias de serviços e casos de uso.
    """

    document_repository = providers.Factory(DjangoDocumentRepository)
    signer_repository = providers.Factory(DjangoSignerRepository)

    zapsign_service = providers.Factory(
        ZapSignService
    )

    queue_service = providers.Factory(
        RedisQueueService
    )

    create_document_use_case = providers.Factory(
        CreateDocumentUseCase,
        zapsign_service=zapsign_service,
        queue_service=queue_service,
        document_repository=document_repository,
        signer_repository=signer_repository
    )
    get_signer_signing_url_use_case = providers.Factory(
        GetSignerSigningUrlUseCase,
        repository=signer_repository
    )
    process_zapsign_webhook_use_case = providers.Factory(
        ProcessZapSignWebhookUseCase,
        doc_repo=document_repository,
        signer_repo=signer_repository
    )
