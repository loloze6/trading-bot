---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
line: 7.b inconclusive
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves that points in the direction of the rise, the more it keeps rising over the next 3 days.
Consequence: A smooth, steady climb is a reason to stay long, and a choppy climb of the same size a reason to step aside.
Why:
- F1: On the plan's own grid of 72-hour climbs (n=2865 independent cases), the raw 3-day share of hourly movement pointing up predicts the next 3 days' excess return with slope 0.055 and t=3.21. The recorded forecast, which standardises that share against its own past 72 hourly values, reaches only t=1.41 (the verdict's t is 1.25). The two correlate at 0.72, and in a joint regression the raw share keeps t=3.16 while the standardised forecast falls to t=-1.31. The test's transform diluted an effect that the raw share shows clearly.
- F3: The direction holds broadly, but no single slice is strong on its own. The raw-share slope is positive in all 6 coins, from XMR (t=0.33) to ZEC (t=2.33), and in all 8 years, from 2022 (t=0.29) to 2024 (t=2.49). No coin or year is reversed, so the result is not concentrated in one place.
