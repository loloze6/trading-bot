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
- Situation: short SMA above long SMA, from the up-cross to the next down-cross -> adapted: the on/off state is made graded as the positive SMA50 minus SMA200 spread, and is zero below.
- Comparison: random stretches of the same length -> kept: a random stretch's expected return equals the all-bar average, which buy-and-hold over the same window gives.
- Outcome: price rises more often and further while in the stretch -> kept: measured as daily coin returns on in-stretch bars.
- Verdict transfer: yes: the position is non-zero exactly on in-stretch bars, so their returns against all bars confirm or reject the idea directly.
Forecast: The forecast uses the 50-day and 200-day simple moving averages of the close (the usual golden-cross setting on daily bars). It takes their percent spread, (SMA50 - SMA200) / SMA200, and standardises it against its own past 200 values (target 10, cap 20). Negative values are clipped to 0. The forecast is positive only while the 50-day average is above the 200-day, and grows with how far apart the two averages are. It is zero from the down-cross until the next up-cross. It is never short.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take the coin's next-bar return on bars where the forecast is above 0 (in-stretch), pooled over the 6 windows. Compare it with the next-bar return on all bars of the same windows, which is buy-and-hold. Judge before costs.
- Supporting check: Compare the share of up days on in-stretch bars with the share of up days on all bars.
- Confirm: The in-stretch mean daily return exceeds the all-bar mean, with a one-sided t-statistic of at least 2.0 on non-overlapping daily returns. The in-stretch up-day share also exceeds the all-bar share.
- Reject: The in-stretch mean daily return is at or below the all-bar mean, which means there is no persistence. A t-statistic of -2.0 or lower on the difference means moves reverse after up-crosses, and this also rejects the idea.
- Inconclusive: A t-statistic between -2.0 and 2.0 is inconclusive. So are fewer than 100 in-stretch bars, or fewer than 3 distinct up-cross stretches across the windows.
