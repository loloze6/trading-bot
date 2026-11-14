---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits below its 200-day simple moving average, the coin keeps falling, and it falls further the farther the close sits below the average, except when the close is far below a still-rising average, where the coin rebounds more the farther below it sits.
Consequence: A trader would stop deepening a short as the distance under the long average grows while that average still rises, and treat a close deep under a rising average as a reason to refuse the short.
Why:
- F3: Shorts held while the 200-day average was still rising lost (gain −0.0029, t −1.11, n 244). The loss was worst when the close was also deep below that rising average (gain −0.0107, t −1.59, n 63; mean excess 10-bar return +0.0093). Shorts under a falling average gained +0.0024 (n 551).
- F4: The grading by depth worked against the book. In the deepest distance quartile (close 32% to 72% below the SMA200), the coin rose beyond holding (mean excess +0.0074) and the short gain was −0.0040 (t −0.65, n 233). The two middle quartiles gained +0.0008 and +0.0014.
- F5: The losses fell in recovery years. The short gain was −0.0184 in 2020 (t −3.26, n 87), −0.0108 in 2021 (t −2.65, n 68) and −0.0110 in 2023 (t −2.13, n 119). It was positive in the falling-market years 2018 (+0.0125, t 1.59), 2019 (+0.0061, t 2.02) and 2022 (+0.0080, t 1.42).
