---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's close sits within its 60-day close range and the larger its 28-day return, the higher its return over the next 10 days.
Consequence: A trader would lean long a coin trading near its 60-day high after a strong 28-day rise, and would refuse to buy a coin after a deep 28-day fall near its 60-day low.
Why:
- F1: The test's result points the other way from the idea, not short of it. The pooled slope of the 10-day unusual return on the forecast is −0.0010 (t −1.49, 1,691 grid cells). Cells with a positive forecast average −0.67 % unusual over 10 days (1,036 cells), against +1.06 % for cells with a zero forecast (655 cells). The cases' unusual move is −0.92 % per case (931 cases).
- F2: The idea's situation is followed by continuation, not rebound, and most clearly over the shortest horizon. The slope is −0.0017 over 5 days (t −3.66, 1,728 cells), −0.0010 over 10 days (t −1.49) and −0.0012 over 20 days (t −1.05, 1,547 cells). Five of the six coins have a negative 5-day slope (ETH t −2.66, XRP t −1.92, BTC t −1.68); XMR is the exception (t −0.04).
- F3: Sorted by the 28-day return, the 10-day unusual return rises steadily from the deepest falls to the largest rises: about 250 cells per quintile.
- F4: Sorted by the close's position in its 60-day range, the 10-day unusual return is lowest near the low and highest near the high.
- F7: The 28-day return used as a straight line is a weak predictor. Its raw pooled slope on the 10-day unusual return is positive but small (t +1.50), and positive in each volatility tercile (t +1.84, +0.30, +2.24). This is weaker than the quintiles of F3 suggest, probably because a few very large 28-day rises dominate the straight line.
