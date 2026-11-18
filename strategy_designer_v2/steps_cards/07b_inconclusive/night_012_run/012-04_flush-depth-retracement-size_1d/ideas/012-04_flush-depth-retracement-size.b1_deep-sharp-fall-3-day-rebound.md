---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.b inconclusive
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among days on which a coin falls sharply compared with its own last 20 days of daily moves, the larger that day's close-to-close fall, the larger the coin's rise over the next 3 days.
Consequence: After a sharp daily fall, a trader would lean long for 3 days in proportion to the size of the fall, with or without a volume burst or a long wick, and would refuse the trade after only modest sharp falls.
Why:
- F4: Across all sharp falls (one-day z of -2 or lower, 411 independent cases), the size of the day's fall grades the next 3 days clearly: the slope t of excess 3-day return on the one-day return is -5.16 (-5.02 with the 1% tails trimmed), and the slope t on the open-to-low drop is +4.53, so a deeper fall is followed by a larger rise.
- F5: That grading in F4 sits mostly in the deepest falls and is broad across coins and years: the deepest quintile (mean one-day return -17.9%) is followed by +2.35% excess over 3 days, while the other quintiles run from -0.95% to +0.21%; all 6 coins have a negative slope t (-1.08 to -3.24), and 6 of the 8 years do (2022 is the exception at +1.68).
- F6: The volume burst and the wick are not what carries the rebound: among sharp falls the wick slope t is -0.97 at 3 days (-0.33 at 5 days and -0.73 at 10), and the grading by one-day fall holds in the non-flush falls (t -5.06, n 362) but not in the flush ones (t -0.93, n 49).
- F2: Flush bars show no rebound of their own over 3 days: the mean excess 3-day return is +0.0021 (t 0.28, 84 independent cases), against +0.0027 after other sharp falls (367 cases, Welch t -0.07); at 1 day flushes do worse than other sharp falls (-0.0068 against +0.0090, Welch t -2.33).
- F1: The tested forecast barely varies, so its slope cannot show grading: 78% of the flush cases sit at the cap of 20, the forecast's standard deviation across them is 2.09, and the middle and top terciles both average exactly 20.
