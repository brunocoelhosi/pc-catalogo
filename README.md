<div align="center">
  <h1>📦 Catálogo de Produtos📦 </h1>
</div>

## Introdução

O projeto tem como objetivo **fornecer as informações dos produtos** presentes no catálogo, considerando suas características e especificações detalhadas..

## 🎯 Para que Serve um Catálogo de Produtos?

| Benefício                         | Descrição                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| **📁 Organização e Apresentação** | Exibe os produtos de forma estruturada, facilitando a busca e a comparação.        |
| **📑 Informações Detalhadas**     | Inclui descrição completa, fotos, preço e especificações técnicas dos produtos.    |
| **🛒 Facilitação da Compra**      | Auxilia os compradores a encontrarem o que procuram e tomarem decisões informadas. |
| **💼 Ferramenta de Vendas**       | Ajuda os vendedores a apresentarem seus produtos de forma profissional e atrativa. |

## 🏆 Equipe Responsável

### 👤Integrantes do Projeto

- **Bruno Coelho Lopes**
- **Carlos Eduardo Lima**
- **Isabella Ramos Carvalho**
- **João Pedro Pereira Porfírio**

## 💻 Tecnologias

Este projeto foi construído usando várias tecnologias chaves para garantir performance, segurança e facilidade de uso:

- **Linguagem**: [Python 3.12](https://docs.python.org/3.12/) - Escolhido por sua simplicidade e poderosas capacidades de programação. A versão 3.13 é a mais recente, oferecendo melhorias
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Uma moderna e rápida (altas performances) web framework para Python, que é ideal para a construção de APIs.
- **Documentação da API**: [Swagger](https://swagger.io/) (via FastAPI)
- **Banco de Dados**: [MongoDB](https://www.mongodb.com/)
- **Orquestração**: [Docker](https://www.docker.com/) / [Docker-compose](https://docs.docker.com/compose/)
- **Testes**: [Pytest](https://docs.pytest.org/)
- **Code Quality**: [SonarQube](https://www.sonarsource.com/products/sonarqube/)
- **Cache dos dados**: [Redis](https://redis.io/)
- **Makefile**: Automação de tarefas
- **Autenticação**: Keycloak (OpenID Connect)
- **Gerenciamento de dependências**: requirements.txt (com separação por ambiente)
- **Migração de dados**: mongodb-migrations
- **Modelo de IA**: [Ollama Phi3-mini](https://ollama.com/library/phi3:mini)
- **Front-End Integration**: [Streamlit](https://streamlit.io/)

## 📁 Estrutura do projeto

```bash
📁 pc-catalogo/
├── 📁 app/                       # Código-fonte principal da aplicação
│   ├── 📁 api/                   # Camada de apresentação (FastAPI)
│   │   ├── 📁 common/            # Recursos compartilhados (auth, trace, handlers)
│   │   ├── 📁 middlewares/       # Middlewares globais (CORS, trace, etc.)
│   │   ├── 📁 v1/                # API versão 1 (dados em memória)
│   │   └── 📁 v2/                # API versão 2 (MongoDB + IA)
│   ├── 📁 common/                # Utilitários e funções auxiliares
│   ├── 📁 integrations/          # Integrações externas (Keycloak, Redis, MongoDB)
│   ├── 📁 models/                # Modelos de dados utilizados na aplicação
│   ├── 📁 repositories/          # Camada de acesso a dados (repositórios)
│   ├── 📁 services/              # Lógica de negócio e regras da aplicação
│   ├── 📁 settings/              # Configurações da aplicação (env, API, worker)
│   └── 📁 worker/                # Tarefas assíncronas e workers de background
├── 📁 devtools/                  # Ferramentas auxiliares para desenvolvimento
│   ├── 📁 api/                   # Testes manuais com arquivos .http
│   └── 📁 scripts/               # Scripts de automação e utilitários
├── 📁 tests/                     # Testes automatizados do projeto
│   ├── 📁 unit/                  # Testes unitários
│   └── 📁 integration/           # Testes de integração entre módulos
├── 📁 venv/                      # Ambiente virtual Python (não versionado)
├── 📄 .env                       # Arquivo de variáveis de ambiente
├── 📄 Dockerfile                 # Imagem Docker para a aplicação
├── 📄 Makefile                   # Comandos utilitários para desenvolvimento
├── 📄 requirements.txt           # Lista de dependências Python
└── 📄 README.md                  # Documentação principal do projeto
```

## ✨ Configuração do ambiente local

Confirme se o [Python 3.12](https://docs.python.org/3.12/) está instalado em sua máquina.

#

### 🐧 Comandos via Linux .

Clone o projeto e acesse o diretório:

```sh
https://github.com/projeto-carreira-luizalabs-2025/pc-catalogo.git
```

```sh
cd pc-catalogo
```

Crie o [ambiente virtual](https://docs.python.org/3.12/tutorial/venv.html)
para instalar as bibliotecas e trabalharmos com o projeto:

```sh
make build-venv
```

Uma vez criado o ambiente virtual do Python, você precisa ativá-lo:

```sh
source ./venv/bin/activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias para o seu projeto. Execute os comandos:

```sh
# Instala os pacotes.
make requirements-test
```

## 🐳 Execução com Docker

#### API, Banco MongoDB, IA, Redis e Keycloak

Gere um token do [GitHub](https://github.com/settings/tokens), crie um arquivo `.env` dentro da pasta `devtools` e cole seu token.

```bash
GITHUB_TOKEN=<SEU_TOKEN>
```

###### Obs.: Token necessário para instalação da [Biblioteca pc-logging](https://github.com/projeto-carreira-luizalabs-2025/pc-logging)

🟢 Subir o Docker IA

```bash
make docker-run-dev
# Esse comando sobe os Dockers (API, Banco, IA, Redis e Keycloak )
```

🛑 Parar e remover container

```bash
make docker-dev-down
```

#

### 🗔 Comandos via Windows .

Este projeto foi desenvolvido utilizando o [Python 3.12](https://docs.python.org/3.12/), confirme se o mesmo está instalado em sua máquina.

Clone o projeto e acesse o diretório:

```sh
https://github.com/projeto-carreira-luizalabs-2025/pc-catalogo.git
```

```sh
cd pc-catalogo
```

Crie o [ambiente virtual](https://docs.python.org/3.12/tutorial/venv.html)
para instalar as bibliotecas e trabalharmos com o projeto:

```sh
# Cria o ambiente virtual.
python3.12 -m venv venv
```

Uma vez criado o ambiente virtual do Python, você precisa ativá-lo:

```sh
# Ativa o ambiente virtual.
venv\Scripts\activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias para o seu projeto. Execute os comandos:

```sh
# Instala os pacotes.
pip install -r requirements.txt
```

Para novos commits, siga o padrão do https://commitlint.io/

##

## ▶️ Execução da API localmente

Configure o arquivo de env:

Crie o arquivo `.env` na pasta raiz do projeto com o seguinte conteúdo:

```bash
ENV=dev
```

ou execute o seguinte script na pasta raiz do projeto com o Git Bash:

```bash
./devtools/scripts/push-env devtools/dotenv.dev
```

Use o comando para subir a API:

```sh
uvicorn app.api_main:app --reload
```

##

## 🐳 Execução da API, Banco MongoDB, IA, Redis e Keycloak usando Docker

Gere um token do [GitHub](https://github.com/settings/tokens), crie um arquivo `.env` dentro da pasta `devtools` e cole seu token.

```bash
GITHUB_TOKEN=<SEU_TOKEN>
```

###### Obs.: Token necessário para instalação da [Biblioteca pc-logging](https://github.com/projeto-carreira-luizalabs-2025/pc-logging)

Na raiz do projeto, execute o comando:

🟢 Subir o pack de Dockers

```sh
docker-compose -f devtools/docker-compose.yml up --build
# Esse comando sobe os dockers (API, Banco, IA, Redis e Keycloak)
```

🛑 Parar e remover container

```bash
docker-compose -f devtools/docker-compose.yml down
```

#### Obs.: Para subir os dockers separadamente, os comandos estão presente no Makefile

#

## 🔑 Configurações do Keycloak

Após o Docker do Keycloak estar rodando, execute o seguinte comando para realizar as configurações necessárias dos usuários pré-cadastrados

```sh
python ./devtools/keycloak-config/setup_sellers_attribute.py
```

### Autorização no Swagger

Para realizar a autorização diretamente no swagger e poder testar os endpoints protegidos, siga os passos:

Acesse: [Localhost](http://localhost:8000/api/docs#/)

Authorize 🔒

Usuário para testes:

- username: vendedorcatalogo
- password: senha123
- client_id: varejo

## 🗃️ Migração do Banco de dados

Para migração do MongoDB, instalamos a biblioteca mongodb-migrations.

```sh
pip install mongodb-migrations==1.3.1
```

Criamos o arquivo no formato <DATA>\_<TEXTO>.py na pasta migrations, exemplo: 20250101102030_somethingindexes.py.

Fazemos a migração:

```sh
mongodb-migrate --url "$APP_DB_URL_MONGO"
```

Sendo que a variável "APP_DB_URL_MONGO" contém a URL de conexão com o MongoDB.

##

## ⚙️ Execução dos Containers separadamente

#### Todos os comandos devem ser executados na raiz do projeto

### Linux

#### 🟢 API

```bash
make docker-catalogo-up
```

#### 🟢 IA

```bash
make docker-ia-up
```

#### 🟢 Keycloak

```bash
make docker-tests-keycloak-up
```

#### 🟢 Redis

```bash
make docker-redis-up
```

#### 🟢 MongoDB Teste

```bash
make docker-mongo-test-up
```

### Windows

#### 🟢 API Catálogo

Gere um token do [GitHub](https://github.com/settings/tokens), crie um arquivo `.env` dentro da pasta `devtools` e cole seu token

```bash
GITHUB_TOKEN=<SEU_TOKEN>
```

```sh
docker-compose -f devtools/docker-compose-catalogo.yml up --build
```

API: http://localhost:8000

#### 🟢 Banco MongoDB

```sh
docker-compose -f devtools/docker-compose-mongo.yml up --build
```

#### 🟢 IA Ollama PHI3

```sh
docker-compose -f devtools/docker-compose-ia.yml up --build
```

#### 🟢 Keycloak

```sh
docker-compose -f devtools/docker-compose-keycloak.yml up --build
```

#### 🟢 Redis

```sh
docker-compose -f devtools/docker-compose-redis.yml up --build
```

##

## ▶️ SonarQuve para análise do projeto

```
docker-compose -f devtools/docker-compose-sonar.yml up --build
```

SonarQube: http://localhost:9000 (usuário padrão: admin, senha: admin)

##

### 🔎 Análise com SonarQuve

#### 1. Gere e exporte o token do SonarQube

Após acessar o SonarQube:

- **Vá em "My Account" > "Security".**

- **Gere um novo token (ex: catalogo).**

- **Em outro terminal, vá ate a raiz do projeto execute o seguinte comando para executar o Sonar-scanner**

#### Windows

```
set SONAR_TOKEN=<seu_token_aqui>
```

```
set SONAR_HOST_URL=http://localhost:9000
```

```
sonar-scanner -Dsonar.login=%SONAR_TOKEN% -Dsonar.host.url=%SONAR_HOST_URL%
```

#### Linux

```
export SONAR_TOKEN=<seu_token_aqui>
```

```
SONAR_HOST_URL=http://localhost:9000 pysonar-scanner
```

Isso irá enviar os dados da sua aplicação para análise no SonarQube.

##

## 📊 Cobertura de Código com pytest-cov

A cobertura de código é uma métrica que indica a porcentagem do seu código-fonte que foi executada durante a execução da sua suíte de testes. Ela ajuda a identificar partes do seu código que não estão sendo testadas e que, portanto, podem conter bugs ocultos.

### 📂 Estrutura dos testes

```bash
tests/
└── unit/         # Testes unitários do service, model e repository
└── integration/  # Testes de integração da API
└── fixture/      # Fixtures
└── conftest.py   # Fixtures globais do pytest
```

### Medindo a Cobertura com pytest-cov

O pytest-cov é um plugin para o pytest que integra a medição de cobertura de forma muito simples.

#### Instalação:

```
pip install pytest-cov
```

#### Executando Testes com Cobertura:

Para executar seus testes e gerar um relatório de cobertura no terminal, use a flag `--cov`:

```bash
pytest --cov=app
# Windows
```

```bash
make coverage
# Linux
```

### Gerando Relatórios Detalhados:

Para uma análise mais aprofundada, você pode gerar relatórios em formatos diferentes:

- Relatório HTML: Cria um HTML para navegar pelos seus arquivos e ver exatamente quais linhas foram ou não cobertas.

```
pytest --cov=app --cov-report=html
```

Isso criará um diretório htmlcov. Abra o arquivo index.html em seu navegador.

- Relatório XML: Este formato é muito útil para integração com ferramentas de análise de qualidade de código, como o SonarQube.

```
pytest --cov=app --cov-report=xml
```

Isso criará um arquivo coverage.xml no seu diretório.

## Contribuições e Atualizações

O projeto está aberto a contribuições e atualizações da comunidade. O processo para contribuições é o seguinte:

- **Pull Requests**: Contribuições devem ser submetidas como pull requests.
- **Code Review**: Cada pull request passará por um code review detalhado pela equipe. Isso garante que o código esteja alinhado com os padrões de qualidade e funcionamento do projeto.
- **Incorporação de Mudanças**: Após a aprovação no code review, as mudanças serão integradas ao código principal.

## 📖 Recursos úteis

- [Conventional Commits](https://www.conventionalcommits.org)

## 👍 Merge Requests

- Fluxo de desenvolvimento e entrega contínua documentado no Kanban.
