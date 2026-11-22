---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the closer its close sits to the bottom of that 30-day range, the more it falls over the next 5 days.
Consequence: A flat coin pinned near its 30-day low is a short to size up, and one just below the middle is a short to take small or refuse.
Why:
- F5: Closes deep in the bottom of the 30-day range continue down more than closes nearer the middle. The lowest quartile of range position (0.02–0.20) is followed by -2.52 % against drift (n=143), against -0.80 % to -1.19 % for the other quartiles.
- F2: The book loses on the trades themselves, not mainly on fees. All 2907 trades are shorts, averaging -1.54 % gross and -1.64 % net. Trades entered at a forecast below -10 lose the most: -1.84 % gross, n=1570. Bars held at a forecast below -10 (mean position -0.81) lose 0.23 % a bar, while bars held at -10..-5 gain 0.11 %.
