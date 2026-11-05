# Try 04: branch 3, the profit answer, on the one validated claim (2026-11-05)

**What ran.** `steps/profit/profit.py`, code only: trade the claim's own signal on its bars (enter at the event bar's close, hold 12 bars, one position at a time), pay 0.15% per round trip, fold A, BTC hourly. The bar was written before the result: net positive in 5 of 6 windows, Sharpe at least 1.0, drawdown no worse than 20%.

**Result: fail.**

| Fold A | Net return | Sharpe | Max drawdown | Time in market | Trades | Windows positive |
|---|---|---|---|---|---|---|
| heavy volume spike continues | +11.3% | 0.37 | -19.7% | 12.7% | 185 | 3 of 6 |

The belief is right (the claim passed) and the book is not worth trading: one good window carries the fold, three lose. That is the correct answer of branch 3, and it is why branch 1 and branch 3 are separate questions.

**The spine, closed once.** Brief, many claims, one verdict per claim, profit answer on the validated one. Four files of code, about 400 lines in all, one model prompt. Every step leaves a file a person can read and a row in the trial ledger.

**The engine's first ask.** No engine component expresses an event rule ("a big bar on big volume, follow it for 12 bars"); the catalogue says so itself for its breakout components. So the backtest ran in the claim's own terms, not in the engine. The engine run is needed when sizing, regimes or combinations matter. The ask, recorded here as v2's first: one event component in `trading-bot/`, about forty lines on the pattern of the existing components. Not built in this try.

**Proposed try 05: branch 2 and the next idea.** Give an AI the record of this run (the claims, the verdicts, the profit answer, the per-window numbers) and ask the two questions: what did we see, and what one claim should run next. Then run that claim through the judge. That closes the loop: run, record, next idea, run.
