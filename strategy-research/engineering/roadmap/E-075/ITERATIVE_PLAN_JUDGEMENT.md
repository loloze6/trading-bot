# Judgement of the iterative plan v2 (A1.10) and of the A1.9 interpretation

Read-only, 2026-10-08. Line numbers are on the `plan-amend` worktree unless marked "main checkout" (saved runs). No test, backtest or model call was run; no cache, no holdout.

## 0. Facts verified in code that the judgement rests on

- `claim_measure.measure_test` already returns, per horizon, the pooled effect AND the per-window effects (`per_window`), plus `windows_with_claimed_sign / windows_with_a_value` (`tools/claim_measure.py:185-192`; computed in `claim_tests.effect_sizes`, `tools/claim_tests.py:1042-1045, 1060`). Confirmed on a saved run: main checkout `runs/run_074/artifacts/variants/base/claim_test.yaml` shows `windows_with_claimed_sign: 6`, `windows_with_a_value: 6` and a `per_window` map at h=1.
- The claim-test vocabulary already has a `consistency: {unit: window|era, min_same_sign: k}` slot (`claim_tests.py:717, 832-836, 1145-1151`). It is only acted on by the parked verdict path; `claim_measure` ignores it.
- `test_sign` holds when every horizon with a value has `oriented > 0`, and treats `no_events` as not held (`tools/explore_confirm.py:697-715`). No size rule, no window rule.
- The parked p-value path (`run_test(calibrated=True)`, `_graded`, block permutation, calibration gate) exists (`claim_tests.py:990-1019, 1064-1155`) but is parked by operator decision (CUL-394 / D-077, module docstring `:16-26`) and can recompute the signal only for Donchian and Keltner (`SIGNALS`, `:232`).
- The repeat gate's key already contains the window fingerprint: `novelty_key = (forecast_hash, symbols, timeframe, "windows:" + windows_sha256)` (`tools/novelty.py:186-207`, fingerprint `:168`). With fixed folds this IS "a config runs on a given fold once"; no code change is needed, only a test.
- `finding_route` sends price-only claims to IN_RUN and block claims to PENDING (`explore_confirm.py:677-694`); `resolve_pending` measures the child run's own card tests on the child's base variant, on the E-072 confirmation split, marks it `weak`, and sets `not_comparable` when the spec hashes changed (`:865-929`). The "measure the child's own tests, compare spec hashes" logic is reusable; the split and the `weak` label are not.
- decide-next copies the parent's `machine_constraints` (windows) into the child (`tools/decide_next.py:2129-2131`); the child's start config is the source run's base config plus the finding's config change (`side_finding_start`, `:2153-2168`); the pre-filled claim is copied unchanged (`:2145-2148`). So `vehicle: same_strategy` = empty config change already works mechanically. Lineage is recorded as `source_run` / `parent_hypothesis_id` (`:2132-2137`).
- `CLAIM_KINDS` has no strategy-behaviour kind; `check_claim` refuses unknown claim keys (`tools/claim_card.py:50-54, 62-63, 164-171`). `KIND_BLOCK` maps forecast/regime kinds only (`:57-61`).
- Ranking of reader candidates is by self-scores (`rank_key`, `decide_next.py:1900-1906`).
- Memory shown to readers carries the largest exploratory effect and k/6 window counts (`tools/reader_findings.py:285-334`).
- The combiner takes forecast blocks on one timeframe and gates by regime; nothing else (`tools/composition.py:10-38, 79`).
- `bars.csv` carries `close/high/low/forecast/regime/allocation_change/postRebalance_current_allocation` (main checkout run_074 header); `trades.json` is per window; `trade_diagnostics.json` is one file per variant (`runs/run_074/variants/base/trade_diagnostics.json`). The E-074 exit classifier is specified from `exit_forecast` + the exit row's allocation, measured 74% reductions / 26% flips on run_074 (`roadmap/E-074/PHASE_A.md:382-408`); it is not built (no `tools/exploration_digest.py` in the tree). `exit_reason` in the engine's own file is 99% `signal_flip` (A5, `docs/DATA_DICTIONARY.md:175, 666-672`); MAE/MFE/exit_efficiency are A6 and `after` fields (`:190-193`).
- Trades per 4-month block at 1h: 1,477-1,615 per window on run_074 base (counted, main checkout). At 1d: 70-87 (A1.7 fact 7).
- E-075's tool design is six typed query functions behind an SDK MCP server with `tools=[]`, a deny hook and caps (`roadmap/E-075/PHASE_A.md:73-126, 129-244`); its slice 1 includes a placebo outcome layer and recomputed trade outcomes in both arms (`:165-174, 478-494`); per session about $0.67-1.20 (`:411-437`).

## 1. Answers to A1.10's four questions

### Q1. Is Stage 1 the smallest loop that can produce a confirmed claim of each kind?

Nearly. Three things are missing that block a confirmed claim; three things are already there or over-built.

Missing (each blocks one claim kind):
- The claim record cannot hold a strategy claim: add one kind, `execution_behaviour`, to `CLAIM_KINDS` (`claim_card.py:50-54`). Put `vehicle`, `combines_as` and `fold_observed` on the proposal envelope (E-075 `proposal.yaml`, `PHASE_A.md:227-244` already has `variant`, `falsifier`, `citations`), not inside the `claim` mapping, so `check_claim` and step 1a's unchanged copy keep working.
- The confirmation routing is still E-072's: `finding_route` sends price-only claims to IN_RUN (`explore_confirm.py:694`). Under the fold design every claim is pending until its child runs. One small function `confirm_on_fold(child_run)` replaces `resolve_pending`: measure the child's card tests on the child's base variant over all its windows (the fold), keep the `tests_changed_from_finding -> not_comparable` rule (`:918-926`), drop the split and the `weak` label, write the fold into the ledger row.
- The analyst's proposal must reach decide-next: write it in the reader-proposal shape (`artifacts/proposals/<lens>.yaml`, kind `side_finding`) so `decide_next` takes it with no new candidate source. A1.10 does not say this.

Already there or over-built:
- "A config runs on a given fold once" is free: the novelty key contains the windows fingerprint (`novelty.py:186-207`). Ship a test, not code.
- "The E-074 grid as a parameterised tool": `conditional_effect(by=window|coin)` and `trade_slice(by=...)` (`E-075/PHASE_A.md:194-196`) already are the grid, one cell per call. Do not build a separate grid tool. `trailing_vol` is already a field (PR #348).
- The placebo arm and its outcome layer (`PHASE_A.md:165-174, 247-335`): with D4 (process checks, no statistical go rule) and folds (no in-run split), the placebo buys little and is the largest piece of E-075 slice 1. Drop it from Stage 1. The query engine then reads the run's own bars and trades directly.
- The validation guard (D5): right, small, not blocking. Ship it inside the folds PR (same code area), not as its own slice.

Two shape points on the folds:
- "B and C split 2018-2021, 2 blocks per year each" does not divide: 2018-2021 is 12 four-month blocks. Write the exact blocks in `folds.yaml`, six each, one or two per year, e.g. B = 2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05 and C = the other six. Six per fold keeps the 6-window shape the rule below assumes.
- SOL (from 2021-06) and UNI (from 2020-10) have almost no bars in B/C (A1.7 fact 4), so a SOL/UNI run's claim has no next fold on the same coin. The coverage gate will leave fewer than 6 windows; the rule must say "all but one window, with at least 4 windows, else not measurable". Daily runs have 70-87 trades per block, so trade-level floors will often make a daily trade claim not measurable; that is the honest answer, not a bug.

### Q2. Is the cost-free statistical confirmation rule right and simple enough?

The operator is right that cost does not belong in the grading. A 10 bps effect at h=24 is a fact about the market whether or not a 15 bps round trip eats it; the cost comparison belongs where a strategy is assembled (Stage 3) and in the profit bars that already judge every run. v3's `relevance_floor` and `confirmed_small` should go. 

But "an effect is an effect" only answers "is cost part of it"; it does not answer "is this number an effect or noise". With sign only, a null claim passes about half the time on one fold (`test_sign` requires only `oriented > 0`; the horizons are nested, so they move together). About 12 claims per lens per fold would then put roughly 5 chance "confirmed" rows per lens into the registry as building blocks. A rule is needed, and it is about noise, not cost.

"Sign holds AND the uncertainty range excludes zero" is the right idea. The simplest form the existing output supports:
- Rule: confirmed when, at every horizon with a value, the pooled oriented effect is > 0 AND the claimed sign holds in all but at most one of the fold's windows (`windows_with_claimed_sign >= windows_with_a_value - 1`, with `windows_with_a_value >= 4`). Otherwise not confirmed. No events, or fewer than 4 windows with a value: not measurable (a look, counted).
- Why this one: both numbers are already in every measurement (`claim_measure.py:185-189`); it is the existing `consistency` slot (`claim_tests.py:717`) applied by code with a fixed k, like `alpha`; one rule serves bar tests and trade tests (the trade family must report per window too); and it reads in plain words: "held in 5 of 6 windows on fold B".
- What it buys: under a symmetric null, P(>= 5 of 6 same sign) = 7/64, about 11%; 6/6 is about 1.6%. A lineage that confirms on B and then C is near 1%. Windows in one fold share a market phase, so the true chance rate is somewhat above the coin-flip number; say so in the record and count every look in the ledger.
- Minimum code: about ten lines in `test_sign` (`explore_confirm.py:708-715`) reading the two counts; the analyst never sets `consistency` (code-fixed, as `CODE_FIXED_KEYS` does for alpha, `claim_card.py:67`).
- Alternatives considered: a t-interval over the six per-window effects (also ten lines from `per_window`, but it weighs a window with 30 events like one with 3,000 and is fragile with six points); the parked block-permutation p-value (real and calibrated, but parked by D-077, no trade tests, and the signal recomputation covers two component classes only, `claim_tests.py:232`). Neither for Stage 1.
- Fairness note: the operator did not ask for any rule; the rule is the reviewer's addition. It is justified, and it must be presented as a noise rule, not a size rule.

### Q3. Does "every claim is confirmed by its own run" hold up for market claims?

Yes, with one correction to the consequence drawn from it.
- No confound, provided the confirmation is the claim test and not the vehicle's P&L. A market claim's test reads `close`, `past_return`, `calendar`, `trailing_vol` (`claim_tests.py:146, 530`), columns that come from the data cache and do not depend on the strategy that ran. Whatever vehicle produces fold B's `bars.csv`, the measured number is the same. The confound appears only if someone reads the vehicle's grid as the claim's confirmation; the record must say "confirmation = the claim test on the child's base variant; the vehicle's grid is information".
- The over-interpretation is "a market claim must come with the strategy that exploits it". The operator said no separate post-backtest analysis; he did not say the vehicle must exploit the claim. Requiring an exploiting vehicle costs: the analyst designs a strategy per market claim (v1's tuner pull, in a new place), 1b must build a component before confirmation, and the lineage's next fold is spent on a config built to carry a claim rather than to be a strategy.
- Simplest honest alternative, consistent with "no post-backtest analysis": default `vehicle: same_strategy`, the parent config re-run on the next fold. That run is "the run built from the claim"; the claim test is measured on its bars; nothing else is scanned. The block that exploits a confirmed market claim is built after confirmation (1b from the selector) and runs as a new config on the following fold. A `variant` vehicle is for strategy claims that need a changed behaviour to be observable; even then the claim is measured on the child's base variant and the variant's grid is information only.
- One collision to accept: two claims from the same parent, both `same_strategy`, both bound for fold B, are the same config on the same fold, and the repeat gate refuses the second. For Stage 1, accept it (the second waits for fold C). If it bites, let decide-next pre-fill both claims into the one child; that is lineage-local and is not the piggyback the operator refused.
- A forecast-conditioned claim (selector on `forecast`, e.g. run_074's rank_ic) is not strategy-independent; it needs `same_strategy` by construction. The kind list should make this visible: `event_behaviour`/`calendar_effect`/`conditional_behaviour` on price fields are market claims; `direction_forecast` is a forecast claim; `execution_behaviour` is a strategy claim.

### Q4. What is missing or over-built, given the preference for simplicity?

Missing (small): the claim kind and envelope fields; the fold confirmation function; the analyst proposal in the reader shape; the exact fold blocks; the no-claim trail in the skill (P8: `what_was_examined` and `best_rejected`, zero code, stops a lazy "no claim"); the hindsight rule stated on use, not observation (P10, zero code; as written, A1.8 item 6 forbids every strategy observation since exit fields are `after`).
Over-built: the placebo arm; a separate grid tool; the per-fold repeat gate as code; the validation guard as its own slice; the novelty line (P6, the memory view suffices); any analyst self-score ranking change in Stage 1 (about 12 proposals per lens; rank by the order they arrive and move P9 to Stage 2 as planned).
Right-sized: trade-level tests in Stage 1 (without them the trade lens writes `tests: none` by construction, `claim_card.py:184-194`); the memory view with numbers for confirmed claims only; `combines_as` as a field only.

## 2. How A1.9 "How these remarks are applied" matches what the operator said

- Cost (remark 1): matches. A1.9 dropped the floor as asked. The statistical rule is an addition the operator did not request; it is needed (section Q2) and must be labelled a noise rule.
- Combination (remark 2): matches exactly. Keep `combines_as` analyst-written from a closed list (`forecast_block | regime_gate | execution_rule | knowledge_only`), code validates the word only; do not derive it from `kind` by code, that is a step toward touching the logic he parked.
- Piggyback (remark 3): "every claim is confirmed by its own run" is faithful. "The vehicle must exploit the market claim" goes beyond what he said (section Q3). The sentence "the market claims will be integrated into the agent" can also be read as "market observations are internal reasoning and the output claim is about the strategy"; under that reading there would be no market-claim records at all. His thesis (Step 9: confirmed claims carry information on the market and on the strategy) supports keeping market claims as records, so A1.9's reading is defensible, but it is a reading and should be put to him in one line.
- Order (remark 4): matches.
- Under-interpreted: "most points sound valid, so the work is done iteratively". A1.10 keeps some review points silently (ranking to Stage 2, memory view) and drops others without saying (P2 one-claim-or-no-claim, P8 no-claim trail, P10 hindsight on use, P12 mechanism type). All four are skill text with no code; the plan should list which are in.
- Under-interpreted: his dislike of case-by-case patching applies to E-075's own design too. The placebo outcome layer, the 12 operator decisions in `PHASE_A.md:530-570`, and the two-arm trade-outcome recomputation are heavy; A1.10 item 8 cites D4 but leaves E-075's slices unchanged.

## 3. The confirmation rule without cost (summary)

- Yes to no cost. Yes to a rule. The rule: pooled sign at every horizon AND the claimed sign in all but one window of the fold (at least 4 windows with a value); else not confirmed; no events or fewer than 4 windows: not measurable. Fixed by code, ten lines in `test_sign`, same rule for bar and trade tests. About 11% chance rate per fold under a symmetric null, near 1% after two folds, every look counted.

## 4. Stage 1 as listed: order, done-when

PR-1 Folds + validation guard.
- `config/folds.yaml` with the six exact blocks per fold; decide-next writes the child's windows from the next fold its lineage (`source_run` chain) has not used, replacing the deep copy at `decide_next.py:2129-2131`; fold label into the brief, `run_context`, memory and the trial row; refusal of any window in 2024-2025 or the holdout.
- Done when: a child of a fold-A run gets fold B's windows and its brief, run_context and trial row say `fold: B`; a test shows the novelty key differs across folds and matches within one; a 2024 window raises; flag off is byte-identical.

PR-2 Claim record + confirmation on the child.
- `execution_behaviour` in `CLAIM_KINDS`; envelope fields `vehicle {kind: same_strategy|variant, config_change}`, `combines_as`, `fold_observed`; `confirm_on_fold` (measure the child's card tests on its base variant, all windows; the rule of section 3; `not_comparable` on a spec change; ledger row with fold and basis `child_run`); statuses `confirmed | not_confirmed | not_measurable`.
- Done when: on a fixture child, a planted effect is confirmed, a null is not, a changed spec is not comparable, no events is not measurable; each writes one ledger row; the old `finding_route` IN_RUN path is unreachable under the fold flag.

PR-3 Trade-level test family.
- Loader (`trades.json` + `bars.csv` per window), the E-074 4.2 classifier, selector `trade {where: [...]}` over a closed field list, outcomes `trade_net_return` (A7-corrected) and `post_exit_return {horizons}`, baseline `other_trades`, statistics `mean_diff | hit_rate`, per-window values, `spec_hash` unchanged for old specs, CLAIM_TESTS.md entry.
- Done when: hand numbers on a synthetic lot set; the classifier passes flip / reduction / to_zero / same_sign_flat / last-bar / last-day-but-not-last-bar; `check_claim` accepts the new selector; a lookahead test (changing rows after the exit leaves entry fields unchanged; changing rows after t+h leaves the outcome unchanged).

PR-4 Analyst query engine + memory view.
- E-075 slice 1 minus the placebo: six functions over the run's own bars and trades, closed vocabularies, caps, log-before-return, `conditional_effect` equal to `effect_sizes`; the trade functions read PR-3's loader. The memory view: statement, kind, fold, status per earlier claim; numbers for confirmed claims only.
- Done when: equality test against `effect_sizes` for every selector/outcome/baseline/statistic; no `local_data` path opened; every refused call logged; the memory view on run_074's memory shows no exploratory effect and no k/6.

PR-5 Wiring + skill.
- E-075 slice 2 (`_stage_agent_options(analyst=...)`, deny hook, `_invoke_analyst_llm`), the skill with the two lens texts, the proposal validator (`check_claim`, citations against the log, falsifier, vehicle resolves with `resolve_patch`, seal-date scan, the claim's test and the predicted query present in the log), the proposal written in the reader-proposal shape. Flag `orchestrator.analyst.enabled`, off.
- Done when: a stubbed session writes a proposal decide-next picks and turns into a fold-B child brief; flag-off byte-identity; the CUL-336 assertions; one live smoke session.

Pilot (operator-run, after PR-5): both lenses on saved runs 065-074 (fold A), every proposal through decide-next onto fold B, graded by PR-2; the process checks of the review's section 5 item 9 minus the relevance floor; hold rates per fold as information; the operator decides.

## 5. A clean final A1.10 I would sign off

Stage 1: the smallest loop that can confirm a market claim and a strategy claim.
1. Folds. `config/folds.yaml` with six exact blocks per fold (A = 2022-2023; B and C from 2018-2021, each with a block in every year); a child runs on the next fold its lineage has not used; the fold is on every run, claim and ledger row; no window in 2024-2025 or the holdout. The per-fold repeat gate is the existing novelty key, proven by a test.
2. The claim record. One new kind, `execution_behaviour`. On the proposal, not inside the claim: `vehicle` (`same_strategy` by default; `variant` with a config change only when the behaviour needs it), `combines_as` (closed list, analyst-written, code checks the word), `fold_observed`.
3. Confirmation by code, on the child run only. The claim's tests measured on the child's base variant over the fold. Confirmed when the pooled sign holds at every horizon and the claimed sign holds in all but one window (at least 4 windows); not confirmed otherwise; not measurable when there are no events or too few windows. No cost anywhere. A changed spec is not comparable. Every measurement is a ledger row with its fold. Refuted and not-measurable claims are kept as knowledge.
4. Trade-level tests. One family: trade selector over a closed field list, outcomes trade net return and post-exit return, baseline the other trades, per-window values, a lookahead test. Exit causes from E-074's interim classifier now, E-029 later.
5. The analyst's tools. E-075's six query functions on the run's own bars and trades, no placebo arm, no separate grid tool; `trailing_vol` is a field they read.
6. The skill, both lenses. Objective: observe, dig in, end with one claim or no claim. Claim: statement, kind, evidence (query ids), why (market or mechanical, with the second query it predicted), the vehicle, the test in the slots, the falsifier, `combines_as`. No claim: what was examined and the best rejected candidate. The observation may read any column; a use-if-confirmed and a config change act only on fields known at the close or fill. No profit or cost judgement by the analyst.
7. Memory view. Statement, kind, fold, status per earlier claim; numbers only for confirmed claims.
8. Pilot. Both lenses on the saved runs, proposals onto fold B through decide-next, graded by item 3; process checks and the operator's judgement (D4).

Order: 1, 2, 3 (one PR each), then 4, then 5+6 together, then 7 can ride with 4, then the pilot.

Stage 2: E-029 replacing the classifier; E-027; code-computed ranking of analyst candidates; CUL-416/417.
Stage 3: combination of confirmed claims using `combines_as`, logic redesigned then; validation once; then the holdout.

Open to the operator, one line each:
- Market claims as records with `same_strategy` vehicles, or market observations internal only with strategy claims as the sole output?
- The noise rule "all but one window" (about 11% chance per fold) versus "every window" (about 2%, fewer true effects pass)?
- Drop the placebo arm from the pilot?
