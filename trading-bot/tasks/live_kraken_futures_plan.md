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

## 3. Operator's rulings (2026-11-17, first review)
- Kraken only; Binance is dropped (its live code is removed in step 2).
- The backtest on Kraken Futures candles is another session's work; not touched here.
- No holdout in live: the live path reads any candle it needs.
- Remaining risks (timing, spot/perp, funding, risk management) accepted for now.
- 1: first run with orders off. 6: on stop, close the positions (today's behaviour, kept). 8: the local book starts at
  the real account's value.
- 2: candles from Kraken Futures. Instrument `PF_XBTUSD`: Kraken's BTC perpetual, linear (quoted and settled in USD,
  1 contract = 1 BTC, step 0.0001 BTC). `PI_XBTUSD` is the inverse one (margined and settled in BTC), which the book's
  USD arithmetic does not fit.
- 3: fetch finer and aggregate. Measured: over the last 30 days, Kraken Futures' daily candle equals the 24 hourly
  candles aggregated, on every field (0 differences). So 1h is fetched and aggregated to 1d. The day closes as soon
  as its 23:00 hour is complete (not when the next row arrives), so the decision comes about one poll (60 s) after
  midnight UTC.
- 5: the strategy is `night_013_run / 013-01 ... b1_nearness-to-high-more-coins_1d` (step 5 confirmed, step 6
  profitable; Sharpe 1.246, Calmar 1.675 in step 6's record). Long-only, daily, vol-target sizing (60 days, cap 2).
  required_bars 456, so the warm-up is 2 x 456 = 912 days (Kraken Futures daily history starts 2022-03).
  Run on BTC (`PF_XBTUSD`): the engine trades one coin.

## 4. Plan (small steps; each ends with its proof)

| # | Step | Files | Effort | Risk | Proof |
|---|---|---|---|---|---|
| 0 | Baseline: run fixed backtests on the start commit and keep their files | a compare script | S | low | the baseline itself |
| 1 | Kraken Futures connection (ccxt, truststore, target switch real / demo URL, keys from environment variables) and a read-only `main.py live_check` | new `trading-bot/live/` | S | low | unit tests on recorded replies; live_check prints the last complete candles and the account value |
| 2 | Live candle feed: poll every 60 s, completed 1h candles only, fed through `add_row`, the day closed when its last hour is in; warm-up replays 912 days through the same callback with the backtest's warm-up cutoff. Binance live code removed | `live/`, `data/data_manager.py` (live branch), `execution/`, `core/launcher.py`, `requirements.txt` | M | medium | recorded candles through the feed and through a backtest give identical bars and forecasts; backtest rerun = step 0 files |
| 3 | First live run, orders off: real account value read, local book (the backtest's own classes) started at that value, one row per bar written as it happens, candles recorded | `live/`, `core/launcher.py` | M | low | after N bars, a backtest over the recorded candles gives the same book |
| 4 | Real book: account read from Kraken, orders to `PF_XBTUSD` (market; close = reduce-only of the real position), fills read back, next to the local book | `live/` | M | high | fake-exchange tests; one orders-off day showing the would-be orders |
| 5 | First real orders on a small real account | none | S | money | daily real vs local comparison |

Not touched: `strategies/strategy_components.py`, `strategies/strategy_engine.py`, the configs, the research workflow,
the backtest's Kraken Futures work.

## 5. Open: live book and backtest book
Option A (recommended): both books inside the live process, one candle feed, two bots, each with its own strategy
from the same config; the local book uses the backtest's own classes. Comparison at every bar; independent of the
other session. Option B: live records its candles and the backtest engine reruns on them automatically. It is the
literal backtest, but it needs the Kraken Futures backtest (other session), and the backtest's seal guard refuses a
912-day warm-up reaching into the sealed period. B kept as a later check, fed by the candles step 3 records.

## 6. API key (operator)
1. Kraken Pro, Settings, Connections & API, Futures tab: create a key. General API: Read only (enough for steps 1
   to 4); Withdrawal API: No access. A Full access key replaces it only at step 5.
2. Copy the public and private keys (shown once).
3. Windows: Start, type "environment variables", open "Edit environment variables for your account"; under User
   variables, New: `KRAKEN_FUTURES_API_KEY` = public key; New: `KRAKEN_FUTURES_API_SECRET` = private key; OK. Not in a
   PowerShell line (its history file keeps it in clear text), not in any file of the repository.
4. Restart the terminal and Claude Code so they see the variables. The check prints "key found: yes/no" and the
   account value, never the key.
