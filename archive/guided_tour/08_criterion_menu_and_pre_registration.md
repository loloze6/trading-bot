# Stop 08: The criterion menu and the pre-registration (branch 1's measures)

## Speech (verbatim)

**Stop 08 of 29: The criterion menu and the pre-registration.** Open on the side: `config/criterion_menu.yaml`, run_102's `artifacts/pre_registration.yaml`, `run_campaign.py`, `run_phase1_research.py`.

**In one sentence.**
The criterion menu is the short, fixed list of measures an idea may be judged by; the pre-registration is the run's own sheet, written before any result, saying which of those measures will judge it and on which test months.

**Why it exists.**
If each run invented its own pass mark, a weak idea could always find a measure it passes.
So the measures come from one menu, each with its threshold and its minimum sample fixed in advance and written with its reasons.
The run's choice is then written down at launch, before the backtests. The pass/fail grid (branch 1, stop 19) reads only that sheet.

**What comes in, what goes out.**
- In: the menu (written by hand, each threshold decided by the operator); the brief's criteria, or step 1a's pick (stop 07).
- Out: the run's `pre_registration.yaml`: the pass rule, the test settings, and two fixed notes.
- Next: the grid judges the run against the pass rule; decide-next copies the test settings, and a fold child's criteria, into the next brief (stop 24).

**What happens here, step by step.**
The menu holds four entries an idea may name, and two that only code adds:
1. **Forecast quality** (`forecast_ic_median`): the forecast's correlation with the coming return over all bars, its median over the test windows (an IC, information coefficient). It must be above 0.02 over at least 5 windows. The idea may set only the horizon: 1, 6, 24, 72 or 168 bars. The entry's notes say no past hourly variant has reached 0.02.
2. **Same sign in every era** (`sign_consistent_by_era`): every era (a slice of market history named in the data policy) shows the same sign, by default on window profit. Only the measured field may be changed.
3. **Positive whole-test Sharpe** (`whole_test_sharpe_positive`): the Sharpe ratio (return per unit of risk) of the whole test, chained, above 0. For a brief only, not for step 1a.
4. **Edge over cost** (`realized_edge_to_cost_ratio`): gross gain per trade over cost per trade, above 2.2. Retired for new block ideas (D-133); it still resolves where a run already registered it.
5. **Added by code: overlap** (`residual_ic`): the information an idea holds that the proven pieces do not, above 0.02 with enough independent days and a significance test. Only when combinations are switched on and a proven piece exists on that bar size.
6. **Added by code: profit bars** (`profit_bars`): the only criterion of a combination run.

The pre-registration:
1. It is written at launch from the brief, after the menu checks (stop 04). A brief that leaves the choice to 1a gets its pass rule written right after step 1a (stop 07).
2. The short names are expanded into full rules from the menu: the measured field, window by window or pooled, the reducer (median, sign by era...), the comparison, the threshold, the minimum sample.
3. It also holds the test settings (coins, bar size, fold or dates, window length) and two fixed notes: a sentence on how this lineage started and the sealed holdout's range with a one-line note.

Example: run_102's pass rule is one criterion: forecast quality at a 24-hour horizon, median of the windows above 0.02, at least 5 windows. Its test settings: BTC, hourly bars, fold B (six 4-month blocks across 2018-2021), window length 4.

**What it costs and how long it takes.**
No cost.
4 entries an idea may name (one retired for blocks) and 2 added by code (`config/criterion_menu.yaml`, 306 lines).

**What is switched off or not used here.**
- A placeholder entry for regime pieces ("gated beats ungated") is commented out: it reads no field yet.
- Edge over cost is retired for new block ideas.
- My grep found no code that reads back the pre-registration's lineage sentence or its holdout note; the holdout itself is guarded elsewhere (stop 27).
- The pre-registration's `hypothesis_id` is a placeholder of the form `run_102-initial`.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Header | `criterion_menu.yaml:1-21` | Purpose, record shape, profit measures excluded |
| Edge over cost | `criterion_menu.yaml:24-90` | Retired for blocks (`:40`), threshold 2.2 (`:65`), not overridable |
| Same sign by era | `criterion_menu.yaml:91-122` | Default metric `net_return_pct`, `card_overridable: [metric]` |
| Whole-test Sharpe | `criterion_menu.yaml:123-146` | Brief only (D-121), threshold 0.0, pooled |
| Forecast quality | `criterion_menu.yaml:147-224` | `forecast_return_corr_all_bars`, median, `> 0.02`, horizon 1/6/24/72/168, floor 5 windows, basis text |
| D-186 brackets | `criterion_menu.yaml:157-186` | Text step 1a sees with the horizon switch off |
| Placeholder | `criterion_menu.yaml:226-237` | `gated_beats_ungated`, commented out |
| Code-added | `criterion_menu.yaml:239-306` | `residual_ic` (`:255`, `> 0.02`, p < 0.05, n_eff >= 30), `profit_bars` (`:287`) |
| Menu loader | `run_phase1_research.py:4395-4410` | Horizon keys stripped when the switch is off |
| Menu filter for the prompt | `run_phase1_research.py:4386-4392` | D-186 brackets |
| Written at launch | `run_campaign.py:795-935` | Stop 04; brief criteria `:862-869`, `:905-920` |
| Written after 1a | `run_phase1_research.py:8386-8452` | Card's pick, when 1a chooses |
| Overlap added | `run_phase1_research.py:5913` | `residual_ic` |
| Readers | `tools/verdict_criteria_evaluator.py`, `tools/decide_next.py`, `tools/research_folds.py:418-427`, `tools/protocol_resolution.py`, `tools/near_miss_scoreboard.py`, `tools/structure_key.py` | Grid, next brief, fold, protocol, scoreboard, trial key |
| Example | `runs/run_102/artifacts/pre_registration.yaml` | `pass_rule`, `machine_constraints` (fold B), `sample_split_design`, `reactivation_context`, `hypothesis_id: run_102-initial` |

Remarks: send them as "stop 08: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Step 8: 
I am really not convinced by the current design of this step. But maybe i am wrong. 
The idea is simple, but the design is complex (at least to understand). Here the point is to associate an idea with quantitative threshold that would allow to test of the idea is proven or not. 
The test being mechanical, this step should generate an output being readable and runnable by code. The step output being code is not necessarily to be a code associate to test pre-coded. It could be a config (a bit like strategy-config) or even piece of code. 
I am also challenging the shortness of the test menu as of now. 
The fact that we keep a criterion not to be chosen is also really questionable. 
Finally, i am thinking that the crierion menu (or any other future element allowing to generate readable code as output) should not predefine pass criteria. Each pass criteria depend on the idea, no ? And even further, some could depend on the currency / market context, so they could be standardized.. 
Here the crierion menu is overloaded by comment line, is it normal ? 
To conclude, i repeat, but the concept is simple: associating an idea with quantitative test verifying its correctness readable by code. But the current design is super complex for that and seems generated as a "patch" (inherhiting specificities of the discussion context it was created from)

Btw, an idea being around 

(Guide's note: the last line arrived as written above; it appears cut off.)

## Inspector notes

### (1) Design and mechanism

1. For the campaign's main bar size, branch 1 has one live measure and it has never been passed. Of the four nameable entries, `realized_edge_to_cost_ratio` is retired for blocks (`criterion_menu.yaml:40`), `whole_test_sharpe_positive` is brief-only (`:124`), and `sign_consistent_by_era` "adds nothing" on a one-era protocol by the skill's own rule (`hypothesis-design/SKILL.md:50`; fold A lies in one era of the policy's list, B and C straddle two). What a 1a card can pick for a return-direction idea is `forecast_ic_median` (stop 07 note 1.2). Its own basis text reports that no hourly variant of 29 in 11 runs reached 0.02 (`:204-206`, `:213-214`) and that the three daily passes came from a strategy that failed every profit bar (`:208-215`); the memory's 25 refuted of 28 (stop 07) is this entry's record. The operator confirmed 0.02 at merge (`:223-224`). A judge that no idea passes gives the loop no information per run: every refutation is the same refutation, and decide-next (stop 24) ranks among ideas the grid cannot tell apart. Whether 0.02 is right is the operator's; that the pipeline cannot measure its own discrimination is the finding.
2. The grid's `validated` is not "worth trading", and the menu says so (`:216`, "IC measures direction, not profit after costs"). That split (branch 1 idea-level, branch 3 profit-level) is intended; the consequence is that `idea_status`, the one word 1a and decide-next read from memory (stop 07 note 1.4), means "IC above 0.02 on at least 5 windows" and nothing about money. run_083, run_089, run_091 read `validated` in `tried_ideas.yaml` with no bars outcome beside them except the optional `base_*` book fields.
3. The pre-registration mechanism is sound where it matters: the menu is resolved at launch (`RC:918-920`) or right after 1a (`RP:8425-8442`), meta keys stripped (`RP:8380-8382`), the threshold not overridable (`card_overridable: [horizon]`, `:186`), a retired entry refused for a new choice but kept resolving for an old rule (`vce:1979-1982`, `:2003-2006`), and `pass_rule_source_ref` records who wrote the rule (`RP:8441`). The one degree of freedom, the horizon, is chosen before the child's data but from the parent's analysis (run_102's horizon 24 is the analyst's q19 horizon, stop 07 card `:8`): allowed by the fold discipline, and it is the intended use.
4. On the live loop nobody chooses the criterion anew. A fold child copies its source's criteria (`decide_next.py:2805`, D-121), the child's 1a leaves them (stop 07), so a lineage carries the criterion its first run picked; with the menu as it is, that is always `forecast_ic_median`. Consistent for comparability across a lineage; also one more reason the live loop's judge is a constant.
5. `sign_consistent_by_era` defaults to `net_return_pct` (`:99`), a window P&L sign, under a header that excludes profit measures (`:17-21`) and a skill that says "never a profit measure" (`SKILL.md:47`). The entry is scale-free by sign, so the letter of card B holds; the default metric is still a profit read. Overridable to `forecast_return_corr` (`:104`), which the skill does not mention.
6. `whole_test_sharpe_positive` has threshold 0.0 and `floor: {}` (`:137`, `:141`): no minimum sample; only computability (30 daily returns, `:131-132`) stands between a brief and a pass. The weakest entry, brief-only.
7. The file carries the sealed range in clear (`pre_registration.yaml:30-32`, `RC:829-835`), pinned by two tests (`test_k4_routing_registration.py:445`, `test_k3_protocol_pinning.py:498`); its `hypothesis_id` is a placeholder (`:2`, `RC:811`) that `_write_pass_rule_from_card` never updates although it rewrites the file (`RP:8440-8442`); `reactivation_context` is a fixed sentence (`:4-6`). Stop 04 notes 1.5 and 1.7 stand.

### (2) Legacy or simplifiable (leads)

1. `realized_edge_to_cost_ratio` (`:24-90`, 67 lines): kept so old rules resolve; `campaign_memory.yaml` mentions the three older ids 70 times (count only; which runs not checked). An archive section would separate "resolvable" from "pickable".
2. `gated_beats_ungated` (`:226-237`): a commented placeholder with no field; delete or build with the regime-block story.
3. D-186 brackets (`:157-174`, `:180-189`), `_menu_text_for_prompt`/`_prompt_input_content` (`RP:4386-4392`), `menu_without_horizon` (`vce:1377`), `_load_criterion_menu`'s flag branch (`RP:4403-4409`) and the fixture `tests/fixtures/d186/criterion_menu_pre_d186.yaml`: a prompt-text filter and a loader branch for the off-state of a flag that is on. Fold the flag, delete the four.
4. `reactivation_context` and `sample_split_design` (`RC:813-835`, dry-run copy `:1089-1097`): no reader (grep over `workflow/` and `tools/`: writers and tests only; `RP:3155-3157` says the one field it fed has no reader). The key-order test (`test_e059_s2a_decide_next.py:570-571`) pins them.
5. `basis` texts (`:75-86`, `:114-121`, `:142-145`, `:194-224`): a 2026-10-15 measurement and three decision histories in a config file; the live value, floor and one line of reason belong here, the rest in the decision log (the operator's stop 03 rule).
6. `_find_pass_rule`'s nested `machine_constraints.pass_rule` shape (`vce:914-944`, run_057) and the `legacy_not_evaluable` returns of `evaluate_pass_rule_criteria` (`vce:859-1040`): the pre-grid evaluator; whether the live path calls it or only `evaluate_grid` is stop 19's.
7. `hypothesis_id: <run>-initial` (`RC:811`): write the card's id after 1a or drop the key.

### (3) Disagreements between the speech and the element

1. Step 1, "above 0.02 over at least 5 windows ... horizon 1, 6, 24, 72 or 168 ... no past hourly variant has reached 0.02": `:179`, `:193`, `:188`, `:204-206`; correct. The speech does not add the basis text's own reading that the daily passes did not discriminate (`:213-216`, note 1.1).
2. Step 2, "by default on window profit. Only the measured field may be changed": `:99`, `:104`; correct; the tension with the header (note 1.5) is not stated.
3. Step 3, "For a brief only": `:124`; correct; no floor (`:141`) not stated.
4. Step 5, residual_ic "only when combinations are switched on and a proven piece exists on that bar size": `:282`, `RP:5854-5879`; correct.
5. "The menu holds four entries an idea may name": correct by the file; what a 1a card may name today is two (note 1.1).
6. Reading map "Readers ... `tools/protocol_resolution.py`": its one mention (`:328`) is an error message naming the file, not a read. `structure_key.py:316-324` reads `machine_constraints.protocol_ref` only; `near_miss_scoreboard.py:501-507` the comparators; `decide_next.py:1487`, `:2688`, `:2805` the constraints and the pass rule; `research_folds.py:418-427` the fold; `explore_confirm.py:374-389` the criteria through `_resolve_grid_criteria`. Five readers, not six.
7. Reading map "D-186 brackets `:157-186`": the second bracket closes at `:189`; "Code-added `:239-306`", `residual_ic :255`, `profit_bars :287`: correct. "Menu loader `:4395-4410`": correct.
8. Example: one criterion, horizon 24, median above 0.02, 5 windows, BTC, hourly, fold B, window length 4: `pre_registration.yaml:7-28`; correct (the window length is overridden by the fold, stop 01 note 1.4).
9. Verified as stated: `criterion_menu.yaml` ranges `:1-21`, `:24-90`, `:91-122`, `:123-146`, `:147-224`, `:226-237`, `:239-306`; `RP:4386-4392`, `:4395-4410`, `:8386-8452`, `:5913`; `RC:795-935` (stops 01/04); `vce:1964-2009`; the example file.
