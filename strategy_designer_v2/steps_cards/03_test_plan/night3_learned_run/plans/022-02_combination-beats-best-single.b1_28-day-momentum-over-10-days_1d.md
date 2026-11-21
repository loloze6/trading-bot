---
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: a coin's 28-day return, higher or lower -> kept
- Comparison: higher 28-day return against lower, across its whole range -> kept
- Outcome: the return over the next 10 days is higher, in the same direction as the 28-day return -> kept
- Verdict transfer: yes: the forecast is the 28-day return itself, signed and graded, and each bet is held 10 days, so a confirm or a reject here is one for the idea.
Forecast: The forecast is the coin's 28-bar percent return (PriceEvolutionComponent, period 28). It is standardised against the mean absolute value of its previous 60 values (min_periods 20, target 10, cap 20). It runs on every bar with no regime gate and no re-weighting. It is positive after a 28-day rise and negative after a 28-day fall, and zero only when the 28-day return is zero. It grows linearly with the size of the return against its recent usual size, up to ±20.
Config: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the bars at positions 0, 10, 20, ... of each window, per coin. At each, take forecast/10 x (close[t+10]/close[t] - 1 minus the coin's mean 10-bar return over all its windows). The measure is the t of the mean of these products over all coins and windows: a gain that grows with position size, net of holding the coin.
- Supporting check: none
- Confirm: The mean forecast-weighted excess 10-bar return is positive with t ≥ 2, over at least 300 non-overlapping cases.
- Reject: The mean forecast-weighted excess 10-bar return is negative with t ≤ -2, over at least 300 non-overlapping cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is any result on fewer than 300 non-overlapping cases. About 1,700 cases are expected (6 coins × 24 windows × about 12 cells).
