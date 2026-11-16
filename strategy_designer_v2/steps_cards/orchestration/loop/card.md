# Function card: loop (orchestration, proposed 2026-11-16, for the operator's review)

A function card, not a step card: no model of its own, so no prompt, no model variants. It has what a step card
has not: the turn of the loop, the selection of the next idea, stop rules, failures, where its state lives.

## Business objective, one question
Which ideas should the workflow try next, and what did it learn from them?

**Establish, from one starting idea, a chain of tested ideas in which each next idea is one the analysis lines
proposed, chosen by one rule fixed in advance, until a stop rule is met, so that the workflow follows its own leads
towards ideas that are real and books that pay.**

## Input and output
- **Input:** a starting idea (step 2's or step 7's format) with its brief, a run name, and the stop limits.
- **Output:** every idea it ran, each run by `run_idea` (its row, journal, logs); the queue (every idea proposed in
  the run, with its place in the order and what happened to it); the run's consumption.

## What a loop is
**A loop is a sequence of `run_idea` calls in one run: the first on the starting idea, each next one on the idea the
selection rule picks among those the step 7 lines proposed in the run and not yet tested, until a stop rule is met.**

- **It chooses; the steps judge.** The only decision it makes is which idea comes next, by a rule written here.
- **One idea at a time.** Not "test everything": each turn picks one.
- **Its state is the run's files.** Nothing is kept anywhere else, so a loop stopped for any reason resumes.

## One turn
1. Ask `select_next` for the run's candidates, ranked.
2. Check the stop rules; if one is met, stop and say which.
3. Call `run_idea` on the first candidate; go to 1.

## The selection of the next idea
Delegated to `select_next` (`../select_next/card.md`): the run's candidates ranked by one score (the proposing line's
record x novelty), the first is the next idea. The loop writes the ranking it used in its queue.

## Duplicates
Found by `select_next`: an idea already tested or already a candidate (same text, same data) is not run again.

## Stop rules (the operator sets the limits on each call)
The loop stops at the first that holds, and the queue says which:
- **budget:** the run's USD has reached the limit (an idea already started is finished);
- **ideas:** the number of ideas run has reached the limit;
- **depth:** the next idea would be beyond the limit of generations from the starting idea;
- **empty queue:** no idea left to try.

An idea **confirmed with a profitable book** is marked in the queue and the table ("goal reached"); the loop goes on
unless the call asks it to stop there (`--stop-on-goal`).

## When a step fails
An idea whose `run_idea` call fails (a helper error, a step that writes nothing) is marked "failed at step N" with its
log, and the loop goes on with the next idea. It is not retried.

## Where its state lives
Nothing of its own but the queue's rendering: the ideas tested are `run_idea`'s table; the ideas proposed are the step 7
lines' `ideas/` folders in the run; an idea's generation is read from its `source-idea` chain. A resumed loop rebuilds
the queue from these files.

## Visibility
- **The queue** (`<name>_run/queue.md`, `queue.json`): every idea proposed in the run: its line, parent, generation,
  rank, and what happened (tested: its step 5 and step 6; waiting; duplicate of; not reached: stop rule).
- **The turns** (`<name>_run/loop.jsonl`): one line per turn: the idea picked, why (its rank), the stop rules' values,
  the run's USD so far.
- **What each idea did:** `run_idea`'s table, journal and logs, unchanged.

## Storage
```
orchestration/loop/
  card.md                    this card
  helper/loop.py, test_loop.py
  validation/reading.md      once validated
  <name>_run/
    queue.md, queue.json     every idea proposed in the run and what happened to it
    loop.jsonl               one line per turn
(the ideas' own runs: orchestration/run_idea/<name>_run/ and the steps' <name>_run/ folders)
```

## How to call it
```
python3 orchestration/loop/helper/loop.py --run NAME_run --python VENV_PYTHON [IDEA_FILE [--brief BRIEF]]
    [--budget USD] [--max-ideas N] [--max-depth G] [--stop-on-goal] [--model MODEL]
```
Without `IDEA_FILE`, it resumes the run. Defaults (to decide): budget 10 USD, 8 ideas, depth 3.

## Checks in code
Refused before any call: a run name not ending in `_run`; no starting idea for a new run; a limit that is not a
positive number.

## Done when
On a fixed starting idea, with small limits: every turn picks the idea the rule says, no duplicate is run, the loop
stops on the rule it reports, the queue and the turns say what happened, and a resumed call continues where it
stopped.

## Open (for the operator)
1. Going on after a goal is reached (default) or stopping (`--stop-on-goal`).
2. The default limits.

## What this function does not do
It does not judge an idea, change a step, test on data the analysis did not see, or start from a brief.
