---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, it rises over the next three days, and the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, the larger the rise.
Consequence: A 4-hour sell-off far larger than usual is a reason to buy for a three-day rebound, whatever the volume did during it.
Why:
- F2: The effect shows only on the largest losses. On the raw streak loss in usual moves (not standardised), the top fifth (median 4.0 usual moves) gains 1.32 % over 18 bars (t 4.43, 917 cases), while the bottom fifth (median 0.53) loses 0.72 % (t −3.09, 922 cases). The middle three fifths are near zero or negative (−0.06 %, −0.37 %, −0.20 %).
- F3: Fading volume adds nothing measurable. Among streaks rebuilt from prices in the top loss fifth (median 4.17 usual moves), those with fading volume gain 1.41 % (t 2.88, 423 cases, strength 0.16) and those with rising volume gain 1.02 % (t 2.91, 634 cases, strength 0.11); the difference, fading minus rising, is 0.39 % (Welch t 0.65).
- F4: Over the next 18 bars the rebound is clearest. Over all cases, the 6-bar mean is +0.06 % (t 0.92), the 18-bar mean is −0.005 % (t −0.04) and the 36-bar mean is −0.13 % (t −0.70). In the top forecast fifth, the 18-bar mean of +0.66 % (t 2.00) exceeds the 36-bar mean of +0.66 % (t 1.31) in reliability.
