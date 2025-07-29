# backend/Dockerfile

# Usa uma imagem base leve do Python
FROM python:3.15-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Configura variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia apenas o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta em que o Gunicorn irá rodar
EXPOSE 8000

# O comando para iniciar o servidor de produção Gunicorn quando o contêiner iniciar
CMD ["gunicorn", "zapsign_project.wsgi:application", "--bind", "0.0.0.0:8000"]