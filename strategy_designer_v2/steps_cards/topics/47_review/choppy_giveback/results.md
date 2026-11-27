# Choppy books: how much of the best gain is given back (2026-11-27)

Inputs: choppy_books.json (27 choppy confirmed, 41 reference profitable), all 1d, folds A-D.
Scripts: giveback.py (per trade, per book -> per_book.csv / per_book.json), table.py (group medians).
Trades: chart_trades.csv.gz of each record, 134,888 rows, 0 skipped. Bars: local_data daily highs/lows/closes, read only on the
dates in each record's chart_bars.csv.gz (the fold windows that ran).

Definitions
- MFE / MAE: as run_protocol._compute_mae_mfe, on the bars after the entry bar up to the exit bar, % of the fill price.
- give-back = MFE - gross return (gross from the fill prices, as the engine's realized_return); net = chart_trades realized_return.
- give-back/MFE = (mean MFE - mean gross) / mean MFE, per book; above 1 means the trades end below their entry on average.
- share gave >half: trades with MFE > 0 whose gross return < MFE / 2.
- share >=2x mean then below mean: trades whose MFE >= 2 x the book's mean net return and whose net return < that mean;
  only defined when the book's mean net return is > 0 (bks = books where defined).
- hold N: exit at the close N bars after the entry bar (window's last bar if sooner), same costs as the trade paid
  (net_N = close-to-close_N - (close-to-close at the plan exit - net)). Same entries, same lots, no re-entries.
- Each chart_trades row counts as one trade (the engine closes a position in lots); means are unweighted by size.

Check against the engine: 119,097 of the 134,888 trades are also in the records' trade_diagnostics.json.gz (the rest
are not kept there); all 119,097 match on MFE, MAE and gross return within 0.01 pts (worst 0.0017, the rounding of the
chart prices).

| group | books | trades | bars held | net % | gross % | MFE % | MAE % | give-back pts | give-back/MFE | share gave >half | share >=2x mean then below mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| choppy calm | 7 | 1420 | 7 | 1.51 | 1.61 | 9.97 | 7.06 | 8.36 | 0.84 | 0.70 | 0.27 (6 bks) |
| choppy agitated | 14 | 508 | 5 | -0.27 | -0.17 | 6.99 | 6.13 | 7.45 | 1.03 | 0.76 | 0.50 (2 bks) |
| choppy | 6 | 2344 | 8 | -2.04 | -1.94 | 9.22 | 10.56 | 11.28 | 1.21 | 0.78 | nan (0 bks) |
| all choppy | 27 | 1185 | 5 | -0.27 | -0.17 | 7.59 | 6.52 | 7.72 | 1.03 | 0.77 | 0.35 (8 bks) |
| reference profitable | 41 | 1734 | 1 | 0.61 | 0.71 | 4.71 | 5.66 | 4.31 | 0.87 | 0.67 | 0.26 (31 bks) |

Net % per trade, exit at the plan's exit vs after N bars (median across books; books where N bars beats the plan)
| group | plan | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| choppy calm | 1.51 | 0.01 (1/7) | 0.13 (1/7) | 0.22 (1/7) | 0.87 (1/7) | 0.88 (0/7) |
| choppy agitated | -0.27 | -0.02 (10/14) | -0.11 (6/14) | -0.13 (8/14) | 0.04 (13/14) | -0.28 (6/14) |
| choppy | -2.04 | -0.91 (6/6) | -1.31 (5/6) | -1.62 (5/6) | -1.51 (6/6) | -1.71 (6/6) |
| all choppy | -0.27 | -0.12 (17/27) | -0.40 (12/27) | -0.31 (14/27) | -0.09 (20/27) | -0.28 (12/27) |
| reference profitable | 0.61 | 0.18 (5/41) | 0.05 (2/41) | 0.10 (4/41) | 0.52 (16/41) | 1.26 (22/41) |

Books with mean net per trade > 0 at the plan's exit: {'choppy calm': '6/7', 'choppy agitated': '2/14', 'choppy': '0/6', 'all choppy': '8/27', 'reference profitable': '31/41'}
Engine check (trade_diagnostics): trades matched 119097 of 134888 ; equal within 0.01 pts: 119097 ; worst diff 0.0017256743901725713

Holding-length check (reference books holding a median of >=3 bars, vs choppy):
  reference, median hold >=3 bars: books 11, median bars 5.0, MFE 15.50, give-back 11.34, give-back/MFE 0.72, gave >half 0.73, books with give-back/MFE >1: 0
  reference, median hold <3 bars: books 30, median bars 1.0, MFE 4.37, give-back 4.12, give-back/MFE 0.92, gave >half 0.66, books with give-back/MFE >1: 8
  all choppy: books 27, median bars 5.0, MFE 7.59, give-back 7.72, give-back/MFE 1.03, gave >half 0.77, books with give-back/MFE >1: 16
