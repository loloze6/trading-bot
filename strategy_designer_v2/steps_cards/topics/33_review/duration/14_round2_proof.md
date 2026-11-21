# Round 2, proof: A to D built, results unchanged (2026-11-20)

Built on the operator's go ("go for A, B, C and D"), from `12_round2_plan.md`. Branch `engine-speed-round2`, one
commit per change: A `f1ffee6`, B `8077241`, C `e99d410`, D `c583ff4`. Today's code = `ad854eb` (before A).
D(2) of the plan (the history table built with its indicator column in one construction) was built, measured as no
gain once (1) and (3) were in, and left out.

## How
The three fixed plans (grind, deep, evening; `hold_ideas_1h_run/plans/`) through step 4's own helper
(`run_backtest.py PLAN --out-root SCRATCH --force`), 6 coins x folds A to D, on this container (4 cores), each stage
alone on the machine. Compared per coin and window: `bars.csv`, `trades.json` (unzipped), `metrics.json`,
`forecast_distribution.csv` byte for byte; `manifest.json` except `run_id`, `created_utc`, `git_sha`; `run.md`,
`config.json`, the `INDEX.md` line; which window folders exist; the wrapper's per-window summary entries and the
diagnostics' trades. Before C, also the wrapper's whole files. 0 USD, no model call.

## Files
| Compared | Identical | Differ |
|---|---|---|
| today vs A (grind, deep) | 1,518 | 0 |
| today vs A+B | 2,277 | 0 |
| today vs A+B+C | 2,241 | 0 |
| today vs A to D, run 1 | 2,241 | 0 |
| today vs A to D, run 2 | 2,241 | 0 |
| A to D run 1 vs run 2 | 2,241 | 0 |

(After C, fewer items: the two wrapper files per coin are no longer whole-file comparable, see below; their window
entries and trades are compared.)

**Steps 5 and 6** on today's records and on A to D's (the saved measures of `hold_ideas_1h_run`, `--measure`;
`check_profitability.py`): the verdicts and checks are identical except the line naming the record's folder.
| Plan | Step 5 | Step 6 |
|---|---|---|
| grind | inconclusive (t 1.50) | not profitable enough (Sharpe 0.84) |
| deep | confirmed (t 2.63) | not profitable enough (Sharpe 0.25) |
| evening | confirmed (t 6.95) | not profitable enough (Sharpe 1.15) |

**Tests:** the bot's suite 1,575 passed, 16 skipped; step 4's helper tests 12 passed. New tests: A
(`test_a851a_method_only.py`), B (`test_trailing_return_stds.py`, bit for bit against the old loops on real BTC
closes), D (`test_backtest_rows_and_bar_table.py`).

## The one layout change (C, as planned)
The wrapper's `protocol_summary.json.gz`, `trade_diagnostics.json.gz` and `engine_log.txt` are now one per coin and
fold (`<COIN>/fold_<X>/`). The episode method label in `protocol_summary` is therefore decided per fold: in 3 of 72
coin-folds it differs from the old per-coin label (deep: LTC fold C, ZEC folds B and D). Nothing in the workflow reads
it (only step 4 reads `protocol_summary`, for the window entries).

## Times per idea (seconds, 6 coins x 4 folds, 4 cores)
| Plan | Today | A | A+B | A+B+C | A to D |
|---|---|---|---|---|---|
| grind | **557** | 500 | 526 * | 415 * | **340** (347, 353) |
| deep | **591** | 482 | 515 * | 384 * | **332** (336, 342) |
| evening | **3,783** * | - | 585 * | 425 * | **388** (394) |

Bold: re-timed back to back, each alone (today, A, A to D). * one run of the stage sequence; the first baseline
(grind 606, deep 524) shared the machine with tests, so it is replaced by the re-timing.
- grind -39 %, deep -44 %, evening -90 % (63 min -> 6.5 min).
- Against the plan's estimates: light books 5.5 to 5.7 min (plan: 4.5 to 5); evening 6.5 min (plan: 5.5).

## Why these cannot leak
Shown by the files: every window's manifest data block (start, end, bar count, data hash) and `bars.csv` are
identical. A computes less after the backtest; B reuses stds computed from the same closes on the previous bar; C
changes which process runs a window, not what it reads; D builds the same tables from the same bars.

## Next
- Merge into the designer's working branch: the designer session (not while a loop runs on it). Into master: the
  operator's go.
- Not done, a separate decision: the dynamic warm-up (`13_round2_warmup.md`), about -20 % more (estimate).
