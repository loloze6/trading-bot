---
idea: 042-01_falling-agitated-low-close-rebound
brief: 042_falling-agitated-low-close-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's close sits low within that day's high-low range, in a falling agitated market -> kept: the close's place in the day's range, measured by `CloseLocationInRangeComponent` "high", inside the falling agitated profile that code adds.
- Comparison: lower closes against higher closes in the range -> kept: the position grows with how low the close sits, and the test compares next-day returns across that size.
- Outcome: the coin rises over the next day, most after a close at the very bottom -> kept: next-day return, 1 bar on 1d bars.
- Verdict transfer: yes: the test measures how next-day returns change with the close's place in the range, inside the profile, so a confirm or a reject carries over to the idea.
Forecast: One component, the close's distance down from the day's high as a share of the day's range: 0 at the high, 1 at the low. It is standardised over its last 60 bars (min 20), so a mid-range close gives about +10 and a close at the very low about +20 (capped). The forecast is always zero or positive. It is 0 when the close is at the day's high and grows linearly as the close sits lower, so the book is most long after a close at the bottom. It applies only on falling agitated bars; code adds the profile, and the book is flat outside it.
Config: 042-01_falling-agitated-low-close-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On in-profile bars, regress the coin's next-day return minus its mean daily return over all windows (the excess return) on `debug_info.components.low_close.last_history_value`. Report the slope's t, with cases of the same day summed per day.
- Supporting check: On in-profile bars with a close in the bottom fifth of the range (raw value at least 0.8), the mean next-day excess return is above 0.
- Confirm: The slope's t is +2 or more and the supporting check's mean is above 0.
- Reject: The slope's t is -2 or less: lower closes are followed by smaller next-day returns.
- Inconclusive: A slope t between -2 and +2, or a positive t of 2 or more with the bottom-fifth mean at or below 0. A verdict needs at least 100 in-profile bars across coins and windows, with at least 20 of them in the bottom fifth of the range.
