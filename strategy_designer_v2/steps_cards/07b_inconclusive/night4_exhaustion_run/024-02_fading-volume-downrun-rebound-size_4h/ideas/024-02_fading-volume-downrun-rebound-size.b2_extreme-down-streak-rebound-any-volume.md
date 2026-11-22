---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods whose loss is several times its typical four-hour move over the past 30 days, it rises over the next one to three days, whatever the volume did during the streak. The larger the loss relative to that typical move, the larger the rise.
Consequence: A trader can buy into an extreme down-streak's rebound without waiting for volume to fade, which roughly doubles the number of opportunities.
Why:
- F2: The rebound appears only in the largest losses relative to the usual move. The top decile of the streak's loss in usual moves (mean 5.9 usual moves, 422 cases) has a mean 18-bar unusual move of +2.03 % (t 4.18), and the ninth decile (3.3 usual moves) has +0.75 % (t 1.95). Deciles 0 to 6 (0.4 to 2.0 usual moves) are all at or below zero, between −0.32 % and −0.93 %, with the second decile at t −2.80. Over the whole set, the forecast's above-median minus below-median difference is +1.07 %.
- F3: The top quintile of relative loss (at least 2.8 usual moves, 843 cases) gives a clear and stable result. Its mean 18-bar unusual move is +1.39 % (t 4.48), a strength of 0.165. It is also positive at 6 bars (+0.71 %, t 3.93) and at 12 bars (+0.97 %, t 3.61). It is positive in all six coins, from LTC's +0.32 % (t 0.53) to ZEC's +2.37 % (t 2.31). It is positive in 6 of 8 years; the exceptions are 2018 (−0.34 %) and 2022 (−1.06 %).
- F5: The fading volume the idea requires adds little to the large-loss rebound. Among all down-streaks recomputed from prices, the top relative-loss quintile gives +1.41 % over 18 bars with fading volume (t 2.88, 423 cases) and +1.02 % with rising volume (t 2.91, 634 cases). Over 6 bars the order reverses: +0.27 % (t 1.04) with fading volume against +0.63 % (t 2.70) with rising volume.
- F7: In its large-loss part, the idea's move covers the cost of a trade many times over. The top quintile's total 18-bar move per case is +1.80 %, about 9 times the 0.19 % a trade cost, against 0.41 % (2.1 times) for all cases.
