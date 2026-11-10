# Exercises 1 and 2: reading (the same file is in exercise_2)

**What ran.** The step 5 helper, run twice on the 29 daily plans of `03_test_plan/plans/`. Opus.
- **Cost:** run 1 about 1.25 USD, run 2 about 0.97 USD (0.05 to 0.10 per plan); about 20 to 30 seconds per plan.
- **Refusals:** no function was refused by the code in either run.
- **No verdict, correctly, for 14 plans:** 7 untestable, 6 missing-components, and `003-02`, refused by the engine in step 4.

## Status: 14 of 15 the same in both runs

| | Run 1 | Run 2 |
|---|---|---|
| confirmed | 0 | 0 |
| rejected | 7 | 6 |
| inconclusive | 8 | 9 |

**The one difference: `001-03`, rejected in run 1, inconclusive in run 2.**
- **The plan says** "only non-overlapping 5-bar returns are used, each counted once", but not how to pick them.
- **Run 1** took every 5th bar from the start of each window: 42 cases, t = -0.06. The plan rejects at t ≤ 0, so: rejected.
- **Run 2** picked bars greedily, at least 5 bars apart: 51 cases, t = +0.28, so: inconclusive.

Both readings are literal, and both are stated in "reading". The result sits on the plan's threshold of 0.

## The same status, different numbers (four plans)

- **`002-02`, `002-05`, `003-01`:** "value" holds the measure in one run and the t-statistic in the other (for example 0.466 against 0.0047).
- **`003-05`:** opposite signs and sizes (44.5 against -59.4). One run wrote heavy minus thin, the other thin minus heavy. The values are huge because the measure divides by small moves.
- **`002-06`:** "cases" counts 5 stretches in one run and 434 bars in the other. The plan sets minimums on both.
- **`001-01`:** 60 cases against 80, the same sampling difference as in `001-03`.

## Reading the functions against their plans

Read for `001-03`, `002-06`, `003-05` and `002-05`:
- Each function takes the plan's horizon, groups, thresholds and minimum counts, keeps returns inside a window, and names its open choices in "reading".
- No function added a measure or changed a threshold.

The differences come from what the plans leave open, not from functions departing from the plans.

## Changes made for exercises 3 and 4 (untested here)

1. **Conventions for open details, written once in `record_description.md`,** used only when the plan says nothing:
   - non-overlapping samples are bars 0, h, 2h, ... of each window;
   - the t-statistic is Welch's for two groups, and the ordinary t for one mean;
   - a difference is "A minus B" in the order the plan names them.
2. **The result format:**
   - the measure's value and its test statistic are two separate numbers;
   - "cases" becomes "counts": every count the plan's minimums refer to, each one named.

**For step 3, proposed and not made:** a plan should state how its non-overlapping samples are drawn, and which test it uses. The conventions cover the common cases, but the plan is the right place for them.
