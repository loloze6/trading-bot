# Function card: loop (orchestration, agreed with the operator 2026-11-16; met on demo_run, `validation/reading.md`)

A function card, not a step card: no model of its own, so no prompt, no model variants. It has what a step card
has not: the turn of the loop, the selection of the next idea, stop rules, failures, where its state lives.

## Business objective, one question
Which ideas should the workflow try next, and what did it learn from them?

**Establish, from one starting idea, a chain of tested ideas in which each next idea is one the analysis lines
proposed, chosen by one rule fixed in advance, until a stop rule is met, so that the workflow follows its own leads
towards ideas that are real and books that pay.**

## Input and output
- **Input:** a starting idea (step 2's or step 7's format) with its brief, a run name, and an optional budget.
- **Output:** every idea it ran, each run by `run_idea` (its row, journal, logs); the queue (every idea proposed in
  the run, with its place in the order and what happened to it); the run's consumption.

## What a loop is
**A loop is a sequence of `run_idea` calls in one run: the first on the starting idea, each next one on the idea the
selection rule picks among those the step 7 lines proposed in the run and not yet tested, until a stop rule is met.**

- **It chooses; the steps judge.** The only decision it makes is which idea comes next, by a rule written here.
- **One idea at a time.** Not "test everything": each turn picks one.
- **Its state is the run's files.** Nothing is kept anywhere else, so a loop stopped for any reason resumes.

## One turn
0. Turn every new discovery of the run into a brief (below).
1. Ask `select_next` for the run's candidates, ranked.
2. Check the stop rules; if one is met, stop and say which.
3. Call `run_idea` on the first candidate; go to 1.

## The selection of the next idea
Delegated to `select_next` (`../select_next/card.md`): the run's candidates ranked by one score (the record of the
line that wrote the idea / (1 + its generation)), the first is the next idea. The loop writes the ranking it used in its queue.

## Duplicates
Found by `select_next`: an idea already tested or already a candidate (same text, same data) is not run again.

## Stopping (operator, 2026-11-16)
The loop has no natural end (every tested idea brings new ones) and no default limit. It stops when:
- **the operator stops it:** it can be stopped at any time and resumed, nothing is lost, and the journal shows the
  spend after every idea;
- **a budget is given and reached** (`--budget USD`, optional): an idea already started is finished;
- **no candidate is left.**

An idea **confirmed with a profitable book** is marked in the queue and the table ("goal reached"); the loop goes on.

## The components step (2026-11-17)
Between two ideas (after an idea's step 7, before the next is chosen), when the run has open wishes (components step 3
could not find), the loop calls the components step (`../../components/card.md`) on the run's open wishes:
- **every 10 turns** since its last call (counted from `loop.jsonl`, so restarts and resumes count right);
- **before stopping for "no candidate left"**: what it builds can unblock ideas, which `select_next` counts as candidates
  again, and the loop goes on.
It is never called twice without a turn between (a call that fails before answering is not repeated), nor once the
budget is reached. Its cost counts in the run's spend. Each call is one line in `loop.jsonl` (`"components"`).

## Discoveries become briefs (operator, 2026-11-24; topic 50)
A discovery is a pattern off a brief's theme that line 7.e or 7.g found (`../../common/theme.md`), written in its
analysis's `discoveries/` folder. Before each turn, the loop turns every discovery of the run not yet handled into a
brief: `run_brief`'s step 1 with the discovery as its source (the brief gets its own number and its own theory), then
its step 2 (the brief's first ideas, in the run). `select_next` ranks those ideas like any brief's: group 1. Once per
discovery: one line in `loop.jsonl` (`"discovery"`: its file, the brief, the number of ideas, or why none). Not once
the budget is reached; a refused model call stops the loop, and the discovery is handled when it resumes. Steps 1 and
2 count in the run's spend.

## When a step fails
An idea whose `run_idea` call fails (a helper error, a step that writes nothing) is marked "failed at step N" with its
log, and the loop goes on with the next idea. It is not retried.

**A refused model call is not a failure of the idea** (2026-11-21, night 3: the account's usage limit refused every
call; the loop marked 138 untested ideas failed in minutes, and turned one idea about 4,000 times). A helper whose model
call the service refused (it never ran: a usage limit, an outage; `common/lib.py`, exit code `SERVICE_REFUSED`) stops
`run_idea` with that code; the loop then writes "not run: the model service refused a call", marks nothing failed, and
stops; the idea is picked again when the loop is resumed. The components step refused the same way stops the loop too.
An idea's **latest** outcome line counts: a "retry" line written after a failure, with its reason, makes it a candidate
again (used once, for the ideas the usage limit marked failed on night 3). The budget holds before every
`run_idea` call, a resumed idea's included (2026-11-21: 29 re-admitted ideas counted as unfinished ran before the
budget check, 58 USD on a 35 USD budget).

## When the loop is stopped mid-idea
An idea whose turn started but whose `run_idea` call did not finish (the operator stopped the loop, the machine
restarted) is finished first when the loop resumes: `run_idea` is called on it again and skips the steps already done.
Without this, its plan would make it count as tested and it would never get its backtest and verdict (found by
night_run, 2026-11-17). The resumed call is written in `loop.jsonl` ("resumed").
**Finished** = the idea's row in `run_idea`'s table was written after its latest turn started (the row's `finished_at`).
So an idea turned again after a row, a refusal the components step unblocked, is unfinished until `run_idea` writes its
row again (2026-11-19: 017-02 was read as finished from its old refusal row, and finished by hand). A row written before
rows carried their end time counts as finished, as before. Proof: the unfinished ideas of all 12 runs, old rule against
new, identical; a test of the 017-02 sequence.

## Where its state lives
Nothing of its own but the queue's rendering: the ideas tested are `run_idea`'s table; the ideas proposed are the step 7
lines' `ideas/` folders in the run, and step 2's for the run's briefs (its own, and its discoveries'); an idea's line and generation are read from its id (`common/idea_created_from.md`). A resumed loop rebuilds
the queue from these files.

## Visibility
- **The queue** (`<name>_run/queue.md`, `queue.json`): every idea written in the run: its line, generation, record,
  score, rank (its parent is its id), and what happened (tested: its step 5 and step 6, a goal marked; candidate:
  waiting; duplicate of; excluded: its call failed).
- **The turns** (`<name>_run/loop.jsonl`): one line per turn: the idea picked, why (its score and its parts), the run's
  USD so far; one line per call of the components step (its summary); one line per discovery turned into a brief.
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
    [--budget USD] [--model MODEL]
```
Without `IDEA_FILE`, it continues with the ideas already in the run (a resumed run, or the brief's ideas `run_brief`
wrote). No limit unless `--budget` is given.

## Checks in code
Refused before any call: a run name not ending in `_run`; a new run with no starting idea and no idea written in it
(`run_brief` writes the brief's ideas first, then calls the loop without a starting idea); a budget that is not a
positive number.

## Done when
On a fixed starting idea, with a small budget: every turn picks the idea `select_next` ranks first, no duplicate is
run, the loop stops on the budget and says so, the queue and the turns say what happened, and a resumed call continues
where it stopped.
Status: **met** on demo_run, budget 4 USD (`validation/reading.md`); the duplicate rule met by the tests only (no
duplicate in that run).

## What this function does not do
It does not judge an idea, change a step, test on data the analysis did not see, or start from a brief.
