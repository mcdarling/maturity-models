# Dimension 6 — AI Infrastructure & Platform Security

This dimension covers the compute, platform components, credentials and external
services that AI systems run on. It deals only with AI-specific infrastructure
concerns: GPU clusters and data-science notebooks, inference servers and vector
databases, model-provider API keys and hosted AI services. It assumes the
organization's general infrastructure security program already covers baseline
operating system, network and cloud hardening. Where that baseline is missing,
fix it there first; this dimension does not repeat it. The components in scope
are identified from the AI inventory (GOV-1), and "high-risk" follows the AI risk
classification (GOV-2).

| ID | Element | Applies to |
|---|---|---|
| INF-1 | AI Compute & Workload Isolation | ML · LLM · Agentic |
| INF-2 | Model Serving & Hosting Hardening | ML · LLM · Agentic |
| INF-3 | Secrets & Credential Management for AI | ML · LLM · Agentic |
| INF-4 | Third-Party AI Service & Vendor Security | ML · LLM · Agentic |

---

## INF-1 AI Compute & Workload Isolation

**Applies to:** ML · LLM · Agentic

**Intent:** Run AI training, fine-tuning, inference and experimentation on
hardened compute with isolation between tenants, workloads and environments. This
covers GPU clusters and shared accelerators, data-science notebooks and
workstations, the separation of research from production, and confidential
computing where the sensitivity of models or data warrants it.

**Key risks addressed:** Internet-exposed or unauthenticated notebooks giving code
execution and access to training data and credentials; cross-tenant data leakage
through shared GPUs; research environments with a path into production data or
serving; compromise of a training cluster used to tamper with models; agent
code execution escaping onto model-serving infrastructure.

**References:** NIST AI RMF (MANAGE); NIST SP 800-218A (secure development
environments for AI); CIS Benchmarks (Kubernetes and container platforms used for
AI workloads); CSA AI Controls Matrix (infrastructure and virtualization
security); ISO/IEC 42001 (AI system resources).

### Traditional
AI workloads run on whatever infrastructure is available, usually shared general
purpose clusters or individual cloud accounts set up by data-science teams.
Notebooks such as Jupyter are started ad hoc, sometimes with public IP addresses
or no authentication, and often hold long-lived credentials and copies of
production data. GPUs are shared between teams and workloads without any
decision about isolation. Research and production are not clearly separated, and
nobody owns the AI compute estate as a whole.

### Initial
The organization has a documented AI compute security standard and knows where
its AI compute runs. For high-risk systems, training and inference run in
environments separated from research and experimentation, notebooks require
authentication and are not reachable from the internet, and there is a recorded
decision on how shared GPUs are isolated. Execution is mostly manual.

**Practices**
- Maintain a register of AI compute environments (training clusters, inference
  clusters, notebook platforms, GPU pools) linked to the AI inventory (GOV-1).
- Require authentication on every notebook server and prohibit direct internet
  exposure; scan for exposed notebooks at least quarterly.
- Separate research/experimentation from production by account, project or
  network boundary; access to production data from research requires an approved
  exception.
- For each shared GPU pool running high-risk workloads, decide and record the
  isolation mode: dedicated nodes, hardware partitioning (e.g., MIG) or accepted
  time-slicing with a rationale.
- [ML] Restrict access to training clusters to named roles and review it at least
  quarterly, because access to a training cluster is effectively write access to
  the model (see MDL-2).
- [LLM] Run self-hosted LLM inference for high-risk systems on dedicated nodes or
  hardware-partitioned GPUs, not on pools shared with untrusted workloads.
- [Agentic] Run agent code-execution environments on compute separate from model
  serving (see AGT-4).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-1.I.1` | AI compute security standard | `Doc` | All | Covers notebook authentication and exposure, research/production separation, GPU isolation options and when each is required, and access control to training and inference clusters. Approved by a named owner. |
| `INF-1.I.2` | AI compute environment register | `Tech` | All | Lists every training cluster, inference cluster, notebook platform and GPU pool supporting high-risk systems, with owner, environment tier (research/production) and the GOV-1 inventory IDs it serves. |
| `INF-1.I.3` | Notebook exposure scan | `Test` | All | A scan within the last 90 days of external and internal address ranges showing no notebook servers reachable without authentication and none reachable from the internet, or tickets for every finding. |
| `INF-1.I.4` | Research/production separation | `Tech` | All | Account, project or network configuration showing research environments cannot reach production data stores or serving endpoints for high-risk systems, except through recorded exceptions. |
| `INF-1.I.5` | GPU isolation decisions | `Rec` | All | For each shared GPU pool running high-risk workloads, a recorded isolation decision (dedicated, partitioned or time-sliced) with rationale and approver. |
| `INF-1.I.6` | Training cluster access review | `Rec` | ML | Access list for each training cluster limited to named roles, with a review completed within the last quarter and removals actioned. |

### Advanced
All AI compute, including experimentation environments that touch production
data, is provisioned from versioned infrastructure-as-code with an AI-specific
hardened baseline. Isolation is enforced by the platform rather than by
convention: scheduling and admission policies place workloads on the right node
pools and GPU partitions and reject privileged or non-compliant workloads.
Notebooks run on a centrally managed platform. Criteria for confidential
computing are defined and applied. Isolation coverage is measured and reported.

**Practices**
- Provision all AI clusters and notebook platforms from IaC that includes
  AI-specific hardening (GPU drivers and operators, device plugins, container
  runtime settings, shared-memory limits).
- Enforce tenant and workload isolation with admission policy: dedicated node
  pools or GPU partitions per sensitivity tier, no privileged containers or host
  mounts on GPU nodes, workload identities instead of node credentials.
- Run all data-science notebooks on a managed platform with SSO, idle timeouts,
  no public IPs and egress restrictions; detect and retire unmanaged notebook
  servers.
- Define when confidential computing (trusted execution environments,
  confidential GPUs) is required, for example for regulated data or high-value
  proprietary models, and record the decision for each high-risk system.
- Report isolation metrics to the AI governance body (GOV-5).
- [ML] Default-deny internet egress from training jobs, except to allowlisted
  package and model registries (see MDL-1, MDL-2).
- [Agentic] Run agent code execution in hardened sandboxes (e.g., gVisor or
  microVMs) on node pools isolated from model serving and from other tenants'
  agents (see AGT-4).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-1.A.1` | AI compute IaC and drift report | `Tech` | All | All sampled AI clusters and notebook platforms are defined in version-controlled IaC with the AI hardening baseline; drift report shows at least 95% of resources conformant, with deviations as tracked exceptions. |
| `INF-1.A.2` | Isolation admission policy | `Tech` | All | Policy configuration enforcing node-pool/GPU-partition placement by sensitivity tier and blocking privileged containers and host mounts on GPU nodes, plus at least one example of a rejected workload. |
| `INF-1.A.3` | Managed notebook platform | `Tech` | All | Configuration showing SSO, idle timeout, no public IPs and egress restrictions, and discovery output showing unmanaged notebook servers found in the last quarter were triaged (migrated, shut down or excepted). |
| `INF-1.A.4` | Confidential computing decisions | `Rec` | All | Documented criteria plus a recorded decision for every high-risk system; where required, configuration shows the workload runs in a confidential computing environment. |
| `INF-1.A.5` | Isolation metrics report | `Rec` | All | Quarterly report with percentage of AI compute on the hardened baseline, exposed or unmanaged notebooks found, open exceptions and their age. |
| `INF-1.A.6` | Training egress controls | `Tech` | ML | Network policy showing training jobs deny internet egress by default, with an allowlist limited to approved registries. |
| `INF-1.A.7` | Agent sandbox separation | `Tech` | Agentic | Configuration showing agent code execution runs in a hardened sandbox runtime on node pools separate from model serving, with no shared service-account credentials. |

### Optimal
AI compute posture is continuously verified across the whole estate and
misconfigurations are corrected automatically. High-risk training and inference
workloads run only on nodes whose integrity is attested. Isolation has been
tested by adversarial exercises aimed at breaking it, and the results drive
improvements.

**Practices**
- Continuous posture monitoring of AI clusters and notebook platforms, with
  automatic remediation (e.g., revoking public exposure, stopping
  non-compliant notebooks) and alerts to monitoring (VIS).
- Schedule high-risk workloads only on attested nodes (measured boot,
  confidential computing attestation) where the INF-1.A.4 criteria require it.
- Test isolation adversarially at least annually: container and sandbox escape,
  cross-tenant GPU memory access, research-to-production pivoting.
- Track remediation times and feed findings into baseline and policy changes.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-1.O.1` | Automated posture remediation | `Tech` | All | Assessor observes an injected misconfiguration (e.g., a publicly exposed notebook) detected and remediated automatically; measured mean time to remediate ≤ 24 hours over the last quarter. |
| `INF-1.O.2` | Workload attestation | `Tech` | All | Scheduling policy and attestation logs showing workloads that require confidential computing run only on nodes that passed attestation, with failed attestations blocked. |
| `INF-1.O.3` | Isolation breakout test | `Test` | All | Test or red-team exercise within 12 months covering container/sandbox escape, cross-tenant GPU isolation and research-to-production pivoting; all critical and high findings remediated or on a tracked plan. |
| `INF-1.O.4` | Improvement log | `Rec` | All | Metric trends and documented changes to baselines, admission policies or sandboxing made as a result of tests, incidents or threat intelligence. |

---

## INF-2 Model Serving & Hosting Hardening

**Applies to:** ML · LLM · Agentic

**Intent:** Securely configure, patch and monitor the platform components that
host and serve AI: inference servers, model registries, vector databases, ML
orchestration frameworks, AI gateways and agent runtimes. None of them may be
exposed without authentication, and vulnerabilities in AI frameworks and
libraries are managed with defined timelines. The consumer-facing API surface of
an AI system is covered by APP-3; protection of the model files themselves is
covered by MDL-4.

**Key risks addressed:** Unauthenticated dashboards and management APIs on
orchestration frameworks and inference servers leading to remote code execution;
exposed vector databases leaking embedded sensitive content; exploitation of
known vulnerabilities in fast-moving AI frameworks; unsafe model loading
(e.g., pickle deserialization, remote code in model repositories) on serving
hosts; resource exhaustion of inference infrastructure.

**References:** NIST SP 800-218A (vulnerability management for AI software);
CIS Benchmarks (container and Kubernetes platforms hosting AI components); CSA
AI Controls Matrix (application and infrastructure security); OWASP Top 10 for
LLM Applications (LLM03 Supply Chain, LLM10 Unbounded Consumption); NIST AI RMF
(MANAGE).

### Traditional
AI platform components are installed by the teams that use them, often with
default settings. Dashboards, management APIs and vector databases may be
reachable without authentication on internal networks or the internet. Nobody
tracks security advisories for AI frameworks, and components are upgraded when a
feature is needed rather than when a vulnerability is fixed. General
vulnerability scanning may not recognize AI components at all.

### Initial
The organization maintains a register of AI platform components supporting
high-risk systems and has a hardening baseline for each component type. No
component is exposed without authentication. Security advisories for AI
frameworks and libraries are monitored, triaged against the register and patched
within defined timelines. Execution is mostly manual.

**Practices**
- Register each inference server, model registry, vector database, orchestration
  framework and AI gateway with version, owner and network exposure.
- Write a hardening baseline per component type covering authentication, TLS,
  dashboard and admin exposure, default credentials, debug endpoints and model
  loading paths.
- Scan for unauthenticated AI platform endpoints at least quarterly.
- Subscribe to advisories for AI frameworks and libraries in use and apply patch
  SLAs by severity.
- [ML] Restrict write access to the model registry to pipeline identities and
  approvers (see MDL-2, MDL-4).
- [LLM] Enable authentication, per-collection or per-tenant access and encryption
  on vector databases (see DATA-4), and restrict AI gateway admin APIs to
  administrators.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-2.I.1` | AI platform component register | `Tech` | All | Lists every inference server, model registry, vector database, orchestration framework and AI gateway supporting high-risk systems, with version, owner, network exposure and linked GOV-1 inventory IDs. |
| `INF-2.I.2` | Component hardening baselines | `Doc` | All | A baseline for each component type in the register covering authentication, TLS, admin/dashboard exposure, default credentials, debug endpoints and permitted model-loading sources. |
| `INF-2.I.3` | Unauthenticated exposure scan | `Test` | All | A scan within the last 90 days of internal and external ranges showing no AI platform management, dashboard or data APIs reachable without authentication, or tickets for every finding. |
| `INF-2.I.4` | AI framework vulnerability triage records | `Rec` | All | Records showing advisories for AI frameworks and libraries in the register were triaged within 5 business days, with a patch SLA defined (e.g., critical ≤ 14 days, high ≤ 30 days) and met or excepted. |
| `INF-2.I.5` | Model registry access configuration | `Tech` | ML | Registry configuration showing authentication required and write/promote rights limited to pipeline identities and named approvers. |
| `INF-2.I.6` | Vector database and gateway configuration | `Tech` | LLM | Configuration showing authentication, access segmentation and encryption at rest on vector databases, and admin APIs on the AI gateway restricted to named administrators. |

### Advanced
All AI platform components are deployed from approved, hardened images or charts
and checked against their baselines automatically. Dependency scanning that
understands AI frameworks runs in every build and blocks known critical
vulnerabilities. Unsafe model-loading options are disabled by default. Patch
performance is measured, and exceptions are tracked.

**Practices**
- Deploy AI platform components only from approved hardened images, charts or
  managed services; block unapproved images.
- Run automated configuration checks against the baselines at least weekly.
- Include AI frameworks, inference servers and model-format libraries in software
  composition analysis, and fail builds on critical or known-exploited
  vulnerabilities.
- Disable unsafe model loading by default on serving hosts: prefer safe formats
  (e.g., safetensors), turn off remote-code execution options and load only from
  the approved registry (see MDL-1).
- Apply resource limits, quotas and autoscaling bounds to inference servers to
  limit resource exhaustion (see APP-3).
- Track deviations and missed SLAs in an exception register and report metrics to
  the governance body (GOV-5).
- [Agentic] Include agent runtimes, orchestration frameworks and self-hosted MCP
  servers in the register and baselines; none may accept unauthenticated
  connections (authorization of their use is covered by AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-2.A.1` | Approved image enforcement | `Tech` | All | Admission or deployment policy allowing only approved AI platform images/charts, plus at least one example of a blocked unapproved image. No unapproved images in the sample. |
| `INF-2.A.2` | Automated baseline compliance | `Tech` | All | Configuration checks against INF-2.I.2 baselines run at least weekly across all registered components; latest result shows at least 95% compliance, with every deviation in the exception register. |
| `INF-2.A.3` | AI-aware dependency scanning | `Tech` | All | Pipeline configuration scanning AI frameworks and model-format libraries on every build and failing on critical/known-exploited vulnerabilities, plus one example of a failed build. |
| `INF-2.A.4` | Safe model-loading configuration | `Tech` | All | Serving configuration for sampled systems shows remote-code options disabled, unsafe deserialization formats rejected or excepted, and models loaded only from the approved registry. |
| `INF-2.A.5` | Patch SLA and exception report | `Rec` | All | Report covering the last two quarters with percentage of critical/high AI framework vulnerabilities fixed within SLA (target ≥ 90%) and open exceptions with owner and expiry. |
| `INF-2.A.6` | Agent runtime and MCP server hardening | `Tech` | Agentic | Register entries and baseline compliance results for every agent runtime and self-hosted MCP server, with an exposure scan showing none accept unauthenticated connections. |

### Optimal
New advisories for AI components trigger automated rebuilds, testing and
rollout. Newly exposed AI endpoints anywhere in the estate are detected within a
day. The AI platform is penetration tested as a whole, and results and metrics
drive changes to baselines and tooling.

**Practices**
- Automate patching: advisories matched to the component register trigger
  rebuilds, regression tests and staged rollout.
- Continuously monitor the external and internal attack surface for AI platform
  endpoints and alert on new exposure (VIS).
- Penetration test the AI platform (inference servers, registries, vector
  databases, orchestration, gateways, agent runtimes) at least annually.
- Feed metrics, test findings and threat intelligence on AI infrastructure
  attacks into baseline updates.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-2.O.1` | Automated patch pipeline | `Tech` | All | Assessor observes an advisory-to-rebuild flow for an AI component; median time to deploy fixes for critical AI framework vulnerabilities ≤ 7 days over the last two quarters. |
| `INF-2.O.2` | AI attack surface monitoring | `Tech` | All | Continuous discovery of AI platform endpoints with an alert raised within 24 hours of a new unauthenticated or internet-facing exposure, shown by a test or real alert. |
| `INF-2.O.3` | AI platform penetration test | `Test` | All | Test within 12 months covering all registered component types; no critical findings open beyond SLA. |
| `INF-2.O.4` | Improvement log | `Rec` | All | Documented baseline, image or tooling changes made as a result of metrics, penetration tests, incidents or threat intelligence. |

---

## INF-3 Secrets & Credential Management for AI

**Applies to:** ML · LLM · Agentic

**Intent:** Protect the credentials AI systems depend on, including model
provider API keys, tokens for tools and data sources, vector database and model
registry credentials, and cloud keys used by pipelines. Keep them in a vault,
scope them to the minimum, rotate them, detect leaks quickly, and never place
secrets in prompts, system prompts or model context where the model could
disclose them.

**Key risks addressed:** Provider API keys leaked in code, notebooks or logs and
used for fraud or resource abuse; secrets embedded in system prompts extracted
through prompt injection or system prompt leakage; over-scoped tokens letting a
compromised agent reach far beyond its task; long-lived shared personal keys
with no owner or revocation path.

**References:** NIST SP 800-218A (protection of secrets in AI development);
OWASP Top 10 for LLM Applications (LLM02 Sensitive Information Disclosure, LLM07
System Prompt Leakage, LLM10 Unbounded Consumption); CSA AI Controls Matrix
(identity, access and key management); NIST AI RMF (MANAGE).

### Traditional
Model provider keys are created by individual developers, often on personal
accounts, and shared between applications. Keys appear in notebooks, environment
files, source code and sometimes in system prompts. Nobody knows how many AI
credentials exist or who owns them, keys are rarely rotated, and a leaked key is
discovered only when an unexpected bill arrives.

### Initial
The organization has a secrets standard that covers AI credentials, and the
credentials used by high-risk systems are registered, owned, stored in an
approved vault and rotated on a defined cadence. Repositories, including
notebooks, are scanned for AI provider keys. Placing secrets in prompts or system
prompts is prohibited and checked. Execution is mostly manual.

**Practices**
- Register each AI credential used by high-risk systems with owner, scope, vault
  location and rotation date.
- Issue credentials per application or service, never personal keys, for
  production use.
- Retrieve credentials from the vault at runtime; do not store them in code,
  notebooks, container images or environment files committed to repositories.
- Scan repositories, including notebook files and their saved outputs, with
  detectors for AI provider key formats; revoke any leaked key within 24 hours.
- Rotate AI credentials at least every 90 days, or on staff change or suspected
  exposure.
- [LLM] Keep secrets out of system prompts, prompt templates and retrieved
  context; review them before release.
- [Agentic] Scope tool tokens to the minimum operations each agent needs (see
  AGT-1, AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-3.I.1` | AI secrets standard | `Doc` | All | Covers approved vaults, prohibition of secrets in code, notebooks, prompts, system prompts and logs, per-application keys, rotation cadence and leak response. |
| `INF-3.I.2` | AI credential register | `Tech` | All | Lists every model provider key, tool token and platform credential used by high-risk systems with owner, scope, vault path and last rotation date. No personal keys in production use. |
| `INF-3.I.3` | Vault retrieval configuration | `Tech` | All | For sampled high-risk systems, deployment configuration shows credentials fetched from the vault at runtime; image and repository inspection finds none embedded. |
| `INF-3.I.4` | Secret scanning results | `Rec` | All | Scan results within the last quarter covering repositories and notebook files with AI provider key detectors; every confirmed leak revoked within 24 hours, shown by ticket timestamps. |
| `INF-3.I.5` | Rotation records | `Rec` | All | Every credential in the register rotated within the last 90 days or since issue. |
| `INF-3.I.6` | System prompt secret review | `Test` | LLM | Review or automated scan of all system prompts and prompt templates for high-risk systems within the last release, finding no embedded credentials or with findings removed and the credential rotated. |
| `INF-3.I.7` | Agent tool token scopes | `Tech` | Agentic | Token or IAM configuration for each high-risk agent's tools showing scopes limited to the operations listed in its GOV-1 capability record. |

### Advanced
All AI systems follow the standard. Applications reach model providers through
an AI gateway or broker so that provider keys are held centrally, not by each
application. Secret scanning blocks commits across all repositories and extends
to prompt logs, traces and evaluation datasets. Rotation is automated or
credentials are short-lived. Every provider key has quota and spend limits.
Metrics are reported.

**Practices**
- Enable push protection for AI provider key formats on all repositories,
  including notebooks.
- Scan or redact secrets in prompt and response logs, traces, observability data
  and evaluation datasets (see VIS, DATA-3).
- Hold provider keys in the AI gateway or vault; applications authenticate to the
  gateway with workload identity.
- Automate rotation or use short-lived credentials for AI services.
- Set per-key quotas, spend limits and model restrictions at the provider or
  gateway.
- Report leaks detected, time to revoke, vault coverage and rotation compliance
  to the governance body (GOV-5).
- [Agentic] Issue agents short-lived, task-scoped tokens through a credential
  broker, injected into tool calls outside the model's context so the model never
  sees the raw secret.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-3.A.1` | Commit-time secret blocking | `Tech` | All | Push protection or CI secret scanning with AI provider key detectors enabled on all repositories, including notebook files, plus at least one example of a blocked commit. |
| `INF-3.A.2` | Automated rotation coverage | `Tech` | All | Configuration showing automated rotation or short-lived issuance; at least 90% of registered AI credentials covered, with the remainder in the exception register. |
| `INF-3.A.3` | Secrets metrics report | `Rec` | All | Quarterly report with leaks detected, median time to revoke, vault coverage and rotation compliance for all AI systems. |
| `INF-3.A.4` | Log and trace secret scanning | `Tech` | LLM | Scanning or redaction configured on prompt/response logs, traces and evaluation datasets, with findings from the last quarter triaged. |
| `INF-3.A.5` | Centralized provider credentials | `Tech` | LLM | Gateway/vault configuration showing provider keys held centrally; applications authenticate with workload identity; any application holding a direct provider key is a tracked exception. |
| `INF-3.A.6` | Key quotas and spend limits | `Tech` | LLM | Every provider key or gateway route has a quota or spend limit and an allowed-model list, with alerting on threshold breach. |
| `INF-3.A.7` | Brokered agent credentials | `Tech` | Agentic | Broker configuration issuing task-scoped tokens with a lifetime of 1 hour or less, and trace samples showing raw credentials never appear in model inputs or outputs. |

### Optimal
Leaked AI credentials are detected inside and outside the organization and are
revoked and reissued automatically. Canary credentials placed where attackers
would look give early warning. Adversarial testing confirms that credentials
cannot be extracted through the model, its tools or its logs.

**Practices**
- Automate leak response: detection triggers revocation, reissue and owner
  notification without manual steps.
- Monitor public code repositories, paste sites and provider leak notifications
  for the organization's AI credentials.
- Plant canary credentials in notebooks, prompt stores and vector stores, with
  alerts routed to monitoring and IR.
- Include credential extraction in red teaming (MDL-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-3.O.1` | Automated leak response | `Tech` | All | Assessor observes a test key detected, revoked and reissued without manual action; median time to revoke ≤ 1 hour over the last two quarters. |
| `INF-3.O.2` | External leak monitoring | `Tech` | All | Monitoring of public repositories, paste sites and provider leak notifications is active and feeds the automated response, with at least one tested or real alert in the last 12 months. |
| `INF-3.O.3` | Canary credentials | `Tech` | All | Canary credentials deployed in notebooks, prompt stores and vector stores, with a tested alert reaching the IR queue within 15 minutes. |
| `INF-3.O.4` | Credential extraction test | `Test` | LLM | Red-team results within 12 months showing attempts to extract credentials through prompt injection, system prompt leakage, tool outputs and logs; no live credentials recovered, or findings remediated. |
| `INF-3.O.5` | Improvement log | `Rec` | All | Documented changes to detectors, broker design or response automation made as a result of metrics, tests or incidents. |

---

## INF-4 Third-Party AI Service & Vendor Security

**Applies to:** ML · LLM · Agentic

**Intent:** Assess and manage the security of third-party AI services, including
hosted model APIs, AI SaaS, AI features embedded in existing SaaS, hosted agent
platforms and remote tools. Cover due diligence, contract terms, account
configuration, model version change, ongoing monitoring and exit planning. For
LLM and agentic systems that consume a third-party model API, this is where
model-provider risk is assessed, in place of the ML items the organization cannot
perform itself (see [profiles.md](../model/profiles.md)).

**Key risks addressed:** Customer data retained by a provider or used to train
its models; data processed in unapproved jurisdictions or by unknown
sub-processors; silent model changes or deprecations breaking safety behavior;
provider security incidents with no notification; lock-in with no way to exit a
failing or non-compliant vendor.

**References:** NIST AI RMF (GOVERN, third-party risk); ISO/IEC 42001 (supplier
and third-party relationships); CSA AI Controls Matrix (supply chain management
and transparency); OWASP Top 10 for LLM Applications (LLM03 Supply Chain).

### Traditional
Third-party AI services are adopted through standard software procurement, or by
individuals with a credit card, without questions specific to AI. Nobody checks
whether prompts and data are retained or used for training, where they are
processed, or which sub-processors are involved. Applications call "latest"
model aliases, and model changes or deprecations are discovered when something
breaks.

### Initial
Third-party AI services supporting high-risk systems go through an AI-specific
due diligence assessment, and their contracts contain AI-specific data terms.
Account settings such as data retention and training opt-out match what was
agreed. LLM systems pin model versions and track provider deprecation dates.
Execution is mostly manual.

**Practices**
- Assess each third-party AI service supporting high-risk systems before use:
  data retention, use of customer data for training, residency, sub-processors,
  security attestations (e.g., SOC 2, ISO/IEC 27001, ISO/IEC 42001), incident
  notification and model change notice.
- Include AI data terms in contracts or data processing agreements.
- Use zero-data-retention or reduced-retention options where the data
  classification (DATA-3) requires it.
- Link each vendor to the systems that depend on it in the AI inventory (GOV-1).
- [LLM] Pin model version identifiers rather than floating aliases, and track
  provider deprecation dates.
- [Agentic] Extend the assessment to hosted agent platforms and remote tools:
  where actions execute, what is logged and which credentials the vendor holds.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-4.I.1` | AI vendor assessment procedure | `Doc` | All | Defines AI-specific due diligence questions (retention, training use, residency, sub-processors, attestations, incident notification, model change notice), required contract terms and who approves residual risk. |
| `INF-4.I.2` | Completed vendor assessments | `Rec` | All | A completed, approved assessment for every third-party AI service supporting high-risk systems, with a recorded risk decision and date. |
| `INF-4.I.3` | AI contract terms | `Rec` | All | Executed contracts or DPAs for those vendors showing clauses on training use of customer data, retention period, data residency, sub-processor notification and breach notification timeline, or an approved exception. |
| `INF-4.I.4` | Provider account settings | `Tech` | LLM | Console or API export for each model provider account showing retention/zero-data-retention setting, training opt-out and region match the contract and assessment. |
| `INF-4.I.5` | Model version and deprecation register | `Tech` | LLM | Each high-risk LLM system's configuration pins a model version identifier; a register lists provider deprecation dates with a named migration owner for any within 6 months. |
| `INF-4.I.6` | Agent platform and remote tool assessments | `Rec` | Agentic | Assessments for hosted agent platforms and remote tools used by high-risk agents cover action execution location, logging and vendor-held credentials. |

### Advanced
All third-party AI is assessed, including AI features embedded in existing SaaS,
at a depth set by risk tier. Assessment is a procurement gate. Vendors are
monitored between assessments for attestation expiry, term changes, incidents
and sub-processor changes. Model version changes go through evaluation before
adoption. Critical AI vendors have exit plans. Metrics are reported.

**Practices**
- Require an AI vendor assessment before purchase orders or new AI feature
  enablement; tier assessment depth and reassessment cadence by risk.
- Monitor vendors for attestation expiry, terms of service and privacy policy
  changes, sub-processor changes and security incidents.
- Before adopting a new provider model version, run regression, safety and
  security evaluations (see MDL-3, APP-2) and record the approval.
- Maintain an exit plan for each critical AI vendor: alternative provider or
  model, data export and deletion, and estimated time to switch.
- Report vendor coverage, overdue reassessments and open vendor risks to the
  governance body (GOV-5).
- [Agentic] Treat third-party MCP servers and tool providers as vendors subject
  to the same assessment and monitoring (see AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-4.A.1` | Procurement gate | `Tech` | All | Procurement or SaaS-enablement workflow configuration requiring a completed AI assessment before approval, plus at least one example of a held request. |
| `INF-4.A.2` | Tiered assessment coverage | `Rec` | All | Every third-party AI service in the GOV-1 inventory has a current assessment at its tier's depth; high-tier vendors reassessed within the last 12 months. |
| `INF-4.A.3` | Ongoing vendor monitoring records | `Rec` | All | Records from the last two quarters showing attestation expiry, term changes, sub-processor changes and vendor incidents were tracked and each triaged within 30 days. |
| `INF-4.A.4` | Exit plans | `Doc` | All | An exit plan for each critical AI vendor naming the alternative, data export and deletion steps and target switch time, reviewed within 12 months. |
| `INF-4.A.5` | Vendor risk metrics report | `Rec` | All | Periodic report to the governance body with assessment coverage, overdue reassessments, open vendor risks and exceptions. |
| `INF-4.A.6` | Model change evaluation records | `Test` | LLM | For the most recent model version change in each sampled LLM system, evaluation results and an approval dated before the change reached production. |
| `INF-4.A.7` | Third-party tool assessments | `Rec` | Agentic | Every third-party MCP server or remote tool used by agents has a current assessment and appears in vendor monitoring. |

### Optimal
Vendor risk is monitored continuously through automated feeds, and AI traffic
can only reach approved providers. Provider model behavior is checked
continuously so unannounced changes are caught. Exit and failover plans have
been exercised, and lessons feed into vendor strategy and contracts.

**Practices**
- Automate vendor monitoring through attestation, security rating, provider
  status and incident feeds, raising tickets on material change.
- Enforce egress so AI traffic reaches only approved providers and accounts
  through the gateway or proxy (see GOV-1 shadow AI discovery).
- Run scheduled canary evaluations against production provider models to detect
  unannounced behavior changes.
- Exercise exit or failover for critical AI vendors at least annually (see IR).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `INF-4.O.1` | Automated vendor monitoring | `Tech` | All | Automated feeds covering all high-tier AI vendors, with an observed alert-to-ticket flow for a material change. |
| `INF-4.O.2` | Approved-provider egress enforcement | `Tech` | All | Gateway or proxy policy allowing AI traffic only to approved providers and organization accounts, plus an assessor-observed block of an unapproved provider endpoint. |
| `INF-4.O.3` | Exit or failover exercise | `Test` | All | Exercise within 12 months moving a critical AI system to an alternative provider, model or degraded mode within its target switch time, with an after-action report and tracked actions. |
| `INF-4.O.4` | Provider behavior drift monitoring | `Tech` | LLM | Canary evaluations run at least daily against production provider models, with defined alert thresholds and at least one reviewed alert or threshold test in the last quarter. |
| `INF-4.O.5` | Improvement log | `Rec` | All | Documented changes to vendor selection, contract terms, monitoring or exit plans made as a result of monitoring, exercises or incidents. |

---
