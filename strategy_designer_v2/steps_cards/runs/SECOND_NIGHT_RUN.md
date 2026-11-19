# Run brief: the second night (2026-11-18, written before the run)

**Purpose.** Two things, with the machine as it stands tonight (the components step, option A, the shared definition of
how a forecast is built):
1. **Test the unblocked ideas still untested** in the older runs: 25 of the 34 (night_012_run 4, night_006_run 2,
   night_005_run 1, volume_run 8, night_run 10); the brief's own ideas first (option A), then the lines' ideas. night_013_run's
   9 (all lines' ideas, of a theory tested today) wait.
2. **Two new theories chosen by step 1** (theme: "a trading theory of your choice"), each in its own run with `run_brief`:
   014 (price pressure around the perpetual funding settlement hours: hourly bars, probably a missing "hour of the day"
   component: the components step's first automatic build at night), 015 (do rallies raise later volatility more than
   falls: a question about volatility, perhaps untestable by a long/short book).

**Budgets (each the run's total; the operator's 50 USD in all, with the overshoot of the idea that ends each run):**
night_012_run 6.44 (+5), night_006_run 4.58 (+4), night_005_run 3.38 (+3), volume_run 19.80 (+7), night_run 35.40 (+7),
night_014_run 10, night_015_run 10. One run at a time (the components step writes one code file).

**Monitoring.** A check every 90 minutes (a message scheduled to this session): processes alive, the run's files
checkpointed (partial backtest folders left out), a stopped stage restarted with the same command (every command
resumes from the run's files).

**Pre-registered outcomes.**
- **A.** An idea confirmed with a profitable book outside the trend-following family.
- **B.** Only trend following pays again (any new confirmed-and-profitable idea is a rising-trend idea).
- **C.** Nothing new confirmed and profitable.
- **D.** The components step builds a component by itself during a loop (014), its ideas then tested.
- **E.** A theory untestable or not observable as a whole (015, or 014 if hourly data is short).
- **F.** A defect: fixed if general and proven, written here; else parked.

## Reading
(written during and after the night)

**Stages 1 and 2 (00:15 to 02:32 UTC; 29.56 USD; one container restart, resumed).** Stage 1: the 25 unblocked ideas of
the five older runs tested, budgets reached. Stage 2: both new theories untestable as written: 014's 5 ideas planned
on daily bars where its 2-hour windows cannot be seen (step 2 wrote no bar size: parked for the operator); 015's 4
ideas predict volatility, not a direction. The full reading comes at the end of the night.

**Stage 3, written before it starts (02:40 UTC).** The only new effect with a profitable book tonight is a reversal
in volatile periods (night_005_run, `…g2_volatile-reversal-completes-quickly`: confirmed t +3.50, Sharpe 1.16, +0.52
over holding, Calmar 1.05, 163 cases), outside the trend-following family. Purpose: follow its lineage (the lines'
ideas from it, a 7.b on more coins among them) to see whether it holds; then night_006_run's 2 unblocked ideas.
Budgets: night_005_run 15.83 (+12), night_006_run 11.21 (+6); 47.6 USD in all tonight. Outcomes: as above; plus **G**:
the volatile-period reversal holds in its lineage (another confirmed and profitable variant, or more coins).

**The night (00:15 to 03:58 UTC; 50.2 USD in all: 47.78 in `run_idea`, 2.25 in the components step, 0.16 for steps 1 and 2;
the 50 USD budget passed by 0.2, the idea that ends each run finished; three container restarts, each resumed with
nothing lost or half-built).**

| Run | Ideas run | Confirmed | Confirmed and profitable | Inconclusive | Other |
|---|---|---|---|---|---|
| night_012_run | 4 | 1 | 0 | 3 | |
| night_006_run | 12 | 6 | **1** | 4 | 1 untestable, 1 missing a component |
| night_005_run | 13 | 9 | **1** | 3 | 1 mismatch |
| volume_run | 7 | 5 | 0 | 1 | 1 mismatch |
| night_run | 7 | 1 | 0 | 5 | 1 missing a component |
| night_014_run | 5 | 0 | 0 | 0 | 5 untestable (daily bars for an hourly theory) |
| night_015_run | 4 | 0 | 0 | 0 | 4 untestable (they predict volatility) |
| **All** | **52** | **22** | **2** | **16** | 10 untestable, 2 mismatch, 2 missing |

**The two confirmed and profitable ideas.**
- `night_005_run`, `…g2_volatile-reversal-completes-quickly`: "in a coin whose 20-day volatility is high against its last
  100 days, a large one-day move gives back within 3 days, the larger the move the larger the give-back": t +3.50
  (163 cases), Sharpe 1.16, +0.52 over holding, Calmar 1.05. **Outside the trend-following family.** But its lineage
  (stage 3) found the effect real in every variant (t +2.27 to +4.27) and profitable in none: a narrow result.
- `night_006_run`, `…g1_volatility-scaled-momentum-continuation`: "the stronger a coin's 10-day return against its own
  volatility, the more it rises over the next 3 days": t +3.00, Sharpe 0.97, +0.42, Calmar 0.82. Trend following again;
  the same move unscaled (`…g2_ten-day-momentum-continuation`) is confirmed but does not pay: scaling by the coin's
  volatility looks like what makes it pay.

**Outcomes.** **A**, narrowly (the volatile-period reversal: one variant pays, its others do not). **B** (trend following
pays again; the family now counts 5 profitable ideas from 4 briefs). **D** met: the loop called the components step 3
times on its own (5 components built, every one passing every check and the proof), and the ideas it unblocked were
tested the same night (`…calm-regime-daily-move-continuation`: blocked, built, tested). **E** met: 014 and 015 untestable
as written. **G** not met: the reversal's variants did not pay. Short rebounds again real and too small to pay: the
strongest, `…b1_wide-range-breakout-continuation.g1_one-day-drop-rebound`, t +5.93, misses step 6 on its Calmar only
(0.70 against 0.75).

**Defects found and fixed (each general, with a test):**
1. The components step's answer reader stripped `**` from the code (Python's power operator): 3 attempts lost.
2. Its proof compared the chart files and the call summaries (whose folder depends on how step 4 grouped its calls): a
   correct build failed it. It compares the engine's files, window by window, now.
3. `run_idea` stopped on a verdict without a main measure (a mismatch records it as null): the idea's row was missing.
The wishes and the idea they touched were asked or run again.

**Parked for the operator:** step 2 writes no bar size for a theory that needs one (014: an hourly theory planned on
daily bars). Seen, not acted on: the same idea gets different verdicts from two plans written separately (013-04: t
+1.99 in one run, +2.46 in another; 012-01: +2.11 and +3.26): step 3's freedom in writing a test is a source of noise
in the verdicts. Two step 5 mismatches tonight (82 % and one other), now true config-versus-plan differences.

**Step back.** Two nights and a day: 22 ideas confirmed tonight, 2 profitable. The workflow finds real effects easily;
what pays stays narrow: trend following (with the move scaled by volatility), and one reversal in volatile periods.
More ideas will not change this picture; data the analysis never saw will (topic 8).
