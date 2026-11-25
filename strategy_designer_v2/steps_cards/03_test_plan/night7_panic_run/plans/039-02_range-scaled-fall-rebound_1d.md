---
idea: 039-02_range-scaled-fall-rebound
brief: 039_scaled-one-day-falls-rebound-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f9d41455da54
---
Fidelity:
- Situation: a down day, sized by its fall in units of the 30-day average daily high-to-low range -> kept: the regime holds only down days, and inside it the fall is divided by the 30-day mean of (high-low)/close.
- Comparison: next-day return after ordinary days, and against holding the coin -> kept: next-day return measured net of the coin's mean daily return.
- Outcome: the coin rises over the next day, more so after larger scaled falls -> kept: the 1-day forward return, long and growing with the scaled fall.
- Verdict transfer: yes: the forecast is the idea's scaled fall on down days only, held for one day, so the test's result is the idea's result.
Forecast: The regime detector checks the day's 1-day return. On a down day (return below 0) the bar is in the active regime. On any other day the book is flat. Inside the regime, the forecast comes from `MeanAbsScaledReturnComponent` (`period` 1, `window` 30, `base` "mean_relative_range"). This is the day's return divided by the 30-day mean of (high-low)/close. It is standardised over 60 bars, then negated and clipped at 0. The forecast is therefore positive (long) and zero only for a flat move. It grows linearly with the size of the fall in usual daily ranges: a fall of average size reads about +10, and the cap is +20. It is never negative.
Config: 039-02_range-scaled-fall-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On down-day bars (forecast > 0), the slope of the next-day return (close[t+1]/close[t]-1, minus the coin's mean daily return over all its windows) on the forecast. Cases from all coins are pooled, and the t-statistic is computed with the cases of one day taken together.
- Supporting check: Take the down-day bars in the top quintile of forecast. Their mean next-day excess return must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the top-quintile mean excess next-day return is above 0.
- Reject: The slope is negative with t ≤ -2. Separately, the top-quintile mean excess next-day return being negative with t ≤ -2 also rejects the idea, since the largest scaled falls would then be followed by further declines.
- Inconclusive: Any other result, including a slope with |t| < 2 or a positive slope with a top-quintile mean at or below 0. At least 300 down-day cases on at least 150 distinct days are required; below that the result is inconclusive.
