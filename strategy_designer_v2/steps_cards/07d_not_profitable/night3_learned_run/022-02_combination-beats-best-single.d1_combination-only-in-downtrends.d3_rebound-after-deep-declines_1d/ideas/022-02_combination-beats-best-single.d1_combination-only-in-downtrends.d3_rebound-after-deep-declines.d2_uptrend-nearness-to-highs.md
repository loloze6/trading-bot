---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is positive, the closer its close stands to its 90-day high, the higher its return over the next 5 days.
Consequence: A trader stays long in coins rising over the quarter and trading near their highs, which is where this book sat out and lost ground to holding.
Why:
- F3: The gain is lost to holding mostly because the book is out when the coin's 90-day return is positive. Those bars earn +0.10 % excess per 5 days on 1767 grid cases, against -0.10 % on 1652 cases in the tested regime. Near the 90-day high (within 10 %) they earn +1.05 % excess (t 2.56, 775 cases; total move +1.63 %, about 8.6 times the 0.19 % cost). The book gives up this continuation and trails the coin's mean daily return in 21 of 24 windows.
- F6: The tested idea's size at the tested depths is below the cost. Its unusual move is -0.44 % per case (strength -0.050), and its total move of +0.13 % is 0.7 times the 0.19 % round trip. Only the deepest cases (F1) have a move many times the cost.
