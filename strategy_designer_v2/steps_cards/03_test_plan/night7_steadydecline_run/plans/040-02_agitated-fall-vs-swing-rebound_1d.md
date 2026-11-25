---
idea: 040-02_agitated-fall-vs-swing-rebound
brief: 040_agitated-big-fall-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: in an agitated market, a coin's one-day fall -> kept: the agitated profile is added by code, and the fall is the day's close-to-close return.
- Comparison: the fall against the standard deviation of daily returns over the past 30 days -> kept: the return is divided by its 30-day standard deviation, today's return included.
- Outcome: the larger that scaled fall, the larger the rise over the next day -> kept: a long position graded by the scaled fall, held 1 bar.
- Verdict transfer: yes: the forecast is the scaled fall inside the agitated profile, so the next-day gains confirm or reject exactly that relation.
Forecast: The forecast uses `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 30). Its raw value is the day's return divided by the standard deviation of the last 30 daily returns. It is standardised against its own past 60 values (`min_periods` 20), then negated, then clipped at 0. The forecast is therefore positive only on down days, and its size grows linearly with the fall measured in usual daily moves. It is 0 on up days and flat days, and never negative (long only). The code adds the agitated profile, so the book is flat outside it.
Config: 040-02_agitated-fall-vs-swing-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use every bar inside the agitated profile, within windows (1-bar returns do not overlap). Regress the coin's next-day return, minus its mean daily return over all windows, on the bar's forecast. Read the slope's t, with cases of the same day taken together.
- Supporting check: The mean of that excess next-day return over the bars with forecast above 0 is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less, meaning bigger scaled falls are followed by weaker next days or further decline.
- Inconclusive: A slope t between -2 and 2, or a confirming slope with a mean excess return of 0 or below. At least 200 profile bars with forecast above 0 are needed, falling on at least 100 distinct days; fewer is inconclusive.
