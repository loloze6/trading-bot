---
line: 7.c no effect
backtest: 050-02.b1.d3_rise-with-room-below-high_1d
idea tested: 050-02.b1.d3_rise-with-room-below-high
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3838 USD
---
## Findings
- **F1:** The tested idea's effect is missing because the falling side carries and the rising side barely does: in falling calm markets, coins whose 7-day move was a fall kept falling (unusual move over 3 days −1.90 %, t −2.33, 101 days; over 5 days −2.90 %, t −2.15, 59 days), while coins whose 7-day move was a rise drifted only slightly up (over 3 days +1.00 %, t 1.20, 57 days; over 7 days +0.75 %, t 0.28, 21 days).
- **F2:** The rise side carries only when the rise is large against the coin's own swing. Among 7-day rises in profile, the top tercile of the scaled rise (mean 1.57 usual moves) gained +2.24 % unusual over 3 days (t 1.46, 20 days) and +2.98 % over 5 days (t 1.40, 11 days). The bottom tercile (0.14 usual moves) lost −0.71 % and −0.75 %. Over all in-profile moves at 3 days, the top quintile gained +2.16 % (t 2.29, 43 cases) and the bottom quintile lost −2.54 %, a graded ladder with Spearman ρ 0.20 (216 cases).
- **F3:** The plan's 7-day horizon dilutes the carry, which shows most over 2 to 5 days. The correlation of the scaled move with the unusual move falls from ρ 0.20 at 3 days to 0.11 at 7 days and 0.03 at 14 days. At 3 days the rising-side cases also outnumber those at 7 days (82 against 31), so the evidence is stronger.
- **F4:** The plan's second component, depth below the 30-day high, does not grade the outcome. The unusual 7-day move by depth quartile, from deepest to nearest the high, is −0.50 %, −5.02 %, +2.03 % and −2.52 %, all with |t| under 1.8. Rises at the 30-day high were too few to compare, with 4 to 13 cases per horizon.
- **F5:** The rise-side carry over 3 days is positive on all four coins (BCH +1.64 %, ETH +0.61 %, XMR +1.01 %, ZEC +0.73 %, each about 20 days), but it is concentrated in time. In 2021 it was +3.30 % (t 2.45, 16 days); in 2019 it was −0.76 % and in 2020 −1.17 %. Windows w7 (+7.7 %) and w17 (+4.3 %) carry most of it.
- **F6:** Size against cost: the top tercile's +2.24 % unusual move over 3 days is about 7 times the 0.31 % cost of a trade. The tested idea's case was 1.5 times.

## Ideas
- `050-02.b1.d3.c1_scaled-weekly-rise-short-carry` (from F2, F3, F4, F6): In a falling, calm market, a coin whose 7-day rise is large against its usual daily swing keeps rising over the next 3 days. The larger that rise in units of its usual swing, the further it carries.
- `050-02.b1.d3.c2_scaled-three-day-rise-carries` (from F2, F3, F6): In a falling, calm market, a coin whose 3-day rise is large against its usual daily swing keeps rising over the next 5 days. The larger the scaled 3-day rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
