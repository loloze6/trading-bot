---
idea: 025-01_downtrend-bounce-given-back
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a coin with a negative 90-day return has a one-day rise that is large against its 20-day standard deviation of daily returns -> adapted: the negative 90-day return is a regime condition, and "large" is made graded as the rise in usual moves with a cubic dead zone.
- Comparison: the rise is judged against the usual daily move, its 20-day standard deviation -> kept.
- Outcome: a fall over the next 5 days, larger the larger the rise in usual moves -> kept: a short sized by the scaled rise, held 5 bars.
- Verdict transfer: yes: the test measures the scaled rise, in falling coins only, against the 5-day move that follows, so a confirm or a reject carries straight to the idea.
Forecast: On bars where the coin's 90-bar return is below zero (regime `mean_reversion`), the forecast reads the day's return divided by the standard deviation of the last 20 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 20). It is standardised over 60 bars (min 20) and clipped at 0, so only rises count. It then goes through `signed_power` exponent 3 (pivot 10), so ordinary rises are pushed close to 0 and big ones are amplified. Finally it is negated, so the forecast is a short that grows with the size of the rise in usual moves. It is zero on down days, near zero on small rises, and zero whenever the 90-day return is not negative (other regimes are null). It is never positive.
Config: 025-01_downtrend-bounce-given-back_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are short bets: a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close minus the coin's mean 5-bar return over all windows, in the short direction. The measure is the mean of this unusual move over all cases, with its t against 0, before costs.
- Supporting check: Split the cases at the median of the absolute forecast. The mean short-direction unusual move of the larger half minus that of the smaller half must be greater than 0.
- Confirm: The mean short-direction unusual move is positive with t >= 2, and the larger-forecast half shows a larger unusual move than the smaller half.
- Reject: The mean short-direction unusual move is negative with t <= -2, meaning the coins rose more than their drift after these bounces.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirming t whose larger half does not exceed its smaller half. The test also needs at least 30 cases across all coins and windows; with fewer it is inconclusive.
