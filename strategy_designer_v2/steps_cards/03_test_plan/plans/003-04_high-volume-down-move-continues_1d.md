---
idea: 003-04_high-volume-down-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp one-day drop on heavy volume -> adapted: a down close-to-close day while volume is at or above its 20-day mean opens a regime, and the short is sized by how big the drop is.
- Comparison: volume against its usual level -> adapted: "unusually high" becomes volume at or above its 20-bar mean, the only volume cut the catalogue allows (a veto with `volume_filter`).
- Outcome: price keeps falling after the drop -> adapted: "after X" becomes "while X", so the short is held only for the bar after each qualifying day.
- Verdict transfer: yes: the test shorts exactly the heavy-volume down days, sized by the drop, and is judged on whether the next bar falls more than usual.
Forecast: One indicator: the one-day price change (`PriceEvolutionComponent`, period 1), standardised against its own last 60 values (window 60, min_periods 20). A veto turns on the active regime only on bars that are both down days and at or above their 20-day mean volume. On those bars the forecast is the standardised move. It is always negative, so the position is a short. An average-size drop gives about -10 (100% short), and a sharper drop gives a larger short, up to -20. On every other bar the forecast is 0 (flat).
Config: 003-04_high-volume-down-move-continues_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Mean next-bar return after active bars (heavy-volume down days) minus the mean next-bar return over all bars in the same windows (the hold-the-coin baseline), before costs. Each bar counts once, so returns do not overlap.
- Supporting check: Across active bars, the regression slope of next-bar return on forecast size should be positive: a larger short should be followed by a larger fall.
- Confirm: The excess return is negative with t ≤ -2 over at least 60 active bars, and negative in at least 4 of the 6 windows.
- Reject: The excess return is zero or positive (heavy-volume drops are followed by rebounds or no extra fall), with at least 60 active bars.
- Inconclusive: A negative excess return with t between -2 and 0, or a negative one in fewer than 4 windows; any result with fewer than 60 active bars across the 6 windows.
