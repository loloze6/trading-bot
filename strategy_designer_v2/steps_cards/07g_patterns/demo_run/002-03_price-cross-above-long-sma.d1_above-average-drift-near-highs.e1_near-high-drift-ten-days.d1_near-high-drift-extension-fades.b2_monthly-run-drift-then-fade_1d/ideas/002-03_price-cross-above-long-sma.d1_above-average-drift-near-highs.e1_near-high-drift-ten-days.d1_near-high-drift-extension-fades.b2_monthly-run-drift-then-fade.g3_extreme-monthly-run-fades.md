---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return beyond its usual size, the smaller its rise over the next 10 days.
Consequence: A trader would cut a trend-following long as the month's run stretches into extreme territory, since the book's worst days follow run-ups.
Why:
- F5: Above the 200-day average, the 10-day excess return rises with the 30-day return only up to about the 8th decile (mean 0.0634, t=1.96, 30-day return ≈0.30). It then drops to −0.0079 and 0.0083 in the top two deciles (30-day return ≈0.44 and 0.66).
- F4: The book's worst 5% of days come after a run-up. On those days the coin's prior 5-day return averaged +0.0583; the coin then fell 0.0465 and the book lost 0.0303.
