---
idea: 002-06_sma-down-regime-negative-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA below long SMA, from the downward cross until the next upward cross -> adapted: the "below" state is made graded, using the signed SMA50/SMA200 spread kept only when negative.
- Comparison: random stretches of the same length -> kept: the mean return of in-state bars is compared with the mean of all bars of the same coin and window, which is the expected return of random stretches.
- Outcome: price falls more often and further until the opposite cross -> kept: the short is held on every bar of the stretch, and exits exactly when the spread turns positive.
- Verdict transfer: yes: the forecast is short exactly over the down-cross stretches and flat elsewhere, so results transfer both ways.
Forecast: The forecast is the SMA(50) minus SMA(200) spread in percent of SMA(200). It is standardised against its own last 200 values and clipped at 0 from above. It is negative only while the 50-day SMA is below the 200-day SMA, which is the stretch between a downward and an upward cross. It is zero on every other bar. The short grows as the short average sits further below the long one, up to the cap of -20.
Config: 002-06_sma-down-regime-negative-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The mean next-bar close-to-close return of BTC on bars where the forecast is below 0, minus the mean next-bar return over all bars of the same windows. Windows are pooled, and the standard error is computed over whole stretches, so each stretch counts once.
- Supporting check: The share of down bars inside the stretches compared with the share of down bars over all bars. The strategy's equity curve, before costs, should end above flat and beat holding the coin over the in-state bars.
- Confirm: Pooled in-state mean return is at least 0.10% per day below the all-bars mean, with stretch-clustered t ≤ -2. The share of down bars inside the stretches is higher than over all bars.
- Reject: In-state mean return is at or above the all-bars mean. This means price did not fall faster during down-cross stretches, or it reversed upward.
- Inconclusive: The difference is negative but t > -2 or it is smaller than 0.10% per day. The test also cannot conclude with fewer than 3 distinct down-cross stretches or fewer than 60 in-state bars pooled across the 6 windows.
