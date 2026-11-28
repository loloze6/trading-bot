---
idea: 061-01_falling-calm-scaled-rise-fade
brief: 061_falling-calm-rally-next-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: a one-day rise that is large against the 30-day standard deviation of daily returns, in a falling, calm market -> kept: a regime holds only when the rise is at least 2 standard deviations (the usual "large move" level). Inside it the short is graded by the scaled rise. The falling calm profile is added by code.
- Comparison: the larger the scaled rise, the larger the next-day fall -> kept: the short grows with the scaled rise inside the regime.
- Outcome: the price falls over the next day -> kept: a 1-bar short, held for 1 bar.
- Verdict transfer: yes: the test measures the next-day move after large scaled rises in falling calm markets, and its size against the rise, as the idea states.
Forecast: The forecast is the one-day return divided by the standard deviation (ddof 1) of the last 30 daily returns, using `VolatilityScaledReturnComponent` (period 1, vol_period 30). The book holds a position only on days when that scaled return is at least +2; on every other day the forecast is 0. On those days the scaled return is standardised against its own past 60 values with target 4, so the typical absolute scaled move maps to 4. A 2-sigma rise then gives about 10, a 3-sigma rise about 15, and 4 sigma or more the cap of 20. The value is then negated, so the position is a short that grows with the size of the rise. The forecast is never positive. Code adds the falling calm profile on top, so the book is also flat outside it.
Config: 061-01_falling-calm-scaled-rise-fade_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: For each case (a short bet on a bar), the coin's return from that close to the next close, minus the coin's normal daily drift over all windows, taken in the short direction. Cases on the same day are summed into one. The measure is the mean of this unusual move and its t.
- Supporting check: Split the cases at the median absolute forecast. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean unusual move is positive (the coin falls more than its drift) with t of 2 or more, over at least 30 case-days, and the supporting check passes.
- Reject: The mean unusual move is negative (the coin rises more than its drift after large rises) with t of -2 or less, over at least 30 case-days.
- Inconclusive: A t between -2 and 2, a confirming t with the supporting check failing, or fewer than 30 case-days.
