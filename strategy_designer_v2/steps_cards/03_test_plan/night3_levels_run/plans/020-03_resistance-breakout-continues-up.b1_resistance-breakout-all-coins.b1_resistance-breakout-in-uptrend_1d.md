---
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: the on/off "closes above" becomes a regime gate on the break measure being above 0, and "several times" becomes graded by the touch count N in N x clearance.
- Comparison: only while the 30-day return is positive -> kept: a regime rule on the 30-day return being above 0.
- Outcome: keeps rising over the next 5 days, more with more touches, more clearance and a stronger 30-day rise -> kept: long, held 5 bars, sized by the standardised break measure and the 30-day return.
- Verdict transfer: yes: the forecast is long exactly on fresh closes through repeatedly-held 90-day swing highs in a rising month, it grows with all three strengths, and it is judged on the following 5 days.
Forecast: The regime is "trending" only on a bar where the close has just crossed above a swing-high close level of the last 90 bars and the 30-day return is above 0. The level is measured by ResistanceBreakTouchCountComponent (period 90, side 2, band 2 %, cross_period 1), which must be above 0, and the 30-day return by PriceEvolutionComponent (period 30). On all other bars the regime is null and the forecast is 0. In the trending regime the forecast is the equal-weight mean of two standardised values. The first is the break measure (touch count x percent clearance above the level), standardised over 90 bars. The second is the 30-day return, standardised over 60 bars. Both are positive in this regime, so the forecast is long only, and a clip at 0 keeps it there. It grows with the number of past turns at the level, with how far the close clears it, and with the strength of the 30-day rise.
Config: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's return over the 5 bars after each case, minus the coin's mean 5-bar return over all its windows. A case is a long bet: the forecast rising at least 2 points, read once per 5-bar grid cell. The measure is the mean of these differences over all coins and windows, with its t-statistic.
- Supporting check: Split the cases at the median of their entry forecast. The mean excess 5-bar return of the upper half minus that of the lower half must be above 0.
- Confirm: The mean excess return is positive with t >= 2 over at least 30 cases, and the upper-half-minus-lower-half difference is above 0.
- Reject: The mean excess return is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2. A t >= 2 whose size check is not above 0. Fewer than 30 independent cases in total.
