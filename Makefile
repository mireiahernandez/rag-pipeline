# quality check
lint:
	flake8 src tests
	mypy --explicit-package-bases src

# docker compose up
up:
	$(MAKE) lint
	docker compose up --build

# docker compose down
down:
	docker compose down

# install dependencies in local env for testing
install:
	. venv/bin/activate
	pip install -r requirements-dev.txt

# run tests
test:
	$(MAKE) lint
	$(MAKE) install
	python -m pytest -v tests/*