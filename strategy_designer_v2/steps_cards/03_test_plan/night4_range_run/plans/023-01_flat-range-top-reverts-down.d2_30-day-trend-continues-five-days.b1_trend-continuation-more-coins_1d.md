---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the coin's 30-day net move is large against its 30-day high-low range -> kept: a regime rule on NetMoveToRangeRatio (30 bars, high-low) at 0.5 or more, the conventional midpoint of its 0-to-1 scale.
- Comparison: the larger the 30-day return, the further the move -> kept: the forecast is the 30-day return, standardised, so the position grows with it.
- Outcome: the price moves further in the 30-day return's direction over the next 5 days -> kept: each bet is held 5 daily bars, long after a rise and short after a fall.
- Verdict transfer: yes: the test bets the 30-day direction, sized by the 30-day return, only in high net-move-to-range coins, over 5 days, as the idea states.
Forecast: The forecast is active only on bars where the 30-day net move covers at least half of the 30-day high-low range (NetMoveToRangeRatioComponent, period 30, source high_low). It is flat on all other bars. On active bars the forecast is the 30-day percent return (PriceEvolutionComponent, period 30), standardised against its 60 past values (min_periods 20). It is positive after a 30-day rise and negative after a 30-day fall. Its size grows in proportion to the size of the return, capped at ±20. The regime is used because the idea is itself a condition ("in a coin whose net move has been large").
Config: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Pooled over all coins and windows, on the non-overlapping 5-bar grid of each window, use the bars in the trending regime with a nonzero forecast. Regress the coin's 5-bar forward return, minus that coin's mean 5-bar return over all its windows, on forecast / 10. Report the t of the slope.
- Supporting check: On the same cases, the mean unusual move in the forecast's direction (the 5-bar return minus the coin's drift, times the forecast's sign) is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check's mean is above 0.
- Reject: The slope's t is -2 or less, meaning larger 30-day returns are followed by larger moves against them.
- Inconclusive: A slope t strictly between -2 and 2 is inconclusive. A slope t of 2 or more with a mean directional unusual move at or below 0 is also inconclusive. Any result from fewer than 100 grid cases in the regime is inconclusive.
