# E-002 — Land the parked `strategy-research/` restructure

**State:** planned
**Owner:** Jeremy
**Updated:** 2026-08-04

## Why

A ~190-file reorganization of `strategy-research/` was built and parked on
`restructure/parked-20260731` pending unification with Dorian's fork, which
had diverged onto its own layout. **Three distinct commits, do not conflate:**
`4adb7403` is the PARK commit itself — the actual 190-file move — reachable
only on `restructure/parked-20260731`, immediately after baseline `4b84ab6f`.
`1f7525f8` is the branch's TIP, one commit further, which added the replay
mapping to that branch. `3cfa7b24` is a **separate** commit on **master**
(same author, two minutes after `1f7525f8`, identical diff, different
parent/hash) that recorded the same mapping directly onto master —
`docs/RESTRUCTURE_MAPPING.tsv` (200 rows) and `docs/RESTRUCTURE_REPOINT_SITES.tsv`
(32 rows) — specifically so the move could be replayed later without
re-deriving it. `docs/RESTRUCTURE_MAPPING.tsv` as it exists on master today
descends from `3cfa7b24`, not from the branch. To inspect the parked
branch's actual file content (e.g. for a 3-way conflict), read `4adb7403`
or `1f7525f8` with `git show`/`git diff` — either works, since no code
changed between them — never checkout the branch itself. The parked branch's
own commit message records it as **KNOWINGLY INCOMPLETE**:
`strategy-research`'s own pipeline is broken on that branch as parked.

Master has moved since the park (E-001's `engineering/` tree, this epic
system, the S2 tracker retirement). Replaying stale moves onto a master that
has changed underneath them will collide.

## Done when

Master's file layout matches `RESTRUCTURE_MAPPING.tsv`'s `new_path` column for
every row still applicable, `RESTRUCTURE_REPOINT_SITES.tsv`'s referrers are
repointed, both suites are green, and `restructure/parked-20260731` is either
merged or explicitly superseded. Verify with a script that diffs current
master paths against the mapping's `new_path` column and reports any row not
yet satisfied.

## Stories

- [x] S1 — Re-verify `RESTRUCTURE_MAPPING.tsv` against current master: which
      rows are still valid, which collide with post-park commits (E-001's own
      `engineering/` tree did not exist when the mapping was written).
      **Done (dispatch W28, measured):** 191 rows valid, 6 need amending, 2
      dead, ZERO path collisions.
- [x] S2 — Amend the replay mapping's 6 needs-amending + 2 dead rows against
      current master, per the director's settled per-row rulings (dispatch
      W33): the `HANDOFF_CURRENT.md` dead-row supersession, the
      `BACKLOG_DEFERRED.md` removal, `holdout_gate_exemptions.txt`
      reclassified DERIVED, the `whale_footprint_fetcher.py` 3-way conflict
      marked MANUAL, the fixture ADDED row annotated with its parked blob
      SHA, and the two DEFERRED glob corrections expanded into their literal
      rows (28 `done/`-lowercase + 2 `analysis-reports`-spelling). `docs/ROADMAP.md`
      left UNRESOLVED-PENDING-DIRECTOR — the earlier "drop it" ruling was
      withdrawn as too quick; see this dispatch's report for the
      section-by-section evidence. **Done (dispatch W33).** New row total:
      196 (was 199) — 188 `RENAMED` (the true move count), 3 `DELETED`,
      1 `MODIFIED`, 1 `DERIVED`, 1 `MANUAL`, 1 `ADDED`, 1
      `UNRESOLVED-PENDING-DIRECTOR`.
- [ ] **S2a — COORDINATION GATE, blocks S3.** Dorian pulled master into the
      Mac fork on 2026-08-03 and has in-flight `strategy-research` test fixes
      open there (the POSIX path-traversal one-liner). A ~191-file rename
      lands on whatever he has open. No files move until a window is agreed
      with him. This is a gate, not a suggestion — S3 does not start without
      it. Correcting the record: the director previously claimed Dorian's
      Kraken work was inside the blast radius; it is not —
      `trading-bot/tools/ingest_kraken_archive.py` is outside
      `strategy-research/`, which is all E-002 touches. The gate stands on
      the in-flight test fixes, not on the Kraken work.
- [ ] S3 — Execute the replay (188 `RENAMED` moves; the 8 non-move rows —
      3 `DELETED`, 1 `MODIFIED`, 1 `DERIVED`, 1 `MANUAL`, 1 `ADDED`, 1 left
      `UNRESOLVED-PENDING-DIRECTOR` — are handled per their row's own
      annotation, not as plain moves). S3 MEASURES the full research suite's
      collected count before the move and again after, and compares the two
      — write NO target number into this epic. Reference point only, not a
      pass criterion: Dorian measured 708 passed / 2 failed / 11 skipped =
      721 collected on macOS (post-CLEAN-series). The director's earlier
      "710" was a misreading that dropped the skips; the operator's own HQ
      banner figure of 472/1 is stale — it predates the CLEAN-series test
      additions. The test is before == after, never equality with a
      constant.
- [ ] S4 — Repoint every referrer in `RESTRUCTURE_REPOINT_SITES.tsv`.
- [ ] S5 — Run both suites; fix the "knowingly incomplete" pipeline breakage
      the park commit disclosed.
- [ ] S6 — Independent audit (read-only) before merge/close, per this
      campaign's standing independent-audit-before-ratify rule.

## Log

- 2026-08-03 — `new` → `planned`. Seeded from E-001's S1 and written up in
  E-001 S4 (dispatch W24), using the replay mapping already recorded in
  `3cfa7b24`. Not started.
- 2026-08-04 — S1 marked done with W28's measured counts (191 valid / 6
  amend / 2 dead / 0 collisions). S2 (amend the mapping) done — dispatch
  W33 applied the director's 7 settled row rulings, left `docs/ROADMAP.md`
  UNRESOLVED-PENDING-DIRECTOR pending an operator choice among
  archive-as-legacy / move-to-engineering / split, and self-verified the
  result (every old_path exists on current master, zero new_path
  collisions, zero collisions with paths master already owns). Added S2a as
  a hard coordination gate ahead of S3 (Dorian's in-flight test fixes on the
  Mac fork) and split old S2's "replay" into its own S3, renumbering the
  former S3/S4/S5 to S4/S5/S6. Corrected the parked-commit reference: three
  distinct SHAs (`4adb7403` park commit, `1f7525f8` branch tip,
  `3cfa7b24` master's copy of the mapping), previously conflated under one
  hash. Files moved: none — mapping only.
- 2026-08-05 — L48 (`docs/ROADMAP.md`, `UNRESOLVED-PENDING-DIRECTOR`) dropped
  from `RESTRUCTURE_MAPPING.tsv`, per E-013's ruling (dispatch W36): the
  file's disposition is owned by E-013, which splits and renames it — not
  "master keeps the file" (that reasoning was already withdrawn above), but
  that this replay must not relocate a file separate work is restructuring.
  Row total: 196 → 195 (188 `RENAMED`, 3 `DELETED`, 1 `MODIFIED`, 1
  `DERIVED`, 1 `MANUAL`, 1 `ADDED`, 0 `UNRESOLVED-PENDING-DIRECTOR`).
  `RESTRUCTURE_REPOINT_SITES.tsv` checked for the same reference — none
  found, no change needed there. Files moved: none — mapping only.
