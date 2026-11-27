---
idea: 077-02_choppy-agitated-wide-high-close-fade
brief: 077_choppy-agitated-wide-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a wide day that closes near its high, wider against its 30-day swing and nearer the high -> kept: a regime holds the wide, high-closing day (range at or above its 30-day mean, close in the top quarter); inside it the forecast grows with range in 30-day return std and with close location.
- Comparison: the day's range against its 30-day swing, and the close against the day's high -> kept
- Outcome: price falls over the next day -> kept: a short held 1 bar.
- Verdict transfer: yes: the book is short only on wide high-closing days, sized by width and nearness to the high, so its next-day result answers the idea either way.
Forecast: The forecast is zero unless the day is wide and closes near its high. A wide day has a range at or above the mean daily range of the last 30 days. Near its high means the close sits in the top quarter of the day's range. Only bars inside the choppy agitated profile count; code adds the profile vetoes. On such days the forecast is short. It is the equal-weight mean of two standardised readings, each negated. The first is the day's range in units of the 30-day standard deviation of daily returns. The second is the close location in the range, where 1 means the close is at the high. Each is standardised over 60 bars with min_periods 20. The forecast is never positive. It grows in size as the day gets wider against its swing and as the close nears the high, and it is capped at -20.
Config: 077-02_choppy-agitated-wide-high-close-fade_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Each case is a short bet (a fall of the forecast of at least 2 points). For each case, take the coin's next-bar return minus its normal daily drift over all windows, signed for the short. Average these unusual moves and compute their t, with cases on the same day counted as one.
- Supporting check: Split the cases at the median absolute forecast. The upper half's mean unusual move must exceed the lower half's (difference upper minus lower above 0).
- Confirm: The mean unusual move is positive with t >= 2 (the coin falls more than its drift the next day), and the supporting check passes.
- Reject: The mean unusual move has t <= -2 (the coin rises more than its drift the next day after wide high closes).
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing. At least 100 distinct case days are required, else inconclusive.
