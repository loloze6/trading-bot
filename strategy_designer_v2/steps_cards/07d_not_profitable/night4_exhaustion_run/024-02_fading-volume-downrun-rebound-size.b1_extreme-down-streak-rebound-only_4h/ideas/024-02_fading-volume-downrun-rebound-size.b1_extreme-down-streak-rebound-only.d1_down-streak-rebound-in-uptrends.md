---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only while the coin's 30-day return is positive; the larger that 30-day rise, the larger the rebound.
Consequence: A trader buys fading-volume down-streaks only as dips inside a strong 30-day uptrend, and stays out of those inside a decline, which keep falling.
Why:
- F1: The book's Calmar of 0.33 comes from a deepest fall of -58.5 % over 82 days across windows w16–w17, which is deeper than the coins' own chained fall of -43.9 % over the same days; the book's chain lost -56.9 %.
- F2: The book is mostly a leveraged long on the coins rather than a timing book: it is long on 75 % of bars with a mean allocation of 0.70, and of its mean gain of 1.82 bp per bar, 1.54 bp is the coins' own drift and only 0.27 bp is timing.
- F4: Down-streak cases split sharply by the coin's 30-day return, over 643 cases per quintile:
