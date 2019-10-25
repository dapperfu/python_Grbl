VENV:=virtual_env
BIN=${VENV}/bin
PYTHON=${BIN}/python3
PIP=${BIN}/pip

${PYTHON}:
	git submodule update --init
	python3 -mvenv ${VENV}
	${PIP} install --upgrade wheel setuptools pip
	${PIP} install -r requirements.txt
	${PIP} install -r requirements_test.txt


.PHONY: clean
clean:
	git clean -xfd

.PHONY: venv
venv: ${PYTHON}


.PHONY: test
test:
	${BIN}/pytest


.PHONY: jupyter
jupyter:
	${BIN}/jupyter-notebook

.PHONY: build
build:
	${PYTHON} setup.py build

.PHONY: develop
develop:
	${PYTHON} setup.py develop

grbl.hex:
	wget https://github.com/gnea/grbl/releases/download/v1.1h.20190825/grbl_v1.1h.20190825.hex


.PHONY: watch
watch:
	watcher -cmd 'pre-commit run --all-files' -keepalive
