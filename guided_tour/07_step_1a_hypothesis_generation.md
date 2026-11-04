# Stop 07: Step 1a, hypothesis_generation

## Speech (verbatim)

**Stop 07 of 29: Step 1a, hypothesis generation.** Open on the side: `workflow_artifacts/skills/hypothesis-design/` (7 files), `workflow_artifacts/templates/handoffs/research_brief_to_hypothesis.yaml`, `run_phase1_research.py`, run_102's `hypothesis_card.yaml`.

**In one sentence.**
Step 1a is where an AI turns the brief's idea into a hypothesis card (a one-page statement of the idea): what is believed, what it predicts, how it will be judged, and how the belief itself will be tested.

**Why it exists.**
A brief says an idea in words. The rest of the pipeline needs it as quantities, a prediction with a time horizon, one pass/fail criterion, and a claim that can be measured.
Writing these before any test means the judge is chosen before the result is known, so the result cannot pick its own judge.
The step also keeps the operator's words: the card opens with them word for word, so later steps cannot drift from the idea.

**What comes in, what goes out.**
- In: the brief as a data file; the indicator library; the criterion menu (the fixed list of approved pass/fail measures); the list of ideas already tried; the claim-test instructions; and, depending on the brief, an extra instruction sheet for a decide-next brief, a pre-filled claim, or several ideas from one brief.
- Out: the hypothesis card, plus check records: the claim check, its power (can the test reach its minimum sample), its status, and for a pre-filled claim whether it was kept.
- Next: step 1b (stop 10) builds a strategy config from the card. The criteria go into the pre-registration (the rules fixed before results) when the brief left them to 1a.

**What happens here, step by step.**
1. The loop gives the AI (Sonnet 5.5) its role sheet, the "hypothesis design" skill, and its inputs, closed book (no tools, the prompt only).
2. The skill asks for four steps. Step 0, the mode: a brief already fully authored is copied through; a decide-next brief, a pre-filled claim, several cards, an exhausted brief and the claim instructions each change what is written.
3. Step 1, the idea: the brief's words first, then every quantity the idea names with its formula, the parts a forecast cannot express (only exits, position state, order placement), why the edge should exist, and the library entry it builds on.
4. Step 2, the statement: what it predicts, of which kind (a return's direction or a market state), over how many bars, when it applies, and what a pass or a fail would mean. Then one criterion picked from the menu by what the statement predicts, at its horizon. Never a profit measure: profit is judged by the campaign's own bars.
5. Step 3, the proof: the claim, a measurable test of the belief, written with the claim-test instructions (stop 09).
6. After the answer, code checks: a card from an "open" brief must not repeat an idea that brief already produced; several cards are split, the extra ones queued; a brief declared exhausted ends the run.
7. A pre-filled claim is written into the card by code, unchanged, and any difference in the AI's own version is recorded as a warning.
8. Every card's claim is checked, and its minimum sample compared with what the data can give. A refusal gets one retry of step 1a with the reason. Whatever remains is recorded and the run goes on: a claim never stops a run.
9. For a decide-next brief, code checks the card keeps the candidate's id. When 1a was to choose the criteria, code turns the card's pick into the pre-registration's pass rule, checks it against the menu, and adds the overlap criterion where it applies. When the brief brought its criteria, the card's pick does not replace them.

Example: run_102's card keeps the operator's words, predicts the direction of BTC's 24-hour return, picks `forecast_ic_median` at horizon 24 (the forecast's rank correlation with the next 24 hours' return), and carries the pre-filled claim unchanged (`claim_prefill.yaml`: `status: unchanged`).

**What it costs and how long it takes.**
run_102: one call, 0.41 USD, 65 seconds, one turn (`runs/run_102/pipeline_state.yaml`, audit_log `hypothesis_generation_attempt_0`).

**What is switched off or not used here.**
- Queueing the extra cards as soon as 1a ends is off; they are queued after the run.
- run_102's brief carried its own criteria, so the card's pick was not written into the pre-registration.
- The ideas-already-produced note was written for run_102 but not given to 1a (a decide-next brief).
- The execution-claim instruction file (`CLAIM_TESTS_EXECUTION.md`) is not given to step 1a.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Skill | `skills/hypothesis-design/SKILL.md:1-84` | Steps 0-3 (`:13-62`), regime idea (`:64-71`), card fields (`:73-84`) |
| Several cards, exhausted brief | `skills/hypothesis-design/BRIEF_HYPOTHESES.md` (83 lines) | Given when the brief context file exists |
| Claim instructions | `skills/hypothesis-design/CLAIM_TESTS.md` (237 lines) | The claim block and its four slots |
| Trade-level tests | `skills/hypothesis-design/CLAIM_TESTS_TRADE.md` (135 lines) | Added when the analyst switch is on |
| Execution claims | `skills/hypothesis-design/CLAIM_TESTS_EXECUTION.md` (16 lines) | Read by `tools/analyst_session.py:429`; not added at 1a |
| Pre-filled claim | `skills/hypothesis-design/PREFILLED_CLAIM.md` (20 lines) | Copy `candidate.claim` unchanged |
| Decide-next candidates | `skills/hypothesis-design/DECIDE_NEXT_CANDIDATES.md` (51 lines) | Given to a decide-next brief |
| Handoff template | `templates/handoffs/research_brief_to_hypothesis.yaml` | Brief and indicator library required; run context optional |
| Model | `config/campaign_config.yaml:879` | Sonnet 5.5 |
| Criterion menu input | `run_phase1_research.py:9036-9075` | Added at 1a under config-direct |
| Tried ideas input | `run_phase1_research.py:3775-3813`; `tools/campaign_memory.py:931` | `tried_ideas.yaml` from campaign memory |
| Decide-next addendum | `run_phase1_research.py:8455-8475`, `:8143` | `DECIDE_NEXT_CANDIDATES.md` |
| Brief addendum | `run_phase1_research.py:8615-8635` | `BRIEF_HYPOTHESES.md` and the context file |
| Claim addenda | `run_phase1_research.py:17409-17466` | `CLAIM_TESTS.md`, `CLAIM_TESTS_TRADE.md`, `PREFILLED_CLAIM.md`, retry message |
| Dispatch | `run_phase1_research.py:20088-20131` | Set aside earlier outputs (`:17637`), call, split, exhausted, repeat, claim check, pass rule |
| Card checks | `run_phase1_research.py:8749`, `:8765` | One card; repeat of the brief's ideas |
| Claim check after 1a | `run_phase1_research.py:17737-17800`, `:17815` | One retry; never stops the run |
| Pre-filled claim kept | `run_phase1_research.py:17321` | Written into the card by code |
| Claim status | `run_phase1_research.py:17690-17714` | `claim_test_status.yaml` |
| Pass rule from the card | `run_phase1_research.py:8386-8452` | Id check; brief criteria kept (`:8411-8416`); else built, linted, written |
| Overlap criterion | `run_phase1_research.py:5913` | Residual IC added by code |
| Card schema | `workflow_artifacts/schemas/hypothesis_card.schema.json` | Checked when the card is read back |
| Example files | `runs/run_102/artifacts/hypothesis_card.yaml`, `claim_prefill.yaml`, `claim_check.yaml`, `claim_power.yaml`, `claim_test_status.yaml`, `tried_ideas.yaml`, `brief_hypotheses_context.yaml` | run_102's 1a outputs and inputs |

Remarks: send them as "stop 07: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop7
Wondering why step1a get the indicator library. 
The "depending on the brief, one extra" concerns me as we are deviating from standardization. 
Wondering why 1a is still triggered when the brief is "fully authored". Maybe because the brief does not respect a good data structure ? Otherwise it could be checked and skipped mechanically. 

Same concern here on the "Each of these also changes what is written" 
Challenging here "the parts a forecast cannot express" here a forecast could normally express most when we know how to interpret it. 

Step 6 - curious about what we mean by i
"Idea does not repeat", it should be the exact same claim for me, any deviation could be accepted. 

We should be careful about the skills and instructions of this step. Here should live an amazingly clever agent allowing to extract sub-ideas from a brief, but also innovate and take various point of view respecting a brief. 
I would be curious how much this step generate ideas from a brief, but it should be numerous. 
The problem might sit into idea_quantities (a brief does not need to list "quantities", and a step before that would understand the brief and all what it implies from a trading expert point of view. Then generate quantity ideas (or not) 
Edge source might be blocking. Why would an idea brainstormed say "why an edge should exist". The logical aspect of the idea however is something important - maybe just a rewording. Here step 1 should push the strategy ideation from a general concept 
I would challenge also the horizon bars forced in a field. 
Never a profit measure is wrong. An idea could be proven by a profit for exemple. 

Overall i find this step overcomplexified by rules and different mode, while the concept should be around ideation. 

To help rewritting this skills, we could brainstorm around exemple of brief, and "pushed" expected claims and see how we could make this step arrive to this claim.

Step7 
Additionally, to enhance 1a we could iterate in a separated way with fake inputs, and test various version of the skils to observe variations until we reach something acceptable as output. Skills tested standalone on fake input data. You see what i mean ?

## Inspector notes

### (1) Design and mechanism

1. On the live loop, almost nothing 1a authors is read by code. For a decide-next candidate (every run since run_100's two operator runs; run_102 is one), the id is fixed and checked (`RP:8404-8410`), the claim is the brief's and is written back into the card by code whatever the model wrote (`_keep_prefilled_claim :17321-17351`; run_102 `claim_prefill.yaml:2` `unchanged`), the criteria are the brief's and the card's pick is not written (`:8411-8416`), and the start config is the source run's (stop 10). What remains of the 0.41 USD Sonnet call is `thesis`, `idea_quantities`, `not_expressible`, `edge_source`, `library_lookup`, `statement`, `criteria_rationale`: the schema says of the four D-186 fields "information only, nothing in code reads it to decide" (`hypothesis_card.schema.json:252`, `:257`, `:262`, `:279`), and grep over `.py` finds readers of `statement.predicts_kind` only in the D-192 warning (`RP:8290-8332`) and of `idea_quantities`/`statement` in the analyst's prompt builder and `explore_confirm` (`analyst_session.py:149`, `explore_confirm.py:127,151`). So on this path 1a is a prose step whose output is prompt material for 1b and the analyst; the "judge chosen before the result" (speech, "Why it exists") is done by decide-next and the brief, not here. Not a defect of correctness; a question of whether the step earns its call on the common path. On an operator brief (run_100, run_101) the step does decide: the id, the criterion, the claim, and possibly several cards.
2. The criterion choice is nearly forced. The skill says pick "from the menu's live entries" by what the statement predicts (`SKILL.md:43-50`); the addendum names the live entries as two, `sign_consistent_by_era` and `forecast_ic_median` (`DECIDE_NEXT_CANDIDATES.md:28-31`), the third being retired for blocks (`criterion_menu.yaml:40`); the code-added ones are `residual_ic` (`RP:5913`) and `profit_bars` (compositions). A `return_direction` statement therefore always takes `forecast_ic_median` at the nearest allowed horizon (1, 6, 24, 72, 168; `criterion_menu.yaml:188`), which D-192 then checks for (`RP:8316-8331`); a `market_state` statement finds no measure and the run parks (`SKILL.md:44`, `:67`; `RP:8306-8309` always returns `_NO_LABEL_MEASURE`). For the goal: branch 1 can judge exactly one kind of idea today (a graded forecast of a forward return), and every regime idea stalls at 1a by design. Whether the menu has grown is stop 08's check; the skill and addendum text are the fact here.
3. The claim check is information only by construction (`CLAIM_TESTS.md:14-18`, `RP:17739-17751`): a refused claim, an unreachable floor, or `tests: none` records a status and the run spends its backtests anyway. The one retry is bounded and undone if it leaves the card worse (`:17765-17789`). Sound as a record; weak as a gate: a run whose claim "teaches the campaign nothing" (`CLAIM_TESTS.md:17-18`) costs the same as one whose claim is testable. For a continuous loop the cost of an untestable claim is not an idea refused but a backtest paid for a finding nobody can read back.
4. What 1a knows of the campaign is a list of ids and statuses. `tried_ideas.yaml` (run_102: 28 rows, `:16`) gives `run_id`, `hypothesis_id`, `symbols`, `timeframe`, `idea_status`, `variants_tested`, sometimes `approximation` and the base book (`campaign_memory.py:931-990`); no finding text, no claim result, no reason for a refutation. The knowledge base's findings (stop 22) reach 1a only through the template's optional `campaign_knowledge_base.yaml` input, repointed by the `stale_input_path_fix` flag (`RP:3855-3860`) and whole-file pasted; whether that file is small enough to be useful is stop 22's question. So the idea source sees "what was tried" but not "what was learned": 25 of 28 rows say `refuted` with no why. For autonomy this is the gap between an exclusion list and a memory.
5. Several cards from one brief are scored by their author: `confidence_real` 0-3 on a rubric the model applies to its own cards (`BRIEF_HYPOTHESES.md:30-62`), and that score ranks waiting cards against analyst proposals at decide-next (`:46-49`). The stamp of the answering model (`_stamp_card_scores_text`, stop 05a) records who scored, not whether the score is honest. Self-grading is explicitly "never decides whether an idea is true"; it still decides what runs next among the cheap candidates. Hold for stop 24.
6. Lineage is encoded in the id by concatenation (`..._trade_efficiency-run_070-1__profitability-run_073-1`, `tried_ideas.yaml:61`) and the memory view says "No family grouping: an idea's identity is its hypothesis_id" (`:12-13`). So a third-generation child looks to 1a like a new idea with a long name; the view carries nothing that says "these five rows are one lineage, refuted five times". Combined with stop 06 note 1.1 (the fold draw forgets the lineage too), the loop has no object that is "an idea across its runs".
7. The schema is not enforced where it would matter. run_102's card writes `library_lookup.regime_affinity_for_target` as a sentence (`hypothesis_card.yaml:81-82`) where the schema allows `favorable|unfavorable|neutral|null` (`schema:116-119`) and the skill says the same (`SKILL.md:76`); the read-back check warned to stderr (stop 05a note 1.5) and the run went on. The recent commit `f230d0d8` re-pins the skill on that line, so the text was fixed after the fact; the mechanism that let it through is unchanged.
8. The pre-filled claim is copied with its defects. The card's `claim.rationale` carries unfilled placeholders ("held <n> bars", "rank IC <n> at 1 bar", `hypothesis_card.yaml:148-150`), copied from the brief (`claim_prefill.yaml:44-46`) by code "unchanged, the whole claim" (`RP:17329`). The rationale is text for people and the analyst; the placeholders came from the analyst's proposal (stop 21) through decide-next (stop 24). A copy-by-code rule faithfully propagates whatever the upstream writer left.
9. What is sound: the id check before 1b (`:8406-8410`), the pass rule written from the card and linted before spend (`:8417-8442`), the retry's set-aside/restore discipline (`:17637-17687`), the `brief_repeat` and ambiguous-output refusals (`:8749-8786`), and the power check against the real protocol's bar count (`:17576-17633`; run_102 `claim_power.yaml:8` 17520 bars). The step cannot pick its own judge after the result: the judge is written here or earlier, and the grid reads that.

### (2) Legacy or simplifiable (leads)

1. `hypothesis_card.schema.json`: `edge_source`, `signal_concept`, `assumptions`, `expected_failure_modes` (`:33-109`), `power_parameters` (`:139-177`, "A8.6 ... before prescreen", a deleted stage), `cost_feasibility` (`:187-207`, "relocated from quant-validation", unreached) are the pre-D-186 card; the skill's card (`SKILL.md:69-84`) names `edge_source` and `library_lookup` but none of the other four. Not checked: whether any live reader uses `power_parameters` or `cost_feasibility`.
2. `_check_specialist_readers_preflight` (`RP:4511-4528`) and `sr_flag` (`:8386`, `:8414`, `:8450`): a deleted stage's name on the live grid pre-flight. Rename.
3. `_handle_hypothesis_generation_multi_card_split` (`RP:11616+`): the flag-off "scaffold a sibling run" split with `campaign_state.hypothesis_splits`; under `decide_next` the queue path (`_queue_extra_hypothesis_cards :8637`) is taken. Which branch run_loop's call at `:20101` reaches under the live flags was not traced; the docstring at `:8577-8581` says the flag-on split scaffolds nothing.
4. `CLAIM_TESTS_EXECUTION.md` (16 lines): "shown to no prompt yet" (`:3`); its one reader is `analyst_session.py:429` per the speech. Either wire it or delete it.
5. The 1a template's `optional_inputs` `run_context.yaml` reason ("Present on instrument escalation runs ... `run_context.target_symbol`", `research_brief_to_hypothesis.yaml:12-13`): the file now carries `run_type`, `protocol`, `fold` (stop 05b) and no `target_symbol`; the reason text is from the retired escalation route. The stale KB/wishlist paths (`RP:3816-3860`) are patched by a flag rather than fixed in the template.
6. `_EXCLUSION_DIGEST_*` (`RP:3311-3314`, `:3806-3807`): the digest branch is taken only when `campaign_memory.yaml` is absent; with 28 runs in memory it is dead on this campaign (stop 03a note 2.3).
7. `criteria_fit` (`SKILL.md:82`, schema `:183-186`) and `not_expressible` kinds: the park on a missing measure (`SKILL.md:44`, `:67`) is routed where? Not located at this stop (stop 10's component-gap park is the candidate).
8. `extra_cards_at_1a` off: the `after_1a` hook (stop 05b note 2.5); the extra cards wait for the DONE branch.

### (3) Disagreements between the speech and the element

1. Step 7, "A pre-filled claim is written into the card by code, unchanged, and any difference in the AI's own version is recorded as a warning": correct (`:17321-17351`, `:17354-17395`); the speech does not say the copy also carries the brief's unfilled placeholders (note 1.8). Omission.
2. Step 9, "When the brief brought its criteria, the card's pick does not replace them": correct (`:8411-8416`); run_102's `criteria_rationale` says as much ("the criterion the fold child's brief fixes", `hypothesis_card.yaml:105-107`). The D-192 consistency file is then not written (`:8445-8449` is after the early return); run_102 has no `criterion_consistency.yaml` (artifacts listing). Consistent, not stated.
3. Step 2, "a brief already fully authored is copied through": `SKILL.md:18` (pass-through) and `DECIDE_NEXT_CANDIDATES.md:9-15` (the exception). Correct.
4. Section 6, "The ideas-already-produced note was written for run_102 but not given to 1a": confirmed (`RP:8623`; `brief_hypotheses_context.yaml:5-6`); the cause is stop 04 note 1.6.
5. Reading map "Dispatch `run_phase1_research.py:20088-20131`": correct (stop 05b read). "Claim check after 1a `:17737-17800`, `:17815`": the function ends `:17796`; `:17799-17812` is the error net; `:17815` the retry. Fine.
6. Reading map "Pass rule from the card `:8386-8452`": correct. "Overlap criterion `:5913`": `_ensure_residual_ic_in_pre_registration`, the brief-run path; for a candidate the append is at `:8428-8429`. Both exist; the map names one.
7. "Example: run_102's card ... predicts the direction of BTC's 24-hour return, picks `forecast_ic_median` at horizon 24": `hypothesis_card.yaml:87-104`; correct. "carries the pre-filled claim unchanged": `claim_prefill.yaml:2-3`; correct.
8. Figures: 0.41 USD, 65 s, one turn (`pipeline_state.yaml:41-53`): correct. Skill file lengths: SKILL.md 85 lines (the file ends at `:85`; the speech says 84), BRIEF_HYPOTHESES.md 84 (speech 83), CLAIM_TESTS.md 238 (speech 237), CLAIM_TESTS_TRADE.md 136 (135), CLAIM_TESTS_EXECUTION.md 17 (16), PREFILLED_CLAIM.md 21 (20), DECIDE_NEXT_CANDIDATES.md 52 (51): each one short by one, a trailing-line counting difference, not an error.
9. Verified as stated: `RP:9036-9075`, `:3775-3813`, `:8455-8475`, `:8143`, `:8615-8635`, `:17409-17466`, `:17637`, `:8749`, `:8765`, `:17737-17796`, `:17815`, `:17321`, `:17690-17714`, `:8386-8452`, `:5913`; `campaign_memory.py:931`; `campaign_config.yaml:879`; the template; the seven run_102 example files.
