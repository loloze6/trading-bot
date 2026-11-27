---
line: 7.g patterns
backtest: 061-01.b1_high-close-fade-more-coins_1d
idea tested: 061-01.b1_high-close-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6905 USD
---
## Findings
- **F1:** The fade the idea describes is a one-day effect. On the bars in the recorded choppy-agitated profile, the coin's unusual next-day return falls as the close sits higher in the day's range: slope −0.033 per unit of close location, t −2.37, 449 non-overlapping cases. At 2 days the slope is about the same, −0.032, but cannot be told from zero (t −1.10, 227 cases), and the tested 2-day horizon dilutes it (step 5: t 1.74).
- **F2:** The effect is graded across the whole range, not only above 0.8, and it peaks before the very top. In choppy and falling agitated markets together, the mean unusual next-day move by close-location bin is +1.64 % (0–0.2), +0.72 % (0.2–0.4), −1.09 % (0.4–0.6), −1.78 % (0.6–0.8) and −1.05 % (0.8–1), with about 250 cases per bin. This explains why step 5's upper-half-minus-lower-half check inside the ≥ 0.8 regime failed (−0.31 %).
- **F3:** The effect needs agitation. With the coin's own 60-day trend and its 30-day swing against its recent median, the next-day slope on close location is:
- **F4:** The choppy-agitated next-day slope survives leaving out any one window: slope from −0.046 to −0.026, t from −2.41 to −2.06. It is negative in every year shown, 2018 to 2021, at −0.036, −0.022, −0.074 and −0.020 (t −1.91 to −1.09).
- **F5:** The move is large against the cost of a trade. A next-day spread of about 3.4 % between the lowest and highest close-location bins (F2), or 1.8 % between the middle and the 0.6–0.8 bin, is several times the 0.22 % a trade costs. The tested book instead earned +1.3 % a year (Sharpe 0.34, in a position on 4 % of coin-days), because it held 2 days and traded only closes ≥ 0.8.
- **F6:** In the recorded profile, closes ≥ 0.8 are followed by an unusual 5-day fall of −7.2 % (t −2.80, n 21). This rests on too few cases to count after this many angles, and its windows disagree: w12 is +2.6 %, w16 is −17.2 %.
- **F7:** In falling agitated markets the same next-day fade (F3, t −2.92) is already held on the short side by 060-01.g1.d2.d1, "own range close height fade". The matching low-close rebound is held on the long side in the agitated profiles by 045-01 and 039-02. Neither is a new discovery. The choppy-agitated short box of the map is empty.

## Ideas
- `061-01.b1.g1_choppy-agitated-close-next-day-fade` (from F1, F2, F3, F4, F5): In a choppy, agitated market, the higher a coin's daily close sits within that day's high-low range, the more its price falls over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
