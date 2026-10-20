# Vehicle-format plan (approved 2026-10-20, with the operator's answers below)
# Done 2026-10-20: V1 #503 (D-159), V1d #505 (D-160), V2-1 #506 (D-161), V2-2+V3 #507 (D-162).
# Open: V4 smoke; operator scope points S1-S4 (D-162) and D-157 edge case (3).

Ruled scope (opening prompt 2026-10-19, approved in principle; 2026-10-20 direction adds item V1c):
complete config as the vehicle; `requires: [{kind, name, spec, example}]` for a missing op or
component; decide-next marks such a candidate INFEASIBLE `requires_component:<name>` and appends
the spec to campaign_record/component_requests.yaml; eligible with no rewrite once the piece
exists; the D-110 exact-config 1b route copies the config (refusal lifted for this form only);
1b never builds anything; gate-plus-strategy form and one detector-only exception sentence in
PREFILLED_CLAIM.md ride with it; the ungated twin is the design variant; the complete config is
validated at reading time (refusal with message, the analyst retries).

Operator answers 2026-10-20: plan approved with one change of order: V1e (the SKILL.md text that
advertises the config vehicle and `requires`) moves to the V3 PR, so no analyst answer can use the
form before decide-next and 1b route it; V1a-V1d land first, unused. Q1 three PRs, V1, V2, V3 in
order. Q2 beside the patch list; exactly one of the two per candidate; D-151 stays. Q3 one prefix
per kind: requires_op:<name>, requires_component:<name>. Q4 requires orchestrator.exact_config_1b;
with it off, INFEASIBLE exact_config_1b_off (new reason, this use only); the flag is on in
c4/flag-set. Q5 the lead drafts the one detector-only sentence and sends it for approval, quoting
the line of the opening prompt it implements, before touching PREFILLED_CLAIM.md. Q6 the
detector-component transforms rule is its own PR (D-158) before this work; V1c inherits it.
Start V1 when the item 2 (D-157) and item 5 (D-158) agents have finished.

Facts checked on master 467bdcd7 (line drift from c51026fb noted):
- 1b refusal: run_phase1_research.py:17868 (was :17820) -- `_exact_config_1b` refuses any
  pass-through candidate (`_is_pass_through_candidate`, :17446 = brief carries
  `candidate.source.expected_config_sha256`). Route: :20741; flag `orchestrator.exact_config_1b`
  (:4454, off by default).
- Vehicle today: only a patch list `[{component_id, field, before, after}]`
  (reader_proposals.py:29, `_check_envelope` :374); empty vehicle refused (D-151).
- decide-next: `_candidate` decide_next.py:1548; INFEASIBLE reasons list; `requires_feed_gate`
  :463 is the model for a requires gate; `component_class_status` :255; ops in
  strategies/registry.py `TRANSFORM_OPS_REGISTRY` :236.
- component_requests.yaml exists; appender `append_component_requests`
  (campaign_review_retired.py:120) plus four writers in run_phase1_research.py.
- Reading-time checks available: trading-bot/tools/validate_config.py `validate(config)`
  (V1-V16), forecast_rules.strategies_violations (D-051/D-149), block_manifest.check_manifest.
- PREFILLED_CLAIM.md is 16 lines, one heading; no gate or detector-only text yet.

## Slices (three PRs in order, each from origin/master; Opus core + Opus safety review, Sonnet tests/docs)
- [x] V1 Reading-time format and validation: PR #503 merged 2026-10-20 (D-159); lands unused
- [x] V1d gate form + code-derived ungated twin + V18 (threshold_rules only): PR #505 merged 2026-10-20 (D-160)
  - [x] V1a `vehicle: {kind: config, config: <complete strategy config>}` accepted beside the patch
        list; exactly one of the two per candidate; D-151 stays
  - [x] V1b optional `requires: [{kind: op|component, name, spec, example}]`; each named piece must be
        absent today and used by the config; every absent piece the config names must be listed
  - [x] V1c the config is validated when read: validate(), D-051/D-149, names in `requires` exempt
        from V3/V12 only; any failure -> refusal with the message, the analyst retries (existing loop);
        inherits the detector-component transforms rule (D-158, merged first)
  - [x] V1d gate-plus-strategy form (`combines_as: regime_gate` with a complete config); ungated twin
        named as the design variant
  - [x] V1 tests; Opus safety review; D-row
- [x] V2 split (operator 2026-10-20): V2-1 scaffolding rule + derived manifest + reading-time manifest check +
      no-manifest refusal (behind the off-switch); V2-2 the rest below. V2-2 and V3 merge back to back, no campaign
      run between them. Q1 regime relabel for regime_gate only; Q2 added detector components allowed when a rule or
      veto reads them; Q3 manifest check also at reading; Q4 slim copies {kind: config, config_sha256, requires} with
      a pointer to the full config; Q6 regime_* claims on a gate stay INFEASIBLE (regime_block_needs_composition).
- [x] V2 decide-next (decide_next.py): V2-1 PR #506, V2-2 with V3 PR #507
  - [x] V2a config-vehicle candidate: missing op -> INFEASIBLE `requires_op:<name>`; missing
        component -> INFEASIBLE `requires_component:<name>`
  - [x] V2b append the spec to component_requests.yaml once per name (no duplicate rows)
  - [x] V2c re-checked every pass: eligible with no rewrite once the piece exists
  - [x] V2d brief carries the config as an exact config plus its exact block manifest
  - [x] V2e `orchestrator.exact_config_1b` off -> INFEASIBLE `exact_config_1b_off` (this use only)
  - [x] V2f delete CONFIG_VEHICLE_ROUTED (operator 2026-10-20: delete, not flip)
  - [x] V2g the V1 safety review's items: side_finding_start from vehicle.config (manifest, composition
        source, D-089 branch, digest/sha); fold_confirm whole-config comparison; _merge_key on the
        canonical config; explore_confirm treats a config vehicle like config_change; the brief copy
  - [x] V2h scaffolding rule for config vehicles (operator 2026-10-20): it must tell the V1d gate form
        (rules or vetoes added on the source's kept detector components) apart from a scaffolding
        rewrite (mode, components, structure); the V2 agent states how before wiring
  - [x] V2 tests; Opus safety review (decide-next); D-row
- [x] V3 Step 1b, the 1a sentence and the analyst skill (run_phase1_research.py, PREFILLED_CLAIM.md, SKILL.md)
  - [x] V3a lift the :17868 refusal for the config-vehicle form only; the patch pass-through refusal stays
  - [x] V3b 1b refuses if a required piece is still missing (never builds one)
  - [x] V3c PREFILLED_CLAIM.md, after the "The block is the source run's" bullet, the sentence approved
        2026-10-20: "Exception: when the brief's config changes only the regime detector (a gate on the
        source run's unchanged strategies), the claim is about that gate: in signal_concept describe the
        gate's condition and the source run's block it gates; keep the strategies as the source run's; the
        ungated twin (the same config without the gate) is the design variant, and code derives it, so do
        not write it."
  - [x] V3d (moved from V1e) analyst SKILL.md: the config vehicle and `requires`, one example each
  - [x] V3 tests; Opus safety review (analyst prompt, 1b); D-row
- [ ] V4 smoke after V3 merges, on a run_097 copy, both lenses

# Roadmap re-edit (agreed 2026-09-16..18) — engineering_roadmap.html

Approved by Jérémy 2026-09-18 ("Yes please go"). Source of truth for the agreed target: memory file
project_target_workflow_redesign.md + the review thread.

## Header / legend / scope note
- [x] Bump version note; record revision date and basis (review + operator answers)
- [x] Replace "0 decisions needed" with decision cards (7 answers + window-aggregation, composite trigger, residual-IC, regime-as-composite, component-gap at spec, hybrid scoring, one-symbol default)
- [x] Correct "Objective 1 solid" scope note (mechanical path fired on 1 of 60 runs; holdout gate never reached)
- [x] Add run-budget rule to the header

## Ordered plan
- [x] CUL-267: strengthen (prerequisite of the grid; binding evaluator is verdict_criteria_evaluator.py)
- [x] E-033.3 resolved card: idea criteria from anchored menu per hypothesis; profit bars campaign-level manual file (new ticket)
- [x] E-056: 1a/1b split, criterion menu, instrument-set field, component-gap detectable at spec step, escalation-route correction
- [x] E-057: variant set shape = base + design diff + asset diff
- [x] CUL-298: merged into E-046b (grid aggregation rule, unanimity)
- [x] E-036: add legacy-tagging scope
- [x] E-046a: absorbs E-040 checks; raw per-window table + slices to readers; structured proposals with anchored LLM scores
- [x] E-046b: the grid (field-path + reducer vocabulary, pooled family, sample floors -> inconclusive, unanimity, symbol reducer only for multi-symbol variants)
- [x] Regroup stage (new): memory + block registry + scoreboard + trial ledger, BEFORE decision
- [x] NEW epic: block registry + composition (re-scope E-044); residual-IC criterion; composite = own run, code-enforced trigger; variants = weighting schemes
- [x] NEW epic: retire verdict routing (validated/refuted/inconclusive; next-run selection to Step 10)
- [x] E-031: decide-next (hybrid scoring) + queue; shared-queue item merged in; registry-changed rule
- [x] E-035 + feed lane moved into plan
- [x] NEW tickets: campaign profit-bars file; cost-stress axis; E-054 on by default + flag registered; lift A2.3 no-regime-gating rule
- [x] Feeds: E-033.1 real issue (3 variants, cap 4, E-026 folded, retract "no cap"); skip-re-deriving absorbed; E-054.1 keep; E-029 keep

## Backlog
- [x] E-040 superseded (content -> E-046a + criterion menu; firewall kept)
- [x] E-044 re-scoped into plan (remove from backlog)
- [x] E-049 note: escalation route independently picks symbol/timeframe
- [x] "Announce when profitable" folded into branch 3 stop rule

## Walkthrough (now / what changes / target per step)
- [x] Rewrite steps: 0, 1a, 1b, 2, 2b (validation stage, open decision), 3, 4, 5a, 5b, 6 (grid), 7 (readers), 8 (profit check), 9 (regroup), 10 (decide), 11 (park), 12 (holdout)
- [x] Add "composition runs" and "regime ideas" notes
- [x] Remove Step 5 cost-stress/era claim from "today"

## Gaps list
- [x] Add the 2026-09-16 review corrections and the 2026-09-18 design decisions as the record

## Verify
- [x] Every "Step N" cross-reference matches the new numbering (grep) — re-run on v26
- [x] Every epic ID mentioned exists / status matches Linear snapshot (Linear connector needs re-auth for a live re-check; statuses from the 2026-09-15/16 snapshot)
- [x] HTML still parses (python html.parser) and renders (no unclosed tags)
- [x] Append the review record file (roadmap_review_2026-09-18.md) and update tasks/lessons.md if any correction occurred

## v26 (2026-09-18, operator round 2) — applied
- [x] Source: third verbatim block (operator's words)
- [x] Cards A–N (K config-as-vocabulary, L runbook, M multi-hypothesis briefs, N entry point); F composition via LLM at 1b
- [x] Plan: item 3 = cost-survival criterion; item 16 = E-048; decision card removed; E-046b owns the menu
- [x] Feeds: validation stage DELETED card; pass-through MOVED into E-056
- [x] Backlog: E-048 out; E-010 done noted; 19 entries / 8 categories
- [x] Walkthrough: Step 2b removed; 5a no-LLM; 5b windows only; runbook note added; composition note = trigger + LLM assembly
- [x] Verify tag balance + references (v26)
- [x] Delivery sequence on paper + Linear artifacts list -> strategy-research/engineering/delivery_plan_v26.md (2026-09-19)
- [x] Operator reviewed delivery_plan_v26.md 2026-09-20; 4 guesses surfaced and answered (composition = new E-060 not E-044; E-048 not a gate; verdict_interpreter deleted; any-coin eligibility). Board bumped to v27, both files corrected and re-verified.
- [ ] NEXT: Linear reconciliation (connector re-auth) then first dispatches (0.1, 0.3, 1.1, 1.2, 5a)

## Overnight autonomous session (2026-09-20)
- [x] Master merge: conflicts resolved, CUL-15/CUL-270 bug fix ported and verified, tests green (1459/1467, 8 pre-existing failures proven unrelated)
- [x] Merge committed locally (a20fb7ec on master)
- [ ] **BLOCKED: `git push origin master`** — harness permission classifier denied it as a shared-resource action. Needs Jeremy to push himself or grant permission.
- [x] Linear reconciliation: E-058/E-059/E-060 created; CUL-299/300/301/302/303 created; CUL-298 moved; 11 projects/issues updated with v27 cards
- [x] Confirmed E-039/E-018/E-026/E-041/E-054 already correctly Completed in Linear
- [x] Dispatched 4 background agents: E-056 S1, E-046b S1 (characterize), CUL-267, CUL-300 (build on local branches, not pushed)
- [x] E-056 S1, E-046b S1, CUL-267 build all completed and reviewed (findings solid; CUL-267 verified cherry-pick-compatible with real master)
- [x] Infrastructure finding: all worktree agents based on stale unpushed origin_master -- recorded, workaround pattern noted for future
- [x] CUL-300 build reviewed: solid, self-verified compatible with real master, single clean commit on top of a20fb7ec
- [x] Found and corrected a real error in my own earlier work: CUL-300 ticket wrongly claimed slippage was already in the cost figure — corrected on board + Linear, follow-up CUL-304 filed
- [ ] NEXT: push master (still blocked, needs Jeremy); review/merge CUL-267 + CUL-300 branches; confirm FAIL/INCONCLUSIVE tie-break; decide CUL-304 priority; decide on S2 work for E-056/E-046b
