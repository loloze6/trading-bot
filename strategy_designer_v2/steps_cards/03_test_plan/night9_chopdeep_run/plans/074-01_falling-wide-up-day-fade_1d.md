---
idea: 074-01_falling-wide-up-day-fade
brief: 074_falling-market-wide-up-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling market, an up day with a wide high-to-low range against the past 20 days' average range -> adapted: the falling market is the brief's profile, added by code; "up day and range above its 20-day average" is a regime; inside it the size is graded by the range multiple.
- Comparison: the day's range against the coin's average daily range over the past 20 days -> kept: bar range over the mean bar range of the last 20 bars.
- Outcome: price falls over the next day, more the wider the range -> kept: a short held 1 bar, sized by the range multiple.
- Verdict transfer: yes: the book is short only on falling-market wide up days, sized by width, and held exactly the next day, so its next-day result answers the idea.
Forecast: The forecast is active only on bars that close above the prior close and whose high-to-low range exceeds its 20-day mean bar range, where the mean includes the current bar. The brief's falling profile is added by code, so the book is flat on every other bar. Inside that regime the forecast has two equal-weight parts. The first is the range multiple (range / 20-day mean range), standardised over its past 60 values and negated. The second is the constant +10 offset. The forecast is about -(x - 10)/2, where x is the standardised multiple. It is near 0 for a range just above average, about -5 at twice the usual width, and grows more negative as the day gets wider. It is short only, apart from a small positive value of under 2 forecast points just above the edge, which is too small to trade from flat.
Config: 074-01_falling-wide-up-day-fade_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Over the cases (bars with forecast <= -2), the coin's next-day return minus its normal daily drift, in the short direction (the unusual move). Its t is computed with the cases of one day taken together.
- Supporting check: Across the cases, the slope of the next-day return minus drift on the forecast must be positive (a more negative forecast is followed by a weaker next day), with t >= 1.
- Confirm: The mean unusual move is a fall, with t >= 2 over at least 30 case-days, and the supporting slope is positive with t >= 1.
- Reject: The mean unusual move is a rise (the next day is stronger than drift), with t <= -2 over at least 30 case-days.
- Inconclusive: Any other result counts as inconclusive. That covers t between -2 and 2, or a confirming mean whose slope check fails. It also covers fewer than 30 case-days, the minimum count of cases.
