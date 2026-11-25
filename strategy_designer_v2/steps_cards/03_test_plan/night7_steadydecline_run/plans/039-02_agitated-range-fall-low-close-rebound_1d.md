---
idea: 039-02_agitated-range-fall-low-close-rebound
brief: 039_agitated-low-close-big-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: in an agitated market, a one-day fall measured against the 30-day average daily range, with the close near the day's low -> kept: FallCloseLocationComponent multiplies the close-to-close fall, in prior 30-day mean daily ranges, by the close's nearness to the low. It is 0 on days that do not fall, and the agitated profile is added by code.
- Comparison: the fall against the coin's 30-day average daily range -> kept: the fall is divided by the mean high-low range of the prior 30 days.
- Outcome: the price rises over the next day, more when the two features are larger together -> kept: long only, sized by the product, held 1 bar.
- Verdict transfer: yes: the forecast is the idea's own product of the two features, held for its one-day horizon inside the agitated profile, so a confirm or a reject of this test transfers to the idea.
Forecast: The forecast is one component, FallCloseLocationComponent (`vol_period` 30, `base` "mean_bar_range", `exclude_current` 1). It takes the day's close-to-close fall in the prior 30 days' mean daily range and multiplies it by (high − close) / (high − low). The result is standardised over its past 60 values (`min_periods` 20). The forecast is exactly 0 on any day that did not close down. It is positive on down days and grows continuously with the depth of the fall and with how close the close sits to the low. It is never negative (long only). Outside the agitated profile, code keeps the book flat.
Config: 039-02_agitated-range-fall-low-close-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the forecast-weighted mean of the next-day return minus the coin's mean daily return over all windows. Its t is taken with cases on the same day summed into one piece of evidence.
- Supporting check: Among the bars with forecast > 0, the mean next-day excess return of the top half by forecast minus that of the bottom half must be above 0 (the rise grows with the two together).
- Confirm: The weighted mean excess return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the supporting check failing. At least 100 distinct days with forecast > 0 are needed, otherwise the result is inconclusive.
