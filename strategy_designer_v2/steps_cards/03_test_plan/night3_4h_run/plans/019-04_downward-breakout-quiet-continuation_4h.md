---
idea: 019-04_downward-breakout-quiet-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h bar closes below the lowest low of the preceding two-day (12-bar) stretch -> adapted: the on/off break becomes a regime that is active while the close is below the prior 12-bar low.
- Comparison: the stretch's range against the coin's 30-day (180-bar) average 4h bar range, narrower giving a larger fall -> kept: it is measured as the 12-bar stretch range over the 180-bar mean bar range, and the short grows as the ratio shrinks.
- Outcome: the coin falls over the next three days (18 bars) -> kept: each bet is held for 18 bars and is judged on the 18-bar return.
- Verdict transfer: yes: the test bets short exactly on closes below the prior two-day low, sized by narrowness, and judges the three-day fall.
Forecast: The regime detector reads the close's percent distance from the lowest low of the prior 12 bars (bar t excluded). Bars where that distance is below 0, meaning the close broke below the stretch low, are "trending". All other bars are flat. On trending bars the forecast is built from the width ratio, the 12-bar stretch range (bars t-12 to t-1) divided by the mean bar range of the last 180 bars: - The ratio is standardised against its own past 180 values, giving w (0 to 20, about 10 at its usual width). - It is averaged, at weight 1, with a constant -10 at weight 2. - The forecast is (w - 20) / 3, which is never positive. - The forecast is 0 when the stretch is very wide, about -3.3 at a usual width, and -6.7 as the stretch range nears zero. - The short therefore grows continuously as the stretch narrows against the 30-day average range.
Config: 019-04_downward-breakout-quiet-continuation_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Cases are the short bets, read once per 18-bar grid cell. For each case, take the coin's return from the signal bar's close over the next 18 bars, inside its window. Take the minus sign of that return (the short's direction) and subtract the coin's normal 18-bar drift. The measure is the mean of these values, with the t of the mean, pooled over coins and windows.
- Supporting check: Split the cases at their median absolute forecast (narrower stretches against wider ones). The drift-adjusted short gain of the larger-forecast half must be above that of the smaller-forecast half.
- Confirm: The mean drift-adjusted short gain is positive with t >= 2, and the supporting check passes.
- Reject: The mean drift-adjusted short gain is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose supporting check fails is also inconclusive. Fewer than 30 independent cases is inconclusive whatever the t.
