# E-015 — Venue/product declared at brief registration

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §1.3, verbatim: "**Registration rule: venue
declared.** Objective: no more testing on an unauthorized system's
assumptions. Deliverable: every new brief states venue + product; anything
using a product not legally tradable for you is auto-flagged **research-only**
at registration. Immediate consequence to settle: whether the funding family
is live-tradable at all (perp access), or research-only."

Of the seven items in the audit, this is the only one actionable today with
nothing in front of it — no dependency on E-010, E-012, or a phase gate.

## Done when

1. The brief registration schema requires a venue field and a product field;
   registration of a brief missing either fails rather than proceeding with
   an implicit default.
2. At registration, any brief whose declared product is not legally tradable
   for the operator (French non-professional) is auto-flagged
   `research-only`, without a manual step.
3. The immediate consequence named in the source text is settled as part of
   enacting this rule: whether the funding family is live-tradable (perp
   access) or `research-only` is decided and recorded.

## Stories

- [ ] S1 — Add venue + product as required fields to the brief registration
      schema/contract; wire the auto-flag for products not legally tradable
      for the operator.
- [ ] S2 — Settle and record the funding family's venue status (live-tradable
      perp access vs. research-only) as the rule's first application.

## Log

- 2026-08-05 — `new`. Created from E-013 S1's audit of `docs/ROADMAP.md` §1.3
  (dispatch W35). No dependency; ready to dispatch.
