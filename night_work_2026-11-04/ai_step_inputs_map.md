# AI step inputs map (read-only analysis, 2026-11-05)

Scope: every model call the research workflow makes, and exactly what code puts in front of each one.
Paths: SR = `strategy-research/`, RP = `SR/workflow/run_phase1_research.py`. Line numbers are from this checkout.
Sizes: lines / characters (Python `len`, about the same as bytes); tokens are estimated as chars / 4.
"Sample" means a run-specific file whose size changes from run to run. Its size comes from the named example file,
because this checkout's `SR/runs/` stops at run_060.
Flag set used for every total ("tour flag set"): every `orchestrator:` flag in `SR/config/campaign_config.yaml:88ff`
is ON except `deviation_gate`, `zero_trade_windows_not_computed` and `extra_cards_at_1a`. The committed values are ignored.

## 0. How a prompt is built (applies to every call below)

- **Where calls are made.** Only RP makes model calls. A grep for `claude_agent_sdk` / `query(` / `genai` across
  `SR/workflow` and `SR/tools` finds `query(` at RP:1454 (stage worker), RP:4668 (`_invoke_reader_llm`) and
  RP:4844 (`_invoke_analyst_llm`), plus the Gemini call at RP:1628. Elsewhere the SDK appears only in comments
  (`tools/data_availability_gate.py:63`, `tools/stamp_protocol.py:13`, `tools/protocol_resolution.py:16`).
  `workflow/run_campaign.py` and `tools/decide_next.py` import no model SDK.
- **The stages are closed-book.** `_stage_agent_options` (RP:1174-1254) sets `tools=[]` (RP:1239),
  `setting_sources=[]`, `strict_mcp_config=True`, auto-memory off and an empty temp cwd. The model has no file tool,
  so it cannot open any path. Everything it sees is pasted by code (docstring RP:1182-1225). The one exception is
  the analyst (section 1.6), which gets seven query tools over the run's data and nothing else.
- **Stage prompt assembly.** `_build_stage_prompt` (RP:1030-1129) works as follows:
  1. It pastes the stage's `SKILL.md` in full (RP:1048-1050, map RP:1019-1027) under "PERSONA AND RULES".
  2. It pastes the whole handoff dict as YAML (`yaml.dump(handoff)`, RP:1087), with objective, constraints,
     every input path and its reason, and injected_context.
  3. It pastes every `required_inputs` and `optional_inputs` file **in full**, each under `--- CONTENT OF <path> ---`
     (RP:1053-1061). A required file that is missing raises (RP:1062-1063). An optional file that is missing is
     skipped with a warning (RP:1064-1078).
  4. It adds the B7 sentence for B7 stages (RP:1080-1083, text RP:3109-3113).
  5. It adds a fixed output and YAML-format frame of about 1,264 characters (RP:1093-1112). With B7 the frame is
     about 1,435.
  The only filtered input is `config/criterion_menu.yaml`, through `_prompt_input_content` (RP:4386-4392), and only
  while `forecast_ic_horizons` is off. Under the tour flag set it is pasted unchanged.
- **Handoff mutation before the call.** In order, `async_invoke_agent` (RP:9671-9748) applies:
  - `_apply_b7_mandatory_inputs` (RP:3116)
  - `_apply_closed_book_inputs` (RP:3255; table RP:3167-3214)
  - `_apply_exclusion_digest_input` (RP:3775)
  - `_apply_stale_input_path_fix` (RP:3872)
  - `_apply_config_direct_authoring_context` (RP:9036)
  - `_apply_decide_next_context` (RP:8455)
  - `_apply_brief_hypotheses_context` (RP:8615)
  - `_apply_regroup_record_context` (RP:8998)
  - `_apply_retired_routing_review_context` (RP:7891)
  - the 1b retry, nearest-build and start-config helpers (RP:9724-9735)
  - `_apply_claim_tests_context` (RP:17409)
  - `_apply_variant_shape_retry_context` (RP:18856)

  The base handoff is the template in `SR/workflow_artifacts/templates/handoffs/`, which `setup_run.py:109-118`
  copies into each run. Some handoffs are written by code instead (noted per call).

## 1. Every AI call and what goes into its prompt

### Which calls exist and which run under the tour flag set

| # | Call | Code | Model | Reached under tour flags? |
|---|---|---|---|---|
| 1 | 1a hypothesis_generation | STAGE_CONFIGS RP:157-162 → run_claude_worker RP:1425 | stage_models: sonnet (`campaign_config.yaml:879`) | yes, except composition runs, which are written by code (RP:20068-20080, RP:6121) |
| 1r | 1a claim retry (same stage, called again) | RP:17765-17771, context RP:17448-17460 | same | when the claim check refuses (at most 1, RP:17397) |
| 2 | 1b strategy_config_authoring | RP:170-174 | sonnet (`campaign_config.yaml:880`) | yes, except composition runs and exact-config briefs (RP:20081-20083) |
| 3 | Step 2 innovation_expansion | RP:175-183 | haiku default (RP:1140) | yes, except composition runs and exact-config step 2 (RP:20084-20086) |
| 4 | Claim revision (after 1b) | `_claim_revision_after_1b` RP:18319, called RP:20218 → `_claim_llm_call` RP:17989 → `_invoke_reader_llm` RP:4660 | haiku default (no model passed, RP:4668) | only when no test reads the block, once per run (RP:17925-17938) |
| 5 | Analyst, lens `forecast` | `_run_analyst_stage` RP:5323 → `run_analyst_worker` RP:4885 → `_invoke_analyst_llm` RP:4834 | `orchestrator.analyst.model` = sonnet (`campaign_config.yaml:845`) | yes, every backtested run (RP:20175-20184) |
| 6 | Analyst, lens `trade_efficiency` | same | same | yes |
| 7 | Campaign review | RP:225-229; handoff written by `_write_retired_review_handoff` RP:7815 | haiku default | only when `review_every_n_runs` (6, `campaign_state.yaml:641`) unreviewed runs have piled up (RP:7759-7787, RP:7867) |
| 8 | Step 3 validation | RP:184-197 | haiku | **no**: skipped under config_direct_authoring (RP:20229-20230) |
| 9 | Step 5a backtest_specification (LLM form) | RP:198-202 | haiku | **no**: a tool stage under config_direct_authoring (RP:9676-9679) |
| 10 | verdict_interpreter | RP:217-221 | haiku | **no**: refused under grid_evaluation (RP:19972-19977) |
| — | Gemini engine (`run_gemini_worker` RP:1576) | — | gemini-2.5-flash-lite | **dead**: every template and every code-written handoff sets `assigned_engine: claude` |
| — | decide-next | `tools/decide_next.py` | none | code only, no model call |
| — | analyst reading review | RP:5176 | none | code only |
| — | 1a-1b claim match, power check | RP:17900ff | none | code only |

**Total under the tour flag set: 7 model-call kinds (rows 1, 1r, 2, 3, 4, 5, 6, 7).** Calls 8-10 exist in STAGE_CONFIGS
but are not reached. Out of scope, because the workflow never calls them: `SR/engineering/roadmap/E-032/artifacts/s1_measure_idea_generation.py`
(an offline script that imports the SDK) and the parked LLM review in `engineering/roadmap/E-068/review_measurement/`
(RP:17939-17941 says "Nothing here calls it").

Retries per call:
- **YAML or format retry.** Every stage call can repeat once with an error note and its previous answer appended
  (RP:862-918, RP:1114-1121). The repeat costs the full prompt again plus the previous answer.
- **SDK misclassification retry.** Every stage call can also repeat once with the prompt unchanged (RP:877-887).
- **Analyst retry.** The analyst repeats once with `retry_section` appended (RP:5011, `tools/analyst_session.py:1857`).

### 1.1 Step 1a, hypothesis_generation (operator brief run)

Base handoff: `templates/handoffs/research_brief_to_hypothesis.yaml` (21 lines / 1,301 chars). Everything below is pasted by code. The model cannot open anything.

| Input | Included by | How | Size (lines / chars, ~tok) |
|---|---|---|---|
| `skills/hypothesis-design/SKILL.md` | RP:1048-1050 (`_SKILL_MAP` RP:1020) | full, as "PERSONA AND RULES" | 84 / 7,902 (~2.0k) |
| handoff YAML dump | RP:1087 | full | ~2,756 (~0.7k) |
| `artifacts/research_brief.yaml` | template :7-8 | full | sample run_060: 170 / 8,209 (~2.1k) |
| **`config/indicator_library.yaml`** | template :9-10 (required) | full | 321 / 16,096 (~4.0k) |
| `config/criterion_menu.yaml` | `_apply_config_direct_authoring_context` RP:9066-9070 | full (D-186 filter off: RP:4389-4391) | 307 / 17,937 (~4.5k) |
| `skills/hypothesis-design/BRIEF_HYPOTHESES.md` | `_apply_brief_hypotheses_context` RP:8615-8635 (brief run only, file `brief_hypotheses_context.yaml` present) | full | 84 / 3,570 (~0.9k) |
| `artifacts/brief_hypotheses_context.yaml` | same, RP:8631 | full | sample fixture run_098: 7 / 172 |
| `skills/hypothesis-design/CLAIM_TESTS.md` | `_apply_claim_tests_context` RP:17425-17429 | full | 238 / 16,563 (~4.1k) |
| `skills/hypothesis-design/CLAIM_TESTS_TRADE.md` | same, RP:17432-17437 (under analyst flag) | full | 136 / 8,375 (~2.1k) |
| `artifacts/tried_ideas.yaml` (optional) | `_apply_exclusion_digest_input` RP:3798-3813: derived from `campaign_record/campaign_memory.yaml` at each call and written into the run | full | 296 / 9,965 (~2.5k) as derived now (24 runs in memory, cap 200 rows: `tools/campaign_memory.py:911`) |
| `artifacts/run_context.yaml` (optional) | template :13-14 | full, only on escalation runs | sample run_060: 95 chars |
| output frame | RP:1093-1112 | fixed text | ~1,264 |

Variants of this call:
- **Decide-next candidate run.** `DECIDE_NEXT_CANDIDATES.md` (52 / 3,410) is added (RP:8455-8471) instead of
  BRIEF_HYPOTHESES.md and its context file (RP:8623).
- **Pre-filled claim.** `PREFILLED_CLAIM.md` (21 / 1,494) is added when the brief carries `candidate.claim` (RP:17440-17445).
- **Claim retry (1r).** The inputs are the same, plus `injected_context.claim_check_error` (a few hundred chars, RP:17448-17460).
- **Never added to 1a:** `CLAIM_TESTS_EXECUTION.md`. A grep finds it only in `tools/analyst_session.py:429`, even
  though `hypothesis-design/SKILL.md:24` has a branch "When CLAIM_TESTS_EXECUTION.md is among your inputs".
- **Stale-path fix.** `_apply_stale_input_path_fix` (RP:3907-3912) is a no-op today. The template no longer
  lists the two stale paths it fixes.
- **Not given to 1a:** COMPONENT_CATALOG.md, STRATEGY_DESIGN_GUIDE.md, the KB, campaign_state, pre_registration.yaml.
  `hypothesis_generation` is not a B7 stage (RP:3092-3108).

### 1.2 Step 1b, strategy_config_authoring

Base handoff: `templates/handoffs/hypothesis_to_strategy_config_authoring.yaml` (47 / 2,954).

| Input | Included by | How | Size |
|---|---|---|---|
| `skills/strategy-config-authoring/SKILL.md` | RP:1048, RP:1022 | full | 317 / 24,130 (~6.0k) |
| handoff dump | RP:1087 | full | ~3,562 |
| `artifacts/hypothesis_card.yaml` | template :15-16 | full (1a's card, including `library_lookup`) | sample fixture run_098: 86 / 8,192 (~2.0k) |
| `docs/STRATEGY_DESIGN_GUIDE.md` | template :17-18 | full | 659 / 49,443 (~12.4k) |
| `docs/COMPONENT_CATALOG.md` | template :19-20 | full | 183 / 29,733 (~7.4k) |
| `docs/DATA_AVAILABILITY.md` (optional, tracked, so always present) | template :22-23 | full | 90 / 4,974 (~1.2k) |
| `artifacts/pre_registration.yaml` | B7 RP:3088-3134 | full | sample run_060: 63 / 2,625 |
| `artifacts/user_brief_verbatim.yaml` | B7 | full | sample run_057: 151 / 7,913 (~2.0k) |
| `skills/quant-fundamentals/SKILL.md` | closed-book RP:3162-3166, RP:3204 | full | 172 / 10,630 (~2.7k) |
| `skills/strategy-config-authoring/NEAREST_BUILD.md` | RP:16775-16786 | full | 39 / 2,354 |
| `skills/strategy-config-authoring/CLAIM_NOTE.md` | RP:17418-17423 | full | 14 / 817 |
| `findings_carryover.yaml`, `run_context.yaml` (optional) | template :24-27 | full, when present | — |
| `START_FROM_CONFIG.md` (18 / 1,323) + `start_config.json` + `start_block_manifest.yaml` | RP:16806-16835 | full, only for a reader side-finding brief | — |
| B7 sentence + frame | RP:1080-1083, RP:1093 | fixed | ~1,435 |
| retry messages | RP:16749-16769, RP:17259-17283 | injected_context, retry only | — |

### 1.3 Step 2, innovation_expansion

Base handoff: `templates/handoffs/hypothesis_to_innovation_expansion.yaml` (22 / 1,139).

| Input | Included by | How | Size |
|---|---|---|---|
| `skills/innovation-expansion/SKILL.md` | RP:1023 | full | 364 / 23,297 (~5.8k) |
| handoff dump | RP:1087 | full | ~2,714 |
| `artifacts/research_brief.yaml` | template :7-8 | full | sample 8,209 |
| `artifacts/hypothesis_card.yaml` | template :9-10 | full | sample 8,192 |
| **`config/indicator_library.yaml`** | template :11-12 (required) | full | 321 / 16,096 (~4.0k) |
| `config/coin_universe.yaml` | closed-book RP:3168-3172 | full | 229 / 9,781 (~2.4k) |
| `artifacts/backtest_spec.yaml` | RP:9071-9076 | full | sample fixture run_098: 51 / 4,086 |
| `docs/STRATEGY_DESIGN_GUIDE.md` | RP:9082-9088 | full | 659 / 49,443 (~12.4k) |
| `docs/COMPONENT_CATALOG.md` | RP:9089-9095 | full | 183 / 29,733 (~7.4k) |
| `artifacts/tried_ideas.yaml` (optional) | RP:3798-3813 | full | 296 / 9,965 |
| `artifacts/refinement_notes.yaml` (optional) | template :14-15 | only in a refine loop (validation is unreached, so effectively never) | — |
| frame | RP:1093 | fixed | ~1,264 |
| retry message | RP:18856-18880 | injected_context, retry only | — |

### 1.4 Claim revision (one call after 1b, under claim_tests)

The handoff is built by code in `_claim_revision_prompt` (RP:18043-18061) and assembled by the same `_build_stage_prompt`
(RP:18060-18061) with the skill `claim-revision` (RP:17944).

| Input | Included by | How | Size |
|---|---|---|---|
| `skills/claim-revision/SKILL.md` | RP:18061 | full | 48 / 2,566 |
| handoff dump (objective, request message, floor facts) | RP:18044-18059 | full | ~1,100 |
| `artifacts/hypothesis_card.yaml` | RP:18049-18050 | full | sample 8,192 |
| `artifacts/block_manifest.yaml` | RP:18051-18053 | full | sample fixture run_098: 7 / 343 |
| `skills/hypothesis-design/CLAIM_TESTS.md` | RP:18054-18055 (`_claim_guide_rel` RP:17958-17965) | full | 238 / 16,563 |
| frame | RP:1093 | fixed | ~1,264 |

### 1.5 Campaign review (verdict_routing_retired form)

Under the tour flags the template `templates/handoffs/campaign_review.yaml` is **not used**. Code writes the
handoff (RP:7815-7864) when `_retired_review_route` fires (RP:7867-7882).

| Input | Included by | How | Size |
|---|---|---|---|
| `skills/campaign-review/SKILL.md` | RP:1025 | full | 245 / 15,043 (~3.8k) |
| handoff dump | RP:7835-7861 | full | ~2,550 |
| `artifacts/campaign_review_digest.yaml` | RP:7841-7844; written by `_write_review_digest` RP:7789-7812 from `campaign_record/campaign_memory.yaml` | full: every run since the last review in full, plus counts | **estimate** 42k-70k chars (6 entries; memory entries run 4.2k / 7.1k / 17.4k chars min / median / max; the last 6 entries total 69.4k) |
| `artifacts/research_brief.yaml` | RP:7845-7846 | full | sample 8,209 |
| `campaign_record/campaign_knowledge_base.yaml` (optional) | RP:7848 | full | 2,003 / 107,884 (~27.0k) |
| `artifacts/pre_registration.yaml`, `artifacts/user_brief_verbatim.yaml` | B7 RP:3092-3108 | full | samples 2,625 + 7,913 |
| `skills/campaign-review/RETIRED_ROUTING.md` | RP:7891-7907 | full | 61 / 3,662 |
| `skills/quant-fundamentals/SKILL.md` | closed-book RP:3213 | full | 172 / 10,630 |
| B7 sentence + frame | | fixed | ~1,435 |

### 1.6 Analyst (two sessions per run: lens `forecast`, lens `trade_efficiency`)

The prompt is built by `tools/analyst_session.build_prompt` (`analyst_session.py:417-436`), called from RP:4905-4907. It does not use
`_build_stage_prompt`, a handoff or `_SKILL_MAP` (RP:20070-20072). It is a different path from the other stages.

| Input | Included by | How | Size |
|---|---|---|---|
| `skills/analyst/SKILL.md` | `analyst_session.py:423` | full | 396 / 28,906 (~7.2k) |
| `skills/analyst/<lens>.md` | :423 | full | forecast 22 / 1,807; trade_efficiency 28 / 2,185 |
| Run context (`run_context`, :382-414) | :424 | code text: coins, timeframe, windows, horizon, sizing line + base config in full + `variant_patches.yaml` in full + **the run's book** (code-built from grid, idea_status, profit bars, claim tests, :152-380) + `config/cost_model.yaml` in full | measured on fixture run_098: 389 / 24,316 (~6.1k), including cost_model 17,252 and the book 4,676 |
| Component and op catalogue | :425-426 → `tools/catalogue_section.py` | **rendered extract**: the rows between the CATALOG markers of COMPONENT_CATALOG.md cut to one line each, plus the op tables of STRATEGY_DESIGN_GUIDE.md "## Transform ops" | 60 / 11,588 (~2.9k) |
| `docs/DATA_DICTIONARY.md` | :427-428 | full | 696 / 72,484 (~18.1k) |
| CLAIM_TESTS.md, CLAIM_TESTS_TRADE.md, CLAIM_TESTS_EXECUTION.md | :429-430 | full | 16,563 + 8,375 + 1,113 |
| Memory view | :431-432; `tools/analyst_memory_view.load_memory_view` (:447-474) over campaign_memory.yaml + confirmations.yaml + each run's base config | YAML dump of a derived, number-masked view | 696 / 20,855 (~5.2k) as derived now |
| Tool list | :433-434 | names of the 7 tools | ~0.3k |
| **Model reads through tools** | `_analyst_tools` RP:4794-4817; seven query tools over the run's bars and trades (`tools/analyst_queries.QueryEngine`, RP:4899-4900) | results added turn by turn, not pasted up front | up to 40 turns, $3, 15 min (RP:4702) |

The whole first prompt was measured on fixture run_098: **186,752 chars (~46.7k tokens) for `forecast` and
187,130 (~46.8k) for `trade_efficiency`**. Tool results come on top of that.

### 1.7 Calls that exist but are not reached under the tour flags (for completeness)

- **Validation.** Inputs: skill `quant-validation` (12,082), template `innovation_expansion_to_validation.yaml`
  (expanded card, `human_resolution.yaml`), B7 files, `config/cost_model.yaml` (closed-book RP:3174-3177), and in a
  refine loop `innovation_notes.yaml` and DATA_AVAILABILITY.md (RP:3178-3183).
- **5a LLM.** Inputs: skill `backtest-engineering` (13,862), template `validation_to_backtest_specification.yaml`
  (expanded card, validation_protocol, **COMPONENT_CATALOG.md** :16), closed-book `innovation_notes.yaml`,
  DATA_AVAILABILITY, findings_carryover, run_context and quant-fundamentals (RP:3185-3196), and B7.
- **verdict_interpreter.** Inputs: skill (56,075, the largest skill), template (protocol_result, validation_protocol,
  backtest_spec, research_brief), closed-book `pass_rule_evaluation.yaml`, coin_universe, campaign_state, the
  trade-diagnostics summary and quant-fundamentals (RP:3198-3212), regime report (RP:10207-10226), and B7.

## 2. Totals per AI call (tour flag set)

The counts list files pasted in full plus generated sections. The skill, handoff dump and frame are counted separately.
Run files use the samples above.

| Call | Skill (chars) | Handoff + frame | Files / sections pasted | Total chars | ~Tokens |
|---|---|---|---|---|---|
| 1a operator brief | 7,902 | 2,756 + 1,264 | 8 (brief, **indicator library**, criterion menu, BRIEF_HYPOTHESES, brief context, CLAIM_TESTS, CLAIM_TESTS_TRADE, tried_ideas) | **93,341** | **~23.3k** |
| 1a decide-next candidate (+ pre-filled claim) | 7,902 | 2,796 + 1,264 | 8 (brief, **indicator library**, menu, CLAIM_TESTS, CLAIM_TESTS_TRADE, DECIDE_NEXT, PREFILLED_CLAIM, tried_ideas) | 94,578 | ~23.6k |
| 1a claim retry | same as 1a | + claim_check_error | same | ~93.5k-95k | ~23.5k |
| 1b | 24,130 | 3,562 + 1,435 | 9 (card, design guide, **component catalogue**, DATA_AVAILABILITY, pre_reg, user_brief, quant-fundamentals, NEAREST_BUILD, CLAIM_NOTE) | **146,393** | **~36.6k** |
| Step 2 | 23,297 | 2,714 + 1,264 | 8 (brief, card, **indicator library**, coin_universe, backtest_spec, design guide, **component catalogue**, tried_ideas) | **163,193** | **~40.8k** |
| Claim revision | 2,566 | ~1,082 + 1,264 | 3 (card, block manifest, CLAIM_TESTS) | ~30,200 | ~7.5k |
| Analyst, forecast | 28,906 + 1,807 | — (no handoff) | 9 sections (run context incl. base config, patches, book, cost model; catalogue extract; data dictionary; 3 claim-test files; memory view; tool list) + tool turns | **186,752** (first prompt) | **~46.7k** + tool results |
| Analyst, trade_efficiency | 28,906 + 2,185 | — | same | 187,130 | ~46.8k + tool results |
| Campaign review | 15,043 | ~2,550 + 1,435 | 7 (digest, brief, KB, pre_reg, user_brief, RETIRED_ROUTING, quant-fundamentals) | **~203k-230k** (digest 42k-70k) | **~51k-58k** |

The calls that run on every backtested run add up to about 1a 23k + 1b 37k + step 2 41k + analyst 2 × 47k ≈ **195k
input tokens per run**, before retries and analyst tool turns.

## 3. Indicator library vs component catalogue

### 3.1 What each contains

| | `SR/config/indicator_library.yaml` | `SR/docs/COMPONENT_CATALOG.md` |
|---|---|---|
| Size | 320 lines / 16,182 bytes | 182 lines / 29,733 bytes |
| Unit | 15 "indicator" entries, keyed by `id` (:26-303) | 28 component classes (:5-7), rows between `<!-- CATALOG:START/END -->` (:67-117) |
| Fields | `id`, `category` (oscillator / trend_following / volatility / volume_flow / order_book_imbalance / sentiment / structural_rate), `known_regime_affinity` {trending, ranging, high_vol}, `typical_lag_bars`, `crowding_risk`, `data_requirements`, `edge_source_compatibility`, `campaign_empirical_results`, `notes` (vocabulary :10-17) | class, params (defaults), exact output formula, range & sign, **kind** (graded / on/off / constant / regime measure, :29-39), units, warmup, data & NaN, notes; plus a naming rule (:41-59), variant patterns (:119), feeds (:144), other config names (:171) |
| Nature | Domain opinion about indicator *families*: how crowded they are, which regime suits them, which edge source. No class names. A grep for "Component" in the file finds nothing. | The engine's actual inventory. Every class "lives in `strategies.strategy_components`" (:4-7). "A class name that is not a row below is invented." |
| Empirical part | `campaign_empirical_results: []` in all 15 entries. The header (:3-5) says these are "populated via the KB". No code writes them (a grep for `campaign_empirical_results` finds only `tests/test_improvement04_acceptance.py:178-212`, which **asserts** they stay empty). | n/a |
| Cross-reference | none to the catalogue | none to the library (a grep for "library" in COMPONENT_CATALOG.md and STRATEGY_DESIGN_GUIDE.md finds nothing) |

### 3.2 Who writes each

- **Indicator library.** Hand-written seed: "Improvement 04 — Indicator Knowledge Library ... Domain-knowledge seed ...
  Version 1.0" (:1-8). No code in `SR/workflow` or `SR/tools` writes it. The only `.py` mention outside tests is a
  docstring (`tools/build_exclusion_digest.py:136`). The checkout is a shallow clone (188 commits), so the authoring
  history is not visible here.
- **Component catalogue.** Hand-maintained doc. No code writes it (the grep finds only readers). One test pins its
  rendered extract: `tests/test_catalogue_section.py`.

### 3.3 Which AI calls receive each (tour flag set)

| Call | Indicator library | Component catalogue |
|---|---|---|
| 1a | **yes**, in full, required (template `research_brief_to_hypothesis.yaml:9-10`; pinned by `tests/test_d195_skills_handoffs.py:111`) | no |
| 1b | no | **yes**, in full (template `hypothesis_to_strategy_config_authoring.yaml:19-20`) |
| Step 2 | **yes**, in full (template `hypothesis_to_innovation_expansion.yaml:11-12`; test :122) | **yes**, in full (RP:9089-9095, flag-on only) |
| Claim revision | no (the pasted card carries 1a's `library_lookup` values) | no |
| Analyst | no | **yes, as a rendered one-line-per-row extract** (`tools/catalogue_section.py`, `analyst_session.py:425-426`) |
| Campaign review | no | no |
| (unreached) 5a LLM | no | yes (`validation_to_backtest_specification.yaml:16`) |
| (unreached) verdict_interpreter | no | named in a constraint only (RP:9930), file not pasted |

### 3.4 Which code reads each (beyond prompts)

- **Indicator library: no code reads the file.** A grep for `indicator_library` in all `.py` files outside
  `tests/` and `archive/` finds only the docstring at `tools/build_exclusion_digest.py:136`. Tests read it:
  `tests/test_improvement04_acceptance.py:25`.
- **Component catalogue: read by code in four places.**
  - `tools/forecast_rules.py:48`, `:68` `catalog_rows`, `:86` `on_off_classes` parse the Kind column.
  - That parse drives the D-051 check on 1b's base config (RP:16535-16536) and on every step-2 variant at 5a
    (RP:2849-2850, RP:2920-2922). These are binding checks that cause retries or pauses.
  - `tools/config_vehicle.py:255`, `:268` uses it for the analyst's vehicle check.
  - `tools/catalogue_section.py:8-9` uses it to render the analyst's catalogue section.

### 3.5 Output fields produced from the library, and whether code reads them back

| Field (who writes it) | Instruction | Code reader | Effect |
|---|---|---|---|
| `hypothesis_card.library_lookup.indicator_id` (1a) | `hypothesis-design/SKILL.md:34`, `:76` ("Code groups tried ideas by `indicator_id`") | `tools/build_exclusion_digest.classify_family` :151-154. It runs (a) in `build_digest` (:359, :498), which only the CLI calls (`main` :532; note :515 "Regenerate on demand"); (b) in `legacy_family_lookup` :461-478, called by `tools/decide_next._digest_advisory` :1576-1590 (called :1800); the digest file is passed in by `run_campaign.py:5026-5027`; (c) in the offline `tools/replay_repeat_gate.py:521` | **information only.** decide_next records `digest_advisory` and "never refuses" (`decide_next.py:39-41`, :1577-1579). The tried-ideas view 1a and step 2 get has "No family grouping: an idea's identity is its hypothesis_id" (`campaign_memory.py:926`), so it does not group by indicator_id. |
| `library_lookup.regime_affinity_for_target`, `library_lookup.crowding_risk` (1a) | SKILL.md:76 | **none** (grep of `.py` in workflow/ and tools/) | read only by later prompts that receive the card (1b, step 2, claim revision). The readers' copy of the card drops `library_lookup` (`tools/explore_confirm.py:123-129`). |
| `expanded_hypothesis_card.yaml` `library_category`, `data_requirements`, `diversity_axis`; `innovation_notes.yaml` `diversity_audit` (step 2) | `innovation-expansion/SKILL.md:79-93`, `:322-325` | **none under the tour flags.** The expanded card is read only by `_record_variant_selection` RP:9258, on the LLM 5a path (called RP:20266, unreached under config-direct), and only for variant ids. A grep of `tools/` and `run_campaign.py` for these field names finds nothing. | unused by code |

Observed in sample cards: `indicator_id` holds values outside the library's ids, e.g. `"none_nearest_moving_average_crossover"`
(fixture `tests/fixtures/run_viewer/runs/run_098/artifacts/hypothesis_card.yaml:34`). Cards also carry keys the current skill
does not list (`affinity_justification`, `prior_campaign_failures`, `indicator_note`: run_098 :36-37,
`campaign_record/queued_cards/run_094/hypothesis_card_3.yaml:59-61`, `runs/run_060/artifacts/hypothesis_card.yaml:34-36`).

### 3.6 Overlap (matched by name and description; no file or code links the two)

| Library `id` | Catalogue class(es) of the same indicator |
|---|---|
| rsi_mean_reversion, rsi_momentum | `RSIPullbackComponent` (:85, (50 - RSI) × sf) |
| moving_average_crossover | `EMASpreadComponent` (:86, fast vs slow MA), `EMADiff` |
| keltner_channel_trend, keltner_channel_mean_reversion | `KeltnerBreakoutComponent` (distance from EMA in ATR units) |
| macd | `EMADiff`, `MacdHistogramComponent`, `MacdHistogramCrossoverComponent` |
| funding_rate_extreme | `FundingRateMeanReversionComponent`, `FundingRateComponent` |
| fear_greed_index_contrarian | `FearGreedContrarianComponent`, `FearGreedComponent` |
| volume_ratio_momentum | partial: `VolumeExpansionHedgeComponent` (:104, volume vs its average, on/off, never positive) |
| atr_volatility_filter | partial: no ATR class; volatility classes `VolatilityPercentileRegimeComponent`, `VolatilityFromStdDevComponent` |
| **Library only (no class):** stochastic_oscillator, bollinger_bands, on_balance_volume, open_interest_divergence, order_book_imbalance (its note says the feed is unavailable) | — |
| **Catalogue only (no library entry):** RSquaredRegime, EfficiencyRatioRegime, VolatilityPercentileRegime, ADXDirectional, VarianceRatio, PriceEvolution, PriceEvolutionOnPeriod, MacroTrendFilter, MovingAverageDistance, DonchianBreakout, MomentumDivergence, SmaTrendLongOnly, GatedSmaTrendLongOnly, BuyAndHold, PriceOverextensionHedge, VolatilityFromStdDev, WhaleLargeTradeImbalance | — |

## 4. Inputs shared across calls, and inputs a call's instructions do not use

### 4.1 Inputs in more than one call (tour flag set)

| Input | Calls (all in full unless noted) |
|---|---|
| `artifacts/research_brief.yaml` | 1a, step 2, campaign review |
| `artifacts/hypothesis_card.yaml` | 1b, step 2, claim revision; the analyst gets only the card's statement inside the book |
| `config/indicator_library.yaml` | 1a, step 2 |
| `docs/COMPONENT_CATALOG.md` | 1b, step 2 (full); analyst (rendered extract) |
| `docs/STRATEGY_DESIGN_GUIDE.md` | 1b, step 2 (full); analyst (op tables only, through catalogue_section) |
| `skills/hypothesis-design/CLAIM_TESTS.md` | 1a, claim revision, analyst |
| `skills/hypothesis-design/CLAIM_TESTS_TRADE.md` | 1a, analyst |
| `skills/quant-fundamentals/SKILL.md` | 1b, campaign review |
| `artifacts/pre_registration.yaml`, `artifacts/user_brief_verbatim.yaml` (B7) | 1b, campaign review |
| `artifacts/tried_ideas.yaml` | 1a, step 2 (derived again and rewritten at each call, RP:3801-3803) |
| `campaign_record/campaign_memory.yaml`, as three different code-derived views | tried_ideas (1a, step 2), the analyst's memory view, the campaign review digest |

The two largest docs, STRATEGY_DESIGN_GUIDE (49k) and COMPONENT_CATALOG (30k), are pasted in full into both 1b and
step 2: about 79k chars (~20k tokens) per call.

### 4.2 Inputs the call's own instructions do not use

Method: grep of the call's SKILL.md and of the addenda in the same prompt for the file name and its field names.
The counts were taken with `grep -c` (listed in section "Not checked" where coverage is partial).

| Call | Input | Finding |
|---|---|---|
| 1a | `indicator_library.yaml` (16.1k chars, ~17% of the 1a prompt) | hypothesis-design/SKILL.md uses it only to fill `library_lookup` (:34, :76; 3 fields). No addendum mentions it: a grep of BRIEF_HYPOTHESES, DECIDE_NEXT_CANDIDATES, CLAIM_TESTS, CLAIM_TESTS_TRADE and PREFILLED_CLAIM for "library\|indicator" finds nothing. The skill never uses the library's `category`, `typical_lag_bars`, `data_requirements`, `edge_source_compatibility`, `notes` or (empty) `campaign_empirical_results`. Of the 3 output fields, code reads only `indicator_id`, for information only (3.5). |
| 1a | `tried_ideas.yaml` | the skill mentions it once, for the `approximation` rows (SKILL.md:23). The rest of its use is only the reason text in the handoff (RP:3324-3333). |
| 1a | (missing input) | SKILL.md:24 branches on `CLAIM_TESTS_EXECUTION.md`, which code never gives 1a. |
| 1b | `pre_registration.yaml`, `user_brief_verbatim.yaml` | strategy-config-authoring/SKILL.md never names them (grep 0). Only the B7 sentence (RP:3109-3113) points to them. |
| Step 2 | `indicator_library.yaml` | used by IMPROVEMENT 04 (SKILL.md:55-103). Under config-direct, design variants are exempt from its rejection and the asset variant carries diversity (:73-77, :300-304). The fields it asks for are still required (:308-311, :324-325), but no code reads them (3.5). |
| Step 2 | STRATEGY_DESIGN_GUIDE.md, COMPONENT_CATALOG.md | referred to once in the config-direct section (SKILL.md:301). The skill's "Context rule" (:364) lists the inputs to use and leaves both out ("Do not read other files unless explicitly required"). |
| Campaign review | `pre_registration.yaml`, `user_brief_verbatim.yaml` | campaign-review/SKILL.md and RETIRED_ROUTING.md never name them (grep 0); only the B7 sentence does. |
| Campaign review | (the skill's own context rule) | campaign-review/SKILL.md:239 says "Read campaign_state.yaml and research_brief.yaml only", but campaign_state is not an input in this form. RETIRED_ROUTING.md:18-25 tells the model not to use it. |
| Analyst | all sections | each one is named in analyst/SKILL.md:18-40, including CLAIM_TESTS_EXECUTION, the cost model and variant patches. |
| Claim revision | all three files | each one is named in claim-revision/SKILL.md. |

## Questions this answers for the operator

- **Stop 07, "why step1a get the indicator library"** and **stop 11, "i do not understand why 1a would havr access to indicator library"**:
  - It comes from the template `research_brief_to_hypothesis.yaml:9-10`, whose reason is "the entries the card's
    library_lookup.indicator_id can name, with their regime_affinity and crowding_risk".
  - Its only use in 1a's instructions is the `library_lookup` block (hypothesis-design/SKILL.md:34, :76).
  - Its cost is about 16k chars, ~4k tokens, about 17% of the 1a prompt (§2).
  - The values 1a writes from it have no binding code consumer. `indicator_id` reaches only an information-only
    legacy family lookup in decide-next; the other two fields reach no code at all (§3.5, §4.2 row 1).
- **Stop 11, "the AI steps may have access to too many docs"**:
  - §1 lists every input per call, and §2 gives the totals: 1a ~23k, 1b ~37k, step 2 ~41k, analyst ~47k per lens,
    campaign review ~51-58k tokens.
  - §4.1 lists the docs pasted into several calls. The design guide and catalogue in both 1b and step 2 come to ~20k tokens per call.
  - §4.2 lists the inputs a call's own skill does not use.
  - Fact: no stage can open a doc itself; everything is pasted by code (§0, RP:1174-1254).
- **Stop 11, "usage of indicator library (especially comparing to component catalog)"**: see §3.
  - **The library** is a hand-written opinion file about 15 indicator families: crowding, regime fit, edge source.
    No code reads it. It goes to 1a and step 2.
  - **The catalogue** is the engine's list of 28 real classes with exact formulas and kinds. Code reads it for
    binding checks (D-051 at 1b and 5a, the analyst vehicle check). It goes to 1b, step 2 and (as an extract) the analyst.
  - Their overlap is partial: 8 library ids map to catalogue classes, 5 have none, and 17 classes have no library
    entry (§3.6).
- **Stop 07, "how much this step generate ideas" / skill rewriting**: not answered here. This map covers inputs only.

## Not checked

- **Run-specific file sizes are samples.** They come from run_060, run_057, fixture run_098 and the current
  `campaign_memory.yaml`; this checkout has no run after run_060. Real research briefs, cards and the review digest
  vary. The digest size is an estimate made from memory entry sizes, not a generated file.
- **Handoff dump sizes for claim revision and campaign review are approximations.** They were measured with
  placeholder strings of about the same length as the code's literals. The other handoff dumps were measured on the
  real templates after applying the code's own pure helpers in memory.
- **Not measured: analyst tool-result volume and retry-prompt sizes.** These are the turns after the first prompt,
  the YAML/format retries and the analyst `retry_section`.
- **"Not used by instructions" is a text grep only.** It does not show whether the model actually draws on a file.
  Run transcripts were not read.
- **The library-to-class mapping (§3.6) is my reading of names and descriptions.** No file defines it.
- **Not opened:** `guided_tour/` beyond the two "Operator remarks" sections, any "Inspector notes", `guided_tour/_post_tour/`,
  `local_data/`, and anything named holdout_sealed. No date from `campaign_data_policy.yaml` was read or written.
- **Side effect:** the read-only Python counting imported `SR/tools` modules. Before I switched to `-B`, this
  refreshed 10 git-ignored `.pyc` files in `SR/tools/__pycache__/`. Nothing else was written except this file.
