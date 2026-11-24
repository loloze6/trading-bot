---
line: 7.g patterns
backtest: 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d
idea tested: 031-01.b1.b2.b1_wide-day-strong-run-more-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6629 USD
---
## Findings
- **F1:** When a coin's 20-day return is negative, the deeper that fall measured in units of its 20-day volatility, the more the coin beats its drift over the next 3 days: the slope of the excess return (in usual moves) on the fall's depth is -0.132 (t -2.23, 5085 non-overlapping cases on 702 days), and at 7 days it is -0.143 (t -2.01, 2162 cases on 299 days). After 20-day rises the slope is +0.051 (t 1.60), a different shape.
- **F2:** The rebound after deeper 20-day falls holds across most years. At 3 days the depth slope is positive in 6 of 8 years: 2019 and 2021–2025, from 0.084 to 0.263, and 2025 alone has t 2.69. At 7 days, leaving out 2022, the slope is 0.163 (t 2.01, 1793 cases on 253 days).
- **F3:** The book earns from long holds and loses on short ones:
- **F4:** Coins whose 5-day return has stayed positive for more than 10 days running beat their drift by:
- **F5:** The tested idea's move is smaller than a trade's cost.
- **F6:** The brief's "wide day that closes flat" shows no edge of its own.

## Ideas
- `031-01.b1.b2.b1.g1_volatility-scaled-20-day-fall-rebound` (from F1, F2): The deeper a coin's 20-day fall, measured against its own daily volatility over those 20 days, the more the coin rises above its usual drift over the next 3 to 7 days.
- `031-01.b1.b2.b1.g2_persistent-rise-keeps-rising` (from F3, F4): The longer a coin's 5-day return has stayed positive day after day, the more the coin rises above its usual drift over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
