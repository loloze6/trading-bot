What "unseen coins" are, for the test of an idea on coins its plan never tested (operator, 2026-11-25;
`runs/UNSEEN_COINS_RUN.md`). Read by `orchestration/unseen_test/` (its code, with `--coins`) and the operator.

A file of its own, not a section of `unseen_dates.md`: it is another notion (other coins on the same dates, not other
dates), and one notion is defined in one place. The "holds" rule is not repeated here: it is `unseen_dates.md`'s.

**The unseen coins of a plan are the coins with data in its folds that the plan did not test.**
- **The coins with data:** the Kraken coins of the data (`common/data_available.md`, 19 coins today), read from the
  data tool's record `trading-bot/local_data/coverage.yaml` (its `kraken_<COIN>USD_*` files: names only, no price).
- **Did not test:** not in the plan's `data-instruments` (a coin the plan names but the data does not have, e.g. BNB,
  is not a coin of the data and changes nothing).
- **In its folds:** the plan's own folds (its `data-period`), unchanged. Step 4 runs each unseen coin only in the
  windows where it has data (as it does in-sample); a coin with no window there is not counted.
- **A plan that tested every coin of the data has no unseen coin:** its result says so ("none"), it is not a failure.

**Holds** on the unseen coins: the rule of `unseen_dates.md`, unchanged: the main measure (the idea's own
`measure.py`, applied as it is) has the sign it had in-sample AND the book's Sharpe after costs (step 6, on the unseen
coins only, equal weight per coin as in-sample) is above 0. Next to it, holding's Sharpe on the same coins and dates.

**Why this cannot leak**
- **No lookahead:** the plan, its config, the engine and its folds are unchanged; only the coins change. Each bar's
  decision uses data at or before its close, as in-sample (step 4 adds no data source and reads data as before).
- **Not seen by the plan:** no step designed, planned, judged or analysed this plan on these coins' prices: its records
  in-sample hold only its own coins. The unseen coins' files go under the run's `unseen_coins/` folders, which no step
  reads (as the unseen periods'): step 7 and `select_next` read the folds' results of the plan's own coins only. The
  result records; it chooses nothing, so the coins stay unseen.

**What it can and cannot show** (say it in every reading)
- **It tests the coins, not the dates.** The folds' years were seen, on the plan's coins. Coins move together (a market
  that rose for BTC rose for most coins), so an idea that only rode its folds' market can still hold on other coins
  over the same years. Unseen coins catch a fit to a few coins (XMR's or ZEC's own history); unseen dates catch a fit
  to the years. Neither replaces the other, nor the sealed holdout.
- **The other coins are younger and fewer per window.** Most have data in folds A and D only (`data_available.md`), so
  a book on them covers fewer years, mostly 2018 and 2024-25; the reading gives the coins and years each book ran on.
- **The idea's relatives may have seen them.** The definition is per plan: an idea whose sibling ran "on more coins"
  had those coins' results in its run (step 7 read them). The reading names such cases when it finds them.
- **Every idea meets the same coins:** choosing ideas by their unseen-coins result would make those coins seen.
