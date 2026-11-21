---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall compared with its 30-day volatility, the higher its return over the next 1 day.
Consequence: After a large daily fall, a trader would buy the coin for one day, and refuse it after small falls whose rebound does not cover the cost of a trade.
Why:
- F7: The 1-day reversal is the one clear effect, and it only shows over the next 1 day. Its rank correlation with the next day's unusual return is +0.079 (t 10.2, 16,523 cases), against +0.001 over 5 days.
- F8: That 1-day rebound comes from falls, and it grows with the size of the fall measured against the coin's 30-day volatility. On down days, from the smallest to the largest fifth of size, the next day's unusual return is +0.03 %, -0.09 %, +0.13 %, +0.23 % and +0.52 % (t 3.18, 1,143 cases). Up days show no such grading (+0.27 % falling to +0.05 %, t 0.35).
- F9: Only the largest falls are big enough to pay for a trade. In the largest fifth of falls the rebound of +0.52 % per case is about 2.7 times the backtest's round-trip cost of 0.19 %. The smaller fifths sit below that cost, so a book on this idea would pay only on its largest falls (findings F11, F4).
