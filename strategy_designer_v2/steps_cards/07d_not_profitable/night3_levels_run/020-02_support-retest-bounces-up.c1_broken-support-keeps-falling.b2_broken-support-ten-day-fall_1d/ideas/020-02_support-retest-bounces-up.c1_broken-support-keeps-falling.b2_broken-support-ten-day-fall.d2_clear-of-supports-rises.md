---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits high in its 60-day range, above every price where it turned up in the past 90 days, it tends to rise over the next 10 days, and the nearer the close is to its 60-day high, the larger the rise.
Consequence: A close near its 60-day high with no past support above it is a reason to be long for the next ten days, rather than short where supports sit overhead.
Why:
- F1: The book loses because it is a short book in coins that rise. On its 1164 short grid cases, the 10-day return is still +0.55 % on average (raw short gain -0.55 %, t -1.33). The normal drift against the short is -1.19 % and the total move is -0.66 % per case, which is -3.4 times the 0.19 % cost of a trade. In window after window the book's mean daily return mirrors the coin's with the opposite sign (w11: book -0.50 %, coin +1.26 %; w21: -0.39 % against +0.57 %; w7: +0.38 % against -0.47 %).
- F2: The situation picks out relatively weak stretches, not falling ones. Closes with a past turning-up low above them rise +0.55 % over 10 days. Closes with none above (the flat bars) rise +2.58 % (t 3.10, 527 cases). Welch t of active minus flat is -2.18.
- F6: Position in the 60-day range carries the move the book misses. Grid closes in the lower three fifths of the range rise only +0.43 % to +0.61 % over 10 days (t 0.5 to 0.8), and the book is short on 86 % to 100 % of them. Closes in the upper two fifths rise +2.24 % (t 2.18) and +2.70 % (t 2.45), and the book is short on only 40 % and 15 % of them.
