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
- Situation: a sharp one-day drop on unusually low volume -> adapted: low volume becomes an on/off regime (volume below its 20-day mean), and drop size is graded.
- Comparison: volume against its usual level -> adapted: "unusually low" becomes "below the 20-bar volume mean", the only volume test the config can express.
- Outcome: price rebounds upward after the drop -> adapted: the hold is dropped; the long lasts only while the low-volume, down-move reading persists, and it is judged on the next bar.
- Verdict transfer: yes: a next-bar rebound that grows with the size of a thin-volume drop confirms the idea, and its reliable absence or reverse rejects it.
Forecast: The forecast is zero on any bar where volume is at or above its 20-day mean. On a bar where volume is below that mean, it reads the current bar's 1-day percent change. That change is standardised against its own past 60 values and negated, so a drop gives a positive value. It is clipped at 0, so up days give 0 and the strategy is long only. A signed power with exponent 2 then damps small drops smoothly and amplifies sharp ones. The long position is therefore larger the sharper the thin-volume drop, and never short.
Config: 003-02_low-volume-down-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use the active bars (forecast > 0), pooled over all 6 windows. Regress the coin's next-bar return, minus its mean daily return in that window, on the forecast, and report the t-statistic of the slope. Each bar is counted once, so there is no overlap.
- Supporting check: Take the top quartile of active forecasts. Their mean next-bar return, minus the window's mean daily return, should be positive.
- Confirm: The slope t-statistic is 2 or more and the supporting check is positive.
- Reject: The slope t-statistic is -2 or less, meaning sharper thin-volume drops are followed by further relative decline.
- Inconclusive: A t-statistic between -2 and 2 is inconclusive. Fewer than 60 active bars in total is also inconclusive, whatever the t-statistic.
