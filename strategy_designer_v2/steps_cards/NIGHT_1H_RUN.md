# Night run on hourly bars (brief written 2026-11-18, before the run)

## Purpose
Do hourly bars give ideas that are real and pay after costs? The engine is now fast enough for hourly ideas (orchestration/duration/
8 and 9), step 4 runs any bar size, step 6 counts trades per day, and the gap rule ignores holes of up to one day on any
bar size (operator, 2026-11-18). Costs are the main enemy on hourly bars (15 to 25 bps a round trip): an idea must earn
more than that per trade.

## Three tracks, run at the same time (operator, 2026-11-18)
| Run | What | How |
|---|---|---|
| `retest_1h_run` | the 12 ideas confirmed and profitable on daily bars (UNSEEN_RUN.md), each unchanged but planned on 1h bars | `run_idea` on each, the idea's header set to `bar: 1h` (an operator's run decision, as `hourly_run` did); steps 3 to 7 and the unseen test as validated |
| `slow_1h_run` | a brief, from a theme: ideas read on hourly bars that trade rarely (positions held for days), so costs stay small | `run_brief --theme`, the brief's header `bar: 1h`, then its loop |
| `intraday_1h_run` | a brief, from a theme: effects within the day (time of day, moves within a day, short momentum or reversal) | `run_brief --theme`, `bar: 1h`, then its loop |

Default data: BTC, ETH, LTC, XMR, XRP, ZEC, folds A to D (24 windows), as every run. Budget: 200 USD in all
(operator, raised from 100: retest about 20, slow 90, intraday 90, each as its run's `--budget`). The three tracks run
at the same time (operator: parallel): model calls wait while backtests compute; the 4 cores are shared. Time is the
other limit: an hourly idea takes about 15 minutes to an hour alone (more with a long history), longer when shared.
Components: the loop calls the components step on its own; the operator also allows building one by hand when ideas
wait for it (the same step, its checks and proof).

## Before the run: the changes it relies on, proven (2026-11-18)
| Change | Proof |
|---|---|
| Speed (data read locally, table by columns, warm-up checked once, record per column) | identical files on 4 reruns each; 1h fold A 329 s -> 135 s alone (`orchestration/duration/9_data_and_table_proof.md`) |
| Step 4 on any bar size | the 4h probe runs; 4,380 bars equal the hourly data added by hand |
| Step 6 trades per day | 174 records rerun: 173 identical, the hourly one's trades per day changed, its status not |
| Gap rule: holes up to one day ignored | daily identical except XRP's 2-day hole of 2022-05 (w2 to w5 of a 19-coin record; w2 net return -0.55% -> 0); ZEC 1h fold A: 0% of hours blocked (was 47%) |

## Expected outcomes, fixed now
**Retest (12 ideas):**
- **A. Most hold** (8 or more confirmed by step 5 AND profitable by step 6): the daily edge holds on hourly bars.
- **B. Confirmed, not profitable** (most confirmed, few profitable): hourly bars add trades and costs, not edge.
- **C. Not confirmed** (most inconclusive or rejected): the edge is a daily-scale effect; settings on hourly bars test
  another thing (an RSI of 14 hours is not one of 14 days).

**Slow and intraday briefs** (counts of ideas tested, confirmed, profitable): few profitable is the expected outcome on
hourly bars because of costs; the slow brief should do better than the intraday one. Any idea confirmed and profitable
gets the unseen test on 2016-17 (no hourly 2026 data yet: that period reads "not fetched").

## What is not done
No merge into master; no change to a step during the run; nothing is tuned to the night's results.

## Journal of the night
- 00:12 UTC: the three tracks started.
- 00:26: the container restarted (every process stopped). Found then: the two briefs' first ideas mostly refused by
  step 3 as missing components (slow 5 of 5, intraday 4 of 6, 1 untestable); the intraday loop had called the
  components step, cut mid-build (`HoursToSettlementComponent`: its class and catalogue row written, its checks and
  proof not run, no index line). Undone (git), as the card says for an unfinished build: the wish stays open and is
  answered again.
- 00:28: restarted, the two briefs one after the other (two loops at once could build components into the same
  shared file together), the retest beside them.
- 01:14: the container had restarted again (up for less than a minute at the check-in; no activity after 00:28).
  Memory is not the cause (one coin's hourly step 4 call peaks at 368 MB, the machine has 15 GB). Both restarts came
  while the session was idle, with the night started detached (not a task the session tracks), while the day's tracked
  background tasks (an hour of timing, the proofs) ran through idle periods. Relaunched 01:16 as a tracked task (capped
  at 2 hours a launch; relaunched each time, every run resuming from its files).
- 02:09: running since 01:16 without a restart. Retest 1 of 12 done (inconclusive, not profitable); slow brief 9 ideas (7 of its 8 own ideas wait for components; 1 step 7 idea confirmed, not profitable); about 5 USD spent.
- 03:01: found that every components build of the night failed its proof (4 wishes "cannot build" after 3 attempts
  each): the proof's reference record (night_013 momentum in uptrends) was made before the 1-day gap rule, which
  changes the hole's label in 2 of its files (XRP w2, w3 metrics; bars and trades identical). Builds stopped, the bot's
  files restored; reference refreshed with the current code (exactly those 2 files changed); the 4 wrong answers
  removed from the index (the wishes open again). Also found: the loop crashed after a components call ended in
  failure (`failed()` read that line as an idea's turn); fixed, with a test. The two briefs paused; the components step
  run by hand on their 12 open wishes (operator's go), then the briefs resume.
- 03:16: the night's tracked task stopped at its 2-hour cap (the tool's limit; not to be relaunched as is), mid retest idea 4. From now on one tracked task per retest idea (each well under the cap); the briefs resume after the components step. Retest idea 3 (momentum inside golden-cross uptrends) on 1h: confirmed (t +7.19), profitable enough, holds on 2016-17.
- 03:5x: components step done on the 12 wishes: 8 built (HoursToSettlement, HourOfDay, five move/volume concentration classes, a VolumeRatio setting), 4 exist; 2.96 USD. Four of the five concentration classes are one measure (parked). Committed; the briefs resume.
