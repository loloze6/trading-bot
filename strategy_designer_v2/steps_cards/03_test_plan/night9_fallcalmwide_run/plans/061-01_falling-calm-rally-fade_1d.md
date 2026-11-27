---
idea: 061-01_falling-calm-rally-fade
brief: 061_falling-calm-rally-next-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a coin's one-day rise, measured in standard deviations of its last 30 days' daily returns, in a falling calm market -> kept: the one-day return over its 30-day return std, kept only on up days (zero otherwise); the falling calm profile is added by code.
- Comparison: the rise against the coin's usual daily swing of recent weeks -> kept: the return is divided by the 30-day std of daily returns, today's return included.
- Outcome: the coin falls over the next day, more so the larger the rise -> kept: a short position, sized by the scaled rise, held 1 bar.
- Verdict transfer: yes: the short follows the scaled rise inside the profile, so its next-day result confirms or rejects the fade.
Forecast: One component, VolatilityScaledReturnComponent (period 1, vol_period 30). It is today's return divided by the 30-day standard deviation of daily returns. It is standardised over its past 60 values (min_periods 20), then clipped at 0 from below, then negated. The forecast is 0 on down and flat days. On up days it is negative (short), and the short grows linearly with the size of the rise in usual moves, capped at -20. It is never positive. Code keeps it at 0 outside the falling calm profile.
Config: 061-01_falling-calm-rally-fade_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use the cases: bars where the forecast falls by at least 2 points onto the short side, one per 1-bar grid cell. For each case, take the next-day return minus the coin's mean daily return over all windows, in the short direction (the unusual move). Report its mean and its t, with the cases of one day pooled.
- Supporting check: Split the cases at the median of |forecast|. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: Both must hold: the mean unusual move is above 0 with t >= 2, and the larger-half minus smaller-half difference is above 0.
- Reject: The mean unusual move is below 0 with t <= -2, which means the rises continue the next day.
- Inconclusive: Inconclusive cases: - a t between -2 and 2; - t >= 2 with a size difference at or below 0; - fewer than 100 cases; - cases on fewer than 50 distinct days.
