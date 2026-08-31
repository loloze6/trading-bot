# E-033 — Review, challenge and rationalize the pre-backtest stages

**State:** in-progress (S1 done 2026-08-26; S2 partial, S3 awaits an operator decision)
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
- [~] S3 — Propose stage changes, if S1 justifies any, with an explicit
      baseline-impact statement per change. Operator chooses before any build.
      **Proposals written 2026-08-31** from S1's evidence plus Jérémy's review
      of §1–§2.2 during E-037 — see "S3 proposals" below. **Six decisions are
      open; none has been built.**

## Independent confirmation from E-037 (2026-08-31)

E-037's audit re-measured the narrowing without knowing S1 had already found
it. The numbers agree and extend slightly, one run later:

```
runs producing variants                    44      (S1: 43)
variants GENERATED                        139      (S1: 138)
variants built as a config and tested      36
discarded without ever being tested       103   (74%)
most configs ever built in a single run     1      (S1: exactly 1)
```

Two things this adds to S1's evidence:

1. **The trial-accounting consequence.** Seven variants generated and one
   tested costs **one** trial. The other six were selected against — a real
   multiple comparison — and are never counted, so the deflated-Sharpe
   denominator is too small and every promotion bar sits too low. S3 should
   decide the accounting rule for discarded variants, not only whether to test
   them.
2. **Jérémy's framing, 2026-08-31**, which is the argument for S3 choosing to
   test rather than to restate: *"to reach the objective it would mean we test
   each and every variant. Here I understand we are not doing that."* The stage
   exists to test a mechanism rather than one arbitrary parameterisation, and
   the pipeline tests exactly one arbitrary parameterisation — so a kill still
   cannot separate "the mechanism is wrong" from "this setting was wrong".

**The campaign currently pays the cost of breadth and gets the evidence of a
single test.** Either half alone is defensible; together they are not. That is
the decision S3 has been holding.

Recorded in E-037 as [E037-36](../E-037/FINDINGS.md#e037-36). A separate epic
was drafted for this on 2026-08-31 and **deleted on discovering S1 had already
found it** — the duplicate is itself recorded as
[E037-43](../E-037/FINDINGS.md#e037-43).

---

## S3 proposals (2026-08-31) — six open decisions

Written from S1's characterization and Jérémy's §1–§2.2 review. **Nothing here
is built.** Each carries the baseline-impact statement Done-when 4 requires.

### D1 — Variants: test each survivor, or stop generating them

**Evidence.** 139 generated, 36 tested, 103 discarded untested (74%); never
more than one config per run.

**The choice.** Build a config for each surviving variant and backtest each —
which makes the stage's objective true and fixes the trial count — **or** stop
generating variants and restate the objective for a single-candidate pipeline.

**Why not deciding is the worst option:** the campaign pays the cost of breadth
(tokens to generate up to 8 variants, plus the diversity reasoning) and gets
the evidence of a single test. Either half alone is defensible.

**Baseline impact.** Testing each variant does **not** invalidate past results —
it adds runs. But it **raises the promotion bar** for everything, because the
trial count grows (see D2). Stopping generation invalidates nothing and saves
tokens.

**Depends on** [E-039](../E-039/EPIC.md): if the go/no-go moves after the
backtest, "test each variant" means "backtest each variant", which is the
expensive reading. Sequence them together.

### D2 — How discarded variants count as trials

**Evidence.** Seven variants generated and one tested currently costs **one**
trial. The other six were selected against — a real multiple comparison — and
are never counted, so the deflated-Sharpe denominator is too small and every
promotion bar sits too low.

**The choice.** Count only tested variants; count all generated; or count with
a discount for the selection. **Pre-register the rule before implementing D1** —
choosing it after seeing which strategies pass is the exact failure the DSR
machinery exists to prevent.

**Baseline impact.** Any rule but "count only tested" retroactively raises the
bar on the existing corpus. That is a real re-grading and must be declared.

### D3 — Merge `validation_gate` and `refinement_planner`

**Evidence.** With A8.6 removed ([E-039](../E-039/EPIC.md), Jérémy's call
2026-08-31), `validation_gate`'s remaining work overlaps the planner's.
Jérémy: *"indeed I would merge them."*

**One thing must survive the merge:** pre-registering what would count as
success **before any result exists** — the holdout split (A6.1) and the
`pass_rule` the C7 evaluator scores against. That is scientific integrity, not
feasibility; without it a verdict can be written after seeing the number.

**Open sub-question:** does pre-registration need a stage, or is it a field on
the brief validated at registration? If the latter, the merge is clean; if the
former, one stage survives with a much narrower job.

**Baseline impact.** None on results. Changes stage names and routing, so it
invalidates nothing but touches every handoff template.

### D4 — Where implementation feasibility is answered

**Evidence.** The router reads `implementation_allowed`, **defaulting to
`True`** when absent — and the planner's skill is never told to write it (0
mentions in `SKILL.md`; 2 of 4 real files omit it). Meanwhile stage 6 already
answers the question by emitting `component_gap`.

**The choice.** Instruct the skill and default the router **closed**, or move
the question wholly to stage 6 and delete `implementation_allowed`.

**Why it cannot stay:** it is the only open default in a module whose stated
convention is *"silence is never a green light"*.

**Baseline impact.** None on results — no run has been routed by it in a way
that changed an outcome, because the 2 files that omit it both looped back as
the default intended.

### D5 — `stages.yaml`: revive or delete *(Done-when 2, still open)*

S1's recommendation is **delete**. The file has been moved out of `workflow/`
to this epic's `artifacts/`, so it no longer reads as operational. What remains
is the decision itself.

**Baseline impact.** None. Nothing reads it.

### D6 — Wire `validation_decision.yaml`'s `conditions` into `backtest_specification`

S1's own "smallest lever", still unbuilt. The `conditions` field is attached to
**78% of validation decisions** (36/46 `conditional_approve`), is printed to
console, and never reaches the stage that builds the config — which is
closed-book and can only read its declared handoff inputs.

**Related and found independently by E-037:** the same handoff also omits
`refinement_notes.yaml` ([E037-40](../E-037/FINDINGS.md#e037-40)), so on a
refine loop the planner's conclusions reach the spec stage only if the expanded
card happened to carry them. **Both are the same defect** — a stage that cannot
see what an earlier stage decided — and should be fixed in one change.

**Baseline impact.** **Invalidates baselines on every `conditional_approve`
run — 78% of validation outcomes.** Must ship off-by-default with a
byte-identical proof, and per [E-041](../E-041/EPIC.md) with a written
switch-on criterion.

---

### What S3 does *not* propose

- **Changing what `innovation_expansion` generates.** The generation side is
  sound; only the testing side fails to match it.
- **Removing the prescreen's IC computation.** Useful and cheap; the question
  of whether it may *terminate* a run belongs to [E-039](../E-039/EPIC.md).
- **Any build.** Every item above is a decision for the operator first.


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

- 2026-08-25 — **S1 REVIEW: two corrections, both found by the operator
  challenging the finding rather than by the dispatching session's own
  verification. Recorded prominently because a future agent reading S1's
  artifact without these corrections would be actively misled.**

  **CORRECTION 1 — the `anti_adjacency_retry` "finding" is a timeline
  artifact, not evidence about stage design. RETRACT it.**
  S1 reports that `innovation_expansion` "has zero live routing decision in
  the entire 59-run corpus" because `_route_post_innovation_expansion` is
  gated by `orchestrator.anti_adjacency_retry.enabled`, false for all 59
  runs. That is true and useless. **That flag and that function were both
  written THIS SESSION** (E-032 S2c, 2026-08-23/24); the 59 corpus runs all
  predate the code by weeks. Verified: `_route_post_innovation_expansion` is
  the ONLY function ever called after `innovation_expansion` — there is no
  older routing code that was switched off. So the correct statement is
  "this stage has never had a routing decision, and we added the first one
  a day ago," NOT "a decision point exists but has never fired," which
  invites the reader to infer a historical design failure that did not
  happen. The operator caught this; the dispatching session did not, having
  verified the claim's mechanics without questioning whether the evidence
  could bear the weight put on it. **A count over a corpus that predates the
  code being counted is not evidence about that code.**

  **CORRECTION 2 — the recommended fix targeted the wrong stage, and the
  underlying problem is a stage-shape problem, not a plumbing gap.**
  S1's "smallest lever" (wire `validation_decision.yaml.conditions` into
  `backtest_specification`'s handoff) rests on a premise the operator
  challenged and which does not survive: **most of those conditions are not
  build-time instructions at all.** Real examples pulled from the corpus:
  *"Backtest must achieve Sharpe >= 0.5 AND win_rate >= 0.45 ... Reject if
  Sharpe < -1.0"* (run_012), *"regime_frequency must be >= 0.15. Reject if
  <0.10"* (run_012), *"Screening backtest must report mean_reversion
  regime_frequency. If actual < 0.15, hypothesis moves to reject"*
  (run_011). These can only be evaluated AFTER a backtest runs.
  `backtest_specification` could not act on them if it received them. Only a
  minority (*"Commission configured at 5 bps round-trip"*, run_010) are
  genuine config instructions.

  **The real finding, which is better than the one S1 reported.**
  `validation`'s contracted objective is *"Act as a critical gatekeeper to
  pressure-test the expanded hypothesis for statistical soundness, lookahead
  bias, and data feasibility"* — a pre-flight check on the IDEA. Grading
  results against thresholds is `verdict_interpreter`'s contracted job
  (*"Interpret backtest findings against hypothesis-specific criteria"*).
  And the correct channel between them **already exists and already works**:
  `validation` also writes `validation_protocol.yaml` (`falsifiable_
  statement`, `null_expectation`, `required_evidence`, `failure_modes`,
  `sample_split_design`, `decision_rules`), and `verdict_interpreter`'s
  handoff lists it as a REQUIRED input, reason *"original success criteria
  and failure modes to interpret against."*
  So `validation_decision.yaml`'s free-prose `conditions` field is a SECOND,
  PARALLEL channel duplicating what the structured contract already carries
  — and it is the one nothing reads (verified: no handoff template, and
  neither `prescreen_signal.py`, `run_protocol.py` nor
  `verdict_criteria_evaluator.py`, references `validation_decision.yaml`).
  **The question for S2/S3 is therefore not "where do we plumb this file"
  but "why does `validation` emit result thresholds in loose prose at all,
  when it has a structured field for exactly that which the right consumer
  already reads — and when the pre-registered `pass_rule`, frozen before the
  run, is supposed to outrank anything a stage decides mid-flight?"**
  Operator's framing, and it is the correct one.

  **Standing lesson for future dispatches on this epic:** S1's Task-1
  measurements (input/output/routing per stage, the 36-of-46
  `conditional_approve` count, the 138-variant corpus stats, the correctly-
  killed "3-6 variants" false alarm) are sound and independently reproduced.
  Its INTERPRETATIONS in the verdict and "smallest lever" sections are the
  parts corrected above. Read the artifact's measurements; do not inherit
  its recommendation.
