# Dimension 2 — Data Security

Data shapes what an AI system learns, what it knows at run time and what it can
reveal. This dimension covers where AI data comes from and whether it may be used
(DATA-1), whether training data can be trusted not to have been tampered with
(DATA-2), how sensitive data is kept out of models, prompts and outputs (DATA-3),
and how retrieval and memory stores enforce who may see what (DATA-4). The
inventory (GOV-1) identifies the datasets and data stores in scope, and the risk
classification (GOV-2) determines which systems must meet a stage first.

| ID | Element | Applies to |
|---|---|---|
| DATA-1 | Data Provenance & Lineage | ML · LLM · Agentic |
| DATA-2 | Training & Fine-Tuning Data Integrity | ML · LLM · Agentic |
| DATA-3 | Sensitive Data Protection | ML · LLM · Agentic |
| DATA-4 | Retrieval (RAG) & Context Access Control | LLM · Agentic |

---

## DATA-1 Data Provenance & Lineage

**Applies to:** ML · LLM · Agentic

**Intent:** Know, for every dataset used to train, fine-tune, evaluate or ground an
AI system, where it came from, under what license and consent terms it may be
used, and how it was transformed before use. Be able to trace a model or RAG
index back to the exact data versions that produced it.

**Key risks addressed:** Use of data without legal right or consent; inability to
respond to a data-subject deletion request, license dispute or poisoning
discovery because affected models cannot be identified; unvetted sources
entering training or retrieval corpora; evaluation results that cannot be
reproduced.

**References:** NIST AI RMF (MAP, MEASURE); ISO/IEC 42001 (data for AI systems:
acquisition, provenance, data preparation); EU AI Act Article 10 (data and data
governance); ISO/IEC 5259 series (data quality for analytics and ML);
"Datasheets for Datasets" (Gebru et al.); CISA/NSA/FBI joint guidance "AI Data
Security" (data supply chain); OWASP Top 10 for LLM Applications (LLM03 Supply
Chain, LLM04 Data and Model Poisoning).

### Traditional
Datasets are collected and copied by individual data scientists or engineers as
needed. Their origin, license and consent basis are not recorded, or are known
only to the person who gathered them. Transformations happen in notebooks and
ad hoc scripts. Nobody can say which data a deployed model was trained on or
which documents a RAG index contains.

### Initial
Datasets used by high-risk and production AI systems have a documented source,
owner, license or usage right, and consent basis where personal data is
involved. Each has a dataset card or datasheet. Dataset versions are recorded
against the model or index versions that used them, even if the linkage is
maintained manually.

**Practices**
- Record a dataset card for each dataset used by a high-risk or production AI
  system: source, collection method, owner, license/usage terms, personal-data
  content and consent or lawful basis, known limitations.
- Legal or privacy review approves new external data sources before first use.
- Record dataset version identifiers (hash, snapshot ID or tag) in the model or
  index release record.
- Link datasets to the AI inventory entry (GOV-1).
- [ML] Record feature engineering and labeling steps, including who labeled the
  data and under what instructions.
- [LLM] Record the sources of fine-tuning, evaluation and RAG corpora, including
  web crawls and internal document repositories, and the provider's published
  training-data disclosures for third-party foundation models.
- [Agentic] Record the data sources an agent can write into its own memory or
  knowledge store, so that later use of that data can be traced.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-1.I.1` | Dataset provenance standard | `Doc` | All | Defines required dataset card fields (at minimum source, owner, license/usage right, personal-data content, consent/lawful basis, version, known limitations), when a card is required and who approves it. |
| `DATA-1.I.2` | Dataset cards | `Doc` | All | A completed card for every dataset used by each sampled high-risk/production system. No blank source, owner or license fields. |
| `DATA-1.I.3` | External data source approvals | `Rec` | All | Legal/privacy approval record for each external or third-party data source used by sampled systems, dated before first training or ingestion use. |
| `DATA-1.I.4` | Model-to-data linkage | `Tech` | All | For each sampled system, the current model or index release record identifies the dataset versions (hash or snapshot ID) it was built from. |
| `DATA-1.I.5` | Labeling and feature records | `Rec` | ML | For each sampled ML system, a record of labeling source (internal/vendor/crowd), labeling instructions version and feature transformation steps. |
| `DATA-1.I.6` | RAG and fine-tuning corpus register | `Tech` | LLM | For each sampled LLM system, a list of fine-tuning, evaluation and RAG sources with owner and ingestion date, and for third-party models a link to the provider's training-data disclosure. |

### Advanced
Provenance and lineage are captured for **all** in-scope AI systems, including
evaluation sets and data used by third-party AI services under the
organization's control. Lineage is recorded automatically by the data and ML
pipelines rather than by hand. A dataset without an approved card and
recorded lineage cannot be used in a training run or ingested into a
production index. Data subject to deletion, license expiry or source
withdrawal can be traced to every model and index that used it.

**Practices**
- Data and ML pipelines emit lineage metadata automatically (source, transform
  step, code version, output version) to a central catalog or lineage store.
- Training and indexing pipelines check for an approved dataset card and
  lineage record before running (see MDL-2).
- Dataset cards are versioned with the data and reviewed when the source,
  license or collection method changes.
- A documented procedure handles deletion requests, license withdrawal and
  source compromise, including identifying affected models and indexes and
  deciding whether to retrain, re-index or remove.
- Report provenance coverage metrics to the governance body (GOV-5).
- [LLM] RAG ingestion pipelines record the source system, document ID and
  version for every chunk, so retrieved content can be traced to its origin.
- [Agentic] Memory writes by agents carry provenance metadata (agent identity,
  session, originating source) so poisoned or erroneous memories can be traced
  and purged.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-1.A.1` | Automated lineage capture | `Tech` | All | Lineage store or catalog export showing, for each sampled system, source → transformation → dataset version → model/index version, populated by pipeline jobs rather than manual entry. |
| `DATA-1.A.2` | Provenance pipeline gate | `Tech` | All | Pipeline/policy configuration that blocks a training run or production ingestion when the dataset lacks an approved card or lineage record, plus one example of a blocked or held run. |
| `DATA-1.A.3` | Data withdrawal procedure and records | `Rec` | All | Documented procedure plus at least one executed case (deletion request, license withdrawal or source removal) showing affected models/indexes were identified and a decision recorded within the defined SLA. |
| `DATA-1.A.4` | Provenance coverage metrics | `Rec` | All | Periodic report to the governance body with percentage of in-scope datasets having current cards and lineage, and age of open gaps. |
| `DATA-1.A.5` | Chunk-level source metadata | `Tech` | LLM | Sample of indexed chunks from each sampled LLM system shows source system, document ID and document version for every chunk. |
| `DATA-1.A.6` | Agent memory provenance | `Tech` | Agentic | Sample of memory records for each sampled agent shows writing agent identity, session ID, timestamp and originating source. |

### Optimal
Lineage is complete and queryable across the AI estate, including supplier data
and third-party model disclosures, and is consumed by other controls. When a
source is found to be poisoned, unlicensed or subject to removal, the
organization identifies every affected model, index and memory store within
hours and remediates through automated retraining or re-indexing workflows.
Provenance attestations are cryptographically bound to the data they describe.

**Practices**
- Signed provenance attestations (for example, in-toto or SLSA-style
  attestations, or C2PA for media) accompany datasets and are verified at use.
- Vulnerability management, IR and vendor management query the lineage store
  through an API (VIS, IR, INF-4).
- Run periodic lineage drills: simulate a compromised or withdrawn source and
  measure time to identify and remediate affected systems.
- Contractually require suppliers of data and models to provide provenance
  information in a defined format, and verify it at intake.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-1.O.1` | Signed provenance verification | `Tech` | All | Pipeline configuration verifying signed provenance attestations for datasets at training/ingestion time, plus a demonstration of an unsigned or tampered attestation being rejected. |
| `DATA-1.O.2` | Lineage drill results | `Test` | All | A drill within the last 12 months that identified all affected models, indexes and memory stores for a simulated compromised source within the target time (e.g., ≤ 24 hours) and initiated remediation. |
| `DATA-1.O.3` | Lineage integrations | `Tech` | All | At least IR and vulnerability management tooling query lineage data automatically. |
| `DATA-1.O.4` | Supplier provenance requirements | `Rec` | All | Contract clauses and intake verification records for every sampled third-party data or model supplier. |

---

## DATA-2 Training & Fine-Tuning Data Integrity

**Applies to:** ML · LLM · Agentic (for LLM and Agentic systems, only where the
organization trains, fine-tunes or builds preference/reward data for the model;
otherwise record N/A with justification and rely on INF-4)

**Intent:** Ensure that data used to train or fine-tune models has not been
tampered with, poisoned or backdoored, and that only authorized people and
processes can change it. Detect and reject malicious or corrupted records before
they reach a training run.

**Key risks addressed:** Data poisoning that degrades accuracy or biases
decisions; backdoors (trigger patterns) planted in training or fine-tuning data;
label flipping; tampering by insiders or compromised pipelines; silent
corruption of datasets between validation and training.

**References:** NIST AI RMF (MEASURE, MANAGE); NIST AI 100-2 (Adversarial Machine
Learning taxonomy: poisoning attacks); MITRE ATLAS (poisoning and backdoor
techniques); OWASP Top 10 for LLM Applications (LLM04 Data and Model Poisoning);
CISA/NSA/FBI joint guidance "AI Data Security" (data integrity, digital
signatures, trusted infrastructure); ISO/IEC 42001 (data quality for AI
systems).

### Traditional
Training data lives in shared buckets, file shares or personal workspaces with
broad access. Nobody checks whether data changed between collection and
training. Data validation, if any, looks for format errors, not manipulation.
Poisoning and backdoors are not considered.

### Initial
Training and fine-tuning datasets for high-risk systems are stored in
access-controlled locations, hashed or snapshotted at approval, and validated
before training. Changes to approved datasets go through a recorded change
process. The team has considered poisoning in the system's threat model.

**Practices**
- Store approved training datasets in locations restricted to named roles; no
  public or organization-wide write access.
- Record a cryptographic hash or immutable snapshot of each approved dataset,
  and verify it before training.
- Run schema, range, distribution and duplicate checks on each new dataset
  version before training.
- Changes to approved datasets require a ticket or pull request with a
  reviewer other than the author.
- Include data poisoning and backdoor scenarios in the threat model (GOV-2).
- [ML] Check label distribution and class balance against the previous version,
  and investigate unexpected shifts.
- [LLM] Screen fine-tuning and preference data for injected instructions,
  trigger phrases and policy-violating content before use.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-2.I.1` | Training data access configuration | `Tech` | All | IAM/storage policy export for each sampled system's training data showing write access limited to named roles or service identities, with no public or organization-wide write. |
| `DATA-2.I.2` | Dataset integrity records | `Tech` | All | For each sampled model version, the hash or snapshot ID of the training dataset recorded at approval, and a log showing it was verified before the training run. |
| `DATA-2.I.3` | Pre-training validation results | `Test` | All | Validation report for the most recent training dataset of each sampled system covering schema, ranges/distributions and duplicates, with failures resolved before training. |
| `DATA-2.I.4` | Dataset change records | `Rec` | All | Tickets or pull requests for changes to approved datasets since the last model release, each with a reviewer different from the author. |
| `DATA-2.I.5` | Poisoning threat model | `Doc` | All | Threat model for each sampled system that names poisoning/backdoor paths (sources, labelers, pipelines, insiders) and the controls for each. |
| `DATA-2.I.6` | Fine-tuning data screening results | `Test` | LLM | For each sampled fine-tuned model, a screening report on the fine-tuning/preference data covering embedded instructions, trigger strings and disallowed content, with flagged records dispositioned. |

### Advanced
Integrity controls apply to **all** in-scope training and fine-tuning data and
are enforced by the pipeline. Datasets are signed, and training jobs refuse
unsigned or altered data. Poisoning detection runs automatically on new data,
and trained models are tested for backdoors before release. Access to training
data is reviewed periodically and exceptions are tracked.

**Practices**
- Sign approved dataset versions; the training pipeline verifies signatures and
  fails on mismatch (see MDL-2).
- Automated poisoning and outlier detection (for example, distribution-shift,
  spectral or influence-based methods, or duplicate and near-duplicate
  analysis) runs on every new dataset version.
- Test trained models for backdoor behavior and targeted misclassification
  before release (MDL-3).
- Review access to training data stores at least quarterly and remove
  unneeded access.
- Vet third-party labeling vendors and external data contributors, and sample
  their output for quality and manipulation (INF-4).
- Track integrity metrics: validation failures, poisoning alerts and time to
  disposition.
- [ML] Monitor for feedback-loop poisoning where production inputs or user
  feedback are recycled into training data, and gate such data separately.
- [LLM] Apply the same controls to RLHF/preference data and to synthetic data
  generated by other models.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-2.A.1` | Signature verification in training pipeline | `Tech` | All | Pipeline definition showing dataset signature verification before training for all in-scope systems, plus one example of a run failed on an unsigned or modified dataset. |
| `DATA-2.A.2` | Automated poisoning detection | `Tech` | All | Configuration of poisoning/outlier detection jobs triggered on every new dataset version for each sampled system, with alert routing to a named owner. |
| `DATA-2.A.3` | Backdoor testing results | `Test` | All | Pre-release backdoor/targeted-behavior test report for each sampled model version released in the last 12 months, with findings resolved or risk-accepted. |
| `DATA-2.A.4` | Training data access reviews | `Rec` | All | Quarterly access review records for training data stores, showing access removed where not justified. |
| `DATA-2.A.5` | Labeling vendor and contributor vetting | `Rec` | All | Vetting record and quality/manipulation sampling results for each external labeling vendor or data contributor used by sampled systems. |
| `DATA-2.A.6` | Feedback-loop data gate | `Tech` | ML | For sampled ML systems that retrain on production data or feedback, pipeline configuration that holds recycled data for validation and rate-limits its share of any training set. |
| `DATA-2.A.7` | Integrity metrics report | `Rec` | All | Periodic report with validation failures, poisoning alerts, time to disposition and signature-check failures across in-scope systems. |

### Optimal
Data integrity is verified continuously from source to trained model, and
detection keeps pace with published poisoning and backdoor techniques. The
organization has shown, through red teaming, that planted poisoned or
backdoored data is caught before a model reaches production.

**Practices**
- End-to-end verification: integrity is checked at ingestion, after each
  transformation and at training, with results recorded in lineage (DATA-1).
- Red team exercises plant poisoned and backdoored samples in the data supply
  chain and measure detection (MDL-3).
- Threat intelligence on new poisoning techniques leads to updated detection
  rules and tests within a defined period.
- Training runs on isolated, attested infrastructure (INF-1).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-2.O.1` | Poisoning red team results | `Test` | All | Exercise within the last 12 months that inserted poisoned and backdoored samples through realistic entry points; report shows detection rate against a defined target and remediation of misses. |
| `DATA-2.O.2` | End-to-end integrity checks | `Tech` | All | Pipeline configuration showing integrity verification at ingestion, each transformation and training, with results written to the lineage store. |
| `DATA-2.O.3` | Detection update log | `Rec` | All | Records showing at least one new poisoning/backdoor technique from threat intelligence converted into a detection rule or test within the target period. |
| `DATA-2.O.4` | Observed pipeline block | `Test` | All | Assessor observes a tampered dataset being rejected by the pipeline in a live or staging run. |

---

## DATA-3 Sensitive Data Protection

**Applies to:** ML · LLM · Agentic

**Intent:** Keep personal data, secrets and confidential information out of AI
systems unless there is a defined need, and prevent it from leaking through
model outputs, prompts, context, logs or third-party AI services. Classify data
before AI use, minimize it, and test that models do not reveal what they were
trained on.

**Key risks addressed:** Personal or confidential data memorized by a model and
reproduced in outputs; secrets pasted into prompts or embedded in training data;
sensitive data sent to external AI providers without approval; membership
inference and training-data extraction; prompt and output logs becoming an
unprotected store of sensitive data.

**References:** NIST AI RMF (MAP, MANAGE); NIST Privacy Framework; ISO/IEC 42001
(data for AI systems); ISO/IEC 27701; GDPR (data minimization, purpose
limitation, storage limitation); OWASP Top 10 for LLM Applications (LLM02
Sensitive Information Disclosure, LLM07 System Prompt Leakage); CISA ZTMM (Data
pillar: categorization and DLP).

### Traditional
Data is copied into training sets, prompts and notebooks without
classification. Users paste whatever they need into AI tools. Prompt and
response logs are kept indefinitely, or not at all, with no thought to what
they contain. Leakage through model outputs is not tested.

### Initial
Data used by high-risk AI systems is classified, and a standard defines which
classes may be used for training, sent in prompts or sent to external AI
providers. Obvious sensitive data (PII, credentials) is removed or masked
before training. Prompt and output logs have a defined retention period. Users
are told what they may and may not enter into AI tools (GOV-3).

**Practices**
- Classify each dataset and data source used by high-risk systems using the
  organization's data classification scheme.
- Publish an AI data-handling standard mapping data classes to permitted uses
  (training, fine-tuning, prompts, RAG, external providers).
- Scan training data for PII and secrets and remove, mask or pseudonymize
  findings before training.
- Set retention periods and access restrictions for prompt, context and output
  logs.
- [LLM] Apply DLP or pattern-based redaction to prompts sent to external model
  providers for high-risk systems, and confirm provider data-use and retention
  terms (INF-4).
- [LLM] Keep secrets and sensitive business logic out of system prompts.
- [Agentic] Restrict which data classes an agent may read from tools and pass to
  other tools or external services.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-3.I.1` | AI data-handling standard | `Doc` | All | Maps each data classification level to permitted AI uses (training, fine-tuning, prompts, RAG, external providers) and required protections. Approved and linked from the AI acceptable-use policy (GOV-3). |
| `DATA-3.I.2` | Dataset classification records | `Rec` | All | Every dataset and data source used by each sampled high-risk system has a recorded classification. |
| `DATA-3.I.3` | Training data PII/secret scan results | `Test` | All | Scan report for the most recent training/fine-tuning dataset of each sampled system, with findings removed, masked or risk-accepted before training. |
| `DATA-3.I.4` | Log retention configuration | `Tech` | All | Configuration showing retention period and access restrictions for prompt, context and output logs matching the standard for each sampled system. |
| `DATA-3.I.5` | Prompt DLP for external providers | `Tech` | LLM | DLP/redaction configuration on the path to external model providers for each sampled high-risk LLM system, plus the provider's data-use and retention terms on file. |
| `DATA-3.I.6` | System prompt review | `Rec` | LLM | Review record for each sampled LLM system confirming the system prompt contains no credentials, keys or data classified above the level permitted for exposure to users. |

### Advanced
Classification, minimization and DLP apply to **all** in-scope AI systems and
data flows, including embedded AI features in SaaS. Controls are enforced at a
central point, such as an AI gateway, for prompts and outputs. Models are tested
for memorization and leakage before release. Sensitive-data findings are
tracked as metrics.

**Practices**
- Route AI traffic through a gateway or proxy that applies DLP to prompts,
  retrieved context and outputs in both directions (APP-2, APP-3).
- Enforce data minimization at design review: each AI system documents the
  data fields it needs and why.
- Test models for memorization and training-data leakage before release
  (for example, canary insertion, extraction prompts or membership inference
  tests) (MDL-3).
- Apply privacy-enhancing techniques where the classification requires it
  (pseudonymization, aggregation, differential privacy or synthetic data).
- Block or alert on sensitive data sent to unapproved AI services (GOV-1
  shadow-AI discovery feeds this).
- [ML] Test high-risk models for membership inference and model inversion.
- [LLM] Test for system prompt extraction and disclosure of other users' data.
- [Agentic] Inspect data passed between tools and to external destinations by
  agents, and block transfers of restricted classes.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-3.A.1` | AI gateway DLP configuration | `Tech` | All | Gateway/proxy policy export applying DLP to prompts, context and outputs for all in-scope systems, with detection classes aligned to the data-handling standard. |
| `DATA-3.A.2` | Data minimization records | `Rec` | All | Design review records for each sampled system listing required data fields with justification, approved before production. |
| `DATA-3.A.3` | Memorization and leakage test results | `Test` | All | Pre-release test report for each sampled model trained or fine-tuned by the organization, showing method (e.g., canaries, extraction prompts, membership inference), results against a defined threshold and remediation. |
| `DATA-3.A.4` | Unapproved AI service controls | `Tech` | All | Network/CASB/endpoint configuration that blocks or alerts on sensitive data sent to AI services not approved in the inventory, with alerts from the last 90 days. |
| `DATA-3.A.5` | Sensitive data metrics | `Rec` | All | Periodic report with DLP detections by class and system, blocked transfers, leakage test failures and time to remediate. |
| `DATA-3.A.6` | Prompt leakage test results | `Test` | LLM | Test results for each sampled LLM system covering system prompt extraction and cross-user/cross-session data disclosure, with findings remediated. |
| `DATA-3.A.7` | Agent egress data controls | `Tech` | Agentic | Policy configuration inspecting agent tool inputs and outbound calls for restricted data classes, plus one example of a blocked transfer. |

### Optimal
Sensitive-data controls are continuous and adaptive across the AI estate.
Classification of new data sources is automated, DLP rules are tuned from
measured false-positive and false-negative rates, and leakage resistance is
proven by adversarial testing. The organization can demonstrate that it knows
where sensitive data sits across models, indexes, memory stores and logs.

**Practices**
- Automated classification of new data sources and datasets at ingestion,
  feeding the AI data-handling rules.
- Red teaming targets data extraction from models, RAG systems and agents
  (MDL-3).
- DLP detection quality is measured and rules are tuned on a defined cadence.
- A sensitive-data map covers models, indexes, memory stores, caches and logs,
  and drives deletion and breach-response workflows (IR).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-3.O.1` | Automated classification at ingestion | `Tech` | All | Pipeline configuration classifying new AI data sources automatically, with coverage of ≥ 95% of in-scope datasets and indexes. |
| `DATA-3.O.2` | Data extraction red team results | `Test` | All | Exercise within the last 12 months attempting extraction of sensitive data from models, RAG systems and (where present) agents; report shows success rate against a defined target and fixes applied. |
| `DATA-3.O.3` | DLP tuning records | `Rec` | All | Measured false-positive and false-negative rates per detection class and documented rule changes, at least quarterly. |
| `DATA-3.O.4` | Sensitive data map | `Tech` | All | Map of sensitive data locations across models, indexes, memory stores, caches and logs for all in-scope systems, updated automatically and used in at least one deletion or incident workflow. |

---

## DATA-4 Retrieval (RAG) & Context Access Control

**Applies to:** LLM · Agentic

**Intent:** Ensure that content retrieved into a model's context (from vector
stores, search indexes, document repositories or agent memory) is limited to
what the requesting user or agent is authorized to see, and that content
ingested into those stores is vetted. Protect vector stores and embeddings as
sensitive data assets in their own right.

**Key risks addressed:** Users receiving content through the AI system that
source permissions would have denied; cross-tenant or cross-user leakage in
shared indexes or memory; indirect prompt injection through ingested documents,
web pages or emails; poisoned retrieval content; reconstruction of source text
from embeddings; tampering with or persistence of malicious content in agent
long-term memory.

**References:** OWASP Top 10 for LLM Applications (LLM08 Vector and Embedding
Weaknesses, LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure,
LLM04 Data and Model Poisoning); NIST AI 100-2 (Adversarial Machine Learning:
indirect prompt injection and generative AI attacks); MITRE ATLAS; CISA ZTMM
(Data pillar: access determination); NIST AI RMF (MANAGE).

### Traditional
Documents are bulk-loaded into a vector store or index using a service account
with broad read access. Every user of the AI application can retrieve anything
in the index. Nobody checks what content is ingested. Vector stores are treated
as caches, not as copies of the source data.

### Initial
For high-risk LLM systems, retrieval respects the permissions of the source
system, at least by separating indexes per audience or tenant. Ingested sources
are approved, and the vector store has access controls and encryption
equivalent to the most sensitive data it holds. Indirect prompt injection
through retrieved content is recognized in the threat model.

**Practices**
- Maintain an approved list of sources for each index; new sources require
  owner approval (DATA-1).
- Enforce source permissions at retrieval, either by per-user or per-group
  filtering on ACL metadata or by separate indexes per audience/tenant.
- Classify each vector store at the highest classification of its content
  and apply matching access control and encryption (DATA-3).
- Restrict direct access to vector stores to the application's service
  identity and named administrators.
- Include indirect prompt injection via ingested content in the threat model
  (APP-1).
- [Agentic] Scope agent memory per user or tenant, and record what an agent may
  write to long-term memory.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-4.I.1` | Retrieval access design | `Doc` | All | For each sampled high-risk system, a design showing how source permissions are enforced at retrieval (ACL filtering or index separation) and how tenants/users are isolated. |
| `DATA-4.I.2` | Approved source list | `Rec` | All | Per-index list of approved sources with owner approval dates; no indexed source missing from the list. |
| `DATA-4.I.3` | Vector store access and encryption config | `Tech` | All | Configuration export showing encryption at rest, network restriction and access limited to the application identity and named administrators. |
| `DATA-4.I.4` | Permission-aware retrieval test | `Test` | All | Test results for each sampled system showing that a user without source access cannot retrieve that content, covering at least one restricted document per source. |
| `DATA-4.I.5` | Agent memory scoping | `Tech` | Agentic | Configuration showing agent long-term memory partitioned per user or tenant, with write permissions defined. |

### Advanced
Permission-aware retrieval applies to **all** in-scope RAG systems and agent
memory stores, using document-level ACLs synchronized from source systems.
Permission changes and deletions in the source propagate to indexes within a
defined window. Content is scanned for injection and malicious instructions at
ingestion, and retrieved content is treated as untrusted input. Access to vector
stores is logged and monitored.

**Practices**
- Carry document-level ACLs from source systems into index metadata and filter
  at query time using the end user's identity, not the service account's.
- Synchronize permission changes and deletions from sources to indexes within
  a defined SLA, and measure lag.
- Scan content at ingestion for embedded instructions, hidden text and
  malicious links; quarantine flagged items for review (APP-1).
- Mark retrieved content as untrusted in prompt construction, separated from
  system instructions (APP-4).
- Log queries and retrievals with user identity, and send logs to monitoring
  (VIS).
- Assess embedding inversion risk for stores holding restricted data, and apply
  controls accordingly (access restriction, encryption, not exposing raw
  vectors through APIs).
- [Agentic] Validate and scan content before it is written to long-term memory;
  provide a way to inspect, correct and purge memory entries.

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-4.A.1` | Document-level ACL enforcement | `Tech` | All | Retrieval configuration for each sampled system showing query-time filtering on synchronized source ACLs using the end user's identity. |
| `DATA-4.A.2` | Permission and deletion sync metrics | `Rec` | All | Measured lag between source permission change/deletion and index update, meeting the defined SLA (e.g., ≤ 24 hours) for sampled systems over the last 90 days. |
| `DATA-4.A.3` | Ingestion content scanning | `Tech` | All | Ingestion pipeline configuration scanning for embedded instructions, hidden text and malicious links, with quarantine records from the last 90 days. |
| `DATA-4.A.4` | Retrieval access logs | `Tech` | All | Logs of queries and retrieved document IDs with user identity for sampled systems, forwarded to the monitoring platform. |
| `DATA-4.A.5` | Cross-tenant and indirect injection tests | `Test` | All | Pre-release test results for each sampled system covering cross-user/cross-tenant retrieval and indirect prompt injection via ingested documents, with findings remediated. |
| `DATA-4.A.6` | Embedding inversion risk assessment | `Doc` | All | Assessment for each vector store holding restricted data, stating inversion risk and controls applied (e.g., no raw vector export, access restriction). |
| `DATA-4.A.7` | Agent memory write controls | `Tech` | Agentic | Configuration showing validation/scanning before memory writes and an operator function to inspect and purge entries, plus one record of its use. |

### Optimal
Context access control is continuously verified across all RAG systems and
agent memory. Authorization is evaluated at retrieval time against a central
policy engine, drift between source permissions and index permissions is
detected automatically, and red teaming shows that indirect injection and
cross-boundary retrieval are caught or contained.

**Practices**
- Evaluate retrieval authorization through a central policy engine at query
  time (policy-as-code), consistent with source-system and zero trust data
  policies.
- Continuously compare index ACLs with source ACLs and alert on drift.
- Red teaming targets poisoned retrieval content, indirect injection and
  cross-tenant access, including agent memory persistence (MDL-3, AGT-4).
- Detection rules alert on anomalous retrieval patterns such as bulk
  enumeration or access to unusual sources (VIS).

**Evidence to produce**

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `DATA-4.O.1` | Policy engine retrieval authorization | `Tech` | All | Policy-as-code rules evaluated at query time for all in-scope RAG systems, plus an observed denial of an unauthorized retrieval. |
| `DATA-4.O.2` | ACL drift detection | `Tech` | All | Automated job comparing index and source ACLs at least daily, with drift alerts and resolution records from the last 90 days. |
| `DATA-4.O.3` | Retrieval red team results | `Test` | All | Exercise within the last 12 months covering poisoned content, indirect injection and cross-tenant retrieval; report shows detection/containment against a defined target and remediation of misses. |
| `DATA-4.O.4` | Anomalous retrieval detection | `Test` | All | Detection test showing an alert raised for simulated bulk enumeration or unusual-source access. |
| `DATA-4.O.5` | Memory poisoning exercise | `Test` | Agentic | Exercise showing that malicious content persisted to agent memory is detected, traced via provenance (DATA-1) and purged within the target time. |
