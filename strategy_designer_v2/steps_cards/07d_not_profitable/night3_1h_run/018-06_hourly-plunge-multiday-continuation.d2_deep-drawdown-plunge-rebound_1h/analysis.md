---
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4583 USD
---
## Findings
- **F1:** The book loses by holding too long, not on its entries: its 4274 trades last 197 hours on average against a 72-hour horizon, and those of 24 to 168 hours earn +1.3 % to +6.1 % net each, while the 912 trades of 168 to 336 hours lose -4.2 % and the 639 trades longer than 336 hours lose -10.8 % (all trades: -0.26 % net on average).
- **F2:** The rebound comes early and fades. Over all 2199 cases, the unusual move is +0.22 % at 6 hours (t 3.2) and +0.33 % at 24 hours (t 2.6), only +0.04 % at 72 hours (t 0.19), and -0.80 % at 168 hours (t -2.5, 2126 cases).
- **F3:** The idea holds only for real plunges, which few cases are. Cases whose 24-hour drop is 2 or more usual daily moves show a 72-hour unusual move of +1.6 % (t 2.5, 181 cases, 3 or more moves) and +1.8 % (t 2.5, 203 cases, 2 to 3 moves), a strength of about 0.19, about 9 times the 0.19 % cost. The 955 cases with a drop under 1 usual move lose -0.62 % (t -2.1) and make up 44 % of the bets.
- **F4:** The rebound grows with the coin's recent hourly volatility against its past 30 days. In the top quartile of the 7-day/30-day volatility ratio, cases rebound +1.33 % over 72 hours (t 3.0, 510 cases); in the bottom quartile they fall -0.76 % (t -1.9). Strong drops (2 or more usual moves) with above-median volatility rebound +2.25 % (t 3.7, 268 cases, strength 0.24), and strong drops with low volatility only +0.52 % (t 0.65, 116 cases).
- **F5:** The book's falls come while the coin keeps sliding. On days when the coins' 30-day return is in its lowest fifth (-13.5 % or worse), the book holds a mean allocation of 0.54 and loses -0.37 % a day. In every other fifth it holds 0.10 to 0.34 and earns +0.10 % to +0.19 % a day, and its deepest fall is 62 %.
- **F6:** Depth below the 30-day high grades the rebound only at its extreme. Cases more than 50 % below the high rebound +2.6 % over 72 hours (t 2.0, 92 cases), while cases 20 % to 50 % below are near zero (-0.26 % to +0.28 %, 1846 cases).
- **F7:** The gain is spread unevenly over time: the 72-hour unusual move per window ranges from -2.1 % (w2, t -2.5) and -2.0 % (w7, t -3.6) to +5.4 % (w11, t 4.7), and the book's daily mean beats holding in only 11 of 24 windows.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound.d1_deep-plunge-in-turbulence` (from F3, F4, F1): While a coin stands far below its 30-day high, the larger its 24-hour drop in multiples of its 30-day average absolute daily return, the larger its rise over the next 3 days, only while its hourly volatility over the past 7 days is high against its past 30 days; the higher that ratio, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound.d2_one-day-plunge-rebound` (from F2, F1, F3): While a coin stands far below its 30-day high, the larger its 24-hour drop in multiples of its 30-day average absolute daily return, the larger its rise over the next 1 day, and that rise is largest within the first day.
- `018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound.d3_deep-slide-keeps-falling` (from F5, F2, F1): While a coin stands far below its 30-day high, the larger its fall over the past 30 days, the larger its further fall over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
