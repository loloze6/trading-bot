---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4345 USD
---
## Findings
- **F1:** On the non-overlapping 24-hour grid (about 15,800 cases), the coin's 24-hour fall, scaled by its usual 24-hour move, predicts the next 24 hours better than the tested 2-hour fall: the lowest quintile of the scaled 24-hour return gives a strength of +0.102 (t 5.04), against +0.075 (t 3.97) for the lowest quintile of the scaled 2-hour return.
- **F2:** The 24-hour reversal is concentrated in volatile markets. In the top tercile of 30-day volatility, the slope of strength on the scaled 24-hour return is −0.114 (t −9.03, n 5,271), against +0.004 (t 0.70) in the bottom tercile. In that volatile tercile, the deepest-fall quintile returns a total +1.48 % (excess +1.34 %, strength 0.27, t 5.38, n 981) over the next 24 hours, which is 7.8 times the 0.19 % cost of a trade.
- **F3:** The reversal also grows with the coin's last-24-hour volatility against its 30-day volatility. In the top tercile of that ratio the slope is −0.051 (t −7.05, n 5,175), against +0.006 (t 0.36) in the bottom tercile. The deepest-fall quintile gives a strength of 0.178 (t 5.85, total +1.04 %) in the top tercile, against 0.021 (t 0.33) in the bottom tercile.
- **F4:** The 24-hour reversal holds across coins and years. The slope is negative in all 6 coins (t from −2.35 for LTC to −4.69 for XMR), in 7 of 8 years (2024 is +0.008, t 0.66), and in 71 % of the 24 windows.
- **F5:** Rises reverse as well, and the effect is stronger when volatility is high. The top quintile of the scaled 24-hour return is followed by an excess of −0.29 % (t −3.18) over all cases. In the high-volatility tercile it is −0.69 % excess and −0.54 % total (strength −0.135, t −3.09, n 972).
- **F6:** The tested idea's size is tiny because its forecast is positive on roughly half of all bars. Its 17,241 cases average an unusual move of +0.01 % (strength 0.001), and the book is close to holding the coin. It is in a position on 100 % of days, and its daily-return deciles track the coin's same-day return: −6.9 % against −7.7 % in the worst decile, +7.5 % against +8.3 % in the best.
- **F7:** The next-hour return after the 20:00 and 21:00 UTC bars is positive, at +0.055 % (t 6.75) and +0.044 % (t 5.66). This holds in all 6 coins (t 2.98 to 4.44) and in 7 of 8 years (2022: −0.022 %, t −1.44). Neither hour is a funding settlement time, and each hourly move is well under one trade's cost.
- **F8:** The 24-hour excess return from Friday grid bars is +0.52 % (t 5.41, n 2,478). It fades over time: +1.2 % to +1.3 % in 2018 and 2019, and −0.26 % and −0.07 % in 2022 and 2025.

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound.g1_volatile-day-fall-rebound` (from F1, F2, F4): In a coin whose 30-day hourly volatility is high, the return over the next 24 hours after a fall over its last 24 hours runs upward, and the larger that fall against the coin's usual 24-hour move, the larger the rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound.g2_volatility-burst-fall-rebound` (from F1, F3, F4): The return over the next 24 hours after a fall over a coin's last 24 hours runs upward. The rise is larger the larger that fall is against the coin's usual 24-hour move, and the higher the coin's volatility over its last 24 hours is against its volatility over its last 30 days.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound.g3_volatile-day-rise-giveback` (from F2, F5, F4): In a coin whose 30-day hourly volatility is high, the return over the next 24 hours after a rise over its last 24 hours runs downward, and the larger that rise against the coin's usual 24-hour move, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
