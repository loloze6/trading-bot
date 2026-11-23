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
- The book's gain from the market's own rise: the position held x the coin's mean daily return over all the windows,
  averaged like the book; the rest of the book's mean gain is timing (being in when the coin rises more than usual).
- Sharpe: the mean of the daily returns over their standard deviation, times the square root of 365. Calmar: the yearly
  return of the daily returns chained in window order, over the deepest fall of that chain.
- A book's **mean daily return on days in a position** (operator, 2026-11-22; step 6): the mean of its daily returns divided by
  the share of (coin, day) pairs in which the coin held a position (held into one of the day's bars, or traded on it).
  A day out of the market earns 0, so this is the mean over the days in a position. Calmar stays on calendar days.
- **An informative measure** (operator, 2026-11-22): a measure a step computes and shows, that enters no rule and decides
  nothing; it is there to be read. A step's card lists its informative measures apart from the measures its rule uses.
- The book's daily standard deviation: the standard deviation (ddof 1) of its daily returns, the one inside the
  Sharpe: how much the book's value typically moves in a day. The yearly return: the daily returns chained in window
  order (Calmar's chain), compounded to one year: (value at the end / value at the start) ^ (365 / days) - 1; with the
  number of years it covers, the total over the period follows (operator, 2026-11-22: per year, so books tested over
  different lengths compare).
- A t-statistic not named: for a difference between two groups, Welch's two-sample t; for one group's mean, the
  ordinary t of the mean (mean / (standard deviation / square root of n)).
- A difference is "A minus B" in the order named, so its sign keeps its meaning. A mean "weighted by" X is
  sum(value x X) / sum(X).
- Rows with a missing value in a column a measure needs are left out of that measure.
- **The size of an idea** (operator, 2026-11-20; `runs/RETRO_DIAGNOSIS_RUN.md`). Whether an idea is real (step 5) says
  that its effect exists, not how large it is. Its size says how large, with no cost in it:
  - a **case** is a signal of the idea: a rise of the forecast on its side of at least the band (the holding period's
    bet, `forecast.md` 7), read once per grid cell of the horizon, so no move is counted twice;
  - the **coin's usual move** over the horizon: the standard deviation of its returns over the horizon, on
    non-overlapping stretches of all its windows; its **normal drift**: their mean (holding the coin);
  - the **unusual move**: per case, the coin's return from the close of the signal's bar over the horizon, minus its
    normal drift, in the signal's direction; its mean over the cases;
  - the **total move**: the same without removing the drift (what a trade on the signal earns before costs);
  - the **strength**: the unusual move divided by the coin's usual move, per case, then averaged: a pure number (0.05
    means the idea predicts 5 % of a usual move).
  - **how sure** the unusual move is (operator, 2026-11-23; topic 47, N2): its t, the mean over its standard error, the
    cases of one day taken together (their deviations summed per day: cases on several coins the same day are one
    piece of evidence, not several); with the number of days the cases fall on. A t under 2 means the size cannot be
    told from 0 (night 5: 50 of the 81 real books had a positive size with a t under 2).
  Example: over 3 days a coin usually moves about 10 % up or down; an idea whose cases end 0.5 % higher than the coin's
  normal drift has a strength of 0.05. Real ideas measured so far have a strength of about 0.05 whatever their horizon
  (`runs/RETRO_DIAGNOSIS_RUN.md`, fourth question).
- **The cost of a trade** (operator, 2026-11-20): what the backtest applied to a buy and a sell, as its record states it
  (each window's `manifest.json`, `config.cost_model`: the fee per trade and the slippage per trade for the coin, or the
  table's default): twice the fee plus the slippage, as a share of the value traded. For a record of several coins, the
  mean over its coins. Its values come from `trading-bot/config/cost_model.json` (taker execution): the fee is Kraken
  futures' taker fee; the slippage was a guess until 2026-11-20, then measured once on the venue's order books (topic 38).
  They are estimates, not the bot's own fills.

- **A paying book, and what it shares with the books we have** (operator, 2026-11-21; topic 41; computed by
  `orchestration/ideas_similarities_check/`). The question: does a book that pays make its money on the same bars as a book we
  already have, or is its profit new?
  - A **paying book**: a backtest record whose idea step 5 confirmed and step 6 found profitable enough, in any run. An
    idea run again in another run counts once (its latest record). Paying books are compared only with each other.
  - A **confirmed book** (operator, 2026-11-22; topic 45): a record whose idea step 5 confirmed and step 6 found not
    profitable enough: a real idea that is not yet a profit. It is in the register too, compared with the paying books
    ("is this real effect one we already earn, or a variation?"), and a repair (`idea_created_from.md`) also with the
    idea it repairs (did it keep that idea?). A paying book is still compared with paying books only. A confirmed book's
    returns are rebuilt from its record when needed (its chart file if its bars are not on the machine), not committed.
  - A book's **bar returns**: its value after the last bar of each period against the one before, read from the
    record's value series (`postRebalance_total_value`), inside each window, all its coins together (each period, the
    mean of the coins' returns), as the book is built above for daily returns. Holding its coins: the same from their
    closing prices.
  - The **comparison timeframe** of two books: the larger of their two bar sizes (1h with 1h: the hour; 1h with 4h: 4
    hours; with 1d: the day). A bar belongs to the UTC period it opens in (hours; 4-hour blocks from 00:00; days from
    00:00), as the data files are cut.
  - The **window in common**: the periods of the comparison timeframe both books ran, inside the folds. Every output
    uses these periods only. Under one year in common, the pair is "not comparable".
  - The **share explained**: the share (0 to 1) of the new book's period returns that the other book's period returns
    account for (one-variable least squares: the square of their correlation), read three times: the other book's same
    period, the period before, the period after. The largest of the three is the share explained; the reading it comes
    from is **who leads** (the same period; the new book one period ahead: the other follows; one period behind). Its
    **direction** is the sign of the slope (+ moves with, − against: the same effect either way).
  - **What is left**: in that reading, the new book's mean return per period that the other book does not explain (the
    intercept), and its t.
  - The **nearest relative**: the paying book with the largest share explained (for a confirmed book too).
  - The **similarity matrix of the paying books** (operator, 2026-11-22; topic 44): for every pair of paying books, the
    share explained, its direction and who leads, as above (the share is the same read from either book). The books
    are ordered so that similar books sit together (from the first book, always next the book most explained by the
    last one placed): a block of high shares is a family. It is the map of what the research earns, and the input for
    combining books in one bot later (topic 44). The new book is also compared with
    holding its own coins, the same way.
  - Example: a 1h book and a 1d book compared on days; the 1h book's day returns match the 1d book's next day (share
    explained 0.8, the new book one period ahead, direction +, what is left 0.01 % a day with t 0.9): the same profit,
    caught a day earlier, adding nothing reliable.
  - Limit: a lead of more than one period of the comparison timeframe does not show (two 1h books 3 hours apart).
