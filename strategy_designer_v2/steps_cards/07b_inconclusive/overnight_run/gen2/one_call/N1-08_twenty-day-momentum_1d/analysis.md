---
line: 7.b inconclusive
backtest: N1-08_twenty-day-momentum_1d
idea tested: N1-08_twenty-day-momentum
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2716 USD
---
## Findings
- **F1:** The forward 20-bar excess return is U-shaped across forecast fifths, not a straight line: the bottom fifth (mean forecast -14.9) has +0.040, the middle three fifths have -0.017, -0.026 and -0.020, and the top fifth (mean +17.6) has +0.023 (827 non-overlapping cases, about 165 per fifth). Both extremes beat the middle, so the linear slope cancels to t = 0.05.
- **F2:** The two sides pull in opposite directions. Long bars have a mean signed forward return of +0.027 (t = 1.67, n = 400). Short bars have -0.023 (t = -2.20, n = 427), so shorting after 20-day falls loses money, and the slope inside the short side is t = -2.65.
- **F3:** After the deepest falls (forecast ≤ -12) the next 20 bars rise: mean excess return is +0.030 (t = 1.75, n = 124). It is positive for all six coins (+0.010 to +0.057) and in 5 of 8 years (2020: +0.143, t = 4.1, n = 10). Against the cross-coin mean at the same bar it is -0.002 (t = -0.19), so the rebound is market-wide.
- **F4:** The market's common move drowns the coin-specific part. The cross-coin mean explains 47% of the variance of forward 20-bar returns. Relative to that mean, no forecast fifth differs from zero (t between -1.54 and +0.41).
- **F5:** Long forecasts when the close is above its 50-day average have a mean forward 20-bar return of +0.037 (t = 2.40, n = 221). Their excess over each coin's own mean is only +0.012 (t = 0.78), so most of the gain is the coins' upward drift and not added persistence. The same group lost in 2022 (-0.061, t = -2.34, n = 31).
- **F6:** The effect is unstable over time and noisy. The yearly slope t runs from -2.90 (2023) to +1.48 (2025), with 6 of 8 years negative. The top forecast fifth has nearly twice the dispersion of the others (forward sd 0.41 vs 0.21 to 0.25).

## Ideas
- `N1-08_twenty-day-momentum.b1_deep-fall-twenty-day-rebound` (from F1, F2, F3): After a coin's 20-day return falls deep into the bottom of its recent range, the coin's price rises over the next 20 daily bars by more than its usual 20-bar return.
- `N1-08_twenty-day-momentum.b2_long-momentum-in-uptrends` (from F2, F5, F6): When a coin closes above its 50-day average and its 20-day return is positive, its price rises over the next 20 daily bars.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
