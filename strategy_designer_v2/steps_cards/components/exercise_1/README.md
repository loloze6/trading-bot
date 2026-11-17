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

## Reading
(written after the run)
