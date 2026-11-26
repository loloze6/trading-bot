---
idea: 039-01_agitated-swing-fall-low-close-rebound
brief: 039_agitated-low-close-big-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a one-day fall, measured against the coin's 30-day standard deviation of daily returns, with the close near the day's low, in an agitated market -> adapted: graded by the fall in usual moves times the close's nearness to the low; zero on up days; the agitated profile is added by code.
- Comparison: the fall judged against the coin's 30-day standard deviation of daily returns -> kept.
- Outcome: a larger rise over the next day, growing with the two features together -> kept.
- Verdict transfer: yes: the forecast is the product the idea names, measured inside its profile, against the next day's return.
Forecast: The forecast uses one indicator, FallCloseLocation with a 30-bar volatility window. On each bar it computes the day's fall in units of the 30-day standard deviation of daily returns. It multiplies that by (high − close) / (high − low), which is 1 when the close is at the low and 0 when it is at the high. The value is standardised against its own past 60 values, with a target of 10 and a cap of 20, then clipped at 0 so the book is long only. The forecast is 0 on up days and flat days. It is positive on down days and grows with the fall's size and the closeness of the close to the low together. Outside the agitated profile the code holds the book flat.
Config: 039-01_agitated-swing-fall-low-close-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day return, minus the coin's mean daily return over all windows, regressed on the forecast. It is measured on bars with a forecast above 0. Cases on the same day across coins are summed into one case, and the measure is reported with its t and the number of days.
- Supporting check: The book's mean daily return, minus its gain from the market's own rise, is above 0 before costs.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any slope with t between −2 and 2 is inconclusive. So is a positive slope with t ≥ 2 when the supporting check fails. At least 100 days with a positive forecast are needed; fewer is inconclusive.
