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

## Stories

- [x] S1 — Audit the seven items; classify each epic-vs-card. Report only,
      no records created. (dispatch W34)
- [ ] S2 — Create the work items the audit calls for.
- [ ] S3 — Rewrite and rename the file; repoint `DOC_INDEX.md`; verify no
      content lost.

## Log

- 2026-08-05 — `new` → `planned`. Epic created; S1 audit run in the same
  dispatch (W34) and reported to the operator (chat only — Step 2 of the
  dispatch was report-only, nothing written to disk beyond this file). Next
  step: S2 — create the work items S1's audit calls for.
