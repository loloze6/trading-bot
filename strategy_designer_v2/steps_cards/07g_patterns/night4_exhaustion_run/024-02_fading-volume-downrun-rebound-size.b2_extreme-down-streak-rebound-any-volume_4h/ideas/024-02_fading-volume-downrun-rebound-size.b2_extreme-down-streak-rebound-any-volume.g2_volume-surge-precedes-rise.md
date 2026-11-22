---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's traded volume over the past day is high relative to its 30-day average volume, it rises over the next 3 days; the higher that ratio, the larger the rise.
Consequence: A trader can lean long on coins whose volume over the last day has surged against their month's norm, and lean away from those whose volume has dried up.
Why:
- F4: High recent volume predicts a rise over the next 3 days. Volume is measured as the last day's volume over the 30-day average. Its top quintile (ratio 2.25) is followed by +0.108 usual moves (t 3.04) and its bottom quintile (ratio 0.36) by -0.087 (t -3.07). The slope is positive on all six grid offsets (t 3.04 to 5.12).
- F5: Volume adds information beyond price. In a joint regression on 5,292 base-grid cases, log of the day's volume ratio has beta 0.096 (t 4.59) next to the 3-day return's beta 0.062 (t 3.69). In the same regression the 1-day return's beta is -0.050 (t -2.98).
