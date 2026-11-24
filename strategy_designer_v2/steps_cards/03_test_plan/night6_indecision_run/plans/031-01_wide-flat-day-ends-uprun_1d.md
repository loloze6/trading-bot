---
idea: 031-01_wide-flat-day-ends-uprun
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: after a 5-day rise, a day with a wide range that closes near its open -> adapted: the 5-day rise, a range at least 1.5x the 20-day average and a body at most 10% of the range form a regime; inside it the forecast is graded by range ratio and flatness.
- Comparison: the day's range against its average daily range over the past 20 days -> kept
- Outcome: a fall over the next 5 days, larger for wider and flatter days -> kept
- Verdict transfer: yes: a short held 5 days from exactly these days either earns the fall, larger on wider and flatter days, or it does not.
Forecast: The regime detector picks `mean_reversion` only on a day that meets all three conditions: - the 5-day close-to-close return is above 0; - the day's high-low range is at least 1.5 times its 20-day mean bar range (the usual wide-range-bar convention); - the day's flatness, 1 minus |close−open|/range, is at least 0.9 (the doji convention: body at most 10% of the range). On every other day the forecast is 0 (flat). Inside the regime, two components are each standardised over 60 values and negated: the range ratio (today's range over the 20-day mean range) and the flatness. A `signed_power` with exponent 2 and pivot 20 then spreads values that would otherwise sit near the cap. The two are averaged with equal weight. The forecast is always negative (short). It runs from about −11 to −20, larger the wider the day's range against its average and the closer the close to the open.
Config: 031-01_wide-flat-day-ends-uprun_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Over the cases (short bets opened in the regime, one per 5-bar grid cell), the coin's 5-day return from the signal close minus its normal 5-day drift, in the short direction. The t is computed with same-day cases taken together.
- Supporting check: The mean unusual move of cases above the median |forecast| exceeds that of cases below it (the difference is above 0).
- Confirm: The mean unusual move in the short direction is above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move in the short direction is below 0 with t ≤ −2 over at least 30 cases.
- Inconclusive: Any t between −2 and 2, a confirming t whose supporting check fails, or fewer than 30 cases.
