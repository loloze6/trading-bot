# Potential adjustments (parked)

Items noted while designing and running the steps, not started: each waits for the operator's go. What was fixed or
built is removed from this list once done (git keeps it; each fix is in its card and its commit). Reviewed with the
operator 2026-11-19: 20 items to 11, plus the operator's new item on short positions and the run session's defect on
an unblocked idea.

## Parked: recent ideas rarely take a short position (operator, 2026-11-19)
The operator: investigate why the recent ideas did not reach a negative forecast. Measured on BTC, every window of every
backtest (a forecast below 0 on at least one bar; a short position follows it in every case):
| Run | Backtests | Never below 0 |
|---|---|---|
| slow_1h_run | 18 | 13 |
| retest_1h_run | 12 | 9 |
| night_013_run | 26 | 14 |
| volume_run | 18 | 13 |
| night_rsi_run (earlier) | 12 | 2 |
To find out where it comes from: the briefs and step 2 (ideas written as long-only bets), step 3 (configs built
one-sided: a component that is never negative, a clip at 0, a rule that only opens longs), or the components (many built
"never negative, no direction"). Also seen: `forecast_distribution.csv` puts a forecast of exactly 0 in the bin "-5_0"
(bins closed on the right), so its "negative" bins count the flat bars.

## Parked: an unblocked idea cut mid-run is never finished (run session, 2026-11-19)
- **What was seen:** `intraday_1h_run` 017-02 was refused at 00:13 (missing-components; a row in run_idea's table),
  unblocked, re-planned by step 3 at 08:55 (plan index: "plan"), then cut before its backtest when the night's runs were
  stopped. On resume (09:54) the loop did not finish it: `loop.unfinished()` counts an idea as finished when it has any row
  in the table, and the old refusal row was still there; `select_next` counts it as tested (its plan exists). The queue
  read "tested: step 5 -; step 6 -" and nothing would ever run its backtest. Checked: the only such idea in both 1h runs.
- **Workaround taken (no code changed):** `run_idea` called by hand on 017-02 in the same run, the loop stopped (step 3
  skipped, steps 4 to 7 run), which is what the loop's resume rule should have done.
- **Fix to consider (design session):** read "finished" from the turn, not the table: an idea is unfinished when its
  latest turn has no finished `run_idea` call after it (e.g. the table row older than the turn, or a "done" line per turn).

## Parked: step 3, the noise from writing a test freely
- **Details only a plan can settle:** how its non-overlapping samples are drawn, which test it uses, and what each case
  is ("sharp-move bars": up moves only, or every labelled bar?). Step 5's conventions cover the common cases.
- **One idea, different tests:** the same idea gets different verdicts from two plans written separately (second night:
  013-04 t +1.99 in one run and +2.46 in another; 012-01 +2.11 and +3.26), and one judgement differs by bar size or
  between mirror ideas (a volume split "adapted" on daily bars, "replaced" on hourly ones; 003-05 against 003-06).
- **True mismatches remain:** plans whose config does not trade the stated situation (night_013_run d2: averaging an
  always-negative and an always-positive block; second night: two more, one at 82 %).

## Parked: duplicate ideas, a rule on the plan
`select_next` finds a duplicate only when two ideas have the same text and data. Seen: two ideas from different parents
(`...d1_weekend-moves-reverse-both-ways` and `...b1_weekend-fall-reverses-monday.d1_weekend-moves-reverse-both-ways`,
night_run) gave the same t (+2.75) and the same failures, about 1 USD each; step 2's 002-01 (after the cross) and 002-05
(from cross to cross) became the same config in step 3. A rule on the plan (same config, same data) rather than on the
text would catch both. Not built.

## Parked: ideas tested on data step 7 did not see
From the overnight run (2026-11-13): of 8 ideas confirmed on the 6 default coins, 4 did not hold on 9 other coins, and
step 7's own numbers are inflated by its search; 6 coins count as about 2 independent coins (books' correlation 0.40 to
0.46), so years, not coins, set what an idea can show. Unseen dates are standard since 2026-11-18
(`orchestration/unseen_test/`). Left to discuss: test the same plan unchanged on coins step 7 never saw (the overnight
tool `oos.py`, removed, in git history); and count the ideas tried on one data set, with a limit past which a result
there counts only with an unseen test.

## Parked: coins without data on the reachable venue
BNB: no data on Kraken. Parked with the quality of the backtest output.

## Parked: record the regime detector's values in the backtest
From the overnight run (2026-11-13; step 5's false "mismatch" on N1-01), parked by the operator.
- **What was seen:** the engine records the strategies' components, but not the regime detector's components: only its decision (the `regime` column). Step 5 and step 7 must recompute the detector's measures from prices.
- **To do:** record the detector's value and each of its components' values in the backtest record, for analysis.

## Parked: an idea proven and profitable, what next (a topic of its own)
Operator, 2026-11-15. Line 7.f ("what could break a confirmed idea and its profitable book") is on hold: being real and
profitable is not a result to diagnose but the end of the research, where a decision starts. To design as one topic:
the final test on the sealed holdout, what could break the idea and its book, how several such books combine, paper
trading, a small live test, and watching it once live. First inputs: 7.e's two confirmed and profitable ideas
(002-03's e1, N2-04's e1, 2026-11-14).
- **2026-11-18:** the unseen test is done (`runs/UNSEEN_RUN.md`, outcome 1); next is paper trading of momentum in uptrends
  (night_013) and high-RSI trend continuation (validation), via the live session.
- **The regime line, folded in here (operator, 2026-11-15):** most of its problem is now covered by validated lines
  (7.d asks when a book should not be in the market; 7.b and 7.c propose an effect limited by a condition; the sizing
  cuts exposure in violent periods). What is left belongs with combining books: a regime shared by several strategies
  (one condition that switches books on and off), and pure regime findings (a condition with nothing graded inside,
  not an idea under the shared definition), as building blocks for that switch.

## Parked, larger topic: brief management (2026-11-17)
The operator's grouping: **result loop back** (a file next to the brief, not inside it, saying what its run found: its
ideas' results, its blocked ideas, where the lines went), **brief archiving**, **brief reopening**. Seen tonight: the
answer to "which of the theory's ideas are real and pay" was written by hand in runs/NIGHT_RUN.md; no file holds it.

## Parked: the operator's next topics (2026-11-18)
Each waits for its own plan and go. Where each lives: the live session (live), the visualizer session (viewer).
| Topic | Where | What |
|---|---|---|
| Several coins in one bot | live | one bot trading a few coins at once, each with its share of the account (the research tests one book per coin) |
| Hosting the bot | live | the live bot runs on the operator's PC today |
| Live operations | live | failure, stop, restart, crash, notification |
| Research viewer, round 2 | viewer | improvements, hosting, access from the phone |
| A viewer of the live bot | live / viewer | the live runs' books and decisions, day by day |

## Parked: futures candles for a pre-live check (live session's comparison, 2026-11-18)
Live trades Kraken futures; the research backtests spot. Prices differ by 0.002% to 0.05%: 5 decisions in 321 days
differ (the 0.2 rule on a knife edge), at most 8.67 per 1,000. Futures candles start 2022-03-23 (ZEC 2022-08-24), so
they cannot replace spot for the folds (B and C are 2018 to 2021). Proposed when a topic opens: the data source as a
backtest setting (spot by default) and a pre-live check of an idea going live on futures candles from 2022-03, with
funding once modelled (funding is the larger spot vs futures difference).

## Parked: the GitHub security warning (2026-11-17)
GitHub reports 1 critical vulnerability on the default branch (Dependabot alert 1). Not examined. The operator: park.

## Parked: two loops calling the components step at the same time (night 1h, 2026-11-19)
Two loops on the same working tree would build into the same shared files (`strategy_components.py`, the catalogue,
the specs) at the same time. Tonight the briefs ran one after the other. (A build cut by a restart is undone at the
step's next start since 2026-11-19: `components/card.md`.)
