---
idea: 039-02_agitated-high-close-next-day-giveback
brief: 039_agitated-close-location-next-day-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: an agitated market, with the close's place in the day's high-low range -> kept: the profile is added by code, and the close location is measured as stated.
- Comparison: higher close against lower close in the range -> adapted: the forecast is graded by close location, centred on its usual level.
- Outcome: a larger fall over the next day, the higher the close -> kept: the next-day return over 1 bar, short when the close is high.
- Verdict transfer: yes: the forecast is the idea's graded close location, read against the next day's move, inside the idea's agitated profile.
Forecast: The forecast uses CloseLocationInRangeComponent with reference "high", which gives 0 when the close is at the day's high and 1 when it is at the low. It is standardised over 60 bars (min_periods 20), which gives about 20 x location, capped at 20. A standardised constant (BuyAndHoldStrategy, negated to -10) is added at equal weight. The forecast is therefore (x − 10) / 2, between about -5 and +5: - it is 0 for a mid-range close; - it is negative (short) when the close sits in the upper half, larger the nearer the high; - it is positive (long) when the close sits in the lower half, larger the nearer the low. The agitated-profile regime is added by code, and the book is flat outside it.
Config: 039-02_agitated-high-close-next-day-giveback_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the coin's next-day return, minus that coin's mean daily return over all its windows, on the bar's forecast. It uses all bars in the profile with a non-zero forecast, one sample per bar, inside each window. Its t is computed with the cases of one day taken together.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2: the lower the close, the better the next day; the higher the close, the larger the fall.
- Reject: The slope is negative with t ≤ -2: a high close is followed by a stronger next day, so the pressure continues.
- Inconclusive: Any t between -2 and 2 is inconclusive. Fewer than 500 bars in the profile, or fewer than 250 distinct days, is also inconclusive.
