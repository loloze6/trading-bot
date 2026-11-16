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
XRP w7 and w13 in full_data_run). It changes verdicts: a plan whose minimum count is close to the most the data can
give becomes "not observable" (002-03's repair in demo_run); and since step 4's one-call-per-coin change, a coin with
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
