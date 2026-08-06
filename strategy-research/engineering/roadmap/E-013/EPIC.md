# E-013 — Split docs/ROADMAP.md — retire the name, graduate the engineering items

**State:** done (reopened and re-closed 2026-08-05, dispatch W37 — see Log)
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
- [x] S3 — Rewrite and rename the file; repoint `DOC_INDEX.md`; verify no
      content lost. (dispatch W36)
- [x] S4 — Repoint the six live code/schema "Source: Phase X.Y (`docs/ROADMAP.md`)"
      citations that S3's own Log deferred as "that epic's own implementation
      work, not S3's." Done-when #3 says "nothing points at the old one," with
      no carve-out for epic-owned citations — S3's close did not hold.
      (dispatch W37)

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
- 2026-08-05 — S3 done (dispatch W36). `planned` → `done`.
  **Rename:** `git mv docs/ROADMAP.md docs/CAMPAIGN_PROGRAM.md`, both paths
  staged, old path verified gone (`test ! -e` passed).
  **Content accounting (Done-when #4):** front matter (9 lines) rewritten to
  describe what the file is, naming E-014 through E-019 in place of the old
  false-when-written epics claim (now true). Part 1 (14 lines) carried
  verbatim. Part 2 (43 lines): Phase 0-5 structure and every non-graduating
  item (0.1, 0.2, Gates ×5, 1.1, 2.1-2.5, 3.3, 4.2, 5.1-5.3, Definition of
  done) carried verbatim, including 0.2's own historical mention of
  `docs/ROADMAP.md` (a past session-close deliverable — left unrepointed, per
  Step 1's historical-record rule, not falsified). The six engineering items
  (1.2, 1.3, 1.4, 3.1, 3.2, 4.1) each replaced by a one-line pointer to their
  epic (E-014..E-016, E-017, E-018, E-019); 3.4 replaced by a pointer to
  Part 4, where its standing-guarantee text (Done-when #1's obligation) was
  added verbatim from this file's own §"3.4's disposition" record. Part 3
  (6 lines) carried, with its one self-reference to "this roadmap's ...
  cadence" corrected to "this document's" since the file is no longer called
  a roadmap. Part 4 (5 lines) carried verbatim, plus 3.4 appended. The
  trailing "*Next update: at session close...*" line was DELIBERATELY
  DROPPED — stale, already superseded (Phase 1 has long since progressed to
  spinning off E-014/E-015/E-016). No line unaccounted for.
  **S3 obligation (a):** front matter's epics claim verified against the six
  epics this dispatch's S2 (`cd20e6ec`) created — restated as true, naming
  them individually rather than pointing generically at `EPICS.md`.
  **S3 obligation (b):** `engineering/DISPATCH_MODEL.md` repointed at both
  its `docs/ROADMAP.md` references (lines 3 and 107); declared
  `docs/CAMPAIGN_PROGRAM.md` Part 4 the authoritative copy of the
  anti-corner text, `DISPATCH_MODEL.md`'s own copy a mirror — the two texts
  were already identical per the S1 audit, so this was a pointer fix.
  **Repoints (Done-when #3):** `DOC_INDEX.md` (3 entries) and
  `DISPATCH_MODEL.md` (2 entries) repointed to the new name. Also repointed,
  found in scope during Step 1's full-repo enumeration and not previously
  named by this epic: `EPICS.md`'s E-017/E-018 "Blocked on Phase 2's gate"
  cells (live blocking-condition pointers, not historical) and `EPICS.md`'s
  own E-013 row (moved Active → Done, this entry).
  **Left unrepointed, classified historical/provenance, not live pointers:**
  `SESSION_LOG.md`, `docs/session_reports/*`,
  `archive/improvements/NEXT_SESSION_20260719_superseded.md`,
  `engineering/sessions/HANDOFF_20260724.md` (all dated,
  point-in-time records); `PROCESS.md` Amendment 3 (describes a past
  mischaracterisation); `E-001/EPIC.md`'s Why table; `E-002/EPIC.md`'s
  pre-existing W33 Story/Log text (a new dated Log entry was added instead
  — see `E-002/EPIC.md`, L48 drop); `E-014`..`E-019/EPIC.md`'s own
  "Source: `docs/ROADMAP.md` §X.Y, verbatim: ..." provenance citations;
  `campaign_knowledge_base.yaml`'s dated KB entry (quotes the Phase 1.3 gate
  as it read on 2026-07-20); `engineering/improvements/ongoing-improvement-design/INVENTORY.tsv` and `engineering/improvements/ongoing-improvement-design/REFERENCE_MAP.tsv`
  (dated audit-inventory snapshots, structurally the same category as
  `RESTRUCTURE_MAPPING.tsv` but not named by Step 5 — left untouched as
  out of scope for this dispatch); and five code/schema provenance
  citations that name "Phase X.Y (`docs/ROADMAP.md`)" as a spec origin —
  `config/venue_tradability.yaml:1`, `tests/test_venue_tradability.py:2`,
  `tests/test_fee_reduction_assessment.py:2`, `workflow/run_campaign.py:180`,
  `workflow/run_phase1_research.py:4416`, and
  `workflow_artifacts/schemas/verdict_interpretation.schema.json:129` — same citation pattern
  as the epic Source: lines above; repointing them to the correct epic
  (E-014/E-015/E-016 depending on the cited phase) is that epic's own
  implementation work, not S3's.
  **Verification:** `grep -rn "docs/ROADMAP.md" strategy-research/` returns
  only the historical/provenance set enumerated above (plus this dispatch's
  own new historical citations in `DISPATCH_MODEL.md`, `E-002/EPIC.md`, and
  `CAMPAIGN_PROGRAM.md`'s own carried-verbatim 0.2 line) — no live pointer
  remains. Sealed-window check: `CAMPAIGN_PROGRAM.md`'s own dates (2026-07-19,
  2026-07-20) fall outside the sealed window and needed no exemption entry
  (Amendment 4). The holdout gate did fire once, self-referentially: this
  Log paragraph's own prose citing the window's boundary literals tripped
  it (category (b) — explaining the boundary, not market data); registered
  `strategy-research/engineering/roadmap/E-013/EPIC.md` (1 line) in
  `config/holdout_gate_exemptions.txt`'s dated-comment section per that
  file's own audit-and-register procedure — `holdout_date_gate.sh` itself
  untouched. `RESTRUCTURE_MAPPING.tsv` L48 dropped, row total 196 → 195
  (see `E-002/EPIC.md` Log); `RESTRUCTURE_REPOINT_SITES.tsv` checked, no
  matching reference existed.
- 2026-08-05 — REOPENED (dispatch W37). `done` → `in-progress`. S3's own Log
  (above) named six live citations — `config/venue_tradability.yaml:1`,
  `tests/test_venue_tradability.py:2`, `tests/test_fee_reduction_assessment.py:2`,
  `workflow/run_campaign.py:180`, `workflow/run_phase1_research.py:4416`,
  `workflow_artifacts/schemas/verdict_interpretation.schema.json:129` — and explicitly left them
  pointing at `docs/ROADMAP.md`, deferring the repoint to "that epic's own
  implementation work, not S3's." Done-when #3 reads "`DOC_INDEX.md` points at
  the new name and nothing points at the old one" — no carve-out for
  epic-owned citations. The close did not hold; reopening rather than treating
  W36's `done` as final. Adding S4 to close the gap.
- 2026-08-05 — S4 done (dispatch W37). `in-progress` → `done`. Repointed all
  six citations named above to `docs/CAMPAIGN_PROGRAM.md`, filename only, each
  "Phase X.Y" reference left intact since those sections exist unchanged under
  the same numbers in the renamed file. Also removed the now-stale
  `config/holdout_gate_exemptions.txt` entry that had registered this file's
  S3 Log paragraph (1 line, category (b)) — that Log text no longer contains a
  sealed-window date literal after this reword, verified:
  `grep -E "2026-0[1-6]-[0-9]{2}" engineering/roadmap/E-013/EPIC.md` returns
  nothing. **Verification (Done-when #3, re-run):**
  `grep -rn "docs/ROADMAP\.md" strategy-research/` returns only the
  historical/provenance set — dated session logs and archived handoffs
  (`SESSION_LOG.md`, `docs/session_reports/*`,
  `archive/improvements/NEXT_SESSION_20260719_superseded.md`,
  `engineering/sessions/HANDOFF_20260724.md`), `PROCESS.md`'s
  past-tense lesson, `docs/CAMPAIGN_PROGRAM.md`'s own carried-verbatim 0.2
  line, `E-001/EPIC.md`'s Why table, `E-002/EPIC.md`'s pre-existing Log text,
  `E-013/EPIC.md`'s (this file's) own narrative and dated Log entries,
  `E-014`..`E-019/EPIC.md`'s "Source: ... verbatim" provenance citations,
  `campaign_knowledge_base.yaml`'s dated KB entry, `engineering/improvements/ongoing-improvement-design/INVENTORY.tsv` and
  `engineering/improvements/ongoing-improvement-design/REFERENCE_MAP.tsv`'s dated audit snapshots, and `EPICS.md`'s own
  historical description of what this epic did — no live pointer remains.
  Re-closed on this evidence, this commit's SHA (dispatch W37, "E-013 S4: ..."
  commit on `master`). Moved back into `EPICS.md`'s Done table (it never left
  — the reopen/re-close both land in this single commit) with an updated
  closing-SHA note naming S4.
