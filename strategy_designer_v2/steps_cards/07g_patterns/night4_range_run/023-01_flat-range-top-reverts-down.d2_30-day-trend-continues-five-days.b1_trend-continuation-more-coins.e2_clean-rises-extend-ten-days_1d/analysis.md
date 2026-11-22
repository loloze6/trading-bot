---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4564 USD
---
## Findings
- **F1:** In flat coins, where the 30-day net move covers less than half the 30-day high-low range, prices kept going the same way instead of reverting. Sorted by where the close sits in the 30-day range (1,595 non-overlapping 10-day cases), the 10-day excess over normal drift rose from the bottom up:
- **F2:** The coin's whole spread of 30-day moves points the same way. Sorted by the signed 30-day net-move-to-range ratio (268 cases per decile), the middle deciles 2 to 5 lost −2.2 %, −3.1 %, −1.0 % and −2.1 % over 10 days (t −2.5, −3.5, −1.2, −2.2). The top three deciles gained +1.7 %, +2.9 % and +3.0 % (top t 2.3). The overall rank correlation was +0.04.
- **F3:** Inside clean 30-day rises (ratio ≥ 0.5, 574 cases), the cases in the top tercile of 5-day return gained +6.5 % over 10 days beyond drift (t 2.89, 192 cases). The middle tercile gained −0.2 % and the bottom tercile +1.8 %. That top-tercile excess:
- **F4:** Clean 30-day falls (ratio ≤ −0.5) showed no grading. Their 10-day excess by tercile of 30-day return was +0.6 %, −1.1 % and −0.2 %, all with |t| < 1.1 over 170 cases each.
- **F5:** The book earns by avoiding the coins' bad days more than by catching their full gains.
- **F6:** Saturday's cross-coin mean daily return was +0.47 % (t 2.96, 414 days). It was positive in all 8 years, though no single year reached t 2. Friday was +0.43 % (t 2.05). Given how many angles I looked at, this is borderline, and weekday is not a graded situation.
- **F7:** The day after a coin's bottom-decile volatility-scaled drop, it rose +0.37 % (t 1.83 at the day level, 613 days). The bounce was strong in 2018–2021 (+0.65 % to +1.84 %, t up to 3.8) and about zero from 2022 to 2025. It fades and does not stand out.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days.g1_flat-range-position-persists` (from F1, F2): In a coin whose 30-day net move covers only a small share of its 30-day high-low range, the higher its close sits within that range, the more it rises beyond its normal drift over the next 10 days. The lower its close sits, the more it falls short of that drift.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days.g2_fresh-push-extends-clean-rises` (from F3, F5): In a coin whose 30-day rise covers a large share of its 30-day high-low range, the larger its 5-day return, the further it rises beyond its normal drift over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
