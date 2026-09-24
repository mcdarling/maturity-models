# Cross-Cutting Capabilities

Cross-cutting capabilities span every dimension of the model. As in the CISA
Zero Trust Maturity Model, where Visibility & Analytics, Automation &
Orchestration and Governance run across all pillars, these capabilities determine
whether the controls in the six AISMM dimensions can be seen, acted on and
enforced at scale. A strong guardrail (APP-1) is of limited value if nobody sees
it fire; a well-scoped agent (AGT-2) is still a risk if nobody can stop it when it
misbehaves. Assessors rate each cross-cutting capability **once for the
organization**, not per dimension. To do so, they sample evidence across
dimensions and profiles, and the capability's stage is limited by the weakest
area sampled. Governance is not repeated here because it is covered in full by
Dimension 1 (GOV-1 to GOV-5).

| ID | Capability | Applies to |
|---|---|---|
| VIS | Visibility, Monitoring & Detection | ML · LLM · Agentic |
| IR | Incident Response & Resilience | ML · LLM · Agentic |
| AUTO | Automation & Orchestration | ML · LLM · Agentic |

---

## VIS Visibility, Monitoring & Detection

**Applies to:** ML · LLM · Agentic

**Intent:** Collect the telemetry needed to understand how AI systems are used and
misused, keep it in a way that respects privacy and retention rules, and turn it
into timely detection of abuse, anomalies, drift and attacks. AI telemetry
includes prompts, completions, retrieved context, tool calls, model and version
identifiers and guardrail decisions. Detection is integrated with the security
operations center (SOC) rather than left to individual product teams.

**Key risks addressed:** Prompt injection, jailbreaks and data exfiltration that
go unnoticed; model extraction and inversion through high-volume querying;
silent model or data drift that degrades safety controls; agents taking harmful
actions that cannot be reconstructed or attributed; AI telemetry that itself
becomes an unprotected store of sensitive data.

**References:** NIST AI RMF (MEASURE, MANAGE); MITRE ATLAS (adversary tactics and
techniques against AI systems); OWASP Top 10 for LLM Applications (prompt
injection, sensitive information disclosure, excessive agency, unbounded
consumption); CISA ZTMM (Visibility & Analytics cross-cutting capability).

### Traditional
AI systems produce only the generic application and infrastructure logs that any
software would. Prompts, model outputs and guardrail decisions are either not
logged or logged inconsistently by individual developers, often including
sensitive data with no retention rule. The SOC has no AI-specific detection
content and does not know which systems are AI. Misuse is discovered through user
complaints or by chance.

### Initial
High-risk AI systems produce defined AI telemetry that is sent to a central log
platform. There is a documented logging standard stating which fields are
captured, how sensitive content is masked or minimized, and how long records are
retained. The SOC receives a small set of AI-specific alerts, such as guardrail
block spikes or unusual query volume, and has a basic procedure for triaging
them. Detection content is still largely hand-written and reviewed manually.

**Practices**
- Define an AI logging standard covering required fields, masking of sensitive
  data and retention periods consistent with DATA-3.
- Send AI telemetry from high-risk systems to the central log platform or SIEM,
  tagged with the GOV-1 inventory ID.
- Deploy an initial set of AI detection rules (e.g., volume anomalies, repeated
  guardrail blocks, known jailbreak signatures) and route alerts to the SOC.
- Train SOC analysts on AI-specific alert triage.
- [ML] Monitor input and prediction distributions for drift on high-risk models
  and alert on threshold breaches.
- [LLM] Log prompts, completions, retrieved context references (DATA-4) and
  guardrail decisions (APP-1, APP-2), with the model provider and version.
- [Agentic] Log every tool call with its arguments, result status, the agent
  identity (AGT-1) and the human or service principal on whose behalf it acted.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `VIS.I.1` | AI logging and retention standard | `Doc` | All | Approved standard listing required telemetry fields per profile, masking/minimization rules for sensitive data, access restrictions on AI logs and retention periods aligned to DATA-3. |
| `VIS.I.2` | Central AI telemetry feed | `Tech` | All | Log platform/SIEM configuration or query output showing telemetry received from every high-risk AI system within the last 7 days, each event tagged with the GOV-1 inventory ID. |
| `VIS.I.3` | AI detection rule set | `Tech` | All | At least 5 enabled AI-specific detection rules in the SIEM or monitoring platform, each with an owner, severity and linked triage procedure. |
| `VIS.I.4` | AI alert triage records | `Rec` | All | SOC tickets for at least 3 AI alerts (real or test) in the last 90 days, showing triage decision, analyst and closure reason. |
| `VIS.I.5` | Drift monitoring configuration | `Tech` | ML | For each high-risk model, drift metrics on inputs and predictions with defined thresholds and an alert destination. |
| `VIS.I.6` | LLM interaction telemetry sample | `Tech` | LLM | Sample records for each high-risk LLM system showing prompt, completion (or masked equivalent), retrieved-context references, guardrail decision and model version. Sampled records show masking applied as the standard requires. |
| `VIS.I.7` | Agent action trace sample | `Tech` | Agentic | Sample records for each high-risk agent showing every tool call with arguments, outcome, agent identity and originating principal, with no calls missing from a traced session. |

### Advanced
Telemetry covers **all** in-scope AI systems, including third-party AI services
accessed through the AI gateway. Telemetry is standardized in a common schema so
the SOC can query across systems and providers. Detection content is mapped to
MITRE ATLAS techniques, version-controlled and tested before release. The
organization detects model extraction, abuse and drift in addition to basic
guardrail events, and measures detection performance. Access to AI logs is
itself monitored, because they may contain sensitive prompts and outputs.

**Practices**
- Adopt a common AI telemetry schema (e.g., based on OpenTelemetry generative AI
  semantic conventions) for all in-scope systems and providers.
- Route third-party and SaaS AI usage through the AI gateway (APP-3, INF-4) so it
  is logged in the same schema.
- Map detection rules to MITRE ATLAS techniques and track coverage gaps.
- Keep detection content in version control and test each rule against sample
  attack data before deployment.
- Detect model extraction and inversion patterns (high-volume, systematic or
  boundary-probing queries) on exposed inference endpoints.
- Monitor and alert on access to AI telemetry stores.
- Track and report mean time to detect (MTTD) and false-positive rates for AI
  alerts to the governance body (GOV-5).
- [LLM] Detect indirect prompt injection indicators in retrieved content and
  tool outputs, not just in user prompts.
- [Agentic] Correlate multi-step agent sessions into a single trace so a
  sequence of individually benign actions can be evaluated as a whole.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `VIS.A.1` | Telemetry coverage report | `Tech` | All | Report reconciled to the GOV-1 inventory showing ≥ 95% of in-scope AI systems, including third-party AI services, sending telemetry in the common schema, with gaps tracked to remediation. |
| `VIS.A.2` | ATLAS coverage map | `Doc` | All | Detection content mapped to MITRE ATLAS techniques relevant to the organization's profiles, with uncovered techniques listed and either accepted or scheduled. Reviewed within 12 months. |
| `VIS.A.3` | Detection content repository | `Tech` | All | Version-controlled repository of AI detection rules with change history, peer review on each change and test cases attached to each rule. |
| `VIS.A.4` | Detection validation results | `Test` | All | Results from replaying attack samples (e.g., jailbreaks, extraction patterns, injection payloads) against the rule set within the last 12 months, with detection rate per technique and failures remediated. |
| `VIS.A.5` | AI detection metrics report | `Rec` | All | Quarterly report to the governance body with MTTD, alert volume, false-positive rate and telemetry coverage, showing at least two consecutive reporting periods. |
| `VIS.A.6` | Telemetry access monitoring | `Tech` | All | Configuration showing access to AI log stores is restricted to named roles and that access events are logged and alerted on outside approved roles. |
| `VIS.A.7` | Agent session correlation | `Tech` | Agentic | SIEM or tracing output showing complete multi-step agent sessions reconstructed by trace ID, including delegated sub-agent calls (AGT-5), for each sampled agent. |

### Optimal
Visibility is continuous across the entire AI estate, including shadow AI found
through GOV-1 discovery. Detection is behavioral and adaptive: baselines are
learned per system, new ATLAS techniques and threat intelligence are turned into
detection content quickly, and red-team findings (MDL-3) automatically become
detection test cases. The organization can show that detections work against
realistic adversaries and continuously improves MTTD.

**Practices**
- Maintain per-system behavioral baselines for usage, cost, output and tool-use
  patterns, and alert on deviations.
- Convert AI threat intelligence and new ATLAS techniques into tested detection
  content within a defined time.
- Feed every MDL-3 red-team finding into the detection test suite.
- Run purple-team exercises where red-team activity is measured against live
  detection.
- [Agentic] Evaluate agent action sequences against intended task scope in
  near real time and alert on out-of-scope behavior.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `VIS.O.1` | Behavioral baselining in production | `Tech` | All | Baselines and anomaly alerts active for all production AI systems, observed by the assessor raising an alert during the assessment. |
| `VIS.O.2` | Threat-intel-to-detection records | `Rec` | All | Records showing new AI threat intelligence or ATLAS techniques converted into tested detection content within a target time (e.g., ≤ 30 days), for at least 3 items in the last 12 months. |
| `VIS.O.3` | Purple-team detection results | `Test` | All | Exercise within the last 12 months measuring detection of red-team AI attacks, with ≥ 90% of executed techniques detected and an achieved MTTD at or below target (e.g., ≤ 1 hour for high-severity). |
| `VIS.O.4` | Detection improvement log | `Rec` | All | Metric trends for MTTD, coverage and false-positive rate over at least 4 quarters, with documented changes made in response. |
| `VIS.O.5` | Agent scope-deviation detection | `Test` | Agentic | Test showing an agent deliberately driven outside its task scope (e.g., through injected instructions) generated an alert within target time (e.g., ≤ 5 minutes). |

---

## IR Incident Response & Resilience

**Applies to:** ML · LLM · Agentic

**Intent:** Prepare for, respond to and recover from AI security incidents with
defined categories, AI-specific playbooks, the technical means to contain an AI
system quickly and the ability to preserve evidence and meet disclosure
obligations. Lessons from incidents feed back into testing and controls so the
same failure does not recur.

**Key risks addressed:** Slow or improvised response to prompt injection,
data leakage, model poisoning or agent misbehavior; inability to stop or roll
back a compromised model or agent; loss of forensic evidence; missed regulatory
notification deadlines; single points of failure in AI providers; repeated
incidents because lessons are not captured.

**References:** NIST SP 800-61 (incident handling lifecycle); NIST AI RMF
(MANAGE); MITRE ATLAS (case studies and techniques to inform playbooks); OWASP
Top 10 for LLM Applications and OWASP guidance on agentic AI threats; EU AI Act
(serious incident reporting for high-risk AI systems); CISA ZTMM (cross-cutting
capabilities).

### Traditional
AI incidents are handled through the general IT incident process, if they are
recognized as incidents at all. There is no definition of what makes an AI
incident, no AI-specific playbook and no tested way to disable a model or agent
quickly. Evidence such as prompts, model versions and agent traces is not
preserved. Regulatory notification duties for AI are not identified.

### Initial
The organization has defined what counts as an AI incident and has added AI
categories to its incident taxonomy. Playbooks exist for the most likely AI
incident types affecting high-risk systems. High-risk systems have a documented
way to be disabled or rolled back, and the IR team knows who owns each system.
At least one AI tabletop exercise has been run.

**Practices**
- Define AI incident types and severity criteria and add them to the
  organization's incident taxonomy.
- Write playbooks for priority scenarios: prompt injection compromise, data
  leakage through a model, poisoned or tampered model, agent misbehavior, and
  AI provider outage or compromise (INF-4).
- Document a disable or rollback procedure for each high-risk AI system.
- Identify AI-related notification obligations (e.g., EU AI Act serious incident
  reporting, data protection breach notification) and who decides on them
  (GOV-4).
- Define which AI evidence must be preserved during an incident (telemetry from
  VIS, model and prompt versions, retrieval sources, agent traces).
- Run at least one AI tabletop exercise per year.
- [ML] Keep previous validated model versions available for rollback (MDL-4).
- [Agentic] Document how to revoke an agent's credentials and tool access
  (AGT-1, AGT-2, INF-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `IR.I.1` | AI incident taxonomy and severity criteria | `Doc` | All | Incident taxonomy includes AI-specific categories and severity criteria, approved and integrated into the organization's main IR plan. |
| `IR.I.2` | AI incident playbooks | `Doc` | All | Playbooks covering at least prompt injection compromise, data leakage via model, poisoned/tampered model, agent misbehavior (if agents are in use) and provider outage/compromise, each with roles, containment steps and evidence to preserve. |
| `IR.I.3` | Disable/rollback procedures | `Doc` | All | For each high-risk AI system, a documented procedure naming the owner, the mechanism to disable or roll back, and the expected time to execute. |
| `IR.I.4` | Notification obligations register | `Doc` | All | Register mapping AI incident types to applicable notification obligations (regulatory, contractual, data protection), deadlines and decision owner. |
| `IR.I.5` | AI tabletop after-action report | `Test` | All | Report from a tabletop within the last 12 months using an AI scenario, listing participants, gaps found and remediation actions with owners. |
| `IR.I.6` | Model rollback readiness | `Tech` | ML | For each high-risk model, registry output showing at least one prior validated version retained and deployable. |
| `IR.I.7` | Agent credential revocation procedure | `Doc` | Agentic | For each high-risk agent, steps and responsible role for revoking its credentials, tokens and tool/MCP access. |

### Advanced
AI incident response is consistent across **all** in-scope AI systems and
integrated with the enterprise IR process and SOC. Kill switches and rollback
are technical controls that have been tested, not only documented. Evidence
preservation is standardized, notification decisions are recorded, and every AI
incident produces a post-incident review whose findings are tracked. Lessons
learned are turned into new adversarial test cases (MDL-3) and detection
content (VIS).

**Practices**
- Implement kill switches for all production AI systems, for example at the AI
  gateway, feature flag or serving layer, operable by the on-call team.
- Test rollback and kill switches on a defined schedule.
- Preserve AI evidence with integrity protection and legal hold capability.
- Run post-incident reviews for every AI incident of defined severity and track
  actions to closure.
- Add each incident's attack pattern to the MDL-3 test suite.
- Maintain fallback or degraded-mode plans for critical dependencies on external
  AI providers (INF-4).
- Track time to contain and time to recover for AI incidents.
- [Agentic] Kill switches can halt a running agent mid-task, cancel queued
  actions and revoke delegated credentials in one operation.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `IR.A.1` | Kill switch configuration | `Tech` | All | Configuration showing a kill switch for every sampled production AI system, operable by the on-call role without a code deployment. |
| `IR.A.2` | Kill switch and rollback test records | `Test` | All | Test within the last 6 months for each sampled system showing the kill switch or rollback executed and effective within the documented target (e.g., ≤ 15 minutes). |
| `IR.A.3` | AI incident records | `Rec` | All | IR tickets for AI incidents (or exercises, if none occurred) in the last 12 months, showing AI category, severity, timeline, evidence preserved and notification decision recorded. |
| `IR.A.4` | Post-incident reviews and actions | `Rec` | All | A post-incident review for every AI incident at or above the defined severity, with actions tracked; ≥ 80% of actions closed by their due date. |
| `IR.A.5` | Lessons-to-tests traceability | `Rec` | All | For each reviewed incident, a link to the MDL-3 test case or VIS detection rule created from it. |
| `IR.A.6` | AI incident response metrics | `Rec` | All | Report to the governance body with mean time to contain (MTTC) and mean time to recover (MTTR) for AI incidents, against defined targets, for at least two reporting periods. |
| `IR.A.7` | Provider failover plan and test | `Test` | LLM | For each LLM system dependent on an external provider and rated business-critical, a documented fallback (alternate model, degraded mode or safe shutdown) exercised within the last 12 months. |
| `IR.A.8` | Agent halt test | `Test` | Agentic | Test showing a running agent halted mid-task, pending actions cancelled and credentials revoked, with no further tool calls observed after the halt. |

### Optimal
AI incident response is automated where possible and proven under realistic
pressure. Detections trigger containment automatically for well-understood
scenarios. Full-scale exercises involving technical, legal, communications and
provider contacts are run regularly. The organization demonstrates improvement
in response times and shows that incidents lead to measurable changes in
controls across dimensions.

**Practices**
- Automate containment for high-confidence AI incident types (e.g., isolate an
  agent, block a user or key at the gateway, roll back a model) through AUTO.
- Run live or simulation-based exercises that inject a realistic AI attack into
  a production-like environment.
- Include critical AI providers in joint exercises or verify their response
  commitments.
- Analyze incidents across systems for systemic causes and feed them into policy
  (GOV-3) and architecture (APP-4) changes.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `IR.O.1` | Automated containment | `Tech` | All | Automated containment actions configured for at least the top 3 AI incident types, observed by the assessor firing in a test. |
| `IR.O.2` | Live AI incident exercise | `Test` | All | Exercise within the last 12 months injecting a realistic AI attack into a production-like environment, including legal and communications roles, meeting MTTC and MTTR targets. |
| `IR.O.3` | Notification timeliness evidence | `Test` | All | Exercise or real-incident record showing a regulatory notification decision (e.g., EU AI Act serious incident) made and a draft notification ready within the applicable deadline. |
| `IR.O.4` | Systemic improvement log | `Rec` | All | Trend of MTTC/MTTR over at least 4 quarters and documented control, policy or architecture changes made across dimensions as a result of incident analysis. |
| `IR.O.5` | Critical provider response verification | `Rec` | LLM | For each critical external AI provider, records of a joint exercise or a verified contractual incident notification commitment, tested at least once. |

---

## AUTO Automation & Orchestration

**Applies to:** ML · LLM · Agentic

**Intent:** Enforce AI security controls consistently and at speed by expressing
them as code, building security evaluations into the delivery pipeline for
models, prompts and agents, enforcing policy centrally at an AI gateway and
automating response. The organization measures how much of its control set is
automated so that coverage does not depend on manual effort.

**Key risks addressed:** Controls that are applied inconsistently or bypassed
under delivery pressure; unsafe model, prompt or agent changes reaching
production untested; slow manual response giving attackers time to act;
fragmented guardrails across teams and providers; overestimating control
coverage.

**References:** NIST AI RMF (MANAGE, MEASURE); CISA ZTMM (Automation &
Orchestration cross-cutting capability); OWASP Top 10 for LLM Applications;
OWASP AI security guidance; NIST SP 800-61 (use of automation in incident
handling).

### Traditional
AI security controls are applied manually by individual teams, if at all.
Guardrails are configured separately in each application, and there is no
central enforcement point for AI traffic. Model, prompt and agent changes go to
production without automated security testing. Response actions are performed
by hand.

### Initial
The organization has started to automate the most important AI controls for
high-risk systems. Some guardrail and access policies are defined as code, at
least one automated security evaluation runs before high-risk model or prompt
changes are released, and a central AI gateway or proxy exists for at least
some AI traffic. Automation is maintained by a named owner but coverage is
partial and not yet measured.

**Practices**
- Define key guardrail and AI access policies as version-controlled code or
  configuration rather than manual console settings.
- Run automated security evaluations (e.g., jailbreak and injection test sets,
  robustness checks) in CI/CD for high-risk systems before release (MDL-2,
  MDL-3).
- Route high-risk LLM traffic through a central AI gateway that applies common
  guardrails, authentication and logging (APP-3).
- Automate at least one simple AI response action, such as blocking an API key or
  user at the gateway.
- [ML] Run automated robustness and data validation checks in the training
  pipeline for high-risk models.
- [LLM] Treat system prompts and guardrail configurations as versioned artifacts
  that trigger the evaluation suite when changed.
- [Agentic] Define agent tool permissions as code and validate them in CI
  against the approved permission set (AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AUTO.I.1` | Policy-as-code repository | `Tech` | All | Version-controlled repository containing guardrail and AI access policies for high-risk systems, with change history and review. |
| `AUTO.I.2` | CI/CD security evaluation stage | `Tech` | All | Pipeline definitions showing an automated security evaluation step for each high-risk AI system, with defined pass/fail thresholds. |
| `AUTO.I.3` | Evaluation run results | `Test` | All | Results from the last 3 releases of each high-risk system showing the evaluation ran and passed, or failed and was remediated before release. |
| `AUTO.I.4` | AI gateway configuration | `Tech` | LLM | Gateway configuration showing high-risk LLM traffic routed through it, with authentication, guardrails and logging enabled. |
| `AUTO.I.5` | Automated response action | `Tech` | All | Configuration for at least one automated AI response action, and a record of it executing (real or test) within the last 12 months. |
| `AUTO.I.6` | Prompt and guardrail change triggers | `Tech` | LLM | Pipeline configuration showing that a change to a system prompt or guardrail configuration triggers the security evaluation suite. |
| `AUTO.I.7` | Agent permission validation | `Tech` | Agentic | CI check that compares each high-risk agent's declared tool permissions to the approved set and fails on unapproved additions. |

### Advanced
Automation is standard across **all** in-scope AI systems. Security evaluation
gates block releases of models, prompts and agents that fail defined thresholds,
and exceptions go through a tracked process. The AI gateway is the enforced path
for AI traffic, including to third-party providers, and direct access is blocked.
Common AI incident responses are orchestrated through SOAR playbooks. The
organization measures automation coverage and reports it.

**Practices**
- Make security evaluation a blocking gate for every production release of a
  model, prompt, guardrail or agent configuration.
- Manage gate exceptions through a tracked, time-limited approval process.
- Enforce the AI gateway as the only permitted path to AI providers, blocking
  direct egress (INF-4).
- Orchestrate common AI response actions (block, rate limit, rollback, revoke
  credentials) through SOAR playbooks linked to VIS alerts and IR playbooks.
- Maintain a control automation register showing which AISMM controls are
  automated, partially automated or manual.
- [Agentic] Enforce agent tool authorization policies at runtime through a
  central policy engine, not in each agent's code.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AUTO.A.1` | Blocking evaluation gates | `Tech` | All | Pipeline policy showing security evaluation gates are mandatory and blocking for all in-scope systems, plus at least one example of a blocked release in the last 12 months. |
| `AUTO.A.2` | Gate exception register | `Rec` | All | Register of gate overrides with approver, justification and expiry; no expired exceptions left open. |
| `AUTO.A.3` | Gateway enforcement | `Tech` | LLM | Network or egress configuration showing direct access to external AI provider endpoints is blocked except through the gateway, and gateway coverage ≥ 95% of in-scope LLM traffic. |
| `AUTO.A.4` | SOAR AI playbooks | `Tech` | All | At least 3 SOAR playbooks for AI response actions, each linked to a VIS detection and an IR playbook. |
| `AUTO.A.5` | SOAR execution records | `Rec` | All | Execution logs for each AI SOAR playbook (real or test) within the last 6 months, showing time from alert to action. |
| `AUTO.A.6` | Control automation register | `Rec` | All | Register covering all AISMM elements in scope, classifying each control as automated, partial or manual, with coverage percentage reported to the governance body at least quarterly. |
| `AUTO.A.7` | Central agent policy enforcement | `Tech` | Agentic | Policy engine configuration showing tool authorization decisions for all in-scope agents are made centrally, with decision logs sent to VIS. |

### Optimal
AI security controls are enforced and verified automatically across the entire
AI estate. Policy changes roll out everywhere from a single source, gates adapt
as new threats and red-team findings add test cases, and routine response is
closed-loop without human action. The organization continuously tests that its
automation works and uses automation coverage metrics to drive improvement.

**Practices**
- Propagate policy changes from a single source to all gateways, pipelines and
  agent policy engines, with drift detection on deployed configuration.
- Update evaluation gates automatically as new MDL-3 findings and threat
  intelligence add test cases.
- Run closed-loop remediation for well-understood issues (e.g., auto-rollback on
  a failed post-deployment evaluation).
- Continuously test automated controls with synthetic attacks and alert when a
  control fails to fire.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `AUTO.O.1` | Policy drift detection | `Tech` | All | Configuration detecting and alerting on (or auto-reverting) divergence between deployed AI policies and the policy-as-code source, observed by the assessor during the assessment. |
| `AUTO.O.2` | Continuous control validation | `Test` | All | Synthetic attack tests run at least weekly against gateways, gates and agent policy engines, with results showing controls fired and failures alerted. |
| `AUTO.O.3` | Closed-loop remediation | `Tech` | All | At least one closed-loop remediation (e.g., auto-rollback on failed post-deployment evaluation) configured and observed executing without manual intervention. |
| `AUTO.O.4` | Automation coverage trend | `Rec` | All | Automation coverage metrics over at least 4 quarters, showing ≥ 80% of applicable controls automated and documented actions to close the remaining gaps. |

---
