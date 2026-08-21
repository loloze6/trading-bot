# E-027 — Exit-cause attribution: stop labelling a switched-off strategy as a signal flip

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-21

## Why

`tools/run_protocol.py:289` `_infer_exit_reason()` classifies every trade exit
as one of `signal_flip | end_of_window | stop_loss | time_stop`. Its rule for a
LONG is `if exit_forecast <= 0: return "signal_flip"`, and its final line is a
bare `return "signal_flip"` with the comment "default". `stop_loss` and
`time_stop` are documented in the same docstring as "not currently implemented;
included for schema completeness". So in practice the classifier emits two
values, and one of them is a catch-all.

That matters because the forecast reaching exactly `0.0` is not one event. At
least three different things produce it, and `strategies/strategy_engine.py`
returns a hard `0.0` for each:

- the active regime has no strategy block — `forecast()`: `cfg = self._regime_cfgs.get(rkey)` then `if cfg is None: return 0.0, {}`
- a component inside a **mapped** regime is not warmed up — `if not h or len(h) < 2: return 0.0, {"not_ready_component": cid}`
- the ensemble genuinely computed zero — a real decision to be flat

The first two are the plumbing switching the strategy off. The third is the
strategy speaking. `_infer_exit_reason` cannot tell them apart, calls all three
`signal_flip`, and the result is aggregated into `trade_diagnostics_summary`
(`run_protocol.py:448`) and consumed by `tools/verdict_criteria_evaluator.py`
at `:187`, `:310`, `:396`.

`signal_flip` is the RIGHT label for most exits — the measurements below show
the strategy reversing and trimming constantly. The defect is that a real,
separate population is hidden inside it with no way to be counted: exits caused
by the plumbing switching the strategy off are filed under the strategy's own
decision-making, and the verdict machinery grades signal quality on the total.

### Measured

Script and raw output in `artifacts/`. Run over every run directory that has a
`bars.csv` (31 runs), using only columns those files already carry. Every
APPROVED allocation move, by shape:

```
approved allocation moves          : 51848
  open_from_flat    : 5342 (10%)
  full_exit_to_zero : 5094 (10%)
  sign_flip         : 8335 (16%)
  partial_reduce    : 17760 (34%)
  increase          : 15317 (30%)
moves with a NONZERO forecast      : 46754 (90%)
rebalance attempts / refused       : 91122 / 39274 (43%)
```

The strategy changes its view constantly: 8,335 full reversals and 17,760
partial reductions, 90% of all moves made while holding a nonzero forecast.
Those are genuine signal-driven exits and partial exits, and `signal_flip` is
the correct label for them.

The problem is the remaining 10%. **5,094 moves took the position to exactly
flat, and that can only happen when the forecast is exactly zero** — so all
three zero-paths land there, indistinguishable. The regime label at those moves
is `mean_reversion` 2164, `trending` 1596, `unknown` 982, `chop` 352, and
`bars.csv`'s `strategy` column is empty on every row of every run, so neither
field discriminates. **Which of the three paths fired is not recoverable from
the artifacts.** That unrecoverability is this epic's subject.

Note the bound this puts on the epic: 5,094 is an upper bound on gate-driven
exits, not a count of them. Some unknown share are case (c), the ensemble
honestly reaching zero. Sizing the real number is S1's job, not a claim this
epic gets to make up front.

**Two retractions, kept because they are the argument for Done-when 2.** An
earlier reading of two runs found 100% of full exits in regime `unknown` and
generalised; widening to 31 runs refuted it. A second version then counted only
full-exits-to-zero and concluded "the strategy never exits by changing its
mind" — that was near-circular, since target allocation is a linear function of
the forecast through the origin, so reaching zero allocation *requires* a zero
forecast. It measured a definition and reported it as a discovery. Both errors
have the same shape as the classifier defect this epic fixes: a catch-all
category absorbing populations that were never checked for being different. The
script retains the controls that caught them.

### Prior art checked (amendment 9)

- **Improvement 03** (`engineering/improvements/done/design_and_docs/03_trade_level_diagnostics.md`)
  designed and shipped this exit-attribution field. `IMPROVEMENTS_REGISTER.md:35`
  records it **IMPLEMENTED, acceptance UNKNOWN**. This epic does not rebuild it —
  it fixes a classifier that is live, wrong, and feeding verdicts.
- `_infer_exit_reason` has already had one misclassification defect found and
  fixed in place (see its own 2026-08-15 comment block: on `run_054`, 15 of 16
  held-to-end windows fell through to the `signal_flip` default). This is the
  same failure shape a second time, which is the argument for making the default
  branch impossible rather than patching it again.
- **E-017** (autopsy standard, parked) touches trade attribution but is blocked
  on Phase 2's gate and does not cover exit causes.

## Done when

1. `exit_reason` can express *why* the forecast was zero, sourced from the
   engine rather than inferred from the forecast's sign — at minimum
   distinguishing "no strategy for this regime", "component not ready", and
   "ensemble decided flat".
2. `_infer_exit_reason` has no unconditional fallback return. An unclassifiable
   exit raises or emits an explicit `unattributed` value; it never silently
   becomes `signal_flip`.
3. `trade_diagnostics_summary` reports the share of each cause, and
   `verdict_criteria_evaluator.py` refuses to grade signal quality on a run
   whose switched-off share exceeds a pre-registered threshold — routing
   "signal untested" rather than a verdict about the signal.
4. `python engineering/roadmap/E-027/artifacts/measure_exit_causes.py <run>`
   reproduces from a fresh run's artifacts, and a regression fixture built from
   an archived run proves at least one trade reclassifies away from
   `signal_flip`.
5. Fast and slow suites green; holdout gate PASS; any change to recorded metrics
   declared with a before/after artifact diff.

## Stories

- [ ] S1 — **Characterize, do not fix.** Determine which of the three zero-paths
      fired for the 5,094 recorded closes, or prove it is unrecoverable from
      existing artifacts and state exactly which field would have to be emitted.
      Read `strategy_engine.forecast()`, the `bars.csv` writer, and the
      `debug_info.*` columns. Evidence with `file:line`. No code changes.
- [ ] S2 — Emit the cause at source: carry the reason for a zero forecast out of
      `StrategyEngine.forecast()` (the `debug` dict already returns
      `{"not_ready_component": cid}` for one path and `{}` for another) through
      to `bars.csv`. Off-by-default if it changes any recorded column; prove
      byte-identical default output.
- [ ] S3 — Rewrite `_infer_exit_reason` to consume S2's field. Remove the
      unconditional `return "signal_flip"`. Add the regression fixture from
      Done-when 4.
- [ ] S4 — Wire the summary into `verdict_criteria_evaluator.py` as a gate on
      grading signal quality, with the threshold pre-registered before it is
      applied to any run.

## Incidental findings (amendment 6 — file as cards, do not fix here)

- **43% of all rebalance attempts are refused by the risk band's minimum-change
  control** (39,274 of 91,122 across 31 runs; `run_034` alone: 5,595 of 14,296;
  `run_059`: 76%). `risk/risk_manager.py:_ctrl_min_allocation_change` rejects
  any `|Δ| < threshold`, so realized allocation drifts from strategy intent and
  nothing records the divergence. Belongs to E-028.
- `bars.csv`'s `strategy` column is empty on every row of every run measured.
  Either populate it or drop it; today it is a column that looks informative and
  is not.
- `run_020` recorded 16,562 bars and **zero** rebalance attempts. `run_021` and
  `run_023` recorded 14,296 attempts, 22 opens and **zero** closes. Both shapes
  were graded as ordinary results.

## Relationship to other epics

- **E-029** (trade record fields) should land FIRST — this corrects the
  sequencing written below on the same day. E-027 exists because
  `_infer_exit_reason` asserts a cause it cannot know; the clean fix is to hand
  it the cause as data rather than a cleverer inference. If E-029 ships first,
  this epic's S2 folds into it and E-027 narrows to removing the fallback
  (Done-when 2) and gating the verdict stage (Done-when 3).
- **E-028** is the other half: this epic measures who closed the position, E-028
  decides whether that close should have happened at all. E-027 first — it is
  additive instrumentation, and E-028's decision needs its numbers.
- **E-026** (cross-sectional): sequencing note in that epic's log. Multiplying a
  strategy across 19 symbols before exits are attributable multiplies whatever
  is generating these closes.
- **E-012** (two-bars loop defect) touches the same end-of-window force-close
  behaviour that already caused one `_infer_exit_reason` defect. Coordinate.

## Log

- 2026-08-21 — `new`. Opened from a research-system-evolution review. The Why is
  measured, not asserted: `artifacts/measure_exit_causes.py` plus
  `measured_all_runs.txt` and `measured_totals.txt` are the evidence (amendment
  5). One over-claim was made and retracted during the review — see the Measured
  section — and the falsification check that caught it is retained in the script.
- 2026-08-21 — Sequencing corrected the same day, after measuring the archived
  `trade_diagnostics.json` files: 4,392 trades carry only two `exit_reason`
  values (92.6% `signal_flip`, 7.4% `end_of_window`) and the record has no
  `regime_at_exit`, no forecast values and no allocation pair. That is a capture
  gap, not a classifier gap, and it is now E-029 — which this epic should follow
  rather than precede.
