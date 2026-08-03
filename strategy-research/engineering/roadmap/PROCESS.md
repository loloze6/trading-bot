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
                  ↘             ↗
                     parked        killed
```

| State | Means | Requires |
|---|---|---|
| `new` | Identified, not yet planned | A one-line why |
| `planned` | Stories written, ready to dispatch | A testable "done when" |
| `in-progress` | At least one story dispatched | — |
| `parked` | Work exists but cannot proceed | **A written unblock condition.** "Resumes when X" |
| `done` | Complete and verified | **Commit SHA + a verification command and its output** |
| `killed` | Deliberately abandoned | Evidence for why. A killed epic is not `done` |

`parked` is not a soft `done`. Recording parked work as closed asserts a verdict
we do not have — this has caused real damage before. If it is blocked, say so and
say on what.

## Stories are dispatches

A story is **one dispatch**, producing **one commit** (or a small, stated set).
The story list is the dispatch queue. Do not invent a separate unit of work — the
numbered dispatch is the thing that actually happens, and anything else drifts
from it.

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
