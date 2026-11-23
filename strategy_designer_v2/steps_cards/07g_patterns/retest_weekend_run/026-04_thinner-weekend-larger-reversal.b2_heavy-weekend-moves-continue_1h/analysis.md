---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.2629 USD
---
## Findings
- **F1:** Across all 2,446 weekends, not only those the idea's gate kept, the next 48 hours follow the weekend move more the heavier the weekend's volume against the five weekdays before it. By quartile of that volume ratio, the mean move in the weekend's direction beyond drift is −0.14 % (t −0.71), +0.30 % (t 1.37), +0.61 % (t 2.51) and +1.25 % (t 3.98), about 611 cases each. The top quartile already starts at a ratio of 0.83, so the tested gate of ratio above 1 discarded weekends that still carry the effect.
- **F2:** The volume ratio grades the continuation, and the move's size does not. Regressing the 48-hour forward move (in usual moves) on the weekend's sign, sign × log(volume ratio) and the weekend's z gives sign × log ratio a coefficient of 0.234 (t 3.85) and the z a coefficient of −0.009 (t −0.31), over 2,446 weekends.
- **F3:** Most of the continuation comes in the first 24 hours (Monday UTC). In the top volume quartile, Monday gives +0.84 % (t 3.81) and Tuesday +0.40 % (t 1.55); in the third quartile, Monday gives +0.32 % (t 1.83) and Tuesday +0.29 % (t 1.48); 611–612 cases each.
- **F4:** The effect belongs to weekends. Ordinary 48-hour blocks on the window grid, with the same "last 48 h volume over the prior 120 h" ratio, continue only +0.30 % (t 1.80) in their top volume quartile and −0.05 % (t −0.40) in their bottom quartile, over 2,853 cases each. That is about a quarter of the weekend's top-quartile +1.25 %.
- **F5:** The volume-graded weekend continuation shows up in every coin. Above the median volume ratio, the 48-hour directional excess is +0.49 % for BTC (t 1.27, 200 cases), +0.81 % for ETH (t 2.03), +0.85 % for LTC (t 1.92), +0.94 % for XMR (t 2.06), +1.10 % for XRP (t 2.22) and +1.00 % for ZEC (t 1.81).
- **F6:** Saturday's direction alone and Sunday's direction alone each predict the next 48 hours with the same volume gradient. The top quartile gives +1.01 % (t 3.18) for Saturday and +0.99 % (t 3.04) for Sunday; the bottom quartile gives +0.02 % and −0.18 %.
- **F7:** Patterns by hour and weekday do not stand out from chance once the number of tests is counted. The largest of 24 hourly means is hour 21 at +2.1 bp (t 2.94). The Monday and Tuesday hourly drifts have t 2.06 and t 2.94 out of 7 weekdays.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.g1_weekend-volume-graded-monday-follow-through` (from F1, F3, F5, F6): A coin's Saturday-Sunday move is followed by a move the same way over the next 24 hours. The continuation grows with the weekend's mean hourly volume against its mean over the five weekdays before, across all weekends including the lighter-than-usual ones.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.g2_weekend-relative-volume-grades-continuation` (from F1, F2, F4): A coin's Saturday-Sunday move continues in its direction over the next 48 hours in proportion to how heavy the weekend's volume was against the five weekdays before. The weekend move's own size adds nothing beyond its direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
