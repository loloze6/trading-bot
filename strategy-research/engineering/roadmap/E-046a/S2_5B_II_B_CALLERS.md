# E-046a Slice 5b-ii-B — readers of `verdict_interpretation.yaml` under `orchestrator.specialist_readers.enabled`

Under the flag `verdict_interpreter` is never reached (bypassed, not deleted), so
`artifacts/verdict_interpretation.yaml` is never written. The only routes a
flag-on run can take after `protocol_execution` are:
`specialist_readers` → promote (→ `holdout_evaluation`), kill/terminate
(`completed_rejected`), or `human_pause` (`component_execution_error` /
`inconclusive_grid`). `campaign_review` is not reachable (only
`determine_post_verdict_route` routes there).

Classification:
- **(a)** not reached under the flag;
- **(b)** reached, re-pointed to `idea_status.yaml` / `grid_evaluation.yaml` /
  proposals / `protocol_result.yaml` / `hypothesis_card.yaml`;
- **(c)** reached, left as is with a `# legacy routing (v26 card G) -- retired in
  slice 6c` comment.

## Re-verification of the S1 count

`S1_FINDINGS.md` §1 counts 16 locations. Re-grepped on this branch
(`grep -n verdict_interpretation` over `workflow/*.py` and `tools/*.py`, then call
sites of each function): the same 16 still exist, no new ones. The three tools S1
could not check (`lint_verdict_provenance.py`, `record_schema.py`,
`verdict_criteria_evaluator.py`) have **0** literal hits. `campaign-review/SKILL.md`
has **0** hits (its required inputs do not list the file). Comment-only or
non-reader hits, excluded as before: `anti_adjacency_gate.py:221` (comment),
`killed_run_gate.py:270` (writes a synthetic file in a test fixture),
`run_campaign.py:892`/`:1381` (comments). Line numbers below are this branch's.

## Table

| # | Caller (file:def) | Reads at | Class | Decision under the flag |
|---|---|---|---|---|
| 1 | `_verify_verdict_outputs` (`run_phase1_research.py:6041`) | `:6058` | a | Only caller is `determine_post_verdict_route` (`:7393`), which is unreached. |
| 2 | `_write_promotion_audit` (`:6253`) | `:6302` | **b** | Reached on `validated` → promote. It only needed `hypothesis_id`; re-pointed to `hypothesis_card.yaml` via `_idea_hypothesis_id` (the old stage only restated that field). Raises if absent — no fallback to `run_id`, which would let one idea spend the single-use holdout twice. |
| 3 | `_route_holdout_evaluation` (`:6804`) | `:6831` | **b** | Reached after promote. Its fallback read (used only when `promotion_audit.yaml` is missing) re-pointed to the same `_idea_hypothesis_id`. |
| 4 | `determine_post_verdict_route` (`:7250`) | `:7251` | a | Called only from run_loop's `verdict_interpreter` branch. Replaced under the flag by `determine_post_specialist_readers_route`. |
| 5 | `determine_post_campaign_review_route` (`:7421`) | `:7470`, `:7560` | a | `campaign_review` is unreachable under the flag. |
| 6 | `run_loop` (`:7845`) | `:7994`/`:8000` (skip probe), `:8353` (load) | a | Both inside `verdict_interpreter` branches, which are unreached. New guard: a run whose `pending_stage` is already `verdict_interpreter` when the flag is on fails loudly instead of invoking it. |
| 7 | `_extract_run_numbers` (`run_campaign.py:1471`) | `:1499` | **b** | Reached every transition (log line only), but guarded by `exists()`. Under the flag the log line also shows `idea_status` from `idea_status.yaml`. Flag off: unchanged. |
| 8 | `_route_pivot` (`:5270`) | dict | a | Reached only via `lineage_routing == "pivot"`; under the flag `lineage_routing` ∈ {`None`, `terminate`}. |
| 9 | `_auto_generate_findings_carryover` (`:5956`) | dict | a | Called from `determine_post_verdict_route` (`:7384`) and run_loop's `verdict_interpreter` branch (`:8354`) only. |
| 10 | `_write_kb_findings_entry` (`:5803`) | dict | a | Called from `determine_post_verdict_route` (`:7387`) only, and there only on non-terminal routes — flag-off promote and kill/terminate already skip it, so the flag-on routes lose nothing relative to flag-off. |
| 11 | `_resolve_verdict_fields` (`:7057`) | dict | **b** | Reached: the flag-on route calls it with `pre_eval = idea_status.yaml` (same shape as a binding `pass_rule_evaluation.yaml`) and `interp = {}`. For `validated`/`refuted` (`result` PASS/FAIL) it returns the mechanical pair before touching `interp`; `original_status == breaker_status` so no breaker override. `inconclusive` never reaches it (paused first). |
| 12 | `_check_pass_rule_evaluation_conformance` (`:7124`) | none (message text only) | a | Called from `determine_post_verdict_route` / campaign-review route only. |
| 13 | `_check_kb_reactivation_conformance` (`:4883`) | dict | a | Callers are `_route_refine`, `_route_pivot`, `determine_post_campaign_review_route` — all unreached. |
| 14 | `_inject_regime_context_into_handoff` (`:3917`) | writes the old stage's handoff | a | Called only in the `verdict_interpreter` branch (`:8019`). The readers take no regime context by design (each SKILL.md scopes a reader to its report + the grid). The retune firewall that ran beside it now runs before the `regime_power` reader. |
| 15 | `_create_remaining_handoffs` (`:3754`) | lists it as a deliverable | **c** | Reached (backtest_specification). Still writes `protocol_to_verdict_interpreter.yaml`, inert under the flag, like the data-availability handoff when that gate is off. Comment added. |
| 16 | `tools/near_miss_scoreboard.py` | `:408` | a | Standalone tool, not called by the run loop. Flag-on runs read as "no verdict_interpretation.yaml" (like the 21 early runs it already handles). Wiring it to the grid/proposals is slice 6a (`regroup_record` calls `build_scoreboard`). |

**Totals: (a) 11, (b) 4, (c) 1.**

### Reached under the flag, taking the `interp` dict, not in S1's 16

| Caller | Class | Decision |
|---|---|---|
| `_dispatch_verdict_route` (`:7166`) | b | Called with the grid's pair and `interp = {}`. The promote branch never reads `interp`; terminate hands it to `_route_kill`. |
| `_route_kill` (`:5415`) | c | Reads `interp.get("hypothesis_family", "")` for `altitude_history`; gets `""`. `hypothesis_family` is retired (card G / slice 6c) and deliberately not fed. Comment added. |

## Narrative fields not re-created

`root_cause`, `altitude_justification`, `findings_carryover`, `proposed_brief`,
`primary_failure_mode`, `hypothesis_family`, `proposed_change_dimension` — none
are produced under the flag. No caller reached under the flag needs them.

## Questions for the operator (not blocking — nothing reached needs an answer)

1. **Asset-stability gate (E-026).** Before `promote`, the old stage checked
   (in its prompt, not in code) that ≥2 `coin_universe.yaml` categories were
   tested. Under the flag the grid alone decides `validated`. The target covers
   this through the asset variant (slice 3: base + design patch + asset patch) and
   the grid's unanimity across variants; until slice 4's variants run, a
   single-variant grid can be `validated` on one symbol. Promote still stops at
   `holdout_evaluation`'s human pause, so nothing irreversible happens
   automatically. Confirm this is acceptable for the interim, or add a
   pre-registered asset-breadth criterion to the menu.
2. **KB entries for killed ideas.** Neither flag-off (kill/terminate short-circuits)
   nor flag-on writes a KB entry for a killed idea. Slice 6a's `regroup_record`
   is where the new memory writer lands; no change here.
