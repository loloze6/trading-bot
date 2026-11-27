# Build A4, part 5: portfolio versions by rule, readiness, the final test (2026-11-26, night 9)

Session session_012maTgXAtxsdTfut9XYn1TR, branch `build-a4-portfolio` from 80957b2e84. The operator's go on
`common/data_use.md` (2026-11-26); its build plan, part 5: steps 10 to 12.

## Purpose and expected outcome (written before the build)
- **Purpose:** no person builds or judges a portfolio version any more: a version is built when the list of
  candidates changes (step 10), it is ready when it beats holding its coins (step 11), and the final test is made once
  per final group (step 12).
- **Expected:** `update.py` builds `v3` from hand-made common records and nothing when the list is unchanged or empty;
  `final_test.py` refuses a version that is not ready and a used group, writes its record before it runs; with no
  common record on disk (tonight), every default path gives the same files as before; both test suites pass. No final
  test is run tonight; `trading-bot/` is not changed.

## What was built
| File | What |
|---|---|
| `orchestration/combine/helper/update.py` (new) | steps 10 and 11: the candidates (paying books with a common record), compared with the last version's `candidates`; when they differ, `v<n+1>` by the card's rules 1 to 5 on the common records (boxes, admission, families, correlation on the common records' daily returns, 1 ÷ n); measured against holding the same coins, equal weight, the same days; `ready` in `measures.json` and in INDEX.md's new table |
| `orchestration/combine/helper/final_test.py` (new) | step 12: refuses unless `ready` and no record for the current final group (`final_tests/final_XLM-SOL-DASH-UNI-LINK-FET-SHIB.json`); writes that record first (status `started`); runs each strategy's plan unchanged, one step 4 call per final coin (`--coins C --windows`: the windows of `research_2016.json` past the coin's first 90 days, as step 9), then chart files; the portfolio at the version's weights against holding; go when Sharpe > 0 and > holding's |
| `orchestration/combine/helper/combine.py` | `choose` takes the correlation rule as an argument (default: the register's research returns, as before) |
| `orchestration/run_idea/helper/run_idea.py` | after the unseen test, only when `orchestration/loop/<run>/data_use.json` says `"version": 2` and the idea's common record exists: one step `portfolio_update` (`update.py`) |
| `orchestration/night_merge/helper/night_merge.py` | at the end, after the register's rebuild: `update.py`; a version it writes goes in its own commit |
| cards | `combine/card.md` (steps 10 to 12, the bar, the final test, what `judge_unseen.py` becomes), `run_idea/card.md`, `night_merge/card.md` |
| tests | `combine/helper/test_update.py` (8), one in `run_idea/helper/test_run_idea.py` |

## Proofs
| Proof | Result |
|---|---|
| a changed list builds a version (hand-made: 2 paying books with common records, 1 confirmed only) | `v3` after `v2b`, 2 candidates, 2 books; the old table of INDEX.md kept byte for byte, a second table added |
| an unchanged list builds nothing | second call: "the list of candidates (2) is that of v3"; INDEX.md byte-identical |
| a third candidate | `v4`, 3 candidates |
| no candidate (no common record; a confirmed-only book) | nothing written: INDEX.md byte-identical, the folder's file list unchanged |
| ready / not ready | a book earning 0.2 % a day on noise: ready, Sharpe above holding's, the same number of days; a book of half the coin's move less a cost: admitted (it earns), not ready |
| holding | equals the mean of the two coins' close-to-close returns, day by day, 1,499 days |
| final test refusals | `v3` not ready: refused; `v2b` (no `measures.json` by rule): refused; after a test on `v4`: refused ("already made"); a test that fails half-way leaves status `started` and the group used |
| the record before the run | the fake step 4 read the record at every call: status `started` each time; at the end `done`, `go`, the result, `final_test` in `measures.json`, the INDEX cell |
| the final windows | step 9's windows past each coin's first 90 days: a coin from 2014 keeps all; a coin from 2020-06-01 starts at 2020-09 |
| `update.py` on this repository (no common record exists) | "no candidate has a common record: no version"; INDEX.md md5 unchanged (8474138c…), nothing written |
| `combine.py` default path, the old and the new code on the same inputs (this machine's register and records) | `measures.json` identical; `portfolio.json` identical but its version name and time; its 10 books and weights identical to `v2b`'s (the scratch versions removed after) |
| `run_idea` without `data_use.json` | the new step is not called (`data_use_version` is None: test); no rerun of a real idea was made |
| cards' tests | 184 passed |
| bot's tests (`cd trading-bot`) | 1677 passed, 16 skipped |

## Not done, untested, for the merge
- **No final test was run** (as asked); `final_test.py`'s step 4 calls (`run_backtest.py --coins C --windows FILE`,
  the 32 windows per coin) were not run on real data: untested on the engine, hourly books included.
- **Order in `run_idea`:** the update is placed after the unseen test, where part 4's common record is expected; at
  the merge of `build-a4-common`, the update must come after its step.
- **Step 12's days, settled by the designer (22:52 UTC):** the 32 windows of `research_2016.json`, per coin only those
  whose start is past its first 90 days, as step 9 (one kind of record for steps 11 and 12). `final_test.py` changed
  so (commit after 747c53cede; test: a coin from 2014 keeps every window, a coin from 2020-06-01 starts at the window
  after its 91st day). Its windows are numbered w1.. per coin, where part 4 keeps the file's numbering; **at the merge,
  `final_test.run_book` becomes one call to part 4's `common_record.backtest(..., coin_list=coins.FINAL)`**.
- **The common record's json is written last** (after steps 4 to 6, part 4's answer): requiring both files, as
  `update.py` does, reads only finished records.
- `combine.py`'s in-sample Sharpe on this machine reads 2.18 where `v2b` says 2.055 (the same books and weights): the
  records on this machine, not this change (the old code gives the same 2.18).
- `trading-bot/` not changed; `campaign_data_policy.yaml` and `local_data/holdout_sealed/` not touched.
