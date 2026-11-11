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
- Situation: the stretch from an upward cross of the short average over the long until the next downward cross -> adapted: the "short above long" state made graded by the SMA spread, kept only when positive.
- Comparison: random stretches of the same length -> kept: in-stretch bars compared with all bars of the same coin and windows, which is buy-and-hold.
- Outcome: price rises more often and further during the stretch -> kept: next-bar close-to-close return during the stretch.
- Verdict transfer: yes: the forecast is positive exactly while the short SMA is above the long one, so returns earned there test the idea directly.
Forecast: The percent spread of the 50-day SMA over the 200-day SMA (the usual daily cross pair; the brief gives no periods). It is standardised against its own last 200 values and clipped at zero. The forecast is positive and grows with the spread while the 50-day SMA is above the 200-day SMA. It is zero from the downward cross until the next upward cross. It is never short, because the idea covers only the upward stretch.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Mean next-bar close-to-close return on bars where the forecast is above 0, minus the mean next-bar return over all bars, which is buy-and-hold. It is pooled over the 6 windows, before costs, with one return per bar so there is no overlap. Report a Welch t-statistic.
- Supporting check: The share of up bars during the stretch minus the share of up bars over all bars, with a two-proportion z-test.
- Confirm: The excess mean return has t >= 2, and the up-bar share during the stretch is higher than over all bars.
- Reject: The excess mean return has t <= -2, meaning the stretch does worse than holding the coin and moves after the cross reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive, including an estimate near zero. The test is also inconclusive with fewer than 100 in-stretch bars or fewer than 100 out-of-stretch bars, or with fewer than 2 distinct up-stretches across the windows.
