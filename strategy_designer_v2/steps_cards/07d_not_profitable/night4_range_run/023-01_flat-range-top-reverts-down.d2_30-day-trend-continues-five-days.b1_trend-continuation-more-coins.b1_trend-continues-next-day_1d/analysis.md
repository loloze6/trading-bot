---
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4286 USD
---
## Findings
- **F1:** The short side is what keeps the book from paying. On 7,684 active short bars the mean move in the position's direction is −0.080 %, against +0.368 % on 7,918 long bars. Rebuilt with the shorts set flat, the book (an approximation: allocation × next-day return, minus 0.11 % per unit of turnover) clears both failed measures: mean daily return 0.000617 against 0.000488 for all bars, Calmar 1.25 against 0.49, Sharpe 1.02 against 0.60, deepest fall −17.8 % against −29.2 %. The shorts alone have a mean of −0.000082, a Sharpe of −0.15 and a deepest fall of −50.1 %.
- **F2:** Short losses come from falling coins whose volatility is high. Shorts in the top quartile of 30-day daily volatility move −0.517 % per day in their direction (t −3.12, n 1,452). Shorts in the three lower quartiles move between +0.09 % and +0.14 % (t about 0.9 each).
- **F3:** The same reversal grows with volatility against the coin's own recent level, measured as 30-day volatility over its 60-day median. In falling coins the next-day move in the short's direction falls steadily across the quartiles: +0.329 % (t 2.70, n 1,363), −0.070 %, −0.003 %, then −0.773 % in the top quartile (t −3.38, n 718).
- **F4:** Rising coins keep rising at every volatility level, and most strongly when volatility is high against its own past. Longs in the top relative-volatility quartile move +0.724 % (t 4.06, n 1,659), and longs in the top absolute-volatility quartile move +0.507 % (t 2.80).
- **F5:** The book's worst periods are years with a large short share. In 2018 longs were 17 % of active bars and the move in the position's direction was −0.155 %. In 2025 longs were 37 % and the move was −0.005 %. In 2020 longs were 75 % and the move was +0.307 %.
- **F6:** Costs are not the main problem.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.d1_uptrend-continues-next-day` (from F1, F4, F5): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next day, only while that 30-day return is a rise.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.d2_volatile-downtrends-rebound-next-day` (from F2, F3, F4): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next day, except after a 30-day fall, where the higher its 30-day volatility against its own last 60 days, the more the coin rises over the next day.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.d3_volatile-selloff-next-day-rebound` (from F2, F3): In a coin whose 30-day net move has been a large fall relative to its 30-day high-low range, the higher its 30-day daily volatility against its own median of the last 60 days, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
