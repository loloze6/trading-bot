---
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d
idea tested: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3241 USD
---
## Findings
- **F1:** The book earns a mean of 0.000173 a day against 0.00119 for holding (Sharpe 0.18 against 0.46), and about half its gross gain goes to fees (0.000362 gross per bar, 0.000187 in fees). Its market part is -0.000076 because it is short on 32% of bars and long on only 19%, and on the 49% of bars where it is flat the coin rises 0.00216 a day.
- **F2:** Only the extreme forecasts pay. The most negative sixth (forecast ≤ -14.7, mean position -0.88) gains 0.00263 a bar with excess next-bar return -0.0066, and the most positive sixth (≥ 9.2) gains 0.00127. The middle sixths (-8.7 to 1.5) lose -0.000383 and -0.000058 a bar while still holding -0.32 and -0.06 positions, so they mainly pay fees.
- **F3:** On the 3-bar grid inside 5-day falls, only the thinnest-volume quintile (log 5/30 ratio ≤ -0.45) gives a clear further decline: excess 3-bar return -0.0151 when the 30-day return is down (n=263) and -0.0115 when it is up (n=152). The middle quintiles are mixed in sign, for example -0.0074 and +0.0039 in uptrends.
- **F4:** Thin volume costs more after deeper falls. With thin volume, the two deepest 5-day-fall quartiles (≤ -4.4%) give excess 3-bar returns of -0.0090 and -0.0090 (n=199 and 315), against -0.0027 and -0.0055 for the two shallowest.
- **F5:** The long side is strongest when a fall comes on heavy volume inside a rising month. The heaviest-volume quintile (ratio > 0.238) gives excess 3-bar return +0.0279 when the 30-day return is up (n=122), against +0.0032 when it is down (n=292).
- **F6:** The book's falls happen while the coin trends, not because of it. The worst window drawdown is -0.51 (BTC) in a window where holding gained +0.20, and LTC fell -0.31 in a window where holding gained +1.32. Among the 47 windows where holding rose over 20%, the book's mean total is -0.02. The worst 3% of bars are 49% short.

## Ideas
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling.d1_deep-thin-volume-falls-continue` (from F2, F3, F4, F1): After a coin has fallen over the last 5 days, the lower its 5-day average volume against its 30-day average, the larger its further decline over the next 3 days, the more so the deeper that 5-day fall.
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling.d2_heavy-volume-dips-rebound-uptrend` (from F5, F1, F6): After a coin has fallen over the last 5 days while its 30-day return is positive, the higher its 5-day average volume against its 30-day average, the larger its rebound over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
