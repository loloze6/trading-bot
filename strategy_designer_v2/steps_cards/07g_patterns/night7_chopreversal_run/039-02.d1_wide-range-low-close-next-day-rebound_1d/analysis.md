---
line: 7.g patterns
backtest: 039-02.d1_wide-range-low-close-next-day-rebound_1d
idea tested: 039-02.d1_wide-range-low-close-next-day-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3863 USD
---
## Findings
- **F1:** In agitated days, the day's own return over its 30-day swing explains the next day better than the close's place in the range: with both in one regression on standardised next-day returns, the fall's coefficient is +0.077 (t 2.98) and the wider-range coefficient +0.069 (t 2.60), while the close's place drops to -0.142 (t -1.41); in calm days the fall's t is only 0.98 and the range's 0.42.
- **F2:** In agitated days, the fall and the range compound: the lowest quintile of the day's return gives -0.11, +0.11 and +0.26 standardised next-day return across range terciles from narrow to wide, and the second quintile +0.02, +0.05 and +0.32; the product (fall x range) has t 2.38 in agitated days and 0.23 in calm days.
- **F3:** The agitated lowest-return quintile is followed by +0.184 standardised next-day return (582 cases, 242 days, day-summed t 1.96). The top quintiles show no matching fall (+0.077, -0.029, -0.115, -0.018), so the effect sits on the falling side.
- **F4:** The close's place matters only on agitated down days: the lowest close tercile is followed by +0.190 (469 cases, 215 days, t 2.08) against +0.089 and +0.096 for the higher terciles. On agitated up days the three close terciles are flat at -0.086, -0.073 and -0.084 (each t about -1.2), so the brief's high-close mirror is not in the bars.
- **F5:** The book's gain is carried by its lowest-close days: held days in the lowest close quintile earn +0.48 % a day (896 cases, t 4.68), the second +0.22 % (t 2.20), and the top two about 0 (-0.01 %, t -0.21 and -0.00 %, t -0.03). The gain is spread across all six coins (+0.11 % to +0.24 %).
- **F6:** The rebound does not last beyond the next day: over non-overlapping 3-day stretches, agitated close quintiles give +1.0 %, -0.5 %, +0.5 %, +0.7 % and +0.1 % (lowest close t 1.60, no grading). Over 2 days, the agitated lowest-return quintile gives +0.20 standardised (t 1.61).
- **F7:** Weekday differences fade once the cases of one day are taken together (all |t| < 1.3: Wednesday -0.094, t -1.22; Thursday +0.068, t 1.11), and their signs change between window halves, so they are not a finding.

## Ideas
- `039-02.d1.g2_down-day-low-close-next-day-rebound` (from F4, F5): In an agitated market, on a day the coin closes lower than it opened the day before, the lower it closes within its day's high-low range, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `039-02.d1.g1_wide-day-sharp-fall-rebound` (from F1, F2, F3, F6): In an agitated market, the larger a coin's one-day fall against its usual daily swing over the past 30 days, and the wider that day's range against its usual range over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
