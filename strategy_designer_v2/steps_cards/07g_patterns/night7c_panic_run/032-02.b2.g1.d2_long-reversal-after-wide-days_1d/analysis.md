---
line: 7.g patterns
backtest: 032-02.b2.g1.d2_long-reversal-after-wide-days_1d
idea tested: 032-02.b2.g1.d2_long-reversal-after-wide-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3824 USD
---
## Findings
- **F1:** Over the next 3 days, the coin's unusual move rises steadily with its past 5-day return. By quintile of the 5-day return the means run −1.35 %, −0.68 %, −0.04 %, +0.39 %, +0.80 % (non-overlapping 3-day cases, 168 to 260 days per quintile). Top minus bottom is +2.14 %, Welch t 2.06.
- **F2:** The past 20-day return gives the same rising pattern over the next 3 days. Its quintiles run −1.07 %, −0.45 %, −0.22 %, +0.86 %, +0.79 %, top minus bottom +1.86 % with t 1.91. Over the next 1 day the 20-day return spread is +0.72 % with t 1.86, so continuation, not reversal, is what longer past moves show.
- **F3:** The tested forecast reverses after its first day. Over 1 day its top quintile minus bottom is +0.58 % (t 1.80). Over 3 days it is −1.06 % (t −1.34), and the close-location part alone goes from +0.69 % (t 2.29) at 1 day to −0.71 % (t −0.93) at 3 days. The 1-day bounce after a low close on a wide day looks given back inside the larger multi-day trend.
- **F4:** The tested forecast's 1-day link is small but points the same way everywhere. Its Spearman correlation with the next day's unusual return is positive on all 6 coins (0.064 to 0.125) and in all 4 years (0.057 to 0.137). Its size per case is only +0.09 % (t 0.81), against a trade cost of 0.19 %, so its 1-day move cannot pay for a trade.
- **F5:** Several angles show nothing beyond chance.

## Ideas
- `032-02.b2.g1.d2.g1_five-day-momentum-continues-briefly` (from F1, F2, F3): The higher a coin's 5-day return, the more the coin rises over the next 3 days, and the lower it is, the more the coin falls, in steady steps across the whole range of past returns.
- `032-02.b2.g1.d2.g2_monthly-trend-carries-over-days` (from F2, F3): The further a coin's 20-day return sits above its usual range, the more the coin rises over the next 3 days, and the further below, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
