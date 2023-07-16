install:
	flit install

dev:
	flit install -s

test:
	pytest --junitxml=junit/test-results.xml --cov=settus --cov-report=xml --cov-report=html tests

coverage:
	open htmlcov/index.html

build:
	flit build

publish:
	flit publish