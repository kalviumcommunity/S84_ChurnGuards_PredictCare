.PHONY: help install run clean test lint format

help:
	@echo "ChurnGuard AI - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install    Install dependencies"
	@echo "  run        Run the Streamlit application"
	@echo "  clean      Remove Python cache files"
	@echo "  lint       Run code linting (flake8)"
	@echo "  format     Format code with black"
	@echo "  test       Run tests (future)"

install:
	pip install -r requirements.txt

run:
	streamlit run streamlit_app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	@echo "Running flake8..."
	@pip show flake8 > /dev/null 2>&1 || pip install flake8
	flake8 streamlit_app.py --max-line-length=100

format:
	@echo "Formatting with black..."
	@pip show black > /dev/null 2>&1 || pip install black
	black streamlit_app.py

test:
	@echo "No tests configured yet. Run: pytest tests/"
