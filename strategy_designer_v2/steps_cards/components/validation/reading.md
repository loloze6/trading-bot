# components: validation (2026-11-17 and 18)

The card's validation: quality of the components, standardization, unblocking, on the fixed inputs (the wishes of the
night runs), twice. Three exercises, then the second night, where the loop called the step on its own. The exercises'
own folders are removed now that the card is validated (git keeps them: `components/exercise_1/` to `exercise_3/`).

## What was run
| Exercise | Wishes | Answers | Cost | Notes |
|---|---|---|---|---|
| 1 (first pass) | 13 of 57, then stopped to keep wishes for exercise 2 | 8 built, 4 exists, 1 cannot build | 2.24 USD | 3 defects of the step found and fixed |
| 2 (the automatic path, night_rsi_run) | 8 | 4 built, 4 exists | 1.28 USD | the loop called the step, the 8 ideas were unblocked, step 3 called again, steps 4 to 7 run |
| 3 (second pass) | 36 | 13 built, 23 exists, 0 cannot build | 4.44 USD | 1 defect found and fixed |
| Second night (called by `loop`, 3 times) | 7 | 5 built (2 first refused by defects, asked again) | 2.25 USD | 3 defects found and fixed |

About 0.12 USD and a minute a wish; a build about 3 minutes, most of it the proof. Model: Opus (Sonnet not compared).

## The three tests
- **Quality: met.** Every component built passed every standard check (warm-up, a hand computation on rows up to t, the
  engine and the validator, a value on every bar of 19 coins' real data, its old defaults unchanged, a new setting that
  changes the output) and the proof, in every exercise.
- **Standardization: met, after the operator's rulings.** One component per measure (two lower-wick classes merged into
  `LowerWickComponent`; `ConvexHighProximityComponent` into `DistanceFromHighComponent`); a mirror of a measure is the
  same measure; a setting must change the output on real data (`tie_side` removed); one setting per purpose (`centred`
  and `log` on `VolumeRatioComponent` merged into `form`). Each merge proved: every value identical to the old classes'.
- **Unblocking: met.** 46 of the 49 ideas refused for missing components were unblocked and tested; on the second night
  the loop built, unblocked and tested within the same night (`…calm-regime-daily-move-continuation`).

## Defects of the step found and fixed (each general, with a test)
1. A build undone kept no record (now in `builds/not_built/`).
2. The harness's engine check left out `standardise` (step 3 writes it first in every config).
3. A spec written by hand with a comment could not be read.
4. The harness's synthetic data was shorter than a long warm-up.
5. The answer's reading stripped `**` from the code (Python's power operator).
6. The proof compared the chart files and the call summaries (whose folder depends on how step 4 grouped its calls): it
   compares the engine's files window by window now.
And one in the engine, found by it and fixed on the operator's go: a one-bar component's history was too short.

## Status
Validated. The cost of an answer and of a build is measured; a Sonnet variant was not compared.
