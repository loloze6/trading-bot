# CLAIM_TESTS.md: the claim block and its test slots (E-068)

You are reading this file because `orchestrator.claim_tests.enabled` is on. It is added to
step 1a's inputs only under that flag. When it is present, `hypothesis_card.yaml` MUST carry
a `claim` block as described here. Code (`tools/claim_card.py`) checks the block before any
other step runs. If the check fails, you get one retry with the error; if the retry fails too,
the run fails.

The block list below is kept equal to `tools/claim_tests.py` by a test. Use only what is listed
here. Do not invent blocks, fields or parameters.

## 1. What to write

```yaml
claim:
  statement: >                       # the claim, in words a new joiner can read
    After a daily close in the top 20% of its 20-day range, returns over the next
    1 to 5 days are higher than on other days.
  kind: conditional_behaviour        # one of the kinds in section 4
  tests:                             # 1 to 3 tests; the claim is supported only if ALL pass
    - name: upper_breakout           # unique within the claim
      selector:  {kind: event, field: forecast, op: ">=", value: 12}
      outcome:   {kind: fwd_return, horizons: [1, 2, 3, 4, 5]}
      baseline:  {kind: complement}
      statistic: mean_diff
      direction: greater
      floor:     {min_events: 100, min_windows: 4}
      consistency: {unit: window, min_same_sign: 4}   # optional
  pass_if: >   # restate the code's rule (section 3) in plain words for THIS claim
    At every horizon, breakout days beat other days significantly, and the effect points
    the same way in at least 4 windows, with at least 100 breakout days.
  fail_if: >
    At any horizon, breakout days are significantly WORSE than other days.
  rationale: >                       # why these tests answer this claim
    If herding drives continuation after a breakout, the days just after it must beat
    ordinary days over the stated horizon; a linear IC over all days would dilute it.
```

- **`alpha` and `significance` are set by code.** Never write them.
- **`pass_if` / `fail_if` decide nothing.** The verdict rule is fixed in code (section 3).
  Restate that rule in plain words for your claim; do not invent another one.
- **Horizons are in bars** of the run's timeframe (1h bars: 24 = one day).
- **Fix the test now, before any data.** It is stored with its hash and never changed after.
- **The test reads what the block produces** (`forecast`, or `regime` for a regime block). It
  never contains the block's code. Step 1b decides whether the idea is a block, and of which
  kind (`block_manifest.yaml`). If your test and 1b's block disagree, a warning is recorded
  and the run continues.

### When a menu criterion is the test

Some kinds are already tested by a criterion in your card's own `criteria` list
(`cost_turnover` -> `realized_edge_to_cost_ratio`; `robustness` -> `sign_consistent_by_era`).
Name those criteria instead of, or in addition to, `tests`:

```yaml
  criteria_refs: [realized_edge_to_cost_ratio]   # ids from this card's `criteria` list only
```

### When the slots cannot express the test

Do not force a test that does not measure the claim. Write `tests: none` and name the missing
building block:

```yaml
  tests: none
  missing_block: "outcome fwd_return_of(other_symbol, h): BTC's return predicting SOL's"
```

The idea is then parked, not stopped. A test request is recorded, and the idea runs once a
person has added the block.

## 2. The four slots

> **On these bars** (selector), **what happens next** (outcome) is **different from these
> other bars** (baseline), **measured like this** (statistic).

### Selector: which bars (reads bar t only, never the future)

| kind | parameters | selects |
|---|---|---|
| `all` | none | every bar |
| `event` | `field`: `forecast` or `close`; `op`: `>=` `>` `<=` `<` `==`; `value`: a number | bars where `field op value` |
| `quantile` | `field`: `forecast` or `close`; `side`: `top` or `bottom`; `q` in (0, 0.5]; `lookback`: int >= 2 | bars in the top/bottom `q` of the trailing `lookback` bars (past only) |
| `calendar` | `weekdays`: list of 0 (Monday) .. 6 and/or `hours`: list of 0 .. 23 (UTC) | bars on those days/hours |
| `regime` | `value: <label>` or `values: [<labels>]` | bars whose regime label is one of these |
| `regime_change` | `to: <label>` | bars where the regime label changes to `to` |

**Regime selectors are effect-size only for now.** No calibrated significance method exists
for regime labels yet (CUL-391), so such a test reports its effect size and is marked
`verdict_possible: false`. Write them anyway when the claim is about a regime: the run
continues normally, and the measured effect is kept.

### Outcome: what happens next (the label, computed by code)

| kind | value at bar t, for each horizon h |
|---|---|
| `fwd_return` | close[t+h] / close[t] - 1 |
| `fwd_volatility` | sample std of the h one-bar log returns after t (needs h >= 2) |
| `fwd_max_drawdown` | lowest close over the next h bars / close[t] - 1 |
| `trend_ends` | 1 if the next-h-bar move has the opposite sign of the last-h-bar move, else 0 |

`horizons`: a non-empty list of distinct ints >= 1, for example `[1, 2, 3]` or `[24, 72]`.

### Baseline: compared with what

| kind | parameters | the other bars |
|---|---|---|
| `complement` | none | all bars not selected |
| `placebo` | optional `n_draws` (default 20) | the same selection moved to other dates; the default when the claim has no natural comparison |
| `other_selector` | `selector`: any selector above | the bars that selector picks (minus the selected ones) |

With `statistic: rank_ic` there is no baseline: write `baseline: null` or leave it out.

### Statistic: measured how

| name | measures |
|---|---|
| `mean_diff` | mean outcome on the selected bars minus the baseline's mean |
| `hit_rate` | share of selected bars whose outcome points the claimed way, minus the baseline's share |
| `rank_ic` | rank correlation of the bar-t `forecast` with the outcome, on the selected bars |
| `decay_curve` | `mean_diff` at each horizon, reported as a curve (use several horizons) |

`direction`: `greater` (the claim says higher / positive) or `less`.

### Floor and consistency

- `floor` (required): at least one of `min_events`, `min_windows`, `min_eras`, `min_blocks`,
  each an int >= 1. Below any floor the result is inconclusive, never a pass. Use
  `min_events` for a rare event selector; `min_blocks` only means something for `all`.
- `consistency` (optional): `{unit: window | era, min_same_sign: <int >= 1>}`, meaning the
  effect must point the claimed way in at least that many windows or eras.
- Pick floors the windows can reach: an event that fires twice a month will not reach 100
  events in six one-month windows.

## 3. The verdict rule (fixed in code; restate it in `pass_if` / `fail_if`)

The floor must be met at every horizon. Then:
- **supported**: right direction and significant at every horizon, and the consistency rule is met;
- **refuted**: at any horizon, the OPPOSITE effect is itself significant;
- **inconclusive**: everything else, including a non-significant wobble in the wrong
  direction and anything below the floor.

With several tests, the claim is supported only if every test is. A refuted test makes the
claim refuted. Until a significance method is calibrated, only effect sizes are reported.

## 4. Kinds and tests that fit them

| kind | example test (selector + outcome + baseline + statistic) |
|---|---|
| `regime_classifier` | `regime` + `fwd_return` or `fwd_volatility` + `complement` + `mean_diff` |
| `regime_transition` | `regime_change` + `trend_ends` + `placebo` + `hit_rate` |
| `direction_forecast` | `all` + `fwd_return` + (none) + `rank_ic` |
| `volatility_forecast` | `all` + `fwd_volatility` + (none) + `rank_ic` |
| `event_behaviour` | `event` + `fwd_max_drawdown` + `placebo` + `mean_diff` |
| `conditional_behaviour` | `regime` or `event` + `fwd_return` + `complement` + `mean_diff`, or + `rank_ic` |
| `horizon_decay` | `event` + `fwd_return` over several horizons + `complement` + `decay_curve` |
| `calendar_effect` | `calendar` + `fwd_volatility` + `complement` + `mean_diff` |
| `redundancy` | `criteria_refs` (residual IC, when your criteria list has it) |
| `lead_lag` | `tests: none` (missing outcome `fwd_return_of(other_symbol, h)`) |
| `data_feed_value` | `criteria_refs`, or a test on the feed-built forecast |
| `cost_turnover` | `criteria_refs: [realized_edge_to_cost_ratio]` |
| `robustness` | `criteria_refs: [sign_consistent_by_era]` |

The `kind` says whether the idea could be a block: a forecast kind is a forecast-block
candidate, a regime kind is a regime-block candidate, and `calendar_effect` is a finding only.
