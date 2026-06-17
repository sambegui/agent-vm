#!/usr/bin/env bash
# common.sh — shared library for agent-vm control scripts.
# SOURCE this file (do not execute). Provides ssh target resolution, logging,
# guard helpers, dry-run gating for mutating scripts, and a context banner.

# Workspace root (override with AGENT_VM_ROOT). common.sh lives in scripts/lib/,
# so the repo root is two levels up.
AGENT_VM_ROOT="${AGENT_VM_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
export AGENT_VM_ROOT

# Guest access: host ~/.ssh/config alias 'agent-runtime' = user admin (passwordless sudo).
GUEST_SSH="${GUEST_SSH:-agent-runtime}"
GUEST_NAME="${GUEST_NAME:-agent-runtime}"

# --- logging ---
log()    { printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*" >&2; }
banner() { printf '\n=== %s ===\n' "$*" >&2; }
die()    { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# --- guards ---
require_cmd() { command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"; }

# --- guest helpers (read-only by default) ---
guest_ssh()  { ssh -o BatchMode=yes -o ConnectTimeout=10 "$GUEST_SSH" "$@"; }
guest_sudo() { guest_ssh "sudo -n $*"; }

# --- dry-run gating for mutating scripts ---
APPLY=0
applying() { [ "$APPLY" = "1" ]; }

# --- every script prints what it operates on ---
print_context() {
  log "workspace=$AGENT_VM_ROOT  guest=$GUEST_SSH($GUEST_NAME)  apply=$APPLY"
}
