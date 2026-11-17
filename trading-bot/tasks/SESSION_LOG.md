# Session log: live trading on Kraken Futures

## Session 2026-11-17/18

**Hypothesis.** The bot's per-bar decision is already shared by the backtest and live paths, so live trading on
Kraken Futures perpetuals needs only new parts around it (completed candles in, the real account read, records),
and a live decision can be made identical to the backtest's decision on the same candles.

**Result.** Confirmed for steps 0 to 3 (orders off).
- Picture measured: the old live path was Binance-only, never run, with 10 defects; Kraken's public Futures demo was
  decommissioned on 2026-07-14 (host redirects); Python on this PC needs `truststore` to reach Kraken.
- Operator rulings: Kraken only, Binance live code removed; no holdout in live; Kraken Futures candles, `PF_XBTUSD`
  (linear perpetual); hourly candles combined into daily bars (measured: Kraken's daily candle = its 24 hourly ones,
  30 days, 0 differences); both books in one live process with one strategy update per bar (step 4); live settings
  in each run's own folder, never in `config.json`; stop closes positions; local book starts at the real account's
  value; strategy `night_013_run 013-01 ... b1_nearness-to-high-more-coins_1d` on BTC (step 5 confirmed, step 6
  profitable, required_bars 456).
- Built: `live/kraken.py`, `live/runner.py`, `DataManager.ingest_completed_rows`, `main.py run_live` / `live_check`,
  proofs `live/proof/backtest_fingerprint.py` and `live/proof/replay_session.py`, tests `test_live_kraken.py` and
  `test_live_session_parity.py`.
- Proven: the 3 fixed backtests give the same 24 files before and after (run time, id and commit aside); a 60-day
  simulated live session feeds no candle early, decides each day within one poll after midnight UTC, and its record
  is byte-identical to the backtest engine's; bot suite 1,520 passed. 3 card tests fail in the components helper
  (other session's work, Windows path/encoding; they import no changed file).
- Found and fixed on the way: a readiness check moved the strategy's state (now a throwaway copy, as the backtest
  does); `_aux_feed_poll_loop` was removed by mistake and restored; a refused start left an empty session folder.
- First live run `first_paper` started 2026-11-17 23:19 UTC by the operator (orders off, read-only key, local book
  $105.94, warm-up 912 days, first decision ~00:00:30 UTC on 11-18). Claude Code monitors it: hourly health check,
  daily full check with the replay proof; kill only on >2 GB memory, candles.csv +1 MB, or >30 errors in an hour.
  Pre-registered outcomes: A mechanism works / B replay differs / C missing days or failed polls.

**Files touched** (branch `live-kraken-futures`, worktree `../tb-live`; commits e4e47fe, cf70cb7, dd52aa0, 1163a40):
`.gitignore`; `trading-bot/`: `main.py`, `requirements.txt`, `config/settings.py`, `core/launcher.py`,
`core/trading_bot.py`, `data/data_manager.py`, `data/ARCHITECTURE.md`, `DOC/USER_GUIDE.md`,
`execution/execution_handler.py`, `execution/portfolio_info.py`, `live/` (new), `tests/test_live_kraken.py`,
`tests/test_live_session_parity.py`, `tests/test_d176_sizing_block.py`, `tasks/live_kraken_futures_plan.md`,
`tasks/SESSION_LOG.md`. Outside git: `live_runs/first_paper/` (run records), `../tb-live-proof/` (baselines).

**Prompt for the next session (copy-paste):**

> Repository loloze6/trading-bot, branch `live-kraken-futures` (worktree `C:\Users\alauz\Documents\Projects\tb-live`).
> Read CLAUDE.md, then `trading-bot/tasks/live_kraken_futures_plan.md` (sections 3-7) and
> `trading-bot/tasks/SESSION_LOG.md`. The live run `first_paper` (orders off, Kraken Futures PF_XBTUSD, daily bars
> from hourly candles) runs in the operator's own PowerShell window. First: read
> `trading-bot/live_runs/first_paper/summary.md`, `run.log` and `session_01/real_book.csv`, run
> `live/proof/replay_session.py live_runs/first_paper/session_01` with `C:\Users\alauz\venvs\trading-bot\Scripts\python.exe`
> from `tb-live/trading-bot`, and say which pre-registered outcome happened (A mechanism works / B replay differs /
> C missing days or failed polls), with counts. Then, only on the operator's go, plan step 4: the real book next to
> the local book (one shared strategy update per bar through a wrapper, account read from Kraken, market orders to
> PF_XBTUSD, close = reduce-only of the real position, an orders-off mode that logs the would-be orders), proven by
> fake-exchange tests and one orders-off day. Never print the API key; do not touch
> `strategies/strategy_components.py` or `strategies/strategy_engine.py`; shared-code changes need the backtest
> rerun proof (`live/proof/backtest_fingerprint.py compare ../../tb-live-proof/baseline_1 <new>`).
