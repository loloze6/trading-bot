# Deep dive: inside the backtest engine (2026-11-16)

Question: once change 1 is in (one process per coin, so Python starts once), where does a window still spend its time,
and what could be faster with identical results?

How measured: on this PC, the d1 config, 6 BTC windows in one process (what change 1 produces). Each hot function was
timed in place with a light wrapper (a scratch driver that patches nothing in the repo), plus a profiler for detail.
0 USD, no model call. Real time for the 6 windows: 18.7 s of engine work (3.1 s per window) + 2.7 s of imports, once.

## Where a window's engine time goes (measured, real seconds)

| Part | Share | What the code does |
|---|---|---|
| **Rebuilding the bar table, every bar** (`RollingBuffer.get_df`, `strategies/strategy_base.py`) | **38%** | The strategy keeps its last ~300 bars as a list of dicts, and rebuilds a whole pandas table from it at every bar (5,530 rebuilds for 6 windows, warm-up included), then recomputes a 24-bar std column on it. |
| Strategy maths (the components) | 13% | Rolling max/min/mean over the table, per bar |
| **Flattening the state table, twice** (`flatten_dict_columns`, `execution/portfolio_info.py`) | **16%** | At the end of a window, dict fields (balances, debug info) become columns, by building one small pandas Series per row. Done once for the metrics and once again for `portfolio_states.csv`. |
| **`git status` per window** (`_get_git_sha`, `reporting/run_artifact.py`) | **7%** | Runs `git rev-parse` and `git status` on this 32,000-file repository, for the manifest's `git_sha` field |
| Loading the coin's prices (`load_data`) | 5% | Re-reads the coin's whole CSV each window |
| Reading YAML policy files | 4% | The holdout policy and cost model are parsed again for each window (26 parses for 6 windows) |
| Per-bar candle history (`get_data_history`) | 5% | Slices the last candles per bar |
| Excel exports | 2% | `tradesxl.xlsx`, which step 4 deletes |
| Other per-bar engine and metrics code | about 10% | |

Warm-up: 400 of every window's 920 strategy updates are warm-up bars, so it pays the same per-bar costs.
Correction to phase 2 (F3): `portfolio_states.csv` is **not** pure waste. `run_protocol.py` reads it back to get
full-precision closes for `trade_diagnostics.json`. Only the Excel files are pure waste.

## What could be faster, with identical results

| # | Change (all in `trading-bot/`, shared with the campaign and the live bot) | Tested here | Gain on a window's engine time | Effort | Risk |
|---|---|---|---|---|---|
| B1 | **Faster bar table**: build each column straight from typed values (float, int, date) instead of the generic dict-to-table path. Fall back to today's path if any value is not plain. Better still: keep the columns up to date as bars arrive. | simple version: 1.39 -> 1.01 ms per bar on a 301-bar buffer (-27%), table identical (values, types, order) | 10% (tested version) to about 20% (estimate, incremental version) | small to medium | low: same table or the old path |
| B2 | **Faster flatten**: build the dict columns in one go instead of one Series per row | 13x faster (4.28 -> 0.33 s), **but** 2 of about 30 columns differ in type: an integer `0` that today's per-row Series turns into `0.0` (`balances.<coin>.locked`). It needs today's exact type rule reproduced and checked. | about 14% | medium | medium: type rules are the trap. Only with a strict check on every call. |
| B3 | **`git status` once per process**, not once per window | not timed (simple) | 7% here (git is likely faster on the Linux run machine) | trivial | none for results. The manifest's `git_sha` "-dirty" mark could reflect the start of the coin rather than the end of each window. |
| B4 | **Parse the policy YAML files once per process** (cached by path and file time) | not timed | 4% | small | none |
| B5 | **Read the coin's CSV once per process** (cached by path, size and file time; the cache is dropped if the file changes) | not timed | about 4% | small | low |
| B6 | Opt-in: skip the Excel exports | not timed | 2% | trivial | none: step 4 deletes them |

Together: about **30 to 45% less engine time per window** (estimate; B1 and B2 measured alone).
B3, B4 and B5 only pay off once change 1 runs several windows per process.

Not proposed:
- **Strategy maths** (13%): faster rolling formulas can change the last digits of floats, so results could differ.
- **Sharing warm-up between windows:** that changes the state each window starts from.
- **Rewriting the engine in numpy:** the real fix for pandas overhead per bar, but large and high risk.
- **Lazy imports:** 1.4 s per process; change 1 already pays the imports only 6 times per idea.

## What it is worth in minutes per idea (run machine, estimates)

| If done after | Step 4 today | Engine items save |
|---|---|---|
| nothing else | 9.3 min | 2 to 3 min (B1, B2, B6 only; B3 to B5 need change 1) |
| change 1 | about 5.5 min | 1.5 to 2.5 min |
| changes 1 and 2 | about 1 to 2.5 min | 0.3 to 1 min |

Verdict: changes 1 and 2 (orchestration) are worth far more. The engine items are a second step: worth it if the run
machine has few cores, or because they also speed up every campaign backtest. They change shared engine code, so each
one needs your go.

## How we would prove identical results
- Each change is checked **inside a real run**: today's code and the new code both run on every call, a strict
  comparison is made (columns, types, values, the type of every element), and today's result is the one that is used.
  This is how B1 and B2 were tested above.
- Then the phase 3 proof: all 144 windows of e1, byte for byte, against a baseline.
- The bot's own tests must still pass (including `tests/test_bar_equity_bit_identical.py`).
