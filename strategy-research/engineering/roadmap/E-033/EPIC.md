# E-033 — Review, challenge and rationalize the pre-backtest stages

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-24

## Why

The pre-backtest chain — `hypothesis_generation` → `innovation_expansion` →
`validation` → `backtest_specification` — has run 59 times and produced **0
promotions across 38 graded verdicts**. Nobody has ever asked whether those
stages are *shaped* correctly for the goal they serve, as opposed to whether
each one executes correctly. This epic asks that question, against the
evidence of the runs that already happened.

Opened at the operator's direction (2026-08-24) after a design review found
three structural problems that are not bugs in any single stage:

### Measured: the chain narrows three times and records the narrowing zero times

- `hypothesis_generation` produces **1** idea.
- `innovation_expansion` multiplies it into a menu — **138 variants across the
  43 runs that carry an expansion card**, up to 8 in a single run.
- `validation` and `backtest_specification` both receive that **full menu**
  (confirmed from the handoff templates, which are what the orchestrator
  actually reads: `validation_to_backtest_specification.yaml` names
  `expanded_hypothesis_card.yaml`, reason "the validated hypothesis **and
  variants** to implement").
- Exactly **1** configuration is ever backtested.

**No artifact anywhere records which variant was chosen, or why.** Verified on
`run_019`, which produced three genuinely distinct variants (thresholds
17.5 / 20.0 / 22.5): neither `validation_decision.yaml` nor `backtest_spec.yaml`
names one. The narrowing happens inside an LLM's reasoning and leaves no trace.

### Measured: ~100 generated ideas were discarded unrecorded, then the loop declared itself out of ideas

138 variants generated, one tested per run. A grep of the entire 59-run corpus
for any record of unpursued variants returns **1 file out of 59**. On
2026-07-19 the campaign logged *"Queue exhausted — no ready or in_progress
entries remain"* and stopped. The loop did not run out of ideas; it discarded
them and then reported itself empty.

### Measured: one prose paragraph is the whole inter-run learning channel

`setup_next_run` (`workflow/run_phase1_research.py:2055`) copies exactly one
file into the next run: `proposed_brief.yaml` → `research_brief.yaml`. Nothing
else carries over. The next run's `hypothesis_generation` is closed-book
(`allowed_tools=[]`, no campaign history — E-032 S1). So 59 runs of
accumulated knowledge reach the next idea through a single
`change_from_previous` prose field.

## Scope

**In scope:** the four pre-backtest stages, their objectives, their skills,
what each receives and produces, where decisions are made and recorded, and
whether the sequence serves "find a profitable, tradeable strategy."

**Out of scope:** the backtest engine, protocol execution, verdict machinery,
and anything post-`protocol_execution`. Those have their own epics.

## Method constraint (why this is not a rewrite epic yet)

**The loop has not run since 2026-07-19.** Redesigning stages from artifacts
rather than from observed behaviour is speculative, and this project has
already made the analogous mistake twelve times at the strategy level. The
prior lesson also applies: E-012's two-bars fix put 58 of 59 runs on an
obsolete engine convention, so any change that invalidates baselines again
must be declared loudly, not slipped in.

Therefore S1 is characterize-and-STOP. **No stage boundary moves until the
characterization is read and a direction is chosen by the operator.**

## Done when

1. A single, maintained, discoverable document describes the real pre-backtest
   pipeline — what each stage is *for*, what it receives, what it decides, and
   what it records. Correct against the code, not against `stages.yaml`.
2. `stages.yaml`'s status is resolved: made authoritative (the orchestrator
   actually reads it) or explicitly demoted/removed. Not left as a file that
   reads authoritative and is not.
3. Each pre-backtest stage has a stated objective that can be checked against
   its actual output on past runs, and any stage that cannot justify its
   existence against the 59-run record is named as such.
4. Any recommended change is evaluated for whether it invalidates existing
   baselines, and says so explicitly.

## Stories

- [x] S1 — **Characterize and STOP.** For each of the four stages, from the
      code and the run corpus, not from `stages.yaml`: real inputs (handoff
      templates), real outputs, real routing (`determine_post_*`), and what it
      actually decided across the 59 runs. Where does information enter, and
      where is it destroyed? No code changes, no stage moves.
      **Done 2026-08-26.** Full writeup:
      `E-033/artifacts/s1_stage_characterization.md`; measurement script
      `E-033/artifacts/s1_measure_pre_backtest_stages.py`. Headline finding
      (the pre-registered success signal): `validation`'s `conditions` field
      — attached to 78% of its own decisions (36/46 `conditional_approve`) —
      is printed to console and never reaches `backtest_specification`;
      `validation_decision.yaml` isn't in that stage's handoff inputs at all,
      and the stage agent is closed-book (`allowed_tools=[]`, prompt built
      only from declared `required_inputs`/`optional_inputs`,
      `run_phase1_research.py:699-727`). Two more: (a) E-034 S1's
      "`backtest_specification`'s narrowing has no routing decision" finding
      generalizes to `innovation_expansion` too — its routing function exists
      but is flag-gated (`orchestrator.anti_adjacency_retry.enabled`), and
      that flag was `false` for all 59 corpus runs, so it was a bare
      passthrough every time; only `validation` has ever branched on content.
      (b) `regime_specific_variants` (48 entries across 24/43 expansion runs)
      and `findings_carryover.yaml` (copied across run boundaries by
      `_route_refine`/`_route_pivot`, not by `setup_next_run`) both cross a
      stage/run boundary but are named in no handoff template that would let
      a closed-book stage agent read them back — recorded, then permanently
      unreachable. Smallest lever named (not built): wire `validation_
      decision.yaml`'s `conditions` into `backtest_specification`'s handoff,
      same shape as E-034 S2's `selected_variant_id` — would invalidate
      baselines on every `conditional_approve` run (78% of validation
      outcomes) and must ship off-by-default with a byte-identical proof.
      `docs/USER_GUIDE.md` confirmed as the correct canonical home, with two
      corrections flagged for whoever next edits it: §3's "all artifacts are
      schema-validated" claim is false (no schema is loaded by any code —
      independently reconfirmed via `innovation_notes.schema.json`'s
      required-but-1/59-honored `variants_not_pursued` field), and §2.2's
      "3-6 variants" objective should note the `REPLICATION_DIAGNOSTIC`/
      single-hypothesis-brief exception (18/43 single-variant runs are all
      upstream-constrained, not stage failures — checked and ruled out before
      writing this up as a finding). `stages.yaml` archival confirmed as the
      right call, independently re-derived (characterization never needed
      it); recommendation for S2's still-open revive-or-delete decision is
      **delete**.
- [~] S2 — Consolidate pipeline documentation into one maintained home and
      resolve `stages.yaml` (Done-when 1 and 2).
      **Partially done 2026-08-24, ahead of S1, at the operator's direction:**
      `docs/USER_GUIDE.md` §2 declared the single canonical home (banner + a
      false claim corrected: it had said the orchestrator reads `stages.yaml`);
      `DOC_INDEX.md` routes there; and **`stages.yaml` was MOVED OUT of
      `workflow/` to this epic's own `artifacts/`** — the operator's call:
      a file that is wrong and unread reads as operational wherever it sits,
      so a banner was not enough. **Remaining for S2:** the revive-or-delete
      decision itself, which still depends on S1.
- [ ] S3 — Propose stage changes, if S1 justifies any, with an explicit
      baseline-impact statement per change. Operator chooses before any build.

## Relationship to other epics

- **E-032** (proactive idea generation) — S1's finding that the generating
  stages are closed-book is this epic's starting evidence, not a duplicate:
  E-032 changes what a stage *sees*, this epic asks whether the stage should
  exist in that position at all.
- **E-034** (selection record + variant pool) — the narrowing-record defect
  measured above is being fixed there as a targeted change. This epic may
  later conclude the *shape* should change too; E-034 does not pre-empt it.
- **E-009** — owns the `STAGE_CONFIGS`/`skill_map` merge, which is the
  mechanical half of making `stages.yaml` authoritative. S2 must not duplicate
  it; coordinate or hand the decision there.
- **E-018** (near-miss scoreboard) — its ranked table over tested ideas is an
  input to S1's "what did these stages actually decide" question.

## Success signal (pre-registered)

S1 names at least one stage whose actual behaviour across the 59-run record
diverges from its stated objective, with the run evidence — or states
positively that all four are correctly shaped, which is equally a result. A
characterization that produces neither has not been done.

## Log

- 2026-08-24 — `new`. Opened at the operator's direction: *"review, challenge,
  rationalize, enhance the pre-backtest steps based on the past run."* The
  three measurements above are the opening evidence, taken during the design
  review that prompted it.

- 2026-08-24 — **`stages.yaml` archived out of `workflow/`** to
  `E-033/artifacts/stages_yaml_ARCHIVED_not_authoritative.yaml`. Operator
  ruling: *"i do not agree of keeping a file unread, wrong, and standing here
  while we have a real epic to make it work."* Repointed every live reference
  (8 README citations, USER_GUIDE, DOC_INDEX, 5 source comments). Suite after
  the move: strategy-research **1003 passed**, unchanged — confirming by
  execution that nothing depended on it, which is the same fact that made it
  safe to move and dangerous to leave.

  **One correction to this session's own earlier claim, found while doing it.**
  "Nothing loads `stages.yaml`" was true of the orchestrator but NOT globally:
  `E-032/artifacts/s1_measure_idea_generation.py` did load it, and that is the
  script behind E-032 S1's headline "the generator is closed-book" finding.
  So that measurement was taken from the decorative file rather than from the
  handoff templates that actually feed the stages. **Re-checked against
  `workflow_artifacts/templates/handoffs/research_brief_to_hypothesis.yaml`:
  the two AGREE** — same three `required_inputs`, no campaign history — so
  E-032 S1's conclusion stands. It was right, read from the wrong source. The
  script is repointed at the archived copy (verified re-runnable, reproduces
  its original numbers) with that caveat recorded inline.

- 2026-08-26 — **S1 done.** Characterize-and-STOP, per the Method
  constraint: no code changed, no stage boundary moved. Full findings in
  `E-033/artifacts/s1_stage_characterization.md`; every MEASURED number
  reproducible via `E-033/artifacts/s1_measure_pre_backtest_stages.py`.
  Success signal satisfied: `validation` is named as the stage whose real
  behaviour diverges from its stated objective — its `conditions` field
  (attached to 78%, 36/46, of its own decisions) is printed to console and
  structurally cannot reach `backtest_specification`, whose handoff doesn't
  list `validation_decision.yaml` and whose stage agent is closed-book
  (`allowed_tools=[]`). Two findings extend prior epics rather than
  duplicating them: E-034 S1's "no routing decision on the chosen variant"
  finding generalizes to `innovation_expansion` (its routing function has
  never fired live — the gating flag was `false` for all 59 corpus runs);
  and `regime_specific_variants` (48 entries, 24/43 runs) plus
  `findings_carryover.yaml` both cross a stage/run boundary on disk but are
  named in no handoff template, so a closed-book stage agent can never read
  them back — recorded, not destroyed, but permanently unreachable. One
  self-check that changed a draft finding before it shipped: an apparent
  "innovation_expansion violates its own 3-6 variant objective 44% of the
  time" reading did not survive checking the 18 single-variant runs against
  their `research_brief.yaml` — all 18 carry an explicit upstream
  single-hypothesis or replication-diagnostic constraint; excluding those,
  the stage matches its objective 84% of the time (21/25). Two corrections
  flagged for `docs/USER_GUIDE.md` (still the correct canonical home): its
  §3 claim that artifacts are schema-validated before the pipeline advances
  is false (re-confirmed independently via `innovation_notes.schema.json`'s
  required `variants_not_pursued` field, honored in 1/59 runs), and §2.2's
  "3-6 variants" line should note the constrained-brief exception.
  `stages.yaml` archival re-confirmed as correct; recommendation for S2's
  open revive-or-delete call is delete. Smallest lever named for S3 (not
  built): wire `validation_decision.yaml.conditions` into
  `backtest_specification`'s handoff, E-034 S2's `selected_variant_id`
  shape — would invalidate baselines on 78% of validation outcomes, must
  ship off-by-default with a byte-identical proof.
