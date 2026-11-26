---
line: 7.g patterns
backtest: 067-02.b1_raw-swing-stretch-keeps-falling_1d
idea tested: 067-02.b1_raw-swing-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4134 USD
---
## Findings
- **F1:** In the choppy bars (the regime 'unknown', 17.1 % of all bars in folds B and C), the 10-day excess return after drift falls further the deeper the close sits below its 20-day average in units of its 20-day swing: −7.08 % (t −2.88, 24 grid cases) for a stretch below −2, −3.12 % (t −0.94, 19 cases) for −2 to −1, and −3.49 % (t −1.11, 27 cases) for −1 to 0. Above the average there is no matching carry: +2.22 % (t 0.66) for 0 to 1, −1.07 % for 1 to 2, and +0.58 % (t 0.19) above 2. The carry shows on the short side only, and step 5's slope over all folds was flat (t 0.18, 200 cases).
- **F2:** In the choppy bars, the coin's 20-day return in units of its swing grades the next 10 days more cleanly than the stretch does. The 10-day excess is −7.55 % (t −2.46, 18 cases) for a scaled 20-day return below −1, −5.39 % (t −2.97, 34 cases; day-clustered t −2.93 on the 5 agitated cases that could be classed) for −1 to −0.3, +0.11 % for −0.3 to +0.3, and +2.00 % for +0.3 to +1. Over all choppy grid cases its correlation with the 10-day excess is 0.21 (stretch: 0.20).
- **F3:** The choppy fall carry is concentrated where the coin swings most. The coin's highest 20-day swing tercile shows a 10-day excess of −6.90 % (t −2.68, 22 cases). The middle tercile shows −1.96 % (t −0.70, 34 cases) and the lowest −0.83 % (t −0.48, 70 cases). Choppy agitated short is the one empty cell of the profile map.
- **F4:** Outside the choppy profile, a close more than 2 swings above its 20-day average is followed by a 10-day excess of +5.34 % (t 3.01, 126 cases). This holds in rising markets (+8.60 %, day-clustered t 1.92, 22 days) and falling ones (+8.75 %, t 1.52). It is an upside continuation in trending markets, which the map already holds (034-01.e1, 034-02, 033-03.b2), so it is not a discovery.
- **F5:** Outside the choppy profile, a daily fall of more than 2 swings is followed by a next-day excess of +1.41 % (t 3.11, 189 days), and a rise of 0 to 1 swing by −0.34 % (t −3.28, 2,196 days). This is the next-day reversal the map already holds in falling agitated markets (038-01, 047-01, 058-02.b1.g1.b1.b1).
- **F6:** The weekday pattern is not strong enough to count. Next-day excess returns on Fridays (+0.47 %) and Saturdays (+0.39 %) have day-clustered t of only 1.50 and 1.54 (about 207 days each), and the late-week gain is already held (045-01).
- **F7:** The book lost in 8 of 12 windows (mean daily returns −0.0009 to +0.0016) while holding the coins rose in 7. This fits F1: the short forecast was active on every choppy close below the average, most of whose cases (the shallow ones) carry no fall after drift.

## Ideas
- `067-02.b1.g1_choppy-agitated-fall-carries` (from F2, F3, F1): In a choppy, agitated market, the more a coin's 20-day return has fallen, counted in units of its current 20-day standard deviation of daily returns, the more it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
