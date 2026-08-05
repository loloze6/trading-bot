# Engineering process — epics, stories, evidence

The unit of engineering work is an **epic**. This file is the whole spec. If you
are an agent starting cold, read `EPICS.md` first — it is one line per epic and
tells you what is in flight. Come here only when you need the rules.

## What is and is not an epic

An epic is an **engineering evolution**: infrastructure, tooling, process,
portability, or structure. Something that makes future work cheaper or safer.

It is an epic if it needs **more than one dispatch** OR **changes shared
structure**. Otherwise it is a Notion bug card and a single dispatch. Do not
create an epic for a two-character fix.

**Research hypotheses are NOT epics.** They go through the campaign's
preregistration and verdict machinery (`protocols/`, `prereg_*.yaml`,
`prescreen_signal.py`). That machinery is stricter than this one and must not be
bypassed or duplicated here. If the work would produce a *verdict about a
strategy*, it is campaign work. If it changes *how we work*, it is an epic.

## States

```
new  →  planned  →  in-progress  →  done
  ↘               ↘             ↗
   withdrawn         parked        killed
```

| State | Means | Requires |
|---|---|---|
| `new` | Identified, not yet planned | A one-line why |
| `planned` | Stories written, ready to dispatch | A testable "done when" |
| `in-progress` | At least one story dispatched | — |
| `parked` | Work exists but cannot proceed | **A written unblock condition.** "Resumes when X" |
| `done` | Complete and verified | **Commit SHA + a verification command and its output** |
| `killed` | Deliberately abandoned | Evidence for why. A killed epic is not `done` |
| `withdrawn` | Was not an epic after all; work continues as a card | The card reference |

`parked` is not a soft `done`. Recording parked work as closed asserts a verdict
we do not have — this has caused real damage before. If it is blocked, say so and
say on what.

## Stories are dispatches

A story is **one dispatch**, producing **one commit** (or a small, stated set).
The story list is the dispatch queue. Do not invent a separate unit of work — the
numbered dispatch is the thing that actually happens, and anything else drifts
from it.

## Relationship to the dispatch model

`PROCESS.md` (this file) governs how work is **organised**: epics, stories,
states, evidence. `../DISPATCH_MODEL.md` governs how a unit of work is
**executed**: who dispatches, who audits, which model tier, cost discipline,
context economy. They meet at exactly one point: **a story is a dispatch**
(see "Stories are dispatches" above) — the story list this file's epics
produce is the same queue `DISPATCH_MODEL.md`'s loop consumes one at a time.
Neither file duplicates the other's content; a question about *what* to work
on or *how epics are structured* belongs here, a question about *who runs it
and on what tier* belongs there.

## Layout

```
engineering/roadmap/
  PROCESS.md        this file
  EPICS.md          the index — one line per epic, the only mandatory read
  E-001/
    EPIC.md         one page. If it needs more, it is two epics or it needs a design.
    design/         optional, by exception
    artifacts/      outputs produced by the epic
```

**Folders are named by ref only** — `E-001/`, never `E-001-some-title/`. Titles
change; refs do not. Lowercase, no spaces, ever: a space in a directory name has
blocked commits here before.

## Design documents are by exception

Write one only if:

- the decision is **irreversible**, or
- two competent agents would **plausibly choose differently**

Otherwise `EPIC.md` is enough. A design doc that only restates the plan is pure
cost.

## Done means evidence

Closing an epic requires a commit SHA plus a verification command and its actual
output. Not a narrative claim that it works. This workspace has a documented
history of confidently-wrong claims; this rule is the cheap structural fix.

## Notion

Git is **authoritative** for state. Notion is a **notification surface**, not a
second state store — two state stores is how parallel taxonomies get created.

- One Notion page per epic, updated in place. Not one page per transition.
- Post to Trading Bot HQ only on `done` or `parked` — the two transitions someone
  else has to act on.

## Writing about the sealed window

The pre-commit holdout gate pins exempted files to an audited **line count**, so
adding one more line containing a sealed-window date to a pinned file will block
your commit. This has fired three times.

**Cite `config/campaign_data_policy.yaml:holdout_range` instead of writing the
literal boundary dates.** That keeps the count stable and is more accurate anyway
— the policy file is the source of truth.

## EPIC.md template

```markdown
# E-0XX — <title>

**State:** new | planned | in-progress | parked | done | killed
**Owner:** <name>
**Updated:** YYYY-MM-DD

## Why
Two or three lines. What is worse today, and what is better after.

## Done when
Testable. A command someone can run, or an observable state. Not "improved".

## Stories
- [ ] S1 — <one dispatch> 
- [ ] S2 — <one dispatch>

## Log
- YYYY-MM-DD — `new` → `planned`. <what changed, SHA if any>
```

## Amendments

Rules added from testing this process, each with the one-line cause that
produced it:

1. **No two files may share a bare filename if they serve different
   purposes.** *Cause: two `ROADMAP.md` files (`docs/ROADMAP.md`,
   `engineering/roadmap/ROADMAP.md`) existed at once; renamed the latter to
   `EPICS.md` (dispatch W25).*
2. **Done epics never move; `EPICS.md` carries Active and Done tables.**
   *Cause: renames cost a full session of pain, and a space in a directory
   name has blocked commits three times — moving a closed epic is a rename
   with no offsetting benefit.*
3. **An epic's Why must be VERIFIED, not asserted.** *Cause: E-001 claimed
   "six overlapping places" / "four superseded trackers" when the S2 audit
   found only two were actually redundant; `docs/ROADMAP.md` was
   characterised (as a "campaign plan") without being read first.*
4. **Any dispatch that MOVES a file must check
   `config/holdout_gate_exemptions.txt` for that path and authorize the
   re-key in the same dispatch.** *Cause: the pinned-count holdout gate has
   blocked four commits over path renames it didn't know about in advance.*
5. **An epic's `artifacts/` holds the evidence that justified it, not only
   its outputs.** The measurements, command output, and reads that
   established the epic's Why belong there alongside whatever the epic
   produces — not just the deliverable.
6. **Incidental findings go to Notion immediately, tagged with the epic ref
   that found them.** Anything discovered during an epic that is not that
   epic's Why is filed on 🐛 Bugs & Tasks the moment it is found. It is never
   fixed inline (scope creep) and never carried only in conversation. If it
   later proves to need more than one dispatch or to change shared structure,
   it graduates to an epic and its card is reduced to a POINTER — never
   maintained as a parallel record.
   *Cause: E-001 surfaced six defects while doing something else; they survived
   only because they were kept in a chat list, which is not a durable store.
   And E-003 was filed as both a Bugs & Tasks card and an epic — two state
   stores for one item, which this file already forbids.*
7. **An epic that turns out to be below the threshold is `withdrawn`, not
   `killed`.** New terminal state. `killed` means the work was abandoned;
   `withdrawn` means the work is still happening, just as a card, because it
   needed only one dispatch after all. Requires: the card reference it
   continues as.
   *Cause: E-003's true size is unknown until its investigation story runs.
   Overloading `killed` to mean "wasn't an epic" repeats the parked-vs-done
   confusion in a different key.*
8. **CROSS-FORK COORDINATION.** Four rules governing work that crosses the
   fork boundary — this file, until now, assumed one side.

   (a) **Two axes, not one.** `State` answers "is the work done" (new /
       planned / in-progress / done / parked / killed / withdrawn).
       `Location` answers "where does the code live" (master / fork / in
       transit, i.e. PR open). They are independent — an item can be
       `in-progress` on master and `done` in the fork with neither being
       wrong. The fork's existing six-value field collapses both into one;
       this rule decomposes it without loss.

   (b) **Three roles, not one owner.** Designer (specified it), implementer
       (wrote it), verifier (proved it). Across a fork these are routinely
       three different parties. Worked example: E-010 (slippage model) —
       Dorian designed it, this side implements it, and no verifier is
       assigned. A two-field scheme cannot express that gap. This also
       makes visible on the board what `DISPATCH_MODEL.md` already requires
       in review: three parties for orchestrator/engine/shared-state
       commits.

   (c) **One item, one home — across both repos.** Every item is owned by
       exactly one system: epics in git on master, bugs in Notion,
       fork-only work in the fork's ledger. Cross-references are pointers,
       never copies. Amendment 6 extended from one repo to two.

   (d) **A decision that binds both sides is written to the shared surface
       — dated and attributed, at the moment it is taken.** Chat is not a
       record. Git-on-one-side is not a shared record.
       *Cause: trial-ledger Option A was decided in conversation on
       2026-08-03 and recorded only in `E-011/EPIC.md`. The fork's
       "Trial-ledger DUAL-WRITER merge protocol" page subsequently stated
       it "was never confirmed by Jeremy, so nothing needs unwinding" — and
       a protocol was designed on that premise. Neither side misread
       anything; the decision was simply unreadable from one of them.*

9. **BEFORE AN EPIC IS CREATED, GREP THE TREE FOR ITS SUBJECT.** Amendment 3
   requires an epic's Why to be verified; it does not say against what.
   Checking the record layer (existing epics, Notion tickets) is not enough
   — it finds duplicate RECORDS, not existing CODE.
   *Cause: dispatch W34 audited seven roadmap items for overlap against
   E-002..E-012 and Notion, found none, and six epics were created as
   unstarted work. A tree audit (W37) then found four of the six already
   implemented and tested. Root cause: `docs/ROADMAP.md` was written
   2026-07-19/20 and partly executed 2026-07-20 without being updated, so it
   described as future what had already shipped. Unrecorded does not mean
   undone.*
