# E-040 — Merge the regime auditor into detector validation

**State:** new
**Owner:** Jérémy
**Updated:** 2026-08-31

## Why

`regime_auditor` was documented as stage 10 of the pipeline. **The orchestrator
never dispatches it.**

- Absent from `STAGE_CONFIGS` — so it is never a `current_stage`.
- Absent from `_SKILL_MAP` — and `_build_stage_prompt` **raises**
  `ValueError("No SKILL file mapped for stage: …")` for anything not in that
  map, so it could not be dispatched even if reached.
- **No code writes `regime_audit_decision.yaml`.** The orchestrator only reads
  it if it already exists; the sole writer anywhere is
  `prescreen_signal.py::_resolve_ungated_escape`, which *updates* an existing
  file and returns early when there is none.

What happens in practice: on the `regime_misattribution` path the pipeline
pauses (`status="paused_for_human"`) and prints *"consult regime-auditor skill
and regime_detector_report.yaml"*. A person runs the skill by hand, on one path
only.

Recorded as [E037-16](../E-037/FINDINGS.md#e037-16).

### Why merging is the coherent fix, not just re-labelling

Stage 9 and stage 10 answer **the same question**: *is this detector
trustworthy?* Stage 9 computes the evidence — persistence, class-conditional
sensitivity under ±10% perturbation, activation band. Stage 10 reads that
evidence and returns `trustworthy` / `needs_retune` / `unusable`.

Splitting measurement from judgment across two stages bought nothing and cost
the judgment half ever being built. Jérémy, 2026-08-31: *"its objective might
belong into the regime detector validation step."*

### What silently depends on the missing file

Both of these are conditional on a human having produced
`regime_audit_decision.yaml`, and neither says so:

- **The A2.2 retune firewall** — `_validate_retune_firewall` scans
  `recommended_action` for `pnl`, `sharpe`, `ic`, `backtest`, `cost_drag`,
  `forecast_return_corr`, `per_trade`, `expectancy`, and **raises** on a hit.
  Real enforcement, on a file that may not exist.
- **Stage 7's `ungated_escape_eligible` write-back** — returns early and writes
  nothing when the file is absent, so the escape stays unresolved with no
  trace.

---

## Scope

### In

- Fold the audit judgment into stage 9, so the tool that measures also
  classifies: `trustworthy` / `needs_retune` / `unusable`.
- Keep the **A2.2 retune firewall** — it is genuinely enforced and must survive
  the merge with its raising behaviour intact.
- Decide what produces `regime_audit_decision.yaml` afterwards, since two
  downstream consumers read it.
- Remove `regime_auditor` from the pipeline's stage numbering. **Already done
  in the guide** (2026-08-31): it is documented as a human procedure outside
  the flow, pending this epic.
- Keep `workflow_artifacts/skills/regime-auditor/SKILL.md` as the reference for
  what the judgment must contain — it is the specification, even though nothing
  calls it.

### Out

- Building a new detector. A2.3 forbids that until an ungated edge exists.
- The silent-`None` defect in `_ensure_regime_detector_report`
  ([E037-17](../E-037/FINDINGS.md#e037-17)) — related, and worth doing in the
  same pass, but a separate decision.

---

## Stages

- [ ] **S1 — Characterise and stop.** Every reader of
      `regime_audit_decision.yaml` and what each does when it is absent. Whether
      the classification can be computed deterministically from the report, or
      genuinely needs a judgment call. Report, then stop.
- [ ] **S2 — (blocked on S1) Merge.** Stage 9 emits the decision; the firewall
      moves with it and still raises.
- [ ] **S3 — (blocked on S2) Documentation and cleanup.** Guide, `CLAUDE.md`,
      the stage registry. The legacy skill file stays, marked as the spec.

## Risks

- **The firewall is the one real guard here.** Losing or weakening it in the
  merge would remove the only thing stopping a detector being tuned until the
  PnL looks good. Its behaviour must be test-pinned before the merge, not
  after.
- **`needs_retune` may not be mechanisable.** If the judgment genuinely needs a
  human, the honest outcome is a documented human procedure with a defined
  trigger — not a stage that pretends to be automated. S1 decides which.

## Log

- 2026-08-31 — `new`. Found during E-037's stage audit; confirmed by Jérémy,
  who proposed the merge: *"I would stop considering regime_auditor as a step
  if it is not called. More than that, its objective might belong into the
  regime detector validation step."* The guide was updated the same day to stop
  presenting it as a stage; this epic is the code side.
