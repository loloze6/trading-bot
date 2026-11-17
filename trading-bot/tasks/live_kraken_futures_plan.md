# Live trading on Kraken Futures perpetuals: picture, findings, plan

Status: waiting for the operator's go. Nothing built yet. Branch `live-kraken-futures` (from `ccr-6624e33e-aakrpv`,
which a loop is writing to; this branch is a separate worktree and never pushes there).

## 1. The current state, measured (2026-11-17)

### What runs live today
`python main.py run_bot` -> `Launcher.run_bot` wires a Binance-only live bot. It has never been run (its own comment:
"the forbidden live-trading entry point, never exercised in CI"). I did not run it either: it would talk to Binance.

| Piece | Backtest | Live today | Shared? |
|---|---|---|---|
| Per-bar decision (strategy update, forecast -> allocation, min-change band, gap rule, rebalance) | `TradingBot._process_symbol_candle_completion` | the same method | yes |
| Order logic (close then open, add, reduce) | `BaseExecutionHandler` | the same | yes |
| Bar building | `CandleBuilder._ingest` fed by `add_row` (fetched candles) | `_ingest` fed by `add_tick` (Binance price sampled every N s) | half |
| Fill | `MockExecutionHandler`: bar close +/- slippage | `ExecutionHandler`: Binance margin market orders | no |
| Portfolio value | `MockPortfolioInfo`: local book | `PortfolioInfo`: Binance spot account | no |
| Warm-up | `warmup_prefetch`: 2 x required_bars, fed without trading | none (TODO in `run_bot`) | no |
| Records | run folder (bars.csv, trades.json, metrics.json, manifest) | none | no |

### Defects in the live path (found by reading the code, not by running it)
1. Binance only; no Kraken code for live (ccxt is used only to fetch history).
2. Bars are built from price samples: high/low come from samples, volume is 0. Not the candles the backtest reads.
3. Sample times use the PC's local clock (`datetime.now()`), bars are aligned on UTC: bars shifted by 1 h in France.
4. No warm-up: 120 bars without a decision for the default config (5 days at 1h, 4 months at 1d).
5. `ExecutionHandler(performance_tracker)` passes the tracker into `test_mode`; the tracker stays empty.
6. No state tracker: every bar raises after the orders are sent (caught and logged); nothing is recorded.
7. Balance read from the Binance spot account, orders sent on the margin account: the allocation is computed on
   the wrong account.
8. Closing uses a remembered quantity that an "add" overwrites: a close sells only the last addition; lost on restart.
9. `stop()` (Ctrl+C) closes every position.
10. The gap rule is on in every backtest, off in live.

### The environment
- Kraken spot public API: reachable. 1m candles: the last 720 (12 h); the last one is the minute still forming.
- Kraken Futures real API: reachable (`PF_XBTUSD`, the BTC perpetual).
- **Kraken Futures demo: gone.** Kraken decommissioned demo-futures.kraken.com on 14 July 2026; the host now
  redirects (HTTP 301) to a Kraken marketing page (measured with curl). Kraken offers a test environment only to
  "qualified clients" after onboarding with its API team.
- Python on this PC fails certificate checks with its default file; it works with the Windows certificate store
  (`truststore`, already in the venv). Live code must use it.
- ccxt 4.5.68 (installed) supports Kraken Futures: balance, positions, market and reduce-only orders, candles. Its
  "sandbox" switch points to the retired demo host.
- What the backtests use (step 4 card, `venue_resolver`): Kraken **spot** candles (`BTCUSD`), costed as the perpetual
  (fee 5 bps, slippage 2.5 bps on BTC), warm-up of 2 x required_bars, gap rule on.
- The sealed holdout ended 139 days ago. A daily warm-up of 2 x 120 bars = 240 days would reach into it.
- `ccr-6624e33e-aakrpv` vs `master` in `trading-bot/`: only strategy components and their tests differ; the live-path
  files are identical.

## 2. Findings and risks
- The core is already shared: one decision method serves both paths. The work is around it: candles in, account in,
  orders out, records.
- The demo cannot be the first live target. The safe first step is a run with orders off (real data, parallel book
  only).
- Real account math fits the existing book without touching `TradingBot`: a perpetual position of q BTC on an
  account worth E reads as `{cash: E - q x price, BTCUSD: q}`; the existing formulas then give value E and
  allocation q x price / E.
- The parallel book cannot share one strategy object with the real book (each bar would update it twice). Two bot
  instances, one candle feed, each with its own strategy built from the same config: same bars in, same forecast out.
- Leverage: the backtest allows an allocation up to +/-2 (forecast +/-20 / 10). Live inherits it. No limit is added.
- Not handled yet (operator's later list): funding, spot-vs-perp price gap (decisions use spot candles, orders go to
  the perpetual), risk management.
- Risks: real money (sign or size error), order timing (sent seconds after the bar close, the backtest fills at the
  close), Kraken's 720-candle limit for longer warm-ups, a restart loses the parallel book (first version).

## 3. Plan (small steps; each ends with its proof)

| # | Step | Files | Effort | Risk | Proof |
|---|---|---|---|---|---|
| 0 | Baseline: run fixed backtests on this branch's start commit and keep their files (regression fixture + one step-4 Kraken daily run) | none (a compare script) | S | low | the baseline itself |
| 1 | Kraken connection: spot candles, futures account/positions/orders, target switch, keys from environment variables, truststore. Read-only command `main.py live_check` | new `trading-bot/live/` | S | low | unit tests on recorded replies; live_check prints the last complete bars (and the account, once keys exist) |
| 2 | Live candle feed: poll every 60 s, keep completed candles only, feed them through `add_row` (the backtest's own path), close a bar when its last candle is in; warm-up replays history through the same callback with the backtest's warm-up cutoff. Replaces the Binance sampler in `DataManager`'s live branch | `live/`, `data/data_manager.py` (live branch only) | M | medium | replay test: recorded candles through the feed and through a backtest give identical bars and forecasts; backtest rerun = step 0 files |
| 3 | **First live run, orders off**: real data, strategy, parallel book only (mock fills, as in a backtest), one row per bar written as it happens | `live/`, `core/launcher.py` (new command) | M | low (no money) | after N bars, a backtest over the same recorded candles gives the same portfolio files |
| 4 | Real account: portfolio read from Kraken (shape above), orders to the perpetual (market; close = reduce-only of the real position), fills read back; real book and parallel book side by side; orders-off mode logs the orders it would send | `live/` | M | high | tests against a fake exchange (signs, sizes, rounding, failures); one orders-off day showing the would-be orders |
| 5 | First run with real orders: demo if Kraken grants access (same switch), else a small real account sized by the operator; real vs parallel compared each day | none | S | high (money) | the daily comparison |
| 6 | Clean-up list for the operator's go: remove Binance live code (`ExecutionHandler`, `PortfolioInfo`, `OtherPortfolioOperations`, two CLI commands, the price sampler, `python-binance`) | several | S | low | backtest rerun = step 0 files |

Not touched: `strategies/strategy_components.py`, `strategies/strategy_engine.py`, the strategy configs, the research
workflow.

## 4. Decisions for the operator
1. Demo retired: first runs with orders off (step 3), then real orders on a small real account? Or apply to Kraken
   for test access first?
2. Decisions on Kraken spot candles (what the backtest reads), orders on `PF_XBTUSD`?
3. Granularity: fetch the completed bar at the bar's own interval (exactly the backtest's candle) by default, 1m as a
   setting? (1m-built bars can differ when minutes are missing; at bar close they add nothing to the decision.)
4. Warm-up and the seal: never read sealed-period candles; start on 1h bars (10-day warm-up); a daily strategy starts
   only once enough post-seal history exists, else the bot refuses and says how many days are missing?
5. Strategy and timeframe of the first run (config file, coin, bar)?
6. On stop: keep positions (restart reads them back), instead of today's close-all?
7. Keys: no credential form exists in a local session. The operator sets two Windows user environment variables
   (names given at step 4); the key has trade permission, no withdrawal; Claude never sees it?
8. Parallel book starting value: the real account's value at start, or 1000 as in backtests?
