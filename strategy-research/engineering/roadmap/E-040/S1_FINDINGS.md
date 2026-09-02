# E-040 S1 — Every reader of `regime_audit_decision.yaml`, and can the
# classification be automated? (CUL-181)

**Date:** 2026-09-03
**Status:** characterize-and-STOP, per CUL-181's own instruction. No code
changed. Report, then stop for Jérémy's go-ahead on S2.

## Every reader, and what each does when the file is absent

Two call sites in `workflow/run_phase1_research.py`, structurally identical,
both immediately before `verdict_interpreter` runs:

1. **Full-backtest path** (`current_stage == "verdict_interpreter"`, line
   ~6398-6412): reads `regime_audit_decision.yaml` before invoking the
   verdict-interpreter LLM.
2. **Prescreen-kill path** (`next_stage == "verdict_interpreter"` inside the
   `signal_prescreen` branch, line ~6524-6542): same read, same handling, on
   the shortcut route that bypasses the full walk-forward backtest.

**Both sites, when the file is absent** (`_regime_aud = None`):

- The A2.2 retune firewall (`_validate_retune_firewall`) is skipped —
  correctly: with no audit content, there is nothing to violate.
- `_inject_regime_context_into_handoff(handoff, regime_report, None, run_id)`
  is still called (gated on `regime_report`/`_regime_rpt` being present, NOT
  on the audit being present). Inside it, the `if regime_audit:` block
  (line 2573) is skipped entirely, so **`ungated_escape_eligible` and
  `ungated_escape_rationale` are never written into the handoff at all** —
  not set to `false`, simply absent as keys.
- **The constraint text referencing that field is injected regardless**
  (line 2578-2588, outside the `if regime_audit:` block): *"Do NOT conclude
  ... UNLESS `ungated_escape_eligible` is true (see handoff field)."* When
  the audit is absent, `verdict_interpreter`'s own prompt tells it to check a
  handoff field that was never written. This is a real, silent gap — worth
  fixing regardless of what E-040 S2 decides, since it affects the 60 of 61
  runs that never produce an audit (see below).

**Third reader, `tools/prescreen_signal.py:1158`:** reads the same file at a
different point in the prescreen tool's own flow — not investigated in this
pass; flagged for whoever picks up S2, since a fix to the handoff-injection
gap above should check this site too for the same "field referenced but not
written" shape.

## Measured incidence

**1 of 61 run directories** has ever produced a `regime_audit_decision.yaml`
(`run_039`). The regime-auditor step is exercised extremely rarely in
practice — consistent with USER_GUIDE.md's own note that it is "a human
procedure the orchestrator never dispatches."

## Can trustworthy / needs_retune / unusable be computed deterministically?

**Read the skill file directly** (`workflow_artifacts/skills/regime-auditor/SKILL.md`,
136 lines) rather than inferring from the one real example. Answer: **mostly
yes, with two specific, well-scoped gaps** — not a blanket "needs a human."

**Step 2 (the core status assignment) is a pure lookup table, already
written as one in the skill file itself:**

| Condition | status |
|---|---|
| All relevant symbols/timeframes have `confidence: high` | `trustworthy` |
| Any has `confidence: medium` and no prior retune attempted | `needs_retune` |
| Any has `confidence: low`, OR `confidence: medium` with retune attempted | `unusable_for_this_symbol_timeframe` |

`confidence` and `retune_attempted` both come from data already on disk
(`regime_detector_report.yaml`'s `per_symbol_per_timeframe[].confidence`,
and the audit's own prior-run history). **Nothing about this step requires
subjective judgment — it is already specified as a deterministic rule.**

**Step 3 (A2.1 ungated-escape check) is mostly numeric threshold checks**
against `protocol_result.yaml`'s `hypothesis_verdict.diagnostics` block
(`median_forecast_return_corr < 0.03`, `median_cost_drag_pct > 150%` OR
`per_trade_expectancy_bps mean <= 0`) — also mechanical, not a judgment call.

**Two genuine gaps found, both well-scoped, neither a fundamental blocker:**

1. **Gated-vs-ungated IC provenance is not recorded anywhere.** The skill
   file itself flags this as "CRITICAL" (lines 99-108 of SKILL.md): IC
   measured on gated bars only must NOT be used for the ungated-escape
   check, but `protocol_result.yaml`'s actual schema has no field recording
   which kind a given run's IC is. **Checked directly:** grepped
   `run_protocol.py` and `protocol_result.schema.json` for `gated_scope`,
   `ic_scope`, `all_bars`, `is_gated`, `regime_gate` — none exist. Today this
   distinction is tracked only in the auditor's (human or LLM) head. Fixing
   this is a small, additive schema change (one new boolean/enum field,
   written at the point `run_protocol.py` already knows whether it ran
   gated or ungated), not a design problem.
2. **"`known_weak_periods` vs `needs_retune`" is written as prose, not a
   formula.** SKILL.md line 56: *"Assess whether the weak periods are
   detector error or true regime absence by checking `activation_rate` and
   `parameter_sensitivity` together"* — no threshold or combination rule is
   given. This is the one place that currently needs a human/LLM to exercise
   real judgment, because the rule hasn't been written down precisely enough
   to automate, not because the question is inherently subjective. Making
   this mechanical would need Jérémy or Dorian to state the actual
   threshold/combination rule once, in writing — the same "pre-register
   before automating" discipline the project already applies elsewhere.

## Net assessment for S2

**E-040's premise holds.** The regime-auditor's decision procedure is
already, on paper, almost entirely mechanical — it reads like a deterministic
rule set that happens to currently be executed by an LLM rather than code.
Merging it into detector validation (making Step 2 + Step 3's threshold
checks real code, run automatically at stage 9 instead of waiting for a rare
human-triggered stage 10) looks achievable without inventing new judgment
calls, **provided**:

- The handoff-injection gap above is fixed first (small, unrelated to the
  merge itself, but sits in the same code path).
- The gated/ungated IC provenance field is added (small schema change).
- Jérémy or Dorian states the `known_weak_periods` threshold rule explicitly
  (the one real open question — a decision, not an investigation).

None of this was built in this pass. Reporting and stopping per CUL-181.
