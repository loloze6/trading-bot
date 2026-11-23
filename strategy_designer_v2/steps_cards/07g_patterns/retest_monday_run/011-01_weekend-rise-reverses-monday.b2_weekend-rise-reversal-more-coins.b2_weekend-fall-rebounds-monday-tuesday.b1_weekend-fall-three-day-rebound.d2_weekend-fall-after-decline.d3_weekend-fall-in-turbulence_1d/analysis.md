---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5124 USD
---
## Findings
- **F1:** On Sunday bars, the Sunday return predicts the next 3 days in the opposite direction, with a coefficient of -1.90 % excess 3-day return per standard deviation of Sunday return (t -4.96, about 830 weekly cases). Across all days on the 3-day grid the same reversal is only -0.41 % per standard deviation (t -2.03, 2288 cases), so weekend moves reverse several times more than weekday moves.
- **F2:** The Sunday reversal is graded both ways: the bottom Sunday-return quintile is followed by +1.49 % excess over 3 days (t 1.97) and the top quintile by -1.29 % (t -1.81). The tested idea kept only the long side and weighted it by the volatility ratio, and the volatility-ratio quintiles on the 3-day grid show no ordered pattern (-0.51 %, -0.18 %, +0.03 %, +0.98 %, +0.07 %; regression slope t 1.36).
- **F3:** The Sunday reversal weakens as weekend volume rises against the coin's 20-day volume. The interaction of Sunday return with weekend volume surprise is +0.95 % per standard deviation squared (t 3.17), so low-volume weekends reverse most, as the brief's second prediction says.
- **F4:** A day's volume surprise (log volume minus its 20-day mean) predicts the next 3 days' excess return only on down days: +1.01 % per standard deviation (t 3.22, 969 cases) against +0.16 % on up days (t 0.55, 965 cases). It holds alongside the day's return in a joint regression (t 2.68) and at 1 day over 6006 bars (t 3.17). By year it is positive in 2023 (t 2.58) and 2024 (t 4.75) and negative in 2022 (t -1.58) and 2025 (t -1.03).
- **F5:** A weekday pattern stands out beyond the 7 weekdays looked at. Wednesday's daily return averages +0.48 % excess (t 2.56) and Thursday's -0.52 % (t -2.98), a Welch difference with t 3.90. It has the same sign in all 8 coins and in 2023 to 2025, but it is ungraded and does not hold in 2022.
- **F6:** The trades in the lowest entry-forecast quartile (mean forecast 3.4) earned +0.14 % net and were held 7.0 days on average. The other three quartiles earned +2.8 % to +3.1 % net in 2.2 to 4.0 days, so the weakest signals carry most of the book's time in the market for almost no return.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence.g1_thin-weekend-moves-reverse-both-ways` (from F1, F2, F3): A coin's Sunday return (Saturday close to Sunday close) is reversed over the next 3 days, falls followed by rises and rises followed by falls, and the larger the Sunday move the larger the reversal. The reversal is larger the lower the weekend's volume stands against the coin's 20-day average volume.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d3_weekend-fall-in-turbulence.g2_high-volume-falls-rebound` (from F4): A coin that falls on a day of unusually high volume against its 20-day average volume rises over the next 3 days, and the higher that day's volume stands above its average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
