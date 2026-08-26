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
- [x] S2 — Emit the selection record and the unpursued-variant pool.
      **Done 2026-08-25.**
- [x] S3 — Point E-032's gate at the recorded selection; retire the
      parent-card read. **Done 2026-08-26.**

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

- 2026-08-25 — **S2 done: the selection record and the discard pool, built at
  the code seam, not the schema.** Implements S1 Task 3 exactly, with the
  2026-08-24 review's fix baked in from the start (Option A: enforce at the
  seam, not Option B/schemas-live-repo-wide, which stays out of scope).

  **Task 1 (SKILL.md):** `backtest-engineering/SKILL.md` gets one new
  "IMPROVEMENT 01 — Name the Chosen Variant" section: `backtest_spec.yaml`
  MUST carry `selected_variant_id`, copied verbatim from the
  `expanded_variants` entry implemented (variant_id, else id/name/
  variant_name/label, else the bare string itself), whenever
  `status: spec_ready`. If no menu entry honestly matches, that's a
  `component_gap`, same as a missing engine piece — never a fabricated
  hybrid. `backtest_spec.schema.json` also gets the field added (documentation
  only, `$comment`-flagged as unenforced — matches the review's finding that
  nothing loads these schemas).

  **Task 2 (derivation rule):** one function, `_derive_variant_id(variant,
  index)` in `workflow/run_phase1_research.py`, implementing S1's rule exactly:
  dict+`variant_id` verbatim -> dict+`id`/`name`/`variant_name`/`label` (first
  present) -> bare string or id-less dict -> `str_{index}_{hash8}` (sha256,
  stable across re-reads, distinct per position even for identical text).
  Used identically by both the record-writer (this story) and, per S1's note,
  reusable as-is by S3's future gate-matching code — not duplicated.

  **Task 3 (the enforcement, the real deliverable):** `_record_variant_
  selection(run_dir)`, called from `run_loop` right where `current_stage ==
  "backtest_specification"` and `next_stage in ("signal_prescreen",
  "protocol_execution")` — i.e. only on the confirmed spec_ready path
  (component_gap means no config/variant was implemented, nothing to record).
  Flag off (`orchestrator.variant_selection_record.enabled`, default false,
  same shape as S2a/S2b/S2c's three flags in `config/campaign_config.yaml`):
  returns before reading anything else — no file touched. Flag on: loads
  `backtest_spec.yaml.selected_variant_id` — **RAISES if absent** (the actual
  enforcement; the schema's "required" is decorative, per the 2026-08-24
  finding that no schema under `workflow_artifacts/schemas/` is loaded by any
  code, verified again independently this session by grep). Matches it against
  `expanded_hypothesis_card.yaml.expanded_variants` via `_derive_variant_id` —
  **RAISES if unmatched** (refuses to write a record pointing at a
  hallucinated ID). On a match: writes `artifacts/variant_selection.yaml`
  (`run_id`, `hypothesis_id`, `selected_variant_id`, the matched variant
  copied verbatim, resolved `instrument`/`timeframe` — variant override else
  parent `hypothesis_card.yaml`, per S1's Task 2 finding that only ~15%/~24%
  of variants carry these themselves — and `chosen_rationale` lifted from
  `backtest_spec.yaml.config_rationale` else `decision.yaml.rationale`) and
  `artifacts/variants_not_pursued.yaml` (every other menu entry, verbatim,
  tagged with its derived/native id + `run_id` + `hypothesis_id`, optional
  best-effort `lost_reason` never fabricated when absent).

  New schema files `variant_selection.schema.json` /
  `variants_not_pursued.schema.json` added for documentation, both
  `$comment`-flagged the same way as the `backtest_spec.schema.json` edit:
  nothing loads them; `_record_variant_selection`'s own code is the source of
  truth.

  **Flag-off proof (Done-when #4):** `tests/test_variant_selection_record.py`
  snapshots every file under `artifacts/` (path + byte content) before and
  after calling `_record_variant_selection` with the flag off — asserts the
  snapshot is byte-identical and neither new artifact file exists. This is
  the same "genuine no-op, not run-and-discard" bar as S2a/b/c's own
  prompt-text diffs, adapted to this function's shape (it never touches
  prompt assembly — it runs strictly after a stage's output already exists —
  so the comparable surface is the artifacts directory itself, not
  `_build_stage_prompt`'s output).

  **Task 4 (tests, 23 new, all passing):** flag-off bit-identity (2 tests,
  including one proving flag-off doesn't even raise on a broken
  `backtest_spec.yaml`) + flag-absent-key-and-section (1); derivation rule —
  dict+variant_id, dict+id-no-variant_id, dict+name-no-id, bare string
  positional-hash stability and distinctness, id-less dict fallback (7);
  missing `selected_variant_id` raises (1); unmatched `selected_variant_id`
  raises (1); dict-with-variant_id end-to-end record correctness (1);
  bare-string variant selectable via its derived id (1); id-only dict
  end-to-end (1); instrument/timeframe fallback-to-parent and
  variant-override-wins (2); `variants_not_pursued` excludes-selected/
  none-dropped/none-duplicated (1); `lost_reason` carried-when-present/
  never-fabricated-when-absent (1); **run_019 real-corpus regression fixture**
  — the three real threshold variants (17.5/20.0/22.5) frozen verbatim from
  `runs/run_019/artifacts/expanded_hypothesis_card.yaml`, with only the
  (synthetic — no historical run carries this field yet) `selected_variant_id:
  V2-THRESHOLD-20p0` added to a copy of the fixture, confirming the selection
  record matches variant 2 of 3 verbatim and the discard pool holds exactly
  the other two, by id (1).

  **Suites, full run, both green, MEASURED not estimated:** strategy-research
  **1026 passed** (reference 1003 + this story's 23 new tests, exact
  arithmetic match, zero drop elsewhere); trading-bot **383 passed / 2
  skipped**, unchanged from reference. No campaign or backtest run, no LLM
  spend, `local_data/holdout_sealed/` never opened.

  **Out of scope, not built, per the dispatch:** S3 (repointing E-032's gate
  at `variant_selection.yaml`) — `tools/anti_adjacency_gate.py` and
  `_route_post_innovation_expansion` untouched. Nothing else was narrowed;
  everything in the dispatch's Tasks 1-4 landed as specified.

- 2026-08-25 — **S2 reviewed by the dispatching session. Verified, not
  relayed: the fail-loud enforcement is real code, not documentation.**

  Read `_record_variant_selection()` and `_derive_variant_id()` directly:
  both match S1's Task 3 spec exactly, including the priority-chain
  derivation and the two RAISE points (missing `selected_variant_id`;
  `selected_variant_id` naming something outside the menu). Confirmed the
  schema file was updated for documentation only, with an explicit
  `$comment` saying nothing loads it — Option A, not Option B, as required.

  Suite run independently: strategy-research **1026 passed** (1003 baseline +
  23 new, zero regressions). The run_019 regression fixture (real three
  threshold variants: 17.5/20.0/22.5) passes on its own when isolated.

  **The one flagged concern checked out as a non-issue, not a bug.**
  `expanded_hypothesis_card.yaml` also carries a separate
  `regime_specific_variants` list (1 entry on `run_019`). S2 only matches
  against `expanded_variants`. Verified: `backtest_specification`'s own
  handoff template and `SKILL.md` never reference `regime_specific_variants`
  as a pickable option anywhere — it is not part of the stage's contract, so
  it was never a candidate `selected_variant_id` could legitimately name.
  If the stage's own reasoning ever did pick something from there against its
  instructions, S2's fail-loud check would correctly halt the run rather than
  silently accept an out-of-menu selection — that is the intended behaviour,
  not a defect to patch. No fix applied; none needed.

- 2026-08-26 — **S3 done: E-032's gate now evaluates the CHOSEN VARIANT, at
  a NEW, LATER call site — not a redirect of the existing one.** Closes the
  OPEN DEFECT E-032/EPIC.md logged on 2026-08-24 (see that epic's own
  2026-08-26 Log entry for the closure record). Off by default; no campaign
  or backtest run; no LLM spend; `local_data/holdout_sealed/` never opened.

  **Task 1 — the new call site.** `_route_post_variant_selection(run_dir,
  run_id)` in `workflow/run_phase1_research.py`, called immediately after
  `_record_variant_selection()` succeeds in `run_loop`'s
  `backtest_specification` branch (same lifecycle point, same run_loop
  region S2 already hooks into — right after `variant_selection.yaml` is
  written, before the config-schema validation subprocess runs). The
  pre-existing `_route_post_innovation_expansion` is untouched: it still
  runs before `validation`, still reads the parent `hypothesis_card.yaml`,
  and still does its own, narrower job ("was the original idea a repeat").

  Candidate construction, per S1 Task 4's explicit recommendation ("merging
  base-card fields for anything the variant doesn't override"): starts from
  the parent `hypothesis_card.yaml` (for `library_lookup`/`edge_source`/
  `thesis` — measured, across the 138-variant corpus, essentially absent
  from variant definitions themselves), then overlays the chosen variant's
  own fields (`variant_selection.yaml`'s `variant_definition`) on top, and
  sets `hypothesis_id` from `variant_selection.yaml`'s own (base-mechanism)
  value. `instrument`/`timeframe` are NEVER derived from this merged dict —
  they are passed explicitly via `evaluate_candidate()`'s `instrument=`/
  `timeframe=` override parameters, sourced verbatim from `variant_
  selection.yaml`'s already-resolved fields (S2 did the variant-override-
  else-parent-card resolution once; this story does not redo it). This is
  the exact override mechanism the E-032 2026-08-24 Log entry flagged as
  built and never used. `tools/anti_adjacency_gate.py` itself needed no
  change.

  Why `hypothesis_id` stays the BASE mechanism id, not `selected_variant_
  id`, despite the epic's own success signal wording ("references the
  chosen variant's identifier, not the base hypothesis id"): Layer 1 (KB)
  matches via `hypothesis_id` containment against `campaign_knowledge_
  base.yaml` findings, which are registered at MECHANISM grain (e.g.
  `funding_rate_continuous_mean_reversion_expanded_auto`), never per-variant
  (`V2-THRESHOLD-20p0`-shaped ids never appear in the KB). Using the variant
  id as the matching key would silently break every KB match, including the
  calibration case. Resolved by keeping the MATCHING key at mechanism grain
  and instead recording the variant identifier on the RESULT ARTIFACT:
  `variant_anti_adjacency_result.yaml` now carries `selected_variant_id`
  and `hypothesis_id` alongside the gate's own `route`/`layer`/`reasons`, so
  the success signal is satisfied at the artifact a human/future stage
  actually reads, without breaking the gate's own logic.

  **Task 2 — REFUSE policy, decided here, not copied from S2c.** S2c's
  "retry 4 times then escalate" ruling (operator, 2026-08-23) was scoped to
  the EARLIER, pre-validation checkpoint, where only `innovation_
  expansion`'s output is at stake on a retry. At THIS checkpoint,
  `validation` and `backtest_specification` have already run — two
  additional LLM stages' spend beyond what the earlier checkpoint would
  lose. Landed: immediate escalation on the FIRST REFUSE, no automatic
  retry, via a DISTINCT flag (`variant_anti_adjacency_gate_refused`, never
  `anti_adjacency_gate_exhausted`). Reasoning (full version in
  `_route_post_variant_selection`'s own docstring):
  1. **Cost asymmetry** — retrying here throws away strictly more sunk work
     than S2c's checkpoint ever risked.
  2. **The lever doesn't fit the failure mode** — S2c's retry (regenerate an
     entirely new hypothesis) is the right response to "this whole idea is
     adjacent." A REFUSE here means something narrower: the ALREADY-ADMITTED
     parent idea's CHOSEN VARIANT pivoted into an excluded combination.
     Discarding the whole hypothesis doesn't target that, and additionally
     throws away every OTHER still-viable variant this run already
     persisted in `variants_not_pursued.yaml` — the exact artifact E-034
     built so that supply wouldn't be wasted.
  3. **A human has better information at hand than a blind retry would** —
     both `variant_selection.yaml` (what collided) and `variants_not_
     pursued.yaml` (what else was on the menu) are on disk at halt time.

  Escalation reuses the project's existing mechanism exactly:
  `status="paused_for_human"`, `flags.variant_anti_adjacency_gate_
  refused=True`, wired into `run_campaign._classify_human_pause` (new
  branch, positioned immediately after `anti_adjacency_gate_exhausted`) and
  mirrored into `_PAUSE_FLAG_TO_REASON` in the same commit — not as a later
  fix, specifically because the 2026-08-24 bug-fix pass's FIX 6 added a
  regression test
  (`test_every_known_sticky_flag_branch_has_a_pause_flag_to_reason_entry`,
  in `tests/test_halt_quarantine_policy.py`) precisely to catch a future
  omission of this kind — that test's `known_sticky_flags` tuple was
  extended with the new flag in this story, not left for it to catch later.
  Deliberately NOT added to `_QUARANTINE_SAFE_REASONS`/
  `_REQUEUEABLE_QUARANTINE_REASONS` — a genuine must-escalate, same as
  `anti_adjacency_gate_exhausted`. `docs/RUNBOOK.md` gets a new table row
  and is added to the sticky-flags reset list — caught immediately by
  `tests/test_holdout_research_only_gate.py::
  test_every_classifier_flag_is_in_the_runbook_reset_list` when first
  omitted, fixed in the same session.

  **Task 3 — off by default, gated, with an explicit dependency check.**
  New flag `orchestrator.variant_anti_adjacency_gate.enabled` in
  `config/campaign_config.yaml`, same shape as the five prior flags in this
  chain. **Depends on `orchestrator.variant_selection_record.enabled` also
  being on — enforced as a fail-loud `RuntimeError`, not a silent no-op.**
  Chosen over a silent no-op because this gate's only input,
  `variant_selection.yaml`, is written exclusively by the function the
  OTHER flag gates: a silent no-op would either always find the file absent
  (indistinguishable from a real misconfiguration) or, worse, read a STALE
  copy left over from an earlier flag-on run and evaluate the WRONG run's
  artifact — per this project's standing rule ("anything feeding decisions
  raises on degenerate inputs"), the same class of fix FIX 3 (2026-08-24)
  applied to the digest/KB required-inputs check at the earlier checkpoint.
  Flag-off bit-identity proven the same way every prior story in this chain
  proved it: `_route_post_variant_selection` returns `None` before reading
  anything else when the flag is off, verified by comparing actual
  `pipeline_state.yaml` bytes before/after and confirming no new artifact is
  written — not merely asserting the flag reads `False`
  (`tests/test_variant_anti_adjacency_gate.py::
  test_flag_off_returns_none_and_writes_nothing`).

  **Task 4 — tests, `tests/test_variant_anti_adjacency_gate.py`, 16 new,
  all passing.** Flag-off bit-identity (2); the dependency-on-`variant_
  selection_record` fail-loud check (1); missing-`variant_selection.yaml`
  caller-ordering raise (1); missing-digest/missing-KB fail-loud raises (2,
  mirroring FIX 3's discipline at this new call site); ADMIT writes the
  result artifact (1); REFUSE policy end to end — immediate escalation, the
  distinct flag, correct classification via the REAL `run_campaign._
  classify_human_pause`, confirmed outside both quarantine sets (3); the R11
  table cross-check for the new flag (1); the calibration case (4h funding
  retest ADMITs) re-proven through THIS new call site, built via the REAL
  `_record_variant_selection()` against real KB/run_059 artifacts, not a
  hand-typed candidate (1) — mirroring `test_anti_adjacency_retry_policy.py
  ::test_calibration_case_still_admits_through_the_orchestration_layer`'s
  own "through orchestration, not just the gate's own unit level" bar; and
  **the single most important test, per the dispatch**
  (`test_pivot_away_from_clean_parent_is_caught_only_by_the_new_call_site`):
  one run, a CLEAN parent card (`keltner_channel`, BTCUSDT/1h — nothing in
  the digest matches), a chosen variant whose OWN fields pivot to
  AVAXUSDT/4h — which DOES collide with the digest. The OLD call site
  (`_route_post_innovation_expansion`, reading only the parent card) ADMITs
  the run. The NEW call site (`_route_post_variant_selection`, reading the
  variant's resolved instrument/timeframe from `variant_selection.yaml`)
  REFUSEs the SAME run. Both routes are asserted directly against the real
  functions in the same test — this is the direct, executable proof the
  2026-08-24 defect is closed, not a theoretical argument.

  **Verification, MEASURED.** `tests/test_variant_anti_adjacency_gate.py`
  alone: 16 passed. Full strategy-research fast suite, run clean (foreground,
  144.08s): **1042 passed** — exactly 1026 (S2 baseline) + 16 (this story's
  new file), zero regressions, zero drift elsewhere. A mid-session run
  caught one real gap before this final count: `tests/test_holdout_
  research_only_gate.py::test_every_classifier_flag_is_in_the_runbook_
  reset_list` (a pre-existing regression test, not new) failed once because
  the new flag wasn't yet in `docs/RUNBOOK.md`'s reset snippet — fixed
  (see Task 2) and re-verified green, folded into the 1042 above. trading-bot
  fast suite: **383 passed / 2 skipped**, MEASURED, exactly unchanged from
  the reference figure — nothing under `trading-bot/` touched. No campaign
  or backtest run; no LLM call made; `local_data/holdout_sealed/` never
  opened.

  **Left out, stated plainly, not silently narrowed:** none of Tasks 1-4
  were narrowed. `tools/anti_adjacency_gate.py` itself needed no change —
  its `instrument=`/`timeframe=` override parameters already existed and
  worked exactly as designed. Noted, not fixed here (pre-existing, outside
  this story's mandate): `_record_variant_selection`'s `instrument`/
  `timeframe` resolution (E-034 S2) stores the parent card's raw
  `target_market` field verbatim when the variant carries no override — for
  a multi-symbol card (a real, common shape: e.g. `run_059`'s own
  `target_market: [BTCUSDT, ETHUSDT]`) this can be a LIST, not a scalar
  string. `evaluate_candidate()`'s `instrument=` override expects a single
  string to compare against digest triples; a list value never equals any
  triple's `instrument` string, so Layer 2 (digest) would silently never
  match on such a candidate's fallback-resolved instrument. This does not
  affect any test or case built in this story (the pivot test's variant
  carries its own scalar override; the calibration case resolves entirely
  at Layer 1, which never reads instrument at all) — flagged here as a
  discovered gap for a follow-up story to fix in `_record_variant_
  selection` itself, not patched in this one.
