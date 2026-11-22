---
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
idea tested: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4427 USD
---
## Findings
- **F1:** The book loses because being short costs more than its timing earns. Per bar it makes -0.017 %. Before fees that is -0.011 %, which splits into -0.029 % from shorting coins whose average daily return is positive and +0.018 % from timing, plus 0.006 % of fees. The book is short on 44 % of bars, at a mean of -0.45 of the book.
- **F2:** The fade exists only in coins that are also deep in a 30-day fall. Among rises of more than 1 usual daily move in falling coins, those whose 30-day return is in the lowest third (below -12.7 %) are followed by a large unusual fall:
- **F3:** Inside that deepest 30-day third the fade grows with the bounce. Rises of 1–1.75 usual moves give 3.7 % (t 2.34, n 84), 1.75–2.5 give 4.3 % (t 1.93, n 21), and above 2.5 give 11.5 % (t 4.44, n 11). The product of the bounce size and the 30-day fall depth grades the same way: its top quartile gives 4.8 % (t 3.09, n 87) and its two lowest quartiles about -0.4 %.
- **F4:** Where the 90-day return is negative but the 30-day return is positive, the shorts lose. Bounces of 1–1.75 usual moves in the top 30-day third (above +4.4 %) give -3.0 % unusual (t -2.06, n 75). The book's short bars in the top 30-day quartile (above +6.9 %) average -0.149 % per bar, summing to -4.71, against +0.09 % per bar in the two lowest quartiles.
- **F5:** The 90-day return, which defines the regime, does not grade the effect. Rises of more than 1 usual move give -0.1 % (t -0.05), 1.0 % (t 0.56) and 1.4 % (t 0.70) across its three terciles (30 cases each).
- **F6:** The book's strongest shorts lose the most. Trades entered at a forecast of -15 or below lose 4.07 % net (n 2092), against 0.53 % net for entries between -5 and -2 (n 766). Also, 35 % of the book's active bars have a one-day rise below 1 usual move, because the forecast standardises the rise against its own 60-day history.
- **F7:** In coins with a non-negative 90-day return, large rises are followed by further rises. Rises of 1.5–2 usual moves give -2.4 % unusual in the short direction (t -2.33, n 161), and rises of 2–3 usual moves give -9.9 % (t -2.36, n 100).

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.d1_bounces-fade-in-deep-falls` (from F2, F3, F4, F5, F1): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, only while its 30-day return is negative. The fall grows steeply both with the size of the rise in usual daily moves and with the depth of the 30-day fall.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.d2_short-horizon-bounce-giveback` (from F2, F3): In a coin, a one-day rise of several usual daily moves (its 20-day standard deviation of daily returns) is given back over the next 3 days, and more so the deeper the coin's 30-day fall before the rise.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back.d3_outsized-rises-extend-uptrends` (from F7): In a coin whose 90-day return is positive, a one-day rise large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, growing with the size of the rise in usual daily moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
