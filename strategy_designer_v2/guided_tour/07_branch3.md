# Stop 07 of 10: Branch 3: is the book profitable?

## Speech (verbatim)

Stop 07 of 10: Branch 3, "is the book profitable?". Open on the side: `strategy_designer_v2/steps/engine/backtest.py` (`SHARPE_MIN, DD_MAX, AGREE`, `_run_size`, `backtest_claim`); `runs/real_01_daily_breadth_fold_a/003/engine_r0_short_horizon_reversal_3d_BTCUSD/engine_verdict.yaml`; `trading-bot/performance/bar_equity.py` (docstring, `max_drawdown_pct`, `sharpe_ratio_daily`); `trading-bot/strategies/registry.py` (the D-176 sizing block, `normalise_sizing_block`).

### 1. In one sentence
Branch 3 is a profit bar: three numbers the book must reach in the backtester's own results, at one of its two sizes, for the claim to count as profitable.

### 2. Why it exists
A claim can be right (branch 1) and still lose money once traded with costs. Branch 3 asks the second question from the same engine run, with the bar written in the code before any result.

### 3. What comes in, what goes out
In: the backtester's metrics for each of the six windows, at each size (stop 05). Out: inside `engine_verdict.yaml`, per size, the three checks, a verdict (pass, fail, refused) and the fold totals; for the claim and coin, one verdict and, on a pass, which size passed (`passed_as`).

### 4. What happens here, step by step
1. For each window the step takes from the backtester's metrics: net return and number of trades (the "core" block), Sharpe and worst drawdown (the "bar equity" block: computed from the book's value at every bar, Sharpe on daily values, yearly scale).
2. Three checks, per size:
   - net return above zero in at least 5 of the 6 windows;
   - the middle (median) of the six window Sharpes at least 1.0;
   - the worst window's drawdown at most 20%.
3. A size passes if all three hold. A size with no trade at all is "refused".
4. The claim and coin pass if either size passes. The fold total reported is the size that passed, or full size otherwise; fold net return is the six window returns compounded.

The two sizes: full size, where forecast 10 means 100% of capital; and the volatility target, where the position is the forecast divided by 10, times 20% divided by the coin's recent yearly volatility (last 30 bars), kept between −100% and +100% (`registry.py`, D-176 block). Both settings are constants in `backtest.py`, marked "fixed before any result".

Your brief speaks of a cap on "the whole-test maximum drawdown at 20%"; the code checks the worst single window, and names its source as its own constants, not v1's profitability-bars file.

Run 003, the 3-day reversal on BTC: full size, 2 of 6 windows positive, window Sharpes from −3.6 to +0.49, worst drawdown 61%; volatility target, 0 of 6 positive, worst drawdown 30%. Fail, fail. Across run 003's 40 books (20 pairs, two sizes): none passed all three; 2 passed the 5-of-6 check, 2 the Sharpe check, 4 the drawdown check. The highest median Sharpe, 1.57, was the skewness claim on ADA at full size, net +245% over the fold, with 4 of 6 windows positive and a worst window drawdown of 49%: fail.

Live: inside every engine run.

### 5. What it costs
Inside the engine time of stop 05: 868 seconds for run 003.

### 6. How it stands against the two rules
It reads no bars: only the backtester's metrics files. Pass or fail is a verdict on the book, not a forecast; nothing here switches a position.

### Reading map
| Part | File and section | One line |
|---|---|---|
| The bar | `steps/engine/backtest.py`, `SHARPE_MIN, DD_MAX, AGREE` | Sharpe 1.0, drawdown 20%, 5 of 6 windows |
| The checks | `backtest.py`, `_run_size`, `checks` and `verdict` | Three checks per size; refused at zero trades |
| Either size | `backtest.py`, `backtest_claim`, `verdicts`, `best`, `passed_as` | Pass if one size passes |
| The numbers it reads | `trading-bot/performance/bar_equity.py`, docstring, `max_drawdown_pct`, `sharpe_ratio_daily` | Per-bar equity; daily Sharpe, √365 |
| The second size | `trading-bot/strategies/registry.py`, D-176 block, `normalise_sizing_block` | forecast/10 × target vol / realised vol, capped |
| Run 003 example | `runs/.../003/engine_r0_short_horizon_reversal_3d_BTCUSD/engine_verdict.yaml` | Fail at both sizes |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Next

## Inspector notes

1. The two rules (`V2/steps/engine/backtest.py` `_run_size` lines 61 to 80, `backtest_claim` lines 100 to 105): clean. It reads `metrics.json` of the engine's run and nothing else; the verdict is on the book. The volatility target (`registry.py` D-176: allocation = forecast / 10 × target / realised, clipped) scales and never switches; the full-size book is forecast / 10, so a capped forecast of 20 is a 200% position, which is why the full-size drawdowns (61%) run about twice the vol-target's (30%) on the same signal.
2. The bar against the brief (`backtest.py` line 15 `DD_MAX` on the worst window; the operator's brief body: "branch 3 caps the whole-test maximum drawdown at 20%"): each window is an independent run from fresh capital, so the whole-test curve's drawdown is at least the worst window's. The code's check is the looser of the two, not a restatement. The speech names the difference; the direction (looser) should be on the page, and the bar's three constants have no page at all: they are code comments, where v1 had `profitability_bars.yaml` signed by the operator. Fixed before any result, yes; fixed by whom and against which brief, unwritten (stop 05, note 5 on the 20% target).
3. Two accounting bases in one bar (`backtest.py` lines 62 to 65; `trading-bot/performance/bar_equity.py` docstring): the 5-of-6 check uses `core.net_return_pct` (the tracker's per-trade accounting), the Sharpe and drawdown checks use the bar-equity series; the docstring says the core basis understates risk. The run 003 book summary shows the two Sharpes differing (−0.69 core, −0.49 bar). One basis for all three checks, the bar-equity one, removes a question the post-tour review already raised about v1 (theme 7, "two Sharpes").
4. What the second size buys (`backtest.py` lines 92 to 93, 100 to 102; STEPBACK "~00:45" and "01:28"): Sharpe is nearly scale-free and the 5-of-6 sign check nearly so, both books sit at 97 to 99% exposure, so the sizes differ materially only on the drawdown check (and on cost share). "Pass if either passes" is therefore mostly a second drawdown look at 20% vol, the n04 case. That is a reasonable rule and a cheaper one would be a single vol-target book with full size reported as information; the two-size run doubles the engine time (868 s for run 003) for one check. A ruling, not a defect.
5. Numbers that read larger than they are (`backtest.py` line 70 `fold_totals.net_return`; `sharpe_ratio_daily` √365 on 120-day windows): the fold return compounds six restarts from fresh capital, a return no book earned in sequence (the skew claim's "+245%" on ADA is six independent four-month runs chained); and an annualised Sharpe from 120 daily returns has a standard error near 1.7, so a median of six such numbers against a bar of 1.0 is a coarse instrument. Both are fine as a bar; as headlines in the record and the morning file they need their unit said.
6. Small code points: line 65 `abs(float(be.get("max_drawdown_pct") or 0.0))` turns a missing drawdown into 0.0, which passes the drawdown check; today the missing Sharpe on the same path fails the book, so the hole is covered by accident. Line 77 refuses only when the sum of trades over all windows is 0, so a book with one trade in six windows is a scored fail; the judge's 30-event floor has no twin here (a minimum trade count, or a minimum exposure, would be the analogue).
7. The finding the bar makes and nothing acts on (`engine_verdict.yaml` rows: `exposure_pct` 97 to 99 on every window; `cost_drag_pct` 4 to 134): under the dense-strength rule every book is always in a position and rebalanced every bar, so branch 3 is in practice testing "does a daily-rebalanced tilt beat 10 bps plus slippage", and fees ate 32% to 134% of gross in the calm windows. The engine has a rebalance band (`trading-bot/core/trading_bot.py`, the `min_allocation_change` band of the RiskManager around line 532) that the v2 config leaves at its default, and a smoothing op (stop 04, note 4). The operator's working rule asks "what one change would a practitioner make to this book": from these rows, trade less. The knob is in the engine, unset by v2, and no page lists it as a lever.
8. Speech against element: the three checks, "either size", the fold total of the passing or full size, √365, the D-176 formula, 2 of 6 and 0 of 6 windows, 61% and 30%, and the 40-book tally (2, 2, 4, none) and the skew claim's 1.57 / +245% / 4 of 6 / 49% all match (recomputed across the 20 `engine_verdict.yaml` files). The speech says the brief's "whole-test" drawdown differs from the code's "worst window"; it does not say which is stricter (note 2).

Running view after stop 07: branch 3 is three honest constants on the engine's own numbers, with two accounting bases, a looser drawdown than the brief, a second size that is mostly a second drawdown look, and headlines (fold return, annualised Sharpe) whose units are not on the page. Its rows already say what a practitioner would change; nothing in the loop reads them for that.
