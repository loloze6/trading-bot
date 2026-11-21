# Function card: run_idea (orchestration, 2026-11-15)

## Business objective, one question
What does the workflow learn from one idea?

**Establish what the workflow learns from one idea: its test plan, its backtest, whether it is real, whether its book
pays, and what each analysis line reads and proposes, by running the validated steps 3 to 7 in order, unchanged.**
(operator, 2026-11-15)

## Input
One idea file (step 2's or step 7's format), its brief, and a run name.

## Output
The run's files, in each step's `<name>_run/` folder; one row in the run's table; the run's journal (one line per step
call) and the helpers' logs; the ideas the step 7 lines propose, ready for the next idea's run. All of it is
visibility: nothing in it controls a step (operator, 2026-11-15).

## What a run of an idea is
**A run of an idea is the idea taken once through steps 3 to 7, each step called as validated, on the files of the
step before it, and recorded under one run name.**

- **It calls; it decides nothing.** No step is changed, skipped by judgment, or given anything its card does not say.
- **The chart files** (2026-11-17): after step 6 it writes the record's chart files (`04_backtest/helper/chart_files.py`,
  code only), for the run viewer, for every backtest: under the committed names for a backtest confirmed by step 5 or
  profitable enough by step 6, under the local names (ignored by git) for any other; one journal line (`chart_files`).
  The rule is steps 5 and 6's results, not a judgment.
- **The unseen test** (2026-11-18): after step 7, for an idea step 5 confirmed and step 6 found profitable enough, it
  calls `orchestration/unseen_test/` (code only): the plan unchanged on every unseen period; one journal line
  (`unseen_test`). Step 7 has run before it and never reads its files. The rule is steps 5 and 6's results.
- **A step that fails stops it** (2026-11-21, night 3): a called step whose helper fails ends the run of the idea, for
  steps 3 to 6, whose outputs the next step reads (an output left on disk by an earlier call is not read as this call's
  answer: step 3 called again for an unblocked refusal failed on the usage limit, and its old refusal was read instead).
  A step 7 line or the chart files that fail are recorded in the journal and the run goes on. A model call the service
  refused stops the run of the idea at any step with exit code `SERVICE_REFUSED` (`common/lib.py`), for the loop to
  retry later.
- **It stops where a step stops.** A plan that is untestable or misses a component ends the run of that idea (the
  component goes to step 3's wish list, as step 3 does).
- **It can be resumed.** A step whose output for the idea already exists in the run is not called again, but step 3
  for a missing-components refusal the components step has unblocked: it is called again, its new answer replaces the
  refusal, and the run of the idea goes on from there (`../../components/card.md`, "Unblocking"; 2026-11-17).

## The fields of a run's row
In `<name>_run/table.md` (and `table.json`, for code), one row per idea:
1. **idea and parent:** the idea's id and its source idea (the tested idea a step 7 line read; none for a step 2 idea).
   - For: what was run, and where it comes from.
   - Used by: the operator; the selection of the next idea (scope 2).
   - Without it: a result cannot be traced to its idea and its lineage.
2. **step 3:** the plan's outcome (plan, untestable, missing-components).
   - For: whether the idea could be tested.
   - Used by: the operator.
   - Without it: a stopped run looks like a missing result.
3. **step 5 and step 6:** the verdict (status and its statistic) and the check (status and the measures that failed).
   - For: the idea's two answers: is it real, does its book pay.
   - Used by: the operator; the selection of the next idea.
   - Without it: every result must be read in four folders.
3b. **unseen dates** (2026-11-18): for a confirmed and profitable idea, whether it holds on each unseen period
   (`unseen_test`'s index line); "-" for any other.
   - For: whether a paying idea still holds on dates the research never used.
   - Used by: the operator (no step reads it).
   - Without it: an idea reaches live trading on the evidence of its own dates alone.
4. **step 7:** the lines that ran, and the ideas each proposed (their ids), or "no ideas".
   - For: what the run proposes next.
   - Used by: the selection of the next idea (scope 2).
   - Without it: step 7's ideas must be searched for.
5. **consumption:** the USD of the model calls the run made for the idea, and the minutes, in all and per step (the
   table ends with the run's totals, per step).
   - For: what a run costs, and where.
   - Used by: the operator; the stop rules (scope 2).
   - Without it: a run's cost is unknown.
5b. **finished at** (`finished_at`, in `table.json` only, 2026-11-19): the UTC time this call of `run_idea` wrote the
   row, at its end (a refusal at step 3, or the whole run of the idea).
   - For: telling a finished idea from one whose latest turn was cut.
   - Used by: `loop` (its resume rule).
   - Without it: an idea turned again after a row (a refusal the components step unblocked) and cut before its end
     reads as finished, and is never backtested (017-02, intraday_1h_run, 2026-11-19).

**Next to the table:**

6. **The journal** (`journal.jsonl`): one line per step call: the time, the backtest, the step, called or skipped (its
   output exists) , its USD and seconds, its number of model calls and the longest one's seconds, the files it wrote
   (paths from `steps_cards/`), its log. Every model call prints one line in the step's log: its seconds, its tokens
   (input, cache, output and thinking) and its USD. A call killed at the timeout (15 minutes, `common/lib.py`) is
   written so, "cost unknown", in the log and in the journal's action (operator, 2026-11-16). The step's USD is the
   sum of its calls, so the calls made before a step stops are counted.
   - For: auditing a run step by step, a resumed run included.
   - Used by: the operator.
   - Without it: what ran, when, and what it wrote must be pieced together from four folders.
7. **The logs** (`logs/<backtest>/<step>.txt`): each helper's own output, whole (its refusals and retries included).
   - For: reading why a step did what it did.
   - Used by: the operator.
   - Without it: a step's retries and messages are lost.

## Storage and naming
```
orchestration/run_idea/
  card.md                      this card
  helper/
    run_idea.py                one idea -> steps 3 to 7; writes the run's row
    test_run_idea.py           tests of its own logic (no model call, no backtest)
  validation/reading.md        once validated
  <name>_run/
    table.md, table.json       one row per idea run, then the run's consumption (totals, per step)
    journal.jsonl              one line per step call (called or skipped, USD, seconds, model calls, files written, log)
    logs/<backtest>/<step>.txt each helper's own output
The steps' files for the run, in their usual named-run folders:
  01_brief/<name>_run/briefs/              the brief (a copy)
  02_ideation/<name>_run/ideas/            the idea (a copy)
  03_test_plan/<name>_run/plans/           its plan and config
  04_backtest/<name>_run/backtests/        its record
  05_verification/<name>_run/verdicts/     its verdict
  06_profitability/<name>_run/checks/      its check
  07x_<line>/<name>_run/<backtest>/        each line's analysis, with its ideas/
  04_backtest, 05_verification, 06_profitability/<name>_run/unseen_*/   the unseen test's files (confirmed and profitable ideas)
  orchestration/unseen_test/<name>_run/   the unseen test's results
```
A run name ends in `_run` (for example `demo_run`).

## How to call it
```
python3 orchestration/run_idea/helper/run_idea.py IDEA_FILE --run NAME_run --python VENV_PYTHON [--brief BRIEF_FILE] [--model MODEL]
```
- `IDEA_FILE`: the idea (step 2's or step 7's format).
- `--run`: the run's name; its folders are created when needed.
- `--python`: the interpreter of a venv with `trading-bot/requirements.txt` (steps 4, 5 and 7 run code on the record with it).
- `--brief`: the brief file; by default, the brief the idea's header names, found among the steps' brief folders.
- `--model`: the model for steps 3, 5 and 7 (default: each helper's own).

## The AI
None: the function is code only. The steps' own calls are theirs (steps 3, 5 and 7).

**Checks in code:** a run name not ending in `_run`, an idea file without its `brief`, `Idea:` or `Consequence:` line,
or a brief that cannot be found is refused before any step is called. A line whose `helper/line.yaml` says
`active: false` (7.f, on hold) is not run.

## Quality criteria
- **Every step is called as validated:** its own helper, its usual arguments, the run's folders.
- **The row says what the steps' files say:** every status is read from the step's own result file.
- **A second call on the same idea and run makes no model call and no backtest**, and its journal says so.
- **Every step call has its journal line,** and the consumption adds up to the row's cost.

## Fixed inputs for the iterations
The 002-03 repair from 7.d (`07_common/validation_run/ideas/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.md`,
brief 002). What the validation run found: a plan; step 5 inconclusive; step 6 profitable enough; lines 7.b, 7.e and
7.g run (7.a, 7.c, 7.d do not: their entry conditions are not met).

## Variants compared
None.

## Who judges the output
The operator: "is this what running the steps by hand would have given?". Tests check the function's own logic.

## Done when
On the fixed input, every status in the row is the one in the step's own file, the lines that ran are those whose
entry condition held, every file is in its place and in the journal, and a second call makes no model call and no
backtest. (Not "the same statuses as an earlier run": step 3 writes a new plan with a model, and its plan can differ.)
Status: met on the fixed input (`validation/reading.md`), for the operator's review.

## What this function does not do
It does not choose ideas, loop, change a step, or judge a result.
