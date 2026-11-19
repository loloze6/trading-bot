---
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
idea tested: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3174 USD
---
## Findings
- **F1:** On the plan's own grid of 72-hour climbs (n=2865 independent cases), the raw 3-day share of hourly movement pointing up predicts the next 3 days' excess return with slope 0.055 and t=3.21. The recorded forecast, which standardises that share against its own past 72 hourly values, reaches only t=1.41 (the verdict's t is 1.25). The two correlate at 0.72, and in a joint regression the raw share keeps t=3.16 while the standardised forecast falls to t=-1.31. The test's transform diluted an effect that the raw share shows clearly.
- **F2:** The effect is graded and strongest at the top. Mean next-3-day excess return rises steadily across raw-share quintiles of climbs: -0.0051, -0.0022, -0.0010, +0.0020, +0.0116. The smoothest fifth beats the rest by 0.0132 (Welch t=3.00, 573 vs 2292 cases).
- **F3:** The direction holds broadly, but no single slice is strong on its own. The raw-share slope is positive in all 6 coins, from XMR (t=0.33) to ZEC (t=2.33), and in all 8 years, from 2022 (t=0.29) to 2024 (t=2.49). No coin or year is reversed, so the result is not concentrated in one place.
- **F4:** The effect shows at the idea's own 3-day horizon and not at nearby ones. The raw-share slope among climbs has t=0.78 over 1 day and t=0.95 over 7 days, against t=3.21 over 3 days.
- **F5:** Climbing alone adds nothing: all climb cases together have mean excess return 0.00105 (t=0.66, n=2865). Size of the rise does not carry the effect either: with the rise as a second regressor, the share keeps slope 0.042 (t=1.79) while the rise's own t is 0.81. Uneven volume adds nothing (slope t=-1.36).
- **F6:** Because climbing alone adds nothing (F5) and the test sized positions on the diluted forecast (F1), the book lost money: Sharpe -0.50 and mean daily return -0.00034.

## Ideas
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.b1_smooth-climbs-keep-rising` (from F1, F2, F4, F5): When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves over those 3 days that points up, the more it keeps rising over the next 3 days. The extra rise is largest for the smoothest climbs.
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.b2_smooth-climb-more-coins` (from F1, F3): When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves that points in the direction of the rise, the more it keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
