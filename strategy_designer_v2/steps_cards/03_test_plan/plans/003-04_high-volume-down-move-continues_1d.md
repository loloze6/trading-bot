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
- Situation: a sharp down move on unusually high volume -> adapted: a down day with volume at or above its 20-day mean opens the regime, and the size of the drop grades the position instead of a "sharp" cutoff.
- Comparison: volume judged against its usual level -> adapted: "unusually high" becomes "at or above the 20-bar mean volume", the only volume test the config has (`volume_filter`).
- Outcome: price keeps falling afterwards -> adapted: the position lasts only while the situation holds, so the test measures the next 1-day bar.
- Verdict transfer: yes: a short sized by the drop and held into the next day profits if and only if high-volume drops tend to continue.
Forecast: On each daily bar, the detector takes the 1-day percent change of the close. It keeps that change only if the bar's volume is at or above its 20-bar average, and otherwise sets it to 0. If the kept value is below 0, the bar is a high-volume down day and goes to the `trending` regime; every other bar is flat. In `trending`, the forecast is the same 1-day change, standardised against the 60 previous daily changes (target 10, cap 20), then clipped at a maximum of 0. A typical-sized down day gives about -10 (100% short). A drop twice as large as usual gives about -20 (200% short). A tiny drop gives a near-zero short. The forecast is never positive. The position is held into the next bar and closes as soon as a bar is not a high-volume down day.
Config: 003-04_high-volume-down-move-continues_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On every bar with a non-zero forecast, take the position (forecast / 10) times the next bar's close-to-close return of BTC. Subtract from that return the window's mean daily return, so buy-and-hold drift is not credited. Pool these per-bar products across the 6 windows; they do not overlap at a 1-bar horizon. Report their mean and t-statistic.
- Supporting check: Split active bars into the larger-short half and the smaller-short half by forecast. The larger-short half should show a higher mean demeaned per-bar gain.
- Confirm: The mean demeaned per-bar gain is above 0 with t ≥ 2, meaning BTC falls further than its drift on the day after high-volume down days.
- Reject: The mean demeaned per-bar gain is below 0 with t ≤ -2, meaning the day after high-volume down days rises relative to drift.
- Inconclusive: A t-statistic between -2 and 2, or fewer than 40 active bars pooled across windows, neither confirms nor rejects.
