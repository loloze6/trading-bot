# Step 7: the analysis lines, shared part (2026-11-12)

Step 7 is a set of analysis lines, each with its own objective and its own card: 7.a to 7.g. This card holds what they share: input, output, how they read the data, the model, storage. A line's card holds only its objective, its entry condition, what it looks for and what it proposes.

| Line | Card | Entry condition | Objective |
|---|---|---|---|
| 7.a | `../07a_not_observable/` | step 5: not observable | why the idea could not be observed, and how to make it observable |
| 7.b | `../07b_inconclusive/` | step 5: inconclusive | why the result is unclear, and what idea would give a clear answer |
| 7.c | `../07c_rejected/` | step 5: rejected | why the idea was rejected, and what other idea could be confirmed |
| 7.d | `../07d_not_profitable/` | step 6: not profitable enough | why the book does not pay, and what idea would make it pay |
| 7.e | `../07e_profitable_unproven/` | step 6: profitable enough, step 5: not confirmed | what the book really earns from |
| 7.g | `../07g_patterns/` | none | what patterns the bars and the book show |

## Input (every line)
One backtest record (its bars, its trades, its book day by day; its explorations see the exploration folds only, B
and C: see "How it reads the data"), the idea it tested (the fields step 3 reads: brief, data lines, Idea, Consequence; found by the plan's idea id, or `--idea`; operator, 2026-11-15), the plan it ran and its brief, step 5's verdict on the idea and step 6's check of the book, **the idea's size and what one
trade cost the backtest** (operator, 2026-11-20): step 5's `size.json` ("not measured" when the verdict has none), and
the cost of a trade the backtest applied, read from its record (`../common/measures.md`, "The cost of a trade"). Why:
of 103 confirmed ideas that did not pay, 53 had a move per case smaller than the cost of a trade, and none of those
paid (`../runs/RETRO_DIAGNOSIS_RUN.md`); a line that does not see it proposes more ideas of the same small kind.

## Output (every line)
One analysis per backtest: findings, then ideas, each idea in step 2's format, or "no ideas" with the reason.

## What an analysis is
**An analysis is a practitioner's reading of one backtest, for one line's objective: findings drawn from the backtest's own data on the exploration years, each with its numbers, and the ideas they suggest, each resting on named findings.**

- **Findings first, ideas second.** An idea names the findings it rests on; an idea no finding supports is not written.
- **The ideas are ideas, not test plans.** A test plan is written closed book (step 3), so that it cannot be shaped by data already seen; the analyst has seen the data.
- **It chooses on some years; its ideas are checked on others** (operator, 2026-11-24; `../common/explore_and_check.md`).
  The analyst explores folds B and C (2018 to 2021); step 5 then requires a confirmed idea to point its way on folds A
  and D (2022 to 2025) too. Why: an idea chosen after looking at results looks better than it is on the years it was
  chosen from.
- **It proposes; it changes nothing.** What is done with its ideas is decided outside the step.

## The fields of an analysis
**In `analysis.md`:**
1. **Header:** the line, the backtest, the idea tested, step 5's verdict, step 6's check, the mode, the number of explorations, the cost.
   - For: tracing the analysis.
   - Used by: the operator.
   - Without it: an analysis cannot be traced to its backtest and its entry condition.
2. **Findings** F1, F2, ...: one sentence each, with the numbers from the explorations that support it, the most important first.
   - For: what the data shows, checkable.
   - Used by: the ideas (field 3), the operator.
   - Without it: ideas with nothing to stand on.
3. **Ideas:** each with its id, the findings it rests on, and its sentence; or "no ideas" with the reason.
   - For: the line's proposal.
   - Used by: the operator, and step 3 if an idea is taken further.
   - Without it: the analysis gives no direction.

**Next to it:**

4. **One file per idea** (`ideas/<id>.md`), in step 2's format: a header (the brief, the source idea, the line, the backtest, the data lines copied from the tested idea, or the idea's own when it is about other data), then `Idea:`, `Consequence:` and `Why:` (the findings it rests on, in full).
   - For: an idea step 3 can read as it reads step 2's ideas.
   - Used by: step 3.
   - Without it: an idea cannot be tested.
   - **Id:** `<tested idea id>.<line letter><n>_<short name>`, for example `002-03_price-cross-above-long-sma.d1_above-average-with-rising-month`.
5. **The explorations** (`exploration/round_k.py` and `round_k_result.txt`): each function the model wrote and what it returned.
   - For: every number in a finding can be traced; the number of looks at the data is known.
   - Used by: the operator.
   - Without it: findings cannot be checked.
6. **`result.json`** (the same, for code) and **the index line** (`analyses/INDEX.md`): `<backtest>: <n> ideas (<k> explorations)`, `<backtest>: no ideas: <why>`, or `<backtest>: not run: entry condition not met (step 5: ...; step 6: ...)`.

## Storage and naming
```
07_common/
  card.md                      this card
  helper/
    analyse.py                 one line, one backtest: entry condition, rounds, answer, saved files
    common_rules.md            the shared part of every line's instructions (role, input, how to explore, findings)
    output_one_call.md         the answer's format, one call (findings, then ideas)
    data_description.md        how the backtest's tables are handed to the code; their columns: ../common/backtest_record.md
    test_analyse.py            tests of the code checks
  validation/reading.md        the readings of the one-call choice
  validation_run/ideas/        the ideas the validation run tested (written by the lines)
07x_<line>/
  card.md                      the line's card
  helper/
    line.yaml                  id, name, entry condition
    line_prompt.md             the line's objective, what it looks at, what it proposes
  validation/reading.md        the reading of the exercises that validated the line
  analyses/                    created by analyse.py when it runs (default): INDEX.md, <backtest>/ with analysis.md, result.json, ideas/, exploration/
```

## The AI
**How it reads the data.** The model never sees the rows. It writes one Python function per round, `explore(data)`, over three tables: the bars, the trades, the book day by day (`helper/data_description.md`). A separate, isolated process runs it on the record with the venv's Python and returns aggregates only: at most 40 rows per result, every date hidden. At most three rounds, then the answer. Every function and its result are kept.
- **The exploration folds only.** The tables hold the windows of folds B and C (`exploration_windows`, from the plan's
  fold order: `common/lib.py`); the description of the record lists those windows, and the request says that folds A
  and D are kept to check its ideas. A backtest not run on its plan's folds (no `fold_` folder) is explored whole.
- **What it still reads on every fold:** step 5's verdict, step 6's check and the idea's size of the tested idea:
  summaries of the parent idea, not of the ideas it will write.

**Closed book,** as in steps 1 to 3 and 5: no tools, no files, no web; what it needs is pasted into the call (the brief, the plan, its config, the verdict, the check, the data description, the earlier rounds).

**One call:** the same model explores, writes its findings, then its ideas (chosen over an analyst-then-deducer split, see "Variants compared").

**Checks in code.** They refuse only an answer they cannot read, and send it back (three attempts): no findings; an idea without its sentence, consequence or findings; an idea resting on a finding that does not exist; a field over 300 words; neither ideas nor "no-ideas"; a `same-idea-on:` block (the tested idea unchanged, on other data) whose data is not in `../common/data_available.md`. For that block, code copies the tested idea's Idea and Consequence into the idea file. A function that fails returns its error as the round's result, without any file path. Code also refuses a period named by its months and year (a month name next to a year, a quarter with its year, a year and month written as numbers): periods are named by window or by year. The verdict and check text given to the model carry no path lines.

**Model.** Opus. **Cost.** About 0.3 USD and 1 to 2 minutes per analysis.

**Prompts.** `helper/common_rules.md` + the workflow's measuring definitions (`../common/measures.md`) + the line's `line_prompt.md` + `helper/output_one_call.md`, with the definition of an idea (`../common/idea_definition.md`); shared files are pasted where a prompt names them (`{{NAME}}`).

## Quality criteria (every line)
- **Every finding states its numbers,** and they are in its exploration results.
- **Every idea rests on named findings** and follows from them.
- **Every idea meets the definition of an idea** (`../common/idea_definition.md`, the same as step 2's).
- **The line keeps to its objective:** it looks where its card says, and proposes what its card says.
- **No dates** in what it writes.

## Variants compared
- **One call against analyst then deducer,** on the same backtests (exercises 1 and 2): one call kept (blind quality 9 of 16, ideas found again on a rerun 59 % against 42 %, fewer values fitted to the data, cheaper; `validation/reading.md`).
- **Exploring folds B and C only (2026-11-24):** a real analysis (7.g on 001-01...c1, 2 rounds allowed, 0.31 USD) whose
  exploration results name windows w7 to w18 only; a test proves the tables and the record's description hold those
  windows alone (`helper/test_analyse.py`).
- **To try later:** a fixed query format instead of Python functions, if the functions prove hard to control.

## Who judges the output
The workflow: a line is relevant when one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to the line (each line's card says which). The operator reads the findings ("are they true and important?"). Code checks the shape.

## Done when
Each line's own card says when the line is done. The parts every line shares (the call, the explorations, the
checks in code, the files) are done when, on two exercises, the lines' analyses meet the quality criteria above.
Status: **met** for the shared parts and lines 7.a, 7.b, 7.d, 7.g (`validation/reading.md`); 7.c and 7.e in their own
folders' validation.

## To observe in the tests
- **Durations in ideas.** Settled (operator, 2026-11-15): an idea states its time in real time (its horizon, and the past period of its situation), never in bars; levels and thresholds stay out (`../common/idea_definition.md`). Before: Exercise 1: almost every idea names values, some inherited from the plan, some new and found in the data (`validation/reading.md`).
- **How many looks at the data** a line takes before its ideas.
- **Ideas after a move too small for its cost** (since 2026-11-20): do they make the move larger (a longer horizon, a
  stronger situation), and do those ideas pay when tested? First read: `../runs/STEP7_SIZE_AB_RUN.md`.

## What the lines do not do
They do not test an idea, write a test plan, change a backtest or a rule, or decide what is done with their ideas.
