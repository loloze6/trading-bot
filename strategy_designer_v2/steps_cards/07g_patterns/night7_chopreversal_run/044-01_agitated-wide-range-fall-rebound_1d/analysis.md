---
line: 7.g patterns
backtest: 044-01_agitated-wide-range-fall-rebound_1d
idea tested: 044-01_agitated-wide-range-fall-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6171 USD
---
## Findings
- **F1:** Among the agitated down days, the next-day rebound sits almost entirely in the falling trend (60-day return below -10 %): the mean next-day excess return is +1.40 % (t 2.42, 377 cases on 147 days) against +0.01 % (t 0.02, 358 cases) in a rising trend and -2.19 % (t -1.13, 61 cases) in a choppy one, and the book's active bars split the same way.
- **F2:** Inside the falling agitated profile, the next-day rise grows with the product of the fall's size against the 30-day swing and the day's range against its 30-day mean. By tercile of that product it is +0.15 % (t 0.17), +1.43 % (t 1.99) and +2.61 % (t 2.42), with about 125 cases each. The rank correlation is 0.19 (p 0.0002, 377 cases). The slope is positive in all six coins (44 to 148 bp per unit) and in all four years (53 to 136 bp). The top tercile beats the bottom one in each year (2018 +1.87 % vs -2.69 %; 2019 +0.48 % vs -0.37 %; 2020 +6.67 % vs +1.86 %; 2021 +1.59 % vs -1.05 %).
- **F3:** The day-clustered t of the falling-agitated slope (11.3) is inflated by a few extreme cases: without the top 5 % of products the slope stays similar (76 bp) but its t falls to 1.16, so the grading rests on the rank and tercile evidence of F2.
- **F4:** Outside the agitated profile the product does not grade the rebound: the slope is -17 bp (t -1.02) in choppy calm, -6 bp (t -0.50) in falling calm and +19 bp (t 0.87) in rising calm.
- **F5:** The rebound after a falling-agitated fall is spent in one day: the second day's excess return is -0.73 % (t -1.47, 375 cases), and after all large agitated falls it is +0.17 % (t 0.32, 417 cases).
- **F6:** The mirror shows up, but weakly. In the falling agitated profile, an up day is followed by a next-day excess fall that grows with the up-day product of size against swing times range against usual range: by tercile -0.63 % (t -0.97), -0.83 % (t -1.38) and -1.68 % (t -2.17). The rank correlation is -0.13 (p 0.013, 361 cases). The mean is negative in all six coins and all four years. It loses its significance without the top 5 % of products (t -0.58).
- **F7:** The other angles show nothing that stands out from chance after this many looks: weekday of all days (largest |t| 1.55), weekday of agitated falls (largest t 1.87), and close location on agitated days (lowest quintile +0.85 %, t 1.76).

## Ideas
- `044-01.g1_falling-agitated-wide-fall-rebound` (from F1, F2, F3, F4, F5): In a falling, agitated market, after a day the coin closes lower, the next day's rise grows with the product of the day's fall against the coin's 30-day standard deviation of daily returns and the day's high-to-low range against its average daily range over the past 30 days; the largest falls on the widest days are followed by the largest rises over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `044-01.g2_falling-agitated-wide-rally-fade` (from F6): In a falling, agitated market, after a day the coin closes higher, the next day's fall grows with the product of the day's rise against the coin's 30-day standard deviation of daily returns and the day's high-to-low range against its average daily range over the past 30 days; the largest rises on the widest days are followed by the largest falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
