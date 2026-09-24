# Evidence Requirements

Every stage above Traditional lists the **evidence** a team must produce to defend
a claim that it has reached that stage. The guiding principle:

> **If it isn't evidenced, it isn't implemented.** A practice counts only when the
> team can show records of it being performed, not just a document saying it
> should be.

## Evidence types

Each evidence item is tagged with one of four types. Assessors should expect a
mix of types. A stage evidenced only by `Doc` items is rarely defensible.

| Type | Meaning | Examples |
|---|---|---|
| `Doc` | **Document.** An approved, version-controlled statement of intent or design. | Policy, standard, procedure, threat model, architecture diagram, RACI |
| `Rec` | **Record.** Output that shows a practice actually happened. | Review tickets, sign-offs, meeting minutes, training completion reports, exception register entries |
| `Tech` | **Technical configuration or data.** An export from the system showing a control is in place. | IaC, gateway/guardrail config, IAM policy, registry export, pipeline definition, dashboard |
| `Test` | **Test or exercise result.** Proof that the control works. | Red-team report, eval results, pen-test findings, tabletop after-action report, detection test |

## What every evidence item must include

When a team submits evidence, each item should state:

1. **Evidence ID.** The ID it satisfies, e.g. `GOV-1.I.2`.
2. **Owner.** The accountable person or role.
3. **Location.** A link or repository path to the evidence.
4. **Date.** When it was produced or last reviewed.
5. **Scope.** Which AI systems or inventory IDs it covers.
6. **Profile applicability.** If an item is N/A, the justification.

## Freshness

Unless an element states otherwise, evidence must be within these windows:

| Evidence type | Maximum age |
|---|---|
| `Doc` | Reviewed or approved within **12 months** |
| `Rec` | At least one record within the practice's stated cadence. If no cadence is stated, within **12 months** |
| `Tech` | Exported within **90 days** of the assessment |
| `Test` | Within **12 months**, *and* after the most recent major change to the system (new model, new tool, new data source) |

## Sampling guidance for assessors

- **Initial:** Examine evidence for every high-risk system. If there are more than
  5, examine at least 5.
- **Advanced:** Draw a random sample of at least 10% of in-scope systems, with a
  minimum of 5. Include at least one system from each profile in use and at least
  one third-party AI system.
- **Optimal:** Use the Advanced sample. Also verify the automation directly by
  observing a control fire, for example a blocked deployment or an alert raised.
  Screenshots alone are not enough.
- A single failed sample item does not automatically fail the stage. However, it
  must be recorded as a finding with a remediation date. Two or more failures for
  the same evidence ID fail that ID.

## Evidence table format

In each element, evidence is listed in a table:

| ID | Evidence | Type | Profile | Acceptance criteria |
|---|---|---|---|---|
| `GOV-1.I.1` | Short name of artifact | `Doc` | All | What the assessor must be able to see for this to count |

ID format: `<ELEMENT>.<STAGE>.<n>`, where the stage letter is `I` (Initial),
`A` (Advanced) or `O` (Optimal).

A machine-readable checklist of every evidence item can be generated with
[`tools/build_checklist.py`](../tools/build_checklist.py).
