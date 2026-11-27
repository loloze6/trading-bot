# Night 9 (2026-11-26): data-first briefs aimed at the empty boxes (written before the runs)

**The operator (2026-11-26, about 23:00 Paris):** "this night would be launched soon ... continue research workflow
during the night (300 budget) with research workflow completion around 9am tomorrow morning"; earlier the same day, in
the night 8 review: B2 option a ("a run starts from a target box, explored in the data, not from a theme the designer
writes"). Standing rules: `NIGHT_RULES.md`.

**Nothing changed in the steps since night 8** (the theme rule of `common/theme.md` was taken by 5 sessions during
night 8; `night_merge`'s fix and the combination's judge run in the morning only): no pilot is needed (NIGHT_RULES,
before the night, 3). B2's own entry (a run started from a box) is not built yet; tonight takes its idea with what
exists: each session starts from **briefs written by the analysts from the data** (night 8's line 7.g discoveries,
written as briefs and never run), chosen for the boxes the portfolio lacks. No brief is written by the designer.

## Purpose
One question: **do briefs found in the data, aimed at the empty boxes (choppy agitated; the short side in falling calm
markets), give confirmed and profitable specialists there, where the designer's themes of night 8 gave none?**
The map before the night (combination v2b, 10 strategies): choppy agitated empty on both sides; falling calm short 3
strategies, none a specialist; the one short specialist is in falling agitated (night 8, C's 060-01.g1.d2.d1).

## Sessions
| Session | Run | Target box | Briefs (each a night 8 discovery, its file in `01_brief/<night 8 run>/briefs/`) | Budget |
|---|---|---|---|---|
| A | `night9_chopagishort_run` | choppy agitated, short | `night8_risingagitated_run/briefs/061_choppy-agitated-high-close-fades.md` | 42 USD |
| B | `night9_chopdeep_run` | choppy, short | `night8_risingagitated_run/briefs/072_choppy-deep-below-high-falls.md` | 42 USD |
| C | `night9_chopmonth_run` | choppy, both sides | `night8_choppyagitated_run/briefs/067_choppy-market-monthly-move-continues.md`, `night8_choppycalm_run/briefs/064_choppy-market-up-days-carry-one-way.md` | 42 USD |
| D | `night9_chopstretch_run` | choppy, both sides | `night8_risingagitated_run/briefs/067_choppy-average-stretch-carries-forward.md` | 42 USD |
| E | `night9_fallcalmfade_run` | falling calm, short | `night8_risingagitated_run/briefs/070_falling-calm-run-break-fade.md`, `night8_risingcalm_run/briefs/064_falling-calm-scaled-rallies-fade.md` | 42 USD |
| F | `night9_fallcalmwide_run` | falling calm, short | `night8_choppycalm_run/briefs/060_falling-calm-wide-high-close-fade.md`, `night8_choppycalm_run/briefs/061_falling-calm-rally-next-day-fade.md` | 42 USD |
| designer | check-ins (the usage limit), the coin-data session, the morning merge and reading | - | - | 48 USD reserve |
| data | `data-coins` (no model call for research): the 20 coins of the coin card fetched from Kraken's archive, daily | - | - | 0 USD of research calls |

Each research session: on branch `night9-<name>` from the working branch; for a session with two briefs, the second
brief is added first with a tiny budget (`run_brief <brief 2> --budget 0.01`: step 2 runs, the loop does not start),
then `run_brief <brief 1> --budget 42` starts the loop on both briefs' ideas (one queue, one score). No new idea after
07:00 UTC (08:00 Paris); the runs end by about 08:30 Paris; the morning merge and reading follow.

## Expected outcomes (by the counts)
| # | Outcome | Shown by |
|---|---|---|
| N1 | Specialists in the target boxes | a confirmed and profitable strategy whose positions sit in its target box (10 % or more of its days, by `boxes.py`), the nearest held strategy explaining under 0.5 |
| N2 | Effects real, strategies not profitable | confirmed in the target box, none profitable (Calmar, as night 8's falling markets) |
| N3 | Not real | lines 7.b and 7.g answer "not in the data" on most briefs: data-first briefs do no better than night 8's themes |
| N4 | The machinery fails | a failed turn, a resume without `--budget`, a component not committed |
Also counted: each brief's answer and the turn and spend at which it was answered; the share of first ideas confirmed
(night 8's designer themes: brief first ideas confirmed 9 % of the time, 1g); the confirmed and profitable strategies by
box; the spend after each brief was answered.

## During the night (the designer's watch)
- **23:07 Paris, launched** (each from the working branch at cb0082585f): A session_012maTgUzR7xXwQD1YPANVoh, B
  session_012maTgU5oYFjQviY1WCoPbJ, C session_012maTgXQjABpAt28f1NaT6W, D session_012maTgWKHxciErKS8p8QxBx, E
  session_012maTgXZeByYDKaY7hNoCyZ, F session_012maTgXSHfqjCc58AZKxYqd; the data session session_012maTgYEHsvC54ogG22iB3h
  (branch `data-coins`). The designer's check-ins: 01:15, 03:30, 05:45 Paris; the morning merge from 08:15 Paris.
- **23:25 Paris, the data session ended** (branch `data-coins`, fc9d0121ec, report `runs/DATA_COINS_RUN.md`): 20 of 20
  daily files, read from Kraken's archive by byte ranges (about 2 MB; each member's checksum checked), then the public
  API to 2026-11-25; prices agree on the 664 days both sources cover. The 19 present files unchanged (checksums), the
  policy file untouched. Gaps: XLM misses 181 days (177 in a row, August 2017 to February 2018); DASH and ETC 1 day
  each; the others none. Odd: OCEAN still trades but is near-dead (median 16k USD a day in 2026); BCH's first day has a
  bad print. Finding: Kraken rebuilt its archive; against our BTC file the new edition differs on 8 days' highs (2013)
  and on volume for 1,083 days (at most 4.5 %); nothing changed. Two data tools gained options (defaults unchanged).
  For `common/data_use.md`: a liquidity rule (a coin left out of a window where it barely trades) to add; the 90-day
  rule covers BCH's first print.
- **23:30 Paris, the operator: "use the best of the tokens during the night, so feel free":** the build of
  `common/data_use.md` started tonight. The designer merged `data-coins` into the working branch (05020744fd), wrote
  `common/coins.md` (the universe: Kraken, 3 years, at least 100,000 USD traded a day, which leaves out STORJ, OCEAN,
  YFI, SNX, COMP, ETC, XTZ: 32 coins; the final draw, seed 20261126: XLM, SOL, DASH, UNI, LINK, FET, SHIB; the portfolio
  group the other 25), `common/coins.py` (the groups, the per-run draw, the 90-day rule; 3 tests) and the 32 research
  windows 2016-01 to 2026-08 (`04_backtest/windows/research_2016.json`). Three build sessions from 80957b2e84, each on
  its own branch, with fixed interfaces between them: part 3, the research run's coins and windows
  (session_012maTgXRa1jWmZqLrKEGSXH, `build-a4-research`); part 4, a candidate's common record
  (session_012maTgUMyP5tGx1A41UkuNs, `build-a4-common`); part 5, the portfolio versions by rule, readiness, the final test
  (session_012maTgXAtxsdTfut9XYn1TR, `build-a4-portfolio`). None changes what tonight's six research sessions run.
- **23:51 Paris, part 5 built** (`build-a4-portfolio`, 975ffd478e, `runs/BUILD_A4_PORTFOLIO.md`): `update.py` (a new
  version when the candidates with a common record change; ready when its Sharpe beats holding the same coins),
  `final_test.py` (refuses unless ready and the final group unused; writes its record before running; not run), the
  calls from `run_idea` (new mode only) and `night_merge`; 8 tests; on today's files it writes nothing (INDEX.md
  unchanged); cards 184 passed, bot 1677. For the merge: its call in `run_idea` after part 4's step; one runner for "one
  series per coin" with part 4; a "complete" field in the common record's json.
- **00:00 Paris, steps 9, 11 and 12 on the same 32 windows** (part 5 raised the mismatch with `data_use.md`'s "every
  complete day"; decided: one kind of record; the card corrected, 04c942cc8b; part 5 aligned, 066b0d0cff).
- **00:27 Paris, part 4 built** (`build-a4-common`, 1522e63, `runs/BUILD_A4_COMMON.md`): `orchestration/common_record/`
  (25 portfolio coins × 32 windows, from each coin's usable windows; step 5 by the plan's own measure, step 6); the call
  from `run_idea` (new mode only); `--register --shard i/n`; 7 tests; the default path: 1,853 of 2,127 files identical,
  the rest only run ids, times, paths. Measured: 881 s and 776 s per daily book; the engine's warm-up (not the 90-day
  rule) decides where a coin starts (375 of 466 coin-windows ran). First two records: 060-01.g1.d2.d1 on the common data
  step 5 inconclusive, step 6 not profitable (Sharpe 0.59, 0.35 below holding); 058-03.e1 confirmed and profitable
  (Sharpe 1.20, +0.25 over holding, Calmar 0.78). **00:28 Paris:** the 120 paying books in 6 shard sessions
  (`common-shard-1` to `-6`, about 5.5 h each; only the files the combination reads committed): session_012maTgTp2Ga59drvc8Q5nR6,
  session_012maTgXxFUnkNga346MP4P2, session_012maTgYGU794NAAhShSdrCg, session_012maTgXJVsLfJQ2ySu8vG52,
  session_012maTgTxq6gqHYWn9QXmiZy, session_012maTgWXAatuQQz9BBcw6f7.
- **00:47 Paris, part 3 built** (`build-a4-research`, eaf4e3f, `runs/BUILD_A4_RESEARCH.md`): `run_brief --data-use 2`
  writes the run's `data_use.json` (its 8 coins); `run_idea` alone decides the data (step 4 on the 8 coins and the 32
  windows, a coin left out of a window before its 91st day or with a hole over 1 day, counted); step 7 explores w1-w18
  (before 2022), step 5's direction check w19-w32. Proof: the default path, 602 of 818 files identical (the rest run
  ids, times, paths), the same verdicts; the new mode, a 3-idea run (3.80 USD) whose explorations show only 2017-2021.
  Cards 182, bot 1678 passed. For the merge: step 4's index line fixed ("ran" when any coin ran a window); a component
  built (ScaledMoveSmallnessComponent, standing go); `run_idea` must not call `unseen_test` in the new mode (its dates
  overlap the research windows). **All three builds done; the night's research and the 6 shards run on.**
- **01:20 Paris, first watch** (each branch as last pushed, 00:00 to 00:11 UTC): all 6 running, no failed turn, both
  briefs added in C, E and F. Tested 76 ideas, spent 93.3 USD; confirmed 22, profitable 4: B 074-01.g1.d1 (falling
  agitated, a wide close-high bounce fades: a night 8 effect again, off B's choppy box), E 074-01.b1.d2,
  074-01.b1.d1.d1, 074-01.b1.g1 (falling, a run-break up-day fades: on target, short). A: 3 confirmed on its theme
  (choppy agitated, a high close fades), none profitable yet; C: 4 confirmed (choppy, a weak month keeps falling); D: 0.
  **A fault of the set-up (the designer's):** the starting briefs carry night 8's `discovery:` line, so `select_next`
  (1n) counts their ideas as night 8 follow-ups several generations deep (F's 060 and 061: 5 and 6; C's: 7), and the
  night's own new discoveries (generation 1) rank above them: F's 061-01 untested, its turns on two discoveries (074
  rising calm rebound, 075 volume). Each session told to delete that line from its starting briefs' run copies (no
  code; the `source:` line keeps where they came from); for the record: when a run starts from a brief, the brief is
  generation 0 whatever its origin (next steps: `run_brief` drops it itself).
  **01:25 Paris:** all 6 sessions applied it (A db19a89694, B ad6485b7dd, C 8f4e67c, D d6c7df2, E cff147a547, F
  2daabb6488), no loop stopped; B's queue: its 072 ideas back at ranks 1 to 3 (score 0.1825 against 0.0338 next). All
  six had their 2-hour task cut around 01:10 Paris and resumed with `--budget 42`. Noted: E counts 12 backtested ideas
  (7 stopped at step 3, 2 untestable), 8 confirmed, 3 profitable, 074-01.b1.g1 holding on both unseen periods; C's
  brief 075 is named "falling agitated, monthly move reverses" but its discovery is a falling-calm slide that continues
  (a naming slip by step 1, for the reading).

## Reading
(written in the morning)
