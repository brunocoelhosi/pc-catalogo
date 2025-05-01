<div align="center">
  <h1>📦 Catálogo de Produtos📦 </h1>
  
</div>

## Introdução

O projeto tem como objetivo **descrever os produtos**, considerando suas características e especificações detalhadas. As informações são obtidas por meio de pesquisas em **diversos sites de e-commerce**, permitindo uma visão ampla e comparativa de cada item. Isso facilita a **organização, comparação e apresentação** dos produtos de forma clara e padronizada.

---

## 🎯 Para que Serve um Catálogo de Produtos?

| Benefício                         | Descrição                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| **📁 Organização e Apresentação** | Exibe os produtos de forma estruturada, facilitando a busca e a comparação.        |
| **📑 Informações Detalhadas**     | Inclui descrição completa, fotos, preço e especificações técnicas dos produtos.    |
| **🛒 Facilitação da Compra**      | Auxilia os compradores a encontrarem o que procuram e tomarem decisões informadas. |
| **💼 Ferramenta de Vendas**       | Ajuda os vendedores a apresentarem seus produtos de forma profissional e atrativa. |

---

## 🏆 Equipe Responsável

### 👤Integrantes do Projeto

- **Bruno Coelho Lopes**
- **Carlos Eduardo Lima**
- **Isabella Ramos Carvalho**
- **João Pedro Pereira Porfírio**

##

## 📄 Documentação

<!-- Colar o design docs da sua aplicação no link abaixo -->

Você pode encontrar a documentação completa referente a este projeto neste [design docs](substituir com o link do seu design doc)

## 💻 Tecnologias

Este projeto foi construído usando várias tecnologias chaves para garantir performance, segurança e facilidade de uso:

- **Python 3.12**: Escolhido por sua simplicidade e poderosas capacidades de programação. A versão 3.13 é a mais recente, oferecendo melhorias significativas em eficiência e recursos linguísticos.
- **FastAPI**: Uma moderna e rápida (altas performances) web framework para Python, que é ideal para a construção de APIs.

## ✨ Configuração do ambiente local

Este projeto foi desenvolvivo utilizando o [Python 3.12](https://docs.python.org/3.12/), confirme se o mesmo está instalado em sua máquina.

Comandos via Linux 🐧.

Clone o projeto, acesse o diretório:

```sh
cd pc-catalogo
```

Crie o [ambiente virtual](https://docs.python.org/3.12/tutorial/venv.html)
para instalar as bibliotecas e trabalharmos com o projeto:

```sh
make build-venv
```

Uma vez criado o ambiente virtual do Python, você precisa ativá-lo
(estou supondo que você está no Linux 🐧):

```sh
./venv/bin/activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias para o seu projeto, veja com a equipe qual é a URL do [pypi](https://pypi.org/) do Magalu e defina o seu valor para `PIP_LUIZALABS_URL`. Execute os comandos:

```sh
# Definindo a PIP do Magalu
export PIP_LUIZALABS_URL=<pega com alguém 😉>
# Verifique se sua PIP foi gerada
echo $PIP_LUIZALABS_URL
# Instala os pacotes.
make requirements-dev
# OU instale sem o makefile:
# pip install -i $PIP_URL -r requirements/develop.txt
# Instala configurações do pre-commit
make install-pre-commit
```

Comandos via Windows 🗔.

Este projeto foi desenvolvivo utilizando o [Python 3.12](https://docs.python.org/3.12/), confirme se o mesmo está instalado em sua máquina.

Clone o projeto, acesse o diretório:

```sh
cd pc-catalogo
```

Crie o [ambiente virtual](https://docs.python.org/3.12/tutorial/venv.html)
para instalar as bibliotecas e trabalharmos com o projeto:

```sh
python3.12 -m venv venv
```

Uma vez criado o ambiente virtual do Python, você precisa ativá-lo
(estou supondo que você está no Linux 🐧):

```sh
source ./venv/bin/activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias para o seu projeto, veja com a equipe qual é a URL do [pypi](https://pypi.org/) do Magalu e defina o seu valor para `PIP_LUIZALABS_URL`. Execute os comandos:

```sh
# Instala os pacotes.
pip install -r requirementes.txt
```

Para se gerar novos commits, favor seguir o padrão do https://commitlint.io/

## ▶️ Execução

Configure o arquivo de env, execute o script no bash:

```bash
./devtools/scripts/push-env devtools/dotenv.dev
```

Use o comando para subir a api:

```bash
uvicorn app.api_main:app --reload
```

Acesse a doc da API em: [localhost:8000/api/docs](http://0.0.0.0:8000/api/docs) ou em [localhost:8000/redoc](http://0.0.0.0:8000/redoc)

Para rodar os workers configurados no .env:

## Contribuições e Atualizações

O projeto está aberto a contribuições e atualizações da comunidade. O processo para contribuições é o seguinte:

- **Pull Requests**: Contribuições devem ser submetidas como pull requests.
- **Code Review**: Cada pull request passará por um code review detalhado pela equipe. Isso garante que o código esteja alinhado com os padrões de qualidade e funcionamento do projeto.
- **Incorporação de Mudanças**: Após a aprovação no code review, as mudanças serão integradas ao código principal.

## 📖 Recursos úteis

- [Conventional Commits](https://www.conventionalcommits.org)

## 👍 Merge Requests

- Fluxo de desenvolvimento e entrega contínua documentado no Kanban.
