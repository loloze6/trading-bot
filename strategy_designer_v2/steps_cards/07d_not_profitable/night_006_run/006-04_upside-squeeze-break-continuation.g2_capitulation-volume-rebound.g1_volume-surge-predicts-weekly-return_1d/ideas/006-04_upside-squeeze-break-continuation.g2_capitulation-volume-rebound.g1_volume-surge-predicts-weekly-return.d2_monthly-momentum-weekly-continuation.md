---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the higher its 30-day return, the higher its return over the next 7 days.
Consequence: A trader would lean long on coins with strong monthly gains and away from coins with monthly losses.
Why:
- F4: The forecast's information is concentrated where the coin's 30-day return is high. In the top 30-day-return tercile, the slope of 7-day excess return on the forecast is 0.001378 (t=2.52, n=575), against 0.000464 (t=1.01) and 0.000155 (t=0.37) in the lower two terciles. Across all samples, the forecast × z(30-day return) interaction has t=2.02.
- F6: The coin's own 30-day return predicts its 7-day excess return by itself (beta 0.0074 per standard deviation, t=2.34, about 1,723 non-overlapping cases). Positive forecasts after a 5-day rise lead to an excess return of +0.0136 (n=559), against -0.0053 after a 5-day fall (n=388).
