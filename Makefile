TOX=tox

.PHONY: lint
lint:
	$(TOX) -c tox.ini -e lint

.PHONY: coverage
coverage:
	$(TOX) -c tox.ini -e coverage

.PHONY: test
test:
	$(TOX) -c tox.ini -e test

PYREVERSE_OPTS = --output=pdf
.PHONY: view
view:
	-rm -Rf _pyreverse
	mkdir _pyreverse
	PYTHONPATH=src pyreverse ${PYREVERSE_OPTS} --project="pyprocdev" src/pyprocdev
	mv classes_pyprocdev.pdf _pyreverse
	mv packages_pyprocdev.pdf _pyreverse

.PHONY: archive
archive:
	git archive --output=./pyprocdev.tar.gz HEAD

.PHONY: upload-release
upload-release:
	python setup.py register sdist upload

.PHONY: docs
docs:
	cd doc/_build/html; zip -r ../../../docs *
