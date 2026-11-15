---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3022 USD
---
## Findings
- **F1:** The pooled short gain is near zero at every horizon. The mean allocation × excess return is 0.000025 (t 0.21, n 17022) at 1 bar, -0.000271 (t -0.23, n 1657) at 10 bars and -0.001625 (t -0.29, n 388) at 40 bars, so no horizon shows the effect more clearly than the plan's 10 bars.
- **F2:** The effect is mixed by period. Over the 10 bars after a short block's start, the coin's excess return was -0.0365 (t -2.18, n 133) in 2018, -0.0165 (t -1.85, n 140) in 2019 and -0.0232 (t -2.48, n 195) in 2022, which is downward persistence. It was +0.0257 (t 1.72, n 87) in 2020 and +0.0683 (t 2.78, n 68) in 2021, which is a reversal. The years cancel out to a pooled -0.0020 (t -0.44, n 931).
- **F3:** The persistence shows where the 200-day average itself is falling. In the quartile of active blocks with the steepest 20-day fall of the SMA, the 10-bar excess return is -0.0148 (t -1.49, n 199), and it is negative for 5 of 6 coins. In the other three slope quartiles it is +0.0010, -0.0029 and -0.0030, all with |t| < 0.4.
- **F4:** The plan's grading runs the wrong way at its extreme. Blocks in the deepest quartile of distance below the SMA are followed by a +0.0074 excess return (t 0.68), while the q2 and q3 quartiles are followed by -0.0071 and -0.0072. Likewise, blocks after the largest 60-day fall rebound +0.0077 (t 0.70), against -0.0166 (t -1.64) for the middle tercile. The supporting slope is -0.0126, which also fails.
- **F5:** The book's loss is the market's own rise. Its mean daily return is -0.000281, of which -0.000280 is the short position × the coins' mean daily return, so the timing part is essentially zero. On raw returns the coins rose +0.0109 over 10 bars while shorted (t 2.37, n 931).
- **F6:** No coin carries the effect on its own. The 10-bar excess returns while short range from -0.0054 (XMR, t -0.57) to +0.0047 (XRP, t 0.35), all with |t| < 0.6.

## Ideas
- `002-04_price-cross-below-long-sma.b1_below-falling-long-average` (from F3, F2, F5): While a coin's close sits below its 200-day simple moving average, it keeps falling more over the following days than its usual drift, only while that long average is itself falling, and the steeper the average's decline the larger the further fall.
- `002-04_price-cross-below-long-sma.b2_deep-extension-below-average-rebounds` (from F4, F2): While a coin's close sits below its 200-day simple moving average, it keeps falling more over the following days than its usual drift, but only for moderate distances below the average; the further the close is stretched beneath it, the larger the rebound that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
