---
idea: 034-01_agitated-low-close-rebounds
brief: 034_agitated-close-location-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: an agitated market, a daily close sitting in its high-low range -> kept: the agitated profile is added by code, and the close's place in the day's range is read on every bar.
- Comparison: the nearer the close is to the day's low, the larger the rise -> adapted: graded around the close's usual place in the range (long when lower, short when higher).
- Outcome: the coin rises over the next day -> kept: one-bar horizon on daily bars.
- Verdict transfer: yes: the forecast is the idea's graded close location, read only in agitated bars, and judged on the next day's move.
Forecast: The forecast measures how near the close is to the day's low. It uses `CloseLocationInRangeComponent` with `reference` "high", which runs from 0 when the close is at the high to 1 when it is at the low. This value is standardised over its last 60 values (min_periods 20), so a usual reading is about +10, a close at the low is about 20, and a close at the high is 0. It is averaged at equal weight with the standardised constant at -10. The result is (x - 10) / 2: positive and growing as the close nears the low (up to about +5), negative as it nears the high (down to about -5), and 0 at the usual close location. The code's agitated profile keeps the book flat on calm bars.
Config: 034-01_agitated-low-close-rebounds_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with a non-zero forecast, the mean of forecast x (the next day's return minus the coin's mean daily return over all windows), as a t of the mean. Bars on the same day are summed into one case per day.
- Supporting check: The next-day return minus the coin's mean, for the top third of forecasts (lowest closes) minus the bottom third (highest closes), must be above 0 (Welch t).
- Confirm: The main measure has t >= 2 and the supporting check's difference is above 0.
- Reject: The main measure has t <= -2, meaning low closes are followed by further falls.
- Inconclusive: Any t between -2 and 2, or a main t >= 2 with the supporting difference at or below 0. The test needs at least 300 agitated days with a non-zero forecast; with fewer, the result is inconclusive.
