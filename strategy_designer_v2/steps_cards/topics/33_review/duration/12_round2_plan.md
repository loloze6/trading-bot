# Round 2, plan: a faster hourly backtest, results unchanged (2026-11-20). Nothing is built before the operator's go.

From `11_round2_measure.md`. Today, per idea (6 coins x folds A to D, 4 cores): about **10 min** for a light book
(grind, deep; recorded 606 to 688 s) and about **58 min** for a book with a 720-bar volatility average (evening;
recorded over 53 min).

## Speed changes (every recorded result file identical)
| Rank | Change | Where | Gain (per idea, 4 cores) | Effort | Risk |
|---|---|---|---|---|---|
| A | **Compute the episode bootstrap only where its numbers are read.** On step 4's path only its method label is written, and the label is decided before the resamples. The resamples stay on the path that reads them (a validation protocol's decision rules) | `trading-bot/backtest/run_protocol.py` (shared with the campaign) | deep: 87 s of 307 per coin, so **10 -> about 7.5 min**; grind and evening: under 1 min | small | low: the protocol summary must be byte-identical; the campaign's verdict path is unchanged |
| B | **Volatility components reuse the previous bar's standard deviations.** One shared helper ("the std of each of the last L return windows"), used by the four components with this loop: when the closes read are the previous bar's shifted by one bar, only the newest std is computed; otherwise all, as today. Each std is still `np.std` on the same values, the mean still `np.mean` of the same list in the same order | `trading-bot/strategies/strategy_components.py` | evening: **58 -> about 9 min** (prototype: 433 -> 63 s, 7x, files identical). 7 of 88 hourly plans have such a component; 0 gain for the others | small | low: proven bit for bit on every bar (check mode), then by files |
| C | **Step 4 runs one call per coin and fold** (24 calls, 4 at a time) instead of one per coin (6 calls, two waves) | `04_backtest/helper/run_backtest.py` only (not shared) | all books: about **-25 % of step 4** (6 coins on 4 cores leave a quarter of the core time idle); estimate | small | low for results: each window is already its own engine call. **Changes the record's layout**: the wrapper's `protocol_summary.json.gz`, `trade_diagnostics.json.gz` and `engine_log.txt` become one per coin and fold. Only step 4 reads `protocol_summary` (to find run folders); no other step reads the three. The fallback rule (one call per window) stays, per call |
| D | **Per-bar glue, the same tables built more cheaply**: (1) the backtest rows read from arrays taken once per window; (2) the strategy's history table built with its indicator column in one construction; (3) the one-bar table built from typed arrays; (4) debug messages formatted only when debug logging is on | `trading-bot/data/data_manager.py`, `strategies/strategy_base.py`, `core/trading_bot.py` | all books: about **-20 % of the bar loop** ((1)+(2) measured -15 %, files identical; (3) about -6 %, micro-benchmark; (4) estimate) | medium (4 places) | low to medium: types and column order must match exactly; check mode compares every table with today's on every bar, then files |

**Together (estimates):**
| Book | Today | After A and B | After C | After D |
|---|---|---|---|---|
| light, deep kind | about 10 min | about 7.5 min | about 5.5 min | about 4.5 min |
| light, grind kind | about 9 min | about 9 min | about 6.5 min | about 5 min |
| 720-bar volatility, evening kind | about 58 min | about 9 min | about 6.5 min | about 5.5 min |

**Recommended order: A and B first** (small, independent, exact, the largest gains on the slowest books), **then C**
(orchestration only, but a layout change for your go), **then D** (medium effort; worth it once A to C are in, as
the bar loop is then most of the time). One branch and one proof per change, as in round 1.

**Why these cannot leak.** A computes less after the backtest, on bars already recorded. B reads the same closes
(the last bars up to bar t) and reuses values computed from those same closes on the previous bar. C changes which
process runs a window, not what a window reads (each window is its own `run_backtest` call with its own dates,
warm-up and holdout guard). D builds the same tables from the same bars. Shown, not argued: each window's manifest
data block (start, end, bar count, data hash) and `bars.csv` must stay identical.

## How each change is proven (0 USD, no model call)
- **Fixed inputs:** the three plans above (grind, deep, evening), through step 4's own helper
  (`run_backtest.py PLAN --out-root SCRATCH --force`), 6 coins x folds A to D. Today's code once (the baseline, about
  80 min, resumable), the changed code twice (new-1, new-2).
- **Compared byte for byte, per coin and window:** `bars.csv`, `trades.json`, `metrics.json`,
  `forecast_distribution.csv` (unzipped); `manifest.json` except `run_id`, `created_utc`, `git_sha`; `run.md`,
  `INDEX.md`, `config.json`; which windows ran and why not. A: `protocol_summary` too. C: each window's entry in the
  wrapper files equals today's (the layout aside).
- **B and D also in check mode:** today's code and the new code both run on every bar of one coin and fold; every
  value (B) or table (D: values, types, column order) must be equal.
- Step 5 (the saved measure) and step 6 (`check_profitability.py`) rerun on old and new: same results.
- The bot's suite, the cards' suite.

## Research changes: proposed only, not part of this work
| Option | Gain | What it changes in the research |
|---|---|---|
| **A shorter warm-up** | half the bars processed today are warm-up (2 x 1,441 bars before each window, set by the 60-day sizing window): up to about -40 % | the state on each window's first bars (`common/backtest_record.md`); the sizing and every component must still be ready, so it needs a rule for how much warm-up each piece needs |
| A shorter history table handed to the components (today 1,541 rows, set by the sizing's 1,440 closes; most components read under 100) | part of the 13 to 17 s of table work per 6 windows | rolling sums start elsewhere, so the last digits of some values can move: not identical |
| More cores (6 or 8) | 6 cores: all coins in one wave, about -50 % of step 4 (C then adds nothing) | none: the environment's choice (operator's settings) |
| Fewer coins, folds or windows; sampling bars; fewer recorded columns; another cost model | see the brief | as the brief says |

## Not proposed
- Skipping the Excel exports step 4 deletes: about 1 s per 6 windows (under 2 %), a change to shared code for little.
- A rewrite of the bar loop without pandas tables: the real cure for the glue, but large and high risk; reconsider
  only if D is not enough.
