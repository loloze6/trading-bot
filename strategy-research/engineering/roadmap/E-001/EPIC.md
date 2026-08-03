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

**Correction (S2 audit, dispatch W23/W24 — kept below the original claim, not
in place of it): "six overlapping places" was wrong.** Only **two** of the
five files were genuinely redundant trackers competing for the same job —
`improvements/HANDOFF_CURRENT.md` and `improvements/BACKLOG_DEFERRED.md`.
The other three keep distinct, non-overlapping roles and were corrected, not
retired: `DOC_INDEX.md` is a documentation index (not a work tracker),
`docs/ROADMAP.md` is the program roadmap (strategy + engineering + process),
and `improvements/IMPROVEMENTS_REGISTER.md` is a historical audit of
completed plans. `docs/ROADMAP.md` in particular was characterised in this
epic's original drafting without being read first — see Amendment 3 in
`PROCESS.md`.

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

1. `engineering/roadmap/EPICS.md` exists on `master` and is the only file
   needed to know what is in flight.
2. **Corrected against the S2 audit (was: "all four superseded trackers"
   deleted/reduced to a pointer — wrong; only two were superseded):** the two
   genuinely redundant trackers, `improvements/HANDOFF_CURRENT.md` and
   `improvements/BACKLOG_DEFERRED.md`, are retired (archived or deleted, not
   left as independent trackers); the three that keep distinct roles
   (`DOC_INDEX.md`, `docs/ROADMAP.md`, `improvements/IMPROVEMENTS_REGISTER.md`)
   are corrected against the audit's findings, not retired. Verified by:
   `grep -rl "improvements/HANDOFF_CURRENT.md\|improvements/BACKLOG_DEFERRED.md" strategy-research/`
   returning only the known frozen historical records (`engineering/roadmap/E-001/EPIC.md`'s
   own Why table above, `docs/CLEANUP_PLAN.md`'s move-mapping table,
   `docs/RESTRUCTURE_MAPPING.tsv`'s parked-restructure replay mapping) — no
   live pointer to either retired filename remains anywhere else.
3. A Notion **Epics** database exists, one page per epic, each linking to its
   `EPIC.md`.
4. The next agent session can answer "what should I work on" from `EPICS.md`
   alone, without reading `SESSION_LOG.md`.

## Stories

- [x] **S1** — Write `PROCESS.md`, `ROADMAP.md`, and this file. Seed E-002…E-006
      from known outstanding work. *(Written directly by the director rather than
      dispatched: the content was already designed, and dispatching designed
      content means writing it twice.)*
- [x] **S2** — Audit the four superseded trackers. For every item in each,
      classify as **live** (becomes or joins an epic), **done** (archive), or
      **dead** (delete). Reduce each file to a pointer. This is the story that
      makes E-001 worth doing — read-heavy, judgment-heavy, one dispatch.
      *(Audited in dispatch W23; applied in W24: `HANDOFF_CURRENT.md` archived
      to `engineering/sessions_archive/HANDOFF_20260724.md`,
      `BACKLOG_DEFERRED.md` deleted with its 4 live items carried into E-009,
      `DOC_INDEX.md`/`docs/ROADMAP.md`/`IMPROVEMENTS_REGISTER.md` corrected
      and reduced to their distinct, non-overlapping roles.)*
- [ ] **S3** — Create the Notion Epics database mirroring 🐛 Bugs & Tasks'
      property shape; seed one page per epic with a link back to `EPIC.md`.
- [x] **S4** — Create `E-002`…`E-009` epic files from the seeds in `ROADMAP.md`
      plus the items S2's audit surfaced (E-007, E-008, E-009), each with a
      testable *Done when* except E-004, which needs a joint decision first
      (recorded as such, not invented).
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
- 2026-08-03 — S2 audited (W23) and applied (W24, commits `895a3def`,
  `371e3eb3`): of the five tracked files, two retired (`HANDOFF_CURRENT.md`
  archived, `BACKLOG_DEFERRED.md` deleted) and three corrected in place
  (`DOC_INDEX.md`, `docs/ROADMAP.md`, `IMPROVEMENTS_REGISTER.md` — not
  overlapping trackers, per the S2 audit). S4 complete (W24): `E-002`
  through `E-009` written, expanded past the original E-002…E-006 seed with
  E-007/E-008/E-009 surfaced by the S2 audit. Next: S3 (Notion Epics
  database), then S5 (close-out).
- 2026-08-03 — S6 (dispatch W25): killed the `ROADMAP.md` name collision
  (renamed to `EPICS.md`, commit `c7039809`); extracted the dispatch model to
  `engineering/DISPATCH_MODEL.md` (commit `b7cdd50c`); named the seam between
  it and `PROCESS.md`, added five amendment rules from testing (commit
  `955d543e`); corrected this epic's own Why table and Done-when #2 against
  the S2 audit's actual finding (two redundant, not four/six) — this commit.
