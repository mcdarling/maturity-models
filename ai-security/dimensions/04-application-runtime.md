# Dimension 4 — AI Application & Runtime Security

This dimension covers the security of AI systems while they run: what goes into
the model, what comes out of it, who can call it, and how the surrounding
application is designed so that a manipulated model cannot do serious harm. For
LLM and agentic systems the central problem is that instructions and data share
one channel, so prompt injection cannot be fully prevented with today's
techniques. Maturity in this dimension therefore means layered defenses, designs
that limit the blast radius of a successful injection, and measured, accepted
residual risk. It does not mean a claim that injection has been "solved". Runtime
controls here depend on the inventory and risk classification (GOV-1, GOV-2),
are verified by adversarial testing (MDL-3), and feed monitoring and response
(VIS, IR).

| ID | Element | Applies to |
|---|---|---|
| APP-1 | Input Validation & Prompt Injection Defense | ML · LLM · Agentic |
| APP-2 | Output Handling & Content Safety | ML · LLM · Agentic |
| APP-3 | Inference Endpoint & API Security | ML · LLM · Agentic |
| APP-4 | Secure AI Application Architecture | ML · LLM · Agentic |

---

## APP-1 Input Validation & Prompt Injection Defense

**Applies to:** ML · LLM · Agentic (most requirements are `[LLM]` or `[Agentic]`)

**Intent:** Reduce the likelihood that untrusted input changes a model's
behavior in ways the application owner did not intend. For LLM and agentic
systems this means defending against direct prompt injection and jailbreaks
(from users) and indirect prompt injection (instructions hidden in retrieved
documents, web pages, emails, tool results or files). For classical ML it means
validating inputs against the expected schema and detecting adversarial or
out-of-distribution inputs. Because no single defense is reliable, the element
requires several independent layers and honest measurement of what still gets
through.

**Key risks addressed:** Direct and indirect prompt injection; jailbreaks that
bypass safety instructions; instruction smuggling through retrieved or tool
content; adversarial examples and evasion against classical models; malformed
inputs that crash or degrade the model.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM01 Prompt Injection);
MITRE ATLAS (prompt injection and evasion techniques); NIST AI 100-2
(Adversarial Machine Learning taxonomy — evasion and prompt injection attacks);
NIST AI RMF (MEASURE, MANAGE); Google Secure AI Framework (SAIF).

### Traditional
User input is passed to the model as-is, or with only the generic input
validation a web application would apply. System prompts may contain
"ignore any instructions in the text" style warnings, which are treated as a
security control. Retrieved documents and tool output are concatenated directly
into the prompt with no marking of where untrusted content starts or ends.
Classical models accept any input the calling code sends. Nobody has measured
how easily the system can be manipulated.

### Initial
High-risk AI systems have a documented input-defense design that names the
untrusted input sources and applies at least one defense beyond the system
prompt. For LLM systems this usually means a guardrail layer (an injection or
jailbreak classifier, or a provider safety filter) and structural separation of
instructions from untrusted content. For classical models it means input schema
validation. The team has tested the defenses at least once with known attack
payloads and recorded the results, including what got through.

**Practices**
- For each high-risk system, list every source of input that reaches the model
  (user, retrieval, files, email, web, tool results, other agents) and mark each
  as trusted or untrusted.
- Do not rely on system-prompt instructions alone as an injection defense;
  record them as defense-in-depth only.
- Validate input type, length, encoding and size before it reaches the model;
  reject or truncate over-limit input.
- [ML] Validate feature inputs against the model's expected schema and value
  ranges; reject or flag out-of-range and malformed records.
- [LLM] Place a guardrail layer in front of the model that screens user input
  for known injection and jailbreak patterns.
- [LLM] Mark untrusted content structurally (delimiting, tagging or
  "spotlighting" such as encoding or datamarking) so the model and downstream
  filters can tell it apart from instructions.
- [LLM] Normalize or strip content that is commonly used to hide instructions
  (invisible Unicode, zero-width characters, hidden HTML/CSS text, document
  metadata) from retrieved and uploaded content.
- [Agentic] Treat tool results, web content and messages from other agents as
  untrusted input and screen them before they re-enter the agent's context.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-1.I.1` | Input-source inventory and defense design | `Doc` | All | For each high-risk system, lists every input source reaching the model, its trust level and the defenses applied to it. Names an owner. States explicitly that system-prompt instructions are not relied on as the sole defense. |
| `APP-1.I.2` | Input validation configuration | `Tech` | All | Configuration or code showing length/size/type limits enforced before model invocation for each high-risk system. |
| `APP-1.I.3` | ML input schema validation | `Tech` | ML | For each high-risk classical model, a schema or validation rule set (types, ranges, required fields) enforced at the inference boundary, with rejected-input handling defined. |
| `APP-1.I.4` | Guardrail layer configuration | `Tech` | LLM | Export showing an input guardrail (injection/jailbreak classifier or equivalent) enabled for each high-risk LLM system, including its action on detection (block, flag, sanitize) and thresholds. |
| `APP-1.I.5` | Untrusted-content separation | `Tech` | LLM | Prompt templates or code showing retrieved, uploaded and tool content is delimited or otherwise marked as data, and that hidden-text normalization is applied to retrieved/uploaded content. |
| `APP-1.I.6` | Baseline injection test results | `Test` | LLM | A test run against each high-risk LLM system using a documented payload set that includes both direct and indirect injection cases (at least 50 payloads), recording attack success rate and the payloads that succeeded. |
| `APP-1.I.7` | Agent tool-result screening | `Tech` | Agentic | Configuration showing tool outputs, fetched web content and inter-agent messages pass through the guardrail layer or equivalent screening before returning to the agent context. |

### Advanced
Input defenses are standardized and applied to **all** in-scope AI systems,
usually through a shared guardrail service or AI gateway rather than each team
building its own. Defenses are layered: no system depends on a single
classifier. Injection resistance is tested automatically before every release,
and results are tracked as metrics with defined thresholds. Where testing shows
the defenses cannot bring risk to an acceptable level, the system's design is
changed to limit what an injected instruction could achieve (see APP-4, AGT-2,
AGT-3) and the residual risk is formally accepted.

**Practices**
- Provide input guardrails as a central, versioned service or gateway policy
  that all AI applications use; track exceptions.
- Require at least two independent defense layers for each LLM system (for
  example, input classifier plus structural separation plus privilege-limited
  design).
- Run an automated injection and jailbreak regression suite in the release
  pipeline; block release when attack success rate exceeds the approved
  threshold.
- Maintain the payload corpus from public research, red-team findings (MDL-3)
  and production detections.
- Record residual injection risk per system and have it accepted by the system
  owner as part of risk assessment (GOV-2).
- Log guardrail detections to the monitoring platform (VIS) with the system ID
  and input source.
- [ML] Deploy adversarial-input or out-of-distribution detection for
  high-risk classical models exposed to untrusted callers, and monitor
  detection rates.
- [LLM] Cover indirect injection through every retrieval source (DATA-4),
  including documents that users can upload or edit.
- [Agentic] Test injection scenarios end to end through the agent's real tool
  set, measuring whether an injected instruction leads to an unauthorized tool
  call, not only whether the model "complies" in text.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-1.A.1` | Central guardrail/gateway policy | `Tech` | LLM | Export of the shared guardrail or gateway policy, with its version, showing it applies to every sampled LLM system. Systems not behind it appear in the exception register. |
| `APP-1.A.2` | Layered-defense mapping | `Doc` | LLM | For each sampled LLM system, at least two independent defense layers are named and mapped to the input sources they cover, with no untrusted source left uncovered. |
| `APP-1.A.3` | Release-gate injection suite | `Tech` | LLM | Pipeline definition showing the automated injection/jailbreak suite runs on every release (model, prompt or tool change), with the pass threshold, plus one example of a failed or held release. |
| `APP-1.A.4` | Injection resistance metrics | `Rec` | LLM | Report, at least quarterly, of attack success rate per system for direct and indirect injection, trend over time and systems exceeding threshold, delivered to the accountable owner or governance body. |
| `APP-1.A.5` | Residual-risk acceptance | `Rec` | LLM | For each sampled LLM system, a signed residual-risk statement citing the latest test results and the blast-radius controls relied on (APP-4, AGT-2, AGT-3). |
| `APP-1.A.6` | Adversarial input detection | `Tech` | ML | For high-risk classical models exposed to untrusted callers, configuration of adversarial/OOD detection with alerting to VIS, and a detection-rate record for the last 90 days. |
| `APP-1.A.7` | End-to-end agent injection tests | `Test` | Agentic | Test results for each sampled agent in which injected content in a tool result, document or web page attempts a state-changing tool call. Results report the rate of unauthorized tool calls actually attempted and whether downstream controls blocked them. |

### Optimal
Input defenses adapt continuously. Guardrail models and rules are updated from
threat intelligence, red-team results and production detections, and each
update is regression-tested before rollout. Adaptive attacks (automated,
optimization-based or multi-turn) are part of continuous testing, not only
static payload lists. The organization can show measured residual risk for
every system over time and demonstrate that its defenses held during red-team
exercises or real attempted attacks.

**Practices**
- Run continuous automated adversarial testing, including adaptive and
  multi-turn attacks, against production-equivalent systems.
- Feed confirmed production injection attempts and red-team successes into the
  payload corpus and guardrail tuning within a defined SLA.
- Measure both attack success rate and false-positive rate so tuning does not
  silently degrade usability or security.
- [Agentic] Exercise indirect-injection scenarios in multi-step and multi-agent
  workflows (AGT-5) where injected content propagates across agents or memory.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-1.O.1` | Continuous adversarial testing | `Tech` | LLM | Scheduled job (at least weekly) running adaptive or automated attack generation against every production LLM system, with results flowing to the metrics dashboard. |
| `APP-1.O.2` | Threat-driven update log | `Rec` | LLM | Log of guardrail and corpus updates over the last 12 months, each traced to a source (threat intel, red team, incident, detection) and showing regression-test results before rollout; median time from confirmed new technique to deployed defense is reported. |
| `APP-1.O.3` | Detection and false-positive trends | `Rec` | All | 12-month trend of attack success rate and guardrail false-positive rate per system, with documented tuning decisions made in response. |
| `APP-1.O.4` | Red-team validation | `Test` | Agentic | Red-team exercise (MDL-3) within 12 months covering multi-step or multi-agent indirect injection, showing that no injected instruction achieved a high-impact action, or that any that did were remediated and retested. |

---

## APP-2 Output Handling & Content Safety

**Applies to:** ML · LLM · Agentic

**Intent:** Treat everything a model produces as untrusted until it has been
validated for the place it is going. Model output can carry injection payloads
into browsers, databases, shells and APIs, can leak sensitive data or the
system prompt, can contain harmful content, and can be confidently wrong. This
element makes sure outputs are encoded, validated and filtered for their
destination, and that high-stakes outputs are checked for grounding. For
agentic systems the "output" includes proposed actions and tool arguments,
which must be validated before execution.

**Key risks addressed:** XSS, SQL injection, SSRF, command and code injection
in downstream consumers; system prompt and sensitive data leakage; harmful or
policy-violating content; hallucinated facts relied on in high-stakes
decisions; unsafe or out-of-policy tool calls; ML scores consumed outside their
valid range.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM05 Improper Output
Handling, LLM02 Sensitive Information Disclosure, LLM07 System Prompt Leakage,
LLM09 Misinformation, LLM06 Excessive Agency); OWASP Application Security
Verification Standard (output encoding and injection prevention); NIST AI 600-1
(Generative AI Profile — information integrity and harmful content risks);
NIST AI RMF (MANAGE).

### Traditional
Model output is inserted directly into web pages, queries, templates or
commands. Nobody has identified which downstream components consume model
output or what they do with it. Content filtering, if any, is whatever the
model provider applies by default. The system prompt contains secrets or
internal details and there is no check for it appearing in responses. Agents
execute whatever tool calls the model emits.

### Initial
For high-risk AI systems, the team has identified every downstream consumer of
model output and applies context-appropriate encoding or validation for each.
LLM systems have a content-safety filter configured for the organization's
policy (GOV-3), and system prompts contain no secrets. Agents validate tool
arguments against a schema before executing them. Controls have been tested at
least once.

**Practices**
- Map every consumer of model output (UI, database, API, file system, shell,
  email, downstream model) for each high-risk system.
- Apply the same output encoding and parameterization used for any untrusted
  user input: HTML/JS encoding for browsers, parameterized queries for
  databases, allowlisted URLs for fetches, no direct shell or `eval`
  execution.
- [ML] Validate model scores and predictions against expected type and range
  before downstream decisions consume them; define a safe fallback.
- [LLM] Configure content-safety filters (provider or self-hosted) on outputs,
  with categories and thresholds set to match acceptable-use policy.
- [LLM] Keep secrets, credentials and access-control logic out of system
  prompts; assume the system prompt can be extracted.
- [LLM] Constrain output format where possible (structured output / JSON
  schema) and reject outputs that do not conform.
- [Agentic] Validate every tool call's arguments against a strict schema and
  allowlist before execution; reject calls that do not validate rather than
  "repairing" them silently.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-2.I.1` | Output consumer map | `Doc` | All | For each high-risk system, lists every downstream consumer of model output and the encoding/validation control applied for each. No consumer marked "none" without a documented justification. |
| `APP-2.I.2` | Output encoding/validation implementation | `Tech` | All | Code or configuration showing the controls in `APP-2.I.1` are implemented (e.g., templating auto-escape enabled, parameterized queries, URL allowlist), with no direct execution of model output via shell or `eval`. |
| `APP-2.I.3` | ML output range checks | `Tech` | ML | For each high-risk classical model, validation of output type and range at the consumer, with defined fallback behavior on invalid output. |
| `APP-2.I.4` | Content-safety filter configuration | `Tech` | LLM | Export of output content-safety settings for each high-risk LLM system, showing categories, thresholds and action on detection, traceable to GOV-3. |
| `APP-2.I.5` | System prompt review | `Rec` | LLM | Review record for each high-risk LLM system confirming the system prompt contains no secrets, credentials or authorization logic, dated after the last prompt change. |
| `APP-2.I.6` | Output injection test results | `Test` | LLM | Test showing crafted model outputs (e.g., script tags, SQL fragments, internal URLs, markdown image exfiltration links) are neutralized by each consumer of each high-risk system. |
| `APP-2.I.7` | Tool-argument schema validation | `Tech` | Agentic | For each high-risk agent, schemas or allowlists for every tool's arguments and code showing non-conforming calls are rejected and logged. |

### Advanced
Output handling is standardized across **all** in-scope systems through shared
libraries, gateway policies or platform components. Sensitive data and system
prompt leakage are detected automatically in outputs. High-stakes uses have
grounding or verification checks. For agents, proposed actions are validated
against policy, not just schema, before execution: the check asks whether this
action, with these arguments, is permitted in this context. Output-handling
tests run in the release pipeline, and metrics are reported.

**Practices**
- Provide shared output-handling components (sanitizers, safe renderers,
  structured-output validators) and require their use through secure design
  review (APP-4).
- Scan outputs for sensitive data (DATA-3 classifications), secrets and
  system-prompt content, and block or redact on detection.
- Define which use cases are high-stakes (e.g., medical, legal, financial,
  security decisions) and apply grounding checks, citation verification or
  human review to their outputs.
- Include output-handling and leakage tests in the automated release suite.
- [Agentic] Evaluate each proposed action against a policy engine (resource,
  action, arguments, user context, risk level) independent of the model before
  execution, and route high-risk actions to human approval (AGT-3).
- [Agentic] Check tool arguments for embedded exfiltration paths (attacker
  URLs, recipients, file paths outside the allowed scope).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-2.A.1` | Shared output-handling standard and components | `Doc` | All | Standard naming the required output-handling components per consumer type, with evidence that every sampled system uses them or has a tracked exception. |
| `APP-2.A.2` | Output leakage detection | `Tech` | LLM | Configuration of automated output scanning for sensitive data, secrets and system-prompt fragments on every sampled LLM system, with block/redact actions and logging to VIS. |
| `APP-2.A.3` | Grounding controls for high-stakes uses | `Tech` | LLM | List of high-stakes use cases and, for each, the grounding/verification control in place (citation checking, retrieval-grounding score, secondary model check or mandatory human review) with thresholds. |
| `APP-2.A.4` | Release-pipeline output tests | `Tech` | LLM | Pipeline definition showing output-injection, leakage and content-safety tests run on every release, with pass criteria, plus results from the last release of each sampled system. |
| `APP-2.A.5` | Output-handling metrics | `Rec` | LLM | Report, at least quarterly, of content-safety blocks, leakage detections and grounding-check failures per system, with trends and follow-up actions. |
| `APP-2.A.6` | Action policy enforcement | `Tech` | Agentic | Policy-engine configuration evaluating tool calls on action, arguments and context before execution for each sampled agent, and logs showing at least one denied action in the last 90 days or a test demonstrating denial. |
| `APP-2.A.7` | Action-validation test results | `Test` | Agentic | Test in which model-proposed actions with out-of-policy arguments (external recipients, disallowed paths, attacker-controlled URLs) are attempted; all are blocked or routed to approval. |

### Optimal
Output controls are continuously verified and tuned. Leakage, content-safety
and grounding checks are measured for precision and recall, and thresholds
change based on measured results and incidents. Action validation for agents
is policy-as-code, versioned, tested and updated from red-team findings. The
organization can show that output controls stopped real or simulated
exploitation.

**Practices**
- Measure detection quality (false positives and false negatives) of output
  filters against labeled test sets and tune from the results.
- Replay confirmed incidents and red-team findings as regression tests.
- [Agentic] Manage action policies as code with tests, review and automated
  deployment; update them from observed agent behavior and red-team results.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-2.O.1` | Filter quality measurements | `Test` | LLM | Precision/recall (or FP/FN rates) for leakage and content-safety filters measured against a labeled set at least quarterly, with thresholds adjusted and changes recorded. |
| `APP-2.O.2` | Incident and red-team regression corpus | `Rec` | All | Every output-handling finding from incidents and red teams in the last 12 months has a corresponding automated regression test. |
| `APP-2.O.3` | Action policy as code | `Tech` | Agentic | Action policies stored in version control with automated tests and CI deployment; change history shows updates driven by red-team or monitoring findings. |
| `APP-2.O.4` | Exploitation resistance demonstration | `Test` | All | Red-team or exercise result within 12 months showing output-based exploitation attempts (downstream injection, data exfiltration, unsafe action) were blocked, observed by the assessor or reproduced on request. |

---

## APP-3 Inference Endpoint & API Security

**Applies to:** ML · LLM · Agentic

**Intent:** Control who can call AI models and applications, how much they can
consume, and what they can learn by querying. Inference endpoints are APIs with
unusual properties: each call can be expensive, responses can reveal
information about the model itself, and one tenant's traffic can affect
another's. This element covers authentication and authorization, rate limits
and quotas, cost and resource abuse ("denial of wallet"), tenant isolation,
abuse monitoring, model extraction resistance and, for agents, limits on steps
and actions.

**Key risks addressed:** Unauthenticated or over-privileged access to models;
unbounded consumption and denial of service or denial of wallet; model
extraction and membership inference through repeated querying; cross-tenant
data exposure through shared caches, sessions or context; runaway agent loops;
stolen API keys used for abuse.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM10 Unbounded
Consumption, LLM02 Sensitive Information Disclosure); OWASP API Security Top 10
2023 (API4:2023 Unrestricted Resource Consumption); MITRE ATLAS (model
extraction and inference API abuse techniques); NIST AI 100-2 (privacy and
model extraction attacks); CISA ZTMM (Applications & Workloads pillar).

### Traditional
Inference endpoints are protected, if at all, by a shared API key embedded in
applications. There are no per-user or per-application limits on requests,
tokens or spend, and cost overruns are found on the monthly bill. Nobody
monitors for unusual query patterns. Multi-tenant applications share sessions,
caches or conversation state with no isolation review. Agents can loop
indefinitely.

### Initial
Every high-risk inference endpoint requires authentication, and access is
granted per application or user rather than through one shared key. Rate
limits, token limits and spend alerts are configured. Tenant isolation has
been reviewed for multi-tenant systems. Agents have a maximum step or iteration
limit. The controls have been tested at least once.

**Practices**
- Require authentication for every inference endpoint, including internal
  ones; no anonymous access to high-risk models.
- Issue separate credentials per consuming application, managed under INF-3.
- Configure request rate limits and maximum input/output size per caller.
- Set spend budgets and alerts with the model provider or platform.
- Review multi-tenant systems for shared state (caches, conversation history,
  vector indexes, fine-tuned adapters) that could expose one tenant's data to
  another.
- [ML] Limit query rates and the detail of responses (e.g., return labels or
  rounded scores rather than full probability vectors) for models exposed to
  external callers.
- [LLM] Enforce maximum tokens per request and per conversation.
- [Agentic] Set maximum steps, tool calls and wall-clock time per agent task,
  and terminate the task when a limit is reached.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-3.I.1` | Endpoint authentication configuration | `Tech` | All | For each high-risk system, configuration showing authentication is required on every inference endpoint and credentials are per application/user, not shared. |
| `APP-3.I.2` | Rate, size and spend limits | `Tech` | All | Export of rate limits, input/output size limits and spend budgets with alert thresholds for each high-risk system. |
| `APP-3.I.3` | Tenant isolation review | `Rec` | All | For each multi-tenant high-risk system, a review record identifying shared state (caches, history, indexes, adapters) and the isolation control for each, with open findings tracked. |
| `APP-3.I.4` | Response detail limiting | `Tech` | ML | For externally exposed high-risk classical models, configuration showing response detail is limited (e.g., top label only, rounded confidence) and per-caller query limits are set. |
| `APP-3.I.5` | Token limits | `Tech` | LLM | Configuration showing maximum tokens per request and per conversation/session for each high-risk LLM system. |
| `APP-3.I.6` | Agent step and time budgets | `Tech` | Agentic | Configuration showing maximum steps, tool calls and runtime per task for each high-risk agent, with defined termination behavior. |
| `APP-3.I.7` | Limit enforcement test | `Test` | All | Test showing unauthenticated calls are rejected and that exceeding a rate, token or step limit is enforced, for each high-risk system. |

### Advanced
All in-scope inference traffic, including calls to third-party model APIs,
flows through a managed control point (typically an AI gateway) that enforces
authentication, per-caller quotas, cost controls and logging centrally.
Authorization is fine-grained: callers are allowed specific models and
operations. Abuse monitoring detects extraction patterns, key misuse and cost
anomalies, and alerts go to the security operations process. Metrics on
consumption and abuse are reported.

**Practices**
- Route all AI inference traffic, internal and third-party, through a managed
  gateway or equivalent control point; block direct calls to provider APIs from
  applications where feasible.
- Authorize callers per model and operation, using workload identities
  instead of static keys where the platform supports it.
- Enforce per-caller and per-tenant quotas on requests, tokens and spend, with
  automatic throttling or cut-off at hard limits.
- Detect abuse patterns: cost spikes, unusual query volume or distribution,
  credential use from unexpected locations, and systematic probing.
- [ML] Detect query patterns indicative of model extraction or membership
  inference (high-volume, synthetic or boundary-probing queries) and throttle
  or block the caller.
- [Agentic] Enforce per-agent and per-task budgets (steps, tool calls, tokens,
  spend) centrally, and alert on agents that repeatedly hit limits.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-3.A.1` | Gateway coverage | `Tech` | All | Gateway configuration and traffic data showing every sampled system's inference calls, including third-party APIs, pass through the control point; egress controls or exception register entries cover any direct calls. |
| `APP-3.A.2` | Fine-grained authorization policy | `Tech` | All | Policy showing callers are authorized per model and operation, with workload identities or short-lived credentials for sampled systems. |
| `APP-3.A.3` | Quota and hard-limit configuration | `Tech` | All | Per-caller and per-tenant quotas (requests, tokens, spend) with automatic throttling at hard limits, and a log entry showing a limit enforced in the last 90 days. |
| `APP-3.A.4` | Abuse detection rules | `Tech` | All | Detection rules in VIS for cost anomalies, volume anomalies and credential misuse on AI endpoints, with alert routing to the security operations process. |
| `APP-3.A.5` | Extraction detection | `Tech` | ML | For externally exposed classical models, detection rules for extraction/probing query patterns with automated throttling or blocking. |
| `APP-3.A.6` | Consumption and abuse metrics | `Rec` | All | Report, at least monthly, of consumption against budgets, limit hits, abuse alerts and their dispositions, per system. |
| `APP-3.A.7` | Central agent budgets | `Tech` | Agentic | Centrally enforced per-agent and per-task budgets with alerting on repeated limit hits, covering every sampled agent. |

### Optimal
Endpoint controls adapt automatically. Quotas and throttling respond to
observed behavior and risk signals rather than static values, and compromised
credentials or abusive callers are contained automatically. Extraction and
abuse defenses are tested with realistic attack simulations. Cost and abuse
metrics drive tuning.

**Practices**
- Apply adaptive throttling based on caller risk scores and behavioral
  baselines.
- Automate containment (revoke key, suspend caller, lower quota) on
  high-confidence abuse detections, linked to IR playbooks (AUTO).
- Simulate denial-of-wallet, extraction and credential-abuse attacks
  periodically and measure time to detect and contain.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-3.O.1` | Adaptive throttling | `Tech` | All | Configuration showing limits adjust based on behavioral baselines or risk scores, with a record of an automatic adjustment in the last 90 days. |
| `APP-3.O.2` | Automated containment | `Tech` | All | Playbook automation that revokes or suspends abusive callers without manual steps, and an execution record observed by the assessor or from the last 90 days. |
| `APP-3.O.3` | Abuse simulation results | `Test` | All | Simulation within 12 months covering denial of wallet and credential abuse (and extraction for `ML` systems), with measured time to detect and contain meeting defined targets (e.g., ≤ 15 minutes to contain). |
| `APP-3.O.4` | Tuning log | `Rec` | All | Record of limit and detection changes made from metrics, simulations or incidents over the last 12 months. |

---

## APP-4 Secure AI Application Architecture

**Applies to:** ML · LLM · Agentic

**Intent:** Design AI applications so that the model is never the only thing
standing between an attacker and a harmful outcome. Since prompt injection and
model manipulation cannot be fully prevented, architecture must assume the
model can be steered and limit what that achieves. This element covers
trust-boundary design, privilege separation, least-privilege context,
approved design patterns (such as dual-LLM or plan-then-execute), secure design
review for AI applications, reference architectures and the use of an AI
gateway as a standard control point.

**Key risks addressed:** A single injected instruction leading to data
exfiltration or harmful action; models holding more privilege or context than
the task needs; security decisions delegated to the model; inconsistent,
team-by-team designs that repeat known mistakes; AI features added to existing
applications without security review.

**References:** OWASP Top 10 for LLM Applications 2025 (LLM06 Excessive
Agency, LLM01 Prompt Injection); Google Secure AI Framework (SAIF); NIST AI RMF
(MAP, MANAGE); NIST SP 800-160 Vol. 1 (systems security engineering
principles); CISA Secure by Design guidance.

### Traditional
AI features are designed by individual teams with no AI-specific security
review. The model receives whatever context and permissions are convenient,
often the full privileges of the user or a service account. Authorization
decisions, such as whether a user may see a document, are left to the model's
judgment via instructions. There are no approved patterns or reference
architectures, and nobody has drawn the trust boundaries.

### Initial
High-risk AI systems have a threat model and architecture diagram that show
trust boundaries around the model, untrusted inputs and privileged actions.
Authorization is enforced outside the model. A security design review with
AI-specific checks is performed before production. The organization has
documented a small set of design principles for AI applications.

**Practices**
- Produce a threat model for each high-risk AI system covering the model,
  prompts, data sources, outputs, tools and integrations.
- Enforce authorization and access control in deterministic code or policy,
  never in the model's instructions.
- Give the model only the data and context needed for the task
  (least-privilege context), filtered by the requesting user's permissions
  (DATA-4).
- Perform an AI-specific security design review before production use.
- [ML] Identify where model decisions have security or safety impact and
  design fallback or override paths that do not depend on the model.
- [LLM] Document where untrusted content and sensitive data meet in the same
  context, since that combination enables exfiltration.
- [Agentic] Separate the component that reads untrusted content from the
  component that can take privileged actions, or document why this is not
  feasible and which compensating controls apply (AGT-2, AGT-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-4.I.1` | AI threat model and trust-boundary diagram | `Doc` | All | For each high-risk system, a threat model dated after the last major change, with a diagram showing trust boundaries, untrusted inputs, sensitive data and privileged actions, and mitigations mapped to threats. |
| `APP-4.I.2` | AI design principles | `Doc` | All | Approved principles including, at minimum: authorization outside the model, least-privilege context, model output treated as untrusted, and blast-radius limitation. |
| `APP-4.I.3` | Security design review records | `Rec` | All | Completed AI-specific design review for each high-risk system before production, with findings and their resolution or acceptance. |
| `APP-4.I.4` | Out-of-model authorization | `Tech` | All | Code or policy showing access decisions for data and actions in each high-risk system are enforced deterministically outside the model. |
| `APP-4.I.5` | Untrusted-content/sensitive-data analysis | `Doc` | LLM | For each high-risk LLM system, identifies contexts where untrusted content and sensitive data coexist and the exfiltration paths (links, images, tool calls) that are blocked. |
| `APP-4.I.6` | Agent privilege separation design | `Doc` | Agentic | For each high-risk agent, shows how untrusted-content processing is separated from privileged actions, or records the justification and compensating controls. |

### Advanced
Secure AI architecture is standardized. The organization publishes reference
architectures and approved patterns that teams must use for **all** in-scope
AI applications, including AI features embedded in existing products and
third-party AI components. Security design review is a lifecycle gate, and
deviations from approved patterns go through tracked exceptions. The AI
gateway is the standard path for model access, inputs and outputs. Pattern
adoption and review findings are measured.

**Practices**
- Publish reference architectures for common AI application types (RAG
  assistant, copilot, classification service, tool-using agent) with required
  controls built in.
- Maintain a catalog of approved patterns for limiting injection impact, such
  as dual-LLM (a quarantined model handles untrusted content and returns only
  constrained data to a privileged model), plan-then-execute (the plan is
  fixed before untrusted content is read), action-selector and
  context-minimization patterns, with guidance on when each applies.
- Make AI security design review a mandatory gate for new AI systems and
  material changes (new model, new tool, new data source).
- Require AI inference to flow through the approved gateway (APP-3) so input,
  output and logging controls apply consistently.
- Track exceptions to approved patterns with an owner and expiry.
- [Agentic] Require an approved agent pattern that separates untrusted-content
  processing from privileged tool execution for every agent that can take
  state-changing actions.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-4.A.1` | Reference architectures and pattern catalog | `Doc` | All | Published, versioned reference architectures covering each AI application type in use and a pattern catalog describing when each injection-limiting pattern applies. |
| `APP-4.A.2` | Design review lifecycle gate | `Tech` | All | Lifecycle or pipeline configuration requiring a completed AI design review before production release and on material change, plus one example of a held release. |
| `APP-4.A.3` | Pattern conformance records | `Rec` | All | For each sampled system, a record identifying the reference architecture or pattern used, or an exception register entry with owner and expiry. |
| `APP-4.A.4` | Design review metrics | `Rec` | All | Report, at least quarterly, of review coverage, common findings, open exceptions and overdue exceptions. |
| `APP-4.A.5` | Agent pattern conformance test | `Test` | Agentic | For each sampled state-changing agent, a test showing that content processed by the untrusted-content component cannot directly trigger a privileged tool call. |

### Optimal
Secure architecture is enforced automatically and improves from evidence.
Platform guardrails (golden paths, templates and policy-as-code) make approved
patterns the default and detect drift from them in running systems. Red-team
results and incidents are analyzed for architectural root causes, and patterns
are updated accordingly. The organization can show that architectural
controls contained successful model manipulation during exercises.

**Practices**
- Provide golden-path templates that implement approved patterns by default.
- Detect architectural drift automatically (e.g., direct provider calls
  bypassing the gateway, agents gaining new tools without review).
- Perform root-cause analysis of red-team findings and incidents at the
  architecture level and update patterns and reference architectures.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `APP-4.O.1` | Golden-path adoption | `Tech` | All | Templates implementing approved patterns, with data showing the share of production AI systems built from them (target set and trend reported). |
| `APP-4.O.2` | Architecture drift detection | `Tech` | All | Automated checks detecting gateway bypass and unreviewed capability changes, with a detection observed by the assessor or recorded in the last 90 days. |
| `APP-4.O.3` | Blast-radius validation | `Test` | All | Red-team exercise or incident within 12 months in which the model was successfully manipulated and architectural controls prevented or limited the impact, with the result documented. |
| `APP-4.O.4` | Pattern improvement log | `Rec` | All | Updates to reference architectures and patterns over the last 12 months, each traced to a red-team finding, incident or threat-intelligence source. |
