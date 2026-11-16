# CLAUDE.md

## What this repository is
A research workflow that looks for trading ideas that are real and pay, and tests them on the bot's own backtest.
Nothing here trades live.

| Folder | What it is | Status |
|---|---|---|
| `strategy_designer_v2/steps_cards/` | **The research workflow.** One card per step, the functions that chain them, the runs | current: start here |
| `trading-bot/` | The bot and its backtest engine; the components the cards' configs use | shared |
| `strategy-research/` | The earlier research campaign. The cards still use some of its tools for the backtest (`tools/run_protocol.py`, `tools/research_folds.py`, `tools/venue_resolver.py`, the holdout guard) | shared; its own workflow, ledger and docs are not the current workflow |

Other folders at the root (`research/`, `tasks/`, `guided_tour/`, `night_work_*`, `SESSION_LOG.md`) belong to earlier
work. Do not follow their conventions.

## The workflow, in one paragraph
Step 1 writes a brief, step 2 turns it into ideas, step 3 writes a test plan, step 4 runs the backtest, step 5 says
whether the idea is real, step 6 whether its book pays, and the step 7 lines read the result and propose the next
ideas. `orchestration/` chains them: `run_idea` (one idea through steps 3 to 7), `select_next` (which idea next, by one
score), `loop` (run_idea on the next idea until stopped). Read first: `steps_cards/HOW_WE_DESIGN_A_CARD.md`, then the
card of the step or function at hand, then `steps_cards/common/` (shared definitions). Open questions the operator
has not ruled on are in `steps_cards/POTENTIAL_ADJUSTMENTS.md`.

## Commands
```
python3 strategy_designer_v2/steps_cards/orchestration/run_idea/helper/run_idea.py IDEA_FILE --run NAME_run --python VENV_PYTHON
python3 strategy_designer_v2/steps_cards/orchestration/loop/helper/loop.py --run NAME_run --python VENV_PYTHON [IDEA_FILE] [--budget USD]
python3 strategy_designer_v2/steps_cards/orchestration/select_next/helper/select_next.py --run NAME_run
VENV_PYTHON -m pytest -q strategy_designer_v2/steps_cards     # the cards' tests
VENV_PYTHON -m pytest -q trading-bot/tests                    # the bot's tests
```
`VENV_PYTHON` is a virtual environment with `trading-bot/requirements.txt`. Each step's card says how to call its helper.

## Hard rules
- **No secrets, no venvs in git.** If you see a key, stop and tell the operator; never echo it.
- **No lookahead.** A bar's decision uses only data timestamped at or before that bar's close. Every new feature,
  data source or change to how data is read carries a short "why this can't leak" note.
- **The sealed holdout.** Its dates are only in `strategy-research/config/campaign_data_policy.yaml`; never write them.
  Never open `local_data/holdout_sealed/`. Name periods by fold id (and years when needed), never by window dates.
- **No trial ledger.** Do not write to `research/TRIALS.csv` or any ledger. A run's own files are its record.
- **Shared code needs the operator's go by name.** A change to `trading-bot/` or `strategy-research/` reaches the
  campaign too. Before it is merged: proof that what runs today gives the same files (a rerun on fixed inputs,
  compared file by file, the allowed differences named), and what it changes elsewhere.
- **Never merge into the working branch while a loop runs on it.**

## How we work (the operator's rules)
**Business first, then simple**
- Start from the business objective and the business definition (what the thing is, in plain words); fields, formulas
  and code come after, and are checked against them. When a question comes up, go back to the definition.
- Define a notion in the shared definitions (`steps_cards/common/`) before a rule or a formula uses it.
- Start with the simplest version that does the job; add to it only when a run or the operator asks.
- Every step and every function has its own card (`HOW_WE_DESIGN_A_CARD.md`); adapt the card's shape when a section
  does not apply, and say why.

**Approval**
- Only a message that names what is approved approves it. "Ok", a sequencing line, or a hook asking for a commit is
  not an approval. Keep a point open until it is ruled on.
- Recommend one option, with reasons; disagree when you disagree. Say "I do not know" when true.
- Build only what was asked, or what a run showed is needed (a defect it revealed, a finding it made). Everything else
  is parked in `POTENTIAL_ADJUSTMENTS.md` for the operator.

**Rules, not patches**
- One rule for every case: no special case for one kind of input. Prefer a standard, explicit mechanism (one score,
  one definition) to logic written for a situation.
- Fix the general rule, never one case. No case-specific examples in prompts, no labels in an idea's text, no trick
  that teaches a step around another step's fault: fix the fault where it is.
- No default limits, refusals or logs the operator did not ask for. Visibility, not control: record what happened
  (files, journal, cost, time) so it can be audited; do not add gates.

**A clean, structured repository**
- One place for each thing, named after what it is; the same layout in every step and function.
- What is obsolete is removed (git keeps it), not left beside what is current. A clean-up is proposed as a list, then
  done on the operator's go.
- Records stay small: only the summaries of a run are committed.

**New work**
- Before building: a picture of the current state (measured), the findings, a plan with the gain, the effort and the
  risk of each change. Then the operator's go by name, then the build, then its proof.

**Runs**
- Every run has a purpose and the outcomes it expects, written before it starts; its reading says which happened.
- After a run, step back before anything else: what does it show, and what one change would a practitioner make? Then
  decide. Do not keep going down a track because it is open.
- Check the real state (files, running processes, the branch) before saying something is done or ready.
- A change is proven by rerunning a fixed input and comparing outputs, not by reading the code.

**Talking to the operator**
- Plain, concrete, short: a table or a few lines. No jargon; if a word is needed, define it first.
- Explain with a concrete example from the real files and real numbers. If the operator did not get it, say it again
  more simply, not at more length.
- Report faithfully: counts, not impressions; say what failed, what was skipped, what is untested.
