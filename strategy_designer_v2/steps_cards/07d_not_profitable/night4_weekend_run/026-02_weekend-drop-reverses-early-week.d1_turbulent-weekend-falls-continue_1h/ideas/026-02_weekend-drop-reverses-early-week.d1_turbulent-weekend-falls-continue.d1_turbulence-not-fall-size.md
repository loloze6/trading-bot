---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls over the weekend (Saturday 00:00 to Monday 00:00 UTC), it keeps falling over Monday and Tuesday. The fall grows with how much more volatile the weekend's hours were than the coin's previous week, not with how far the coin fell over the weekend.
Consequence: A trader leaning short after a weekend fall should size by the weekend's turbulence against the prior week, and lean least on the deepest weekend falls, which tend to bounce.
Why:
- F2: The forecast's grading does not work. Across the five |forecast| quintiles of the 804 short cases, the short excess move runs +0.58 %, +0.53 %, −0.06 %, +0.05 %, +0.44 %, with no rise from bottom to top. Meanwhile the position grows from −0.02 to −0.76 of the book (correlation of forecast with allocation 0.87). The plan's own check of upper minus lower half was −0.00106.
- F3: The size of the weekend fall points the wrong way, so scaling by it puts the largest bets on the cases that reverse.
- F4: The weekend's volatility against the prior week is what carries the continuation.
