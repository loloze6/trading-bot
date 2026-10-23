# D-176 fixtures

## master-recorded byte-identity fixtures

`master_recorded_run_099.csv` and `master_recorded_run_084.csv` are the `bars.csv` files
produced by **master's code (no D-176)**, sha `4b1b1c60d6ca8b0acb5e4b990a8f6ba0d156cb1b`
(merge of PR #521), for the two real configs below, with no `strategies.sizing` block:

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
contain real activity (run_099: 10 executed rebalances; run_084: 40; guarded by replay_harness.assert_traded at generation and in the test; sidecars: master_recorded_run_*.meta.yaml).

Compared by the test: the whole file, header and every row string, after normalising
`\r\n` -> `\n` (the recording was made on Windows). No column is excluded: bars.csv carries
no wall-clock or run-id field (the run dir name, which holds the hash, is not in the file).

The test (`trading-bot/tests/test_d176_master_replay.py`) replays the same series through the
branch's code with the same harness and never touches a master checkout.

