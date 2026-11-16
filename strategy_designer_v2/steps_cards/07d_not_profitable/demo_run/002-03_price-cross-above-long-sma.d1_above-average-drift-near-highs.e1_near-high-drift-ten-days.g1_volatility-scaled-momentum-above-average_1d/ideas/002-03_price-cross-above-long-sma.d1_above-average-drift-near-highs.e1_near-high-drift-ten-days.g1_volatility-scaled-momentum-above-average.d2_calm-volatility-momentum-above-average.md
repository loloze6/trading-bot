---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 10-day return measured against its 20-day daily volatility, the larger its rise over the next 10 days, and this rise is larger the lower its 20-day daily volatility stands against its 60-day daily volatility.
Consequence: A trader would size the momentum long down as short-term volatility expands relative to its longer level, because the signal's edge disappears and the large daily losses cluster there.
Why:
- F3: On the non-overlapping 10-day trending grid, the forecast's slope on the excess 10-day return is strongest when the coin's 60-day return is low: slope 0.0082, t 4.39, n 137. In the high 60-day-return tercile it falls to slope 0.0027, t 1.38, n 137, and in the middle tercile to t 0.50.
- F4: When 20-day volatility is high against 60-day volatility, the forecast loses its edge. In the top vol-ratio tercile the grid slope is 0.0004 (t 0.24, n 137), against 0.0058 (t 3.84) in the middle tercile. On the long bars, the top two vol-ratio quintiles hold the largest share of daily losses beyond 5% (5.96% and 3.55%, against 0.99% to 2.27% in the others) and the largest summed losses (-6.66 and -5.77).
- F5: The biggest daily losses come from the strongest signals. Bars with forecast above 17.5 average 0.00537 per bar, but 9.9% of them lose more than 5% in a day, against 0.4% for forecasts between 3.9 and 9.5. Bars in the top 10-day-return quintile carry summed losses of -17.9, against -6.5 in the 3rd quintile. The falls therefore come from full-size positions held after the coin is already stretched.
