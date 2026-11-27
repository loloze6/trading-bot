---
line: 7.g patterns
backtest: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling_1d
idea tested: 067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3706 USD
---
## Findings
- **F1:** On the 5-day grid, the raw stretch (close minus its 20-day average, over the average, divided by the 20-day standard deviation of daily returns) predicts the next 5 days' excess return in the same direction in a choppy 60-day trend. The slope is 0.0190 per unit with t 2.30 (127 cases, 66 days), and both sides point the same way: above the average slope 0.0136 (t 1.39, 67 cases), below it 0.0308 (t 1.18, 60 cases).
- **F2:** The tested forecast standardised the stretch against its own last 60 values, and that measure gave a slope t of −0.56. The raw stretch's quintiles inside the backtest's choppy regime are monotone at the low end instead: lowest quintile −6.71 % excess over 5 days (t −2.80, 35 cases), against +0.86 % and +0.66 % in the top two. The standardisation likely hid the level that carries the effect.
- **F3:** Pooled over all trends, the raw stretch's continuation is weak. Its slope is 0.0052 (t 2.03, 1422 cases, 256 days), and no single window (|t| ≤ 1.17), coin (t 1.24 to 1.84) or year (t 0.07 to 1.37) shows it on its own. In a rising trend it reaches t 2.05, which repeats the rising-market continuation ideas the map already holds.
- **F4:** The lower a coin's 20-day swing against its 90-day swing, the more it rises over the next 5 days, quartile by quartile:
- **F5:** After the lowest fifth of one-day returns, the next day's excess is +0.72 % (t 4.61, 1724 cases). This is the next-day rebound the map already holds in many cells, so it is not a discovery.
- **F6:** Weekday means of the next day's excess range from −0.49 % on Wednesday (t −2.69) to +0.47 % on Thursday (t 3.19). These are 7 groups among many angles looked at, so the pattern is not held as a finding to build on.

## Ideas
- `067-01.b1.b1.b1.g1_choppy-raw-stretch-carries-both` (from F1, F2): In a choppy market, the further a coin's close stands from its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin keeps moving the same way over the next 5 days, rising after closes above the average and falling after closes below it.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `067-01.b1.b1.b1.g2_swing-contraction-precedes-rise` (from F4): The lower a coin's swing over the last 20 days stands against its swing over the last 90 days, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
