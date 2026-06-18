SHELL := /usr/bin/env bash

AGENT_VM_NAME ?= agent-platform
AGENT_VM_IP ?= 10.0.0.60
AGENT_VM_MAC ?= 52:54:00:00:00:01
AGENT_VM_USER ?= agent
AGENT_VM_SSH ?= $(AGENT_VM_NAME)
AGENT_VM_PUBKEY ?= $(HOME)/.ssh/$(AGENT_VM_NAME).pub
AGENT_VM_IMGDIR ?= /var/lib/libvirt/images/$(AGENT_VM_NAME)

BASH_SCRIPTS := $(shell grep -rl '^#!/usr/bin/env bash' control-plane platform | sort)
YAML_FILES := $(shell find .github deploy docs examples platform -type f \( -name '*.yml' -o -name '*.yaml' \) 2>/dev/null | sort)
PLATFORM_TESTS := $(shell find platform/tests -maxdepth 1 -type f -name '*-test' 2>/dev/null | sort)

.PHONY: ci syntax lint yaml test provision docs

ci: syntax lint yaml test

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

test:
	@set -e; \
	for test_script in $(PLATFORM_TESTS); do \
		echo "bash $$test_script"; \
		bash "$$test_script"; \
	done

provision:
	AGENT_VM_NAME="$(AGENT_VM_NAME)" \
	AGENT_VM_IP="$(AGENT_VM_IP)" \
	AGENT_VM_MAC="$(AGENT_VM_MAC)" \
	AGENT_VM_USER="$(AGENT_VM_USER)" \
	AGENT_VM_SSH="$(AGENT_VM_SSH)" \
	AGENT_VM_PUBKEY="$(AGENT_VM_PUBKEY)" \
	AGENT_VM_IMGDIR="$(AGENT_VM_IMGDIR)" \
	platform/vm/provision-vm
	AGENT_VM_SSH="$(AGENT_VM_SSH)" platform/vm/bootstrap-runtime

docs:
	@echo "Start with README.md, then docs/operations/operator-quickstart.md and docs/verification.md"
