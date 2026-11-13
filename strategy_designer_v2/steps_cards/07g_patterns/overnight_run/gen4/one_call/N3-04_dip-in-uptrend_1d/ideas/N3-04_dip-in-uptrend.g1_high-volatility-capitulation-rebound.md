---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.g patterns
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Outside a 20- and 60-day uptrend, when a coin closes a down day larger than its typical daily move while its 20-day volatility is high for that coin, the following one to three days rise more than the coin's average.
Consequence: A trader could take high-volatility capitulation drops long even when the coin is not in an uptrend, and refuse the same drop when volatility is low.
Why:
- F1: Outside the uptrend regime, a down day larger than the coin's mean absolute daily move (z < -1) in the coin's top third of 20-day volatility was followed by a next-day excess return of +1.40% (t 5.27, n 650, hit 62.6%), and by +2.31% over three days on non-overlapping samples (t 2.94, n 180); the same drop in the lowest volatility third was followed by -1.03% over three days (t -2.26, n 210).
- F2: The F1 rebound is positive on every coin, from +1.19% (LTC) to +1.94% (ZEC) next day, with t between 1.50 and 2.92 and n between 93 and 134 per coin; by year it is positive from 2018 to 2024 (2018: +1.35%, t 3.41, n 248) but is -0.28% in 2025 (t -0.48, n 51).
- F6: Large drops on volume 1.5 to 2.5 times the 20-day mean were followed by +0.85% next day outside the uptrend (t 3.26, n 410) and +1.20% inside it (t 2.78, n 173); drops on below-average volume gave +0.30% (t 1.68, n 737) and +0.45% (t 1.58, n 273).
