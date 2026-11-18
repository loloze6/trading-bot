---
brief: 013_anchoring-to-recent-high
source-idea: 013-04_heavy-volume-below-high-breakout
line: 7.g patterns
backtest: 013-04_heavy-volume-below-high-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's average volume over the last 10 days relative to its own 30-day average, the larger its return over the next 5 days.
Consequence: A trader would lean long a coin whose recent volume is rising against its monthly norm and refuse long trades when recent volume has dried up, over a one-week holding.
Why:
- F1: Across all bars, a heavier 10-day volume relative to its own 30-day mean is followed by a higher 5-day excess return: the pooled slope on the per-coin percentile rank is 0.0262, t = 3.62 on 2503 non-overlapping cases. The top two quintiles average +1.01% (t 2.39) and +0.90%, against -0.78% for the bottom quintile. Controlling for the 20-day return and the 20-day volatility leaves it at 0.0246 (t 3.36).
- F2: The volume effect in F1 is not stable over time or across coins. In windows w13–w24 its slope is 0.0466 (t 4.11, n 1249); in w1–w12 it is only 0.0053 (t 0.60, n 1254). By coin it is strongest in XRP (t 3.12) and ZEC (t 2.34), and slightly negative in BTC (t -0.33).
- F3: The effect of F1 fades at longer horizons. The same 10-to-30-day volume slope falls to t 1.00 over 10 days and t 0.85 over 20 days. Measured against a 90-day mean instead, it is t 1.14 over 5 days and t 0.21 over 10 days.
