# Potential adjustments (parked)

Items noted while designing the steps, not started. Each waits for the operator's go.

Two separate defects, both seen as "not ready at warm-up" (split 2026-11-16, after the "Known data defects" session's findings):
- **A. A component that needs 0 bars makes the strategy wait forever** (the volume plans 003-01, 003-02). **Fixed**
  in the engine (operator's go, 2026-11-16; merged in `171902d`).
- **B. A few XMR and XRP windows do not run: the engine waited for 400 rows while it declares 250.** **Fixed** in the
  engine (operator's go, Option 1: ready at the rows the config declares; merged in `171902d`). Proof on the six
  full_data_run plans: the 846 windows that ran before give the same files; XMR w13 and XRP w7 now run (12 more
  windows); XRP w13 is still refused (228 rows, fewer than the 250 its plan needs: a real lack of data). The records
  in the named runs were made before the fix and were not rerun.

Both are kept below as the record of the cause.

## Parked A: a component that needs 0 bars of history makes the strategy never ready (cause found 2026-11-16)
**Cause** (the "Known data defects" session, on made-up bars, no market data used, no file changed): `BuyAndHoldStrategy`
needs no history, so it reports 0 bars needed (`trading-bot/strategies/strategy_components.py:671`). The regime detector
sizes its history store to the most its components report, so it keeps room for 0 values
(`regime_engine.py:56`), then counts itself ready only once it holds at least 1 (`regime_engine.py:100`). It never
can, so the strategy is never ready. No number of warm-up bars helps (still not ready after 200); `required_bars=24`
in the message is the engine's floor, and the message ("2x-required_bars was insufficient") points the wrong way.
003-02 ran when its detector component was `PriceEvolutionComponent` (needs 2 bars).

**At fault: the engine.** The config is valid; the component catalogue lists `BuyAndHoldStrategy` with 0 warm-up bars.

**The fix, when approved:** in the engine, a component that needs 0 bars counts as ready (shared with the campaign:
the operator's call). Not in step 3: a config workaround exists (swap the detector component for one that needs a bar
and put a constant clip before the veto; checked on 153 of 153 test bars), but it would teach step 3 a trick for one
engine fault.

**To check first:** whether a run without the warm-up check would trade nothing and read as an ordinary flat result (a
false "nothing here"). Expected by the session, not checked.

## Parked B: the engine waits for 400 rows while it declares 250 (cause found 2026-11-16)
**What is seen:** XMR 23 of 24 windows, XRP 22 of 24 on the default data ("the engine stopped" at warm-up: XMR w13,
XRP w7 and w13 in full_data_run). It could change a verdict whose minimum count is close to the most the data can
give (an earlier note here named 002-03's repair in demo_run: wrong, that record ran every window); and since step
4's one-call-per-coin change, a coin with
a failing window is run twice.

**Not the sizing rule** (an earlier note here said so, wrongly): the same three windows failed in the first full-data
run (commit `5fb1516`), whose configs had no sizing, with the same row counts. Sizing needs 61 rows; the strategy
already needs more, so `required_bars` is 250 either way (measured on all six plans).

**Cause** (the "Known data defects" session, on made-up bars, no market data used, no file changed): the engine says
the strategy needs 250 rows (200 for the 200-day average, plus the 50 values the standardise step declares as its
minimum), but it becomes ready only at row 400: its readiness check reuses `required_bars` (a count of rows) as the
number of past values to wait for, capped at the standardise buffer's size (201), so 200 + 201 - 1. The warm-up
fetches 2 x 250 = 500 days, so a window runs only if at most 100 of them are missing. The three windows got 364, 347
and 228 rows; every window that ran had at least 400.

**At fault:** the engine for XMR w13 and XRP w7 (it demands 400 rows while declaring 250; its message blames the
warm-up length). The data for XRP w13: 228 rows is fewer than the 250 the config needs, so refusing it is right.
Not the config.

**The fix, when approved:** one line in `trading-bot/strategies/strategy_engine.py` `is_ready` (line 567): wait only
for the past values the transforms declare (drop `self._warmup` from the max; it is used nowhere else). The outer
check (rows >= `required_bars`) still holds. All six plans then become ready at row 250.

**What it changes:** XMR w13 and XRP w7 would run (their opening bars may be flat: the engine's gap rule blocks new
entries for some bars after a medium gap); XRP w13 is still refused (needs data). Windows that run today do not
change (on made-up bars: identical forecasts once both versions are ready, 501 bars, six plans), except a window with
a gap of 250 or more missing bars inside it, where the engine re-warms from row 250 instead of 400 (its trades and
not-ready rows would change). The engine is shared: any campaign config with a history transform is affected; the
campaign's windows were not checked.

## History of A and B (the original brief, kept as written)
**Where the files are now (2026-11-16):** the brief's example files (`04_backtest/backtests/003-01_low-volume-up-move-reverts_1d/run.md`, `config.json`) were removed from the working tree by the clean-up of 2026-11-15; they are in git history, commit `57269c6` (the commit before the clean-up): `git show 57269c6:strategy_designer_v2/steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d/run.md`. A current example, in a folder that stays: `04_backtest/full_data_run/backtests/` (see its `INDEX.md`): XMRUSD runs 23 of 24 windows and XRPUSD 22 of 24, "the engine stopped", since the sizing's 60-day window. Only the summaries of a backtest are committed now (`04_backtest/.gitignore`): to look inside, rerun that backtest (a trial, as the note below says).

Added on the operator's instruction, relayed from the "Known data defects" session. The brief is the operator's, unchanged:

> In loloze6/trading-bot, branch ccr-6624e33e-aakrpv, find out why the backtest engine refuses some valid strategy configs at warm-up. Do not change any file.
>
> Symptom: strategy_designer_v2/steps_cards/04_backtest/backtests/ has five plans that did not run, for example 003-01_low-volume-up-move-reverts_1d (see its run.md and config.json). Each stops in trading-bot/core/launcher.py: "warmup_prefetch: strategy not ready after 48 prefetch bars ... required_bars=24". All five have a regime detector with one component, BuyAndHoldStrategy, a veto applying volume_filter to it, no rules, and a flat default regime. Similar configs ran fine: for example 003-02_low-volume-down-move-reverts_1d, whose veto is on PriceEvolutionComponent.
>
> Read the code path: launcher.run_backtest warm-up, strategies/main_strategy.py is_ready, the regime engine and strategies/strategy_engine.py is_ready. You may run that one backtest through strategy_designer_v2/steps_cards/04_backtest/helper/run_backtest.py.
>
> Report in plain words:
> 1. the exact cause;
> 2. whether the config or the engine is at fault;
> 3. the smallest change to the config pattern that avoids it.
> Name periods by fold id only; never write dates.

The other session noted that running that backtest touches market data, so under the repository's hard rules it is a trial and gets a trial-ledger row, even if it only reproduces the refusal.

Since then, the refreshed plans give the refusal on one plan only: `003-02_low-volume-down-move-reverts_1d` (see `04_backtest/backtests/REVIEW.md`). After the symmetric-criteria rewrite: two plans, `003-01` and `003-02`, with the same pattern.

## Other parked items
- **Step 2: the bar size.** An idea's bar size comes from the brief, or from the idea's time scale, or else a default value. Today step 3 applies the default (1d).
- **Step 3: details only a plan can settle.** A plan should state how its non-overlapping samples are drawn, which test it uses, and what each case is ("sharp-move bars": up moves only, or every labelled bar?). Step 5's conventions cover the common cases.
- **Step 3: one judgement differs by bar size.** The same volume idea was "adapted" on daily bars and "replaced" on hourly bars (`03_test_plan/plans/REVIEW.md`). It also differs between mirror ideas: in the symmetric-criteria rewrite, 003-05 (up move) keeps an above/below-average volume split as "adapted", and 003-06 (down move) calls it "replaced" (missing-components).
- **Step 2: two ideas give the same forecast.** 002-01 (after the cross) and 002-05 (from cross to cross) become the same config in step 3.
- **The default data** (BTC/USDT, 1d, fold A): small samples, so many verdicts come out inconclusive.
- **Coins without data on the reachable venue** (BNB): parked with the quality of the backtest output.

- **Step 3: the "holding" reference (found by the full-data run, 2026-11-11).** Every plan compares against the coin's mean over the same window, which shares the bars that set the forecast and biases the result against trend ideas (t = -2.60 on random walks). Fixed (approved: "Go"): step 3 exercises 27 and 28, and the full-data rerun in `FULL_DATA_RUN.md`.
- **Steps 3 and 4: several folds.** Added during the investigation; kept, with the new default data (approved: "Go").
- **Step 2: an idea's time scale (2026-11-12). Applied (operator, 2026-11-15):** every idea states its time in real time, and step 3 converts it to bars (`common/idea_definition.md`). The bar size itself still comes from the brief or the default. Almost every idea is calendar-free but has a time scale: how long its situation takes to form (an indicator's bars) and how long its effect lasts (the horizon). The bar size turns them into real time: "high RSI" (14 bars) is a two-week run on daily bars and a 14-hour run on hourly bars, two different market phenomena. Today the time scale comes from convention and the default bar size, not from the theory. Proposal: each idea states its time scale in plain words ("over days", "within hours"), and the bar size follows from it. Calendar-dependent ideas (hours, weekdays) are few: 003-07, and brief 011 of step 1, exercise 8.
- **After step 7: on which data its ideas are tested.** An idea step 7 found in some data must be tested on data it did not see. Options discussed (2026-11-12): a time split (step 7 reads 2018 to 2021, its ideas are tested on 2022 to 2025), alternate folds, other coins, a stricter bar. Measured: 6 coins count as about 2 independent coins (books' correlation 0.40 to 0.46), so years, not coins, set what an idea can show. To settle with the orchestration of the steps, not in a step's design.


## Parked: unseen-data tests and a limit of ideas per data set (orchestration)
From the overnight run (2026-11-13), parked by the operator until the steps are final.
- **What was seen:** of 8 ideas confirmed on the 6 default coins, 4 did not hold on 9 other coins, and step 7's own numbers are inflated by its search. About 32 ideas were tested on the same 6 coins in one night; the more ideas tried on one data set, the more a good result there can be luck.
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

## Parked: two coins at once could rewrite the same data file (found 2026-11-16, step 4's change 2)
Since step 4 runs the coins at the same time, two backtests can read the same aux data file at once
(`fear_greed_daily.csv` is one file for every coin). The fetcher rewrites a data file only when a read adds rows the
file lacked (`_merge_and_store`, `trading-bot/data/fetchers/base_fetcher.py`); it writes in place, so a backtest
reading the file during that write could see part of it. Not seen: no data file changed in change 2's proof (3 plans,
3 runs each) nor in `demo_run`; the folds' data is already in the files. The plan's guard (check the data folder
before and after, rerun one coin at a time if a file changed) was not built: the operator's rules say no gates.
**Proposed fix, at its cause:** the fetcher writes the new file to a temporary name and then renames it, so a reader
sees the old file or the new one, never part of one. A change to `trading-bot/`, so it needs its own go and proof.
**Fixed (operator's go, 2026-11-16):** `_merge_and_store` writes to `<file>.<process id>.tmp` in the same folder and
renames it over the file; a failed write leaves the file as it was and no temporary file. Proof: tests on made-up data
(`trading-bot/tests/test_merge_noop_no_rewrite.py`: the file holds exactly the bytes `to_csv` writes, one rename, nothing
left behind; a failed rename leaves the old bytes); the bot's suite passes (1,499). No named run reaches this write
today (the folds' data is already in the files), so no run was rerun for it.

## Parked: a relative-volume component (night_run, 2026-11-17)
**Built (operator's go, 2026-11-17):** `VolumeRatioComponent` (`period` 30): volume[t] / the mean volume of the last
`period` bars, bar t included; catalogue row in `03_test_plan/helper/reference/component_catalogue.md`. Proof: 6 tests (8 cases) in
`trading-bot/tests/test_designer_v2_components.py` (hand computation on rows up to t, later bars ignored, warm-up, NaN,
engine run, validator); the bot's suite passes (1,515); one backtest rerun on fixed inputs
(`night_013_run`'s momentum idea, 6 coins, 24 windows): 588 files compared, identical but for the run ids, times and
temporary paths in protocol_summary.json. It adds a class; nothing else in the engine changes.
Brief 003 (volume separates reversal from continuation) cannot be tested: all four of its ideas need a graded measure
of a bar's volume against its own recent average, and no component computes one (step 3: missing-components, four
times). The four wish-list entries converge on one component: the bar's volume divided by the mean volume of the last
N bars (or its log), from the `volume` column (`03_test_plan/night_run/plans/COMPONENT_WISHLIST.md`). Why it cannot
leak: it reads the current bar's volume and the volumes before it, known at the bar's close. A change to `trading-bot/`
(a new component and its tests), so it waits for the operator's go.

## Parked: two more components asked for by night_run (2026-11-17)
Besides relative volume (above): **the close's place in the day's high-low range** (1 idea), and **a move held as the
forecast over the next N bars** (a weekend return carried through Monday and Tuesday, 2 ideas). Each is a change to
`trading-bot/`, so each waits for the operator. Wish lists: `03_test_plan/night_run/plans/COMPONENT_WISHLIST.md`.

## Parked: near-duplicate ideas (night_run, 2026-11-17)
`select_next` finds a duplicate only when two ideas have the same text and data. Two ideas from different parents
(`...d1_weekend-moves-reverse-both-ways` and `...b1_weekend-fall-reverses-monday.d1_weekend-moves-reverse-both-ways`)
gave the same t (+2.75) and the same failures: probably one test written twice in other words (about 1 USD each).
A rule on the plan (same config, same data) rather than on the text would catch it. Not built.


## To discuss: the score that ranks the next idea favours re-finding a known effect (night, 2026-11-17)
A line's record counts each confirmed idea as a success, so a line that keeps confirming one effect in new words keeps
a high record and its variants keep coming first. Seen twice: in night_run, brief 010's ideas ranked below the 7.g
line's third-generation variants of one rebound (0.17 against 0.18); in night_013_run, 8 of the last 13 tested ideas
were variants of momentum or of the one-day rebound. The operator: "improvement point on the idea ranking decision, to
be discussed". Not changed.

## Parked: one list of missing components across runs (night, 2026-11-17)
Each run has its own `03_test_plan/<run>/plans/COMPONENT_WISHLIST.md`; there is no list across runs. Tonight, 40 ideas
in 6 runs were refused for missing components (48 requests), and the same component carries several names (11
"VolumeRatioComponent", 3 "RelativeVolumeComponent", "volume_ratio", ...). By subject: volume against its recent average
19 ideas, a past high or a break of it 13, RSI's time above or below its midline or a divergence 10, a bar's wick or
range 7. Nothing says which component would unblock the most ideas.

## Parked: step 5 "mismatch" on 4 of 19 tested ideas in night_013_run (night, 2026-11-17)
Step 5 found that the config does not trade the plan's situation (57 % to 68 % of active bars on the plan's situation
and side, 90 % needed). The idea's backtest is spent (about 1 USD each) and says nothing about the idea. Whether the
fault is step 3's config or step 5's reading of the situation is not looked at.

## Parked: TAO has no data where `common/data_available.md` says it has (night, 2026-11-17)
`data_available.md` lists TAO for fold D; the more-coins backtest got "No historical data for TAOUSD" in all 24
windows. The other 18 coins ran.

## Parked: the GitHub security warning (2026-11-17)
GitHub reports 1 critical vulnerability on the default branch (Dependabot alert 1). Not examined. The operator: park.

## Parked, larger topic: brief management (2026-11-17)
The operator's grouping: **result loop back** (a file next to the brief, not inside it, saying what its run found: its
ideas' results, its blocked ideas, where the lines went), **brief archiving**, **brief reopening**. Seen tonight: the
answer to "which of the theory's ideas are real and pay" was written by hand in NIGHT_RUN.md; no file holds it.

## New topic: develop the live part of the trading bot (operator, 2026-11-17)
Refactor the bot's live mode (not the research workflow) so that it runs live, connected to the Kraken API, for real
trading. Today nothing in this repository trades live (CLAUDE.md). Not started: a picture of the current live code, then
a plan, then the operator's go.

## New topic: a visual of the runs (operator, 2026-11-17)
A user-friendly HTML view of the runs done: brief, ideas, backtests, results, analyses (step 5, 6 and 7 readings), and
how the ideas lead to one another. Not started.

## New topic: a card for creating a component from the wish list (operator, 2026-11-17)
A card (business objective, guideline, possibly a prompt, the implementation steps) for turning a wish-list block into
a component, written from the expertise and the lessons of building `VolumeRatioComponent`. Lessons so far: group the
wish-list blocks that ask for one measure under different names, and take the general form (volume_run: two ideas need
a short average of several bars, not one bar, against the long one); a "why it cannot leak" note; tests that compute by
hand on rows up to bar t, show later bars are ignored, and run the engine; the catalogue row (and its class count); the
proof rerun on fixed inputs, file by file; the bot's tests run from its own folder. Not started.

## Parked: the engine keeps too short a history for a one-bar component with no history op (components exercise 1, 2026-11-17)
`ConfigDrivenStrategyEngine` sizes each component's history to the largest lookback its components and transforms
need (`strategy_engine.py`, phase 2): a component that needs one bar, with no history op (`identity`, `clip`), gets a
history of length 1, but `forecast` needs 2 values (`max(2, ...)`), so it is never ready. Not met by real configs (step
3 writes `standardise` first, whose window sets the history); met by the components step's harness, which ran its
engine check without `standardise` (fixed: it now uses step 3's form). Fix when approved: a history at least as long as
the forecast needs (`max(2, lookback)`). A change to `trading-bot/`: the operator's go.
