---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only when the streak's loss is among the largest the coin has made relative to its typical four-hour move over the past 30 days; the larger that loss, the larger the rise.
Consequence: Only an exceptionally deep 4-hour sell-off, not an ordinary down streak, is a reason to buy for a three-day rebound.
Why:
- F1: The test's zero result (mean +0.0003 %, t 0.002, 4,537 cases) is an average of two opposite halves: by forecast quintile, the lowest fifth of cases loses 0.66 % against drift over 18 bars (t −2.84, 915 cases) and the highest fifth gains 0.66 % (t 2.00, 915 cases), the mean rising steadily from quintile 0 to 4 (−0.66, −0.37, −0.11, +0.45, +0.66 %).
- F2: The effect shows only on the largest losses. On the raw streak loss in usual moves (not standardised), the top fifth (median 4.0 usual moves) gains 1.32 % over 18 bars (t 4.43, 917 cases), while the bottom fifth (median 0.53) loses 0.72 % (t −3.09, 922 cases). The middle three fifths are near zero or negative (−0.06 %, −0.37 %, −0.20 %).
- F5: The large-loss rebound is mixed across years, with bear years against it. For fading-volume streaks in the top loss fifth:
