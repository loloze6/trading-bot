---
idea: 020-01_resistance-retest-turns-down
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: price rises back to a price where it turned down several times in the past 90 days -> adapted: "after rising back" becomes "while the close sits just below a level of 90-day swing highs", and "several times" becomes a graded count of the turns there.
- Comparison: the more times it turned down there before -> kept: the count of swing highs within 2% of the level scales the forecast.
- Outcome: it falls over the next 5 days, more after more turns -> kept: a short position held 5 bars, larger with more turns.
- Verdict transfer: yes: the forecast is the touch-count of the overhead turning level times its nearness, short, so its gains test exactly this claim.
Forecast: SwingHighClusterCountComponent (period 90, side 2, band 2%, form "proximity", level "above", pivot "high") gives N x 1/(1+D). Here N is the number of 90-day swing highs within 2% of the lowest swing high at or above the close, and D is the close's percent distance below that level. It is standardised against its own past 90 values (min_periods 22) and negated, so it is short. A signed_power with exponent 3 and pivot 20 then acts as the strongest graded dead zone. The forecast is near zero unless the close is close to a level that turned price down several times. It grows in size with the number of turns and the nearness. It is 0 when no swing high sits above the close, and it is never positive.
Config: 020-01_resistance-retest-turns-down_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, pooled over coins and windows, take the bars with a forecast below 0. Regress the coin's 5-bar return minus its normal drift (its mean 5-bar return over all windows) on the forecast, and take the slope's t. The slope is positive if more negative forecasts are followed by larger falls.
- Supporting check: Take the cases (bets, forecast at -5 or below, one per grid cell). Their mean unusual move in the short direction, before costs, is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less: stronger levels are followed by rises relative to drift.
- Inconclusive: A slope t between -2 and +2 is inconclusive. So is a confirming t whose supporting check fails, or fewer than 30 cases with forecast at -5 or below, or fewer than 100 grid bars with a non-zero forecast.
