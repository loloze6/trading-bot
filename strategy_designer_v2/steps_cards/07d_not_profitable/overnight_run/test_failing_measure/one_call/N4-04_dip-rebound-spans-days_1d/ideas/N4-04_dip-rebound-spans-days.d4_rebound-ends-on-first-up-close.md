---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a sharp dip in an uptrend, the first up-close above about one percent marks the end of the rebound, and the coin's next days return below its average.
Consequence: A trader should leave the dip long on the first strong up day instead of holding it into later falls.
Why:
- F6: Once a dip has rebounded, the edge is spent. On held days that follow an up-close above +0.97%, the coin's next-day return averages -0.24% (n=590). On held days that follow drops below -2.55%, it averages +0.47% to +0.83% (n=590 and 589).
- F2: The loss comes from positions the dip does not repay quickly. Of 1432 trades, the 1017 closed within 1.5 days average +1.11% after fees. The 251 that lasted 1.5 to 3.5 days average -4.35% (worst -28.9%), and the 86 that lasted 3.5 to 7.5 days average -3.59%. A dip that keeps falling after entry is what the book holds into its falls.
