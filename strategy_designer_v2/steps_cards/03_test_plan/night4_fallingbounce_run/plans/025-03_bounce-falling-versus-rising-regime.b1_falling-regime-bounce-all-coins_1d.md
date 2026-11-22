---
idea: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a one-day rise of several usual daily moves -> adapted: graded size of the day's rise in units of the 20-day return std, with the strongest graded dead zone.
- Comparison: the same rise when the 90-day return is negative versus positive -> kept: the 90-day return's sign selects the regime.
- Outcome: the 5-day return is lower in falling markets, and the gap widens with the rise's size -> kept: the 5-bar forward return is compared between the two regimes, overall and for the larger rises.
- Verdict transfer: yes: both regimes see the same graded rise reading, so the gap between their next 5 days is the idea's claim measured directly.
Forecast: On every daily bar, the regime is set by the coin's 90-day percent return. - Falling regime (90-day return below 0): the component is the day's return divided by the std of the last 20 daily returns. It is standardised over 60 bars, clipped at 0 so only rises count, and passed through signed_power (exponent 3, pivot 20). The result is negated, so the forecast is short. It is near 0 on ordinary days and grows steeply with the size of the rise. - Rising regime (90-day return at or above 0): the same rise reading is used without the negation, so the forecast is long. - Down days and flat days: the forecast is 0 in both regimes. - Holding: each bet is held 5 bars.
Config: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are bets (a forecast rise of at least 2 points on its side), one per 5-bar grid cell, with all coins and windows pooled. For each case, take the coin's 5-bar return from the signal bar's close minus the coin's mean 5-bar return over all windows (its unusual move). The measure is the mean unusual move of mean_reversion cases minus that of trending cases, tested with Welch's t.
- Supporting check: The same difference is computed again on only the cases whose rise reading (`last_history_value`) is above its pooled median. It must be more negative than the difference on all cases.
- Confirm: Welch t ≤ -2 on the main difference, and the supporting check passes.
- Reject: Welch t ≥ +2 on the main difference, meaning bounces in falling markets are followed by higher 5-day returns than bounces in rising markets.
- Inconclusive: Any t between -2 and +2 is inconclusive, as is a main t ≤ -2 whose supporting check fails. A test with fewer than 30 cases in either regime is also inconclusive.
