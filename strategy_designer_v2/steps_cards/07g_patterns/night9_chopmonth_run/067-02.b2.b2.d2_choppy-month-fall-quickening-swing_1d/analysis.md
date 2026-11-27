---
line: 7.g patterns
backtest: 067-02.b2.b2.d2_choppy-month-fall-quickening-swing_1d
idea tested: 067-02.b2.b2.d2_choppy-month-fall-quickening-swing
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4367 USD
---
## Findings
- **F1:** In choppy bars (60-day return between -10 % and +10 %), a coin's 5-day return scaled by its 30-day daily swing predicts its excess 10-day move in the same direction: Spearman 0.245 (p 7e-7, 402 non-overlapping cases), about twice the 30-day return's 0.126 (p 0.012) that the brief uses. This would survive a correction for the roughly 50 correlations looked at.
- **F2:** When both are in one regression on the same choppy 10-day cases, the 5-day move carries the effect and the month adds nothing: slope t 3.14 for the 5-day move against 0.96 for the 30-day move.
- **F3:** The effect is graded across choppy 5-day-move quintiles. The excess 10-day return runs -5.91 % (t -3.30), -4.13 % (t -2.52), +1.60 %, -2.45 %, +8.94 % (t 2.17), about 80 cases each.
- **F4:** The fall side is the surer one. After a 5-day fall in a choppy market the excess 10-day return is -4.65 % (t -3.99, 177 cases); after a 5-day rise it is +2.98 % (t 1.64, 225 cases).
- **F5:** The signed continuation is positive in 8 of 12 windows and in 3 of 4 years. It is concentrated late: 2020 +2.95 % (t 2.40), 2021 +7.62 % (t 2.61), w16 +12.7 % (t 6.41), w18 +10.4 % (t 4.86), while 2019 is flat (-0.06 %) and w7, w8 and w10 are slightly negative.
- **F6:** The same short-lookback continuation is weaker in rising bars (5-day Spearman 0.198, p 0.002, 239 cases) and absent in falling bars (-0.030, p 0.64). It lives mainly in the choppy profile.
- **F7:** The tested idea's own situation shows here. In choppy bars after a 30-day fall with the 10-day swing above the 30-day swing, the excess 10-day return is -6.02 % (t -3.36, 71 cases), against -1.95 % (t -1.77, 122 cases) without the quickening swing. The book still earned only +0.6 % a year, and its mean daily return on days in a position was 0.0002 against a cost of 0.22 % per trade.
- **F8:** Other patterns repeat what the map already holds and are left out:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `067-02.b2.b2.d2.g1_choppy-week-move-continues` (from F1, F2, F3, F5, F6): In a choppy market, the larger a coin's 5-day move against its usual daily swing, the further it keeps moving the same way over the next 10 days, up after a rise and down after a fall.
- `067-02.b2.b2.d2.g2_choppy-week-fall-continues` (from F3, F4, F7): In a choppy market, the deeper a coin's 5-day fall against its usual daily swing, the more it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
