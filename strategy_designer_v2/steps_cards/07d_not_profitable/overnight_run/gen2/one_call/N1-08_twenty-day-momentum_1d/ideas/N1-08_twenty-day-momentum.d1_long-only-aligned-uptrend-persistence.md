---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.d not profitable
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin's daily bars, when the coin's 60-day return is positive and its 20-day return is also positive, the following 20 days rise more than the coin's average 20-day return.
Consequence: A trader takes the long side only when both the medium and the slow trend point up, and stays flat instead of shorting after falls.
Why:
- F1: Only the long side pays: 4,507 long trades made +4.71% mean before fees (+21,229% summed), while 4,864 short trades lost −0.66% mean (−3,191% summed), and on non-overlapping 20-bar cases the short signal's signed forward return was −2.3% (t −2.20, n 427) against +2.7% for the long signal (t 1.67, n 400).
- F5: Almost all the book's daily gain comes from being long while the 60-day return is positive: +53.3 bp per day (t 4.02, n 3,040 days), against +9.2 bp for long in a 60-day decline, +7.1 bp for short in a 60-day rise and +0.2 bp for short in a 60-day decline (all t < 0.8).
- F6: The slower trend selects better: on non-overlapping 20-bar cases a long signal in a 60-day rise is followed by +3.6% excess (t 1.63, n 141), and a long signal above the 100-day average by +3.2% (t 1.57, n 152); a long signal in a 60-day decline gets −3.7% (t −1.49, n 62).
- F7: The book lags holding the coin because it is short or flat in rising markets: in up windows it made +43.8% against +79.3% for holding (long share 0.64, n 68), and in down windows it lost −15.7% against −30.0% (n 76).
