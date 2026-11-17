---
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds_1d
idea tested: 003-02_thin-volume-drop-rebounds
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3368 USD
---
## Findings
- **F1:** Across all coins and windows, a coin's 5-day excess return rises with the size of its one-day move scaled by its own 20-day volatility. The slope is 0.0045 per unit of scaled move (t 2.49, 2555 non-overlapping cases). Days up by 1 to 2 usual moves are followed by +1.58% (t 2.21, n 255). Days up by more than 2 usual moves are followed by +2.47% (t 1.96, n 110). Days down by more than 2 usual moves are followed by only +0.35% (t 0.34, n 76), so falls show no rebound.
- **F2:** The continuation after up days of more than 1 usual move is positive in all six coins. It is largest in XRP (+5.3%, t 2.09) and ZEC (+3.4%, t 1.75). It is concentrated in the early years: +3.5% (t 3.14, n 147) in 2018–2021 against +0.9% (t 1.22, n 202) in 2022–2025.
- **F3:** Volume adds to the continuation of up days, but only weakly.
- **F4:** The tested situation almost never occurs. There were only 5 active bars in 17,524. Pooled, only 3 grid cases are falls of 2 or more usual moves on volume below 0.7 of average. Those 3 were followed by −9.4%, the opposite of a rebound, so the thin-drop idea cannot be judged on this data.
- **F5:** Saturday's own daily return beats each coin's average by +0.34% (t 4.08, n 2484). It holds in both halves: t 3.38 in 2018–2021 and t 2.29 in 2022–2025. Saturday is also the quietest day (mean absolute return 2.5% against 3.3–3.7% on weekdays). Being a calendar effect, it cannot be graded into an idea.

## Ideas
- `003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue` (from F1, F2, F3): When a coin rises sharply over one day relative to its own 20-day volatility, it keeps rising over the next 5 days, and the larger the volatility-scaled rise and the heavier its volume against the coin's 30-day average, the larger the further gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
