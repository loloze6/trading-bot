---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: a coin's close near its 52-week closing high, only while its 30-day return is positive, larger with a higher 30-day return and a greater distance above the 52-week low -> kept: "only while 30-day return positive" is the idea's own condition, so it is a regime; the rest is graded on 8760- and 720-bar hourly closes.
- Comparison: near the high against far below it, and standing aside against shorting -> kept: the position shrinks toward zero far below the high, and it is zero, never short, outside the state.
- Outcome: a higher return over the next 7 days -> adapted: the 7-day holding period is dropped, and the forecast is judged on 168-bar forward returns.
- Verdict transfer: yes: the forecast grows with each of the idea's three quantities, only inside its stated state, and it is judged on the idea's own horizon.
Forecast: The forecast is active only while the 720-bar (30-day) return is above 0. On other bars it is flat. Inside that state it is the equal-weight mean of two standardised parts: - (a) HighProximityMomentum: the 720-bar return times (1/(1+D))², where D is the percent distance below the 8760-bar (52-week) closing high. It is clipped at 0 and grows with the 30-day return and with closeness to the high. - (b) the percent distance of the close above its 8760-bar lowest close. It grows the further the close sits above the low. Both parts are at least 0, so the forecast is long-only. It is larger when the coin is nearer its high, the 30-day return is higher, and the close sits further above its low. Each part uses standardise with window 500 and min_periods 120.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: On a non-overlapping 168-bar grid in each window, regress the coin's 168-bar forward return on the forecast, pooled over coins and windows. The forward return is taken minus that coin's mean 168-bar return over all its windows (holding the coin). The slope's t is the measure.
- Supporting check: On grid bars with forecast > 0, the mean excess 168-bar forward return (same benchmark) is above 0.
- Confirm: The slope's t is ≥ 2 and the supporting check passes.
- Reject: The slope's t is ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the check failing, is inconclusive. A decision needs at least 300 non-overlapping grid cases with forecast > 0; with fewer, the result is inconclusive.
