# Phase 3: plan, ranked by gain for effort (2026-11-16, revised after review the same day). Nothing is built before the operator says go.

Today: about 11.7 min per idea, 9.3 of them in step 4 (from `demo_run`'s journal, written on the machine that runs
the loop).
- **The run machine:** a Linux container with 4 cores and 15 GB of memory (reviewer, 2026-11-16). The record's
  tracebacks show its `/home/user/...` paths.
- **Where my timings were taken:** on a 4-core Windows laptop. Starting Python is slower on Windows, so every gain
  below is an **estimate** for the run machine until gate 0 and the proof time it there.
- **Target with changes 1 and 2:** about **5 to 6.5 min per idea** (estimate). This replaces the earlier 4 to 5.5 min,
  which assumed more than 4 cores.

| Rank | Change | What changes | Expected gain per idea (run machine, estimate) | Needs the operator's go on |
|---|---|---|---|---|
| 1 | **One process per coin** (F1) | `04_backtest/helper/run_backtest.py` only: one `run_protocol.py` call per coin with its 24 windows, instead of 24 calls. Each run folder is matched to its window through the coin's `protocol_summary.json`. **Failure rule:** `run_protocol.py` stops at the first window that fails (no `try` around `run_backtest` in its window loop), so the coin's later windows would be lost. If the call fails, or returns fewer run folders than windows (the same-second clash), the whole coin is rerun one window at a time, as today. That coin's record, including the failure text in `run.md`, is then exactly today's. Cost: a coin with a failed window is paid twice. | 2 to 3.5 min (-44% measured on Windows; the Linux share of start-up is not known yet) | the record's new layout: `protocol_summary.json.gz`, `trade_diagnostics.json.gz` and `engine_log.txt` per coin instead of per window; every other window file unchanged |
| 2 | **Coins in parallel** (F2), only after change 1 is proven | (a) `strategy-research/tools/run_protocol.py`: an opt-in flag, **off by default**, giving the engine's interim trades file a path inside the call's own output folder (the engine's existing `trades_log_file` parameter). Without the flag, nothing changes for the campaign. (b) `run_backtest.py`: the coins run at the same time; `run.md` and `INDEX.md` stay in the same order. **Workers:** 6 at once, not "one per core". On the 4-core laptop, 6 at once (21.6 s) beat 4 at once (27 s), because 4 workers run 6 coins in two waves with idle cores in the second. The proof times 4 and 6 on the run machine and keeps the faster. **Data-file guard:** see "Shared files" below. | 2.5 to 3.5 min more on 4 cores | the change to a tool shared with the campaign |
| 3 | Step 6 alongside step 5 (F5) | `run_idea.py` | 3 s | not proposed |
| 4 | Engine, safe and simple (B3 to B6 in `4_backtest_code.md`) | `trading-bot/` | under 1 min once 1 and 2 are in | **deferred** (see below) |
| 5 | Engine, faster tables (B1, B2) | `trading-bot/` | under 1 min once 1 and 2 are in | **deferred** (see below) |

**Deferred: changes 4 and 5.** After changes 1 and 2, step 4 is about 2.5 to 4 min. The 15 to 35% they cut from the
engine is then under a minute per idea. They also change engine code that the campaign and the live bot use. Revisit
only if step 4 is still over about 3 min on the run machine after 1 and 2.

Not proposed: lazy imports (F4: covered by change 1), a faster model (F7: changes results), shared warm-up (F8:
changes results), two workers on one coin (F9: price-file risk), faster strategy maths or a numpy engine
(`4_backtest_code.md`: results or risk).

## Shared files (why change 2 needs a guard)
- **The interim trades file** (`trading-bot/results/trades.json`, one fixed path). Parallel coins crashed on it in the
  phase 2 test. Fix: the opt-in flag in change 2(a).
- **Data files shared between coins.** Each coin's price file is used by one process only. But every backtest also
  loads all registered aux feeds unless they are dropped (`core/launcher.py`, `extra_feeds`). `fear_greed_daily.csv` is
  one file for every coin. The fetcher rewrites a data file when a read adds new rows (`_merge_and_store` in
  `data/fetchers/base_fetcher.py`). Two coins at once could both rewrite it. A past run (`run_096`) already died on this
  very file, with a Windows lock error, while another handle held it.
- **Guard:** before and after the parallel step, step 4 records the size and modification time of every file in
  `trading-bot/local_data/`, the sealed holdout store excluded, never opened. If any file changed, the step is rerun
  one coin after another (today's way) and `run.md` says so. In `demo_run`, no data file changed (same data hash for
  the same coin and window in all four ideas), so the guard should not fire.
- **The bot's log file** (`logs/bot.log`) is shared too. It holds logs, not results.

## Why this can't leak (no lookahead)
- **Change 1:** each window still makes its own `run_backtest` call with the same start, end, warm-up and holdout
  guard as today. What a window sees is fixed by its own call, not by the window run before it in the same process.
  - No data carries over: each `run_backtest` call builds a new launcher, data manager and fetcher
    (`core/launcher.py`). This was checked after review; an earlier version of this note wrongly said the fetcher's
    copy carried over.
  - Reading the price file once per process would be engine item B5, which is deferred.
- **Change 2:** separate processes, one coin each; nothing is shared in memory. The shared files are handled by the
  flag and the guard above.
- **Neither change** touches the holdout path or `local_data/holdout_sealed/`.
- **Shown, not only argued:** for every window, the manifest's data block must match the baseline (`start`, `end`,
  `bar_count`, `data_sha256`), and so must `bars.csv`.

## How we prove results did not change (0 USD, no model call)
**Gate 0, before building (run machine, 0 USD):**
- Time one bare Python start with the bot's imports, and one window of e1.
- This gives the Linux share of start-up, so change 1's real gain is known before any code is written.
- I cannot reach that machine from here.

**Three cases**, each with `--force` into a scratch `--out-root`, never into the run's folders:

| Case | Why | Windows |
|---|---|---|
| `demo_run` e1 | the plain case: every window runs | 6 coins x 24, all run |
| `full_data_run` 002-03 | windows that fail in the middle of a coin (warm-up assertion): tests the failure rule | 6 coins x 24; XMR w13, XRP w7 and w13 fail |
| `hourly_run` 001-01 | hourly bars (more data per process), and a coin that fails on every window | BTC, ETH, BNB x 6 (fold A); all 6 BNB windows fail (no data on the venue) |

For each case:
1. **Old**: today's `run_backtest.py`, timed. This is needed because `bars.csv.gz` and `trades.json.gz` are not in git.
2. **New**: the changed helper, twice (new-1, new-2), timed. A second run catches anything that depends on timing.
3. **Compare old, new-1 and new-2.** Zero differences outside this list of allowed ones:
   - `manifest.json`: `run_id`, `created_utc` and `git_sha` only.
   - `engine_log.txt`: per coin instead of per window, by design. Not compared, except that the failure text kept in
     `run.md` must match.
   - `protocol_summary.json.gz`, `trade_diagnostics.json.gz`: per coin instead of per window.
     - Each window's own entry in the coin file must equal that window's entry in the old file.
     - Their totals over all windows of the call (e.g. the diagnostics `summary`) differ by design: they now cover 24
       windows, not 1. No later step reads these two files.
     - Neither file is in git; both exist only in the scratch runs.
   - Gzip files are compared unzipped (a gzip header holds a time).
   - **Byte for byte**:
     - per window: `metrics.json`, `forecast_distribution.csv`, `bars.csv`, `trades.json`;
     - per idea: `run.md`, `INDEX.md`, `config.json`;
     - and which windows failed, with what reason.
   - `metrics.json` and `forecast_distribution.csv` are also compared with the committed record.
4. **Verdicts:**
   - Step 6's check, old vs new: same `result.json`. This applies to e1 and 002-03; `hourly_run` has no step 6
     record.
   - Step 5: the saved `measure.py`, run by step 5's own runner on old vs new: same result, with no new model call.
     This applies to all three cases.
5. **Time:** step 4's minutes for old, new-1 and new-2, on this PC. On the run machine: gate 0, then the journal's
   clock times at the next real run. Change 2 also times 4 and 6 workers there.
6. Change 2 also runs the new helper once without the new flag, to show that the campaign's path is unchanged.
7. The helper's own tests (`test_*.py`) still pass, plus new tests:
   - the failure rule (a failing window, and the same-second clash);
   - for change 2, the data-file guard.

Order: change 1, then proof, then operator review; then change 2, proof, operator review. One branch per change. The
loop uses `run_backtest.py`, so each change is merged into `ccr-6624e33e-aakrpv` only when no loop is running.
