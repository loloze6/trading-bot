# Flag switchboard clean-up: a proposal

Night work, 2026-11-04. This is a **proposal only**. Nothing in `campaign_config.yaml`, `feature_flag_register.yaml`, the code or the tests was changed. Every class below is a proposal for the operator to rule on.

**Asked for by:** the operator's tour remarks. In 03a: remove unused flags; remove the "core" flags that will never be switched off; keep the modular ones; merge duplicates; shorten the wording; group the flags into categories. In 03b: delete legacy; keep only "mechanism workflow parameter[s] – no statistical / specific".

**Abbreviations:** SR = `strategy-research/`, RP = `SR/workflow/run_phase1_research.py`, RC = `SR/workflow/run_campaign.py`, TB = `trading-bot/`, CC = `SR/config/campaign_config.yaml`, REG = `SR/config/feature_flag_register.yaml`, T = `SR/tests/`.

**State I classified under.** The live state on the operator's PC, as the brief gives it: every `orchestrator:` flag is ON except `deviation_gate`, `zero_trade_windows_not_computed` and `extra_cards_at_1a`. The committed CC in this checkout differs: only 5 flags are `true` there. A dependency check against the live set passes: `nearest_build` needs `config_direct_authoring` and `claim_tests`, `analyst` needs `folds`, `operator_approval` needs `decide_next` and `verdict_routing_retired`, and all of them are on. So the RC launch pre-flight (RC:3750) would accept the live set.

---

## 1. Summary

**What I covered:**
- 33 `orchestrator.<name>.enabled` keys. These are the same 33 names in CC and in REG.
- `orchestrator.halt_policy.quarantine_enabled`. It is a real runtime switch, but REG does not list it.
- The 2 REG `engine_param` entries: `bar_equity` and `model_funding`.
- That makes 36 switches in total.

| Class | Count | Flags |
|---|---|---|
| CORE: hard-wire ON, delete the off path | **21** | grid_evaluation, regroup_record, decide_next, verdict_routing_retired, config_direct_authoring, data_availability_gate, claim_tests, folds, exact_config_1b, brief_criteria, variant_anti_adjacency_gate, forecast_size_probe, profit_bars_every_backtest, profit_bars_v2, cost_bar_all_costs, dsr_same_structure, forecast_ic_horizons, residual_ic_requires_block, score_provenance, schedulability_block, bar_equity (engine) |
| MODULAR: keep as a switch | **7** | exclusion_digest_input, nearest_build, variant_loop, composition_runs, analyst, operator_approval, halt_policy.quarantine_enabled |
| UNUSED: remove | **3** | stale_input_path_fix, variant_selection_record, model_funding (engine) |
| DUPLICATE: merge into the twin, then remove | **2** | profit_bars_file (twin: profit_bars_every_backtest), config_replay_gate (twin: exact_config_1b) |
| DEAD-OFF: remove | **1** | deviation_gate |
| UNSURE: operator rules | **2** | zero_trade_windows_not_computed, extra_cards_at_1a |

**The non-flag keys in CC:**
- 4 are workflow mechanism parameters to keep:
  - `orchestrator.token_budget_per_run_weighted_units`
  - `orchestrator.stage_models`
  - `orchestrator.analyst.model` (with its optional caps)
  - `orchestrator.halt_policy`, which carries the MODULAR switch above
- Everything else is statistical, legacy or unread. That covers `prescreen`, `episode_significance`, `regime_detector`, `verdict_interpreter`, `symbol_correlation`, and five scalar `orchestrator` keys. See §2b.

**Size today:** the `orchestrator:` block in CC runs from line 88 to line 1116, which is about 1,030 lines and mostly comments. REG is 929 lines.

**After the clean-up (proposal):**
- 7 switches plus 2 pending rulings.
- 4 mechanism parameters.
- One comment line each.

---

## 2. Full table

**How the evidence was gathered:**
- **Readers:** code call sites only (not comments or docstrings), found by grepping `_<name>_enabled(`, `values.get("<name>")` and `_strict_orchestrator_flag("<name>")`.
- **Pre-flight:** every orchestrator flag is also called once in RC's launch pre-flight registry `_flag_readers` (RC:3709–3747). That line is listed as "pf" and is not repeated in the evidence.
- **Generic tests:** every orchestrator flag is also touched by three generic tests:
  - T/test_e061_end_to_end_wiring.py. `TARGET_FLAGS` at :188–238 sets every flag explicitly.
  - T/test_e061_c1_4_5_pauses_preflight.py.
  - T/test_feature_flag_register.py. Its checks at :120 and :146 are data-driven over CC and REG.
- **Test counts:** "n files" counts the files under T that contain the flag name. It is a substring match, so it is an upper bound: `folds`, `analyst` and `decide_next` also match file names such as `folds.yaml` and `decide_next.py`.

### 2a. Switches

| Flag | Class | Readers (file:line) | Tests | Effect when off | Evidence |
|---|---|---|---|---|---|
| **exclusion_digest_input** (CC:142, REG:26) | MODULAR | def RP:3764; RP:3798 (`_apply_exclusion_digest_input`, called RP:9700); pf RC:3714 | test_exclusion_digest_input.py (7 files) | Step 1a and step 2 are not shown the tried ideas (`artifacts/tried_ideas.yaml` or `exclusion_digest.yaml`). | This is the operator's own example of a modular feature ("list of tried ideas shown to AI"). No other flag depends on it. |
| **stale_input_path_fix** (CC:177, REG:45) | UNUSED | def RP:3863; RP:3889 (`_apply_stale_input_path_fix`, called RP:9703); pf RC:3715 | test_stale_input_path_fix.py (3) | Nothing. The rewrite has nothing left to match. | The fix table at RP:3855–3860 rewrites `../../campaign_knowledge_base.yaml` and `../../feed_wishlist.yaml` in hypothesis_generation's `optional_inputs`. The live template `SR/workflow_artifacts/templates/handoffs/research_brief_to_hypothesis.yaml` no longer declares either path: its `optional_inputs` holds only `artifacts/run_context.yaml`. Commit 1feca0aa (D-195, 2026-10-26) dropped them. ON and OFF now produce the same prompt. |
| **variant_selection_record** (CC:206, REG:56) | UNUSED | def RP:9158; RP:9241 (`_record_variant_selection`, called only at RP:20266); RP:9488; RC:3813 (pre-flight, only when config_direct_authoring is off); pf RC:3716 | test_variant_selection_record.py, test_e036_s2a_exact_match_gate.py (6) | Nothing in the live state. | RP:20266 sits in the `elif current_stage == "backtest_specification":` branch (RP:20257). That is the legacy LLM 1b path, and it is unreachable because the branch before it, at RP:20246, takes `backtest_specification` whenever config_direct_authoring is on. `SR/workflow_artifacts/skills/strategy-config-authoring/SKILL.md:117` calls it "a different, older single-selected-variant mechanism". |
| **schedulability_block** (CC:279, REG:68) | CORE | def RC:3396; RC:2337, 2465, 2620, 2761, 2805, 4516 (all call `_write_schedulability`, RC:3605); pf RC:3745 | test_schedulability_block.py (4) | `campaign_record/schedulability.yaml` is not written. | A purely additive record. No code reads the file, and only `docs/USER_GUIDE.md` §schedulability.yaml documents it. There is no reason to switch it off, so: hard-wire it, or delete the writer if nobody reads it (see §5). |
| **variant_anti_adjacency_gate** (CC:247, REG:87) | CORE | def RP:9351; RP:9485 (legacy path, unreachable); RP:9583 (`_gate_config_direct_variants`, 5a); RC:3812–3823 (pre-flight dependency); pf RC:3729 | test_variant_anti_adjacency_gate.py, test_e036_s2a_exact_match_gate.py, test_e036_s2b_corpus_replay.py (7) | An exact repeat (same config hash, coins, timeframe and windows) is backtested again and gets a new trial row. | It protects trial accounting (N in DSR) and spend. decide_next checks novelty only for its own candidate (SR/tools/decide_next.py:1692), not for the variants step 2 creates afterwards, so the 5a gate is not a duplicate. |
| **grid_evaluation** (CC:318, REG:114) | CORE | def RP:3369; RP:2447, 2655; alias `_grid_route_enabled` RP:4011 → RP:1823, 5346, 5432, 6686, 12009, 13439, 19680, RC:2884, RC:5496; dependency of RP:4118, 5503; pf RC:3718 | test_grid_evaluation.py, test_d198_* (35) | Legacy route: `evaluate_pass_rule_criteria` plus the LLM verdict_interpreter stage (RP:216, RP:19838). | regroup_record (RP:5503) and zero_trade (RP:4118) require it, and decide_next, verdict_routing_retired and composition_runs depend on it through regroup_record. Turning it off alone is refused by the pre-flight, and the off path is the pre-grid design. |
| **profit_bars_file** (CC:349, REG:141) | DUPLICATE (twin: profit_bars_every_backtest) | def RP:3385; RP:16078 (inside `_dispatch_verdict_route`); dependency of RP:3425; pf RC:3719 | test_profit_bars_stop.py (11) | Nothing in the live state. | Its only runtime branch, RP:16078, is inside `_dispatch_verdict_route`, which raises under verdict_routing_retired (RP:16033–16038). Its only other role is as a required prerequisite of profit_bars_every_backtest (RP:3425), so the two are always on together. Merge: profit_bars_every_backtest loads `profitability_bars.yaml` itself. |
| **profit_bars_every_backtest** (CC:388, REG:169) | CORE | def RP:3400; RP:1834, 16080, 19719; dependency of RP:3483, 5743, 5794; pf RC:3724 | test_profit_bars_every_backtest.py (24) | No per-backtest bar grading and no profit_bars_reached stop. | verdict_routing_retired (RP:5742) and composition_runs (RP:5793) require it. Under retired routing it is the only path that grades a run against the bars (RP:5744–5746). |
| **profit_bars_v2** (CC:422, REG:192) | CORE (statistical, so hard-wire it) | def RP:3450; RP:2173, 3500, 6359, 7173, 7292, 9617, 14438, 15445, 19729; pf RC:3725 | test_e062_s2b1_profit_bars_v2.py (15) | Grades on the v1 bar definitions and loader schema. | The off path is the superseded bar set. RP:7173 and RP:7292 refuse a holdout spend when the definitions differ (`bars_changed`), so switching back would invalidate graded evaluations. A statistical rule, not a mechanism. |
| **data_availability_gate** (CC:463, REG:236) | CORE | def RP:3684 (defaults ON); RP:19489, 20316; pf RC:3717 | test_e054_data_availability_gate.py, test_e054_stage_wiring.py (23) | backtest_specification goes straight to protocol_execution with no data check. | The docstring at RP:3684–3700 says the brief requires this gate "for every hypothesis by default". It is the only flag that defaults ON. |
| **config_direct_authoring** (CC:497, REG:267) | CORE | def RP:3919; RP:1739, 9055, 9676, 10054, 10070, 10083, 10122, 10862, 17014, 17162, 17263, 18724, 18862, 18886, 19079, 20160, 20233, 20246; RC:638, 5487, 5684; dependency of RP:3976, 4229, 5628, 5657; pf RC:3720 | test_e056_config_direct_authoring.py (42) | Legacy flow: LLM backtest_specification after a validation stage. | variant_loop, claim_tests, nearest_build and decide_next require it, so turning it off is refused in the live state. The off path is the old pipeline. |
| **variant_loop** (CC:541, REG:294) | MODULAR | def RP:3946; RP:1846, 2042, 2843, 9591, 10059, 10090, 10129, 13460, 13950, 17014, 17162, 18724, 19371, 19452, 19464, 20329, 20453; RC:5686; dependency of RP:5792; pf RC:3721 | test_e033_slice4a_variant_loop.py (34) | Only the `base` variant is backtested. exact_config_1b then writes step 2 by code (D-112, RP:17162). | A real run-mode choice: it was off for the lane-1 exact-config runs and switched on for the daily-breadth loop (`SR/engineering/flagset_daily_breadth/apply_flagset.py:22–28`, D-130). Note: it is always set together with composition_runs and analyst (see §3). |
| **regroup_record** (CC:580, REG:332) | CORE | def RP:5488; RP:9006, 9393, 19709; RC:2684, 3819; dependency of RP:3432, 5626; pf RC:3722 | test_e058_s2a_regroup_record.py (28) | No campaign memory, registry or KB entry is written, and decide_next has nothing to read. | decide_next (RP:5626) and profit_bars_every_backtest (RP:3432) require it. |
| **score_provenance** (CC:613, REG:523) | CORE | def RP:4021; RP:1449, 4666, 5044, 19738; pf RC:3723 | test_c5_7b1_model_id_stamp.py (11) | The answering model is not stamped on scores, and the audit log has no `provenance` block. | Additive audit record (docstring RP:4021–4032), with no dependency in either direction. There is no reason to switch it off. |
| **decide_next** (CC:649, REG:362) | CORE | def RP:5599; RP:8462, 8605, 8798, 11652, 17763, 17833; RC:4522, 5624; dependency of RP:5741, 5791, RC:3423; pf RC:3726 | test_e059_s2a_decide_next.py (64*) | No automatic next run. | verdict_routing_retired, composition_runs and operator_approval require it. Under retired routing it is the only source of the next run (RP:5729–5732). |
| **verdict_routing_retired** (CC:699, REG:402) | CORE | def RP:5726; RP:2000, 3068, 7899, 19749; RC:324, 645, 2360, 4523; dependency of RP:5796, RC:3425; derived `_promotion_retired_enabled` RP:10848 and RC:3832; pf RC:3727 | test_e059_6c_s2a_route_retirement.py (15) | Legacy refine, pivot and escalate routing, the circuit breaker and promote→holdout. | The off path carries 17 `legacy routing (v26 card G)` markers in RP. composition_runs and operator_approval require it. |
| **composition_runs** (CC:750, REG:476) | MODULAR | def RP:5776; RP:2469, 6162, 8424, 8941, 20128; RC:5037; pf RC:3728 | test_e060_s3b_composition_wiring.py, test_e060_s2_residual_ic.py (11) | No residual-IC criterion, composite or registry fields, and composition briefs are refused (RP:6162). | Off for lane 1 and on for breadth (apply_flagset.py:24). A real run-mode choice. |
| **forecast_size_probe** (CC:775, REG:553) | CORE | def RP:5513; RP:2980, 5558, 16547; pf RC:3734 | test_d056_forecast_size_probe.py (3) | A config whose forecast cannot move a position is backtested anyway and gets a trial row. | A pre-trial safety check (D-056). No dependency. |
| **claim_tests** (CC:793, REG:571) | CORE | def RP:5642; RP:17420, 17750, 17871, 17888, 18411, 20090, 20119; dependency of RP:4230; pf RC:3735 | test_e068_claim_tests.py (24) | No claim block at 1a and no claim match, measure or finding. | nearest_build requires it (RP:4230), so turning it off is refused in the live state. The analyst's trade tests build on it. |
| **zero_trade_windows_not_computed** (CC:823, REG:619) | UNSURE | def RP:4087; RP:4131 (`_zero_trade_grid_kw`); pf RC:3731 | test_cul415_zero_trade_windows.py (3) | OFF in the live state: a zero-trade window votes with its 0.0 placeholder. | The on path is reachable and not superseded. But this is a statistical grading rule (D-084), not a workflow mechanism. Operator: rule it ON and hard-wire it, or delete it. |
| **analyst** (CC:843, REG:643) | MODULAR | def RP:4169; RP:1829, 5047, 5338, 15459, 17436, 17474, 17494, 18508, 18610, 19696; RC:2684, 5052; SR/tools/analyst_session.py:1920 (forces it on); pf RC:3733 | test_e075_pr5_analyst.py, test_d197_analyst_own_stage.py (41*) | No analyst stage and no trade-level claim family. | Off for lane 1, and switched on 2026-10-14 as the breadth loop's idea source (apply_flagset.py:25, 42–44). A real choice. |
| **folds** (CC:894, REG:670) | CORE | def RP:4134; RP:17480, 18161, 18579, 18597, 19669; RC:3846, 5042; SR/tools/run_protocol.py:2171 via SR/tools/research_folds.py:369 (reads CC directly); dependency of RP:4192; pf RC:3732 | test_e077_folds.py (32*) | A child copies its parent's windows. **A window overlapping the validation period is no longer refused** by the generator, the launch pre-flight or run_protocol. | The docstring at RP:4134–4156 lists the validation-period guard. Switching it off removes a leak barrier, which conflicts with the no-lookahead hard rule. analyst requires it. Kept on for both lane 1 and breadth (apply_flagset.py:38–41). |
| **operator_approval** (CC:939, REG:709) | MODULAR | def RC:3411; RC:5083, 5600; pf RC:3746 | test_e068_4_approval_cap_warnings.py (4) | decide-next picks go straight to `ready` with no hold for the operator. | REG:709 calls this "the operator's choice to supervise each agent pick". A supervision mode. |
| **nearest_build** (CC:960, REG:733) | MODULAR | def RP:4201; RP:16730, 16759, 16779, 17229, 17908, 18936; dependency of RP:4255; pf RC:3736 | test_e068_6_nearest_build.py (6) | 1b parks a component_gap instead of building the nearest version. | This is the operator's own example ("when a component is missing, the nearest buildable version is built instead"). |
| **deviation_gate** (CC:983, REG:752) | DEAD-OFF | def RP:4242; RP:18919; pf RC:3737 | test_deviation_gate.py, test_exact_config_1b.py (3) | (Live: off.) When on, any deviation 1b reports pauses the run before step 2. | Superseded in two ways. For lane 1 (its only use, D-104) it was replaced by exact_config_1b (1b written by code, so deviations read `exact`, RP:17089–17100) and by config_replay_gate (D-109, which "does not depend on 1b reporting its own deviations", RP:4413–4423). Elsewhere it cancels nearest_build: every approximation pauses. This is the operator's "pausing when approximation?" item. Switched off for breadth (apply_flagset.py:28). |
| **config_replay_gate** (CC:996, REG:766) | DUPLICATE (twin: exact_config_1b) | def RP:4412; RP:18921; pf RC:3738 | test_config_replay_gate.py (2) | No replay of 1b's config against the brief's exact config. | It acts only when the brief carries an exact config (RP:4416–4421). With exact_config_1b on, such a brief's 1b is the brief's config copied by code (RP:17089–17100: "the brief's exact config goes into backtest_spec.yaml … unchanged"), so the replay compares the config with itself. Both were switched on together for the lane-1 fold-B runs (REG:766, REG:780). |
| **exact_config_1b** (CC:1008, REG:780) | CORE | def RP:4260; RP:17081 (`_exact_config_1b_mode`); RC:5057, 5685; pf RC:3739 | test_exact_config_1b.py, test_exact_config_step2.py (5) | An exact-config brief goes to the LLM 1b, and decide-next config vehicles become INFEASIBLE (SR/tools/decide_next.py:2074–2077). | The off path is the CUL-429 failure mode: the LLM diverges from the brief's config. It acts only when the brief carries an exact config, so ON costs nothing for other briefs. |
| **brief_criteria** (CC:1025, REG:798) | CORE | def RP:4273; RC:862, 5106; pf RC:3740 | test_d121_brief_criteria.py (4) | A brief's menu-id criteria go through the legacy lints, and a fold child's criteria are re-picked at 1a instead of being copied from its source. | Copying the source run's criteria is what makes a fold child a confirmation (D-121). With no criteria given, 1a picks as before (RP:4282–4283), so ON is a superset. It was off only in lane 1, where there were no fold children. |
| **dsr_same_structure** (CC:1034, REG:812) | CORE (statistical, so hard-wire it) | def RP:4287; RP:12122, 12132, 12216, 14463, 15127, 15461; pf RC:3744 | test_d185_dsr_same_structure.py (2) | DSR N and K are campaign-wide, and trial rows carry no structure_hash or timeframe. | A statistical method choice (D-185). SR/tools/backfill_structure_hash.py has already keyed the old ledger rows. |
| **extra_cards_at_1a** (CC:1055, REG:829) | UNSURE | def RP:4301 (no direct call); RC:4647 (`flag_values.get`); pf RC:3741 | test_d138_extra_cards_at_1a.py (2) | OFF in the live state: 1a's extra cards are enqueued only after run_loop and are lost if the run then fails. | Reachable and not superseded: 1a still writes extra cards (RP:8580–8586, `queued_hypotheses.yaml`). It has never been switched on in a run. ON looks strictly safer (it keeps the cards on a later failure). Operator: hard-wire ON, or delete. |
| **cost_bar_all_costs** (CC:1065, REG:875) | CORE (statistical, so hard-wire it) | def RP:4045; RP:4077 (`--cost-bar-all-costs` to SR/tools/run_protocol.py:2412), 4084, 7265, 14879; pf RC:3730 | test_cul414_cost_bar_all_costs.py (4) | The D-038 ">2.2" bar compares the edge with fees only. | REG:875 records the operator's decision of 2026-10-08 to switch it on as a declared, stricter output change. |
| **forecast_ic_horizons** (CC:1086, REG:842) | CORE (statistical, so hard-wire it) | def RP:4314; RP:4348 (`--forecast-ic-horizons`), 4391, 4403, 6057; pf RC:3742 | test_d186_forecast_ic_horizons.py (6) | The menu loses its `horizon` keys, and the IC and residual IC use the next bar only. | The off path strips menu text by regex (`_menu_text_for_prompt`, RP:4356–4383). Hard-wiring deletes that bracket logic. |
| **residual_ic_requires_block** (CC:1103, REG:862) | CORE (statistical, so hard-wire it) | def RP:4333; RP:5897, 6052; pf RC:3743 | test_d186_forecast_ic_horizons.py (2) | The first block on a timeframe gets a residual-IC criterion against an empty composite. | A method fix (D-186). No dependency. |
| **halt_policy.quarantine_enabled** (CC:121; **not in REG**) | MODULAR | def RC:1993; RC:3350, 4683; type check in the pre-flight at RC:3787, 3807 | test_halt_quarantine_policy.py (5) | Every halt stops the campaign. ON lets the four quarantine-safe reasons continue. | A real halt-policy choice. Its live value is assumed ON from the brief (see §5). It is the only flag the reader coerces with `bool()` (RC:2007) instead of strictly, and REG does not list it, because T/test_feature_flag_register.py:79 discovers only `.enabled` keys. |
| **bar_equity** (engine_param, REG:896) | CORE | TB/core/launcher.py:623, TB/core/backtester.py:90, 114; caller SR/tools/run_protocol.py:2611 and 2684 (`bar_equity=True`) | TB/tests/test_bar_equity*.py; T/test_feature_flag_register.py:223 | No `bar_equity` block in metrics.json. | Already hard-wired by the only caller. There is no config key, so it is not something the operator can switch. |
| **model_funding** (engine_param, REG:914) | UNUSED | TB/core/launcher.py:625, TB/core/trading_bot.py:41, 107, 424, TB/core/backtester.py:93, 153, 161, 343; **no SR caller** | TB/tests/test_model_funding_*.py (3 files), test_funding_*.py; T/test_feature_flag_register.py:239 | Always off: SR/tools/run_protocol.py never passes it. | An engine feature blocked on E-014 (status now in Linear, not checked). Not a workflow switch: drop it from the workflow register and keep it as an engine parameter in TB. |

### 2b. Non-flag keys of CC ("keep only workflow mechanism parameters")

| Key | Mechanism parameter? | Readers | Tests | Proposal |
|---|---|---|---|---|
| `orchestrator.token_budget_per_run_weighted_units` (CC:92) | **Yes** (budget) | RP:998 (`_load_token_budget` RP:983, used RP:5030, 17981, 19805); RC:3147 (message) | test_token_budget_weighted.py | Keep. |
| `orchestrator.stage_models` (CC:878) | **Yes** (model) | RP:1153 (`_stage_model` RP:1143) | test_d189_stage_models.py | Keep. |
| `orchestrator.analyst.model` (+ optional `max_turns`, `max_budget_usd`, `timeout_minutes`) | **Yes** (model and budget) | RP:4731 (`_analyst_caps` RP:4726) | test_e075_pr5_analyst.py | Keep, next to the `analyst` switch. |
| `orchestrator.halt_policy` | **Yes** (holds quarantine_enabled) | RC:2006 | test_halt_quarantine_policy.py | Keep as a switch. |
| `orchestrator.token_budget_per_run` (CC:89) | No: superseded | none (CC:89–91 itself says "no longer read") | none | Remove. |
| `orchestrator.max_refinements_default` (CC:116) | No: legacy | none. The real default is a literal `2` at RP:9798, on the legacy validation route. | none | Remove. |
| `orchestrator.review_every_n_runs_default` (CC:117) | Mechanism in nature, but **unread** | none. The real knob is `campaign_state.yaml review_every_n_runs`, literal default `6` at RP:7752. | none | Remove (or wire it, if the operator wants it here). |
| `orchestrator.distinct_failed_families_trigger` (CC:118) | No: legacy (families retired in slice 6c) | none | none | Remove. |
| `orchestrator.below_floor_pct_threshold` (CC:119) | No: statistical | none at runtime. The literal `50.0` is at RP:12330 and 13269. | test_campaign_config_sync.py:124 (source-text parity) | Remove. The constant stays in code. |
| `prescreen.*` (4 keys, CC:18) | No: statistical | none at runtime ("declared parity only", CC:7–12) | test_campaign_config_sync.py:42–86 | Remove. The constants live in TB/performance/signal_statistics.py:233, 240 and SR/tools/timeframe.py. |
| `episode_significance.*` (4 keys, CC:51) | No: statistical | none from CC. Runtime reads use the data-policy file (SR/tools/run_protocol.py:1563–1565) or code defaults (SR/tools/claim_tests.py:155–159). | test_campaign_config_sync.py:147 | Remove. The constants live in SR/tools/episode_significance.py:88–91. |
| `regime_detector.*` (4 keys, CC:67) | No: statistical, plus CLI default dates | none at runtime | test_campaign_config_sync.py:89–121 | Remove. The constants live in SR/tools/validate_regime_detector.py. |
| `verdict_interpreter.*` (7 keys, CC:1117) | No: legacy and statistical | none ("applied by the LLM agent, not code", CC:1118). The stage is unreached on the grid route. | none | Remove. |
| `symbol_correlation.btc_eth_return_correlation_1h` (CC:1132) | No: statistical | none. `_load_symbol_correlation`, which RC:1999 names in a comment, no longer exists, and the A8.6 mirror is deleted (test_campaign_config_sync.py comment). | none | Remove. |

Removing the statistical sections means deleting T/test_campaign_config_sync.py, or turning it into a code-only check. CC's header (lines 1–12) presents the file as their "canonical reference", so the operator rules on whether those values move to a separate reference file or to the code comments.

---

## 3. Proposed cleaned register (YAML)

```yaml
# feature_flag_register.yaml -- proposal (night work 2026-11-04). One line per entry.
# Switches = real choices the operator may flip. Everything else is hard-wired or gone.

switches:                       # orchestrator.<name>.enabled unless noted
  ideas:                        # steps 1a / 2
    exclusion_digest_input:  "Show the tried-ideas list to steps 1a and 2."
  build:                        # step 1b
    nearest_build:           "When a component is missing, build the nearest version and record the deviation (needs claim_tests: hard-wired)."
  test:                         # protocol execution
    variant_loop:            "Backtest every step-2 variant, not only base."
    composition_runs:        "Residual-IC criterion and composite; composition briefs allowed (needs variant_loop)."
  read:                         # after the backtests
    analyst:                 "Run the analyst stage and the trade-level claim family."
  next_run:                     # campaign loop
    operator_approval:       "Hold every decide-next pick for operator approval."
    halt_policy.quarantine_enabled: "Continue past the four quarantine-safe halts instead of stopping."
  # Note: variant_loop + composition_runs + analyst were flipped together (D-130: off for
  # lane 1, on for breadth). Option: merge them into one run-mode switch. Operator rules.

pending_ruling:                 # off today; operator rules: hard-wire ON, or delete
  zero_trade_windows_not_computed: "A zero-trade window does not vote in the grid (statistical rule, D-084)."
  extra_cards_at_1a:               "Enqueue step 1a's extra cards as soon as 1a completes (D-138)."

parameters:                     # workflow mechanism parameters kept in campaign_config.yaml
  token_budget_per_run_weighted_units: "Per-run weighted-token circuit breaker."
  stage_models:                        "Model per LLM stage."
  analyst.model:                       "Analyst model (+ optional caps)."

always_on_to_be_hard_wired:     # CORE: reader -> constant True, then delete the off branch
  pipeline:
    config_direct_authoring:  "1a -> 1b config authoring -> 2 -> tool 5a; no validation stage, no LLM backtest_specification."
    data_availability_gate:   "Data gate before every backtest."
    exact_config_1b:          "A brief's exact config becomes 1b by code."
    claim_tests:              "Claim block at 1a, matched and measured."
    forecast_size_probe:      "Refuse a config whose forecast cannot trade, before any trial."
    variant_anti_adjacency_gate: "Exact repeats are not re-tested."
  route_and_record:
    grid_evaluation:          "Grid decides idea status (verdict_interpreter route deleted)."
    regroup_record:           "Campaign memory, registry and KB written after each run."
    verdict_routing_retired:  "Run ends completed_<status>; refine/pivot/escalate deleted."
    decide_next:              "Code picks the next run."
    brief_criteria:           "A brief's menu criteria are read as one field; fold children keep their source's criteria."
    folds:                    "Fold windows; validation-period windows refused (leak barrier)."
  grading:                      # statistical: out of the switchboard per the operator's 03b remark
    profit_bars_every_backtest: "Grade every backtest against the profit bars."
    profit_bars_v2:           "v2 bar definitions."
    cost_bar_all_costs:       "Cost bar counts fees and slippage."
    dsr_same_structure:       "DSR N/K counted within the same structure and timeframe."
    forecast_ic_horizons:     "Forecast IC at h1..h168."
    residual_ic_requires_block: "No residual IC for the first block on a timeframe."
  records:
    score_provenance:         "Stamp the answering model on scores and the audit log."
    schedulability_block:     "Write campaign_record/schedulability.yaml (or delete: no code reader)."
  engine:
    bar_equity:               "Already passed True by tools/run_protocol.py:2611/2684; drop from register."

to_remove:
  stale_input_path_fix:       # UNUSED: nothing left to rewrite since D-195
    touches: [RP:3855-3895 (table, reader, _apply_stale_input_path_fix), RP:9703 call, RC:3715,
              CC:177-205, REG:45-55, T/test_stale_input_path_fix.py, TARGET_FLAGS in
              T/test_e061_end_to_end_wiring.py:190, docs/USER_GUIDE.md + docs/RUNBOOK.md mentions]
  variant_selection_record:   # UNUSED: legacy LLM-1b path only
    touches: [RP:9158-9166 reader, RP:9220-~9300 _record_variant_selection, RP:9488-9500 check,
              RP:20266 call (goes with the legacy backtest_specification branch RP:20257-),
              RC:3716, RC:3813-3817, CC:206-246, REG:56-66, T/test_variant_selection_record.py,
              T/test_e036_s2a_exact_match_gate.py + test_variant_anti_adjacency_gate.py legacy cases,
              SKILL.md strategy-config-authoring:117 sentence]
  profit_bars_file:           # DUPLICATE of profit_bars_every_backtest
    touches: [RP:3385-3394 reader, RP:3425-3430 dependency check, RP:16078-16100 legacy promote
              branch (deleted with _dispatch_verdict_route), RC:3719, CC:349-387, REG:141-168,
              T/test_profit_bars_stop.py, 10 other test files that set it]
  config_replay_gate:         # DUPLICATE of exact_config_1b
    touches: [RP:4412-4423 reader, RP:18921 call, _route_config_replay_gate (RP:17186-),
              CONFIG_REPLAY_ARTIFACT RP:16913, RC:3738, CC:996-1007, REG:766-779,
              T/test_config_replay_gate.py, SR/tools/run_viewer replay_gate column (DESIGN.md:55),
              engineering/lane1_replay/replay_config.py if no other user]
  deviation_gate:             # DEAD-OFF: superseded by exact_config_1b (+ replay); cancels nearest_build
    touches: [RP:4242-4257 reader, RP:18919-18920 call, _route_deviation_gate (RP:16884-),
              RC:3737, CC:983-995, REG:752-765, T/test_deviation_gate.py,
              T/test_exact_config_1b.py deviation cases, docs/RUNBOOK.md, L1 briefs (history only)]
  model_funding:              # UNUSED in the workflow: no caller; engine param stays in TB
    touches: [REG:914-929, T/test_feature_flag_register.py:239-258 and :288 (count of engine params)]
  parameters:                 # non-mechanism keys of campaign_config.yaml
    - orchestrator.token_budget_per_run
    - orchestrator.max_refinements_default
    - orchestrator.review_every_n_runs_default
    - orchestrator.distinct_failed_families_trigger
    - orchestrator.below_floor_pct_threshold
    - prescreen, episode_significance, regime_detector, verdict_interpreter, symbol_correlation
    touches: [T/test_campaign_config_sync.py (whole file), CC header lines 1-12]
```

**For comparison, the proposed CC `orchestrator:` block** (comments shortened to one line, values as in the live state):

```yaml
orchestrator:
  # --- mechanism parameters ---
  token_budget_per_run_weighted_units: 1800000   # per-run circuit breaker (weighted tokens)
  stage_models: {hypothesis_generation: claude-sonnet-5-5, strategy_config_authoring: claude-sonnet-5-5}
  # --- switches ---
  exclusion_digest_input: {enabled: true}   # ideas: show tried ideas to 1a/2
  nearest_build:          {enabled: true}   # build: nearest version when a component is missing
  variant_loop:           {enabled: true}   # test: every variant, not only base
  composition_runs:       {enabled: true}   # test: residual IC + composite (needs variant_loop)
  analyst:                {enabled: true, model: claude-sonnet-5-5}   # read: analyst stage
  operator_approval:      {enabled: true}   # next run: hold decide-next picks for approval
  halt_policy:            {quarantine_enabled: true}   # next run: continue past quarantine-safe halts
  # --- pending ruling ---
  zero_trade_windows_not_computed: {enabled: false}
  extra_cards_at_1a:               {enabled: false}
```

---

## 4. Migration steps for a later build window (not done)

Per the CLAUDE.md working rules ("Build only what a run asked for … Everything else waits"; "A sequencing line is not an approval"), this is a separate build that the operator would have to approve by name. Start from the PC's uncommitted CC and REG, not from this checkout's copies.

**Phase A — pin (small, reversible):** CORE readers return True; UNUSED, DUPLICATE and DEAD-OFF readers are deleted. No branch code is deleted yet.

- [ ] For each of the 20 CORE orchestrator flags, replace the reader body with `return True`. Keep the function, so every call site is unchanged. The readers are RP:3369, 3400, 3450, 3684, 3919, 4021, 4045, 4134, 4260, 4273, 4287, 4314, 4333, 5488, 5513, 5599, 5642, 5726, 9351 and RC:3396.
- [ ] Delete the now-vacuous dependency checks inside those readers and in the remaining modular readers. These are `_flag_dep` / `requires=` at RP:3425, 3432, 3483, 3976, 4118, 4192, 4229–4230, 5503, 5626–5628, 5657, 5741–5743, 5791–5796, RC:3423–3425 and RC:3812–3823.
- [ ] Shrink `_flag_readers` (RC:3709–3747) to the 7 switches plus the 2 pending ones.
- [ ] Remove the CORE, UNUSED, DUPLICATE and DEAD-OFF blocks from CC and from REG (the PC copy).
- [ ] Collapse the aliases and derived values:
  - `_grid_route_enabled` (RP:4011) becomes `True`.
  - `_promotion_retired_enabled` (RP:10848) and `_promotion_retired_from` (RC:3832) become `True`.
  - `_folds_from` (RC:3842) becomes `True`.
  - `SR/tools/research_folds.folds_flag_enabled` (:369), which run_protocol uses at :2171, becomes `True`. It reads CC directly.
- [ ] Delete the stale_input_path_fix, variant_selection_record, profit_bars_file, config_replay_gate and deviation_gate readers and their call sites (listed under `to_remove` above).
- [ ] Add `halt_policy.quarantine_enabled` to REG. Make `_quarantine_enabled` (RC:2007) strict like the others.
- [ ] Rewrite REG to the short schema in §3, and update T/test_feature_flag_register.py to match:
  - The checks at :120, :132 and :146 discover `.enabled` keys. Add `halt_policy`.
  - :187 requires `blocked_on` for `off_incomplete`. Change it for the new `pending_ruling` group.
  - :223–:302 are the engine_param checks. Drop model_funding; drop bar_equity or keep it as a code assertion on run_protocol.py.
- [ ] Update **T/test_e061_end_to_end_wiring.py** (the costly part). `TARGET_FLAGS` (:188–238) runs every scenario with folds, claim_tests, forecast_size_probe, score_provenance, profit_bars_v2, brief_criteria, cost_bar_all_costs, dsr_same_structure, exact_config_1b and others OFF, and its stubs rely on that:
  - stub cards have no claim block (:226);
  - stub briefs' windows are copied (:220);
  - the probe needs the real engine (:214).
  - Hard-wiring these ON means the stubs must carry claim blocks and fold-valid windows, and the probe must be patched out in the harness.
  - `test_target_flags_name_every_orchestrator_flag` (:2468) and the `V2_FLAGS` / `C4_FLAGS` sets shrink.
  - Cases built on `variant_loop: False` (:1841) and `composition_runs: False` (:2087) stay, because those flags stay modular.
- [ ] Update T/test_e061_c1_4_5_pauses_preflight.py. Its dependency-refusal cases for pairs that no longer exist must go.
- [ ] Update every test that sets a CORE flag to False to test the flag-off path. Grep each name: up to 64 files for decide_next, 42 for config_direct_authoring, 35 for grid_evaluation, 34 for variant_loop (that one stays). Each flag-off "byte-identical" test is deleted or turned into a flag-on assertion.
- [ ] Update docs/RUNBOOK.md §3 (the flag list near :300 and the `flag_misconfiguration` row near :690) and the flag table in docs/USER_GUIDE.md (near :2456–2470).
- [ ] Update `SR/engineering/flagset_daily_breadth/apply_flagset.py` and `preflight_check.py`, or retire them. They edit flags that would no longer exist.

**Phase B — prune the off paths (large; one PR per group, run-driven if possible):**

- [ ] **Legacy pipeline (config_direct_authoring):**
  - the validation stage and the LLM backtest_specification branch (RP:20257 onwards, including `_record_variant_selection` and `_route_post_variant_selection` RP:9464);
  - `determine_post_spec_route`;
  - the templates `innovation_expansion_to_validation.yaml` and `validation_to_backtest_specification.yaml`.
- [ ] **Legacy route (grid, verdict_routing_retired):**
  - the verdict_interpreter stage (RP:214–216, 1025, 3095, 3197, 3263, 9898, 9962, 9980, 19838, 19971–19977);
  - `_dispatch_verdict_route` and its 17 `legacy routing (v26 card G)` blocks;
  - the template `protocol_to_verdict_interpreter.yaml`;
  - the `verdict-interpreter` skill.
- [ ] **v1 profit bars:** the `_profit_bars_v2_enabled() == False` branches and the v1 loader schema. Holdout `bars_changed` refusals (RP:7173, 7292) then compare against a constant `v2`.
- [ ] **Statistical keyword defaults:** either flip the tool-side defaults to True, or have callers always pass them. The tools are SR/tools/verdict_criteria_evaluator.py (`cost_bar_all_costs`, `single_era_inconclusive`), SR/tools/run_protocol.py (`--cost-bar-all-costs` :2412, `--forecast-ic-horizons` :2419) and SR/tools/explore_confirm.py:391–393. Delete `_menu_text_for_prompt` and the D-186 OFF markers in criterion_menu.yaml (RP:4356–4383).
- [ ] **Non-flag CC sections:** remove them (§2b), and delete or rewrite T/test_campaign_config_sync.py.
- [ ] After each group, run the full suite (`python run_tests.py`, which CI also runs in .github/workflows/tests.yml:97). CI has no flag-specific step.

---

## 5. Not checked

- **The live flag values.** They come from the brief, not from the PC; this checkout's CC has only 5 flags on. In particular, `halt_policy.quarantine_enabled` is assumed ON because "every `orchestrator:` flag" is ON, but it is not an `.enabled` key, so this is not certain. If it is off on the PC, it stays MODULAR anyway.
- **No runs and no tests were executed.** Every "effect when off" was read from code, docstrings and the gate order, not observed.
- **config_replay_gate as a DUPLICATE.** This is inferred from RP:17089–17100 (code-written 1b copies the brief's config unchanged) and the gate order RP:18913–18921. I did not check whether `engineering/lane1_replay/replay_config.py` compares anything that the code copy or the pass-through manifest (`_write_pass_through_manifest`, RP:18913) could alter.
- **The UNSURE and borderline calls.** Whether `schedulability_block`, `score_provenance` and `brief_criteria` are truly "never off" is a judgement from their additive or superset effect. There is no operator statement on them.
- **E-014's status (model_funding).** The epic says it moved to Linear, which I did not query.
- **The `c4/flag-set` branch** that REG cites as where flags were switched on: not inspected.
- **Skills and prompts.** I checked SKILL.md text only for the removal candidates. I did not check whether any skill relies on a flag-gated input file for a CORE flag's off state.
- **Operator tooling outside the repo, and the PC's uncommitted CC/REG comments:** not visible from here.
- **Test-file counts** are substring matches and therefore upper bounds.
- **Sources not read, by instruction:** guided_tour "Speech" beyond the remarks, "Inspector notes", `guided_tour/_post_tour/`, `TB/local_data/`, `holdout_sealed`. No date from `campaign_data_policy.yaml` is written here, and neither are the `regime_detector` default dates.
