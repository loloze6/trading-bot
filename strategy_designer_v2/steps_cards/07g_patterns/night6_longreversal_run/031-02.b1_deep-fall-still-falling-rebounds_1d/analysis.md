---
line: 7.g patterns
backtest: 031-02.b1_deep-fall-still-falling-rebounds_1d
idea tested: 031-02.b1_deep-fall-still-falling-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4463 USD
---
## Findings
- **F1:** A coin's strong 30-day rise tended to continue over the next 7 days rather than reverse. On non-overlapping 7-day stretches, the coin's 7-day return minus its normal drift rose with its 30-day return scaled by its own 30-day daily volatility. The covariance of the two was +0.0131, with a day-clustered t of 2.51 over 2,830 cases on 315 days. The top quintile of the 30-day return was followed by +2.38 % (t 2.07, 154 days) and the bottom quintile by −0.73 % (t −0.73, 148 days). That is roughly 10 times the 0.22 % cost of a trade.
- **F2:** The same continuation shows on most coins and most years. The Spearman correlation between the scaled 30-day return and the excess 7-day return was positive on 12 of 15 coins, with a median of 0.058. The top-minus-bottom quintile difference was positive in 6 of 8 years and clearly negative only in 2018, at −10.2 %.
- **F3:** A shorter look-back gives the same lean. The top quintile of the 7-day return, scaled by 30-day volatility, was followed by an excess 7-day move of +2.07 % (t 1.99, 156 days), against −0.01 % for the bottom quintile.
- **F4:** At the brief's own 30-day horizon, past 30-day moves show no lean toward reversal. The Spearman correlation between the scaled 30-day return and the excess 30-day return was +0.091 (p 0.019, 654 cases), so it leans toward continuation. The top quintile was followed by +6.28 % (day-clustered t 1.47, 33 days) and the bottom by −2.23 % (t −0.49).
- **F5:** Within the tested regime, depth of fall does not grade the rebound. The deepest third of the 90-day fall was followed by +8.05 % excess over 30 days (t 1.54, 22 cases), the shallowest third by −5.01 % (t −1.01). The forecast's Spearman correlation with the excess return was −0.013, and the idea's own size is +4.51 % with a t of only 1.23 on 96 days.
- **F6:** Summed per-trade net returns are concentrated in a few coins and are not part of a graded effect. XRP gives +968 % over 28 trades, UNI +550 % and AVAX +358 %, out of about +2,751 % in total. BTC (−52 %), ADA (−78 %) and INJ (−76 %) lose. By entry-forecast tercile, median trade results are 3.2 %, 1.1 % and 2.2 %, so they do not rise with the forecast.
- **F7:** The weekday pattern is too weak to count after the many angles examined. Saturday's cross-coin mean daily return is +0.46 % (t 3.01 over 414 days) and Friday's +0.38 % (t 1.89). Only one weekday out of seven passes a t of 3, so I note it but propose no idea from it.

## Ideas
- `031-02.b1.g1_strong-month-continues-next-week` (from F1, F2, F3, F4): The further a coin's 30-day return stands above its usual 30-day move, judged against its own recent daily volatility, the more its price keeps rising over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
