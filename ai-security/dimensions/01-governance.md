# Dimension 1 — Governance & Risk Management

Governance determines whether the organization knows which AI systems it has, how
risky they are, what rules apply and who is accountable. Nearly every other
element depends on it. For example, the AI inventory (GOV-1) and risk
classification (GOV-2) define what counts as "in scope" and "high-risk" across
the rest of the model.

| ID | Element | Applies to |
|---|---|---|
| GOV-1 | AI Inventory & Asset Management | ML · LLM · Agentic |
| GOV-2 | AI Risk Assessment & Classification | ML · LLM · Agentic |
| GOV-3 | Policy & Acceptable Use | ML · LLM · Agentic |
| GOV-4 | Regulatory & Standards Alignment | ML · LLM · Agentic |
| GOV-5 | Roles, Accountability & Training | ML · LLM · Agentic |

---

## GOV-1 AI Inventory & Asset Management

**Applies to:** ML · LLM · Agentic

**Intent:** Maintain a complete, current and owned inventory of every AI system and
AI asset: models, datasets, prompts, agents, tools, vector stores and AI-enabled
third-party services. Include systems adopted without approval ("shadow AI").

**Key risks addressed:** Unmanaged or shadow AI; unknown exposure when a model or
vendor vulnerability is disclosed; no owner to act during an incident.

**References:** NIST AI RMF (GOVERN, MAP); ISO/IEC 42001 (AI system inventory and
resources); CISA ZTMM (asset visibility); OWASP Top 10 for LLM Applications
(LLM03 Supply Chain).

### Traditional
There is no AI-specific inventory. AI systems may appear in a general CMDB or
application list, but nothing identifies them as AI, and their models, datasets
and providers are not recorded. Teams find out about AI use by chance. Nobody is
formally accountable for any given AI system.

### Initial
There is an AI inventory, even if it is only a spreadsheet, that covers all
production and high-risk AI systems. Each entry has a named owner, a profile
(ML/LLM/Agentic) and its main model and data sources. It is updated manually when
teams report new systems. There is a basic mechanism for detecting shadow AI, such
as a procurement check or a periodic survey.

**Practices**
- Teams register new AI systems before production use.
- An inventory owner reviews the inventory for completeness at least quarterly.
- Procurement and expense reviews flag new AI-enabled SaaS purchases for
  inventory entry.
- [LLM] Record the model provider, model version and whether prompts or data
  leave the organization.
- [Agentic] Record the tools, APIs and data stores each agent can access.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-1.I.1` | AI inventory | `Tech` | All | Lists every production/high-risk AI system with owner, profile, business purpose, model(s), key data sources and deployment status. No blank owner fields. |
| `GOV-1.I.2` | Inventory registration procedure | `Doc` | All | Defines what counts as an "AI system", when registration is required and who approves entries. |
| `GOV-1.I.3` | Quarterly completeness review records | `Rec` | All | At least one review within the last quarter, showing systems added or removed and discrepancies followed up. |
| `GOV-1.I.4` | Shadow-AI discovery output | `Rec` | All | Results of at least one discovery activity (procurement review, survey or network/SaaS discovery), with findings reconciled to the inventory. |
| `GOV-1.I.5` | Provider and data-egress fields | `Tech` | LLM | For each LLM system, the inventory shows the model provider/version and whether prompts leave the organization's boundary. |
| `GOV-1.I.6` | Agent capability fields | `Tech` | Agentic | For each agent, the inventory lists the tools, APIs and data stores it can use. |

### Advanced
The inventory covers **all** AI systems and assets, including internal
experiments that touch production data, third-party AI features embedded in
existing SaaS, and AI components (models, datasets, prompts, tools). The
inventory is fed from authoritative sources such as model registries, cloud
accounts, AI gateways and procurement, not from self-reporting alone. Each
production system has an AI Bill of Materials (AI-BOM). Inventory status is a
deployment gate: an unregistered system cannot reach production.

**Practices**
- Automated discovery jobs pull from model registries, cloud AI services, AI
  gateways/proxies and SaaS management tools.
- Production deployment pipelines check that the system has an inventory record.
- Maintain an AI-BOM per system listing models, versions, datasets, libraries,
  prompts/system prompts and external services.
- Report inventory metrics to the AI governance body (GOV-5).
- [Agentic] Record the MCP servers/tool integrations and the identities agents
  run as, linked to AGT-1 and AGT-2.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-1.A.1` | Automated discovery configuration | `Tech` | All | Configuration showing discovery connectors to at least the model registry, cloud AI services and AI gateway/SaaS management, run at least weekly. |
| `GOV-1.A.2` | Discovery reconciliation records | `Rec` | All | Records showing discovered-but-unregistered systems were triaged (registered, blocked or retired) within a defined SLA. |
| `GOV-1.A.3` | Deployment gate | `Tech` | All | Pipeline/policy configuration that blocks production deployment when the system has no inventory record, plus one example of a blocked or held deployment. |
| `GOV-1.A.4` | AI-BOMs | `Tech` | All | An AI-BOM in a defined format (e.g., CycloneDX ML-BOM or SPDX AI profile) for each sampled production system, generated or updated at the last release. |
| `GOV-1.A.5` | Inventory metrics report | `Rec` | All | Periodic report to the governance body with coverage, shadow-AI findings and age of unresolved discrepancies. |
| `GOV-1.A.6` | Agent tool/identity mapping | `Tech` | Agentic | Each agent entry links to its tool/MCP registrations and service identities. |

### Optimal
The inventory is continuous and complete. Discovery covers endpoints, network
egress, code repositories and SaaS, and new AI use is detected within days. The
inventory is the single source of truth other controls consume: risk
classification, monitoring coverage, vulnerability response and vendor
management all read from it. When a model or library vulnerability is disclosed,
the organization can identify every affected system within hours.

**Practices**
- Continuous discovery across network egress to AI providers, source code
  (AI SDK/package usage), endpoints/browsers and SaaS.
- Other controls (monitoring, vulnerability management, IR) consume inventory data
  through an API.
- Run periodic "exposure drills": simulate a vulnerable model or library and
  measure time-to-identify affected systems.
- Track and continuously improve coverage and detection-latency metrics.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-1.O.1` | Continuous discovery coverage | `Tech` | All | Discovery sources include network egress, code repositories and endpoint/SaaS telemetry, with a measured mean time-to-detect new AI use of ≤ 7 days. |
| `GOV-1.O.2` | Inventory integrations | `Tech` | All | At least monitoring, vulnerability management and IR tooling pull AI system data from the inventory automatically. |
| `GOV-1.O.3` | Exposure drill results | `Test` | All | A drill within the last 12 months that identified all affected systems for a simulated model/library vulnerability within the target time (e.g., ≤ 24 hours). |
| `GOV-1.O.4` | Improvement log | `Rec` | All | Metric trends and documented changes made to discovery/inventory processes as a result. |

---

## GOV-2 AI Risk Assessment & Classification

**Applies to:** ML · LLM · Agentic

**Intent:** Assign every AI system a risk tier using documented criteria, identify
AI-specific threats through structured threat modeling, and record, treat and
re-assess the resulting risks. The tiers defined here set the meaning of
"high-risk" used throughout the model.

**Key risks addressed:** High-impact AI systems deployed with the same controls as
low-impact ones; AI-specific attacks (prompt injection, data poisoning, model
extraction, tool misuse) left out of threat models; risks accepted by default
because no one recorded or owned them; assessments that go stale when the model,
data or tools change.

**References:** NIST AI RMF (MAP, MEASURE, MANAGE); ISO/IEC 42001 (AI risk
assessment, AI risk treatment and AI system impact assessment); ISO/IEC 23894
(AI risk management guidance); MITRE ATLAS; OWASP Top 10 for LLM Applications
(LLM01–LLM10); OWASP Top 10 for Agentic Applications; EU AI Act (prohibited
practices and high-risk categories, as inputs to classification).

### Traditional
AI systems go through the organization's general application risk process, if
any. Nothing in that process asks about model behavior, training data, prompts or
autonomy. There is no risk tier for AI, so no one can say which AI systems are
high-risk. Threat models, where they exist, cover the surrounding application
but not AI-specific attacks. AI risks are not recorded in any risk register.

### Initial
A documented classification scheme assigns each production AI system a risk
tier based on defined criteria. The scheme defines "high-risk" for the rest of
the model and identifies prohibited uses. Every high-risk system has an
AI-specific threat model that draws on MITRE ATLAS and the relevant OWASP lists.
Identified risks are entered in a risk register with an owner and a treatment
decision. Classification and threat modeling are mostly manual and are done
before a high-risk system first goes to production.

**Practices**
- Classify each AI system at registration (GOV-1) using documented criteria and
  record the tier in the inventory.
- Criteria include at least: sensitivity of data processed, impact of outputs on
  people, finances, safety or legal standing, degree of autonomy, exposure to
  untrusted users or content, and regulatory designation (GOV-4).
- Threat model each high-risk system, covering data flows, trust boundaries and
  AI-specific attack techniques mapped to MITRE ATLAS.
- Record each AI risk in a risk register with owner, likelihood, impact,
  treatment decision and target date. Risk acceptance follows the authority
  levels defined in GOV-5.
- [ML] Threat models cover data poisoning, evasion, model extraction, model
  inversion and membership inference where the organization trains or hosts
  the model.
- [LLM] Threat models address each applicable OWASP Top 10 for LLM Applications
  entry, including LLM01 Prompt Injection, LLM02 Sensitive Information
  Disclosure and LLM07 System Prompt Leakage.
- [Agentic] Threat models record each agent's tools, autonomy level and
  worst-case action, and address LLM06 Excessive Agency and the risk categories
  in the OWASP Top 10 for Agentic Applications.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-2.I.1` | AI risk classification standard | `Doc` | All | Defines at least three tiers plus a prohibited category, the criteria and scoring used to assign them, the definition of "high-risk", who approves a tier, and the events that trigger re-assessment. Approved within 12 months. |
| `GOV-2.I.2` | Tier recorded in inventory | `Tech` | All | Inventory export shows a tier, classification date and approver for every production AI system. No production system is unclassified. |
| `GOV-2.I.3` | Threat models for high-risk systems | `Doc` | All | Each high-risk system has a threat model showing data flows, trust boundaries, AI-specific threats mapped to MITRE ATLAS techniques, and the mitigation or AISMM element addressing each threat. Dated before the system's most recent production release. |
| `GOV-2.I.4` | AI risk register | `Rec` | All | Entries exist for every high-risk system, each with risk description, likelihood, impact, owner, treatment decision and target date. Accepted risks show the approver's role and an expiry or review date. |
| `GOV-2.I.5` | ML attack coverage | `Doc` | ML | Threat models for high-risk ML systems address poisoning, evasion, extraction, inversion and membership inference, or record each as N/A with a justification. |
| `GOV-2.I.6` | LLM threat coverage | `Doc` | LLM | Threat models for high-risk LLM systems address each of LLM01–LLM10, or record an entry as N/A with a justification. |
| `GOV-2.I.7` | Agentic threat coverage | `Doc` | Agentic | Threat model for each high-risk agent lists every tool it can call, its autonomy level and the highest-impact action it can take, and addresses the OWASP Top 10 for Agentic Applications risk categories (for example tool misuse, privilege abuse, memory or context poisoning, and cascading failures). |

### Advanced
Classification covers **all** in-scope AI systems, including third-party AI
services and AI features embedded in SaaS. The tier determines which controls a
system must have: a documented matrix maps each tier to minimum requirements in
other elements. Classification and threat modeling are lifecycle gates at design
and before release. Defined material changes, such as a new model version, data
source, tool or user population, trigger re-assessment automatically. The AI
risk register is part of enterprise risk management, and residual AI risk is
reported to the governance body.

**Practices**
- Maintain a tier-to-controls matrix. For example, high-risk systems require
  adversarial testing (MDL-3) before release and monitoring coverage (VIS)
  before go-live.
- Design reviews and release pipelines require a current classification, and
  for medium and high tiers a current threat model.
- Change management flags defined material changes and holds the change until
  re-assessment is complete.
- Classify third-party AI services and embedded AI features through the vendor
  intake process (INF-4).
- Track threat model findings as work items with owners and due dates.
- Update threat models with findings from red teaming (MDL-3) and incidents (IR),
  and review each at least annually.
- [LLM] Re-assess when the model version, system prompt or retrieval sources
  (DATA-4) change.
- [Agentic] Re-assess when a tool, MCP server, permission scope or autonomy level
  changes (AGT-2, AGT-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-2.A.1` | Classification coverage | `Tech` | All | Inventory export shows 100% of in-scope AI systems, including third-party AI, with a tier set within the last 12 months or since the last material change, whichever is later. |
| `GOV-2.A.2` | Tier-to-controls matrix | `Doc` | All | For each tier, lists the required AISMM elements and minimum stage or evidence IDs. Approved by the governance body (GOV-5). |
| `GOV-2.A.3` | Classification and threat-model gate | `Tech` | All | Pipeline or change-workflow configuration that blocks release without a current classification (and a threat model for medium and high tiers), plus one example of a blocked or held release. |
| `GOV-2.A.4` | Material-change re-assessment records | `Rec` | All | For sampled systems, every material change in the last 12 months has a re-assessment dated before the change reached production. |
| `GOV-2.A.5` | Threat-model finding tracking | `Rec` | All | Findings are tracked as tickets with owners and due dates. At least 80% of high-severity findings closed within the defined SLA; overdue items have an approved exception (GOV-3). |
| `GOV-2.A.6` | Residual risk reporting | `Rec` | All | Quarterly report to the governance body showing systems by tier, open high risks, accepted risks and their expiry dates, with minutes recording any decisions. |
| `GOV-2.A.7` | Agent capability re-assessments | `Rec` | Agentic | For sampled agents, every tool, MCP server, permission or autonomy change in the last 12 months has a linked re-assessment and threat model update. |

### Optimal
Risk classification is continuous. Risk scores are calculated from inventory,
data classification, exposure and runtime signals and are recalculated when
those signals change. Threat models are updated from threat intelligence such as
new MITRE ATLAS techniques, OWASP updates, published AI vulnerabilities and
incidents. The organization checks whether its classifications were right by
comparing them with incidents and red-team results, and adjusts its criteria
accordingly.

**Practices**
- Compute risk scores automatically from inventory attributes, data
  classification labels (DATA-3), exposure and agent permissions, and notify
  owners when a score or tier changes.
- Review AI threat intelligence on a fixed cadence and update affected threat
  models within a defined window.
- Compare incidents, near misses and red-team findings (MDL-3) with assigned
  tiers, and revise the criteria when systems prove to be misclassified.
- Use residual-risk trends to set priorities for control investment.
- [Agentic] Feed runtime telemetry of agent actions (VIS) into the risk score, so
  that tool or data use outside the threat-modeled scope triggers re-assessment.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-2.O.1` | Automated risk scoring | `Tech` | All | Configuration showing risk scores derived from inventory, data classification and exposure signals. The assessor observes a changed attribute producing a re-score and an owner notification. |
| `GOV-2.O.2` | Threat intelligence to threat model updates | `Rec` | All | Log showing AI threat intelligence reviewed at least monthly, with affected threat models updated within 30 days. At least two examples in the last 12 months. |
| `GOV-2.O.3` | Classification validation review | `Test` | All | Review within 12 months comparing incidents, near misses and red-team results against assigned tiers, reporting the misclassification rate and the resulting criteria changes. |
| `GOV-2.O.4` | Out-of-scope agent behavior trigger | `Tech` | Agentic | Detection rule that opens a re-assessment when an agent uses a tool or data source not in its threat model, with at least one triggered example. |

---

## GOV-3 Policy & Acceptable Use

**Applies to:** ML · LLM · Agentic

**Intent:** Set clear, enforceable rules for how the organization builds, buys and
uses AI: which tools and models are approved, what data may be used with them,
what developers must do, and how exceptions are granted. Verify that the rules
are followed.

**Key risks addressed:** Confidential or regulated data submitted to unapproved AI
tools; unvetted models, libraries or AI services introduced into products;
inconsistent security requirements across teams; exceptions that never expire;
agents given authority no one approved.

**References:** NIST AI RMF (GOVERN); ISO/IEC 42001 (AI policy and responsible
use of AI systems); OWASP Top 10 for LLM Applications (LLM02 Sensitive
Information Disclosure, LLM06 Excessive Agency); CISA ZTMM (Governance
cross-cutting capability).

### Traditional
General acceptable use and IT security policies do not mention AI. Staff use
public AI tools at their own discretion, and developers choose models, AI
libraries and AI services without review. There is no list of approved AI
tools. Exceptions, where anyone asks for them, are granted informally and not
recorded.

### Initial
An approved AI security policy and acceptable use rules exist. They state which
AI tools and models are approved, what classes of data may be used with each,
and what is prohibited, including putting confidential data into unapproved
tools. Developers have basic rules for sourcing models and handling AI
credentials. Exceptions follow a documented, time-limited process. Staff
acknowledge the policy, and at least one technical control enforces the most
important rule.

**Practices**
- Publish an AI acceptable use policy that states which data classifications may
  be used with which approved tools and prohibits confidential or regulated data
  in unapproved tools.
- Maintain an approved list of AI tools and models, with an owner, permitted data
  classifications and permitted uses for each entry.
- Set basic developer rules: approved model sources (MDL-1), no credentials in
  prompts or code (INF-3), and registration (GOV-1) and classification (GOV-2)
  before production use.
- Require exceptions to be justified, risk-assessed, approved by a named
  authority and time-limited.
- Obtain policy acknowledgment from staff with access to AI tools.
- [LLM] Require human review of AI-generated content before external publication
  and of AI-generated code before merge.
- [Agentic] Define which action classes agents may take autonomously and which
  require human approval (AGT-3), and prohibit agents from acting with shared or
  personal human credentials (AGT-1).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-3.I.1` | AI security and acceptable use policy | `Doc` | All | Approved by a named executive within 12 months. Covers scope, data-use rules by classification, prohibited uses, the approved list, developer rules, the exception process and consequences of violation. |
| `GOV-3.I.2` | Approved AI tools and models list | `Tech` | All | Published where staff can find it. Each entry shows owner, permitted data classifications, permitted uses and last review date. |
| `GOV-3.I.3` | Policy acknowledgment records | `Rec` | All | At least 90% of staff with access to AI tools have acknowledged the current policy version. |
| `GOV-3.I.4` | Exception register | `Rec` | All | Each exception shows requester, justification, risk assessment, approver, compensating controls and an expiry no more than 12 months out. No open-ended exceptions. |
| `GOV-3.I.5` | Basic enforcement control | `Tech` | All | Configuration that blocks or warns on access to known unapproved AI services from managed devices or the corporate network, or a DLP rule for the highest data classification sent to external AI services, with log entries showing it has fired. |
| `GOV-3.I.6` | AI output review rule | `Doc` | LLM | Policy or developer standard requires human review of AI-generated external content and code, naming the review point (for example pull request approval). |
| `GOV-3.I.7` | Agent authority policy | `Doc` | Agentic | Defines agent action classes (for example read, write, external communication, financial, code execution, destructive) and the minimum oversight required for each by risk tier. Referenced by AGT-3. |

### Advanced
The policy is backed by a secure AI development and deployment standard with
testable requirements for each lifecycle stage. The approved list is enforced
technically across **all** managed endpoints and networks: sanctioned use goes
through an AI gateway or equivalent, and unapproved services are blocked or
coached. Pipelines reject models and AI packages that are not approved. A
working approval path lets teams request new tools within a stated SLA.
Violations and exceptions are measured and reported, and AI rules are flowed down
to contractors and vendors (INF-4).

**Practices**
- Publish a secure AI development and deployment standard whose requirements map
  to AISMM elements.
- Route sanctioned LLM use through an AI gateway or proxy that applies data rules,
  and block or coach unapproved AI endpoints on managed devices and networks.
- Enforce model and AI-library allowlists in build and deployment pipelines
  (MDL-1, MDL-2).
- Run a tool and model approval workflow with security review and a published
  decision SLA.
- Track exception expiry automatically, and revoke or re-assess expired
  exceptions.
- Triage detected violations and follow a defined path for coaching or
  disciplinary action.
- [Agentic] Enforce the agent authority policy through tool authorization
  configuration (AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-3.A.1` | Secure AI development and deployment standard | `Doc` | All | Contains testable requirements for design, build, deployment and operation, each mapped to AISMM element IDs. Reviewed within 12 months. |
| `GOV-3.A.2` | Approved-list enforcement | `Tech` | All | Gateway, proxy or CASB configuration showing approved AI services allowed with data rules and unapproved services blocked or coached, covering at least 95% of managed endpoints and all corporate egress. |
| `GOV-3.A.3` | Pipeline allowlist enforcement | `Tech` | All | Pipeline configuration that rejects models and AI packages not on the approved list, plus at least one example of a rejected build. |
| `GOV-3.A.4` | Tool and model approval records | `Rec` | All | Requests from the last 12 months with security review outcome and decision. Median time to decision is within the published SLA. |
| `GOV-3.A.5` | Policy violation metrics | `Rec` | All | At least quarterly report to the governance body of blocked or flagged AI usage by type, with trend and follow-up actions. |
| `GOV-3.A.6` | Exception lifecycle records | `Rec` | All | Register export shows no active exceptions past expiry, and each renewal in the last 12 months has a fresh risk assessment. |
| `GOV-3.A.7` | Agent authority enforcement | `Tech` | Agentic | For sampled agents, tool authorization configuration permits only the action classes the agent authority policy allows for the agent's tier. Any deviation has an approved exception. |

### Optimal
Policy requirements are expressed as code and evaluated automatically in
pipelines, AI gateways and runtime environments. Enforcement decisions take
context into account: the user, the data classification, the destination tool
and the system's tier. Policy and rules are updated quickly when new threats or
new classes of AI tool appear. The organization tests whether its controls can
be bypassed and uses usage telemetry to decide which tools to approve next.

**Practices**
- Encode testable standard requirements as policy-as-code evaluated at build,
  deploy and runtime.
- Make enforcement context-aware, combining user role, data classification
  labels (DATA-3), destination and system tier.
- Update policy and rules within a defined time after a new AI threat or tool
  category is identified.
- Test AI usage controls for bypass at least annually.
- Analyze blocked-usage and shadow-AI telemetry (GOV-1) to prioritize onboarding
  of tools staff need.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-3.O.1` | Policy-as-code | `Tech` | All | Version-controlled, peer-reviewed rules covering at least 75% of the standard's testable requirements, evaluated at build, deploy and runtime. The assessor observes a rule blocking a non-compliant change. |
| `GOV-3.O.2` | Enforcement bypass test | `Test` | All | Test within 12 months that attempts to reach unapproved AI services and move classified data through approved ones (for example personal accounts, browser extensions, direct API calls, alternate domains). Findings remediated and retested. |
| `GOV-3.O.3` | Policy update records | `Rec` | All | At least two examples in the last 12 months where a new threat or tool category led to a policy or rule change within 30 days. |
| `GOV-3.O.4` | Demand-driven onboarding review | `Rec` | All | Quarterly analysis of blocked usage and shadow-AI findings, with approve or deny decisions recorded and a trend in unapproved usage. |

---

## GOV-4 Regulatory & Standards Alignment

**Applies to:** ML · LLM · Agentic

**Intent:** Identify the legal, regulatory, contractual and standards obligations
that apply to each AI system, map them to a single set of controls, keep
evidence ready for audit and track regulatory change.

**Key risks addressed:** Deploying a system in a prohibited or regulated category
without the required steps; penalties and enforcement action; duplicated or
conflicting controls built separately for each framework; failed or delayed
audits; missed effective dates for new obligations.

**References:** NIST AI RMF (GOVERN); ISO/IEC 42001 (AI management system,
certifiable); EU AI Act (prohibited practices, high-risk AI systems, transparency
obligations, general-purpose AI model obligations, provider and deployer roles);
ISO/IEC 23894; data protection law (for example GDPR provisions on automated
decision-making and data protection impact assessments); sector rules such as
model risk management guidance in financial services.

### Traditional
Legal or compliance teams deal with AI questions case by case, if at all. No one
has a consolidated view of which laws and standards apply to which AI systems.
AI frameworks are not used to structure controls. Audit and customer requests
about AI are answered ad hoc by whoever is available.

### Initial
An obligations register lists the laws, regulations, standards and contractual
commitments that apply to the organization's AI use. Each high-risk system has a
recorded regulatory classification, including the organization's role (for
example provider or deployer) and the applicable risk category. The organization
has chosen a primary framework, such as NIST AI RMF or ISO/IEC 42001, assessed
its gaps against it and started a crosswalk to its own controls. Legal or
compliance signs off high-risk systems before launch.

**Practices**
- Identify the jurisdictions and sectors the organization's AI systems operate
  in, and build an obligations register from them.
- Record each high-risk system's regulatory classification in the inventory
  (GOV-1) and use it as an input to risk tiering (GOV-2).
- Select a primary framework and run a gap assessment against it.
- Require legal or compliance review of high-risk systems before launch.
- [ML] Identify model risk management and explainability requirements for models
  used in regulated decisions, such as credit or employment.
- [LLM] Identify transparency obligations, such as disclosing that users are
  interacting with AI or labeling AI-generated content.
- [Agentic] Identify obligations triggered by the actions agents take, such as
  consumer protection, payment rules and record-keeping of actions.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-4.I.1` | Obligations register | `Doc` | All | Lists each applicable law, regulation, standard and contractual commitment with source, applicability rationale, owner, affected systems and effective dates. Reviewed within 12 months. |
| `GOV-4.I.2` | Regulatory classification in inventory | `Tech` | All | Each high-risk system shows its jurisdictions, the organization's role and its regulatory risk category (for example the EU AI Act category, where applicable). |
| `GOV-4.I.3` | Primary framework gap assessment | `Rec` | All | Gap assessment against NIST AI RMF or ISO/IEC 42001 completed within 12 months, with gaps, owners and target dates. |
| `GOV-4.I.4` | Initial control crosswalk | `Doc` | All | Maps the primary framework's requirements to internal controls or AISMM elements. Unmapped requirements are listed as gaps. |
| `GOV-4.I.5` | Pre-launch compliance sign-off | `Rec` | All | Legal or compliance sign-off dated before go-live for every high-risk system launched in the last 12 months. |
| `GOV-4.I.6` | Transparency implementation | `Tech` | LLM | For each user-facing LLM system with a transparency obligation, a screenshot or configuration showing the disclosure or content label in place. |

### Advanced
A unified crosswalk maps **all** frameworks and regulations in the obligations
register to one control set, so that one control and its evidence can satisfy
several requirements. Every in-scope system has its obligations identified.
Compliance documentation is produced as part of the AI lifecycle rather than
assembled for audits. A named function monitors regulatory change and assesses
the impact of each relevant change. Internal audit reviews AI controls, and
obligations are flowed down to AI vendors (INF-4).

**Practices**
- Maintain a unified crosswalk from NIST AI RMF, ISO/IEC 42001, the EU AI Act and
  applicable sector rules to AISMM elements and evidence IDs.
- Review regulatory developments at least monthly and assess the impact of each
  relevant change on affected systems.
- Generate required documentation (for example technical documentation, risk
  assessments, human oversight descriptions and logs) during the lifecycle for
  every regulated system.
- Run an internal audit of AI controls or the AI management system at least
  annually.
- Include AI obligations in contracts with AI vendors (INF-4).
- [ML] Produce model documentation, such as a model card, for each release of a
  model used in regulated decisions.
- [Agentic] Retain agent action logs for as long as the longest applicable
  record-keeping obligation (VIS).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-4.A.1` | Unified control crosswalk | `Tech` | All | GRC tool export mapping every requirement from every framework and regulation in the obligations register to controls, with each control linked to the evidence IDs that satisfy it. |
| `GOV-4.A.2` | Regulatory change log | `Rec` | All | Records of reviews at least monthly. Each relevant change has an impact assessment naming affected systems and an action plan with dates. |
| `GOV-4.A.3` | Internal audit report | `Rec` | All | Internal audit of AI controls within 12 months covering a sample of systems, with findings, owners and remediation status. |
| `GOV-4.A.4` | Lifecycle compliance documentation | `Tech` | All | For sampled regulated systems, the required documentation is complete, current as of the last release and linked to the inventory ID. |
| `GOV-4.A.5` | Compliance status reporting | `Rec` | All | Quarterly report to the governance body covering obligation status, open gaps and upcoming effective dates. |
| `GOV-4.A.6` | Vendor obligation flow-down | `Rec` | All | Contracts for sampled third-party AI services include the terms the obligations register requires (for example data use limits, incident notification and audit rights). |
| `GOV-4.A.7` | Agent action log retention | `Tech` | Agentic | Retention configuration for agent action logs meets the longest applicable obligation, and the assessor observes retrieval of a sample record from the start of the retention window. |

### Optimal
Compliance is monitored continuously. Most controls in the crosswalk have
automated evidence collection, and each system's compliance status is visible at
any time. The organization holds a current external certification or independent
attestation for its AI management system or controls. Horizon scanning lets it
implement new obligations before they take effect, and it can produce a complete
evidence pack for any system on short notice.

**Practices**
- Collect evidence automatically for crosswalk controls and alert when evidence
  passes its freshness window.
- Obtain and maintain external certification or independent attestation.
- Track draft regulations and standards, and plan implementation ahead of
  effective dates.
- Run audit-readiness drills against randomly chosen systems.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-4.O.1` | Continuous control monitoring | `Tech` | All | At least 70% of crosswalk controls have automated evidence collection. Dashboard shows compliance status per system and alerts on stale evidence. |
| `GOV-4.O.2` | External assurance | `Test` | All | Current certification (for example ISO/IEC 42001) or independent attestation covering the in-scope AI estate, with nonconformities closed within the agreed timelines. |
| `GOV-4.O.3` | Ahead-of-deadline implementation | `Rec` | All | At least one regulatory or standards change in the last 12 months implemented before its effective date, with a traceable crosswalk update. |
| `GOV-4.O.4` | Audit-readiness drill | `Test` | All | Drill within 12 months in which a complete evidence pack for a randomly chosen system was produced within 5 business days. |

---

## GOV-5 Roles, Accountability & Training

**Applies to:** ML · LLM · Agentic

**Intent:** Make specific people accountable for AI risk decisions, give an AI
governance body the authority and information it needs, and make sure everyone
who builds, operates, defends or uses AI has the skills their role requires.

**Key risks addressed:** No one authorized to accept or reject AI risk, so risks
are accepted by default; orphaned AI systems after staff changes; developers
unaware of AI-specific attacks; SOC and IR teams unable to recognize or handle
AI incidents; staff misusing AI tools; leadership unaware of the AI risk
posture.

**References:** NIST AI RMF (GOVERN: roles, responsibilities and training);
ISO/IEC 42001 (leadership, roles and responsibilities, competence, awareness);
EU AI Act (AI literacy obligations); CISA ZTMM (Governance cross-cutting
capability).

### Traditional
AI decisions are made inside project teams. No one is formally accountable for
AI risk, and no forum oversees it. Security is involved in AI projects only if
someone thinks to ask. There is no AI-specific training; staff and developers
learn from public sources on their own.

### Initial
A RACI defines who does what for the main AI risk activities. An AI governance
body, which may be part of an existing risk committee, has a charter and meets
on a set cadence. Each high-risk system has a named business owner and technical
owner who have accepted their responsibilities. Risk acceptance authority is
defined by tier. General staff receive AI acceptable use training, and people
building high-risk systems receive AI security training.

**Practices**
- Publish a RACI covering at least registration, classification, risk
  acceptance, deployment approval, exceptions and AI incident response.
- Establish a governance body with a charter, cross-functional membership
  (security, legal, privacy, data, business), decision rights and a meeting
  cadence.
- Assign each high-risk system a business owner and a technical owner.
- Define risk acceptance authority by tier (GOV-2).
- Add the AI acceptable use policy (GOV-3) to general awareness training.
- Train developers and data scientists on high-risk systems in AI security.
- [LLM] Cover prompt injection, sensitive information disclosure and output
  handling (APP-1, APP-2) in developer training.
- [Agentic] Name an owner accountable for each agent's permissions and actions,
  who approves any addition to its tools (AGT-2).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-5.I.1` | AI RACI | `Doc` | All | Covers at least the activities listed above, with exactly one Accountable role per activity. Approved by the governance body within 12 months. |
| `GOV-5.I.2` | Governance body charter | `Doc` | All | States membership, decision rights, risk acceptance thresholds by tier, escalation path and a meeting cadence of at least quarterly. |
| `GOV-5.I.3` | Governance meeting minutes | `Rec` | All | Minutes for each meeting required by the charter's cadence over the last two quarters, recording attendance, decisions and assigned actions. |
| `GOV-5.I.4` | Owner acknowledgments | `Rec` | All | Each high-risk system's business and technical owners have acknowledged their responsibilities in writing and are current employees. |
| `GOV-5.I.5` | Awareness training completion | `Rec` | All | AI acceptable use content is part of general awareness training, with at least 90% completion among staff with AI tool access in the last 12 months. |
| `GOV-5.I.6` | Builder training completion | `Rec` | All | 100% of developers and data scientists assigned to high-risk systems completed AI security training within the last 12 months. The curriculum covers the AI threats in GOV-2 threat models. |
| `GOV-5.I.7` | Agent owner approvals | `Rec` | Agentic | Each high-risk agent has a named owner, and each tool in its current tool set has a recorded approval by that owner. |

### Advanced
Accountability and training extend to **all** in-scope systems and to every role
that touches AI. Role-based curricula with assessments exist for developers, data
scientists and ML engineers, SOC and IR analysts, procurement, general staff and
executives. Access to AI build and deployment platforms depends on completed
training. Approval workflows follow the RACI, ownership is kept current as people
join, move and leave, and leadership receives a standard set of AI security
metrics every quarter.

**Practices**
- Maintain role-based curricula with learning objectives and assessments, and
  make training a prerequisite for access to AI platforms and deployment rights.
- Train SOC and IR analysts on detecting and responding to AI attacks (VIS, IR),
  using MITRE ATLAS case studies and hands-on exercises.
- Build a network of AI security champions in engineering teams.
- Route approvals in workflow tooling according to the RACI.
- Reassign ownership automatically when an owner leaves or changes role.
- Report a standard metric set to leadership quarterly: inventory coverage, tier
  distribution, open high risks, exceptions, violations, training completion,
  AI incidents and AISMM stage by element.
- [Agentic] Train teams building agents on tool authorization, excessive agency
  (LLM06) and human oversight design (AGT-2, AGT-3).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-5.A.1` | Role-based training curricula | `Doc` | All | Modules for at least developers, data scientists/ML engineers, SOC/IR, procurement, general staff and executives, each with learning objectives and an assessment. Updated within 12 months. |
| `GOV-5.A.2` | Role-based completion and assessment results | `Rec` | All | Report by role showing at least 95% completion for each technical role and assessment pass rates against a defined threshold. |
| `GOV-5.A.3` | Training-gated access | `Tech` | All | Access configuration showing that rights to AI platforms, model deployment or production AI pipelines require completed training, plus one example of access held or denied. |
| `GOV-5.A.4` | Ownership lifecycle integration | `Tech` | All | HR or IAM integration that flags AI systems whose owner has left or moved. Inventory export shows no system without a current owner beyond a 30-day reassignment SLA. |
| `GOV-5.A.5` | Leadership metrics reports | `Rec` | All | Quarterly reports containing the standard metric set, with minutes showing decisions or actions taken on them. |
| `GOV-5.A.6` | SOC/IR AI readiness records | `Rec` | All | SOC and IR analysts completed AI-specific training and at least one hands-on exercise (for example investigating a simulated prompt injection alert) in the last 12 months. |
| `GOV-5.A.7` | Agent builder training | `Rec` | Agentic | 100% of engineers on agent teams completed training covering tool authorization, excessive agency and human oversight design in the last 12 months. |

### Optimal
The organization measures whether training changes behavior, not just whether
it was completed, and updates curricula as threats and incidents emerge. Key
risk indicators (KRIs) with thresholds escalate automatically to accountable
leaders when breached. Decision rights and escalation paths are exercised with
executives, and results lead to documented improvements.

**Practices**
- Measure training effectiveness through behavior: policy violation rates
  (GOV-3), AI-related findings in code review and red teaming (MDL-3) by team,
  and SOC performance in exercises.
- Update curricula within a defined window after a significant new threat or
  incident.
- Define KRIs with thresholds, and escalate automatically when a threshold is
  breached.
- Run executive tabletop exercises on AI incidents that test risk acceptance and
  escalation under the RACI (IR).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-5.O.1` | Training effectiveness measurement | `Test` | All | At least one behavioral test within 12 months (for example a simulated lure to submit data to an unapproved AI tool, or a secure AI coding assessment), with a baseline, trend and targeted follow-up for underperforming groups. |
| `GOV-5.O.2` | Curriculum update log | `Rec` | All | At least two curriculum updates in the last 12 months made within 60 days of a significant new threat or incident. |
| `GOV-5.O.3` | KRI thresholds and escalation | `Tech` | All | Dashboard with defined AI KRIs and thresholds, and automated escalation to the accountable role on breach. At least one escalation example or an observed test escalation. |
| `GOV-5.O.4` | Executive AI incident exercise | `Test` | All | Tabletop within 12 months in which executives exercised risk acceptance and escalation decisions under the RACI. The after-action report lists improvements, each tracked to closure. |

---
