# Stop 05 of 10: The engine step

## Speech (verbatim)

Stop 05 of 10: The engine step. Open on the side: `strategy_designer_v2/steps/engine/backtest.py` (whole, 122 lines); `trading-bot/core/launcher.py`, `run_backtest` (signature and docstring); from run 003, `engine_r0_short_horizon_reversal_3d_BTCUSD/` (`strategy_config_full_size.json`, `strategy_config_vol_target.json`, `engine_verdict.yaml`).

### 1. In one sentence
The engine step takes one claim and one coin, writes the strategy settings for it, has the bot's backtester trade it over each of the fold's six test windows twice (at two position sizes), and writes down what happened.

### 2. Why it exists
The engine is the only reader of bars: this step is where every claim meets the market, once, and every later answer (branches 1, 2, 3) is read from what it leaves behind.

### 3. What comes in, what goes out
In: the claims file, the claim's id, the fold (A), the bar size (1d), the coin. Out, in the claim-and-coin folder: two settings files, two trade logs, the backtester's own results per window (not in this checkout: git-ignored), `engine_verdict.yaml`, and one row in `records/trials.yaml`. It then calls branch 1 (stop 06).

### 4. What happens here, step by step
1. **How much history the claim needs.** It adds up every window length written in the claim's code, plus 50, with a floor of 200 bars. For the 3-day reversal (60 + 3 + 50) the floor applies: 200.
2. **The settings.** One component (stop 04), weight 1, standardise at window 500, minimum 100, target 10, cap 20; no market-state detector. The second settings file adds a volatility target: the position is sized so the book aims at 20% yearly volatility, measured over 30 bars, never more than 100% of capital. The first is "full size": forecast 10 means 100%. Both are marked "fixed before any result".
3. **The fold.** The six windows of fold A come from v1's fold tool, reused by hand. The start of the sealed holdout is read from the data policy and given to the backtester, which refuses a warm-up that would reach it; it is never printed.
4. **The runs.** For each window the backtester is called with: Kraken, 5 basis points (0.05%) commission per side, its own slippage, futures market type, history fetched before the window to warm up, a per-bar equity record. From each window's metrics it keeps net return, trades, Sharpe (return per unit of risk), worst drawdown (largest fall from a peak), exposure, cost drag, seconds.
5. **The profit bar** is applied to each size (stop 07). The claim passes if either size passes; the record says which.
6. **Refusals.** If no trade happens in any window, the verdict is "refused". If the backtester raises an error (for example, not enough history before the fold for the warm-up), the verdict is "refused", with any date in the message replaced by "<date>"; on this path no row is written to `trials.yaml`.
7. **Writes** `engine_verdict.yaml`, then calls branch 1 on the same folder, then appends the ledger row.

Run 003, the 3-day reversal on BTC: 559 trades at full size, net −86% over the fold, worst window drawdown 61%; at the volatility target, net −56%, drawdown 30%. Fail at both sizes. All 20 claim-and-coin pairs of run 003: fail, none refused.

Live: called by the runner for every claim and coin.

### 5. What it costs
Engine time, summed from the `seconds` of every window row of run 003's 20 `engine_verdict.yaml` files: 868 seconds (about 14 minutes) for 240 window runs; 36 to 60 seconds per claim and coin for both sizes.

### 6. How it stands against the two rules
This is the engine: the only step that reads bars, through the bot's backtester. Its verdict comes from the backtester's own metrics. Nothing in its settings is on-off: one continuous component, graded by standardise; the volatility target scales the position, it does not switch it.

### Reading map
| Part | File and section | One line |
|---|---|---|
| History needed | `steps/engine/backtest.py`, `min_bars_of` | Sum of the code's window lengths + 50, at least 200 |
| The two sizes | `backtest.py`, `SIZING`, `STD`, `config_of`, `_config_of` | Full size, and a 20% volatility target |
| One window run | `backtest.py`, `_run_size` | Kraken, 5 bps per side, warm-up, per-bar equity |
| Both sizes, verdict, refusals | `backtest.py`, `backtest_claim` | Pass if either size passes; refused on no trade or engine error |
| Branch 1 and the ledger | `backtest.py`, last lines of `backtest_claim` | Calls the judge; one row in `records/trials.yaml` |
| The backtester | `trading-bot/core/launcher.py`, `run_backtest` docstring | Warm-up before the window, holdout guard, commission override |
| Run 003 example | `runs/.../003/engine_r0_short_horizon_reversal_3d_BTCUSD/engine_verdict.yaml` | Fail at both sizes; 40 seconds |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Direct: the claim to backtesting strategy config is AI, correct ?

**Guide's direct answer (2026-11-07)**

No. Code writes the strategy config; no model is called for it.
- The AI writes only the claim: its plain words, its few lines of code, `horizon_bars`, `min_effect` (stop 03). It is told "Do not design the strategy config. One line in `how_it_trades` is enough" (`steps/ideas/PROMPT.md`, "Constraints").
- `steps/engine/backtest.py`, `config_of` and `_config_of`, build the config by filling a fixed template: the claim's `code` and `horizon_bars` go into the component's settings; the minimum history comes from `min_bars_of` (counted from the code); everything else is a constant of the file: standardise (`STD`: window 500, minimum 100, target 10, cap 20), the volatility target (`SIZING`: 20% a year, 30 bars, at most 100%), the commission (`FEE_PER_LEG`: 5 bps). The same template for every claim.
- The README says otherwise: "The path", step 3: "**Config** (AI, then code checks): one strategy config per claim." The code has no AI step and no config check here (`validate_config.py` is not called, stop 04).

> I realize in these stops that i am not clear on the idea to claim (idea + quantitative test) to backtest config, and then branch 1. I would need you to help me to see clearer in what i want to achieve... 
> Idea being explained before. Claim with an idea and a test allowing to verify the idea reality. In ly mind, i thought the strategy config would be created with the purpose to test this idea. And branch 1 to apply the claim test to backtest with config designed. Problem, i see now contradictory with a claim test that would be created to veirfy idea on results from a config not being written before. You see what i mean ?? Then wondering if the idea should only be tested on forecast, and a strategy being created with the purpose to have a forecast that would illustrate the strategy. Please think wisely and try to udnerstand what i mean. Also suggest if we are far from having a clear design on this.

> Next

## Inspector notes

1. The two rules (`V2/steps/engine/backtest.py`, whole): this is the engine's doorway and it is clean. The only market-data entry is `run_backtest` (line 57) with `warmup_prefetch=True` and `holdout_start` from the policy (line 90), never printed; dates in refusal messages are scrubbed (line 95). The verdict is computed from `metrics.json` of the engine's own run (lines 61 to 66). Nothing on-off in the config: one component, standardise, a volatility target that scales. The one place rule 1 can still be breached from inside this step is the claim's code the config carries (stop 04, note 1); this step does not check it either.
2. Scar 5 is not met here (`backtest.py` lines 94 to 99 and 110 to 113; `records/trials.yaml`): a refused engine run (no history, warm-up too long, a code error caught by `run.py`) writes `engine_verdict.yaml` and returns before the ledger line; the run touched the cache for the warm-up fetch and gets no row. Of the 731 ledger rows, the 60 live `engine` rows and 27 live `judge` rows carry `claim`, `symbol`, `fold`, `verdict` and no run or brief name (`try: engine`), while every pre-clean-up row carries its run name as `try`. The live ledger cannot be joined back to a run; the void one can. And one engine run writes two rows (engine, then judge), which is one experiment counted twice. The ledger write is read-modify-write (line 110 to 113; scar 4), two writers per claim (`judge.py` lines 61 to 64 and here), sequential today.
3. The exception filter (`backtest.py` line 94: `AssertionError, RuntimeError, ValueError`): a `NameError`, `KeyError`, `TypeError` or `ZeroDivisionError` from the claim's code at bar time escapes to `run.py`, which writes a refused marker with the raw message unscrubbed (`run.py` line 54, `str(exc)[:200]`): the date scrub of line 95 does not run on that path, so an engine message that carries a window date can reach a tracked file by the second door. STEPBACK "Wakeup 03:02" fixed exactly this once, on the first door.
4. The headline of a failing claim is always the full-size book (`backtest.py` line 102 `best`, line 105 `fold_totals`): when both sizes fail, `best` is `full`, so `engine_verdict.yaml`'s top `fold_totals` and therefore `run.py` `entry_of` and `claims_tried.yaml` carry the full-size numbers (−86% here) while the volatility-target book did −56%. The record and the morning file read the worse of two books for every fail. Since the pass rule is "either", the fail headline should be the better of the two, or both; the analyst already receives both (`run.py` `analyst_extra`).
5. Where the two sizes disagree with the brief (`backtest.py` `SIZING` 20% a year, `max_allocation` 1.0; the operator's brief body: a book "that targets about 40% a year volatility usually breaches 20% drawdown"): the operator's own number was 40%; v2 fixed 20% during the night (STEPBACK "~00:45", "tied to n04") and never asked. Fixed before any result is true; fixed from the brief is not. Not a defect; a choice made for the operator and written in code, not on a page.
6. Dead or stale in the element: the docstring's first line, "The engine's backtest of a validated claim" (line 1): since try 12 every claim is backtested, validated or not; `--windows N` (lines 3, 121) is a try-09 test knob no live caller uses; `horizon` is passed to the component and dead there (stop 04). `README.md` "The path" step 3 says "Config (AI, then code checks)": no AI, no check; the direct answer says so and the page should.
7. Cost and the one number (`backtest.py` line 14 `FEE_PER_LEG` = 5 bps per leg, Kraken perp taker, on `market_type="futures"` with `model_funding` left at its default False): consistent with the brief's "perp fees applied to spot prices" and with shorting (`short_net` appears in the book summary). The ideas prompt's 0.15% per round trip (stop 01, note 3) should be derived from this constant plus the engine's slippage table, not typed separately. `cost_drag_pct` of 61 to 134% in the calm windows (W3, W5, both sizes) says what the dense-strength rule costs: the book pays more in fees than it makes gross whenever the signal is flat. That is the practitioner's first finding of run 003 and it comes straight from this file's rows.
8. On the operator's remark (idea → claim → config → branch 1), from the files only. What v2 does: the config is one fixed template (`_config_of`) that trades the claim's strength; it is not designed to test the idea, and the AI does not write it (the direct answer is right). Branch 1 (`judge.py`) measures the IC of the engine's graded forecast, not of the raw strength, so the idea's test depends on an engine constant (the 500-bar standardise window); the raw `strength` column is in the same `bars.csv` and could be judged too, which would give the operator the clean split they describe: the idea judged on its own number, the book judged on the engine's. Branch 3 judges the fixed book. So the contradiction the operator sees is real only in the pages: the README says a config is designed per claim (step 3) and nothing in code does; what exists is "one claim, one strength, one template, two questions of one run". That is a clear design and a simple one; it is just not written anywhere as one sentence, and the horizon, `how_it_trades` and `compared_to` are the three fields that pretend to a design that is not there (stop 03). Not far; a page, not a build.
9. Speech against element: the 122 lines, min bars, the two sizes, the fold tool, the holdout guard, 5 bps per side, the refusals and their missing ledger row, 559 trades, −86%, 61%, −56%, 30%, 868 seconds all match the files. One gap: the speech says "the record says which" size passed, true for a pass; for a fail the record says the full-size numbers only (note 4).

Running view after stop 05: the engine step is the soundest file in v2 and keeps rule 1. Its ledger rows cannot be traced to a run, refusals get none, the fail headline is the worse book, and the 20% target was chosen in the night for a brief that said 40%. The design the operator is looking for exists in code and on no page.
