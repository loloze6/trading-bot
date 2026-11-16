---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 10-day return measured against its 20-day daily volatility, the larger its rise over the next 10 days, and this rise is larger the smaller the coin's 60-day return already is.
Consequence: A trader would scale a volatility-adjusted momentum long down as the coin's 60-day gain grows, cutting exposure in the stretched late-trend phase where the book's falls build.
Why:
- F1: The book's deepest falls are long and slow rather than single crashes: the chained daily book fell 26.5% over 797 days (windows w4 to w10) and 21.0% over 430 days (w11 to w15), against a yearly return of 19.4%. The long bars inside falls deeper than 12% earned a mean of 0.00056 per bar over 4330 bars, against 0.00362 over 2275 bars outside them.
- F2: The gain sits in the middle of the trend's age, not at its stretched end. Long bars in the 4th 30-day-return quintile earned a mean of 0.0040 per bar (sum 4.20), while the top quintile (30-day return above 37.8%) earned only 0.0011 per bar and carried the largest summed losses, -10.69 against -8.17. The 60-day return shows the same pattern: 0.0034 per bar in its middle quintile against 0.0005 in its top quintile (above 54.5%).
- F3: On the non-overlapping 10-day trending grid, the forecast's slope on the excess 10-day return is strongest when the coin's 60-day return is low: slope 0.0082, t 4.39, n 137. In the high 60-day-return tercile it falls to slope 0.0027, t 1.38, n 137, and in the middle tercile to t 0.50.
- F5: The biggest daily losses come from the strongest signals. Bars with forecast above 17.5 average 0.00537 per bar, but 9.9% of them lose more than 5% in a day, against 0.4% for forecasts between 3.9 and 9.5. Bars in the top 10-day-return quintile carry summed losses of -17.9, against -6.5 in the 3rd quintile. The falls therefore come from full-size positions held after the coin is already stretched.
