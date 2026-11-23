---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move is followed by a move the same way over the next 24 hours. The continuation grows with the weekend's mean hourly volume against its mean over the five weekdays before, across all weekends including the lighter-than-usual ones.
Consequence: A weekend move made on relatively heavy volume is a reason to follow it through Monday, with more conviction the heavier the weekend was against its week.
Why:
- F1: Across all 2,446 weekends, not only those the idea's gate kept, the next 48 hours follow the weekend move more the heavier the weekend's volume against the five weekdays before it. By quartile of that volume ratio, the mean move in the weekend's direction beyond drift is −0.14 % (t −0.71), +0.30 % (t 1.37), +0.61 % (t 2.51) and +1.25 % (t 3.98), about 611 cases each. The top quartile already starts at a ratio of 0.83, so the tested gate of ratio above 1 discarded weekends that still carry the effect.
- F3: Most of the continuation comes in the first 24 hours (Monday UTC). In the top volume quartile, Monday gives +0.84 % (t 3.81) and Tuesday +0.40 % (t 1.55); in the third quartile, Monday gives +0.32 % (t 1.83) and Tuesday +0.29 % (t 1.48); 611–612 cases each.
- F5: The volume-graded weekend continuation shows up in every coin. Above the median volume ratio, the 48-hour directional excess is +0.49 % for BTC (t 1.27, 200 cases), +0.81 % for ETH (t 2.03), +0.85 % for LTC (t 1.92), +0.94 % for XMR (t 2.06), +1.10 % for XRP (t 2.22) and +1.00 % for ZEC (t 1.81).
- F6: Saturday's direction alone and Sunday's direction alone each predict the next 48 hours with the same volume gradient. The top quartile gives +1.01 % (t 3.18) for Saturday and +0.99 % (t 3.04) for Sunday; the bottom quartile gives +0.02 % and −0.18 %.
