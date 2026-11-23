---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move continues in its direction over the next 48 hours in proportion to how heavy the weekend's volume was against the five weekdays before. The weekend move's own size adds nothing beyond its direction.
Consequence: A trader following weekend moves should scale by the weekend's relative volume rather than by the move's size, and refuse light-volume weekends.
Why:
- F1: Across all 2,446 weekends, not only those the idea's gate kept, the next 48 hours follow the weekend move more the heavier the weekend's volume against the five weekdays before it. By quartile of that volume ratio, the mean move in the weekend's direction beyond drift is −0.14 % (t −0.71), +0.30 % (t 1.37), +0.61 % (t 2.51) and +1.25 % (t 3.98), about 611 cases each. The top quartile already starts at a ratio of 0.83, so the tested gate of ratio above 1 discarded weekends that still carry the effect.
- F2: The volume ratio grades the continuation, and the move's size does not. Regressing the 48-hour forward move (in usual moves) on the weekend's sign, sign × log(volume ratio) and the weekend's z gives sign × log ratio a coefficient of 0.234 (t 3.85) and the z a coefficient of −0.009 (t −0.31), over 2,446 weekends.
- F4: The effect belongs to weekends. Ordinary 48-hour blocks on the window grid, with the same "last 48 h volume over the prior 120 h" ratio, continue only +0.30 % (t 1.80) in their top volume quartile and −0.05 % (t −0.40) in their bottom quartile, over 2,853 cases each. That is about a quarter of the weekend's top-quartile +1.25 %.
