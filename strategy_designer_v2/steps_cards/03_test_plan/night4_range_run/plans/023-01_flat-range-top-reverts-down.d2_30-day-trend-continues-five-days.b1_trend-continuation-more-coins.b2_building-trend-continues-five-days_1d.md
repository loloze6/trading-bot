---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 10d8cbead801
---
Fidelity:
- Situation: the 30-day net move is a moderate share of the 30-day high-low range -> adapted: "moderate" is made graded by the hump s(1−s) on the net-move share s.
- Comparison: the larger the 30-day return, and the nearer the share sits to the middle of its scale, the larger the move -> kept: the forecast is the 30-day return × s(1−s), which is largest at s = 0.5 and 0 at s = 1.
- Outcome: the coin moves further in its 30-day direction over the next 5 days -> kept: 5 bars, signed like the 30-day return.
- Verdict transfer: yes: the forecast is the idea's own product of the return and the share hump, so a reliable link between that forecast and the next 5 days' move confirms the idea, and a reliably reversed link rejects it.
Forecast: The forecast uses one indicator, RangeShareHumpWeightedReturnComponent with period 30. Its raw value is R × s × (1−s): - R is the 30-day simple return. - s is the absolute 30-day net move divided by the 30-day high-low range, capped at 1. The raw value is standardised against its own past 60 values (target 10, cap 20), with no regime and no dead zone. - It is positive after a net 30-day rise and negative after a net fall. - It is 0 when there is no net move or when the move spans the whole range. - Its size grows with the size of the return. - Its size also grows as s approaches 0.5, and it fades as s nears 1.
Config: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, pooled over coins and windows: - Take the coin's 5-bar forward return close[t+5]/close[t]−1, minus the coin's mean 5-bar return over all its windows (its drift). - Regress that excess return on the forecast at bar t, and read the slope's t.
- Supporting check: The book's timing gain must be above 0. It is the book's mean daily return before costs minus its gain from the market's own rise.
- Confirm: The idea is confirmed only when both hold: - the slope's t is 2 or more, on at least 300 grid cases with a non-zero forecast; - the timing gain is above 0.
- Reject: The slope's t is −2 or less on at least 300 grid cases with a non-zero forecast.
- Inconclusive: The idea is neither confirmed nor rejected in these cases: - the slope's t is between −2 and 2; - the t is 2 or more but the timing gain is 0 or below; - there are fewer than 300 grid cases with a non-zero forecast.
