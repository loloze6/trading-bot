---
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation_1h
idea tested: 018-04_hourly-surge-multiday-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4449 USD
---
## Findings
- **F1:** The tested idea's own situation shows no continuation: across the 24-hour return measured in multiples of the coin's 30-day mean absolute daily return, the unusual 120-hour move is +0.25 % at 0.5 to 1 multiples (t 0.53, n 424), +0.41 % at 1 to 2 (t 0.66, n 403), +3.50 % at 2 to 3 (t 2.75, n 130) and −0.81 % at 3 or more (t −0.54, n 94); one cell out of ten reaches t > 2 and the grade does not rise steadily, so this is chance among many cells, in line with the verdict's −0.01 % per case.
- **F2:** After a large 24-hour fall the coin rebounds over the next day. At −3 multiples or worse, the unusual 24-hour move is +1.87 % (strength 0.38, t 4.56, n 371) and the 48-hour move is +2.43 % (t 3.84, n 180). The rebound is graded: on all bars with a negative multiple, the slope of strength on the multiple is −0.092 (t −8.1, n 8040), so the deeper the fall, the larger the rebound. The rebound is about 10 times the 0.19 % cost of a round trip.
- **F3:** The rebound after a large fall (−2 multiples or worse) is positive on all 6 coins: XRP +1.54 % (t 2.65), ZEC +1.39 % (t 2.22), XMR +1.15 % (t 2.08), ETH +0.81 %, BTC +0.51 %, LTC +0.21 % (n 163 to 179 each). It is concentrated in <date> (+1.72 %, t 4.85, n 502) against <date> (+0.17 %, t 0.72, n 525).
- **F4:** The higher a coin sits in its 30-day high-low range, the more it rises over the next 5 days. The slope of strength on range position is 0.189 (t 3.21, n 3106). The top two bands earn +1.00 % (range position 0.8 to 0.95, t 2.12, n 516) and +2.40 % (above 0.95, t 2.02, n 188), against −0.26 % to −0.82 % below 0.8. The top quintile of nearness to the 30-day high earns +1.55 % (t 3.00, n 624).
- **F5:** The near-high continuation is uneven. By coin, at the top of the range: XRP +5.79 % (t 2.51), ZEC +3.10 %, BTC +0.95 %, ETH +0.82 %, LTC −0.42 %, XMR −0.01 %. By period: <date> +2.32 % (t 3.01, n 330), <date> +0.55 % (t 0.97, n 374).
- **F6:** The book is essentially the coin held at a volatility-targeted size, not the idea's timing. It is in the market 94 % to 98 % of bars on every coin, and its gain from the market's rise is close to its total gain (BTC 13.5 of 13.0 bps a day, XMR 11.4 of 10.2). Trades at the lowest entry forecast earn the most, 9.39 % net (forecast 4.3, median 550 hours held), against 1.9 % to 5.6 % for higher forecasts.
- **F7:** Hour-of-day and weekday patterns are strong but too small to trade:

## Ideas
- `018-04_hourly-surge-multiday-continuation.g1_deep-daily-fall-rebounds` (from F2, F3): When a coin's 24-hour return, read at an hourly close, is a fall of several times its 30-day mean absolute daily return, the coin rises over the next 1 to 2 days by more than its usual 1-to-2-day return, and the deeper the fall in those multiples, the larger the rebound.
- `018-04_hourly-surge-multiday-continuation.g2_top-of-range-continues` (from F4, F5, F1): The higher a coin's last hourly close sits within its 30-day high-low range, the more the coin rises over the next 5 days compared with its usual 5-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
