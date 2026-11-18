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
