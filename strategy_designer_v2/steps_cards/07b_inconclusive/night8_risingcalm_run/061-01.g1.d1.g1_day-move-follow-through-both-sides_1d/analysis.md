---
line: 7.b inconclusive
backtest: 061-01.g1.d1.g1_day-move-follow-through-both-sides_1d
idea tested: 061-01.g1.d1.g1_day-move-follow-through-both-sides
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3406 USD
---
## Findings
- **F1:** The effect lives in calm markets only. On the plan's 5-day grid (folds B, C), the slope of the excess 5-day return on the forecast is +0.00151 with t 4.53 over 712 calm cases, and the top fifth's signed excess is +3.65 % (t 3.76). In agitated markets the slope is +0.00024 (t 0.51, 710 cases) and the top fifth is −0.81 % (t −0.81), so the pooled test averages a real calm effect with an agitated one that is absent.
- **F2:** Inside calm markets the effect grows with the size of the day, and in agitated markets it does not. On 5-day returns over all five grid offsets, the mean signed excess by quintile of |forecast| is +0.53 %, +0.39 %, +0.27 %, +0.79 % and +1.10 % in calm markets (about 700 cases each). In agitated markets it runs +0.52 %, −0.22 %, −1.28 %, +0.25 % and −0.29 % with no order.
- **F3:** The calm effect holds on both sides and in every trend. In calm markets the top-fifth signed excess is +5.36 % (t 2.98) after up days and +2.88 % (t 2.96) after down days. The calm slope t is 2.27 in falling markets (160 cases), 2.59 in choppy (99) and 2.51 in rising (182). In the agitated part the slope t is 1.13 falling and 0.28 rising, and the top fifth is −1.24 % after down days.
- **F4:** The calm effect is less sure than F1 suggests, because the single 5-day grid overstates it. Averaged over the five grid offsets, the calm slope t is 1.68 (from −2.04 to 4.52, positive on 80 % of offsets) against −0.36 in agitated markets. Calm offset-averaged t by window is positive in 6 of 10 readable windows but mostly under 1.2.
- **F5:** The calm continuation is as clear or clearer over 7 days as over 5. The calm offset-averaged slope t is 1.78 at 7 days, positive on 86 % of offsets with a lowest t of −0.07, against 1.68 at 5 days. Agitated markets show 0.06 at 7 days. Over shorter horizons the relation turns negative: at 1 day the slope t is −4.49, driven by agitated markets (−4.91 against −1.66 calm).
- **F6:** Pooled over all profiles, the effect is too small to pay. The verdict's unusual move is +0.22 % per case (t 0.76 over 1177 days, strength 0.018) against a cost of 0.19 % per trade. The main measure turns negative on the check folds A and D (−8.5e-05 against +3.49e-04 overall), which is consistent with an effect diluted by agitated markets that carry none.

## Ideas
- `061-01.g1.d1.g1.b1_calm-big-day-follow-through` (from F1, F2, F3, F6): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further the coin keeps moving the same way over the next 5 days, upward after up days and downward after down days.
- `061-01.g1.d1.g1.b2_calm-big-day-seven-day-follow` (from F1, F4, F5): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further the coin keeps moving the same way over the next 7 days, upward after up days and downward after down days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
