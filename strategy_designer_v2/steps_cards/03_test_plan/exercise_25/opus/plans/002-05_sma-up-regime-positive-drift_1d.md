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
- Situation: the stretch from an upward cross of the short average over the long one until the next downward cross -> adapted: "after the up-cross until the down-cross" becomes "while the short SMA is above the long SMA", and the on/off state becomes graded by the size of the gap.
- Comparison: random stretches of the same length -> kept: each bar's next-bar return is compared with the coin's average next-bar return over all bars, which is what holding the coin earns.
- Outcome: price rises more often and further during the stretch -> kept: the next-bar return of the coin, upward.
- Verdict transfer: yes: the in-stretch bars are exactly the bars with a positive forecast, and the measure is their return against holding the coin.
Forecast: Use the 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA. These are the conventional daily averages; the source script gives no periods. The value is standardised against its own past 200 values, then clipped at 0, so the forecast is long only. It is positive while the short average is above the long one (the stretch between an up-cross and the next down-cross). It grows with the gap between the averages and is 0 while the short average is below the long one.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's next-bar return minus its average next-bar return in the same window, weighted by the forecast. Taken over bars with a positive forecast, pooled across the 6 windows, as a t-statistic of the forecast-weighted excess return, before costs.
- Supporting check: The share of positive-forecast bars whose next bar closes up, compared with the share across all bars.
- Confirm: The forecast-weighted excess return has t >= 2, and the up-bar share in stretches is above the all-bar share.
- Reject: The forecast-weighted excess return has t <= -2, meaning returns during up-stretches fall short of holding the coin.
- Inconclusive: Any t between -2 and 2. Also inconclusive if fewer than 100 bars have a positive forecast, or if fewer than 3 separate up-stretches occur across the windows.
