---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 60-day return is positive, the larger its 20-day return is relative to that coin's own usual 20-day returns over the past few weeks, the more its return over the next 1 to 3 days exceeds its average return over the same span.
Consequence: A trader should size a long in an uptrending coin by how unusually strong its recent 20-day run is, and give weakly trending coins little or no weight, since the continuation shows up mainly in the strongest stretches.
Why:
- F1: The book's gain sits almost entirely on the days after the strongest trends. Days whose previous-day mean forecast is in the top third of active days earn a mean daily book return of 0.00540 (t 5.54, n 2254) and carry 105.5 % of the book's summed daily return. The low third earns -0.00038 (t -1.50) and the middle third 0.00014 (t 0.32), and flat days carry -0.9 %.
- F2: The coin's next 3-day excess return is graded by trend strength only at the top. At top-third forecast grid bars it is +0.0130 (t 3.03, 620 non-overlapping cases), against +0.0002 (t 0.06) in the low third and -0.0021 (t -0.58) in the middle third. The plan's pooled measure (+0.0037, t 1.66, 1858 cases) averages the top third with the two flat thirds.
- F3: The top-third effect is carried as much by the fast 20-day return as by the slow 60-day one. The top third of the standardised 20-day return gives a 3-day excess of +0.0125 (t 2.78, 620 cases) and a 1-day excess of +0.0044 (t 3.23, 1883 cases). The top third of the standardised 60-day return gives +0.0101 (t 2.31) and +0.0034 (t 2.57).
- F5: The book earns mostly from timing, not from the market's own rise. The market part averages about 0.00024 a day against a mean book return of 0.00066. BTC's timing part is 0.00102 (book t 3.91) and ETH's is 0.00083 (book t 3.40), while LTC (-0.00004) and XMR (-0.00031) earn nothing.
