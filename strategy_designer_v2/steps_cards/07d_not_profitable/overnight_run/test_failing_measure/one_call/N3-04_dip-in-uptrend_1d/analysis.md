---
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
idea tested: N3-04_dip-in-uptrend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3670 USD
---
## Findings
- **F1:** The Calmar failure comes from one stretch of windows: book drawdown measured on daily book returns reaches -36.2% across w11–w17, against a 21.1% annualised mean, with within-window falls of -18.5% (w11), -19.1% (w13) and -21.3% (w17); w1–w10 never fall below -11.0%.
- **F2:** The falls are concentrated on a few days when many coins are held at once. The 58 worst book days (2%) sum to -3.04, against +1.67 summed over all days. On those days the book holds 3.9 coins on average, against 2.3 on ordinary negative days. Coin-days with 4 or more coins held show a summed coin P&L standard deviation of 0.288 and a worst of -1.23, against 0.037 and -0.38 when one coin is held (167 vs 764 days).
- **F3:** The large positions carry both the edge and the losses. Bars held at allocation ≥1 have a next-day excess return of +0.0069 (t 3.56, n 821), but their summed losses are -22.7 against -7.2 for all smaller positions (n 1949), and their P&L standard deviation is 0.102 against 0.019.
- **F4:** The edge depends on short-term volatility expanding.
- **F5:** Held bars whose own 60-day return, computed from the bars, is ≤0 have a next-day excess of -0.0049 (t -1.98, n 282). Held bars in 2018 have -0.0150 (t -2.10, n 126). Dips bought once the uptrend has faded are followed by underperformance.
- **F6:** The windows holding the drawdowns (w11–w17, w20–w23) give a held-bar excess of only +0.0012 (t 0.83, n 1403) with summed losses of -20.9. The other windows give +0.0032 (t 2.80, n 1367) with losses of -9.0.
- **F7:** A dip that follows a prior down day of more than one mean absolute move is followed by an excess of +0.0062 (t 2.35, n 356). After a prior up day the excess is +0.0022 (t 1.68, n 1319), and these bars carry -15.4 of losses.

## Ideas
- `N3-04_dip-in-uptrend.d1_dips-pay-in-expanding-volatility` (from F3, F4, F6): In a coin whose 20-day and 60-day returns are positive, a large one-day drop is followed by an above-average next-day return when the coin's 20-day volatility is above its 60-day volatility. When the 20-day volatility is below the 60-day volatility, the same drop is followed by a below-average next-day return.
- `N3-04_dip-in-uptrend.d2_faded-uptrend-dips-keep-falling` (from F1, F5, F6): A one-day drop in a coin whose own 60-day return has fallen to zero or below is followed by a below-average next-day return. The drop marks continuation of a fading trend rather than a dip to buy.
- `N3-04_dip-in-uptrend.d3_second-day-dips-rebound-more` (from F2, F3, F7): In an uptrend, a large one-day drop that follows a previous day's drop of more than the coin's mean absolute move is followed by a larger next-day rebound than a single drop after an up day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
