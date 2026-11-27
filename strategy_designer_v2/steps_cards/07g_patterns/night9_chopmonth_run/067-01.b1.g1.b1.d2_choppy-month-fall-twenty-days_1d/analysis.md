---
line: 7.g patterns
backtest: 067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days_1d
idea tested: 067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4562 USD
---
## Findings
- **F1:** In choppy bars (60-day return between -10 % and +10 %), the 30-day return scaled by the coin's 30-day daily swing ranks the next move the same way. The Spearman rho with the unusual move is 0.28 over 5 days (189 non-overlapping cases, p 0.0001), 0.37 over 10 days (96 cases, p 0.0002) and 0.31 over 20 days (48 cases, p 0.03). Over 10 days the lowest third averages -11.9 % and the highest third +10.8 %; over 20 days the gap narrows to -10.9 % against +4.4 %. The tested 20-day horizon is past the effect's peak.
- **F2:** The choppy continuation appears after falls and after rises, but it is only sure after falls at short horizons. After a 30-day fall the short-signed unusual move is +4.6 % over 5 days (median +3.2 %, pooled t 2.08, 48 days) and +6.2 % over 10 days (t 1.63, rho of size against the move 0.56). After a rise it is +5.4 % over 5 days, but its median is only +0.35 % (t 1.17), so a few large cases carry it.
- **F3:** The choppy continuation is not stable over time. Its 5-day signed mean is -4.0 % in 2018 (30 % positive), then +1.5 %, +3.0 % and +13.2 % in 2019 to 2021, and it is positive in 8 of 12 windows. Calm and agitated choppy bars look alike (+5.1 % against +4.6 % over 5 days).
- **F4:** Outside choppy markets, the 30-day move continues over the next 10 days in falling calm bars: signed unusual move +3.8 %, t 3.18, 106 cases, rho 0.24. It continues less surely in rising calm bars (+3.8 %, t 2.46, 125 cases). It reverses slightly in falling agitated bars (-1.2 %, t -0.77). The map holds only 2 strategies, both "calm" ones, in falling calm on each side.
- **F5:** Other effects found are already held by the map. After a daily fall of more than 2 swings in the most volatile third of bars, the next day rebounds +5.4 % (t 4.15, 47 cases). A close in the bottom fifth of the day's range is followed by +0.44 % the next day (t 3.33, 1852 cases); a close in the top fifth by -0.29 % (t -2.33). Both are agitated or low-close rebounds.
- **F6:** The tested book lost on its trades: 453 trades of 20.2 days on average, mean net -5.1 %, 38 % winners. This fits a horizon too long and a signal scaled against the coin's own last 60 monthly returns rather than against its swing.

## Ideas
- `067-01.b1.g1.b1.d2.g1_choppy-swing-scaled-month-continuation` (from F1, F2, F3): In a choppy market, the larger a coin's 30-day return measured against its daily swing over the past 30 days, the further it moves the same way over the next 10 days, after rises and after falls alike.
- `067-01.b1.g1.b1.d2.g2_choppy-month-fall-week` (from F1, F2): In a choppy market, the larger a coin's 30-day fall measured against its daily swing over the past 30 days, the more it keeps falling over the next 7 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `067-01.b1.g1.b1.d2.g3_falling-calm-month-continuation` (from F4): In a falling, calm market, the larger a coin's 30-day move measured against its daily swing over the past 30 days, the further it moves the same way over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
