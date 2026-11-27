# Build A9: the forward record of a portfolio version (2026-11-27)

(Next steps A9, the operator's go "Go for next", 2026-11-27. Branch `build-a9`, from `ccr-6624e33e-aakrpv`; not merged.
Card: `orchestration/forward_record/card.md`.)

## Purpose (written before the build)
Evidence on days nobody has seen, renewed every month, without using the final coins: each month the frozen portfolio
version (v4 first) is run, unchanged, on the days after it was built, and its daily return and holding's are appended
to one file.

## Expected outcomes (written before the build)
| # | Outcome | How it is seen |
|---|---|---|
| 1 | v4's record exists with its start day and zero days (v4 was built today; the first forward day is tomorrow) | `orchestration/forward_record/v4/` |
| 2 | An update only adds days | a test; and two updates in a row on the scratch record, the first rows compared byte for byte |
| 3 | On past days, the mechanism gives the common records' numbers | a scratch record with a pretended start day, compared day by day with what `update.py` computes from the common records; every difference explained |
| 4 | The holdout guard accepts the coming forward days, or refuses them | the guard asked before any run; its message reported unchanged |
| 5 | The final coins are never read | a test of the kind `common_record` has |
| 6 | Both test suites pass | counts below |

What could go otherwise, named before: the guard refuses (then stop and report); the data tool cannot extend what a
strategy needs (then stop and report, no change to the tool); the numbers differ from the common records beyond the
windows' edges (then the difference is the finding).

## What was built
| File | What it is |
|---|---|
| `orchestration/forward_record/card.md` | the function card: the words, the definition, why it cannot leak, the fields, what is open |
| `orchestration/forward_record/helper/forward_record.py` | the helper: `VERSION --python VENV [--update-data]` |
| `orchestration/forward_record/helper/test_forward_record.py` | 11 tests (no backtest: the runner is replaced by a fake) |
| `orchestration/forward_record/v4/` | v4's record: `frozen.json`, `days.csv` (0 days), `record.md` |
| `orchestration/common_record/helper/common_record.py` | **a defect fixed** (below): one call, one test |
| `orchestration/README.md` | the function's line |
| `trading-bot/local_data/` (data, no code) | 25 portfolio coins' daily files extended to 2026-11-26 by the data tool, and `coverage.yaml` |

Nothing in `trading-bot/` code changed. One runner: the strategies are run by `common_record.backtest`.
What the helper depends on, by name: `common_record.backtest` and `common_record.commit`; step 4's `chart_files.py`
and the columns of `chart_bars.csv.gz`; `coins.portfolio_group()`, `coins.usable()`, `coins.dates()`;
`holdout_policy.check_windows_before`, `holdout_start_of`, `load_policy` (called in the venv);
`extend_kraken_daily.py --coins`. It reads the two returns with its own functions (`day_returns`,
`portfolio_and_holding`); it calls nothing of `update.py` or `combine.py`, so the other build's change of the holding
bar (A8, A10) does not reach it. The proof script (outside the repository) calls `combine.portfolio` and
`update.holding` by their current names.

## Findings of the build
1. **The shared runner was broken on the working branch.** `common_record.backtest` called step 4's `run_part` with
   the number of windows before the coin's first one; since data use 2 (the A4 join) `run_part` takes the list of the
   windows' numbers. Any new common record (step 9) or final test (step 12) stopped with `TypeError: 'int' object is
   not iterable`; the tests did not see it because their fake kept the old arguments. Fixed: the runner passes the
   numbers (the same `wK` as before); the fake takes step 4's arguments and a test checks them. Proof: proof A below
   (the runner's numbers equal the 131 existing records' on a whole window).
2. **The engine closes every position on a window's last bar.** In the first version of the helper, the last day of
   each update was written with that closing cost: on the scratch record, the day written by a 30-day update
   (-0.0334 %) was computed as -0.0208 % by the next update (the common record: -0.0208 %). Rule added to the card:
   the window's last day is not written; it enters at the next update. The record is one day behind the data.
3. **v4 has one hourly strategy** (weight 0.2), and the data tool extends daily files only (card, Open 2).
   `common/data_available.md` says the hourly files stop at the end of 2025; in fact 6 portfolio coins' hourly files
   go to 2026-11-17 and 10 stop at the end of 2025 (not corrected here: it is not this build's file).
4. **The holdout guard** accepts v4's forward window today and a window one month ahead; it refuses a window half a
   year ahead, with: "a protocol window's test.end is at or past the holdout_range start (dates withheld) -- a
   training window must never reach into the holdout range. [...]". So the record can be updated now, and an update
   will be refused later, when its days reach the frozen half-year (card, Open 1; the operator decides). I did not look
   for the day it starts.

## First entry: v4
`python3 orchestration/forward_record/helper/forward_record.py v4 --python VENV --update-data` (2026-11-27, about
22:10 UTC):
- the data tool: 25 coins, 9 days added to 15 files and 1 day to 10 (to 2026-11-26), every overlapping day equal;
  the 7 final coins' files not touched;
- "no forward day yet: the last complete day (2026-11-26) is not after the start day (2026-11-27)";
- `v4/frozen.json`: start day 2026-11-27, 11 strategies with their weights and fingerprints. The 22 plan and config
  files are identical to those of the version's commit (`git diff 210187f965 HEAD`: empty);
- `v4/days.csv`: the header, 0 days.

**What an update will add:** one line per complete day after 2026-11-27, the window's last day waiting. An update on
2026-12-28 (data to 2026-12-27) writes 2026-11-28 to 2026-12-26: 29 lines; the next one starts at 2026-12-27. The first
line can be written from 2026-11-30 (when 2026-11-28 and 29 are complete).

## Proof on past days (scratch records outside the repository; v4, a pretended start day)
The common records stop with the last research window (w32 of `research_2016.json`); no common record covers the 60
days before today. So the pretended start days are inside w32: the comparison needs days both have.

| Proof | Pretended start day | Days compared | Portfolio | Holding |
|---|---|---|---|---|
| **A**, the whole window (made before the last-day rule) | w32's first day | 122 | **122 of 122 equal** (largest gap 5e-11); total -0.860 % both | **122 of 122 equal**; total +3.526 % both |
| **B**, 60 days in two updates (30 days, then 60) | 61 days before w32's end | 59 (the 60th waits) | 0 of 59 equal to 1e-9; 51 of 59 within 0.0002 %, all within 0.02 %; total **-2.356 % against -2.365 %** | **59 of 59 equal**; total +18.178 % both |

Compared with `combine.portfolio` and `update.holding` on the common records (what `update.py` computes).

**B's differences, explained** (strategy by strategy, 15,360 coin-days):
- **Same positions in both records: 14,604 coin-days.** The returns differ by at most 0.0014 % (mean under 0.0001 %):
  the chart files keep 6 digits of an account's value, and the two accounts are at different values (the common
  record's started two months earlier).
- **Different positions: 756 coin-days.** The forward record starts flat on the start day; the common record carries
  what it held. 3 strategies differ only in the first 1, 4 and 16 days (4, 30 and 55 coin-days). One,
  `001-01...high-rsi-trend-continuation` (667 coin-days, to the last day), holds positions for weeks: on 76 coin-days
  one record is in a position and the other is not, on 591 both are in a position whose size differs by 0.04 % of
  the capital on average (I do not know the engine's exact rule there; the size follows the account's own history).
- The gap is in the first 10 days (0.005 % a day on average), then 0.00004 % a day.
- 7 strategies, the hourly one included, hold the same positions on every coin-day.

**An update only adds days** (B, with the rule): first update 29 lines; second update 30 lines added, the 29 earlier
lines byte for byte, the 29 earlier days computed again and **all equal** (0 different). Before the rule: 29 equal, 1
different (finding 2).

**Time:** 542 to 576 s per update on 4 cores (11 strategies x 25 coins), the same for 60 and 122 days.

## Tests
| Suite | Result |
|---|---|
| `orchestration/forward_record` | 11 passed |
| the cards (`pytest -q strategy_designer_v2/steps_cards`) | 236 passed; `topics/47_review/fold_rules_test.csv` restored |
| the bot (`cd trading-bot && pytest -q`), with the extended data | 1685 passed, 16 skipped, 75 deselected |

## Reading: which outcomes happened
| # | Expected | Happened |
|---|---|---|
| 1 | v4's record exists, zero days | yes |
| 2 | an update only adds days | yes, after a rule the run asked for (the window's last day waits) |
| 3 | the common records' numbers on past days | yes on a whole window (122 of 122); from a start inside a window, equal where positions are the same, the rest is the flat start (0.009 % over 59 days) |
| 4 | the guard accepts or refuses | accepts now; will refuse later (not worked around) |
| 5 | the final coins never read | yes (test); the data tool was called with the 25 portfolio coins by name |
| 6 | both suites pass | yes |

Named before and happened: the data tool cannot extend what one strategy needs (the hourly one). Not named before:
the broken runner, the closing cost of a window's last day.

## Untested
- A real forward update (a day after 2026-11-27 does not exist yet): the engine path was run only on past days.
- The guard's refusal on the real policy: seen through the guard's function on a far window, and in a test with a
  fake guard; no engine run was refused.
- A coin whose daily file ends before the others': the engine's refusal is expected ("the dates were not fetched"),
  not run here on daily data (seen for the hourly files).

## Open (for the operator; the card's Open has the detail)
1. **The frozen half-year:** an update will be refused when its days reach it. Stop there, or open those days to
   frozen portfolios only?
2. **The hourly strategy (weight 0.2):** extend the hourly files of BTC, ETH, LTC, XMR, XRP, ZEC? Possible from
   Kraken's public API **until about 2026-12-17** (it serves 30 days of hourly bars; the files stop on 2026-11-17).
   It is a change to the data tool. Without it the record is v4 without that strategy, and the days written stay so.
3. **How the monthly update is started.** Proposed, not built: **at the start of every batch**, where the data is
   already extended (`data_use.md`, section 2: "refreshed at the start of every batch"), before the runs' branches are
   made: one more command, about 10 minutes, and its commit (`days.csv`, `record.md`, the data files). By hand when no
   batch runs in a month. A schedule is not proposed: it needs a machine with the data, the venv and the right to push.
   It must not run while a loop runs on the branch (it commits there).
4. **The extended data files are committed on this branch** (25 daily files and `coverage.yaml`, a commit of their
   own, so it can be left out). Another branch that extends the same files will conflict on those lines.
5. **`run.md` in a forward engine folder** names the research windows file (the shared runner's fixed text, as in the
   final test's folders).
6. `NEXT_STEPS.md` (A9's status), CLAUDE.md's workflow paragraph and `common/data_available.md` are not touched: the
   designer's.
