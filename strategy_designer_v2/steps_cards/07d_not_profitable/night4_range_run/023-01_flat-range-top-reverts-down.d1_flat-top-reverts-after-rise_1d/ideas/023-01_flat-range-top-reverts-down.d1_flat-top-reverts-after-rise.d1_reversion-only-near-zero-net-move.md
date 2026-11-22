---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range, the further its close sits above the middle of that range, the more it falls over the next 5 days, only while its 90-day return is positive, and the more so the closer its 30-day net move is to zero, so that the fall shows only in the flattest months.
Consequence: A trader would sell the top of a range only in a month that went almost nowhere, and would refuse the short when the month's net move is a sizeable part of its range.
Why:
- F3: The flatness factor lets mostly trending months into the cases. Only 15.6 % of the cases fall in the flattest fifth of months, and that fifth is the only one where the short gains: +0.70 % (t 0.90, n 109). The other four fifths lose between -1.02 % and -1.50 % per case.
- F4: In the 90-day-rise regime, the shorts that lose most are closes above the middle in the most trending fifth of months: -1.68 % per case (t -1.93, n 238). Closes above the middle in the flattest fifth earn +0.54 % (t 0.64, n 90). At the very top of the flattest fifth the coin fell 3.34 % against drift (t -2.84, n 38), against +1.68 % at the top of the most trending fifth.
- F7: Taken over all regimes, the flattest two fifths of months show no graded reversion. The far third from the middle reverted 0.00 % (t 0.01, n 341) and the slope of the unusual move on range position there was +0.0042 (t 0.75, n 1022). The reversion in F4 is therefore narrow, not a broad effect.
