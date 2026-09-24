# Dimension 3 — Model Security

Model security covers the model itself as a security-relevant asset: where it comes
from, how it is built and promoted, how it holds up under attack and how its
weights, prompts and other artifacts are protected. A model is both executable
code and a store of valuable (and sometimes sensitive) information. It can carry
malicious payloads in, and it can leak data or intellectual property out. This
dimension depends on the AI inventory (GOV-1) and risk classification (GOV-2) for
scope, and on the data controls in DATA-1 and DATA-2 for what goes into a model.

| ID | Element | Applies to |
|---|---|---|
| MDL-1 | Model Supply Chain & Provenance | ML · LLM · Agentic |
| MDL-2 | Secure ML Pipeline (MLOps / LLMOps) | ML · LLM · Agentic |
| MDL-3 | Adversarial Testing & Red Teaming | ML · LLM · Agentic |
| MDL-4 | Model Artifact Protection | ML · LLM · Agentic |

---

## MDL-1 Model Supply Chain & Provenance

**Applies to:** ML · LLM · Agentic

**Intent:** Ensure every model the organization uses (third-party, open-weight,
fine-tuned or hosted by a provider) comes from a vetted source, has verifiable
provenance and integrity, is free of known malicious content and is pinned to a
known version, so that a compromised or silently changed model cannot enter
production.

**Key risks addressed:** Malicious code embedded in serialized model files (for
example, pickle-based formats that execute on load); backdoored or poisoned
open-weight models; typosquatted or impersonated repositories on model hubs;
tampering with model files between source and deployment; hosted models changing
behavior without notice; inability to tell which systems are affected when a
model vulnerability is disclosed.

**References:** NIST AI RMF (MAP, MANAGE: third-party risk); NIST SP 800-218A
(Secure Software Development Practices for Generative AI and Dual-Use Foundation
Models); SLSA (build provenance and integrity levels); OpenSSF Model Signing
specification; CycloneDX ML-BOM and SPDX 3.0 AI profile; MITRE ATLAS (ML supply
chain compromise techniques); OWASP Top 10 for LLM Applications 2025 (LLM03
Supply Chain, LLM04 Data and Model Poisoning).

### Traditional
Models are downloaded from public hubs or selected from provider catalogs by
individual engineers based on performance or convenience. Nobody checks who
published a model, whether the file has been altered, or whether it contains
executable code. Serialized files in unsafe formats are loaded directly. Hosted
models are called by a floating alias such as "latest", so the model in use can
change without anyone noticing. There is no record of which model versions are in
which systems.

### Initial
The organization has a defined procedure for approving models before they are used
in high-risk or production systems. Approval covers the publisher's reputation,
license, model card and known issues. Model files from outside the organization
are scanned for embedded code before they are loaded, and safe serialization
formats are preferred. Hosted model versions are pinned for production. Each
high-risk system records the models it uses and where they came from.

**Practices**
- Maintain an approved-sources list (model hubs, publishers, providers) and a
  model intake procedure with a named approver.
- Scan third-party model files for malicious code and unsafe deserialization
  before first load, in an isolated environment (INF-1).
- Prefer non-executable formats (for example, safetensors or ONNX) and require a
  documented exception to load pickle-based formats.
- Verify checksums or signatures published by the model source where available.
- [ML] Record the framework, library versions and pre-trained base model (if any)
  for each production model.
- [LLM] Pin hosted model versions in production configuration and record the
  provider's deprecation dates; treat a version change as a model change under
  MDL-2.
- [LLM] Record the base model and the source of any adapters (for example, LoRA)
  applied to it.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-1.I.1` | Model intake and approval procedure | `Doc` | All | Defines approved sources, vetting criteria (publisher, license, model card, known vulnerabilities, format), the approver role and the exception process for unsafe formats. |
| `MDL-1.I.2` | Model approval records | `Rec` | All | An approval record for every third-party or open-weight model used by a high-risk system, showing the reviewer, date, source, version/hash and decision. |
| `MDL-1.I.3` | Model file scan results | `Test` | All | Scanner output for each externally sourced model file in high-risk systems, run before first load, with no unresolved findings of executable or malicious content. |
| `MDL-1.I.4` | Format exceptions | `Rec` | All | Every production use of a pickle-based or other code-executing format has an approved exception with justification and compensating controls; none are missing. |
| `MDL-1.I.5` | Model provenance record | `Tech` | All | For each high-risk system, the inventory (GOV-1) or registry shows each model's source, version or content hash, and date obtained. |
| `MDL-1.I.6` | Pinned hosted model configuration | `Tech` | LLM | Production configuration for each sampled LLM system references an explicit, dated model version or snapshot, not a floating alias. |

### Advanced
Supply chain controls apply to **all** in-scope AI systems, including models
consumed through third-party services. Model intake is automated and enforced:
models can only be pulled from an internal mirror or approved registry, and the
pipeline refuses unsigned, unscanned or unapproved models. Every production system
has an AI-BOM that is regenerated at each release. The organization monitors its
model sources for vulnerabilities, revocations and upstream changes.

**Practices**
- Route all model downloads through an internal proxy, mirror or registry; block
  direct pulls from public hubs in build and production environments.
- Sign approved models (for example, using the OpenSSF Model Signing
  specification) and verify signatures at pipeline and deployment time.
- Run model file scanning automatically on every intake and every new version.
- Generate an AI-BOM per system in a standard format and link it to the
  inventory (GOV-1).
- Subscribe to advisories for model hubs, frameworks and providers, and triage
  them against the AI-BOM.
- [LLM] Run a regression evaluation (behavior and safety, see MDL-3) before
  moving to a new hosted model version, including provider-initiated upgrades.
- [Agentic] Include tool/MCP server packages and agent framework versions in the
  AI-BOM alongside models.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-1.A.1` | Model source enforcement | `Tech` | All | Egress, proxy or registry configuration that blocks model downloads from unapproved sources in build and production environments, plus one example of a blocked pull. |
| `MDL-1.A.2` | Signature verification gate | `Tech` | All | Pipeline or admission policy that rejects unsigned models or models whose signature or hash does not match the registry entry, with one example rejection or test run. |
| `MDL-1.A.3` | Automated scan configuration | `Tech` | All | Scanning runs on every model intake and version change; the pipeline fails on high-severity findings. Scan logs cover 100% of sampled models. |
| `MDL-1.A.4` | AI-BOMs | `Tech` | All | An AI-BOM in CycloneDX ML-BOM or SPDX AI format for each sampled production system, regenerated at the latest release and listing model versions/hashes, base models, adapters and key libraries. |
| `MDL-1.A.5` | Advisory triage records | `Rec` | All | Records showing model, framework and provider advisories were matched against AI-BOMs and triaged within a defined SLA; at least one triage within the last quarter. |
| `MDL-1.A.6` | Hosted model upgrade evaluations | `Test` | LLM | For each hosted model version change in the last 12 months, a regression and safety evaluation completed and approved before production cutover. |
| `MDL-1.A.7` | Agent component BOM entries | `Tech` | Agentic | AI-BOMs for sampled agents list agent framework, tool/MCP server packages and versions, cross-referenced to AGT-2 registrations. |

### Optimal
Model provenance is verified end to end and continuously. Every model in the
estate, including those in supplier products, has verifiable provenance back to its
training or publication source. Runtime environments verify model integrity at
load, not only at deployment. When a model, hub or provider is found to be
compromised, the organization identifies every affected system and can roll back
or block quickly. Supplier model provenance requirements are contractual and
checked.

**Practices**
- Require build provenance attestations (for example, SLSA-style) for internally
  trained and fine-tuned models, and verify them at deployment.
- Verify model hashes or signatures at every load in serving environments (INF-2)
  and alert on mismatch (VIS).
- Continuously re-scan the model registry as scanner rules and threat intelligence
  change.
- Include model provenance and version-change notification requirements in
  supplier contracts (INF-4) and verify compliance.
- Run model compromise drills measuring time to identify and contain affected
  systems.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-1.O.1` | Provenance attestations | `Tech` | All | Every sampled internally trained or fine-tuned model has a signed provenance attestation linking it to its pipeline run, source code revision and dataset versions (DATA-1), verified at deployment. |
| `MDL-1.O.2` | Load-time integrity verification | `Test` | All | Assessor observes a tampered or unsigned model being refused at load in a serving environment, with an alert raised to monitoring. |
| `MDL-1.O.3` | Continuous re-scan records | `Rec` | All | Registry-wide re-scans at least monthly and after scanner rule updates, with findings triaged and trend metrics reported. |
| `MDL-1.O.4` | Model compromise drill | `Test` | All | A drill within the last 12 months that identified all systems using a simulated compromised model or hub within target time (e.g., ≤ 24 hours) and contained them, with improvements logged. |
| `MDL-1.O.5` | Supplier provenance compliance | `Rec` | All | For each critical AI supplier, contract clauses on model provenance and version-change notice, plus a verification record within the last 12 months. |

---

## MDL-2 Secure ML Pipeline (MLOps / LLMOps)

**Applies to:** ML · LLM · Agentic

**Intent:** Build, train, fine-tune, evaluate and deploy models and their
configuration (prompts, system prompts, guardrail settings) through hardened,
reproducible pipelines with controlled promotion, so that no unreviewed or
tampered model or configuration reaches production.

**Key risks addressed:** Tampering with training jobs, code, data or artifacts in
the pipeline; compromised pipeline credentials; untraceable models that cannot be
rebuilt or investigated; unreviewed changes to system prompts or guardrail
configurations that silently weaken controls; models promoted without passing
security evaluation.

**References:** NIST AI RMF (MANAGE); NIST SP 800-218A (Secure Software
Development Practices for Generative AI and Dual-Use Foundation Models); SLSA
(build integrity and provenance); MITRE ATLAS (ML supply chain and pipeline
compromise techniques); OWASP Top 10 for LLM Applications 2025 (LLM04 Data and
Model Poisoning, LLM07 System Prompt Leakage).

### Traditional
Models are trained in notebooks or on individual workstations and copied to
production by hand. There is no record of which code, data or hyperparameters
produced a given model. Prompts and system prompts are edited directly in
production configuration or application code without review. Pipeline credentials
are shared and broadly privileged. Nobody can rebuild the model that is currently
running.

### Initial
High-risk models are built and deployed through a defined pipeline rather than by
hand. Models are stored in a model registry with versioning, and promotion to
production requires a documented approval. Changes to system prompts and guardrail
configurations are version-controlled and reviewed. Pipeline access is restricted
to named roles.

**Practices**
- Store models in a registry with versions, owners and stage (for example,
  development, staging, production).
- Require a recorded approval before a model version is promoted to production.
- Keep training/fine-tuning code, configuration and pipeline definitions in
  version control.
- Restrict who can run training jobs, write to the registry and deploy models;
  store pipeline secrets in a secrets manager (INF-3).
- [ML] Record the dataset version, code revision and hyperparameters for each
  production model.
- [LLM] Manage system prompts, prompt templates and guardrail configurations as
  versioned artifacts with peer review before release.
- [Agentic] Manage agent instructions and tool configuration the same way, with
  review of any change to tool access (AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-2.I.1` | Model registry export | `Tech` | All | Every production model for high-risk systems appears in the registry with version, owner, stage and link to its training/fine-tuning run or source. |
| `MDL-2.I.2` | Model promotion procedure | `Doc` | All | Defines promotion stages, required checks (including security evaluation from MDL-3) and approver roles. |
| `MDL-2.I.3` | Promotion approval records | `Rec` | All | An approval record for each production promotion of a high-risk model in the last 12 months, naming approver and checks passed. |
| `MDL-2.I.4` | Pipeline access control | `Tech` | All | IAM or RBAC export showing training, registry-write and deploy permissions limited to named roles, with no shared human accounts. |
| `MDL-2.I.5` | Training lineage records | `Rec` | ML | For each sampled production model, the dataset version, code commit and hyperparameters are recorded and retrievable. |
| `MDL-2.I.6` | Prompt and guardrail change history | `Rec` | LLM | System prompts and guardrail configs are in version control; every production change in the last 90 days has a reviewed pull request or equivalent. |

### Advanced
All in-scope models and model configurations move through standardized pipelines
with automated promotion gates. Pipelines run on hardened, isolated infrastructure
with short-lived credentials. Builds are reproducible: a production model can be
traced to, and rebuilt from, its code, data and configuration. Direct changes to
production models, prompts or guardrails are technically blocked. Pipeline
metrics are reported.

**Practices**
- Enforce promotion gates in the pipeline: registry approval, signature (MDL-1),
  passing security and safety evaluation (MDL-3) and linked risk assessment
  (GOV-2).
- Run training and fine-tuning in isolated environments with no interactive
  access to production and restricted egress (INF-1).
- Use workload identities and short-lived credentials for pipeline jobs.
- Record lineage automatically (code, data, environment, parameters) for every
  run and link it to DATA-1.
- Block out-of-band changes to production models and configurations, and detect
  drift between deployed and registered versions.
- [LLM] Run automated prompt and guardrail regression tests on every change
  before deployment.
- [Agentic] Treat changes to agent tool manifests and permission scopes as
  gated changes requiring security review.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-2.A.1` | Pipeline gate configuration | `Tech` | All | Pipeline definitions for all in-scope systems enforce registry approval, signature check and security evaluation pass before production deployment, with one example of a blocked promotion. |
| `MDL-2.A.2` | Hardened pipeline environment | `Tech` | All | IaC or configuration showing training/fine-tuning runs in isolated environments with workload identity, short-lived credentials and restricted egress. |
| `MDL-2.A.3` | Reproducibility test | `Test` | All | For at least one sampled model per profile in use, a rebuild or verification from recorded lineage within the last 12 months that matched the deployed artifact or stayed within documented tolerance. |
| `MDL-2.A.4` | Drift and out-of-band change detection | `Tech` | All | A control that compares deployed models and configurations with the registry at least daily and alerts on mismatch, with alert records from the last 90 days. |
| `MDL-2.A.5` | Pipeline metrics report | `Rec` | All | Quarterly report covering gate pass/fail rates, emergency changes and exceptions, reviewed by the model risk or AI governance owner. |
| `MDL-2.A.6` | Prompt and guardrail regression suite | `Test` | LLM | Automated regression run results for every production prompt/guardrail change in the last 90 days, with failing changes not deployed. |
| `MDL-2.A.7` | Agent configuration change reviews | `Rec` | Agentic | Security review records for every change to agent tool manifests or permission scopes in the last 12 months. |

### Optimal
The pipeline is fully policy-as-code and self-verifying. Every production model
and configuration carries verifiable build provenance, and deployment is refused
automatically without it. The pipeline itself is treated as a high-value target:
it is threat-modeled, tested against compromise and monitored. Rollback to a
known-good model or configuration is automated and exercised.

**Practices**
- Express promotion rules as policy-as-code shared across all AI pipelines, with
  versioned policies and tests.
- Produce signed provenance for every model and configuration build and verify it
  at admission (MDL-1).
- Monitor pipeline activity for anomalies (unexpected jobs, data sources,
  credential use) and feed alerts into VIS.
- Exercise automated rollback of models, prompts and guardrails, and measure time
  to restore.
- Periodically red-team the pipeline itself (for example, simulated poisoning or
  artifact substitution).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-2.O.1` | Policy-as-code repository | `Tech` | All | Versioned promotion policies with automated tests, applied to 100% of AI pipelines, with change history. |
| `MDL-2.O.2` | Pipeline compromise exercise | `Test` | All | An exercise within the last 12 months (for example, artifact substitution or injected training data) that was detected or blocked by pipeline controls, with remediation of any gaps. |
| `MDL-2.O.3` | Rollback exercise | `Test` | All | Assessor observes or reviews an automated rollback of a model or prompt/guardrail configuration completed within the target time (e.g., ≤ 1 hour). |
| `MDL-2.O.4` | Pipeline anomaly detection | `Tech` | All | Detection rules for pipeline anomalies deployed in monitoring, with at least one tested alert in the last 90 days. |

---

## MDL-3 Adversarial Testing & Red Teaming

**Applies to:** ML · LLM · Agentic

**Intent:** Test models and AI systems against realistic adversarial attacks
before deployment and on a recurring basis, use the results as release gates and
feed findings back into controls, so that the organization knows how its AI
systems fail under attack rather than finding out in production.

**Key risks addressed:** [ML] evasion through adversarial inputs, data poisoning and
backdoors, model inversion, membership inference and model extraction; [LLM]
jailbreaks, direct and indirect prompt injection, system prompt leakage and
sensitive information disclosure; [Agentic] goal hijacking, tool misuse,
privilege escalation and multi-step attack chains that combine individually
harmless actions.

**References:** NIST AI RMF (MEASURE); NIST AI 100-2 (Adversarial Machine Learning:
A Taxonomy and Terminology of Attacks and Mitigations); MITRE ATLAS; OWASP Top 10
for LLM Applications 2025 (LLM01 Prompt Injection, LLM02 Sensitive Information
Disclosure, LLM06 Excessive Agency, LLM07 System Prompt Leakage); OWASP GenAI Red
Teaming Guide; OWASP Machine Learning Security Top 10.

### Traditional
AI systems are tested for accuracy and functionality only. Any security testing is
a standard application penetration test that does not look at the model. Nobody
tries to jailbreak, inject, evade or extract the model before release. Adversarial
weaknesses are discovered by users, researchers or attackers after deployment.

### Initial
High-risk AI systems receive documented adversarial testing before first
production release. Test scope is based on the system's profile and threat model,
using a recognized taxonomy (MITRE ATLAS, NIST AI 100-2 or OWASP). Findings are
tracked to resolution or formal risk acceptance. Testers may be internal but are
not the system's own developers.

**Practices**
- Define an adversarial testing standard that sets minimum test scope per
  profile and maps test cases to a recognized taxonomy.
- Test high-risk systems before first production release and after major changes
  (new model, new tool, new data source).
- Track findings with severity, owner and due date; require documented risk
  acceptance (GOV-2) for any unresolved high-severity finding at release.
- [ML] Test at least evasion (adversarial examples) and, where the model is
  exposed to untrusted users, membership inference and extraction via the
  prediction API.
- [LLM] Test jailbreaks, direct prompt injection, indirect prompt injection
  through retrieved or uploaded content, system prompt leakage and sensitive
  information disclosure.
- [Agentic] Test goal hijacking, tool misuse and privilege escalation through
  injected instructions in tool outputs and retrieved content.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-3.I.1` | Adversarial testing standard | `Doc` | All | Defines minimum test scope per profile, mapping to MITRE ATLAS, NIST AI 100-2 or OWASP categories, tester independence requirements and triggers for retesting. |
| `MDL-3.I.2` | Pre-release test reports | `Test` | All | A report for every high-risk system, dated before its current production version was released, listing test cases, results and findings by severity. |
| `MDL-3.I.3` | Findings tracker | `Rec` | All | All findings from `MDL-3.I.2` have an owner, severity and status; unresolved high-severity findings at release have a signed risk acceptance. |
| `MDL-3.I.4` | ML attack test results | `Test` | ML | Results for evasion testing and, for externally exposed models, membership inference and extraction testing, with measured attack success rates. |
| `MDL-3.I.5` | LLM attack test results | `Test` | LLM | Results covering jailbreak, direct and indirect prompt injection, system prompt leakage and sensitive information disclosure, with at least 20 distinct test cases per category. |
| `MDL-3.I.6` | Agent attack test results | `Test` | Agentic | Results covering goal hijacking, tool misuse and privilege escalation, including at least one injection delivered through a tool output or retrieved document. |

### Advanced
Adversarial testing is part of the lifecycle for **all** in-scope AI systems.
Automated security evaluation suites run as release gates (MDL-2) with defined
pass thresholds, and are rerun on every model, prompt or tool change. Manual red
teaming supplements automation for high-risk systems on a recurring cadence.
Results are measured, trended and reported, and findings feed into detection
content and guardrails.

**Practices**
- Maintain automated security evaluation suites per profile and run them in the
  pipeline on every model, prompt, guardrail or tool change.
- Set pass/fail thresholds (for example, maximum attack success rate) per risk
  tier, and block releases that exceed them.
- Conduct manual red-team exercises on high-risk systems at least annually and
  after major changes.
- Include third-party and embedded AI in testing scope where the organization
  controls the integration (prompts, retrieval, tools).
- Convert confirmed findings into regression test cases and into detections
  (VIS) or input/output controls (APP-1, APP-2).
- [ML] Include poisoning and backdoor detection testing for models trained on
  data from external or user-contributed sources (DATA-2).
- [Agentic] Test multi-step attack chains end to end in a sandbox with realistic
  tool permissions (AGT-4), including cross-agent injection where agents
  delegate to each other (AGT-5).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-3.A.1` | Security evaluation gate | `Tech` | All | Pipeline configuration for all in-scope systems runs the security evaluation suite and enforces documented thresholds per risk tier, with one example of a blocked release. |
| `MDL-3.A.2` | Evaluation run history | `Test` | All | Evaluation results for every production change in the last 90 days for sampled systems, each within threshold or covered by an approved exception. |
| `MDL-3.A.3` | Recurring red-team reports | `Test` | All | A manual red-team report within the last 12 months for each high-risk system, including at least one third-party AI integration in scope. |
| `MDL-3.A.4` | Findings-to-controls records | `Rec` | All | For confirmed high-severity findings in the last 12 months, records showing each was added as a regression test and resulted in a control or detection change. |
| `MDL-3.A.5` | Adversarial testing metrics | `Rec` | All | Quarterly report to the governance body with coverage (% of in-scope systems tested within cadence), attack success rates by category and time to remediate findings. |
| `MDL-3.A.6` | Poisoning and backdoor tests | `Test` | ML | For models trained on external or user-contributed data, poisoning/backdoor detection results for the current production version. |
| `MDL-3.A.7` | Multi-step agent attack tests | `Test` | Agentic | End-to-end attack-chain test results in a sandbox with production-equivalent tool permissions, covering at least 3 distinct chains and any agent-to-agent delegation paths. |

### Optimal
Adversarial testing is continuous and threat-informed. Evaluation suites update
automatically from threat intelligence, new public techniques and the
organization's own incidents. Independent red teams, internal or external,
regularly test the highest-risk systems, and the organization can show that its
controls hold up against current attack techniques. Metrics show improving
resistance over time.

**Practices**
- Update evaluation suites at least quarterly from threat intelligence (MITRE
  ATLAS updates, published research, vendor advisories) and from incidents (IR).
- Run continuous or scheduled adversarial testing against production-equivalent
  systems, not only at release.
- Commission independent red teams for the highest-risk systems, and run a
  public or private disclosure / bug bounty program covering AI systems.
- Use automated attack generation (for example, adaptive or model-driven
  attackers) alongside fixed test sets.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-3.O.1` | Threat-informed suite updates | `Rec` | All | Change log showing evaluation suites updated at least quarterly, each update linked to a threat intelligence source or incident. |
| `MDL-3.O.2` | Continuous adversarial testing | `Tech` | All | Scheduled or continuous adversarial testing against production-equivalent environments for all high-risk systems, running at least weekly, with results feeding dashboards. |
| `MDL-3.O.3` | Independent red-team report | `Test` | All | An independent red-team engagement within the last 12 months on the highest-risk systems, with a retest confirming remediation of high-severity findings. |
| `MDL-3.O.4` | Adaptive attack results | `Test` | LLM | Results from automated, adaptive attack generation (not only static prompts) for sampled LLM systems, with attack success rates tracked against thresholds. |
| `MDL-3.O.5` | Resistance trend analysis | `Rec` | All | At least four quarters of attack success rate and time-to-remediate trends, with documented control improvements tied to the results. |

---

## MDL-4 Model Artifact Protection

**Applies to:** ML · LLM · Agentic

**Intent:** Protect the confidentiality and integrity of model artifacts (weights,
adapters, system prompts, proprietary evaluation sets and related configuration)
wherever they are stored, moved or served, and make it hard to steal or replicate
a model's capability through its interfaces.

**Key risks addressed:** Theft of proprietary weights or adapters; exposure of
system prompts containing business logic or embedded secrets; unauthorized
modification of weights (for example, inserting a backdoor); model extraction or
distillation through repeated querying; leakage of evaluation sets that would let
attackers tune attacks against the organization's defenses; inability to prove
ownership of a stolen model.

**References:** NIST AI RMF (MANAGE); NIST AI 100-2 (model extraction and privacy
attacks); MITRE ATLAS (model exfiltration and extraction techniques); OWASP Top 10
for LLM Applications 2025 (LLM02 Sensitive Information Disclosure, LLM07 System
Prompt Leakage, LLM10 Unbounded Consumption); NIST SP 800-218A.

### Traditional
Model weights and adapters sit in shared storage, notebooks or general-purpose
buckets alongside other files, with broad access. System prompts are treated as
ordinary application strings and sometimes contain credentials. Nobody knows who
has downloaded a model. Inference APIs have no limits that would slow extraction.
Evaluation datasets are shared freely.

### Initial
Model artifacts for high-risk systems are identified as sensitive assets and
stored in controlled locations with least-privilege access and encryption at rest.
System prompts contain no secrets. Access to weights is logged. Inference
endpoints for high-risk systems have basic rate limiting to reduce extraction risk
(coordinated with APP-3).

**Practices**
- Classify weights, adapters, system prompts and proprietary evaluation sets and
  record their locations in the inventory (GOV-1).
- Store artifacts in the model registry or dedicated storage with least-privilege
  access, encryption at rest and access logging.
- Remove secrets from system prompts and prompt templates; use a secrets manager
  (INF-3).
- Restrict access to proprietary evaluation and red-team datasets to the teams
  that need them.
- [ML] Limit the detail of prediction outputs (for example, labels or rounded
  scores rather than full probability vectors) where full detail is not needed.
- [LLM] Assume system prompts may be disclosed, and design them so disclosure does
  not expose secrets or bypass controls.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-4.I.1` | Artifact classification and locations | `Tech` | All | For each high-risk system, the inventory or registry lists weights, adapters, system prompts and eval sets with their classification and storage location. |
| `MDL-4.I.2` | Artifact access controls | `Tech` | All | Storage/registry IAM and encryption configuration for high-risk model artifacts, showing encryption at rest and read access limited to named roles or service identities. |
| `MDL-4.I.3` | Access log review | `Rec` | All | Artifact access logs enabled, and at least one review in the last quarter with anomalies followed up. |
| `MDL-4.I.4` | System prompt secret scan | `Test` | LLM | Secret-scanning results over all production system prompts and templates for high-risk systems, with zero unresolved credentials or keys. |
| `MDL-4.I.5` | Extraction-limiting controls | `Tech` | All | Rate limits and, where applicable, output-detail restrictions configured on inference endpoints of high-risk externally exposed models. |

### Advanced
Artifact protection applies to **all** in-scope models, including fine-tuned
adapters and models deployed at the edge or with partners. Access to weights
is granted through a controlled, approved process and is reviewed regularly.
Artifacts are integrity-protected so tampering is detectable. Extraction and
distillation attempts are monitored, not only rate-limited. System prompt leakage
is tested (MDL-3) and does not expose anything sensitive.

**Practices**
- Grant human access to production weights by request and approval, time-bound
  where possible; service identities use least privilege.
- Encrypt weights at rest with customer-managed keys and in transit; restrict
  export and download of weights from production environments.
- Verify artifact integrity (hash or signature, see MDL-1) before serving.
- Monitor inference traffic for extraction and distillation patterns (high
  volume, systematic input coverage, unusual query distributions) and alert via
  VIS.
- Review artifact access entitlements at least quarterly.
- [ML] Consider watermarking or fingerprinting proprietary high-value models to
  support ownership claims.
- [LLM] Apply controls against distillation through the API, such as usage
  quotas per identity, terms enforcement and anomaly detection on prompt
  patterns.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-4.A.1` | Weight access approval records | `Rec` | All | Every human access grant to production weights in the last 12 months has an approval record; time-bound grants have expired as scheduled. |
| `MDL-4.A.2` | Encryption and export controls | `Tech` | All | Configuration showing customer-managed-key encryption for weights at rest, TLS in transit and controls that block or alert on bulk download/export from production. |
| `MDL-4.A.3` | Entitlement reviews | `Rec` | All | Quarterly access reviews for all in-scope model artifact stores, with removed entitlements recorded. |
| `MDL-4.A.4` | Extraction detection rules | `Tech` | All | Detection rules for extraction/distillation patterns deployed for all externally exposed models, with at least one test alert or real alert in the last 90 days. |
| `MDL-4.A.5` | System prompt leakage test | `Test` | LLM | Test results (from MDL-3) for sampled LLM systems showing that system prompt extraction, if achieved, discloses no secrets, access-control logic or personal data. |
| `MDL-4.A.6` | Model fingerprint or watermark records | `Rec` | ML | For proprietary high-value models, a record of the watermarking/fingerprinting method applied or a documented decision that it is not appropriate. |

### Optimal
Model artifacts are protected by strong, verified controls across the estate and
supply chain. Weights for the most sensitive models are served from hardened or
confidential computing environments where practical, and no human can export them
without multi-party approval. Anti-extraction defenses are tuned based on
measured attack results. The organization can detect and prove unauthorized use
of its models and has exercised its response to weight theft.

**Practices**
- Require multi-party approval for any export of the most sensitive weights.
- Serve the most sensitive models in hardened or confidential computing
  environments (INF-2) where practical.
- Test extraction defenses with simulated extraction or distillation attacks and
  tune thresholds using the results.
- Monitor for unauthorized external use of proprietary models using
  fingerprints or watermarks where applied.
- Exercise weight-theft and system-prompt-leak scenarios in IR tabletop exercises.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `MDL-4.O.1` | Multi-party export control | `Tech` | All | Configuration requiring at least two approvers for export of the most sensitive weights; assessor observes an unapproved export attempt being blocked. |
| `MDL-4.O.2` | Simulated extraction test | `Test` | All | A simulated extraction or distillation attack within the last 12 months against externally exposed high-risk models, showing detection within the target time and resulting threshold tuning. |
| `MDL-4.O.3` | Model theft tabletop | `Test` | All | A tabletop or exercise within the last 12 months covering weight theft or system prompt leakage, with an after-action report and completed improvement actions (IR). |
| `MDL-4.O.4` | Protection metrics | `Rec` | All | Trend metrics on artifact access anomalies, extraction alerts and time to revoke access, with documented improvements from the last 12 months. |
