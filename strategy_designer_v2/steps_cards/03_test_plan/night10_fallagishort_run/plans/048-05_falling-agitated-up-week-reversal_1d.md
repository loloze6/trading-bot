---
idea: 048-05_falling-agitated-up-week-reversal
brief: 048_scaled-week-moves-continue-both-ways
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: a falling, agitated market, after a week in which the coin rose -> adapted: the profile is added by code; "after an up week" becomes "while the 7-day return is above 0", a regime rule.
- Comparison: the 7-day return in units of the 30-day standard deviation of daily returns -> kept: the 7-day return over the 30-day daily-return std; the constant sqrt(7) cancels under standardise.
- Outcome: it falls over the next 3 days, more so the larger the scaled week -> kept: a short position, graded by the scaled return, held 3 bars.
- Verdict transfer: yes: the book is short only inside the profile after up weeks, sized by the scaled week, so its 3-day results answer the idea both ways.
Forecast: The regime detector selects `mean_reversion` only on bars whose 7-day return is above 0; every other bar is flat. Code adds the falling-agitated profile vetoes on top. Inside the regime, the forecast is built from `VolatilityScaledReturnComponent` (period 7, vol_period 30), which is the 7-day return divided by the 30-day std of daily returns times sqrt(7). It is standardised (window 60, min_periods 20), negated, and clipped at a maximum of 0. The forecast is therefore always short or zero. It is near 0 after a barely-up week and grows more negative as the up week gets larger in swing units, capped at -20. It is never positive.
Config: 048-05_falling-agitated-up-week-reversal_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window, keeping grid bars with forecast < 0. Regress y on x, where y is the coin's 3-day return from that close minus the coin's mean 3-day return over all windows, and x is the size of the forecast (|forecast|). The measure is the t of the slope.
- Supporting check: The mean of y over the same cases is below 0, which means the short side earns against holding the coin.
- Confirm: The slope's t is -2 or lower (larger scaled up weeks are followed by larger falls) and the mean y is below 0.
- Reject: The slope's t is +2 or higher (larger scaled up weeks are followed by larger rises) and the mean y is above 0.
- Inconclusive: Any other result, or fewer than 50 cases (grid bars with forecast < 0), counts as neither confirm nor reject.
