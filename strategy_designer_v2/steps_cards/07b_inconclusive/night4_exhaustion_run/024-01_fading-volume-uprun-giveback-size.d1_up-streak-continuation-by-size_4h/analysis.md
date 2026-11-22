---
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3258 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but short of the bar: the forecast-weighted excess 18-bar return is +0.0029, with t 1.21 over 2857 grid cases. The supporting check passed. The size is nil: the unusual move is −0.09 % per case (strength −0.009), against a cost of 0.19 % per trade.
- **F2:** The effect is mixed by forecast size, not graded smoothly. The bottom three forecast quintiles have excess 18-bar returns of −0.16 %, −0.36 % and −0.40 % (t −0.50, −1.11, −1.20). The top two quintiles together have +0.58 % (t 2.04, n 1111). The top 40 % of forecasts carry +0.58 % (t 2.10, n 1143, strength 0.065), while the rest carry −0.25 % (t −1.34, n 1714).
- **F3:** The continuation shows where the volume behind the streak is high against the 30 bars before it. Among the strongest forecasts, the top volume tercile gives +1.27 % over 18 bars (t 2.98, n 573). The low and middle volume terciles give +0.07 % (t 0.12) and −0.31 % (t −0.67). This is the opposite of the brief's fading-volume give-back.
- **F4:** The effect changes sign with the market regime. Excess 18-bar returns after up-streaks are −1.73 % in 2018 (t −2.97, n 332) and −1.07 % in 2022 (t −2.66, n 319). They are +0.98 % in 2020 (t 1.97) and +0.66 % in 2024 (t 1.73). For the strongest streaks, the coin's 30-day return matters: +1.20 % in its top tercile (mean 30-day return +42 %, t 1.66), against −0.07 % in its bottom tercile (t −0.14).
- **F5:** The sign is the same across coins but no single coin is clear. Each of the six coins has a positive top-forecast excess, from +0.15 % (BTC) to +1.30 % (XRP), with every t between 0.26 and 1.57 and about 170 to 220 cases per coin.
- **F6:** At other horizons the picture changes. Over 6 bars (one day), the weakest streaks reverse: their excess return is −0.28 % (t −3.21, n 2802), and the all-streak weighted measure is t −1.49. Over 12 and 36 bars, the weighted t is 0.20 and 0.63. The plan's 3-day horizon is where the continuation is largest.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins` (from F1, F2, F5): When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, and the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b2_volume-backed-up-streak-continuation` (from F2, F3, F4): When a coin has just risen in an unbroken streak of four-hour periods while the volume traded during the streak is above its volume of the five days before, it keeps rising over the next three days. The larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
