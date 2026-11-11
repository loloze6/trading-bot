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
- Situation: short SMA above long SMA, from up-cross to down-cross -> adapted: on/off "short above long" made graded as the long-only SMA50/SMA200 spread.
- Comparison: random stretches of the same length -> adapted: all bars of the same coin and windows, which is the same as simply holding the coin.
- Outcome: price rises more often and further during the stretch -> kept: next-bar close-to-close return while the spread is positive.
- Verdict transfer: yes: the forecast is positive exactly while the short average is above the long one, so its next-bar returns against all bars test the stretch claim both ways.
Forecast: The forecast uses the percent spread of the 50-day SMA over the 200-day SMA. It is standardised against its own past 200 values and clipped at 0, so it is long-only. It is positive only while SMA50 is above SMA200, which is the stretch between an up-cross and the next down-cross. It is zero otherwise. It grows smoothly with the gap between the averages, from about 0 at the cross up to the cap of 20, where the cap applies.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Mean next-bar log return of the coin on bars where the prior close's forecast is above 0, minus the mean next-bar log return over all bars. It is pooled across the 6 windows, with a Newey-West t-statistic (lag 10), before costs.
- Supporting check: Share of up bars when the forecast is above 0, against the share of up bars over all bars (two-proportion z).
- Confirm: The excess mean return has t ≥ 2 and is positive, and the supporting up-bar share is not lower than over all bars.
- Reject: The excess mean return has t ≤ -2, which means moves after the up-cross reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive. A sample with fewer than 2 complete up-cross stretches or fewer than 100 in-position bars is also inconclusive, whatever the t.
