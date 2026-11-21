---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.6008 USD
---
## Findings
- **F1:** Narrow two-day ranges come before weaker, not larger, moves over the next 3 days. On the 18-bar grid, the narrowest fifth of two-day ranges (measured against the coin's own 30-day median) ends -0.90 % below drift (t -5.0, 2189 cases). Its mean absolute move is 0.66 of a usual move, against 0.76 for the widest fifth. In coins whose 30-day return is negative, the narrowest fifth gives -1.08 % (t -3.9, 915 cases). The pattern holds in both halves of the windows (early -0.47 % with t -1.9, late -0.85 % with t -2.9), and 17 of 19 coins have a negative mean.
- **F2:** In coins whose 30-day return is negative, a 4h close below the prior two-day low falls further when the range it breaks was narrow, and the effect is graded across range quintiles. Over 3 days the quintiles run from -1.35 % (t -4.5, 648 cases) for the narrowest to +1.25 % for the widest. Over 6 days the narrowest quintile falls -2.57 % below drift (t -5.3, 556 cases), strength -0.17, total move -1.53 %, about 7 times the 0.22 % round trip. It is negative in both halves (early -0.80 %, t -1.7; late -1.86 %, t -4.3), and 18 of 19 coins have a negative mean.
- **F3:** Breaks below the two-day low out of a wide range rebound instead, and more so the wider the range. In rising coins (30-day return positive), the quintiles of range width run from -0.38 % for the narrowest to +1.99 % for the widest over 3 days (widest t 3.8, 423 cases, strength 0.22). The widest quintile is positive in both halves (+1.46 %, t 2.0; +2.53 %, t 3.4), and 15 of 19 coins have a positive mean.
- **F4:** The sharpest one-day falls are followed by a 3-day rebound, and only the extreme decile stands out. The bottom decile of one-day return (scaled by volatility) gains +1.48 % over drift (t 5.8, 1156 cases, strength 0.16, total +2.00 %), while deciles 2 to 9 sit between -0.6 % and -0.2 %. In rising coins this bottom-fifth rebound holds in both halves (+1.02 %, t 2.7; +2.06 %, t 3.7). Over all regimes, 15 of 19 coins have a positive mean.
- **F5:** The tested upward breakout in rising coins keeps paying beyond its 3-day horizon. Over 6 days it gains +1.58 % over drift (t 5.0, 2807 cases, strength 0.11), against +0.58 % at 3 days and +0.17 % at 1 day. It holds in both halves (+1.89 %, t 3.8; +1.26 %, t 3.3), and 16 of 19 coins are positive. In line with this, the book's trades lasting 4.5 to 12.5 days earn +10.0 % to +10.9 % net, against -1.5 % for trades closed at about 3 days.
- **F6:** The weekday pattern of the breakouts is not stable, so it is not counted as a finding to build on. Sunday breakouts end -1.24 % (t -2.8), but that comes from -2.81 % in the late half against +0.16 % in the early half. Monday also flips sign between halves (+1.00 % to -1.39 %).

## Ideas
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins.g1_quiet-breakdowns-in-falling-coins` (from F1, F2): When a coin whose 30-day return is negative closes a four-hour bar below the lowest low of its preceding two days, it falls over the next six days, and the narrower that two-day range was compared with the coin's usual two-day range over the past 30 days, the larger the fall.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins.g2_wide-range-breakdown-rebound` (from F3, F1): When a coin whose 30-day return is positive closes a four-hour bar below the lowest low of its preceding two days, it rises over the next three days, and the wider that two-day range was compared with the coin's usual two-day range over the past 30 days, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins.g3_deep-one-day-fall-rebound` (from F4, F3): When a coin's one-day return is a sharp fall compared with its usual daily move, the coin rises over the next three days, and the deeper that fall, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins.g4_rising-breakouts-over-six-days` (from F5): When a four-hour bar closes above the highest high of a coin's preceding two days while its 30-day return is positive, the coin rises over the next six days, and the further the close clears that high, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
