# Makefile para facilitar o desenvolvimento local do serviço de API (Backend).

PYTHON = python

.DEFAULT_GOAL := help

# --- Comandos Principais ---

.PHONY: help setup install venv run migrate clean
help: ## Mostra esta mensagem de ajuda com todos os comandos disponíveis.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: install ## (Comando principal) Prepara o ambiente completo do backend.
	@echo "\nAmbiente do Backend pronto!"
	@echo "Use 'make run' para iniciar o servidor ou 'make migrate' para rodar migrações."

venv: ## Cria o ambiente virtual, se não existir.
	@if [ ! -d "venv" ]; then \
		echo "Criando ambiente virtual para o Backend..."; \
		$(PYTHON) -m venv venv; \
	else \
		echo "Ambiente virtual já existe."; \
	fi

install: venv ## Instala as dependências Python para o backend.
	@echo "Instalando dependências do Backend..."
	@. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run: ## Inicia o servidor de desenvolvimento do Django.
	@echo "Iniciando servidor do Backend em http://127.0.0.1:8000/ ..."
	@. venv/bin/activate && $(PYTHON) src/manage.py runserver

migrate: ## Aplica as migrações do banco de dados para o backend.
	@echo "Aplicando migrações do Backend..."
	@. venv/bin/activate && $(PYTHON) src/manage.py migrate

clean: ## Remove o ambiente virtual e arquivos de cache.
	@echo "Limpando ambiente virtual e arquivos de cache do Backend..."
	@rm -rf venv
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Limpeza concluída."

	
test: ## Roda a suíte de testes do Pytest.
	@echo "Rodando testes do Backend..."
	@. venv/bin/activate && pytest

.PHONY: freeze
freeze: venv ## Atualiza o requirements.txt com as dependências do ambiente virtual.
	@echo "Gerando requirements.txt para o Backend..."
	@. venv/bin/activate && pip freeze > requirements.txt