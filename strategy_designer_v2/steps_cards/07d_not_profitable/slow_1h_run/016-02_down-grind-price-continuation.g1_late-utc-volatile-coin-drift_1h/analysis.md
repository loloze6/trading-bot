---
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
idea tested: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2893 USD
---
## Findings
- **F1:** Fees, not the forecast, sink the book: summed over all coins and windows, the position's gains before costs come to 7.77 while fees come to 18.24, about 0.00044 against 0.00104 per coin-day. That leaves a mean daily book return of -0.000596 (sd 0.0067), which is where the failing Sharpe of -2.1 comes from.
- **F2:** The slot effect itself is real but too small for its cost. The return from the 21:00 to the 23:00 close averages 0.101 % (t 9.07, 16,256 independent days), and every coin is positive with t between 3.1 and 4.7. Yet the fee per unit of turnover is 0.075 % to 0.125 %, so a daily in-and-out round trip costs 0.15 % to 0.25 % of the position, more than the 0.10 % it earns.
- **F3:** Holding longer does not grow the gain to pay the fee. The mean return from the 21:00 close is 0.108 % over 4 hours (t 6.6), falls to 0.038 % over 8 hours (t 1.8) and is 0.118 % over 24 hours (t 3.1), so nearly all of the drift sits in the first 2 to 4 hours.
- **F4:** The slot gain is concentrated in the most volatile week. In the top quintile of raw 7-day hourly volatility (mean 1.70 % per hour) the 2-hour slot return is 0.250 %, against 0.04 % to 0.10 % in the four lower quintiles. The book's sizing by standardised volatility spreads its position much more evenly: mean position 0.33 in the lowest forecast quintile against 0.65 in the highest.
- **F5:** The slot gain is largest after a fall. When the coin's 24-hour return into 21:00 is in its lowest quintile (mean -5.95 %), the slot return is 0.229 %, against 0.071 % to 0.074 % in the middle quintiles. The lowest quintile of the 7-day return (mean -15.3 %) also gives 0.132 %, against 0.076 % in the middle.
- **F6:** The slot drift is not steady across years: the mean slot return is -0.043 % in 2022 and 0.038 % in 2023, against 0.10 % to 0.20 % in the other years.

## Ideas
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls` (from F1, F2, F4, F5): Each coin rises over the two hours from 21:00 to 23:00 UTC, and the higher its hourly volatility over the past 7 days, the larger that rise, the more so the further the coin fell over the past 24 hours.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops` (from F2, F3, F5): Each coin rises over the two hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
