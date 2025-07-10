URL_MONGO_MIGRATION_TEST = "mongodb://admin:admin@localhost:27018/test_db?authSource=admin"
APP_DIR=app

# Criar o diretório venv
build-venv:
	python3.12 -m venv venv

# Instalar os pacotes
requirements-test:
	pip install --upgrade pip
	pip install -r requirements/test.txt

# Verificar o código
check-lint:
	isort -c ${APP_DIR} ${ROOT_TESTS_DIR}
	bandit -c pyproject.toml -r -f custom ${APP_DIR} ${ROOT_TESTS_DIR}
	black --check ${APP_DIR} ${ROOT_TESTS_DIR}
	flake8 --max-line-length=120 ${APP_DIR} ${ROOT_TESTS_DIR}
	mypy ${APP_DIR} ${ROOT_TESTS_DIR}

#Carregar as variáveis de ambiente
load-env:
	@./devtools/scripts/push-env "devtools/dotenv.$(env)"

# Carregar a variável de testes
load-dev-env:
	@env=dev make $(MAKE_ARGS) load-env

# Docker completo de desenvolvimento
docker-run-dev:
	docker-compose -f devtools/docker-compose.yml up --build
docker-run-dev-down:
	docker-compose -f devtools/docker-compose.yml down

# Docker API Catalogo
docker-catalogo-up:
	docker-compose -f devtools/docker-compose-catalogo.yml up --build
docker-catalogo-down:
	docker-compose -f devtools/docker-compose-catalogo.yml down

# Docker IA
docker-ia-up:
	docker-compose -f devtools/docker-compose-ia.yml up --build
docker-ia-down:
	docker-compose -f devtools/docker-compose-ia.yml down

# Docker Redis
docker-redis-up:
	docker-compose -f devtools/docker-compose-redis.yml up --build
docker-redis-down:
	docker-compose -f devtools/docker-compose-redis.yml down

# Docker Keycloak 
docker-tests-keycloak-up:
	docker-compose -f devtools/docker-compose-keycloak.yml up --build
docker-tests-keycloak-down:
	docker-compose -f devtools/docker-compose-keycloak.yml down

# Docker MongoDB
docker-mongo-up:
	docker-compose -f devtools/docker-compose-mongo.yml up --build
docker-mongo-down:
	docker-compose -f devtools/docker-compose-mongo.yml down

# Docker MongoDB Teste
docker-mongo-test-up:
	docker-compose -f devtools/docker-compose-mongo-test.yml up --build
docker-mongo-test-down:
	docker-compose -f devtools/docker-compose-mongo-test.yml down

# Docker SonarQube
docker-sonarqube-up:
	docker-compose -f devtools/docker-compose-sonar.yml up --build
docker-sonarqube-down:
	docker-compose -f devtools/docker-compose-sonar.yml down

# Realizar a migração do banco de dados
migration:
	mongodb-migrate --url "$(URL_MONGO_MIGRATION_TEST)"

# Testar fazendo a cobertura do código
coverage:
	pytest --cov=${APP_DIR} --cov-report=term-missing --cov-report=xml ${ROOT_TESTS_DIR} --cov-fail-under=90 --durations=5


