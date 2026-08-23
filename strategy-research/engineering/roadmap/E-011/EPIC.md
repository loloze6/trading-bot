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

Not yet fully written — still depends on the E-003 unblock (see Log
2026-08-18: not a quick fix, has an open design question of its own). The
machine half is no longer an open question: `culi.to` is the shared host
(see S1a below), so "define the shared location" is done; "write-
serialization for `campaign_state`" and the actual cutover from Option A
are what remain once E-003 clears.

## Stories

- [x] S1a — Provision the shared host. Folded in 2026-08-18 from the
      standalone "Ubuntu server deployment readiness" bug card (Notion,
      closed as a pointer here): `culi.to` (Ubuntu 24.04, 4c/8GB/145GB) is
      live, the fork is cloned, and baseline `simulate` reproduces the
      reference run byte-identically (`5ccbec42`/`5a75366c`/−23.021%/−5.646,
      deterministic ×2), fast 260/0 + slow 14/0 green — done 2026-08-08.
      Residual pieces from that card, not yet done: Jeremy's own SSH access
      (his key sent 2026-08-18, awaiting Dorian adding it to
      `authorized_keys`); the CI Linux leg is covered by the repo's own
      `.github/workflows/tests.yml` (ubuntu-latest already in the matrix),
      so no separate action needed there; the Kraken recorder has still
      never actually been run on a Linux host (systemd unit + rsync bundle
      exist in `deploy/kraken_recorder/`, untested); bit-identity on the
      real server stack was proven once (leg 6B) but wants re-confirming
      whenever the toolchain there changes.
- [ ] S1b — **Blocker cleared 2026-08-18** (E-003 closed `done`; the seal gate
      is enforceable in every clone). The "(blocked behind E-003)" note here
      outlived its blocker by 5 days — EPICS.md's own row already recorded the
      clearance, this story line did not. Remaining work, unchanged:
      write-serialize `campaign_state` for concurrent launches and cut over
      from single-writer Option A. Joint with Dorian.

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
- 2026-08-18 — Folded in the standalone "Ubuntu server deployment
  readiness" Notion bug card as S1a (Jeremy's call: don't run two tracking
  threads for the same underlying work) and closed that card as a pointer
  here. S1a is effectively done — the shared machine E-011 needed no longer
  needs deciding, `culi.to` already is it. Still genuinely blocked on S1b:
  investigated E-003 the same day and it is NOT a quick unblock (see
  `E-003/EPIC.md` Log) — the seal gate cannot be safely turned on yet, so
  neither can write-serialized shared campaigns.
- 2026-08-18 (later) — **E-003 closed `done`; this epic's blocker is
  cleared.** Design input (b) above — "the seal gate must be enforceable
  there, so this epic is BLOCKED BEHIND E-003" — is satisfied, and in a
  stronger form than assumed when it was written: enforcement now lives in
  CI, so it holds on `culi.to` (or any host) with no per-machine setup at
  all, rather than depending on each clone being configured correctly.
  Running `setup_hooks.sh` on the server is still worth doing for
  fast local feedback, but is no longer load-bearing for the gate.
  S1b (write-serialize `campaign_state`, retire single-writer Option A) is
  now the live next step. Note it overlaps E-025's S4 — both concern
  concurrent writers to the same trial ledger — so sequence them together
  with Dorian rather than solving the race twice.
