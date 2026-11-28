---
idea: 086-02_repeated-heavy-volume-buying-days
brief: 086_falling-calm-heavy-volume-up-day-accumulation
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling calm market, several of the last 3 days closed up on volume heavy against the 20-day average -> adapted: heavy is a regime condition (3-day mean volume above the prior 20-day mean); the per-day count is carried by the graded 3-day rise times that volume ratio.
- Comparison: heavier and more repeated heavy up days against fewer or lighter ones -> adapted: graded, so the forecast grows with the 3-day rise in usual moves times the volume ratio.
- Outcome: the coin rises over the next 5 days, more as the forecast grows -> kept.
- Verdict transfer: yes: the test bets only inside heavy recent volume in a falling calm market, sized by the up-move on that volume, which is the idea's claim.
Forecast: The regime detector computes the mean volume of the last 3 days against the mean of the 20 days before them (VolumeRatioComponent, period 20, short_period 3, exclude_current 3). When that ratio is above 1, the bar is in `trending`; otherwise it is flat. Inside `trending`, one component sets the size: RecentToPriorVolumeScaledReturnComponent (period 3, base_period 20, window 20). It is the 3-day return, in usual 3-day moves over 20 days, times the 3-day volume over the prior 20-day volume. This value is standardised (window 60, min_periods 20), then clipped at 0, so the book is long only. The forecast is 0 when the 3 days did not rise. It grows with the size of the rise and with how heavy its volume is. The falling-calm profile is added by code.
Config: 086-02_repeated-heavy-volume-buying-days_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, take the bars with forecast > 0. Measure each one's 5-day return minus the coin's mean 5-day return over all windows. Average these, weighted by the forecast; its t groups the cases of one day together.
- Supporting check: Split the cases at the median forecast. The mean excess 5-day return of the upper half, minus that of the lower half, must be above 0.
- Confirm: The weighted mean excess return is above 0 with t >= 2, and the supporting check passes.
- Reject: The weighted mean excess return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose supporting check fails, and any result from fewer than 30 cases.
