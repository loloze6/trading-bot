---
idea: 060-02_falling-calm-close-above-low-fade
brief: 060_falling-calm-wide-high-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling, calm market, a day's close sits above that day's low, measured against the coin's 30-day swing of daily returns -> kept: (close − low)/close over the 30-day return std, built as the day's range in usual moves minus its high-to-close drop in usual moves; the profile is added by code.
- Comparison: the distance against the coin's 30-day swing of daily returns -> kept: both parts divide by the std of the last 30 daily returns.
- Outcome: the price falls over the next day, more as the distance grows -> kept: a short that grows with the distance, held 1 bar.
- Verdict transfer: yes: a graded short on this distance that earns the next-day fall confirms the idea, and one that loses it rejects the idea.
Forecast: Two components on daily bars, both using a 30-day return swing. The first is RangeInReturnStd (vol_period 30), the day's range (high − low)/close in usual moves. The second is VolatilityScaledDistanceFromHigh (period 1, source high, exclude_current 0, base close, vol_period 30), which is −(high − close)/close in usual moves. Each component is standardised over 60 bars (min_periods 20), then negated, with equal weights. The forecast is −(range term − high-to-close term)/2. It grows more negative (a larger short) the further the close sits above the day's low against the usual swing. It is most negative when a wide day closes at its high. It is near zero, or slightly positive, when the close sits at the low. The book holds nothing outside the falling calm profile, which code adds.
Config: 060-02_falling-calm-close-above-low-fade_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The per-bar position gain before costs, net of the market's drift. This is the position held × (next-day return − the coin's mean daily return over all its windows), on bars in a position. Its t is computed with the cases of one day summed together.
- Supporting check: On bars in a position, the forecast must correlate positively with the next-day excess return (lower forecast, lower next-day return), with correlation t ≥ 2 counted by day.
- Confirm: The mean drift-adjusted position gain is above 0 with t ≥ 2, and the supporting check passes, over at least 100 days in a position.
- Reject: The mean drift-adjusted position gain is below 0 with t ≤ −2, over at least 100 days in a position.
- Inconclusive: A t between −2 and 2, or a confirming main measure whose check fails, or fewer than 100 days in a position.
