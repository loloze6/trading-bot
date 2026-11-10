---
idea: 003-02_low-volume-down-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: sharp one-day drop on unusually low volume -> adapted: the drop's size is graded, and "low volume" is an on/off regime gate (the day's volume below its 20-day mean, the only volume test the catalogue offers).
- Comparison: the day's volume against its usual level -> kept: compared with the 20-bar mean volume via `volume_filter` in a veto.
- Outcome: price rebounds upward, recovering part of the drop -> adapted: measured as the next bar's return while the position is held; the multi-day holding period is dropped.
- Verdict transfer: yes: a long sized by the drop, held only after low-volume down days, gains if and only if such drops are followed by rebounds.
Forecast: A veto sends a bar to `mean_reversion` only when that day's volume is below its 20-day mean. Every other bar is flat. In `mean_reversion` the forecast comes from the one-day percent change (`PriceEvolutionComponent`, period 1). It is standardised against its last 60 values, negated so a drop is positive, clipped at 0 so only drops count, then passed through `signed_power` with exponent 2 so sharp drops weigh much more than small ones. The forecast is zero on up days and on normal- or high-volume days. On low-volume down days it is positive and grows with the square of the drop's size relative to recent daily moves, capped at 20.
Config: 003-02_low-volume-down-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The excess return of active bars, before costs. Take the forecast-weighted mean of the next bar's return on bars with forecast > 0, pooled over all 6 windows. Subtract BTC's mean daily return over all bars of the same windows.
- Supporting check: Split active bars at the median forecast. The mean next-bar return of the top half should exceed that of the bottom half, meaning gains grow with the size of the drop.
- Confirm: The excess is positive with a t-statistic of at least 2.0, and the top half beats the bottom half.
- Reject: The excess is at or below 0, or the top-half mean next-bar return is negative.
- Inconclusive: An excess that is positive but has a t-statistic below 2.0, or a positive excess where the top half does not beat the bottom half. Also inconclusive when there are fewer than 60 active bars across the 6 windows (each bar counted once, since the horizon is 1 bar).
