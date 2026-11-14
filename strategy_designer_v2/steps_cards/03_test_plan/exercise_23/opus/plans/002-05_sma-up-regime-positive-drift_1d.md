---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch from an upward cross of the short average over the long average until the next downward cross -> adapted: "short SMA above long SMA" is held graded by how far apart they are, and is zero outside the stretch.
- Comparison: random stretches of the same length -> adapted: compared with all bars of the same windows, which is the same as holding the coin.
- Outcome: price rises more often and further over the stretch -> kept: the coin's daily returns on the bars of the stretch.
- Verdict transfer: yes: the main measure uses every in-stretch bar with equal weight, so the graded sizing does not change what is judged.
Forecast: The forecast is the percent spread of SMA50 over SMA200 on daily closes. It is divided by the mean absolute value of its own past 200 values, times 10, and capped at 20. It is then clipped at 0, because the idea concerns only the upward-cross stretch. It is positive exactly while SMA50 is above SMA200, which is the time between an upward cross and the next downward cross. It grows as the averages separate and returns smoothly to 0 at the downward cross. It is zero otherwise. The brief gives no settings, so 50/200 is the usual daily convention.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's mean next-bar (1d) return on bars where the forecast is above 0, minus its mean next-bar return on all bars of the same windows. Returns are taken before costs and counted once each because they do not overlap. The t-stat uses Newey-West errors with 10 lags.
- Supporting check: The share of up days on in-stretch bars, compared with the share of up days on all bars.
- Confirm: The in-stretch mean daily return exceeds the all-bar mean with t >= 2. The in-stretch up-day share must also be at least the all-bar share.
- Reject: The in-stretch mean daily return is below the all-bar mean with t <= -2. That would mean moves after upward crosses lag or reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive, including a difference near zero. The result is also inconclusive if there are fewer than 3 separate upward-cross stretches or fewer than 100 in-stretch bars across the 6 windows.
