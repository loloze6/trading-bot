# D-176 fixtures

## master-recorded byte-identity fixtures

`master_recorded_run_099.csv` and `master_recorded_run_084.csv` are the `bars.csv` files
produced by **master's code (no D-176)**, sha `4b1b1c60d6ca8b0acb5e4b990a8f6ba0d156cb1b`
(merge of PR #521), **with the Parked A/B engine warm-up fix applied on top** (the
`regime_engine.py` and `strategy_engine.py` changes of commit `550f447`, nothing else), for the two
real configs below, with no `strategies.sizing` block:

| fixture | config |
|---|---|
| `master_recorded_run_099.csv` | `run_099_strategy_config.json` (this directory) |
| `master_recorded_run_084.csv` | `../d142/run_084_BTCUSD_2018-05/strategy_config.json` |

Input series: `synthetic_daily_ohlcv.csv`, 700 daily bars from 2019-01-01, a seeded geometric
random walk (numpy `default_rng`, **seed 176**, drift 0.0004, daily vol 0.03), made by
`python -I replay_harness.py --make-series synthetic_daily_ohlcv.csv`. No market data.

Entry point: the real `core.launcher.run_backtest` (strategy, buffer, forecast manager, risk
manager, mock execution, tracker, `write_bars_csv`); only `DataManager.fetch_historical_data`
is replaced by a read of the CSV. Command (master worktree checked out detached at the sha
above, run from a neutral cwd):

    python -I replay_harness.py <master>/trading-bot <config.json> synthetic_daily_ohlcv.csv <out>.csv

Recording is deterministic (two recordings of run_099 were byte-identical). Both recordings
contain real activity (run_099: 13 executed rebalances; run_084: 40; guarded by replay_harness.assert_traded at generation and in the test; sidecars: master_recorded_run_*.meta.yaml).

Compared by the test: the whole file, header and every row string, after normalising
`\r\n` -> `\n` (the recording was made on Windows). No column is excluded: bars.csv carries
no wall-clock or run-id field (the run dir name, which holds the hash, is not in the file).

The test (`trading-bot/tests/test_d176_master_replay.py`) replays the same series through the
branch's code with the same harness and never touches a master checkout.


## Re-recorded after the Parked B warm-up fix (operator ruling 2026-11-16)

The first recordings were made on master `4b1b1c6` alone. Parked B changed when a strategy becomes
ready (at its declared `required_bars` rows, no longer component warm-up + `required_bars`), and
this harness feeds the strategy from the first bar with no warm-up prefetch, so both replays start
trading earlier. The operator accepted that change and ruled to re-record. The fixtures are now
master `4b1b1c6` + the engine fix only, which keeps this test what it was: D-176 versus master's
code, everything else equal. Master alone still reproduces the first recordings byte for byte.

What changed, per replay (row indices 0-based, 700 rows each):

| | run_099 | run_084 |
|---|---|---|
| bars not ready (`NOT_READY`) | 499 -> 311 | 198 -> 100 |
| first executed rebalance, row | 573 -> 311 | 198 -> 139 |
| executed rebalances | 10 -> 13 | 40 -> 40 |
| final portfolio value (start 1000) | 1293.09 -> 1272.22 | 1405.01 -> 1812.00 |

- Forecasts are identical on every bar where the old code was already ready; only the newly
  ready bars are new (run_099: 188 bars, 140 with a nonzero forecast; run_084: 98 bars, 59).
- Different positions over those bars carry through to every later portfolio column.
- `balances.USDT.free` and `postRebalance_balances.USDT.free` differ on every row, the not-ready
  rows included: those columns hold the end-of-run balance on every row (known defect A1 in the
  data dictionary), so they move with the final value.
- The new files have `\n` line endings (recorded on Linux); the test normalises `\r\n`.
