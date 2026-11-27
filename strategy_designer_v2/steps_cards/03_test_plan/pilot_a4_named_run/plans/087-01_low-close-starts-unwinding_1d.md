---
idea: 087-01_low-close-starts-unwinding
brief: 087_rising-agitated-low-close-unwinds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a rising agitated market, a day closing near the low of its own high-low range -> kept: a regime when the close sits in the lowest 20 % of the day's range (the usual internal-bar-strength level); the profile is added by code.
- Comparison: the nearer the close to the day's low, the larger the decline -> kept: inside the regime, the short grows as the close nears the low.
- Outcome: price declines over the next three days -> kept: short, held 3 bars.
- Verdict transfer: yes: the test shorts exactly those days, sized by nearness to the low, over three days, so its result is the idea's.
Forecast: The regime detector reads where the close sits in the day's range, measured from the high (`CloseLocationInRangeComponent`, `reference` "high": 0 at the high, 1 at the low). When that reading is 0.8 or more, the close is in the bottom fifth of the range and the bar is `mean_reversion`. Every other bar is `unknown` and flat. Inside the regime, the same reading is standardised over its past 60 values (about 0.5 on average), then negated. The forecast is therefore short only: about -16 at the edge of the bottom fifth, growing to -20 at a close exactly on the low. It is zero outside the low-close days and outside the rising agitated profile, which code adds.
Config: 087-01_low-close-starts-unwinding_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move of the cases, in the short direction. A case is a short bet, sampled once per 3-bar grid cell. Its unusual move is the coin's 3-day return from the signal bar's close, minus the coin's normal 3-day drift over all windows, with the sign flipped for a short. The t is computed with each day's cases taken together.
- Supporting check: Split the cases at their median |forecast|. The mean unusual move of the larger half (closes nearer the low) must exceed that of the smaller half.
- Confirm: The mean unusual move is positive (the coin falls more than its drift) with t >= 2 over at least 30 case-days, and the supporting check passes.
- Reject: The mean unusual move is negative (the coin rises more than its drift after low closes) with t <= -2 over at least 30 case-days.
- Inconclusive: Any t between -2 and 2, fewer than 30 case-days, or a main measure that confirms while the supporting check fails.
