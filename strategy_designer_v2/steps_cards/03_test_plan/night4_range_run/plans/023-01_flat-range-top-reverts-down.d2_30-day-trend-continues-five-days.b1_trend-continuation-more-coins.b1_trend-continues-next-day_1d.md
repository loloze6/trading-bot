---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: 30-day net move large relative to the 30-day high-low range -> kept: a regime rule on NetMoveToRangeRatio(30, high_low) at or above 0.5.
- Comparison: the larger the 30-day return, the further the move -> kept: the position grows with the standardised 30-day return.
- Outcome: the price moves further in the 30-day direction over the next day -> kept: held 1 bar, long after a rise and short after a fall.
- Verdict transfer: yes: the test bets the 30-day direction, sized by the 30-day return, only in high net-move-to-range coins, over the next day.
Forecast: The regime detector computes the 30-bar net move over the 30-bar high-low range. When it is 0.5 or more (the conventional "net move spans at least half the range"), the bar is `trending`. Otherwise it is `unknown`, which is flat. In `trending`, the forecast is the 30-bar percent return, standardised against its own last 60 values. It is positive after a 30-day rise and negative after a fall, and it grows with the size of the return, capped at ±20. It is 0 outside the trending condition.
Config: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d_config.json
Criterion:
- Horizon: 1 bars
- Main measure: The slope of the next-day excess return on the forecast, pooled over all coins and windows, on `trending` bars with a non-zero forecast. The excess return is close[t+1]/close[t]−1 minus the coin's mean daily return over all its windows. The slope is fitted with an OLS t.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2, so larger same-direction forecasts are followed by larger same-direction excess moves.
- Reject: The slope is negative with t ≤ −2, so the next-day move goes against the 30-day direction.
- Inconclusive: Any t between −2 and 2. Also inconclusive: fewer than 300 trending bars with a non-zero forecast in total.
