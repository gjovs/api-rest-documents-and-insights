from abc import ABC, abstractmethod

class IZapSignService(ABC):
    @abstractmethod
    def create_document(self, payload: dict, api_token: str) -> dict:
        """Contrato para criar um documento em um serviço externo."""
        pass

class IQueueService(ABC):
    @abstractmethod
    def publish_analysis_task(self, task_payload: dict):
        """Contrato para publicar uma tarefa de análise em uma fila."""
        pass