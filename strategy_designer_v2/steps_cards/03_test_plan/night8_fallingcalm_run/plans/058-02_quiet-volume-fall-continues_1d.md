---
idea: 058-02_quiet-volume-fall-continues
brief: 058_quiet-volume-calm-decline-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a falling calm market, a deep 30-day fall on volume lighter than usual -> kept: the 30-day return times the past year's mean volume over the last 30 days' mean volume; the profile is added by code.
- Comparison: the 30 days' volume against the coin's own average volume over the past year -> kept: the base is the mean volume of the year's bars before those 30 days.
- Outcome: it keeps falling over the next 5 days -> kept: a short graded by the fall times the lightness, held 5 bars.
- Verdict transfer: yes: the forecast shorts only as deep, light-volume falls appear, so the 5-day returns that follow decide the idea itself.
Forecast: One component, `ThinVolumeScaledReturnComponent`, with these settings: `period` 30, `window` 365, `volume_period` 30, `base_near` 31, `base_far` 365. Its raw value is the 30-day return, divided by the coin's usual 30-day move over the past year. That is multiplied by the past year's mean volume (bars t-365 to t-31) over the last 30 days' mean volume. It is negative after a fall. Its size grows with the depth of the fall and with how light the recent volume is against the year: heavy volume shrinks it. `standardise` uses window 395 and min_periods 99. A `clip` with max 0 then keeps only the short side. The forecast is 0 when the 30-day return is not negative. It grows more negative as the fall deepens and the volume thins. It is never positive. The falling-calm profile, added by code, keeps the book flat outside that market.
Config: 058-02_quiet-volume-fall-continues_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window and keep the bars with forecast < 0. On each, take the coin's 5-bar return minus its mean 5-bar return over all windows (holding the coin), times -forecast/10. Report its mean and its t, with the cases of one day summed together.
- Supporting check: On those grid bars, compare the mean drift-removed 5-bar return of the cases with |forecast| above the median against those below it (above minus below). The check passes when the difference is below 0.
- Confirm: The main measure's mean is above 0 with t >= 2, and the supporting check passes.
- Reject: The main measure's mean is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming main measure with a failed supporting check. A run with fewer than 30 grid cases, on fewer than 30 distinct days, is also inconclusive.
