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

# Step back after delivery plan v26 (approved 2026-09-27: Opus + Sonnet split; Phase A running)
# A1 = 4 Sonnet agents (slices 0-3, 4-5, 6, 7-8+§3); A2 = 2 Opus (cards A-G, H-N); A3 = 1 Opus (all flags on).
# Outputs: session scratchpad review/*.md; orchestrator verifies top findings, checks §4 Linear table itself.

Goal: check the whole delivery against the plan and the roadmap vision, prove it works end to end,
measure cost, then write a post-completion report and delivery plan v2.

## Phase 0 — running
- [ ] CUL-336 closed-book stages (build dispatched; review → fix → merge)
- [x] Settings deny rule for Read on holdout_sealed (user settings, 2026-09-27)

## Phase A — Delivery review (read-only, parallel, no backtests)
- [ ] A1 Plan vs code: every item of delivery_plan_v26 §2 slices, §3 cross-cutting, §4 Linear table → delivered? where? gaps?
- [ ] A2 Vision vs code: each roadmap v27 decision card (A–N) → faithful? any retired machinery reachable with all flags on?
- [ ] A3 "All flags on" map: flags, dependencies, what one run does end to end, stale docs, dead code
- [ ] A4 Operator one-pagers: start a campaign on the new pipeline; read results; unlock the holdout
- [x] A1/A2/A3 done (7 agents); Linear §4 checked by orchestrator
- [x] Consolidate → engineering/review_2026-09-27/DELIVERY_REVIEW.md (PR #232) — operator reads; 5 decisions pending
- [ ] A4 operator one-pagers (after plan v2 fixes, so they describe the real flow)

## → Superseded by strategy-research/engineering/delivery_plan_v26_continuation.md (approved 2026-09-27, PR #234)
- [x] Decision log merged (PR #233, D-001..D-040)
- [x] Linear: E-061 (P-CUL-69, in progress), E-062 (P-CUL-70); CUL-336 linked to E-061
- [x] C6.1 Linear: 8 plan-v26 epics → In Progress with status comments; 27 slice tickets linked to their epics (CUL-305/306 chores left unlinked)
- [x] C2 S1 done (branch docs/e061-c2-s1); SMALL guesses accepted; **PARKED for operator: G13** (asset variant on partial window coverage?); G14 → C1.3 must keep diagnostics with an empty rule set. Heartbeat cron hourly :17.
- [ ] C2 S2a..S2e: wait for C1.1 on master (all extend tests/test_e061_end_to_end_wiring.py)
- [x] C3 S1 merged (PR #236); SMALL guesses accepted; **PARKED for operator: G10** (slow strategies → sparse path → no DSR → branch 3 can never pass; fix = trial accounting change)
- [ ] E-062 S2a pure functions (Opus, running)
- [x] C0.1 CUL-336 merged (PR #235, master 9900dee3); Linear Done
- [x] C0.2 venv: venv/Scripts/python.exe works (pandas 2.3.3, numpy 2.5.1); trading-bot fast 774 passed; e054/k3 64 passed (verified by orchestrator)
- [x] C1.1 end-to-end wiring test merged (PR #238, 11 strict xfails pinned)
- [x] PR #239: CUL-336 SDK guard skips test files (master was red after #238 — my miss: re-run combined suite after merging two branches)
- [ ] C1.2+C1.3: review 10 findings (incl. default-path DSR statistic change) → fixing
- [ ] C1.4+C1.5: review 10 findings → fixing
- [ ] C1.6+C1.7: in code review
- [x] E-062 S2a merged (PR #240); G1/G7 amendments recorded; checked evaluable on run_054/057/059
- [ ] C1.6+C1.7: fixes done (46252f56; none of 13 protocols fit → template generates 2018-02..2025-12 monthly windows) → focused re-review running
- [ ] **For operator (morning):** generated protocols need a non-generic `promotion` block (G7) that only feeds run_protocol's legacy verdict (ignored by grid/profit bars) → recommend doing C5.6 (retire promotion blocks) before C4 instead of making the operator invent legacy thresholds
- [x] C1.2+C1.3 merged (PR #241, 23abd130) after 3 review rounds; two-run e2e test passes. Agent slip: one unpushed local WIP with --no-verify (reset, redone with hooks) — briefs now say "hooks on every commit, WIP included"
- [x] C1 complete: #242 (C1.4+5), #243 (C1.6+7); D-041..D-044 (#244); CUL-339 merged (#245) → leftovers CUL-340 (URGENT before first holdout spend, with CUL-335)
- [ ] C2 S2a review fixes (fresh Opus agent, running): graded-only variants + failed_variants; re-run bypass; validation needs base+design+asset in one run; D-021 pinned
- [x] C5.6 merged (PR #246); leftovers CUL-341
- [x] C2 S2a merged (PR #248, pushed as c2s2a-fix per operator choice b); leftovers CUL-342 (do with C2 S2b)
- [x] C6.2 stale docs merged (PR #247)
- [x] C5.1 merged (PR #249); leftovers CUL-343
- [x] Layer-1 Kraken per-coin start dates merged (PR #250)
- [x] Old worktrees: 32 removed (18 GB); 35 local branches still to delete (branch -D refused by classifier; awaits operator permission rule); phase/1-3 kept
- [x] C2 S2b merged (PR #251; D-045 logged; leftovers CUL-344). Push block root-caused (operator fixed autoMode env); 35 old branches deleted.
- [x] C2 S2d merged (PR #252; B2 passes, no xfail left)
- [x] C2 S2c merged (PR #253; leftovers CUL-345)
- [x] E-062 S2b-1 merged 2026-09-29 (PR #254, a5d3abf5; body declares CUL-346 item 4); wt_s2b1 + agent-a8f60f421f74aebe8 worktrees removed (no junctions inside), local branches deleted. Leftovers CUL-346.
- [ ] Next: E-062 S2b-2 (D-041, Opus) → S2b-3 (D-042 + lift M1) → S2b-4 (e2e+docs, Sonnet); C2 S2e in parallel
  - [x] S2b-2 Phase A merged (PR #255, a4f7b869): S2B2_FINDINGS.md + D-046 (published BLP DSR; pure-luck spread 1/sqrt(T-1) below 10 same-basis trials — operator rejected the NOT_EVALUABLE floor; recompute tool built, write on operator nod)
  - [x] S2b-2a merged (PR #257, 7b10118f); full suite on preview = same known/environmental set, 3879 passed
  - [x] S2b-2b merged (PR #258, 25df7d5d); full suite same known set, 3921 passed. Builder worktree agent-a63a300c245092273 still locked by live session pid 10804 — remove at session end.
  - [x] S2b-3 Phase A merged (PR #259, c86d91ea): S2B3_FINDINGS.md + D-047 (floor 60, calendar-rate minimum PARKED until C4 trade counts; cost floor scaled same; drawdown x sqrt(f); <2 eras INCONCLUSIVE every variant; wider retest = new trial)
  - [x] S2b-3a merged (PR #261, 9c4b05ab)
  - [x] S2b-3b merged (PR #265, ac456589); bars sha LF → 29aa2642
  - [x] S2b-3c merged (PR #266, 4cccfe4f); N on real ledger 12 → 12; leftovers CUL-350
  - [x] S2b-4 merged (PR #267, 8962424e): e2e v2 chain (28/28 incl. slow), docs, E-062/SIGNING_CHECKLIST.md; D-034..D-039 status fixed. **E-062 S2b build COMPLETE** (S2b-2c moved after C4)
- [x] Bars file SIGNED 2026-09-29 (PR #269, 5816dced; recorded by Claude at the operator's instruction). sha LF 43de3868… / this Windows CRLF checkout a752a2eb… (CUL-348). Next: C4 go (flag set: score_provenance ON per D-049)
- [x] Open points decided (D-049, PR #268): C4 with score_provenance ON; C5.4 accept + measure in C4 by patch vs new_block; C5.5 (count residual-IC backtest, score reframe brief), CUL-349, C5.2, C5.3 all AFTER C4. Remaining operator actions: sign bars file; C4 go. Before holdout spend: CUL-340, CUL-335, CUL-348
- [ ] Remaining no-decision work: C5.8 (stop feeding legacy label to readers; small); CUL-343 (stale prescreen_signal test + 2 tidies); CUL-347/350 tidies
  - [ ] Before first holdout spend: CUL-340 + CUL-335 + **CUL-348** (bars-file sha depends on line endings; verified CRLF f96ce688 vs LF 4a75ed66)
  - [ ] S2b-2b brief MUST carry: (a) overlay read through ONE path constant; record overlay presence + sha in dsr_basis (a missing file silently drops legacy values from K = flattering once K ≥ 10); (b) assert the candidate's own row is in K and equals its ledger value (dedup can collapse it onto an earlier block-less row = flattering); (c) the C11 decide_next re-fire rule on K is probably moot under D-046 (DSR always computable) — confirm
  - [ ] S2b-2c (recompute tool + operator --write) MOVED TO AFTER C4 (operator 'Ok', 2026-09-29): no grade changes before K ≥ 10 (D-046 pure-luck spread ignores the sample below the floor). Order now: S2b-2b merge → S2b-3 → S2b-4 → operator signs → C4 → S2b-2c + write. Brief MUST carry: overlay writer restricts entries to backtest rows (prescreen rows would enter K)
  - [x] C5.7a merged (PR #260, 1dd7d9f4). Leftovers (fold into C5.7b): stale '$comment' in variant_selection/variants_not_pursued + strategy-research/CLAUDE.md ~L22; ~10 test helpers write warning stub grids. C5.7b Phase A merged (PR #262) + D-048 (stamp model id from the call; mismatch = observed vs requested; closed rubric set; citations record-only, A+/B decided after C4). C5.7b-1 merged (PR #263); C5.7b-2 merged (PR #264, bba7747b; my comment fix d94578a6 for the S2e pin). Note for C4 flag choice: score_provenance ON adds a stop path (wrong rubric_version twice → run fails via reader retry path)
  - [x] C2 S2e merged (PR #256, 0e7949cc); leftovers CUL-347. Full suite in a worktree: 6 e054/k3 failures are ENVIRONMENTAL (no untracked venv there → 'No runnable trading-bot interpreter'; pass in main checkout) + known CUL-343 + zstandard
- [x] C4 prerequisite done 2026-09-29 (operator OK for both): venv now has claude-agent-sdk 0.2.82 + google-genai 2.16.0 (strategy-research/config/requirements-mac.txt pins); side effect websockets 17.1 → 16.1.1 (unpinned); pip check clean; run_phase1_research imports in venv; trading-bot fast suite in venv 774 passed (same as C0.2).
- [ ] S2b-1 merge order: AFTER S2c. D-039 values make 4 e2e tests fail (harness profiles: 40 trades/window, edge 0.9). Fix round: merge master + raise harness profiles (≥100 trades/window, edge > 2.2), keep each test's scenario. Stricter values on legacy v1 per-window path accepted (conservative; v1 retired after C4).
- [ ] E-062 S2b split (retro rule, small slices, sequential): S2b-1 v2 flag+rows+values (Opus, running) → S2b-2 D-041 one scoring (Opus) → S2b-3 D-042 normalised bars + lift M1 (Opus) → S2b-4 e2e + docs (Sonnet) → operator signs bars file
- [ ] After S2d merge: C2 S2c (variant shape) ∥ E-062 slices; then C2 S2e (distance rubric, touches reader SKILLs)
- [ ] E-063 Kraken-batch universe epic (parked until after C4): create EPIC.md + Linear project
- [ ] C2 S2d: built 10d41854, local only (push refused by classifier) → after S2b merge: small fix (status label "graded") + merge
- [ ] D-045 (drop 2-era rule) to add to DECISION_LOG + mark D-042 text; E-063 Kraken-batch universe epic (parked until after C4) to create
- [x] (superseded, merged #249) C5.1: WIP f56a682e pushed (feat/c5-1-scale-free-refusal), tests pending venv rebuild — operator rebuilding venv by hand (memory-pressure kill); venv emptied 17:44 by my worktree clean-up following a junction (lesson + memory recorded)
- Next: E-062 S2b (profit bars v2 wiring + D-041 + D-042) and C2 S2b (one coin per variant + D-042 partial coverage + CUL-342 items 1-2) — need venv for full suite
- Next after these: E-062 S2b (profit bars v2 wiring + D-041 unified scoring + D-042 normalised bars), C2 S2b (one coin per variant + D-042 partial coverage), C2 S2c/S2d/S2e
- **Budget rules from 2026-09-28 (operator-approved):** Opus only for core logic + safety review; Sonnet for tests/docs/mechanical; max 2 review rounds; fresh small fix agents; max 2 concurrent agents. C1.4+C1.5 (after round 4) and C1.6+C1.7 (after round 2): no further reviews — my verification + suite, then merge; leftovers → tickets. No new dispatch until ≤2 agents run.
- [ ] C1.4+C1.5: third-round fixes running (no protocol regeneration after spend)
- [ ] CUL-339 (URGENT, holdout safety): run_protocol --holdout uses protocol's holdout block not policy range → build after C1.2+C1.3 merges (both touch run_protocol.py); must land before any holdout spend
- [ ] E-062 S2b (wiring + flag + values) after C1 merged
- [ ] E-062 S2a second-round review fixes (running); record G1 deviation (missing junction/tail → NOT_EVALUABLE) in E-062 S1 decision section at merge

## Phase B — Wiring test, no API cost
- [ ] End-to-end test with all new flags on, LLM stages stubbed, small cached data, sandbox campaign dir (never the real campaign record / trial ledger)

## Phase C — Real runs (operator go needed: API keys, money, trials counted)
- [ ] Prerequisites: CUL-336 merged; Phase B green; operator reviews profitability_bars.yaml values
- [ ] 2 consecutive real runs (= E-059 S4 two-run proof); measure cost/time per stage, turns, failures

## Phase D — Close-out
- [ ] Post-completion report: what plan v26 delivered, with real-run evidence
- [ ] Delivery plan v2: corrective actions + improvements from A–C (operator approves)

---

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


## Session-end cleanup (2026-09-29)
- [x] Removed the 3 worktrees locked by pid 10804 (previous session's claude.exe, still alive; all clean, no junctions, commits on master); deleted feat/e062-s2b2b-dsr-wiring, s2b3b-fix

## C4 prep + no-decision items (2026-09-29 evening)
- [x] C4 prep: PR #271 (docs/c4-prep, 888c43f5) -- C4_PREP.md (14-flag set incl. profit_bars_v2 + score_provenance; register flips with config; recommended c4/flag-set branch never merged; first-brief draft; measurement plan), RUNBOOK 1e current, D-048 status fixed. NOT MERGED (merge blocked by classifier)
- [ ] C4 flip test fallout: INCOMPLETE (host memory stop). Re-run flipped tree once, halves, one process, machine idle, -v to file; re-run failures on master; explain each
- [ ] Operator: pick the first-brief idea (rec. A vol-managed trend), approve c4/flag-set recording, then the go
- [x] C5.8 Phase A: PR #270 (docs/c5-8-findings, 9f81d8b1); trial-accounting claim verified (rows at rpr:1952 before guarded C7 block). NOT MERGED (classifier). One operator question: also withhold kill_/refine_ cost-check route codes (rec. yes, numerics kept). S2 waits for nod
- [ ] CUL-343: built on fix/cul-343-c51-followups (12ee4027, pushed; 1373 targeted passed). NO PR yet; mutation check + full suite (halves) + e2e slow still to do (my mutation check was denied as 'Merge Without Review')

## 2026-09-30 (after operator answers: PRs #270/#271 merged; picks agreed = D-050)
- [x] D-050 recorded (PR #272, open for operator merge)
- [x] c4/flag-set branch 2742191c (14 flags + register + briefs/C4_vol_managed_trend.md, parsed clean, NOT registered) -- never merge
- [x] Flip measurement half 1 complete (28 failed + 1 error, all explained): 21 = e2e harness defect (stub rubric v1 + flags inherited from real config), 4 = flags-off asserts (C7), 3 = e054 env, 1 = CUL-343. Half 2 stopped at 53% (host memory; 3 k3 env so far)
- [x] Harness fix: PR #273 (test/e2e-c4-flag-set ccf87dee): explicit flag sets, C4_FLAGS scenario, guard test; flipped-config e2e 142/0; my pre-merge full suite (quarters, foreground) = known set only
- [x] C5.8 S2: PR #274 (7ac564d3, on #273; merge #273 first); ledger gate-on == gate-off proven; full suite known set only (4330)
- [ ] After #273 merge: re-run the flip measurement (both halves) on c4/flag-set rebased; record in C4_PREP §2.4
- [x] CUL-343: PR #275 (12ee4027); full suite known set only (4325, collection error gone). Mutation check NOT done (classifier) -- operator may run
- [ ] Operator go for the real C4 runs (register brief -> dry run -> single-step launch)
- [x] C4 go given 2026-09-30. Main checkout on c4/flag-set (ef0b93e9); preflight clean (B11/K3 clean, dry run PASSED no warnings); brief registered (queue backup in session scratchpad c4_backup/)
- [x] run_061: 1a ok (1 turn, $0.19) -> 1b parked component_gap (bidirectional SMA(50) trend; only SmaTrendLongOnly exists) ($0.10). decide_next R2 minted __more_1
- [x] run_062 (__more_1): 1a answered "brief exhausted" (1 turn, $0.19) but labelled the block `# artifacts/brief_status.yaml`; parser regex accepts bare filenames only -> nothing saved -> HALT unhandled_exception. BRIEF_HYPOTHESES.md:66 says "artifacts/brief_status.yaml" (prompt invites the prefix). No trials added (15 rows before/after)
- [ ] Operator: (1) OK to fix the label parser + addendum wording (bug fix) then resume run_062; (2) build a long/short SMA trend component or not; (3) go for more runs (C4 has not reached a backtest yet)
- [x] PR #277 merged (parser accepts artifacts/ prefix; OBSERVATIONS_QUEUE.md O-1..O-3). c4/flag-set 6888e9e0 = master 33d607cd + flip + brief
- [x] run_062 retried (--resume --once): 1a wrote brief_status.yaml (exhausted) -> completed_brief_exhausted ($0.1565, 1 turn); DECIDE stop (no eligible candidate). First attempt's audit ($0.1855) saved in scratchpad c4_backup/ (resume overwrote attempt_0). Retry's reason differs from attempt 1: "first hypothesis covers the core mechanism; alternatives repeat exhausted technicals" (not the 34 bps cost argument) -> add to O-3 when investigating
- C4 spend so far: run_061 $0.288 + run_062 $0.1855 + $0.1565 = ~$0.63; trial rows 15 -> 15; no backtest reached yet
- [ ] Operator: investigate O-1..O-3 first (they decide whether run_061's idea can run) vs build long/short SMA component and --unpark C4_vol_managed_trend vs new brief
- [x] Operator chose option 3 (new brief). briefs/C4_donchian_daily_trend.md on c4/flag-set 11104ce1 (Donchian breakout, BTC/ETH 1d, untried family, existing long/short component). Registered, dry run PASSED
- [x] run_063: 1a/1b/2 ok (3 calls, 1 turn each, $0.441), backtest_spec tool ok, PARKED at data_availability_gate: 1/4 variants left (need >=2): base VALIDATE; sentiment_gate invented class FearGreedComponent (real: FearGreedContrarianComponent); SOL coverage 57% < 60%; XRP 2022-05 6.5% bars missing > 5%. decide_next queued C4_donchian_daily_trend__more_1 (not run). Trial rows 15.
- Incident: `tail -1` on ETHUSDT_1d.csv showed one sealed-window row (disclosed; lesson recorded)
- C4 spend so far ~ $1.07; no backtest reached
- [x] O-4..O-7 added to OBSERVATIONS_QUEUE.md (PR #278, open for operator merge). Operator on O-5: >=2 variants is right; the eviction of SOL/XRP instead of re-windowing is the surprise. O-7 (operator): a threshold breakout idea does not respect the linear-forecast design; note 1b built the continuous DonchianBreakoutComponent while the card describes an on/off ~10%-active rule
- [ ] NEXT SESSION: investigate O-1..O-7 together (read-only, no runs), one finding + recommended fix each; then decide how C4 reaches its first backtest
- State: main checkout ON c4/flag-set (11104ce1; never merge) with runtime campaign files modified (queue, campaign_log/summary, loop_health, component_requests, schedulability, protocols/run_06x, runs/run_061..063) -- do not commit or revert. Queue: C4_vol_managed_trend paused:waiting_for_component (brief exhausted); C4_donchian_daily_trend paused (run_063 parked at data gate); C4_donchian_daily_trend__more_1 READY (not run). Trial rows 15. C4 spend ~ $1.07.
- [x] O-1..O-7 investigated read-only (2 agents, top claims re-verified): findings + C4 recommendation in PR #279 (stacked on #278; merge #278 first). $0, no runs, trial rows 15
- [ ] Operator: decisions on O-1 (signed-forecast rule + SmaTrendComponent), O-2 (ask 1a for up to 3 cards), O-3 (drop the hard 1a cost veto; snapshot stage inputs), O-5 (XRP refine -> drop windows; coverage table for step 2), O-7 (forecast rule for 1a, fidelity rule for 1b, latched breakout component) -> D-051+
- [x] O-1 corrected after operator challenge (PR #279 b4962333): signed SMA is composable from existing classes; 1b's gap was false; lesson + memory recorded
- [ ] Fixes toward C4's first backtest (one PR each): O-1 guide 'composing a signal' section + 1b SKILL rule (+ 'claimed by 1b' label on parks, if agreed); O-4 guide input for step 2; then --unpark C4_vol_managed_trend (resumes at 1b). Donchian path after: guide rows, composability check before any new component; settle __more_1
- [ ] Note: local_data/kraken_XRPUSD_1d.csv shows 572 lines rewritten (run_063 data gate) -- uncommitted runtime change, content not displayed; operator to decide whether to keep it

## PLAN (APPROVED 2026-09-30: Phase A go; stop after A4) — design guide review + split (includes the O-1 composition fix)
Operator decisions: (1) do not keep trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md -- delete in this PR and repoint legacy readers (fallback: named deletion item in the D-043 clean-up epic if Phase A shows a hard tie); (2) do the guide rewrite AS the O-1 fix. Open: fold O-4 into the same PR (recommended).
Workflow: A1+A2 Sonnet agent + A3 Sonnet agent in parallel (read-only, NEW); A4 by orchestrator -> STOP; B one Sonnet writer (NEW, worktree); one Sonnet full review + max one safety-only round; fresh small fix agent; orchestrator runs targeted tests + one research suite in quarters.
Goal: one documentation set that lets a closed-book LLM (config writing, making the versions, composition runs, readers) know (a) every existing component and exactly what it outputs, (b) how a strategy config is designed, (c) the full range of combinations, (d) every engine feature reachable through the config -- and what the config cannot express.
Phase A -- characterize, read-only, then STOP for the nod:
- [ ] A1 Consumer map: every stage/skill/handoff/closed-book input/test/code comment that loads or cites STRATEGY_DESIGN_GUIDE.md, WORKFLOW_CAPABILITIES.md, trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md (and which sections: §4, §7c, §7e ...)
- [ ] A2 Coverage check: every config key/option the engine + validator accept (regime_engine, strategy_engine incl. block combiner / weight_schedule / history_transforms / lookback, registry ops, aux_feeds, validate_config V1-V12) vs what the guide documents -> missing / stale / wrong list
- [ ] A3 Catalogue accuracy: each of the 24 rows checked against its class's update() -- output formula, range, sign, continuous vs sparse, warmup, data needs (the Donchian row is known wrong)
- [ ] A4 Proposed structure + section map (old section -> new home or removed), for the nod
Phase B -- implement (one docs PR, after the nod):
- [ ] B1 Write the new files per the agreed structure; keep all valid content, drop engineering history/proposals to an engineering note
- [ ] B2 New "composing a signal" section (negative weights, BuyAndHold offset, one-sided -> two-sided, long-only via clip, signed-SMA example) + "what the config cannot express" (exits, stops, time holds, position state)
- [ ] B3 Every composition example backed by a committed test (validator + synthetic-price engine check), so examples cannot rot
- [ ] B4 Update consumers (handoffs, _CLOSED_BOOK_STAGE_INPUTS, SKILLs, sync test, § references); config-writing SKILL rule "component_gap only after compositions are ruled out"
- [ ] B5 Targeted tests + one research-suite run in quarters, foreground, one process
- Operator 2026-09-30 (all agreed): D-051 HARD rule -- a component feeding the forecast must be graded; an on/off CONDITION is a regime (detector rule; graded strategy in that regime, null/flat elsewhere). Regime-gated designs follow card F / roadmap "Regime ideas" (gated vs ungated composition versions); A2.3 no-regime-gating stays for ordinary runs. Borderline Whale/VolumeExpansionHedge = on/off as forecast sources. On/off classes: not modified/deleted now; graded siblings built on demand; on/off blocked by a 5a check; deleted in D-043 clean-up. Design variants: one parameter/transform of the tested component, never add/remove/replace a component. Readers' catalogue access decided after C4's first reader output.
- [ ] B (docs PR, Sonnet writer): guide + COMPONENT_CATALOG.md + history note; fold WORKFLOW_CAPABILITIES.md; delete STRATEGY_CONFIG_REFERENCE.md + its TB sync test; repoint legacy readers; D-051 + variant rule text; O-4 wiring (flag-on context function)
- [ ] Follow-up code PR: 5a checks (variant keeps base component classes; on/off class in `strategies` refused), flag-on
- [x] DECISION_LOG D-051..D-054 committed on docs/design-guide-rewrite (385c74f2, worktree scratchpad/wt_guide, from origin/master d1a8ddeb = #278 merged)
- [x] Linear: E-064 epic (P-CUL-72) "Regimes designed by the strategy config" + stories CUL-351 (regime names from config), CUL-352 (rule transforms/consecutive_bars); CUL-353 silent-failure code findings (gated SMA warmup dependence, silent 0.0 on missing feed, mode/op typos, V12 subclass, unknown keys)
- [ ] B1 writer (Sonnet, NEW) dispatched: docs rewrite per scratchpad/brief_B1.md -> then B2 (SKILL rule texts D-051/D-053/component_gap + O-4 wiring + test), then one Sonnet review, then orchestrator tests + PR
- [ ] D-052 slice (A2.3 deletion): inventory first; separate PR
- [ ] Code PR: 5a checks (variant keeps base component classes; on/off class in strategies refused)
- Operator 2026-09-30: D-051 amendment (option b) -- `threshold_filter` and `volume_filter` NOT allowed in `strategies` (dead zone = on/off at the edge; volume condition -> regime). Soft dead-zone op = CUL-354. Production/legacy configs are not changed retroactively; the rule binds new configs (text now, Step 5a check in the code PR).
- [ ] After B2 returns (do not edit the worktree while it runs): amend D-051 row + guide ("The design principle", transform table notes, worked example caveat: the production mean_reversion config predates D-051) + catalogue if needed; then review
- Operator 2026-09-30 "Ok agreed": ONE-SHOT graded siblings (new classes, originals untouched) for SmaTrendLongOnly (signed % distance from SMA), FundingRateMeanReversion (-rate x k every bar), FearGreedContrarian ((50-index) x k), MacdHistogramCrossover (scaled histogram). Gated SMA / Whale / VolumeExpansionHedge wait for E-064 (condition part = regime). Own code PR, two-phase: formulas first -> STOP for nod -> build + tests + catalogue rows.
- [x] PR #280 opened (docs/design-guide-rewrite, 6 commits): guide + catalogue + history, deletions, SKILL rules, O-4 wiring, dead-zone amendment, review fixes. Research suite: 7 failures, all pre-existing on origin/master; trading-bot fast 765 passed. Awaiting operator merge; then remove worktree scratchpad/wt_guide
- [x] PRs #279 and #280 merged by the operator (master 7db42b10); worktree wt_guide removed

## PLAN (2026-09-30, next session; AWAITING NOD) — D-051/D-053 5a checks, graded siblings, D-052 inventory
Base for every branch: origin/master 7db42b10, each in its own scratchpad worktree (main checkout stays on c4/flag-set, untouched; venv junction removed before `git worktree remove`). One branch/PR each; operator merges. No runs, no LLM calls, $0, trial rows stay 15.

### (1) fix/step5a-d051-d053-checks — code PR (Opus = me; one Opus safety review)
Where: `run_phase1_research.py` tool-only `backtest_specification` branch (master :2507-2708), per-variant loop, after the patch applies and the manifest paths resolve (:2623-2648), before the validate_config subprocess (:2672). That branch runs only under `orchestrator.config_direct_authoring` -> flag-on by construction; flags-off path unreachable = byte-identical. No new flag (decision a).
- [ ] New pure helper `strategy-research/tools/forecast_rules.py`: `on_off_classes(catalog_path)` parses COMPONENT_CATALOG.md rows between CATALOG:START/END (Kind column; today 7: MacdHistogramCrossover, SmaTrendLongOnly, GatedSmaTrendLongOnly, VolumeExpansionHedge, FundingRateMeanReversion, FearGreedContrarian, WhaleLargeTradeImbalance); raises on missing file / zero rows / a row without a kind. `strategies_violations(config, on_off)` -> D-051 on/off class in `strategies.regimes.*.components[*].class`, and op `threshold_filter`/`volume_filter` in that component's `transforms` or `history_transforms`. `class_signature(config)` = regime_detector.components classes (ordered) + per-regime ordered class list in `strategies` (null regime kept as null); `class_mismatch(base, variant)` -> D-053.
- [ ] 5a: each refusal = variant `not_tested` with reason `D-051: ...` / `D-053: ...` and the detail in `report` (like V12), appended to component_requests like every other 5a refusal. Existing routing then does the rest, unchanged: `_variant_config_errors` (:14105) counts it -> a variant = one Step 2 retry then `variant_config_error` pause; `base` = immediate pause, no retry (1b's fault, review fix M2 :14199).
- [ ] Exempt composition runs (`_comp_run`, code-written from past blocks that may predate D-051 -- "not retroactive").
- [ ] Decision b (operator): E-059 decide_next patch candidates reuse a PAST config verbatim as base (may hold threshold_filter / an on/off class). Recommended: APPLY the rule (refuse -> pause) -- "not retroactive" = old configs/results are not edited, not that banned designs get re-spent. Alternative: exempt pass-through bases.
- [ ] Decision c (operator): an on/off class in the BASE -> `variant_config_error` pause (recommended; 1b re-authors with a graded class, the catalogue lists them) vs park `waiting_for_component` asking for a graded sibling.
- [ ] Not in scope (say so in the PR): `regime measure` / `constant` kinds as forecast sources; regime_detector on/off use (allowed: conditions belong there).
- [ ] Tests (new file): parser = the 7 classes + fail-loud cases; each refusal on base and on a variant (transforms and history_transforms); class swap / add / remove / regime -> null refused, param/transform change and asset variant accepted; composition run exempt; route: variant -> Step 2 retry, base -> pause no retry. Mutation: drop each check -> its test fails.
- [ ] Declared flag-on fixture changes: `test_e061_end_to_end_wiring.py` BASE_CONFIG uses `threshold_filter` (:262, and BAD_OP points at transforms/2) -> graded op; `test_e059_s2a_decide_next.py` fixture (FundingRateMeanReversion + threshold_filter, :55/:70) -> changed only if it reaches 5a (decision b decides the expected outcome).
- [ ] RUNBOOK §3 variant_config_error: one line naming the D-051/D-053 reasons.
- [ ] Verify: targeted tests; research suite in foreground parts < 10 min, one process; trading-bot fast suite; known pre-existing failures only (e054 x3, k3 x3, recorder x1).

### (2) feat/graded-siblings — Phase A only, then STOP
- [ ] Read the four classes (`trading-bot/strategies/strategy_components.py`) and write, per sibling: class name, params (defaults), exact formula on bar t, range & sign, units, warmup, data/NaN handling, why it cannot look ahead. Starting points (agreed 2026-09-30): SmaTrendLongOnly -> signed % distance close vs SMA (keep the one-bar lag or not: to settle); FundingRateMeanReversion -> -rate x k every bar (k sized so a typical 8h rate lands on the forecast scale); FearGreedContrarian -> (50 - index) x k every bar; MacdHistogramCrossover -> histogram / close x 100 x sf (price-free; raw histogram is in price units). Originals untouched. STOP for the nod; Phase B (build + tests + 4 catalogue rows, 24 -> 28) is a later step.

### (3) D-052 inventory (A2.3 deletion) — read-only, then STOP
- [ ] One Sonnet agent (NEW, read-only): every reference to A2.3 / "no regime-gated" / `er_detector_unusable_btc_eth_1h` in SKILLs, run_campaign.py, run_phase1_research.py, near_miss_scoreboard.py, KB entries, tests, docs -> file:line, kind (rule text / code enforcement / test assertion / KB veto), proposed action (delete / withdraw-mark / replace with "ungated version as design variant"). STOP with the table.

### Order and agents
(1) built by me in its worktree while the (3) Sonnet agent runs in the background (2 agents max: that agent + the later Opus review). (2) Phase A by me after (1) is up as a PR. Then: decide the fresh C4 run with the operator (no real run without the go). Before any holdout spend: CUL-340, CUL-335, CUL-348.
- NOD 2026-09-30 with answers: (b) refuse, checked on the config AFTER the patch is applied (a patch removing the banned piece passes); record every refusal. (c) base refusal: NOT pause/park -- send back once to 1b with the error via the existing 1b manifest-error retry path; pause only if the retry still fails. NO exemption for composition runs (registry empty; one uniform rule). (2) must be MERGED before any real run. (2) formulas: SMA version has NO one-bar lag (decide at the bar's close); funding in natural units (bps), no fitted scale constant (transforms normalise); MACD = histogram / close as a percent.
- [x] (1) PR #281 (fix/step5a-d051-d053-checks, 3c434402 + f63ad875; worktree scratchpad/wt_5a, venv junction -- rmdir the junction before removing). Opus safety review: ship after fixes; F1 (stale last_check via update_state merge, reproduced), F4 (RUNBOOK), F6 (unreadable record) fixed. Tests: new file 47 passed, 11/11 mutations killed, e2e D-053 retry test; full research suite 17 parts: only the pre-existing recorder shard failure (e054/k3 passed this time). Follow-ups (not built): decide_next feasibility gate should refuse pre-D-051 lineages before 1a/1b spend; refused composition base at 5a = unclassified pause; regime-measure/constant kinds not refused.
- [x] (3) D-052 inventory (Sonnet, read-only): scratchpad/d052_inventory.md -- 67 rows + 9 tests. STOPPED for operator decisions (see session summary).
- (2) Phase A formulas (below) -- STOPPED for the nod.

### (2) Phase A -- graded siblings, formulas (originals untouched; no scaling_factor: natural units, the config's transforms scale)
| new class | output on bar t (data through t's close) | range & sign | units | warmup | data & NaN |
|---|---|---|---|---|---|
| SmaTrendGradedComponent (lookback_L 100) | (close[t] - SMA_L[t]) / SMA_L[t] x 100, SMA over the last L closes incl. t; no lag | unbounded, signed, + above the SMA | percent | L | closes; NaN in the window -> NaN (not 0.0) |
| FundingRateGradedComponent (no params) | -funding_rate[t] x 10000, every bar | unbounded, signed, contrarian (- when longs pay) | bps per 8h print | 1 | funding_rate (latest print at or before t, backward as-of join); NaN/missing column -> NaN |
| FearGreedGradedComponent (no params) | 50 - fear_greed[t], every bar | -50..+50, contrarian (+ in fear) | index points | 1 | fear_greed (prior day's value, feed's +1 day shift); NaN/missing -> NaN |
| MacdHistogramGradedComponent (fast 12, slow 26, signal 9) | (MACD - signal) / close[t] x 100; MACD = EMA_fast - EMA_slow, signal = EMA_signal(MACD), adjust=False; stateless | unbounded, signed, + when MACD above its signal | percent of price | slow + signal (35) | closes; EWMs skip interior NaN; NaN latest close -> NaN |
- Operator 2026-09-30 night: (2) formulas OK; "delete near-duplicates if too close". Verdict: DROP SmaTrendGraded (= MacroTrendFilterComponent with period=100, scaling_factor=1, EMA instead of SMA; period is a parameter) -> catalogue points SMA-trend ideas to MacroTrendFilter. KEEP MacdHistogramGraded (histogram != EMADiff's MACD line; imitating it needs two EMADiff copies + negative weight + odd scales, not exact). Build 3: FundingRateGraded, FearGreedGraded, MacdHistogramGraded.
- Operator: D-052 "all okay". My picks where I had given none: Q1 detector_wishlist.yaml stays as a list of ideas but can no longer pause the campaign (feed_wishlist pause unchanged); Q2 delete the regime-auditor "no new detector" rule; Q3 lift the per-regime IC suspension; Q4 keep regime_specific_variants in the schema (empty list OK), instructions stop routing ideas there; Q5 KB entry withdrawn (exhausted: false + dated note). Operator may object before the D-052 PR.
- [ ] (2) Phase B: branch feat/graded-siblings from master, 3 classes + tests + catalogue rows (24 -> 27) + sync test
- [ ] (3) D-052 slice PR after (2)
- [x] (2) PR #282 (feat/graded-siblings, eb7e367a + 6de5525b; worktree scratchpad/wt_graded): MovingAverageDistanceComponent (sma|ema) + MacdHistogramComponent; naming rule + "names that mislead" table in COMPONENT_CATALOG.md. Funding / Fear & Greed graded classes held back after the Opus review (do not ship: 1-bar history never forecasts; aux-feed carry-forward broken since 751d403e; F&G +1 day shift gone; NaN forecast unguarded). 8/8 mutations killed; TB fast 796; research suite = known recorder failure only.
- [x] Linear: CUL-355 (aux-feed carry-forward regression, High), CUL-356 (F&G shift / possible lookahead, High), CUL-357 (graded funding + F&G, blocked by 355/356/274). CUL-274 (NaN guard, Urgent) already exists, Backlog.
- [ ] NEXT (operator go given for the order): CUL-355 fix on its own branch -- design below, STOP for the nod on the two choices
- [ ] then CUL-356, CUL-274, CUL-357; D-052 slice (picks recorded above)
- Operator (CUL-355): carried-forward value reused FOREVER (no age limit), as before 2026-09-03. Point 1 (which feeds) re-explained; awaiting confirmation
- Operator: aligned on CUL-355 design -- per-feed declaration in feed_registry.py (agg + fill); funding & F&G agg last, fill carry forever; whale unchanged (empty). Building on fix/cul-355-aux-feed-carry-forward.
- [x] PR #281 CI red (RUNBOOK row contained a literal `flags={`, test_holdout_research_only_gate took it for the reset snippet) -> fixed f922b80c after a FULL suite; CI green both OSes. Lesson recorded.
- [x] PR #282 CI green.
- [x] CUL-355: PR #283 (fix/cul-355-aux-feed-carry-forward, 38913da0 + 5e009e5f; worktree scratchpad/wt_feed, venv junction + 4 copied caches in trading-bot/local_data). Opus red-team: ship after fixes -> done. Declared: gap bars (funding 2022-06/2023-05, F&G 2018-04/2024-10) now carry the old value instead of NaN (needs operator OK); aux columns in bars.csv/portfolio_states.csv change for every run. Slow tests: 2 pre-existing failures (bar_equity exposure 3.7936 vs 3.785; baseline hash 9f3b09c1 vs 5ccbec42) reproduced on pure master -> need own ticket.
- [ ] Operator: OK on the gap behaviour (CUL-355 declared change); merge #281, #282, #283
- [ ] Next: CUL-356 (F&G shift), CUL-274 (NaN guard), CUL-357 (graded funding/F&G), D-052 slice; ticket for the 2 pre-existing slow-test failures
- Operator 2026-10-01: OK on the CUL-355 gap behaviour; #281 #282 #283 merged. Continue: CUL-356 next.
- [x] Worktrees wt_5a / wt_graded / wt_feed removed (junctions first); local branches deleted. 14 older agent worktrees under .claude/worktrees left untouched.
- [x] CUL-356 built: branch fix/cul-356-fear-greed-delay 02d6b269 (worktree scratchpad/wt_fg). FEED_DELAY_SECONDS (fear_greed 86400). Engine NEVER applied the A8.4 shift (only the deleted prescreen loader). API checks: 2026-09-30 23:19Z and 2026-10-01 00:05Z -> value stamped day D published at D 00:00 today; history unverified -> conservative 1-day kept. Fixture warmup_prefetch_reference rebaselined (window to 2024-01-16, 2 trades, -2.581979 / -6.285). Suites green (TB 846; research known recorder only); slow: 2 pre-existing failures only. Opus red-team running.
- Operator 2026-10-01: CUL-356 F1 -> option A (value first used by the bar that STARTS at/after the known time; 1d bars one day more cautious). Documented in feed_registry.py; pinned by test_every_bar_of_day_d_carries_day_d_minus_1[1d].
- [x] CUL-356: PR #284 (fix/cul-356-fear-greed-delay: 02d6b269 + 3905845b + 154403a7; worktree scratchpad/wt_fg with venv junction + 4 copied caches). Option A (bar that STARTS at/after the known time). Suites green (TB 852; research known recorder only; slow: 2 pre-existing). Awaiting operator merge.
- [ ] NEXT: CUL-274 (NaN forecast guard) -- characterize the choke point first (ticket says so), then plan; then CUL-357, D-052 slice; ticket for the 2 pre-existing slow-test failures
- [x] CUL-274: PR #285 (fix/cul-274-nan-forecast-hold 5578ed6f + 8f0b556e; worktree scratchpad/wt_nan). Policy HOLD (operator), risk controls + gap tiers still apply; metrics.json nan_forecast block only when > 0; run_protocol forwards it. Opus review: ship after fixes -> done. CUL-358 (E-029) = NaN -> flat with context label; review notes added (exception path goes flat today).
- [x] Gap groundwork (read-only): run_protocol NEVER passes gap_detection/gap_policy -> research never uses the gap rule. Price-gap counts (pre-seal): Binance BTC/ETH 1h 27 gaps / 122 bars missing (max 33); Binance 4h/1d none; Kraken 1h many 1-3-bar gaps (likely no-trade hours), LTC 146 gaps of 24-167 bars + 5 of 168+, BTC 27 of 24+.
- [ ] NEXT: gap rule on by default -- propose thresholds per timeframe (operator picks), wire run_protocol, declared change + re-pin; then CUL-357, D-052, ticket for 2 pre-existing slow failures
- [x] Gap rule on by default: branch feat/gap-rule-on-by-default ecd0e1af (worktree scratchpad/wt_gap). Option B (ignore<=3, large=required_bars, flatten). run_backtest + simulate; run_protocol inherits (source guard). Pinned slow tests unchanged (2 pre-existing failures only); per-bar pd.Timedelta -> datetime.timedelta (warning flood). Suites green. Opus review running.
- [!] Gap default flip review: DO NOT SHIP as-is. Blockers confirmed by reading: large tier never cleared (stuck flat forever); buffer '<' vs engine '<=' at ignore threshold. Majors: NaN rows, ignore gap cancels active tier, gap settings not in run identity. Ticket CUL-359. Branch feat/gap-rule-on-by-default (ecd0e1af) NOT pushed -- awaiting operator decision on order (fix CUL-359 first, reindex in default or not).
- Operator 2026-10-01: (a) fix CUL-359 first, then flip the gap default (branch feat/gap-rule-on-by-default ecd0e1af kept, rebase after the fix); (b) indicator fill (RollingBuffer reindex) OFF by default -- the flip must be changed to NOT pass ignore_max_bars to AdvancedStrategy (engine tiers only).
- [x] E-029 now holds: CUL-360 (label every trade/forced change with its context -- core), CUL-361 (indicator fill on by default, blocked by 359+360), CUL-362 (revisit hold during re-warm after missing data), CUL-358 (revisit hold when data is not available -- NaN/component error; blocked by 360).
- [ ] NEXT: CUL-359 fix branch (large tier clears after re-warm; ignore gap must not cancel an active tier; gap settings in run identity; buffer '<=' threshold; tests on gapped data), then rebase + finish the flip (fill off), then CUL-357, D-052
- [x] PRs #284/#285 merged (master 3898cb9e); worktrees wt_fg/wt_nan removed. CUL-359 built: fix/cul-359-gap-rule-defects dcec566b (worktree scratchpad/wt_359): large tier clears after re-warm, ignore gap keeps active tier, severity wins, buffer '<=', run identity fold, events tier/bars_missing, early refusal, datetime.timedelta. 6/6 mutations; suites green; slow set green. Opus verification running. Next: PR, then rebuild the default flip on top (fill OFF).
- [x] PR #286 (CUL-359 gap defects, fix/cul-359-gap-rule-defects dcec566b + 6602778b; worktree wt_359). PR #287 (gap rule on by default, fill decoupled/off; feat/gap-rule-default-on 006e82c1; worktree wt_flip; STACKED on #286 -- retarget to master after #286 merges). Old unpushed branch feat/gap-rule-on-by-default (wt_gap) superseded -> remove (junction first).
- Found: test_min_allocation_change_override_bit_identical failed on master only because its pin missed the E-010 S3 rebaseline -> fixed in #287. Remaining pre-existing slow failure: bar_equity exposure 3.7936 vs 3.785 (ticket still to file).
- [ ] Operator: agreed to reduce test frequency + duration? (proposal: targeted while building, one full run per PR, slow only for engine/data, CI as net; scope by change; --durations measurement; xdist only if operator lifts the one-process rule) -> record in lessons once confirmed
- [ ] Next: CUL-357 (graded funding + F&G), D-052 slice, fresh C4 run decision
- [!] #287 merged into fix/cul-359 branch, not master -> PR #288 (same commit 006e82c1) to master. Lesson recorded.
- [x] #288 merged (gap rule on by default on master 526c85b1); worktrees wt_359/wt_flip removed.
- [x] CUL-357: PR #289 (feat/cul-357-graded-funding-fear-greed dfd32400; worktree scratchpad/wt_357). FundingRateComponent (-rate x 1e4) + FearGreedComponent (50 - index), warmup 2, NaN on gaps; tests on real DataManager merge + real engine; 4/4 mutations; TB 902, research green (known recorder). Lighter test approach applied (no slow run: additive).
- [ ] NEXT: D-052 slice (A2.3 deletion) per tasks/d052_inventory.md + picks; then fresh C4 run decision; ticket for the bar_equity exposure pre-existing failure; record testing approach in lessons once operator confirms
- [ ] D-052 slice (branch feat/d052-delete-a23, worktree wt_d052): Sonnet writer = SKILL/handoff/doc text (inventory rows 1-41 minus code); me = run_campaign wishlist (detector families no longer pause; feed_wishlist unchanged), KB entry withdrawn (exhausted false + dated note, derived views recomputed), rpr print text, tests T1/T2/T3, DECISION_LOG status. Ungated design variant = regime rules emptied + default_regime set to the regime holding the strategy (passes D-053 class check).
- [x] D-052: PR #290 (feat/d052-delete-a23 244b7e51; worktree wt_d052). Text (Sonnet writer, 18 files) + run_campaign gating feed-only + KB withdrawn + SKILL re-pin + waiver removed. Research suite green (known recorder).
- [x] Observations status given to operator: done O-1 (except park label), O-4, O-7 (except general 1b clause mapping); open O-2, O-3 (1a cost veto -- maybe blocks), O-5, O-6. Recommended: next session = C4; before it, O-3 + O-6. AWAITING operator answer (agree? remove 1a hard veto?).
- Operator 2026-10-01: agree next session = C4; O-3 (remove 1a hard cost veto) + O-6 (honest park reason) first. O-3 needs an investigation: no element may contradict 'costs only judged by the backtest' (Sonnet inventory running).
- [x] O-6: PR #291 (fix/o6-park-reason-lists-every-variant 5e134862; worktree wt_o6).
- [x] O-3 inventory: tasks/o3_inventory.md (A1 1a hard veto; A2/A3 validation-stage veto + schema; A4-A6/A8 docs/comments/dead schema; C1 'distance_to_profitable' = edge vs cost ranking in BRIEF_HYPOTHESES + decide_next sort; A7 whale prereg block; C4 KB rsi cost-drag entry). Awaiting operator: (1) ranking score -> registry distance (rec.), (2) whale prereg left (rec.), (3) KB rsi entry kept (rec.).
- SESSION END 2026-10-01: open PRs #290 (D-052), #291 (O-6). Worktrees to remove after merge: scratchpad wt_d052, wt_o6 (old session scratchpad; remove junctions first).

## 2026-10-01 (session 2) -- O-3 (costs judged ONLY by the backtest)
- [x] #290 / #291 merged (master a939cd03); worktrees wt_d052 / wt_o6 removed (junctions first), branches deleted.
- Operator decisions: (1) distance_to_profitable -> D-017 (registry distance); 1a gets block_registry.yaml read-only when present. (2) whale prereg gate: leave. (3) KB rsi_momentum_trending_cost_drag: WITHDRAW + fix all now -- the exhausted_mechanisms view admits any entry whose exhausted_basis contains the word "analytic" (run_phase1_research.py ~10682); all 5 forbidden entries have ec 1-2 and are there only via that word. Review the other 4 entries + fix the filter in the O-3 PR (design STOP for operator nod).
- run_018 facts: cost_drag 272.865 = MEDIAN of 22 per-window cost/|gross| ratios; 7/22 windows gross < 0; pooled gross +1,080 / cost 3,163 / net -2,084 / 1,345 trades, one config (pre-A22, baseline_v1 monthly windows, all 2024).
- [ ] Branch fix/o3-costs-judged-by-backtest from master (worktree scratchpad/wt_o3)
- [ ] A1 hypothesis-design SKILL hard veto deleted + sha re-pin; BRIEF_HYPOTHESES §3 "never exhausted / no card dropped on a cost estimate"; rubric distance_to_profitable per D-017
- [ ] decision (1) code: 1a input block_registry.yaml (when present) + test
- [ ] A2/A3 quant-validation SKILL + validation_protocol schema + reason string (~2859)
- [ ] A4 cost_model.yaml comments, A5 CAMPAIGN_PROGRAM, A6 USER_GUIDE, A8 retire prescreen_result schema + tools/README entry
- [ ] KB: rsi_momentum withdrawn (dated note, measured numbers); filter fix + other 4 entries (after operator nod)
- [ ] Opus safety review; full suite once on final head; PR to master
- [!] O-3 PAUSED (operator correction 2026-10-01): uncommitted in wt_o3 -- hypothesis-design SKILL (hard veto -> information only + Forbidden bullet) + sha re-pin; BRIEF_HYPOTHESES rubric per D-017 + §3 "never exhausted on a cost estimate"; 1a gets block_registry.yaml when present (+2 tests); quant-validation SKILL + validation_protocol schema + reason string; cost_model.yaml comments. NOT done: CAMPAIGN_PROGRAM (A5), USER_GUIDE (A6), retire prescreen_result schema + README (A8), tests run, review, PR. No KB edits in O-3.

## D-055 -- how the KB turns findings into bans (own branch + PR, separate from O-3). PLAN -- STOP for operator nod
Branch fix/d055-kb-veto-rule from master (worktree scratchpad/wt_d055).
Facts (measured 2026-10-01, master a939cd03):
- View rule run_phase1_research.py:10681-10683 (`is_analytic = "analytic" in basis`; `ec >= 3 or is_analytic`). All 5 listed entries have ec 1-2 (KB :45, :111, :139, :286, :312; view :1650-1675).
- Rebuilding the views on master's KB ADDS a 6th: keltner_scoremode_fee_isolation_no_flip (KB :192, ec 2, basis "Empirical ...") -- matched by "analytically-explained". coverage_matrix also gains 2 stale rows (that entry + xs_momentum_cost_surviving_but_decaying).
- Second veto path: _check_kb_reactivation_conformance (run_phase1_research.py:9681-9744) pauses a run (kb_reactivation_violation) when campaign_review / verdict_interpreter text names the hypothesis_id of a finding with `exhausted: true` and no reactivation_condition, or with reactivation_consumed_by set. It reads the flag directly, not the view. Today it vetoes 10 findings: the 6 above + H-041-A / H-041-C (consumed) + H-041-C-v2, FUNDING_MR_DAILY_RETEST (exhausted, ec 1).
- anti_adjacency_gate Layer 1 (tools/anti_adjacency_gate.py:298) is advisory only -- untouched.
- Code auto-close F09 (run_phase1_research.py:10802-10816) writes "Empirical (...)" basis -- only a veto at ec >= 3 under both old and new rule.
- Trial count: NOT guaranteed. N for DSR = campaign_state.yaml trial_sharpes (run_phase1_research.py ~11280-11300; deflate_sharpe.load_sharpe_trials :403-416): 15 rows, first is run_041. Evidence runs 011-033 (and 018) are in campaign_state.runs only, not in trial_sharpes; research/TRIALS.csv (13 rows) has none. Freeing the families removes nothing from N -- they were never in it.
Per-entry verdicts (none rests on a structural argument -> withdraw all 5):
- keltner_mean_reversion_no_edge (KB :45): one IC estimate p=0.83 on a detector the KB calls unusable; its 4 evidence runs 017/024/027/033 are identical to the cent (one measurement). WITHDRAW.
- keltner_breakout_inverted (KB :111): "signal_inversion is direction-fatal" is the result's label, not a derivation; run_015 pooled gross +62.2 / net -53.2 / 67 trades; run_033 has the OPPOSITE corr sign (+0.28) so "both runs negative IC" is false; run_015 may be a config_path-bug run (campaign_state.yaml:464). WITHDRAW.
- keltner_scoremode_no_edge (KB :139): "cost_drag 84% on run_028" -- run_028 measured 131%/37% on 3 trades; ~85% is run_030 (AVAX, 3,640 trades, gross +479.7 / net -1,975.5); both declared 4h but ran 1h. Cost arithmetic on one turnover profile. WITHDRAW.
- rsi_mean_reversion_no_edge (KB :286): "parameter space exhaustively searched" = runs 011-014, all 831 trades under 4 different config hashes, same engine stamp 2754e184 -> most likely the default config ran (config_path bug). WITHDRAW; the bug cannot be fixed by text -- the real fix is a re-run (needs operator go) -> ticket.
- rsi_momentum_trending_cost_drag (KB :312): run_018 pooled gross +1,079.5 / costs 3,163.0 / net -2,083.5 / 1,345 trades (one config, pre-A22, baseline_v1, 22 monthly windows); 272.865 = median of 22 per-window cost/|gross| ratios, 7/22 windows gross < 0 -> unstable, not decision-grade. WITHDRAW, keep the pooled fact.
Changes:
- [ ] run_phase1_research.py: one predicate `_kb_finding_is_veto(f)` = exhausted AND (evidence_count >= 3 OR veto_basis + veto_approved_by + veto_approved_on all set). No prose match. Used by _recompute_kb_views (view entries carry `veto_reason: evidence_count | approved`) and by _check_kb_reactivation_conformance's exhausted branch (Q1). Docstrings updated.
- [ ] record_schema.py:198 (KB field types): add veto_basis / veto_approved_by / veto_approved_on.
- [ ] Prompts: research_brief_to_hypothesis.yaml:20, :31-36 and campaign_review.yaml:18, :31-32 -> a listed veto blocks only the same hypothesis id, or the same mechanism with the same config (component classes, parameters, timeframe, symbols as its evidence runs); every other finding is context, never a ban. campaign-review SKILL :128-146/:201/:224 and verdict-interpreter SKILL :202-213 -> "veto (listed in exhausted_mechanisms)" instead of "exhausted: true". Re-pin any sha this touches (to check: pins on those skills / templates).
- [ ] KB: the 5 entries -> exhausted: false, policy_consequence "WITHDRAWN 2026-10-01 (D-055): ...", readjudication_20261001 with the facts above (D-052 pattern, er_detector_unusable_btc_eth_1h KB :562). Nothing deleted. keltner_scoremode_fee_isolation_no_flip NOT edited (not a veto under the new rule; reported). Views rebuilt with _recompute_kb_views: exhausted_mechanisms -> [] ; coverage_matrix +2 stale rows (reported in PR).
- [ ] Tests (new test_d055_kb_veto_rule.py): basis with "analytic" / "Analytic:" / "non-analytic" / "analytically-explained" at ec 1-2 -> no veto; approved structured field -> veto; incomplete field (one of the three missing) -> no veto; ec >= 3 -> veto; reactivation check follows the predicate; live KB: 5 ids not vetoed, each has readjudication_20261001 + WITHDRAWN, finding count unchanged. Update test_resume_idempotency.py:82-97 fixture (it relies on "analytic" at ec 1). Mutation check on the predicate.
- [ ] DECISION_LOG D-055 row; docs mentioning the A5.1 analytic path (grep USER_GUIDE/RUNBOOK).
- [ ] Linear tickets (not fixed here): (a) cost_drag_pct as median of per-window ratios: run_protocol.py:1692/1750 -> consumers run_phase1_research.py:2494, :10305, :10938, verdict-interpreter cost_drag rule (campaign_config.yaml:838 threshold 80), readers, campaign-review -> use pooled gross vs pooled cost; (b) trial count: runs 011-033 not in N -- decide backfill; (c) rsi_mean_reversion evidence re-run (config_path bug); (d) evidence_count independence is unchecked (keltner_mean_reversion's 4 identical runs).
- [ ] Targeted tests; one full suite in parts < 10 min each, one process; Opus safety review; PR to master.
Open questions for the operator:
- Q1: _check_kb_reactivation_conformance: apply the predicate to the exhausted branch (frees H-041-C-v2 and FUNDING_MR_DAILY_RETEST from that check too) -- recommended yes; keep the reactivation_consumed_by branch (a pre-registered reactivation condition the operator wrote, consumed by a definitive run) -- recommended keep.
- Q2: trial-count backfill (runs 011-033 into N) -- ticket (recommended) or in D-055?
- Operator 2026-10-01: agreed on all -- D-055 plan OK; Q1 yes (exhausted branch follows the predicate, consumed branch kept); Q2 ticket; order: finish O-3 first, then D-055.
- [x] O-3 review (Opus): ship after fixes -> fixed #1-4 (rubric: classes only when plainly matching, else 2; unknown timeframe category = assumed match; category mapping; row 3 = no forecast block), #3 cost_model comment (Pearson on active bars, avg_trade_duration_bars), #7 config/README, #8 line ending, #9 pin comment, #10 USER_GUIDE; template prescreen line moved to D-055 (same file). #5 rubric version kept (no queued cards scored under old wording). #6 -> CUL-366 note. Committed 748ddaaa (local). Full research suite running in 16 parts.
- [x] D-055 built in wt_d055 (uncommitted): _kb_veto_reason (view + reactivation check), record_schema veto_* fields, 2 templates + 2 SKILLs wording, KB 5 entries withdrawn + views rebuilt (bans [] ; coverage +2 stale rows), DECISION_LOG D-055, test_d055_kb_veto_rule.py (17), k2/resume fixtures; targeted 432 green after fixture fix; 5/5 mutations killed. Opus review running. Tickets CUL-363..366.
- [x] O-3: PR #292 (fix/o3-costs-judged-by-backtest 748ddaaa; worktree scratchpad/wt_o3 with venv junction). Full research suite 16 parts green.
- [x] D-055: PR #293 (fix/d055-kb-veto-rule dd05d3c3; worktree scratchpad/wt_d055 with venv junction). Opus review applied; full research suite 16 parts green. Independent of #292.
- [ ] Operator: merge #292, #293. Then remove wt_o3 / wt_d055 (rmdir junction first) + local branches.
- [ ] NEXT: plan the fresh C4 run with the operator (unpark C4_vol_managed_trend resuming at 1b with MovingAverageDistanceComponent; then the Donchian brief) -- no real run without the go. Before any holdout spend: CUL-340, CUL-335, CUL-348, and now CUL-364 (N count).
- [x] #292 (O-3) and #293 (D-055) merged (master 94d22122); worktrees wt_o3 / wt_d055 removed (junctions first), branches deleted.

## C4 fresh run -- PLAN (STOP for operator go; no real run without it)
Facts (2026-10-01): c4/flag-set is 44 commits behind master (misses #281-#293: graded components, gap rule, NaN hold, D-052, O-6, O-3, D-055); merging master in touches none of the locally modified or untracked files (checked).
Queue: C4_vol_managed_trend paused:waiting_for_component (run_061 at 1b: needed a two-sided SMA trend -> MovingAverageDistanceComponent now exists, #282), brief_status exhausted (run_062's reason cites the withdrawn Keltner/RSI bans, A2.3 regime ban, "trend signal exhausted per KB" -- all removed today). C4_donchian_daily_trend paused:waiting_for_component (run_063 variant donchian_sentiment_gate needed FearGreedComponent -> exists, #289), brief open; its R2 entry C4_donchian_daily_trend__more_1 is ready (runs first on launch).
1. Merge origin/master into c4/flag-set (main checkout; runtime files untouched). Fast suite subset + validator smoke.
2. Unpark C4_vol_managed_trend (`run_campaign.py --unpark C4_vol_managed_trend`): resumes run_061 at 1b.
3. Reopen its brief (queue entry brief_status exhausted -> open, dated note citing O-3/D-052/D-055) -- or leave exhausted.
4. Unpark C4_donchian_daily_trend (resumes run_063).
5. Order: hold __more_1 until both resumed runs finish.
6. `--dry-run` first, then ONE real `--once` launch with the operator's go; report after each run.
- Operator: GO merge master into c4/flag-set; reopen C4_vol_managed_trend brief; resumed runs before __more_1. Real runs still need a go after the dry run.
- Operator: dry-run self-test bug (D-052 probe -> wishlist_trigger_data_gap rejected) -> fix first, small PR to master.
- [x] c4/flag-set: merged origin/master (2bc16005, local, not pushed); flag tests: only the 2 expected "flag is off" asserts fail (variant_anti_adjacency_gate, category_reports -- both in the deliberate 14-flag flip).
- [x] Unparked C4_vol_managed_trend (run_061 resumes at strategy_config_authoring) and C4_donchian_daily_trend (run_063 resumes at backtest_specification). Brief C4_vol_managed_trend reopened (queue hand-edit, backup %TEMP%/campaign_queue_before_reopen.yaml). Order needs no edit: priority 1 entries before __more_1 (999).
- [x] Dry run: all real checks OK (selects C4_vol_managed_trend, action continue, brief parsed, setup OK), then the self-test failed (D-052 probe bug). Fix: branch fix/dry-run-wishlist-probe 9496ba25 (worktree scratchpad/wt_dry, venv junction), 7 tests, 2/2 mutations; full research suite running.
- [ ] PR -> operator merge -> merge master into c4/flag-set -> dry run again -> ask for the go on the first real --once.
- Operator GO 2026-10-01: first real C4 run (--once, continues run_061 at 1b).
- Operator: override run_061 (base + design_sma_21 data-OK, interior quality gaps; CUL-367), resume at protocol_execution. Backups %TEMP%/run061_before_override.
- [!] run_061 resumed (override) -> base backtest: 0 trades in 95 windows. Cause: 1b used transform vol_adjusted (v / (stddev_24 * close), stddev_24 = rolling std of close in $) on MovingAverageDistanceComponent (percent output) -> |forecast| ~1e-5, below min_allocation_change. Run STOPPED during design_sma_21 (no grid/readers/verdict written). Operator: invalidate run_061:base (done, backup %TEMP%/campaign_state_before_invalidate.yaml); run_061 set paused_for_human. NEXT: O-10 observation; small PR (guide/catalog transform input units + fail-loud dead-forecast check) -- plan first; then send run_061 back to 1b.
- [x] O-10 recorded (docs branch docs/o8-data-quality-vs-missing-window, with O-8/O-9; push after a full suite).
- Operator: fail-loud check = size probe on real bars (not the static rule).

## Forecast-size probe -- PLAN (phase A, STOP for nod). Branch fix/forecast-size-probe from master.
Where: tools/forecast_rules.py gains forecast_size_violations(config, protocol); called by
_base_forecast_rule_violations (after 1b, run_phase1_research ~14111 on master; shares the ONE retry to 1b, then
pause forecast_rule_violation) and by 5a per variant (~2654-2660, variant not_tested with the reason).
How: run the real engine (trading-bot run_backtest, same data merge incl. funding/F&G feeds and gap rule) on a
SAMPLE of the run's own protocol windows, read ONLY bars.csv `forecast`; output in a temp dir, deleted.
Choices to confirm:
 1. Sample = 3 train-era windows of the variant's protocol/symbol: the first window in each era 2018-20, 2021-22,
    2023 (never >= 2024-01-01: no validation or holdout data). Warmup comes from the engine's own prefetch.
 2. Refuse when fewer than 1% of ready bars have |forecast| >= 10 x min_allocation_change (config.json
    risk_management.controls.min_allocation_change.threshold, 0.2 today -> |forecast| >= 2). Also refuse if every
    ready forecast is NaN. Message gives max |forecast|, p50/p95, share >= threshold, and the likely cause.
 3. Not a trial: no PnL, trade or metric is read or recorded (only the forecast column); declared in DECISION_LOG
    (D-056) and the docstring. "Why it can't leak": train-era only, scale only.
 4. Docs: STRATEGY_DESIGN_GUIDE transform table gives each op's input units and resulting scale (vol_adjusted /
    vol_normalize divide by ~price^2 -> only meaningful followed by ratio_to_mean); remove "divide by volatility
    with vol_adjusted" (~459); catalogue note on MovingAverageDistance/MacdHistogram (percent) + EMADiff (price).
 5. Tests: synthetic config with vol_adjusted on MovingAverageDistance -> refused; same without -> passes; NaN-only
    -> refused; threshold read from config; sample never >= 2024; integration via both call sites. Opus review.
Then: merge into c4/flag-set, reset run_061 to strategy_config_authoring (1b re-authors with the fixed guide),
dry run, ask go.
- Operator 2026-10-02 (going offline): "fix as planned and relaunch a new run (from step 1 or backtest directly)". Plan choices 1-3 taken as proposed (sample per era < 2024, 1% / 10x floor, not a trial).
- [x] Probe built: fix/forecast-size-probe 0072c8d1 (worktree scratchpad/wt_probe, venv junction + copied BTCUSDT_1h/funding/F&G caches). Flag orchestrator.forecast_size_probe (off). 20 tests, 8/8 mutations. Smoke on run_061 config: refuse (max 7e-6) / without vol_adjusted ok (51%). Opus review running.
- [ ] After review: full research suite, push, PR (operator merges). Merge branch LOCALLY into c4/flag-set + switch flag on there; reset run_061 to strategy_config_authoring; dry run; relaunch (operator authorised).
- [x] Re-run of run_061 would hit the trial recorder's (trial_id, source) duplicate guard -> new run instead. Queue: C4_vol_managed_trend -> done (note); new entry C4_vol_managed_trend__h1 (origin brief, card_ref campaign_record/queued_cards/run_061/hypothesis_card_relaunch.yaml, priority 1, ready) launches past 1a; C4_donchian_daily_trend priority 1 -> 2 (keeps idea 1 first). Backup %TEMP%/campaign_queue_before_relaunch.yaml.
- [x] Probe review fixes f6dde11c (M1 strategy floor, M2 1b only validated + per-variant errors, cache, sealed outputs, guide wording); holdout gate caught a sealed date in a test -> sentinel (lesson). Full suite running.
- [x] Merged probe into c4/flag-set (a02d1e2d), flag on (3d88c932); dry run PASSED (selects C4_vol_managed_trend__h1, queued_card). Launching --once.
- [!] run_064 (C4_vol_managed_trend__h1) failed pre-flight before spend: queued-card launch skips 1a so _write_pass_rule_from_card never ran (pass_rule null). Filled by calling that function (backup %TEMP%/run064_prereg_before.yaml), state reset to active; resuming. Bug fix PR needed (_launch_queued_card).
- [!] run_064 step 2 (innovation_expansion) wrote only expanded_hypothesis_card.yaml (16k output tokens, 1 turn); missing innovation_notes.yaml + variant_patches.yaml -> unhandled_exception. Kept attempt-0 card as expanded_hypothesis_card.attempt0_incomplete.yaml; ONE retry via --resume. Follow-up: save raw agent output when a deliverable is missing (today only when no block parses).
- [x] D-056 asset fix (probe error on an asset variant = D-042 coverage skip) committed on fix/forecast-size-probe + merged into c4 (14b6bf8b). run_064 reset to backtest_specification to rebuild variants.
- [x] run_064 data gate paused (same 21 BTC refine windows as run_061, verified identical) -> same recorded override (base + V1_conservative_scale), human_resolution.yaml, resume at protocol_execution. Backup %TEMP%/run064_index_before_override.yaml.
- [x] run_064 backtests done (base 32,648 trades gross -1,354 net -12,173 Sharpe -2.88; V1 20,513 / -727 / -6,099 / -2.61; trial rows counted). Halted before grading: CUL-369 windows overlap one day (Urgent), CUL-370 category report over budget (CUL-371 = duplicate, canceled), CUL-368 Kraken cost model missing. O-11 on docs branch.
- [ ] Push 3 PRs after a full suite each (one at a time): fix/forecast-size-probe (running), fix/queued-card-pass-rule, docs/o8-data-quality-vs-missing-window (O-8..O-11).
- [ ] NEXT SESSION: operator merges; decide CUL-369 (declared behaviour change, baselines) first -- grading cannot run without it; then CUL-370; then re-grade run_064 (no new trials) or continue Donchian (priority 2, ready).
- [x] PRs open (full suite green on each head): #295 D-056 forecast-size probe, #296 queued-card pass_rule fix, #297 observations O-8..O-11. Worktrees still present (wt_probe, wt_qcard, wt_o8 with venv junctions; wt_probe has copied caches) -- remove after merge, junctions first.

## Venue wiring (O-12 / CUL-46) -- Phase A done 2026-10-02 (Sonnet map), STOP for operator decision
Facts (file:line in the agent report, summarised):
- Brief (venue, product) reaches ONLY check_venue_tradability (run_campaign.py:368-377, :769-773).
- Data exchange: protocol `exchange` -> else binance (run_protocol.py:2292-2296). Market type: run_backtest kwarg -> config.json (no key) -> 'margin' (launcher.py:852-855); nobody passes it. Fee: run_protocol --cost-product default 'spot' (never set by orchestrator) overrides cost_model.json fee. Slippage + existence check: cost_model.json (binance/margin, kraken/futures only).
- Vocabularies disagree: venue_tradability {spot, perp, margin}; cost_model.json {margin, futures}; cost_model.yaml {spot, perp}; no futures<->perp alias. A brief `product: futures` would be research_only (not in venue_tradability); `perp` would crash the cost lookup.
- Data: NO Kraken futures OHLCV anywhere (fetcher defaultType hardcoded spot, CUL-287). kraken_BTCUSD/ETHUSD_1h are Kraken SPOT (BTC from 2013-10). Kraken perp funding exports PF_XBTUSD/PF_ETHUSD exist only from 2022-03-22 (Kraken_funding_rates/exports), not wired to the engine; engine funding accrual is Binance-8h only and off.
Options: A) resolver (venue,product)->(exchange, market_type, fee product, slippage key) + thread into protocol/run_protocol/probe/variant protocols + fail loud; Kraken futures costs on Kraken SPOT prices, labelled as a proxy; funding declared unmodelled. B) A + real Kraken futures OHLCV ingest (history ~2022+ for PF perps -> test period shrinks, era bar 2018-20/2021-22 not coverable). C) B + funding accrual (E-053).
- [ ] Operator: pick A/B/C (recommend A now, B/C later as their own epic).
- Operator 2026-10-02: size probe -> bug-only on invented data (done d39747a1); review fixes (f04b4b21); coin price level + cap rule = persistence only (forecast at the +/-20 cap on EVERY active bar) (5821422a). Venue: option A (proxy now). Past results: dated note only (CUL-369). O-12 (venue gap, CUL-46/E-014/E-015) and O-13 (zero floor / all-zero pass by design) on docs branch.
- [ ] Probe branch full suite running -> push (updates #295) + PR body; then docs branch suite -> push (#297).
- [ ] NEXT: venue option A -- Phase A plan exists in todo above; write the build plan (resolver + threading + fail-loud + vocab alias) and STOP for nod.

## Venue option A -- BUILD PLAN (operator chose A 2026-10-02). STOP for nod before any code.
Branch fix/venue-resolver from master; one PR.
1. One resolver, strategy-research/tools/venue_resolver.py: (venue, product) -> {exchange, market_type (cost_model.json key), fee_product (cost_model.yaml key: spot|perp), data_exchange, price_proxy: bool, funding_modelled: False}. Explicit alias table in ONE place: futures == perp (cost_model.json says futures, tradability + yaml say perp). Unknown pair -> raise (fail loud). Kraken futures -> data_exchange kraken (SPOT prices), price_proxy True (labelled), market_type futures, fee_product perp.
2. Threading:
   a. _ensure_protocol_from_constraints writes the resolved `exchange` + new additive `market_type` + `fee_product` + `price_proxy` into the generated protocol, from the brief's venue/product (research_brief.yaml). Brief without venue/product: nothing written (byte-identical default).
   b. run_protocol: reads protocol market_type -> run_backtest(market_type=...) and protocol fee_product -> --cost-product equivalent (CLI flags still override). Missing keys -> today's behaviour.
   c. variant_coin.variant_protocol carries the new keys (_VARIANT_KEYS / check_variant_protocol updated).
   d. forecast_size_probe: nothing to thread (invented data, no costs).
3. Fail loud before spend: resolved (exchange, market_type) must exist in cost_model.json and fee_product in cost_model.yaml; the protocol's data cache for (exchange, symbol, timeframe) must exist (data gate already checks coverage; add the venue to its message).
4. Labels: metrics.json / protocol_result carry venue, market_type, fee/slippage bps used, price_proxy, funding_modelled=false, so every result says what it modelled.
5. C4 brief: venue kraken / product perp(=futures) -- set on c4/flag-set only after the PR merges (needs Kraken spot caches for BTC/ETH: kraken_BTCUSD_1h / kraken_ETHUSD_1h exist; symbols BTCUSD/ETHUSD).
6. Tests: resolver table (incl. alias, unknown raises); brief -> protocol keys; run_protocol passes market_type (stub run_backtest); variant protocol keys; byte-identical default (brief w/o venue, binance); fail-loud missing cost entry. Opus review (core + money-affecting). Slow tests: engine path unchanged unless market_type passed -> run pinned slow set once.
Open questions for the operator: (a) does an existing Binance brief stay byte-identical (recommended: yes -- resolver only acts when the brief names a venue the table knows; binance/margin = today's defaults); (b) fee for Kraken perp = cost_model.yaml perp block (5 bps) vs cost_model.json kraken/futures (5 bps) -- same today; pick yaml as the one source? (c) symbols: C4 brief lists BTCUSDT/ETHUSDT; under kraken they map to BTCUSD/ETHUSD via the existing venue_symbol logic -- confirm.

## Venue option A -- REVISED PLAN (operator 2026-10-02: process + fix OK; Kraken futures = Kraken SPOT local data as price proxy, Kraken FUTURES costs)
Design facts confirmed: E-054 gate checks the RESOLVED PROTOCOL (Q2/Q3), deliberately not the brief; E-010 single cost source = trading-bot/config/cost_model.json; E-014 = tradability at registration (CUL-183's fees/data refusal never built). Missing link = brief (venue, product) -> protocol.
1. venue_data_capability.yaml (E-054 Layer 1): kraken.futures gets a declared `price_proxy: {source: kraken.spot, label: "Kraken spot prices as a proxy for Kraken futures; funding not modelled", basis: operator 2026-10-02}`. The gate's Layer 1 resolves futures prices through it (spot symbols BTCUSD/ETHUSD...); everything else unchanged.
2. Protocol creation (_ensure_protocol_from_constraints + variant_coin): write exchange=kraken, market_type=futures (cost key), price_source=kraken.spot (from the proxy), symbols as the venue's data names (BTCUSDT -> BTCUSD). Alias perp==futures in ONE place. Brief with no/unknown venue entry -> unchanged (byte-identical).
3. Engine call: run_protocol passes market_type -> run_backtest (costs from cost_model.json kraken/futures); data fetched from the price_source (kraken spot cache). Remove run_protocol's commission override from cost_model.yaml (E-010 single source) -- DECLARED change (Binance fee 7.5 -> 10 bps on future runs; pinned tests re-pinned deliberately; past results: dated note only).
4. Gate (E-054) reads the protocol's exchange/price_source (no new design), so it checks the Kraken spot caches.
5. Labels in every result: venue, market_type, price_source, fee/slippage bps used, price_proxy=true, funding_modelled=false.
6. Registration (CUL-183): refuse a brief whose (venue, product) has no cost entry or no data/proxy in Layer 1 -- if the operator wants it in this PR.
7. Tests + Opus review (money-affecting); pinned slow set once (fee source change).
- Operator 2026-10-02: GO venue plan; CUL-183 NOT as a separate registration gate -- protocol creation (run start, before any LLM call) fails loud when (venue, product) has no cost entry or no data/proxy; E-054 gate + engine cost lookup remain as later nets. Branch fix/venue-to-protocol from master.
- [x] D-057 venue wiring built: fix/venue-to-protocol d782cfe2 (worktree scratchpad/wt_venue, venv junction). venue_resolver.py + capability price_proxy + protocol creation + run_protocol (market_type + json fee for venue protocols) + variant_coin (base-asset match; asset on run venue). 26 tests, 6/7 mutations (7th equivalent). Gate smoke kraken/BTCUSD 2022-03/04 validate. Opus review running.
- Note: D-056 (#295) and D-057 both insert above D-055 in DECISION_LOG -> second to merge needs a trivial rebase.
- [ ] After review: full research suite, push, PR. Then (separate PR) Binance runs to cost_model.json fee (declared change 7.5 -> 10 bps). Then C4 briefs on c4/flag-set -> venue kraken / product perp.
- [x] D-057 Opus review: B1 + M1-M4 + minors fixed (76897b72), 48 venue tests, 9/9 review mutations caught; full suite 4315 passed (one static pin updated). PR #298 open -> master. Conflicts with #295 on DECISION_LOG (trivial rebase for the second to merge).
- [ ] After #298 merges: c4/flag-set merge master; C4 briefs -> venue kraken / product perp (ASK before editing runtime files); plan next C4 run (no run without go; grading needs CUL-369).
- [ ] Separate PR: Binance runs to cost_model.json fee (declared 7.5 -> 10 bps).
- [x] #298 merged; worktrees wt_o8/wt_probe/wt_qcard/wt_venue removed (junctions first), branches deleted.
- [x] Docs PR #299 (docs/o11-o13-update, worktree scratchpad/wt_obs): O-11/O-12/O-13 updated, O-14 (Binance spot fee + margin slippage mix) added.
- [ ] Next: CUL-369 plan in todo -> STOP for approval. Then C4 briefs spot->perp (decide: edit in place vs new brief). Then O-14 PR.

## CUL-369 -- protocol windows overlap by one day (PLAN, awaiting approval, 2026-10-02)

### Facts (file:line from the inventory, master 70539e03+)
- Engine end is INCLUSIVE BY DAY and documented so: base_fetcher._inclusive_end (336-359) -> 23:59:59.999, trim `<= window_end` (321-324); pinned by trading-bot/tests/test_fetch_end_bound.py. The holdout guards rely on it (holdout_policy.py:174 `end < bound`; run_protocol ~2425 comment).
- Protocol files mostly LOOK exclusive: 10 tracked hand-made protocols (baseline_v1/v2, diagnostic_btceth_4h, escalation_*, funding_mr_*, h041c_v2_backext, ts_trend_daily_v1) have end == next window's start -> every one overlaps by a day.
- _generate_monthly_windows (run_phase1_research.py:9030-9060) MIXES conventions: tiles end on the next month's 1st (exclusive look), the last tile ends on the user's end (inclusive: "...-12-31"). Its docstring/holdout error already say "end is INCLUSIVE-BY-DAY at the engine".
- Consumers disagree:
  - variant_coin coverage counts start..end inclusive (one junction day counted once);
  - portfolio_whole_test.chain_windows already handles the overlap as a "junction" (later window rescaled at the join day);
  - the data gate expects (end - start)//interval bars, i.e. exclusive, so it never checks the end day's data;
  - residual_ic (grid) refuses non-increasing timestamps -> the run_064 halt;
  - run_protocol._assemble_pooled_symbol_records (1283-1340) concatenates per-window bars with no de-dup -> pooled IC/episodes double-count.

### Recommendation: one convention, the engine's -- `test.end` is the LAST INCLUDED DAY
Rejected: making end exclusive at the engine call (the ticket's first idea). The last generated tile would then need an end ON the holdout start date, which touches the holdout guards and the sealed-date rules. The inclusive convention needs no holdout change.

- [ ] 1. Generator: each tile ends on the month's last day (2018-03-31); the last tile is unchanged (user end). Windows tile with no shared day.
- [ ] 2. Fail-loud pre-flight in run_protocol (before any backtest): refuse a protocol whose consecutive windows share a day (`windows[i].test.end >= windows[i+1].test.start`, by day). Cheapest control; catches any hand-written or old protocol.
- [ ] 3. Migrate the 10 tracked hand-made protocols to inclusive ends (end = next start - 1 day). DECLARED: their windows lose the extra day, so any rerun differs from past artifacts. Untracked runs/run_0xx_generated.json are left as-is (history; dated note).
- [ ] 4. Data gate: measure each window through the END OF its end day (expected bars = (end + 1 day - start)//interval), so a gap on a window's last day is no longer invisible. DECLARED.
- [ ] 5. Check, and fix if needed, that chain_windows treats [..03-31][04-01..] as contiguous (no junction, no gap day). Old junction handling is kept for old results.
- [ ] 6. Tests:
  - re-pin the contiguity tests (test_sweep_holdout_clamp 85-100: a.end + 1 day == b.start; test_prereg_conformance_gate);
  - new tests: generated windows are disjoint and contiguous; the pre-flight refuses an overlapping protocol; each tracked protocol passes the pre-flight;
  - gate end-day test; chain adjacent-window test;
  - mutations for each.
- [ ] 7. Docs:
  - DECISION_LOG row (convention + declared changes);
  - dated note in OBSERVATIONS O-11 / runbook: past monthly-window results double-count ~1 day in 30 -- NOT re-scored (operator, 2026-10-02);
  - CUL-369 comment.
- [ ] 8. Full research suite + trading-bot fast suite (one process each, from the right CWD); Opus safety review (holdout-adjacent: generator + pre-flight); PR to master.

Not in scope: engine changes (trading-bot untouched); re-scoring past runs; CUL-370 (report size); O-9 (window length/selection).
Open for operator: (Q1) inclusive convention as recommended? (Q2) migrate the 10 tracked protocols now (recommended) vs leave them and let the pre-flight refuse them? (Q3, carried) C4 briefs spot->perp: new briefs (recommended) or edit in place?
- [x] CUL-369 built: fix/cul-369-window-overlap 5f8c1f25 (worktree scratchpad/wt_369), PR #300. Opus review addressed (1st-of-month end refused; launch pre-flight checks all 3 branches; midnight rule; declarations). 37 new tests, 13/13 mutations; full suite 4397 passed. Linear CUL-369 commented.
- [ ] After #300 merges: remove wt_369 (junction first). Then C4 briefs -> NEW briefs with product perp (operator: new briefs, 2026-10-02). In-flight: run_063 delete generated file; run_061/run_064 relaunch under new id.
- [ ] Open decisions: O-15 (chain anchor at window open?), O-14 (Binance market spot vs margin). Follow-up: check_data.py end convention; CUL-370.

## C4 restart on Kraken perp (PLAN, awaiting approval, 2026-10-02)
Operator 2026-10-02: O-14 (Binance cost mix) PARKED (no Binance research going forward); O-15 FIX approved; C4 = NEW briefs, product perp.

Facts:
- The C4 briefs live only on c4/flag-set (commit 2742191c, NEVER MERGE).
- Queue:
  - C4_vol_managed_trend: done, brief open, run_061 paused, spent;
  - __more_1: done, run_062, brief exhausted;
  - __h1: paused, run_064 failed, spent;
  - C4_donchian_daily_trend: ready, run_063 at the data gate, NO spend;
  - its __more_1: ready.
- Kraken spot caches start: BTCUSD 1h/1d 2013-10, ETHUSD 1h/1d 2015-08 (head only). The data gate checks the end at run time.
- Merging master into c4/flag-set: no conflicts, no overlap with the locally modified runtime files.

### A. Prep on c4/flag-set (touches live files -> needs the go)
- [ ] A1. `git merge origin/master` into c4/flag-set. Brings D-056/D-057/D-058; no conflicts measured.
- [ ] A2. Two new briefs, committed on c4/flag-set like the first ones:
  - `briefs/C4_vol_managed_trend_kraken_perp.md` and `briefs/C4_donchian_daily_trend_kraken_perp.md`;
  - same idea, universe, timeframe and windows; `product: perp`;
  - a header line "supersedes <old brief>: its trials ran on Binance spot data and costs".
- [ ] A3. Queue (runtime file, edited, not committed):
  - the four old C4 entries -> closed / superseded, with a dated note. Their trials stay counted; run_061/run_064 stay as records; run_063 is never resumed (superseded, it spent nothing);
  - two new entries, status HOLD until B is merged.
- [ ] A4. Dry-run pre-flight of both new entries (no LLM, no data): protocol creation must resolve kraken/futures, symbols BTCUSD/ETHUSD, fee 5 bps, drop funding.

### B. Must merge before the first real launch (each its own PR from master)
- [ ] B1. CUL-370: the category report over its size budget on 95 windows (run_064 halted on it). Otherwise the 1h brief halts at grading again.
- [~] B2. PARKED (operator 2026-10-02, PR #301): the left-out entry is a monthly-restart artifact, not a real cost; the real issue moved to O-9. Original plan: the whole-test chain counts each window's first day. Anchor at the window's starting equity (from the run's initial balance, not the first logged bar, which is after the first trade). Buy-and-hold is anchored the same way, entry cost included. Declared metric change; two-phase (characterize, STOP, implement).

### C. Launch
- [ ] C1. Merge master into c4/flag-set again; flip the entries to ready; dry-run again; operator go for the real run.
- [x] PR #302 CUL-370 (per_symbol index, no duplicate core; measured 648K->386K on run_064 slices; 95x2 still over -> fewer windows). Suite 4398 passed.
- [~] feat/window-months (wt_wm): window_months 1/2/3/4/6/12, year-aligned; RUNBOOK 1f (draft limits); template; D-059. 5/5 mutations. Full suite running. Linear CUL-372 (parked auto-check).
- [ ] fix/venue-conformance-symbols (wt_vc): conformance compares base assets for venue protocols (else Kraken runs invalidated after spend). Tests written, not run yet. Note: a brief pinning a Kraken protocol file could still trip the registration lint (_normalize_symbol strips USDT only) -- note in PR.
- [ ] Then part A (needs go): c4/flag-set merge master; new perp briefs 2022-01-01..2023-12-31, window_months 4 (6 windows), labelled end-to-end workflow run; close old entries; dry run.
- [ ] O-9 note: engine force-closes at window end (criterion_menu comment "end_of_window forced closes") -- add to O-9 after #301 merges.
- [x] Epics: E-065 (mandatory C4 Kraken e2e: CUL-373/374/375/376, 369), E-066 (nice-to-have: 367/368/372/377), E-067 (trust results: 364/365/366), E-046a (+370, 363).
- [x] CUL-375 part A done: c4/flag-set merged master (da45fe30), Kraken-perp briefs committed (23092d45), old entries closed, new entries registered (Donchian ready p1; vol blocked_on_cul_374 p2), dry run PASSED, protocol check OK (kraken/futures, BTCUSD/ETHUSD, 5 bps, drop funding, 6 windows).
- [ ] CUL-373 conformance fix: full suite running (wt_vc) -> PR.
- [ ] CUL-374 data gate small gaps -> plan/build (blocks the 1h brief only).
- [ ] CUL-376 launch Donchian 1d after #CUL-373 merges + operator go (single-step, RUNBOOK 1d).

## CUL-374 -- data gate: gaps the engine ignores must not pause the run (PLAN, 2026-10-02)
Facts:
- Kraken BTCUSD/ETHUSD 1h 2022-23: 1 missing bar each (measured). 1d: complete.
- The gate (tools/data_availability_gate.py::_missing_fraction / classify_missing_fraction): any missing fraction > 0 -> `refine`.
  - Run level: refine -> paused_for_human (run_phase1_research ~15933).
  - Variant level: not_tested (~1659).
- Engine default (launcher.DEFAULT_GAP_POLICY): gaps <= 3 bars = "ignore". The comment there says most are Kraken no-trade hours.
- So the gate pauses on what the engine treats as nothing.

Plan (one PR from master):
- [ ] 1. In check_price_window, measure the longest missing run (in native bars) alongside the fraction. Record every gap (start, bars) in the result.
- [ ] 2. A window whose every gap is <= the engine's ignore_max_bars (read from launcher.DEFAULT_GAP_POLICY: one source, no copied 3) -> `validate`, with a `small_gaps` note in the gate artifact. Any longer gap -> today's fraction rule, unchanged. That rest is CUL-367 (E-066).
- [ ] 3. Price windows only; aux feeds unchanged.
- [ ] 4. Tests:
  - 0 gaps, a 1-bar gap, a 3-bar gap, a 4-bar gap (still refine);
  - two 3-bar gaps (validate);
  - an edge gap at the window start/end (counted by the same run measure);
  - the constant is read from launcher.
- [ ] 5. Mutations; full suite; PR. DECLARED behaviour change: windows with only <= 3-bar gaps now validate (e.g. Binance BTC 1h windows whose gaps are 1-3 h; longer ones still refine). DECISION_LOG row.
- [x] PR #304 CUL-373 merged; PR #305 CUL-374 open (4428 passed).
- [x] run_065 (Donchian 1d Kraken) launched; halted in 1a: file name above the YAML fence -> missing file, no retry. No spend beyond one 1a call ($0.21). CUL-379 in E-065.
- [~] CUL-379 (wt_fmt): parser reads name-above-fence; retry once on no-block answers (any stage) and partial answers (not 1a). 21+11 tests, 8/8 mutations; full suite running.
- [ ] After #305 + CUL-379 merge: c4/flag-set merge master; resume run_065 (status active, last_error null, --resume per RUNBOOK §4); unblock the vol 1h entry (blocked_on_cul_374 -> ready).
- [ ] CUL-378 (E-066): gate does not check the warm-up history.
- [ ] Follow-up (non-blocking, seen run_065 2026-10-02): hypothesis_card schema warns on `edge_source.requires_new_feed: null` (model meant "none"); treat null as absent or allow null. Warning only, run continued.
- [ ] Follow-up (non-blocking, pre-existing since run_064): config-direct 1b's decision.yaml / backtest_spec.yaml lack `hypothesis_id`, which their schemas require -> warnings every run. Align the schemas with the new pipeline, or have 1b write the id.
- [x] run_065 resumed: 1a/1b/2/5a OK, data gate VALIDATE x3, backtests 3 trials (473/487/530 trades; Sharpe 0.148/-0.13/1.17 -- 2-year workflow test, best of 3, not a finding), conformance OK (#304 held), grid GRID_EVALUATED idea_status refuted, 5 reports 10-65K chars. Halted at specialist_readers: regime_power reader new_block lacks rationale after retry -> CUL-380 (E-065).
- [x] Queue race confirmed: vol entry edit was lost while the campaign ran; re-applied with no process running (vol entry ready).
- [ ] CUL-380: state the new_block shape in all reader SKILLs + full shape in the refusal message; then resume run_065 from specialist_readers (readers re-run, ~5 AI calls).
- [x] run_065 (Donchian 1d Kraken) COMPLETED END TO END: completed_refuted; KB grid_run_065 + memory recorded; 2 reader proposals, none dropped; decide-next picked C4_vol_managed_trend_kraken_perp (ready). CUL-376 commented.
- [ ] Next (needs go): launch vol-managed 1h brief (--once), monitor; then E-065 done if it completes.
- [x] E-068 epic created (O-18 + O-19, findings + reader rewrite); CUL-381 bug (stale campaign-level regime_detector_report fed to readers). PR #308: O-19 observation.
- [~] run_066 (vol-managed 1h Kraken) launched --once, monitoring. Its regime reader may again read the stale detector report (CUL-381 open).
- [x] run_066 (vol-managed 1h Kraken) COMPLETED END TO END, hands-off: completed_refuted; CUL-374 small_gaps confirmed on real data; XRP asset variant non-blocking refine; readers 2 proposals both unusable (O-19 again: patch to nonexistent entry_lookahead_bars). CUL-376 Done; E-065 Completed.
- [ ] DECISION NEEDED: decide-next R2 added 2 ready queue entries (C4_*_kraken_perp__more_1). A plain campaign launch would run them (more 2-year workflow tests). Hold them (blocked_on_e068?) or run?
- [ ] Open: PR #308 (O-19 docs) to merge; E-068 design discussion; E-066 backlog; E-067 before any holdout; follow-ups: schema warnings (requires_new_feed null, hypothesis_id), check_data.py convention.
- [x] Session closed 2026-10-02: R2 entries blocked_on_e068; no scratchpad worktrees; SESSION_LOG entry + next-session prompt written (quick wins CUL-381 / patch-field check / reader inputs, then E-068 design proposal, no runs).

## 2026-10-03 -- E-068 quick wins + design + faster tests
- [x] (a) CUL-381 readers see only this run's output -> PR #309 (D-062). Full suite 4459 passed + 1 test-only pin fixed after. Opus review clean. Real-run check: master vs fix reports identical except regime_power's 3 intended fields.
- [x] (b+c) readers get hypothesis_card, manifest (optional), base config, COMPONENT_CATALOG, STRATEGY_DESIGN_GUIDE -> PR #310 (D-063). Full suite 4480 passed, 0 failed (-n 8). 5/5 mutations killed. Real-run dry check: all 10 run_065/066 reader prompts build with the 4 inputs and the real component ids.
- [ ] MERGE NOTE: #309 and #310 both add a DECISION_LOG row above D-061 -> rebase whichever merges second.
- [x] E-068 design proposal -> draft PR #311 (document only). Operator to answer section 10 (7 decisions; the unblocking two: templates-only graded tests? review record-first or gate?).
- [~] Faster tests -> chore/faster-test-runs (pytest-xdist pinned, single-thread BLAS per worker, CLAUDE.md test rule). Measured: serial ~20 min; -n 4 12.2 min 0 failures; -n 8 15.6 min with 2 crashed workers (memory). CI already runs the full suite on every push (Ubuntu+Windows) -> local full runs only when CI cannot be used.
- [ ] Follow-up: lazy-import claude_agent_sdk/google.genai in run_phase1_research (~3.6 s per Python subprocess; 26 test files spawn subprocesses). Production change -> its own PR, measure first.
- [ ] Follow-up: order-dependent flake test_grid_evaluation::test_era_id_for_timestamp_open_ended_era_lower_bound_excludes_earlier_dates (returned a real-policy era id for a synthetic era list once, serial run; passes alone and under -n 8). Cause not found in 15 min.
- [ ] Follow-up: token-budget headroom with D-063 inputs (~+20k tokens per reader call; run_065 headroom ~490k -> ~320k est.). Measure on the first run.
- [ ] Deferred: reader-time patch check (decide-next already refuses) -> part of E-068 reader v3.
- [ ] Deferred (later, operator): per-stage reader model setting (Sonnet ~2x Haiku per token).
- [x] #309, #310, #312 merged (2026-10-03). #311 (E-068 proposal) revised: readers explain + propose, never judge (branch 1 judges); composable 4-slot test engine (selector/outcome/baseline/statistic, ~15 blocks, grown on demand via test_requests). Open: section 10's 5 decisions. Next after answers: slice 1 plan (claim_tests.py engine + offline re-grade of run_065/066) -> STOP for nod.

## E-068 slice 1 -- test engine + offline re-grade (PLAN, 2026-10-03; STOP for operator nod)
Facts (measured):
- Backtest output per variant: artifacts/variants/<vid>/protocol_result.yaml results[].run_id -> variants/<vid>/results/<run_id>/bars.csv (same mapping as build_reports.load_run_sources). run_065 base: 6 windows x 120 daily bars, test period only (no warm-up rows), columns timestamp/close/forecast/regime. Regime is 'unknown' everywhere (ungated scaffold).
- Reusable statistics: trading-bot/performance/signal_statistics.py (spearman_correlation :68, block_adjusted_pvalue :188, gap_aware_active_block_count :154, stationary_block_bootstrap_ic_significance :601). Eras: tools/protocol_resolution.py era_id_for_timestamp :125, load_policy_eras :101.
Build (one PR from master, tool only -- nothing calls it yet, so no flag is needed and every run is unchanged):
- [ ] tools/claim_tests.py, pure (no orchestrator import):
  - TestSpec(selector, outcome, baseline, statistic, floor); SELECTORS/OUTCOMES/BASELINES/STATISTICS registries; check_spec, run_test, spec_hash (sha256 of canonical JSON).
  - load_variant_bars(run_dir, vid): the mapping above.
- [ ] v1 blocks:
  - selectors: event, regime, regime_change, calendar, quantile, all.
  - outcomes: fwd_return(h), fwd_volatility(h), fwd_max_drawdown(h), trend_ends(h).
  - baselines: complement, placebo, other_selector.
  - statistics: mean_diff, rank_ic, hit_rate, decay_curve.
- [ ] No-lookahead rules, built into the blocks:
  - selectors read only bar-t fields (forecast, regime, timestamp, close at t); check_spec refuses any other field;
  - `quantile` uses a TRAILING window (past bars only), never the whole-sample quantile, which would leak;
  - forward outcomes are computed inside each window only (the last h bars of a window are dropped, never chained across windows).
- [ ] Significance: one-sided p from a block placebo, the same for every statistic. Shift the selected-bar mask circularly by random offsets within each window and symbol (seeded), recompute the statistic, and compare. This keeps the clustering of events and returns. Floors: min_events, min_eras; below them the result is inconclusive. Per-era values via protocol_resolution.
- [ ] CLI: `python tools/claim_tests.py --run runs/<id> --spec <spec.yaml> --out <file>` writes YAML. It never writes into runs/.
- [ ] Tests (targeted; CI runs the full suite):
  - planted effect -> supported; no effect -> not supported, and the p-value spread is sane over seeds;
  - check_spec refuses a future field;
  - quantile is trailing (changing a future bar never changes today's selection);
  - no crossing of window boundaries;
  - floor -> inconclusive;
  - spec_hash is stable and order-independent.
  - Then a mutation check.
- [ ] Offline re-grade. Specs are fixed HERE, before any result is seen. They are read from saved bars.csv, so no new data, no backtest and no AI call. Output: engineering/roadmap/E-068/REGRADE_run065_run066.md (+ yaml), counting "N tests run = 2".
  - run_065 claim ("after a top-20% close, returns over the next 1-5 days beat ordinary days"): selector event(forecast >= 12) (Donchian forecast = (2*pos-1)*20, so pos >= 0.8 <=> forecast >= 12); outcome fwd_return([1,2,3,4,5]); baseline complement; statistic mean_diff, direction greater. Pass: mean_diff > 0 at every horizon, p < 0.05, same sign in >= 2 eras. Floor: 100 events, 2 eras. Run on every graded variant.
  - run_066 claim, direction part ("multi-week momentum carries continuation"): selector all; outcome fwd_return([24, 72, 168]) (1h bars); statistic rank_ic of the forecast, direction greater. Pass: IC > 0 at every horizon, p < 0.05. Floor: 30 effective blocks.
  - run_066 claim, "cuts crash losses": NOT expressible. It needs the sized vs unsized strategy's drawdown, and vol sizing was not even in the config. Recorded as a test request (the missing outcome block), not forced.
- [ ] PR; DECISION_LOG row; E-068 Linear story for slice 1.
Phase A check (2026-10-03, against origin/master 2ab2f165 + the saved run dirs; no outcome looked at):
- Confirmed: bars mapping build_reports.py:295-337 (results[].run_id -> variants/<vid>/results/<run_id>/bars.csv); signal_statistics.py :68/:154/:188/:601; protocol_resolution.py :101/:125; import via sys.path insert as tools/residual_ic.py:71-79.
- Confirmed: run_065 forecast == donchian component on every row; strategy_components.py:490-492 forecast=(2*pos-1)*20, so forecast>=12 <=> pos>=0.8. run_066 forecast = keltner component clipped to +-20 (checked: every differing row is a clip).
- Graded variants: run_065 base/period_14/solusdt (BTC, BTC, SOL); run_066 base/extended/sol_infra; xrp_payment has no protocol_result -> reported "not graded". One symbol per variant; no ETH anywhere.
- runs/ is untracked -> the worktree has no run data. Re-grade reads the main checkout's runs/ read-only; report records sha256 of every bars.csv used.
- C1 ERAS: all 6 windows (2022-01..2023-09) sit in ONE policy era (era_2019_2023_full_feed). "same sign in >=2 eras" / min_eras 2 can never pass -> inconclusive by construction. Needs a decision.
- C2 PLACEBO: shifting the selected-bar mask does nothing when selector=all (rank_ic). Generalize: shift the bar-t side (mask or forecast) against the outcome, circularly within each window, offset drawn from [h_max+1, n-h_max-1] (a tiny shift re-creates the real statistic).
- C3 GAPS: run_066 window 2023-05 has 2951 rows, 2952 expected -> forward outcomes by timestamp (t+h*step must exist), not by row offset.
- C4 DIRECTION: TestSpec has no `direction`; add it (greater/less), included in spec_hash.
- C5 run_065 thesis is two-sided ("above 80th ... or below 20th"). Plan tests only the upper side. Needs a decision.
- C6 run_066 card says momentum window 3-21 days (72-504 bars); plan horizons [24,72,168] start below it. Needs a decision.
- C7 pre-registration: commit the two spec YAMLs in their own commit BEFORE the re-grade runs.
- C8 per-horizon p; claim passes only if every horizon passes (intersection test, no multiplicity correction needed).
- Undefined blocks get definitions in the module docstring before code: fwd_max_drawdown(h)=min over (t,t+h] of close/close_t-1; trend_ends(h)=sign of fwd h-bar return opposite to sign of trailing h-bar return; hit_rate=share of selected bars with outcome in the claimed direction vs baseline share; decay_curve=mean_diff per horizon.
Build status (2026-10-03): CUL-386 created. Worktree .claude/worktrees/e068s1, branch feat/cul-386-claim-tests (not pushed): 53705062 specs pre-registered; 9d0f595f tool + 48 tests, 17/17 mutations killed.
STOPPED before the re-grade -- Opus review blocker, reproduced (/tmp/probe/p1.py, random walks, no real effect, share of p<0.05, target 0.05):
  daily Donchian-like, 6x120: continuation 0.00-0.01; reversal 0.10-0.12. Shifts restricted to avoid overlap: 0.06-0.09.
  hourly momentum-like rank_ic, 6x600: greater 0.00, less 0.33. Restricted: 0.10 / 0.13.
  Cause: the forecast is built from past prices; a backward shift pairs a bar with a forecast that already contains that bar's future. Even restricted, the null is too narrow (few independent shifts).
  Waiting for an operator decision on the significance method. Review should-fixes queued: validate the combine/across_variants/source_run keys; warn when n_placebo < n_resamples; min_blocks is only meaningful for dense selectors; "p >= alpha -> refuted" rule (kept as pre-registered unless the operator says otherwise).
Slice 1 status (2026-10-03, end of session): PR #315 OPEN (branch feat/cul-386-claim-tests, worktree .claude/worktrees/e068s1, no venv junction). run_065 NOT graded -- no method passed the calibration gate (A8.5.1a: 100% no answer; chunk permutation: 4/8 rows at 0.022). Waiting for operator decision on the method (REGRADE_run065.md open question 1). run_066 -> CUL-387. CUL-386 In Review.
Amendment 4 (2026-10-03): A8.5.1a with a 2-day gap FAILED the gate for Donchian(20) and (14) (opposite direction up to 0.125). run_065 stays ungraded; method search STOPPED (operator). PR #316 open (worktree .claude/worktrees/e068a4, no venv junction). Next: E-068 slice 2 (step 1a writes the claim card) -- operator starts it separately. Old worktree .claude/worktrees/e068s1 (PR #315 merged) can be removed.

## E-068 slice 2 -- step 1a writes the claim block (CUL-389), 2026-10-03
Worktree .claude/worktrees/e068s2, branch feat/e068-s2-claim-card (from origin/master 39e274e5). Phase A done, WAITING FOR NOD.
- [ ] Flag orchestrator.claim_tests.enabled (config + register; requires config_direct_authoring)
- [ ] Schema: optional `claim` block in hypothesis_card.schema.json
- [ ] 1a input CLAIM_TESTS.md (slot menu), added to 1a's inputs only when the flag is on; SKILL section keyed on its presence; 1b SKILL note
- [ ] tools/claim_card.py: check_claim (wraps claim_tests.check_spec), match_check (test vs manifest)
- [ ] run_loop: check after 1a, one in-place retry, test:none -> park kind "test" + test_requests.yaml
- [ ] match warning after 1b -> artifacts/claim_match.yaml
- [ ] tests, mutation check, Opus review, PR
Decisions pending: D1-D7 in the phase-A message.
Slice 2 status (2026-10-03, end of session): PR #319 OPEN (branch feat/e068-s2-claim-card, worktree .claude/worktrees/e068s2, no venv junction). Phase A approved (D1-D7, D3 changed: regime claims effect-size only). Added on operator request: power warning (bars / longest horizon x coins vs min_events; one shared 1a retry, then a warning). 93 targeted tests; mutations 37/37; two Opus review rounds, all should-fixes fixed. CUL-389 In Review; follow-ups CUL-391 (regime significance method), CUL-392 (split siblings skip 1b). Next: gh pr checks 319.

## E-068 slice 3 (CUL-393): grade the claim tests after the backtests -- PHASE A, waiting for the operator's nod
Worktree ../tb-e068s3, branch feat/e068-s3-claim-grading (from origin/master d3dca283). No code yet.
Measured (run_065 saved bars, worktree code): vectorized B grade 2.5-4.9 s per test x variant at N=1000, 0.5-2.6 s at N=199,
effect sizes only 0.01 s; real AdvancedStrategy replay reproduces base's saved forecast to 5e-7, 2.35 ms/bar (0.28 s per 121-bar window).
- [ ] D1 store: strategy-research/calibrations/claim_tests/<key>.yaml (committed); key = method, n_resamples, alpha, signal, cadence, layout, full test shape (selector, outcome kind, horizons, baseline, statistic); probe re-run for staleness; requests -> campaign_record/calibration_requests.yaml; offline runner only
- [ ] D2 signals: no new recomputable signal in slice 3; replay oracle + bounded-buffer fast path = follow-up (CUL-387)
- [ ] D3 budget: grading_budget_seconds (proposed 600), deadline checked inside the resample loop -> verdict_pending: budget_exceeded
- [ ] D4 seam: run_loop after protocol_execution, beside profit bars (RPR:16936), own never-raise wrapper; NOT a grid input
- [ ] D5 flag: reuse orchestrator.claim_tests.enabled (+ grading_budget_seconds); flag-off = nothing
- [ ] D6 N fakes: in-run N=1000 (spec_hash unchanged) + one new offline Donchian(20) gate at N=1000 (amendment 6), or N=199
- [ ] amendment 6 -> code -> tests -> mutation -> Opus review -> PR -> CI green Ubuntu+Windows
SCOPE SPLIT (operator 2026-10-04): slice 3 = effect sizes only ("measured, not proven"); automatic verdicts parked in CUL-394 (design + measurements there). D1-D6 above are superseded by that split.
- [x] claim_measure.py + run_loop seam + clear at entry + coverage/summary; calibration_for compares outcome kind, exact selector(s), number of fakes; REGRADE note; proposal §3/§8; D-067
- [x] tests (50 new), mutation 35/35, Opus review x2 (all fixed), PR #320
- [x] CI green Ubuntu + Windows on PR #320 (4 checks pass)

## E-068 validation on real runs (2026-10-04) -- STOPPED after (a); report in strategy-research/engineering/roadmap/E-068/VALIDATION_RUN.md
- [x] (a) 1a writes a valid claim card (run_070) -- but its tests read price level, not the claimed move (CUL-397)
- [ ] (b) claim measured after the backtests -- not reached (run_070 parked at 1b, O-21)
- [ ] (c) readers stop inventing components/settings -- not reached
- [x] CUL-395 fixed (PR #321 merged)
- [ ] waiting for operator: fixes (a) parser blank line, (b) CUL-396, (c) retry gets its own first answer, (d) CUL-398; O-21 call (zscore form vs new ATR component)
- [ ] docs PR from master: VALIDATION_RUN.md + O-20/O-21

## E-068 follow-up (operator decisions 2026-10-04) -- no campaign runs until step 4
- [ ] PR 1 docs: VALIDATION_RUN.md + O-20/O-21 (from master, worktree)
- [ ] PR 2 robustness (one PR): parser blank lines before fence (run_069 fixture); CUL-396 one audit key per retry; retries get their own first answer ("change only the layout, keep the content") + fix the "Missing: hypothesis_card.yaml" message vs multi-card rule; CUL-398 blocked_on_* R2 request = outstanding, R2 never queues ready past a hold. Tests, mutation, Opus review, CI Ubuntu+Windows.
- [ ] PR 3 phase A (STOP for nod): O-20 two consecutive independent "exhausted" answers to close a brief; O-21 zscore accepted + 1b must show no combination expresses the idea and name what it tried (no ATR component); CUL-397 slots check for "large 1h move" -> else bar-t past-return selector field (lookahead test) + CLAIM_TESTS.md "tests: none + missing_block, never approximate" + test-vs-claim review call (warning, one revision, never stops).
- [ ] Step 4 (operator go, after 3 PRs merged): --unpark E068_hourly_shock_reversal_kraken_perp, --resume --once; update VALIDATION_RUN.md for (b), (c).
- Held entries stay held. Slices 4-5 wait for (b), (c).

## PR 3a (operator answers 2026-10-04) -- build now; then the run; then PR 3b
- [ ] (i) #323 follow-up: blocked_on_component:<name> (automatic R9 quarantine) stays outstanding but does NOT freeze the brief; only operator holds (any other blocked_on_*) freeze it
- [ ] (ii) #323 follow-up: retry text says "the answer above was truncated" when cut at 60k; neutral wording when no answer is attached
- [ ] O-20: two consecutive independent "exhausted" answers close a brief; close reason names the rule (two exhausted answers vs empty-R2 streak); one answer recorded, brief stays open
- [ ] O-21: 1b SKILL rule (transforms are part of every combination; yardstick change = DEVIATION); `tried:` required on component_gap; missing tried or no transform combination named -> one 1b retry with that message, then accept; warning recorded if still missing; check COMPONENT_CATALOG.md PriceEvolution wording ("lagged"?)
- [ ] tests, mutation, Opus review, CI green Ubuntu+Windows; PR from master (after #323 merges)
- [ ] after merge + go: merge master into c4/flag-set, --unpark E068_hourly_shock_reversal_kraken_perp, --resume --once; update VALIDATION_RUN.md
- [ ] PR 3b after the run: past_return + lookahead tests; CLAIM_TESTS.md never approximate; review call off/record/revise (default off), measured offline on run_067/run_070 first
- [x] PR 3a merged (#324); run_070 completed_refuted with goals (a), (b), (c) shown with caveats; report PR #325 (docs)
- [ ] PR 3b: past_return + lookahead tests; CLAIM_TESTS.md never approximate; review call off/record/revise (default off), measured offline on run_067/run_070 first; also consider: flag claims whose tests ignore the block's output (run_070 base == design variant), and a catalogue check of free-text *Component names in reader proposals
- [ ] operator: S3b per-brief R2 cap for quarantined requests (declared trade-off in D-069)

## E-068 PR 3b -- PHASE A (2026-10-04), waiting for the operator's nod
Commit order (one PR from master; tests, mutation, Opus review, CI both OSes):
- [ ] 1. past_return selector field (claim_tests.py BAR_T_FIELDS :127, sel_event :429, sel_quantile :473, _check_selector :712): strict "all n bars present", timestamp-matched, NaN first n bars / gaps; lookahead + window + gap tests; CLAIM_TESTS.md rows + sync test
- [ ] 2. CLAIM_TESTS.md: never approximate (tests: none + missing_block); "at least one test must read the block's output" up front (prefer rank_ic or a forecast quantile)
- [ ] 3. claim_card.block_visibility (ANY test reads forecast/regime per manifest kind) -> warning in claim_match.yaml
- [ ] 4. claim-revision small call after 1b (new flag-on skill; re-emits `claim` only; statement+kind locked; check_claim + power check; splice into card + split twin, never queued copies; state key claim_revision written before the call; audit key claim_revision_attempt_0; budget pre-check; never raises; artifacts/claim_revision.yaml)
- [ ] 5. orchestrator.claim_test_review {enabled: false, mode: record|revise}; review call after 1b; artifacts/claim_review.yaml; revise shares the ONE revision with (3); DESIGN_PROPOSAL gate->revise
- [ ] 6. offline review measurement script on run_067 (2 cards) + run_070 (~$0.30, needs go)
- [ ] 7. reader free-text *Component name warning (reader_proposals + decide_next candidate `warnings`, schema)
- [ ] 8. S3b cap: 3 component-quarantined requests (owner counts; reset by reopen marker) -> R2 stops asking; quarantine_capped_briefs + stop line
Follow-up PR: operator approval mode (status blocked_on_operator_approval, --approve <id>, orchestrator.operator_approval.enabled default off), new Linear ticket under E-068.
Budget measured (run_070): 1,212,255 weighted (80.8% of 1.5M); clean 1,044,415. PR 3b adds <= ~45k (estimate). 30% headroom: 1.80M on a run like run_070, 1.55M on a clean one.

## E-068 slice 4 -- built (2026-10-05): PR #328, CUL-402; phase A answered (a)-(d) yes
- [x] 1. tools/claim_findings.py (pure): build_finding(run_dir, run_id, entry) + findings_summary(memory_doc, run_id)
- [x] 2. regroup_record wiring (run_phase1_research.py ~7795, after KB write, before upsert_memory): flag on -> entry["finding"]; never raises (error recorded in the finding)
- [x] 3. after upsert: artifacts/findings_summary.yaml (deterministic; error logged, run continues)
- [x] 4. campaign_memory.schema.json: optional `finding` on entry (fault entries unchanged)
- [x] 5. tests: flag-off byte identity; never stops; record shape; summary from run_070 fixture (holdout key stripped); no supported/refuted in code-written strings
- [x] 6. DESIGN_PROPOSAL §5/§8 aligned (flag = claim_tests; no claim_status supported/refuted); DECISION_LOG row; FLAG register note
- [ ] 7. mutation check, Opus review, PR from master in worktree, CI both OSes; Linear story under E-068; SESSION_LOG

## E-068 slice 5 -- readers v3 (2026-10-05) -- BUILT, PR #329 (CUL-403), CI green, waiting for operator merge
Worktree ../tb-s5, branch feat/e068-slice5-readers-v3 from master 4a6185b7. No campaign run.
- [x] D1-D6 answered (all as recommended; D3: no offline A/B) + additions 1-3 (no verdict, skips visible, blind pure findings allowed)
- [x] flag orchestrator.reader_findings.enabled (off; needs claim_tests + specialist_readers) + register + campaign_config key
- [x] reader_proposals: v3 mapping loader next to v2 list loader; V3 rubric dict
- [x] tools/reader_findings.py: skip rules, claim_result_digest, reader summary (prior runs only, compact, 10 rows), side-finding review, skip record + summary lines
- [x] run_phase1: handoff v3 inputs, skip rules, v3 validation (check_claim, resolve_patch, scaffolding), salvage, test requests, warnings
- [x] decide_next: side_finding candidate + brief candidate.claim; warnings; decision_record schema
- [x] 1a: PREFILLED_CLAIM.md (flag-on input) + claim_prefill.yaml warning
- [x] 5 short v3 SKILLs + READING_CONTRACT.md; rubric pin test
- [x] tests 109; mutation 30/30; Opus review x2 (round 1: schema + 3 should-fixes applied; round 2: confirmed, 1 trade-off documented)
- [x] docs: DESIGN_PROPOSAL s6/s8, D-073, USER_GUIDE, flag register; Linear CUL-403; PR #329
- [x] CI Ubuntu + Windows green on 9df87503 (first run failed: flag missing from run_campaign._flag_readers; fixed)
- [ ] after merge: remove ../tb-s5 (check reparse points first), ../tb-s5-mutate.py, ../tb-s5-pr-body.md; merge origin/master into c4/flag-set; CUL-403 Done

## E-068 final validation run (2026-10-05) -- Phase A, waiting for the operator's nod
- [x] Step 0: reader-input OSError never stops the readers -- PR #330 (worktree ../tb-s0), 2 review rounds, 18/18 mutations; CI pending; operator merges
- [x] Step 1: tb-s5 + temp files removed (no reparse points; tb-s4/3b/4/docs2 already gone); CUL-402/403 already Done; origin/master merged into c4/flag-set (b39bb4e7); claim_tests, reader_findings, operator_approval on (+ register)
- [x] After #330 merged: master merged into c4/flag-set (54356e88), flags checked
- [x] (done; plus all 8 blocked_on_e068 converted) Release E068_hourly_shock_reversal_kraken_perp__more_1: relabel blocked_on_e068 -> blocked_on_operator_approval (no campaign running), then `run_campaign.py --approve`
- [x] (run_071 parked at 1b; fallback run_072 failed at pass-through check) `run_campaign.py --once` in background, absolute log path; progress from runs/run_071/pipeline_state.yaml every few minutes; no code fixes during the run
- [x] Append "Final run" (a)-(g) to E-068/VALIDATION_RUN.md; tickets for bugs; SESSION_LOG.md

## (3) 1b builds the nearest version instead of parking -- Phase A delivered 2026-10-05, waiting for the operator's nod
- [ ] Q1 flag: new orchestrator.nearest_build (off; requires config_direct_authoring) vs behind config_direct_authoring
- [ ] Q2 structured `deviations` in decision.yaml (recommended) vs parsing DEVIATION: text only
- [ ] Q3 deviation component-request rows excluded from --unpark and the quarantine cap
- [ ] Build after the nod: flag-on 1b note, deviations.yaml, component_requests rows (kind: deviation), core_lost rule + one retry, finding + reader digest carry deviations, claim_match context, tests, mutation, review, CI
