---
idea: 064-02_choppy-range-top-break-continuation
brief: 064_choppy-market-up-days-carry-one-way
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy market, a close above the highest close of the past 30 days -> kept: a regime rule on the close's distance above the prior 30-day closing high (> 0); the choppy profile is added by code
- Comparison: how far the close sits above the old high, in units of its 30-day daily swing -> kept: the distance above the prior high over the 30-day standard deviation of daily returns, which grades the forecast
- Outcome: the coin rises further over the next 5 days, more after a larger clearance -> kept: long, held 5 bars
- Verdict transfer: yes: the test measures the same breakout, scaled the same way, in the same market and over the same horizon as the idea.
Forecast: The forecast uses `VolatilityScaledDistanceFromHighComponent` with period 30, vol_period 30, source "close", exclude_current 1 and base "level". It computes (close − highest of the prior 30 closes) / that high / std of the last 30 daily returns. The regime detector reads the same quantity. Above 0 (a close over the old 30-day closing high), the bar is "trending". Every other bar is "unknown", and that regime is flat. Inside the regime the forecast is the standardised distance (60/20), clipped at 0. It is long only, and it grows continuously from 0 at the old high, larger the more usual daily moves the close clears it by. Outside a breakout it is exactly 0. Code adds the choppy profile on top.
Config: 064-02_choppy-range-top-break-continuation_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case. A case is a bet, a rise of the forecast of at least the band, read once per 5-bar grid cell. The unusual move is the coin's return from the signal bar's close over 5 bars, minus the coin's normal 5-bar drift over all windows. Its mean and t are taken with cases of the same day pooled.
- Supporting check: Across cases, the forecast at the signal bar is positively related to that 5-bar unusual move. This is the slope of the unusual move on the forecast, with t ≥ 2.
- Confirm: The mean unusual move is above 0 with t ≥ 2, on at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ −2, on at least 30 cases.
- Inconclusive: Any t between −2 and 2. A positive main measure whose supporting slope has t < 2 is also inconclusive. Fewer than 30 cases, or fewer than 20 distinct days, is too few to decide either way.
