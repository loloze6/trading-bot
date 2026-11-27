---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7567 USD
---
## Findings
- **F1:** The book's gain comes from one window, and it fails on Calmar because it is so rarely exposed, not because of cost. In folds B and C, w16 alone summed +0.119 of daily book return out of +0.128 over all twelve windows, so the other eleven windows together added about +0.009. w16's trades netted +267 % summed against +165 % for all 141 trades, and the 2021 trades lost −121 % over 55 trades. The book was in a position on only 4.2 % of bars, with a mean absolute allocation of 0.28. With a total move of +1.80 % per case, 8.1 times the 0.22 % cost, the fee is not what sinks it.
- **F2:** The range multiple that sizes the short does not carry the fall on these folds, so the forecast's size points at the wrong cases. Upper-close, negative-5-day-return bars with a wide day (range multiple above 1.3) gave an unusual 5-day short move of +0.4 % (t 0.22, 17 bars, 15 days). Narrower days gave +6.3 % (t 2.85, 92 bars, 72 days). The trades in the lowest range-multiple tercile lost −0.43 % net each, with a 27 % win rate.
- **F3:** The fall grows with the depth of the 5-day fall measured in the coin's own swing (5-day return over its 20-day daily standard deviation × √5), and that depth alone is not the effect.
- **F4:** The fall is larger when the coin swings more than usual for itself, which is the brief's own claim that agitation carries the reversal. The condition alone does not earn.
- **F5:** A short whose first day goes against it keeps losing. Of the 141 trades, the 79 whose next day closed higher netted −3.67 % on average, and the coin kept moving against the short by about 0.95 % over the remaining days. The 62 trades whose first day went their way netted +7.34 %. The fall builds over the whole 5 days rather than at once: on all situation bars the short gave +1.9 % at 1 day (t 0.99), +3.5 % at 3 days (t 1.78) and +4.5 % at 5 days (t 2.33, 109 bars, 81 days).

## Ideas
- `061-01.b1.b1.b1.d1.d1.d3.d2.d1_deep-dip-upper-close-fade` (from F3, F2, F1): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the deeper that 5-day fall against the coin's usual daily swing over the last 20 days, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d3.d2.d2_own-agitation-graded-upper-close-fade` (from F4, F1, F2): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the more the coin's swing over the last 20 days ranks high against its own past year, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d3.d2.d3_confirmed-upper-close-fade` (from F5, F1): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative and the next day closes lower again, its price falls over the following four days, and the lower that next day's close against the signal day's close, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
