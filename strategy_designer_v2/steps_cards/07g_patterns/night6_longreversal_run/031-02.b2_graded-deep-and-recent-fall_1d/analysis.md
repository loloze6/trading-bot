---
line: 7.g patterns
backtest: 031-02.b2_graded-deep-and-recent-fall_1d
idea tested: 031-02.b2_graded-deep-and-recent-fall
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6411 USD
---
## Findings
- **F1:** A coin's 7-day return lines up with its own recent trend: on the non-overlapping 7-day grid, its excess 7-day return (minus its normal drift, in units of its usual move) rises with its 14-day return scaled by its trailing 30-day daily volatility, slope +0.155, day-clustered t 2.59 (1,642 cases, 315 days); the top quintile of the scaled 14-day return earns +2.23 % excess against −1.04 % for the bottom quintile.
- **F2:** The F1 slope is positive at every grid offset for both pasts: for the 14-day past, t 2.59, 1.77, 1.69 and 2.34; for the 30-day past, slopes +0.065 to +0.115, t 1.29 to 2.35. Over the next 3 days it is also positive at every offset, t 1.85 to 2.27 (about 4,000 cases).
- **F3:** The same 7-day continuation shows coin by coin for the scaled 30-day return, with all six slopes positive and unclustered t from 0.76 (XMR) to 2.22 (ETH). It also shows in 7 of 8 years; the exception is 2018, slope −0.42 with clustered t −1.50.
- **F4:** The continuation is concentrated in the coin's quiet periods: in the lowest tercile of trailing 30-day volatility the slope of the 7-day excess on the scaled 30-day return is +0.261 (clustered t 2.45, 548 cases), against +0.063 (t 1.16) in the middle tercile and +0.039 (t 0.71) in the high-volatility tercile.
- **F5:** The 7-day trend move is about six times the cost of a trade, but it is not firmly established. Taking the 40 % of cases with the strongest scaled 30-day return, the 7-day excess move in the trend's direction averages +1.17 % (t 1.35, 657 cases on 239 days), about 0.09 of the coins' usual 7-day move of 12.6 %, against a trade cost of 0.19 %.
- **F6:** The tested reversal does not appear at the 30-day horizon on the plain grid. Across quintiles of the past 30-day and 60-day return the 30-day excess is not monotonic (quintile means between −9.3 % and +4.5 %), and the slopes are +0.021 (t 1.35, 377 cases) and −0.020 (t −0.98, 240 cases).
- **F7:** The book's gain rests on few coins and few days, and its long holdings lose. XRP, XMR and ZEC contribute 3.62, 1.50 and 1.25 of the summed daily book returns, while BTC and LTC are slightly negative. The top 1 % of book days (29) sum to 1.29, more than the whole book's 1.07. Trades held longer than 60 days average −4.4 % (median −12.8 %, 44 trades), against +19.7 % for trades closed at about 30 days (44 trades).
- **F8:** After a coin's daily move, scaled by its trailing volatility, the next day leans the other way only in its mid- and high-volatility terciles (slopes −0.067, t −2.24 and −2.15), not overall (t −1.16) and not in its quiet tercile (+0.017). Given how many angles were looked at, this does not stand out from chance.

## Ideas
- `031-02.b2.g1_short-horizon-scaled-trend-continuation` (from F1, F2, F3, F5, F6): The further a coin's 14-day return stands above its own recent daily volatility (scaled by the square root of 14 days), the more its price rises over the next 7 days, and the further below, the more it falls.
- `031-02.b2.g2_quiet-market-trend-continuation` (from F4, F1, F2): While a coin's last 30 days of daily returns are calmer than its usual, the further its 30-day return stands above its recent daily volatility, the more its price rises over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
