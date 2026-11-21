---
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day return plus its closeness to its 90-day high -> kept: 28-bar return plus the distance of the close below its 90-bar closing high, each put on its own past scale and summed.
- Comparison: none -> kept
- Outcome: the higher that sum, the higher the coin's return over the next 10 days -> kept: 10 bars on daily bars, measured as a graded relation.
- Verdict transfer: yes: the forecast is the idea's own sum, graded and signed, and is judged against the 10-day returns that follow it.
Forecast: The forecast adds two terms and divides by 3 (three components at weight 1). - The first term is the 28-bar percent return, divided by its mean absolute size over the past 60 bars and multiplied by 10. - The second term is the percent distance of the close below its highest close of the last 90 bars, bar t included, which is 0 at the high and negative below it. It is standardised over 90 bars, which makes it about -10 at its usual depth, and a constant +10 is added to it. So it is positive when the close sits nearer its high than usual and negative when further below. - Forecast = (momentum + (distance + 10)) / 3. - It is positive when the 4-week rise and the nearness to the high together are stronger than usual. It is negative when they are weak or reversed, and near 0 when both sit at their usual level. - Its size grows continuously with both terms, up to about ±13.
Config: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The slope of the regression of each coin's next 10-bar return against the forecast at that bar's close, with the coin's normal 10-bar drift subtracted from the return. The bars are taken on a non-overlapping grid of every 10th bar in each window, and all coins and windows are pooled. The drift is the coin's mean 10-bar return over all its windows.
- Supporting check: The book's timing gain before costs is positive: its mean daily return minus the part due to the market's own rise.
- Confirm: The slope's t is 2 or more and the timing gain is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2, or a t of 2 or more with a timing gain at or below 0. At least 300 non-overlapping cases are required in total; with fewer, the result is inconclusive.
