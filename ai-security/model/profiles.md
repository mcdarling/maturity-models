# AI System Profiles

AISMM is a single model with three **stacking profiles**. Each AI system is assigned
one profile, and its assessment includes every requirement for that profile and
for the profiles below it.

```
┌─────────────────────────────────────────────┐
│ Agentic   LLM + tools, autonomy, memory,    │  adds: Agentic AI dimension,
│           multi-step actions                │  higher bars on runtime/IR
├─────────────────────────────────────────────┤
│ LLM       Generative / foundation models,   │  adds: prompt injection, RAG,
│           prompts, RAG, chat, copilots      │  output handling, jailbreaks
├─────────────────────────────────────────────┤
│ ML        Classical / predictive ML,        │  base: data, supply chain,
│           classifiers, recommenders, CV     │  pipelines, infra, governance
└─────────────────────────────────────────────┘
```

| Profile | Tag | Typical systems | Assessed against |
|---|---|---|---|
| Classical ML | `ML` | Fraud scoring, recommendation, forecasting, computer vision, anomaly detection | Items tagged `All` or `ML` |
| LLM (pre-agentic) | `LLM` | Chat assistants, RAG search, summarization, copilots that suggest but do not act | `All` + `ML`* + `LLM` |
| Agentic | `Agentic` | Systems that call tools, run code, take actions or delegate to other agents with some autonomy | `All` + `ML`* + `LLM` + `Agentic` |

\* **ML items for LLM-based systems.** ML-tagged items apply to an LLM or agentic
system when the organization trains, fine-tunes or hosts the model. Most ML items
do not apply when the system only calls a third-party model API. In that case,
those risks are covered by INF-4 (Third-Party AI Service & Vendor Security). An
item that does not apply is recorded as **N/A with a justification**. It is not
silently skipped.

## How tags appear in the model

- Each element lists **Applies to**, the profiles for which the element is in
  scope. For example, the Agentic AI dimension (AGT) applies only to `Agentic`.
- Practices and evidence items without a tag apply to every profile in the
  element's scope.
- Practices and evidence items tagged `[ML]`, `[LLM]` or `[Agentic]` apply only
  when the system being assessed has that profile. Because profiles stack, an
  `[LLM]` item also applies to Agentic systems.
- Where the bar is higher for a profile, the element states the profile-specific
  criterion directly. For example, "Output handling" at Advanced adds
  action-validation requirements for `[Agentic]`.

## Assigning a profile

Assign the **highest** profile that describes any capability of the system. If an
LLM application can call even one tool that changes state (sending email, writing
to a database, running code), it is `Agentic`. Record the profile in the AI
inventory (GOV-1) and review it whenever the system's capabilities change.
