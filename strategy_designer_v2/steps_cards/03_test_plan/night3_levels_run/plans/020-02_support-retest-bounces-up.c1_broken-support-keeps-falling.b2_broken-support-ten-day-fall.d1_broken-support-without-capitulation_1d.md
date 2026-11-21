---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close sits just below prices where the coin turned up several times in the past 90 days -> adapted: the count of 90-day swing lows within 2% of the nearest one above the close is weighted by how near the close is, and the "several" threshold becomes a graded damping.
- Comparison: the more such turning-up lows lie just above the close, the larger the fall, except after a deep 90-day fall -> kept: the position grows with that count, and a regime on the 90-day return (at or below -30%) flips the side to long.
- Outcome: the price falls over the next 10 days, or rebounds after a deep 90-day fall -> kept: each bet is held for 10 daily bars, short normally and long in the deep-fall regime.
- Verdict transfer: yes: the forecast is the idea's own count-and-nearness reading, with its own exception and horizon, so its gain or loss over 10 bars answers the idea.
Forecast: Each bar, SwingHighClusterCountComponent (pivot "low", level "above", period 90, side 2, band 2%, form "proximity") finds the lowest past swing low at or above the close. It counts the swing lows within 2% of that level and multiplies the count by the close's nearness to it. The value is 0 when no swing low sits above the close. It is standardised over its past 90 values (min 22) and squared with signed_power (exponent 2, pivot 10), so a single-touch or distant level gives almost nothing and a many-touch level just above the close gives a large value. When the coin's 90-day return is above -30%, the value is negated, giving a short that grows with the touch count and nearness. When the 90-day return is -30% or lower, the same value is kept positive, giving a long (the rebound). The forecast is zero whenever no turning-up low lies above the close.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the grid of bars 0, 10, 20, ... of each window, keeping cells where the forecast is not 0. For each cell, take forecast/10 x (the coin's 10-bar return minus its mean 10-bar return over all windows). Measure the mean of this value and its t, pooled over coins, before costs.
- Supporting check: The same signed excess return is larger in the upper half of |forecast| than in the lower half (difference upper minus lower above 0).
- Confirm: The mean is above 0 with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean is below 0 with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a confirm-sign t whose supporting check fails, or fewer than 30 non-zero grid cases.
