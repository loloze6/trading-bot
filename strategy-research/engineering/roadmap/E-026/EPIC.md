# E-026 — Cross-sectional strategies: two engines, one decision

**State:** new
**Owner:** Jeremy (joint with Dorian)
**Updated:** 2026-08-19

## Why

The production engine cannot express a cross-sectional strategy at all.
`core/backtester.py:92,:359` load `self.symbols[0]` only, `main_strategy.py:44`'s
`RollingBuffer` is unpartitioned, and there are no netting hooks. This is not a
defect in code that tries and fails — it is a capability nobody wrote. The
engine was built single-symbol and remains correct as a single-symbol engine.

That matters because breadth is where this project's own kill-map says the
probability actually is: a 19-pair universe over single-symbol timing, with
"classic single-indicator TA on BTC/ETH 1h" recorded as a proven dead lane.
The strategy family most likely to contain an edge is the one the production
engine structurally cannot run.

**The finding that makes this an epic rather than a build ticket (2026-08-19):
a working cross-sectional path already exists.** `strategy-research/tools/
panel_backtester.py` (545 lines) runs dollar-neutral cross-sectional momentum
on the ratified 19-pair Kraken universe today, and — the part that makes it
trustworthy — carries a `validate_gate` that reproduces an archived
single-symbol engine run (P4_ts_trend / run_054) to prove its return, cost,
Sharpe and drawdown accounting matches the production engine before any
cross-sectional number is believed. Its metric functions are deliberate ports
of the engine's own formulas, so engine drift is caught rather than silently
tolerated.

So breadth research is **not blocked**, and the question is not "build
multi-asset". It is: **do we keep two engines, or fold panel capability into
the production one?**

Both answers are defensible, which is exactly why this needs a decision rather
than a dispatch:
- **Keep two.** `panel_backtester.py` is explicitly research-only and imports
  nothing from the live path, so it cannot destabilise production. The
  accounting gate is what makes a second implementation safe.
- **Fold in.** Two implementations of the same accounting is two places for a
  formula to drift, and the gate only catches drift after the fact. A panel
  result can never be promoted through the normal engine path while the engine
  cannot run it.

The second horn is the real cost: a strategy validated only in the research
panel has no path to the production engine, and therefore no path to live —
which collides with E-011/E-023 the moment a cross-sectional candidate looks
promotable.

## Done when

Not yet written — this epic opens on a decision, not an implementation. S1
produces the evidence; the decision follows; only then does a Done-when make
sense. Recording it early would presume the answer.

## Stories

- [ ] S1 — **Characterize, do not build.** Establish what
      `panel_backtester.py` can and cannot do today: which universes and
      timeframes it supports, whether `validate_gate` still passes against the
      current engine, whether any cross-sectional result has been produced and
      recorded as a trial, and what a promotion path for a panel result would
      actually require. Evidence with `file:line`, no code changes.
- [ ] S2 — (blocked on S1) The joint decision: two engines with a standing
      accounting gate, or panel capability folded into the production engine.
      Record the reasoning, not just the verdict.

## Relationship to other epics

- **E-010** (slippage / lot-size) touches `symbols[0]`-shaped assumptions in
  execution and carries a non-BTCUSDT hard-fail amendment; whatever is decided
  here changes what that hard-fail should eventually become. Sequence E-010
  first — it is ratified and narrower.
- **E-011** (shared campaign execution) and **E-023** (live trading) are where
  the "no promotion path" cost lands. Neither is blocked by this epic today,
  and both would be affected by folding in.
- Not related to **E-025** (trial-ledger), which mentions multi-symbol only
  incidentally.

## Log

- 2026-08-19 — `new`. Opened from the Bugs & Tasks card "P11: Single-symbol
  hardcoding blocks multi-asset work" (Notion), which is reduced to a pointer
  per amendment 6. Created after checking the tree rather than taking the
  card's framing: the card reads as "multi-asset is blocked", and the blocking
  claim is only half true — the production engine genuinely cannot express
  cross-sectional strategies, but `panel_backtester.py` already runs the
  19-pair universe with an engine-equivalence gate, so research is not
  blocked and the epic is a consolidation decision rather than a build.

- 2026-08-21 — Sequencing note from a research-system-evolution review (no state
  change). Breadth remains the right direction, and the universe is more ready
  than this epic's Why implies: 19 Kraken symbols now carry engine-format 1h AND
  1d caches (`local_data/kraken_<SYM>_{1h,1d}.csv`, daily set added by
  `8cff3f24`, 2026-08-07), all ending at the seal boundary in
  `config/campaign_data_policy.yaml:holdout_range`. 17 of the 19 cover the full
  validation window; 6 cover the full training window. No recorded campaign run
  ever used more than 4 symbols and the modal run used 2, so the same 12 monthly
  windows would give ~204 window-symbol slots instead of 24.

  **But sequence this AFTER E-027 and E-028.** Every one of the 5,094 position
  closes in the recorded history happened at a forecast of exactly zero and none
  happened while the strategy held a view (E-027 artifacts). Running the same
  rules across 19 symbols before exits are attributable multiplies whatever is
  producing those closes, and reports the result as evidence.

  Second caution for whoever writes the pass rules: 19 correlated crypto pairs
  are not 19 independent samples. If pooled trade counts are graded against the
  existing floors as raw counts, the floors get cleared by correlation rather
  than by edge. Whether pooled samples count raw or correlation-adjusted is a
  research-integrity call for the operator, and it changes what every
  pre-registered threshold means.
