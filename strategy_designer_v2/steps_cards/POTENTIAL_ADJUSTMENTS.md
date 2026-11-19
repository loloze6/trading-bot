# Potential adjustments (parked)

Items noted while designing and running the steps, not started: each waits for the operator's go. What was fixed or
built is removed from this list once done (git keeps it; each fix is in its card and its commit).

## Other open items
- **Step 3: details only a plan can settle.** A plan should state how its non-overlapping samples are drawn, which test
  it uses, and what each case is ("sharp-move bars": up moves only, or every labelled bar?). Step 5's conventions cover
  the common cases.
- **Step 3: one idea, different tests.** The same idea gets different verdicts from two plans written separately (second
  night: 013-04 t +1.99 in one run and +2.46 in another; 012-01 +2.11 and +3.26), and one judgement differs by bar size or
  between mirror ideas (a volume split "adapted" on daily bars, "replaced" on hourly ones; 003-05 against 003-06). Step 3's
  freedom in writing a test is a source of noise in the verdicts.
- **Step 3: true mismatches remain.** With the shared definition of how a forecast is built, step 5's misreadings are
  gone; the mismatches left are plans whose config does not trade the stated situation (night_013_run d2: averaging an
  always-negative and an always-positive block; second night: two more, one at 82 %).
- **Step 2: two ideas give the same forecast.** 002-01 (after the cross) and 002-05 (from cross to cross) become the same
  config in step 3 (with "near-duplicate ideas" below).
- **Coins without data on the reachable venue** (BNB): parked with the quality of the backtest output.
- **After step 7: on which data its ideas are tested** (with "unseen-data tests" below): an idea step 7 found in some data
  must be tested on data it did not see. Measured: 6 coins count as about 2 independent coins (books' correlation 0.40
  to 0.46), so years, not coins, set what an idea can show.

## Parked: unseen-data tests and a limit of ideas per data set (orchestration)
From the overnight run (2026-11-13), parked by the operator until the steps are final.
- **What was seen:** of 8 ideas confirmed on the 6 default coins, 4 did not hold on 9 other coins, and step 7's own numbers are inflated by its search. About 32 ideas were tested on the same 6 coins in one night; the more ideas tried on one data set, the more a good result there can be luck.
- **Done once, by hand (2026-11-18, `UNSEEN_RUN.md`):** the 12 confirmed and profitable ideas on 2026 and 2016-17 (step 4 `--windows`, step 5 `--measure`): 10 and 11 of 12 hold. Made standard the same day: `orchestration/unseen_test/`, called by `run_idea` for every confirmed and profitable idea.
- **To discuss:** after a confirmation or a profitable book, test the same plan unchanged on coins step 7 never saw (the overnight tool `oos.py`, removed, in git history); and count the ideas tested on a data set, with a limit past which a result there counts only with an unseen-data test.

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
- **2026-11-18:** the unseen test is done (`UNSEEN_RUN.md`, outcome 1); next is paper trading of momentum in uptrends
  (night_013) and high-RSI trend continuation (validation), via the live session.

## Parked: the regime line, folded into "proven and profitable, what next" (operator, 2026-11-15)
Most of its problem is now covered by validated lines (7.d asks when a book should not be in the market; 7.b and 7.c propose an effect limited by a condition; the sizing cuts exposure in violent periods). What is left belongs with combining books: a regime shared by several strategies (one condition that switches books on and off), and pure regime findings (a condition with nothing graded inside, not an idea under the shared definition), as building blocks for that switch.

Before (approved 2026-11-14):
A step 7 line that asks in which market conditions a strategy loses, and what the coin's own bars show at a bar's
close to recognise them. To include (operator, 2026-11-15): pure regime ideas, an effect that holds as a condition
alone ("on Saturdays the coin rises", "in a bear market the coin falls"), which the shared definition of an idea now
leaves out (inside a regime the effect must be graded). Options to weigh then: a strategy assigned to a regime, with
step 5 measuring the regime's own values (see "record the regime detector's values").

## Parked: a cost limit per model call (operator, 2026-11-16: only if it happens again)
On demo_run (budget 15), one 7.b analysis cost 3.77 USD in 14.4 minutes (usually at most 0.37 USD, about a minute):
two calls (one exploration and the answer), no retry. A call cannot loop (no tools, one answer); each is killed at
15 minutes; a line makes at most 6. Every call's tokens and time are now in the step's log, so a repeat would show
which call and why. If it happens again: test the `claude` command's `--max-budget-usd` (not known to stop a single
answer partway).

## Parked: a component with no history step declares one bar fewer than it needs (found 2026-11-16)
`SmaTrendLongOnlyComponent(100)` declares `required_bars` 101 but is ready at bar 102: a component with no history
step stores 2 values, and the declared count covers the first only. No harm today: the warm-up fetches twice
`required_bars`, so the extra bar is always there (the engine's design guide now says so). Found by the warm-up fix
session; not built.

## Parked: near-duplicate ideas (night_run, 2026-11-17)
`select_next` finds a duplicate only when two ideas have the same text and data. Two ideas from different parents
(`...d1_weekend-moves-reverse-both-ways` and `...b1_weekend-fall-reverses-monday.d1_weekend-moves-reverse-both-ways`)
gave the same t (+2.75) and the same failures: probably one test written twice in other words (about 1 USD each).
A rule on the plan (same config, same data) rather than on the text would catch it. Not built.


## Parked: TAO has no data where `common/data_available.md` says it has (night, 2026-11-17)
`data_available.md` lists TAO for fold D; the more-coins backtest got "No historical data for TAOUSD" in all 24
windows. The other 18 coins ran.

## Parked: the GitHub security warning (2026-11-17)
GitHub reports 1 critical vulnerability on the default branch (Dependabot alert 1). Not examined. The operator: park.

## Parked, larger topic: brief management (2026-11-17)
The operator's grouping: **result loop back** (a file next to the brief, not inside it, saying what its run found: its
ideas' results, its blocked ideas, where the lines went), **brief archiving**, **brief reopening**. Seen tonight: the
answer to "which of the theory's ideas are real and pay" was written by hand in NIGHT_RUN.md; no file holds it.

## Parked: the operator's next topics (2026-11-18)
Noted by the operator after the unseen run; each waits for its own plan and go. Where each lives: the live session
(live), this session (research), the visualizer session (viewer).
| Topic | Where | What |
|---|---|---|
| Several coins in one bot | live | one bot trading a few coins at once, each with its share of the account (the research tests one book per coin) |
| Hosting the bot | live | the live bot runs on the operator's PC today |
| Live operations | live | failure, stop, restart, crash, notification |
| Finer bars | research | strategies on 4h, 1h or other bars: what the steps and the data need |
| Research viewer, round 2 | viewer | improvements, hosting, access from the phone |
| A viewer of the live bot | live / viewer | the live runs' books and decisions, day by day |
| The parked list itself | research | review this file: what to keep, merge or drop |

## Parked: a position left open while the forecast is 0 (the 0.2 rule; live session, 2026-11-18)
The bot skips any allocation change smaller than 0.2 (`risk_management.controls.min_allocation_change`, judged on
forecast / 10 with a sizing block), in every backtest and live: a position below 0.2 cannot close while the forecast
stays at 0 (live: 0.17 held 12 days). Measured on the 12 confirmed and profitable ideas: 9.5% of bars hold such a
position (up to 114 days in a row), of mean size 0.01 to 0.05, worth -1% to +1% of each book's gross return. Minimal:
kept as it is (operator, 2026-11-18). The change, if ever wanted: a move to flat always executes.

## Parked: futures candles for a pre-live check (live session's comparison, 2026-11-18)
Live trades Kraken futures; the research backtests spot. Prices differ by 0.002% to 0.05%: 5 decisions in 321 days
differ (the 0.2 rule on a knife edge), at most 8.67 per 1,000. Futures candles start 2022-03-23 (ZEC 2022-08-24), so
they cannot replace spot for the folds (B and C are 2018 to 2021). Proposed when a topic opens: the data source as a
backtest setting (spot by default) and a pre-live check of an idea going live on futures candles from 2022-03, with
funding once modelled (funding is the larger spot vs futures difference).

## Parked: a components build cut by a container restart (night 1h, 2026-11-19)
The components step undoes a build that fails its checks, but a build cut by a restart leaves its class, catalogue row
and spec in the shared files (found 00:26, undone by hand). Proposed: at its start, the step restores
`strategy_components.py`, the catalogue and `tests/built_components/` to their committed state when a class there has
no index line. Also: two loops calling the step at the same time would build into the same files (tonight the briefs
run one after the other).

## Parked: four near-duplicate components built in the night (2026-11-19)
For brief 016 the components step built `RiseBeyondLargestMovesComponent`, `LossShareBeyondLargestComponent`,
`TopGainsShareOfRiseComponent` and `TopLossesShareOfFallComponent`: one measure (how much of a move its `k` largest bars
make) on rises and on falls, as a share or as what is left, from simple or log returns. By the card's rule 1 (one
measure, one component; another base or side is a setting) they should be one component with settings (side, form).
Not merged during the night (plans in flight use them); to review and merge on the operator's go, with the proof.
