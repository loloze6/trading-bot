# E-029 — The trade record must carry the decision, not just the outcome

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-21

## Why

Every per-trade record written by `tools/run_protocol.py` describes what the
position *did* — return, MAE/MFE, holding bars, efficiency, cost. Almost nothing
describes what the engine *knew* or *decided* at the two moments that matter.

The full field list on every recorded trade:

```
trade_id  symbol  window  direction  regime_at_entry
entry_time  exit_time  holding_bars
realized_return  net_portfolio_return_pct  profitable_net
mae  mfe  entry_efficiency  exit_efficiency
post_exit_return_5bars  post_exit_return_20bars  cost_paid
exit_reason
```

`regime_at_entry` is there; **there is no `regime_at_exit`**, so no recorded
trade can answer "did the regime change while this position was open?" — the
single most useful question about a regime-gated strategy. The forecast values
that produced both decisions are discarded. The allocation before and after is
discarded, so a full flatten, a partial trim and a reversal are indistinguishable
after the fact. And there is no entry label at all: `exit_reason` has no
counterpart.

### Measured

Across every `trade_diagnostics.json` in the tree (4,392 trades):

```
exit_reason   signal_flip    4069  (92.6%)
              end_of_window   323  ( 7.4%)
```

Two values, and one of them means "the backtest ran out of data". **The label
carries no information about 92.6% of trades.** Every analytic question asked of
this project in the last two sessions — which exits were the gate switching off,
how many were reversals, how many were trims — required a throwaway script
against `bars.csv` because the trade record cannot answer any of them.

**F7 — attempt to disprove the above.** If the two labels separated outcomes
sharply, low cardinality would not matter. They do separate:

| exit_reason | n | median return | mean return | median hold |
|---|---|---|---|---|
| signal_flip | 4069 | +0.068% | −0.026% | 3 bars |
| end_of_window | 323 | −0.200% | +2.820% | 7 bars |

So the field is not useless — it isolates the end-of-data artifact, which is
worth having. The claim survives only in its narrow form, which is the one this
epic rests on: **the label cannot discriminate anything inside the 92.6%.** It
separates a measurement artifact from everything else, and everything else is
where the strategy lives.

Two further measurements from the same records, both of which the record itself
should have surfaced and did not:

- **1,219 trades (28%) last exactly one bar; 41% last one or two. Median holding
  is 3 bars.** On 1h data that is a ~3-hour average hold. This is the turnover
  story stated at trade level for the first time.
- **858 trades (20%) carry `regime_at_entry: "unknown"`.** A position was opened
  while the active regime had no strategy block — which by
  `strategies/strategy_engine.py`'s `if cfg is None: return 0.0` should have
  produced a zero forecast and therefore no opening trade. Either the engine
  opens positions with no strategy allocated, or `regime_at_entry` is sampled
  from the wrong bar. Both are defects and neither is currently visible.

**Sampling caution for whoever reads these numbers next:** only 6
`trade_diagnostics.json` files exist and `run_030`'s three copies contribute
3,534 of the 4,392 trades, so the symbol mix (80% AVAXUSDT) reflects which runs
happened to keep diagnostics, not the campaign. The field-level gaps are
structural and hold regardless; the distributions are not a campaign-wide sample.

### Prior art checked (amendment 9)

A tree-wide grep for `regime_at_exit|entry_reason|forecast_at_entry|
forecast_at_exit|allocation_at_` returns **nothing** in any `.py`, `.md` or
`.yaml`. Improvement 03's design doc specified the record that shipped and did
not include them. **E-017** (autopsy standard, parked) covers the *metric
palette* the verdict stage draws from — profit-per-forecast-bin, regime-ID
correctness — not the per-trade fields those metrics would need. No overlap.

## Done when

1. Every per-trade record carries, at minimum: `regime_at_exit`,
   `forecast_at_entry`, `forecast_at_exit`, `allocation_before`,
   `allocation_after`, and a `move_shape` in
   `{open, add, reduce, reverse, flat}` derived from the allocation pair rather
   than inferred from the forecast's sign.
2. An `entry_reason` exists and is populated. A trade whose entry cannot be
   explained is labelled `unattributed`, never given a plausible default.
3. `python engineering/roadmap/E-027/artifacts/measure_exit_causes.py` becomes
   redundant: the same five-way move breakdown is readable straight out of the
   trade records, and the script is either deleted or reduced to a check that
   the emitted fields agree with `bars.csv`.
4. The two anomalies above are resolved or explicitly recorded as known
   behaviour: the 20% `unknown`-regime entries, and the 28% one-bar holds.
5. Schema change is additive, existing consumers keep working, and a test proves
   the pre-existing fields are byte-identical.
6. Fast and slow suites green; holdout gate PASS.

## Stories

- [ ] S1 — **Characterize, do not build.** Establish where each proposed field
      can be sourced without changing engine behaviour: which are already in
      `bars.csv`, which exist only inside `StrategyEngine.forecast()`'s debug
      dict, and which are genuinely not captured anywhere. Resolve the
      `regime_at_entry: "unknown"` anomaly — engine defect or sampling defect.
      Evidence with `file:line`. No code changes.
- [ ] S2 — Extend the per-trade schema and its writer with the fields S1 proved
      are available. Additive only; prove the existing fields are unchanged.
- [ ] S3 — Add `move_shape` and `entry_reason`, with the `unattributed` value
      and no silent default.
- [ ] S4 — Retire the throwaway script (Done-when 3) and make the move breakdown
      part of `trade_diagnostics_summary`, so it is produced on every run rather
      than on request.

## Relationship to other epics

- **E-027** (exit-cause attribution) is the consumer, and **this epic should
  land first** — a correction to the sequencing recorded in E-027's log on the
  same day. E-027's job is to stop `_infer_exit_reason` asserting a cause it
  cannot know; the cleanest way to do that is to give it the cause as data
  rather than a better inference. If E-029 ships first, E-027's S2 collapses
  into it and E-027 narrows to removing the fallback and gating the verdict
  stage.
- **E-028** (allocation vs intent) needs `allocation_before`/`allocation_after`
  to state its case per-trade rather than per-bar.
- **E-017** (autopsy palette, parked) would consume these fields if unparked.
  No conflict; this epic supplies inputs, that one defines metrics.
- **E-012** (two-bars loop defect) owns the `end_of_window` population. Do not
  re-derive it here.

## Log

- 2026-08-21 — `new`. Opened at the operator's prompt: *"is there another epic to
  maybe change trade label to make it more explicit for analysis? always think
  long term — if you need to do it once, maybe worth to make it implemented and
  fully done at each run."* That is F3 (instrument shape) applied to a script
  written by hand twice in one session. The Why is measured from the 6 archived
  `trade_diagnostics.json` files, and the F7 check that could have refuted it was
  run and reported rather than skipped.
