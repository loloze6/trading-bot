---
line: 7.d not profitable
backtest: N4-03_breakouts-pay-in-uptrends_1d
idea tested: N4-03_breakouts-pay-in-uptrends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3578 USD
---
## Findings
- **F1:** The short side causes most of the book's loss. The 1330 SHORT trades in the mean_reversion regime average −1.58 % before fees, −2104 % summed, and short bars run −0.00103 a day against +0.00102 for long bars. When the short forecast is at its strongest (≤ −10), the coin then beats holding by +0.034 over 10 days (t 1.80, 37 non-overlapping cases). In a downtrend, a close near the 20-day high is followed by a rise, not a fall.
- **F2:** Long trades pay only when the 60-day trend is up. In the trending regime, forecast-active bars beat holding over 10 days by +0.0276 when the past 60-day return is positive (t 2.19, 253 cases), and by −0.0029 when it is negative (t −0.25, 288 cases).
- **F3:** Every position pays when it points the same way as the past 20-day move. Longs gross +0.0029 a day when the 20-day return is up and −0.00082 when it is down. Shorts gross −0.00225 a day when it is up and +0.00052 when it is down.
- **F4:** Fees are not the cause: the gross sum is 12926 % and the net sum 12560 %, about 0.3 % of commission per trade. The losses come from short holds. The 765 long trades held 2 days or less average −3.18 % before fees (−2430 % summed). Long trades held 10–30 days average +19.0 %, and those held over 30 days +32.0 %.
- **F5:** Only the largest forecast earns. Long bars with forecast ≥ 10 beat holding by +0.084 over 10 days (t 2.90, 87 cases). The 2–10 bucket earns +0.005 (t 0.39, 225 cases) and the 0–2 bucket −0.013 (t −1.20, 198 cases). Over all trending grid bars, the regime alone earns +0.0023 (t 0.38, 902 cases).
- **F6:** The book lags plain holding. Its mean daily return in the trending regime is 0.00097 against the coin's 0.00119, with a mean absolute position of only 0.34 when active. Results vary across windows: 11 of 24 windows have a negative mean book return.
- **F7:** Long gains shrink as volatility rises. Long bars gross +0.00153 a day in the calm third of 20-day volatility, +0.00118 in the middle third and +0.00062 in the volatile third. Shorts lose most in the volatile third (−0.00111).

## Ideas
- `N4-03_breakouts-pay-in-uptrends.d1_breakouts-pay-in-uptrends` (from F1, F2, F3, F5): A close at or very near its 20-day high, while the coin is above its 200-day average and its 60-day return is positive, is followed by a 10-day rise larger than the coin's usual 10-day move.
- `N4-03_breakouts-pay-in-uptrends.d2_persistent-highs-keep-rising` (from F4, F5): When a coin's close has stayed in the top part of its 20-day close range for several consecutive daily bars, the coin keeps rising over the next 10 days more than it does on average.
- `N4-03_breakouts-pay-in-uptrends.d3_calm-breakouts-drift-further` (from F7, F2): A close near its 20-day high in an uptrend is followed by a larger 10-day rise when the coin's recent 20-day volatility is low than when it is high.
- `N4-03_breakouts-pay-in-uptrends.d4_downtrend-highs-mark-rebounds` (from F1, F3): Below its 200-day average, a coin whose close reaches the top of its 20-day range then rises over the next 10 days more than its usual 10-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
