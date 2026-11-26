---
line: 7.d confirmed, not profitable
backtest: 035-01_wide-low-close-rebounds_1d
idea tested: 035-01_wide-low-close-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3992 USD
---
## Findings
- **F1:** The recorded book is long almost all the time, so its falls are the coin's falls: it holds a position on 97.6 % of coin-bars (mean allocation 0.37), its daily returns correlate 0.82 with holding the coins (beta 0.35), and its deepest fall, −36.9 % in w14, came while holding fell −81 %. The reason is the standardise transform: a usual day already reads about +10 (median post-pipeline value 6.9), which puts the book long.
- **F2:** Only the wide, low-closing days carry the effect. In the per-coin top fifth of the raw product, the next-day excess return is +0.69 % (t 4.75, n 1740; mean range multiple 1.76, close-from-high 0.74). The second fifth adds +0.16 % (t 1.21). The lower three fifths lose −0.26 %, −0.25 % and −0.35 % (t −2.0 to −2.6, about 5,200 cases), yet the book still holds 0.07 to 0.30 of value on those bars.
- **F3:** The move on the signal days covers the cost; the move on all days does not. The top fifth's total move is about +0.81 % a day, 4.3 times the 0.19 % cost of a trade. The idea as tested has a total move of 1.2 times the cost and an unusual move of 0.6 times. Its unusual move of +0.11 % is not sure on its own (t 1.00), and that weak size comes from pooling the ordinary days.
- **F4:** Holding only on days whose product exceeds the coin's own past 80th percentile (rolling 120 days, known at the close) cuts the deepest fall from −36.3 % to −25.9 %. In my reconstruction on folds B and C, that book reaches Calmar 0.74 (Sharpe 0.85, 14.5 % of coin-days held, 0.38 % a day while in a position).
- **F5:** The effect lives in agitated markets. With the past-only top signal, next-day excess is +1.24 % (t 3.46, n 345) when the 30-day swing is above the 90-day swing, against +0.27 % (t 1.70, n 924) when calm. Agitation alone, without the signal, earns −0.45 % (t −2.79, n 1320), so it is not an effect of its own. It belongs to the theory: in agitated markets a wide low close is more often forced liquidation.
- **F6:** The top-signal book restricted to agitated markets has the shallowest fall: deepest fall −9.1 %, Calmar 1.25, Sharpe 0.97, lowest Sharpe with one window left out 0.85. It earns 0.80 % a day while in a position, on 3.9 % of coin-days.
- **F7:** Inside the past-only top days the effect is graded. The tertile furthest above the coin's 80th percentile earns +0.96 % next-day excess (t 3.33, n 423), against +0.33 % and +0.31 % for the other two tertiles.
- **F8:** A falling trend does not repair the book. The top fifth earns +0.84 % excess in a falling 60-day trend (t 3.16, n 437) and +0.57 % in a rising one (t 1.72). But the top-signal book outside rising markets has Calmar only 0.26 (deepest fall −26.3 %), so the trend is not where the falls are avoided.

## Ideas
- `035-01.d1_agitated-wide-day-low-close-rebound` (from F1, F2, F3, F5, F6, F7): In an agitated market, the further a day's high-to-low range times the nearness of its close to the low rises above what is usual for that coin over the past four months, the larger the coin's rise over the next day.
- `035-01.d2_unusual-wide-day-low-close-rebound` (from F1, F2, F3, F4, F7): The further a day's high-to-low range against its 14-day average, times the nearness of its close to the day's low, rises above what is usual for that coin over the past four months, the larger the coin's rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
