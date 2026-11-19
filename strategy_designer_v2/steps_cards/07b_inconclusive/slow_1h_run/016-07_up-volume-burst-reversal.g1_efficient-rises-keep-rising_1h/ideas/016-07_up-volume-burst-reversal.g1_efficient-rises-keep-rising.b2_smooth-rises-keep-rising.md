---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
line: 7.b inconclusive
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its hourly movement over those 3 days that went in the direction of the rise (net 3-day move over the sum of absolute hourly moves), the more it rises over the next 5 days.
Consequence: A rise built from steady, one-directional hours is a reason to stay long for about five days, and a rise of choppy hours is a reason not to join it.
Why:
- F1: The test's forecast standardises the efficiency ratio against its own past 72 hourly values, and this standardisation is what loses the effect. Among 2139 non-overlapping 3-day rises, the 72-hour excess return regressed on the raw ratio has slope t 2.49, on the standardised ratio only t 0.60, and the two correlate at just 0.31.
- F2: Measured in the idea's own terms (the raw share of hourly movement in the rise's direction), the effect is on the predicted side and graded. Mean excess 72-hour return across raw-ratio quintiles of rises runs -0.0033, -0.0037, +0.0030, +0.0069, +0.0092 (about 443 cases each), with slope t 2.71 on 2217 cases.
- F4: The effect grows with the horizon. The forecast's slope t is -0.41 at 24 hours, 1.19 at 72 hours and 1.23 at 120 hours. The raw ratio's slope t is 0.67, 2.71 and 3.03 at the same horizons. A 5-day horizon shows it more clearly than the plan's 3 days.
