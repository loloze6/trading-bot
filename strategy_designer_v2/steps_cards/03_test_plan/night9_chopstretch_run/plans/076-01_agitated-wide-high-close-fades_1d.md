---
idea: 076-01_agitated-wide-high-close-fades
brief: 076_agitated-wide-high-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ad4516fba127
---
Fidelity:
- Situation: in an agitated market, a day with a wide high-low range that closes near its high -> kept: the profile is added by code; "wide" (range above its 20-day mean) and "near its high" (close in the upper half of the range) are regime conditions, with the strength graded by their product inside.
- Comparison: the day's range against the coin's average range over the past 20 days -> kept: the range is divided by the 20-day mean bar range, which includes the day itself.
- Outcome: a fall over the next day, larger the wider the range and the higher the close, the two multiplying -> kept: a 1-bar short sized by range multiple x close location.
- Verdict transfer: yes: the config shorts exactly these days for one day, sized by the stated product, so the test's result is the idea's result.
Forecast: The regime detector selects `mean_reversion` on days when both conditions hold: the day's range is at least its 20-day mean bar range, and the close sits in the upper half of the day's range. All other days are flat, and code adds the agitated-profile vetoes. Inside the regime, the forecast comes from BreakoutInMeanRangesComponent (period 1, base_period 20, extreme low, source high, high_current 1). Its value is (close − low) / 20-day mean range, which equals close location x range multiple. It is standardised over 60 past values and negated. The forecast is therefore always short or zero, and its size grows with the product: about −9 at the regime's edge, reaching the −20 cap for the widest, highest-closing days.
Config: 076-01_agitated-wide-high-close-fades_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars where the forecast is below 0, the next-day return minus the coin's mean daily return over all windows, in the short direction; its mean and its t, with deviations summed per day.
- Supporting check: Among those cases, the short-direction unusual move of the half with the larger |forecast| minus that of the smaller half must be above 0.
- Confirm: The mean short-direction unusual move has a t of 2 or more, and the supporting difference is above 0.
- Reject: The mean short-direction unusual move has a t of −2 or less, meaning these days rise more than the drift.
- Inconclusive: Any t between −2 and 2, or a confirming t with the supporting difference at or below 0; at least 30 distinct days of cases are required, else inconclusive.
