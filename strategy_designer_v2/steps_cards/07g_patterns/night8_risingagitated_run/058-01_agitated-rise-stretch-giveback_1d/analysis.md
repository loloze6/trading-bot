---
line: 7.g patterns
backtest: 058-01_agitated-rise-stretch-giveback_1d
idea tested: 058-01_agitated-rise-stretch-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5331 USD
---
## Findings
- **F1:** In the rising agitated profile the tested giveback is not in the bars: on the 5-day grid the distance above the 20-day average has a positive slope against the next 5 days' unusual move (0.042 per point, t 0.95, 304 cases), and its top fifth (16 % to 86 % above the average) is followed by +0.83 % (t 0.49), not a fall. The book this built lost money (mean daily return -0.041 %), and its daily returns moved against the coin's (correlation -0.40).
- **F2:** Across all profiles, the coin's 20-day return divided by its 20-day swing (its daily standard deviation × √20) predicts a move the same way over the next 5 days, not a reversal. The slope is 1.04 (t 3.56, 1,364 non-overlapping cases), its fifths rise in order from -1.57 % (t -1.97) to +1.57 % (t 2.01), and the slope is positive on all 6 coins (t 0.82 to 2.22).
- **F3:** This continuation is strongest in a choppy market (60-day return between -10 % and +10 %): slope 4.55 (t 4.60, 125 cases), against 1.93 (t 2.60) in a rising market and 0.55 (t 0.80) in a falling one. Its mean move in the signal's direction is +3.81 % per case, a strength of 0.303 (day-clustered t 2.70, 65 days), against 1.31 % (strength 0.105, t 2.49, 256 days) over all profiles.
- **F4:** In the choppy market it holds in both of the agitation splits, agitated (slope 9.66, t 3.32, 29 cases) and calm (slope 3.03, t 3.09, 96 cases). It holds on all 6 coins (slopes 1.3 to 14.6) and at 10 days too (slope 5.87, t 3.09, 62 cases). It is positive in 7 of the 10 windows with at least 5 cases.
- **F5:** The strongest part of the choppy continuation is the falling side. The lowest quarter of the scaled 20-day return (-1.85 to -0.55) is followed by -7.15 % against the drift over 5 days (t -3.05, 32 cases), and the next quarter by -2.92 % (t -2.41, 31 cases). The highest quarter gives +2.91 % (t 1.17, 31 cases). The map has no strategy specialised short in choppy agitated, and only one in choppy calm.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g1_choppy-scaled-move-continues` (from F2, F3, F4): In a choppy market, the larger a coin's 20-day return is against its usual daily swing over those 20 days, the further the coin keeps moving the same way over the next 5 days.
- `058-01.g2_choppy-scaled-fall-continues` (from F3, F5): In a choppy market, the further a coin has fallen over 20 days against its usual daily swing over those days, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
