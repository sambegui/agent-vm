# 05 — Secure gated agent preview access

Agent previews are useful because reviewers need to see the actual running surface, not only a
screenshot or a local build log. They are risky because an agent runtime or development server is a
network service attached to code, tools, files, logs, and sometimes sensitive task context.

This pattern treats preview access as a temporary, least-privilege access grant. The goal is not to
make the preview public. The goal is to let an approved operator or reviewer reach only the intended
preview ports through an explicit, auditable gate, while the host/control plane keeps its normal
network identity and the guest/runtime uses a separate isolated network identity.

Tailscale is used below as one illustrative implementation. The normative requirements apply equally
to another private overlay, bastion, VPN, access proxy, or zero-trust gateway.

## Standards posture

The secure preview gate is part of the governance layer, not a convenience tunnel. A preview session
MUST be:

- **explicit** — created for a named review window and preview surface;
- **temporary** — short-lived, revoked, and torn down after use;
- **least-privilege** — scoped to approved reviewers and approved ports only;
- **isolated** — the guest/runtime identity is separate from the host/control-plane identity;
- **auditable** — access grants, firewall openings, preview start, and teardown are recorded;
- **reversible** — logout, daemon stop, firewall rollback, and inactive-state verification are part of
  the runbook;
- **secret-by-reference** — auth keys or credentials are stored outside the repo and never copied into
  prompts, logs, transcripts, Markdown examples, manifests, or receipts.

A preview path SHOULD NOT become a permanent management path. Production access should have its own
identity, policy, monitoring, and incident procedures.

## Reference topology

```text
operator / approved reviewer
        |
        | private overlay ACL/grant: approved reviewer -> preview ports only
        v
isolated guest/runtime preview identity
        |
        | guest firewall: default deny, allow only overlay interface + scoped preview ports
        v
agent preview service on <preview-port>

host/control plane
        |
        | normal operator network identity; does not join or expose through the preview identity
        v
promotion, status, rollback, receipts
```

Design intent:

- The **host/control plane** remains reachable through its normal operator-controlled path.
- The **guest/runtime** gets a separate, temporary preview identity.
- The overlay grants reviewer access only to approved preview ports such as `4000-4099`, `5173`, and
  `8000-9000`.
- The guest firewall remains default-deny and allows preview traffic only on the private overlay
  interface.
- Broad routing features are disabled unless a separate, reviewed use case justifies them.

## Threat model

| Threat | Why it matters | Control |
|---|---|---|
| Unauthorized preview access | A preview server may expose drafts, logs, local state, or agent outputs. | Overlay ACLs/grants/tags restrict source identities; guest firewall allows only scoped ports on the overlay interface. |
| Persistent agent network identity | A forgotten runtime identity can become a standing access path. | Use ephemeral identity/session state where possible; require logout, daemon stop, and inactive-state proof. |
| Accidental subnet exposure | A preview tunnel can accidentally bridge more of the guest or site network than intended. | Disable subnet route advertisement and route acceptance by default. |
| Exit-node exposure | A guest can accidentally become a general network relay. | Disable exit-node advertisement and selection. |
| Public exposure | Public sharing features can bypass the private-review model. | Disable Funnel/public exposure unless explicitly approved in a separate threat model. |
| Broad remote shell access | Tailscale SSH or equivalent features can exceed preview needs. | Disable overlay SSH by default; use the existing operator-controlled management path. |
| Auth-key leakage | Auth keys can join devices or mint identities. | Treat keys as secrets-by-reference; never place values in prompts, logs, repos, memory, transcripts, or receipts. |
| Broad firewall rules | Allowing all overlay traffic exposes unintended local services. | Keep guest firewall default-deny; allow only the private overlay interface and approved preview ports. |
| Forgotten preview sessions | A demo path can become unowned infrastructure. | Teardown is mandatory; verify no daemon, interface, temporary rules, or key material remain. |

## Control objectives

| Objective | Practices |
|---|---|
| Identity isolation | Keep host/control-plane identity separate from guest/runtime preview identity; prefer tags or device identities scoped to preview use. |
| Least privilege | Grant only approved reviewers or operator accounts access to approved preview ports. |
| No broad routing | Disable subnet routes, accepted routes, exit nodes, public exposure, and overlay SSH unless separately justified. |
| Temporary access | Prefer ephemeral auth keys and in-memory session state; record the review window and revoke access after use. |
| Firewall scoping | Keep input default-deny; allow preview traffic only on the private overlay interface and only to scoped ports. |
| Secrets-by-reference | Store auth-key material outside the repo; reference a protected path such as `<auth-key-file>` without printing its value. |
| Auditability | Record who requested access, who was allowed, which ports were exposed, when it started, and teardown evidence. |
| Teardown / rollback proof | Verify logout, stopped transient daemon, removed temporary firewall rules, removed key material, and inactive overlay state. |

## Normative requirements

A secure agent preview access design MUST:

1. define the preview purpose, owner, reviewer identities, ports, and expiration before opening access;
2. use a separate guest/runtime preview identity rather than reusing the host/control-plane identity;
3. restrict access to specific reviewers or groups through ACLs, grants, tags, or equivalent policy;
4. expose only scoped preview ports, for example `4000-4099`, `5173`, and `8000-9000`;
5. keep guest firewall input default-deny and allow preview traffic only on the private overlay
   interface;
6. keep auth keys and equivalent credentials out of prompts, logs, repositories, Markdown examples,
   transcripts, and receipts;
7. disable subnet routing, exit-node behavior, public exposure, and overlay SSH unless a separate
   approval and threat model require them;
8. verify active state before telling reviewers the preview is ready;
9. require teardown and inactive-state verification before the work is closed;
10. run repository secret scanning before publishing examples or receipts.

A secure agent preview access design SHOULD:

- use ephemeral auth keys or equivalent short-lived join credentials;
- use in-memory daemon state such as `tailscaled --state=mem:` when the implementation supports it;
- put temporary runtime files under an operating-system runtime directory rather than the repository;
- bind preview services to explicit interfaces where the framework supports it;
- write a short receipt that includes command output summaries but no secret values;
- prefer an approved wrapper script for implementation details so operators do not paste secrets into
  shells or transcripts.

## Illustrative Tailscale implementation

> This section is an example, not a vendor endorsement or a requirement to use Tailscale. Replace every
> placeholder with environment-specific values outside the repository. Do not paste real auth keys into
> this document, prompts, logs, or tickets.

### Tailnet policy shape

Use ACLs, grants, groups, and tags to restrict reviewer access to the preview identity and preview
ports only. The exact syntax may vary by Tailscale policy version; the shape should be equivalent to:

```json
{
  "tagOwners": {
    "tag:agent-preview": ["group:platform-operators"]
  },
  "grants": [
    {
      "src": ["group:approved-preview-reviewers"],
      "dst": ["tag:agent-preview"],
      "ip": ["tcp:4000-4099", "tcp:5173", "tcp:8000-9000"]
    }
  ],
  "ssh": []
}
```

Policy intent:

- only approved reviewers can reach the tagged preview node;
- only preview ports are reachable;
- overlay SSH is empty/disabled;
- the tag cannot be self-assigned by arbitrary users;
- the policy does not grant subnet routing, exit-node use, or public exposure.

### Preflight checklist

Before starting the preview, the operator MUST confirm:

- [ ] The preview purpose, owner, reviewers, ports, and expiration are documented.
- [ ] The auth key is ephemeral or short-lived where supported.
- [ ] The auth key grants only the preview tag/identity and no broad device ownership.
- [ ] The auth key is stored in `<auth-key-file>` with restrictive file permissions outside the repo.
- [ ] The guest/runtime has a default-deny firewall posture.
- [ ] The preview app is bound to an explicit preview port in the approved range.
- [ ] The Tailscale policy allows only approved reviewers to the preview tag and ports.
- [ ] Subnet routes, route acceptance, exit-node behavior, Funnel/public exposure, and Tailscale SSH
      are not required for this review.
- [ ] The teardown owner and deadline are known.
- [ ] Secret scanning will run before any example, receipt, or docs change is published.

### Placeholder-only runbook

The following commands are intentionally placeholder-only. They show the required control shape, not a
copy/paste deployment recipe.

Set local variables without secret values in the command text:

```bash
PREVIEW_DIR=/run/agent-preview
TAILSCALE_SOCKET="$PREVIEW_DIR/tailscaled.sock"
AUTH_KEY_FILE="<auth-key-file>"
OPERATOR_TAILNET_IP="<operator-tailnet-ip>"
PREVIEW_HOSTNAME="<preview-hostname>"
PREVIEW_PORT="<preview-port>"
OVERLAY_IFACE=tailscale0
APPROVED_TAILSCALE_PREVIEW_WRAPPER="<approved-tailscale-preview-wrapper>"
```

Create runtime-only state outside the repository:

```bash
sudo install -d -m 0700 "$PREVIEW_DIR"
sudo install -m 0600 "$AUTH_KEY_FILE" "$PREVIEW_DIR/authkey"
```

Start a transient daemon with in-memory identity state where supported:

```bash
sudo tailscaled \
  --state=mem: \
  --statedir="$PREVIEW_DIR" \
  --socket="$TAILSCALE_SOCKET" &
```

Join with restrictive preview defaults. Use an approved wrapper in real operations so the auth-key
value is read from `<auth-key-file>` without being printed, logged, stored in shell history, or copied
into a transcript.

```bash
sudo "$APPROVED_TAILSCALE_PREVIEW_WRAPPER" up \
  --socket "$TAILSCALE_SOCKET" \
  --auth-key-file "$PREVIEW_DIR/authkey" \
  --hostname "$PREVIEW_HOSTNAME" \
  --advertise-tags tag:agent-preview \
  --reset \
  --accept-dns=false \
  --accept-routes=false \
  --advertise-routes= \
  --advertise-exit-node=false \
  --exit-node= \
  --ssh=false
```

If the implementation supports disabling managed firewall changes, prefer explicit local firewall
rules controlled by the operator. The exact commands depend on the host firewall. This nftables-shaped
example allows only one reviewer IP and only one preview port on the overlay interface:

```bash
sudo nft add table inet agent_preview
sudo nft add chain inet agent_preview input '{ type filter hook input priority 0; policy accept; }'
sudo nft add rule inet agent_preview input \
  iifname "$OVERLAY_IFACE" ip saddr "$OPERATOR_TAILNET_IP" tcp dport "$PREVIEW_PORT" accept \
  comment "agent-preview-temporary"
sudo nft add rule inet agent_preview input \
  iifname "$OVERLAY_IFACE" tcp dport { 4000-4099, 5173, 8000-9000 } drop \
  comment "agent-preview-temporary"
```

Start the preview app through the normal development command for the project, with no secrets printed
and no broad bind unless required by the framework:

```bash
START_PREVIEW_COMMAND="<start-preview-command>"
PRIVATE_OVERLAY_BIND_ADDRESS="<private-overlay-bind-address>"
"$START_PREVIEW_COMMAND" --host "$PRIVATE_OVERLAY_BIND_ADDRESS" --port "$PREVIEW_PORT"
```

Verify the preview is reachable only through the approved gate:

```bash
sudo tailscale --socket="$TAILSCALE_SOCKET" status
sudo nft list ruleset | grep 'agent-preview-temporary'
curl --fail --silent --show-error "http://$PREVIEW_HOSTNAME:$PREVIEW_PORT/health"
```

Record a preview-ready receipt containing:

- preview owner and expiration;
- reviewer identity or group, not secret values;
- preview hostname and approved port;
- firewall rule summary;
- overlay status summary;
- app health-check result;
- teardown deadline and owner.

### Ready checklist for agents

An agent or operator MUST NOT mark preview access ready until all items are true:

- [ ] The preview service is the intended code/artifact and runtime alignment is known.
- [ ] The exposed port is in the approved preview range.
- [ ] The overlay identity is the guest/runtime preview identity, not the host/control-plane identity.
- [ ] ACLs/grants/tags restrict access to the approved reviewer set.
- [ ] The guest firewall allows only overlay-interface traffic to the approved preview port(s).
- [ ] Subnet routes are not advertised.
- [ ] Route acceptance is disabled unless explicitly justified.
- [ ] Exit-node advertisement and exit-node selection are disabled.
- [ ] Funnel/public exposure is disabled.
- [ ] Tailscale SSH or equivalent overlay SSH is disabled.
- [ ] Auth-key material is referenced only by protected path and not present in logs, prompts, repo,
      receipts, memory, or transcripts.
- [ ] The readiness receipt has been written without secret values.
- [ ] A teardown deadline and owner are recorded.

## Teardown checklist

Teardown is required even for failed preview sessions.

- [ ] Notify reviewers that the preview window is closed.
- [ ] Stop the preview application.
- [ ] Log out the preview overlay identity.
- [ ] Stop the transient overlay daemon.
- [ ] Remove temporary firewall rules.
- [ ] Remove runtime-only key material and daemon state.
- [ ] Revoke the auth key or remove the ephemeral node if it still exists in the admin console.
- [ ] Verify the overlay interface is gone or has no address.
- [ ] Verify no preview process is listening on the exposed port.
- [ ] Verify no temporary firewall rules remain.
- [ ] Write a teardown receipt without secret values.

Placeholder-only teardown commands:

```bash
sudo tailscale --socket="$TAILSCALE_SOCKET" logout || true
sudo pkill -f 'tailscaled.*agent-preview' || true
sudo nft delete table inet agent_preview || true
sudo rm -rf "$PREVIEW_DIR"
```

Verification commands:

```bash
sudo tailscale --socket="$TAILSCALE_SOCKET" status || true
ip addr show "$OVERLAY_IFACE" || true
sudo nft list ruleset | grep 'agent-preview-temporary' && exit 1 || true
ss -ltnp | grep ":$PREVIEW_PORT" && exit 1 || true
```

The final teardown receipt SHOULD include the inactive overlay status, absent firewall rules, absent
listener, removed runtime directory, and revoked/expired key reference. It MUST NOT include the auth-key
value.

## Publication and secret-scan gate

Before publishing a preview-access example, run the repository's normal static checks and every
available secret scanner over the changed files. At minimum, run the available subset of:

```bash
gitleaks detect --source . --no-git --redact
trufflehog filesystem . --only-verified --no-update
detect-secrets scan --all-files
git secrets --scan
```

If a tool is unavailable, record it as unavailable rather than silently skipping it. Pair scanner output
with manual review for private hostnames, private addresses, auth-key material, transcript content,
firewall handles, and environment-specific identifiers.

## Non-goals

This pattern does not:

- make an agent runtime production-ready by itself;
- replace authentication on the preview application;
- justify exposing production data in previews;
- grant broad remote administration;
- replace promotion, rollback, audit, and canary evidence;
- claim endorsement by Tailscale or any other vendor.

The preview gate is only one control. It should be used with the rest of the platform posture:
workload isolation, default-deny egress, secrets-by-reference, explicit promotion, audit records, and
verified rollback.
