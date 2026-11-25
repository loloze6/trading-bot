---
idea: 034-02_agitated-high-close-gives-back
brief: 034_agitated-close-location-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in an agitated market, how near the daily close sits to the day's high within its high-low range -> kept: the profile keeps the agitation, and the forecast is graded by the close's place in the day's range
- Comparison: none -> kept
- Outcome: the coin falls over the next day, more the nearer the close was to the high -> kept: a short position held for 1 daily bar, larger the nearer the close is to the high
- Verdict transfer: yes: the forecast is the idea's own graded reading inside its own profile, held for its own one-day horizon.
Forecast: The config uses one component, the close's location in the day's range, (close − low) / (high − low). It reads 0 at the day's low and 1 at the day's high. It is standardised against its own past 60 values (mean absolute value 10), then negated. The forecast is therefore short, or zero when the close is at the low. Its size grows linearly as the close nears the day's high, to about −20 for a close at the high. It is never positive. Market-profile code adds the agitated profile, so the book is flat outside agitated bars.
Config: 034-02_agitated-high-close-gives-back_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On every bar with a nonzero forecast, take the position before costs (`postRebalance_current_allocation`) times the coin's next-day return minus its mean daily return over all windows. Test whether the mean of that product is above 0, using the t of the mean with the cases of one day taken together.
- Supporting check: Regress the next-day excess return on the forecast across the same bars. The slope must be positive, meaning larger shorts are followed by larger falls than drift.
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the supporting slope is positive.
- Reject: The main measure's mean is below 0 with t ≤ −2. That would mean closes near the high are followed by rises against drift.
- Inconclusive: Any t strictly between −2 and 2 is inconclusive. So is a confirming main measure with a non-positive slope. The test needs at least 300 agitated bars in a position, across at least 3 coins.
