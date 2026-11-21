---
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 0974d5467d9f
---
Fidelity:
- Situation: a 4h close below the lowest low of the preceding two-day narrow stretch -> adapted: the threshold "below the low" made graded, as the depth of the close below the 12-bar prior low.
- Comparison: stretch narrowness against the coin's 30-day average 4h range, only while the 30-day return is negative -> kept: the narrowness is the 180-bar mean bar range over the 12-bar stretch range, and the negative 180-bar return is a regime condition.
- Outcome: the coin falls over the next three days, more the narrower the stretch -> kept: shorts are held 18 bars and sized by narrowness.
- Verdict transfer: yes: the short forecast is the break depth times the narrowness ratio, held for three days, and is active only in falling months, so its result is the idea's result.
Forecast: The forecast is NarrowRangeBreakoutComponent with side "below", period 12 (two days) and base_period 180 (30 days). It equals max(0, prior 12-bar low − close) / close × 100 × (180-bar mean bar range / 12-bar stretch range). It is standardised over its own past 180 values (min_periods 45), then negated, so it is never positive. It is 0 when the close is not below the stretch's low. It is more negative the deeper the break and the narrower the stretch against the 30-day average range. The forecast is active only in bars whose 180-bar return (30 days) is below 0. Those bars are the regime "trending", picked by a rule on PriceEvolutionComponent(180). In all other bars it is 0 (flat).
Config: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are the short bets: a fall of the forecast of at least 2 points, read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the signal's close and subtract the coin's normal 18-bar drift (holding the coin, over all windows). Read the result in the short direction, as the unusual move. Pool the cases over coins and windows and take the mean and its t.
- Supporting check: Split the cases at the median |forecast| at the signal. The mean unusual move of the larger half minus that of the smaller half must be above 0 (narrower stretch, larger fall).
- Confirm: The mean unusual move is positive with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 whose supporting check fails, and any result with fewer than 30 cases.
