STREAM_KEY ?= NOT_EXIST
STREAM_SECRET ?= NOT_EXIST

.PHONY: help check test lint lint-fix

help: ## Display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

lint:  ## Run linters
	black --check stream_django
	flake8 --ignore=E501,E203,W503 stream_django

lint-fix:
	black stream_django

test:  ## Run tests
	STREAM_API_KEY=$(STREAM_KEY) \
	STREAM_API_SECRET=$(STREAM_SECRET) \
	DJANGO_SETTINGS_MODULE=stream_django.tests.test_app.settings \
	pytest stream_django/tests

check: lint test  ## Run linters + tests

reviewdog:
	black --check --diff --quiet stream_django | reviewdog -f=diff -f.diff.strip=0 -filter-mode="diff_context" -name=black -reporter=github-pr-review
	flake8 --ignore=E501,E203,W503 stream_django | reviewdog -f=flake8 -name=flake8 -reporter=github-pr-review
