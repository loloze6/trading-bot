---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin's daily bars, a close at its highest close of the prior 20 days, made while the close is below its close of 60 bars earlier, is followed by a rise over the next ten bars larger than the coin's average ten-bar rise.
Consequence: A trader would take 20-day breakouts that come out of a longer decline and refuse those that extend an already long rise.
Why:
- F5: The drift after a new 20-day closing high appears only when the coin's 60-bar return is negative. In that case the non-overlapping 10-bar excess return is +0.046 (87 events, t=3.32). When the 60-bar return is positive it is -0.0006 (198 events, t=-0.05).
- F4: Two of six coins lose. LTC's net log sum is -11.40 and XMR's is -12.64, against ETH +16.47 and XRP +12.00. Per coin, the non-overlapping 10-bar excess return after new 20-day highs has no t above 2 (XRP 1.90 on 38 events; BTC -0.77 on 51; XMR -0.33 on 52).
