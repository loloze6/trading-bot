---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is far below its 200-day average during high volatility, the coin's rise over the next 10 days is larger in a period whose deep-drawdown signals do not keep recurring on consecutive checks, that is when the coin was not already this deep below its average 10 days earlier.
Consequence: A trader would take the first deep-drawdown signal of an episode and refuse its repeats inside a long bear phase.
Why:
- F3: The cases are clustered in time, and one window weighs on the result: the 69 cases fall on only 46 distinct dates (date-clustered t 0.75), and w2 (2022) alone holds 28 cases averaging -1.4% (t -0.53); without w2 the 41 remaining cases average +4.4% (t 1.29, median +0.9%).
- F1: The 69 non-overlapping cases with forecast >= 10 have a mean 10-bar excess return of +2.06% (t 0.90) but a median of -1.60% and a hit rate of 48%; their spread (std 0.19) is larger than that of all bars (0.16), so a few large rebounds (XRP mean +11.9% on 11 cases, median -1.9%) carry a mean that most cases do not share.
