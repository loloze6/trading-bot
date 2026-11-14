---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: sharp move in quiet hours or weekends on low volume -> replaced: on 1d bars intraday quiet hours are hidden inside the bar, and no component reads the weekday, so only "low-volume day" remains.
- Comparison: low-volume moves against busier, normal-volume periods -> adapted: a veto with `volume_filter` could split days by volume against a 20-bar mean, but not by hour or weekday.
- Outcome: move partly reversed once busy hours and volume return -> adapted: a contrarian position held while volume is low, judged on the next bar's return.
- Verdict transfer: no: a test of "low-volume days revert" on daily bars says nothing about moves in a coin's quiet hours or on weekends.
Reason: The idea's situation is a time-of-day or day-of-week condition (quiet hours, weekends). On 1d bars quiet hours sit inside a single bar, and no component or rule reads the bar's weekday, so the situation can only be replaced by "low-volume day". The bar size is set by the run, not by the config.
