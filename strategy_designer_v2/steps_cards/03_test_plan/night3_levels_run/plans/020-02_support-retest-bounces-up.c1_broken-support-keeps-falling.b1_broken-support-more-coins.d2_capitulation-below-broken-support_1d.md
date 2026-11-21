---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d2_capitulation-below-broken-support
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: daily close just below prices where it turned up several times in the past 90 days, after a steep 20-day fall -> adapted: "several turns" (3 or more 90-day swing lows within 2 % of the nearest one above the close) and "a 20-day fall" are the regime condition; "just below" and "steep" become graded sizes.
- Comparison: the deeper its 20-day fall, the larger the rise -> kept: the position grows with the depth of the 20-day fall.
- Outcome: it rises over the next 20 days -> kept: 20-bar horizon, long side.
- Verdict transfer: yes: the regime is exactly the idea's situation and the forecast grades by its stated strengths, so a 20-bar rise beyond drift confirms it and a 20-bar fall rejects it.
Forecast: Two detector measures pick the bars. The first counts the 90-day swing lows (side 2) lying within 2 % of the nearest swing low at or above the close. The second is the 20-day percent change of the close. The bar is mean_reversion when that count is 3 or more and the 20-day change is below 0. All other bars are flat. On mean_reversion bars the forecast is the equal-weight mean of two parts: - the support proximity, which is the count times 1/(1 + percent distance below that level), standardised over 90 bars; - the 20-day fall depth, which is the negated 20-day price change standardised over 60 bars and clipped at 0. The forecast is never negative. It grows the closer the close sits under a well-touched support and the deeper the 20-day fall.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d2_capitulation-below-broken-support_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The mean unusual move over 20 bars of the cases: the coin's 20-bar return from each signal bar minus its normal drift, on the non-overlapping 20-bar grid of each window, pooled over all coins.
- Supporting check: Among the cases, the slope of the 20-bar unusual move on the case's 20-day fall depth (the fall_depth raw value, negated) is positive.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 independent cases, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, a confirming t with a slope at or below 0, or fewer than 30 independent cases.
