# Function card: live mode on Kraken Futures (2026-11-18: steps 0-3 built and proven offline; validating run running)

Runs a strategy from the research live: Kraken Futures candles in, the backtest's own decision, the books recorded.
Code in `trading-bot/live/`; command `python main.py run_live` / `live_check`; validation in `live/validation/`.
Shaped after `strategy_designer_v2/steps_cards/HOW_WE_DESIGN_A_CARD.md`; sections that do not apply say why.

## Business objective, one question
Does a strategy run live on Kraken Futures make the decision the backtest makes on the same candles, and what
does that decision give on the real account next to the backtest's own book?

## Input
- A strategy config the step-4 backtest ran (e.g. `04_backtest/<run>/backtests/<idea>/config.json`), unchanged.
- A coin in the research's naming (`BTCUSD`); it trades the coin's Kraken linear perpetual (`PF_XBTUSD` for BTC:
  quoted and settled in USD, 1 contract = 1 coin; Kraken writes bitcoin XBT). The inverse `PI_` perpetuals are
  settled in the coin, which the book's USD arithmetic does not fit.
- Kraken Futures: completed candles (public) and, with a key, the account's value and position.

## Output
A live run: one folder, `trading-bot/live_runs/<name>/`, that a reader can audit bar by bar and replay.

## What a live run is
The strategy decided once per bar, on Kraken Futures candles whose whole period has passed, by the same code that
decides in a backtest (`TradingBot`), with two books side by side: the **local book**, simulated exactly as in a
backtest (the backtest's classes, Kraken perpetual costs from `config/cost_model.json`), and the **real book**, the
Kraken account (read only until step 4; real orders from step 5). A run lasts from a start to a stop; each start is
a session.

## Mechanism
1. Start: the run folder is created (first start) or read back (restart; refused if the strategy or coin differ).
2. Warm-up: the last 2 x `required_bars` bars of history are fetched at once (the backtest's warm-up length) and fed
   through the same per-bar callback without trading (the backtest's warm-up cut-off). Readiness is checked on a
   throwaway copy of the strategy, as `run_backtest` does: `is_ready()` on the live strategy moves its state.
3. Every `poll_seconds`: the candles completed since the last one fed are fetched at `fetch_interval_seconds` and fed
   through the backtest's `CandleBuilder.add_row` (`DataManager.ingest_completed_rows`). A bar closes as soon as its
   last fetched candle is in (a daily bar once its 23:00 hour is complete), so it is decided about one poll after
   it ends. Fetching 1h and combining to 1d is exact on Kraken Futures (measured 2026-11-17: 30 days, 0 differences
   on open, high, low, close, volume).
4. The bar is decided by `TradingBot._process_symbol_candle_completion`, unchanged; the gap rule as in backtests.
5. Stop (Ctrl+C): the local book's position is closed at the last decided bar, as at the end of a backtest
   (operator 2026-11-17: close for security). Real positions too, from step 5.

**Why this can't leak.** Only candles whose whole period has passed are fed (the one Kraken is forming is dropped);
a bar is decided once all of its period has passed; warm-up bars only prime the strategy.

## Settings (`live_config.json`, one per run, written at the first start)
| Setting | Default | What it is |
|---|---|---|
| `symbol` | given | the coin, research naming |
| `interval_seconds` | 86400 | the bar: when a decision is taken |
| `fetch_interval_seconds` | 3600 | the candles fetched and combined into a bar |
| `poll_seconds` | 60 | how often Kraken is asked |
| `orders` | `off` | `on` from step 5 |
| `target` | `real` | `test` needs `test_host` (Kraken's public demo was retired on 2026-07-14) |
| `start_value` | none | the local book's start; none = the real account's value (operator 2026-11-17) |
Live settings never go in `config.json`: research backtests read its `fetch_interval_seconds`.

## Storage and naming
```
trading-bot/live_runs/<name>/
  live_config.json       committed   the run's settings
  strategy_config.json   committed   a copy of the strategy: a later edit of the original changes nothing here
  summary.md             committed   status, rewritten after every bar
  run.log                local       the run's log, appended by every start
  session_NN/            local       one per start
    session.json         start time, start value, warm-up cut-off and length, the account at start
    candles.csv          every completed candle fed, warm-up included: what the replay proof reads
    local_book.csv       the backtest's per-bar record (PortfolioStateTracker)
    real_book.csv        per bar: decision time, close, forecast, local and real values, real position
    local_trades.json    the local book's trades
```
Each file's use: `candles.csv` + `session.json` make a session replayable (without them, parity cannot be shown);
`local_book.csv` is what the replay is compared with; `real_book.csv` is the live-vs-local comparison the business
question asks for (without it, the real account's path is lost); `summary.md` is what the operator reads.

## The AI
None: this function calls no model.

## Quality criteria
1. Parity: a backtest of the session's recorded candles gives a byte-identical `local_book.csv`
   (`live/proof/replay_session.py`).
2. No lookahead: no candle fed before its period ended.
3. Timing: each bar decided within one poll after it ends.
4. Completeness: one decision per bar, no missing day, no failed poll left unretried.
5. Backtest unchanged by this function's shared-code changes (`live/proof/backtest_fingerprint.py`).

## Fixed inputs
- Strategy: `night_013_run 013-01 ... b1_nearness-to-high-more-coins_1d` (step 5 confirmed, step 6 profitable;
  `required_bars` 456, so a 912-day warm-up), on `BTCUSD` / `PF_XBTUSD`, daily bars from hourly candles.
- Backtest baseline: 3 fixed backtests of that strategy on BTCUSD (two daily fold-A windows, one from hourly
  candles), kept in `../tb-live-proof/baseline_1`.
- Offline replay: `local_data/kraken_BTCUSD_1h.csv`, 60 simulated days, polls every 1,789 s
  (`tests/test_live_session_parity.py`).

## Variants compared
None yet. Considered and not built: opening a position at launch on the last completed bar (a decision the backtest
never makes); building both books from one strategy instance by restructuring `TradingBot` (rejected for a wrapper,
step 4).

## Who judges the output
The operator, from `live/validation/reading.md` and each run's `summary.md`.

## Done when, with its status
| Step | Done when | Status |
|---|---|---|
| 0 Baseline | fixed backtests kept, a rerun identical | done |
| 1 Kraken connection | completed candles only, account read, keys never shown | done |
| 2 Live feed, Binance live code removed | parity test holds; backtest rerun = baseline | done |
| 3 First live run, orders off | outcome A on `first_paper` (see validation) | running since 2026-11-17 23:19 UTC |
| 3b Decision on the clock | poll 3 s after each bar's last candle ends, one retry 5 s later; the price at decision recorded beside the close; the decided candle re-read later and any change recorded | planned, built after `first_paper`'s reading (operator 2026-11-18) |
| 4 Real book next to the local book, orders logged only | fake-exchange tests; one day of would-be orders | not started |
| 5 First real orders, small account | daily real vs local comparison | not started |

## Planned: decision on the clock (step 3b)
Measured 2026-11-18 around 13:00 UTC: Kraken publishes an hour's finished candle within 2 s of the hour and does
not change it afterwards (read until +132 s); in the first minute after a close the price moved up to 0.05%. Today a
bar is decided 0 to 60 s after it ends (the poll runs every 60 s from the start's second; first bar: 55 s). Change:
poll 3 s after each candle ends, one retry 5 s later if it is not there (1 to 2 requests an hour instead of 60);
record the price and time at decision next to the close; re-read the decided candle a few minutes later and record
whether Kraken changed it (record only, no rule). Built after `first_paper`'s reading so the code under the three
runs does not change; needed before real orders, when a late decision costs money.

## Open (not ruled on)
- Funding payments, the spot-versus-perpetual price gap, risk management: later, with the operator.
- Aux feeds live: refused at start for now (the poll method is kept, unwired).
- A restart starts the local book again from the real account's value (stop closed its position).
- Starting from a terminal opened before the key was set: the key must be loaded into that window first.

## What this function does not do
It does not design, test or choose strategies; it runs one the research already backtested.
