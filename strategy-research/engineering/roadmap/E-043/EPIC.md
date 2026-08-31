# E-043 — Refuse untradable or unimplementable briefs at registration

**State:** new
**Owner:** Jérémy
**Updated:** 2026-08-31

## Why

Two questions that should stop a run at the door are asked far too late, or by
nobody.

### 1. Tradability is checked at stage 13

The `research_only` gate fires inside `_route_holdout_evaluation` — **after**
hypothesis generation, expansion, validation, specification, prescreen and a
full walk-forward backtest. If it refuses, every one of those was spent on a
product the operator cannot legally trade.

The information it needs — venue and product — is available **at the brief**.
[E-015](../E-015/EPIC.md) already established declaring them at registration,
and `run_campaign.py::_materialize_run` already derives `research_only` there
from `config/venue_tradability.yaml`. **Only the check is late.**

Jérémy, 2026-08-31: *"it should be part of the step where feasibility of the
strategy should be checked, not checked at the very last step."*

Recorded as [E037-41](../E-037/FINDINGS.md#e037-41).

### 2. Implementation feasibility is nobody's job, and defaults open

The router reads
`refinement.get("decision", {}).get("implementation_allowed", True)` —
**defaulting to `True`** when the key is absent.

**The skill is never told to produce that key.**
`workflow_artifacts/skills/refinement-planner/SKILL.md` contains **zero**
occurrences of `implementation_allowed`, "component" or "framework". Its stated
mission is *"turn validation blockers into a concrete refinement artifact"*.

Measured over the 4 real `refinement_notes.yaml` files: **2 carry the key, 2
omit it.** In those 2 the router silently assumed "yes, implementable".

**This is the only open default in the module.** Everywhere else the convention
is explicit and opposite — `determine_post_spec_route` pauses on an unrecognised
status; every `orchestrator.*.enabled` flag defaults `False` with the comment
*"silence is never a green light"*. Here, silence is a green light.

Meanwhile the question *is* answered — at **stage 6**, which emits
`component_gap` when the engine lacks a piece. Jérémy's observation: that
should be rare or never, because feasibility was supposed to be settled
earlier.

Recorded as [E037-39](../E-037/FINDINGS.md#e037-39).

### 3. A related gap found alongside

`backtest_specification`'s handoff carries only
`expanded_hypothesis_card.yaml` and `validation_protocol.yaml`. It does **not**
receive `refinement_notes.yaml`. So on a refine loop the planner's conclusions
reach the stage that builds the config only if innovation_expansion folded them
back into the expanded card, and nothing checks that it did.
[E037-40](../E-037/FINDINGS.md#e037-40).

---

## Scope

### In

- **An early refusal at brief registration** for an untradable venue/product.
  Keep gate 2b at stage 13 as the last-line defence before the single-use
  holdout — the two are not alternatives.
- **Decide where feasibility is answered.** Either the refinement planner is
  instructed to answer it and the router defaults closed, or the question moves
  wholly to stage 6 and `implementation_allowed` is removed rather than left
  defaulting open.
- Add `refinement_notes.yaml` to the spec handoff, or document and check the
  expanded-card carry.

### Out

- Changing `venue_tradability.yaml`'s content or the venue survey behind it.
- The holdout gate's *ordering* relative to the seal — that positioning is
  deliberate and documented ("looking is spending") and stays.

---

## Stages

- [ ] **S1 — Characterise and stop.** How many briefs would an early gate have
      refused, given that **0 of 57 carry `research_only` at all**? Whether
      `component_gap` has ever actually fired. Where feasibility can be
      answered earliest with real information. Report, then stop.
- [ ] **S2 — (blocked on S1) Early tradability refusal** at registration.
- [ ] **S3 — (blocked on S1) Close the open default.** Whichever way S1
      decides, `implementation_allowed` stops defaulting to `True` on a key
      nobody is asked to write.
- [ ] **S4 — Handoff fix.** `refinement_notes.yaml` reaches the spec stage, or
      the carry is documented and checked.

## Risks

- **An early gate fails closed on every existing brief.** Measured: none carry
  `research_only`. S2 must decide whether registration back-fills it from the
  venue table (it already can) or whether existing queued briefs are
  grandfathered — and say which, loudly.
- **Moving feasibility earlier may just move the guess.** At registration you
  know less than after validation. S1's job is to find the earliest point where
  the answer is *real*, not merely the earliest point.

## Log

- 2026-08-31 — `new`. Both raised by Jérémy reviewing §2.2: the tradability
  check's position, and whether `component_gap` should ever fire given that the
  refinement planner is supposed to settle feasibility. Verifying the second
  found that the planner is never asked, and that the router defaults open.
