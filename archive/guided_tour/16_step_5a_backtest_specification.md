# Stop 16: Step 5a, backtest_specification (a code step)

## Speech (verbatim)

**Stop 16 of 29: Step 5a, building and checking the variants.** Open on the side: `run_phase1_research.py`, `tools/block_manifest.py`, `tools/json_pointer.py`, `tools/forecast_rules.py`, `tools/variant_coin.py`, `trading-bot/tools/validate_config.py`, `tools/anti_adjacency_gate.py`, `tools/novelty.py`, run_102's `artifacts/variants/`.

**In one sentence.**
Step 5a is a code step with no AI: it applies each variant's edits (patches) to the base config, writes one finished config and one test protocol per variant, checks every one, and drops any variant that repeats something already tested.

**Why it exists.**
An AI wrote the edits (step 2); code must turn them into exact configs and check them before money is spent on backtests.
Two failures matter most: a broken config that crashes or silently tests nothing, and a variant identical to one already tested, which would spend money for no new knowledge and count twice in the statistics.

**What comes in, what goes out.**
- In: the base config and block manifest (step 1b, stop 10); the variant edits (step 2, stop 15); the run's protocol (its test windows); campaign memory (every variant tested before).
- Out: per variant, a folder with its `strategy_config.json` and `protocol.json`; an index of all variants and their status; a frozen copy of the run's protocol; a repeat-check record; a copy of the base as `candidate_strategy_config.json`.
- Next: the data check (stop 17), then the backtests (stop 18), for every variant marked validated.

**What happens here, step by step.**
1. It reads the base config and the variant list; a missing file stops the run loudly.
2. It checks the block manifest (which parts of the config are the idea) against the base config, with the same check the block registry uses later.
3. For a follow-up run whose config must pass through unchanged, it checks the config's fingerprint.
4. It freezes the run's protocol once (a copy with its fingerprint), so every later step reads the same windows.
5. For each variant: refuse a duplicate or malformed id; apply its edits by config path; resolve its coin (one coin per variant, the venue's own symbol name, which windows the coin's data covers); write its config and protocol.
6. Each variant's config goes through the engine validator (rules V1 to V19, stop 12b), the graded and standardised rules (decision D-149, a row of the decision log), a check that no component class changed, and the forecast size probe on invented prices. A failing variant is marked, and its errors written to a report in its folder.
7. A failing design or asset variant sends step 2 back once with the errors; a failing base pauses the run.
8. The repeat check: each variant's exact key (its config fingerprint, its coins, the bar size, a fingerprint of its windows) is looked up in campaign memory. A repeat is marked "not tested" and gets no backtest. If every variant is a repeat, the run ends "no new hypothesis".

Example: run_102's index lists four validated variants: `base` and `split_stretch_weight` on BTC, `asset_xrp_payment` on XRP and `asset_ltc_altcoin_l1` on LTC, each covering all 6 windows of fold B (six 4-month blocks across 2018-2021). The repeat check found no repeat (`variant_anti_adjacency_result.yaml`: `repeats: []`, every variant "novel").

**What it costs and how long it takes.**
No AI call. Its duration is not recorded in the audit log.
run_102: 4 variants, 4 configs and 4 protocols (`runs/run_102/artifacts/variants/index.yaml`).

**What is switched off or not used here.**
- The variant-selection record is on but does nothing on this path: it belongs to the old flow where an AI picked one variant from a menu.
- The old AI version of this step (backtest engineering) is not reached.
- No `spec_validation_report.txt` exists in run_102: it is written only for a failing variant.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| The tool step | `run_phase1_research.py:2757-3072` | `run_tool_worker` branch for `backtest_specification` |
| Inputs present | `run_phase1_research.py:2771-2789` | Base config, variant list |
| Manifest check | `run_phase1_research.py:2790-2825`; `tools/block_manifest.py` | Same check as the registry |
| Pass-through hash | `run_phase1_research.py:2826-2833`, `:8479` | Follow-up config unchanged |
| Frozen protocol | `run_phase1_research.py:2834-2846`, `:19172` | `variants/run_protocol.json` |
| Per variant | `run_phase1_research.py:2853-3055` | Id checks (`:2856-2880`), patch (`tools/json_pointer.py`), coin (`:19309`, `tools/variant_coin.py`, rule G4 `:681-682`, `:725`), validator (`:2961`, `trading-bot/tools/validate_config.py`), D-051/D-149 and class match (`:2915-2925`, `tools/forecast_rules.py`), size probe, report (`:2968`) |
| Base re-check, requests | `run_phase1_research.py:3056-3072` | Base variant; component requests |
| Route | `run_phase1_research.py:19407-19520` | Repeat gate first, then step-2 retry or pause |
| Repeat gate | `run_phase1_research.py:9549-9668`; `tools/anti_adjacency_gate.py`; `tools/novelty.py`; `tools/campaign_memory.py` | Exact key against memory; all repeats → `completed_no_new_hypothesis` |
| Variant selection (inert here) | `run_phase1_research.py:9220`, `:9464` | Old-flow record |
| Outputs | `runs/run_102/artifacts/variants/<vid>/{strategy_config.json,protocol.json}`, `variants/index.yaml`, `variants/run_protocol.json`, `candidate_strategy_config.json`, `variant_anti_adjacency_result.yaml`; `campaign_record/component_requests.yaml` | run_102: 4 validated, 0 repeats |

Remarks: send them as "stop 16: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

### (1) Design and mechanism

1. This is the step the pipeline needed and it is built right: code, not a model, turns the patches into configs (`json_pointer.apply_json_pointer_patch`, fail-loud on a missing parent, `json_pointer.py:32-35`), checks the manifest with the registry's own function (`RP:2815-2825`, `block_manifest.py:6-17`), refuses a variant that removes a block path (`:2904-2913`), applies D-051/D-053/D-176 after the patch (`:2915-2932`), runs the engine validator and the size probe per variant (`:2961-3032`), resolves one coin per variant with its venue symbol and window coverage (`:2934-2953`, `variant_coin.py:606-665`), freezes the run protocol with its hash on every index entry (`:2842-2846`, `:19172-19186`, index `:9`, `:17`, `:41`, `:65`), and writes the base copy the later tool stages read (`:3052-3054`). run_102: four validated, four configs, four protocols, the split variant's weight 0.125 applied (`split_stretch_weight/strategy_config.json:38`). The frozen copy answers half of stop 05b note 1.6: after 5a the run folder holds its own protocol; the fold draw (stop 06) still reads the shared `protocols/` file through the memory's `protocol_ref` (`variant_anti_adjacency_result.yaml:3`).
2. The repeat gate refuses only a byte-identical re-run. The key is the full config hash, the coins, the timeframe and the window hash (`novelty.py:7-9`, `anti_adjacency_gate.py:17-26`); a changed weight (0.25 vs run_101's 1.0), a changed coin or a different fold is NOVEL by construction, and "there is no NEIGHBOUR outcome" (`:22-24`, the design rejected 2026-09-02). Layer 1 (the knowledge base) is advisory and read `no_opinion` on all four variants (`variant_anti_adjacency_result.yaml:21-24`); its input is a retired routing field (`anti_adjacency_gate.py:31-34`). So the stated purpose ("a variant identical to one already tested ... would spend money for no new knowledge", speech) is served only against an accidental re-run: a resume, a relaunch, or an operator re-registering the same brief on the same fold. The lineage of stop 15 note 1.3 (one weight walked up and down over three runs) passes this gate every time. The gate is named for a design it does not implement; "exact-repeat check" is what it is.
3. Memory is the only source, and memory starts at the regroup stage: a run before it "can never produce REPEAT" (`novelty.py:38-42`); 28 of 102 runs are in memory (stop 07). Everything tested before 2026-09 is novel to this gate. Documented, and a fact the operator should hold when reading `repeats: []`.
4. "Component requests" is the name of a list that holds every reason a variant was not built: a patch whose parent path is missing (`:2890-2895`), an unresolved manifest path (`:2908-2913`), a D-051/D-053 refusal (`:2923-2932`), a validator violation (`:2966-2978`), a size-probe refusal (`:3022-3032`), each appended to `campaign_record/component_requests.yaml` (`:3059-3068`). A typo in a step-2 path becomes a "component request". With stop 10 note 1.4 and note 2.6: the one file that could tell the operator which engine pieces are missing is filled with build failures of every kind and has no status field.
5. The variant protocol records what is really tested: Kraken spot prices as a proxy for Kraken futures, funding not modelled, the funding feed dropped (`asset_xrp_payment/protocol.json:5-18`). Every "perp" brief of this campaign is a spot-price backtest with futures fees and no funding leg (stop 03b note 1.5, stop 13 note 1.2). The file says so in its `label`; the brief's `product: perp` and the memory's `venue` do not. Stop 18's territory; recorded here because 5a is where the per-variant protocol is written.
6. The route is sound and its floors are placed well: step 2's shape and config errors first (retry once, base errors to 1b, `:19435-19439`, stop 15), the repeat gate second (`:19444-19446`), "nothing validated" parks on a missing class or pauses (`:19449-19488`), the three-variant floor only when the data gate is off (`:19491-19519`); coverage and repeat skips never count against the floor (`:19497-19498`). The one subprocess cost (a Python start per `validate_config.py` and per probe, up to eight per run) is not recorded anywhere (stop 05a note 1.4).

### (2) Legacy or simplifiable (leads)

1. `anti_adjacency_gate.py`: the Layer-1 KB advisory (`:28-34`, `_kb_findings_matching_candidate`, `_branch_closed_by_lineage_routing`, the precedence rule `:41-58`) reads `pass_rule_evaluation.yaml`'s `lineage_routing`, a retired field; it answered `no_opinion` four times on run_102 and is written into every result. The `from build_exclusion_digest import extract_timeframes` (`:74`) ties the live gate to the digest tool the campaign does not run. Keep the exact-match layer; delete Layer 1 and rename the module.
2. `index.yaml` path style: `config_path` is written with the OS separator (`str(... .relative_to(RUN_DIR))`, `:2972`, `:3036`; index `:4` has backslashes) while `protocol_path` is posix (`:3048`; index `:7`). Readers that compare refs (`campaign_memory.protocol_ref_of`, `config_ref` in the gate result, `:31`) normalise; a Windows-written index read on Linux may not. One `.as_posix()`.
3. Two symbol conventions in one index: base/design carry the resolved venue symbol (`BTCUSD`, `:6`, `:14`), asset variants the universe name with the venue name under `coverage.venue_symbol` (`XRPUSDT`/`XRPUSD`, `:22-24`). The gate's key uses the venue names for all (`variant_anti_adjacency_result.yaml:28`, `:43`, `:58`).
4. `_record_variant_selection` and `_route_post_variant_selection` (`:9220`, `:9464`), with the `variant_selection_record` flag on and inert (stop 03a note 2.4): called only from the legacy 5a branch (`RP:20266`, `:20287`). With the flag folded, both go.
5. `_check_pass_through_config_hash` is called twice in one pass (`:2828`, `:3057`); the first call cannot see `variants/base/strategy_config.json` yet, so it checks the spec only. One call after the loop would do.
6. The composition branches inside this step (`:2799-2813`, `:2897-2901`) and the `_comp_run` guards in the route (`:9585-9586`): the composition path (one active block in the registry, stop 03a note 2.9).
7. `spec_validation_report.txt` is written per variant folder for validator failures only (`:2968`); D-051 and size refusals go to `index.report` and a run-level refusals file (`_record_forecast_rule_refusal`). One place for a variant's refusal would serve the operator and the retry context alike.

### (3) Disagreements between the speech and the element

1. Step 8, "each variant's exact key ... is looked up in campaign memory. A repeat is marked not tested": correct (`:9600-9648`); not stated that only a byte-identical config on the same coins and windows can match, and that nothing before the regroup stage is in memory (notes 1.2, 1.3). The speech's "Why it exists" paragraph promises more than the gate does.
2. Step 6, "A failing variant is marked, and its errors written to a report in its folder": true for validator failures (`spec_validation_report.txt`, `:2968`); D-051/D-053/D-176 and size-probe failures are written to `index.yaml`'s `report` and the run-level refusals record, not to the folder (`:2924-2930`, `:3023-3031`). Half.
3. Step 5, "resolve its coin (one coin per variant, the venue's own symbol name ...)": for base/design the index carries the venue name, for asset variants the universe name (note 2.3). The protocol files carry the venue name in both cases (`asset_xrp_payment/protocol.json:2-4`). Fine.
4. Step 7: correct (`_route_variant_step2_outputs`, stop 15). Step 4: correct (`:19172-19186`). Step 2: correct (`:2815-2825`).
5. Example: four validated with full coverage and no repeat: index `:1-66`, result `:11-12`; correct. Not stated: the four keys share one window hash and the two asset keys share the base's config hash with another coin (`variant_anti_adjacency_result.yaml:26-30`, `:41-45`, `:56-60`), which is what the index already says in words.
6. Section 6: all three facts correct (`_record_variant_selection` unreached on this path; the LLM 5a branch `:20257-20327` unreached; no report file in run_102's variant folders by the artifacts listing at stop 05b).
7. Reading-map ranges verified: `RP:2757-3072`, `:2771-2789`, `:2790-2825`, `:2826-2833` (`:2826-2828`), `:8479`, `:2834-2846`, `:19172`, `:2853-3055`, `:2856-2880` (`:2853-2886`), `:19309`, `variant_coin.py:681-682` (docstring) and `:724-727` (code), `:2961`, `:2915-2925` (`:2915-2932`), `:2968`, `:3056-3072`, `:19407-19520`, `:9549-9668`, `:9220`, `:9464`; `json_pointer.py:1-70`; the five run_102 output files named (the `run_protocol.json` copy not opened; its hash is on every index entry).
