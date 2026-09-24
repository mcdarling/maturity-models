# Dimension 5 — Agentic AI Security

Agentic AI systems do more than generate text. They call tools, run code, change
data and delegate work to other agents, often with limited human involvement. This
dimension covers the risks that come from that autonomy: who an agent acts as,
what it is allowed to do, when a human must approve, how far a failure can spread,
and whether agents can trust each other. It applies **only to systems with the
Agentic profile** and stacks on top of dimensions 1–4 and 6. An agent must still
meet every applicable governance, data, model, application and infrastructure
requirement. For example, prompt injection defense (APP-1) and output handling
(APP-2) remain the first line of defense, and the controls here limit what an
agent can do when those defenses fail.

| ID | Element | Applies to |
|---|---|---|
| AGT-1 | Agent Identity & Authentication | Agentic |
| AGT-2 | Tool, Plugin & MCP Authorization | Agentic |
| AGT-3 | Human Oversight & Action Approval | Agentic |
| AGT-4 | Agent Containment & Isolation | Agentic |
| AGT-5 | Multi-Agent & Inter-Agent Trust | Agentic |

---

## AGT-1 Agent Identity & Authentication

**Applies to:** Agentic

**Intent:** Give every agent a distinct, managed non-human identity, and make sure
that when an agent acts for a user it carries that user's identity and
authorization rather than broader privileges of its own. Every action an agent
takes must be attributable to both the agent and the principal it acted for.

**Key risks addressed:** Agents running on shared service accounts or borrowed
human credentials; privilege escalation when an agent's own rights exceed the
requesting user's (confused deputy); long-lived or unrotated agent credentials;
actions that cannot be traced to a specific agent or user during an incident;
identity spoofing and impersonation.

**References:** CISA ZTMM (Identity pillar); NIST AI RMF (GOVERN, MANAGE); OWASP
Top 10 for LLM Applications 2025 (LLM06 Excessive Agency); OWASP Top 10 for
Agentic Applications (identity and privilege abuse); OWASP Agentic AI Threats &
Mitigations (identity spoofing and impersonation, privilege compromise); Model
Context Protocol security guidance (authorization).

### Traditional
Agents run under whatever credentials were convenient when they were built: a
shared service account, a developer's personal token or the API key of the
application that hosts them. Several agents may share one identity. When an agent
acts for a user, downstream systems see only the agent's account, so they cannot
apply the user's permissions. Logs record that "the service" did something but not
which agent or which user was behind it.

### Initial
Each high-risk agent has its own non-human identity, registered with a named owner
and linked to its inventory record (GOV-1). Human credentials and shared service
accounts are no longer used by these agents. Agent credentials are stored in a
secrets manager (INF-3) and rotated on a defined schedule. There is a documented
pattern for agents acting on behalf of users, and high-risk agents log the agent
identity and the requesting user for every tool call.

**Practices**
- Create a dedicated identity per agent (per agent type and environment at
  minimum) in the organization's identity provider or workload identity system.
- Prohibit agents from using personal user credentials, shared service accounts
  or tokens copied from a human session.
- Record each agent identity's owner, purpose and permitted systems, linked to
  GOV-1 and AGT-2.
- Store agent credentials in a secrets manager and rotate them at least every
  90 days, or immediately on suspected compromise.
- Document how user identity is passed to downstream systems when an agent acts on
  a user's behalf, and when agent-only authority is permitted.
- Log agent identity, principal (user or triggering system) and session ID with
  every tool call.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-1.I.1` | Agent identity standard | `Doc` | Agentic | Requires a distinct identity per agent, prohibits shared service accounts and human credentials, sets a rotation period (≤ 90 days) and defines the on-behalf-of pattern and when agent-only authority is allowed. |
| `AGT-1.I.2` | Agent identity register | `Tech` | Agentic | Export from the identity provider or workload identity system listing each high-risk agent's identity, owner and linked inventory ID. No agent shares an identity with another agent or a human. |
| `AGT-1.I.3` | Credential storage and rotation records | `Rec` | Agentic | For each sampled agent, the secrets manager shows credentials stored there and at least one rotation within the stated period. No agent credentials found in code, prompts or config files by a secret scan. |
| `AGT-1.I.4` | Attributed action logs | `Tech` | Agentic | Log sample from each high-risk agent in which every tool call records agent identity, principal and session ID. |
| `AGT-1.I.5` | Shared/human credential review | `Rec` | Agentic | A review within the last 12 months that checked high-risk agents for shared or human credentials, with findings remediated or on the exception register with an expiry date. |

### Advanced
**All** agents, including agents built on third-party platforms and agents
embedded in SaaS, have managed non-human identities that follow a lifecycle:
provisioned through a standard process, reviewed periodically and deprovisioned
when the agent is retired. Agents authenticate with short-lived, workload-bound
credentials rather than static secrets where the platform allows it. When an
agent acts for a user, it uses standards-based delegation (such as OAuth token
exchange or on-behalf-of flows) so downstream systems authorize the request
against the user's own permissions, and the agent never has more access than the
user who invoked it. Identity requirements are checked at the deployment gate.

**Practices**
- Provision and deprovision agent identities through a standard workflow tied to
  the inventory (GOV-1); retiring an agent revokes its identities and credentials.
- Use short-lived tokens issued through workload identity federation or token
  exchange; static secrets require a tracked exception.
- Implement delegated authorization so downstream services see both the user and
  the agent (for example, subject and actor claims) and enforce the intersection
  of user and agent permissions.
- Review agent identities and their entitlements at least quarterly with the
  agent owner.
- Block deployment of an agent that lacks a registered identity or uses a
  prohibited credential type.
- Report agent identity metrics (coverage, static secrets, overdue reviews,
  orphaned identities) to the governance body (GOV-5).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-1.A.1` | Agent identity lifecycle procedure | `Doc` | Agentic | Defines provisioning, periodic review, credential issuance and deprovisioning, linked to the inventory and retirement process. |
| `AGT-1.A.2` | Short-lived credential configuration | `Tech` | Agentic | Configuration showing sampled agents use federated or exchanged tokens with a lifetime of ≤ 1 hour. Any static secret has an open exception with an expiry date. |
| `AGT-1.A.3` | Delegated authorization configuration | `Tech` | Agentic | For each sampled agent that acts for users, token or gateway configuration showing the user and agent are both represented and downstream authorization uses the user's permissions. |
| `AGT-1.A.4` | Confused-deputy test results | `Test` | Agentic | Tests within the last 12 months showing that a low-privilege user cannot, through the agent, read or change data they could not access directly. All failures remediated or tracked. |
| `AGT-1.A.5` | Quarterly entitlement review records | `Rec` | Agentic | Records for the last quarter covering all agents, showing excess entitlements removed and orphaned identities (no owner or retired agent) disabled. |
| `AGT-1.A.6` | Deployment gate for identity | `Tech` | Agentic | Pipeline or policy check that blocks agents without a registered identity or using a prohibited credential type, plus one example of a blocked or held deployment. |

### Optimal
Agent identity is fully automated and continuously verified across the AI estate.
Credentials are ephemeral and issued per task or session, bound to the workload
and, where possible, to the specific action requested. Identity analytics
establish a behavioral baseline for each agent identity and flag anomalous use,
such as an agent calling systems it has never used or acting for users outside
its normal population. Identity misuse triggers automatic credential revocation.
The organization has shown through red teaming that stolen or replayed agent
credentials and impersonation attempts are detected and contained.

**Practices**
- Issue per-task or per-session credentials scoped to the requested action and
  audience, with proof-of-possession or workload binding where supported.
- Feed agent identity activity into VIS for behavioral baselining and anomaly
  detection.
- Automatically revoke credentials and suspend the agent identity when misuse is
  detected (AUTO, IR).
- Red team agent credential theft, replay and impersonation at least annually
  (MDL-3).
- Use identity metrics and incident findings to tighten delegation and credential
  policies.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-1.O.1` | Ephemeral credential configuration | `Tech` | Agentic | Sampled agents receive per-task or per-session credentials with audience restriction and lifetime ≤ 15 minutes. No standing static secrets remain for sampled agents. |
| `AGT-1.O.2` | Identity anomaly detection and auto-revocation | `Tech` | Agentic | Detection rules for agent identity anomalies with an automated revocation or suspension action. The assessor observes a simulated misuse raise an alert and revoke the credential. |
| `AGT-1.O.3` | Credential theft and impersonation red-team report | `Test` | Agentic | Exercise within the last 12 months covering credential theft, token replay and agent impersonation, with time-to-detect and time-to-revoke measured against targets. |
| `AGT-1.O.4` | Improvement log | `Rec` | Agentic | Identity metric trends and documented changes to credential or delegation policy made as a result of metrics, red-team findings or incidents. |

---

## AGT-2 Tool, Plugin & MCP Authorization

**Applies to:** Agentic

**Intent:** Control which tools, plugins and MCP servers an agent can use and what
each call is allowed to do. Grant each agent only the tools and permissions its
task needs, authorize every call, constrain parameters, and admit tools into use
only after they have been vetted as part of the software supply chain.

**Key risks addressed:** Excessive functionality and permissions; tool misuse
driven by prompt injection; malicious or compromised tools and MCP servers; tool
description poisoning that hides instructions in tool metadata; "rug-pull" updates
that change a tool's behavior after approval; tool name collisions and shadowing;
destructive parameters passed to otherwise legitimate tools.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM06 Excessive Agency,
LLM03 Supply Chain); OWASP Top 10 for Agentic Applications (tool misuse, agentic
supply chain); OWASP Agentic AI Threats & Mitigations (tool misuse, privilege
compromise); Model Context Protocol security guidance (authorization, tool safety,
server trust); MITRE ATLAS; NIST AI RMF (MANAGE).

### Traditional
Developers add tools, plugins and MCP servers as needed, often from public
sources, without review. Tools run with broad, long-lived API keys, commonly the
same key for every tool. The agent can call any tool it has been given with any
parameters, and nothing checks whether a particular call is appropriate. Nobody
tracks which versions of third-party tools are in use or notices when they change.

### Initial
High-risk agents use only tools and MCP servers that have been reviewed and
recorded in an approved list. Each agent has a documented tool allowlist based on
its task, and each tool's credentials are scoped to the minimum operations it
needs. The review of a new tool or MCP server checks its source, maintainer,
permissions and tool descriptions for hidden instructions. Tool versions are
pinned so changes do not arrive silently.

**Practices**
- Maintain an approved list of tools, plugins and MCP servers, with owner, source,
  version and permissions requested.
- Review each new tool or MCP server before use: provenance, maintainer, requested
  scopes, data it can reach, and tool names and descriptions for embedded
  instructions or misleading claims.
- Define a per-agent tool allowlist; remove tools the agent's task does not need.
- Give each tool its own credential scoped to the minimum operations (for example,
  read-only where writes are not needed), stored per INF-3.
- Pin tool and MCP server versions and re-review before upgrading.
- Separate read-only tools from state-changing tools in the allowlist so AGT-3
  approval rules can target the latter.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-2.I.1` | Tool and MCP onboarding standard | `Doc` | Agentic | Defines review criteria (provenance, maintainer, scopes, data access, description review), approval authority, version pinning and re-review triggers. |
| `AGT-2.I.2` | Approved tool/MCP list | `Tech` | Agentic | Lists every tool and MCP server used by high-risk agents with owner, source, pinned version, requested permissions and approval date. No tool in use by a sampled agent is missing from the list. |
| `AGT-2.I.3` | Tool review records | `Rec` | Agentic | A completed review for each tool on the list used by high-risk agents, including a check of tool names and descriptions for embedded instructions. |
| `AGT-2.I.4` | Per-agent tool allowlists | `Tech` | Agentic | Agent configuration for each high-risk agent showing an explicit allowlist, with each tool marked read-only or state-changing. Allowlists match GOV-1 agent capability fields. |
| `AGT-2.I.5` | Scoped tool credentials | `Tech` | Agentic | IAM or API key configuration showing each sampled tool credential is limited to the operations the tool needs. No credential grants administrative or wildcard scope without an approved exception. |

### Advanced
Tool authorization is enforced at runtime for **all** agents through a central
tool gateway, MCP proxy or policy enforcement point, not only through agent
configuration. Every tool call is authorized against policy using the agent
identity, the principal (AGT-1), the tool, the operation and its parameters.
Parameter constraints block dangerous values such as unbounded queries, wildcard
deletes, external recipients or out-of-scope paths. Tool credentials are
short-lived and issued per call or session. The tool registry is integrated with
the deployment pipeline: unregistered tools cannot be connected, and changes to a
tool's code, schema or description are detected and trigger re-review.

**Practices**
- Route all agent tool and MCP traffic through a gateway or proxy that enforces
  per-call authorization and logs every decision.
- Express tool permissions and parameter constraints as policy (for example,
  allowed domains, record limits, path prefixes, recipient domains).
- Issue tool credentials just in time with lifetimes of minutes, scoped to the
  call or session.
- Fingerprint tool schemas and descriptions; alert on and block changes until
  re-reviewed (rug-pull protection).
- Detect and block duplicate or shadowing tool names across connected servers.
- Include third-party tools and MCP servers in vendor security review (INF-4) and
  in the AI-BOM (GOV-1).
- Measure and report unused permissions, denied calls and tools pending re-review.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-2.A.1` | Tool gateway / MCP proxy configuration | `Tech` | Agentic | Configuration showing all sampled agents' tool and MCP traffic passes through the enforcement point. Network or platform controls prevent direct tool access that bypasses it. |
| `AGT-2.A.2` | Tool authorization policies | `Tech` | Agentic | Policy set covering every state-changing tool used by sampled agents, with per-call authorization on agent, principal and operation and at least one parameter constraint per state-changing tool. |
| `AGT-2.A.3` | Authorization decision logs | `Rec` | Agentic | Logs from the last 30 days showing allow and deny decisions with agent, principal, tool, operation and reason, including examples of denied calls. |
| `AGT-2.A.4` | Tool change detection | `Tech` | Agentic | Configuration that fingerprints tool schemas/descriptions and holds changed tools pending re-review, plus at least one record of a detected change and its review outcome. |
| `AGT-2.A.5` | Registry deployment gate | `Tech` | Agentic | Pipeline or gateway check that blocks connection of unregistered tools or MCP servers, plus one example of a blocked connection. |
| `AGT-2.A.6` | Tool misuse test results | `Test` | Agentic | Tests within the last 12 months, including indirect prompt injection and poisoned tool descriptions, showing that out-of-policy calls and dangerous parameters are blocked. All failures remediated or tracked. |
| `AGT-2.A.7` | Least-privilege metrics report | `Rec` | Agentic | Quarterly report to the governance body covering unused tool permissions, deny rates and tools awaiting re-review, with actions taken to remove unused permissions. |

### Optimal
Tool permissions adapt to the task. Agents receive only the tools and scopes needed
for the specific task at hand, and permissions are removed automatically when they
go unused. The tool supply chain is continuously monitored: tool and MCP server
publishers, versions and behavior are checked against threat intelligence, and a
newly malicious or vulnerable tool is disabled across the estate automatically.
Runtime monitoring flags unusual tool call sequences. Red teaming shows that
tool misuse and supply chain attacks are blocked or contained.

**Practices**
- Grant tools and scopes dynamically per task based on the declared plan or
  intent, with default-deny for everything else.
- Automatically remove permissions and tools that have gone unused for a defined
  period.
- Monitor tool publishers and versions against threat intelligence and disable
  compromised tools across all agents automatically (AUTO).
- Baseline tool call sequences per agent and alert on anomalous chains (VIS).
- Red team the tool layer at least annually, including rug-pull and
  cross-server shadowing scenarios (MDL-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-2.O.1` | Task-scoped permission configuration | `Tech` | Agentic | Sampled agents receive tools and scopes per task with default-deny. Automatic removal of permissions unused for ≤ 90 days is configured and has fired at least once. |
| `AGT-2.O.2` | Automated tool kill capability | `Tech` | Agentic | Automation that disables a flagged tool or MCP server across all agents. The assessor observes a simulated compromised tool disabled estate-wide within the target time (e.g., ≤ 1 hour). |
| `AGT-2.O.3` | Tool-layer red-team report | `Test` | Agentic | Exercise within the last 12 months covering tool description poisoning, rug-pull updates, shadowing and parameter abuse, with results and remediation. |
| `AGT-2.O.4` | Improvement log | `Rec` | Agentic | Trends in deny rates, unused permissions and tool incidents, with documented policy or registry changes made as a result. |

---

## AGT-3 Human Oversight & Action Approval

**Applies to:** Agentic

**Intent:** Keep humans meaningfully in control of consequential agent actions.
Require human approval in proportion to risk, show approvers exactly what will
happen so their decision is informed, limit agent autonomy to what the use case
needs, and give agents and users a clear path to escalate.

**Key risks addressed:** Excessive autonomy; irreversible or high-impact actions
taken without review; rubber-stamping and approval fatigue; approval prompts that
misrepresent or hide what the agent will actually do; manipulation of human trust
in the agent to obtain approval; no escalation path when an agent is uncertain or
blocked.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM06 Excessive Agency);
OWASP Top 10 for Agentic Applications (human-agent trust exploitation, excessive
autonomy); OWASP Agentic AI Threats & Mitigations (overwhelming human-in-the-loop,
human manipulation); NIST AI RMF (GOVERN, MANAGE; human oversight); EU AI Act
(human oversight for high-risk systems) where applicable (GOV-4).

### Traditional
Agents act with whatever autonomy the developer chose. Some prompt the user for
confirmation, often with a generic "Allow?" dialog that shows little detail;
others take actions with no confirmation at all. There is no agreed view of which
actions are consequential. Approvers click through prompts without understanding
them, and no one measures whether approvals are meaningful.

### Initial
The organization has defined which agent actions are consequential, such as
financial transactions, external communications, data deletion, permission
changes, production changes and anything irreversible. High-risk agents require
explicit human approval before those actions. The approval request shows the
concrete action, its target and its parameters, not the agent's summary of them.
Each agent's autonomy level is documented and approved. Approvals and rejections
are logged.

**Practices**
- Define an action risk classification (for example, read-only, reversible
  state change, consequential, irreversible) and map each state-changing tool
  (AGT-2) to a tier.
- Require human approval for consequential and irreversible actions by
  high-risk agents; document any exceptions.
- Render approval requests from the actual tool call: tool, operation, target,
  full parameters and expected effect, separate from any model-generated
  explanation.
- Document each agent's autonomy level and have the system owner approve it as
  part of risk assessment (GOV-2).
- Provide an escalation path when the agent is uncertain, blocked or asked to act
  outside its scope, with a named human queue.
- Brief approvers on their role and on manipulation risks (GOV-5).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-3.I.1` | Action risk classification and oversight standard | `Doc` | Agentic | Defines action tiers, which tiers require approval, who may approve, what an approval request must display and the escalation path. |
| `AGT-3.I.2` | Tool-to-tier mapping and autonomy statements | `Doc` | Agentic | For each high-risk agent, every state-changing tool is mapped to a tier and the agent's autonomy level is approved by the system owner. |
| `AGT-3.I.3` | Approval enforcement configuration | `Tech` | Agentic | Configuration showing consequential and irreversible actions by high-risk agents are held until a human approves. Approval is enforced outside the model (in the tool layer or gateway), not by prompt instruction. |
| `AGT-3.I.4` | Approval request sample | `Tech` | Agentic | Screenshots or captures of approval requests for each sampled agent showing the tool, target and full parameters derived from the actual call. |
| `AGT-3.I.5` | Approval and escalation logs | `Rec` | Agentic | Logs from the last 90 days showing approvals, rejections and escalations with approver identity, timestamp and action details. |

### Advanced
Risk-based oversight applies to **all** agents and is enforced by a shared
approval service or gateway, so agents cannot bypass it. Approval requirements
consider context as well as action type: amount, data sensitivity, recipient,
reversibility and the agent's recent behavior. The approval experience is designed
to prevent rubber-stamping: it highlights unusual or risky elements, applies
step-up confirmation for the highest tiers and routes high-impact approvals to
people with the right authority, not only the requesting user. The organization
measures approval quality and uses it to tune thresholds.

**Practices**
- Enforce approvals through a central service integrated with the tool gateway
  (AGT-2) for every agent.
- Apply context-aware thresholds (for example, payment amount, external
  recipients, bulk operations, sensitive data classes from DATA-3).
- Require step-up authentication or second-person approval for irreversible or
  highest-tier actions.
- Highlight anomalies in approval requests, such as first-time recipients,
  unusual volumes or parameters that differ from the user's original request.
- Track approval metrics (approval rate, time-to-approve, approvals per approver
  per day, reversed or regretted approvals) and investigate signs of fatigue.
- Add excessive-agency review to the deployment gate: new tools or increased
  autonomy require re-approval of the autonomy statement.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-3.A.1` | Central approval service configuration | `Tech` | Agentic | Configuration showing all sampled agents route tiered actions through the shared approval service, with context-aware rules covering at least amount/volume, recipient and data sensitivity. |
| `AGT-3.A.2` | Step-up and dual-approval configuration | `Tech` | Agentic | Irreversible or highest-tier actions require step-up authentication or a second approver with appropriate authority. The requesting user cannot be the sole approver for those actions. |
| `AGT-3.A.3` | Approval bypass test results | `Test` | Agentic | Tests within the last 12 months showing agents cannot complete tiered actions without approval, including through prompt injection, action splitting (many small actions below threshold) and alternative tools. |
| `AGT-3.A.4` | Approval display fidelity test | `Test` | Agentic | Tests showing the approval request matches the executed action, including a case where the model's explanation differs from the actual call and the discrepancy is visible to the approver. |
| `AGT-3.A.5` | Approval quality metrics report | `Rec` | Agentic | Quarterly report covering approval rates, time-to-approve, approvals per approver and reversed approvals, with fatigue indicators investigated and thresholds adjusted where needed. |
| `AGT-3.A.6` | Autonomy change gate records | `Rec` | Agentic | Records showing every change that added a state-changing tool or increased autonomy in the last 12 months was re-approved before release. |

### Optimal
Oversight is adaptive. The level of human involvement adjusts automatically to
measured risk: autonomy is extended for action types with a strong track record
and tightened automatically when anomalies, incidents or threat intelligence
indicate higher risk. Approval quality is verified continuously, including through
seeded test approvals that confirm approvers catch harmful requests. Exercises
show that attackers cannot obtain approval for harmful actions by manipulating
approvers or overwhelming them with requests.

**Practices**
- Adjust approval thresholds automatically from measured outcomes and risk
  signals, with governance sign-off on the adjustment rules.
- Automatically tighten oversight (for example, require approval for all
  state-changing actions) for an agent when VIS raises an anomaly.
- Seed periodic known-bad approval requests to measure approver detection rates.
- Run exercises that attempt human-agent trust exploitation and approval flooding
  (MDL-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-3.O.1` | Adaptive oversight configuration | `Tech` | Agentic | Rules that change approval requirements based on risk signals. The assessor observes a simulated anomaly automatically raise an agent's approval requirements. |
| `AGT-3.O.2` | Seeded approval test results | `Test` | Agentic | Seeded known-bad requests at least quarterly, with approver detection rate measured against a target (e.g., ≥ 95%) and follow-up where it is missed. |
| `AGT-3.O.3` | Trust exploitation and flooding exercise report | `Test` | Agentic | Exercise within the last 12 months attempting persuasive or deceptive approval requests and high-volume approval flooding, with results and remediation. |
| `AGT-3.O.4` | Improvement log | `Rec` | Agentic | Documented changes to thresholds, approval UX or autonomy levels driven by metrics, exercise results or incidents. |

---

## AGT-4 Agent Containment & Isolation

**Applies to:** Agentic

**Intent:** Limit how much damage an agent can do if it is manipulated, malfunctions
or is compromised. Run agent-generated code and actions in isolated environments,
restrict network and filesystem access, enforce budgets on steps, time and spend,
and make sure agents can be stopped quickly and safely without causing cascading
failures.

**Key risks addressed:** Remote code execution through agent-run code; data
exfiltration through unrestricted network egress; access to files and secrets
outside the task's scope; runaway loops and resource exhaustion; unbounded cost
("denial of wallet"); cascading failures across dependent systems or agents; no
way to stop a misbehaving agent quickly.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM06 Excessive Agency,
LLM10 Unbounded Consumption); OWASP Top 10 for Agentic Applications (unexpected
code execution, cascading failures); OWASP Agentic AI Threats & Mitigations
(unexpected RCE and code attacks, resource overload, cascading hallucination and
failures); MITRE ATLAS; NIST AI RMF (MANAGE); CISA ZTMM (Networks and Applications
& Workloads pillars).

### Traditional
Agents that run code do so in the same process, container or host as the
application, often with the host's network and filesystem access. There are no
limits on how many steps an agent can take, how long it can run or how much it can
spend. Stopping a misbehaving agent means finding and killing the process or
revoking a key manually, and nobody has checked what happens to in-flight work
when that is done.

### Initial
High-risk agents that execute code or commands do so in a sandbox separate from
the host application, with no access to host credentials. Network egress from
agent environments is restricted to an allowlist, and filesystem access is limited
to a task working directory. Each high-risk agent has limits on steps, run time
and spend. There is a documented, tested way to stop each high-risk agent.

**Practices**
- Run agent-generated code in an isolated sandbox (container with hardened
  profile, microVM or equivalent) separate from the agent host, per INF-1.
- Restrict egress from agent and sandbox environments to an allowlist of required
  destinations.
- Scope filesystem access to a per-task working directory; mount nothing
  sensitive, and keep secrets out of the sandbox.
- Set per-run limits on steps or tool calls, wall-clock time, tokens and spend.
- Document a kill procedure for each high-risk agent: who can trigger it, how, and
  what happens to in-flight actions.
- Test the kill procedure at least once per agent.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-4.I.1` | Containment standard | `Doc` | Agentic | Defines sandbox requirements for code execution, egress and filesystem restrictions, required budget types and the kill procedure requirements. |
| `AGT-4.I.2` | Sandbox configuration | `Tech` | Agentic | For each high-risk agent that runs code, configuration showing execution in an isolated sandbox with no host credentials, no privileged mode and no access to the host filesystem. |
| `AGT-4.I.3` | Egress and filesystem restrictions | `Tech` | Agentic | Network policy or proxy configuration showing an egress allowlist, and mount/permission configuration showing filesystem access limited to the task directory. |
| `AGT-4.I.4` | Budget configuration | `Tech` | Agentic | Configured limits on steps or tool calls, run time and spend for each high-risk agent, with the values stated. |
| `AGT-4.I.5` | Kill procedure and test record | `Rec` | Agentic | For each high-risk agent, a documented kill procedure and a record of it being exercised, showing time-to-stop and handling of in-flight actions. |

### Advanced
Containment is standard for **all** agents and provided by a shared, hardened
agent runtime rather than built per project. Sandboxes are ephemeral and destroyed
after each task. Egress goes through a controlled proxy that logs and filters
traffic. Budgets apply per run, per agent and per principal, and exceeding one
halts the agent gracefully and alerts the owner. Each agent has a documented blast
radius, and design reviews (APP-4) limit it with circuit breakers, rate limits and
transactional or compensating actions. A central kill switch can halt any agent or
all agents of a type, and halting leaves systems in a consistent state.

**Practices**
- Provide a platform-managed agent runtime with ephemeral, hardened sandboxes as
  the default for all agents.
- Route all agent egress through a proxy with allowlists, logging and data loss
  prevention for sensitive data classes (DATA-3).
- Enforce budgets at multiple levels (run, agent, principal, organization) with
  graceful halt and alerting on breach.
- Document each agent's blast radius (systems, data and actions reachable) and
  apply circuit breakers and rate limits on high-impact tools.
- Design state-changing workflows to be transactional, idempotent or reversible
  with compensating actions, so a halt does not leave partial changes.
- Provide a central kill switch integrated with IR runbooks, able to halt a single
  run, a single agent or a class of agents.
- Include containment checks in the deployment gate.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-4.A.1` | Managed agent runtime configuration | `Tech` | Agentic | Configuration showing all sampled agents run on the shared runtime with ephemeral sandboxes destroyed after each task. Exceptions are on the exception register. |
| `AGT-4.A.2` | Egress proxy configuration and logs | `Tech` | Agentic | Proxy configuration with per-agent allowlists and sensitive-data filtering, and logs from the last 30 days showing blocked egress attempts. |
| `AGT-4.A.3` | Multi-level budget enforcement | `Tech` | Agentic | Budget limits at run, agent and principal level for sampled agents, with at least one record of a breach causing a graceful halt and an owner alert. |
| `AGT-4.A.4` | Blast-radius assessments | `Doc` | Agentic | For each sampled agent, a documented blast radius listing reachable systems, data and actions, with circuit breakers, rate limits or reversibility controls for each high-impact action. |
| `AGT-4.A.5` | Central kill switch test | `Test` | Agentic | Test within the last 6 months halting a single agent and a class of agents via the central kill switch, measuring time-to-halt against target (e.g., ≤ 5 minutes) and confirming no partial state changes remain. |
| `AGT-4.A.6` | Sandbox escape and exfiltration test results | `Test` | Agentic | Tests within the last 12 months attempting sandbox escape, access to host credentials and data exfiltration through agent-run code. All failures remediated or tracked. |

### Optimal
Containment is automated and adaptive across the estate. Runtime monitoring
detects anomalous agent behavior, such as loops, unexpected egress, spend spikes or
activity outside the agent's baseline, and automatically tightens limits,
quarantines the run or halts the agent. The organization runs failure-injection
exercises that confirm a failed or compromised agent does not cascade into
dependent systems. Kill switches and graceful halt are verified routinely, not
only after incidents.

**Practices**
- Feed runtime telemetry (steps, egress, spend, resource use) to VIS with
  automatic containment actions (AUTO).
- Automatically quarantine or halt agents on anomaly, with owner notification and
  preserved forensic state for IR.
- Run chaos or failure-injection exercises on agent workflows and dependent
  systems at least annually.
- Verify the kill switch and graceful halt automatically on a schedule.
- Use containment metrics and exercise findings to tighten defaults.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-4.O.1` | Automated containment rules | `Tech` | Agentic | Detection rules with automatic quarantine or halt actions for loops, anomalous egress and spend spikes. The assessor observes a simulated runaway agent halted automatically with forensic state preserved. |
| `AGT-4.O.2` | Cascading failure exercise report | `Test` | Agentic | Failure-injection exercise within the last 12 months showing a failed or compromised agent was contained without unplanned impact on dependent systems or agents, with findings remediated. |
| `AGT-4.O.3` | Scheduled kill switch verification | `Rec` | Agentic | Automated kill switch and graceful-halt checks run at least monthly, with results recorded and failures investigated. |
| `AGT-4.O.4` | Improvement log | `Rec` | Agentic | Containment metric trends (halts, budget breaches, blocked egress, time-to-halt) and documented changes to defaults made as a result. |

---

## AGT-5 Multi-Agent & Inter-Agent Trust

**Applies to:** Agentic

**Intent:** Make interactions between agents as trustworthy as interactions between
services. Authenticate agents to each other, protect the integrity of the messages
they exchange, prevent privileges from growing as tasks are delegated across hops,
protect shared memory and context from poisoning, and detect agents that behave
outside their intended role.

**Key risks addressed:** Spoofed or unauthenticated agents in a multi-agent
system; tampered or replayed inter-agent messages; privilege escalation through
delegation chains; prompt injection that spreads from one agent to others; poisoned
long-term memory or shared context; rogue or compromised agents; loss of
attribution across delegated tasks.

**References:** OWASP Top 10 for Agentic Applications (inter-agent communication,
memory and context poisoning, rogue agents, cascading failures); OWASP Agentic AI
Threats & Mitigations (memory poisoning, agent communication poisoning, rogue
agents in multi-agent systems, repudiation and untraceability); Agent2Agent (A2A)
protocol security considerations; Model Context Protocol security guidance; MITRE
ATLAS; NIST AI RMF (MANAGE); CISA ZTMM (Identity pillar).

### Traditional
Agents pass messages to each other as plain text through queues, shared prompts or
direct calls, and trust whatever they receive. A sub-agent inherits or is given
the orchestrator's full permissions. Agents write to shared memory or context
stores without validation, and anything written there is later treated as
trusted. Nobody tracks which agents talk to which, and a task's delegation chain
cannot be reconstructed.

### Initial
High-risk multi-agent systems have a documented architecture that shows each
agent, its role, which agents it communicates with and the trust level of each
channel. Agents authenticate to each other using their AGT-1 identities over
encrypted channels, and each agent accepts requests only from agents it is
expected to work with. Delegated tasks carry no more privilege than the delegating
agent and the original principal have. Content received from other agents is
treated as untrusted input subject to APP-1 controls. Writes to persistent or
shared memory are restricted and logged.

**Practices**
- Document the multi-agent architecture: agents, roles, communication paths,
  trust boundaries and memory stores (APP-4).
- Require mutual authentication between agents using their managed identities and
  encrypted transport.
- Maintain an allowlist of permitted agent-to-agent interactions per agent.
- Enforce privilege non-escalation: a delegated task's permissions are limited to
  the intersection of the delegating agent's and the original principal's.
- Treat inter-agent messages and retrieved memory as untrusted input; apply
  APP-1 and APP-2 controls.
- Restrict which agents can write to shared or long-term memory, and log all
  writes with the writing agent and source.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-5.I.1` | Multi-agent architecture and trust model | `Doc` | Agentic | For each high-risk multi-agent system, shows agents, roles, permitted communication paths, trust boundaries and memory stores, reviewed within 12 months. |
| `AGT-5.I.2` | Inter-agent authentication configuration | `Tech` | Agentic | Configuration showing agents authenticate each other with managed identities (e.g., mTLS or signed tokens) over encrypted channels, and reject requests from agents not on their allowlist. |
| `AGT-5.I.3` | Delegation privilege rules | `Tech` | Agentic | Configuration or code showing delegated tasks receive permissions no broader than the delegating agent and original principal. |
| `AGT-5.I.4` | Memory write controls and logs | `Tech` | Agentic | Access controls limiting which agents can write to shared or persistent memory, and a log sample showing each write with agent identity, principal and source. |
| `AGT-5.I.5` | Inter-agent injection test | `Test` | Agentic | Test within the last 12 months showing that instructions injected into one agent's input or output do not cause another agent to take out-of-scope actions. Failures remediated or tracked. |

### Advanced
Inter-agent trust controls apply to **all** multi-agent systems, including those
that interact with third-party agents. Agent-to-agent communication uses a
standard protocol (for example, an A2A-style protocol) with authenticated agent
identities, verified agent descriptors or capability cards, signed or
integrity-protected messages and replay protection. The original principal and
the full delegation chain are propagated with each task, so every action can be
traced end to end and downstream agents enforce privilege non-escalation at every
hop. Memory and shared context have provenance, integrity checks, expiry and
validation before use. Third-party agents are onboarded through vendor review
(INF-4) with a restricted trust level.

**Practices**
- Standardize on an inter-agent protocol that supports authenticated identities,
  signed agent descriptors, message integrity and replay protection.
- Propagate the original principal and delegation chain in every inter-agent
  request; each hop verifies it and narrows permissions.
- Limit delegation depth and fan-out to defined maximums.
- Attach provenance (writing agent, principal, source, time) to memory entries;
  validate entries before use and expire or re-validate them on a schedule.
- Isolate memory per user or tenant where the use case allows, and prevent
  cross-tenant memory reads.
- Onboard external agents with verified descriptors, restricted scopes and
  vendor review.
- Log inter-agent interactions centrally so delegation chains can be
  reconstructed (VIS).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-5.A.1` | Inter-agent protocol standard | `Doc` | Agentic | Specifies the approved protocol, identity and descriptor verification, message signing or integrity protection, replay protection, maximum delegation depth and fan-out, and external-agent trust levels. |
| `AGT-5.A.2` | Message integrity and replay protection configuration | `Tech` | Agentic | Configuration for sampled multi-agent systems showing signed or integrity-protected messages, descriptor verification and nonce/timestamp replay protection. |
| `AGT-5.A.3` | Delegation chain traces | `Rec` | Agentic | End-to-end traces from the last 30 days for sampled systems showing the original principal and every hop, with permissions at each hop no broader than the previous one. |
| `AGT-5.A.4` | Memory provenance and isolation configuration | `Tech` | Agentic | Configuration showing memory entries carry provenance, are validated before use, expire or are re-validated on a defined schedule, and are isolated per user or tenant where required. |
| `AGT-5.A.5` | Multi-agent attack test results | `Test` | Agentic | Tests within the last 12 months covering agent spoofing, message tampering and replay, delegation escalation beyond the limit and memory poisoning, with all failures remediated or tracked. |
| `AGT-5.A.6` | External agent onboarding records | `Rec` | Agentic | For each third-party agent integrated with sampled systems, a completed vendor review, verified descriptor and assigned restricted trust level. |

### Optimal
Inter-agent trust is continuously verified. Each agent's communication and
behavior is baselined, and deviations from its declared role, such as calling
unexpected agents, requesting unusual delegations or writing anomalous memory, are
detected automatically. A suspected rogue or compromised agent is isolated from the
multi-agent system automatically, its credentials are revoked and memory it wrote
is quarantined for review. Exercises show that a compromised agent cannot spread
its compromise or escalate privilege across the system.

**Practices**
- Baseline agent-to-agent interaction graphs and behavior per role; alert on
  deviations (VIS).
- Automatically isolate suspected rogue agents, revoke their credentials (AGT-1)
  and quarantine the memory entries they wrote (AUTO, IR).
- Scan memory and shared context continuously for injected instructions and
  poisoned entries.
- Run multi-agent compromise exercises at least annually, including a rogue agent
  inside the trust boundary (MDL-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AGT-5.O.1` | Rogue agent detection and isolation | `Tech` | Agentic | Behavioral detection rules for agents with automatic isolation, credential revocation and memory quarantine. The assessor observes a simulated rogue agent isolated automatically. |
| `AGT-5.O.2` | Continuous memory integrity scanning | `Tech` | Agentic | Scheduled or streaming scans of shared and persistent memory for injected instructions, running at least daily, with findings routed to triage. |
| `AGT-5.O.3` | Multi-agent compromise exercise report | `Test` | Agentic | Exercise within the last 12 months with a compromised agent inside the trust boundary, measuring spread, privilege gained and time-to-isolate against targets, with remediation. |
| `AGT-5.O.4` | Improvement log | `Rec` | Agentic | Trends in inter-agent anomalies, memory findings and exercise results, with documented changes to protocols, delegation limits or memory controls made as a result. |
