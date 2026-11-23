---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day hourly volatility is high, the return over the next 24 hours after a rise over its last 24 hours runs downward, and the larger that rise against the coin's usual 24-hour move, the larger the fall.
Consequence: A trader shorts or steps out after large one-day rises in volatile markets, and refuses to chase them, because they give back more than a trade costs.
Why:
- F2: The 24-hour reversal is concentrated in volatile markets. In the top tercile of 30-day volatility, the slope of strength on the scaled 24-hour return is −0.114 (t −9.03, n 5,271), against +0.004 (t 0.70) in the bottom tercile. In that volatile tercile, the deepest-fall quintile returns a total +1.48 % (excess +1.34 %, strength 0.27, t 5.38, n 981) over the next 24 hours, which is 7.8 times the 0.19 % cost of a trade.
- F5: Rises reverse as well, and the effect is stronger when volatility is high. The top quintile of the scaled 24-hour return is followed by an excess of −0.29 % (t −3.18) over all cases. In the high-volatility tercile it is −0.69 % excess and −0.54 % total (strength −0.135, t −3.09, n 972).
- F4: The 24-hour reversal holds across coins and years. The slope is negative in all 6 coins (t from −2.35 for LTC to −4.69 for XMR), in 7 of 8 years (2024 is +0.008, t 0.66), and in 71 % of the 24 windows.
