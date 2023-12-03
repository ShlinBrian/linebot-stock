include .env

.PHONY: clean init

service_up:
	docker-compose up -d postgres

service_down:
	docker-compose down

analysis: bandit


reformat: isort black

black:
	black api/

lint: flake8 pylint

test:
	pytest -vv\
	 --cov-report=term-missing\
	 --cov=api/endpoints\
	 --cov=api/common\
	 --cov=api/machine api/tests

ci-bundle: analysis reformat lint test

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf .tox
	rm -f report.xml
	rm -f coverage.xml

run-api:
	cd api/ && uvicorn --port $(API_PORT) --host 0.0.0.0 --log-level error app:APP --reload