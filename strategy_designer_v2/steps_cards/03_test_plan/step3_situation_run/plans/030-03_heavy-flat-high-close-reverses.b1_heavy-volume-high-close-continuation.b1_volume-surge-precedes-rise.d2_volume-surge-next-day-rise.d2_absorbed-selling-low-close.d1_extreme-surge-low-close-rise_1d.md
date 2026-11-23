---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a day whose volume is several times its prior 20-day average and whose close sits near the low -> adapted: both conditions are a regime (volume ratio ≥ 2, close in the bottom 20 % of the range), and inside it the position is graded by the surge times the closeness to the low, squared.
- Comparison: the day's volume against the coin's own prior 20-day average, excluding that day -> kept
- Outcome: the coin rises over the next day -> kept
- Verdict transfer: yes: the book is long only on heavy, low-closing days, sized by the squared surge, and judged on the next day's move against the coin's drift.
Forecast: The forecast is zero on every day except those where two things hold together. The day's volume must be at least 2 times its prior 20-day mean (the most common volume-spike convention). The close must sit in the bottom 20 % of the day's high-low range (the usual low internal-bar-strength cut). On those days the forecast comes from one measure: the share of the range between the high and the close, times today's volume over its prior 20-day mean. That measure is standardised against its own past 60 values. It uses target 2, because the regime's edge is about three times that measure's ordinary size, so at target 10 every active day would sit at the cap. It is then squared with signed_power (exponent 2, pivot 10). The forecast is always positive (long only). It is about 4 at the regime's edge and grows with the square of the surge and of the lowness of the close, reaching the cap near a 4x surge with a close at the low.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: For each case, take the next day's return close[t+1]/close[t] − 1, minus the coin's mean daily return over all its windows. A case is a bar where the forecast rises by at least 2 points from flat on the long side. Report the mean of these excess returns and its t, with cases on the same day summed into one observation.
- Supporting check: The case days are compared with control days, all recomputed from the bars. Control days have volume under 1.5x the prior 20-day mean and a close in the bottom 20 % of the range. The check passes if the cases' mean excess next-day return minus the controls' is above 0, with a Welch t of at least 1.
- Confirm: The cases' mean excess next-day return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The cases' mean excess next-day return is below 0 with t ≤ −2.
- Inconclusive: Anything else is inconclusive: a t between −2 and 2, or a confirming main measure whose check fails. Fewer than 30 distinct case days is inconclusive whatever the t.
