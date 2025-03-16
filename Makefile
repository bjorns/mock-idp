VERSION:=$(shell ./.venv/bin/python3 -c "from mockidp.__version__ import version; print(version)")

all: dist docker_image

clean:
	rm -rf dist build *.egg-info test_reports .coverage .venv
	rm -f *.log
	find . | grep \.pyc$ | xargs rm -rf
	find . | grep __pycache__ | xargs rm -rf

test: .venv
	./.venv/bin/pytest tests/

test_release: dist
	./.venv/bin/twine upload -r pypitest dist/*

release: pypi_release docker_release

pypi_release: dist
	./.venv/bin/twine upload --verbose -r pypi dist/*

dist: clean .venv
	./.venv/bin/python setup.py bdist_wheel

.venv: requirements.txt setup.py
	python3 -m venv --upgrade-deps --upgrade $@
	./.venv/bin/pip install -r requirements.txt

docker_release: docker_image
	docker push bjornskoglund/mock-idp:$(VERSION)

docker_run: docker_image
	docker run -p 5000:5000 bjornskoglund/mock-idp:$(VERSION)

docker_image:
	docker build --rm -t bjornskoglund/mock-idp:$(VERSION) .


.PHONY: all clean test test_release release pypi_release docker_release docker_run docker_image
