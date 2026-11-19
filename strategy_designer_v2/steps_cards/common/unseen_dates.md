What "unseen dates" are, for the test of an idea on dates the research never used (operator, 2026-11-18;
`runs/UNSEEN_RUN.md`). Read by `orchestration/unseen_test/` (its code) and the operator.

**Unseen dates are dates no fold covers.** Steps 1 to 7 see only the folds' windows (A to D, 2018 to 2025,
`trading-bot/config/folds.yaml`): no step designs, plans, judges or analyses an idea on any other date. So a date
outside every fold is unseen by every idea, whatever its run or generation.

**The unseen periods**: one windows file each, in `04_backtest/windows/unseen_*.json` (4-month windows like the
folds'; the code reads every file there):

| Period | Windows | Coins with data | What it is |
|---|---|---|---|
| `unseen_2016_2017` | 6 (2016-01 to 2017-09) | BTC, ETH, LTC; XMR, XRP, ZEC from 2017 | a bull market (BTC x32); earlier years too thin to use |
| `unseen_2026` | 3 (2026-01 to the last finished day added, 2026-11-17) | the 19 Kraken coins | a falling market for most coins |

- **A later period** is a new file: add the days with `trading-bot/tools/extend_kraken_daily.py`, then write the
  windows (the last one may end before its 4 months).
- **What an unseen test can and cannot show:** a period is short next to the folds (2026: 11 months, against 8
  years), so a real idea often stays below its plan's t ≥ 2 there; and every idea is tested on the same few periods,
  so choosing ideas by their unseen results would make those dates seen. The test says whether an idea still holds;
  it is not a new search.
- **Holds** (fixed before the first unseen run): on a period, the main measure has the sign it had in-sample AND the
  book's Sharpe after costs is above 0. Next to it, holding's Sharpe on the same coins and dates (step 6's).
