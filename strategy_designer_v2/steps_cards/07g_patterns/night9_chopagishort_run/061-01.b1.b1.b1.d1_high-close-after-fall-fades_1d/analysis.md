---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1_high-close-after-fall-fades_1d
idea tested: 061-01.b1.b1.b1.d1_high-close-after-fall-fades
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5076 USD
---
## Findings
- **F1:** Outside the choppy agitated profile, a close in the top quarter of the day's range after a negative 5-day return is followed by a 2-day unusual move of -1.51 % (t -2.51, 397 cases on 164 days). Inside the profile the same situation gives -3.06 % (t -1.96, 28 cases on 25 days). The effect the idea claims is therefore not confined to the market profile the brief names.
- **F2:** Outside the profile, this fade is graded by the depth of the 5-day fall measured against the coin's 20-day swing. The 2-day unusual move is -2.83 % (t -2.68, 125 cases, 61 days) in the deepest third, -1.56 % (t -1.81, 126 cases, 78 days) in the middle third and -0.03 % (t -0.05, 126 cases, 83 days) in the shallowest third.
- **F3:** Outside the profile, after a 5-day fall, the 2-day move is also graded by how high the close sits in the day's range: -0.17 % (t -0.31) for the lowest quarter, +0.03 % for the second, -0.51 % (t -0.92) for the third and -1.51 % (t -2.51) for the top quarter.
- **F4:** The out-of-profile fade is broad:
- **F5:** The tested book is in its profile on only 4.6 % of bars, and folds B and C produce just 79 trades, which is why it fails trades per day. Its trades are graded by forecast size: a mean net -1.90 % in the smallest third of |entry forecast|, +1.12 % in the middle third and +3.97 % in the largest third.
- **F6:** Two other patterns did not clear the bar for the number of angles looked at, or are already held:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.g1_high-close-after-fall-fades` (from F1, F2, F3, F4): When a coin's daily close sits near the top of that day's high-low range after its 5-day return has been negative, its price falls over the next two days. The deeper that 5-day fall is against the coin's usual daily swing, and the nearer the close is to the day's high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
