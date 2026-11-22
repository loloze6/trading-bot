---
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size_4h
idea tested: 024-01_fading-volume-uprun-giveback-size
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3774 USD
---
## Findings
- **F1:** Coins kept rising after up-runs instead of giving them back. On the first case per 18-bar cell, 4 or more 4h up bars in a row were followed over the next 3 days by a move above the coin's normal drift of +0.59 % (strength 0.069, t 2.58, n 1437) when volume faded. With rising volume the move was +0.51 % (strength 0.058, t 2.45, n 1813). The tested idea's short entries themselves showed +0.11 % (t 0.35, n 1258) against the short.
- **F2:** The continuation grew with the run. Runs of 6 or more up bars were followed by +1.38 % above drift over 3 days (strength 0.157, t 3.52, n 612). This is far above the 0.19 % cost of a trade.
- **F3:** Inside 4-bar up-runs the continuation also grew with the run's gain, measured in the coin's 30-day 4h volatility. By gain tercile the move over 3 days was −0.39 % (t −1.27, n 757) for the lowest, +0.66 % (t 2.34, n 756) for the middle and +1.03 % (t 2.25, n 757) for the highest.
- **F4:** On the non-overlapping 18-bar grid, the top quintile of the 3-day volatility-scaled return was followed by +0.91 % above drift over the next 3 days (strength 0.102, t 3.00, n 1032). The middle quintiles were followed by −0.25 % to −0.51 %. The top-quintile continuation held in the calmer half of 30-day volatility (+1.04 %, t 3.12, n 667) and was weaker in the more volatile half (+0.67 %, t 1.07, n 365).
- **F5:** Falls did not mirror rises. Down-runs of 4 or more bars were followed by −0.16 % (fading volume, t −0.76) and −0.37 % (rising volume, t −1.89). The smallest-gain tercile of down-runs continued down by −1.02 % (t −3.87, n 711), while the largest tercile turned up by +0.75 % (t 1.84, n 711).
- **F6:** The book lost on every coin, with mean daily returns from −0.033 % (BTC) to −0.080 % (ZEC) while holding the coins earned +0.07 % to +0.15 % a day. Its SHORT trades lost on average on every coin, from −1.15 % (BTC) to −4.37 % (ZEC) after fees, while its LONG trades gained +0.63 % to +2.57 %.
- **F7:** The top quintile of bar volume relative to its 30-day mean was followed over 3 days by +1.12 % above drift (strength 0.123, t 3.31, n 1032). The lowest two quintiles were followed by about −0.48 % (t −1.96 and −1.77). This grouping did not separate up bars from down bars.
- **F8:** Timing effects stood out above the many angles examined, but they are fixed calendar conditions rather than graded situations. The 4h bar after the one opening at 16:00 UTC returned +0.048 usual 4h moves (t 5.73, n 16066), and the bar after a Friday bar returned +0.053 (t 6.01, n 13735).

## Ideas
- `024-01_fading-volume-uprun-giveback-size.g1_long-up-run-continues-rising` (from F1, F2, F3, F6): When a coin has just risen for many four-hour periods in a row, it keeps rising over the next three days. The longer the streak, and the larger its gain against the coin's typical four-hour move over the past 30 days, the larger the further rise.
- `024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues` (from F4, F2): When a coin's 3-day return is high against its typical move over the past 30 days, it rises further over the next three days. The higher that scaled return, the larger the rise, and the effect is strongest when the coin's 30-day volatility is low.
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise` (from F7): When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days. The higher the volume against that average, the larger the rise.
- `024-01_fading-volume-uprun-giveback-size.g4_shallow-down-run-keeps-falling` (from F5): When a coin has fallen for four or more four-hour periods in a row with only a small total loss against its typical four-hour move over the past 30 days, it keeps falling over the next three days. The smaller the run's loss for its length, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
