---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next day, while its close is still above that high.
Consequence: A trader should carry a breakout long only while the close stays beyond the old 90-day high, larger the further beyond, and stand aside once price falls back under it.
Why:
- F1: The book's gain comes from the few days the close stands above its prior 90-day high: on those days the next day's drift-adjusted return is +0.69 % (730 bars, t 2.80), but they are only 5.2 % of bars, while the 20-day minimum holding keeps the book in for 24.7 % of bars, and the 3,601 held days after the forecast fell back to 0 earn only +0.09 % (t 0.92).
- F3: The breakout state is short-lived: of 903 positive-forecast bars, 809 are within 3 days of the forecast turning positive, 94 are 4 to 10 days in, and none are later, so a 20-day hold is mostly spent after the situation has ended.
- F5: In position, the size of the next day's drift-adjusted gain grows with the distance above the 90-day high: -0.10 % at 5 to 10 % below it (601 bars), +0.04 % at 0 to 5 % below (857), +0.39 % at 0 to 5 % above (382, t 1.70), and +0.95 % at 5 to 15 % above (157, t 1.49); the same order holds on all bars (+0.11 %, +0.22 %, +0.86 %).
- F8: The book's gain is concentrated in one coin: ZEC's trades sum +3,803 % of the 6,308 % total, while LTC's 49 trades lose (-1.7 % mean), and trade profit does not grow with the entry forecast (mean +32 %, +13 %, +11 % from the low to the high tercile); the deepest chained fall is 16.2 %, which gives the failing Calmar of 0.50.
