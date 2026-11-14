# Stop 04 of 10: A claim as code in the engine: the component and the grading

## Speech (verbatim)

Stop 04 of 10: A claim as code in the engine: the component and the grading. Open on the side: `trading-bot/strategies/claim_linear.py` (whole, 66 lines); `trading-bot/strategies/registry.py` (the `standardise` block, `standardise_block_forecast`, `TRANSFORM_OPS_REGISTRY`); `trading-bot/strategies/strategy_engine.py` (`forecast`); `trading-bot/tools/validate_config.py` (V15); `strategy_designer_v2/tries/try_09/READING.md`; from run 003, `engine_r0_short_horizon_reversal_3d_BTCUSD/strategy_config_full_size.json` and `book_summary.yaml`.

### 1. In one sentence
The component is the piece of the bot's engine that runs a claim's code on each bar and hands the engine one number, the strength, which the engine grades into a forecast between −20 and +20 that the book trades.

### 2. Why it exists
The engine is the only reader of bars, so the claim runs inside it. Forecasts are linear, so the claim hands over a continuous number and the engine's grading step, standardise, sizes it. Built after the clean-up (try 09).

### 3. What comes in, what goes out
In: the claim's code, a minimum number of bars (200 or more, set at stop 05), and a `horizon` it stores and does not use; on each bar, the bars the engine hands it, up to that bar's close. Out, per bar: the strength and two debug fields, `event` and `strength`, which the engine copies into its per-bar output for branch 1.

### 4. What happens here, step by step
1. At set-up the component refuses code that is empty or contains a forbidden form: a backward shift with a minus sign (looking forward), a centred window, a reversed series, an import, opening a file, or running other code.
2. On each bar, once it has its minimum number of bars, it takes the open, high, low, close and volume columns it was given, defines the names the claim format promises and runs the claim's lines. A bar fed twice is skipped.
3. It keeps the last value of `event` (true or false) and of `strength`. A strength that is not a finite number becomes 0. The strength is its output; `event` goes only into the debug fields.
4. The engine keeps a history of these raw strengths. Standardise takes the current one, divides it by the average size of the previous 500 values (not counting the current one) and multiplies by 10; the result is cut at −20 and +20. Fewer than 100 previous values give 0; an average size near zero gives 0. There is no mean subtraction, so the sign and a zero survive. The leak note in `registry.py`: the average uses only values strictly before the current one.
5. With one component of weight 1, the forecast is that graded value, cut again at ±20. The component opts in (`report_debug`), so its `event` and `strength` join the engine's per-bar debug row.

In run 003's config: lookback 800 bars, standardise window 500, minimum 100, target 10, cap 20, the claim's code verbatim. The per-bar output is not in this checkout (raw engine results are git-ignored, `CHANGES.md`, try 07); its book summary is. For `short_horizon_reversal_3d` on BTC the forecast sat at the cap on 6% to 20% of bars depending on the window; across the 16 first-round claim-and-coin pairs of run 003, from 0% to 70%.

`validate_config.py` check V15 (standardise first, alone, valid settings) ran in try 09; neither the runner nor the engine step calls it. Of the registry's steps (threshold filter, sigmoid, clip and more) v2 uses only standardise.

Live: every engine run of v2.

### 5. What it costs
Engine time is at stop 05.

### 6. How it stands against the two rules
The component does read bars, as part of the engine: only the ones the engine hands it, up to the current close; it opens no file. On-off: the strength reaches the engine as a continuous number, and standardise grades it. Three places flatten it: the ±20 cap (beyond twice the recent average size, every value is the cap), the 0 before 100 past values, and the 0 for a non-finite strength. Nothing checks that a claim's strength is not itself a switch; the format forbids it in words only (stop 03). `event` is true-or-false and goes only to the debug fields.

### Reading map
| Part | File and section | One line |
|---|---|---|
| The component | `trading-bot/strategies/claim_linear.py`, docstring and `ClaimStrengthComponent` | Runs the claim's code; strength out on every bar |
| The refusals | `claim_linear.py`, `_FORBIDDEN` | Future shift, centred window, reversal, import, file, exec |
| The grade | `trading-bot/strategies/registry.py`, standardise block, `_standardise`, `standardise_block_forecast` | 10 × value / past average size, cut at ±20 |
| The steps on offer | `registry.py`, `TRANSFORM_OPS_REGISTRY` | v2 uses only standardise |
| Debug to bars | `trading-bot/strategies/strategy_engine.py`, `forecast`, the `report_debug` line | Event and strength reach the per-bar output |
| The config check | `trading-bot/tools/validate_config.py`, V15 | Used in try 09; not called by v2 |
| Saturation and churn | `strategy_designer_v2/tries/try_09/READING.md` | Sparse: 3 values; dense: 2544 values, constant trading |
| Run 003 example | `runs/.../003/engine_r0_short_horizon_reversal_3d_BTCUSD/strategy_config_full_size.json`, `book_summary.yaml` (`share_at_cap`) | The config as run; share of bars at the cap |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Direct: i do not get it. Your explanation is too complex to understand

**Guide's direct answer (2026-11-07)**

The same stop, in four plain steps, with run 003's claim `short_horizon_reversal_3d` on BTC.

1. **The claim computes one number each day.** Its few lines say: take the move of the last 3 days, divide it by the usual daily move of the last 60 days, flip the sign. A big drop gives a big positive number ("expect a bounce"); a big rise gives a big negative number. This number is the strength. (`trading-bot/strategies/claim_linear.py`, `update`: runs the claim's lines and keeps today's value.)
2. **The engine resizes that number.** It compares today's number with its usual size over the previous 500 days. A usual-size number becomes 10; twice the usual size or more becomes 20, the maximum; half the usual size becomes 5. The sign is kept. The result is the forecast, between −20 and +20, and it is what the book trades. (`trading-bot/strategies/registry.py`, `_standardise`.)
3. **Two safety rules.** Code that looks into the future is refused before it runs (`claim_linear.py`, `_FORBIDDEN`). Until the engine has 100 past numbers to compare with, the forecast is 0 (`_standardise`).
4. **Both numbers are written into the engine's daily log**, so that branch 1 can later check whether the number predicted the next 3 days (`trading-bot/strategies/strategy_engine.py`, `forecast`, the `report_debug` line).

In run 003, this claim's forecast was at the maximum (±20) on 6% to 20% of days, depending on the window (`book_summary.yaml`, `share_at_cap`). On those days a bigger number no longer changes the forecast.

> Direct
> [Request interrupted by user]
> Next

## Inspector notes

1. Rule 1 inside the engine (`trading-bot/strategies/claim_linear.py`, line 17 `_FORBIDDEN`, line 53 `exec`): the component runs the claim's code with `pd` and `np` in scope and only a regex between the code and the world. The regex stops `import `, `open(`, `exec(`, `eval(`; it does not stop `pd.read_csv(`, `pd.read_parquet(`, `pd.read_pickle(` or `__import__(` (no whitespace after `import`). A claim's code can therefore read the price cache, or any file, from inside the engine; the engine would still be "the only reader" in name only. The model is not an adversary, but the rule is written as a property of the system, and here it is a property of the model's manners. One line closes it: forbid `read_`, `__import__`, `getattr`, `globals`, or run the code with `pd` and `np` replaced by restricted namespaces.
2. The lookahead refusal is a sieve (`claim_linear.py` line 17; speech section 4 step 1 and direct answer step 3, "code that looks into the future is refused before it runs"): `shift(-` is caught, `shift(periods=-3)`, `diff(-3)`, `pct_change(-3)`, `bfill()`, `fillna(method="bfill")`, `interpolate()`, `np.roll(x, -1)`, `np.flip`, `sort_index(ascending=False)` are not; each looks forward. Scar 1 is enforced by the model's `why_no_lookahead` sentence, which nothing reads (stop 03). An honest model asked for an IC above its own floor and finding none is exactly the one that writes an innocent `bfill`. A real guard exists cheaply because the code runs per bar on a buffer that ends at the current close: run the claim's code on the buffer with the last bar removed and check that the earlier values do not change. That is the test the engine's own structure makes possible and no one runs.
3. Rule 2 in the mechanism (`trading-bot/strategies/registry.py` lines 172 to 232, `_standardise`, `standardise_block_forecast`; `V2/steps/engine/backtest.py` line 27 `STD`): scale-only, no mean subtraction, cap at twice the target. Anything beyond twice the recent mean size is the cap, so the share of on-off bars is set by the claim's distribution shape, not by the claim's words: a Gaussian strength sits at the cap on about one bar in nine; a fat-tailed one much more. Run 003 shows 6% to 20% for this claim (`book_summary.yaml` `share_at_cap`) and up to 70% across the round (speech). At 70% the book is mostly a switch, built by the engine's own grading, and nothing in branch 1 or branch 3 reads `share_at_cap`; only the analyst sees it. If rule 2 is to be a property of the system, a bound on `share_at_cap` (a refusal, or a wider cap-to-target ratio) belongs in code at stop 05 or 07.
4. The claim's horizon is dead in the engine (`claim_linear.py` line 35, `self.horizon` stored and never read; `backtest.py` `_config_of` passes it): the book rebalances on every bar whatever the horizon (W1 of this claim: 91 trades in 120 bars, turnover 72, fees 31.7 against gross −98, `cost_drag_pct` 32). The engine's registry already holds a smoothing step (`ema` in `TRANSFORM_OPS_REGISTRY`, `registry.py` line 312 onward) that could take its span from `horizon_bars`; V15 forbids a second history op in `transforms` but not a per-value step after standardise. Whether to smooth is the operator's ruling (try 09 said so); that the lever exists in the engine and the knob exists in the claim, unconnected, is a fact of the files.
5. Design, speed (`claim_linear.py` `update`, lines 44 to 53): on every bar the whole claim code is re-run over the whole buffer (`lookback` 800 rows for this claim), so a window costs bars × buffer; the engine's slowness, named under "not built" in the README, lives largely here. The per-bar re-run is also what makes the lookahead test of note 2 possible, so it should not go; but the buffer could be cut to `min_bars` for the component (the 500 + 100 standardise rows are the engine's history, not the claim's), which `component_effective_lookback` (`registry.py` line 480) already separates.
6. Small code points (`claim_linear.py`): line 55 `bool(ev.iloc[-1])` turns a NaN event into True (`bool(nan)` is True), so a claim whose `event` has a NaN on the last bar is measured there; line 59 `self.confidence = 1.0` is a base-class field nothing in v2 reads; a `strength` that is a DataFrame or scalar gives `nan` then 0 silently (line 56), not a refusal, so a claim that forgot to make a Series runs as an all-zero book and is scored. `min_bars_of` (`backtest.py` line 20) misses `rolling("30D")` string windows and `ewm(halflife=`; sum of windows plus 50 is a floor, which is the right side to err on.
7. Simplifiable or unused: `horizon` as a component parameter (note 4): either used or dropped from `claim_linear.py` and `_config_of`. `tools/validate_config.py` V15: no v2 caller (grep over `V2/*.py`, `V2/steps/`), and the config is built by fixed code, so one check at build time was enough; nothing to delete, nothing to add. Of the registry's ops v2 uses one, as the speech says; the dead regimes (`trending`, `mean_reversion`, `chop`: None) and the empty `regime_detector` in every config are v1 scaffolding the engine requires, not v2 knobs.
8. Speech against element: the grade (10 × value / past mean size over 500, 0 under 100, cut at ±20, cut again at ±20 in `forecast`), the lookback 800, the debug opt-in at `strategy_engine.py` lines 632 to 633, the share at cap 6% to 20%, and V15 unused all match the files. One overstatement, in section 4 step 1, section 6 and the direct answer step 3: "code that looks into the future is refused" describes six regex forms, not the property (note 2). The direct answer's four steps are right and plain.

Running view after stop 04: the component is small and the grade is honest; the two guards that make rule 1 and scar 1 properties of the system are a regex, and the on-off share is decided by the engine's cap, which nothing bounds. The horizon exists in the claim and the judge and nowhere in the book.
