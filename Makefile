.PHONY: help setup install test lint format demo clean verify check

help:
	@echo "Available commands:"
	@echo "  make setup      - Run full setup (recommended for first time)"
	@echo "  make install    - Install dependencies only"
	@echo "  make verify     - Verify installation"
	@echo "  make check      - Check environment"
	@echo "  make test       - Run tests"
	@echo "  make demo       - Run dashboard demo"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean cache files"

setup:
	@echo "Running setup script..."
	@chmod +x setup.sh
	@./setup.sh

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r ai_tools/requirements.txt
	@if [ -f "tests/requirements.txt" ]; then pip install -r tests/requirements.txt; fi
	@echo "Dependencies installed!"

verify:
	@echo "Verifying installation..."
	@python3 scripts/check_environment.py || python scripts/check_environment.py

check: verify

test:
	pytest tests/ -v --cov=ai_tools --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

lint:
	flake8 ai_tools/ dashboard/ tests/ --max-line-length=100 --exclude=__pycache__
	pylint ai_tools/ dashboard/ tests/ --disable=C0111

format:
	black ai_tools/ dashboard/ tests/
	isort ai_tools/ dashboard/ tests/

demo:
	streamlit run dashboard/app.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

