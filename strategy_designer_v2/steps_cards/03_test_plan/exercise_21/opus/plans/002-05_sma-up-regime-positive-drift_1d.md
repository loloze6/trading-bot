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
- Situation: the stretch from an up-cross of SMA50 over SMA200 to the next down-cross -> adapted: "after the up-cross, until the down-cross" becomes "while SMA50 is above SMA200", and the on/off state is graded by the size of the spread.
- Comparison: random stretches of the same length -> kept: returns on in-state bars are compared with returns on all bars of the same coin and windows.
- Outcome: price rises more often and further during the stretch -> kept: the next-bar return while in the state, upward.
- Verdict transfer: yes: the main measure uses exactly the bars between the two crosses, against unconditional bars, so a confirm or a reject carries over to the idea.
Forecast: The forecast uses one indicator, the spread between the 50-day and 200-day simple moving averages, (SMA50 − SMA200) / SMA200 in percent. 50/200 is the standard daily cross, since the brief gives no settings. The spread is standardised against its own past 200 values and clipped at 0. The forecast is positive and grows with the spread whenever SMA50 is above SMA200, which is the stretch after an up-cross. It falls smoothly to zero at the down-cross and stays zero while SMA50 is below SMA200. It is long only, because the idea claims only the up-cross stretch.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The mean next-bar close-to-close return on bars where the forecast is above 0, minus the mean next-bar return over all bars of BTC in the 6 windows, before costs. Each bar is used once, so no returns overlap.
- Supporting check: The share of up bars on in-state bars versus the share on all bars.
- Confirm: The in-state excess mean return is above 0 with a t-statistic of +2 or more (Welch, in-state versus all bars).
- Reject: The in-state excess mean return has a t-statistic of −2 or less. That would mean price falls behind the unconditional drift during up-cross stretches, as if the cross marked exhaustion.
- Inconclusive: Any t-statistic between −2 and +2 is inconclusive. So is any result with fewer than 100 in-state bars, or fewer than 2 distinct up-cross stretches, across the 6 windows.
