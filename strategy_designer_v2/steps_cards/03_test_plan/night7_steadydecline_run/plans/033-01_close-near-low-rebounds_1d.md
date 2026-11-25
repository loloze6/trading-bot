---
idea: 033-01_close-near-low-rebounds
brief: 033_close-location-next-day-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: the day's close position within the day's high-low range, nearer the low -> kept
- Comparison: near the low against near the high, graded across the range -> adapted: centred on the coin's usual close location, so the forecast runs long near the low and short near the high
- Outcome: larger rise in price over the next day -> kept
- Verdict transfer: yes: a graded forecast that rises as the close nears the low, judged on next-day returns, confirms or rejects the stated relation directly.
Forecast: Two components with equal weights. The first is the close's distance from the day's high as a share of the day's range (`CloseLocationInRangeComponent`, `reference` "high"). It is 0 when the close is at the high and 1 when it is at the low. It is standardised over the past 60 days, so a typical value is about 10, a close at the low gives about 20 and a close at the high gives 0. The second is the constant offset -10. The forecast is their mean, (x − 10) / 2, which runs from about -5 to +5. It is positive when the close sits nearer the low than usual and grows the closer it is to the low. It is negative when the close sits nearer the high, and about 0 at the usual location. There is no regime gate.
Config: 033-01_close-near-low-rebounds_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Per bar, compute (forecast / 10) × (next-day return minus the coin's mean daily return over all windows). Sum these per calendar day across coins, then take the t of the mean over days.
- Supporting check: The mean next-day excess return after bars with forecast ≥ +2.5 minus the mean after bars with forecast ≤ −2.5 must be above 0.
- Confirm: The main-measure t is ≥ 2 and the supporting check's difference is above 0.
- Reject: The main-measure t is ≤ −2.
- Inconclusive: A t between −2 and 2, or t ≥ 2 with the check failing. At least 500 distinct days of cases are required, else the result is inconclusive.
