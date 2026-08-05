# E-011 — Shared campaign execution location

**State:** new
**Owner:** Jeremy (joint with Dorian)
**Updated:** 2026-08-04

## Why

The enhancement, in the operator's own words: **a shared run folder that
both parties can launch.** ("Shared campaign execution location" is the
same thing said less precisely.)

Trial-ledger Option A (single-writer: campaigns run only on Jeremy's master,
Dorian's fork stays engine work) exists because two forks share one holdout
and one deflated-Sharpe N with no way to combine trial counts — see the
Trial-Ledger Merge Protocol decision, Notion. A shared location with ONE
authoritative `campaign_state` dissolves that constraint rather than working
around it. Option A was confirmed by the operator on 2026-08-03 as an
**interim** measure, explicitly "until a next enhancement." E-011 is that
enhancement, and its delivery retires Option A.

Sequencing: the fork's dual-writer merge protocol and E-011 are **not
competing designs.** Dual-writer accepts the concurrent-write race and
manages it (disjoint trial-ID allocation, append-only union merges, no
DSR/promotion/holdout touch until both ledgers merge) and works today on two
machines. E-011 removes the race entirely, but needs a shared host that does
not yet exist. Dual-writer is the interim; E-011 is the endpoint.

This deliberately and temporarily **relaxes single-writer for campaigns.**
The fork cited single-writer as binding when handing over the E-010 spec;
that constraint is being revisited here on purpose, not drifting.

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
- 2026-08-04 — `new` (unchanged). Sharpened Why to the operator's scope line
  (a shared run folder both parties can launch); recorded Option A as an
  operator-confirmed interim pending this epic, and the dual-writer/E-011
  sequencing (interim vs. endpoint, not competing designs); recorded the
  deliberate, temporary relaxation of single-writer for campaigns. See
  PROCESS.md amendment 8(d) for the evidence this addresses.
