# E-001 — Establish the engineering operational process

**State:** in-progress
**Owner:** Jeremy
**Updated:** 2026-08-02

## Why

Engineering work is currently tracked in **six overlapping places**, 664 lines
across five files plus Notion:

| Path | Lines |
|---|---|
| `improvements/HANDOFF_CURRENT.md` | 327 |
| `DOC_INDEX.md` | 144 |
| `improvements/IMPROVEMENTS_REGISTER.md` | 97 |
| `docs/ROADMAP.md` | 89 |
| `improvements/BACKLOG_DEFERRED.md` | 7 |
| Notion 🐛 Bugs & Tasks | — |

None is authoritative, several are stale, and the stated problem that started
this work was *"I do not understand anymore what is used for what."*

`DOC_INDEX.md` is the exception worth care: it is a **documentation index**, not
a work tracker, and it may already partly deliver the original ask — *"overarching
documentation on files where I do not know when they are used and why."* S2 must
judge whether it is stale or worth keeping and updating, not retire it by default.

The real cost is not human confusion. It is that **every cold agent session pays
to rediscover what is in flight**, and sometimes gets it wrong — a prior session
lost a dispatch by re-opening work that was deliberately parked.

After this epic there is exactly **one** index, it is one line per epic, and
"what happens next" is answerable without reading history.

**This epic must not become a sixth tracker.** If S2 does not retire the others,
E-001 has failed regardless of what else it delivers.

## Done when

1. `engineering/roadmap/ROADMAP.md` exists on `master` and is the only file
   needed to know what is in flight.
2. All four superseded trackers are either deleted or reduced to a single
   pointer line at their old path. Verified by:
   `grep -rLl "roadmap/ROADMAP.md" strategy-research/improvements/ strategy-research/docs/ROADMAP.md`
   returning nothing that still carries independent status.
3. A Notion **Epics** database exists, one page per epic, each linking to its
   `EPIC.md`.
4. The next agent session can answer "what should I work on" from `ROADMAP.md`
   alone, without reading `SESSION_LOG.md`.

## Stories

- [x] **S1** — Write `PROCESS.md`, `ROADMAP.md`, and this file. Seed E-002…E-006
      from known outstanding work. *(Written directly by the director rather than
      dispatched: the content was already designed, and dispatching designed
      content means writing it twice.)*
- [ ] **S2** — Audit the four superseded trackers. For every item in each,
      classify as **live** (becomes or joins an epic), **done** (archive), or
      **dead** (delete). Reduce each file to a pointer. This is the story that
      makes E-001 worth doing — read-heavy, judgment-heavy, one dispatch.
- [ ] **S3** — Create the Notion Epics database mirroring 🐛 Bugs & Tasks'
      property shape; seed one page per epic with a link back to `EPIC.md`.
- [ ] **S4** — Create `E-002`…`E-006` epic files from the seeds in `ROADMAP.md`,
      each with a testable *Done when*. One dispatch, mechanical.
- [ ] **S5** — Close: verify the four *Done when* criteria, record SHA and
      output, post the `done` callout to Trading Bot HQ.

## Decisions taken, with reasoning

Recorded so they are not relitigated:

- **A story is a dispatch.** Not a new abstraction. The numbered dispatch is the
  unit that actually happens here; anything parallel to it drifts from it.
- **Folders are named by ref only.** Titles change. Renames caused a full session
  of pain, and a space in a directory name blocked commits three times.
- **`parked` is a first-class state with a mandatory unblock condition.** The
  campaign lives in parked states — Phase 2.3 is built but unevaluated and must
  never be recorded as closed, because closing asserts a verdict we do not have.
- **Git is authoritative; Notion notifies.** Two state stores is precisely how
  two parallel record taxonomies got created (see E-004).
- **Done requires evidence, not narrative.** This workspace's own honesty log
  records three confidently-wrong claims.
- **Not everything is an epic.** Threshold: more than one dispatch, or changes
  shared structure. Otherwise a bug card and one dispatch.

## Log

- 2026-08-02 — `new` → `in-progress`. S1 complete: `PROCESS.md`, `ROADMAP.md`,
  `E-001/EPIC.md` written on `master`. Created on `master` rather than on the
  parked restructure branch because `engineering/` is a new path there and will
  not collide with the replay mapping (E-002).
