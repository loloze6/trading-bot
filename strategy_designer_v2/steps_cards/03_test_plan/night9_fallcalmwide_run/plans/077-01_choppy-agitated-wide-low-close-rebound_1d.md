---
idea: 077-01_choppy-agitated-wide-low-close-rebound
brief: 077_choppy-agitated-wide-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a wide day closing near its low, in a choppy, agitated market -> adapted: the condition is the regime (range at or above its 30-day mean bar range, close in the bottom quarter of the range, inside the code-built profile), and the forecast is graded inside it.
- Comparison: the day's range against its 30-day swing, and the close's nearness to the low -> kept: the day's range in 30-day return standard deviations, times (high − close) / (high − low).
- Outcome: a rise over the next day, larger the wider and lower the close -> kept: a long position sized by that product, held 1 bar.
- Verdict transfer: yes: the book is long only on wide low-close days in the profile, sized by width and low-close nearness, and judged on the next day's excess return.
Forecast: The regime is `mean_reversion` only on a wide day that closes near its low. A wide day is one whose range is at or above its 30-day mean bar range (`RangeCompressionRatioComponent`, short 1, long 30, base "mean_bar_range", form "width", at least 1.0). Near its low means the close sits in the bottom quarter of the range (`CloseLocationInRangeComponent` "low", at most 0.25). On every other bar the book is flat, and the code-added choppy-agitated profile vetoes keep it flat outside the profile. Inside the regime the forecast comes from `VolatilityScaledDistanceFromHighComponent` (period 1, source "high", exclude_current 0, base "close", vol_period 30). Its raw value is −(high − close)/close/s30, which equals −(the range in 30-day usual moves) × (the close's nearness to the low). It is standardised over 60 bars and then negated, so it is always positive (long only). It grows continuously with the day's width against its 30-day swing and with how near the close sits to the low.
Config: 077-01_choppy-agitated-wide-low-close-rebound_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On case bars (forecast > 0), the coin's next-day return (close[t+1]/close[t] − 1) minus the coin's mean daily return over all its windows. The measure is the mean of this excess over the cases, with its t computed with cases clustered by day.
- Supporting check: The slope of next-day excess return on the forecast's size across the cases is above 0.
- Confirm: The idea is confirmed when the mean next-day excess return is above 0 with t ≥ 2 and the slope on forecast size is above 0.
- Reject: The idea is rejected when the mean next-day excess return is below 0 with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is a confirming mean with a slope at or below 0. Any result from fewer than 30 distinct case days is also inconclusive.
