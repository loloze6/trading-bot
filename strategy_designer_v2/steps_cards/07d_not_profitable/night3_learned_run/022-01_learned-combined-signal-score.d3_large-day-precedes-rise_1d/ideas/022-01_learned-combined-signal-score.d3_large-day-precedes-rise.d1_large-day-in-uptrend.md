---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's absolute return over its last day, the higher its return over the next 5 days, only while the coin's 60-day return is positive, and the more so the larger that 60-day return.
Consequence: Lean long after a day of unusually large movement only when the coin has risen over the past 60 days, and stay out of such bets in a 60-day decline, where the book's deepest fall happened.
Why:
- F1: The book fails on its falls. Its deepest fall is 31.9 % against a yearly return of 16.2 %, a Calmar of 0.51. That fall lasted 276 days across windows w12 to w14, while holding the coins fell 81.2 % over the same days. The book's gain is real but small next to that fall: Sharpe 0.69, holding's Sharpe 0.55.
- F4: The deepest fall was carried by positions opened on down days. In w12 to w14, positions last raised after a down day lost a summed 0.95 of daily gain while the 20-day trend was falling (781 bars) and 0.15 while it was rising (229 bars). Positions opened on up days gained a net +0.42 over the same windows. In w14 alone, down-day positions lost 1.02 against 0.14 for up-day positions.
- F5: Over all windows, the book's gain sits where the coin's 60-day return is positive. Up-day positions there earned 4.49 (2489 bars, 0.18 bps... mean 0.0018 per bar). Down-day positions in a falling 60-day trend lost 0.77 (2476 bars), and up-day positions in one lost 0.20 (1880 bars). Down-day positions hold 51 % of the book's bars.
