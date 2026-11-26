---
idea: 039-01_agitated-low-close-next-day-rebound
brief: 039_agitated-close-location-next-day-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in an agitated market, where the coin closes within its day's high-low range -> kept: the close's place in the day's range, from the day's high (0) to its low (1); the agitated profile is added by code.
- Comparison: the lower the close, the larger the rise -> adapted: graded against the coin's own usual close location; long below it, short above it.
- Outcome: the coin rises over the next day, more after lower closes -> kept: next-day return, horizon 1 day = 1 bar.
- Verdict transfer: yes: a graded close-location bet held for one day inside the agitated profile is the idea itself, so its slope's sign confirms or rejects it.
Forecast: One component, CloseLocationInRangeComponent with reference "high", reads (high - close) / (high - low): 0 at the day's high, 1 at its low. Standardise (window 60, min_periods 20) puts it near +10 at its usual level, up to 20 for a close at the low, and near 0 for a close at the high. A constant (BuyAndHoldStrategy, standardised then negated, -10) at equal weight centres it, so the forecast is (x - 10) / 2. It runs from about -5 to +5 and is graded throughout. It is positive (long) when the close sits lower in the range than usual, more so the nearer the low. It is negative (short) when the close sits higher than usual, and 0 at the usual location. The code keeps it flat outside agitated bars.
Config: 039-01_agitated-low-close-next-day-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of next-day return on the forecast. The sample is the bars with a non-zero forecast, all coins and windows pooled. The return is close[t+1]/close[t]-1 within a window, minus the coin's mean daily return over all windows. The slope's t treats the cases of one day as one piece of evidence: their deviations are summed per day.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise (the timing part), is above 0.
- Confirm: The slope is positive with t >= 2 and the timing part is above 0.
- Reject: The slope is negative with t <= -2: the next day rises more after higher closes.
- Inconclusive: Any slope with t between -2 and 2, or a confirming slope with a timing part at or below 0. At least 300 bars with a non-zero forecast, falling on at least 150 distinct days, are needed; with fewer, the result is inconclusive.
