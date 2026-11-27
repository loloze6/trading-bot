# Function card: run_brief (orchestration, 2026-11-17; validated: `validation/reading.md`, the operator's ruling on the theme path, 2026-11-17)

A function card, not a step card: no model of its own, so no prompt and no model variants. Like `loop`, it has what
a step card has not: its sequence, its stop rules, failures, where its state lives.

## Business objective, one question
Which of a theory's ideas are real and pay, and where do the analysis lines lead from them?

**Establish, from one trading theory, its ideas and the chain of tested ideas that follows from them, chosen by
one rule fixed in advance, until a stop rule is met, so that a theory is researched from end to end without the
operator picking each next step.**

## Input and output
- **Input:** a run name, and one of: a brief (step 1's file), a theme in the operator's words, or a source the
  operator pastes (step 1 then writes the brief); an optional budget.
- **Output:** the brief (in step 1's list and in the run), its ideas (step 2), and everything `loop` produces in the
  run: each tested idea's row, journal and logs, the queue, the turns; the run's consumption.

## What a run of a brief is
**A run of a brief is step 1 (only when the input is a theme or a source), then step 2 on the brief, then `loop` in
the same run: each turn tests the idea `select_next` ranks first among the brief's ideas and the ideas the step 7
lines propose from them, until a stop rule is met.**

- **It adds no rule of its own.** Steps 1 and 2 are called as validated; the next idea is `select_next`'s; the stop
  rules are `loop`'s. A brief's ideas and the lines' ideas compete in one queue, by one score.
- **One run can hold several briefs.** Called again on the same run with another brief, it adds that brief's ideas
  to the same queue; the loop goes on with all of them.
- **Its state is the run's files.** Stopped for any reason, it resumes: a step whose output exists is not called again.

## The sequence
1. **Step 1** (theme or source only): `01_brief/helper/make_brief.py`, writing in step 1's list of briefs
   (`01_brief/briefs/`): the brief gets the next free number, and the list of briefs already written keeps a theory
   from being written twice. "Not researchable" ends the call: no brief, no run.
2. **The brief in the run:** copied to `01_brief/<run>/briefs/`, where the run's ideas find it.
3. **Step 2:** `02_ideation/helper/make_ideas.py` on the brief, writing in `02_ideation/<run>/ideas/`. Skipped when
   the run already holds ideas of this brief. "No ideas" ends the call, with step 2's reason.
4. **`loop`** on the run, without a starting idea: the brief's ideas are its first candidates.

Steps 1 and 2 are two functions (`write_brief`, `write_ideas`) the loop also calls, to turn a discovery into a brief
(`../loop/card.md`, "Discoveries become briefs"; topic 50): one way to write a brief and its first ideas. A brief
written from a discovery gets a `discovery:` header field (the discovery's id), written by code: `select_next` ranks its
ideas as follow-ups of the idea it was found in (next steps 1n, 2026-11-25).

## Stopping
`loop`'s rules, unchanged: the operator stops it (it resumes); an optional budget is reached (`--budget USD`, the
run's total, steps 1 and 2 included: the loop counts them in the run's spend, from this function's journal); no
candidate is left. No default limit.

## When a step fails
Step 1 or step 2 failing (no valid answer) ends the call, with the step's message; nothing is half-written (the steps
write their files whole). An idea that fails inside the loop is `loop`'s rule: marked, not retried, the loop goes on.

## Visibility
- **The journal** (`orchestration/run_brief/<run>/journal.jsonl`): one line per call of step 1 or step 2: the time,
  the brief, the step, called or skipped, its USD and seconds, the files it wrote, its log.
- **The logs** (`orchestration/run_brief/<run>/logs/<brief>/<step>.txt`): each step's own output.
- **What the loop did:** `loop`'s queue and turns, and `run_idea`'s table, journal and logs, unchanged.

## Storage
```
orchestration/run_brief/
  card.md                    this card
  helper/run_brief.py, test_run_brief.py
  validation/reading.md      once validated
  <name>_run/
    journal.jsonl            one line per call of step 1 or 2
    logs/<brief>/            each step's output
(the brief: 01_brief/briefs/ and 01_brief/<name>_run/briefs/; its ideas: 02_ideation/<name>_run/ideas/; the loop:
 orchestration/loop/<name>_run/; the tested ideas: orchestration/run_idea/<name>_run/ and the steps' <name>_run/ folders)
```

## How to call it
```
python3 orchestration/run_brief/helper/run_brief.py --run NAME_run --python VENV_PYTHON
    (BRIEF_FILE | --theme "TEXT" | --source FILE) [--budget USD] [--model MODEL] [--data-use 2]
    [--target-box auto | --target-box "rising agitated, long"]
```
Called again with the same brief on the same run, it resumes. Called with another brief, it adds it to the run.

**`--data-use 2`** (2026-11-26, `../../runs/BUILD_A4_RESEARCH.md`; `../../common/data_use.md`): the run in the new data
use. Before step 1, it writes `orchestration/loop/<run>/data_use.json` once: `{"version": 2, "research_coins": the run's
8 coins (common/coins.py, research_draw: seeded by the run's name), "windows": "04_backtest/windows/research_2016.json"}`
(the file other helpers read; resumed, it is kept as written, with or without the flag). `run_idea` then backtests every
plan of the run on those coins and windows; step 7 explores the explore half, step 5 checks on the check half
(`../../common/explore_and_check.md`). Refused: a run that has already tested ideas without it (`run_idea`'s
`table.json` exists), or whose file names another version. Without the flag, nothing changes.

**`--target-box auto` or `--target-box "rising agitated, long"`** (2026-11-27, next steps B2.1;
`../../common/target_box.md`; `../../runs/BUILD_B2_1.md`): the run's target box, the box (a market profile and a side)
where it searches. `auto` applies the rule (the box with the most market days per strategy whose idea names it exactly:
share / (1 + count), from the profile map); a box in words is the operator's choice. Before step 1 (after the data use),
it writes `orchestration/loop/<run>/target_box.json` once: the profile, the side, who chose it, and for the rule its
table of the twelve boxes. Resumed, the file is kept (with or without the option); a call naming another box is
refused. Then `select_next` lists the ideas not acting in the box as outside it (the loop tests only the others), and
line 7.g is told to look there first. Without the option, nothing changes.

## Checks in code
Refused before any call: a run name not ending in `_run`; none or more than one of brief, theme, source; a brief file
that does not exist; a budget that is not a positive number; a target box that is not `auto` or one of the twelve boxes.

## Done when
On one brief from step 1's list, with a small budget: step 2 writes the brief's ideas in the run, the loop's first
turn tests the idea `select_next` ranks first among them, the loop goes on with the lines' ideas, stops on the budget
and says so, and a second call makes no model call for steps 1 and 2.
Status: **met** (`validation/reading.md`).

## What this function does not do
It does not judge an idea, change a step, choose which theory to research (the operator or step 1 does), or test on
data the analysis did not see.
