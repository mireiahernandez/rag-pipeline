# docker compose up
up:
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
	$(MAKE) install
	python -m pytest -v tests/*