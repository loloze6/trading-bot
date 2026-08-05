# E-017 — Autopsy standard v1

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §3.1, verbatim: "**Autopsy standard v1, with the
right metrics (your addition, adopted).** Objective: every kill explains
itself precisely enough to make a prediction. Deliverable: a defined
**autopsy metric palette** the verdict stage must draw from: *profit per
forecast bin at entry* (does a stronger signal actually earn more? — the
table already exists in our diagnostics), *regime-identification correctness*
(when we labeled 'trending', was it, measured after the fact — and PnL
conditional on the label being right vs wrong), *forecast calibration*
(realized return vs predicted magnitude), *entry/exit efficiency, MAE/MFE,
post-exit returns* (already built), and *cost decomposition* (how much of
the loss is fees vs signal). Rule: no sibling of a killed family is
registered until the parent's autopsy is on file with at least one micro-test
of its claimed cause."

**The load-bearing part is the rule, not the palette itself**: the hard gate
— no sibling of a killed family is registered until the parent's autopsy is
on file with at least one micro-test of its claimed cause — is what this
epic must enforce. The palette is the menu the autopsy draws from; the gate
is what makes the autopsy mandatory rather than optional documentation.

**Blocked on:** Phase 2 verdict. §3.1 belongs to Phase 3 ("Hypothesis wave
2, with real autopsies"), whose own header states it runs "ongoing once
Phase 2 delivers." Phase 2's gate (`docs/ROADMAP.md` §Phase 2): "≥2 new data
axes on disk with provenance + a first registrable indicator each; recorders
running."

## Done when

1. A defined autopsy metric palette exists that the verdict stage draws from:
   profit per forecast bin at entry; regime-identification correctness
   (post-hoc label check + PnL conditional on label correctness); forecast
   calibration (realized vs. predicted magnitude); entry/exit efficiency,
   MAE/MFE, post-exit returns; cost decomposition (fees vs. signal).
2. The hard gate is enforced mechanically: registering a sibling of a killed
   family fails (or is blocked at registration) unless the parent's autopsy
   is on file with at least one micro-test of its claimed cause.

## Stories

- [ ] S1 — (blocked behind Phase 2's gate) Define and wire the autopsy metric
      palette into the verdict stage.
- [ ] S2 — Implement the sibling-registration gate against parent-autopsy
      presence + micro-test.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §3.1 (dispatch W35). Parked on Phase 2's gate.
