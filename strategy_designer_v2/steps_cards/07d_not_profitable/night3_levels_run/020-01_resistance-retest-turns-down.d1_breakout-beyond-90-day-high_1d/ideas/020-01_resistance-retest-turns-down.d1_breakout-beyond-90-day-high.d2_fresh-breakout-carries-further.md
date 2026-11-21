---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 20 days, and the more so the fewer days have passed since that close first broke the 90-day high.
Consequence: A trader should weight a breakout long most heavily in its first days and reduce it as the breakout ages without a new high.
Why:
- F5: The book's gain per bar fades as the last new 90-day high grows older, and the book is still in the coin then. Mean gain per in-position bar is 0.17 % on the day of a new high, 0.26 % one to two days after, 0.11 % three to five days after, 0.04 % six to ten days after, and about 0 beyond ten days. The book still has 618 position bars more than ten days after a new high.
- F2: The breakout's move keeps growing well past the 5-day horizon that was tested. The mean total move after a breakout case is +1.4 % over 5 days, +3.2 % over 10, +4.8 % over 20 and +6.9 % over 40 (175, 172, 162 and 124 cases). The unusual move is +0.8 %, +2.0 %, +2.4 % and +2.5 % (t 0.81, 1.32, 1.14, 0.64).
- F4: The size of the breakout grades the longer move but not the 5-day one. By forecast quartile, the 20-day unusual move is -1.4 %, +0.5 %, +2.7 % and +8.1 %, and the 10-day one rises to +5.6 % in the top quartile. The 5-day move peaks in the third quartile (+5.4 %) and falls back to +0.7 % in the top one, which is why the 5-day slope has t 0.37.
- F6: The book's falls, the Calmar of 0.64, come in windows where the coin itself did well. ETH w17 fell 26 % while the coin rose 55 %, and BTC w15 fell 17 % while the coin rose 80 %. This points to breakouts that failed inside rising markets rather than to the market's own declines.
