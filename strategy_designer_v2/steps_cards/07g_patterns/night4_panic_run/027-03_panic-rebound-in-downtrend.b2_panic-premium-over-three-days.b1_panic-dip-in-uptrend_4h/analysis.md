---
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h
idea tested: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4248 USD
---
## Findings
- **F1:** Over 3 days, a 24h fall on wide bars is followed by an excess return that grows with how wide the bars are against their 30-day mean. On the 18-bar grid, falls whose 24h bar range is 1.5 to 2 times its 30-day mean returned +2.1 % above the coin's drift (t 2.48, n 156). At 2 to 3 times it was +3.4 % (t 3.45, n 58). Below 1 times it was −0.5 % to −0.1 % (t −1.24 and −0.35). The plan's own 3x-and-above level gave only +1.1 % (t 1.09, n 34). Rises on the same widths showed nothing (all |t| < 1.7).
- **F2:** The fall's depth matters only once the bars are wide. With bars over 1.5 times their usual width, a 24h fall of 1 to 2 usual 24h moves returned +4.7 % over 3 days (t 3.51, n 60), and a fall beyond 2 usual moves returned +2.4 % (t 3.40, n 134). The same falls on bars of normal width returned +0.4 % (t 0.80, n 239) and +0.3 % (t 0.30, n 16). Shallow falls under 1 usual move returned −0.7 % (t −0.50).
- **F3:** The rebound after a panic comes almost entirely from coins that were rising beforehand.
- **F4:** The wide-bar fall effect sits in the smaller coins and is uneven across years.
- **F5:** The 4h bar from 20:00 to 24:00 UTC returns more than the coin's mean 4h return, consistently across coins and years.
- **F6:** The 4h bar from 00:00 to 04:00 UTC returns less than the coin's mean.
- **F7:** The tested book's problem is too few trades, not the size of the move.

## Ideas
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g1_wide-range-falls-rebound` (from F1, F2, F7): A 24-hour fall in which the coin's bars are wider than their 30-day average is followed by higher than usual returns over the next 3 days. The wider the bars against their 30-day average, the higher the return, already from moderately widened ranges, well below several times the usual size.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g2_wide-range-dip-in-uptrend` (from F3, F1, F4): Among 24-hour falls on unusually wide bars, the higher the coin's 30-day return before the fall, the higher its return over the next 3 days. Falls that interrupt a 30-day rise give the largest rebound.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g3_late-utc-evening-bid` (from F5): Over the 4 hours from 20:00 to 24:00 UTC, the coin returns more than its usual 4-hour return. The larger the coin's 24-hour move up to 20:00 UTC, in either direction, the larger that excess.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend.g4_post-midnight-utc-weakness` (from F6): Over the 4 hours from 00:00 to 04:00 UTC, the coin returns less than its usual 4-hour return. The larger the coin's absolute 24-hour return up to midnight UTC, the larger that shortfall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
