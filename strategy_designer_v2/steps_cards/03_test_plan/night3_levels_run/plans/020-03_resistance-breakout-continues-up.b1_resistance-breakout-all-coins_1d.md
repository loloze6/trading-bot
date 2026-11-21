---
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: the count threshold ("several") becomes graded by touch count x the close's margin above the level, on the bar the level is crossed (90-bar window, swing highs on closes).
- Comparison: the more times the level held, the larger the rise -> kept: the forecast grows with the number of swing highs at the level.
- Outcome: keeps rising over the next 5 days -> kept: the book holds each long bet for 5 daily bars.
- Verdict transfer: yes: the forecast is non-zero only on fresh closes through repeatedly-turned levels, sized by their touch count, so its 5-day result is the idea's result.
Forecast: The forecast uses one indicator, ResistanceBreakTouchCountComponent (period 90, side 2, band 2, cross_period 1). A swing high is a close that is at or above the 2 closes before it and above the 2 closes after it, within the last 90 daily bars. The component looks for the highest such level that the close crossed upward on this bar (yesterday's close at or below it, today's close above it). It counts the swing highs within 2 % of that level (N) and outputs N x the close's percent margin above the level. It is 0 on every bar without a fresh break, and never negative, so the forecast is long-only. It is standardised against its past 90 values (min_periods 22). The forecast is positive only on a break bar, and its size grows with how many times the level turned price down and how far the close cleared it.
Config: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean unusual move per case. A case is a long bet: a rise of the forecast of at least 2 points, counted once per 5-bar grid cell. Its unusual move is the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows. The test is the ordinary t of that mean, pooled over coins and windows.
- Supporting check: Split the cases at the median of their signal-bar forecast. The mean unusual move of the upper half minus that of the lower half must be positive (Welch t >= 1).
- Confirm: The mean unusual move is > 0 with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is < 0 with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive main result whose supporting check fails is also inconclusive. So is any result with fewer than 30 cases.
