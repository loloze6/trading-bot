# Stop 12b: The strategy config, part b: the two engines, readiness, the validator

## Speech (verbatim)

**Stop 12 of 29, part b: the two engines, readiness and the validator.** Open on the side: `trading-bot/strategies/main_strategy.py`, `regime_engine.py`, `strategy_engine.py`, `strategy_base.py`, `trading-bot/tools/validate_config.py`.

**In one sentence.**
Each bar, the strategy object adds the new bar to its memory, lets the regime engine label the market state, lets the strategy engine combine that state's components into one forecast, and stays silent (forecast 0) until it has seen enough bars.

**Why it exists.**
The config (a recipe file, stop 12a) is only words. Something must run it the same way in every backtest and in live trading.
It must also refuse a broken recipe before trading, and never trade on half-filled indicators: a forecast built on too few bars is noise that looks like a signal.

**What comes in, what goes out.**
- In: the strategy config; one new price bar at a time.
- Out: the forecast (between -20 and +20), the regime label, and a debug record per component (its last raw value, its value after transforms, its weight, its share of the forecast).
- Next: the per-bar trading cycle turns the forecast into a position (stop 13); the debug record is saved per bar and is what the claim test and the analyst read later.

**What happens here, step by step.**
1. At the start, the strategy reads the config and runs the validator. Any violation stops the backtest before it begins.
2. It computes how many bars it needs before its first forecast: the longest warm-up among all components and transforms, at least 24, and at least the sizing window plus one.
3. On each new bar it adds the bar to a rolling memory, then updates the regime engine, then the strategy engine. A component error is counted and sampled, not hidden.
4. The **regime engine** first checks vetoes (forced states), then labels the bar by its mode: first matching rule, a score, or a product of scores; with no rules, the default state.
5. The **strategy engine** updates every component of every state each bar, and adds a value to a component's history once it is ready.
6. Readiness has three gates: enough bars in memory, the regime engine ready, and every component of this bar's state with enough history.
7. The forecast: for this bar's state, each component's history goes through its transforms, the results are averaged by weight, and the sum is clipped to ±20. A state with nothing assigned gives 0.
8. Not ready, or an error while forecasting: the strategy returns forecast 0 with the label "not ready" or "error".

The validator checks 19 kinds of rule (V1 to V19), among them: both top parts present; every id used is declared; every transform op exists and has a warm-up; history ops before the others; state names valid; the default state is not a real trading state; weights positive; every class path loads; standardise first and well-formed; volatility target and sizing not applied twice. The graded and standardised design rules of decision D-149 are checked by a separate research tool (`tools/forecast_rules.py`, stop 10), not by this validator.

**What it costs and how long it takes.**
No AI call. Per bar: one pass over the components.

**What is switched off or not used here.**
- The rolling memory's timestamp regrid exists in the strategy's constructor but no research call site passes its two arguments (the constructor's own note says so).
- The block combiner's code path is used only by combination runs.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Strategy object | `trading-bot/strategies/main_strategy.py:15-218` | `AdvancedStrategy` |
| Construction | `main_strategy.py:18-122` | Load config, validate (`:41-46`), sizing block, the two engines |
| Bars needed | `main_strategy.py:69-80` | Max of engines' needs, 24, sizing window + 1 |
| Reset | `main_strategy.py:124-134` | Clears memory and histories (gap rule, stop 13) |
| Readiness | `main_strategy.py:145-162` | Three gates |
| Feeds needed | `main_strategy.py:165-176` | Merged across both engines |
| Update | `main_strategy.py:178-199` | Memory, regime engine, strategy engine; error counting |
| Forecast | `main_strategy.py:201-217` | Regime, forecast, debug record |
| Signal wrapper | `trading-bot/strategies/strategy_base.py:371-406` | Not ready / error → forecast 0 |
| Regime engine | `trading-bot/strategies/regime_engine.py:19-241` | `classify` (`:116-143`): vetoes, rules, score, score product |
| Strategy engine | `trading-bot/strategies/strategy_engine.py:268-631` | `update` (`:413-427`), readiness (`:558`), required periods (`:571`), `forecast` (`:602-631`, clip `:631`) |
| Block combiner | `strategy_engine.py:82-266`, `:430-545` | Combination runs only |
| Validator | `trading-bot/tools/validate_config.py:62-614` | V1-V19; 37 violation messages |

Remarks: send them as "stop 12b: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop 12. 
Aligned with my vision. Key asset of the workflow. 
However agree that i do not understand why we would persist any code that is now refused (eg on off)
I see "block combiner code" is mentioned. I thought it was not designed yet, hoping nothing has been created here as hardcoded / specific rule. First, we have not agreed on the design of combined block run (run combining several claim passed right). Second, such run should have a config based on claim associated block, but nothing should differenciate them in the backtest!

(Guide's note: sent as one remark for stop 12; recorded under both 12a and 12b.)

## Inspector notes

### (1) Design and mechanism

1. The warm-up is about twice what the design documents tell the author, and the backtester knows it. `required_bars` for run_102 is 288 (`strategy_engine.get_required_periods :571-578`: 168 + 121 - 1; `main_strategy.py:70-80`), and `set_warmup(288)` (`:89`, `strategy_engine.py:396-405`) makes `is_ready` demand 288 history values per component (`:566-569`), but a component's history starts only when the component is ready (`:420-425`): `trend_spread` at bar 168. So the first forecast comes at bar 168 + 288 - 1 = 455, not 288. The guide's own measurements confirm the rule (RSI(14) "from bar 29" = 15 + 15 - 1, SMA(100) "from bar 201" = 101 + 101 - 1, `STRATEGY_DESIGN_GUIDE.md:254-255`), the size probe warms up "2 x required_bars" (`forecast_size_probe.py:72`), and `launcher.run_backtest` prefetches 2 x required_bars before every window for exactly this reason (`launcher.py:644-663`), so a backtest window loses nothing. What is wrong is the author-facing text: the 1b skill says "a 250-bar component is ready after 310 bars" (`strategy-config-authoring/SKILL.md:208-209`; by this rule 250 + 370 - 1 = 619), and the guide's step 6 wording ("`min(required_bars, S)` values") is right only for a reader who knows the count starts at the component's readiness. The live path has no prefetch at all: `launcher.py:372-373` is a commented "TODO: load historical warmup data before going live", so a live bot on run_102's config would trade nothing for ~455 hourly bars (about 19 days). For the goal "a strategy the operator can trade", that is the gap between the backtest and the bot.
2. Readiness collapses to one shared count per engine (`trading_bot.py:133-138` says so): `is_ready` is `len(h) >= max(_warmup, need)` for every component of the regime (`:566-569`), not a per-indicator validity. A regime with no components is "ready" (`:560-561`); the `forecast()` guard uses the smaller `_need` (`:620`). Correct and conservative; the cost is note 1.1.
3. Errors are fail-open in two layers with different visibility. `update()` catches any component exception, counts and samples it (`main_strategy.py:189-199`), and the conformance check reads those counts (stop 05b, `component_execution_error` pauses the route). `generate_forecast()` errors are caught one layer up (`strategy_base.py:398-406`): forecast 0, regime `ERROR`, and NOT counted in `component_error_count`. A component whose `transforms` key is missing raises `KeyError` at `strategy_engine.py:622` on every bar, which lands in the second layer: a zero-trade run with no error count and no pause; the guide says so (`:242`, "the validator does not check that the key exists") and the validator leaves it (V1-V19 check ops inside a list, not the list's presence). One validator line closes it.
4. The regime engine is small and honest: vetoes first in every mode (`regime_engine.py:124-133`), rules compare raw latest values with five ops and an unknown op is `False` (`:162-170`), `classify()` memoized per bar because of its side effects (`main_strategy.py:136-143`). The guide's "limits stated plainly" (`:215-220`) match the code (`:139-140`: any unknown mode runs `_classify_score`). With the live configs ungated (run_102, rules `[]`), none of this runs; the regime engine's `is_ready` is `all([])` = True (`:98-100`).
5. The validator is the right kind of gate (shape, ids, op existence, ordering, names, dead configs, placement of the three strict ops, sized-twice) and its checks reuse the engine's own functions (`validate_config.py:353-356`, `:366`, `:394`, `:436`, `:558`), so it refuses exactly what the engine refuses. What it does not check is what the guide warns about: unknown keys, misspelt params, a missing `transforms` list, a `params` value of the wrong type for the eighteen-minus-three ops (stop 11 note 1.2, 12a note 1.4). V12 imports the class and stops (`:304-338`). The one engine property it enforces that the engine would not (V17, detector transforms ignored) is the right call.
6. `strategies.warmup` is accepted and ignored (`main_strategy.py:89`, guide `:96`); `aux_feeds` is ignored by the engine and read by the tools (guide `:88`); `min_allocation_change` per strategy overrides the risk band (`:56`). Three config keys with three different owners; documented, and a source of the "silently ignored" class.

### (2) Legacy or simplifiable (leads)

1. `candle_interval_seconds`/`ignore_max_bars` on `AdvancedStrategy.__init__` (`:18-30`, `:91-95`): the CUL-273 regrid, "NOT YET wired through core/launcher.py" by its own docstring; no research call site passes them (speech section 6). Either wire or drop.
2. `strategy_engine.py`'s own `_warmup` default (`:355-366`, `min(config.warmup, min_buf)`) survives only for standalone/test construction; `set_warmup` overrides it on every live path. The comment block explaining the drift (`:355-364`) and `trading_bot.py:133-138` repeat the same story.
3. `launcher.py:644-663` (the `warmup_prefetch` docstring) reasons from the pre-CUL-273 `_warmup = min(config_warmup, min_buf)`; with `set_warmup(required_bars)` the bound `required_bars + _warmup - 2 < 2 x required_bars` still holds (equality minus 2), but the explanation is stale.
4. The `score`/`score_product` modes (`regime_engine.py:180-225`), `vetoes` (`:124-133`), `consecutive_bars`, `min_score`/`min_margin`: unreached by every ungated live config; whether any registered block (stop 22) or tested run since D-162 used a gated detector was not checked.
5. The block combiner (`strategy_engine.py:82-266`, `:430-545`, V13, the `blocks` branches of V14-V18): composition runs only, with one active block in the registry (stop 03a note 2.9); a third of the strategy engine serves a path that has not run.
6. `MainStrategy.generate_signals`'s commented `strategies_readiness_state` (`strategy_base.py:383`) and the "Might be redundant" note (`:374`): the readiness check there is the live one (`:375`); the comment is wrong the other way.

### (3) Disagreements between the speech and the element

1. Step 2, "the longest warm-up among all components and transforms, at least 24, and at least the sizing window plus one": the strategy engine's figure is component periods + history-op minimum - 1 (`:575-577`) plus the `vol_target` data bars (`:578`); "longest warm-up among all components and transforms" reads as a max of two, not a sum. And the first forecast comes ~`required_bars` bars after that (note 1.1), which neither the speech nor the guide says in those words.
2. Step 3, "A component error is counted and sampled, not hidden": true of `update()` (`:189-199`); an error in `forecast()` is caught at `strategy_base.py:398-406` and not counted (note 1.3). Half.
3. Step 5, "adds a value to a component's history once it is ready": correct (`:420-425`); the `history_transforms` are applied to a one-element series there (`:424`), which is why V15 refuses `standardise` in that list.
4. Step 6, 7, 8: correct against `:145-162`, `:602-631`, `strategy_base.py:371-406`.
5. "The validator checks 19 kinds of rule ... 37 violation messages": 37 `VIOLATION V` strings (grep count); correct. "weights positive": V8 is "numeric, and the regime's total above 0" (`:271-290`); a negative weight is allowed (guide `:239`). Wording.
6. Section 6, "no research call site passes its two arguments": consistent with the constructor's note (`:24-29`); not re-verified against `launcher.py`'s call sites.
7. Reading-map ranges verified: `main_strategy.py:15-218` (file ends `:218`), `:18-122`, `:41-46`, `:69-80`, `:124-134`, `:145-162`, `:165-176`, `:178-199`, `:201-217`; `strategy_base.py:371-406`; `regime_engine.py:19-241` (file `:242`), `:116-143`; `strategy_engine.py:268-631`, `:413-427`, `:558`, `:571`, `:602-631`, `:631`; `validate_config.py:62-614` (`validate` ends `:574`, the file `:615`).
