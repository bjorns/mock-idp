all: dist

clean:
	rm -rf dist build *.egg-info test_reports .coverage
	rm -f *.log
	find . | grep \.pyc$ | xargs rm -rf
	find . | grep __pycache__ | xargs rm -rf

dist: clean
	python3 setup.py bdist_wheel

test_release: dist
	twine upload -r pypitest dist/*

release: dist
	twine upload -r pypi dist/*

test:
	nosetests-3.4  --with-coverage --cover-package=mockidp --cover-min-percentage=80 --cover-html --cover-html-dir=build/test_reports

docker-image:
	docker build -t mock-idp .

docker-run: docker-image
	docker run -p 5000:5000 mock-idp
.PHONY: all clean dist lint test
