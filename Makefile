SHELL := /usr/bin/env bash

BASH_SCRIPTS := $(shell grep -rl '^#!/usr/bin/env bash' control-plane platform | sort)
YAML_FILES := $(shell find .github deploy docs examples platform -type f \( -name '*.yml' -o -name '*.yaml' \) 2>/dev/null | sort)

.PHONY: ci syntax lint yaml docs

ci: syntax lint yaml

syntax:
	@if [ -z "$(BASH_SCRIPTS)" ]; then \
		echo "No bash scripts found"; \
	else \
		bash -n $(BASH_SCRIPTS); \
	fi

lint:
	@if ! command -v shellcheck >/dev/null 2>&1; then \
		echo "shellcheck not installed; skipping shell lint"; \
		exit 0; \
	fi
	@if [ -z "$(BASH_SCRIPTS)" ]; then \
		echo "No bash scripts found"; \
	else \
		shellcheck -x -P control-plane $(BASH_SCRIPTS); \
	fi

yaml:
	@if [ -z "$(YAML_FILES)" ]; then \
		echo "No YAML files found"; \
	elif command -v ruby >/dev/null 2>&1; then \
		ruby -rpsych -e 'ARGV.each { |f| Psych.parse_file(f); puts "YAML ok: #{f}" }' $(YAML_FILES); \
	else \
		echo "ruby not installed; skipping YAML parse"; \
	fi

docs:
	@echo "Start with README.md, then docs/operations/operator-quickstart.md and docs/verification.md"
