---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin falls over 24 hours, its return over the next 24 hours is positive, and the steeper the 24-hour fall, the larger that rebound.
Consequence: A trader can buy a coin after a sharp one-day fall for a one-day hold instead of shorting it, sizing up with the depth of the fall.
Why:
- F1: Coins bounce after their largest 24-hour falls. On a non-overlapping 24-bar grid, the bottom decile of past 24h return was followed by a mean 24h return of +1.07% (t 6.44, n 1723), against roughly -0.2% to +0.24% for the other deciles. Among all 24h falls, the forward 24h return falls with the past return: slope -0.223 per unit of past return, se 0.016, p<0.001, so the steeper the fall, the larger the rebound.
- F2: The rebound after the two lowest deciles of 24h return holds in every coin and every year. By coin it ran from +0.37% (BTC, t 2.05) to +0.79% (ZEC, t 2.63). By year it was positive in all of 2018 to 2025, from +0.22% (2022, t 0.88) to +0.95% (2021, t 3.05). Spearman rho between past and next 24h return is negative in all six coins, from -0.050 to -0.114, p ≤ 0.009.
- F6: The book, all short trades held about 238 minutes, lost money. Its mean daily return was -0.154% (t -15.4, n 17381), and its 46,029 trades averaged -0.295% before fees and -0.395% after. This happened despite the confirmed post-settlement edge and a tiny positive per-bar gross position gain of 0.0033% (t 2.43). The bounce after deep falls (F1) works directly against shorting falling coins.
