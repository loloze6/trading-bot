---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3745 USD
---
## Findings
- **F1:** Over the next 7 days a coin keeps its 14-day move: the slope of excess 7-day return on the standardised 14-day return has t = +4.02 (n = 1723 non-overlapping points), and per-coin quintiles rise steadily from −1.49% (t −2.37) in the lowest to +1.96% (t +2.34) in the highest; all six coins have a positive slope (t from +0.29 to +3.52).
- **F2:** The deepest 14-day falls do not rebound, against the tested idea: the lowest octile of the 14-day return over its own volatility has excess 7-day return −0.19% (t −0.26, n 270), not above the moderate-fall octiles at −2.58% (t −3.21) and −1.53% (t −2.25).
- **F3:** The continuation is strongest on the upside: the slope among 14-day rises has t +2.85 (n 834) against t +1.30 (n 889) among falls, and the top octile earns +2.75% excess over 7 days (t +2.48).
- **F4:** Momentum holds at 3 and 7 days and over several lookbacks: the 14-day return has t +2.99 at 3 days and +4.17 at 7 days but only +0.99 at 14 days, while the 7-day return predicts 14 days (t +3.42) and the 28-day return predicts 3, 7 and 14 days (t +2.41, +2.80, +2.27).
- **F5:** Daily moves partly reverse the next day: the slope of next-day excess return on today's return over its 20-day volatility has t −5.00 (n 15940); after a −1 to −2 sigma day the next day averages +0.59% (t +4.44), and after a 0 to +1 sigma day it averages −0.22% (t −3.70).
- **F6:** This reversal is negative in all six coins (t from −0.44 to −5.45) and stronger when the 14-day trend is down (t −5.92, n 7736) than when it is up (t −2.77, n 7627), but it faded in 2024 and 2025 (t +0.32, +0.89).
- **F7:** The book's small gain came from its rare longs: 1124 long bars averaged +0.092% a day, while 9695 short bars, the moderate-fall shorts, averaged +0.004%; the book's mean daily return was 0.0042% against about 0.1% a day for holding the coins.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling.g1_two-week-momentum-carries-a-week` (from F1, F2, F3, F4, F7): The higher a coin's 14-day return relative to its own recent volatility, the higher its return over the next 7 days, with the strongest continuation after the largest rises and no rebound after the deepest falls.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling.g2_one-day-overreaction-reversal` (from F5, F6): The larger a coin's one-day move relative to its 20-day volatility, the more its next day moves the other way, most of all when its 14-day return is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
