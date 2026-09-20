# Agent dispatch template — roadmap v27 implementation

**Purpose.** A fill-in-the-blanks structure for dispatching an S1 (characterize) or S2
(build) agent against the roadmap v27 / `delivery_plan_v26.md` slices. Written 2026-09-20
after the first four dispatches (E-056 S1, E-046b S1, CUL-267, CUL-300), which worked but
exposed three real problems this template exists to prevent from recurring silently. Read
§0 before writing any dispatch, even if you only copy the templates in §2/§3 without
changing a word.

---

## 0. Five lessons this template encodes, and why

1. **A worktree-isolated agent is based on `origin/master`, not your local `master`.**
   If you have unpushed local commits — a merge, a docs commit, anything — no
   worktree-isolated agent can see them unless told explicitly how to reach them. This bit
   all four of the first dispatches identically: every one landed on a stale base. Two
   characterization agents caught it themselves and worked around it by reading files via
   `git show <local-commit>:<path>`; the two build agents had to be told this explicitly
   (§1.3) or verified for compatibility after the fact by the dispatcher. **§1 makes this
   check mandatory, not optional, for every future dispatch** — cheap insurance even once
   master is pushed and current, since it costs one `git log` comparison and catches the
   next time this happens for some other reason (a rebase, a second unpushed commit, etc).
2. **A build agent's output must independently self-verify against the real target
   branch**, not just against whatever base it happened to start from. CUL-300 did this
   proactively (diffed the gap against its own touched files, then rebased its own commit
   onto real master before reporting back) and needed zero follow-up. CUL-267 did not, and
   the dispatcher had to do a disposable cherry-pick test afterward to confirm
   compatibility — extra work, and a real risk if it had been skipped. **§3 makes CUL-300's
   pattern the required step, not the exception.**
3. **A characterization agent's deliverable file must be committed, not just written.**
   Both S1 findings files sat as untracked files inside ephemeral worktrees until the
   dispatcher went looking for them and pulled them into the tracked repo by hand. If that
   worktree had been pruned first, the work would have been lost outright — the agents were
   never told to commit because "read-only, no code changes" was interpreted (reasonably,
   but wrongly) to mean "don't touch git" too. **§2 now requires a commit as part of the
   deliverable**, not merely a file on disk.
4. **A rate-limited dispatch can leave real, uncommitted work behind — secure it before
   anything else, then resume rather than restart.** Happened twice in one night
   (2026-09-20/21, the profit-bars and E-054-gate dispatches): the session hit an
   account-wide rate limit mid-task, and the agent's worktree had real, unstaged file
   changes sitting only in the working tree — nothing an ordinary `git log` on the branch
   would show, and exactly what a worktree prune or a careless `git checkout` would
   destroy with no recovery. The fix, in order, every time a dispatch notification reports
   `status: failed` with a rate-limit reason: (1) `git status --short` in that worktree
   FIRST, before anything else — if it's clean, nothing was lost, the agent died before
   writing anything. (2) If it's dirty, commit everything immediately with a message that
   says plainly it's an unverified WIP snapshot, not a reviewed deliverable — do not skip
   this step to "wait and see if it resumes cleanly." (3) Push that WIP branch to origin
   as a backup (no PR) — a local-only worktree is one bad `rm -rf` or disk event away from
   losing both the branch and the only copy of the commit. (4) Once the rate limit's own
   stated reset time has passed, resume the SAME agent via `SendMessage` to its agent ID
   rather than dispatching a fresh one — a fresh dispatch re-derives all the same context
   the original agent already paid for and re-walks investigation it already did; resuming
   preserves that and just asks it to check `git log`/`git status`, pick up from the WIP
   commit, finish, and replace the WIP commit with a real one before its final report.
5. **A build agent's own naming choices are not self-checked against the rest of the
   codebase.** CUL-267 and CUL-300 (2026-09-20) both shipped with a real bug the builder's
   own tests couldn't catch because the tests only exercise the new code in isolation: CUL-300
   named two new fields (`edge_to_cost_ratio`, `cost_basis`) that collided with existing,
   differently-computed fields elsewhere in the codebase, and CUL-267 exempted a whole
   criterion class from a check the evaluator actually applies to it. Both were only caught by
   a separate adversarial code-review pass the dispatcher ran manually, afterward, against
   each finished branch. This codebase has a *documented history* of exactly the naming-
   collision bug class (the bare `"ic"` keyword collision in `run_protocol.py`, 2026-07-09) —
   it is common enough here to check for by default, not opportunistically. **§3 now makes a
   self-adversarial-review step mandatory inside the build dispatch itself**, before the agent
   reports back, so the dispatcher's follow-up review is confirmation rather than first
   discovery.

---

## 1. Before writing ANY dispatch — the base-commit check

Run this once, right before dispatching (not once per session — re-check every time,
state genuinely changes):

```bash
git fetch origin 2>&1 | tail -3
git log --oneline -1 origin/master
git log --oneline -1 master        # or whatever branch the work actually needs
```

- **If they match:** no special instruction needed. Proceed with the templates below as
  written.
- **If they don't match** (local is ahead of origin, as it usually will be for anything
  not yet pushed): the dispatch prompt MUST include an explicit "Context you need first"
  block naming the exact local commit the agent needs, e.g.:

  > Your worktree may be based on `origin/master` (older than what you need). Before
  > anything else, run `git log --oneline -1` in your worktree and compare it to
  > `<local-commit-hash>`. If your worktree's HEAD is NOT a descendant of
  > `<local-commit-hash>`, the files/code you need may not exist in your working tree yet.
  > Read them via `git show <local-commit-hash>:<path>` instead of assuming they exist at
  > your HEAD — do not skip the task, do not guess their content. State in your final
  > report whether this applied to you and how you handled it.

  For a BUILD dispatch specifically, also add:

  > Before you finish: confirm your final commit is compatible with
  > `<local-commit-hash>` — either build your branch directly off it (`git checkout -b
  > <branch> <local-commit-hash>` at the start, preferred, matches what CUL-300 did), or if
  > your worktree started elsewhere, cherry-pick/rebase your finished commit onto
  > `<local-commit-hash>` before reporting back and confirm it applies without conflict.
  > State which you did.

---

## 2. Template — S1 (characterize-and-STOP)

```
DISPATCH: <EPIC-ID> S1 — characterize and STOP. NEW AGENT (fresh context; no prior agent
holds relevant state).

Read-only: no code changes, no config changes, no backtests, no LLM stage runs, never open
local_data/holdout_sealed/. Do not edit strategy-research/engineering/engineering_roadmap.html,
delivery_plan_v26.md, or any other agent's own S1_FINDINGS.md.

Repo: <path>. Windows layout: trading-bot/ and strategy-research/ subdirectories under the
repo root. Use Git Bash style commands for grep/python. Quote every command verbatim in the
findings next to its number.

[INSERT the base-commit check block from §1 here if origin/master and local master differ]

Context you need first: read strategy-research/engineering/roadmap_review_2026-09-18.md in
full, and card <X> in strategy-research/engineering/engineering_roadmap.html (search the
file for 'order mono">X<'). Also check whether a Linear MCP tool call succeeds for you in
this worktree (try a simple read, e.g. get_project on this epic) — if it fails/is
unauthenticated, note that in your final report and proceed from the dispatch's own text
instead of fabricating ticket content or skipping the read.

<EPIC-ID>'s target, in one paragraph: <...>

Goal: produce the evidence needed to <specific deliverable — a design guide, a menu, a
schema>. Every claim carries a file:line reference. Anything you cannot establish goes in a
"Not determined" section, never guessed.

Tasks:
1. <...>
2. <...>
[Number every task. Each task should specify: which file(s) to read, what exactly to
measure or enumerate, and what shape the output takes — a table, a pseudocode block, a
count. Prefer "measure on the real corpus, state the denominator" over "estimate" for
anything with real data available (strategy-research/runs/run_*/).]

Deliverables:
1. Write strategy-research/engineering/roadmap/<EPIC-ID>/S1_FINDINGS.md (create the
   directory if needed).
2. **Commit it.** `git add strategy-research/engineering/roadmap/<EPIC-ID>/S1_FINDINGS.md
   && git commit -m "docs(<EPIC-ID> S1): characterization findings"` — with the same
   Co-Authored-By line used in this repo's recent commits (check `git log -3` to match the
   exact format). This is a documentation deliverable, not code, and does not violate the
   "no code changes" read-only scope above — the read-only rule is about the REPO'S
   PRODUCTION FILES, not about your own findings artifact.
3. Do NOT push, do NOT open a PR.
4. A paste-ready Linear-comment-shaped section at the end of the file. Do not post to
   Linear yourself.

Final message to me: at most 30 lines. State your worktree's branch name and final commit
hash. Headline findings with file:line. The "Not determined" list. Whether the base-commit
check in §1 applied to you and how you handled it, if so. Then STOP — do not proceed to any
build work.
```

---

## 3. Template — S2 / build

```
DISPATCH: <TICKET-ID> — build. NEW AGENT (fresh context).

IMPORTANT SCOPE LIMIT: build, test, and commit LOCALLY only. Do NOT push to any remote. Do
NOT open a PR. Do NOT merge to master or any other branch. [If dispatched with the operator
present and actively reviewing in real time, replace this whole paragraph with the actual
authorized scope for that dispatch — this default is for unsupervised/overnight dispatches.]

Never open local_data/holdout_sealed/. Never run a real backtest unless the ticket's own
run budget explicitly calls for it.

[INSERT the base-commit check block from §1 here — for a build agent this is not optional,
even when origin and local match today, because "today" can change mid-task if another
agent or the operator pushes/commits concurrently. State explicitly:]

Before your first commit: `git checkout -b <branch-name> <local-target-commit>` — build
directly on top of the real target commit, do not build on whatever your worktree happened
to start at and reconcile later. If for any reason you cannot do this (the target commit
doesn't exist in your worktree's object database), STOP and report this rather than
building on a possibly-stale base silently.

Context: read the Linear issue <TICKET-ID> in full if the Linear MCP tools are
authenticated for you (try a read first); if not, work from the problem statement below,
which is authoritative regardless. Also check whether a relevant S1_FINDINGS.md exists at
strategy-research/engineering/roadmap/<related-epic>/ — if a sibling agent may be producing
it concurrently in a different worktree, proceed without it rather than wait.

The fix, precisely: <...>

Build:
1. <...>
2. <...>
[Number every step. Be explicit about: exact function/file to change, exact new
field/behavior, and the byte-identity or additivity requirement — state plainly what must
NOT change for existing callers/data.]
N. Verify byte-identity/additivity directly against real data: pick 2-3 real runs under
   strategy-research/runs/run_*/ (or wherever the relevant artifact lives) and confirm
   every pre-existing field is unchanged before/after your change. Name the exact run IDs
   you checked in your final report.
N+1. Write a new test file covering: the core new behavior, an edge case (zero/null/empty
   input), and the byte-identity/additivity check as its own explicit test, not just a
   manual confirmation in your report.
N+2. Try to run the new test file with pytest if available in this worktree; if not,
   install pytest (and other pinned deps as needed — versions are in
   strategy-research/config/requirements-mac.txt / trading-bot/requirements.txt) then run.
   Report EXACT pass/fail counts, never an impression ("looks good", "should pass" are not
   acceptable substitutes for a number).
N+3. **Self-adversarial review, before committing — mandatory, not optional.** For every new
   field name, function name, or key you introduced: `grep -rn "<exact_name>"` across the
   WHOLE repo (both trading-bot/ and strategy-research/), not just the file you edited. If it
   already exists anywhere else with a different meaning or computation, that is a collision —
   rename yours, don't assume the two can coexist. This codebase has a documented precedent
   for exactly this bug (the bare `"ic"` keyword collision in `run_protocol.py`, 2026-07-09) —
   treat it as a known failure mode to check for, not a hypothetical. Separately, re-read your
   own new logic once adversarially: what input makes this silently wrong rather than loudly
   wrong (a guard that's too broad, a check exempting a case the evaluator doesn't actually
   exempt, a mismatched N between two related aggregates)? State in your final report what you
   checked and what you found, even if the answer is "no collisions, no gaps found."

When done: `git add` only the files you actually changed, commit locally with a clear
message ending in the same Co-Authored-By line used in this session's recent commits
(check `git log -3` in your worktree to match the exact format), confirm your commit's
parent is the real target commit from the base-commit check above, and STOP. Do not push,
do not open a PR.

Final message to me: the branch name, the final commit hash and its parent (confirming
compatibility), exact test output, the specific run IDs checked for the byte-identity
verification, any caveat/limitation found while building that isn't yet reflected in the
ticket text (state it plainly — do not silently build around a wrong assumption in the
ticket, flag it), and anything unresolved. Keep it under 25 lines.
```

---

## 4. Dispatch pacing (added 2026-09-20, per operator direction)

Do not fire a large batch of parallel agents as a default. The first night's batch of four
(two S1, two build) each consumed on the order of 130k-195k tokens by their own reported
usage, before any of the dispatcher's own verification work on top. Going forward:

- **Push master first**, before dispatching anything worktree-isolated, whenever there is
  an unpushed local commit the dispatched work depends on. This alone removes the need for
  §1's workaround instructions in the common case.
- **One or two agents at a time**, not four, unless there's a specific reason for more
  (e.g., genuinely independent, small, low-risk items with idle time to fill). Review each
  one's output before dispatching the next batch, not after all of them return.
- If token budget for the current window is already tight, prefer direct edits (Bash/Edit
  tools in the primary session) over spawning a new agent for small, well-understood
  changes — a dispatch has fixed overhead (its own context load, its own investigation from
  scratch) that a direct edit skips entirely.

---

## 5. Where this fits

This template assumes `delivery_plan_v26.md` (or its successor) has already named the slice,
the seams, the flag, and the run budget — the dispatch prompt's Tasks/Build sections should
be derived from that slice's text, not invented fresh. `engineering_roadmap.html`'s cards
A-N remain the single source of truth for *what* the target design is; this file is only
about *how to ask an agent to help build toward it* without silently losing work or
producing incompatible output, given what actually went wrong the first time.
