---
idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: in a coin with a negative 90-day return, a one-day rise that is large in units of its 20-day standard deviation of daily returns -> adapted: the 90-day fall is kept as a regime condition, and "large" is made graded by the one-day return over its 20-day standard deviation with a steep dead zone.
- Comparison: the largest bounces of several usual moves against ordinary rises, which are followed by almost nothing -> kept: the position grows steeply with the rise in usual moves and is near zero for ordinary up days.
- Outcome: a fall over the next 5 days -> kept: each short is held 5 bars and judged on the coin's 5-day return.
- Verdict transfer: yes: the test bets against the bounces only in falling coins, sized by the bounce in usual moves, and judges them over 5 days, so its result is the idea's result.
Forecast: The forecast is active only when the coin's 90-day return is below 0. On every other bar it is 0. While active, it reads the day's return divided by the 20-day standard deviation of daily returns, standardised against its own past 60 values. Down days are clipped to 0. The remaining rise goes through a cubic dead zone (exponent 3, pivot 20) and is then negated, so the forecast is never positive. An ordinary up day gives almost 0: half a usual move gives about -0.6. One usual move gives about -5, and about 1.6 usual moves or more gives the full -20 (200 percent short). The short grows steeply with the bounce's size in usual daily moves.
Config: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Each case is a short bet: the forecast falls by at least 2 points on the short side, read once per 5-bar grid cell. For each case, measure the coin's 5-bar return from the signal bar's close minus the coin's normal 5-bar drift (holding the coin), in the short direction. Report the mean over all cases and its t, before costs.
- Supporting check: The mean unusual move of cases with forecast at or below -10 is above that of cases with forecast between -2 and -10, so the largest bounces are given back more.
- Confirm: The mean unusual move is positive (prices fall more than the drift) with t of 2 or more, and the supporting check passes.
- Reject: The mean unusual move is negative with t of -2 or less: bounces in falling coins are followed by rises beyond the drift.
- Inconclusive: Any t between -2 and 2, or a confirming t with a failed supporting check, is inconclusive. So is any result with fewer than 30 cases, or fewer than 10 cases at forecast -10 or below.
