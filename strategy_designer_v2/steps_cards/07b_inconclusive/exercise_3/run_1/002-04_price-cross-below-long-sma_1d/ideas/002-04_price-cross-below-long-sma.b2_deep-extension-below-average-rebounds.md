---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits below its 200-day simple moving average, it keeps falling more over the following days than its usual drift, but only for moderate distances below the average; the further the close is stretched beneath it, the larger the rebound that follows.
Consequence: A trader would avoid adding to shorts as price stretches far below the long average, and would treat deep extension as a reason to cover rather than press.
Why:
- F4: The plan's grading runs the wrong way at its extreme. Blocks in the deepest quartile of distance below the SMA are followed by a +0.0074 excess return (t 0.68), while the q2 and q3 quartiles are followed by -0.0071 and -0.0072. Likewise, blocks after the largest 60-day fall rebound +0.0077 (t 0.70), against -0.0166 (t -1.64) for the middle tercile. The supporting slope is -0.0126, which also fails.
- F2: The effect is mixed by period. Over the 10 bars after a short block's start, the coin's excess return was -0.0365 (t -2.18, n 133) in 2018, -0.0165 (t -1.85, n 140) in 2019 and -0.0232 (t -2.48, n 195) in 2022, which is downward persistence. It was +0.0257 (t 1.72, n 87) in 2020 and +0.0683 (t 2.78, n 68) in 2021, which is a reversal. The years cancel out to a pooled -0.0020 (t -0.44, n 931).
