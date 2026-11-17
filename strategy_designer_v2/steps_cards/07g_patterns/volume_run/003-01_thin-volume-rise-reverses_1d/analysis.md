---
line: 7.g patterns
backtest: 003-01_thin-volume-rise-reverses_1d
idea tested: 003-01_thin-volume-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4856 USD
---
## Findings
- **F1:** Large one-day rises carry on rather than reverse: on the non-overlapping 5-day grid, days with a rise of 1–2 times the coin's 20-day daily volatility were followed by a 5-day excess return of +1.46% (t=2.38, n=307), and rises above 2 times by +3.88% (t=2.80, n=107), against −0.27% (t=−0.64, n=614) for rises of 0.3–1 times.
- **F2:** The continuation after large rises is stable and graded: it holds in both halves of the windows (w1–12 +1.80%, t=2.48, n=197; w13–24 +2.29%, t=2.58, n=217) and in all six coins (from +0.85% in XMR to +5.22% in XRP); across all up days the scaled rise ranks the 5-day excess return with Spearman rho=0.084 (p=0.0013, n=1490).
- **F3:** Volume decides how much a large rise carries on, in the opposite way to the tested idea: large rises on above-average volume (ratio >1) were followed by +2.49% (t=3.42, n=293), those at or below average by +1.02% (t=1.13, n=121); even thin-volume large rises were followed by gains rather than givebacks (ratio ≤0.5: +2.81%, n=20; 0.5–0.75: +1.04%, n=54).
- **F4:** On up days, the rise times the volume ratio ranks the following 5 days: its top quintile was followed by +1.50% (t=2.10, n=285) and its fourth by +1.24% (t=1.79, n=284), against −0.37% to +0.05% for the bottom three quintiles.
- **F5:** The day's volume ratio ranks the next 5 days on all days, whatever the direction of the move: Spearman rho=0.064 (p=0.0005), about the same in each half (w1–12 rho=0.061, p=0.019; w13–24 rho=0.064, p=0.014); days at half the 30-day average volume or less were followed by −0.93% (t=−2.05, n=598).
- **F6:** The book's result comes from its tails rather than a steady edge: its best 1% of days summed to +4.69 and its worst 1% to −5.42, against a total of −1.54, while it held a position on only 18–26% of bars per coin (Sharpe −0.58).

## Ideas
- `003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on` (from F1, F2): When a coin rises over one day by more than its usual daily move (its 20-day volatility), it keeps rising over the next 5 days. The larger the rise in units of that volatility, the larger the further rise.
- `003-01_thin-volume-rise-reverses.g2_heavy-volume-rises-extend-further` (from F3, F4, F2): When a coin rises over one day on volume above its own 30-day average daily volume, it keeps rising over the next 5 days. The larger the rise times the day's volume against that average, the larger the further rise.
- `003-01_thin-volume-rise-reverses.g3_thin-volume-precedes-underperformance` (from F5): The thinner a coin's volume over one day against its own 30-day average daily volume, the more the coin underperforms its usual return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
