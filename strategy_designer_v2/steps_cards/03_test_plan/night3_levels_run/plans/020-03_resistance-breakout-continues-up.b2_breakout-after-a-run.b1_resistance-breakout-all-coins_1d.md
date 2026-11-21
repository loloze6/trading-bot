---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, after a 20-day run -> adapted: "several times" becomes a graded touch count inside the break measure, and the regime is active while the break holds on that bar.
- Comparison: a break after a strong run against a break after a flat or falling month -> kept: a positive 20-day return gates the regime, and a larger return gives a larger position.
- Outcome: the price keeps rising over the next 5 days, more with a larger run and more touches -> kept: each bet is held 5 bars.
- Verdict transfer: yes: the forecast exists only on breaks of 90-day swing-high levels after a rise, sized by touches, margin and run, and is judged on the 5-day move that follows.
Forecast: The regime is active only on a bar whose close has just crossed above a 90-day swing-high level and whose 20-day return is positive. - The break is measured by `ResistanceBreakTouchCountComponent` (period 90, side 2, band 2 %, cross_period 1): the number of swing highs at the level times the close's percent margin above it. - The run is measured by `PriceEvolutionComponent` over 20 bars, clipped at 0. - Both are standardised against their own past and averaged with equal weights. - On those bars the forecast is positive. It grows with the touch count, the margin over the level and the size of the 20-day run. - On every other bar the forecast is 0. It is never short.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case: the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-day drift (holding the coin, all windows). Cases are signals read once per 5-bar grid cell; the measure is the t of their mean, before costs.
- Supporting check: Cases with an entry forecast above the median of all cases have a larger mean unusual move than cases below it (difference greater than 0).
- Confirm: The mean unusual move has t >= 2 over at least 30 independent cases, and the supporting check passes.
- Reject: The mean unusual move has t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, or a confirming t whose supporting check fails. Fewer than 30 independent cases decides nothing.
