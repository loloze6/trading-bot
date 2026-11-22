---
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
idea tested: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3831 USD
---
## Findings
- **F1:** The idea's premium is paid within the first day and is gone by a week: after a broad panic (24-hour fall of at least 1 usual move while the 24-hour mean bar range is at least 1.5 times its 30-day mean), the mean excess return is +1.18 % over 1 day (t 7.21, 1798 cases, strength 0.233), +1.41 % over 3 days (t 4.63, 1206 cases, strength 0.155), +0.27 % over 7 days (t 0.52, 879 cases, strength 0.003) and +0.31 % over 14 days (t 0.37, 645 cases).
- **F2:** The book holds long well beyond that horizon. Positions sat on 16372 bars across the coins against only 480 panic bars; for ETH that is 4270 against 92. Of 249 trades, 46 lasted over 30 days (mean +27.0 %, worst -61.2 %), and the mean trade duration was 334 hours against a 3-day (72-hour) idea. Most of its exposure, and its deepest trade losses, come from holding after the premium is paid, which drives the Calmar of 0.34.
- **F3:** The book is far too small and too rare to reach the required mean daily return (6.9e-05 against 5e-04). Panics as the plan defines them occur on only 60 to 102 bars per coin in about 17500. When in, the allocation averages only 0.15 to 0.29, because the vol-target sizing (target 0.38) meets realised vols of 0.59 to 1.07 during panics. Per-window book returns are mostly within ±3 % while the coins moved -50 % to +268 %.
- **F4:** A broader situation carries the effect with roughly ten times the cases: 1206 cases on the 3-day grid against the plan's 135. The excess grows with the range excess up to about 4 times: +0.88 % (t 2.64, n 939) at 1.5 to 2 times, +2.84 % (t 4.39, n 199) at 2 to 3 times and +6.51 % (t 2.11, n 45) at 3 to 4 times. Above 4 times it is only +0.91 % (t 0.73, n 23), which is why the plan's median split failed (-2.77 %).
- **F5:** For a given range excess, the premium is largest when the 24-hour fall is small relative to the range, not when it is deepest:
- **F6:** Each case's move easily covers a trade's cost (total move 4.07 % over 3 days, 21 times the 0.19 % cost; 1.32 % over 1 day, about 7 times). The book's shortfall therefore comes from how long it holds (F2) and how rarely and how small it trades (F3), not from fees.

## Ideas
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.d1_one-day-panic-premium-broad` (from F1, F2, F4, F6): A 24-hour stretch in which the coin falls while its range exceeds its 30-day average is followed by higher than usual returns over the next 1 day, and the further the range exceeds its 30-day average, the higher the return.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.d2_absorbed-panic-rebound` (from F5, F1, F3): When a coin's 24-hour range is several times its 30-day average, the smaller its 24-hour fall relative to that range, the higher its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
