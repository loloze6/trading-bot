---
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
idea tested: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4009 USD
---
## Findings
- **F1:** The check fails on Calmar (0.62 against 0.75) because of shared, deep falls. The book's deepest fall is 57 % over 80 days, from w16 to w17, while the coins' daily returns summed to −41 %. Five more falls run from 34 % to 54 % (w12–w14 −54 %, w6–w10 −42 %, w1–w3 −40 %). Every window's own deepest fall is 14 % to 51 %.
- **F2:** The falls come from the book being long on many coins while they fall together. On days with all 6 coins long (1430 days) the book's daily standard deviation is 3.7 % and its worst day is −18 %; with 5 coins long the worst day is −22 %; with 1 to 3 coins long the worst day is −2.6 % to −5.2 %. Inside falls deeper than 20 % the coins averaged −0.20 % a day and the book −0.12 % a day, with 4.0 coins long on average.
- **F3:** A stop would not help. The first 48 hours of a trade say nothing about the rest of its 10 days: the Spearman correlation of the 48-hour return with the following 8 days is 0.03 (p 0.25, 1474 trades). So the losses are not a fall that keeps going.
- **F4:** Surges that come with a short-term volatility burst continue; quiet ones do not. Ranked by 24-hour volatility over 30-day volatility at entry, the 10-day return after a trade rises steadily across the quintiles: −2.4 %, +1.5 %, +2.4 %, +3.1 %, +5.0 % (about 212 trades each; top minus bottom ≈ 7.4 %, t ≈ 4 approx.).
- **F5:** Surges that repair a falling week continue most. Trades entered with a negative 7-day return (−20 % to −0.65 %) returned +6.4 % over 10 days (215 trades). The other four 7-day-return quintiles returned −0.7 % to +3.1 %.
- **F6:** An overextended month carries little of the move. By the 30-day return in units of 30-day volatility, the 10-day return falls from +5.9 % in quintile 2 through +3.4 % and +1.1 % to +0.3 % in the top quintile (about 147 trades each). The weakest-month quintile also shows only +0.3 %.
- **F7:** Surge size is not graded. The largest 24-hour rises (top quintile, above 5.75 %) returned only +0.85 % over 10 days, with the deepest average adverse move (−11.3 %). The 4.0–5.75 % quintile returned +3.8 %. By surge size in usual daily moves, the ret240 quintiles are 0.9 %, 0.2 %, 5.0 %, 0.5 % and 3.7 %.
- **F8:** The idea is big enough to pay its costs, so the fault is in the falls, not the cost. The total move per case is 1.94 %, 10.1 times the 0.19 % round trip, and the unusual move is 3.0 times it; the book's Sharpe of 0.82 beats holding by 0.27.

## Ideas
- `018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month.d1_surge-with-volatility-burst` (from F4, F1, F2, F7): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive and its volatility over the last 24 hours is above its 30-day volatility: the larger that ratio, the larger the rise.
- `018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month.d2_surge-recovering-weekly-fall` (from F5, F1, F3): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the more the coin fell over the preceding 7 days, the larger the rise.
- `018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month.d3_surge-early-in-rise` (from F6, F1, F2): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the smaller that 30-day return is in units of the coin's 30-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
