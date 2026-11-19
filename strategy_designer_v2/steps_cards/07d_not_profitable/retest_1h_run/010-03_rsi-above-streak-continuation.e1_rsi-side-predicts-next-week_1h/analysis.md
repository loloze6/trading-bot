---
line: 7.d not profitable
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
idea tested: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2900 USD
---
## Findings
- **F1:** Fees eat the gain: gross gain per bar is +0.000065 (BTC) and +0.000083 (ETH), but fees are 0.000171 and 0.000152 per bar, so the book loses -0.0025 and -0.0017 per day while holding the coins makes +0.0012 and +0.0014 per day.
- **F2:** The position churns. It turns over 0.23 (BTC) and 0.17 (ETH) of the book per bar and trades on 51% of bars, and 31–34% of that turnover comes from sign flips. The forecast changes sign 2.4–2.6 times a day even though its 24-hour autocorrelation is 0.73.
- **F3:** The traded forecast is not the RSI's distance from 50. It correlates only 0.35 (BTC) and 0.39 (ETH) with RSI−50 and agrees with its sign on 78% of bars. Once both are scaled, it loads almost as much on RSI's 7-day change (7.9 and 7.8) as on its level (8.5 and 8.9), because the 337-bar standardisation measures RSI against its own 14-day mean.
- **F4:** The level the idea names carries no 7-day edge. RSI−50 scaled × 168h excess return gives t = −0.98 (n = 718 non-overlapping cases), and its quintiles do not line up: excess +0.0012, −0.0154, +0.0016, +0.0024, −0.0062 from lowest to highest. RSI's 7-day change gives t = +2.01, and the traded forecast t = +1.37.
- **F5:** The loss is broad, not one bad period. The book's mean daily return is negative in 20 of 24 windows, including w10, w21 and w23, where the coin rose +0.0046, +0.0038 and +0.0045 per day while the book lost −0.0027, −0.0020 and −0.0029.

## Ideas
- `010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.d1_smoothed-rsi-side-slow-lean` (from F1, F2, F3): The higher a coin's 14-day RSI sits above 50 at the close, the higher its return over the next 1 to 7 days, and the lower it sits below 50, the lower that return, with the distance read as its average over the past 3 days, so the move follows RSI's slow drift rather than its hour-to-hour swings around 50.
- `010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.d2_rsi-weekly-change-continuation` (from F3, F4): The more a coin's 14-day RSI has risen over the past 7 days, the higher the coin's return over the next 7 days, and the more it has fallen, the lower that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
