# Step card 5: Verification (2026-11-10)

## Business objective, one question
Is this idea real?

**Establish, on evidence fixed before the data was seen, whether the market confirms the idea, shows no effect, or does not yet say, and what that result means for a trader's decisions.**

## Input
One test plan whose outcome is `plan`, and its backtest record. One idea has one plan, so this is one input per idea.

## Output
One verdict per plan: **confirmed**, **inconclusive** (unclear: a sign of the effect, not enough proof; or confirmed on
every fold but pointing the other way on the check folds), **no effect** (enough cases, and the effect near zero or
pointing the other way: the data shows it absent; B11, operator 2026-11-27) or **not observable** (fewer cases than the plan's minimum: the data could not show the idea), with the evidence that decided it. Or **mismatch**, when the test does not do what its plan says: no verdict on the idea, and the plan goes back to step 3. The five answers are defined once, in `../common/verdicts.md`.

## What a verdict is
**A verdict is the plan's own criterion, applied unchanged to the backtest record: the numbers measured, and which of the plan's rules (confirm, reject, inconclusive) they meet.**

- **First, the test must match its plan.** From the plan's Fidelity lines (the situation, and the side the outcome expects) and the record's raw indicator values, the function checks that the config's forecast is active on the bars of that situation, on that side. Below 90 % agreement, the status is "mismatch" and the criterion is not applied. The check reads the Fidelity, not the plan's Forecast line or its config, because those two are what may be wrong. Found by exercise 6's review: the down-cross plan (002-02) went short in up-trends, and nothing in steps 3 to 5 saw it.
- **The criterion was fixed before the data.** The verdict applies it and never adjusts it: no new measure, no other threshold, no other horizon.
- **No effect, one rule for every plan** (B11, operator 2026-11-27; `../common/verdicts.md`). The plan's criterion has
  three rules (confirm, reject, inconclusive). Its reject rule met ("rejected", t at most -2) is **no effect**; and an
  inconclusive result is **no effect** when the measure counts at least 30 cases (the confirmation's minimum) and the main
  measure's t, counted in the idea's direction (the side of the plan's confirm rule), is below 1. Otherwise it stays
  inconclusive: a sign of the effect, which a clearer test may confirm (line 7.b). Why: on nights 7 to 9, 308 of 477
  results were unclear and 1 rejected; the follow-ups of an unclear test with t below 1 were confirmed 10 times in 72
  (14 %, 2 profitable), with t from 1 to 2, 17 in 56 (30 %, 7 profitable). The rule is applied by code
  (`make_verdict.py`, `effect_check`), after the criterion and the direction check: the model applies the plan's
  three rules and is not told of it. Records before 2026-11-27 keep their words; an old "rejected" is read as "no effect".
- **When the criterion leaves a detail open,** the workflow's measuring definitions apply (`../common/measures.md`); what the record holds is `../common/backtest_record.md` (shared with steps 3 and 7). Otherwise the most literal reading of the plan is taken, chosen from its words alone, and stated.
- **What it means for a trader** follows from the status and the plan's forecast:
  - confirmed: the action the forecast describes is supported;
  - no effect: no reason to take it (the effect is absent, or the other way);
  - inconclusive: no action yet.

  It is not written out again.
- **A confirmed idea also points its way on the years step 7 does not see** (operator, 2026-11-24;
  `../common/explore_and_check.md`). The verdict is judged on every fold; a "confirmed" is then checked on the check
  folds (A and D, 2022 to 2025) alone, with the same measure: if it points the other way there, the status is
  "inconclusive". Why: step 7 chooses its ideas on what it explored; an effect that exists only in those years is not an
  effect to trade. **In the new data use** (a record holding `data_use.json`, `common/data_use.md`): judged on every
  window, checked on the check half (the windows from 2022) alone; `direction_check` names `half` in place of `folds`
  (2026-11-26, `runs/BUILD_A4_RESEARCH.md`).
- **The verdict is about the idea's reality, judged before costs.** Whether the book pays is branch 3's question (`06_profitability`).
- **Next to the verdict, the idea's size** (operator, 2026-11-20): how large its effect is, not only whether it exists.
  Computed by code from the record's prices and forecast (`../common/measures.md`, "The size of an idea";
  `../common/idea_size.py`): per case (a signal of the idea), the unusual move over the horizon net of the coin's normal
  drift, the drift in the signal's direction, the total, and the strength (the unusual move as a share of the coin's
  usual move over the horizon). No cost enters it and it does not change the status: the status says "real or not",
  the size says "how large". Why it matters: of 103 confirmed ideas that did not pay, 53 had a move per case smaller than
  the cost of a trade (`../runs/RETRO_DIAGNOSIS_RUN.md`).

## The fields of a verdict
**In `verdict.md`:**
1. **status** (header): confirmed, inconclusive, no effect, not observable or mismatch (before 2026-11-27: "rejected" in place of "no effect"). A plan's minimum counts are applied first: below one, the status is "not observable", whatever the other numbers.
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
   - the literal reading taken ("reading");
   - the direction check, for a confirmed verdict (one line: agrees, disagrees or not judged, and why);
   - the effect check, for an inconclusive or rejected result of the criterion (one line: no effect or unclear, the t in
     the idea's direction and the cases).
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
6. **`result.json`:** what the function returned, as it returned it; for a confirmed verdict, with `direction_check`
   added by code (the check folds, agrees: true, false or null for not judged, why, the main measure, its statistic and
   the counts on the check folds alone).
   - For: auditing the check, and the status it changed.
   - Used by: the operator, and the reading of each run (how many confirms the check turned to inconclusive).
   - Without it: a status changed by code with no trace of why.
   For an inconclusive or rejected result of the criterion, with `effect_check` added by code (no_effect: true or
   false, why, the t in the idea's direction, the cases): the trace of a "no effect".
6b. **`size.json`:** the idea's size (cases, unusual move and how sure it is (its t by day, and the days), normal drift, total move, the coin's usual move, strength),
   with one line in `verdict.md` ("Size: ..."). Not for a mismatch.
   - For: telling a real but small idea from a real and large one.
   - Used by: the operator, step 7, and whoever compares an idea's size with what a trade costs.
   - Without it: "confirmed" says nothing of whether the effect can ever pay.
7. **The index line** (`INDEX.md`): `<plan id>: <status> (fit: exact|adapted) [main: <value>; <statistic>; <counts>]`, or `<plan id>: no verdict: <why>` for a plan with no record (untestable, missing-components, or refused by the engine).

## Storage and naming
Aligned with the other steps.

```
05_verification/
  card.md                      this card
  helper/
    system_prompt.md           the helper's instructions
    record_description.md      how a record is handed to the function; its columns: ../common/backtest_record.md
    make_verdict.py            one closed-book call writes measure(bars); a small runner executes it on the record; saves the verdict
  verdicts/                    created by the helper when it runs (default):
    INDEX.md                   one line per plan
    REVIEW.md, run_log*.txt    once a real run has filled it
    <plan id>/                 one folder per verdict: verdict.md, measure.py, result.json, size.json
  validation/reading.md        the reading of the exercise that validated this card
  planted_test/                a test set: copies of real records with a known gain planted (not market evidence)
  cut_records/                 a test set: two real records cut to one window of one coin, with their plans, verdicts, ideas and briefs (7.a's fixed inputs)
  full_data_run/, hourly_run/, validation_run/   the verdicts of named runs
```

## The AI and the runner
**The mechanism.** A model call writes a short function from the plan; a small fixed runner executes it on the record. This is the same pattern as steps 3 and 4: in step 3 the model writes a config, and the engine runs it.
- **Neither pure option works.** A model reading thousands of bars cannot measure reliably. Fixed code covering every criterion would be heavy, and would break on the next new criterion.
- **The fixed code is small:** it loads the bars, runs the function, and checks what comes back. The per-plan logic is generated, not maintained.

**Closed book.** One call per plan, with no tools and no data. The request holds:
- the plan and its config;
- `record_description.md`;
- the coins, windows, number of bars and columns of this record (names, not values).

**The runner** loads the record into `bars[coin][window]` (pandas DataFrames). It runs the function in a separate process, with the venv's Python, isolated (`-I`), and checks the returned dict. For a confirmed verdict it runs the same function a second time on the check folds' windows only (no model call): the direction check.

**Checks in code** (`make_verdict.py`). It refuses only a major deviation, and sends the error back, up to three attempts:
- no function `measure(bars)`;
- no situation check, or a status that does not agree with it (mismatch exactly when the check fails);
- the function fails on the record;
- a result that is not a dict;
- a status that is not one of the plan's five (confirmed, rejected, inconclusive, not observable, mismatch: the
  function applies the plan's rules; "no effect" is then decided by code);
- no main measure value; a statistic that is not a dict with a value; no named counts;
- no "decided by", no "reading".

**The direction check in code** (`direction_check`, `common/lib.py`'s fold windows): it agrees when the check folds'
main measure has the sign of the main measure on every fold; it disagrees otherwise, and the status becomes
"inconclusive" with a "decided by" that says so. It is **not judged**, and the verdict stands, when the check folds hold
under 100 cases or 30 days (read from the measure's own counts: the smallest count named "case", else the smallest
count; a count named "day"), when the measure cannot run on them alone, when the plan has no check fold, or when the
record did not run on the plan's folds (an unseen-dates record: no `fold_` folder).

**The effect check in code** (`effect_check`, `../common/verdicts.md`): the plan's reject rule met gives "no effect";
an inconclusive result gives "no effect" when its counts hold at least 30 cases (read as the direction check reads
them) and its t, times the side of the plan's confirm rule (the sign of the first t threshold in its "Confirm:" line:
-1 for `t ≤ -2`), is below 1. Without a t or a t threshold the result stays inconclusive. Recorded in `result.json`
(`effect_check`) and in one line of `verdict.md`.

**The same criterion on another record** (`--measure FILE`, 2026-11-18, `runs/UNSEEN_RUN.md`): an earlier verdict's
`measure.py` is applied as it is to another record of the same plan (other dates, other coins). No model call, one
attempt; the checks in code are the same.

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
- **The direction check (2026-11-24):** 71 verdicts whose bars are on the designer's machine rerun with their own
  `measure.py` (no model call): every field of `result.json` identical but the added check; of the 64 confirmed, 60
  agree, 3 not judged (77 to 90 cases on the check folds), 1 disagrees and becomes inconclusive (019-03, a large
  breakout in a rising market: +0.43 % a case on every fold, -0.007 % on folds A and D). A first pass read only counts
  named "cases" or "days" and left 48 not judged: fixed to read the measures' own count names.
- **No effect (B11, 2026-11-27):** night 9's tested ideas rerun with their own `measure.py` (no model call):
  `../runs/BUILD_B11_B12.md`.
- **The full-data run:** 5 "rejected" verdicts came from the plans' per-window holding reference, a bias fixed in step 3; rerun, 6 of 6 inconclusive (`../runs/FULL_DATA_RUN.md`).

## Who judges the output
The operator: "does this verdict apply my plan's rule, and would I accept it?". Code checks the shape of the result. Each exercise has a one-page reading: the functions are read against their plans, and the two runs are compared.

## Done when
On two exercises in a row, every verdict meets every criterion, and the two runs give the same status for every plan. Status: met by exercises 9 and 10, with "not observable" (`validation/reading.md`): the same status for all 13 plans (`validation/reading.md`).

## Open
- **A coin without data** (BNB, for the RSI ideas): the function takes the plan's rule literally on the coins present and says so in "reading". Parked with the quality of the backtest output.
- **An ambiguous criterion** is a fault of the plan. In exercise 8, four plans gave different numbers between runs (the baseline of an excess return, the neutral group, the standard error); no status changed. The conventions cover the common open details. The lasting fix is in step 3: a plan should state how its non-overlapping samples are drawn and which test it uses. Proposed, not made.

## What this step does not do
It does not change a criterion, judge costs or profitability, or rerun a backtest.
