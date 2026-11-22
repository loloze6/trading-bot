---
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d
idea tested: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4180 USD
---
## Findings
- **F1:** The day's high-low range relative to its own 20-day average predicts the coin's next 5 days. On 6,228 non-overlapping 5-day cases, the scaled excess 5-day return rises with the log of that ratio (slope 0.091, t 3.66). The widest-range quintile is followed by +0.103 of a usual 5-day move (t 3.28, 1,246 cases), the two narrowest quintiles by −0.070 (t −2.53) and −0.068 (t −2.80). The slope is positive in 16 of 19 coins.
- **F2:** The pooled numbers suggest a sharp day continues in the direction of the 30-day trend: in coins up over 30 days, the excess 5-day return rises with the day's vol-scaled return (slope 0.077, t 4.57, 2,663 cases). This does not survive averaging the coins on each day (t 0.44 on 367 days up; t −0.28 on 376 days down), so it is a market-wide move shared across coins, not a per-coin effect.
- **F3:** The tested bounce situation shows only a weak, uncertain fade. In coins down over 30 days, a day of at least +2 usual moves is followed by −0.143 of a usual 5-day move (t −1.35, 77 cases). The verdict's own measure gave a slope t of −0.47 on 376 cases and an unusual move of −0.10 %, against a 0.22 % cost per trade.
- **F4:** The short-only book earned −0.031 % per active day over 3,664 coin-days, and its daily return correlates −0.64 with the coin's. Its result is mostly being short coins whose drift over the period was upward (normal drift in the short direction −0.74 % per 5 days).
- **F5:** Next-day returns from a Friday close average +0.43 % with the coins averaged per day (t 2.79, 414 days). The sign holds in both 2018–2021 (t 2.33) and 2022–2025 (t 1.54). Among the seven weekdays tested this is the only t above 2.5, so it is weak evidence and not graded.

## Ideas
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.g1_wide-range-days-precede-rises` (from F1, F4): In a coin, the wider a day's high-low range is compared with its average daily range over the past 20 days, the larger the coin's rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
