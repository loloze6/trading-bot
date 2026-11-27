---
line: 7.g patterns
backtest: 072-04.b2_choppy-deep-close-five-day-fall_1d
idea tested: 072-04.b2_choppy-deep-close-five-day-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5869 USD
---
## Findings
- **F1:** In the choppy profile (regime "unknown", 17 % of bars in folds B and C), the raw depth below the 20-day high in 20-day swing units does grade the next five days. The deepest fifth (depth -8.5 to -4.0) is followed by a drift-adjusted 5-day return of -7.0 % (t -3.97, 50 grid cases), against +1.2 % (t 0.75, 50 cases) for the fifth nearest the high. Over all choppy grid bars the depth slope has a t of 2.12 when the cases of one day are taken together (249 cases, 128 days). Step 5 found a t of 0.04 on all folds.
- **F2:** The gradient lives in calm choppy markets. Inside them the depth slope has a day-clustered t of 2.65 (191 cases, 99 days). Inside agitated choppy markets it has a t of 0.72 (58 cases, 46 days).
- **F3:** In choppy markets, the deepest two fifths fall whether the day closed up or down. After up days the drift-adjusted 5-day return is -6.1 % (t -3.50, 42 cases); after down days it is -2.7 % (t -2.00, 58 cases). This is the brief's "whether that day closed up or down".
- **F4:** The book loses where it holds shallow shorts. On days in a short position, the gain per bar is -0.14 % (t -1.96, 345 bars) in the fifth nearest the 20-day high. It is +0.42 % (t 1.45, 345 bars) in the deepest fifth. Coins then carry a normal drift of +0.56 % per 5 days against the short, which leaves the idea's total move at +0.08 % per case against a trade cost of 0.19 %. The deepest choppy fifth alone moves -7.0 % in five days.
- **F5:** Choppy agitated markets (4 % of grid bars) are followed by falls in every year. The drift-adjusted 5-day return was -7.0 % (t -2.32) in 2018, -2.9 % (t -2.11) in 2019, -14.1 % (t -2.20) in 2020 and -3.0 % (t -1.52) in 2021, with 58 cases. The fall is negative on all six coins and somewhat larger after a weaker 10-day return: -8.3 %, -4.4 % and -3.9 % by tercile of the 10-day return, from the weakest to the strongest. That gradient's slope t is only 0.20. The choppy agitated short cell of the profile map is empty.
- **F6:** In falling calm markets, the lowest third of the 20-day range is followed by -5.0 % over 5 days (t -4.41, 82 cases). In rising calm markets the top third is followed by +4.6 % (t 3.90, 109 cases). The map already holds this as calm range edge continuation (058-02 family), so it is not a discovery.

## Ideas
- `072-04.b2.g1_choppy-calm-deep-close-fall` (from F1, F2, F3, F4): In a choppy, calm market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next five days, whether that day closed up or down.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `072-04.b2.g2_choppy-agitated-weak-drift-fall` (from F5): In a choppy, agitated market, a coin falls over the next five days, and it falls more the weaker its 10-day return in units of its 20-day daily-return standard deviation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
