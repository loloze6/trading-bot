---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: a coin's Sunday close is above its Saturday close -> adapted: on the Sunday bar only (a regime on the weekday), the on/off "above" is made graded as the Sunday rise in usual one-day moves, zero when Sunday did not rise.
- Comparison: Sunday's volume against the coin's 60-day average daily volume, lower meaning a larger fall -> kept: the 60-day mean volume over Sunday's volume multiplies the rise.
- Outcome: the coin falls over the next 2 days, more after thinner Sundays -> kept: a short held 2 daily bars from Sunday's close, sized by the forecast.
- Verdict transfer: yes: the test bets only the stated short over the stated 2 days, sized by the stated volume ratio, so its result is the idea's result.
Forecast: The forecast is active only on the bar stamped Sunday, picked by a regime rule. `WeekdayComponent` reads 0 there, because the coming bar is Monday. On every other bar the forecast is 0. On Sunday the forecast uses `ThinVolumeScaledReturnComponent` with these settings: - `period` 1: Sunday's close over Saturday's close, minus 1. - `window` 60: that return is divided by its mean absolute one-day return over 60 days. - `volume_period` 1, `base_near` 1, `base_far` 60: the result is multiplied by the mean volume of the prior 60 days over Sunday's volume. The steps applied to this value: - `standardise` (60/20) puts it on the forecast scale. - `clip` at min 0 keeps only Sunday rises. - `negate` turns it into a short. So the forecast is 0 or negative. It is never positive. Its size grows with the size of the Sunday rise and with how thin Sunday's volume was against the 60-day average. It is 0 when Sunday closed at or below Saturday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: One case is each Sunday bar with a forecast below 0; Sundays are 7 bars apart, so cases never overlap. For each case, take the coin's return from Sunday's close to Tuesday's close. Subtract the coin's mean 2-bar return over all windows (holding the coin) and negate the result: this is the unusual move in the short's direction. Report its mean over the cases with its ordinary t, before costs.
- Supporting check: Split the cases at the median of |forecast|. Take the mean unusual move of the larger half minus that of the smaller half, and require it to be above 0. This checks that thinner, larger Sunday rises fall more.
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the supporting check's difference is above 0.
- Reject: The main measure's mean is below 0 with t ≤ -2: rising Sundays keep rising over the 2 days more than the coin's drift.
- Inconclusive: These results neither confirm nor reject: a main t between -2 and 2, or t ≥ 2 with a supporting difference at or below 0. Fewer than 200 cases in total across coins and windows is also inconclusive.
