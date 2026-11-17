---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: daily close near its 52-week closing high, while the 30-day return is positive -> adapted: the 30-day rise is a regime condition, and closeness is graded as the distance below the 364-bar closing high.
- Comparison: closer to the high, and higher 30-day and 7-day returns, give a larger gain -> adapted: the near-high, 30-day and 7-day readings are added as graded terms, not multiplied.
- Outcome: the return over the next 7 days is higher -> kept: 7 bars, judged against simply holding the coin.
- Verdict transfer: yes: the forecast rises with closeness to the high and with both rises, only while the 30-day return is positive, which is exactly what the idea claims.
Forecast: Only on bars where the 30-day price change is above 0 (regime `trending`). On all other bars the forecast is 0 (flat). On those bars the forecast is the equal-weight mean of three standardised terms: - the percent distance of the close below its highest close of the last 364 bars (never positive, so it is 0 at the high and more negative the farther below it); - the 30-bar percent return; - the 7-bar percent return. The forecast is largest when the close sits at its 52-week high after strong month and week rises. It shrinks as the close falls away from the high or the week's move fades. It turns negative when the coin is far below its high and the week's move is down.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: On non-overlapping 7-bar grid bars where the regime is `trending`, pooled across coins and windows, regress the coin's 7-bar forward return minus that coin's mean 7-bar return (over all windows) on the forecast. Report the slope's t.
- Supporting check: The book's mean daily return minus its gain from the market's own rise (the timing part) is above 0.
- Confirm: The slope's t is 2 or more and the timing part is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a timing part of 0 or less. Fewer than 100 trending grid cases is inconclusive whatever the t.
