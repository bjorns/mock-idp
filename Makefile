VERSION:=$(shell pipenv run python3 -c "from mockidp.__version__ import version; print(version)")

all: dist docker_image

clean:
	rm -rf dist build *.egg-info test_reports .coverage .pipenv
	rm -f *.log
	find . | grep \.pyc$ | xargs rm -rf
	find . | grep __pycache__ | xargs rm -rf

test: .pipenv
	pipenv run pytest tests/

test_release: dist
	pipenv run twine upload -r pypitest dist/*

release: pypi_release docker_release

pypi_release: dist
	pipenv run twine upload --verbose -r pypi dist/*

dist: clean .pipenv
	pipenv run python setup.py bdist_wheel

.pipenv: Pipfile Pipfile.lock
	pipenv install --dev
	touch $@

docker_release: docker_image
	docker push bjornskoglund/mock-idp:$(VERSION)

docker_run: docker_image
	docker run -p 5000:5000 bjornskoglund/mock-idp:$(VERSION)

docker_image:
	docker build --rm -t bjornskoglund/mock-idp:$(VERSION) .


.PHONY: all clean test test_release release pypi_release docker_release docker_run docker_image
