---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits below its 200-day simple moving average, the coin keeps falling beyond its usual drift only while that average is itself declining, and the faster the average declines, the further the coin falls over the following bars.
Consequence: A trader would short a close below the long average only when the average is turning down, and would size the short by the steepness of that decline instead of by the distance below it, refusing shorts under a still-rising average.
Why:
- F2: The short gain depended on the slope of the 200-day average itself. In the quartile where that average had fallen most over the past 20 bars (−15.9% to −5.5%), the mean excess 10-bar return was −0.0148 and the short gain was +0.0093 (t 1.93, n 199). In the other three slope quartiles the gain was −0.0040, −0.0014 and −0.0008 (t −0.84, −0.34, −0.44, about 199 blocks each).
- F3: Shorts held while the 200-day average was still rising lost (gain −0.0029, t −1.11, n 244). The loss was worst when the close was also deep below that rising average (gain −0.0107, t −1.59, n 63; mean excess 10-bar return +0.0093). Shorts under a falling average gained +0.0024 (n 551).
- F5: The losses fell in recovery years. The short gain was −0.0184 in 2020 (t −3.26, n 87), −0.0108 in 2021 (t −2.65, n 68) and −0.0110 in 2023 (t −2.13, n 119). It was positive in the falling-market years 2018 (+0.0125, t 1.59), 2019 (+0.0061, t 2.02) and 2022 (+0.0080, t 1.42).
- F6: The book's result rests on a few windows. It summed +0.28 in w2 and +0.26 in w14 but −0.33 in w16, and it was negative in 19 of the 24 windows. That matches the failed "lowest Sharpe, one window left out" measure of −0.70.
