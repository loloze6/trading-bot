# STRATEGY_DESIGN_GUIDE.md

How to design a strategy config (`strategy_config.json`) for the backtest engine without reading code: how a config
becomes a trade, every key and option, how components combine, and what the config cannot express. Read together
with `COMPONENT_CATALOG.md`, the inventory of every component and exactly what each outputs.

## How a config becomes a trade

On every completed candle, for one symbol, the engine does this:

1. **The window.** The strategy receives the last `required_bars + 100` bars of that symbol (`required_bars` is the
   largest warmup among the detector's and the strategies' components, and at least 24). Columns: `timestamp`,
   `open`, `high`, `low`, `close`, `volume`, `stddev_24` (24-bar rolling standard deviation of the close), plus one
   column per data feed (`funding_rate`, `fear_greed`, ...). The strategy does NOT see its position, PnL, balance,
   entry price, costs or any other symbol.
2. **The regime.** The regime detector computes its components' values from the window and classifies the bar into
   one regime: `trending`, `mean_reversion`, `chop` or `unknown`.
3. **The regime's components.** Each component of that regime outputs a raw value, which is appended to its own
   history (after `history_transforms`). Each component's `transforms` pipeline then turns its history into one
   number, and the numbers are averaged by weight:

   `forecast = sum( weight_i / sum(weights) x pipeline_i(history_i) )`, clipped to `[-20, +20]`.

   A regime set to `null` has forecast 0.0 (flat).
4. **The allocation.** `allocation = forecast / 10`: the target position as a fraction of equity. Forecast +10 is
   100 percent long, +20 is 200 percent long, -20 is 200 percent short. The allocation is linear in the forecast.
5. **The rebalance.** The bot trades toward the target allocation, filling at that bar's close. The risk layer sits
   outside the strategy config: it rejects a rebalance whose
   size `abs(target - actual allocation)` is below `min_allocation_change` (default 0.2, that is 2 forecast points)
   or above 4.0. The key `strategies.min_allocation_change` overrides the minimum for this strategy.

The forecast is 0.0 until the strategy is ready (see "The forecast for each regime").

## The design principle

**Hard rule (D-051): every forecast must be graded.** Position size must follow signal strength. The allocation is
the forecast divided by 10, so a component that feeds the forecast must output a value that grows with the strength
of the signal: a stronger signal, a bigger position; a weaker one, a smaller position.

- **Refused as forecast sources (on/off).** A component that sits at 0 and jumps to a level when a condition
  fires, or that only takes a few fixed values, does not give a position that follows signal strength. These
  classes must not appear in `strategies`: `SmaTrendLongOnlyComponent`, `GatedSmaTrendLongOnlyComponent`,
  `FundingRateMeanReversionComponent`, `FearGreedContrarianComponent`, `MacdHistogramCrossoverComponent`,
  `WhaleLargeTradeImbalanceComponent`, `VolumeExpansionHedgeComponent`. They are the rows marked **on/off** in the
  "Kind" column of `COMPONENT_CATALOG.md`. A config that uses one will be refused once that check ships; do not
  use them.
  Graded versions exist for three of them: `FundingRateGradedComponent`, `FearGreedGradedComponent`,
  `MacdHistogramGradedComponent`. For an SMA-style trend, use `MacroTrendFilterComponent` (percent distance from an
  EMA, `period` settable); there is no SMA version.
- **No dead zones.** The transforms `threshold_filter` and `volume_filter` must not be used on a component in
  `strategies`: they zero the forecast below a threshold, so the position jumps from 0 to the threshold
  (`min_abs: 15` gives 0 or 15..20), which is on/off at the edge. A condition such as "volume above its average"
  or "signal strong enough" belongs in the regime detector (a rule or veto), where both ops remain allowed in
  vetoes. A graded dead zone that starts from 0 does not exist yet.
- **An on/off condition is a regime.** If the idea is "when X happens, take this kind of position", X belongs in the
  regime detector (a rule on a regime measure, or a veto), the regime it selects gets a GRADED component in
  `strategies.regimes`, and the other regimes are `null` (flat). The regime decides when the idea is active; the
  graded component decides how much and in which direction. Interim: while the hypothesis stage still receives
  cards without regime conditions (until D-052 lands), an on/off condition the card does not carry as a regime is
  declared as a deviation, not built as a regime.
- **Constant.** `BuyAndHoldStrategy` (constant +10) is an offset only: use it inside a composition with a graded
  component (see "Composing a signal"), never as the signal.
- **A rule stated as a threshold becomes a graded measure.** "Long above the 20-day high, short below the 20-day
  low" has a graded counterpart: where the close sits inside its recent range (`DonchianBreakoutComponent`:
  continuous, -`sf` at the bottom of the range, +`sf` at the top). State the difference from the idea as written
  as a deviation; do not pretend the threshold rule was built.

How to tell: run the component mentally over a year of bars. If its output takes two or three distinct values
(0 and a level, or -level, 0, +level), it is on/off. If it takes a continuum of values, it is graded.

## Config shape

```json
{
  "regime_detector": { ... },
  "strategies":      { ... },
  "aux_feeds":       [ ... ]
}
```

| Top-level key | Required | Meaning |
|---|---|---|
| `regime_detector` | yes | classifies each bar into a regime (next section) |
| `strategies` | yes | what to forecast in each regime (section "The forecast for each regime") |
| `aux_feeds` | no | names of data feeds the config depends on. The engine ignores it; the research tools read it (data-availability check). A config that uses a feed-based component should list that component's feed, for example `["fear_greed"]`. See the feeds section of `COMPONENT_CATALOG.md` |

Keys of `strategies`:

| Key | Required | Meaning |
|---|---|---|
| `regimes` | yes | regime name to forecast config, or `null` (flat). A regime that is absent behaves like `null`; list all four for clarity |
| `min_allocation_change` | no | non-negative number; overrides the risk layer's minimum rebalance size for this strategy (default 0.2) |
| `warmup` | no | accepted and IGNORED: the strategy overrides it with its own computed `required_bars`. Existing configs carry `"warmup": 51` harmlessly |

**Unknown keys are silently ignored** at every level: an extra top-level key, an extra key in a component spec,
and a misspelt key inside `params` all pass validation and do nothing (for `params`, the default is used instead).
Check every key and every param name against this guide and the catalogue. (The pipeline may carry a few top-level
keys of its own for its tools, for example `significance_methodology` when a brief requires it; the engine does not
read them.)

## Regime detector

Decides, on each bar, which of the four regimes is active.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `mode` | `"threshold_rules"`, `"score"` or `"score_product"` | `threshold_rules` | classification algorithm |
| `components` | list | required (may be `[]`) | the measurements the rules, vetoes and scores use (component spec: `id`, `class`, `params`) |
| `vetoes` | list | `[]` | evaluated FIRST every bar, in every mode |
| `rules` | list | `[]` | `threshold_rules` mode only: priority-ordered, first match wins |
| `default_regime` | regime name | `"unknown"` | `threshold_rules`: the regime when no rule matches (and the regime of every bar in the ungated pattern). No effect in the two score modes |
| `regimes` | dict | `{}` | score modes only: per-regime scoring components |
| `min_score` | float | 0.35 | score modes: the winner must reach this |
| `min_margin` | float | 0.05 | score modes: winner minus runner-up must reach this, else `unknown` |

The detector's components need only `id`, `class` and `params`. `weight`, `lookback` and `history_transforms` on
`regime_detector.components` are ignored. Use the catalogue's regime measures (`RSquaredRegimeComponent`,
`EfficiencyRatioRegimeComponent`, `VolatilityPercentileRegimeComponent`, `VarianceRatioComponent`, and the signed
`ADXDirectionalComponent` with range -1 to +1) for thresholds: their scale does not depend on the asset. Any other
component can be referenced too, but its scale is asset- and timeframe-dependent.

### Veto
```json
{"id": "vol", "transforms": [{"op": "identity"}],
 "rules": [{"op": "gte", "value": 0.90}],
 "consecutive_bars": 2, "result": "chop"}
```
`id` must be a declared detector component (the engine raises at startup otherwise). The `transforms` key is
required. `rules` are ANDed against the TRANSFORMED value. The first veto (in list order) whose rules all pass for
`consecutive_bars` bars in a row (default 1) forces its `result` regime for that bar, in every mode; the streak
resets to 0 on any bar the veto does not fire.

### Rule (threshold_rules mode)
```json
{"regime": "trending", "any_of": [
  [{"id": "er", "op": "gte", "value": 0.25}, {"id": "vr", "op": "gte", "value": 1.10}],
  [{"id": "er", "op": "gte", "value": 0.30}, {"id": "vr", "op": "between", "low": 0.90, "high": 1.10}]
]}
```
Per bar, the detector walks `rules` top to bottom and the first rule that matches wins; no match gives
`default_regime`. `any_of` is an OR of condition sets; each set is an AND of conditions. Conditions compare the
RAW latest value of the component: rules apply no transforms. Operators: `gte`, `gt`, `lte`, `lt`, and `between`
(with `low` and `high`, inclusive). Write `gte`, not `>=`.

### Score mode
Each regime in `regime_detector.regimes` scores the bar: `score = sum(weight x transformed value) / sum(weights)`,
a weight-normalised average (only weight ratios matter; to reach `min_score`, change the transform output scales,
not the weights). The winner is the highest score, and it must reach `min_score` and lead the runner-up by
`min_margin`, else the bar is `unknown`. Entries reference declared detector components by `id`. Use transforms
whose outputs are comparable across regimes (the 0-to-1 percentile ops are the safe choice). Readiness is stricter
than in `threshold_rules`: every detector component's history must be full.
```json
"regimes": {
  "trending": {"components": [
    {"id": "er", "weight": 0.45, "transforms": [{"op": "percentile"}]},
    {"id": "vr", "weight": 0.55, "transforms": [{"op": "percentile"}]}
  ]},
  "mean_reversion": {"components": [
    {"id": "vr", "weight": 1.0, "transforms": [{"op": "negate_percentile"}]}
  ]}
}
```

### Score-product mode
Each regime scores the bar as a product: `score = product( transformed value / divisor )` over its components
(`divisor` optional, default 1.0). Same `min_score` and `min_margin` gate. Use it when the idea is a product of
measures. With one regime defined, the margin is always 1.0 and only `min_score` decides. It cannot express
"fire when the score is below a threshold" or smooth the score.
```json
"regime_detector": {
  "mode": "score_product",
  "min_score": 0.4,
  "min_margin": 0.0,
  "components": [
    {"id": "er", "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent", "params": {"period": 24, "smooth_period": 5}},
    {"id": "vr", "class": "strategies.strategy_components.VarianceRatioComponent", "params": {"k": 5, "window": 100}}
  ],
  "regimes": {
    "trending": {"components": [
      {"id": "er", "divisor": 1.0, "transforms": [{"op": "identity"}]},
      {"id": "vr", "divisor": 2.0, "transforms": [{"op": "identity"}]}
    ]}
  },
  "default_regime": "unknown"
}
```
With ER = 0.5 and VR = 2.0 the product is 0.5 x 1.0 = 0.5, at or above 0.4: `trending`. With ER = 0.6 and
VR = 0.8 it is 0.6 x 0.4 = 0.24: `unknown`.

### Ungated: a strategy with no regime condition
When the signal should be active on every bar, leave the detector empty and put the real components under one
regime name; every bar then resolves to `default_regime`:
```json
"regime_detector": {
  "mode": "threshold_rules",
  "components": [],
  "rules": [],
  "default_regime": "unknown"
},
"strategies": {
  "regimes": {
    "unknown": { "components": [ /* the real signal */ ] },
    "trending": null, "mean_reversion": null, "chop": null
  }
}
```
Do not invent a dummy always-true rule with an invented regime name (validator V7 rejects the name). When the
detector is fully ungated (no components, no rules), `default_regime` may be any of the four names, as long as
`strategies.regimes[default_regime]` holds the components: pointing it at a `null` regime is a config that
forecasts 0.0 on every bar forever (validator V10). This guide uses `"unknown"` by convention.

### Limits of the detector, stated plainly
- An unknown `mode` string silently runs `score` mode.
- An unknown rule `op` silently evaluates to false (the rule never matches).
- A rule that names a component with no history yet evaluates to false.
- The four names are only labels: a rule can map any condition to any of them, and at most four distinct regimes
  can exist at once.

## The forecast for each regime

`strategies.regimes.<name>` is either `null` (forecast 0.0, flat) or an object with `components`:

```json
"mean_reversion": {
  "components": [ <component spec>, ... ]
}
```

### Component spec

| Key | Type | Default | Meaning |
|---|---|---|---|
| `id` | string | required | unique within the regime |
| `class` | dotted path | required | `strategies.strategy_components.<ClassName>`, a class from `COMPONENT_CATALOG.md` |
| `params` | dict | `{}` | passed to the component constructor; unknown or misspelt keys are silently ignored and the default is used |
| `weight` | number | required | ensemble weight. May be NEGATIVE (it subtracts the component); only the regime's total must be greater than 0 (validator V8) |
| `lookback` | int | derived | size of the component's history. If omitted it is the same for every component in `strategies`: the largest, over all components of all regimes, of (the larger of that component's warmup and its transforms' minimum periods), or 50 when there is no component. It is not computed per component. Set it explicitly with `ratio_to_mean`, `percentile` or `zscore`: it is the statistic's window (production uses 500). An explicit value must be at least the largest minimum period of the component's ops (validator V6; the strategy refuses to start otherwise) |
| `history_transforms` | list of steps | `[]` | applied once when the raw value is stored, so the history holds transformed values. Use it for per-bar normalisation such as `vol_normalize` |
| `transforms` | list of steps | required | the pipeline run at every forecast. Always present: the validator does not check that the key exists, but without it the strategy raises an error on every bar and the run trades nothing. Write `[]` for none |

A transform step is `{"op": "<name>", "params": {...}}`. See "Transform ops".

### What the engine does with a spec
- Every component of every regime is updated on every bar, whichever regime is active. Its raw value is appended to
  its history once the component itself is ready.
- A forecast needs at least 2 history entries for every component of the regime, else the forecast is 0.0.
- The strategy is ready, and emits forecasts, only when the bar window holds `required_bars` bars AND the detector
  is ready AND every component of the classified regime has stored at least `min(required_bars, S)` values, where
  `S` is the smallest history size (`lookback`) of any component in `strategies`, in any regime. One component with
  a short explicit `lookback` therefore lowers the warmup of the whole config.
  Measured on synthetic bars: `RSIPullbackComponent(14)` with `identity` forecasts from bar 29; the same component
  with `ratio_to_mean` from bar 38; `SmaTrendLongOnlyComponent(100)` from bar 201. Before readiness the forecast is
  0.0 and nothing trades.
- If any component value or pipeline result is NaN, the regime forecast is NaN for that bar (a NaN component makes
  the weighted sum NaN); a NaN is never turned into "flat". The catalogue's "Data & NaN" column says which
  components can produce one.

### Block combiner and `weight_schedule` (written by the composition tooling, not hand-designed)
- `blocks` with `block_standardisation` (both or neither; validator V13): a regime built from validated pieces of
  other configs, each standardised against its own past. A config that contains them is valid.
- `weight_schedule` (only alongside `blocks`): per-date block weights that replace the blocks' own weights from each
  `from` date on.

## Transform ops

Fifteen ops. A pipeline is applied in order, seeded with the latest raw value of the component's history.

**History ops** recompute from the component's stored history and DISCARD the value accumulated so far, so they must
come first (validator V5 rejects a history op after a scalar or data-aware op). `identity` is one of them:
`[scale, identity]` throws the scale away.

| op | params (default) | output |
|---|---|---|
| `identity` | none | the latest stored value |
| `percentile` | none | rank of the latest value within the history, above 0 up to 1 |
| `negate_percentile` | none | 1 minus `percentile`, 0 up to below 1 |
| `zscore` | none | (latest - mean) / std of the history (sample std); 0 if std is about 0 |
| `ratio_to_mean` | none | latest / mean(abs(history)); NaN entries are skipped; 0 if the mean is about 0 |
| `ema` | `span` (10) | exponentially weighted mean of the history, span limited to the history length |

**Scalar ops** act on the accumulated value.

| op | params (default) | output |
|---|---|---|
| `scale` | `factor` (1.0) | v x factor |
| `threshold_filter` | `min_abs` (0.0) | v if abs(v) >= `min_abs`, else 0.0 (dead-zone: the forecast jumps from 0 to `min_abs` at the threshold). **Not allowed in `strategies`** |
| `clip` | `min` (no lower bound), `max` (no upper bound) | v limited to `[min, max]` |
| `sigmoid` | none | 1 / (1 + exp(-v)), between 0 and 1 (0.5 at v = 0) |
| `negate` | none | -v |

**Data-aware ops** read the current bar window.

| op | params (default) | output |
|---|---|---|
| `vol_normalize` | none | v / (`stddev_24` x close). Unguarded: NaN propagates by design. Meant for `history_transforms` |
| `vol_adjusted` | none | v / (`stddev_24` x close), or v unchanged if the denominator is invalid. Read-time use only; do not use it to normalise history |
| `price_normalized` | none | v / close (v unchanged if close is invalid) |
| `volume_filter` | `period` (20) | v if the latest volume >= its `period`-bar mean, else 0.0 (dead-zone on volume). **Not allowed in `strategies`** |

**Ordering rule.** In one list, history ops first, then scalar and data-aware ops (V5). `history_transforms` and
`transforms` are separate lists, each checked on its own.

**Minimum periods (V6).** Each history op needs enough history to be reliable: `percentile` and `negate_percentile`
50, `zscore` and `ratio_to_mean` 30, `ema` 3 x `span`, all others 1. The default `lookback` already covers this; an
explicit `lookback` below the largest minimum fails validation.

**`scaling_factor` cancels under normalisation.** Under `ratio_to_mean`, `zscore` and `percentile` the component's
own `scaling_factor` has no effect on the forecast (the statistic divides it out, or ranks it away): only its sign
survives. To size the forecast, put a `scale` op after the normalisation (for example `ratio_to_mean` then `scale`
10 gives an average absolute forecast of about 10). Where a component ignores `scaling_factor` altogether, the
catalogue says so.

**Percentile and sigmoid outputs are one-sided** (0 to 1). They suit regime scores; as a forecast they would be
long-only unless re-centred.

## Composing a signal

Before concluding that a component is missing (`component_gap`), try compositions of the existing components. The
mechanics below are all graded. All examples use the ungated pattern; the four
regime keys are shown once in full, the same way in every example.

**The weighted mean.** The forecast is `sum(weight_i x value_i) / sum(weights)`. Adding a component changes the
scale of the result: two components with weight 1 each average their values. To keep a signal's magnitude while
combining, size the pipelines with `scale` or choose weights accordingly. A component that is 0 for part of the run
dilutes the other one there.

**Combining horizons.** Two components of the same kind at different horizons average into one smoother, slower
signal. The forecast is exactly the weighted mean of what each would forecast alone (as long as neither is clipped
at +/-20 on its own, which is why the slower spread, whose percent distance is larger, gets the smaller
`scaling_factor`).

<!-- example: two_trend_horizons -->
```json
{
  "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
  "strategies": {"regimes": {
    "unknown": {"components": [
      {"id": "fast", "class": "strategies.strategy_components.EMASpreadComponent",
       "params": {"fast_period": 12, "slow_period": 26, "scaling_factor": 5.0},
       "weight": 1.0, "transforms": [{"op": "identity"}]},
      {"id": "slow", "class": "strategies.strategy_components.EMASpreadComponent",
       "params": {"fast_period": 50, "slow_period": 200, "scaling_factor": 1.0},
       "weight": 1.0, "transforms": [{"op": "identity"}]}
    ]},
    "trending": null, "mean_reversion": null, "chop": null
  }}
}
```

**Subtracting a signal (negative weight).** A negative weight subtracts a component; the regime's total weight must
stay above 0. Weights 2 and -1 give `2 x a - b` (before the final clip to +/-20). Below: a 50-bar trend minus the 10-bar run-up, which is long when
the long trend is up and the last few bars have not already run ahead of it.

<!-- example: subtract_short_term_run_up -->
```json
{
  "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
  "strategies": {"regimes": {
    "unknown": {"components": [
      {"id": "trend", "class": "strategies.strategy_components.PriceEvolutionComponent",
       "params": {"period": 50, "scaling_factor": 0.5},
       "weight": 2.0, "transforms": [{"op": "identity"}]},
      {"id": "run_up", "class": "strategies.strategy_components.PriceEvolutionComponent",
       "params": {"period": 10, "scaling_factor": 0.5},
       "weight": -1.0, "transforms": [{"op": "identity"}]}
    ]},
    "trending": null, "mean_reversion": null, "chop": null
  }}
}
```

**A constant offset to centre a one-sided signal.** `BuyAndHoldStrategy` is the constant +10. With `scale` it is
any constant. A one-sided graded signal can be centred into a signed one by subtracting a constant. A percentile
rank is one-sided and graded: the `percentile` op returns where the latest value sits inside its own history, above
0 up to 1. Below, the EMA spread's rank is scaled to (0, 20] and the offset is -10, so the forecast is
`20 x rank - 10`: about -10 when the spread is at the bottom of its recent history, +10 at the top, graded in
between. The two pipelines are sized (x40 and -20, averaged by equal weights) to make the weighted mean exactly that.

The input must be graded ACROSS its range: check that it does not sit at its boundary value on many bars.
`RSIPullbackComponent` with `long_only: true` is exactly 0 on every bar where RSI >= 50 (about half of them), so
centred it would be a constant -10 (100 percent short) on all of those bars: not a graded signal.

<!-- example: centre_one_sided_signal -->
```json
{
  "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
  "strategies": {"regimes": {
    "unknown": {"components": [
      {"id": "rank", "class": "strategies.strategy_components.EMASpreadComponent",
       "params": {"fast_period": 12, "slow_period": 26},
       "weight": 1.0, "lookback": 500,
       "transforms": [{"op": "percentile"}, {"op": "scale", "params": {"factor": 40.0}}]},
      {"id": "offset", "class": "strategies.strategy_components.BuyAndHoldStrategy",
       "params": {},
       "weight": 1.0, "transforms": [{"op": "scale", "params": {"factor": -2.0}}]}
    ]},
    "trending": null, "mean_reversion": null, "chop": null
  }}
}
```

**Sign flip.** To reverse a signal's direction, append `negate`. For a class that uses `scaling_factor`, a negative
`scaling_factor` does the same; `PriceEvolutionOnPeriodComponent`, `MomentumDivergenceComponent` and
`VolatilityFromStdDevComponent` ignore it, and `EMADiff` has none. Below, a Donchian range position
flipped: short near the top of the 20-bar range, long near the bottom (a mean-reversion reading).

<!-- example: sign_flip_negate -->
```json
{
  "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
  "strategies": {"regimes": {
    "unknown": {"components": [
      {"id": "range", "class": "strategies.strategy_components.DonchianBreakoutComponent",
       "params": {"period": 20, "scaling_factor": 20.0},
       "weight": 1.0, "transforms": [{"op": "identity"}, {"op": "negate"}]}
    ]},
    "trending": null, "mean_reversion": null, "chop": null
  }}
}
```

**Long-only from a signed component.** `clip` with `min: 0` removes the short side and keeps the long side graded.

<!-- example: long_only_from_signed -->
```json
{
  "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
  "strategies": {"regimes": {
    "unknown": {"components": [
      {"id": "trend", "class": "strategies.strategy_components.PriceEvolutionComponent",
       "params": {"period": 30, "scaling_factor": 1.0},
       "weight": 1.0, "transforms": [{"op": "identity"}, {"op": "clip", "params": {"min": 0.0}}]}
    ]},
    "trending": null, "mean_reversion": null, "chop": null
  }}
}
```

More combinations the config supports: different components in different regimes; a regime detector built from
any detector components with vetoes, rules or scores; per-component `history_transforms` and `lookback`; negative
weights on any component; the same class twice with different params (as above). A condition that switches an idea
on and off is a regime, not a component (see "The design principle").

## What the config cannot express

The config describes a forecast per bar. It has no key for:

- **Exits, stops, take-profit, trailing stops, time-based holds.** Position management is not configurable: the bot
  simply moves the allocation toward `forecast / 10` whenever the risk layer allows.
- **Position state.** A strategy cannot see its position, entry price, PnL or bars held. Only a few components keep
  their own internal state (`EfficiencyRatioRegimeComponent` and `VolatilityPercentileRegimeComponent` keep a
  smoothing history; `MacdHistogramCrossoverComponent` and `GatedSmaTrendLongOnlyComponent` remember prior bars);
  nothing else does.
- **Sizing other than `forecast / 10`.** There is no volatility-targeting, Kelly, leverage or cap key. The
  risk controls are not in the strategy config. (A signal can be divided by recent
  volatility with a data-aware transform such as `vol_adjusted`; that changes the forecast, and the allocation is
  still forecast / 10.)
- **Per-symbol settings.** The config has no per-symbol section; a component sees only its own symbol's bars and
  feed columns.
- **Symbols, timeframe and date windows.** They belong to the run protocol, not the config (no instrument,
  timeframe or symbol key exists; see `DATA_AVAILABILITY.md` for what data exists per timeframe).
- **New regime names, new transform ops, new indicators, new comparison operators.** These need code.
- **Transforms or `consecutive_bars` on regime rules.** Only vetoes and score entries carry transforms; rules
  compare raw values.

What to do when an idea hits one of these limits: express the idea as a graded forecast that comes closest; state
the part that cannot be expressed as a deviation from the idea; and report `component_gap` only when a graded
component is genuinely missing after trying the compositions above. Examples of a genuine gap: a graded forecast
that follows a feed's level (the funding, sentiment and whale components are all on/off), or an indicator that is
not in the catalogue at all.

## Manifest contract

When stage 1b finishes with status `spec_ready`, it writes `artifacts/block_manifest.yaml` next to
`backtest_spec.yaml`. The manifest says which part of the config IS the hypothesis's block, as opposed to
scaffolding, so the block can be stored on its own.

```yaml
block:
  kind: forecast                 # forecast | regime -- the only two block kinds
  config_paths:                  # non-empty; JSON pointers into the config
    - /strategies/regimes/unknown/components/0
scaffolding:                     # may be []; config the idea needs but that is not the idea
  - /regime_detector
rationale: the RSI pullback component is the hypothesis; the ungated detector only runs it
```

Rules (every one enforced by code):

1. Exactly the keys `block` (with exactly `kind` and `config_paths`), `scaffolding` and `rationale`, no others.
   `rationale` is a non-empty string.
2. `kind` is `forecast` or `regime`. A `forecast` block has at least one `config_paths` entry inside a named regime
   (`/strategies/regimes/<name>` or deeper; the bare `/strategies/regimes` names no regime); a `regime` block has at
   least one at or under `/regime_detector`.
3. Every pointer (block and scaffolding) is an RFC 6901 JSON pointer into the strategy config itself
   (`/strategies/...`, not `/config/strategies/...`) and resolves in the config. Pointers are distinct.
4. No pointer lies inside another's subtree: not two block paths, not a block path and a scaffolding path, not two
   scaffolding paths. Each piece of config is listed once, as block or scaffolding.
5. No coin, symbol, timeframe or instrument field (a validated block is usable on any coin), and no
   `hypothesis_id`.

The orchestrator checks the manifest right after stage 1b: a missing or invalid manifest sends 1b back once with
the error; a second failure stops the run. A variant may change scaffolding, but a variant whose patch removes a
block path is not tested.

## Worked examples

### The production mean_reversion component
This is the component `trading-bot/strategy_config.json` runs under `strategies.regimes.mean_reversion` (the
production detector gates it with efficiency-ratio and variance-ratio rules), shown WITHOUT its last transform:
production additionally applies a `threshold_filter` dead zone (`min_abs: 15`), which is not allowed in a new
config. It illustrates the transform chain:
```json
{"id": "rsi", "class": "strategies.strategy_components.RSIPullbackComponent",
 "params": {"period": 14, "scaling_factor": 0.4, "long_only": true},
 "weight": 1.0, "lookback": 500,
 "history_transforms": [{"op": "vol_normalize"}],
 "transforms": [
   {"op": "ratio_to_mean"},
   {"op": "scale", "params": {"factor": 10.0}}
 ]}
```
Reads as: store vol-normalised pullback scores (500 deep); current value divided by the mean absolute value of
that history (so an average signal is 1); times 10 (an average signal is 10); the regime clips to +/-20.

### A graded, ungated example: normalised trend
One graded trend component, normalised so that its average absolute forecast is about 10 whatever the asset's
price level or volatility, with no regime condition.

<!-- example: normalised_trend -->
```json
{
  "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
  "strategies": {"regimes": {
    "unknown": {"components": [
      {"id": "trend", "class": "strategies.strategy_components.EMASpreadComponent",
       "params": {"fast_period": 12, "slow_period": 26},
       "weight": 1.0, "lookback": 500,
       "transforms": [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 10.0}}]}
    ]},
    "trending": null, "mean_reversion": null, "chop": null
  }}
}
```
Reads as: store the EMA spread (500 deep); divide the latest value by the mean absolute value of that history; times
10. The forecast is signed, continuous, and its average absolute value is about 10 (the component's
`scaling_factor` is irrelevant here: it cancels).

## Checklist and validator rules

Before emitting a config (the validator's rules are in the table below; these are the checks it cannot make):

1. Component ids are unique within a regime; veto ids exist in the detector's `components` (the engine raises at
   startup otherwise).
2. Normalisation against per-bar state (volatility, price) goes in `history_transforms`, never at read time.
3. Set `lookback` explicitly on any component that uses `ratio_to_mean`, `percentile` or `zscore`.
4. Every component in `strategies` is graded and carries no dead-zone op. On/off conditions are regimes.
5. Every class comes from the catalogue; every `params` key is spelt as in the catalogue (a typo is silently
   ignored); `strategies.warmup` does nothing, do not tune it.
6. The regime that holds the components is the one the detector will actually select.

Validator rules (the strategy refuses to start on any violation):

| Rule | Checks |
|---|---|
| V1 | `regime_detector` and `strategies` exist; each `strategies.regimes.<name>` is an object or `null` |
| V2 | every veto id, rule-condition id and score-entry id is declared in `regime_detector.components` |
| V3 | every op in a `transforms` or `history_transforms` list exists in the op registry |
| V4 | every op has a minimum-period entry (internal consistency of the registry) |
| V5 | in one list, no history op comes after a scalar or data-aware op |
| V6 | an explicit `lookback` is at least the largest minimum period of the component's ops |
| V7 | every regime name used (rule `regime`, veto `result`, `default_regime`, keys of `regimes`) is one of the four |
| V8 | each strategy component has a numeric `weight`, and each non-null regime's total weight is above 0 |
| V9 | in `threshold_rules` and `score_product` mode with non-empty `rules`, `default_regime` is not `trending`, `mean_reversion` or `chop` |
| V10 | a fully ungated detector (no components, no rules) does not point `default_regime` at a null or missing regime |
| V11 | `strategies.min_allocation_change`, when present, is a non-negative number |
| V12 | every `class` path in the detector and in the strategies imports to a class (it does not check that the class is a component, or that `params` are right) |
| V13 | the block combiner keys (`blocks`, `block_standardisation`, `weight_schedule`) have the exact shape above |
