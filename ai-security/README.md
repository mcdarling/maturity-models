# AI Security Maturity Model (AISMM)

A maturity model for securing AI systems: classical machine learning, large
language models (LLMs) and autonomous agents. It follows the structure of the
[CISA Zero Trust Maturity Model](https://www.cisa.gov/zero-trust-maturity-model).
**Dimensions** play the role of ZTMM's pillars and contain **elements**, which
play the role of its functions. Three **cross-cutting capabilities** apply
across all dimensions. Each element is rated on ZTMM's four stages:
**Traditional → Initial → Advanced → Optimal**.

What sets AISMM apart is that **every stage of every element lists the evidence a
team must produce to defend the claim**. That evidence consists of the artifacts
and records of practice an assessor can examine, each with acceptance criteria.

## Structure

| Dimension | Elements |
|---|---|
| [1. Governance & Risk Management](dimensions/01-governance.md) | GOV-1 AI Inventory & Asset Management · GOV-2 AI Risk Assessment & Classification · GOV-3 Policy & Acceptable Use · GOV-4 Regulatory & Standards Alignment · GOV-5 Roles, Accountability & Training |
| [2. Data Security](dimensions/02-data.md) | DATA-1 Data Provenance & Lineage · DATA-2 Training & Fine-Tuning Data Integrity · DATA-3 Sensitive Data Protection · DATA-4 Retrieval (RAG) & Context Access Control |
| [3. Model Security](dimensions/03-model.md) | MDL-1 Model Supply Chain & Provenance · MDL-2 Secure ML Pipeline (MLOps/LLMOps) · MDL-3 Adversarial Testing & Red Teaming · MDL-4 Model Artifact Protection |
| [4. AI Application & Runtime Security](dimensions/04-application-runtime.md) | APP-1 Input Validation & Prompt Injection Defense · APP-2 Output Handling & Content Safety · APP-3 Inference Endpoint & API Security · APP-4 Secure AI Application Architecture |
| [5. Agentic AI Security](dimensions/05-agentic.md) | AGT-1 Agent Identity & Authentication · AGT-2 Tool, Plugin & MCP Authorization · AGT-3 Human Oversight & Action Approval · AGT-4 Agent Containment & Isolation · AGT-5 Multi-Agent & Inter-Agent Trust |
| [6. AI Infrastructure & Platform Security](dimensions/06-infrastructure.md) | INF-1 AI Compute & Workload Isolation · INF-2 Model Serving & Hosting Hardening · INF-3 Secrets & Credential Management for AI · INF-4 Third-Party AI Service & Vendor Security |
| [Cross-cutting capabilities](dimensions/07-cross-cutting.md) | VIS Visibility, Monitoring & Detection · IR Incident Response & Resilience · AUTO Automation & Orchestration |

```
            ┌───────────── Cross-cutting: VIS · IR · AUTO ─────────────┐
            │                                                         │
  ┌──────┐ ┌──────┐ ┌───────┐ ┌─────────────┐ ┌─────────┐ ┌──────────┐
  │ GOV  │ │ DATA │ │  MDL  │ │     APP     │ │   AGT   │ │   INF    │
  │ 1–5  │ │ 1–4  │ │  1–4  │ │     1–4     │ │   1–5   │ │   1–4    │
  └──────┘ └──────┘ └───────┘ └─────────────┘ └─────────┘ └──────────┘
   Optimal   ▲  Automated, continuously verified, adaptive
   Advanced  │  Consistent across all systems, lifecycle-integrated, measured
   Initial   │  Defined and evidenced for high-risk systems
   Traditional  Ad hoc
```

**At a glance:** 6 dimensions, 26 elements, 3 cross-cutting capabilities and
494 evidence items (Initial 177 · Advanced 194 · Optimal 123). An ML-profile
system is assessed against up to 307 items, an LLM system up to 375 and an
Agentic system all 494.

## Core concepts

- **[Maturity stages](model/levels.md).** ZTMM's four stages, defined for AI, and
  the rules for claiming a stage. Stages are cumulative, and an element's stage is
  the lowest one it has fully evidenced.
- **[Stacking profiles](model/profiles.md).** One model covers three kinds of
  system: Classical ML, LLM and Agentic. Each AI system is assessed against its
  profile plus every profile below it. For example, agentic systems inherit all
  LLM requirements, and the Agentic dimension applies only to agents.
- **[Evidence requirements](model/evidence.md).** There are four evidence types:
  `Doc`, `Rec`, `Tech` and `Test`. The file also covers freshness windows, what
  every submission must include and how assessors sample.

## Reading an element

Each element has:

1. **Applies to**: the profiles for which the element is in scope.
2. **Intent**, **Key risks addressed** and **References**.
3. For each stage:
   - a **description** of what that stage looks like;
   - the **practices** the team performs, some tagged `[ML]`, `[LLM]` or
     `[Agentic]`;
   - (except Traditional) an **Evidence to produce** table with an ID, evidence
     type, applicable profile and **acceptance criteria**.

## Running an assessment

1. **Scope.** Using GOV-1, list the AI systems and assign each a profile.
2. **Build a checklist.** Generate a checklist for the profile and target stage:
   ```bash
   python3 tools/build_checklist.py --profile Agentic --stage Advanced -o checklist.csv
   ```
   The CSV adds blank `status`, `owner`, `evidence_location`, `date` and
   `notes` columns for teams to fill in.
3. **Collect evidence.** Teams attach evidence for each item that meets the
   acceptance criteria and freshness rules. They record N/A items with a
   justification.
4. **Assess.** Assessors sample as described in [evidence.md](model/evidence.md) and
   rate each element at the lowest fully evidenced stage.
5. **Report.** Report the stage of each element. Where one figure is needed for a
   dimension, use the lowest element stage and show the distribution with it.
   Create a roadmap from the unmet evidence items for the next stage.

## Web reference

`site/index.html` is a single-page reference built from these Markdown files. It
filters by profile, searches evidence and practices, and copies checklists as
CSV. Rebuild it after editing the model:

```bash
python3 tools/build_site.py
```

## Framework alignment

AISMM draws on the NIST AI Risk Management Framework, ISO/IEC 42001, the EU AI
Act, MITRE ATLAS, the OWASP Top 10 for LLM Applications, OWASP's agentic AI
security guidance and CISA's ZTMM. It is not a substitute for any of them. GOV-4
covers mapping AISMM results to the frameworks an organization must comply with.
