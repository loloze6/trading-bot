How the workflow measures. The same definitions in every step that measures (steps 3, 5 and 7; step 6's code computes
the book the same way). A plan's own words come first; these apply wherever it says nothing.

- A coin's return over the next h bars from bar t is close[t+h] / close[t] - 1, inside the same window only. Never
  compute a return across two windows, and never join windows into one series.
- Returns over h bars are counted once: use non-overlapping samples (the bars at positions 0, h, 2h, ... of each window,
  counted from its first row; one grid per window, the same for every group compared), never every bar's overlapping
  forward return. Give the number of independent cases next to a t.
- Holding the coin, or the coin's average: the coin's mean return over all the windows together, never the mean of one
  window (a window's mean already holds the moves being measured).
- The position's gain before costs on bar t: the position held after bar t's trade x (close[t+1] / close[t] - 1).
- The book (what the strategy earns): its value after each rebalance and its fees, read at the last bar of each day;
  its daily returns stay inside a window; each day, the mean of the coins' daily returns. Holding the coins: the same
  from their closing prices. A claim about the book (what it earns, what carries its gain, its falls) is measured on
  these daily returns, never on summed trade returns.
- Sharpe: the mean of the daily returns over their standard deviation, times the square root of 365. Calmar: the yearly
  return of the daily returns chained in window order, over the deepest fall of that chain.
- A t-statistic not named: for a difference between two groups, Welch's two-sample t; for one group's mean, the
  ordinary t of the mean (mean / (standard deviation / square root of n)).
- A difference is "A minus B" in the order named, so its sign keeps its meaning. A mean "weighted by" X is
  sum(value x X) / sum(X).
- Rows with a missing value in a column a measure needs are left out of that measure.
