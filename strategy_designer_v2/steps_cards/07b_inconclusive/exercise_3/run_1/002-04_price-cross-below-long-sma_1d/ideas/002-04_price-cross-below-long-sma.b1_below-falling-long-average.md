---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits below its 200-day simple moving average, it keeps falling more over the following days than its usual drift, only while that long average is itself falling, and the steeper the average's decline the larger the further fall.
Consequence: A trader would short closes below the long average only when the average itself is turning down, and would stand aside when it is still rising.
Why:
- F3: The persistence shows where the 200-day average itself is falling. In the quartile of active blocks with the steepest 20-day fall of the SMA, the 10-bar excess return is -0.0148 (t -1.49, n 199), and it is negative for 5 of 6 coins. In the other three slope quartiles it is +0.0010, -0.0029 and -0.0030, all with |t| < 0.4.
- F2: The effect is mixed by period. Over the 10 bars after a short block's start, the coin's excess return was -0.0365 (t -2.18, n 133) in 2018, -0.0165 (t -1.85, n 140) in 2019 and -0.0232 (t -2.48, n 195) in 2022, which is downward persistence. It was +0.0257 (t 1.72, n 87) in 2020 and +0.0683 (t 2.78, n 68) in 2021, which is a reversal. The years cancel out to a pooled -0.0020 (t -0.44, n 931).
- F5: The book's loss is the market's own rise. Its mean daily return is -0.000281, of which -0.000280 is the short position × the coins' mean daily return, so the timing part is essentially zero. On raw returns the coins rose +0.0109 over 10 bars while shorted (t 2.37, n 931).
