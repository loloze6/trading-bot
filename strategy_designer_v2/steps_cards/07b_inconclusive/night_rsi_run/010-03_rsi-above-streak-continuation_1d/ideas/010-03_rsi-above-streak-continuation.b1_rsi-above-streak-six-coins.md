---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation
line: 7.b inconclusive
backtest: 010-03_rsi-above-streak-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed above 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days.
Consequence: A long unbroken stretch of buyer control means order flow keeps persisting, so the up move continues.
Why:
- F1: The test's result points the way the idea predicts but falls short of the bar: the pooled 14-day slope t is 1.48 on 384 grid cases (199 with a forecast above 0); bars with a forecast above 0 average +0.0063 excess 14-day return against −0.0068 when flat, a gap whose Welch t is only 0.80.
- F2: Noise drowns the effect: the excess 14-day return's standard deviation is about 0.16 in every forecast bin, against a spread of about 0.05 between the bins' means (−0.024 to +0.027).
- F6: The test ran on only two coins, BTC and ETH, over 24 windows each; BNB was not run. The default data offers six coins (BTC, ETH, LTC, XMR, XRP, ZEC) over all four folds, so roughly three times the cases are available for a result that is on the predicted side but short of the bar.
