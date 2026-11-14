---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is far below its 200-day average during high volatility, and that close is also its lowest close of the last 10 days after a falling 5-day return, the coin's price rises over the next 10 days by more than its normal drift.
Consequence: A trader would buy a deep capitulation only on a bar that closes at a fresh 10-day low after a falling week, and would pass on deep bars that have already bounced.
Why:
- F4: The effect sits on bars whose close is still falling: forecast >= 10 cases with a negative 5-bar return average +3.6% (t 1.26, n 50, hit 52%), against -1.9% (n 19, hit 37%) after a positive 5-bar return; at forecast >= 5 the same split gives +2.9% (t 1.36, n 74) against -1.5% (n 38).
- F5: The rebound is strongest when the close is at its 10-bar low: such top cases average +6.9% (median +3.2%, hit 58%, n 19), against +0.3% (median -2.4%) for the 45 cases that are not at the low.
- F1: The 69 non-overlapping cases with forecast >= 10 have a mean 10-bar excess return of +2.06% (t 0.90) but a median of -1.60% and a hit rate of 48%; their spread (std 0.19) is larger than that of all bars (0.16), so a few large rebounds (XRP mean +11.9% on 11 cases, median -1.9%) carry a mean that most cases do not share.
