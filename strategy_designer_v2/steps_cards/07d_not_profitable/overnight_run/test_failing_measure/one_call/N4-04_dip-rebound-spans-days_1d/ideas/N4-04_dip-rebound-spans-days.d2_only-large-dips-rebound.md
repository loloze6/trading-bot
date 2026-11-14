---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In an uptrending coin, a rise over the next three days follows only a one-day drop that is large against the coin's last 60 daily moves, about one standard deviation or more. Milder down days are followed by the coin's ordinary drift.
Consequence: A trader should refuse long entries on ordinary down days, removing half the exposure to crashes that has no rebound to pay for it.
Why:
- F3: The rebound exists only after large standardised drops. Over non-overlapping long-forecast events, the 3-bar excess return against the coin's all-window mean is +1.94% (t=3.58, n=288) when the drop's z is below -1.06, and +1.05% (t=1.64, n=288) for z between -1.06 and -0.64. It is -0.12% (t=-0.27, n=288) and -0.17% (t=-0.38, n=288) for the two milder quartiles. Half the events the book takes carry no edge but still carry crash risk: 6-8% of events in every quartile fall more than 10% in 3 bars.
- F1: The book fails on its falls, not its gain: the book's daily returns (each day, the mean over coins of `book_return`) earn about 21% a year, but the deepest fall chained across windows is -35.6%, and single windows fall far: w17 -21.7%, w13 -19.5%, w11 -17.7%, w19 -15.9%. In those windows nearly the whole fall sits in one to four book days below -2% (w17: one day carried -0.209 of a 3-day, -21.7% fall; w13: two days carried -0.205; w19: two days carried -0.163).
