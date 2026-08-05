# E-013 — Split docs/ROADMAP.md — retire the name, graduate the engineering items

**State:** planned
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

`docs/ROADMAP.md` mixes campaign content with unowned engineering work, and
`DOC_INDEX.md` names it the sole location for material that exists nowhere
else. Per W33's measured audit (cited, not re-derived here): after `b7cdd50c`
extracted Part 3, the file holds front matter (9 lines), Part 1 "What we
built" (14), Part 2 "The roadmap, granular" (43, Phases 0–5), a 6-line Part 3
pointer, and Part 4 "Standing guarantees" (5). `DOC_INDEX.md` names it the
sole location for the KPI/anti-corner rule and the Part 1 concept
explanations; W33 grepped `strategy-research/` and Notion and found them in
neither.

Part 2 embeds seven engineering items (1.2, 1.3, 1.4, 3.1, 3.2, 3.4, 4.1).
None exists as an epic or Notion ticket today. A Notion page on
funding-as-a-cost-line is adjacent to 1.2 but does not cover its scope (venue
fee schedule + 3 calibration reruns). Archiving the file wholesale would
therefore lose information that exists nowhere else, and moving it as-is
would relocate campaign content into `engineering/`.

## Done when

1. The seven engineering items are each recorded as an epic or a Notion card,
   per `PROCESS.md`'s threshold, with the classification reasoning recorded
   per item.
2. The remaining campaign content (Parts 1, 2's phase structure, 4) lives in
   a file whose name describes what it is. It is not called a roadmap.
3. `DOC_INDEX.md` points at the new name and nothing points at the old one.
4. No content is lost: every line of the current file is either carried into
   the renamed file, graduated to a work item, or explicitly recorded as
   deliberately dropped.

## 3.4's disposition (for S3 — do not re-derive)

`docs/ROADMAP.md` §3.4, verbatim: "**Diagnostics extensions on demand.**
Objective: the autopsy palette never blocks on a missing metric. Deliverable:
small, ledgered additions to the diagnostics layer exactly when an autopsy
needs a metric that doesn't exist yet (e.g. the regime-correctness measure)
— never speculatively."

3.4 is **neither an epic nor a card**. "Diagnostics extensions on demand,
never speculatively, ledgered" is a STANDING GUARANTEE — a rule about *how*
work is done (only build a metric when an autopsy actually needs it, and
ledger the addition when it happens), not a work item with a deliverable of
its own to schedule or close. It does not go through `PROCESS.md`'s
epic-vs-card threshold because there is no discrete "done" state for a
standing rule.

**S3 action:** carry this rule verbatim into Part 4 of the renamed file
(the same Part that already holds the KPI and the anti-corner rule) rather
than graduating it to an epic or a Notion card.

## S3 obligations (from the S1 audit)

Two things the S1 audit found that S3 must handle, recorded here so S3 does
not have to re-derive them:

a) `docs/ROADMAP.md`'s front matter (lines 4–7) asserts: "Engineering steps
   in it (1.2, 1.3, 1.4, 3.1, 3.2, 3.4, 4.1) are implemented as epics — see
   engineering/roadmap/EPICS.md." This was **false when written** (no such
   epics existed) and becomes **true once this dispatch (S2) lands** — six
   of the seven are now epics, and 3.4 is recorded above as a deliberate
   non-epic. S3 must **verify** the claim against the epics this dispatch
   created, not delete it outright.

b) `engineering/DISPATCH_MODEL.md`'s anti-corner section states it is
   "Carried across from `docs/ROADMAP.md` Part 4, which otherwise stays
   intact." The rename in S3 breaks that reference — Part 4 will no longer
   live in a file called `docs/ROADMAP.md`. S3 must update
   `DISPATCH_MODEL.md`'s pointer and decide which copy (the renamed file's
   Part 4, or `DISPATCH_MODEL.md`'s own anti-corner section) is
   authoritative. The audit found the two texts identical, so this is a
   pointer fix, not a merge.

## Stories

- [x] S1 — Audit the seven items; classify each epic-vs-card. Report only,
      no records created. (dispatch W34)
- [x] S2 — Create the work items the audit calls for. (dispatch W35: six
      epics — E-014..E-019 — created; 3.4 recorded above as a standing
      guarantee, not an epic or card.)
- [ ] S3 — Rewrite and rename the file; repoint `DOC_INDEX.md`; verify no
      content lost.

## Log

- 2026-08-05 — `new` → `planned`. Epic created; S1 audit run in the same
  dispatch (W34) and reported to the operator (chat only — Step 2 of the
  dispatch was report-only, nothing written to disk beyond this file). Next
  step: S2 — create the work items S1's audit calls for.
- 2026-08-05 — S2 done (dispatch W35). Created E-014 (1.2, new, follows
  E-010), E-015 (1.3, new, unblocked), E-016 (1.4, parked on E-010+E-017),
  E-017 (3.1, parked on Phase 2), E-018 (3.2, parked on Phase 2), E-019 (4.1,
  parked on Phase 3). Recorded 3.4's disposition as a standing guarantee
  (above) and the two S3 obligations found by the S1 audit (above). Next
  step: S3 — rewrite/rename `docs/ROADMAP.md`, repoint `DOC_INDEX.md`, verify
  no content lost. S3 is explicitly out of scope for this dispatch.
