---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.b inconclusive
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls sharply over one day on volume above its own 30-day average daily volume, it rebounds over the next 3 days. The larger the fall in units of its 20-day volatility and the heavier the volume against that average, the larger the rebound.
Consequence: A heavy-volume selloff day in a coin is a reason to expect a short-term bounce rather than continuation, and so a reason to refuse a short taken on that day.
Why:
- F5: The clear volume-dependent effect in this data is on the other side, and opposite to the brief. After falls on above-average volume, the larger the fall times log volume ratio, the higher the next return. Rank correlation is 0.098 (p 0.000002, n 2376) over 1 day and 0.138 (p 0.0002, n 741) over 3 days. Large heavy-volume down days are followed by +0.0065 next-day excess (t 2.71, n 638), while large thin-volume down days show -0.0004 (t -0.12, n 168).
- F4: At 1 day the active bars do give back: mean next-day excess -0.0020, t -3.29, n 5482. This is a general fade of ordinary up days, not a thin-volume or large-rise effect. Small thin up days show -0.0018 (t -2.80, n 3975) and small heavy up days -0.0017 (t -1.39). Large thin up days, the idea's core case, show +0.0005 (t 0.12, n 176).
