---
brief: 010_rsi-midline-regime-direction
source-idea: 010-07_rsi-above-streak-reversal
line: 7.g patterns
backtest: 010-07_rsi-above-streak-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the lower the coin's return over the next 14 days.
Consequence: A long stay of RSI below 50 is a reason to stay short or out of the coin rather than to buy the dip.
Why:
- F1: Among bars where 14-day RSI sat below 50, a longer unbroken run below 50 was followed by a lower 14-day excess return. Run length is entered as negative days, so a positive pooled slope means longer runs did worse. The pooled slope was +0.00357 per day (t = 3.21, n = 142 grid cases), with Spearman rho 0.19 (p = 0.027). It held in ETH (t = 3.17, n = 76) and in w13–w24 (t = 3.86, n = 73), but was weak in BTC (t = 0.92, n = 66) and in w1–w12 (t = 0.86, n = 69). The signs below are re-expressed from round 2, where the regression was run on the signed run length.
- F2: The below-50 run effect partly survives the coin's own 30-day return. With both in the regression, the run-length slope keeps t = 2.30 while the 30-day return has t = 0.04 (n = 110). Across horizons it is mixed: the 7-day slope is negative in the same sense (t = 2.38, n = 330) and the 28-day slope agrees with t = 1.70 (n = 65). The 21-day slope reverses sign (t = 1.09, n = 92), so the effect is not clean across horizons.
- F3: The tested reversal after long runs above 50 is not in the bars. The above-50 run-length slope on the 14-day excess return is +0.00093 (t = +1.20, n = 194), the opposite sign to the idea. The book lost on both coins: mean daily −0.00134 in BTC and −0.00060 in ETH, while holding the coins earned +0.00118 and +0.00137.
