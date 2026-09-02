# E-019 — Feature matrix + leakage checks

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §4.1, verbatim: "**Feature matrix.** Objective: one
aligned table per date × coin of every surviving feature (momentum ranks,
carry, whale flows, regime state, costs). Deliverable: the matrix + leakage
checks."

Phase 4 infra: the ML ranker (§4.2) depends on this matrix existing before it
can be trained.

**Blocked on:** Phase 3 complete. `docs/ROADMAP.md`'s Phase 4 header states
it "starts when Phases 2–3 give a handful of individually-informative
features."

## Done when

1. A single aligned table exists, indexed by date × coin, of every surviving
   feature named in the source text: momentum ranks, carry, whale flows,
   regime state, costs.
2. Leakage checks are implemented against that matrix and pass — i.e., no
   feature column is built from information not available as of its row's
   date.

## Stories

- [ ] S1 — (blocked behind Phase 3 completion) Build the date × coin feature
      matrix from the surviving features Phase 2/3 produce.
- [ ] S2 — Implement and run leakage checks against the matrix.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §4.1 (dispatch W35). Parked on Phase 3 completion.
