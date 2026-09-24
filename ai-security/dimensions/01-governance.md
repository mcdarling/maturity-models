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
