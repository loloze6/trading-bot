---
line: 7.g patterns
backtest: 036-01_fall-vs-swing-next-day-rebound_1d
idea tested: 036-01_fall-vs-swing-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4097 USD
---
## Findings
- **F1:** Among falls of at least one usual move (z ≤ -1; 767 cases), the next-day excess return grows with the raw size of the fall: slope on the day's return -0.32 (t -2.64, clustered by day). The same fall scaled by the 30-day swing gives a slope of -0.012 (t -1.26). With the swing level added, the raw slope stays at -0.37 (t -2.70) and the swing level adds nothing (-0.009, t -0.58). This is why the forecast, graded on the scaled fall, failed its top-minus-bottom check.
- **F2:** Split by quartile of the raw fall, only the deepest quartile rebounds clearly: falls beyond about -9.4 % are followed by +2.07 % excess the next day (t 1.99, 193 cases, 84 days). The other three quartiles give +0.21 % to +0.62 % (t 0.5 to 1.6).
- **F3:** Across all days, the next-day excess return falls as the scaled move rises: slope on z -0.0034 (t -2.37, 6529 cases). Large rises are not mirrored: rises beyond one usual move are followed by -0.14 % to -0.24 % (t -0.15 to -0.70). The effect is one-sided, on falls.
- **F4:** Down days when the coin's 30-day swing is in its top quartile against its own median give +1.22 % excess the next day (t 2.75, 796 cases, 339 days). The three calmer quartiles give +0.24 %, +0.04 % and -0.18 % (t 1.13, 0.19, -0.65). Among falls of at least one usual move, the rebound rises with the swing level: +0.27 %, +0.81 %, +1.39 % by tercile.
- **F5:** Where the day closes in its range adds nothing beyond the day's return. Alone its slope is -0.0117 (t -2.91), but next to the return it drops to 0.0002 (t 0.03) while the return keeps -0.088 (t -2.03). The close-location pattern is the fall itself.
- **F6:** The book's gain per position day grows with the depth of the fall: +0.43 %, +0.43 %, +0.75 % and +2.01 % for z buckets from -1 to below -2.5 (t 1.4, 1.2, 1.5, 1.6). The deepest bucket's rebound is about ten times the 0.19 % cost of a trade.
- **F7:** Other angles did not stand out after counting the more than 20 looked at. These were the weekday of the fall (Thursday +2.56 %, t 2.61, only 42 days), the 60-day trend (rising +1.26 %, t 2.16; falling +0.92 %, t 1.39; choppy -0.36 %), the prior 5-day return, the coin and the 2- and 3-day horizons.

## Ideas
- `036-01.g1_raw-fall-depth-next-day-rebound` (from F1, F2, F6): The larger a coin's one-day percentage fall, measured in raw terms rather than against its recent swing, the larger its rise over the next day.
- `036-01.g2_agitated-market-fall-rebound` (from F4, F1, F3): In an agitated market, the larger a coin's one-day fall, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
