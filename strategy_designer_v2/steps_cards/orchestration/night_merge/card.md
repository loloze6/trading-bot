# night_merge: the night sessions' branches merged by one tested procedure

(Function card. Sections adapted from `../../HOW_WE_DESIGN_A_CARD.md`: no AI, so no prompt, model or variants; the
rules by file stand where an output's fields would.)

## Business objective, one question
**After a night of parallel research sessions, how are their branches brought into the working branch so that nothing
a session found is lost, nothing is invented, and the result is checked before anyone builds on it?** (next steps 3g;
the operator, 2026-11-24: "continue on our main topic")

Why: night 6's morning merge first used a line-set union. It broke `strategy_components.py` (repeated lines dropped,
classes mixed), and it left the component catalogue stating its class count twice (119 and 117), a fault step 3's model
read until 2026-11-24.

## Input
The names of the night's branches, in the order to merge; the working branch checked out with a clean tree; a venv
(the register's rebuild, the tests).

## Output
One merge commit per branch on the working branch (or the merge stopped, with what stopped it); the similarity
register rebuilt over every book, in its own commit; the brief numbers used twice; both test suites' results. Nothing
is pushed.

## What a merged night is
**Every session's work kept as that session wrote it, in one branch: each file a session changed carries that change;
a file two sessions changed carries both changes, or the merge stops and says where.** The procedure never chooses
between two sessions' versions of the same thing.

## The rules, by file
Git merges every file it can. A conflict is resolved by the rule of its file; any other conflict stops the merge
(`git merge --abort`) and is reported.

1. **The components file** (`trading-bot/strategies/strategy_components.py`): three-way, class by class (each top-level
   class or function a block). A block one session changed takes that version; a block both changed differently stops
   the merge; the other session's new classes come after this one's.
   - For: two sessions building components the same night (night 6: three sessions, four builds, one an existing
     class's new setting).
   - Without it: a line merge interleaves two new classes that share lines (`pass`, docstring lines).
2. **The files sessions append to** (the component catalogue, the component index and journal, step 1's brief index):
   three-way, line by line. Lines both sessions inserted at the same place are all kept, this session's first; lines
   both changed stop the merge.
   - For: every session adds rows; few edit the same row.
   - Without it: a session's rows lost, or two versions of one line kept (the catalogue's two counts).
3. **The catalogue's class count:** derived, never merged: recomputed from the merged components file.
4. **The register's books** (`register/books.json`): merged by key; a book both sessions changed differently stops the
   merge.
5. **The register's pages** (`INDEX.md`, `MATRIX.md`, `COMPARISONS.md`): rebuilt once at the end
   (`ideas_similarities_check.py --all`), as they are derived from the books.

**Checked on every file a rule resolved:** every line of each side kept as often as that side has it (unless the other
side removed it); no line more often than the two sides' additions allow; the components file parses and defines each
class once.

## Storage and naming
Nothing of its own: git's merge commits ("Merge night branch <name> (night_merge: <n> conflicts resolved by rule)") and
the register's rebuild commit. What it prints is the morning's record (the reading quotes it).

## How to call it
```
python3 strategy_designer_v2/steps_cards/orchestration/night_merge/helper/night_merge.py BRANCH [BRANCH ...] --python VENV_PYTHON [--no-tests]
```
A branch is fetched from origin when it is there, else taken locally.

## Checks in code
A clean working tree before it starts; each rule's faults (above); a merge with any fault is aborted, the branches
merged before it stay merged.

## Proof
Night 6 replayed (`../../runs/NIGHT6_RUN.md`): from the commit before its morning merge, the four branches in the same
order; the shared files compared with what was committed after the hand repair. Result: see "Done when".

## Done when
Its tests pass (`helper/test_night_merge.py`: two sessions merged by rule; a conflict no rule covers stops and
aborts; class by class; lines kept and a line changed on both sides stopped; brief numbers used twice reported), and
the night 6 replay gives the hand-repaired files, apart from the differences the replay names. Status: see the replay's
reading below.

## What this function does not do
It does not renumber briefs used twice (next steps 3e: it reports them), push, or merge into master.
