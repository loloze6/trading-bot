# Step 7, exercise 2: one call or analyst then deducer, settled

**What ran.** Exercise 1's inputs again, both modes (18 analyses), then two judgements by a separate closed-book model call (`../../overnight_run/judge_modes.py`, results in `../../overnight_run/mode_judgement.json`, 0.95 USD):
- **stability:** for each line, backtest and mode, how many ideas of exercise 2 match an idea of exercise 1 (same situation, same direction);
- **blind quality:** for each line, backtest and exercise, the two modes' ideas, with the findings they cite, under random labels; the judge picks the better set on four criteria: ideas follow from their findings, serve the line's objective, a trader would act on them, a one-coin test can check them. "More ideas is not better in itself."

| Over exercises 1 and 2 | One call | Analyst, then deducer |
|---|---|---|
| Blind quality wins (16 comparisons, planted 7.c left out) | **9** | 7 |
| Ideas found again on a rerun | **59 %** (13 of 22) | 42 % (13 of 31) |
| Ideas naming a value absent from the plan (fitted to the data) | **17 %** | 29 % |
| Numbers in findings traced to the explorations | 95 % | 95 % |
| Findings and ideas per analysis | 6.4 and 2.6 | **9.3 and 3.8** |
| Cost per analysis | **0.27 USD** | 0.35 USD |

**Conclusion: one call.** The split finds more, but the judge repeatedly calls its extra ideas padding (one finding restated as several ideas); it is less stable, fits more values to the data, and costs more. This corrects the impression from exercise 1 alone, which rested on one value-free idea set. Caveats: the judge is the same model family, and 16 comparisons is a small sample; all four measures point the same way.

**Also learned.** Only about half of an analysis's ideas come back on a rerun, in either mode: an idea found twice is more trustworthy. Proposed as an improvement (run each analysis twice, keep the recurring ideas first), and used tonight as a selection criterion.

**Date check.** Twice the deducer named months with a year and was refused, then passed. It does not see the data; brief 002's source line carries a publication date, which it likely echoed.

**Status.** Two exercises: the lines a, b, d and g meet "done when" on their mechanics; the mode is settled as one call. 7.c (planted input only), 7.e and 7.f (no input) remain untested on real cases.
