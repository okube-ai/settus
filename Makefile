install:
	pip install ./

dev:
	pip install -e './[dev,test,azure,aws]'

dev_lean:
	pip install -e './[dev,test]'

test:
	pytest --junitxml=junit/test-results.xml --cov=settus --cov-report=xml --cov-report=html tests

coverage:
	open htmlcov/index.html

build:
	pip install build
	python -m build

publish:
	pip install build twine
	python -m build
	twine upload dist/*

publishdoc:
	pip install mkdocs mkdocstrings[python] mkdocs-material
	mkdocs gh-deploy --force