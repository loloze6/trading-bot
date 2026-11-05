# Research brief restructure: inventory and proposal (night of 2026-11-04)

Read-only analysis for the operator and the direction session. Nothing was changed except this file.
No run, test or pipeline script was executed. This is a proposal: nothing here is approved.

Short names: `SR` = `strategy-research/`; `RC` = `SR/workflow/run_campaign.py`; `RP` = `SR/workflow/run_phase1_research.py`;
`DN` = `SR/tools/decide_next.py`; `VCE` = `SR/tools/verdict_criteria_evaluator.py`; `CRR` = `SR/tools/campaign_review_retired.py`;
`VIEW` = `SR/tools/run_viewer/loaders.py`; `TPL` = `SR/workflow_artifacts/templates/research_brief_new_pipeline.md`.

Source of the operator's request: `guided_tour/01_the_brief.md`, sections "Speech" and "Operator remarks" only.

**Two facts about this checkout to keep in mind**

1. **The two example briefs the tour used are not on this checkout.** `SR/briefs/sma_trend_1h_fold_a.md` and
   `SR/campaign_record/candidate_briefs/forecast_power-run_102-2.md` do not exist here, and `git log --all` has no
   history for either path (`SR/runs/` is gitignored, `.gitignore:130`, and only run_053 to run_060 are on disk).
   Their fields below come from (a) the tour's Speech, which quotes them line by line, and (b) the code that writes
   them (`TPL` for the operator brief, `DN.candidate_brief` for the candidate brief). I checked the shapes against
   two files that are on disk: `SR/briefs/rebase_run_095_standardised_host.md` (a template-shaped operator brief,
   with a fold and an exact config) and `SR/campaign_record/candidate_briefs/forecast_power-run_095-1.md` (a
   decide-next side-finding brief with the same `candidate` keys, but no `source_observations` and no `evaluation`).
2. **Flags.** In this checkout's committed `SR/config/campaign_config.yaml`, every flag named below reads `false`
   (`grid_evaluation` :318, `config_direct_authoring` :497, `decide_next` :649, `folds` :894, `exact_config_1b`
   :1008, `brief_criteria` :1025, `claim_tests` :793). The tour said `exact_config_1b` and `brief_criteria` are on
   in the operator's live config. So each behaviour below is given for both flag states where it matters.

The template on disk (129 lines) also differs from the 98-line version the tour read. Since then, uncommitted
guidance comments for the prose part were added (`git diff`, written by `night_work_2026-11-04/docs_cleanup.md`).
No frontmatter field changed.

---

## 1. Field inventory

### 1.0 Who requires what today (the enforcers)

| Check | Where | When | What it does |
|---|---|---|---|
| Required keys | `CRR:29-30` `REFRAME_BRIEF_REQUIRED_KEYS` = `strategy_domain, market_universe, timeframe, research_goal, venue, product`; loop at `RC:701-703` | Every `_parse_brief_frontmatter` call (`RC:669-733`): registration (`RC:981`), launch (`RC:4412`, `:4429`), dry run (`RC:5865`) | Refuses a key that is missing **or empty** (`not data.get(k)`) |
| Placeholder sentinel `<FILL IN` | `RC:404`, `_find_placeholder_paths` `RC:422`, refusal `RC:719-727` | Every parse | Refuses the sentinel anywhere in the parsed frontmatter (not in comments) |
| Universe/timeframe vs protocol | `_lint_brief_protocol_agreement` `RC:454-545` | Registration only (`RC:983-986`), and only with `config_direct_authoring` on (`RC:638`) | `market_universe` must equal `machine_constraints.protocol.symbols` (`RC:530`); `timeframe` must equal `protocol.timeframe` (`RC:539`, default `"1h"` at `RC:502`) |
| Promotion block | `RC:547-570` (verdict routing live) / `RC:572-607` (retired) | Registration, under `config_direct_authoring` | Requires, or forbids empty or generic, `machine_constraints.protocol.promotion` |
| criteria_from vs pass_rule | `RC:843-855` | Launch (`_materialize_run`), only when `machine_constraints` exists | Refuses a brief that says "criteria from 1a" and also carries a `pass_rule` |
| Menu-criteria lints | `RC:857-920` (D-121, B11, CUL-267, C5.1, K3) | Launch | Lints and resolves `evaluation.pass_rule` |
| Protocol generation | `RP:10649-10729` | Start of `run_loop` (`RP:19649-19669`) | KeyError on missing `symbols`, `start` or `end`; ValueError on a bad `window_months`/`start` (`RP:10552-10557`) |

Nothing in code enforces that `machine_constraints` exists. Without it the run fails later (see 1.2).
`SR/docs/RUNBOOK.md:149` calls it "effectively mandatory".

### 1.1 Template and operator brief: top-level fields

All 11 fields below appear in `TPL` and, per the tour, in `sma_trend_1h_fold_a.md` (except `evaluation`, which is
commented in the template and absent from that brief, and `constraints`, which is commented in both).

| # | Field | Meaning | Required today? (enforcer) | Code readers | Absent → | Duplicates / notes |
|---|---|---|---|---|---|---|
| 1 | `strategy_domain` (`TPL:14-15`) | 1–2 word label for the kind of idea | **Required** (`CRR:29`, `RC:701-703`) | `RC:701` (presence); dry-run log `RC:5866`; copied by `DN:2664` and `DN:1537`; refold copy `RC:5707`; reframe fill `RP:7974-7983`. Model text: 1a (whole `research_brief.yaml`) | Refused at registration and launch | None. No code uses its value, only its presence |
| 2 | `research_goal` (`TPL:17-20`) | The idea in its author's words | **Required** (same) | `VIEW:433-436` (run header "purpose"); written by `DN:2668-2684` and `RC:5711-5714`; KB reactivation text check `RP:11466` (campaign review's `next_research_question` only). Model text: 1a, step 2, verdict interpreter (`RP:9910`), campaign review (`RP:7847`) | Refused | Decide-next writes into it the claim, evidence, fold and config change, which also sit in `candidate.*` (see #19–#33) |
| 3 | `venue` (`TPL:22-23`) | Exchange | **Required** (same) | `RC:787-792` (`research_only` via `check_venue_tradability` `RC:386`); `RP:19021-19043` and `SR/tools/venue_resolver.py:158-165` (protocol exchange, market_type and symbols); `RP:19045-19065` (protocol must model the venue); `DN:1899+` `_fold_data_reason` (coin coverage per venue) | Refused. If a caller bypasses the parser: `research_only: true` (fail-closed), and `resolve(None)` falls to the default venue binance (`venue_resolver.py:56`) | None in the brief. The generated protocol carries `exchange`/`market_type`, derived from it |
| 4 | `product` (`TPL:25-26`) | spot / perp on that venue | **Required** (same) | Same as `venue`, plus `VCE:478-495` (G1 funding gate: perp needs funding modelled or bounded); `RP:19037` (info line) | Refused. Bypassed: not a perp for G1 | None |
| 5 | `market_universe` (`TPL:28-29`) | Coin(s), BASEQUOTE | **Required** (same) | `RC:515-535` (vs `protocol.symbols`, registration, config-direct only); dry-run `RC:5867` (subscript, so a KeyError if absent); copied by `DN:2664` | Refused | **Duplicate of `machine_constraints.protocol.symbols`** (#13). The template says "write the same list again" (`TPL:28`); the test pins the equality (`SR/tests/test_e061_c1_7_first_run_kit.py:219`). The protocol, not this field, decides what is backtested (`RP:10678`) |
| 6 | `timeframe` (`TPL:31-32`) | Bar size | **Required** (same) | `RC:537-544` (vs `protocol.timeframe`); `VCE:439-450` `_bar_hours` (default `"1h"`); copied `DN:2664`; `DN:1538` overwrites it with the composition's timeframe | Refused | **Duplicate of `machine_constraints.protocol.timeframe`** (#14). The protocol decides the bars (`RP:10679`) |
| 7 | `available_data` (`TPL:34-35`) | Data needed beyond price bars | Optional (no check) | **No code reader** (grep). Model text only (1a, step 2) | Nothing changes | Overlaps the `scope` line "Price bars only" (#11). Shapes vary in the corpus: `none`, `[]`, a list of strings |
| 8 | `criteria_from` (`TPL:37-44`; the operator brief `:44`) | "Step 1a picks the pass/fail criteria" (value `hypothesis_generation`, constant `RP:8140`) | Optional in code. The template puts it in as a value; the test requires it (`test_e061_c1_7_first_run_kit.py:208`) | `RC:843-855` (pending marker); `RP:8175-8184` `_brief_criteria_from_1a`; `RP:8386-8452` `_write_pass_rule_from_card`; via the marker: `RP:8188-8212`, grid pre-flight deferral `RP:19680-19690` | See section 2: without criteria, the run fails at the grid pre-flight (grid on) or runs with no pre-registered criteria (grid off) | Mutually exclusive with #9 (`RC:850-855`). The name is shared with `candidate.criteria_from` (#23) |
| 9 | `evaluation.pass_rule.criteria` (`TPL:37-43`, commented) | The brief's own criteria, as menu ids (D-121) | Optional | `RC:808` (copied into `pre_registration.pass_rule`); `RC:862-920` (lints, then resolution against the menu when `brief_criteria` is on); `RP:8160-8172` (fold child keeps its criteria); `VCE:914-956` `_find_pass_rule` | No pass_rule: see #8 | With `brief_criteria` **off**, menu ids without `outcomes` are refused by the B11 lint at launch (`RP:11348-11350` via `RC:876-883`). So the commented example only works with the flag on |
| 10 | `constraints` (`TPL:46-54`, commented) | A list of strings. Two entries, if they begin with a fixed sentence, are machine-read: the exact config (`RP:16912`) and the exact block manifest (`RP:16949`). Any other entry is free text for the model steps | Optional | `RP:16916-16937` `_brief_exact_config`; `RP:16952-16971` `_brief_exact_manifest`; `RP:17078-17086` (1b-by-code mode); `RP:17089-17150` (1b by code); `RP:17186-17215` (replay gate); `RC:5745-5746` (refold check); `VIEW:377-388` **reads an entry containing "Pre-registered outcomes" as the run's outcome letters**; `RP:11466` (KB text check, reframe only). Written by `RC:5715-5721`, `DN:2743-2749` | 1b is authored by the model; replay gate passes (`RP:17200-17201`) | Two meanings under one name: free text (the 14 L1/E068/daily-breadth briefs carry 3–7 text entries each) vs exact config. For a decide-next config vehicle, the exact config is **also** in `candidate.start_config` (#21; `DN:2737` vs `DN:2743`) |
| 11 | `scope` (`TPL:56-65`) | Operator's "scope for now": six in/out-of-scope lines | Optional in code. The template says copy it unchanged; the test pins its six lines (`test_e061_c1_7_first_run_kit.py:238-267`) | **No code reader** (template docstring at the test, `:241-242`). Model text: `hypothesis-design/SKILL.md:10,31` and `innovation-expansion/SKILL.md:35,37` refer to "the brief's scope block" | Nothing in code. Decide-next, refold and reframe briefs never carry it, so 1a's "formulas computable from the feeds in the brief's scope block" has no block to read there | Copied into every brief by hand: 1 of 22 operator briefs on disk carries it. Its claim-slot line references are stale: the slot lists are now `SR/tools/claim_tests.py:719` (SELECTORS), `:778` (OUTCOMES), `:838` (BASELINES), `:904` (STATISTICS), `check_spec` `:1110`, not the `:579-881` it cites |
| 12 | `machine_constraints` (`TPL:67-82`) | Container whose `protocol` block becomes the run's protocol file | Not checked. "Effectively mandatory" (`RUNBOOK.md:149`) | `RC:786` (dropped from `research_brief.yaml`); `RC:795-935` (`pre_registration.yaml` written only if present); `RP:10395-10400`; `RP:19649-19669`; `RP:10908-10955` (K3 lint: `protocol` xor `protocol_ref`); pre-flight `RC:3881`, `RC:3994-4060`; `RC:3842` `_folds_from`; `DN:1876-1897` (fold draw needs a generated `protocol`); `DN:2688-2704` (copied to the child); `RC:5698-5722` (refold); `VIEW:438-440` | No `pre_registration.yaml`. Then the grid pre-flight raises FileNotFoundError at run start (`RP:4519-4523`, grid on), or protocol resolution falls to the claim-checked `last_escalation` and raises (`SR/tools/protocol_resolution.py:235-330`, B10) | See #13–#18 |

### 1.2 `machine_constraints.protocol` sub-fields (template and operator brief)

| # | Field | Meaning | Required today? | Code readers | Absent → | Duplicates |
|---|---|---|---|---|---|---|
| 13 | `protocol.symbols` (`TPL:69-70`) | Coins backtested | Required by generation (`RP:10678`, KeyError) | `RP:10678`; `RC:516-535` (vs `market_universe`); `VIEW:439-440`; `DN:1919` (fold data check) | KeyError at run start, before any model call | **= `market_universe`** |
| 14 | `protocol.timeframe` (`TPL:71-72`) | Bar size backtested | Optional, default `"1h"` (`RP:10679`, mirrored `RC:502`, `RP:5823`) | `RP:10679`; `RC:502`; `RP:5814-5830` (residual-IC timeframe) | `1h` | **= `timeframe`** |
| 15 | `protocol.start` (`TPL:76`) | First test day | Required by generation **even with a fold** (`RP:10681`) | `RP:10681`; window cut `RP:10552-10557` (no-fold path); `DN:2620` rewrites it for a fold child | KeyError | With a fold, its windows are discarded (`RP:10622-10633`): it is only printed (`RP:10712-10713`) |
| 16 | `protocol.end` (`TPL:77`) | Last test day | Same (`RP:10682`) | `RP:10682`; refused on the 1st of a month (no-fold path) | KeyError | Same as `start` |
| 17 | `protocol.window_months` (`TPL:78`) | Window length, 1/2/3/4/6/12 | Optional, default 1 (`RP:10625`) | `RP:10625` (no-fold branch only); `DN:2621` writes `BLOCK_MONTHS` (=4, `SR/tools/research_folds.py:69`) for a fold child | Monthly windows | Unused with a fold (`RP:10622-10633`) |
| 18 | `protocol.fold` (`TPL:79-82`, commented; set in the operator brief, per the tour `:82`) | One of the fixed window sets in `SR/config/folds.yaml` (A, B, C in `order`; D outside it, folds flag only) | Optional | `RP:10622-10638` (fold windows); `RP:10724-10725` (`run_context.yaml`); `SR/tools/research_folds.py:410` `fold_of_constraints`; `SR/tools/fold_confirm.py:559`; `VIEW:439`; `DN:2614-2623` and `RC:5701` (write it) | Windows from start/end | Makes #15–#17 dead weight (their values are not used, but #15/#16 must still be present) |

Code also reads these `protocol` keys, which none of the three files carry: `per_symbol_start` (`RP:10680-10681`),
`holdout` (`RP:10444-10470`, must equal the policy reference), `promotion` (`RC:547-607`, `RP` G7), and the alternative
`machine_constraints.protocol_ref` / `protocol_ref_content_hash` (pin; `RP:10908-10955`, RUNBOOK §1a-bis point 4, used by
`FUNDING_MR_*` and `H-041-C-v2` briefs).

### 1.3 Decide-next candidate brief (`forecast_power-run_102-2.md` per the tour; writer `DN:2646-2832`)

Top level, it carries #1–#6 (copied by `DN:2664-2665`; `research_goal` rewritten), #12–#18 (copied from the source
run's `pre_registration.yaml` and moved onto a fold, `DN:2688-2704`), `evaluation.pass_rule.criteria` (#9) for a fold
child under `brief_criteria` (`DN:2801-2809`), and, for a config vehicle only, `constraints` (#10, `DN:2743-2749`).
It never carries `available_data` or `scope`. Its own fields:

| # | Field | Meaning | Required? | Code readers | Absent → | Duplicates / notes |
|---|---|---|---|---|---|---|
| 19 | `candidate` | Marks a decide-next brief | Writer-only | `RP:8146-8158` `_decide_next_candidate` (counts only with #23 or a kept-criteria fold child, `RP:8160-8172`); `RP:6144` (`candidate.composition`); `RP:5854-5890` | An ordinary brief | An operator cannot use it: without `source` + `criteria_from` it is ignored |
| 20 | `candidate.claim` | Pre-filled claim block (statement, kind, tests, pass_if, fail_if, rationale) | Side findings only (`DN:2723`) | `RP:17307-17316` `_prefilled_claim` (1a copies it, D-139); `RP:18153-18170` (fold-frozen claim note) | 1a writes the claim | **Duplicate**: the same claim is also copied into `candidate.source.proposal.claim` (`DN:2712-2717` copies `claim` into `proposal`) |
| 21 | `candidate.start_config` | Source run's base config with the finding's change | Side findings with a start config (`DN:2737`, `:2763`) | `RP:16793-16834` (written to `artifacts/start_config.json`, given to 1b); `RP:16836-16860` (deviations); `SR/tools/fold_confirm.py:454-475` (did 1b change it?) | 1b authors from the card | For a config vehicle, **duplicate of the exact config in `constraints`** (`DN:2737` and `DN:2743-2746`) |
| 22 | `candidate.start_manifest` | Block manifest for that config | Same | `RP:16802-16803`; `nearest_build` start manifest (`RP:16851`) | — | Same duplication with the `constraints` manifest entry (config vehicle). The tour noted its `rationale` text can contradict the config's weights |
| 23 | `candidate.criteria_from` | Same meaning as #8, under `candidate` | Written unless the fold child keeps criteria (`DN:2811`) | `RC:845-847`; `RP:8154`, `RP:8411` | With #9 instead: criteria fixed at launch (D-121) | Same name as #8, two places |
| 24 | `candidate.source.origin` | `reader` / `composition` | Writer | `RP:5870` (`composition` exempts residual IC) | — | Queue entry also carries `origin` (`RC:5127`) |
| 25 | `candidate.source.proposal_ref` | Analyst proposal pointer | Writer | `SR/tools/fold_confirm.py:391-395`; `SR/tools/explore_confirm.py:808-814`; `RP:18167` | Fold confirmation finds no claim | Queue entry also carries it (`RC:5127`) |
| 26 | `candidate.source.source_run` | Run the finding came from | Writer | `SR/tools/block_registry.py:589` | — | Also in `proposal_ref` and `research_goal` text |
| 27 | `candidate.source.parent_hypothesis_id` | Source idea | Writer | `SR/tools/block_registry.py:590` | — | Also in `research_goal` text |
| 28 | `candidate.source.hypothesis_id` | Id 1a must give the card | Writer | `RP:8404-8410` (card id must match); `RP:6212` (composition) | Refused before 1b | — |
| 29 | `candidate.source.decision_ref` | Decision record pointer | Writer | No brief reader (the queue entry carries its own copy, `RC:5295`) | — | Duplicate of the queue entry field |
| 30 | `candidate.source.proposal` | Copy of the analyst proposal (kind, claim, evidence, config_change, vehicle, combines_as, fold_observed) | Writer | `RP:16974-16990` (`vehicle`, `combines_as`); `SR/tools/block_registry.py:585` (`kind`); `RP:5874-5876` (`block.kind`) | — | `claim` = #20; `evidence` and `config_change` are restated in `research_goal` |
| 31 | `candidate.source.base_config_ref` | Source base config path | Writer | `RP:6267` (composition / patch only) | — | — |
| 32 | `candidate.source.start_config_sha256` / `config_change_ops` | Fingerprint of #21; the change as config paths | Writer (`DN:2740`, `:2766-2768`) | **No code reader** (grep; `fold_confirm.py:634` is a comment, the comparison at `:462` uses #21 itself) | — | Derivable from #21 |
| 33 | `candidate.source_observations` (D-205) | Source run's memory observations, verbatim | Writer (`DN:2812-2815`, keys `DN:2630`) | **No code reader** outside tests (`SR/tests/test_d201_d205_decide_next.py`). Reaches 1a only as text in `research_brief.yaml` | — | Some entries are code-written stand-ins ("Not reported by the model", per the tour) |

Patch and composition candidates carry other keys that the tour's example does not have: `candidate.config`,
`candidate.manifest`, `source.expected_config_sha256` (`RP:6261`, `:8500`, `:16584`), `source.expected_manifest_sha256`
(`RP:8534`), `source.resolved_patch`, and `candidate.composition` (`RP:6144-6165`).

### 1.4 Keys the code reads that none of the three files carry (for completeness)

`research_only` (written by `RC:790`, read by `RP:15626-15695`, holdout hold); `refold` (`RC:4417`, `RP:5221-5230`,
written by `RC:5723`); brief-level `origin` / `composition` (`RP:5870`); `funding_interval_hours`, `rebalance_hours`
(`VCE:472`, `:491`); `existing_context` (`RP:11466`, reframe only); `significance_methodology` (1b skill text,
`strategy-config-authoring/SKILL.md:56`); legacy `brief_id`, `lineage`, `hypothesis`, `gate_definition` (refinement
YAML briefs, `RC:1047`).

---

## 2. `criteria_from` / `constraints`, answered from code

### 2.1 What each name actually means (the operator's reading needs one correction)

- `criteria_from: hypothesis_generation` is about **pass/fail criteria only** (menu ids from `SR/config/criterion_menu.yaml`).
  It is **not** about the claim. The claim (statement plus claim-tests) is a separate block of the 1a card
  (`hypothesis-design/CLAIM_TESTS.md`, checked by `SR/tools/claim_card.py`, flag `claim_tests`).
- **An operator brief has no field for a claim today.** Only a decide-next brief can pre-fill one (`candidate.claim`).
  It is read only through `_decide_next_candidate` (`RP:8146-8158`), which requires a `candidate` block with
  `criteria_from` or with `source` plus kept criteria. So a claim "given in the brief" is possible only for decide-next.
  Criteria "given in the brief" are possible for anyone (D-121 `evaluation.pass_rule.criteria`, needs `brief_criteria`).
- `constraints` is a free-text list for the model steps. Two of its entries become an **authoritative strategy config**
  and **block manifest** when they begin with the fixed sentences (`RP:16912`, `:16949`) **and** `exact_config_1b` is on.
  With the flag off they are only text (the replay gate, `RP:17186`, still compares 1b's config to them when
  `config_replay_gate` is on). The run viewer reads a third kind of entry: "Pre-registered outcomes" (`VIEW:377-388`).

### 2.2 Combinations (criteria side)

| Brief carries | Launch (`_materialize_run`) | Run start (`run_loop`) | After 1a | Net effect |
|---|---|---|---|---|
| `criteria_from` only (the template default) | `pass_rule: null` plus `pass_rule_pending: hypothesis_generation` (`RC:843-856`) | Grid pre-flight deferred while pending (`RP:19684-19686`, `RP:8197-8201`) | `_write_pass_rule_from_card` (`RP:8386-8452`, called `RP:20127`) builds `pass_rule` from the card's criteria, lints it, runs the pre-flight; D-192 consistency warnings (`RP:8445-8449`) | 1a picks criteria. This is the normal path |
| `evaluation.pass_rule.criteria` only, `brief_criteria` **on** | Menu lint, then resolved against the menu (`RC:862-920`) | Pre-flight runs and passes (menu-shaped) | `_write_pass_rule_from_card` returns `False` (`RP:8399-8400`): **1a still runs and still writes `criteria` in its card (menu given under config-direct, `RP:9064-9068`), and they are silently unused**; no D-192 check | Criteria fixed by the brief |
| `evaluation.pass_rule.criteria` only, `brief_criteria` **off** | B11 lint: "dict-shaped but has no outcomes" (`RP:11348-11350`) → **refused at launch** (`RC:879-883`) | — | — | The template's commented example fails with the flag off |
| **Both** | **Refused**: "says its criteria come from step 1a ... but also carries a pass_rule" (`RC:850-855`) | — | — | Mutually exclusive |
| **Neither** | `pass_rule: null`, **no** pending marker | Grid **on**: pre-flight not deferred → `_check_specialist_readers_preflight` raises "pass_rule is not menu-shaped" (`RP:4524-4528`) → run `failed` before any model call (`RP:19687-19690`). Grid **off**: continues | Grid off: 1a writes criteria in the card; nothing copies them (`RP:8399-8400`); `pass_rule` stays null → `legacy_not_evaluable` at evaluation (VCE R3, `VCE:339-342`) | With the grid: an early, cheap failure. Without it: a run with no pre-registered criteria |
| `criteria_from` but **no** `machine_constraints` | Whole block skipped (`RC:798` guard): no `pre_registration.yaml`, no marker | Grid on: FileNotFoundError at the pre-flight (`RP:4519-4523`) | Grid off: `_write_pass_rule_from_card` raises FileNotFoundError (`RP:8430-8433`), **after the 1a spend** | Fails |

### 2.3 Combinations with an exact config (`constraints`), including the case the operator flagged

| Brief carries | 1a | 1b | Coherence of claim and config |
|---|---|---|---|
| Exact config + `criteria_from` (e.g. `briefs/rebase_run_095_standardised_host.md`) | Model call. Reads the whole `research_brief.yaml`, so it **sees the config JSON as text**; writes card, claim and criteria → `pass_rule` | `exact_config_1b` on: written by code from the brief (`RP:17089-17150`, called `RP:20082-20083`); no model. Off: model, config is text | 1a writes the claim knowing the config. No code checks that the claim is *about* that config, apart from the claim-visibility revision request after 1b (`CLAIM_TESTS.md`: a test must read the block's own output; `RP:17904`) |
| **Exact config, no `criteria_from`, with `evaluation.pass_rule`** (the operator's case, with criteria) | Model call; its criteria unused (2.2 row 2) | By code (flag on) | **The strategy is dictated; the claim is written by 1a after the fact, from the goal text and the config text.** The criteria were fixed without a claim. Nothing refuses this |
| **Exact config, no `criteria_from`, no `evaluation`** (the operator's case, literally) | Grid on: never reached (fails at run start, 2.2 "Neither"). Grid off: model call; pass_rule null | Grid off: by code (flag on) | Grid on: refused for missing criteria (not for "config without claim"). Grid off: a dictated config, a 1a claim, no pre-registered criteria |
| Exact config + `refold: {source_run, fold}` (`RC:5691-5731`, D-122) | **Skipped**: the source's card is copied (`RC:5751-5752`) | By code; refused unless the source's config and manifest are unchanged (`RC:5744-5749`) | Intended: no `criteria_from`, the source's pass_rule is copied in at launch (`RC:5755-5756`). **The only designed "constraints without criteria_from" path** |
| Decide-next config vehicle (`DN:2743-2749`) | Model; claim pre-filled from `candidate.claim` | By code | `criteria_from` sits under `candidate` (or `evaluation` for a fold child), not at top level. Coherent by construction |
| Exact config without the manifest entry | — | Refused at 1b, before anything is written: "carries an exact config but no exact block manifest" (`RP:17119-17122`) | Caught late (run start, after 1a) |
| Exact config whose JSON is broken | — | `_exact_config_1b_mode` returns True (`RP:17085-17086`), then 1b refuses (`RP:17113-17114`) | Caught after 1a |

**Answer to "what happens if we give constraints without criteria_from?"**: with the grid on and no criteria anywhere,
the run is refused at start, before any spend, but for missing criteria. With criteria given, it runs: 1b builds the
dictated config and 1a writes a claim that nothing ties to that config. So the gap the operator saw is real for the
"criteria given + config given" path. Only the refold uses this shape by design.

---

## 3. Proposed structure

Principles: two parts (Idea, Trading parameters). Mandatory = `strategy_domain`, `research_goal`, `venue`, `product`.
Everything else optional, with the default the code would apply. Renames only for the two names the operator found
unclear (`criteria_from`, `constraints`) and the fields bound to them. `machine_constraints` leaves the hand-written
brief; code writes it at launch.

### 3.1 Template sketch (frontmatter)

```yaml
---
# research_brief_new_pipeline.md -- step 0, idea intake.  (instructions unchanged: copy, fill, register)
# Claims and criteria: see <claim guideline doc>.  Test periods: see <fold guideline doc>.

# ======================= PART 1: IDEA =======================
# MANDATORY
strategy_domain: "<FILL IN>"          # one- or two-word label for the kind of idea
research_goal: >                       # the idea, word for word, from whoever gave it
  <FILL IN>

# OPTIONAL (leave out = decided by the workflow)
available_data: none                   # default none; data beyond price bars (scope doc lists what exists)
pass_criteria: []                      # default empty = step 1a picks from config/criterion_menu.yaml
                                       #   (was: criteria_from: hypothesis_generation / evaluation.pass_rule.criteria)
                                       #   a list of {id: <menu id>} -- see the claim guideline, "Criteria"
given_strategy_config: null            # default null = step 1b authors the config from 1a's card
                                       #   (was: constraints entry "Build EXACTLY this strategy config (JSON)")
given_block_manifest: null             # required when given_strategy_config is set
                                       #   (was: constraints entry "Use EXACTLY this block manifest (JSON)")
notes_for_steps: []                    # default empty; free-text instructions to the model steps
                                       #   (was: every other constraints entry)
# claim_ref: <path>                    # OPEN QUESTION Q4 -- a claim file checked like a card's claim

# ================== PART 2: TRADING PARAMETERS ==================
# MANDATORY
venue: "<FILL IN>"                     # exchange (config/venue_tradability.yaml)
product: "<FILL IN>"                   # spot or perp on that venue

# OPTIONAL (leave out = default below)
market_universe: null                  # default: OPEN QUESTION Q1 (code has none today)
timeframe: null                        # default "1h" (today's code default, RP:10679 / RC:502 / VCE:440);
                                       #   never above "1d" (operator rule) -- refused at registration
fold: null                             # default: OPEN QUESTION Q2; one of the folds in config/folds.yaml
                                       #   (replaces machine_constraints.protocol start/end/window_months/fold)
---
```

Removed from the hand-written brief: `criteria_from`, `evaluation`, `constraints`, `scope` (moved to a standing doc,
Q3), and the whole `machine_constraints` block. Code writes `machine_constraints` at launch from `market_universe`,
`timeframe` and `fold`: `symbols` and `timeframe` from the brief, and `start`/`end` from `research_folds.fold_span`
(`SR/tools/research_folds.py:234`), as `DN.fold_protocol` already does (`DN:2614-2623`). Decide-next, refold and reframe
briefs, which are machine-written, keep writing `machine_constraints` as today.

### 3.2 Mapping old → new

| Old | New | Why |
|---|---|---|
| `criteria_from: hypothesis_generation` (brief level) | removed; **absence of `pass_criteria` means "step 1a picks"** | Operator: "why forcing a static value instead of accepting empty field". Code then sets the pending marker itself (`RC:843-856`) |
| `evaluation.pass_rule.criteria` | `pass_criteria` | One field, one name; the operator found the pair unclear |
| `constraints[...]` "Build EXACTLY this strategy config (JSON)" | `given_strategy_config` (a mapping, no sentinel sentence) | "constraints" does not say "authoritative strategy config" |
| `constraints[...]` "Use EXACTLY this block manifest (JSON)" | `given_block_manifest` | Same |
| `constraints[...]` other text | `notes_for_steps` | Separates text for the model from data for code |
| `constraints[...]` "Pre-registered outcomes" (viewer) | prose "Pre-registered outcomes" section (already in `TPL:121-129`); `VIEW` reads it there | The template already moved outcomes to prose; the viewer still looks in `constraints` |
| `machine_constraints.protocol.symbols` | `market_universe` (only) | Duplicate |
| `machine_constraints.protocol.timeframe` | `timeframe` (only) | Duplicate |
| `machine_constraints.protocol.fold` | `fold` | Moves to Trading parameters |
| `machine_constraints.protocol.start/end/window_months` | removed from the operator brief | Operator: "keep only the fold capability"; unused with a fold today |
| `scope` | standing scope doc (Q3) | Kept as instruction, not copied per brief |
| `candidate.criteria_from` (decide-next) | unchanged, or `candidate` omits it and absence means 1a (same rule as above) | Keep one meaning across writers |

### 3.3 Defaults (what code would apply when a field is absent)

| Field | Default | Applied where (today's code or proposed) |
|---|---|---|
| `available_data` | `none` | No code reader; text only |
| `pass_criteria` | step 1a picks | `RC:843-856` today keys on `criteria_from`; proposed: key on "no `pass_criteria`, no `refold`, not a kept-criteria candidate" |
| `given_strategy_config` / `given_block_manifest` | 1b authors | `RP:17078-17086` (no exact config → model 1b) |
| `notes_for_steps` | `[]` | Text only |
| `market_universe` | Q1 | Today `RP:10678` KeyErrors without symbols |
| `timeframe` | `"1h"` | Existing defaults `RP:10679`, `RC:502`, `VCE:440` |
| `fold` | Q2 | `RP:10622` (fold windows) once `start`/`end` are derived from the fold |
| `scope` | standing doc | Q3 |

**"Decided later in a workflow step"** (operator, for timeframe, fold and others): the protocol is generated at the
start of `run_loop` (`RP:19649-19669`), **before** step 1a. A value left empty must therefore be either a code default
at launch, or protocol generation moves after 1a, which already writes a `timeframe` in its card
(`SR/tools/explore_confirm.py:127`). That is a real choice (Q2).

**"Never above daily"**: no code caps the bar size today. `SR/tools/timeframe.py` parses up to `1w` (`_UNIT_SECONDS`),
and the scope line "Hourly or daily bars" is a fact about the Kraken caches on disk, not a rule. Proposed: a registration
check `timeframe_seconds(timeframe) <= 86400`, plus the scope line reworded to "any bar size up to daily; weekly or
monthly out of scope (operator rule); today's caches are 1h and 1d".

### 3.4 The two separate documents

**A. Claim guideline** (proposed home: next to `SR/workflow_artifacts/skills/hypothesis-design/CLAIM_TESTS.md`, read by
1a, 1b, the analyst, decide-next and brief writers). Outline, from what the brief and template carry today:

1. What a claim is: the operator's definition from the tour remarks (an idea about market behaviour, with
   quantitative tests and pass criteria that would prove it).
2. Claim vs criteria: the claim block (`statement`, `kind`, `tests`, `pass_if`, `fail_if`, `rationale`, the shape of
   `candidate.claim`) vs pass criteria (`pass_criteria`, menu ids, `card_overridable` overrides; D-121).
3. Test slots, taken from `TPL:64`'s scope line, with lines corrected to code: selector (all, event, regime, regime_change,
   calendar, quantile; `claim_tests.py:719`), outcome (fwd_return, fwd_volatility, fwd_max_drawdown, trend_ends; `:778`),
   baseline (complement, placebo, other_selector; `:838`), statistic (mean_diff, rank_ic, hit_rate, decay_curve; `:904`).
   Anything else is refused by `check_spec` (`:1110`) before any data is read.
4. Floors (min events, min windows), `signal` paths, `direction`, horizons: from the candidate claim example and
   `CLAIM_TESTS.md`.
5. Where a claim comes from: 1a writes it; decide-next pre-fills it (`PREFILLED_CLAIM.md`, D-139); an operator brief
   (only if Q4 is accepted).
6. How criteria are picked: `hypothesis-design/SKILL.md` step 2b rules 1–6 (`:43-49`).
7. Pointers it would absorb or link: `CLAIM_TESTS.md`, `CLAIM_TESTS_EXECUTION.md`, `CLAIM_TESTS_TRADE.md`,
   `PREFILLED_CLAIM.md`, `strategy-config-authoring/CLAIM_NOTE.md`.

**B. Fold creation guideline** (proposed home: `SR/docs/`, beside RUNBOOK §1f). Outline, from `TPL:73-82` and the code:

1. What a fold is: a fixed set of six 4-month blocks in `SR/config/folds.yaml` (`BLOCK_MONTHS`, `research_folds.py:69`);
   A, B, C in `order` (`:62`), D outside it (`:65`), D only with `orchestrator.folds` (`RP:10630-10633`, D-115).
2. How a run gets a fold: the operator names it; decide-next draws one among the folds its source is not on (D-123,
   `research_folds.draw_fold` `:278`, data check `DN:1899`); the refold command (D-122, `RC:5691`).
3. Rules code enforces: research period only (`research_folds.py:113`); never the sealed holdout (referred to only via
   `SR/config/campaign_data_policy.yaml`); validation period refused except fold D's exact blocks (`RP:10583-10604`);
   the coin must exist for every window (data gate).
4. Window-count floors (`criterion_menu.yaml` `floor.min_windows`; RUNBOOK §1f "Limits").
5. Legacy `start`/`end`/`window_months` rules (`RP:10552-10557`, end not on the 1st of a month), for machine-written
   briefs only, or retired (Q7).
6. Pointers: RUNBOOK §1f (`SR/docs/RUNBOOK.md:470`), USER_GUIDE fold section (`SR/docs/USER_GUIDE.md:3108`).

---

## 4. Impact list for a later build window (checklist; nothing implemented)

**Parser and launch (`RC`)**
- [ ] `CRR:29-30` `REFRAME_BRIEF_REQUIRED_KEYS` → split into an operator-required set (4 keys) and the reframe set.
  `RP:7974-7983` (reframe writer) fills the six from the source run; decide whether it keeps six.
- [ ] `RC:701-703` required loop; add the `timeframe <= 1d` check; `<FILL IN` scan unchanged (`RC:719-727`).
- [ ] `RC:5866-5867` dry run reads `brief['market_universe']` by subscript (KeyError once optional).
- [ ] `RC:454-545` `_lint_brief_protocol_agreement`: moot for operator briefs (no duplicate); keep for machine-written ones or delete.
- [ ] `RC:777-935` `_materialize_run`: build `machine_constraints` from `market_universe`/`timeframe`/`fold` when absent; map `pass_criteria` → `pre_registration.pass_rule`; set the pending marker on absence (not on `criteria_from`); always write `pre_registration.yaml`.
- [ ] `RC:3881-3917`, `RC:3994-4090` launch pre-flight: rebuild a fold-only protocol (no `start`/`end` in the brief).
- [ ] `RC:5691-5731` `refold_brief` and `RC:5733-5761` `_launch_refold`: write and read `given_strategy_config`/`given_block_manifest`.
- [ ] Registration: refuse `given_strategy_config` without `given_block_manifest`, and broken JSON, at registration instead of at 1b (`RP:17113-17122`).

**Orchestrator (`RP`)**
- [ ] `RP:10649-10729` `_ensure_protocol_from_constraints`: `start`/`end` from `fold_span` when `fold` is set (`RP:10681-10682` KeyError today); `RP:10607-10638` unchanged.
- [ ] `RP:16916-16971` `_brief_exact_config` / `_brief_exact_manifest`: read the new keys; keep the prefix reading for already-materialized runs (resume).
- [ ] `RP:17078-17086`, `RP:17089-17150`, `RP:17186-17215`: messages and readers follow.
- [ ] `RP:8146-8184` `_decide_next_candidate`, `_candidate_keeps_brief_criteria`, `_brief_criteria_from_1a`; `RP:8386-8452` `_write_pass_rule_from_card`: "absent = 1a" semantics; refold excluded.
- [ ] `RP:19675-19690` grid pre-flight deferral follows the marker (no change if materialization sets it).
- [ ] `RP:9036-9070`: add the standing scope doc (Q3) and the claim guideline to the 1a (and step 2) handoff, as the criterion menu is added today.
- [ ] `RP:11441-11470` KB reactivation reads `constraints` of `next_research_question`: follow the rename.

**Tools and viewer**
- [ ] `DN:2646-2832` `candidate_brief`: `constraints` (`:2743-2749`) → new keys; criteria (`:2801-2811`); decide on `source_observations` (`:2812-2815`, `:2630`), the `proposal.claim` duplicate, `start_config_sha256`/`config_change_ops` (no reader) — Q9.
- [ ] `DN:1515-1560` `composition_brief` (same front keys; `candidate.criteria_from`).
- [ ] `VIEW:417-442` `read_brief`: `fold`/`symbols` from the new top-level keys (fallback to `machine_constraints.protocol` for old briefs); `VIEW:377-388` outcomes from the prose section (today only from `constraints`). Note: the viewer reads only `briefs/` (`VIEW:398-415`), never `candidate_briefs/`.
- [ ] `VCE:439-450` `_bar_hours` (default `1h`, unchanged); `SR/tools/fold_confirm.py:454-475` (unchanged unless `candidate` is reshaped).

**Template, skills, docs**
- [ ] `TPL` rewritten (3.1); legacy `SR/workflow_artifacts/templates/research_brief.yaml` (free-text `constraints`) aligned or retired.
- [ ] `hypothesis-design/SKILL.md:10,31`, `innovation-expansion/SKILL.md:35,37` ("the brief's scope block") → the standing scope doc.
- [ ] `hypothesis-design/DECIDE_NEXT_CANDIDATES.md:5,47`; `campaign-review/RETIRED_ROUTING.md` (reframe brief shape).
- [ ] Handoff `SR/workflow_artifacts/templates/handoffs/research_brief_to_hypothesis.yaml:5-8` reason text.
- [ ] `SR/docs/RUNBOOK.md` §1a-bis (`:144`, point 1 "machine_constraints is effectively mandatory" no longer true for operator briefs), §1f (`:470`); `USER_GUIDE.md` fold section; `OPERATOR_START_CAMPAIGN.md`.
- [ ] The two new docs (3.4).

**Tests to update**
- [ ] `SR/tests/test_e061_c1_7_first_run_kit.py`: `_PLACEHOLDER_LINES` (`:96-108`, 11 placeholders, `:229`), `criteria_from` pin (`:208`), `machine_constraints` shape (`:210-221`), `scope` six lines (`:238-267`), uncomment tests (`:270-306`), K3 lint on template (`:405-410`), registration lints (`:497-690`).
- [ ] `test_d121_brief_criteria.py` (`:198-202` pins "D-121" and `whole_test_sharpe_positive` in `TPL`).
- [ ] Decide-next writers: `test_e059_s2a_decide_next.py`, `test_e059_s2a_review_fixes.py`, `test_d201_d205_decide_next.py` (source_observations), `test_e068_9_one_proposal_start_config.py`, `test_d162_config_vehicle_routing.py`, `test_d133_retired_for_blocks.py`, `test_e077_folds.py`, `test_e060_s3b_composition_wiring.py`.
- [ ] Exact config / refold: `test_exact_config_1b.py`, `test_config_replay_gate.py`, `test_d122_refold.py`.
- [ ] Criteria and materialization: `test_c51_menu_criterion_lint.py`, `test_d134_plain_ic_criterion.py`, `test_d137_residual_ic_pickable.py`, `test_d192_criterion_consistency.py`, `test_d139_prefilled_claim_kept.py`, `test_e059_s2b_briefs.py`, `test_retry_robustness_r2_hold.py`, `test_k3_protocol_pinning.py`, `test_c5_6_no_promotion_for_config_direct.py`.
- [ ] Required keys / reframe: `test_venue_tradability.py`, `test_e059_6c_s2b_campaign_review.py`, `test_e059_6c_s2b_review_fixes.py`, `test_e061_end_to_end_wiring.py`, `test_e061_c1_4_5_pauses_preflight.py`.
- [ ] Windows/folds: `test_window_months.py`, `test_d115_fold_d.py`, `test_e068_s2_claim_card.py`.
- [ ] Viewer: `test_run_viewer.py` (`:317` asserts outcome letter A from a `constraints` entry) and fixtures `SR/tests/fixtures/run_viewer/briefs/*.md`, `.../runs/run_098|run_099/artifacts/research_brief.yaml`, `SR/tests/fixtures/cul_405/run_072/research_brief.yaml`.
- [ ] New tests: 4 mandatory keys; absent `pass_criteria` → pending marker; `given_strategy_config` without a manifest refused at registration; fold-only protocol generation; `timeframe` above `1d` refused.

**Migration**
- [ ] Operator briefs in `SR/briefs/`: 22 Markdown files with frontmatter (1 without; 1 YAML refinement brief). Only briefs still queued (not `done`) need migrating; check `SR/config/campaign_queue.yaml` status first.
- [ ] Candidate briefs in `SR/campaign_record/candidate_briefs/` (15 on this checkout); queued or held ones need the new keys or a loader shim.
- [ ] Refold briefs (4 `refold_run_*` in `SR/briefs/`).
- [ ] Already-materialized `runs/*/artifacts/research_brief.yaml`: readers keep accepting the old keys for resumed runs (shim in `_brief_exact_config`, `_brief_exact_manifest`, `VIEW.read_brief`).

---

## 5. Open questions for the operator (only where the code leaves a real choice)

- **Q1. Default coin when `market_universe` is absent.** Code has no default (`RP:10678`). Options: a fixed default
  (BTCUSDT, the most-used coin), or a required field after all, or step 1a chooses (needs Q2's "after 1a" option).
- **Q2. "Decided later" for `timeframe` and `fold`.** The protocol is generated before 1a (`RP:19649-19669`). Options:
  (a) code defaults at launch: `1h`, and a fold drawn by code with the decide-next draw (`research_folds.draw_fold`,
  seeded by the brief id, among A–C); (b) move protocol generation after 1a and take 1a's card `timeframe` and a
  choice of fold. (a) is a small change; (b) changes the run order and every pre-flight that reads the protocol early.
- **Q3. Where the scope lives.** (a) a standing doc (for example `SR/config/research_scope.md`) that code adds to the
  1a and step 2 inputs for every brief, decide-next included (today they get none); a brief may add `notes_for_steps`;
  or (b) keep `scope` in the brief as an optional override of the standing doc.
- **Q4. An operator-given claim.** The operator asked for "a separated structurally checked claim object with reference
  only". Option: `claim_ref: <path>` to a claim file, checked at registration by `SR/tools/claim_card.py`, and fed to
  1a through the existing pre-fill path (`_prefilled_claim`, `RP:17307`), which today works only for decide-next. Related
  rule to decide: should a brief that gives `given_strategy_config` **also** have to give `pass_criteria` or `claim_ref`,
  or be refused at registration? (Today the code allows "config + criteria, no claim", section 2.3.)
- **Q5. Criteria field name.** `pass_criteria` (proposed) or keep `evaluation.pass_rule.criteria`. The latter is the
  name decide-next, the menu lint and `pre_registration.yaml` use.
- **Q6. Migration style.** Rewrite the queued brief files once, or have the parser map old keys to new for a while.
- **Q7. Legacy window and pin keys.** For operator briefs, retire `start`/`end`/`window_months` and `protocol_ref` pins
  completely, or keep them as an escape hatch for machine-written briefs (decide-next still writes `start`/`end`
  next to `fold`, `DN:2620-2622`).
- **Q8. Bar sizes between 1h and 1d (for example 4h).** The rule "never above daily" allows them, but no Kraken cache
  exists for them, and no brief field sets `trading.fetch_interval_seconds` (`TPL:63`). Allow them in the brief now,
  or keep `1h`/`1d` only until a resampled cache exists?
- **Q9. Decide-next brief content (operator asked "why source observations?").** `candidate.source_observations` has
  no code reader and reaches 1a only as text; `source.start_config_sha256` and `config_change_ops` have no reader;
  `candidate.claim` is duplicated in `source.proposal.claim`; the config vehicle's config is duplicated in `constraints`
  and `candidate.start_config`. Keep, drop, or move to a pointer?
- **Q10. Flags.** The new criteria and given-config fields would still depend on `brief_criteria` and `exact_config_1b`
  (both off in this checkout's committed config). Keep the flags as switches for the new fields, or treat the
  restructure as switching them on for good?

## Not checked

- The two example briefs themselves (absent on this checkout, no git history). Their line numbers are taken from the
  tour's Speech; their shapes are checked against the writer code and two on-disk substitutes.
- The operator's live `campaign_config.yaml` (flag values on the live box).
- Whether step 1b receives `research_brief.yaml`. Its handoff template
  `SR/workflow_artifacts/templates/handoffs/hypothesis_to_strategy_config_authoring.yaml` does not list it, and no code
  adds it (grep). The tour said 1b gets the brief verbatim; not reconciled.
- Whether the data-availability gate can build a 4h bar from the 1h cache (`SR/docs/DATA_AVAILABILITY.md:25-38` not read).
- Which queued entries still point at old-shape briefs (`SR/config/campaign_queue.yaml` statuses not tallied).
- The behaviour of every `RC` pre-flight branch (`RC:3994-4210`) with a fold-only protocol; only its entry points were read.
- No test was run; every test listed in section 4 was found by grep, not by running it.
