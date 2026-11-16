# Phase 2: why it takes that long, and what could make it faster (2026-11-16)

Baseline: 11.7 minutes per idea on the machine that ran `demo_run` (phase 1), step 4 = 9.3 of them.
Measurements below were made on this PC (4-core laptop), 0 USD, no model call, on the d1 idea's config (already tested).

## What I measured for this phase

| Test (this PC) | Result | Outputs identical? |
|---|---|---|
| 6 windows (one per coin), one after the other vs 6 at once | 44.0 s vs 21.6 s (x2.0). With 2, 3, 4 at once: 32, 27, 27 s | yes, 6 of 6 `metrics.json` |
| 6 BTC windows: one process each (today) vs one process for all 6 | 50.7 s vs 28.4 s (**-44%**) | yes, 6 of 6 |
| 6 coins x 6 windows: one process per coin, 6 coins at once | **2 coins crashed** (see F2) | not comparable |

## Findings

| # | Where the time goes | Why | What would make it faster | Gain per idea | Effort | Risk | Results identical? |
|---|---|---|---|---|---|---|---|
| F1 | Step 4: Python start-up, 144 times | `run_backtest.py` starts one process per window, so the bot is imported 144 times (about 1/3 of each window). It does so to avoid a clash: the engine names each run folder after the current second, and two windows ending in the same second would share one folder. | **One process per coin**: `run_protocol.py` already accepts several windows; give it the coin's 24 windows at once. Guard the clash: if fewer run folders than windows come back, rerun that coin one window at a time (today's way). | **3 to 4 min** (step 4 -30% to -44%: -44% measured here; the share on the run machine is an estimate) | small: `run_backtest.py` only | low: a window could inherit state from the previous one in the same process. Measured: 6 of 6 identical; the proof covers all 144. | yes for every window file. Changes the record's layout: `protocol_summary.json`, `trade_diagnostics.json` and `engine_log.txt` become one per coin instead of one per window. No later step reads them. |
| F2 | Step 4: everything runs one after the other | Nothing in step 4 runs at the same time. | **The 6 coins at the same time** (6 workers; the windows of one coin stay in order). Blocker found: the engine writes an interim trades file at one fixed path (`trading-bot/results/trades.json`) and reads it back for an Excel export; two processes at once read each other's file and crash. Fix: give each process its own interim file. The engine already has the parameter (`trades_log_file`); the wrapper `run_protocol.py` does not pass it: one opt-in flag to add there. | alone: **4.5 to 7.5 min** (x2 measured on this laptop; x4 to x5 expected on a machine with 6 free cores: not measured, its core count is unknown) | small, but touches `strategy-research/tools/run_protocol.py`, shared with the campaign | medium until proven: other shared files may exist (the bot's log file is shared too, but it holds logs, not results). One coin per worker means no two processes ever write the same price file. | yes: the interim file only feeds the Excel export, which step 4 throws away; the kept `trades.json` is written from memory. |
| F1+F2 | | | both | **6 to 8 min**: an idea in about **4 to 5.5 min** (estimate) | | | |
| F3 | Step 4: writing files step 4 throws away | The engine writes two Excel files per window that step 4 deletes (2% of a window, measured in `4_backtest_code.md`). Corrected: `portfolio_states.csv` is read back by `run_protocol.py` (full-precision closes for `trade_diagnostics.json`), so it is not waste. | a "do not write Excel" option in the engine | small | trivial | engine change, shared with the campaign | yes |
| F4 | Step 4: heavy imports | `performance/metrics.py` imports hmmlearn/sklearn, `data_manager.py` the binance client, at start-up | import them only where used | covered by F1 | small | engine change | yes |
| F5 | Step 6 waits for step 5 | Step 6 (2 to 4 s, code only) reads only the record, not the verdict | run it alongside step 5 | **3 s** | trivial | none | yes |
| F6 | Step 7 | Already in parallel; its time is its slowest line (60 to 90 s), model calls | nothing at orchestration level | 0 | | | |
| F7 | Steps 3, 5, 7 (model calls, 2.4 min) | Model time | a faster model | | | | **no**: changes the outputs. Out of scope. |
| F8 | Warm-up (14% of a window) | Each window re-feeds 61 bars before it starts | | 0 | | | sharing warm-up between windows would change the state each window starts from. Not proposed. |
| F9 | More than 6 workers (2 per coin) | | | small beyond the core count | | two processes on one coin could rewrite the same price file (the data path tops up a coin's file on read) | not proposed |

## Side finding (visibility, not speed)
The run table's "Minutes" adds up step 7 lines that run at the same time: it shows 13.7 where the real time is 12.5.
To measure the gain honestly, the proof below uses the journal's clock times, not the table's minutes.

## What I do not know
- ~~How many cores the machine that runs the loop has.~~ Answered at review (2026-11-16): a Linux container, 4
  cores, 15 GB. So F2 is worth about x2 there, not x4 to x5, and F1+F2 come to about 5 to 6.5 min per idea (see
  `3_plan.md`).
- How much of a window is Python start-up on that Linux machine. All timings here were taken on Windows, where
  start-up is slower, so F1's gain there is an estimate until gate 0 in `3_plan.md` measures it.
- How step 5's 40 s split between the model and its code: its logs are not in the repository.
