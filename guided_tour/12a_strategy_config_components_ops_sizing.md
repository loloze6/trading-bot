# Stop 12a: The strategy config, part a: its shape, the components, the transform ops, the sizing block

## Speech (verbatim)

**Stop 12 of 29: The strategy config and the engine's forecast.** Two parts: 12a, what a config is made of (this speech); 12b, how the engine turns it into a forecast each bar, and the validator (next). Open on the side: run_102's `artifacts/candidate_strategy_config.json`, `trading-bot/strategies/registry.py`, `trading-bot/strategies/strategy_components.py`.

**In one sentence.**
A strategy config is a recipe in a small file: which market states to recognise, which indicators to compute in each, how to reshape and weigh them into one number between -20 and +20 (the forecast), and how big a position that number should become.

**Why it exists.**
The research must test many ideas without writing new code for each. So the engine is built once, from fixed parts, and every idea is expressed as a different assembly of those parts.
That keeps every idea comparable, every test repeatable from one file, and every change visible as a difference between two files.

**What comes in, what goes out.**
- In: written by step 1b (stop 10) for the base, and by step 5a (variant building, stop 16) for each variant.
- Out: one file per variant, read by the trading engine at the start of each backtest window.
- Next: the engine's two halves (12b) and the per-bar trading cycle (stop 13).

**What happens here, step by step.**
1. A config has two top parts. The **regime detector** labels each bar with one of four market states (trending, mean reversion, chop, unknown), using its own components and rules. The **strategies** part says, for each state, which components make the forecast; a state set to nothing means stay flat.
2. A **component** is one indicator from a fixed list of 28: moving-average spreads, distance from an average, breakouts, momentum, volatility, funding rate, fear and greed, and others. Each has an id, a class name, its parameters and a weight.
3. Each component's output is kept as a history. Its **transforms** reshape that history into one number. There are 18 transform ops (operations): some recompute from the whole history (standardise, z-score, percentile, ratio to mean, smoothing), some change the current value (scale, clip, negate, sigmoid, signed power, a dead-zone filter), some read the current bar (volatility normalise, price normalise, volume filter, volatility target). History ops must come before the others.
4. **Standardise** is the one every forecast component must start with (decision D-149, a row of the decision log): the current value divided by the average size of its own past values (the current one excluded), times 10, capped at ±20. So every component speaks the same scale.
5. The **sizing block** (decision D-176) turns the forecast into a position by volatility targeting: it aims at a fixed yearly volatility over a rolling window, with a maximum position. It is required in every base config.

Example, run_102's base config: no regime rules, so every bar is "unknown" and that state holds the strategy. Two components: `trend_spread`, the spread between the 24-bar and 168-bar moving averages, weight 1.0, standardised over 500 bars; and `stretch_from_short_sma`, the distance of price from its 24-bar average, standardised then negated (a bet on reversal), weight 0.25. Sizing: volatility target 20% a year over 60 bars, at most 2 times equity.

**What it costs and how long it takes.**
No cost: a config is a small file (run_102's is 62 lines).
28 component classes (`strategy_components.py`, 1,713 lines); 18 transform ops (`registry.py`).

**What is switched off or not used here.**
- The block combiner (several proven pieces mixed by weight) exists for combination runs; no run_102 config uses it.
- Volatility targeting as a transform op is allowed only in a config without a sizing block.
- Several component classes are hedges or on/off filters that the graded rule refuses as forecast sources.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Example config | `runs/run_102/artifacts/candidate_strategy_config.json` | Detector (ungated), two components, sizing |
| Transform ops | `trading-bot/strategies/registry.py:312-351` | `TRANSFORM_OPS_REGISTRY`, 18 ops in three groups |
| Ordering rule | `trading-bot/strategies/registry.py:300-311` | History ops before scalar ops |
| Pipeline | `trading-bot/strategies/registry.py:354-376` | `apply_transform_pipeline` |
| Standardise | `trading-bot/strategies/registry.py:186-224`, `:469-476` | Past mean absolute value, target 10, cap 20 |
| Sizing block | `trading-bot/strategies/registry.py:85-135` | `SIZING_KINDS`, errors (`:94`), normalise (`:114`), realised vol (`:123`) |
| Components | `trading-bot/strategies/strategy_components.py` | 28 classes: regime measures, directional, hedges, feed-based |
| Design rules for authors | `strategy-research/docs/STRATEGY_DESIGN_GUIDE.md`, `docs/COMPONENT_CATALOG.md` | Stop 11 |

Remarks: send them as "stop 12a: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop 12. 
Aligned with my vision. Key asset of the workflow. 
However agree that i do not understand why we would persist any code that is now refused (eg on off)
I see "block combiner code" is mentioned. I thought it was not designed yet, hoping nothing has been created here as hardcoded / specific rule. First, we have not agreed on the design of combined block run (run combining several claim passed right). Second, such run should have a config based on claim associated block, but nothing should differenciate them in the backtest!

(Guide's note: sent as one remark for stop 12; recorded under both 12a and 12b.)

## Inspector notes

### (1) Design and mechanism

1. The config is a good unit of research: two engines, components by class path, transforms from one registry, one sizing block; run_102's base is 66 lines (`candidate_strategy_config.json`) and byte-equal to the 1b output (stop 10). The parts that matter to "without fooling ourselves" are built with a no-lookahead note that the code matches: `standardise` divides by the mean of past values only (`registry.py:186-189`, `:219`), `vol_target`/sizing read the last window+1 closes of the strategy's own buffer (`:46-49`, `:133-135`), `signed_power` reads the running value only (`:254-255`). Each op's param check is one function shared by the op and the validator (`:54-56`, `:193-195`, `:261-263`, `:94-97`), so the two cannot refuse different configs. This is well made.
2. `standardise` is scale-only and that fixes what "graded" means. Output = `10 x h[-1] / mean|past window|`, capped at 20 (`:222-224`, `:469-476`); no mean is subtracted. A component whose last 500 values share one sign and size (an EMA spread through a long trend) sits near +10 by construction, whatever the trend's strength; the guide's own worked case shows a constant becoming exactly +10 (`STRATEGY_DESIGN_GUIDE.md:428-429`). So "position size follows signal strength" (D-051) holds relative to the component's own last 500 values, not to the market: a forecast of 10 means "typical for this component lately", and a strategy's average absolute exposure is set by the standardise target, not by the idea. With run_102's weights the two legs are averaged over 1.25 (`strategy_engine.py:613`, `:623`), each ~10 in size, so the forecast is ~10 most bars and the sizing block then scales by `0.2 / realised vol` (`:83-84`). Stop 10 note 1.3 stands: every idea is tested as a near-constant-exposure, rank-rescaled signal; turnover is the sign flips.
3. The sizing block makes the forecast's size nearly irrelevant to exposure. `allocation = clip(forecast/10 x 0.2/realised, +-2)` (`:80-88`); on hourly BTC with realised annual vol well above 0.2, a forecast of 10 sizes to a fraction of equity, and the 0.2 no-trade band (stop 13) is reached by the signal path (`forecast/10` moving 0.2, i.e. 2 forecast points) long before the sized path. Hold for stop 13: whether the band fires on the signal change alone, which with a standardised forecast means on nearly every sign flip.
4. Unknown op params are silent. Every lambda in the registry reads `p.get(name, default)` (`:320`, `:324-326`, `:347`); only `standardise`, `vol_target` and `signed_power` refuse a bad params dict (`:216-218`, `:148-150`, `:284-286`), and none refuses an extra key. A `window` misspelt on `ema` runs span 10 with no error (stop 11 note 1.2). The registry has the checker pattern (`*_param_errors`); it is applied to three ops of eighteen.
5. The registry carries the campaign's rules in prose: the D-149 explanation at `:171-189`, the 2026-10-19 bounds ruling at `:242-252`, `BLOCK_STANDARDISATION_TARGET` and the operator decision of 2026-09-26 at `:447-466`. The engine is the right owner of the arithmetic; the decision history belongs in the decision log (the operator's stop 03 rule), and here it is also what `catalogue_section.py` parses from the guide, not from this file, so the two copies can drift (the test at stop 11 pins the guide to the registry's op set, not to its prose).

### (2) Legacy or simplifiable (leads)

1. `threshold_filter` and `volume_filter` (`:325`, `:345-349`): refused in `strategies` by D-051 (`forecast_rules.py:54`); allowed only in vetoes. `vol_adjusted` (`:334-339`): the op that caused run_061 (`forecast_size_probe.py:3-9`), refused with a sizing block (V19) and called "not a volatility scaler on its own" by the guide (`:302`). `vol_target` as an op (`:147-168`): allowed only without a sizing block, which every base config must have (D-181). Four of eighteen ops are refused or discouraged on the live path; the registry keeps them for old configs (`run_084`'s block, V19 comment). Not checked: whether any registered block (stop 22) uses them.
2. `TRANSFORM_MIN_PERIODS` comments (`:384`, "rank over <20 samples is too coarse" beside the value 50): stale text. `_ratio_to_mean`/`_safe_zscore` (`:26-33`): the pre-D-149 scale ops; live only in `history_transforms`-free legacy configs and as V15's refused "other history op".
3. `component_effective_lookback` (`:479-495`) and `transform_min_periods` (`:404-420`): two places compute what a component needs; `history_op_min_periods` (`:429-435`) a third. One function returning (deque size, first-forecast count, data bars) would replace them; the engine calls all three (`strategy_engine.py:309`, `:315`, `:339`).
4. `SubStrategyComponent` (the components' base in `strategy_base.py`) is the class stop 00's note says is dead in its `generate_forecast`/`standardize_forecast`/`store_raw_forecast` methods (CUL-281); the 28 classes inherit from it. Not re-checked here.
5. The 12a speech's "28 component classes ... 18 transform ops" figures are right; the root `CLAUDE.md` says the registry holds 15 and the itinerary says 17 (`00_itinerary.md`, stop 12 row). Two stale counts in the project's own orientation.

### (3) Disagreements between the speech and the element

1. Step 3 names fifteen ops by group (5 history, 6 scalar, 4 data-aware); the registry has 7, 6 and 5 (`:314-350`): `identity`, `negate_percentile` and `vol_adjusted` are left out of the sentence. The count "18" is right.
2. Step 4, "the current value divided by the average size of its own past values (the current one excluded), times 10, capped at +-20": `:219-224`, `:469-476`; correct. Not stated: it is scale-only, no centring (note 1.2).
3. Step 5, "aims at a fixed yearly volatility over a rolling window, with a maximum position. It is required in every base config": the formula `:83-84`, default cap 2 (`:90`); "required" is the skill's rule (D-181), not the engine's (`main_strategy.py:63-64`: absent block changes nothing). Fine.
4. Section 6, "Volatility targeting as a transform op is allowed only in a config without a sizing block": V19 (`validate_config.py:557-566`); correct.
5. Example: "two components ... weight 1.0 ... 0.25 ... standardised over 500 bars ... negated ... sizing 20% over 60 bars, at most 2": `candidate_strategy_config.json:12-64`; correct. The file is 66 lines (the speech says 62).
6. Reading-map ranges verified: `registry.py:312-351`, `:300-311`, `:354-376`, `:186-224`, `:469-476`, `:85-135` (`:94`, `:114`, `:123`); `strategy_components.py` 28 classes (26 `*Component` + `EMADiff` + `BuyAndHoldStrategy`, by grep); the file's line count (1,713) not verified.
