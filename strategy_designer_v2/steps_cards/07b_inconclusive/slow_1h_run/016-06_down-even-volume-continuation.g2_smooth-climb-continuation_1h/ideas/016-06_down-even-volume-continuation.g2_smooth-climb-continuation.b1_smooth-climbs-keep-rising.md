---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves over those 3 days that points up, the more it keeps rising over the next 3 days. The extra rise is largest for the smoothest climbs.
Consequence: A trader should hold a 3-day climb in proportion to how smooth it has been, keeping a position mainly through the smoothest climbs and stepping aside from choppy ones.
Why:
- F1: On the plan's own grid of 72-hour climbs (n=2865 independent cases), the raw 3-day share of hourly movement pointing up predicts the next 3 days' excess return with slope 0.055 and t=3.21. The recorded forecast, which standardises that share against its own past 72 hourly values, reaches only t=1.41 (the verdict's t is 1.25). The two correlate at 0.72, and in a joint regression the raw share keeps t=3.16 while the standardised forecast falls to t=-1.31. The test's transform diluted an effect that the raw share shows clearly.
- F2: The effect is graded and strongest at the top. Mean next-3-day excess return rises steadily across raw-share quintiles of climbs: -0.0051, -0.0022, -0.0010, +0.0020, +0.0116. The smoothest fifth beats the rest by 0.0132 (Welch t=3.00, 573 vs 2292 cases).
- F4: The effect shows at the idea's own 3-day horizon and not at nearby ones. The raw-share slope among climbs has t=0.78 over 1 day and t=0.95 over 7 days, against t=3.21 over 3 days.
- F5: Climbing alone adds nothing: all climb cases together have mean excess return 0.00105 (t=0.66, n=2865). Size of the rise does not carry the effect either: with the rise as a second regressor, the share keeps slope 0.042 (t=1.79) while the rise's own t is 0.81. Uneven volume adds nothing (slope t=-1.36).
