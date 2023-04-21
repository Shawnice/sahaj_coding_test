.DEFAULT_GOAL := help


.PHONY: help
help: ## Help guide
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort -k 1,1


.PHONY: format
format: ## Format modified python files
	git diff master --name-only --oneline -- '*.py' | xargs isort
	git diff master --name-only --oneline -- '*.py' | xargs black


.PHONY: lint
lint: ## Lint modified python files
	-git diff master --name-only --oneline -- '*.py' | xargs ruff
	-git diff master --name-only --oneline -- '*.py' | xargs mypy


.PHONY: run
run: ## Run application
	python src/main.py $(FILE)


.PHONY: test
test: ## Run project tests
	pytest -ss -v


.PHONY: pip-install
pip-install: ## Upgrade/install required python packages
	pip install --upgrade pip
	pip install --upgrade setuptools wheel
	find . -name "requirements*.txt" -exec pip install --upgrade -r {} \;
