---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 7-day volatility rises above its 30-day volatility after its 30-day return was positive, the coin rises over the next three days, and more so the higher that volatility ratio.
Consequence: In a coin that rose over the past month, treat a fresh rise in volatility as a reason to be long for a few days.
Why:
- F2: A rise of the coin's recent volatility grades the rebound as strongly as width does. Cases where the 7-day volatility is highest against the 30-day volatility (ratio 1.21 to 1.91) end at +2.73 % against the drift (t 3.02, 124 cases); the four lower fifths end between -0.50 % and +0.17 %. At bar level, the position earns 0.067 % per held bar in that top fifth and about 0.000 % in the two lowest fifths, where the book still holds 17 to 26 % allocation.
- F3: Width and the volatility rise together carry the effect. Wide stretches with a high volatility ratio end at +2.91 % (t 3.26, 130 cases). Wide stretches with a low volatility ratio end at -3.07 % (t -2.45, 20 cases), and every narrow-stretch cell is negative (-0.60 % to -0.77 %). Across cases, the Spearman correlation with the excess return is 0.143 for raw width and 0.134 for the volatility ratio, against 0.078 for the book's forecast, which re-standardises width against its own past 180 values.
