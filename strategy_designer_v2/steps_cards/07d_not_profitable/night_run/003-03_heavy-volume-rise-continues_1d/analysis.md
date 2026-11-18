---
line: 7.d not profitable
backtest: 003-03_heavy-volume-rise-continues_1d
idea tested: 003-03_heavy-volume-rise-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3066 USD
---
## Findings
- **F1:** The book is only in the trade on the signal day itself. It holds a mean position of 0.43 on the bar the forecast is positive and about 0.017 on every bar after it, so the book's mean daily return is 4.9e-05 against roughly 0.0012 for holding the coins, and it trails holding in 15 of 24 windows.
- **F2:** After days with forecast >= 5, the coin's daily excess return over its own mean is small on the first day (+0.0012, t 0.92, n 1979, position held 0.90) and is concentrated on the second day (+0.0052, t 4.41, position held 0.22) and the fourth day (+0.0027, t 2.24, position held 0.16). The book has mostly left before the gain it forecasts arrives.
- **F3:** Because of this one-day holding, the book's gain is about the size of its fees. The mean gain before fees is 0.000242 per bar and the mean fee is 0.000188 per bar, while the trades themselves show only a mean net of +1.32 % over 3.3 days with 49 % winners.
- **F4:** The continuation after strong signals depends on the coin's prior 20-day return. For the top third of 20-day return, the 5-day excess is +0.025 (days 2 to 5: +0.022). For the bottom third it is +0.0018 (days 2 to 5: +0.0041). Each group has 530 cases.
- **F5:** The volume part of the forecast adds little among strong signals. The Spearman correlation between relative volume and the 5-day excess is 0.018, and between the scaled rise and the 5-day excess it is 0.017. The 5-day excess is +0.009 for the low-volume third and +0.017 for the high-volume third.
- **F6:** The effect differs across coins. The 5-day excess after strong signals is +0.033 for XRP and +0.023 for ZEC. It is -0.005 for LTC and -0.007 for XMR.

## Ideas
- `003-03_heavy-volume-rise-continues.d1_heavy-rise-continues-later` (from F1, F2, F3): When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days, with most of the further gain arriving from the second to the fifth day rather than on the first; the larger the rise and the heavier its volume against that average, the larger the further gain.
- `003-03_heavy-volume-rise-continues.d2_heavy-rise-within-uptrend` (from F4, F5, F2): When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days, only while its 20-day return is already positive; the larger the rise, the heavier its volume and the higher that 20-day return, the larger the further gain.
- `003-03_heavy-volume-rise-continues.d3_strong-rise-extends-trend` (from F4, F5, F2): When a coin's 20-day return is high and it closes a day with a sharp rise, it keeps rising over the next 5 days; the higher the 20-day return and the larger that day's rise, the larger the gain over the following days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
