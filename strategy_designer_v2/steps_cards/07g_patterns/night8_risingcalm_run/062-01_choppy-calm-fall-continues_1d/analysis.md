---
line: 7.g patterns
backtest: 062-01_choppy-calm-fall-continues_1d
idea tested: 062-01_choppy-calm-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3668 USD
---
## Findings
- **F1:** Only in choppy markets (60-day return between -10 % and +10 %) does the next 5-day excess return clearly rise with the swing-scaled 5-day return: 6.27 % per unit, t 2.82, 125 cases on 65 days. That is far steeper than in rising markets (1.96 %, t 1.76), falling markets (1.10 %, t 0.98) or all bars together (1.08 %, t 1.62, 1364 cases). The relation therefore points to continuation on both sides inside choppy markets.
- **F2:** Inside the tested choppy calm profile the same slope is weaker (1.76 % per unit, t 1.58, 178 cases on 92 days), and its z5 quintiles are not monotone. The largest falls were followed by -3.27 % excess (t -1.71, 36 cases), but the middle quintile also fell, by -1.85 %. So the choppy edge does not come from the calm half alone, and the falls-only reading of the brief is not graded.
- **F3:** The tested short-only idea is inconclusive: the mean short excess is +0.61 % (t 0.97, 269 cases, 164 days) and its strength is 0.043. Its total move is -0.25 % per case against a cost of 0.19 % per trade, and the book's Sharpe is 0.04 against holding's 0.57 (difference -0.53).
- **F4:** The continuation sign is broad but weak outside choppy markets. On all bars, the lowest z5 quintile shows -1.47 % excess (t -0.99) and the highest +1.64 % (t 1.45). The slope on z5 is positive for all 6 coins (0.48 % to 2.57 %, t 0.47 to 1.67) and in 3 of 4 years. On falls only it is 1.35 % (t 0.75), on rises only 0.99 % (t 1.08).
- **F5:** The other angles showed nothing that stands out from chance after this many looks. Next-day excess by weekday has a largest |t| of 1.52. The quintiles of range in swing units, close position in the day's range and 30-day swing all have |t| ≤ 1.18. The second z10 quintile shows -2.45 % (t -2.66), but it sits between quintiles of +0.41 % and -0.13 %, so it is not graded.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `062-01.g1_choppy-scaled-move-continues` (from F1, F2, F4): In a choppy market, a coin's 5-day return measured against its 30-day daily swing continues over the next 5 days, falls falling further and rises rising further. The larger the swing-scaled 5-day move, the larger the move that follows in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
