install-dev:
	.venv/bin/pip install -r requirements-dev.txt

test:
	.venv/bin/pytest

test-v:
	.venv/bin/pytest -v
