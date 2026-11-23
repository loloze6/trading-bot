---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's daily high-low range is relative to its average range over the past 30 days, while its 20-day return is positive and its close is above its 100-day average close, the higher that coin's return over the next 10 days.
Consequence: A trader holds range-expansion buys for 10 days only while the price is above its 100-day average, which drops the cases below that average, where the signal earns nothing.
Why:
- F1: The check failed on Calmar (0.575 against 0.75). The rebuilt book's deepest fall is -48.3 % against a yearly return of +27.8 %, and its worst episode runs from w12 to w16 (456 days), while the coins held fell -51.2 %. The book stays long whenever the 20-day return is positive, so it also buys short rebounds inside long declines.
- F4: The 100-day average gives the same picture. Signal cases above it end +1.66 % above drift (t 1.87, 369 cases), and those below it end +0.07 % (t 0.05, 113 cases). Bars above it without the signal end -1.15 % (t -0.90, 108 cases), so the condition alone does not earn. The book's mean daily gain is 0.216 % on days with the price above its 50-day average, against 0.017 % below it.
- F5: Inside the regime the grading by range is weak and not monotone:
