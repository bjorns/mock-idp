VERSION:=$(shell pipenv run python3 -c "from mockidp import __version__; print(__version__)")

all: dist

clean:
	rm -rf dist build *.egg-info test_reports .coverage
	rm -f *.log
	find . | grep \.pyc$ | xargs rm -rf
	find . | grep __pycache__ | xargs rm -rf

.pipenv: Pipfile Pipfile.lock
	pipenv install --dev
	touch $@

dist: clean .pipenv
	pipenv run python setup.py bdist_wheel

test_release: dist
	pipenv run twine upload -r pypitest dist/*

release: dist
	pipenv run twine upload -r pypi dist/*

test: .pipenv
	pipenv run nosetests  --with-coverage --cover-package=mockidp --cover-min-percentage=80 --cover-html --cover-html-dir=build/test_reports

docker-image:
	docker build --rm -t bjornskoglund/mock-idp:$(VERSION) .

docker-release: docker-image
	docker push bjornskoglund/mock-idp:$(VERSION)

docker-run: docker-image
	docker run -p 5000:5000 bjornskoglund/mock-idp:$(VERSION)

.PHONY: all clean dist lint test
