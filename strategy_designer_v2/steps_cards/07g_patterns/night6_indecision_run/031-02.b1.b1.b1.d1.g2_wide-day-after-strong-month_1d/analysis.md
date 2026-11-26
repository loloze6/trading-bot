---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d
idea tested: 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6305 USD
---
## Findings
- **F1:** The tested effect needs the wide day as well as the rise, and grows with both. Among days after a 20-day rise, split by the product of the day's range ratio and the volatility-scaled 20-day rise, the top quintile is followed by an unusual 3-day move of +2.09 % (strength 0.21, t 3.05, 987 cases on 311 days). The four lower quintiles stay between -0.54 % and +0.05 % (all |t| < 1.7).
- **F2:** The width of the day's range grades the move on its own, inside the tested situation. Wide days (range ratio ≥ 1.5) after a 20-day rise, split in terciles of range ratio, give unusual 3-day moves of +0.32 % (t 0.58, ratio 1.5–1.74), +2.00 % (t 2.33, 1.74–2.11) and +3.28 % (t 2.38, above 2.11), 308–309 cases each. Over all days with a positive 20-day rise, only the widest range-ratio quintile (≥ 1.47) is positive: +1.73 %, t 2.63, against -0.30 % to +0.04 % for the other four.
- **F3:** Without a wide day, the 20-day rise carries no follow-through. On days that are not wide, the top quintile of volatility-scaled 20-day rise gives +0.19 % over 3 days (t 0.42, 1707 cases) and +0.85 % over 10 days (t 0.70). On wide days the same top quintile gives +3.92 % over 3 days (t 2.76, 299 cases).
- **F4:** After a wide day following a strong rise (20-day rise above 13 %), the unusual move keeps growing past the 3-day horizon: +0.77 % at 1 day (t 2.92), +1.68 % at 2 days (t 3.25), +2.91 % at 5 days (t 1.82) and +6.82 % at 10 days (t 2.43, 204 cases on 84 days). Over 10 days, wide days after a rise give +1.85 %, +7.26 % and +7.62 % by tercile of volatility-scaled 20-day rise (top tercile t 2.28).
- **F5:** The book earns on its longer holdings, not on the 3-day bet. Trades of up to 3.5 days (2337 trades) average +0.24 % net. Trades of 6–10 days average +15.1 % (222 trades) and trades of 10–20 days +15.7 % (110 trades). Trades over 20 days average -12.9 % (76 trades). The top 5 % of trades carry 105 % of the summed trade returns, and 56.6 % of trades win.
- **F6:** The brief's own mechanism does not show in the bars. Wide days after a 20-day fall are not followed by a move back up: the widest range-ratio quintile among falling coins gives -0.44 % (t -0.62). Among wide days, where the close lands in the day's range shows no gradient: +0.53 %, +1.39 %, +1.61 % and +0.98 % by quartile, all t < 1.8.
- **F7:** The effect is not steady across years. At the 10-day horizon, wide days after a rise give +9.5 % in 2020, +12.7 % in 2021 and +8.6 % in 2024. They give -7.6 % in 2022 (t -1.34) and -3.0 % in 2025 (t -0.50).

## Ideas
- `031-02.b1.b1.b1.d1.g2.g1_wider-breakout-day-larger-rise` (from F2, F1, F3): After a day whose high-low range is wide compared with its average daily range over the past 20 days, in a coin that rose over those 20 days, the coin rises over the next 3 days, and the wider that day's range relative to its 20-day average, the larger the rise.
- `031-02.b1.b1.b1.d1.g2.g2_width-times-scaled-trend` (from F1, F3, F2): After a wide-range day in a coin that rose over the past 20 days, the coin rises over the next 3 days, and the larger the product of that day's range relative to its 20-day average and the coin's 20-day rise measured in its own 20-day daily volatility, the larger the rise.
- `031-02.b1.b1.b1.d1.g2.g3_wide-day-trend-lasts-ten-days` (from F4, F5): After a wide-range day in a coin that rose over the past 20 days, the coin keeps rising over the next 10 days, and the larger its 20-day rise measured in its own 20-day daily volatility, the larger that 10-day rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
