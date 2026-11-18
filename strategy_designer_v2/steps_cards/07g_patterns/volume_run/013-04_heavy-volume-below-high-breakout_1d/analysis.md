---
line: 7.g patterns
backtest: 013-04_heavy-volume-below-high-breakout_1d
idea tested: 013-04_heavy-volume-below-high-breakout
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3579 USD
---
## Findings
- **F1:** Across all bars, a heavier 10-day volume relative to its own 30-day mean is followed by a higher 5-day excess return: the pooled slope on the per-coin percentile rank is 0.0262, t = 3.62 on 2503 non-overlapping cases. The top two quintiles average +1.01% (t 2.39) and +0.90%, against -0.78% for the bottom quintile. Controlling for the 20-day return and the 20-day volatility leaves it at 0.0246 (t 3.36).
- **F2:** The volume effect in F1 is not stable over time or across coins. In windows w13–w24 its slope is 0.0466 (t 4.11, n 1249); in w1–w12 it is only 0.0053 (t 0.60, n 1254). By coin it is strongest in XRP (t 3.12) and ZEC (t 2.34), and slightly negative in BTC (t -0.33).
- **F3:** The effect of F1 fades at longer horizons. The same 10-to-30-day volume slope falls to t 1.00 over 10 days and t 0.85 over 20 days. Measured against a 90-day mean instead, it is t 1.14 over 5 days and t 0.21 over 10 days.
- **F4:** The 20-day return predicts the next 10-day excess return. The top quintile averages +2.13% and the bottom -0.58% (slope t 2.21, n 1375). This also appears only in w13–w24 (t 2.65; w1–w12 t -0.15), and it drops to t 1.49 once the volume ratio is included.
- **F5:** Wednesday's next-day excess return is negative and Friday's is positive.
- **F6:** The 52-week-high breaks often reverse at once.
- **F7:** The 30-bar excess return after being in the 52-week-high regime is +7.70% across 30 cases, against -0.14% otherwise. It is a large but thin sample with a high spread (std 0.289).

## Ideas
- `013-04_heavy-volume-below-high-breakout.g1_rising-volume-short-continuation` (from F1, F2, F3): The heavier a coin's average volume over the last 10 days relative to its own 30-day average, the larger its return over the next 5 days.
- `013-04_heavy-volume-below-high-breakout.g2_one-month-momentum-continuation` (from F4): The larger a coin's 20-day return, the larger its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
