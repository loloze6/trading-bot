---
idea: N3-02_breakout-shock-continues
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds B, C
outcome: plan
fit: adapted
---
Fidelity:
- Situation: an outsized up day that closes above the highest close of the prior 20 days -> adapted: the new 20-day closing high is a regime rule; "outsized" is made graded, as the up-day's size against its own recent past with a cubic graded dead zone.
- Comparison: shock-up days that stay inside the recent range -> kept: those days are flat in the config, and their one-day return is recorded, so the two sets can be compared.
- Outcome: the coin keeps rising over the following five days -> adapted: the five-day hold is dropped; the five-bar forward return is read from the price record.
- Verdict transfer: yes: the forecast is non-zero only on new-high up days and grows with the size of the shock, and the criterion reads the next five bars.
Forecast: The regime is active only when the 21-bar Donchian position is at its maximum. That means the close is the highest close of the current bar and the prior 20 bars. On those bars the forecast is the one-day percent return, standardised against the mean absolute value of its last 60 values. It is clipped at 0, so down days give 0, and then cubed around pivot 10. An average-size up day gives about 10. An up day twice the average size, or larger, reaches the cap of 20. A small up day stays near 0. On every other bar the forecast is 0. It is never negative.
Config: N3-02_breakout-shock-continues_1d_oos2_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are bars with forecast at or above 10, which means a shock-up new high. For each case, take the 5-bar forward close-to-close return. Subtract the coin's mean 5-bar return over all of its windows pooled together. Signals within 5 bars of an earlier case are merged into one case. Pool the cases across coins and test with a t-statistic. The measure is taken before costs.
- Supporting check: Compare against shock-up days inside the range. These are bars with the standardised one-day return at or above 10 while the forecast is 0. The mean excess 5-bar return after new-high cases should exceed the mean excess after these inside-range cases.
- Confirm: The mean excess 5-bar return after the cases is positive with t ≥ 2, and the supporting difference is also positive.
- Reject: The mean excess 5-bar return is negative with t ≤ -2, meaning prices reverse after shock-up new highs.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any test with fewer than 30 non-overlapping cases pooled across coins.
