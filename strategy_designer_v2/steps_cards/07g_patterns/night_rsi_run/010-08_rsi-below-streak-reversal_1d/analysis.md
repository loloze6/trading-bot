---
line: 7.g patterns
backtest: 010-08_rsi-below-streak-reversal_1d
idea tested: 010-08_rsi-below-streak-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3253 USD
---
## Findings
- **F1:** The book's gain came from the coins' rise, not from timing: the mean position was 0.23, and per bar the market part was +0.000316 and the timing part −0.000287, for a total of +0.000028; daily book returns were +0.000161 (BTC) and −0.000306 (ETH), against +0.001183 and +0.001368 for holding the coins.
- **F2:** The run length of RSI(14) on either side of 50 sorted the next 14-day excess return in no order (grid bars n=288; streak slope t −0.66). Runs of 20 or more days below 50 averaged +2.9% (t 1.01, n=40), and runs of 11–20 days above 50 averaged −3.2% (t −1.74, n=30), with the other buckets in between showing no gradient.
- **F3:** Neither RSI level, 7/14/28-day return, position in the 28-day range, nor 20-day volatility predicted the next 14 days (n=288). All slope t's fell between −0.66 and +1.77, and the RSI quintiles alternated in sign (−0.7%, +0.5%, −1.7%, +3.0%, −1.0%).
- **F4:** A day's volatility-scaled return predicted the next day's return with the opposite sign (slope −0.00156, t −2.69, n=4450). Days down more than 2 sigma were followed by +0.84% (t 1.77, n=141). But the effect sat entirely in 2018–2021 (t −2.04 BTC, −2.58 ETH) and vanished after (t +0.12 BTC, −0.23 ETH).
- **F5:** Over 7 days the same scaled one-day move had the same sign as what followed (slope +0.0108, t 2.55, n=623). A 3-day scaled move predicted the next 3 days with t 2.23 (n=1427). Volume surprise and 28-day drawdown showed nothing at 1, 3 or 7 days (|t| ≤ 0.91).
- **F6:** By weekday, Wednesday averaged +0.41% (t 2.61) and Thursday −0.36% (t −2.03), each with about 696 days. The sign held in both halves and both coins, but no individual t passed 2.3 out of 14 coin-by-day cells.
- **F7:** The book's worst 2% of days (n=116) came with coin moves averaging −7.3%, and its best 2% with +7.5%. Its extremes were simply large coin moves while it was long.

## Ideas
- No ideas: I tested about 30 forecasts across horizons, weekdays and regimes, and none cleared a multiple-testing bar (the largest |t| was 2.69). The strongest, next-day reversal after a large daily move (F4), disappeared after 2021. The data also held only BTC and ETH, not BNB.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
