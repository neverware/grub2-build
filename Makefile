PY_FILES=*.py container/*.py

all: fmt lint

fmt:
	yapf -i ${PY_FILES}

fmt-check:
	yapf --diff ${PY_FILES}

lint:
	pylint ${PY_FILES}

.PHONY: all fmt fmt-check lint
