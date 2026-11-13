---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2895 USD
---
## Findings
- **F1:** Across the 930 short blocks the mean excess fall is only 0.07% per 10 bars (t 0.16, hit rate 52.5%), against a block-to-block spread of 14.0%, so any edge is buried in the market's own 10-day moves.
- **F2:** The sign of the result flips by year: shorts gained in 2018 (+3.9%, t 2.32, n 134) and 2022 (+2.3%, t 2.48, n 195), but lost in 2020 (−4.3%, t −2.73, n 88) and 2021 (−5.1%, t −2.32, n 74), and these cancel in the pooled mean.
- **F3:** The windows split the same way, from w9 (+4.0%, t 3.71) and w7 (+5.8%, t 3.35) to w23 (−6.7%, t −3.12) and w21 (−3.6%, t −2.75), while no coin stands out (coin means range from −0.39% to +0.56%, all |t| < 0.6).
- **F4:** Sitting deeper below the average does not help: the deepest forecast bucket (−20 to −10) gives −0.15% (t −0.17, n 294), the −10 to −5 bucket gives +0.64% (t 0.76), and the slope of excess return on allocation has the wrong sign (−0.0056).
- **F5:** Shorts gained most when the 200-day average itself had fallen more than 5% over the prior 20 bars: +1.6% excess fall (t 1.74, hit 54.8%, n 217), against roughly 0% where the average was flat or rising (−0.58% to +0.44%, all |t| < 0.7).
- **F6:** Timing since the cross matters but is not steady: the first 10 bars below the average give +1.7% (t 1.34, n 155), bars 10–30 give −1.95% (t −1.94, n 224), and bars 60–120 give +1.7% (t 1.81, n 210).
- **F7:** The share of coins below their own averages adds little on its own: with a falling average and broad weakness the shorts gain +0.66% (t 0.95, n 353), and this pocket still swings by year, +4.8% (t 2.95) in 2018 against −2.9% in 2020.

## Ideas
- `002-04_price-cross-below-long-sma.b1_steeply-falling-long-average` (from F5, F1, F4): When a coin's close is below its 200-day average and that average has itself been falling steeply over the past few weeks, the coin keeps falling over the next 10 days by more than its usual drift.
- `002-04_price-cross-below-long-sma.b2_fresh-cross-below-continues` (from F6, F2, F3): In the first days after a coin's close crosses below its 200-day average, the coin keeps falling over the next 10 days by more than its usual drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
