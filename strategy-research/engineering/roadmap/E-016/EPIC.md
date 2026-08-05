# E-016 — Fee-reduction autopsy field

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §1.4, verbatim: "**Fee-reduction autopsy field
(your addition, adopted).** Objective: cost-kills must generate ideas, not
just tombstones. Deliverable: whenever a kill's root cause is cost-dominated,
the autopsy must answer one mandatory question — *'is there a system that
reduces these fees?'* (maker-only execution, lower-frequency variant of the
same signal, different product, venue tier, batching) — and, if yes, register
the cheap variant as a new idea."

**Blocked on:** E-010 (fee/slippage attribution) and E-017 (autopsy standard
v1, which owns cost decomposition). A cost-dominated kill cannot be
identified as cost-dominated before either exists: E-010 supplies the
fee-vs-slippage split in the run artifact, and E-017 supplies the cost
decomposition metric in the autopsy palette that this field's "cost-dominated"
trigger depends on.

## Done when

1. The autopsy process includes a mandatory field, triggered whenever a
   kill's root cause is cost-dominated: "is there a system that reduces these
   fees?" — evaluated against the named options (maker-only execution,
   lower-frequency variant of the same signal, different product, venue
   tier, batching).
2. When the answer is yes, the cheap variant is registered as a new idea,
   observable as a new registration entry that references the parent kill.

## Stories

- [ ] S1 — (blocked behind E-010 and E-017) Add the mandatory fee-reduction
      question to the autopsy template, gated on cost-dominated root cause.
- [ ] S2 — Wire the "yes" branch to brief registration of the cheap variant.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §1.4 (dispatch W35). Parked: cannot proceed until E-010
  and E-017 exist. Resumes when both land.
