---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, the closer its close is to its highest close of the past 20 days, the larger its rise over the next 10 days.
Consequence: A rising coin closing at its recent high is a reason to be long for the next ten days rather than to fade the breakout.
Why:
- F4: In the rising regime, closeness of the close to its 20-day high predicts the next 10 days. The slope of the 10-day unusual move on the distance from the 20-day high is 0.214 with t 3.44 over 808 cases, against -0.030 with t -0.63 outside the regime. Over all regimes, closes at their 20-day high are followed by +4.52 % unusual over 10 days (t 2.88, n 194), against -0.55 % (t -1.39, n 1,353) elsewhere.
- F5: F4 is not stable across years: its slope over all regimes has t 3.35 in 2019 and 4.38 in 2020, but t -3.08 in 2022 and -1.87 in 2023, and it is significant in no single coin (t 0.07 to 1.87).
