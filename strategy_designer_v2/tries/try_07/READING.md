# Try 07: the engine's backtest at the end of the loop (2026-11-05)

**What was built.** One component in the engine, `trading-bot/strategies/claim_event.py`: it runs a validated claim's own few lines of pandas on the history window at every bar and holds the claim's direction for its horizon, one position at a time, future shifts refused. One step in v2, `steps/engine/backtest.py`: it writes the claim's strategy config, runs the bot's backtester on every window of the fold (warmup prefetch, Kraken 5 bps per leg, the engine's slippage, bar-level equity), reads the engine's own metrics and applies the profit bar. The runner now sends a passing book there. The lite profit check stays as a quick tool and is no longer in the loop.

**Result on the BTC candidate, fold A, through the engine.**

| | Net return | Median window Sharpe | Worst window drawdown | Trades | Windows positive | Verdict |
|---|---|---|---|---|---|---|
| engine | +55.6% | 1.03 | 15.4% | 193 | 6 of 6 | pass |
| lite (try 06) | +55.5% | 1.04 | 15.4% | 191 | 6 of 6 | pass |

The two agree to the decimal. That is the check that the claim code, the component and the backtester mean the same thing by "enter at the event bar's close, hold twelve bars, pay the cost". About 32 seconds per window, three minutes per fold.

**What it means.** The spine now ends in the engine, as the design says. Brief, claims, verdicts, the engine's backtest of the validated book, observations, next claim, record. The runner resumed the finished BTC run, made no new model call, and ran the engine for the one passing book.

**What to hold against the candidate is unchanged.** One fold; twenty-one looks on its brief; Sharpe over the bar by a hair. The engine run adds nothing to that and takes nothing away. The holdout stays the operator's.

**Housekeeping.** Each engine window leaves about 1.5 MB of bar-level files; they are git-ignored, the engine rewrites them from the tracked config. The verdict file keeps the per-window numbers and the result folder names.
