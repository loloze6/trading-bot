---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's one-day move (fall or rise), the larger the stronger -> kept
- Comparison: the move's size relative to the coin's usual daily move -> kept
- Outcome: next day, a rise after a fall that grows with the fall, and a smaller opposite fall after a rise -> kept
- Verdict transfer: yes: the forecast bets on next-day reversal in proportion to the volatility-scaled one-day move, as the idea states.
Forecast: The indicator is the one-day return divided by the standard deviation of the last 20 one-day returns. This is VolatilityScaledReturnComponent with period 1 and vol_period 20 (20 days is the conventional "usual daily move" on daily bars). It is standardised against its own past 60 values and then negated. The forecast is positive (long) after a down day and negative (short) after an up day. Its size grows with how large the day's move was relative to the usual move. It is near zero after an ordinary day. It is active on every bar, with no regime.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The OLS slope of the next-bar excess return on forecast[t], pooled over all coins and windows. The excess return is close[t+1]/close[t] - 1 minus that coin's mean daily return over all windows. The slope's t-statistic is reported with the number of bars. Returns never cross a window.
- Supporting check: The book's timing gain is above zero before costs. This is the book's mean daily return minus its gain from the market's own rise.
- Confirm: The slope t is 2 or more and the book's timing gain is positive.
- Reject: The slope t is -2 or less, meaning next-day moves continue in the direction of the day's move.
- Inconclusive: A slope t between -2 and 2, or t of 2 or more with a timing gain of zero or below. At least 1,000 bars with a non-zero forecast are required, out of about 17,500 available.
