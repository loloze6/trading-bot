# E-033 S1 — Pre-backtest stage characterization (characterize-and-STOP)

**Scope:** `hypothesis_generation` → `innovation_expansion` → `validation` →
`backtest_specification`. No code changed, no stage boundary moved. Every
count below states its denominator and is labeled MEASURED (pulled from the
run corpus or code) or INFERRED (my reading of what a measurement implies).
Reproduce all MEASURED numbers with
`engineering/roadmap/E-033/artifacts/s1_measure_pre_backtest_stages.py`
(read-only, no network, no LLM — run from `strategy-research/`).

> ## ⚠️ CORRECTED 2026-08-25 — READ THIS BEFORE THE CONCLUSION BELOW
>
> Two of this artifact's INTERPRETATIONS were corrected after review. Its
> MEASUREMENTS are sound and independently reproduced — read those freely.
> Do NOT inherit its verdict or its "smallest lever" recommendation as
> written. Full detail in `E-033/EPIC.md`'s 2026-08-25 Log entry.
>
> **1. RETRACTED — the `innovation_expansion` "zero live routing decision"
> point is a timeline artifact, not a design finding.** The flag it depends
> on (`orchestrator.anti_adjacency_retry.enabled`) and the function it gates
> were both written on 2026-08-23/24, WEEKS AFTER all 59 corpus runs. A count
> over a corpus that predates the code being counted is not evidence about
> that code. The honest statement is "this stage never had a routing
> decision until one was added a day ago" — not "a decision point exists but
> has never fired."
>
> **2. WRONG TARGET — the recommended fix (wire `validation_decision.yaml.
> conditions` into `backtest_specification`) does not work, because most of
> those conditions are RESULT checks, not build instructions.** Real
> examples: *"Reject if Sharpe < -1.0"* (run_012), *"regime_frequency must be
> >= 0.15"* (run_011/012). `backtest_specification` could not act on these if
> it received them.
>
> **The corrected finding is better than the one below.** `validation`'s job
> is pre-flight pressure-testing of the IDEA; grading results is
> `verdict_interpreter`'s job — and the correct channel between them ALREADY
> EXISTS AND WORKS (`validation_protocol.yaml`'s `decision_rules` /
> `failure_modes`, which `verdict_interpreter`'s handoff lists as a required
> input). `validation_decision.yaml`'s free-prose `conditions` is a second,
> parallel, unread channel duplicating that structured contract. The S2/S3
> question is therefore **"why does `validation` emit result thresholds in
> loose prose at all?"** — not "where do we plumb this file."

## Conclusion first

**The four stages are not shaped correctly.** Three separate, concrete
defects, all newly measured here (not duplicates of E-032 or E-034):

1. **`validation`'s primary output mechanism is disconnected from its
   consumer.** 78% of validation decisions (36/46) are `conditional_approve`
   — an approval with attached `conditions` that are supposed to bind the
   config `backtest_specification` writes. Those `conditions` are printed to
   console and **never** written into any file `backtest_specification`
   reads. `backtest_specification`'s own handoff contract
   (`validation_to_backtest_specification.yaml`) does not list
   `validation_decision.yaml` as an input at all — required or optional —
   and the stage agent is architecturally closed-book (`allowed_tools=[]`,
   prompt assembled only from the handoff's declared inputs,
   `run_phase1_research.py:699-727`). The gate's main way of saying "yes,
   but" enforces nothing, on 78% of its own decisions.
2. **The narrowing-goes-unrecorded finding generalizes beyond
   `backtest_specification`.** E-034 S1 found `backtest_specification`'s
   variant pick has no routing decision anywhere in code. Measured here:
   `innovation_expansion` also has zero live routing decision in the entire
   59-run corpus — a routing function (`_route_post_innovation_expansion`)
   exists, but it is gated by a flag (`orchestrator.anti_adjacency_retry.
   enabled`) that is `false` for every run in the corpus, so for all 59 runs
   it was a bare passthrough to the static `default_next`. `hypothesis_
   generation` has no routing function at all (trivially — one output, one
   destination). So for three of the four stages, across the entire studied
   history, there has never been a machine-visible narrowing decision.
   `validation` is the only stage that ever actually branches on content.
3. **A schema-required field for recording discarded ideas is honored in
   1/59 runs, and a policy-required field for parking regime-gated ideas is
   written 24 times and read by nothing.** `innovation_notes.schema.json`
   requires `variants_not_pursued` — true `required`, not optional — yet
   only `run_0001` populates it (confirmed independently of E-034's grep;
   `run_044`'s apparent second hit is a false positive, hypothetical prose,
   not a recorded decision). This is a second, independent confirmation of
   E-034's "no schema under `workflow_artifacts/schemas/` is loaded by any
   code" finding, on a field this epic's own Why section flags as the
   headline defect. Separately: `regime_specific_variants` (required by
   POST-A2.3 policy to preserve regime-gated ideas until a trustworthy
   detector exists) is non-empty in 24/43 expansion runs (48 parked ideas
   total) — and no code anywhere reads `regime_specific_variants` back. Not
   destroyed, exactly — worse: durably recorded and then permanently ignored.

**Smallest lever (not a rebuild):** wire `validation_decision.yaml`'s
`conditions` (and `blocking_issues` when status is `refine`-adjacent) into
`backtest_specification`'s handoff as a required input, the same shape
E-034 S2 already used to add `selected_variant_id` — a few lines in the
handoff template plus a read at prompt-assembly time. This is the cheapest
fix that makes the single most common validation outcome (conditional
approval) actually bind anything. It does not touch `STAGE_CONFIGS`,
`determine_post_*`, or any stage boundary.

---

## Corpus caveat, established before anything else

"59 runs" (EPIC.md) is run **directories**, not run **executions of the
four-stage chain**. Of the 59:
- **48** actually executed `hypothesis_generation` and have a
  `hypothesis_card.yaml`.
- **2** (`run_036`, `run_037`) are escalation continuations — they carry
  `run_context.yaml` and start directly from a prior run's already-approved
  hypothesis at `backtest_specification`, skipping stages 1-3 entirely.
- **1** (`run_038`) is a `campaign_review`-only entry (status
  `completed_reframed`), not a hypothesis-generation run.
- **6** (`run_040`, `045`, `046`, `049`, `051`, `052`) are scaffolded but
  never executed — `pipeline_state.yaml` shows `pending_stage:
  hypothesis_generation`, `current_stage: None`.
- **2** (`run_055`, `run_056`) are `quarantined_orphan` (K4 routing-
  registration mechanism, `workflow/run_campaign.py` — out of this epic's
  scope).

48 + 2 + 1 + 6 + 2 = 59. All percentages below use the denominator stated
next to them, not a blanket "59."

---

## TASK 1 — per-stage inputs, outputs, routing, corpus behavior

### 1. `hypothesis_generation`

- **Inputs (handoff `research_brief_to_hypothesis.yaml`):** required —
  `research_brief.yaml`, `config/available_feeds.yaml`,
  `config/indicator_library.yaml`. Optional — `run_context.yaml`,
  `feed_wishlist.yaml`, `campaign_knowledge_base.yaml`.
- **Outputs:** `hypothesis_card.yaml` (one hypothesis; deliverable is
  singular by design).
- **Routing:** none. `STAGE_CONFIGS["hypothesis_generation"]["default_next"]
  = "innovation_expansion"`, static, no `determine_post_*` function exists
  for this stage (`run_phase1_research.py:87-92`).
- **Corpus behavior (MEASURED):** 48/59 run directories produced
  `hypothesis_card.yaml` (see corpus caveat above for the other 11).
  Nothing about the hypothesis is machine-checked before it moves on — the
  first content-based gate anywhere in the chain is `validation`.

### 2. `innovation_expansion`

- **Inputs (handoff `hypothesis_to_innovation_expansion.yaml`):** required
  — `research_brief.yaml`, `hypothesis_card.yaml`,
  `config/available_feeds.yaml`, `config/indicator_library.yaml` (the
  template file has a duplicated `required_inputs:` key at lines 6-12 and
  13-22 — cosmetic YAML-merge artifact, the second occurrence wins under
  PyYAML's normal last-key-wins merge, not a functional bug, but worth
  fixing if anyone touches this file). Optional —
  `refinement_notes.yaml`.
- **Outputs:** `expanded_hypothesis_card.yaml` (base_hypothesis_id,
  expanded_variants, alternative_data_candidates, reverse_hypothesis,
  behavioral_features, regime_specific_variants), `innovation_notes.yaml`.
- **Routing:** `_route_post_innovation_expansion` exists
  (`run_phase1_research.py:1472-1502`) but is flag-gated
  (`orchestrator.anti_adjacency_retry.enabled`, `config/campaign_config.yaml:
  183-184`). **That flag is `false`** and was `false` for the entire studied
  history (it is an E-032 feature, added after the loop stopped running
  2026-07-19). So for every one of the 59 runs, this function returned the
  static `default_next` ("validation") immediately — a real decision point
  exists in the code today but has never fired historically.
- **Corpus behavior (MEASURED):** 43/59 runs produced
  `expanded_hypothesis_card.yaml` with a populated `expanded_variants` list.
  138 total variants, max 8 in one run (`run_007`), min 1, mean 3.21/run —
  reproducing EPIC.md's own numbers exactly. **Correction to a naive read of
  those numbers:** the documented objective ("3-6 variants",
  `docs/USER_GUIDE.md:132`) looks violated in 19/43 runs (below 3) and 3/43
  (above 6). Checking the 18 single-variant runs against their
  `research_brief.yaml`: **all 18 carry an explicit upstream constraint** —
  either `"Single registered hypothesis, no parameter sweep"` or a
  `REPLICATION_DIAGNOSTIC` brief with `"DO NOT CHANGE"` / `"Replication
  only"`. Excluding those (not a stage failure — the stage is correctly
  obeying an upstream instruction), of the **25 unconstrained** expansion
  runs: 21/25 (84%) land in [3,6], 1/25 has 2, 3/25 exceed 6 (up to 8). The
  stage matches its stated objective reasonably well *when free to act on
  it* — this was my first hypothesis for a "divergence" finding and it did
  not survive checking the upstream brief; recorded here so the check isn't
  silently lost.
  - `diversity_axis` (required per `innovation_notes.schema.json`'s
    `IMPROVEMENT 04 DIVERSITY CHECK` instruction) is populated with
    free-form prose sentences, not a controlled category value (sampled
    from `run_0001`'s card: "Baseline moving-average crossover; foundation
    for comparison...", "N/A (single variant, reactivation context)", etc.)
    — it cannot be mechanically checked for actual diversity; it is
    LLM self-report, unverified downstream.
  - `regime_specific_variants` non-empty in 24/43 runs (48 entries total) —
    see Task 3.

### 3. `validation`

- **Inputs (handoff `innovation_expansion_to_validation.yaml`):** required
  — `expanded_hypothesis_card.yaml`. Optional — `human_resolution.yaml`.
  Note: the *entire* variant menu is the primary input, named explicitly
  ("the validated hypothesis and variants to implement" in the downstream
  handoff) — this is the "full menu" EPIC.md's Why section measured.
- **Outputs:** `validation_protocol.yaml`, `validation_decision.yaml`.
- **Routing:** `determine_post_validation_route`
  (`run_phase1_research.py:2192-2266`) — the only real, content-driven
  branch in the four stages. Reads `status` (falling back to
  `family_status` for multi-variant family outputs), routes:
  `approve`/`conditional_approve` → `backtest_specification` (with an
  A8.6 deterministic power-gate check that can redirect to
  `signal_prescreen` first); `refine` → `refinement_planner`, or
  `completed_rejected` if the refinement budget (`max_refinements_after_
  validation`, default 2) is exhausted; `reject` → `completed_rejected`.
- **Corpus behavior (MEASURED, 46/59 runs with a readable status):**
  `conditional_approve` **36** (78%), `refine` **7** (15%), `approve` **2**
  (4%), `reject` **1** (2%). Effectively 38/46 (83%) proceed to
  `backtest_specification`; a clean, unconditional `approve` happens in only
  2/46 (4%). `refinement_planner` was actually invoked in only 4/59 run
  directories (`run_0001`, `run_002`, `run_003`, `run_050`), consistent with
  `pipeline_state.yaml`'s `counters.refinements_used` distribution across
  57/59 runs that have the field: 53 runs at 0, 3 at 1, 1 at 2 — no run ever
  hit the budget-exhaustion reject path from refinement alone in this
  corpus.
- **The disconnect (new finding, Task 2 detail below):** `conditions`
  attached to a `conditional_approve` are printed to the console
  (`print(f"\n⚠️  CONDITIONAL APPROVAL...")`, lines 2228-2230) and are not
  written to any artifact `backtest_specification` reads.
  `validation_to_backtest_specification.yaml`'s `required_inputs` are
  `expanded_hypothesis_card.yaml` and `validation_protocol.yaml` only —
  `validation_decision.yaml` (where `conditions` actually lives) is absent
  from both `required_inputs` and `optional_inputs`. The stage agent cannot
  read outside its assembled prompt: `_build_stage_prompt`
  (`run_phase1_research.py:699-792`) builds the entire prompt from
  `handoff.get("required_inputs", []) + handoff.get("optional_inputs", [])`
  and the agent is invoked with `allowed_tools=[]`
  (`run_claude_worker`, `run_phase1_research.py:795-813`) — there is no
  filesystem access, no way for the LLM to go looking for the file on its
  own. This is the same closed-book architecture E-032 S1 already
  established for `hypothesis_generation`; this dispatch is the first to
  point it specifically at `validation_decision.yaml`'s `conditions` field.

### 4. `backtest_specification`

- **Inputs (handoff `validation_to_backtest_specification.yaml`):** required
  — `expanded_hypothesis_card.yaml`, `validation_protocol.yaml`. Optional —
  `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md`, `docs/WORKFLOW_
  CAPABILITIES.md`.
- **Outputs:** `backtest_spec.yaml`, `decision.yaml`.
- **Routing:** `determine_post_spec_route`
  (`run_phase1_research.py:5842-5859`) — reads only `decision.yaml.status`.
  `spec_ready` → `signal_prescreen`; `component_gap` → `human_pause`;
  anything else → `human_pause`. Confirmed (independently of E-034 S1, same
  conclusion): **no variant-identity field is read here at all** — this
  function cannot distinguish "built variant A" from "built variant B."
  E-034 S1's finding generalizes cleanly: of the three stages downstream of
  the hypothesis, only `validation` branches on content; the other two
  branch on nothing (`hypothesis_generation`, `innovation_expansion`) or on
  a binary buildability flag that is blind to *which* variant was built
  (`backtest_specification`).
- **Corpus behavior (MEASURED, 38/59 runs with a readable `decision.yaml`
  status):** `spec_ready` **37** (97%), `validation_incomplete` **1** (3%,
  `run_005` — an early-pipeline run whose `decision.yaml` records a
  `refine`-status validation and a missing `STRATEGY_CONFIG_REFERENCE.md`;
  this predates most of the routing hardening visible elsewhere in the file
  and is not representative of current behavior). **`component_gap`: 0/38.**
  In no run in this corpus did `backtest_specification` ever decline to
  build a config for lack of an engine component. `candidate_strategy_
  config.json` exists in 41/59 run directories (4 more than have a
  `decision.yaml` — `run_036`, `037`, `041`, `042` — these correlate with
  escalation-continuation runs that materialize a config without a fresh
  LLM decision step; not investigated further, out of this epic's scope).

---

## TASK 2 — objective vs. measured behavior, per stage

| Stage | Stated objective (SKILL.md / USER_GUIDE §2.2) | Measured behavior | Verdict |
|---|---|---|---|
| `hypothesis_generation` | "Create one explicit, testable strategy hypothesis with an honest structural reason it should have edge." | Produces exactly one `hypothesis_card.yaml` per execution (48/48 that ran); no downstream gate ever measures whether the *reason* is honest or the hypothesis is good — the first content check on it happens two stages later, inside `validation`, by which point `innovation_expansion` has already multiplied it. | **Shape question, not a correctness question**: the stage does what it's told, but the pipeline gives it no feedback loop — it never learns which of its own hypotheses led anywhere, because nothing downstream reports back to it (see Task 3: the only inter-run channel is `proposed_brief.yaml` → `research_brief.yaml`, authored by `verdict_interpreter`, not by this stage inspecting its own track record). |
| `innovation_expansion` | "Expand the hypothesis space before strict validation... Expand into 3-6 testable variants" with a real-diversity check. | Matches the count objective 84% of the time when not upstream-constrained (see Task 1). Diversity is self-reported prose, unverified. The stage's entire output — however many variants, however diverse — is passed to `validation` as an undifferentiated menu; nothing in this stage or the next ever ranks or prunes it. Mean variant count is roughly flat across final verdict labels (escalate 3.14, pivot 2.80, refine 3.67, kill n=2 mean 1.00) — more variants does not correlate with a "better" outcome in this corpus. | **Matches its literal instruction, but the instruction itself has no downstream payoff.** Producing a wider menu has no measured effect on what happens to the hypothesis — this is the epic's "narrows and discards ~100 ideas, records nothing" pattern, quantified: variance in menu width buys nothing traceable. |
| `validation` | "Act as a critical gatekeeper... Assume the hypothesis is wrong until enough evidence is specified." | 95% of all approvals (36/38) are *conditional*, not clean — consistent with a genuinely skeptical gate that keeps finding something to flag. But the `conditions` that gate attaches are never delivered to the stage that would need to obey them (Task 1 above). So the stage *behaves* like a careful gatekeeper on paper (constantly attaching caveats) while *functioning* like a rubber stamp in practice (83% proceed to backtest_specification regardless, and the caveats bind nothing). | **Diverges.** This is the epic's pre-registered "name at least one stage whose real behaviour diverges from its stated objective, with run evidence" requirement — `validation`'s stated objective ("assume wrong until proven") is undermined by an unconnected condition-delivery mechanism, not by the stage's own reasoning. |
| `backtest_specification` | "Translate the approved hypothesis into one valid strategy config... OR declare a component_gap if the engine lacks a required piece." | 0/38 `component_gap` in the entire corpus. Every hypothesis that reached this stage was buildable with existing components. | **Consistent with its objective, but the "or declare gap" branch is empirically dead.** INFERRED (not measured directly): this is plausibly because upstream constraints already steer away from anything requiring a new component — `hypothesis_generation`'s own constraint says "must not propose ideas that require replacing the whole existing bot architecture" and `validation`'s checklist says "check whether the idea can be tested through a minimal change to the existing bot architecture." If true, the chain is self-selecting for buildability at the cost of novelty, which is a plausible contributor to 0/59 promotions — but this is a hypothesis about *why*, not a measured fact, and would need its own investigation to confirm. |

**Per the epic's pre-registered success signal:** at least one stage's real
behaviour diverges from its stated objective, with run evidence —
`validation` is that stage, on the specific and measured basis that its
`conditions` mechanism (the vehicle for 78% of its own decisions) has no
downstream reader.

---

## TASK 3 — where information enters and where it dies

Building on E-032 S1 (hypothesis_generation is closed-book: no campaign
history, `allowed_tools=[]`) and E-034 S1/S2 (the chosen variant is
unrecorded pre-E-034; E-034 S2 built — but has not turned on —
`variant_selection.yaml`/`variants_not_pursued.yaml`), re-verified against
current code and extended:

1. **Every stage is closed-book by construction, not just
   `hypothesis_generation`.** `_build_stage_prompt`
   (`run_phase1_research.py:699-727`) assembles the full prompt from
   exactly `required_inputs + optional_inputs` for *every* stage in
   `_SKILL_MAP` (`hypothesis_generation`, `innovation_expansion`,
   `validation`, `refinement_planner`, `backtest_specification`,
   `verdict_interpreter`, `campaign_review`), and `run_claude_worker`
   invokes with `allowed_tools=[]`. A file not named in the handoff
   template is invisible to the stage LLM, full stop — not "unlikely to be
   read," structurally absent from what it sees. This makes the handoff
   templates the complete and exhaustive description of each stage's
   information diet, exactly as this dispatch's brief assumed.

2. **`setup_next_run` (`run_phase1_research.py:2517-2523`) copies exactly
   one file — confirmed, EPIC.md's claim holds precisely as stated for that
   function.** But it is not the only inter-run copy: `_route_refine`
   (`3597-3651`) and `_route_pivot` (`3654-3711`) *separately* copy
   `findings_carryover.yaml` into the next run's `artifacts/` directory,
   right after calling `setup_next_run`/scaffolding
   (`3634-3640`, `3699-3705`). **This file physically crosses the run
   boundary — but it is not in `research_brief_to_hypothesis.yaml`'s
   `required_inputs` or `optional_inputs`.** Given finding 1 above
   (handoff templates are the complete information diet), this means
   `findings_carryover.yaml` sits on disk in the next run's artifacts
   folder but `hypothesis_generation`'s prompt never includes it —  an
   undocumented, unused back door, not a working channel. Comments in the
   code (`3658-3663`, `3696-3697`) describe `hypothesis_generation` as
   "using `findings_carryover.yaml` as input," which is the *intent* but
   not what the handoff template + closed-book architecture actually
   deliver. This is worth a one-line handoff-template fix regardless of
   what S3 decides about the larger shape question.

3. **`validation_decision.yaml`'s `conditions` never reach
   `backtest_specification`** — detailed in Task 1/2 above. This is the
   single highest-volume information loss in the chain (78% of all
   validation outcomes carry a `conditions` payload that is discarded).

4. **`regime_specific_variants` is written and never read.** 48 entries
   across 24/43 expansion runs, required by POST-A2.3 policy specifically
   so regime-gated ideas survive until "a trustworthy detector exists."
   `grep` for `regime_specific_variants` or `detector_wishlist` in
   `run_phase1_research.py` returns zero matches — no code loads either
   name. Distinct from the epic's "~100 discarded, unrecorded" pattern:
   these 48 *are* recorded, durably, per-run — and then permanently
   unreachable by anything except a human grepping 24 run directories by
   hand.

5. **`innovation_notes.schema.json` requires `variants_not_pursued`
   (`"required": [...,"variants_not_pursued",...]`) and no code validates
   any artifact against it** (`run_phase1_research.py:1623-1627`, the
   code's own comment: *"no schema under `workflow_artifacts/schemas/` is
   loaded or validated by any code, anywhere (grep-verified) — a
   schema-only 'required' is decorative"*). Independently re-confirmed
   here: 1/59 runs (`run_0001`) actually populates the field; a second
   apparent hit (`run_044`) is hypothetical prose ("if V1 zero/negative IC,
   V2/V3 not pursued"), not a recorded decision — so EPIC.md's "1 file out
   of 59" claim holds under an independent re-derivation, not just the
   original grep.

**Net picture:** information enters each stage strictly and only through
its handoff template (verified structurally, not just by convention).
Nothing "leaks" across that boundary by accident — the leaks are the
opposite problem: fields that ARE recorded (variant conditions, parked
regime variants, `findings_carryover.yaml`) sit unread because no handoff
template names them as an input to the stage that would need them. This
reframes part of the epic's "destroyed" framing: some information isn't
destroyed, it's recorded into a file nobody's handoff template points at.
That is a cheaper class of bug than "never captured" — E-034 S2 already
built and proved the pattern for the variant-selection case
(`selected_variant_id` → `variant_selection.yaml`, still flag-off); the
same pattern (name the file in the handoff, read it, fail loud if it
doesn't match) would close findings 2 and 3 above without a rewrite.

---

## TASK 4 — the four Done-when items

**1. Canonical description.** `docs/USER_GUIDE.md` §2 (banner at lines
38-53) is confirmed as the maintained, discoverable, correct-against-code
home — it explicitly defers to `STAGE_CONFIGS` + handoff templates +
`determine_post_*` when it disagrees with itself, which is the right
posture. **One correction found and worth fixing there:** §3's opening line
(`docs/USER_GUIDE.md:230`) states *"All artifacts are validated against
JSON schemas before the pipeline advances."* This is false — confirmed by
the code's own comment (`run_phase1_research.py:1623-1627`) and by this
story's independent measurement (finding 5 above: a `required` field
honored in 1/59 runs). **Second, smaller correction:** §2.2's `innovation_
expansion` row states "Expand into 3-6 testable variants" without
qualification; Task 1 shows this holds only for unconstrained runs (84% of
25) — worth a footnote pointing at the `REPLICATION_DIAGNOSTIC` /
single-hypothesis-brief exception so a future reader doesn't mistake the
18 single-variant runs for stage failures.

**2. `stages.yaml` status.** Archival (2026-08-24, EPIC.md Log) is the
right call, confirmed here independently: I characterized all four stages
entirely from `STAGE_CONFIGS`, the handoff templates, and `determine_post_*`
— `stages.yaml` was never consulted and was not needed. Its own archived
banner records 14 declared stages against `STAGE_CONFIGS`'s real 10, and a
`next: [hypothesis]` pointing at a stage name (`hypothesis`) that has never
existed (the real one is `hypothesis_generation`) — drift severe enough
that reviving it would mean reconciling two sources of truth that already
work independently (the `STAGE_CONFIGS` dict for structure, the handoff
YAML files for content) for no measured benefit. **My recommendation for
S2's still-open revive-or-delete call: delete, not revive.** Nothing in
this characterization needed it, and every stage's real contract already
has a single, correct, machine-readable home split across `STAGE_CONFIGS`
(existence/ordering) and `workflow_artifacts/templates/handoffs/*.yaml`
(content) — a third file duplicating both is a new place for exactly the
drift that just got archived.

**3. Per-stage existence justification (Task 2's answer, restated):**
- `hypothesis_generation` — justified; it is the only stage that produces
  the seed content, and nothing else could substitute for it in this
  pipeline shape.
- `innovation_expansion` — justified on the measured count objective (84%
  match when unconstrained); **not yet justified on purpose**, because
  Task 1/2 found no measured relationship between menu width/diversity and
  any downstream outcome in this corpus. Existence is defensible as
  "produces optionality," but nothing currently *uses* that optionality —
  see recommendation below.
- `validation` — justified as the chain's only real content gate, but its
  actual behavior (constant conditional approval whose conditions bind
  nothing) diverges from its stated purpose. This is the stage this
  epic's success signal names.
- `backtest_specification` — justified; translates an approved hypothesis
  into a runnable config, which nothing else in the chain does, and its
  `component_gap` branch — even though empirically unused in this corpus —
  is a real safety valve, not decorative (unlike the unenforced schemas).

**4. Baseline impact of recommended changes.** None of the findings above
recommend a change yet — S1 is characterize-and-STOP per the epic's Method
constraint, and this document makes no code change. For the record, on the
one concrete lever named above (wire `validation_decision.yaml.conditions`
into `backtest_specification`'s handoff): **this would invalidate
baselines.** It changes what `backtest_specification`'s LLM sees on every
run where `validation` returns `conditional_approve` (78% of validation
outcomes) — new input content can change the emitted `config`, which
changes `candidate_strategy_config.json`, which changes every downstream
backtest metric. Any such change must ship off-by-default with a
byte-identical proof at flag-off, exactly like E-034 S2's
`variant_selection_record` pattern (`config/campaign_config.yaml:217-232`),
and any run comparison after turning it on must be declared as a new
baseline, not compared silently against the pre-fix numbers (consistent
with `CLAUDE.fork.md`'s bit-identity discipline, even though that document
governs the trading-bot side rather than strategy-research — the same
discipline applies here by the epic's own Method constraint precedent,
E-012's two-bars fix).

---

## Files touched by this measurement

- `engineering/roadmap/E-033/artifacts/s1_measure_pre_backtest_stages.py` —
  the script that produced every MEASURED number above. Read-only against
  `runs/` and `campaign_record/campaign_state.yaml`.
- This document.
- `engineering/roadmap/E-033/EPIC.md` — S1 checkbox ticked, Log entry added
  (see below). State line and `EPICS.md` untouched per instructions.

## What this explicitly did not do

- Did not open, list, or glob `local_data/holdout_sealed/`.
- Did not run any campaign, backtest, or LLM call.
- Did not move `hypothesis_generation`/`innovation_expansion`/`validation`/
  `backtest_specification` stage boundaries, change `STAGE_CONFIGS`, or
  edit any `determine_post_*` function.
- Did not re-litigate E-032 S1's closed-book finding or E-034 S1/S2's
  narrowing-unrecorded finding — both were re-verified against current code
  (post E-034 S3, commit `7c6d6c3c`) and confirmed still accurate; this
  document cites them rather than re-deriving them, except where it extends
  them to a stage or artifact they did not cover (`innovation_expansion`'s
  routing, `findings_carryover.yaml`'s actual delivery mechanism,
  `regime_specific_variants`, `validation_decision.yaml.conditions`).
