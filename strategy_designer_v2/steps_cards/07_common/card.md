# Step 7: the analysis lines, shared part (2026-11-12)

Step 7 is a set of analysis lines, each with its own objective and its own card: 7.a to 7.g. This card holds what they share: input, output, how they read the data, the model, storage. A line's card holds only its objective, its entry condition, what it looks for and what it proposes.

| Line | Card | Entry condition | Objective |
|---|---|---|---|
| 7.a | `../07a_not_observable/` | step 5: not observable | why the idea could not be observed, and how to make it observable |
| 7.b | `../07b_inconclusive/` | step 5: inconclusive | why the result is unclear, and what idea would give a clear answer |
| 7.c | `../07c_rejected/` | step 5: rejected | why the idea was rejected, and what other idea could be confirmed |
| 7.d | `../07d_not_profitable/` | step 6: not profitable enough | why the book does not pay, and what idea would make it pay |
| 7.e | `../07e_profitable_unproven/` | step 6: profitable enough, step 5: not confirmed | what the book really earns from |
| 7.f | `../07f_real_and_profitable/` | step 5: confirmed, step 6: profitable enough | what could break the idea and its book |
| 7.g | `../07g_patterns/` | none | what patterns the bars and the book show |

## Input (every line)
One backtest record (its bars, its trades, its book day by day), the plan it ran and its brief, step 5's verdict on the idea and step 6's check of the book.

## Output (every line)
One analysis per backtest: findings, then ideas, each idea in step 2's format, or "no ideas" with the reason.

## What an analysis is
**An analysis is a practitioner's reading of one backtest, for one line's objective: findings drawn from the backtest's own data, each with its numbers, and the ideas they suggest, each resting on named findings.**

- **Findings first, ideas second.** An idea names the findings it rests on; an idea no finding supports is not written.
- **The ideas are ideas, not test plans.** A test plan is written closed book (step 3), so that it cannot be shaped by data already seen; the analyst has seen the data.
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
    output_analyst.md          the analyst's format, split mode (findings only)
    deducer.md                 the deducer's instructions, split mode (ideas from the findings, no data)
    data_description.md        the backtest's tables and their columns, given to every call
07x_<line>/
  card.md                      the line's card
  helper/
    line.yaml                  id, name, entry condition
    line_prompt.md             the line's objective, what it looks at, what it proposes
  analyses/
    INDEX.md, REVIEW.md, run_log*.txt
    <backtest>/                analysis.md, result.json, ideas/, exploration/
  exercise_k/
```

## The AI
**How it reads the data.** The model never sees the rows. It writes one Python function per round, `explore(data)`, over three tables: the bars, the trades, the book day by day (`helper/data_description.md`). A separate, isolated process runs it on the record with the venv's Python and returns aggregates only: at most 40 rows per result, every date hidden. At most three rounds, then the answer. Every function and its result are kept.

**Closed book,** as in steps 1 to 3 and 5: no tools, no files, no web; what it needs is pasted into the call (the brief, the plan, its config, the verdict, the check, the data description, the earlier rounds).

**Two modes, to compare:**
- **One call** (the default): the same model explores, writes its findings, then its ideas.
- **Analyst, then deducer** (`--split`): the analyst explores and writes findings only; a deducer, who does not see the data, writes the ideas from the findings.

**Checks in code.** They refuse only an answer they cannot read, and send it back (three attempts): no findings; an idea without its sentence, consequence or findings; an idea resting on a finding that does not exist; a field over 300 words; neither ideas nor "no-ideas". A function that fails returns its error as the round's result, without any file path. Code also refuses a period named by its months and year (a month name next to a year, a quarter with its year, a year and month written as numbers): periods are named by window or by year. The verdict and check text given to the model carry no path lines.

**Model.** Opus. **Cost.** About 0.3 USD and 1 to 2 minutes per analysis (exercise 1: 17 analyses, 5.38 USD; the split costs about 20 % more).

**Prompts.** `helper/common_rules.md` + the line's `line_prompt.md` + `helper/output_one_call.md` (or `output_analyst.md`, then `deducer.md`).

## Quality criteria (every line)
- **Every finding states its numbers,** and they are in its exploration results.
- **Every idea rests on named findings** and follows from them.
- **Every idea meets step 2's definition of an idea:** one coin at a time, one direction, it says something happens, concrete, its situation known at a bar's close.
- **The line keeps to its objective:** it looks where its card says, and proposes what its card says.
- **No dates** in what it writes.

## Variants compared
- **One call against analyst then deducer,** on the same backtests (exercises 1 and 2): one call kept (blind quality 9 of 16, ideas found again on a rerun 59 % against 42 %, fewer values fitted to the data, cheaper; `exercise_2/reading.md`).
- **To try later:** a fixed query format instead of Python functions, if the functions prove hard to control.

## Who judges the output
The operator: "are these findings true and important, and would I test these ideas?". Code checks the shape.

## To observe in the tests
- **Setting values in ideas** ("the 200-day average", "20 bars"). Step 2's definition says no setting value; whether an extra guard is needed is decided by the tests. Exercise 1: almost every idea names values, some inherited from the plan, some new and found in the data (`exercise_1/reading.md`).
- **How many looks at the data** a line takes before its ideas.

## What the lines do not do
They do not test an idea, write a test plan, change a backtest or a rule, or decide what is done with their ideas.
