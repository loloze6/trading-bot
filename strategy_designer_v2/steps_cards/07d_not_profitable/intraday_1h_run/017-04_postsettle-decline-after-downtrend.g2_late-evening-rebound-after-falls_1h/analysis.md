---
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h
idea tested: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.1473 USD
---
## Findings
- **F1:** Before fees the book earns money, but fees take more than it gains: the 8,418 trades, all long, make +0.079% each gross (t 2.61) and −0.101% each net, against about 0.18% of fees per round trip. Summed over the bars, the position gained 1.97 against 3.42 of fees.
- **F2:** The fee loss is the same on every coin, so no coin carries the failure on its own: gross per trade runs from +0.041% (BTC) to +0.118% (XRP), and net per trade from −0.139% (BTC) to −0.062% (XRP).
- **F3:** The book holds every trade for exactly 2 hours, entering at the 20:00 bar's close and leaving at the 22:00 bar's close. That means each day pays one full round of fees for a single 2-hour move. The average absolute move over those 2 hours is 0.71%, of which the forecast's edge is only a small part.
- **F4:** The rebound grows steadily with the depth of the fall. Across quintiles of the standardised 3-day fall, the 2-hour return from 21:00 rises from 0.034% to 0.058%, 0.081%, 0.112% and 0.164%. The baseline at that hour is 0.021%, and the top quintile's excess has t 4.31 over 1,702 cases.
- **F5:** Only the deepest falls come near covering the fee, and only when the position is held longer. In the top quintile the return from 21:00 reaches 0.190% after 4 hours (excess t 4.23), 0.212% after 12 hours (t 3.21) and 0.248% after 24 hours (t 1.95, with a 0.098% baseline). The lowest quintile reaches only 0.041% after 4 hours.
- **F6:** Measuring the fall by its raw size gives the same grading. By quintile of the raw 3-day return (mean −0.6% up to −11.4%), the 4-hour return from 21:00 rises from 0.060% to 0.163%, and the 12-hour return from 0.048% to 0.181%.

## Ideas
- `017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls.d1_deep-fall-late-evening-four-hour-rebound` (from F1, F3, F4, F5, F6): For a coin with a 3-day fall, the return over the 4 hours from 21:00 UTC is positive, and the deeper the 3-day fall, the larger that rise, rising most steeply for the deepest falls. The rise is roughly five times larger after the deepest fifth of falls than after the shallowest.
- `017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls.d2_overnight-rebound-after-deep-falls` (from F1, F3, F5, F6): For a coin with a 3-day fall, the return over the 12 hours from 21:00 UTC is positive, and the deeper the 3-day fall, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
