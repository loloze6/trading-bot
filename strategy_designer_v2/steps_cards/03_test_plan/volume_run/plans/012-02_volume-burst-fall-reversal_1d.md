---
idea: 012-02_volume-burst-fall-reversal
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a bar that falls sharply, with volume relative to the coin's 30-day average volume -> adapted: "falls sharply" is a regime rule (one-bar return of 2 or more usual moves down), and the volume ratio is graded.
- Comparison: larger versus smaller volume ratio among sharp falls -> kept: the position grows with the 30-bar volume ratio, so cases with different ratios can be compared.
- Outcome: larger price rise over the next 3 days -> adapted: the 3-day holding period is dropped (the position lasts only while the fall bar is current), and the 3-bar forward return is measured from the record.
- Verdict transfer: yes: the forecast and the criterion both rank sharp-fall bars by their 30-day volume ratio against the 3-day rise that follows.
Forecast: VolatilityScaledReturnComponent (period 1, vol_period 20) gives the bar's return in usual moves. When it is -2 or lower, the bar is a sharp fall and the regime is mean_reversion; on every other bar the forecast is 0. In mean_reversion, the forecast is VolumeRatioComponent (period 30), standardised over the 60 previous bars. That is about 10 x the volume ratio: always long, larger as the bar's volume rises above its 30-day average, and capped at 20 (reached at about twice the average volume).
Config: 012-02_volume-burst-fall-reversal_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the bars where the regime is mean_reversion. Within each window, keep a bar only if it lies 3 or more bars after the previous kept bar. Regress each kept bar's 3-bar forward return, minus the coin's mean 3-bar return over all windows, on its raw volume ratio (volratio last_history_value), pooled over coins, and take the t of the slope.
- Supporting check: The mean excess 3-bar return of the top third of kept cases by volume ratio is above 0.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with a failed check, is inconclusive. A verdict needs at least 30 kept sharp-fall cases in total.
