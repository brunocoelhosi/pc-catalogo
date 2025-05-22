# Primeira etapa: instalar os pacotes do Python
# Montar a estrutura de arquivos da aplicação
FROM python:3.12-slim as construtor

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY requirements.txt .
COPY requirements/ ./requirements/

RUN pip install --upgrade pip && pip install -r requirements/base.txt

# Instalar meus pacotes
RUN python -m venv venv && \
  .  venv/bin/activate && \
  pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Imagem final a ser entregue / conterá a minha aplicação
FROM python:3.12-slim

WORKDIR /projeto
COPY --from=construtor /app/venv /app/venv
COPY app /projeto/app
COPY requirements.txt /app

RUN python -m compileall app

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api_main:app", "--host", "0.0.0.0", "--port", "8000"]