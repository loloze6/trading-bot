---
line: 7.g patterns
backtest: 037-01.b1_choppy-extended-fall-continues_1d
idea tested: 037-01.b1_choppy-extended-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6309 USD
---
## Findings
- **F1:** In the choppy profile (60-day return within ±10 %), the coin's 20-day return in units of its 20-day daily swing predicts the next 5-day unusual move in the same direction: the slope is 0.065 per swing unit (t 2.65, 189 non-overlapping cases), and over 10 days it is 0.088 (t 2.55, 96 cases). Measured on the backtest's own profile regimes, the 5-day slope is 0.040 (t 2.17, 346 cases).
- **F2:** Inside the choppy profile, the 20-day move carries the continuation more than the 5-day fall the tested idea used. In the tested situation (choppy, 20-day return below 0), a 5-day fall of 0.3 to 1 swing is followed by a 5-day unusual move of -5.7 % (t -2.80, 50 cases), but a fall of 1 to 2 swings only by -5.0 % (t -0.91, 28 cases). Step 5's own slope on the 5-day forecast was -0.0004, so there is no grading by the 5-day fall.
- **F3:** In the choppy profile, a 20-day fall is followed by a lower-than-usual 5-day move in every year. The means are -6.9 % (2018, t -1.84), -2.4 % (2019, t -1.99), -4.7 % (2020, t -0.70) and -8.1 % (2021, t -2.51). Over 10 days the same falls give -14.4 % in 2021 (t -3.36), and the 20-day swing-unit bin from -1 to -0.5 gives -6.6 % (t -2.46). Grading inside falls alone is weak: slope 0.053, t 0.96 at 5 days.
- **F4:** The same choppy grading on the 20-day move is in the 2020 and 2021 cases but not the earlier ones. The yearly 5-day slopes are -0.030 (2018, 20 cases), -0.003 (2019), 0.072 (2020, t 1.21) and 0.088 (2021, t 2.57). The 10-day slopes are positive in 2019, 2020 and 2021 (0.033, 0.104, 0.108).
- **F5:** In the rising profile, the 10-day move continues a 5-day or 20-day move in swing units: slope 0.041 on the 5-day (t 2.21) and 0.040 on the 20-day (t 2.34), 239 cases. The 5-day slope is positive in each year with enough cases: 0.045 (2019, t 2.62), 0.044 (2020, t 1.44), 0.038 (2021, t 1.27). At 5 days it is weaker (t 1.30). In the falling profile there is no grading (5-day slope t 1.01, 10-day t -0.28).
- **F6:** None of the other angles stands out given how many were looked at, with |t| at or under 2.2 everywhere. Weekday next-day moves have |t| ≤ 1.47. After a one-day fall of more than 2.5 swings, the next day is +1.7 % (t 1.43). The close's place in the day's range, the day-range quartile and the 20-day volatility quartile outside the choppy profile give |t| ≤ 2.2, with no monotone pattern.

## Ideas
- `037-01.b1.g1_choppy-twenty-day-fall-continues` (from F1, F2, F3): In a choppy market, the more of its own 20-day daily swings a coin's 20-day fall spans, the more the coin falls over the next 10 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `037-01.b1.g2_choppy-market-swing-scaled-momentum` (from F1, F4): In a choppy market, a coin keeps moving over the next 5 days in the direction of its 20-day return, and moves further the more of its own 20-day daily swings that return spans.
- `037-01.b1.g3_rising-market-swing-momentum` (from F5): In a rising market, the more of its own 20-day daily swings a coin's 20-day rise spans, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
