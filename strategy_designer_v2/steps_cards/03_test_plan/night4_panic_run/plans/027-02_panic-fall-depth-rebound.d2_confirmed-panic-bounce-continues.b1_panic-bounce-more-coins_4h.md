---
idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: cb945cd336ee
---
Fidelity:
- Situation: a 24-hour stretch whose range is several times its 30-day average and in which the coin fell -> kept: a regime rule on the 6-bar range in multiples of its 180-bar mean, during a 6-bar fall, read for the stretch that ended 6 bars before the current bar (a multiple of 3 or more).
- Comparison: the larger the coin's rise over the 24 hours after the stretch -> kept: the 6-bar return from the stretch's end to the current bar.
- Outcome: a higher return over the following 14 days -> kept: each bet is held 84 bars from the end of the bounce.
- Verdict transfer: yes: the test measures exactly whether, among panic stretches, a larger 24-hour bounce is followed by a higher 14-day return.
Forecast: The regime is active only on a bar where the 24h stretch that ended 24h earlier (bars t-11 to t-6) qualifies as a panic. A qualifying stretch has a range of at least 3 times its 30-day average 24h range (FallGatedRangeMultipleComponent, period 6, base_period 180, fall_period 6, lag 6), and its close is below the close 24h before it. On every other bar the forecast is 0. On panic bars the forecast is the 24h bounce since the stretch's end, close[t]/close[t-6]-1 (PriceEvolutionComponent, period 6). It is standardised against its own past 60 values and clipped at 0. So it is long, growing with the size of the bounce, and zero when the coin kept falling.
Config: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: Cases are the first mean_reversion-regime bar in each 84-bar grid cell of each window. For each case, take the 84-bar forward return minus the coin's mean 84-bar return over all its windows. Measure the slope of that excess return on the recorded raw bounce (`debug_info.components.bounce.last_history_value`), pooled over all coins and windows, with its t.
- Supporting check: none
- Confirm: The slope is positive with t >= 2, on at least 30 cases.
- Reject: The slope is negative with t <= -2, on at least 30 cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 cases.
