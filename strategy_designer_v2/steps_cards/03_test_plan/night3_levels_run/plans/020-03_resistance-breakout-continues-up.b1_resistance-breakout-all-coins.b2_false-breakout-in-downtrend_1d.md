---
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: the touch count of the level crossed on that bar (90 bars, swing highs on closes, 2% band) times the close's margin above it, so "several times" is graded rather than a threshold.
- Comparison: while the 30-day return is negative, and the deeper the decline, the larger the fall -> kept: a 30-bar return below 0 selects the regime, and the depth effect is judged in the criterion.
- Outcome: the price falls back over the next 10 days -> kept: a short position held 10 bars.
- Verdict transfer: yes: the forecast shorts exactly these breaks inside falling months, and the depth claim is a required check.
Forecast: A regime rule keeps the strategy active only while the 30-bar close-to-close return is below 0; on all other bars the forecast is flat. In that regime the forecast is minus ResistanceBreakTouchCountComponent (period 90, side 2, band 2%, cross_period 1). That component is 0 unless the close has just crossed above a past swing-high close. On a crossing bar it is the level's touch count times the percent margin of the close above the level. It is standardised over its own past 90 values and negated. So the forecast is zero with no fresh break, and short on a fresh break. The short grows with how many times the level turned the price down and how far the close sits above the level. Each short is held for 10 bars.
Config: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Each case is a short bet, read once per 10-bar grid cell. Per case, take the coin's 10-bar return from the signal bar's close, minus the coin's normal 10-bar drift over all windows, in the short direction. The measure is the mean of this over the cases, with its t across cases.
- Supporting check: Recompute each case's 30-bar return from the closes. Split the cases at the median 30-bar return. The mean drift-adjusted fall of the deeper-decline half minus that of the shallower half must be above 0.
- Confirm: The mean drift-adjusted fall is above 0 with t >= 2 over at least 30 cases, and the supporting check is above 0.
- Reject: The mean drift-adjusted 10-bar move after cases is a rise, with t <= -2 over at least 30 cases.
- Inconclusive: The idea is neither confirmed nor rejected when t is between -2 and 2, or when t >= 2 but the deeper half does not fall more. Fewer than 30 cases is also inconclusive, whatever the result.
