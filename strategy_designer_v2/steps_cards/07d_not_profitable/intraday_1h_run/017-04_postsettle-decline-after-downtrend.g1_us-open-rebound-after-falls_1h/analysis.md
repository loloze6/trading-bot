---
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
idea tested: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2998 USD
---
## Findings
- **F1:** Fees, not the forecast, sink the book: per coin the summed gain before fees on the held positions is 0.46 to 0.88, while the summed fees are 1.31 to 1.70, and the fees sit almost entirely on the entry at 11:00 (7256 fee bars, mean 0.058%) and the exit at 13:00 (7368 fee bars, mean 0.058%); that is about 0.1% per daily round trip.
- **F2:** The 2-hour rise is too small to pay that round trip in most cases: the forecast quintiles 1 to 4 (forecast 1.8 to 13.9) give mean 2-hour returns of −0.04%, 0.02%, 0.05% and 0.07%, and only the top quintile (forecast 19.3) gives 0.23%, across 8432 cases with a raw t of 3.57.
- **F3:** The rise belongs to the deepest falls only: the deepest 3-day-fall quintile (mean fall −14.2%) gains 0.24% over the 2 hours, against 0.07%, 0.05%, 0.05% and −0.05% in the four shallower quintiles.
- **F4:** The 1-day fall sorts the cases at least as well: the quintile with the deepest 24-hour fall (−8.3%) gains 0.26% over the 2 hours, and the other four quintiles gain between −0.06% and 0.09%.
- **F5:** Nearly all the gain is in the 13:00 bar, not the 12:00 bar: summed gain before fees is 3.01 on positions held through the 13:00 bar against 0.77 through the 12:00 bar; in the top forecast quintile the 13:00 bar gives 0.19% of the 0.23%.
- **F6:** After the deepest 3-day falls the rise keeps building past 2 hours: the deepest quintile gains 0.52% over 12 hours and 0.25% over 24 hours from the 11:00 close, and over all cases the 12-hour return has a raw t of 2.48.

## Ideas
- `017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls.d1_us-open-rebound-after-double-fall` (from F1, F2, F3, F4): For a coin with a 3-day fall, the return over the 2 hours from 12:00 UTC is positive, and the deeper the 3-day fall, the larger that rise, only while the coin's 1-day return is also a fall, the rise growing with the depth of that 1-day fall.
- `017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls.d2_us-session-rebound-after-falls` (from F1, F3, F6): For a coin with a 3-day fall, the return over the 12 hours from 12:00 UTC is positive, and the deeper the 3-day fall, the larger that rise.
- `017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls.d3_post-open-hour-rebound-after-falls` (from F2, F5): For a coin with a 3-day fall, the return over the hour from 13:00 UTC is positive, and the deeper the 3-day fall, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
