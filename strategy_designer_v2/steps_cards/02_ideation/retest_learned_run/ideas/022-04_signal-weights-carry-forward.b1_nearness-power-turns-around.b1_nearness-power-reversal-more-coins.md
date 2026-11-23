---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power for that coin's 5-day returns over the following 90 days.
Consequence: A trader should lean against, not with, a nearness-to-high relation that has recently worked on a coin, because over the next months it tends to turn around.
Why:
- F1: The test's result falls on the side the idea predicts but just short of the bar: a pooled mean of forecast/10 × excess 5-day return of +0.00457 with t 1.97 over 3042 non-overlapping cases; the same products trimmed at their 1st and 99th percentiles give +0.00533 with t 2.81, and 66 % of the 128 coin-windows have a positive mean (t over windows 2.46).
- F2: The plain t is held below 2 by a few large cases: the 10 largest products carry 58 % of the total, and only 51.4 % of active cases have a positive product.
- F3: The effect is broad rather than confined to one part of the data: 5 of 6 coins have a positive mean (BTC +0.0050 t 1.32, ETH +0.0069 t 1.49, LTC +0.0091 t 1.73, XMR +0.0023, XRP +0.0068), against only ZEC (−0.0038, t −0.52). 6 of 8 years are positive, and both halves of the windows are positive (+0.0042 t 1.34, +0.0051 t 1.45).
- F4: The effect grows with the forecast's size, as the idea's grading predicts: by quintile of |forecast|, the mean product rises from −0.0001 to +0.0010, +0.0019, +0.0023 and +0.0178 (t 1.76). The sign-only excess return rises from −0.19 % in the weakest quintile to +0.91 % in the strongest.
- F5: The plan's 5-day horizon is where the effect shows best: t is 1.72 at 1 day, 1.42 at 3 days, 1.97 at 5 days, 1.05 at 10 days and 0.69 at 20 days. A different horizon would not sharpen the answer.
- F6: The long side carries more of the effect (+0.0074, t 2.20, 1574 cases) than the short side (+0.0016, t 0.49, 1468 cases), but both are positive. The result is too small for six coins to show clearly, rather than present on one side only. More coins are available on daily bars in the same folds.
