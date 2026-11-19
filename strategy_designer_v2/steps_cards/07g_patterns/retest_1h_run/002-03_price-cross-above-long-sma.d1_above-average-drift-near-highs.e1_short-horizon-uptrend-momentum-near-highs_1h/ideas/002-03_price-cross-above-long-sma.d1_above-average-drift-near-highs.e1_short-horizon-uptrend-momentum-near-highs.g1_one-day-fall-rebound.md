---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's fall over the past day, the larger its rise over the next one to three days.
Consequence: After a sharp one-day drop, a trader has reason to buy for a rebound over the next day or so rather than sell into the move, more so the deeper the drop.
Why:
- F1: A coin's 24-hour return predicts the next 24 hours in reverse, and almost entirely after falls. On the non-overlapping 24-hour grid, regressing excess next-24h return on the coin-standardised past-24h return gives a slope of -0.0107 (t -13.9, n 8716) when the past return is below the coin's mean, against -0.0025 (t -3.7, n 8386) when it is above. Within those falls, the deepest quarter is followed by +0.74% excess (t 5.2, n 2179), while the other three quarters show -0.08% to -0.18%.
- F2: The rebound after large 24-hour falls shows in every coin and nearly every year. For the bottom fifth of past-24h returns, the next-24h excess is +0.25% to +0.61% in all six coins (t 1.4 to 2.4) and positive in all eight years 2018–2025 (t 0.3 to 2.6, with 2022 the weakest at +0.08%).
- F3: The rebound after falls lasts beyond one day. On falls, the slope of excess return on the past return stays negative:
