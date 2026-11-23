---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day hourly volatility is high, the return over the next 24 hours after a fall over its last 24 hours runs upward, and the larger that fall against the coin's usual 24-hour move, the larger the rise.
Consequence: A trader buys deep one-day falls in volatile markets and holds for a day, because there the rebound is several times a trade's cost, while in calm markets the trader refuses the trade.
Why:
- F1: On the non-overlapping 24-hour grid (about 15,800 cases), the coin's 24-hour fall, scaled by its usual 24-hour move, predicts the next 24 hours better than the tested 2-hour fall: the lowest quintile of the scaled 24-hour return gives a strength of +0.102 (t 5.04), against +0.075 (t 3.97) for the lowest quintile of the scaled 2-hour return.
- F2: The 24-hour reversal is concentrated in volatile markets. In the top tercile of 30-day volatility, the slope of strength on the scaled 24-hour return is −0.114 (t −9.03, n 5,271), against +0.004 (t 0.70) in the bottom tercile. In that volatile tercile, the deepest-fall quintile returns a total +1.48 % (excess +1.34 %, strength 0.27, t 5.38, n 981) over the next 24 hours, which is 7.8 times the 0.19 % cost of a trade.
- F4: The 24-hour reversal holds across coins and years. The slope is negative in all 6 coins (t from −2.35 for LTC to −4.69 for XMR), in 7 of 8 years (2024 is +0.008, t 0.66), and in 71 % of the 24 windows.
