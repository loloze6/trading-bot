# E-011 — Shared campaign execution location

**State:** new
**Owner:** Jeremy (joint with Dorian)
**Updated:** 2026-08-03

## Why

Trial-ledger Option A (single-writer: campaigns run only on Jeremy's master,
Dorian's fork stays engine work) exists because two forks share one holdout
and one deflated-Sharpe N with no way to combine trial counts — see the
Trial-Ledger Merge Protocol decision, Notion. A shared location with ONE
authoritative `campaign_state` dissolves that constraint rather than working
around it. Confirmed by the operator 2026-08-03 as the intended successor to
Option A.

Design inputs, not afterthoughts:
(a) the holdout becomes reachable from a machine either party can launch
    from — single-use and terminal, so this is not a convenience feature;
(b) the seal gate must be enforceable there, so this epic is **BLOCKED
    BEHIND E-003** — a shared launch location with an unenforced gate is
    strictly worse than today's single-machine gate;
(c) concurrent launches race on `campaign_state`'s trial count — the exact
    number the single-writer scheme protects — so the shared location must
    serialize writes, not just relocate them.

Procurement overlap with E-007 (recorder storage and host migration):
plausibly the same machine, different epics — do not conflate the two
decisions.

## Done when

Not yet written. Depends on the E-003 unblock and a decision on the shared
machine/location itself (overlaps E-007's procurement question). Revisit
once both are resolved.

## Stories

- [ ] S1 — (blocked behind E-003) Once the seal gate is enforceable in every
      clone, define the shared location and its write-serialization for
      `campaign_state`.

## Log

- 2026-08-03 — `new`. Surfaced from the fork sync (dispatch W27) as the
  successor to trial-ledger Option A. Next step: blocked behind E-003 — do
  not start before it.
