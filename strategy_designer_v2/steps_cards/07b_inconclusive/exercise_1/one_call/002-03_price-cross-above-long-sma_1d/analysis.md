---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2961 USD
---
## Findings
- **F1:** On the 7,046 bars with forecast > 0, the next-20-bar excess return averaged +0.65% (naive t 1.83). The median was −3.06% and the hit rate 41.98%, with a standard deviation of 29.8% and skew 4.27. The top 5% of bars carry 656% of the summed excess, so a few large rallies drive the mean and noise swamps it.
- **F2:** Most of the effect comes from one coin. ZEC's above-SMA bars returned +5.11% excess (t 3.16). The other five coins range only from −0.75% (LTC) to +0.44% (BTC).
- **F3:** The market regime drowns the effect. Above-SMA bars lost −19.4% in 2018 (hit 17.0%) and −12.0% in 2022 (hit 18.2%), against +3.83% in 2020 and +3.37% in 2024.
- **F4:** Splitting by the past 20-bar return separates the bars. With a positive past 20-bar return, above-SMA bars earned +3.46% (hit 45.7%, trimmed +0.46%, non-overlapping t 1.25). With a negative one, they earned −2.75% (hit 37.5%, trimmed −4.33%, non-overlapping t −1.75).
- **F5:** Adding the SMA's own 20-bar slope sharpens the split.
- **F6:** The effect sits in the largest forecasts. By forecast quintile, the excess rose from −2.72% and −2.26% in the two lowest to +5.15% in the top one. Forecast ≥ 10 combined with a rising past 20-bar return gave +5.29% on 2,250 bars (hit 45.9%, t 1.39).
- **F7:** The effect also depends on how long the close has been above the SMA.
- **F8:** With past 20-bar momentum up, the result holds across most coins. BTC had median +0.29% and hit 51.0%; ETH +0.81% and hit 52.2%; ZEC +0.25% and hit 50.6%. XMR was the exception at −0.23% mean and 42.7% hit.

## Ideas
- `002-03_price-cross-above-long-sma.b1_above-sma-with-momentum` (from F4, F5, F8): When a coin's close is above its 200-day SMA, that SMA is higher than 20 bars ago, and the close is also higher than 20 bars ago, the coin rises more than its average 20-bar move over the next 20 bars.
- `002-03_price-cross-above-long-sma.b2_above-sma-but-fading` (from F4, F5, F1): When a coin's close is above its 200-day SMA but lower than it was 20 bars ago, and the SMA itself is lower than 20 bars ago, the coin rises less than its average 20-bar move over the next 20 bars.
- `002-03_price-cross-above-long-sma.b3_mature-stay-above-sma` (from F7, F6, F1): When a coin's close has stayed above its 200-day SMA for more than 60 consecutive bars, the coin rises more than its average 20-bar move over the next 20 bars.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
