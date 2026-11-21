---
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea tested: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3454 USD
---
## Findings
- **F1:** The tested slope sits on the wrong side of zero but is tiny (OLS t −0.65 on 947 grid cases), and the forecast cannot grade the rise: 568 of 947 cases (60%) sit at the +20 cap, and excess return does not rise across forecast groups (+0.0128 at mean forecast 5.8, +0.0063 at 14.8, +0.0082 at 20.0).
- **F2:** Measured raw, without the standardisation, a more even rise does carry a little more continuation, but only because even rises are bigger. Across residual-share quintiles of all 2,865 three-day rises, the 72-hour excess return goes −0.0055, 0.0000, −0.0006, +0.0040, +0.0110 while the mean rise size goes 0.009, 0.028, 0.051, 0.076, 0.119. The residual's t of 1.12 falls to 0.55 once rise size is controlled.
- **F3:** The size of the 3-day rise, not its shape, carries the continuation. Rise size predicts the next 72-hour excess return with t 2.98 (n 2,865). Bars inside a rise beat bars outside it by 0.0087 against −0.0017 (Welch t 3.32). Inside the active bars, the forecast adds nothing once the past return is controlled (t −0.55).
- **F4:** The shape effect is not hidden at another horizon, one side or one subgroup. The forecast's t is −0.33 at 24 hours and −1.17 at 168 hours. Per-coin t runs from −1.25 to +0.88. Per-year t runs from −2.90 (2019) to +0.77. On falls, evenness gives t −0.62 at 72 hours.
- **F5:** Volume concentration points the brief's way only faintly. A rise whose volume sits in its 3 heaviest hours continues less (t −1.75 at 72 hours, −1.43 at 24 hours, n 2,865 and 8,529), which is short of clear.
- **F6:** Large 3-day falls rebound rather than continue. Fall size predicts continuation with t −3.60 over the next 72 hours (n 2,669) and t −11.72 over the next 24 hours (n 8,272). Once size is controlled, the fall's evenness adds nothing (t −0.16 at 72 hours).

## Ideas
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b1_three-day-rise-size-continues` (from F2, F3): The larger a coin's 3-day rise, the more the coin keeps rising over the next 3 days.
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b2_deep-three-day-falls-rebound` (from F6): The larger a coin's 3-day fall, the more the coin rebounds over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
