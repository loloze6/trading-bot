# Output generation time, per output (2026-11-16)

Measured on this PC, 0 USD: the d1 config, 6 BTC windows in one process, each writer timed in place (scratch driver,
no repo change). Per window: about 3.1 s of engine work, of which **about 0.94 s (30%) is producing the outputs**.
The machine that runs the loop is roughly twice as fast (phase 1), so there it is about 0.5 s per window, or about
**1.1 min per idea** over 144 windows (estimate).

## Per output, per window (ms, measured)

| Output | Who writes it | Kept by step 4? | ms per window | Where the time goes |
|---|---|---|---|---|
| `portfolio_states.csv` | engine | no (deleted, but `run_protocol.py` reads it first) | **281** | flattens the state table **a second time**, then writes |
| State table for `metrics.json`, `bars.csv`, `forecast_distribution.csv` | engine | (input to three files) | **224** | `flatten_dict_columns`: one pandas Series per row |
| `manifest.json` | engine | yes | **188** | 185 of it is `git rev-parse` + `git status` on the repository; the write itself takes 3 |
| `metrics.json` | engine | yes | 97 | metric builders (core 42, performance 30, bar equity 9, others 15), write 1 |
| `tradesxl.xlsx` (2 sheets) | engine | no (deleted) | 76 | Excel writing |
| `trade_diagnostics.json` | wrapper | yes (gzipped) | about 25 today | schema check 14 and extended summary 10, paid once per call, so once per window today; per-trade records 9 |
| `protocol_summary.json` | wrapper | yes (gzipped) | under 1 | |
| `bars.csv` | engine | yes (gzipped) | 6 | |
| `forecast_distribution.csv` | engine | yes | 5 | |
| `trades.json` | engine | yes (gzipped) | 2 | |
| Run folder | engine | | 1 | |
| Step 4's copies and gzips (7 files) | `run_backtest.py` | | about 5 | gzip 0.2 to 2.4 ms per file (13 to 103 KB) |
| Other end-of-window work (price merge) | engine | | about 20 | |
| **Total** | | | **about 940** | |

## Reading
- **Three items make 75% of the output time.** Flattening the state table twice (505 ms) and the `git` calls for the
  manifest (185 ms). Writing the files themselves is cheap: under 15 ms all together.
- **Files step 4 deletes cost 357 ms per window:** `portfolio_states.csv` 281 and Excel 76. Only Excel is pure waste,
  because the wrapper reads `portfolio_states.csv`.
- **Step 4's own copying and compression** take about 5 ms per window: nothing to gain there.
- Change 1 (one process per coin) also cuts the wrapper's once-per-call costs (about 25 ms) from per window to per coin.

## Pictures and charts: none are drawn
- Step 4 draws no chart. The engine's only chart (`plot_regime_chart` in `performance/metrics.py`) runs in two
  cases, and neither happens here:
  - with `human_reports`, which is off on this path;
  - in a separate past-data analysis mode of `core/launcher.py`.
- Checked three ways: the profiler shows no call in 6 windows; `strategy-research/tools` and the step helpers have no
  chart code; `demo_run` holds no image file.
- **What is paid anyway: loading the chart libraries.** `performance/metrics.py` imports matplotlib and plotly at
  start-up: **0.32 s per process** (measured), about 4% of a window today, since every window is a new process. Loading
  them only when a chart is actually drawn would save about 46 s per idea on this PC (estimate: about 25 s on the run
  machine). After change 1 there are only 6 processes per idea, so about 2 s. That is an engine change for little gain
  once change 1 is in, so it is not proposed.

## What the items in `4_backtest_code.md` would do to it
| Item | Output time per window |
|---|---|
| today | about 940 ms |
| B3 (`git` once per process) | -185 ms |
| B6 (skip Excel, opt-in) | -76 ms |
| B2 (one-go flatten, both calls; must keep today's exact types) | about -450 ms (13x faster when tested; types to fix first) |
| all three | about 200 to 250 ms (estimate) |
