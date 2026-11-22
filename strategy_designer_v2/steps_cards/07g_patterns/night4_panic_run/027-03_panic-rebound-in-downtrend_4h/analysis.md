---
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend_4h
idea tested: 027-03_panic-rebound-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4161 USD
---
## Findings
- **F1:** Over the next 24 hours, a coin's return rises with the depth of its past 24-hour fall measured in units of its usual 24-hour move. On non-overlapping 24-hour cells (15 793 cases), the deepest fall quintile (median −1.56 units) is followed by +0.49 % above the coin's mean (t 5.13, 3 159 cases) and the largest rise quintile by −0.21 % (t −2.26). Within falls the effect is graded: +0.60 % (t 4.12), then +0.40 % (t 3.10), then about 0 for the three milder quintiles (1 541 cases each).
- **F2:** The 24-hour rebound after deep falls holds in every coin and every year. By coin it is +0.22 % to +0.64 % (t 1.27 to 2.74, about 500 to 550 cases each). By year it is +0.19 % to +1.17 % for 2018 to 2025, with 365 to 479 cases a year. This is 1.0 to 6.2 times the 0.19 % cost of a trade.
- **F3:** Range expansion carries the 24-hour reversal on both sides. A deep fall with the 6-bar range in its top tercile against its 30-day average is followed over 24 hours by +0.78 % (t 5.70, 1 811 cases). The same fall in the bottom range tercile is followed by −0.47 % (t −1.89, 350 cases). A large rise in the top range tercile is followed by −0.42 % (t −2.85, 1 647 cases).
- **F4:** In the strategy's panic events, the premium shows within days and fades by the tested 14-day horizon. These events (range at least 3× its 30-day average with a fall, any prior trend, first per 14-day cell, 124 events) are followed by +2.75 % over 24 hours (t 3.73) and +4.38 % over 3 days (t 3.03). Over 14 days the unusual move has a t of only 1.18 for all 124 events and 2.11 for the 45 with a negative prior 30-day return. The step-5 verdict on 40 cases was t 0.99.
- **F5:** Inside panics, the 14-day move is not graded by depth of fall. The deepest-fall tercile (median −7.3 units) is followed by −2.58 % (t −1.32, 42 events) and the mildest by +3.74 % (t 0.56, 42 events). The tested idea's supporting check passed with a difference of 0, so the "more extreme, more premium" part has no support at 14 days.
- **F6:** Over 3 days (18-bar cells, 5 004 cases), the 24-hour fall still predicts: its deepest quintile is followed by +1.06 % (t 3.97). The 3-day fall does not predict (deepest quintile +0.20 %, t 0.77). The reversal therefore belongs to the 24-hour move, not the longer one.
- **F7:** The book held 14 days and traded 0.0042 times a day, so it sat through the drift after the rebound rather than capturing it. Its Sharpe was 0.15, against holding's Sharpe higher by 0.40, and its mean daily return was 0.006 %.
- **F8:** Clock effects are smaller than the cost of a trade.

## Ideas
- `027-03_panic-rebound-in-downtrend.g1_one-day-wide-range-fall-rebound` (from F1, F2, F3, F6): A coin's 24-hour fall, measured against its usual 24-hour move, is followed by a rise over the next 24 hours. The rise is larger the deeper the fall and the wider the coin's bar ranges over those 24 hours relative to their 30-day average.
- `027-03_panic-rebound-in-downtrend.g2_panic-premium-within-three-days` (from F4, F3, F5, F7): After a panic, a 24-hour stretch whose bar ranges are several times their 30-day average while the price falls, the coin rises over the next 3 days. The rise is larger the larger the range expansion of the stretch.
- `027-03_panic-rebound-in-downtrend.g3_one-day-wide-range-rally-fade` (from F1, F3): A coin's 24-hour rise, measured against its usual 24-hour move, is followed by a fall over the next 24 hours. The fall is larger the wider the coin's bar ranges over those 24 hours relative to their 30-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
