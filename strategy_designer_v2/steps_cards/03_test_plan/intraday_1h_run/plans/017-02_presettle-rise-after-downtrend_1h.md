---
idea: 017-02_presettle-rise-after-downtrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a strong 3-day run down, in the 2 hours before a 00:00, 08:00 or 16:00 UTC settlement -> kept for the fall (72-bar graded fall); the 2-hour clock window has no catalogue component.
- Comparison: the stronger the 3-day fall, the larger the pre-settlement rise -> kept: the position grows with the size of the 72-bar fall.
- Outcome: the return over the 2 hours before settlement is positive -> kept: the 2-bar return on 1h bars.
- Verdict transfer: no: without the clock window, the test would bet on every hour after a fall, so its verdict would not be about pre-settlement hours.
Reason: The idea is active only in the 2 bars before each 00:00, 08:00 and 16:00 UTC settlement, and nothing in the catalogue reads the hour of day. `WeekdayComponent` gives only the weekday. `FundingRateMeanReversionComponent` fires on the settlement bar itself, not before it, depends on the funding feed and is on/off. No combination of these marks the hours 22-23, 06-07 or 14-15 UTC, even though the timestamp is in the coin's own bars and a regime rule could hold that condition.
