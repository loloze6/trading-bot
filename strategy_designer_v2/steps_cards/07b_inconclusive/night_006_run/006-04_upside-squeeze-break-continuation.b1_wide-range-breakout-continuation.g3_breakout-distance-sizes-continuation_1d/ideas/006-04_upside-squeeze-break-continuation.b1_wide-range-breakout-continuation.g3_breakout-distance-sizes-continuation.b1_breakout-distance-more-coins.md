---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits above the highest high of its prior 20 days, as a share of that high, the further its price rises over the next 10 days.
Consequence: A trader would size upside breakouts by how far price clears the prior high, not by how compressed the range was before it.
Why:
- F1: The test's slope t of +1.79 on 108 breakout cases rests on a few very large outcomes. Trimming the top and bottom 5 % of excess returns turns it to −1.45 (96 cases), dropping the 3 largest excess returns gives −1.47, and the rank correlation of forecast with excess return is −0.13 (p 0.18).
- F2: The slope is not shared across coins. ZEC alone carries it with t +4.07 on 21 cases; without ZEC it is −0.47 on 87 cases, LTC is −2.77, and ETH and XMR are negative.
- F3: The slope also flips between years: −1.58 in 2021, −1.16 in 2023, −1.10 in 2024 and +3.02 in 2025.
