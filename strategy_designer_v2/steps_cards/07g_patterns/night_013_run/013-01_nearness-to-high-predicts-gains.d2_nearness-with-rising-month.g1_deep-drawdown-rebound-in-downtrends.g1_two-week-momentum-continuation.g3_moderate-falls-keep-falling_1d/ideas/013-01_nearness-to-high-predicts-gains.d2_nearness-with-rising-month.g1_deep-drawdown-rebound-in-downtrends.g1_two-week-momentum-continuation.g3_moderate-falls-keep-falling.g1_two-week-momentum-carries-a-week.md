---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day return relative to its own recent volatility, the higher its return over the next 7 days, with the strongest continuation after the largest rises and no rebound after the deepest falls.
Consequence: A trader would lean long in proportion to a coin's strong two-week rise and would not buy deep two-week falls as rebounds.
Why:
- F1: Over the next 7 days a coin keeps its 14-day move: the slope of excess 7-day return on the standardised 14-day return has t = +4.02 (n = 1723 non-overlapping points), and per-coin quintiles rise steadily from −1.49% (t −2.37) in the lowest to +1.96% (t +2.34) in the highest; all six coins have a positive slope (t from +0.29 to +3.52).
- F2: The deepest 14-day falls do not rebound, against the tested idea: the lowest octile of the 14-day return over its own volatility has excess 7-day return −0.19% (t −0.26, n 270), not above the moderate-fall octiles at −2.58% (t −3.21) and −1.53% (t −2.25).
- F3: The continuation is strongest on the upside: the slope among 14-day rises has t +2.85 (n 834) against t +1.30 (n 889) among falls, and the top octile earns +2.75% excess over 7 days (t +2.48).
- F4: Momentum holds at 3 and 7 days and over several lookbacks: the 14-day return has t +2.99 at 3 days and +4.17 at 7 days but only +0.99 at 14 days, while the 7-day return predicts 14 days (t +3.42) and the 28-day return predicts 3, 7 and 14 days (t +2.41, +2.80, +2.27).
- F7: The book's small gain came from its rare longs: 1124 long bars averaged +0.092% a day, while 9695 short bars, the moderate-fall shorts, averaged +0.004%; the book's mean daily return was 0.0042% against about 0.1% a day for holding the coins.
