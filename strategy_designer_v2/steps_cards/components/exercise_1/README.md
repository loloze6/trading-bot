# components, exercise 1 (2026-11-17, written before the run)

**Purpose.** The card's validation, first pass: the step answers the 57 open wishes of the 11 runs, for real (Opus),
one call each. Judged on the card's three tests: quality of the components, standardization, unblocking.

**Call.** `build_component.py --runs <the 11 runs> --python VENV` (no budget; each call's cost in
`components/journal.jsonl`).

**Pre-registered outcomes.**
- **A.** The volume wishes `VolumeRatioComponent` already gives (a bar's volume over the mean of its last N bars) come
  back **exists**.
- **B.** The new measures (a past high or its break, RSI's time above or below its midline, a price-RSI divergence, a
  bar's wick or place in its range) come back **built**, each passing every check and the proof.
- **C.** The measures close to an existing one (a mean of several bars' volume; the median of the bars before t) come
  back **built** as a setting on `VolumeRatioComponent`, its defaults unchanged; the product (a scaled move times its
  volume ratio) as one new class.
- **D.** Few **cannot build**, each naming what is missing (a forecast held over the next bars may be one: it is not a
  measure of the bars).
- **E.** Standardization: no two classes for one measure once the call ends.
- **F.** A defect of the step (a crash, a wrong undo, an answer the code misreads): fixed if general, written here.
- Unblocking: the ideas whose wishes are all answered built or exists are counted after the call; rerunning them is
  the next exercise's (its own cost).

## Reading (partial: stopped on the operator's choice after 13 of 57 wishes, the other 44 kept to test the automatic path)

**Answers (13 wishes, 16 calls with the 3 asked again, 2.24 USD, 26 minutes).** 8 built (every one passing every check and
the proof), 4 exists, 1 cannot build.

| Answer | Component | What it measures |
|---|---|---|
| built | `RsiChangeFromPriorLowComponent` | RSI now minus RSI at the lowest close of the last 30 bars (a bullish divergence) |
| built | `RangeCompressionRatioComponent` | the recent high-low range against a longer one (a squeeze) |
| built | `LowerWickShareComponent` | the lower wick over the bar's range |
| built | `LowerWickPercentComponent` | the lower wick over the close, in percent |
| built | `CloseLocationInRangeComponent` | where the close sits in the bar's range |
| built | `OpenToLowDropComponent` | the fall from the open to the low, in percent |
| built | `ConvexHighProximityComponent` | nearness to the 365-bar high, raised to a power |
| built (a setting) | `VolumeRatioComponent` + `exclude_current` | volume against the mean of the bars before t; default unchanged (checked on real data) |
| exists (4) | `VolumeRatioComponent` (3), `RangeCompressionRatioComponent` (1) | the second wish for a measure finds the first's build |
| cannot build | (bearish RSI divergence) | the wish is 0 except at a new high: on/off, not graded (rule 3) |

**Against the outcomes.** A: met (the volume wishes come back exists). B: met for the new measures asked so far. C: met
for the setting (`exclude_current`); the product and the median were not reached. D: one cannot build, with its reason.
E: one question (below). F: three defects of the step, fixed.

**Defects of the step, found and fixed (general, with a test):**
1. **A build undone kept no record:** its answers and checks were lost. Now in `builds/not_built/<run>/<plan>/<wish>/`.
2. **The harness's engine check did not use `standardise`** (step 3 writes it first in every config): a one-bar
   component was never ready. Fixed in the harness; the engine's own short history for such a component is parked.
3. **The builder could not read a spec with a comment** (the hand-written `VolumeRatioComponent` spec): a new setting
   failed three times before any check. Read as a Python literal now.
The 3 wishes refused by defects 2 and 3 lost their index line and were asked again (the journal keeps both answers).
The run was stopped twice to load a fix, each time during a model call (no build half-checked).

**Findings for the operator:**
- **Standardization, a rule to make precise:** the lower wick over the range and over the close were built as two
  classes. One measure with a setting (what it is divided by), or two measures? The card's rule 1 does not say.
- **Step 3 wished an on/off measure** (the bearish divergence: 0 except at a new high). The step answered cannot build,
  rightly. The fault is in step 3's wish, not here: a graded form of the idea is step 3's to find.
- **Cost:** about 0.15 USD a wish, 2 minutes; a build about 3 minutes (most of it the proof).

**Not done yet:** the 44 open wishes (night_run 13, night_013_run 14, night_rsi_run 8, volume_run 9); the automatic
path (loop calls the step, ideas unblocked, step 3 again); the second pass the card's validation needs.
