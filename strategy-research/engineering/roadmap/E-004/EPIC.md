# E-004 — Settle the shared record taxonomy with the fork

**State:** new
**Owner:** Jeremy (joint with Dorian)
**Updated:** 2026-08-03

## Why

Master and Dorian's fork have diverged on naming for the same class of
artifact: master keeps `strategy-research/briefs/`; the parked restructure
(commit `4adb7403`, `RESTRUCTURE_MAPPING.tsv`) renames the equivalent files to
`briefs_record/`. This is a live naming disagreement between two people
working the same repo, not a mechanical fix — E-002 (landing the restructure)
cannot proceed cleanly until this is settled, since the restructure encodes
one side's answer.

## Done when

**No testable "done when" yet — deliberately left unwritten.** This needs a
joint decision with Dorian on the taxonomy itself (which name, and the
broader principle it should generalize from) before there is anything to
verify mechanically. Writing a criterion now would mean inventing one side of
a decision that isn't mine alone to make. Once decided, this epic moves to
`planned` with a real "done when" (almost certainly: master's paths match the
agreed taxonomy, verified by a path diff, same shape as E-002's check).

## Stories

- [ ] S1 — Joint conversation with Dorian: settle the taxonomy and record the
      decision (and its reasoning) here.
- [ ] S2 — (blocked on S1) Apply it, coordinated with E-002's replay so the
      two don't fight each other.

## Log

- 2026-08-03 — `new`. Identified during E-001 S4 (dispatch W24) from the
  master-vs-fork naming divergence found in the restructure mapping. No
  decision made yet; not a dispatch until one exists.
