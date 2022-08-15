.PHONY: install format lint test sec

install:
	@poetry install --no-root
format:
	@isort .
	@blue .
lint:
	@blue . --check
	@isort . --check
	@prospector --with-tool pydocstyle --doc-warning --no-autodetect
test:
	@pytest -v
sec:
	@pip-audit