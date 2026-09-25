# E-059 S1 — Retire verdict routing; runbook; parked states (delivery_plan_v26.md slice 6c): characterize-and-stop

Read-only characterization at `56734b65` (master). No code, config or backtest was changed, and
the holdout was not opened. Line numbers come from that commit. They were re-grepped for this
document with Git Bash `grep -n` and read directly; use the function names as the stable
reference. Counts over state files were taken with system `python` 3.13.2. The only thing
executed was pytest on existing test files (§9).

Inputs read:
- `delivery_plan_v26.md`: slice 6c (L375-399), the "10 · decide next" and "runbook" rows
  (L67, L71), the cross-cutting promotion-block row (L473), and the E-059 artifact row (L501);
- `engineering_roadmap.html`: cards G, J, L, M and steps 8, 10-12 (text extracted locally);
- `E-046a/S2_5B_II_B_CALLERS.md` (the 16-caller table);
- `E-058/S1_FINDINGS.md` and its decision;
- `E-059/S1_FINDINGS_6B.md` and its decision, and `E-059/S2A_QUESTIONS.md`;
- `docs/RUNBOOK.md` §3/§4.

---

## Guesses for the operator (read this first)

Each item is a real choice that the target design does not already make. The recommendation is
what S2 builds if you say nothing. **Only guess 1 blocks anything, and it blocks only sub-slice
S2d.** S2a-S2c can be built overnight on the defaults below.

1. **How a validated idea reaches the holdout once routing is retired. — BLOCKS THE BUILD of S2d
   only. S2a-S2c are safe: under the flag nothing reaches the holdout gate at all.**
   Today a validated idea goes promote → `_write_promotion_audit` → `holdout_evaluation`
   (`_dispatch_verdict_route` L8596-8647). Retiring routing removes that path, so under the flag
   **no code path leads to `holdout_evaluation`**. The target says the holdout "happens once, by
   hand, on purpose", after the profit-bars stop (steps 8/12, card L), and resuming afterwards
   "re-enters Step 10". It does not say how you tell the loop "spend it now", or whether the
   existing mechanical guards (one spend per `hypothesis_id`, the tradability hold, the
   consumed-marker write in `_route_holdout_evaluation` L8192-8366) still run.
   *Recommendation:* an explicit operator file on the stopped run,
   `artifacts/holdout_decision.yaml {decision: spend|continue, decided_by, decided_at}`. On
   `--resume`, `spend` routes to the existing, unchanged `holdout_evaluation` stage, so every
   guard runs and the backtest is still done by hand. The stage is **refused mechanically**
   unless this run's `profit_bars_evaluation.yaml` is PASS **and** `idea_status` is `validated`.
   RUNBOOK row `profit_bars_reached` (a2) already says never to spend on a refuted or
   inconclusive idea, and this turns that sentence into code. If the file is absent or says
   `continue`, the run ends `completed_validated` and decide-next runs.
   *Alternative:* fully manual (RUNBOOK only, no code). This loses the mechanical single-use
   check, because `holdout_consumed_by` would be edited by hand.

2. **Inconclusive ideas stop pausing the loop. — default is safe to build on.**
   Today `inconclusive` pauses (`inconclusive_grid`, L3166-3171). The plan says the route returns
   `completed_<idea_status>`. The target lists inconclusive among "idea parked, loop continues"
   and says it "never counts as an attempt" (card G, card L).
   *Recommendation:* `completed_inconclusive` → the queue entry is `done` with
   `outcome: inconclusive` (already admissible, `_NON_VERDICT_OUTCOMES` L111) → decide-next runs.
   The target's rule "inconclusive twice for data reasons → park" is **deferred**: once routing is
   retired nothing re-runs an idea automatically, so a second inconclusive run of the same
   `hypothesis_id` cannot happen. Trial rows are unchanged: the backtest touched data, so it still
   counts in N.

3. **What triggers campaign review. — default is safe to build on.**
   "Triggered as today" does not work literally. `_should_trigger_campaign_review` (L6969-6992)
   fires on ≥2 distinct `failed_families` **or** every 6th entry of `campaign_state.runs`. The live
   state holds **9 distinct failed families** (measured), so the family trigger is permanently
   true, and review would fire after every run. That list is also retired, so it never changes
   again.
   *Recommendation:* drop the family trigger under the flag. Trigger instead on every
   `review_every_n_runs` (6, `campaign_state.yaml`) entries in `campaign_memory.yaml` that have no
   `engineering_fault`. The memory is the complete per-run list under these flags; the
   `campaign_state.runs` list is not (E-058 note at L3666).

4. **What campaign review's `continue` / `escalate_*` do under the flag. — default is safe to
   build on.**
   *Recommendation:* all three are logged as `campaign_review: <rec> recorded, not routed (v26
   card G)` and then route like the run's own idea status. For `escalate_component`, the rationale
   is also appended to `campaign_record/component_requests.yaml` as
   `{run_id, stage: campaign_review, variant_id: null, reason}`, so the operator sees it where
   card J says to look. A `next_research_question` on a `continue` is ignored. Today the route
   treats it as a reframe (L8863-8876), which the skill itself calls a bug (SKILL.md L209-211).

5. **`terminate` must actually stop the loop. — default is safe to build on.**
   Today terminate writes `campaign_decision.yaml` and `campaign_state.status: space_empty`
   (L6248-6277), but **nothing reads `space_empty`**: a grep over `workflow/` and `tools/` finds
   only writers. The run ends `completed_rejected` and the queue carries on. Card L says "campaign
   review says stop" is a loop stop.
   *Recommendation:* under the flag, terminate writes the same decision file with the retired
   fields (`families_tried`, `altitude_justification`) dropped and `runs_attempted` taken from
   memory. It then pauses with a new flag `campaign_review_terminate`, which gets a new
   `_classify_human_pause` row and a RUNBOOK §3 row. After a resume, the run ends
   `completed_<idea_status>` and decide-next runs.

6. **Where a reframe goes. — default is safe to build on.**
   *Recommendation:* the route writes
   `campaign_record/candidate_briefs/<run_id>__reframe.md` (frontmatter brief) from
   `next_research_question`. Missing required keys (`_parse_brief_frontmatter` L235-271) are filled
   from the source run's `research_brief.yaml`; if a key still cannot be filled, the run stops
   loudly rather than silently dropping the brief. The orchestrator cannot import `run_campaign`
   (circular import, 6B S1 §6), so `process_once`'s DONE branch registers the brief through
   `register_hypothesis(..., source="agent", relation=None, extra={origin: campaign_review})`,
   with `status: ready` and priority 999, **before** decide-next runs. It therefore runs next
   unless an operator entry is ready, which matches decision 4 of 6b. The existing A5.4 KB-reactivation check
   (L8842-8858) and the wishlist check (`_hard_pause_reason` L1056-1075) stay in front of it.

7. **What counts as "parkable". — default is safe to build on.**
   Component requests today carry no class name, and three of their four reasons are design
   errors, not missing components: "patch application failed", "manifest paths unresolved", and
   "validate_config.py violations" with the report text (L2001-2039). A missing class surfaces
   only as `V12 ... cannot load` inside the validator report (`trading-bot/tools/validate_config.py:326`).
   *Recommendation:*
   - **waiting_for_component** when 1b returns `component_gap` (L9092-9096), or when every
     not-tested variant's report cites V12.
   - **waiting_for_data** when the data gate says refine or decline (both the non-variant path
     L9718-9739 and the variant path L9693-9702), where the missing variants were data-gated.
   - A mix of the two parks as component; the data gate re-runs on unpark anyway.
   - Anything else (patch failure, manifest, other V-codes) stays the pause it is today, because
     it is a design error to fix, not a gap to wait on.
   - The non-variant data `decline`, which rejects today, parks under the flag, following card J.

8. **What `--unpark` does. — default is safe to build on.**
   *Recommendation:* `run_campaign.py --unpark <entry_id>`:
   - takes the campaign lock (the single-writer rule);
   - refuses unless the entry is `paused:waiting_for_*`;
   - in the component case, refuses while the named class still fails to load;
   - clears the run's parked marker and resets `status: active`;
   - sets the entry to `ready` with its priority kept, never `in_progress`, so there are never
     two active lineages.
   The **same run** then continues from the stage that parked it (`strategy_config_authoring`,
   `backtest_specification` or `data_availability_gate`). Parking always happens before any
   backtest, so no trial row exists yet and none is lost. This is a deliberate shortcut from the
   target's "an un-parked idea enters at 1a with pass-through": it saves a second 1a/1b spend on
   an idea whose card and config already exist.

9. **Parking versus E-030 quarantine. — default is safe to build on.**
   With `halt_policy.quarantine_enabled`, `component_gap` becomes `blocked_on_component:<name>`
   (L1180, L2332-2339). *Recommendation:* under the 6c flag the park branch runs first and
   supersedes it for parkable reasons. The quarantine code is untouched.

10. **"verdict_interpreter is deleted". — default is safe to build on.**
    Under the flag set, the stage is already unreached and guarded (L9420-9425). *Recommendation:*
    6c deletes no code. It stays for flag-off runs, like the legacy routing functions. Physical
    removal is a later cleanup, once the flags are permanently on.

11. **Per-protocol `promotion` blocks and `assert_promotion_ratified` stay. — default is safe to
    build on.**
    The plan retires them in 6c "only after the profit-bars file is the sole reader" (L473). It is
    not the sole reader: `tools/run_protocol.py:2214` reads `protocol["promotion"]` (a KeyError if
    absent) to build `per_symbol_summary` and the protocol's own verdict, on every backtest.
    *Recommendation:* out of 6c. File a separate ticket.

12. **Runs that are mid-flight when the flag is switched on. — default is safe to build on.**
    The live queue has no `ready` or `in_progress` entry (measured: 1 `blocked_on_…`, 4 `done`),
    so today this is theoretical. *Recommendation:* under the flag, a run that arrives in
    `process_once` at a legacy continuation stage (`completed_refined|reframed|escalated`) with a
    `continuation_child` halts loudly (`legacy_continuation_under_retired_routing`) and is not
    followed silently. A run already at `holdout_evaluation` proceeds, because that stage only
    applies guards and pauses.

13. **The RUNBOOK row named `queue_exhausted_with_open_briefs`. — default is safe to build on.**
    The row depends on 6b S2b's stop reasons (R2 and brief exhaustion), which are being built in
    parallel. *Recommendation:* the row covers decide-next's stop whenever parked entries or open
    briefs remain. It uses S2b's reason string verbatim once that lands, and the S2 doc check
    pins that string.

**Already answered by the target or forced by the code, so not asked:**
- An idea's status comes only from the grid, and decide-next alone picks what runs next.
- Refine, pivot, escalate, kill, the circuit breaker, `hypothesis_family`, `altitude_history` and
  continuation children are unreachable under the flag. None survives.
- Profit bars reached → pause for the operator (the existing stop, unchanged). Resuming
  re-enters Step 10.
- Card J: a component-missing proposal is never minted. decide-next already marks it INFEASIBLE
  and re-evaluates it on every call (`decide_next.py` L437-444).
- The plan's seam is stale (§1.1). The flag must require `profit_bars_every_backtest` (§7).

---

## 1. The routing table and its callers under the flag

### 1.1 The plan's seam does not exist under the prerequisite flags

The plan says "`determine_post_verdict_route` returns `completed_<idea_status>`". Under the
flags 6c depends on (decide_next → regroup_record → specialist_readers), that function is
**never called**:
- its only caller is run_loop's `verdict_interpreter` branch (L9828-9844);
- that stage is unreached under `specialist_readers`: `protocol_execution` is redirected at
  L9553-9554, and a run that is pending there raises at L9420-9425.

The live post-run seam is **run_loop's `regroup_record` branch, L9860-9876**. It runs
`_profit_bars_stop_route` (L8153) and then `determine_post_specialist_readers_route` (L3128). That
second function calls `_resolve_verdict_fields({}, "", "", pre_eval=idea)` (L3173), then
`_dispatch_verdict_route` (L3176), using the grid's legacy pair from `_GRID_IDEA_STATUS_ROUTING`
(L2377-2381). **6c's route goes there**, as a flag branch before L3173 (or as a sibling function
called from L9871).

### 1.2 Every caller, and its fate under `verdict_routing_retired`

Callers found by Git Bash `grep -rn --include=*.py` over `workflow/` and `tools/`. Comment and
docstring hits are omitted.

| Symbol (def) | Call sites | Fate under the flag |
|---|---|---|
| `_dispatch_verdict_route` (L8554) | L3176 (readers route), L8791, L8828 (verdict route), L8943 (campaign-review `continue`) | **Never called.** L3176 is bypassed by the new flag branch; the other three sit in unreached or short-circuited code (below). Legacy comment. |
| `determine_post_verdict_route` (L8660) | L9831 | Unreached (the verdict_interpreter guard). Legacy comment. |
| `_route_refine` (L6008) | L8654 | Unreached. Writes `continuation_child` at L6061. Legacy comment. |
| `_route_pivot` (L6065) | L8650 | Unreached. `continuation_child` at L6121. Legacy comment. |
| `_route_escalate` (L6125) | L8652, L8977 (campaign-review `escalate_*`) | Unreached; L8977 is short-circuited by guess 4. `continuation_child` at L6177, L6198. Legacy comment. |
| `_route_kill` (L6210) | L8657 | Unreached. Its flag branch (L6226-6238: append to `campaign_state.runs` and `diagnostics_log`) moves into the new route for every idea status, so nothing that reads `runs` regresses. Legacy `continuation_child=None` write at L6244. |
| `_apply_circuit_breaker` (L8381) | L8701, L8921 | Unreached (inside the verdict route and the campaign-review `continue` branch). Legacy comment. |
| `_create_escalation_protocol` (L5968) | L6150 | Unreached (only `_route_escalate`). Legacy comment. |
| `_create_timeframe_protocol` (L5991) | L6187 | Unreached. Legacy comment. |
| `_resolve_verdict_fields` (L8445) | L3173, L8752, L8922 | Not called on the flag path. Kept (flag-off readers route). |
| `_should_trigger_campaign_review` (L6969) | L8817 | Unreached. The flag uses a memory-count trigger instead (guess 3). |
| `determine_post_campaign_review_route` (L8831) | L9879 | **Reached again** (it is unreachable today under the readers flag). Needs a flag branch: reframe → brief file, terminate → pause, anything else → no route (guesses 4-6). The `continue`/`escalate_*` branches read `verdict_interpretation.yaml` (L8880, L8970) and **must return before that load** (§3). |
| `_route_campaign_terminate` (L6248) | L8991 | Reached through terminate. Flag variant per guess 5. |
| `_LEGACY_STATUS_TO_VERDICT_ROUTING` (L8427) | only inside `_resolve_verdict_fields` and `_verify_verdict_outputs` | Not read on the flag path. |

### 1.3 Every path that sets `continuation_child`

Writers: `_route_refine` L6061, `_route_pivot` L6121, `_route_escalate` L6177 and L6198, and
`_route_kill` L6244 (the value `None`). No other writer exists (grep over `workflow/`, `tools/`).
Readers: `run_campaign._existing_continuation_child` (L511-520, used by the `refinement_brief`
action at L2217), the continuation branch of `process_once` (L2410-2425), and
`campaign_memory.RETIRED_FIELDS` (`tools/campaign_memory.py:88`, a refusal list). Under the flag
every writer is unreachable (table above), so the continuation branch can never fire for a
flag-on run. 6c adds the guess-12 guard for legacy runs and a test that asserts the key is absent.

## 2. Pause paths under the full flag set, and which survive

Flag set assumed: grid_evaluation, category_reports, specialist_readers, regroup_record,
config_direct_authoring, decide_next, profit_bars_file, profit_bars_every_backtest, and the data
gate (on by default). variant_loop may be on or off.

| Pause | Origin (file:line) | Under 6c |
|---|---|---|
| `component_gap` at 1b | `determine_post_strategy_config_authoring_route` L9092-9096 → classifier L1016-1020 | **Parks** as `waiting_for_component` (guess 7) |
| No validated variant at 5a (config-direct) | L9187-9204, no flag → `human_pause_unclassified` | **Parks** if every not-tested variant reports V12; otherwise stays a pause (design error) |
| Data gate `refine` (non-variant) | L9718-9733, no flag | **Parks** as `waiting_for_data` |
| Data gate `decline` (non-variant) | L9734-9739 → `completed_rejected` | **Parks** as `waiting_for_data` (guess 7) |
| `variant_gate_insufficient` (<3 variants) | L9693-9702, classifier L978-979 | **Parks** (data, or component if the missing variants are V12) |
| Block manifest invalid twice | L9037-9040 raises → `unhandled_exception` | Survives (engineering halt) |
| `conformance_gate_failure` | L9789-9793, L9817-9826 | Survives (integrity halt) |
| `component_execution_error` | L3153-3161 | Survives (engineering halt; E-030 quarantine applies as today) |
| `profit_bars_reached` | `_profit_bars_stop_route` L8153-8189 | **Survives, unchanged.** Resume → `completed_<idea_status>` → decide-next; the spend path is guess 1 |
| `inconclusive_grid` | L3166-3171 | **Retired under the flag** (guess 2) |
| Holdout pauses (`provisional_promote_*`, `research_only_unverified`) | L8276-8344 | Reachable only through the guess-1 spend path |
| `campaign_review_terminate` | new | **New loop stop** (guess 5) |
| `wishlist_trigger[_data_gap]` | `_hard_pause_reason` L1056-1075 | Survives (reframe guard) |
| `kb_reactivation_violation` | L8842-8858 | Survives (reframe guard); its refine and pivot sites are unreachable |
| `budget_breaker`, `unhandled_exception`, `stale_escalation_unclaimed` | L1042-1054 | Survive |
| `regime_misattribution`, `pass_rule_evaluation_disagreement`, `new_component_escalation`, `data_block_hitl`, `refinement_brief_conflicts…` | set only on the verdict route, `_route_escalate`, the validation stage, or legacy lineage | Unreachable under the flag (their rows stay, marked flag-off) |
| decide-next `stop` (not a pause) | `run_campaign.py` L2548-2550 | Survives; the RUNBOOK row is widened (guess 13) |

## 3. Readers of `verdict_interpretation.yaml` under the full flag set (the 16 re-verified)

A fresh grep for `verdict_interpretation` over `workflow/*.py` and `tools/*.py`, with each
function's call sites followed, found the same 16 locations as `S2_5B_II_B_CALLERS.md` and no new
reader. Hits that are comments, docstrings, or a test fixture writer are excluded, as before
(`anti_adjacency_gate.py:221`, `grid_kb_writer.py:19`, `killed_run_gate.py:270`,
`run_campaign.py:933`/`:1426`). Non-code hits: the five reader SKILL.md files and
`proposal.schema.json` only *forbid* reading it, and `regime-auditor/SKILL.md:130` forbids
producing it. `campaign-review/SKILL.md` and its handoff template do not list it.

| # | Reader (current def line) | Status under the 6c flag |
|---|---|---|
| 1 | `_verify_verdict_outputs` (L6863) | unreached (only from the verdict route, L8803) |
| 2 | `_write_promotion_audit` (L7354) | **unreached** on the flag path (promote is gone); still re-pointed through `_idea_hypothesis_id` (L7383-7388) |
| 3 | `_route_holdout_evaluation` (L8192) | reached only through the guess-1 path; its reader branch (L8218-8221) is the flag-off else, and under the readers flag it uses `_idea_hypothesis_id` (L8213-8217) |
| 4 | `determine_post_verdict_route` (L8660) | unreached |
| 5 | `determine_post_campaign_review_route` (L8831) | **reached again under 6c.** The loads at L8880 (`continue`) and L8970 (`escalate_*`) must sit behind the flag branch. S2 test: a flag-on `continue` or `escalate_*` with no `verdict_interpretation.yaml` on disk must not raise |
| 6 | `run_loop` verdict_interpreter branches (L9461-9496, L9828-9831) | unreached (guard at L9420) |
| 7 | `run_campaign._extract_run_numbers` (L1516, read at L1544) | reached, guarded by `exists()`, log line only |
| 8 | `_route_pivot` (L6065) | unreached |
| 9 | `_auto_generate_findings_carryover` (L6778) | unreached (L8794, L9830) |
| 10 | `_write_kb_findings_entry` (L6613) | unreached (L8797); the grid KB writer (E-058 S2b) replaces it |
| 11 | `_resolve_verdict_fields` (L8445) | not called on the flag path |
| 12 | `_check_pass_rule_evaluation_conformance` (L8512) | unreached; its campaign-review call (L8933) sits inside the short-circuited `continue` branch |
| 13 | `_check_kb_reactivation_conformance` (L5678) | reached for reframe only (L8849); it reads the KB, not the interpretation |
| 14 | `_inject_regime_context_into_handoff` (L4712) | unreached (L9487) |
| 15 | `_create_remaining_handoffs` (L4549) | **reclassified (a):** its only call (L9651) is in the non-config-direct `backtest_specification` branch, and the 6c flag requires config_direct (through decide_next) |
| 16 | `tools/near_miss_scoreboard.py::build_row` (L550, read at L552) | reached through `regroup_record`'s rebuild, guarded by `exists()` |

**Conclusion (the independent confirmation the plan requires):** under the 6c flag set, no code
path loads `verdict_interpretation.yaml` unguarded, **on one condition**: row 5's two branches
return before their load. That condition is an S2a/S2b build item with its own test, not an open
question.

## 4. Promote and holdout under the flag

- **Today, under the prerequisite flags:** validated → `_dispatch_verdict_route` promote →
  `_write_promotion_audit` → a second profit-bars check is skipped when an every-backtest
  evaluation exists (L8623-8630) → `holdout_evaluation`. The stages run in this order: DSR
  (L8224-8227) → single use (L8230-8236) → research_only hold (L8274-8316) → pause for a manual
  backtest (L8338-8344) → consume marker (L8350-8352) → `completed_promoted|rejected`.
- **Under 6c:** validated → `completed_validated` → the DONE branch (`_apply_idea_status_outcome`
  already writes `outcome: validated` with the ref, L2464-2487) → decide-next. **Nothing routes to
  the holdout.** `promotion_audit.yaml` is not written. The DSR gate still exists, because
  `deflated_sharpe_threshold` is a profit bar graded on every backtest
  (`_evaluate_profit_bars_every_backtest` L8070-8137).
- **Combined with the stop:** the per-backtest profit-bars stop runs before the route
  (L9868-9869), whatever the idea status. It pauses with `profit_bars_reached` while
  `pending_stage` stays `regroup_record`. On `--resume`, the stop sees it was already raised
  (L8178-8181) and falls through to the 6c route, then to `completed_<idea_status>` and
  decide-next. That is exactly the target's "resume re-enters Step 10". Guess 1 is the only
  missing piece: an explicit spend path.
- **Consequence for the flag:** without `profit_bars_every_backtest`, a validated idea under 6c
  would never be graded against the bars, because the promote-path check lives inside
  `_dispatch_verdict_route`. So the flag must require it (§7).

## 5. Campaign review under the flag

- **Trigger:** guess 3, evaluated in the new route after the profit-bars stop and before
  `completed_<idea_status>`. It is not evaluated on engineering-fault runs (they pause first). A
  trigger sets `next_stage = "campaign_review"` in the same run, and the handoff is copied from
  the template as L8820-8825 does. The memory input is already added under `regroup_record`
  (`_apply_regroup_record_context` L3642-3680).
- **Outcomes:** `reframe` → the brief file plus `completed_<idea_status>`, then `process_once`
  registers it with `origin: campaign_review` (guess 6). `terminate` → a
  `campaign_review_terminate` pause (guess 5). `continue` and `escalate_*` → no route (guess 4).
  The skill receives a flag-gated context note listing these semantics, so the prompt is
  byte-identical with the flag off (the `_apply_*_context` pattern).
- **Retired inputs the skill still names:** SKILL.md L202 guards `terminate` on
  `instruments_tried ≥ 3 AND components_built ≥ 1`, which are escalation-era fields that no
  longer grow. Under the flag the context note replaces this with "cite the memory's
  `idea_status` counts". S2b changes only the flag-gated note, never the base SKILL text.
- `_B7_MANDATORY_INPUT_STAGES` (L2086-2089) includes `campaign_review`, so a triggered run needs
  `pre_registration.yaml` and `user_brief_verbatim.yaml`. Both are written by `_materialize_run`
  and 1a for every queue-launched run; an S2b test covers it.

## 6. Parked states

- **Where requests come from today:** `component_requests.yaml` is written by the config-direct
  5a tool stage (L2054-2061, reasons at L2001-2039) and `data_requests.yaml` by the per-variant
  data gate (L1329-1342). 1b's `component_gap` writes only `decision.yaml`. Neither request file
  has a resolved field or a class name (6B S1 §4.2).
- **Marker (orchestrator side, flag on):** at the parkable sites of §2, write
  `pipeline_state.parked = {kind: component|data, stage, reason, request_refs}` along with the
  existing `paused_for_human`. The plan says "no new pause rows". The marker is read by
  `process_once`, not by `_classify_human_pause`.
- **`process_once`:** a new branch **before** `_hard_pause_reason`'s quarantine logic (L2292).
  If the flag is on and `state.parked` exists:
  1. set the entry `status: paused:waiting_for_<kind>` (matches `_QUEUE_STATUS_RE`,
     `record_schema.py` L113) and `parked_reason` (the field already exists, L223-226);
  2. append a halt-history record;
  3. log `PARKED <entry> / <run>: <kind> — <reason>. Requests: <refs>. Unpark with --unpark <entry>.`;
  4. then call `_finish_lineage_with_decision` with the entry's parked status, so decide-next
     picks the next run.

  The last step is required. Without it a park followed by an empty `ready` set would return
  "Queue exhausted" (L2204-2206) without asking decide-next.
- **`resume_paused_entry` (L1450):** it takes `paused[0]` of every `paused:` entry (L1457-1461). A
  parked entry listed first would make `--resume` report "still stuck" and refuse the real pause.
  It **must skip `paused:waiting_for_*`**. This fix is required, not a question.
- **`--unpark <entry_id>`:** a new CLI flag beside `--resume` (L2694-2724), implemented per
  guess 8.
- **Visibility:** `_regenerate_summary` lists parked entries with their request refs (card J:
  "surfaced in the campaign summary"). Schedulability already reports `paused:*` as blocked with
  the blocker text (L1977-1990).

## 7. Flag design

- `orchestrator.verdict_routing_retired.enabled` in `config/campaign_config.yaml`, default `false`.
- Reader: `run_phase1_research._verdict_routing_retired_enabled()`, a strict bool (the
  `_decide_next_enabled` pattern, L3232-3275). It raises if on without:
  - **`decide_next`**, which itself requires regroup_record → specialist_readers → grid +
    reports, and config_direct_authoring. Only decide-next picks the next run once routing is
    gone.
  - **`profit_bars_every_backtest`**, which requires profit_bars_file. Without it, no profit-bar
    check runs on the flag path (§4).
- `variant_loop` is **not** required (6b does not require it); the park logic handles both shapes.
- Resolved once in run_loop's pre-flight next to `_rr_flag`/`_pbe_flag` (L9318-9340), and once
  per step in `process_once` next to `decide_next_enabled` (L2200).
- Register entry: `off_incomplete`, **declared behaviour change** (plan §0.2). `blocked_on` is the
  6b two-run proof plus this slice's own proof. Switching it on needs the before/after artifact
  diff recorded in the register.
- **Off:** stage graph, routes, `campaign_queue.yaml`, `campaign_log.md` and every artifact are
  byte-identical, and the K2/E-018/K4 tests stay green (§9).
- **On:** the route after `regroup_record` is
  1. component errors → pause (unchanged);
  2. the profit-bars stop (unchanged, plus the guess-1 spend branch in S2d);
  3. the campaign-review trigger;
  4. `completed_<validated|refuted|inconclusive>`.

  `_dispatch_verdict_route` is never called. Legacy functions carry
  `# legacy routing (v26 card G)`: two markers exist already (L4597, L6239), and the others are
  added to every row of §1.2.

## 8. Proposed S2 split

**S2a — route retirement (core):**
1. The flag, the config entry, and the register entry.
2. The flag branch in `determine_post_specialist_readers_route` (or a sibling at L9871): the
   `completed_<idea_status>` terminals, with `_route_kill`'s runs/diagnostics bookkeeping kept
   for every status.
3. run_loop step 6 writes `status: completed` for the three new terminals (today anything other
   than `completed_rejected` is written as `active`, L9902-9907). This is cosmetic but truthful.
4. Legacy comments on every §1.2 row.
5. The guess-12 guard in `process_once`, and the `continuation_child`-absent assertion.
6. RUNBOOK: the `profit_bars_reached` and `inconclusive_grid` rows gain their flag-on behaviour.
   USER_GUIDE §2.1/§2.2, CLAUDE.md stage notes, DOC_INDEX.

**S2b — campaign review under the flag** (guesses 3-6):
1. Memory-count trigger.
2. Flag branch in `determine_post_campaign_review_route` that returns before the L8880 and L8970
   loads.
3. Reframe brief writer, plus registration in the DONE branch.
4. Terminate pause, with its classifier row and `_PAUSE_FLAG_TO_REASON` entry (required by
   `test_every_known_sticky_flag_branch_has_a_pause_flag_to_reason_entry`).
5. Flag-gated skill context.
6. RUNBOOK row `campaign_review_terminate`.

**S2c — parked states** (guesses 7-9, 13):
1. The orchestrator `parked` marker at the §2 sites.
2. `process_once` park branch plus decide-next.
3. `resume_paused_entry` skips parked entries.
4. `--unpark`.
5. Summary listing.
6. RUNBOOK §4 parked-state procedure, the `queue_exhausted_with_open_briefs` row, and a
   `docs/HALT_RECOVERY.md` cross-reference.

**S2d — the holdout spend path** (guess 1). **Waits on the operator's answer.**
`holdout_decision.yaml` → the existing `holdout_evaluation`, mechanically refused unless profit
bars PASS and `validated`. RUNBOOK `profit_bars_reached` row (a1) is rewritten.

**Out of 6c:**
- promotion-block retirement (guess 11);
- physical deletion of the legacy code and of `verdict_interpreter` (guess 10);
- the flag-off DONE-branch provenance crash (6B guess 8, its own ticket).

## 9. Tests

**Legacy, must stay green with the flag off.** Ran them at `56734b65` with system python 3.13.2:
`python -m pytest tests/test_k2_verdict_machinery.py tests/test_e018_mechanical_routing.py
tests/test_k4_routing_registration.py tests/test_campaign_review_trigger.py
tests/test_holdout_research_only_gate.py tests/test_halt_quarantine_policy.py
tests/test_e059_s2a_decide_next.py tests/test_e058_s2a_regroup_record.py
tests/test_feature_flag_register.py` → **234 passed**. K2 has 28 test functions, E-018 6, and K4
14; K4 L129-194 pin the three `continuation_child` writers and cross-process continuation. Other
files that touch the retired symbols and must stay green flag-off (grep): `test_circuit_breaker_family_scoping.py`,
`test_kb_reactivation_gate.py`, `test_profit_bars_stop.py`, `test_resume_idempotency.py`,
`test_halt_history.py`, `test_fee_reduction_assessment.py`, `test_k3_protocol_pinning.py`,
`test_e046a_slice5b_ii_b_readers_stage.py`.

**New (all fixture-only; the `campaign_root` sandbox; `orch.run_loop` stubbed as in
`test_halt_quarantine_policy.py`):**

*Flag:*
- false when absent;
- a non-bool raises;
- on without decide_next raises, and on without profit_bars_every_backtest raises;
- the register entry is present.

*Flag off:* byte-identical queue, log and stage graph on the DONE, continuation and pause paths.

*Flag on, routing:*
- each idea status → `completed_<status>`;
- `_dispatch_verdict_route`, `_route_*`, `_apply_circuit_breaker` and both `_create_*_protocol`
  functions are never called (monkeypatched to raise);
- **no new run directory is ever scaffolded** and `continuation_child` is never written;
- inconclusive no longer pauses;
- profit-bars stop → resume → `completed_validated` → decide-next record on disk;
- no path reaches `holdout_evaluation` (S2d adds the spend-path tests: refused on refuted,
  inconclusive, or profit-bars FAIL; allowed path hits the existing guards; a second spend on the
  same `hypothesis_id` refused).

*Campaign review:*
- the trigger fires on the 6th memory entry and never on `failed_families`;
- reframe → brief file → a `ready` entry with `origin: campaign_review`;
- terminate → a classified pause;
- `continue` and `escalate_*` → no route and no load of `verdict_interpretation.yaml` (the file
  is absent in the fixture).

*Parking:*
- each §2 parkable site sets the marker; non-parkable 5a errors still pause;
- `process_once` writes the `paused:waiting_for_*` status and `parked_reason`, a PARKED log line,
  and a decision record;
- `--resume` skips parked entries;
- `--unpark` refusals: wrong status, class still missing, lock held;
- a successful unpark → `ready` → the next step continues the same run from the parking stage.

*Docs:* `test_guide_covers_the_code.py`, `test_doc_anchors.py`.

**The two-run proof (the plan's run budget: "the two runs of 6b, re-checked with the flag on").**
It needs real LLM stages (1a, 1b, innovation_expansion, the five readers, possibly campaign
review), so it **cannot run without an API key**, and none is available to this dispatch.

What fixtures can prove, and S2 should ship as one end-to-end test:
- `process_once` on a synthetic finished run (grid, memory and proposals on disk) under the full
  flag set ends `done` with its idea status and mints a decide-next entry;
- a second `process_once` launches exactly that entry (`fresh_launch`, run_loop stubbed);
- the decision record names it;
- no child run exists;
- trial rows are byte-identical before and after (`tools/killed_run_gate.py` already proves
  killed-run accounting under the readers flag).

The real two runs stay as S4 of the epic, run by the operator.

---

## Decision (operator, 2026-09-25)

**Guess 1 (holdout path) -- answered; S2d is unblocked.** The holdout is reached
ONLY through branch 3: a backtest passes every profit bar -> the existing
`profit_bars_reached` stop -> the operator restarts with a holdout unlock. Branch 1
(the grid / idea status) is knowledge enrichment and block identification only; a
`validated` idea NEVER leads to the holdout by itself, and grid validation is NOT a
precondition for the unlock (the RUNBOOK's best-of-N warning stays as information).
Supersedes the S1 recommendation's "refused unless the idea is validated".
Implementation direction for S2d: on `--resume` from `profit_bars_reached`, an
operator file `holdout_decision.yaml` says `spend` (-> the existing
`holdout_evaluation` stage with all its guards, for the backtest that reached the
bars) or `continue` (-> decide-next). Any other resume path to the holdout is refused.

**Guesses 2-13:** no operator objection; build on the S1 defaults.
