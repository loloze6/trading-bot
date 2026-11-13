---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin makes a new 20-day closing high after a 20-bar rise far larger than its usual 20-bar move, its next 5 bars fall by more than 10% more often than after a high reached through a moderate rise, without a larger average gain.
Consequence: Refuse or shrink longs on new highs that come at the end of an outsized run-up, and keep the long for highs reached by moderate climbs.
Why:
- F2: Long blocks that start after a large 20-bar run-up are where crashes concentrate, and they do not pay for the risk. Over 5 bars, with each 5-bar period counted once, blocks in the top run-up fifth (20-bar return above 33%, n=222) earn only +55 bp over the coin's mean (t=0.54). 18.0% of them lose more than 10%, and their 5th percentile is −19.0%. Blocks after a moderate 5.5–11.5% run-up (n=222) earn +177 bp (t=2.32), and only 6.3% lose more than 10%.
- F1: The Calmar failure comes from deep falls inside single windows, not from one bad stretch. The book's largest falls within a window were −33.4% (w10), −31.6% (w13), −30.7% (w22), −30.3% (w12) and −29.8% (w7), against a 10-day block mean of +1.36%. Across the 304 non-overlapping 10-day blocks of the book's daily returns, the worst was −18.4%, and the worst 10% of blocks hold 54% of all losses.
- F5: Held-day crashes rise steeply with recent volatility. The share of held days losing more than 8% grows from 0.7% in the lowest 20-day-volatility fifth to 7.9% in the highest (1117 days each). That top fifth still carries the largest 5-bar excess, +202 bp (n=222, t=2.03), so volatility alone raises both the gain and the falls.
