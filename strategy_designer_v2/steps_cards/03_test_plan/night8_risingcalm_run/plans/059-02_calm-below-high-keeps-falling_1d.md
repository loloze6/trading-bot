---
idea: 059-02_calm-below-high-keeps-falling
brief: 059_calm-market-steady-declines-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: close below its highest close of the past 14 days, in units of its 30-day daily swing -> kept
- Comparison: the 14-day highest close, scaled by the coin's own 30-day daily swing -> kept
- Outcome: the deeper the scaled decline, the larger the fall over the next 5 days -> kept
- Verdict transfer: yes: the forecast is the idea's own swing-scaled depth below the 14-day high, shorted in proportion over 5 days inside the calm profile, so its result is the idea's result.
Forecast: One indicator, `VolatilityScaledDistanceFromHighComponent` with period 14, vol_period 30, source close and the current bar included (exclude_current 0), on the level base. Its raw value is (close − highest close of the last 14 days) / that high / the standard deviation of the last 30 daily returns. It is 0 at a new 14-day closing high and never positive. It grows more negative as the close sinks below the high in usual daily moves. It is standardised against its own past 60 values (target 10, cap 20), so the sign is kept: the forecast is 0 at the high and a short position that grows with the depth of the decline, about −10 at a usual depth and down to −20 at twice it. It is never long. The calm profile is added by code, so the book is flat outside calm markets.
Config: 059-02_calm-below-high-keeps-falling_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, over in-profile bars, take each coin's 5-bar forward return minus that coin's mean 5-bar return over all windows (holding the coin). Regress it on the bar's forecast and read the t of the slope. A positive slope means more negative forecasts are followed by larger falls than usual.
- Supporting check: The mean unusual move over the cases (forecast rises on the short side of at least 2 points) is positive in the short direction.
- Confirm: The slope is positive with t ≥ 2, and the supporting check is positive.
- Reject: The slope is negative with t ≤ −2, meaning deeper declines are followed by rebounds against the drift.
- Inconclusive: Any slope t between −2 and 2, or a confirming slope with a non-positive supporting check. Fewer than 150 grid cases in profile with a non-zero forecast, over the six coins, is also inconclusive.
