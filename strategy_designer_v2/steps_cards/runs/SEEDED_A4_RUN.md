# Seeded run A4 (2026-11-27): the three pieces the pilot never reached, on real data, with no model call (written before the run)

**The operator (2026-11-27, "Ok go"):** next steps A12, part 4. Proof session, branch `seeded-a4` from the working
branch at 26b53af8185. **Evidence only: never merged; a portfolio version it writes is not a version of the portfolio.**

## Purpose
The pilot (`PILOT_A4_RUN.md`) confirmed no idea, so three pieces of the new chain "did not occur". Show each on real
data, in one run in data use 2 (`seeded_a4_run`), through `run_idea`, with no model call:
- **(a) Steps 9 and 10:** a confirmed and profitable strategy gets its common record, then `update.py` is called.
- **(b) B12:** a confirmed strategy failing 3 or more of step 6's measures gets no 7.d call (one failing 1 or 2 would).
- **(c) The direction check:** step 5's check of a confirmation on the check half (the windows from 2022).

## Method
1. `orchestration/loop/seeded_a4_run/data_use.json` written by `common/coins.py`'s `new_data_use` (the function
   `run_brief --data-use 2` uses): 8 coins drawn by the run's name, the 32 windows.
2. **Strategy S (strong):** confirmed and profitable in its own run, and on its common record (25 coins) with room.
   Seeded: its plan and config, step 7's index lines (and 7.g's outputs). **Not seeded: its verdict.** `run_idea`
   cannot pass `--measure`, so steps 4 and 5 are run by their own helpers on the run's folders first (step 5 with the
   plan's stored `measure.py`, as `common_record` does), then `run_idea` finds their outputs and goes on.
3. **Strategy W (weak):** confirmed in its own run, failing 3 or more of step 6's measures there. The same seeding,
   but nothing for line 7.d: its entry condition is evaluated for real. Step 6 is read before `run_idea`: if W fails
   2 or fewer measures on the new data, 7.d would call the model, so another W is taken.
4. `run_idea` on S and on W; then the files are read.

## Expected outcomes
| # | Outcome | Shown by |
|---|---|---|
| E1 | The three pieces work | S confirmed, the direction check stated on the check half, profitable on the run's coins; then `common_record` called and its record written on the portfolio coins; then `update.py` called (a version v5 if the list of candidates changed, or its line says why not); no unseen test. W: 7.d "not run" with the count of failed measures; no model call |
| E2 | S is not confirmed or not profitable on the run's 8 coins | steps 9 and 10 rightly not called; a second strong strategy, then a third; each reported. None passing is a finding about the drawn coins |
| E3 | A step fails or is called in the wrong order | the journal's lines |

Also reported: the coin-windows run and not run in S's step 4 record, with their reasons; the direction check's text;
the common record's line; what `update.py` printed; every file the three pieces wrote.

## What was done
(2026-11-27, 22:05 to 23:30 UTC; branch `seeded-a4`, pushed, not merged. Engine time only: 0 model calls, 0.00 USD.)

1. **The run's data use:** `orchestration/loop/seeded_a4_run/data_use.json`, by `coins.new_data_use` (what `run_brief
   --data-use 2` writes). Drawn: XRP, TRX, ZEC, CRV, FIL, TAO, PEPE, BTC.
2. **S:** `023-01...b1_range-top-continues-in-risers_1d` (night4_range_run; its common record there: Sharpe 1.56, minus
   holding 0.50, Calmar 2.08). Seeded by `runs/seeded_a4/seed.sh`: plan, config, the six step 7 index lines, 7.g's
   outputs. Steps 4 and 5 run by their own helpers (step 5 with `--measure`, the stored `measure.py`), then `run_idea`.
3. **A defect met, and its fix taken in.** First call of `run_idea` on S: step 9 failed after 436 s (journal:
   `common_record`, "called: its helper failed (exit 1)"; log: `TypeError: 'int' object is not iterable` in step 4's
   `run_part`). The run went on, and step 10 was rightly not called (no record). The designer sent the fix during the
   run: commit db0ebd2c132 of `build-a9` (`common_record.backtest` gives `run_part` the windows' numbers; 2 files under
   `steps_cards/`), cherry-picked here (3e8418c5c3f) when nothing was running; its 12 tests pass. `run_idea` called
   again on S: every step done was skipped, step 9 and then step 10 ran.
4. **W:** twelve weak strategies (confirmed in their own run, 3 or more measures failed there) taken through steps 4,
   5 (`--measure`) and 6 by the helpers, until one was confirmed and failed 3 or more on the run's coins:

   | Result on the run's 8 coins | Count | 7.d's entry rule, evaluated in code |
   |---|---|---|
   | not confirmed (4 inconclusive, t 1.36 to 1.92; 3 no effect) | 7 | not met (step 5) |
   | confirmed, 1 or 2 measures failed (holding; holding and Calmar) | 4 | **met: 7.d would call the model**, so not given to `run_idea` |
   | confirmed, 3 measures failed | 1, the eleventh tried | not met: this is W |

   (12 tried: W is one of the 5 confirmed.) **W:** `013-01...g1_heavy-volume-precedes-gains_1d` (volume_run). Seeded
   as S, with nothing for line 7.d. Then `run_idea`. The eleven others' files were removed from the run's folders
   (they never went through `run_idea`).
5. Committed: the run's small files (plans, verdicts, checks, `run.md`, chart files, the common record's result, v5,
   the register, the journal and table). The per-window files stay on the session's machine.

## Reading
**Outcome: E1, after one E3** (step 9's failure on the first call, a known defect, fixed by db0ebd2c132). The three
pieces work on real data, in the order the card says, with no model call.

| Piece | Seen | From the run's files |
|---|---|---|
| (c) The direction check | yes | S: "confirmed" (t +3.48, 1746 cases). `verdict.md`: "Direction check on the check half (2022 onward) (the years step 7 does not explore): agrees: main measure +0.001046 on the check half (2022 onward) against +0.001227 on every window" (t 2.31 there, 996 cases). W: agrees too (+0.002076 against +0.002432) |
| S profitable on the run's coins | yes | 6 of 6 measures: Sharpe 1.24, minus holding 0.33, Calmar 1.00 (bar 0.75), lowest with one window left out 1.09 |
| (a) Step 9 | yes | journal `common_record`: called, 1368 s. INDEX line: "25 of 25 coins, 458 coin-windows; step 5 confirmed (main 0.0011149770203824115); step 6 profitable enough (Sharpe +1.56, minus holding +0.50, Calmar +2.08); 1368 s" (step 5's t there: 5.37) |
| (a) Step 10 | yes | journal `portfolio_update`: called after step 7, 97 s. It printed: "update: v5 built; ready for the final test (Sharpe 1.914, holding 1.075)" |
| No unseen test | yes | no `unseen_test` line in the journal, no `orchestration/unseen_test/seeded_a4_run/` |
| (b) B12 | yes | W: confirmed (t +5.20), "not profitable enough (failed: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar)". Journal `step7_7.d`: "called: not run: entry condition not met (step 5: confirmed; step 6: not profitable enough; 3 of step 6's measures failed, at most 2)", 0.1 s, 0 model calls. The other half (1 or 2 failures gets the call) is seen only by the entry rule in code, on 4 strategies: no model call was allowed here |
| Order | yes | S: 3, 4, 5 (skipped: done by the helpers), 6, chart files, 9, similarity, the step 7 lines, 10. W: no step 9, no step 10 |

**S's step 4 record: 149 of 256 coin-windows run** (the pilot: 119 and 103). 105 left out by the data use (104 "the
coin's first 90 days", 1 "a hole of 2 days": XRP w20); 2 not run by the engine ("the dates were not fetched": CRV, PEPE,
their first window after the 90 days). Per coin: BTC 32, ZEC 28, XRP 26, TRX 18, CRV 16, FIL 16, PEPE 8, TAO 5.
More than the pilot because this plan has no market-profile detector, so no long warm-up.
**The common record: 458 coin-windows run**, 8 not run ("the dates were not fetched", each coin's first window after
its 90 days: BCH, ATOM, ALGO, DOT, CRV, LDO, GRT, PEPE).

**Findings, for the designer:**
1. **v5 is not a new candidate: it is the same strategy counted under another run.** The register holds one book per
   plan id: the seeded run's book replaced `night4_range_run`'s. v5 lists 131 candidates like v4 (1 in, 1 out), the
   same 11 books, the same Sharpe. A side effect of seeding an id that exists; a real run writes new ids. The rule
   "a version when the list changed" did what it says. v5 and the register's changes are evidence only.
2. **Step 9 took 23 minutes here** (4 cores, with a trial backtest running beside it) against about 9 in the shards.
3. **On these 8 coins, a confirmed strategy with a far book is rare:** of 5 weak strategies confirmed, 4 failed only 1
   or 2 measures (always holding, then Calmar); the 7 not confirmed all had t below 2. Small sample; not a result on B12.
4. W's seeded step 7 lines carry their old words ("step 5: mismatch", from volume_run): seeding, not a fault.

**Files the three pieces wrote** (paths from `steps_cards/`; R = the strategy's id):
- (c) `05_verification/seeded_a4_run/verdicts/R/` (`result.json` with `direction_check`, `verdict.md`, `measure.py`,
  `size.json`), its INDEX line.
- (a) step 9: `04_backtest/seeded_a4_run/common/backtests/R/` (`run.md`, `config.json`, the chart files; per coin and
  window files, local), `05_verification/seeded_a4_run/common/verdicts/R/`, `06_profitability/seeded_a4_run/common/checks/R/`,
  `orchestration/common_record/seeded_a4_run/R.json`, one line in `orchestration/common_record/INDEX.md`.
- (a) step 10: `orchestration/combine/portfolios/v5/` (`boxes.csv`, `portfolio.json`, `measures.json`), one line in
  `portfolios/INDEX.md`.
- (b) `07d_not_profitable/seeded_a4_run/INDEX.md` (W's line; no analysis folder).
- The run: `orchestration/run_idea/seeded_a4_run/` (`journal.jsonl`, `table.md`, `table.json`; `logs/`, local).

**Not tested:** 7.d really called on a close book (a model call); a version built from a truly new candidate; step 11
on a version that differs; a disagreeing direction check.

**Step back:** the chain's last three pieces work. The one change a practitioner would make before the next batch:
merge db0ebd2c132, without which every candidate's common record fails in a data use 2 run.

(Copied to the working branch by the designer, 2026-11-28: the record only. The run's files, its portfolio v5 and its register changes stay on branch `seeded-a4` at 28fb177d760, evidence only, never merged.)
