.DEFAULT_GOAL := help

PYTHON ?= python3

.PHONY: install-frontend build-frontend build-python-package test-python-package test clean version help

###### Development

install-frontend: ## Install the frontend dependencies
	cd frontend && npm install

build-frontend: install-frontend ## Build the frontend project
	cd frontend && npm run build

build-python-package: ## Build the Python source and wheel distributions
	$(PYTHON) -m build

test-python-package: build-python-package ## Validate the Python package distribution metadata
	$(PYTHON) -m twine check dist/*

test: test-python-package ## Run the test suite
	$(PYTHON) -m pytest -v

###### Additional commands

clean: ## Clean up the project by removing build artifacts
	find . -name "*.egg-info" -type d -exec git rm -r --cached {} +
	# node modules and build artifacts
	rm -rf frontend/node_modules
	rm -rf frontend/build
	rm -rf frontend/dist
	rm -rf dist

version: ## Print the current tutor version
	@python -c 'import io, os; about = {}; exec(io.open(os.path.join("tutor", "__about__.py"), "rt", encoding="utf-8").read(), about); print(about["__package_version__"])'

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
