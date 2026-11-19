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
- 04:37: no restart since 01:16. Retest 5 of 12 (2 confirmed, 1 profitable); slow brief resumed 03:49 on the unblocked ideas: 016-03 (a violent up move partly reverses) confirmed t +2.74, not profitable; 016-01 refused again by step 3 for a missing component although its wish was built (the loop puts it to the components step again). About 15 USD spent.
- 05:23: no restart. Retest 8 of 12: 5 confirmed, 1 profitable (6: volatility-scaled momentum t +2.33, 7: RSI side t +2.28, 8: rising-month weekly momentum t +3.65, failing only mean daily return and Calmar). Slow brief: its unblocked ideas inconclusive (t -1.92 to +0.68) except the violent up move (t +2.74); none profitable. About 20 USD spent.
- 06:11: no restart. Slow brief 13 ideas, 4 confirmed, 0 profitable; two step 7 ideas on the time of day strongly confirmed (late-UTC drift of volatile coins t +7.68, late-evening UTC rebound t +5.27, not profitable). Retest on idea 9 (the 19-coin idea, long). The slow loop is in a components call. About 23 USD spent.
- 06:50: retest idea 9 (the 19-coin nearness idea, the live bot's) on 1h: confirmed (t +5.29), profitable enough; on 2016-17 it does not hold (measure ~0, t -0.06; Sharpe 2.88 below holding's 4.14). Found: the unseen test read a period with no data (no hourly 2026 bars) as 'does not hold'; fixed to 'no data' (test, card), the two results recomputed (golden-cross: 2016-17 holds, 2026 no data; nearness: 2016-17 does not hold, 2026 no data). The run table's two rows are refreshed after the retest ends (no write beside a running idea).
- 06:57: no restart. Retest 9 of 12: 6 confirmed, 2 profitable (golden-cross momentum: holds on 2016-17; 19-coin nearness: does not). Slow brief 14 ideas: 4 confirmed, 0 profitable. About 27 USD spent.
- 07:44: retest 11 of 12: 7 confirmed, 2 profitable (11: momentum in uptrends confirmed t +3.83, failing only Calmar). Slow brief on turn 23 (a long-history backtest, 51 min so far). About 29 USD spent.

## Reading: retest (finished 07:55 UTC, 12 of 12, 15.3 USD)
| Idea (on daily bars: confirmed and profitable) | 1h: step 5 | 1h: step 6 (bars failed) | 2016-17 (new dates) |
|---|---|---|---|
| c1_high-rsi-trend-continuation | inconclusive (+4.74) | no (5 of 6: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar) | - |
| c1_high-rsi-uptrend-continuation | confirmed (+3.40) | no (5 of 6: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar) | - |
| b1_momentum-inside-golden-cross-uptrends-more-co | confirmed (+7.19) | profitable enough | holds |
| e1_short-horizon-uptrend-momentum-near-highs | inconclusive (+2.18) | no (5 of 6: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar) | - |
| g2_volatile-reversal-completes-quickly | inconclusive (+1.35) | no (5 of 6: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar) | - |
| g1_volatility-scaled-momentum-continuation | confirmed (+2.33) | no (3 of 6: Sharpe minus holding's Sharpe; Mean daily return; Calmar) | - |
| e1_rsi-side-predicts-next-week | confirmed (+2.28) | no (5 of 6: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar) | - |
| g1_rising-month-weekly-momentum | confirmed (+3.65) | no (2 of 6: Mean daily return; Calmar) | - |
| b1_nearness-to-high-more-coins | confirmed (+5.29) | profitable enough | does not hold |
| e1_heavy-volume-rising-follow-through | inconclusive (+1.90) | no (2 of 6: Mean daily return; Calmar) | - |
| g1_momentum-continuation-in-uptrends | confirmed (+3.83) | no (1 of 6: Calmar) | - |
| e1_short-horizon-dual-momentum-continuation | inconclusive (+1.66) | profitable enough | - |
(2026: no hourly data for any idea: "no data". The new-dates test runs only for ideas confirmed AND profitable.)

**Outcome B, as pre-registered:** most confirmed (7 of 12), few profitable (3 of 12), 2 both (outcome A needed 8).
- **The effects survive on hourly bars; the books do not pay.** 5 of 12 fail 5 of the 6 bars, Sharpe included: the
  same idea read on hourly bars trades more (costs) without more edge.
- **What pays on hourly bars is the slowest trend ideas** (golden-cross uptrends, nearness to the high, slow and fast
  momentum); momentum in uptrends misses only Calmar.
- **Only one holds on new dates:** momentum inside golden-cross uptrends (confirmed t +7.19, profitable, holds on
  2016-17). The live bot's strategy (19-coin nearness) is confirmed and profitable on 1h but does not hold on 2016-17.
- Stepping back: for these ideas hourly bars add costs, not edge; their daily versions are the ones to keep. Hourly
  bars are worth testing where the effect itself is hourly (the time-of-day signals of the slow brief: confirmed, not yet profitable).
- 08:30: retest done (reading above). Slow brief 17 ideas, 7 confirmed, 0 profitable (three of the confirmed are time-of-day ideas: t +7.68, +5.27, +4.42). About 35 USD spent.
- 08:3x: operator's go: the intraday brief after the current slow stretch (the slow brief pauses).
- 09:1x: runs stopped in this session (operator: the design session and a new run session split). intraday_1h_run stopped mid turn 8 (017-02; resumes from its files); slow_1h_run paused at 25.55 USD. The run session continues both from master.

## Day continuation by the run session (brief written 2026-11-19 09:54 UTC, before the run)
**Purpose:** finish the two hourly briefs within the operator's budget: `intraday_1h_run` (brief 017, funding-settlement
clock) up to 90 USD in all, then `slow_1h_run` (brief 016, grind versus jump) up to 90 USD in all. One loop at a time
(both call the components step, which writes the shared components file). Each stretch is a tracked task bounded by the
run's spend + 3 USD; the next stretch is launched when one ends.

**State at the start (measured):** intraday 2.73 USD, 6 ideas (1 tested: inconclusive t +0.85, not profitable; 4 wait for
components, 1 untestable), turn 8 (017-02) cut mid-turn, resumes. Slow 25.55 USD, 19 ideas: 18 planned, 9 confirmed
(t +2.65 to +7.68), 0 profitable: all 18 books fail all 6 measures of step 6, Sharpe included.

**Expected outcomes, fixed now:**
- **Intraday:**
  - **I-A.** At least one idea confirmed AND profitable (it gets the unseen test on 2016-17).
  - **I-B. (expected)** Some clock effects confirmed, none profitable: a few hours a day of edge does not pay 15 to
    25 bps a round trip, as with the slow brief's time-of-day ideas.
  - **I-C.** Few or none confirmed: the settlement clock leaves no trace in spot hourly returns.
- **Slow:** **S-A** one or more profitable; **S-B (expected)** more confirmed ideas, still 0 profitable, its lines
  drifting further to time-of-day signals; **S-C** the lines run dry (no candidate left).
- **Time, not money, is the likely limit:** about 1 USD and 15 to 60 minutes a turn, so 87 USD is far more turns than
  a day holds. The reading says how far each run got.
- **Pre-registered last night, checked here:** the slow brief should do better than the intraday one.

## Journal of the day (run session)
- 09:53 UTC: container fresh (up 0 min); working tree clean, so no build was cut. Venv created. Intraday resumes first.
- 09:54: intraday stretch 1 launched (tracked task, --budget 5.73). Check-ins every 45 minutes.
- 10:19: intraday stretch 1 ended on its budget (5.70 USD, 2 turns, 25 min). 017-03 (recovery after settlement, after an
  uptrend): inconclusive t +1.39, not profitable (6 of 6 failed). 017-04 (decline after settlement, after a downtrend):
  rejected t -5.89 (the opposite of the claim, strongly), not profitable (6 of 6).
- 10:2x: found that 017-02 (re-planned 08:55 once unblocked, cut before its backtest) was not finished on resume: the loop
  reads it as finished because its old refusal row is in the table (POTENTIAL_ADJUSTMENTS.md, "an unblocked idea cut
  mid-run"). The only such idea in both runs. Workaround: `run_idea` on 017-02 by hand, the loop stopped; then the loop resumes.
- 10:31: 017-02 finished by hand: inconclusive t +1.30, not profitable (6 of 6), lines 7.b, 7.d, 7.g proposed ideas; 1.35 USD. Run at 7.00 USD.
- 10:41: check-in, no restart (up 48 min). Stretch 2 on turn 11: 017-05 (settlement move reverses), unblocked, now planned by step 3; backtest running. 7.10 USD.
- 11:05: stretch 2 ended on its budget (10.50 USD, 3 turns, 33 min). 017-05 (the move into a settlement reverses after it):
  confirmed t +5.10, not profitable (6 of 6). 017-01.g1 (midday fade of a 3-day trend): inconclusive t +0.42. 017-02.g1
  (late-evening rise after a daily fall): rejected t -3.73. None profitable. Stretch 3 launched (--budget 13.50).
- 11:28: check-in, no restart (up 1h35). 017-03.g1 (a one-hour move reverses the next hour): inconclusive although its main
  t is +10.23 (417k bars): the plan's supporting check (stronger when volatility is high) is t +1.69, below 2; the gain
  is 0.8 bps an hour before costs, against 15 to 25 bps a round trip; not profitable. Turn 15 (017-04.c1) backtesting.
- 11:53: stretch 3 ended on its budget (13.61 USD, 3 turns, 48 min). 017-03.g1 inconclusive t +10.23 (above); 017-04.c1
  (post-settlement decline over four hours): confirmed t +4.85; 017-04.c2 (rebound after falls, off settlement hours):
  confirmed t +4.08; none profitable (6 of 6 failed each). Run so far: 13 ideas tested, 3 confirmed, 0 profitable.
  Stretch 4 launched (--budget 16.61).
- 12:16: check-in, no restart (up 2h23). 017-04.g1 (rebound at the US open after falls): confirmed t +4.06, not profitable
  (6 of 6). 017-05.g1 refused by step 3 (missing component); the loop called the components step (turn 18, 10 turns since
  its last call): built `MeanAbsoluteMoveRankComponent` (lookback 720, period 168), 0.33 USD; 017-05.g1 unblocked and
  re-planned at once (turn 19, backtesting). Build committed on the working branch (standing go). 14.9 USD.
- 12:51: stretch 4 ended on its budget (16.99 USD, 4 turns and a components call, 58 min). 017-05.g1 (volatile coins' short
  dip rebounds): confirmed t +13.80; 017-01.g2 (an hour's move reverses, by volatility): confirmed t +12.28; neither
  profitable. Example of why: 017-05.g1's book trades 3.9 times a day and loses 0.11 % a day after costs (Sharpe -2.20).
  Run so far: 16 ideas tested, 6 confirmed, 0 profitable. Stretch 5 launched (--budget 19.99).
- 13:03: check-in, no restart (up 3h10). Stretch 5 on turn 21 (017-02.g2, hourly reversal in volatile periods), backtesting. 17.1 USD.
- 13:50: check-in, no restart (up 3h57). 017-02.g2 (hourly reversal in volatile periods): confirmed t +10.25, not profitable; its backtest took 47 min. Turn 22 (017-03.g2, daily move reversal) backtesting. 17.9 USD. The design session asked (13:20, 13:34) to merge master (PR #570 and the fix of the 017-02 resume defect) between two stretches: verified on origin/master; to merge when stretch 5 ends.
- 14:26: stretch 5 ended on its budget (20.42 USD, 4 turns, 94 min). All 4 confirmed, none profitable: 017-02.g2 t +10.25,
  017-03.g2 (daily move reversal) t +3.80, 017-04.g2 (late-evening rebound after falls) t +4.78, 017-05.g2
  (volatility-scaled two-hour reversal) t +13.79. Run so far: 20 ideas tested, 10 confirmed, 0 profitable.
- 14:3x: master merged between stretches (PR #570 to #572: run briefs in runs/, components step changes, the loop's resume fix); one conflict, POTENTIAL_ADJUSTMENTS.md, kept as master's. Cards' tests: 88 passed. Under the new rule no idea of either run is unfinished. Stretch 6 launched (--budget 23.42).
- 14:36: check-in, no restart (up 4h44). Stretch 6 on turn 25 (017-02.g3, daily move reversal), backtesting. 20.5 USD.
- 14:58: stretch 6 ended on its budget after one turn (24.71 USD, 31 min). 017-02.g3 (daily move reversal): confirmed
  t +3.90, not profitable. The turn cost 4.28 USD: one 7.d call wrote 129k output tokens in 866 s, 3.38 USD (usual: about
  0.10); it ended normally and its answer was used. Recorded (POTENTIAL_ADJUSTMENTS.md, 17); nothing changed. Run so far:
  21 ideas tested, 11 confirmed, 0 profitable. Stretch 7 launched (--budget 27.71).
- 15:22: check-in, no restart (up 5h29). 017-03.g3 (trend continues after settlement): confirmed t +9.14; 017-04.g3
  (afternoon continuation of a 3-day trend): confirmed t +8.07; neither profitable. Turn 28 (017-03.g4, midday trend
  giveback) in step 3. Run so far: 23 ideas tested, 13 confirmed, 0 profitable.
