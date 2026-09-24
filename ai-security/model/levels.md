# Maturity Stages

The AI Security Maturity Model (AISMM) uses the same four stages as the CISA Zero
Trust Maturity Model (ZTMM), so organizations can assess both side by side.

| Stage | Summary | Scope | Execution | Measurement |
|---|---|---|---|---|
| **Traditional** | Ad hoc. AI is treated like any other software, or not tracked at all. | Individual projects; unknown coverage | Manual, person-dependent, reactive | None |
| **Initial** | Defined basics. Key AI-specific controls and artifacts exist, at least for high-risk systems. | High-risk / production AI systems | Documented, mostly manual, some tooling | Point-in-time checks |
| **Advanced** | Consistent and integrated. Controls apply to all in-scope AI systems and are built into the AI lifecycle. | All in-scope AI systems, including third-party AI | Centrally managed, partially automated, enforced at lifecycle gates | Metrics tracked and reported |
| **Optimal** | Automated and adaptive. Controls are continuously verified and improve based on threat intelligence and measured results. | Entire AI estate, including suppliers and shadow AI | Automated, policy-as-code, self-correcting where possible | Continuous; metrics drive improvement |

## Stage definitions

### Traditional
The organization has no AI-specific security practice for this element. Any controls
that exist come from general IT security programs and were not designed for AI
risks. They depend on individuals. There is **no evidence requirement** for
Traditional: it is the baseline every element starts from.

### Initial
The organization has recognized the AI-specific risk and put defined, documented
controls in place. Those controls cover at least the systems rated high-risk in the
AI risk classification (GOV-2). Execution is mostly manual. An assessor can find a
named owner, a written procedure and records showing the procedure has been
followed at least once.

### Advanced
Controls are standardized across **all** in-scope AI systems and built into the AI
lifecycle as gates, not handled as one-off reviews. Execution is centrally
managed, and repetitive checks are automated. Exceptions go through a tracked
process. The organization measures how well the control performs and reports the
results to accountable leadership.

### Optimal
Controls are automated and continuously verified. They adapt to new threats,
models and use cases with minimal manual effort. Metrics and threat intelligence
lead to documented improvements. The organization can show that the control has
held up under realistic adversarial pressure, such as red teaming, exercises or
real incidents.

## Rules for claiming a stage

1. **Stages are cumulative.** To claim a stage, you must meet every evidence
   requirement for that stage *and every lower stage*.
2. **An element's stage is its lowest fully evidenced stage.** Partially meeting
   Advanced still means Initial.
3. **Profiles stack.** An element's requirements include every item tagged for the
   system's profile and every profile below it. See [profiles.md](profiles.md).
4. **Evidence must be current.** Evidence older than its freshness window does not
   count. See [evidence.md](evidence.md).
5. **Dimension and organization scores are reported, not averaged away.** Report
   the stage of each element. When a single figure is needed for a dimension, use
   the **lowest** element stage in that dimension and note the distribution
   alongside it.
