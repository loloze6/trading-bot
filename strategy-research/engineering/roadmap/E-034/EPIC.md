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

- [x] S1 — **Characterize and STOP.** Where in the chain is the selection
      actually made? `determine_post_validation_route` and
      `determine_post_spec_route` are the routing candidates, but the
      narrowing may happen inside the `backtest_specification` LLM stage with
      no routing decision at all — establish which, from the code and the run
      corpus, before designing an artifact. Also: what is the minimum content
      that makes a discarded variant reconsiderable later?
      **Done 2026-08-24** — `engineering/roadmap/E-034/artifacts/s1_selection_record.md`.
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
- 2026-08-24 — **S1 done.** Full findings in
  `engineering/roadmap/E-034/artifacts/s1_selection_record.md`; measurement
  script alongside it (`s1_measure_variants.py`, re-run any time). Headline:
  reproduced the EPIC's 138/43/8 and 1-of-59 counts exactly. The narrowing is
  confirmed to happen **inside `backtest_specification`'s LLM reasoning**,
  not in either routing function — `determine_post_validation_route` and
  `determine_post_spec_route` both read only a `status` string and never
  touch variant identity; `_route_post_innovation_expansion` (E-032's gate
  call) runs *before* `validation`, structurally too early to see variants at
  all. Neither `backtest_spec.yaml` nor `decision.yaml` has a schema field
  for the chosen variant; the identifier sometimes leaks into `decision.
  yaml`'s free-text `rationale` (6/19 multi-variant runs checked have zero
  such mentions, several others name multiple candidate IDs with no
  disambiguation) — not usable as a mechanical source. Corpus reality:
  `expanded_variants` items are 74 dict / 64 bare-string across the 138
  (schema declares bare-string-only — real corpus mostly disagrees with its
  own schema); `variant_id` covers 92% of dicts, no key is universal;
  instrument/timeframe live on the *parent* `hypothesis_card.yaml`
  (schema-required there) far more reliably than on the variant itself
  (~15%/~24% presence) — a selection record must resolve, not just read.
  Recommendation: split responsibility — LLM picks from a closed set (one
  new required `selected_variant_id` field on `backtest_spec.yaml`, same
  shape as its existing `status` field) and a new deterministic function
  (`_record_variant_selection`, called at the same stage-output-validation
  lifecycle point `_apply_b7_mandatory_inputs`/friends already use) joins
  that pick against the menu to write `variant_selection.yaml` and
  `variants_not_pursued.yaml` verbatim — no second LLM call, no moved stage
  boundary. `variants_not_pursued` (used once, in `run_0001/artifacts/
  innovation_notes.yaml`, wrong stage, unschemad, never repeated) should be
  superseded, not extended. Checked against both downstream consumers named
  in the epic: E-032's gate can consume the new record via its *existing*,
  currently-unused `instrument=`/`timeframe=` override parameters on
  `evaluate_candidate()` — but S3 needs a **new, later gate call site**
  (after `backtest_specification`, not a redirect of the existing
  pre-validation call), so S2+S3 together close the defect, not S2 alone.
  E-031's refill (per its own S1, `engineering/roadmap/E-031/artifacts/
  s1_refill_sources.md`): a persisted E-034 pool is a legitimate but
  *lower-tier* candidate than E-031's one open KB-reactivation source — it
  has no pre-existing evidentiary bar (never itself run or falsified) — and
  per E-031's own recommended policy it must clear E-032's anti-adjacency
  gate plus the existing exclusion checks before being admissible, landing
  `paused:pending_operator_ratification` like every other E-031 source, never
  auto-`ready`. Sequencing dependency for whoever scopes this: E-034 S2 →
  E-032 S3 → only then is an E-034 discard pool usable E-031 refill input.
  No production code touched; no campaign/backtest run; no LLM spend.

- 2026-08-24 — **S1 reviewed by the dispatching session. Verified, plus one
  finding that changes S1's own recommendation.**

  VERIFIED independently, not relayed: neither `backtest_spec.schema.json`
  (`hypothesis_id`, `status`, `config`, `config_rationale`, `component_gap`)
  nor `decision.schema.json` (`hypothesis_id`, `stage`, `status`, `rationale`,
  `blocking_issues`) carries any field naming the chosen variant — so the
  narrowing genuinely has nowhere to be recorded today. Re-derived the corpus
  split from scratch: **74 dict / 64 bare-string variants, 138 total**, exactly
  matching S1. Suite after S1's docs-only commit: strategy-research **1003
  passed**, unchanged.

  **THE FINDING THAT CHANGES THE PLAN.**
  `expanded_hypothesis_card.schema.json` declares
  `expanded_variants: {type: array, items: {type: string}}`, and **74 of 138
  real variants (53%) are dicts** — i.e. most of the corpus violates its own
  schema. The reason: **no schema in `workflow_artifacts/schemas/` is loaded by
  any code at all.** Verified by grep across `workflow/` and `tools/` — the only
  hit is a source comment. Twelve-plus schema files that read as authoritative
  and enforce nothing.

  **Therefore S1's recommendation as written does not work.** It proposes "one
  new required `selected_variant_id` field on `backtest_spec.yaml`, same shape
  as its existing `status` field." Adding a *required* field to an unenforced
  schema produces a field that is declared and never checked — the LLM stage
  can omit it and nothing fails. The deterministic join S1 also proposes would
  then silently receive nothing.

  **S2 must therefore either** (a) enforce the field at the code seam that
  writes/reads it, independent of the schema file — a real check that raises,
  in the same fail-loud spirit as the 2026-08-24 gate fix — **or** (b) treat
  making the schemas live as a prerequisite and hand that to its own epic. (a)
  is smaller and does not block on a repo-wide change; (b) is the durable fix.
  S2 should state which it chose and why. **What S2 must NOT do is add the
  field and assume "required" means anything.**

  **This is now the fifth instance of one pattern**, and it deserves naming as
  a systemic finding rather than five coincidences: `register_hypothesis`
  (zero callers), `evaluate_and_persist_wishlist_predicate` (zero callers), the
  `campaign_knowledge_base.yaml` optional input path (never resolved),
  `stages.yaml` (never read — archived 2026-08-24), and now
  `workflow_artifacts/schemas/*.json` (never loaded). **This system reliably
  builds the correct declarative artifact and never wires anything to enforce
  it.** Any E-034 design that produces another such artifact repeats the defect
  it is trying to fix.

  ACCEPTED FROM S1 without change: the narrowing happens inside
  `backtest_specification`'s own LLM reasoning (neither
  `determine_post_validation_route` nor `determine_post_spec_route` reads
  variant identity — both read a bare `status`); the chosen variant leaks into
  `decision.yaml`'s free-text `rationale` on some runs but is absent on 6 of 18
  multi-variant runs and ambiguous on others, so it is not mechanically usable;
  and S3 needs a NEW gate call site after `backtest_specification` rather than
  a redirect of the existing pre-validation call — meaning **S2+S3 together**
  close E-032's wrong-artifact defect, not S2 alone.

- 2026-08-25 — **Filed as a Notion bug**, at the operator's direction: "each
  of these files were built for a purpose ... it is a feature that is not
  working properly." No GitHub CLI/token/MCP available in this environment to
  file a GitHub issue as first requested; filed on the project's live
  🐛 Bugs & Tasks board instead (its current standing tracker — GitHub
  consolidation is E-021, still `new`, unstarted).
  https://app.notion.com/p/3c61d1fb05a28126808cc607601ed1bc
