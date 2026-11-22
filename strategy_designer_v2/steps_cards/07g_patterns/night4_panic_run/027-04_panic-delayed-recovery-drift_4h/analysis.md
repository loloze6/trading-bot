---
line: 7.g patterns
backtest: 027-04_panic-delayed-recovery-drift_4h
idea tested: 027-04_panic-delayed-recovery-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3809 USD
---
## Findings
- **F1:** The panic premium is real but short and immediate. In each coin's bottom fifth of 24-hour returns measured in usual 24-hour moves (median -1.13), the next day's unusual move averages +0.094 of a usual move (t 4.91, 3268 non-overlapping cases), and the next 3 days' averages +0.070 (t 2.26). By 7 days it is gone (-0.041, t -0.91), and by 14 days it is negative (-0.079, t -1.35).
- **F2:** The bounce follows the size of the fall. Next-day strength across 24-hour-return fifths, from largest fall to largest rise, is +0.094, +0.010, -0.033, -0.038, -0.047; the last is t -2.56, so large 24-hour rises are followed by a below-usual next day.
- **F3:** Inside the half of bars whose 24-hour range is above the coin's median multiple of its 30-day mean, the bottom fifth of 24-hour returns (median -1.61 usual moves) is followed by +0.122 next day (t 4.28, 1692 cases) and +0.113 over 3 days (t 2.66), larger than without the range condition.
- **F4:** A wide 24-hour range alone predicts a rise over the next 3 days. The top fifth of range multiples (median 1.73 times the 30-day mean) is followed by +0.159 of a usual 3-day move (t 4.80) and +0.059 next day (t 2.86); the other four fifths are all at or below 0 at 3 days (-0.062 to -0.033).
- **F5:** The tested forecast arrives after the bounce. On bars where it is active, the next 3 days average -0.040 of a usual move (t -2.22, 2839 cases) and the next 14 days -0.070 (t -1.39, 504). Raw panic readings, sorted into fifths among non-zero values, show no rising pattern at 14 days (-0.125, +0.009, +0.027, -0.225, -0.070).
- **F6:** The book is almost entirely the coin's own move. Its daily-return deciles match the coin's day by day (worst decile -7.53 % against the coin's -7.56 %; best +8.44 % against +8.20 %). Its mean by coin sits within 0.06 % a day of holding (BTC 0.166 % against 0.118 %).
- **F7:** The 7-day return shows 14-day momentum. Its top fifth (median +14.9 %) is followed by +0.190 of a usual 14-day move (t 2.20, 214 cases). Its bottom fifth (median -13.1 %) is followed by -0.199 (t -3.11, 230 cases), a 6.4 % gap in unusual 14-day return between the two.
- **F8:** Calendar effects are large. The 4-hour bar opening at 16:00 UTC returns +0.077 % above usual (t 5.15) and the one opening at 20:00 UTC -0.071 % (t -4.62), both with about 17500 bars. Fridays return +0.079 % per bar above usual (t 4.83).

## Ideas
- `027-04_panic-delayed-recovery-drift.g1_immediate-bounce-after-sharp-falls` (from F1, F2, F5): The further a coin's 24-hour return falls below zero, measured in its usual 24-hour moves, the more the coin rises above its normal drift over the next 1 to 3 days.
- `027-04_panic-delayed-recovery-drift.g2_wide-range-fall-quick-rebound` (from F3, F1): The further a coin's 24-hour fall goes, in usual 24-hour moves, while its 24-hour range is wide against its 30-day mean range, the more the coin rises above its normal drift over the next 1 to 3 days. Within that wide-range situation, the larger the fall, the larger the rise.
- `027-04_panic-delayed-recovery-drift.g3_wide-range-precedes-rise` (from F4): The larger a coin's 24-hour range is as a multiple of its 30-day mean 24-hour range, the more the coin rises above its normal drift over the next 3 days.
- `027-04_panic-delayed-recovery-drift.g4_weekly-momentum-two-weeks` (from F7): The larger a coin's 7-day return, the higher its return above its normal drift over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
