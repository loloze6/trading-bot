---
idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise, in usual daily moves, in a coin whose 90-day return is positive -> kept: a regime on the sign of the 90-day return, plus the one-day return divided by the 20-day volatility of daily returns, long side only.
- Comparison: the larger the one-day rise, the larger what follows -> kept: the position grows linearly with the size of the rise in usual moves.
- Outcome: the price rises over the next 10 days -> kept: each bet is held for 10 daily bars.
- Verdict transfer: yes: the regime, the graded rise and the 10-day hold measure the idea as stated, so a confirm or a reject carries over.
Forecast: The regime detector computes the 90-day percent return (PriceEvolutionComponent, period 90). When it is above 0 the bar is "trending"; on every other bar the forecast is 0. In "trending" the one component is today's return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). It is standardised over 60 bars (min 20) and clipped at 0. The forecast is therefore 0 on down days and in coins with a non-positive 90-day return. On up days it is positive and grows linearly with the size of the rise in usual moves, up to the cap of 20. It is never negative.
Config: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The unusual move over the cases. A case is a forecast rise of at least 2 points, read once per 10-bar grid cell. Its unusual move is the coin's 10-bar return from the signal bar's close minus the coin's normal 10-bar drift over all windows. Take the mean of the unusual moves over all cases and its t.
- Supporting check: Across the cases, regress the unusual move on the case's forecast (the size of the rise). The slope must be positive.
- Confirm: The mean unusual move is positive with t ≥ 2, and the slope on the forecast is positive.
- Reject: The mean unusual move is negative with t ≤ -2, meaning sharp rises in rising coins are faded.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a slope that is not positive. At least 30 cases are required across coins and windows; with fewer, the result is inconclusive.
