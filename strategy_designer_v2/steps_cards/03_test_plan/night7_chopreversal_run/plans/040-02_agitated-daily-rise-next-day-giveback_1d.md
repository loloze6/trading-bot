---
idea: 040-02_agitated-daily-rise-next-day-giveback
brief: 040_agitated-daily-move-next-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: an agitated market and a one-day rise in percent from the previous close -> adapted: the agitated profile is added by code; inside it, the position exists only on up days and is graded by the size of the rise.
- Comparison: a larger rise against a smaller one -> kept: the short grows linearly with the day's percent rise, scaled against its past 60 daily moves.
- Outcome: a fall over the next day, larger after a larger rise -> kept: the short is held 1 bar and judged on the next day's return.
- Verdict transfer: yes: the forecast is exactly the size of the day's rise, short, inside the agitated profile, for one day.
Forecast: The day's percent change from the previous close (`PriceEvolutionComponent`, period 1). It is standardised against the mean absolute size of its last 60 daily changes, so a usual-sized move gives about 10, capped at 20. It is then negated and clipped at a maximum of 0. The forecast is a short whose size grows linearly with the day's rise. It is zero on down days and flat days, and the code adds the profile so the book is also flat outside the agitated profile. It is never long.
Config: 040-02_agitated-daily-rise-next-day-giveback_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The sample is every bar with forecast below 0. On each bar the measure is the position held after the trade times the coin's excess return: close[t+1]/close[t] - 1, minus the coin's mean daily return over all windows. Its mean is tested with a t. Cases on the same day are summed into one, so the t counts days.
- Supporting check: Regress the next-day excess return on the forecast over the same bars. The slope must be positive: a more negative forecast, that is a larger rise, must be followed by a lower next-day return.
- Confirm: The mean excess gain is above 0 with t ≥ 2, and the supporting slope is positive.
- Reject: The mean excess gain is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 with a slope that is zero or negative. Fewer than 100 distinct days with a short case is also inconclusive.
