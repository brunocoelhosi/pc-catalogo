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
- **Documentação da API**: Swagger (via FastAPI)
- **Banco de Dados**: [MongoDB](https://www.mongodb.com/)
- **Docker**: [Docker](https://www.docker.com/)
- **Testes**: [Pytest](https://docs.pytest.org/)
- **Code Quality**: [SonarQube](https://www.sonarsource.com/products/sonarqube/)
- **Makefile**: Automação de tarefas

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
make requirements-dev
```

## 🛠️ Execução local

Para rodar a aplicação localmente execute os os seguintes comandos:

Carregue as variáveis de ambiente para o modo de teste:

```sh
make load-test-env
```

Inicie a API em modo desenvolvimento:

```bash
make run-dev
```

## 🐳 Execução com Docker

🟢 Subir o Docker

```bash
make docker-tests-up # Esse comando sobe o docker da aplicação + docker do banco para testes
```

🛑 Parar e remover container

```bash
make docker-compose-down
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

### ▶️ Execução da API usando Docker

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

### ▶️ Execução da API usando Docker-compose

🟢 Suba o container com o seguinte comando na raiz do projeto:

```sh
docker-compose -f devtools/docker-compose-catalogo.yml up --build
```

🛑 Parar e remover o container

```sh
docker-compose -f devtools/docker-compose-catalogo.yml down
```

API: http://localhost:8000

##

### ▶️ Execução do Banco MongoDB usando Docker-compose

🟢 Suba o container do banco com o seguinte comando na raiz do projeto:

```sh
docker-compose -f devtools/docker-compose-mongo.yml up --build
```

🛑 Parar e remover o container

```sh
docker-compose -f devtools/docker-compose-mongo.yml down
```

##

## ✨ Configuração ambiente de Testes

### ▶️ Execução da API e Banco MongoDB no modo Teste usando Docker-compose

Na raiz do projeto, execute o comando:

```sh
docker-compose -f devtools/docker-compose-tests.yml up --build
```

### 🗃️ Migração do Banco de dados

Para migração do MongoDB, instalamos a biblioteca mongodb-migrations.

```sh
pip install mongodb-migrations==1.3.1
```

Criamos o arquivo no formato <DATA>\_<TEXTO>.py na pasta migrations, exemplo: 20250101102030_somethingindexes.py.

Fizemos a migração:

```sh
mongodb-migrate --url "$APP_DB_URL_MONGO"
```

Sendo que a variável "APP_DB_URL_MONGO" contém a URL de conexão com o MongoDB.

##

### ▶️ Execução SonarQuve para análise do projeto

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

### 📊 Cobertura de Código com pytest-cov

A cobertura de código é uma métrica que indica a porcentagem do seu código-fonte que foi executada durante a execução da sua suíte de testes. Ela ajuda a identificar partes do seu código que não estão sendo testadas e que, portanto, podem conter bugs ocultos.

### Medindo a Cobertura com pytest-cov

O pytest-cov é um plugin para o pytest que integra a medição de cobertura de forma muito simples.

#### Instalação:

```
pip install pytest-cov
```

#### Executando Testes com Cobertura:

Para executar seus testes e gerar um relatório de cobertura no terminal, use a flag `--cov`:

```
pytest --cov=app
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
