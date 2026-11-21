---
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h bar closes below the lowest low of the preceding two-day stretch while the 30-day return is positive -> kept: a regime rule requires the close below the prior 12-bar low and a 180-bar return above 0.
- Comparison: the stretch's width against the 30-day average 4h range -> kept: the prior 12-bar high-low span divided by the mean bar range over 180 bars sizes the long.
- Outcome: the coin rises over the next three days, more after wider stretches -> kept: each bet is held 18 bars and is long only.
- Verdict transfer: yes: the test measures the idea's break, its momentum condition, its width scaling and its 3-day rise as stated.
Forecast: The regime detector checks two things at each bar's close. First, the close sits below the lowest low of the 12 prior bars (DistanceFromHighComponent: period 12, source "high", extreme "low", exclude_current 1, below 0). Second, the 180-bar return is positive (PriceEvolutionOnPeriodComponent, comparison_period 180, above 0). When both hold, the bar is in the active regime. Otherwise the forecast is 0 (flat). In the active regime the forecast is the stretch's width: RangeCompressionRatioComponent with short_period 12, long_period 180, exclude_current 2, form "width" and base "mean_bar_range". This is the prior 12-bar high-low span counted in average 4h bar ranges over 180 bars, standardised against its own past 180 values. It is always positive: about +10 for a stretch of usual width, up to +20 for one about twice as wide. The forecast is never negative, so the long is larger the wider the broken range was.
Config: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a bet (a rise of the forecast of at least 2 points), read once per 18-bar grid cell. For each case, take the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift (holding the coin over all windows). Then take the mean over all cases and its t.
- Supporting check: The Spearman correlation across cases between the forecast at the signal bar (the width) and that excess return is above 0.
- Confirm: The mean excess return is positive with t ≥ 2 over at least 30 independent cases, and the supporting correlation is above 0.
- Reject: The mean excess return is negative with t ≤ -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, a confirm-level t whose width correlation is not above 0, or fewer than 30 independent cases.
