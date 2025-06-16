<div align="center">
  <h1>📦 Catálogo de Produtos📦 </h1>
</div>

## Introdução

O projeto tem como objetivo **descrever os produtos**, considerando suas características e especificações detalhadas. As informações são obtidas por meio de pesquisas em **diversos sites de e-commerce**, permitindo uma visão ampla e comparativa de cada item. Isso facilita a **organização, comparação e apresentação** dos produtos de forma clara e padronizada.

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

- **Python 3.12**: Escolhido por sua simplicidade e poderosas capacidades de programação. A versão 3.13 é a mais recente, oferecendo melhorias significativas em eficiência e recursos linguísticos.
- **FastAPI**: Uma moderna e rápida (altas performances) web framework para Python, que é ideal para a construção de APIs.

## ✨ Configuração do ambiente local

Confirme se o [Python 3.12](https://docs.python.org/3.12/) está instalado em sua máquina.

#

### 🐧 Comandos via Linux .

Clone o projeto, acesse o diretório:

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
./venv/bin/activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias para o seu projeto. Execute os comandos:

```sh
# Instala os pacotes.
make requirements-dev
```

#

### 🗔 Comandos via Windows .

Este projeto foi desenvolvido utilizando o [Python 3.12](https://docs.python.org/3.12/), confirme se o mesmo está instalado em sua máquina.

Clone o projeto, acesse o diretório:

```sh
# Clona o projeto.
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

Na raiz do projeto, execute o comando:

```sh
docker-compose -f devtools/docker-compose-catalogo.yml up --build
```

API: http://localhost:8000

##

### ▶️ Execução do Banco MongoDB usando Docker-compose

Na raiz do projeto, execute o comando:

```sh
docker-compose -f devtools/docker-compose-mongo.yml up --build
```

##

## ✨ Configuração ambiente de Testes

### ▶️ Execução do Banco MongoDB-test usando Docker-compose

Na raiz do projeto, execute o comando:

```sh
docker-compose -f devtools/docker-compose-mongo-tests.yml up --build
```

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
