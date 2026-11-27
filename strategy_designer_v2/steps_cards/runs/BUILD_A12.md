# Build A12, parts 1 to 3 (2026-11-27): a run is given data that exists, and its box is held by the idea itself

**The operator (2026-11-27, next steps A12): "Ok go"** for the pilot's four fixes; this build is parts 1 to 3 (part 4, the
seeded run, is branch `seeded-a4`). Branch **`build-pilot-fixes`**, from the working branch at 26b53af8185; **not merged**.
The reading that asked for it: `PILOT_A4_RUN.md` (its four defects).

## Purpose and expected outcomes (the designer's brief, set before the build)
One question: **do the three rules below hold on the pilot's own files, and is every other run unchanged?**

| # | Part | The rule | Expected |
|---|---|---|---|
| 1a | Usable windows | a coin's window is used when it starts after the coin's first 90 days **and** the coin's data covers the warm-up the wrapper will load for the plan; else left out before any engine call, with its reason; one rule in steps 4, 9 and 12 | on two pilot plans rerun: the same windows run as in the pilot with identical numbers; 0 failing for dates or warm-up; every window not run listed with its reason |
| 1b | The draw | a portfolio coin is drawable when testable on at least half of the check half's windows (7 of 14) with the profile detector's warm-up; one coin per category that has one, the rest among all | 19 drawable of 25, in 6 categories (to reproduce or correct); the draw for 5 run names with its usable coin-windows of 256 (the pilot: 119 and 103) |
| 2 | The side | an idea states its side (`side: long`, `short` or `both`); `in_box` and B13 read the idea's side | prompts of steps 2 and 7 without a box differ only by the side line; B13's counts for three boxes (before: 52, 8, 8); which of the pilot's 12 taken and tested ideas would still be taken |
| 3 | The brief's instruments | in a run with `data_use.json`, written by code from the run's research coins; no final coin in a file step 1 writes | a test; without `data_use.json`, step 1 byte-identical |
| all | | a run without a box and without `data_use.json` gives the same files as before | a seeded `run_idea` run, old code against new, the allowed differences named; both test suites pass |

**Outcome: the rules are built and proven, with three results the brief did not expect** (each is a question for the
operator, under "Open"):
1. **Part 1a runs 107 windows, not the pilot's 119**, on each of the two plans: the 12 others ran in the pilot with half
   the warm-up, which the engine accepts on some coins and not on others. The rule as written asks the whole warm-up
   of every coin.
2. **Part 1b's draws give 114 to 123 usable coin-windows of 256** (the pilot: 119 and 103): no window fails any more,
   but a run does not get more data, because most of the 256 are windows before the coins existed.
3. **Part 2: a boxed run now takes 0 earlier ideas** in each of the three boxes (before: 52, 8, 8): no idea written so
   far has a side line, and none of their briefs says "long only" or "short only".

## The files
**Shared files touched** (every one is in `strategy_designer_v2/steps_cards/`; nothing in `trading-bot/` or
`strategy-research/` is changed):
| File | What changed |
|---|---|
| `common/data_use.md` | 1.2 the draw among drawable coins; 1.3 a drawable coin; 1.4 the limit measured (9 coins before 2022); section 3: the usable-window count, the warm-up row |
| `common/coins.md` | the research draw, the drawable table |
| `common/coins.py` | `left_out` (the warm-up reason; reads the coin's days only); `warmup_start`, `plan_warmup`, `detector_warmup`, `warmup_days`; `check_half`, `testable`, `testable_counts`, `draw_need`, `drawable`; `research_draw(run, drawable)`; `new_data_use(run, python)` (keeps the draw's count) |
| `common/idea_definition.md` | one bullet: an idea states its side (pasted into the prompts of steps 2 and 7) |
| `common/target_box.md`, `common/target_box.py` | "The idea's side"; `idea_side`, `brief_file`; `in_box` and `box_ideas` read it; the theme note asks for the `side:` line. `brief_side` (the old reading) is removed |
| `common/lib.py` | `side_name`, `IDEA_SIDES` |
| `04_backtest/helper/run_backtest.py`, `card.md` | `--data-use`: the plan's warm-up asked once, passed to `left_out` |
| `orchestration/common_record/helper/common_record.py`, `card.md` | `coin_windows` and `backtest`: the same count, step 4's words in `run.md` and on the index line. **`backtest`'s name and arguments are kept** (`backtest(plan, python, dest, windows, coin_list, usable=coins.usable)`), for step 12 and `forward_record`; one optional argument is added last (`data=None`: the folder of the daily files the count reads) |
| `orchestration/combine/helper/final_test.py`, `test_update.py` | step 12: one line passes its data folder to `backtest` (`data=data`), so the whole count reads the folder its 90-day rule reads; one test follows `coin_windows`' new answer (the windows' numbers and the reasons). `build-a8-a10` does not change `final_test.py`; it does change `test_update.py` (other tests): a conflict there is possible at the join |
| `orchestration/run_brief/helper/run_brief.py`, `card.md` | the draw gets `--python`; step 1 is called with `--run` in a run with `data_use.json` too |
| `orchestration/loop/card.md` | `in_box` and B13 as now read (the code is in `target_box.py`; `loop.py` is unchanged) |
| `01_brief/helper/make_brief.py`, `card.md` | in a run with `data_use.json`: instruments by code, the model not asked for them, a final coin refused |
| `02_ideation/helper/make_ideas.py`, `system_prompt.md`, `card.md` | the `side:` line asked, checked, written in the idea file (the brief's side line is no longer copied into it) |
| `07_common/helper/analyse.py`, `output_one_call.md`, `card.md` | the `side:` line asked, checked, written; in a record with `data_use.json`, an idea's instruments and a discovery's "Seen on" are the record's research coins |
| tests | `common/test_coins.py`, `common/test_target_box.py`, and the helpers' tests of steps 1, 2, 4, 7, `common_record`, `run_brief`, `loop` |

Not touched, on purpose: the rest of `orchestration/combine/` (branch `build-a8-a10`), `topics/NEXT_STEPS.md` and
`PILOT_A4_RUN.md` (the designer's), `loop.py`, `run_idea.py`, step 3.

**A defect found on the way, fixed by part 1a:** since the join of 2026-11-27, `common_record.backtest` passed a
number where step 4's `run_part` expects the list of window numbers, so every real call of step 9 or step 12 would
have stopped with an error; its test replaced `run_part` with one that took the old argument, so it passed. The pilot
never reached step 9 (no candidate). `backtest` now passes the list; the test uses step 4's own argument. **The designer fixed the same call on `build-a9`
(commit db0ebd2c132; message received after this build had rewritten the function, so it was not cherry-picked):** its
added test (`test_the_runner_calls_step4s_run_part_with_its_own_arguments`) is copied here word for word; its one-line
fix is replaced by this build's call (the windows' numbers from the count). At the join the two branches will conflict
on that call and on the test's fake: keep this branch's side.

## Part 1a: usable windows, one count before the engine runs
**The warm-up asked, how it is computed.** The wrapper's number is `2 * strategy.required_bars` bars
(`trading-bot/core/launcher.py`, `run_backtest`, `warmup_prefetch`, which `run_protocol.py` always sets). The 2 is
written inline there: there is no function to call. So `coins.plan_warmup` asks the bot's own strategy class for
`required_bars` on the plan's config (in the venv, nothing run) and multiplies by 2 and by the bar's seconds
(`trading-bot/backtest/timeframe.py`). No 790 in the code: both pilot plans give 395 bars, 790 days.
**Proof that it equals what the engine asked:** every kept `manifest.json` records the first day the engine loaded.
It equals the window's start minus the computed warm-up (or the coin's first day when that is later) on **214 of 214**
manifests of the rerun and **238 of 238** of the pilot's two records; and the pilot's refusals say `required_bars=395`.

**The rerun** (step 4 on the pilot's plans 050-04 and 061-01, taken from `origin/pilot-a4-auto`, with that run's
`data_use.json`, in a scratch folder outside the repository; 2.6 and 4.3 minutes):
| | Pilot | Rerun, each plan |
|---|---|---|
| Coin-windows run | 119 | **107** |
| Left out, with the reason | 109 | **149** (109 the first 90 days; 40 the history shorter than the warm-up) |
| Refused by the engine ("dates not fetched", "engine stopped") | 28 | **0** |
| Total | 256 | 256 |
| On the 107 windows both ran | | **107 of 107 identical**: the row of `run.md` and the `core` block of `metrics.json` |

Per coin: BTC 32, DOT 11, FIL 11, GRT 10 as in the pilot; **XMR 22 (pilot 25), DOGE 13 (16), INJ 8 (11), TAO 0 (3)**.

**The 12 windows the pilot ran and the rule leaves out** (XMR w8 to w10, DOGE w17 to w19, INJ w22 to w24, TAO w30 to
w32): the engine does not treat every coin alike. For a coin whose file is recorded as Kraken's whole archive
(`coverage.yaml`: "from the pair's first trade"), it runs a window as soon as the coin has the needed bars once (395);
for a coin whose file is recorded from a date (DOT, GRT, FIL and the other 2026-11-26 files), it refuses until the
whole warm-up (790 days) is on file. The rule as the brief wrote it ("the coin's data covers the warm-up the wrapper
will load") asks 790 days of every coin: one rule, and 12 windows fewer here. See Open 1.

## Part 1b: the draw
**The count, reproduced with one correction.** With the detector's warm-up (395 bars asked from the bot's regime
engine on the detector step 3 builds; 790 days):
- **19 drawable coins of 25, in 6 categories**: as the designer counted. Not drawable: TAO 0 and ONDO 0 of 14, SUI 3,
  PEPE 3, NEAR 6, LDO 6. AI has no drawable coin.
- **331 usable coin-windows of 800** (the designer: 332), **465 by the 90-day rule alone** (466): the difference is
  XRP's w20, left out for a hole of 2 days (the hole rule, kept).
- **9 coins have a usable window before 2022**: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ZEC, XMR (written in
  `data_use.md`, 1.4, with what it means for the analysts' half).

| Coin | Check-half windows testable (of 14) | All usable (of 32) | | Coin | Check | All |
|---|---|---|---|---|---|---|
| BTC | 14 | 32 | | ZEC | 14 | 23 |
| LTC | 14 | 32 | | XMR | 14 | 22 |
| XRP | 13 | 20 | | CRV | 11 | 11 |
| BCH | 14 | 20 | | AAVE | 10 | 10 |
| ETH | 14 | 26 | | INJ | 8 | 8 |
| ADA | 14 | 17 | | *LDO* | *6* | *6* |
| ATOM | 14 | 15 | | *ONDO* | *0* | *0* |
| ALGO | 13 | 13 | | FIL | 11 | 11 |
| TRX | 12 | 12 | | GRT | 10 | 10 |
| DOT | 11 | 11 | | *TAO* | *0* | *0* |
| AVAX | 7 | 7 | | DOGE | 13 | 13 |
| *NEAR* | *6* | *6* | | *PEPE* | *3* | *3* |
| *SUI* | *3* | *3* | | | | |

**The draw for 5 run names** (the seed is the run's name; the first 6 coins are one per category, the last 2 among the rest):
| Run name | The 8 coins | Usable coin-windows of 256 |
|---|---|---|
| `batch_b14_1_run` | BCH, ATOM, ZEC, AAVE, FIL, DOGE, CRV, DOT | 114 |
| `batch_b14_2_run` | XRP, ETH, ZEC, AAVE, GRT, DOGE, AVAX, TRX | 121 |
| `batch_b14_3_run` | LTC, TRX, XMR, AAVE, GRT, DOGE, ALGO, FIL | 123 |
| `seeded_a4_run` | XRP, DOT, ZEC, AAVE, FIL, DOGE, BCH, AVAX | 115 |
| `night10_fallingcalm_run` | XRP, TRX, XMR, AAVE, FIL, DOGE, ZEC, AVAX | 118 |
| *the pilot's names, drawn again (for comparison only: those runs keep their coins)* | `pilot_a4_auto_run`: BTC, ATOM, XMR, CRV, GRT, DOGE, XRP, ADA; `pilot_a4_named_run`: BCH, ADA, ZEC, INJ, GRT, DOGE, XRP, CRV | 140; 122 |
| **the pilot, as run** | BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL | **119 and 103** (107 for run 1 by the new count) |

**What this shows:** the draw stops the failures and the nearly empty coins (TAO: 3 windows), but **a run still stands
on about 120 coin-windows of 256**: the 19 drawable coins hold 16 usable windows each on average, of 32. DOGE is in
every run (the only drawable meme coin); the infrastructure coin is FIL or GRT (10 or 11 windows). See Open 2.
A run already started keeps its coins: `start_data_use` returns the existing `data_use.json` and makes no draw (a test).

## Part 2: the side is read on the idea
**The rule in one place:** `common/target_box.md`, "The idea's side", and `common/idea_definition.md`. An idea's side
is its own `side:` line; for an idea written before the line, its brief's "long only" or "short only"; else unknown.
`in_box` and B13 use this one reading (`target_box.idea_side`).

**Step 3 keeps one rule, the brief's:** step 3 caps the book to the brief's "long only" or "short only", by code
(`add_side`), and does not read the idea's side (it is not among the idea fields step 3's model is given, so step 3's
prompt and plans are unchanged). The brief limits what is traded; the idea says what it bets; a mismatch is visible
(`in_box: false`, a flat book), not refused.

**The prompts without a box** (`build_a12/prompts_before_after.py`, result in `prompts_before_after.txt`): step 2 and
each of the six step 7 lines gain **4 lines and lose none**: the definition's bullet (3 lines) and the output line
`side: <what the idea bets: long, short or both>`. The code that builds their requests is identical.

**B13 on today's files** (the working branch's ideas; `target_box.box_ideas`, old code against new):
| Box | Taken before | Taken now | Why the others are not |
|---|---|---|---|
| falling calm, long | 52 | **0** | 52: side unknown (no `side:` line, and their briefs have no side line) |
| rising agitated, short | 8 | **0** | 8: side unknown |
| rising agitated, long | 8 | **0** | 8: side unknown |

**The pilot's 12 taken ideas that were tested: none would be taken now** (run 1: 032-01.b1, 032-02.b1, 050-02, 050-03,
050-04, 060-02, 061-01, 064-01, 077-01; run 2: 036-02.g1, 041-01.b1, 064-02): all 12 have an unknown side. That
includes the 6 the pilot's reading named as on the wrong side, and 6 that may have been on the right one. In the
pilot's journals `in_box` said true on 13 and 10 turns and false on none. See Open 3.

## Part 3: the brief's instruments in the new data use
- **The rule:** `01_brief/card.md`. In a run with `data_use.json`, `make_brief.py --run`: the `instruments` key is
  taken out of the model's header keys, one note says the coins are chosen by the workflow, the header's instruments
  line is written by code (the run's research coins), and an answer naming a final coin (as a ticker) is refused and
  asked again. `run_brief` passes `--run` for the run's brief and for discoveries' briefs.
- **Where brief 087's coins came from, fixed there too:** the discovery it was written from said "Seen on: 1d bars of
  BTC, ETH, ..., LINK, ..., UNI, ..., SOL, ..." : the tested plan's coins (an idea taken from an earlier run, on 19
  coins), not the 8 the backtest ran on. Step 7 now names the record's research coins in a record with `data_use.json`.
- **Tests** (`01_brief/helper/test_make_brief.py`): the instruments by code and no final coin in any file written; a
  theory naming any of the 7 final coins: no brief written; without a data use, the call and the files as before.
- **Byte-identical without `data_use.json`:** old `make_brief.py` against new, the model replaced by a fixed answer:
  system prompt, request and the two files written are identical, with no `--run` and with `--run` of a run that has
  neither a box nor a data use (`prompts_before_after.txt`, last lines).

## For all three parts
**A run without a box and without `data_use.json`: the same files.** SEEDED_RESULT

**Tests.** TESTS_RESULT

## Open (for the operator)
1. **Half a warm-up or a whole one?** The rule built asks the whole warm-up of every coin (790 days for a plan naming
   a profile). The engine accepts half of it (395 days) on the coins whose file is recorded "from the first trade", and
   that gave the pilot 12 more windows of 119 (a year more of XMR, DOGE, INJ; TAO's only 3). Asking half of every coin
   would be one rule too, and would give every coin a year more, but the engine refuses it today on the 2026-11-26
   coins (their files are recorded from a date); making it accept is a change in `trading-bot/` (or in how those
   files are recorded), the operator's go. **Recommended: keep the whole warm-up now** (no shared change, nothing
   fails), and decide the half as a topic. The 118 common records made before hold those extra windows; not rerun.
2. **A run still has about 120 coin-windows of 256.** The draw cannot give more: most coins start after 2019. More
   data per run means more coins per run, or a shorter warm-up (Open 1), not another draw rule.
3. **B13 takes nothing until ideas carry a side.** The 68 earlier ideas naming these three boxes have no known side.
   If the operator wants them back: one pass that states the side of each untested idea (a model call per idea, or by
   hand), written as their `side:` line. Not built: not asked.
4. **An idea's `side: both` is never in a box** (a box has one side). An idea that bets both ways in the box's profile
   is counted outside and not taken.
5. **Final coins are still named in older files a model reads:** 65 of the 211 lines of step 1's index (pasted into
   every step 1 call) and `common/data_available.md` (step 7's "same idea on other data": SOL, UNI, LINK) come from
   the old data use. New briefs in a data-use run name none. A clean-up list, if wanted.
6. **The count reads the daily file's dates** for every bar size (as the 90-day rule did): an hourly plan on a coin
   whose hourly file starts later than its daily file can still be refused by the engine. No hourly run is in the
   new data use yet.
7. **A brief given as a file** (`run_brief BRIEF_FILE --data-use 2`) keeps the instruments line its author wrote: only
   step 1's briefs are written by code. The backtests run on the run's coins all the same.
8. **Untested on real data:** no model call was made in this build. The `side:` line as steps 2 and 7 will write it,
   and a boxed run's brief with instruments by code, are first seen in the next run.
