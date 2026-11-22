---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only while the coin stays close to its 60-day high; the closer to that high, the larger the rise.
Consequence: A trader buys short-lived dips near recent highs and refuses down-streaks deep in a correction, where the book's falls build.
Why:
- F1: The book's Calmar of 0.33 comes from a deepest fall of -58.5 % over 82 days across windows w16–w17, which is deeper than the coins' own chained fall of -43.9 % over the same days; the book's chain lost -56.9 %.
- F2: The book is mostly a leveraged long on the coins rather than a timing book: it is long on 75 % of bars with a mean allocation of 0.70, and of its mean gain of 1.82 bp per bar, 1.54 bp is the coins' own drift and only 0.27 bp is timing.
- F5: Cases also split by distance from the 60-day high, over about 790 cases per quintile:
