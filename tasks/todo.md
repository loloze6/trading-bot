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
