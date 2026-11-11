# Step card 6: Applicability (2026-11-11, proposal)

## Business objective, one question
Is acting on this idea worth it?

**Establish whether acting on a real idea pays, after its costs and against its risk, consistently enough to be traded, by one rule fixed in advance and applied the same way to every idea.**

## Input
One real idea: its verdict from step 5 (confirmed), with the standard samples step 5 measured on its backtest record, and its plan (for the horizon). An idea whose verdict is not "confirmed" is not assessed; its index line says so.

## Output
One assessment per real idea: **worth acting on** or **not worth acting on**, with the evidence.

## What an assessment is
**An assessment is the answer, by one rule fixed before any idea is judged and the same for every idea, to whether the gain of a real idea covers the cost of acting on it with a margin, often enough and steadily enough to be worth trading.**

- **It judges the idea, not the backtest.** The backtest's own result (its portfolio value, its fees) reflects how the test was built: a config that rebalances every bar and holds "while", not for a set period. Judging it would judge the test's design. The assessment uses the idea's gain per sample, measured by step 5, per unit of position.
- **It calculates; it does not measure.** It reruns nothing and rebuilds no trade. It does arithmetic on step 5's standard samples: the gain, how often, how much it varies, where.
- **One rule for every idea.** Its thresholds and its cost are written once, before any idea is assessed. An idea never gets its own rule, and the rule is never moved after seeing an assessment.
- **Before sizing.** The gain is per unit of position. How large to trade, and how to combine ideas, is another question.

## The fields of an assessment
**In `assessment.md`:**
1. **status** (header): worth acting on, or not worth acting on.
   - For: the answer.
   - Used by: the operator, to decide which ideas to take further.
   - Without it: no answer.
2. **idea, plan, verdict and fit** (header, copied by code).
   - For: tracing the assessment to the idea and to its proof; an "adapted" test stays marked as such.
   - Used by: the operator.
   - Without it: an assessment cannot be traced to what was proven.
3. **Gross gain per sample:** the average gain of one sample over the plan's horizon, against holding the coin, per unit of position, before costs.
   - For: the size of the effect, in one unit for every idea.
   - Used by: the rule (fields 5 and 6), the operator.
   - Without it: no way to compare an effect with its cost.
4. **Cost per sample:** one round trip at the standard cost, per unit of position.
   - For: what acting on the idea once costs.
   - Used by: the rule.
   - Without it: a gain smaller than its cost looks like a profit.
5. **Gain-to-cost ratio:** field 3 divided by field 4.
   - For: how many times the gain covers the cost. Below 1, acting loses money; near 1, a small error in the cost erases the gain.
   - Used by: the rule, the operator.
   - Without it: no margin against costs estimated too low.
6. **Net gain per sample:** field 3 minus field 4.
   - For: what is left after costs, per action.
   - Used by: fields 8 to 10.
   - Without it: the following fields have nothing to build on.
7. **Samples per year:** the number of samples with a position, divided by the years covered.
   - For: how often the chance comes. A large gain twice a year is not a large gain per year.
   - Used by: fields 8 and 9, the operator.
   - Without it: frequency is invisible.
8. **Net gain per year:** field 6 times field 7, per unit of position.
   - For: what acting on the idea all year leaves.
   - Used by: the operator.
   - Without it: no yearly view.
9. **Net Sharpe per year:** the mean of the net gains per sample, divided by their spread, times the square root of field 7.
   - For: the gain against its ups and downs, the usual measure of whether a gain is worth its risk.
   - Used by: the rule.
   - Without it: a gain with huge swings looks as good as a steady one.
10. **Worst run of losses:** the deepest fall of the net gains added up in time order.
    - For: the worst stretch a trader would live through.
    - Used by: the operator.
    - Without it: the risk is one average number.
11. **Consistency:** the share of coins, and the share of periods (folds), on which the net gain per sample is positive.
    - For: knowing whether the idea pays in most places, or only in one coin or one period.
    - Used by: the rule.
    - Without it: one lucky coin or year can carry the whole result.
12. **Decided by:** the condition of the rule that settled the status.
    - For: the answer can be checked and challenged.
    - Used by: the operator.
    - Without it: a bare word.

**Next to it:**

13. **The index line** (`INDEX.md`): `<plan id>: worth acting on | not worth acting on [gain/cost <x>; net Sharpe <y>; coins <a/b>; periods <c/d>]`, or `<plan id>: not assessed: the verdict is <status>`.

## The rule (one for all, fixed before any idea is assessed)
**Worth acting on** when all three hold; otherwise **not worth acting on**:
1. gain-to-cost ratio of at least 2 (a margin against costs estimated too low);
2. net Sharpe per year of at least 0.5;
3. a positive net gain per sample on at least two thirds of the coins and two thirds of the periods.

**The standard cost:** 0.10 % per side (the venue's fee plus slippage), so 0.20 % per round trip.

These values are proposals, standard rules of thumb, for the operator to set. They are written once in `helper/rule.yaml`. The code reads them from there.

## Storage and naming
Aligned with the other steps.

```
06_applicability/
  card.md                      this card
  helper/
    rule.yaml                  the thresholds and the standard cost
    make_assessment.py         reads a verdict and its standard samples, applies the rule, saves the assessment
  assessments/
    INDEX.md                   one line per idea
    REVIEW.md, run_log*.txt    once a real run has filled it
    <plan id>/assessment.md    one per real idea
  exercise_k/                  the exercises
```

## The AI
**None. The step is code only.**
- The rule is the same for every idea, so no judgement is needed per idea: plain code applies it, the same way every time.
- No model call, so no cost and no run-to-run difference.
- **Checks in code:** it refuses only an input it cannot read: a verdict that is not "confirmed" (written as "not assessed"), or missing standard samples.

## Quality criteria on the assessment
- **Every number recomputes** from step 5's standard samples and the rule file. Nothing else is read.
- **The rule is applied as written,** and "decided by" names the condition that settled it.
- **The same input gives the same assessment,** always.
- **Nothing is measured again:** no backtest, no new statistic on the bars.

## Fixed inputs for the iterations
Planted records, as in step 5's planted test (`05_verification/planted_test/`): one real record, with a known gain added in the forecast's direction, at several sizes. Their standard samples come from step 5. The sizes are chosen so that some pass the rule and some fail it on cost alone. Plus real verdicts that are not "confirmed", which must give "not assessed". Planted records are not market evidence.

## Variants compared
None planned: there is no model to compare. The exercises check the arithmetic and the rule.

## Who judges the output
The operator: "given these numbers, would I trade this idea?". An independent recomputation, by hand or by a separate script, checks every number.

## Done when
On the fixed inputs, every number matches an independent recomputation, and every planted size gets the status the rule gives it. Status: card proposed; to build at the first real confirmed idea (today no idea is confirmed).

## Open
- **What step 5 must add first.** Its standard samples: for every non-overlapping sample of the plan's horizon that starts with a position, the coin, the window, the side, and the gain over the horizon against holding (the coin's mean over all windows), per unit of position. One common form for every plan. Today step 5 reports only each plan's own measure. Not built.
- **The thresholds and the standard cost** are the operator's to set before the first assessment.

## To observe in the tests
- Whether 0.10 % per side is realistic for the coins tested.
- Whether "two thirds of the periods" is too strict with four folds.

## What this step does not do
It does not rerun a backtest, measure the idea again, choose settings, size positions, combine ideas, or decide on the holdout.
