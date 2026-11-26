---
line: 7.g patterns
backtest: 060-01.b1_falling-calm-high-close-fade_1d
idea tested: 060-01.b1_falling-calm-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6608 USD
---
## Findings
- **F1:** In folds B and C, the tested situation's own cases (falling calm, a wide day closing near its high) had a next-day return below the coin's mean of −1.25 % (105 cases on 63 days, day-grouped t −2.65), which is +1.25 % in the short direction. The full-fold verdict is +0.26 % with t 0.87, so folds A and D must point weakly or the other way, and the pattern is not stable across folds.
- **F2:** Over all agitation levels, when the 60-day trend is falling, wide days (range at least 2 swings) closing in the top quarter are followed by −1.90 % next-day excess (109 cases, 50 days, t −2.40). The same days fall in every year shown: 2018 −1.99 %, 2020 −3.70 %, 2021 −0.75 %. The same days in a rising trend are followed by +0.72 % (190 cases, t 1.05). Falling agitated short already holds 060-01.g1.d2.d1, an own-range close-height fade, so the agitated part is already held.
- **F3:** In a falling 60-day trend, the next-day excess return falls step by step as the day's close-to-close move rises against its 30-day swing: z below −2.5 +3.34 %, −2.5 to −1.5 +0.67 %, −1.5 to −0.5 +0.40 %, −0.5 to 0.5 −0.33 %, 0.5 to 1.5 −0.74 % (400 cases, t −1.99), 1.5 to 2.5 −0.69 %, above 2.5 −2.96 % (18 cases, t −2.29). The fade after up days (z above 0.5) held in 2018 (−1.34 %, t −1.81), 2019 (−0.87 %, t −1.89) and 2020 (−1.18 %, t −1.27), but not in 2021 (+0.27 %).
- **F4:** Wide days closing in the bottom quarter of their range are followed by a next-day rebound that grows with width: range 1–1.5 swings −0.30 %, 1.5–2 swings +0.68 % (t 1.42), 2–3 swings +1.02 % (332 cases, 159 days, t 2.21), above 3 swings +2.21 % (165 cases, 79 days, t 2.21). The rebound is positive in every year: 2018 +0.77 %, 2019 +0.88 %, 2020 +2.61 %, 2021 +1.56 % (t 2.01). It is strongest in a rising 60-day trend: +1.91 % (105 cases, 53 days, t 2.68), against +1.54 % in falling (t 1.52) and +1.15 % in choppy (t 1.21). The map already holds this pattern in the agitated profiles (039-02.d1, 044-01, 045-01), but not in rising calm.
- **F5:** Down days (z below −1) are followed by a rebound that grows with the day's volume against its 20-day mean, by volume tercile within each coin: low +0.36 % (73 cases), middle +0.94 % (248 cases, t 1.50), high +1.22 % (641 cases, 212 days, t 2.61). Up days show no such grading (+0.24 %, −0.20 %, −0.23 %). Over all bars, the top volume-ratio quintile is followed by +0.56 % (t 1.95) and the bottom quintile by −0.43 % (t −2.11). The map holds the heavy-volume fall rebound only in falling agitated (064-01).
- **F6:** The other angles show nothing that stands out from chance after about 60 cells were looked at. No weekday has a day-grouped |t| above 1.5, and the signed-volume quintiles all have |t| below 0.9. The book is small: 2 % of coin-days in a position, +1.1 % a year, and a total move per case of only 0.6 times the 0.22 % cost of a trade. A next-day fade therefore needs a much larger move per case (F2 −1.90 %, F3 top bucket −2.96 %) to pay.

## Ideas
- `060-01.b1.g1_falling-calm-rise-size-fade` (from F1, F3): In a falling, calm market, a wide day that closes near its high is followed by a fall over the next day, larger the larger the day's close-to-close rise against the coin's 30-day swing of daily returns.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-01.b1.g2_rising-calm-wide-low-close-rebound` (from F4): In a rising, calm market, a day whose range is wide against the coin's 30-day swing of daily returns and that closes near its low is followed by a rise over the next day, larger the wider the day.
- `060-01.b1.g3_heavy-volume-down-day-rebound` (from F5): A down day traded on heavier volume than the coin's 20-day average is followed by a rise over the next day, larger the heavier the volume against that average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
