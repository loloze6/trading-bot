# E-034 — Record which variant was chosen, and keep the ones that weren't

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-24

## Why

The pipeline generates a menu of ideas, tests one, and throws the rest away
without writing down either the choice or the discards. Both halves cost
something real, and both are fixed by the same small change.

### Measured

- **138 variants generated** across the 43 runs carrying an
  `expanded_hypothesis_card.yaml`; up to 8 in a single run. Exactly **one**
  configuration is backtested per run.
- **1 file out of 59 runs** contains any record of unpursued variants (grep
  for `variants_not_pursued` across the whole corpus).
- **No artifact names the chosen variant.** Verified on `run_019`, which
  produced three distinct threshold variants (17.5 / 20.0 / 22.5):
  `validation_decision.yaml` names only the base hypothesis;
  `backtest_spec.yaml` contains no variant reference at all. The narrowing
  happens inside LLM reasoning and leaves no trace.
- On **2026-07-19** the campaign logged *"Queue exhausted — no ready or
  in_progress entries remain"* and has been stopped since. It did not run out
  of ideas — it discarded roughly a hundred of them, unrecorded, and then
  reported itself empty.

### Why this specific change, and not a bigger one

Three payoffs from one small artifact, none of which requires moving a stage
boundary or invalidating a baseline:

1. **It makes the anti-adjacency gate able to do its job.** E-032's gate
   currently evaluates the parent `hypothesis_card.yaml` because that is the
   only concrete candidate that exists at the point it runs. The real
   candidate — whichever variant is about to be tested — is never written
   down, so the gate cannot read it. Once selection is recorded, "gate the
   chosen variant" stops being a design problem and becomes a one-line read.
   **This is the actual fix for the wrong-artifact defect found in the
   2026-08-24 review**, and it is why that defect was deliberately not
   patched at the time.
2. **It gives E-031's queue refill a real source.** E-031 S1 measured exactly
   **one** legitimate refill candidate in the entire system. A persisted pool
   of already-generated, already-reasoned-about variants — filtered by
   E-032's gate — is a materially better answer to "what should the loop do
   next" than one reactivation clause.
3. **It stops paying for output that is thrown away.** ~100 of 138 generated
   variants were discarded with no record.

## Done when

1. When the pipeline narrows N variants to 1, an artifact records **which**
   variant and **why**, in a form a later stage can read mechanically (not
   only prose).
2. Variants not pursued are persisted with enough context to be reconsidered
   later — at minimum the variant's own definition and the reason it lost.
3. E-032's anti-adjacency gate reads the recorded selection rather than the
   parent card. (Coordinate with E-032; this closes the review defect logged
   there on 2026-08-24.)
4. Off by default with a bit-identity proof, per the standing rule — a new
   artifact that changes what any LLM stage receives changes its output.
5. Both fast suites green.

## Stories

- [ ] S1 — **Characterize and STOP.** Where in the chain is the selection
      actually made? `determine_post_validation_route` and
      `determine_post_spec_route` are the routing candidates, but the
      narrowing may happen inside the `backtest_specification` LLM stage with
      no routing decision at all — establish which, from the code and the run
      corpus, before designing an artifact. Also: what is the minimum content
      that makes a discarded variant reconsiderable later?
- [ ] S2 — Emit the selection record and the unpursued-variant pool.
- [ ] S3 — Point E-032's gate at the recorded selection; retire the
      parent-card read.

## Relationship to other epics

- **E-032** — S3 here closes the wrong-artifact defect recorded in E-032's
  Log on 2026-08-24. E-032's gate is not trustworthy for its stated purpose
  until this lands: it currently checks the pre-expansion idea, so anything
  `innovation_expansion` invents is ungated.
- **E-031** — the persisted pool is a refill source. E-031 S1 found only one
  candidate; this is the supply side of the same problem.
- **E-033** — may later conclude the pre-backtest chain should be reshaped
  entirely. This epic is deliberately the *targeted* fix that works under the
  current shape, and is worth doing regardless of E-033's outcome, because a
  record of what was chosen is needed under any shape.

## Success signal (pre-registered)

Within the first run after S2 ships: an artifact exists naming the tested
variant and listing the unpursued ones, and the count of persisted unpursued
variants is greater than zero. After S3: E-032's gate result references the
chosen variant's identifier, not the base hypothesis id.

## Log

- 2026-08-24 — `new`. Opened at the operator's direction, following a design
  review that surfaced the 138-generated / ~1-tested / ~0-recorded gap. The
  operator considered a full pre-backtest redesign (now E-033) and chose to
  run this targeted change alongside it rather than instead of it.
