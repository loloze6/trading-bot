---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3857 USD
---
## Findings
- **F1:** The book earns less per unit of risk than holding: its daily Sharpe is 0.306 against the coin's 0.509, and its daily return sd is 0.0510 against the coin's 0.0483, even though it is in a position on only 9869 of 17022 days.
- **F2:** The higher risk comes from leverage, not from edge. The average position when in the market is 0.95, with a maximum of 2.2. Book sd rises from 0.0130 at positions 0–0.5 to 0.1096 at positions 1.5–2.3. Window max drawdowns have a median of −22%, a lower quartile of −49% and a worst of −96%, which gives a Calmar of 0.00098.
- **F3:** On days in a position the book makes 0.00141 a day while the coin makes 0.00149. The forecast therefore adds nothing over holding when it is on. On flat days the coin still rises 0.00100 a day and the book makes about 0.
- **F4:** A larger raw spread does not earn more, yet the book sizes up with it. The coin's daily return is 0.00187 and 0.00226 in the two lowest in-position spread quartiles, where mean positions are 0.16 and 0.71. It is 0.00092 in each of the two highest quartiles, where mean positions are 1.31 and 1.62.
- **F5:** Measured per trade, a larger entry forecast earns less. 530 trades entered at forecast 15–20 average −2.89% before fees. 150 trades entered at forecast 0–5 average +9.15%.
- **F6:** Measured per day, the coin's return grows only weakly with the forecast: 0.00094 at forecast 0–5 against 0.00155 at 15–20, with 0.00130 when the forecast is 0. The forward 20-day return is not monotone in the forecast either: its mean is 0.026, 0.074, 0.021 and 0.038 across the four positive buckets, against 0.028 at forecast 0. This is consistent with the inconclusive slope t of 0.37.
- **F7:** Fees are not the cause. The 1091 trades, all long, are held a median of 34 days and average +0.87% before fees against 0.10% of fees.
- **F8:** The trades' gains are carried by the long holds. 351 trades held over 50 days average +21.2%. Every shorter bucket loses on average: 25 trades of 0–2 days lose 12.0%, 65 trades of 2–5 days lose 8.6%, 174 trades of 5–15 days lose 9.7% and 473 trades of 15–50 days lose 8.3%. Only 31% of trades win.
- **F9:** Losses come from in-position days when the market has been falling over 20 days. These 5580 days average −0.42% for the book, against +0.87% on 4289 rising days. The in-position sample has more falling days than rising ones.
- **F10:** In-position days in a newly started signal do poorly. Days 10–30 after the forecast turns on see the coin fall 0.00135 a day, against +0.0030 on days 30–60. This fits a cross that often fires near a short-lived peak before the trend sets in.
- **F11:** Calm in-position days earn little: the book makes 0.00029 a day in the calmest third against 0.00254 in the most volatile third. The coin returns −0.00028 and 0.00273 a day in those same thirds.
- **F12:** The tails nearly cancel out. The 10% of in-position days with book returns below −5% sum to −110.7, against +120.7 from days above +5%. All in-position days together sum to only +13.9.
- **F13:** The book loses money in the bear years, with daily means of −0.00106 in 2018 and −0.00050 in 2022, despite being in position on only 25% and 36% of days. It trails the coin in every rising year, for example 0.00096 against 0.00423 in 2020.
- **F14:** By coin, trades lose on average before fees in LTC (−5.7%), XMR (−4.4%) and ETH (−3.0%). ZEC earns +10.6%, BTC +2.8% and XRP +1.8%.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_mature-up-signal-drifts-higher` (from F10, F8, F5): While a coin's short moving average stays above its long one, the coin's price rises more in the later part of that stretch than in its first weeks. The first weeks after the up-cross often see a pullback from a short-lived peak.
- `002-01_sma-golden-cross-upward-drift.d2_wide-gap-marks-exhaustion` (from F4, F5, F6, F2): When a coin's short moving average stands far above its long one, compared with the gap's own recent history, the coin's next rise is smaller than when the gap is modest.
- `002-01_sma-golden-cross-upward-drift.d3_up-signal-needs-recent-momentum` (from F9, F13, F10): While a coin's short moving average is above its long one, the coin keeps rising only on days when its close is above its close of about a month earlier.
- `002-01_sma-golden-cross-upward-drift.d4_trend-pays-when-volatile` (from F11, F12): While a coin's short moving average is above its long one, the coin rises more on days when its recent volatility is high than on calm days.
- `002-01_sma-golden-cross-upward-drift.d5_down-cross-still-drifts-up` (from F3, F1, F13): After a coin's short moving average crosses below its long one, the coin's price still drifts upward on average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
