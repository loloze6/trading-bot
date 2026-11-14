---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above its long simple moving average, it keeps drifting upward with the size of its distance above the average, only while its own price over the recent weeks has been rising; the stronger that recent rise, the larger the drift that follows.
Consequence: A trader should grade the long on the coin's recent price momentum as well as its distance above the average, and hold little or nothing when the coin is above the average but has been falling over recent weeks.
Why:
- F2: The losing long bars are those where the forecast has been shrinking. The 20-bar change in the forecast was 0 or negative on 3,003 long bars, and these earned -0.00003 per bar (Sharpe -0.02, worst 1% -0.0825). Long bars where it had risen earned 0.00255 to 0.00398 per bar (Sharpe 1.96 and 1.55).
- F5: The coin's own fading move gives the same picture. Long bars with the 20-bar price change below -9.7% earned -0.00022 per bar (Sharpe -0.36), and with the 60-bar change below -9.8%, -0.00023 per bar (Sharpe -1.27). Bars whose distance above the SMA had shrunk by more than 17 points over 20 bars earned 0.00003 per bar (Sharpe 0.04), against 0.00350 per bar where it had grown by more than 21 points.
- F6: Size makes the falls worse: the worst 5% of long-bar losses came at a mean allocation of 1.00 against 0.51 on all long bars. Part of this is late in a trend: when the 60-bar price change was above +49.5%, Sharpe fell to 0.56, from 1.48–1.63 for changes between +11% and +49.5%.
