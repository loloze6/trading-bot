---
idea: 060-01_falling-calm-wide-high-close-fade
brief: 060_falling-calm-wide-high-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling calm market, a day with a wide high-to-low range that closes near its high -> adapted: the falling calm profile is added by code; "wide" and "near its high" become a regime (range of at least 2 daily-return standard deviations, close in the top quarter of the day's range), and inside it the forecast is graded by width and close location.
- Comparison: the range against the coin's 30-day swing of daily returns -> kept: the day's range as a share of the close, divided by the 30-day standard deviation of daily returns.
- Outcome: a fall over the next day, larger the wider the day and the closer the close to the high -> kept: a short held 1 bar, sized by both measures.
- Verdict transfer: yes: the test bets short on exactly these days, sized by width and close location, so its next-day result is the idea's.
Forecast: The forecast is zero except on days the detector marks as the situation. Those are days where the day's range, measured in units of the 30-day daily-return standard deviation (`RangeInReturnStdComponent`, 30), is at least 2.0, and the close sits in the top quarter of the day's range (`CloseLocationInRangeComponent`, reference "low", at least 0.75). The code adds the falling calm profile on top of this. On such days the forecast is the equal-weight mean of the two measures, each standardised against its own past 60 values and then negated. The forecast is therefore short, about -12 to -20. It grows more negative the wider the day is against its usual swing and the nearer the close sits to the high. It is never positive.
Config: 060-01_falling-calm-wide-high-close-fade_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The unusual move per case, in the signal's direction (short). A case is a bar with forecast below 0. The unusual move is the next-day return close[t+1]/close[t]-1 minus the coin's mean daily return over all its windows, then negated. It is averaged over cases, with a t computed with cases of the same day summed together.
- Supporting check: Across cases, the least-squares slope of the per-case unusual move on |forecast| is above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the slope is above 0.
- Reject: The mean unusual move is below 0 with t ≤ -2, meaning the coin rises more than usual the next day. Or the slope of the unusual move on |forecast| has t ≤ -2, meaning the weakness shrinks with width and high close.
- Inconclusive: Any other result counts as neither confirm nor reject. So does a test with fewer than 30 cases or fewer than 30 distinct days.
