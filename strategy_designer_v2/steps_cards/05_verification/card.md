# Step card 5: Verification (2026-11-10)

## Business objective, one question
Is this idea real?

**Establish, on evidence fixed before the data was seen, whether the market confirms or rejects the idea, and what that result means for a trader's decisions.**

## Input
One test plan whose outcome is `plan`, and its backtest record. One idea has one plan, so this is one input per idea.

## Output
One verdict per plan: **confirmed**, **rejected**, **inconclusive** (enough cases, no clear result) or **not observable** (fewer cases than the plan's minimum: the data could not show the idea), with the evidence that decided it. Or **mismatch**, when the test does not do what its plan says: no verdict on the idea, and the plan goes back to step 3.

## What a verdict is
**A verdict is the plan's own criterion, applied unchanged to the backtest record: the numbers measured, and which of the plan's rules (confirm, reject, inconclusive) they meet.**

- **First, the test must match its plan.** From the plan's Fidelity lines (the situation, and the side the outcome expects) and the record's raw indicator values, the function checks that the config's forecast is active on the bars of that situation, on that side. Below 90 % agreement, the status is "mismatch" and the criterion is not applied. The check reads the Fidelity, not the plan's Forecast line or its config, because those two are what may be wrong. Found by exercise 6's review: the down-cross plan (002-02) went short in up-trends, and nothing in steps 3 to 5 saw it.
- **The criterion was fixed before the data.** The verdict applies it and never adjusts it: no new measure, no other threshold, no other horizon.
- **When the criterion leaves a detail open,** the conventions in `record_description.md` apply: how non-overlapping samples are drawn, which t-test, the order of a difference. Otherwise the most literal reading of the plan is taken, chosen from its words alone, and stated.
- **What it means for a trader** follows from the status and the plan's forecast:
  - confirmed: the action the forecast describes is supported;
  - rejected: a reason to refuse it;
  - inconclusive: no action yet.

  It is not written out again.
- **The verdict is about the idea's reality, judged before costs.** Whether the book pays is branch 3's question (`06_profitability`).

## The fields of a verdict
**In `verdict.md`:**
1. **status** (header): confirmed, rejected, inconclusive, not observable or mismatch. A plan's minimum counts are applied first: below one, the status is "not observable", whatever the other numbers.
   - For: the answer.
   - Used by: the operator, and whatever decides what to do with the idea.
   - Without it: no answer.
2. **Situation check:** the share of active bars that are bars of the plan's situation, on its side.
   - For: knowing the verdict is about the idea, not about a faulty config.
   - Used by: the operator, and step 3 when it is a mismatch.
   - Without it: a wrong config gives a confident, wrong verdict.
3. **Evidence** (not for a mismatch):
   - the main measure: its value, its test statistic, and the plan's threshold;
   - the supporting check, its value and whether it passed; it counts in the decision: a main measure that confirms with a failed check gives inconclusive (operator, 2026-11-14; code refuses a "confirmed" with a failed check);
   - the counts: every count the plan's minimums refer to, each one named;
   - the rule the numbers meet ("decided by");
   - the literal reading taken ("reading").
   - For: the status can be checked and challenged.
   - Used by: the operator, and anyone who disputes the status.
   - Without it: a bare word nobody can verify.
4. **plan, idea and fit** (header, copied by code), and the links to the plan and the record.
   - For: tracing the verdict, and keeping an "adapted" test from being read as the idea word for word.
   - Used by: the operator.
   - Without it: "confirmed" can be read as more than was tested.

**Next to it:**

5. **`measure.py`:** the function that produced the numbers.
   - For: auditing them.
   - Used by: the reading of each exercise, and anyone who disputes a number.
   - Without it: the numbers cannot be checked.
6. **`result.json`:** what the function returned, as it returned it.
7. **The index line** (`INDEX.md`): `<plan id>: <status> (fit: exact|adapted) [main: <value>; <statistic>; <counts>]`, or `<plan id>: no verdict: <why>` for a plan with no record (untestable, missing-components, or refused by the engine).

## Storage and naming
Aligned with the other steps.

```
05_verification/
  card.md                      this card
  helper/
    system_prompt.md           the helper's instructions
    record_description.md      how a backtest record is given to the function (pasted into each call)
    make_verdict.py            one closed-book call writes measure(bars); a small runner executes it on the record; saves the verdict
  verdicts/
    INDEX.md                   one line per plan
    REVIEW.md, run_log*.txt    once a real run has filled it
    <plan id>/                 one folder per verdict: verdict.md, measure.py, result.json
  exercise_k/                  the exercises
  planted_test/                step 5 on copies of real records with a known gain planted (not market evidence)
  hourly_run/, full_data_run/  the verdicts of named runs (each with REVIEW.md)
```

## The AI and the runner
**The mechanism.** A model call writes a short function from the plan; a small fixed runner executes it on the record. This is the same pattern as steps 3 and 4: in step 3 the model writes a config, and the engine runs it.
- **Neither pure option works.** A model reading thousands of bars cannot measure reliably. Fixed code covering every criterion would be heavy, and would break on the next new criterion.
- **The fixed code is small:** it loads the bars, runs the function, and checks what comes back. The per-plan logic is generated, not maintained.

**Closed book.** One call per plan, with no tools and no data. The request holds:
- the plan and its config;
- `record_description.md`;
- the coins, windows, number of bars and columns of this record (names, not values).

**The runner** loads the record into `bars[coin][window]` (pandas DataFrames). It runs the function in a separate process, with the venv's Python, isolated (`-I`), and checks the returned dict.

**Checks in code** (`make_verdict.py`). It refuses only a major deviation, and sends the error back, up to three attempts:
- no function `measure(bars)`;
- no situation check, or a status that does not agree with it (mismatch exactly when the check fails);
- the function fails on the record;
- a result that is not a dict;
- a status that is not one of the five;
- no main measure value; a statistic that is not a dict with a value; no named counts;
- no "decided by", no "reading".

**Model.** Opus, as in steps 1 to 3. **Cost.** About 0.08 USD and 20 to 30 seconds per plan.

**Prompt**: `helper/system_prompt.md`.

## Quality criteria on the verdict
- **The situation check is computed from the Fidelity and the raw indicator values,** and a mismatch stops the verdict.
- **The function applies the plan's criterion as written:** the same horizon, main measure, supporting check, thresholds and minimum counts. Nothing is added.
- **The status follows from the numbers and the plan's rules,** and "decided by" names the rule met.
- **Returns stay inside a window,** and the windows are not joined.
- **The "reading" states every open detail,** resolved literally.
- **The same plan gives the same status on a rerun.** A difference shows a criterion read two ways, which is a fault of the plan.

## Fixed inputs for the iterations
The 15 daily plans of `03_test_plan/plans/` whose outcome is `plan` (13 with a backtest record; `003-01` and `003-02`, refused by the engine, have none), and the 14 refusals, which must give "no verdict". Until exercise 7, the plans written before the symmetric criteria.

## Variants compared
- **Exercises 1 and 2:** the same helper, run twice. 14 of 15 statuses agree; the plans' open details explain the rest.
- **Exercises 3 and 4:** conventions for open details, and a clearer result format (value and statistic separate, named counts). 13 of 15 identical numbers; one status still flips.
- **Exercises 5 and 6:** two more conventions (weighted mean, counts only). 15 of 15 statuses agree.
- **Exercise 7:** the situation check. It flags two real config faults (002-02 at 0 %, 003-05 at 19 %); every correct plan scores 100 %.
- **Exercise 8 and `verdicts/`:** the rewritten plans, run twice. 13 of 13 statuses agree (all inconclusive); every situation check passes.
- **The planted test:** step 5 confirms (t 5.5) and rejects (t -4.1) a planted gain, in the right direction; a realistic gain on one fold stays inconclusive (`planted_test/reading.md`).
- **Exercises 9 to 11:** "not observable" split from "inconclusive" by the plan's minimum counts. 13 of 13 statuses agree on the fixed inputs (all inconclusive: every minimum reached); two records cut to one window give "not observable" twice.
- **The full-data run:** 5 "rejected" verdicts came from the plans' per-window holding reference, a bias fixed in step 3; rerun, 6 of 6 inconclusive (`../FULL_DATA_RUN.md`).

## Who judges the output
The operator: "does this verdict apply my plan's rule, and would I accept it?". Code checks the shape of the result. Each exercise has a one-page reading: the functions are read against their plans, and the two runs are compared.

## Done when
On two exercises in a row, every verdict meets every criterion, and the two runs give the same status for every plan. Status: met by exercises 9 and 10, with "not observable" (`exercise_9/reading.md`): the same status for all 13 plans (`exercise_8/reading.md`).

## Open
- **A coin without data** (BNB, for the RSI ideas): the function takes the plan's rule literally on the coins present and says so in "reading". Parked with the quality of the backtest output.
- **An ambiguous criterion** is a fault of the plan. In exercise 8, four plans gave different numbers between runs (the baseline of an excess return, the neutral group, the standard error); no status changed. The conventions cover the common open details. The lasting fix is in step 3: a plan should state how its non-overlapping samples are drawn and which test it uses. Proposed, not made.

## What this step does not do
It does not change a criterion, judge costs or profitability, or rerun a backtest.
