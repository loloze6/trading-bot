# E-017 — Autopsy standard v1

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §3.1, verbatim: "**Autopsy standard v1, with the
right metrics (your addition, adopted).** Objective: every kill explains
itself precisely enough to make a prediction. Deliverable: a defined
**autopsy metric palette** the verdict stage must draw from: *profit per
forecast bin at entry* (does a stronger signal actually earn more? — the
table already exists in our diagnostics), *regime-identification correctness*
(when we labeled 'trending', was it, measured after the fact — and PnL
conditional on the label being right vs wrong), *forecast calibration*
(realized return vs predicted magnitude), *entry/exit efficiency, MAE/MFE,
post-exit returns* (already built), and *cost decomposition* (how much of
the loss is fees vs signal). Rule: no sibling of a killed family is
registered until the parent's autopsy is on file with at least one micro-test
of its claimed cause."

**The load-bearing part is the rule, not the palette itself**: the hard gate
— no sibling of a killed family is registered until the parent's autopsy is
on file with at least one micro-test of its claimed cause — is what this
epic must enforce. The palette is the menu the autopsy draws from; the gate
is what makes the autopsy mandatory rather than optional documentation.

**Blocked on:** Phase 2 verdict. §3.1 belongs to Phase 3 ("Hypothesis wave
2, with real autopsies"), whose own header states it runs "ongoing once
Phase 2 delivers." Phase 2's gate (`docs/ROADMAP.md` §Phase 2): "≥2 new data
axes on disk with provenance + a first registrable indicator each; recorders
running."

**VERIFIED (dispatch W38, tree audit) — the palette is half-built already;
the hard gate does not exist anywhere.**

Existing substrate (3 of 5 palette metrics already on disk, pre-dating this
epic):
- `workflow_artifacts/schemas/trade_diagnostics.schema.json` — `entry_efficiency`,
  `exit_efficiency`, MAE/MFE ratio, `post_exit_return_5bars`/`_20bars`.
- `tools/run_protocol.py:194-244` — `_compute_entry_efficiency()`,
  `_compute_exit_efficiency()`, `_compute_post_exit_returns()`, wired into the
  per-trade record and rolled up into `entry_efficiency_median`/
  `exit_efficiency_median` at lines 400-401/470-471.

Two genuine gaps, confirmed absent by grep across the whole tree (zero
matches for either concept, in any form, anywhere in `strategy-research/`):
- **Profit per forecast bin at entry** — does not exist. No code computes a
  return-by-forecast-bin table.
- **Regime-identification correctness** — does not exist. No code checks a
  regime label against its post-hoc realized behavior, or conditions PnL on
  label-correctness.
- **The sibling-registration hard gate itself** — does not exist. No code
  anywhere blocks or checks brief registration against a killed family's
  autopsy/micro-test status; `forecast_calibration` and `cost decomposition`
  (the palette's other two named metrics) are likewise not implemented, so
  the palette is 2/5 done, not built, and the gate — "the load-bearing part"
  per this epic's own Why — is 0/1 done.

State stays `parked`: none of the above changes the Phase 2 gate dependency.

## Done when

1. The two missing palette metrics are implemented: profit per forecast bin
   at entry (return-by-bin table, joined against forecast magnitude at entry);
   regime-identification correctness (post-hoc label check + PnL conditional
   on label being right vs. wrong). (`forecast_calibration` and `cost
   decomposition` remain named in the palette per the source text but are not
   the focus here since scope was already narrowed once; confirm their status
   alongside these two when this epic is next worked.)
2. The hard gate is enforced mechanically: registering a sibling of a killed
   family fails (or is blocked at registration) unless the parent's autopsy
   is on file with at least one micro-test of its claimed cause. Verified
   absent anywhere in the tree today — this is new work, not wiring.

## Stories

- [ ] S1 — (blocked behind Phase 2's gate) Implement profit-per-forecast-bin
      and regime-identification-correctness; confirm forecast_calibration and
      cost-decomposition status; wire the completed palette into the verdict
      stage alongside the existing entry/exit-efficiency/MAE/MFE/post-exit
      metrics.
- [ ] S2 — Implement the sibling-registration gate against parent-autopsy
      presence + micro-test (zero existing code to build on — new work).

## Pointer

This epic's palette sits on a substrate with an open correctness defect:
`tools/run_protocol.py`'s exit-reason classifier (`_infer_exit_reason`,
`_bar_idx_at`) has a measured contradiction (0.85% `end_of_window_pct` vs 15
of 30 run_054 windows measured ending held) and an unconfirmed hypothesis
that forced closes are silently relabelled `signal_flip`. Notion ticket
`3b31d1fb05a281b1b0dacd644023ebae`. Not diagnosed here, not fixed here — if
confirmed, it affects any exit-reason attribution this epic's autopsy stage
would draw from.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §3.1 (dispatch W35). Parked on Phase 2's gate.
- 2026-08-05 — dispatch W38 (tree audit, no state change — stays `parked`).
  Found 3 of 5 palette metrics (entry/exit efficiency, MAE/MFE, post-exit
  returns) already shipped pre-epic in `trade_diagnostics.schema.json` and
  `run_protocol.py:194-244`; found profit-per-forecast-bin,
  regime-identification-correctness, and the sibling-registration hard gate
  all genuinely absent (zero grep matches tree-wide). Done-when sharpened to
  the real remaining gaps.
