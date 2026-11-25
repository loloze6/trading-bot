---
line: 7.g patterns
backtest: 037-02_fall-range-beyond-loss-rebound_1d
idea tested: 037-02_fall-range-beyond-loss-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4038 USD
---
## Findings
- **F1:** The tested forecast's next-day unusual move is carried entirely by its top quartile: forecast quartiles 1 to 4 give -0.012 % (t -0.06), -0.162 % (t -0.74), +0.326 % (t 1.24) and +0.954 % (t 2.39, 1069 cases on 359 days). Only the top quartile's move is clearly larger than the 0.19 % cost of a trade, while the mean over all cases is +0.13 %.
- **F2:** Among each coin's down days, the deepest third of falls rebounds +1.049 % the next day (t 2.39, 754 cases, 244 days) when the day's range is in the widest third against its prior 20-day average, against +0.404 % (t 0.80) for the middle third and +0.502 % (t 0.40, 79 cases) for the narrowest third. Shallow falls give -0.020 % to -0.973 % whatever their width, so the fall and the range relative to recent ranges act together.
- **F3:** The forecast's cases rebound only when the coin's 20-day swing is high: by tercile of that swing, from low to high, the next-day unusual move is -0.061 % (t -0.30), +0.187 % (t 0.85) and +0.860 % (t 2.36, 1187 cases, 477 days). For all bars, high swing alone gives only +0.113 % (t 0.46), so the swing selects where the fall effect lives rather than adding a drift of its own.
- **F4:** Across all bars, the next-day unusual move falls steadily with the day's own return. The deepest-fall decile gives +0.976 % (t 2.17, 867 cases, 272 days), the second +0.400 % (t 1.40), the middle deciles about 0 to -0.33 %, and the largest-rise decile -0.421 % (t -1.26).
- **F5:** Among the deepest falls, a close near the day's low rebounds +0.984 % (t 2.52, 771 cases, 266 days), against +0.514 % (t 1.03) for a mid close and +0.652 % (t 0.70) for a close near the high. This points against the tested idea's "range beyond the loss" term: the rebound is strongest when the coin closes at its low, not when it travelled far above the close.
- **F6:** When the forecast is 0 and the coin's 30-day return is below -10 %, the next day's unusual move is -0.918 % (t -2.87, 1083 cases, 334 days), against -0.021 % in choppy and +0.027 % in rising markets. It is a single cell among about 60 examined, with no grading shown, so it is noted only and not used.
- **F7:** The book follows the market on its extreme days, so its falls are market falls, not failures of timing. On its best 2 % of days (29) it gains +6.52 % while the coins rise +10.63 %, and on its worst 2 % it loses -7.08 % while the coins fall -10.99 %. Its mean daily return is negative in w7 (-0.044 %) and w9 (-0.083 %), the windows where the coins fell (-0.473 %, -0.256 %).

## Ideas
- `037-02.g1_forced-fall-rebound-when-agitated` (from F3, F1): In an agitated market, the larger a coin's one-day fall and the further that day's high-to-low range stretches beyond the size of the closing loss itself, taken together, the larger the rise over the next day.
- `037-02.g2_deep-fall-wide-relative-range` (from F2, F4, F1): The larger a coin's one-day fall and the wider that day's high-to-low range against the coin's average range over the previous 20 days, taken together, the larger the rise over the next day.
- `037-02.g3_deep-fall-closing-at-low` (from F5, F4): The larger a coin's one-day fall and the nearer its close to that day's low, taken together, the larger the rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
