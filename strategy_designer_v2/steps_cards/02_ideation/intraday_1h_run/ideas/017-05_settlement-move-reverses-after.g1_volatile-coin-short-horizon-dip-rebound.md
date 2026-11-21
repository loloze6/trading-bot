---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's recent hourly volatility (its 7-day mean absolute hourly move) is high, the larger its 2-hour fall relative to its usual 2-hour move, the larger its rise over the next 2 hours, at any hour of the day.
Consequence: A sharp 2-hour fall in a volatile coin is a reason to buy for a 2-hour rebound, and the trade can be scaled to the size of the fall.
Why:
- F2: Across all hours, on the non-overlapping 2-bar grid, the next 2-hour return falls steadily as the past 2-hour z rises. The lowest z quintile (mean z -1.98) gains 7.96 bp (t=9.27, n=40,965), the middle quintile loses 0.77 bp (t=-1.17) and the highest quintile (mean z +1.97) loses 3.28 bp (t=-4.29). The rebound after falls is about 2.4 times the size of the give-back after rises.
- F3: The reversal sits almost entirely in high-volatility conditions, measured as the 168-hour mean absolute hourly return in coin terciles. On the grid the scored reversal is 0.58 bp in the low tercile (t=1.05), 2.67 bp in the middle (t=3.80) and 11.96 bp in the high tercile (t=10.17). On settlement bars alone it is -1.77 bp (t=-1.42), 1.68 bp (t=1.15) and 12.57 bp (t=4.95). Within the high tercile, the lowest z quintile gains 18.6 bp over the next 2 hours (t=8.84) and the highest loses 7.03 bp (t=-3.90).
- F5: Among coins, the settlement-bar reversal is larger in ZEC (10.1 bp, t=3.17) and XMR (6.3 bp, t=2.60) than in BTC (0.3 bp, t=0.17) and ETH (0.7 bp, t=0.32). This matches the volatility gradient in F3.
- F1: The reversal of a 2-hour move is not tied to funding settlement. Scored as minus the clipped 2-hour z times the next 2-hour excess return, the non-settlement hours earn 5.24 bp (t=14.3, n=361,667). The three settlement hours earn 0.14 bp at hour 7 (t=0.09), 4.52 bp at hour 15 (t=2.24) and 8.14 bp at hour 23 (t=4.54). Several ordinary hours score higher: hour 11 earns 14.6 bp (t=7.70), hour 20 earns 11.7 bp (t=7.41) and hour 12 earns 12.3 bp (t=6.22).
