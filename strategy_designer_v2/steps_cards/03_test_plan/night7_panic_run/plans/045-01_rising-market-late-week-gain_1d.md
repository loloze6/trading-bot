---
idea: 045-01_rising-market-late-week-gain
brief: 045_late-week-gains-in-uptrends
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: in a rising market, after a Thursday or Friday close -> adapted: the rising profile is added by code; "after the close" becomes "while the coming bar is a Friday or a Saturday", a regime rule on the weekday.
- Comparison: more than the coin's usual day, and more so the larger the 60-day return -> kept: the forecast grows with the 60-day return, and the criterion is judged against the coin's mean day.
- Outcome: the coin rises over the next day -> kept: held 1 bar, long only.
- Verdict transfer: yes: the test bets only on Friday and Saturday bars in rising markets, sized by the 60-day rise, and judges the next day against the coin's usual day.
Forecast: The regime detector reads `WeekdayComponent`, the weekday of the coming bar. When it is Friday (4) or Saturday (5), the bar goes to `trending`. Every other bar goes to `unknown`, which is flat. Code adds the rising profile on top of this. In `trending`, the forecast is the coin's 60-bar return (`PriceEvolutionComponent`, period 60). That return is standardised against its own last 60 values (window 60, min_periods 20) and clipped at 0. So on Thursday and Friday closes in a rising market the forecast is positive. It sits near 10 when the 60-day rise is at its recent average size and goes up to 20 for a steeper rise. On every other bar it is zero, and it is never negative.
Config: 045-01_rising-market-late-week-gain_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with a position, the position held x (next-day return − the coin's mean daily return over all windows). Its mean and t are taken with the cases of one day summed across coins.
- Supporting check: Across those bars, the slope of the excess next-day return on the forecast is above 0.
- Confirm: The mean excess position gain is above 0 with t ≥ 2, and the slope is above 0.
- Reject: The mean excess position gain is below 0 with t ≤ −2.
- Inconclusive: Any t between −2 and 2. A significant positive mean with a slope at or below 0 is also inconclusive. At least 100 distinct days with a position are required.
