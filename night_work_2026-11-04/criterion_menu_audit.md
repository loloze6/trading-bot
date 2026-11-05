# Criterion menu audit (tour stop 08)

Read-only audit of `strategy-research/config/criterion_menu.yaml` (SR = `strategy-research/`), written 2026-11-05 on branch `ccr-fd96c37b-b5lc87` at commit `0319353e`. Nothing was edited, run or tested. Flag states are the ones in this checkout's committed `SR/config/campaign_config.yaml`.

The operator asked (tour stop 08, "Operator remarks"): *"Here the crierion menu is overloaded by comment line, is it normal ?"*. This file answers that question with facts. Sections 4 and 5 list material for the direction session. They do not take a position on the design challenges.

## Short answer

- **Share of comment lines:** 171 of the file's 306 lines are comment lines (56%), and they hold 67% of its bytes (11,957 of 17,937). A further 56 data lines are the prose of the `basis:` fields. Comments plus `basis` prose make up 227 lines (74%). Only 67 lines (22%) are YAML that defines a criterion.
- **Code does read the comments.** Step 1a (`hypothesis_generation`) receives the raw file text, comments included, as a prompt input whenever `orchestrator.config_direct_authoring` is on. One function also reads 7 comment lines as instructions to itself: the `# D-186 BEGIN/END/OFF` markers. Two tests pin comment text byte for byte. So the comments act as prompt text, not as inert notes (details in section 2.2).
- **Is it normal?** No other config file was measured, so this audit makes no comparison. For a file whose comments are pasted into a model's prompt, it means step 1a reads 148 comment lines of history, rationale and code pointers when the flag is off, and all 171 when `forecast_ic_horizons` is on. Some of those lines are stale (15 lines, plus 2 stale passages in `basis` data). Section 2.3 lists them.

## 1. Counts

Lines are classed as follows. **Data** is any non-blank line that does not start with `#`, including `basis: >` and its folded prose lines. **Comment** is any line whose first non-space character is `#`. **Blank** is an empty line. The file has no trailing (inline) comments.

| Section (lines) | Total | Data | of which `basis` prose | Comment | Blank | Comment share |
|---|---|---|---|---|---|---|
| Header (1-23, incl. the `criteria:` key) | 23 | 1 | 0 | 21 | 1 | 91% |
| `realized_edge_to_cost_ratio` (24-90) | 67 | 24 | 11 | 42 | 1 | 63% |
| `sign_consistent_by_era` (91-122) | 32 | 18 | 7 | 13 | 1 | 41% |
| `whole_test_sharpe_positive` (123-146) | 24 | 13 | 3 | 10 | 1 | 42% |
| `forecast_ic_median` (147-225) | 79 | 44 | 30 | 34 | 1 | 43% |
| `gated_beats_ungated` placeholder (226-238) | 13 | 0 | 0 | 12 | 1 | 92% |
| `code_added_criteria` header (239-254, incl. key) | 16 | 1 | 0 | 15 | 0 | 94% |
| `residual_ic` (255-286) | 32 | 18 | 3 | 14 | 0 | 44% |
| `profit_bars` (287-306) | 20 | 10 | 2 | 10 | 0 | 50% |
| **File** | **306** | **129** | **56** | **171** | **6** | **56%** |

- 5 of the comment lines are a bare `#` (separators: lines 4, 10, 16, 227, 233).
- YAML data that defines a criterion: 129 data lines, minus 56 `basis` prose lines, minus the 6 `basis: >` keys, leaves 67 lines.
- **What step 1a's prompt receives:** with `orchestrator.forecast_ic_horizons` off (the committed state), `_menu_text_for_prompt` removes the D-186 brackets. The prompt text is then 281 lines: 148 comment, 127 data, 6 blank. I reimplemented the filter and checked the result. It equals `SR/tests/fixtures/d186/criterion_menu_pre_d186.yaml` byte for byte. With the flag on, the prompt gets all 306 lines unchanged.

## 2. Comment blocks classified

### 2.1 Classification

The class definitions are the ones given in the task. Line ranges are inclusive. Some blocks are split where one block mixes classes. Abbreviations: `vce` = `SR/tools/verdict_criteria_evaluator.py`, `rpr` = `SR/workflow/run_phase1_research.py`, `rc` = `SR/workflow/run_campaign.py`.

| Lines | # | Class | Content | Evidence |
|---|---|---|---|---|
| 1-3 | 3 | HISTORY | Provenance: E-046b S2, card C; an anchor table with the "pick from this table" discipline | none |
| 4, 10, 16 | 3 | (separator) | bare `#` | none |
| 5-9 | 5 | LIVE RULE (incomplete) | Consumed by `evaluate_grid` via `menu`. A criterion may name only `id` plus overrides and get the rest backfilled, or be self-contained. | `vce:1785-1813` (`_resolve_grid_criteria`, `resolve_criteria_against_menu`: the criterion's fields win and the menu backfills; with no id the base is `{}`). Incomplete: the menu is also consumed by `rpr:8216` (`_pass_rule_from_card`), `rpr:8370` (`_pass_rule_from_menu_ids`), `rc:905-912` and `rc:1139-1144` (C5.1 lint), `SR/tools/decide_next.py:2594` (`_criteria_for_child`), `rpr:8289` (D-192 consistency), `rpr:6170` (`_code_added_criterion`), and the 1a prompt. |
| 11-15 | 5 | STALE | "Record shape": `{id, metric, source: window\|pooled, reducer: ..., reducer_arg, comparator, threshold, floor: {min_windows\|min_trades\|min_n_eff}, scale_free: true, symbol_reducer: ...}` | The enums still match the code: `vce:1091-1092` (`_VALID_GRID_SOURCES`, `_VALID_GRID_REDUCERS`) and `vce:1734`. But the shape leaves out keys the file now uses and code reads: `card_overridable`, `retired_for`, `horizon`, `horizon_allowed`, `statistic`, `max_p_value`, plus `basis`, `ratified` and `requires_flag`. It also leaves out source `profit_bars` (line 299; `vce:1642`, `vce:2246`). |
| 17-21 | 5 | STALE | "Do NOT add median_sharpe / max_abs_drawdown_pct / zero_trade_slot_pct ... a separate, not-yet-built file" | The campaign-wide profit-bar file exists: `SR/config/profitability_bars.yaml`, which this same menu cites at lines 55-56 and 82-83. No code enforces the "do not add" rule; no lint refuses these ids. |
| 25-28 | 4 | RATIONALE | Why `realized_edge_to_cost_ratio` is retired for blocks (lot-based unweighted means) | D-133, D-107, D-128 (DECISION_LOG rows exist) |
| 29 | 1 | HISTORY | run_094 still had step 1a pick it (> 2.2, FAIL on all 4 variants) | none |
| 30-39 | 10 | LIVE RULE | The entry stays so that pre-registered rules keep resolving. A new block choice is refused at 1a and in an operator brief. Composition runs are not affected. | Refusal at 1a: `rpr:8263-8265`. Brief lint: `vce:1948-1961`, `vce:1964-2002`. Copies allowed: `rc:912` (`allow_retired=_candidate_keeps_brief_criteria`), `rc:1144` (`allow_retired=True`). Composition exempt: `rpr:8426` (`block_run=exempt != "composition run"`). |
| 41-50 | 10 | HISTORY (minor drift) | CORRECTION 2026-09-20: rename from `edge_to_cost_ratio` (CUL-300), "grep-confirmed against tools/run_protocol.py:1170" | The field is now computed at `SR/tools/run_protocol.py:1191` (via `tools/cost_helpers.py`) and stored at `:1240`. Line 1170 is inside the CUL-300 comment block. |
| 54-58 | 5 | STALE | D-038/D-039: same numbers as the profit bar `cost_edge_ratio_min`, "which grades every backtest under orchestrator.profit_bars_v2; this menu entry stays optional for step 1a (E-062 S1 G7)" | (a) `cost_edge_ratio_min` is `null` (OFF) in `SR/config/profitability_bars.yaml` since D-118 (that file's comment at lines 29-30; DECISION_LOG D-118). (b) "Stays optional for step 1a" contradicts the data line 40 `retired_for: [block]` (D-133). |
| 59-64 | 6 | RATIONALE (definition caveat) | Same numbers, not the same definition as the bar: rounded to 4 dp over all trades, and a floor that counts forced closes | Still true of the code: `SR/tools/cost_helpers.py:147-151` rounds to 4 dp; `vce:1506` computes pooled `n_trades` as the sum of `core.trade_count`; the bar uses `SR/tools/portfolio_whole_test.py:1195`. The bar it compares to is off (row 54-58). |
| 66-68 | 3 | LIVE RULE | Fields a card may override; any other card field is refused; none here | `vce:1883-1892` (allowlist), called at `rpr:8266` |
| 87-89 | 3 | RATIONALE (known-limit caveat) | Under-complete for perpetuals: funding not modelled until E-053 | Consistent with `SR/tools/run_protocol.py:1072` (`"funding": False`, not modelled) |
| 92-98 | 7 | RATIONALE | Why the default metric is `net_return_pct`; a per-hypothesis `metric` is allowed | Card C. No D-number. The override itself is the LIVE `card_overridable: [metric]`. |
| 102-103 | 2 | LIVE RULE | Only `metric` may be overridden | `vce:1883` |
| 105-108 | 4 | LIVE RULE | `comparator`/`threshold` unused by this reducer and deliberately absent | `vce:1460-1478`: the sign branch returns PASS/FAIL/INCONCLUSIVE before any comparator is applied |
| 124 | 1 | PROMPT TEXT (not code-enforced) | "pre-registered by a brief only (D-121); not for step 1a" | No code refuses it at 1a. `_pass_rule_from_card` accepts any live `criteria` id, and `SR/tests/test_e059_s2a_review_fixes.py:224-226` has a 1a card pick `whole_test_sharpe_positive` successfully. The restriction exists only in the prompt: this line and `SR/workflow_artifacts/skills/hypothesis-design/SKILL.md` step 2b rule 4. The line is pinned verbatim by `SR/tests/test_d143_step1a_criteria_questions.py:122-125`. |
| 125-133 | 9 | LIVE RULE (with D-121/D-141 rationale) | One definition with `sharpe_min`; the value is injected per variant; None reads INCONCLUSIVE; a ruined account FAILs | `rpr:5953` (`_with_whole_test_sharpe`), `vce:1519-1537` (ruin → FAIL), `vce:1538-1548` (None → INCONCLUSIVE) |
| 148-156 | 9 | RATIONALE (D-134) | All-bars IC, not active-bars; median of windows; undefined windows excluded | D-134. The exclusion is live at `vce:1452` (`non_none`). |
| 157-165 | 9 | PROMPT TEXT (marker + editing instruction) | `# D-186 BEGIN` and how the bracket mechanism works, "re-pin the fixture" | Markers read by `rpr:4351-4383` (`_menu_text_for_prompt`); fixture test `SR/tests/test_d186_forecast_ic_horizons.py` (flag-off prompt text equals `tests/fixtures/d186/criterion_menu_pre_d186.yaml`) |
| 166-173 | 8 | LIVE RULE | D-186: card `horizon` (flag on only), the `_h<h>` field, the default and allowed values; stripped with the flag off | `vce:1365-1374` (`horizon_metric`), `vce:1377-1401` (`menu_without_horizon`), `vce:1931-1937` (`horizon_allowed` check), `rpr:4395-4409` (`_load_criterion_menu`) |
| 174, 180, 189 | 3 | PROMPT TEXT (markers) | `# D-186 END` / `BEGIN` / `END` | `rpr:4351-4383` |
| 181-183 | 3 | PROMPT TEXT (emitted) | `# D-186 OFF: ...` lines. With the flag off, the prompt gets them with the prefix removed: a comment pair plus the data line `card_overridable: []`. | `rpr:4354` (`_D186_MENU_OFF_RE`), `rpr:4380-4381` |
| 184-185 | 2 | RATIONALE | D-134: the threshold is one fixed default; D-186 amends only the horizon | D-134, D-186 |
| 226, 228-232 | 6 | HISTORY (backlog note) | "Not yet wired": `gated_beats_ungated` resolves to no field; regime-block story E-060 | Still true: grep finds no `gated_beats_ungated` in `SR/tools`, `SR/workflow` or `trading-bot/` code |
| 227, 233 | 2 | (separator) | bare `#` | none |
| 234-237 | 4 | HISTORY (commented-out entry) | `# - id: gated_beats_ungated ...` | YAML ignores it; no reader |
| 239-240 | 2 | HISTORY | Provenance: E-060 S2, delivery plan slice 7, guesses 6-8, operator decision 5 | none |
| 241-253 | 13 | LIVE RULE | Code-added criteria sit outside `criteria:`. 1a picks only from `criteria` (D-137 exception for `residual_ic`). The grid backfills only from `criteria`. `residual_ic` is appended only under `composition_runs`. 1a never picks `profit_bars`. | `rpr:8252-8256` (1a lookup, D-137 add-in), `rpr:8424-8429`, `rpr:5904` (`_with_residual_ic_criterion`), `vce:1758-1767` (`_menu_entries_by_id` reads `criteria` only) |
| 256-262 | 7 | LIVE RULE | What residual IC is; composite STALE → INCONCLUSIVE, fully_explained → FAIL, only with `composition_runs=True`; otherwise `min_n_eff` raises | `vce:1508-1513`, `vce:1568-1640` (`_evaluate_residual_ic_cell`), `vce:1238-1243` (`min_n_eff` raises on the ordinary path) |
| 267-269 | 3 | RATIONALE (+ ratification history) | D-039 supersedes D-026's 0.01; ratified 2026-09-29 | D-039, D-026 |
| 271-274 | 4 | RATIONALE | Why `max_p_value` 0.05 (pure noise cleared the old 0.01 about half the time) | D-039 |
| 288-297 | 10 | LIVE RULE | `profit_bars`: the composition run's only criterion; the cell is branch 3's grading; PASS only if every bar PASSes; written by code; elsewhere SPEC_ERROR | `rpr:6234-6248` (written by code), `vce:1649-1690` (`_evaluate_profit_bars_cell`), `vce:2246`, `vce:1442-1444` (source not window/pooled → SPEC_ERROR) |

**Lines per class (sums to 171):**

| Class | Lines | Share of comment lines |
|---|---|---|
| LIVE RULE | 71 | 42% |
| RATIONALE | 38 | 22% |
| HISTORY | 26 | 15% |
| PROMPT TEXT | 16 | 9% |
| STALE | 15 | 9% |
| bare `#` separator | 5 | 3% |

The LIVE RULE lines describe rules that code enforces. None of them is itself the enforcement: deleting any of them changes no grade or refusal. It does change step 1a's prompt and the D-186 fixture (see 2.2).

### 2.2 Does any code read the comments themselves? Yes, in three ways

1. **Raw text pasted into a prompt (step 1a).**
   - `rpr:9036-9071` (`_apply_config_direct_authoring_context`) adds `../../config/criterion_menu.yaml` to `hypothesis_generation`'s `required_inputs` when `orchestrator.config_direct_authoring` is on. The reason text it attaches is "pre-register pass/fail criteria here, at 1a, picked from this menu's live entries only."
   - The prompt builders read the file with `f.read()` and inline it as `--- CONTENT OF ... ---` through `_prompt_input_content`. This happens at `rpr:1058-1065` (`_build_stage_prompt`) and `rpr:1592-1599` (`run_gemini_worker`).
   - `rpr:4386-4392`: `_prompt_input_content` filters only this file, through `_menu_text_for_prompt`. Its docstring at `rpr:4400` says "(The raw file is still what step 1a's prompt copies.)"
   - No other stage gets the file as an input. `verdict_interpreter` cites it, but `SR/tests/test_cul336_closed_book_stages.py:528-530` waives it as "reaches the stage via pre_registration.yaml / pass_rule_evaluation.yaml".
2. **Comment markers as instructions to code.** `rpr:4351-4383` treats `# D-186 BEGIN`, `# D-186 END` and `# D-186 OFF:` lines as directives. A BEGIN without an END raises.
3. **Tests that pin comment text.**
   - `SR/tests/test_d186_forecast_ic_horizons.py` (`test_flag_off_menu_prompt_text_is_the_pre_d186_menu_byte_for_byte`, around line 717) compares the flag-off prompt text, all comments included, byte for byte with `SR/tests/fixtures/d186/criterion_menu_pre_d186.yaml`. Any comment edit outside the brackets requires re-pinning that fixture. Line 164 of the menu says so.
   - `SR/tests/test_d143_step1a_criteria_questions.py:122-125` asserts line 124's exact text.

The structured loaders do not see comments. `rpr:4395` (`_load_criterion_menu`, which uses `load_yaml` and then `menu_without_horizon`) and `rpr:5935` / `rpr:6235` (plain `load_yaml`) parse the YAML, so comments are dropped. The `basis` field is data, but no code reads it: it is stripped as a meta key (`rpr:8142` `_MENU_META_KEYS`, `rpr:5773` `_CODE_CRITERION_META_KEYS`). Its only reader is the step 1a prompt, through the raw text.

### 2.3 Stale or drifted passages, all in one list

| Where | What it says | What is true |
|---|---|---|
| Comment 11-15 | Record shape | Leaves out 9 keys in use and source `profit_bars` (table 2.1) |
| Comment 17-21 | Profit-bar file "not-yet-built" | `config/profitability_bars.yaml` exists, and lines 55-56 and 82-83 cite it |
| Comment 54-58 | Bar `cost_edge_ratio_min` grades every backtest; entry "stays optional for step 1a" | The bar is `null` (D-118). The entry is `retired_for: [block]` (D-133, line 40). |
| `basis` data, lines 81-85 | "The same numbers are the campaign-wide profit bar cost_edge_ratio_min ... graded on every backtest ... this idea-level entry stays one that step 1a may pick" | Same contradiction as the row above. This text is data, but no code reads it; it reaches only the 1a prompt. |
| `basis` data, line 221 | "tools/verdict_criteria_evaluator.py:1400-1403" | Those lines are now the end of `menu_without_horizon`. The None exclusion is at `vce:1452`. |
| Comment 44 | "tools/run_protocol.py:1170" | The field is computed at `:1191` and stored at `:1240` (drift, not a wrong claim) |
| Comment 124 | "not for step 1a" | True only as a prompt instruction; code accepts the pick (see 2.1) |
| Outside the file: `SR/config/feature_flag_register.yaml:490` | "`ratified: false` in config/criterion_menu.yaml" | The menu has `ratified: true` (line 276) |

## 3. Data fields and their readers

"Stripped" means the key is removed as a meta key before a criterion is written into `pre_registration.yaml`, and no code reads its value.

| Field | Entries carrying it | Code readers (file:line) |
|---|---|---|
| `criteria` (top) | n/a | `vce:1758-1767`, `rpr:8250`, `rpr:8303`, `SR/tools/decide_next.py:2603` |
| `code_added_criteria` (top) | n/a | `rpr:6170-6176` (`_code_added_criterion`), `rpr:8255` (D-137) |
| `id` | all | `vce:1767`, `rpr:8258-8262`, `rpr:6173`, `rpr:5966` (`whole_test_sharpe_positive`), `rpr:8316` (`forecast_ic_median`), `SR/tools/decide_next.py:2607` |
| `metric` | all | `vce:224`, `vce:1324`, `vce:1431`, `vce:1585`; `rpr:5956` |
| `source` | all | `vce:1432`, `vce:1442-1444`, `vce:1426`, `vce:1783` (menu-shaped detection), `vce:2246` (`profit_bars`) |
| `reducer` | sign_consistent, forecast_ic | `vce:1447-1450`, `vce:1460`, `vce:1480`, `vce:1338` |
| `reducer_arg` | none | `vce:1480` (`fraction_above` only; no entry uses it) |
| `comparator` | realized_edge, whole_test, forecast_ic, residual_ic | `vce:1433`, `vce:1474-1477`, `vce:1586` |
| `threshold` | same four | `vce:1434`, `vce:1477`, `vce:1587`; lint `vce:1900-1901` (only for `scale_free: false`) |
| `floor.min_windows` / `min_trades` | realized_edge, sign_consistent, forecast_ic | `vce:1247-1252` (`_check_floor`); no-lowering lint `vce:1907-1925` |
| `floor.min_n_eff` | residual_ic | `vce:1598-1611` (composition path); `vce:1238-1243` raises on the ordinary path |
| `floor: {}` | whole_test | read as empty (no floor) |
| `scale_free` | all (`true` everywhere) | Read only at `vce:1900` as `is False`. No entry is `false`, so the value `true` changes no code path. |
| `symbol_reducer` | all (`null` everywhere) | `vce:1728-1739` (`null` = naive pool) |
| `card_overridable` | all | `vce:1883`, `vce:1389-1399`, `SR/tools/decide_next.py:2609`; stripped `rpr:8142`, `rpr:5773` |
| `retired_for` | realized_edge | `vce:1953`; stripped `rpr:8142` |
| `horizon` | forecast_ic (flag on) | `vce:1365-1374`; `rpr:6017` (residual-IC horizon); `rpr:8328`; removed when the flag is off (`vce:1397`) |
| `horizon_allowed` | forecast_ic (flag on) | `vce:1931`, `rpr:8317`; stripped `rpr:8142` |
| `statistic` | residual_ic | `vce:229-231` |
| `max_p_value` | residual_ic | `vce:1588-1631` |
| `basis` | all | **No code reader** (stripped `rpr:8142`, `rpr:5773`); reaches only the 1a prompt |
| `ratified` | residual_ic | **No code reader** (stripped `rpr:5773`). `SR/docs/RUNBOOK.md:312` mentions it. |
| `requires_flag` | residual_ic, profit_bars | **No code reader** (stripped `rpr:5773`). The real gate is code: `_composition_runs_enabled` at `rpr:5776` and `vce:1508`/`vce:2246`. |
| `predicts_kind` | none | `rpr:8307` looks for a menu entry with `predicts_kind: market_state`; none exists, so the D-192 check always reports "no label measure in the menu" |

**Fields no code reads:** `basis`, `ratified`, `requires_flag`. `scale_free: true` and `symbol_reducer: null` are read, but their present values change no code path.

## 4. Where each class could live instead (inventory, nothing edited)

| Class (lines) | Possible home | Already there? | Effect of moving it |
|---|---|---|---|
| LIVE RULE (71) | Docstrings of the enforcing functions (`vce:1861`, `vce:1948`, `vce:1964`, `rpr:8216`, `rpr:4351`); a JSON schema for the menu (none exists in `SR/workflow_artifacts/schemas/`); `SR/docs/USER_GUIDE.md` | Mostly yes: each enforcing function's docstring states its rule | The 1a prompt loses code pointers (`run_phase1_research._...`). Re-pin the D-186 fixture. |
| RATIONALE (38) | DECISION_LOG rows D-038/039, D-107, D-121, D-128, D-133, D-134, D-137, D-141, D-186 | Yes, all these rows exist. Card C (92-98) and the funding caveat (87-89) have no D-row. | Re-pin the fixture; the 1a prompt no longer carries the "why" |
| HISTORY (26) | DECISION_LOG, git history, SESSION_LOG, EPICS (backlog note for `gated_beats_ungated`), or nowhere | The CUL-300 rename and run_094 are in their own records (not checked line by line) | Re-pin the fixture |
| PROMPT TEXT (16) | Brief-only status (line 124): a data field read by code, or the skill (SKILL.md step 2b rule 4 already says it). D-186 markers: needed while the bracket mechanism exists, or nowhere once the flag is settled. | Rule 4 is in the skill; the markers have no other home | Line 124 is test-pinned (`test_d143`:122-125). The markers are needed by `_menu_text_for_prompt` while `forecast_ic_horizons` can be off. |
| STALE (15, plus 2 `basis` passages) | Nowhere (delete), or corrected | n/a | Re-pin the fixture |
| `basis` data (56 prose lines) | DECISION_LOG rows (D-038/039, D-121, D-134, D-039) or a design doc | D-134's measured IC distribution may be only here (not checked) | It is data, stripped before registration; only the 1a prompt reads it |

Constraint shared by every row: any change to the comment text changes step 1a's prompt (when `config_direct_authoring` is on). It also breaks `test_flag_off_menu_prompt_text_is_the_pre_d186_menu_byte_for_byte` until the fixture is re-pinned.

## 5. Facts for the operator's design challenges (no judgement)

### Entries and status

| Entry | Section | Status | Picked by step 1a in code | In the skill (1a) | Brief (D-121 lint) | Threshold | Card-overridable |
|---|---|---|---|---|---|---|---|
| `realized_edge_to_cost_ratio` | `criteria` | Retired for blocks (`retired_for: [block]`, D-133). It is kept so that existing pass_rules, fold-child copies and composition runs still resolve. | Refused for a block run (`rpr:8263`); accepted for a composition run (`block_run=False`) | "retired ... refused" (DECIDE_NEXT_CANDIDATES.md) | Refused unless `allow_retired` (`rc:912`, `rc:1144`) | `> 2.2`, floor 5 windows / 100 trades | `[]` |
| `sign_consistent_by_era` | `criteria` | Selectable | Yes | Yes, only when the windows span 2+ eras (step 2b rule 7) | Yes | None (the reducer decides); floor 5 windows / 15 trades | `[metric]` |
| `whole_test_sharpe_positive` | `criteria` | Selectable by code; brief-only by prompt instruction | **Yes** (no code refusal; `test_e059_s2a_review_fixes.py:224`) | No (rule 4; line 124; not in DECIDE_NEXT_CANDIDATES.md, test-pinned) | Yes | `> 0.0`, no floor | `[]` |
| `forecast_ic_median` | `criteria` | Selectable | Yes | Yes (rules 1-2) | Yes | `> 0.02` (median over windows), floor 5 windows | `[]` with `forecast_ic_horizons` off (committed); `[horizon]` (1/6/24/72/168) with it on |
| `gated_beats_ungated` | commented out | Placeholder, not an entry | Unknown id → refused | No | Unknown id → refused | none | none |
| `residual_ic` | `code_added_criteria` | Added by code to forecast-block ideas under `composition_runs` (off) | Only where code adds it anyway (D-137); naming it changes nothing | Rule 3 ("added by code") | Refused (not in `criteria`) | `> 0.02`, p < 0.05, `n_eff >= 30` | `[]` |
| `profit_bars` | `code_added_criteria` | Code-only, composition runs | Never | No | Refused (not in `criteria`) | Every bar in `config/profitability_bars.yaml` | `[]` |

Committed flag states: `config_direct_authoring`, `forecast_ic_horizons`, `brief_criteria`, `composition_runs`, `grid_evaluation`, `decide_next`, `profit_bars_v2` and `residual_ic_requires_block` are all `false`. So in this checkout no menu path is active. The operator's own checkout may differ (not checked).

### Fixed versus overridable

- No entry lists `threshold` in `card_overridable`. Every threshold is fixed per entry.
- No entry lists `floor` either. Every card `floor` value that differs from the menu is therefore refused by the allowlist (`vce:1883-1892`) before the raise-only rule (`vce:1907-1925`) applies, so that rule is currently unreachable from a card.
- The `scale_free: false` threshold lock (`vce:1900`) applies to no current entry: all are `true`.

### Parameterisation per idea or per market that already exists

- **Per idea, in the menu:** `sign_consistent_by_era`'s `metric` override, and `forecast_ic_median`'s `horizon` (flag on). D-192 (`rpr:8289-8331`) warns when the card's `statement.predicts_kind` and `horizon_bars` do not match the chosen criterion and horizon.
- **Per idea, outside the menu:** a brief's `evaluation.pass_rule` can carry fully self-contained criteria (no `id`). `resolve_criteria_against_menu` takes them as written, and `evaluate_grid` grades them if they carry `source`/`reducer`. The legacy K2 shape (`metric_basis`, `threshold`, `per_symbol_threshold`) is graded by `vce:251-308`. Under D-121 a brief's own field must be menu ids only (`rpr:8357`, `is_menu_id_pass_rule`).
- **Per symbol:** `symbol_reducer: per_symbol_all|pooled` exists in the evaluator (`vce:1728-1739`), but every entry has `null`. The legacy `per_symbol_threshold` gives a threshold per symbol (`vce:257-263`).
- **Per market history:** `sign_consistent_by_era` uses the era list in `campaign_data_policy.yaml`. Under `profit_bars_v2`, a single represented era reads INCONCLUSIVE (`vce:1465-1476`, D-047).
- **Per timeframe:** `residual_ic_requires_block` (off) exempts an idea from `residual_ic` on a timeframe with no registered forecast block (`rpr:5854`). The `forecast_ic_median` `basis` records that 0.02 behaves differently on hourly and daily bars (it estimates false-pass rates of about 1 in 3 versus about 2% on 6 windows). The threshold itself is not per timeframe.
- **Profit bars (code-added only):** partial-coverage normalisation scales some bars by covered fraction (D-047; `SR/config/profitability_bars.yaml` lines 320-322), and D-185 counts deflated-Sharpe trials per (structure, timeframe). These are campaign bars, not menu thresholds.

## Not checked

- The operator's local `campaign_config.yaml` flag states, and which runs actually had the menu in their 1a prompt.
- Whether every DECISION_LOG row cited holds the full rationale now in the comments (only the row existence and titles were checked).
- Whether D-134's measured IC distribution (the `basis` of `forecast_ic_median`) is recorded anywhere besides the menu.
- `review_2026-09-27/PLACEHOLDER_VALUES_PROPOSAL.md`, `S1_FINDINGS.md`, `delivery_plan_v26.md` and `engineering_roadmap.html` (cited by the comments): not opened.
- Whether the other `SR/config/*.yaml` files have a similar comment share (not measured, so no comparison is made).
- Whether the C5.1 brief lint at `rc:905` runs without `brief_criteria` on: the surrounding gate was not traced.
- No tests were run; every line reference was read from source in this checkout.
