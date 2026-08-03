# E-002 — Land the parked `strategy-research/` restructure

**State:** planned
**Owner:** Jeremy
**Updated:** 2026-08-03

## Why

A ~190-file reorganization of `strategy-research/` was built and parked on
`restructure/parked-20260731` (commit `4adb7403`) pending unification with
Dorian's fork, which had diverged onto its own layout. The replay mapping was
recorded on master in commit `3cfa7b24`
(`docs/RESTRUCTURE_MAPPING.tsv` — 200 rows — and
`docs/RESTRUCTURE_REPOINT_SITES.tsv` — 32 rows) specifically so the move could
be replayed onto master later without re-deriving it. The parked branch's own
commit message records it as **KNOWINGLY INCOMPLETE**: `strategy-research`'s
own pipeline is broken on that branch as parked.

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

- [ ] S1 — Re-verify `RESTRUCTURE_MAPPING.tsv` against current master: which
      rows are still valid, which collide with post-park commits (E-001's own
      `engineering/` tree did not exist when the mapping was written).
- [ ] S2 — Replay the mapping onto master, resolving any collisions found in S1.
- [ ] S3 — Repoint every referrer in `RESTRUCTURE_REPOINT_SITES.tsv`.
- [ ] S4 — Run both suites; fix the "knowingly incomplete" pipeline breakage
      the park commit disclosed.
- [ ] S5 — Independent audit (read-only) before merge/close, per this
      campaign's standing independent-audit-before-ratify rule.

## Log

- 2026-08-03 — `new` → `planned`. Seeded from E-001's S1 and written up in
  E-001 S4 (dispatch W24), using the replay mapping already recorded in
  `3cfa7b24`. Not started.
