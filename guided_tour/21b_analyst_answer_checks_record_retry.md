# Stop 21, part b: the analyst, what happens to its answer

## Speech (verbatim)

**Stop 21 of 29, part b: the analyst, what happens to its answer.** Open on the side: `strategy-research/tools/analyst_session.py`, `tools/reader_proposals.py`, `tools/reader_findings.py`, `workflow/run_phase1_research.py`, `workflow/run_campaign.py`, `docs/RUNBOOK.md` (the retry-analyst section).

**In one sentence.**
Code checks each lens's answer against the session's own log of measurements, records the session, writes an accepted idea as a proposal for the next-run decision, and lets the operator rerun the analyst on a finished run whose reading they rejected.

**Why it exists.**
An AI can cite a number it never measured, claim an effect its own test contradicted, or propose a change the engine cannot build. Each would send a next run (a full backtest on unseen months) after nothing.
So its words count only where code can trace them to a logged measurement; what it left out, code adds. A rejected reading can be redone without a new backtest.

**What comes in, what goes out.**
- In: the lens's answer (one block: a claim, or no claim); the query log; the run's base config, variants and fold (a fixed set of test months).
- Out: the reading (the proposal file of the lens's category); the session record; one cost line per attempt in the run's audit log.
- Next: record-keeping copies them into campaign memory (stop 22); decide-next ranks proposals and writes the next brief (stop 24).

run_102's readings, records and query logs are not in this checkout. From stops 00, 01 and 02: run_102 was read twice. The first reading's candidate `trade_efficiency-run_102-1` (lens, run, number) was superseded by hand. The second gave `forecast_power-run_102-2`, the waiting brief: two weight changes, on fold B, citing query q9. Two of its ten observations are code-written: "Not reported by the model: query q11 ..." and "... q5 ...".

**What happens here, step by step.**
1. The answer must be exactly one block; two or more are refused.
2. Every citation (query id, place in its result, value) must match the log; a decimal may be rounded to three significant digits.
3. A claim must pass the claim-test check (allowed slots, at most three tests, a reachable sample). Each test must have run in the session with the same floor (minimum events and windows). Refused: a test that ever measured the opposite of its direction; the forecast's rank correlation over all bars, which the protocol already tests.
4. The "why" query must be a second, different measurement the mechanism predicted.
5. A change to position sizing is kept as an observation (a measured behaviour with no change attached), never a claim.
6. A no-claim needs a reason, the best rejected idea and the query that killed it. Both forms need the four-line next-steps ledger.
7. A number in the prose the session never saw is masked and listed, not refused. A date inside the sealed holdout is refused.
8. Results that cleared their floor but went unreported are added by code, tagged "not reported by the model".
9. Then the proposal's shape and content: the change must resolve against the base config (component, field, current value), avoid scaffolding, pass whole if it is a whole config, and name this run's fold.
10. A score from 0 to 3: the lowest share of windows agreeing with the claim, over every run of its test. Decide-next ranks on it.
11. Refused: one retry in a new session, given the reasons, the refused answer and the query log so far. Refused again: code writes a "skipped" reading. Accepted: warnings are noted (a test already measured, or this run's own), never blocking; the reading and record are written.
12. The operator's retry: set the rejected candidate to superseded, run the retry command. It refuses unless the run is completed, its queue line done, not a fold re-run, no review pending, switches on, budget left. It archives the analyst's files and the decision, clears the live ones, and sets the run back at the analyst. The next launch redoes analyst, record-keeping, route and decide-next; new proposals are numbered after the archived ones.

**What it costs and how long it takes.**
run_102: 7 analyst calls, 6.50 USD, two readings (its audit log, as quoted at stop 05a).
The retry runs no backtest: the two lenses only, on the same run budget.

**What is switched off or not used here.**
- In this checkout (master) the analyst switch reads off; the tour's flag set (stop 03a) has it on.
- The analyst's audit lines are still named after the deleted "specialist readers" stage.
- The in-run merge of findings has no caller (its own note says so; my grep found none).
- The post-write review files a test request for a finding with no test; the answer check refuses such a claim first.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Worker loop | `workflow/run_phase1_research.py:4885-5018` | Two attempts; budget before retry `:4926`; audit line `:4935-4944`; tool-list stop `:4945-4952` |
| Answer check call | `run_phase1_research.py:4955-4964` | Claim card, fold, settings, variants, numbering after archive |
| Reading checks | `run_phase1_research.py:4966-4986` | `check_reading` (envelope, analyst tags), content errors |
| Record and write | `run_phase1_research.py:4987-5010` | Attempts, flip count, review, atomic write (`:4867`) |
| Retry, skip | `run_phase1_research.py:5012-5018`; `:5243` | Retry prompt; `output_refused_after_retry` |
| Content checks | `run_phase1_research.py:5062-5150`, `:5153-5169` | Vehicle vs base config, config form, scaffolding, fold observed |
| Review after accept | `run_phase1_research.py:5176-5213` | Warnings; test request row |
| Merge (no caller) | `run_phase1_research.py:5260` | `_record_side_finding_merges` |
| Budget, strictness | `run_phase1_research.py:5027-5047` | Token budget; analyst rubric |
| Answer check | `tools/analyst_session.py:1553-1850` | `check_answer`: one block, no claim `:1598-1664`, claim `:1665-1850` |
| Citations, dates | `tools/analyst_session.py:526-558` | `check_citations`, `sealed_dates` |
| Test identity, opposite | `tools/analyst_session.py:575-621` | Floor set aside; opposite direction |
| Score | `tools/analyst_session.py:624-648` | `in_run_score` 0..3 |
| Unreported, ledger | `tools/analyst_session.py:836-919` | `unreported_results :855`, `completeness_errors :881`, `next_steps_errors :895` |
| Angle | `tools/analyst_session.py:922-1036` | `angle_of :1029`: sizing, regime |
| Observations | `tools/analyst_session.py:1063-1141`, `:1472-1534` | `observation_errors`, ids `O-<run>-<lens>-<n>`, unreported rows |
| Masked numbers | `tools/analyst_session.py:1288-1412` | `config_settings`, `number_hits`, `mask_hits` |
| Numbering after retry | `tools/analyst_session.py:1537-1550` | `archived_proposal_count` |
| Retry text | `tools/analyst_session.py:1853-1886` | Reasons, refused answer, log (40,000 characters) |
| Reading shape | `tools/reader_proposals.py:82-148`, `:337-445` | v3 reading, analyst rubric, skip rules, envelope, `check_reading` |
| Loading | `tools/reader_proposals.py:554`, `:607` | `flatten_reading`, `load_proposals` (decide-next, campaign memory) |
| Findings helpers | `tools/reader_findings.py:40`, `:79`, `:108`, `:147` | Skipped reading, exit-field refusals (D-095), review, test request row |
| Retry command | `workflow/run_campaign.py:2628-2651`, `:2654-2696`, `:2699-2766`, `:5971-5991` | Help, archive items, refusals, archive and reset, CLI |
| Runbook | `docs/RUNBOOK.md:965-1012` | Operator steps for `retry-analyst` (D-202, a row of the decision log) |

Remarks: send them as "stop 21b: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; the readings, records, query logs and `retry_1/` are not checkable. The committed switchboard has `analyst` off.)

### (1) Design and mechanism

1. The answer check is the strongest anti-confabulation layer in the pipeline and it is placed right: every citation must name an `ok` query of this session, a path in its logged result and the logged value (`analyst_session.py:526-553`); each claim test must have run with `conditional_effect` under the claim's own floor, or the error names which queries ran it under another (`:1705-1725`); a test whose own run measured the opposite sign at any horizon is refused (`:1726-1738`, `opposite_horizons :600-620`, written after a smoke found the model keeping `direction: greater` against its own data); the "why" query must be a different measurement (`:1739-1764`); the evidence must cite the test's own horizons (`:1765-1768`); the forecast's all-bars rank IC is refused as already tested (`:1693-1704`); any date at or after the holdout month is refused (`:556-558`, `:1591-1594`); the vehicle must resolve against the base config and stay off scaffolding (`RP:5062-5150`). An answer from a session whose tool list was wrong is never used (`:4945-4952`). The model's words count only where code can trace them to a logged number, which is what the speech promises.
2. What the checks cannot see, they say they cannot see: "nothing ties the statement to that test, so its numbers are accepted whatever the text says" (`:1611-1614`); the mechanism prose is unread; `killed_by` and `why_query` are the model's choice among its own queries. The retry asks for the same outcome and records a flip (`:1866-1869`, `RP:5000-5001`). Honest about its limit: the test is traceable, the story is not.
3. The score decide-next ranks on is in-sample by construction: `in_run_score` is the lowest share of windows with the claimed sign over every run of the test, in the run that inspired the claim, mapped to 0..3 at 1.0 / 0.8 / 0.6 (`:624-648`); the other two scores are fixed at 1 (`:14-15`). The memory view refuses to show the analyst exactly these exploratory numbers (`analyst_memory_view.py:19-23`), and the next run is chosen by them (stop 24). Two rules for one number: hidden from the model, decisive for the loop.
4. Completeness is enforced by disclosure, not refusal (D-184/D-204): a floor-clearing `conditional_effect` the model left out is written into the record and the observations as "Not reported by the model" (`:836-879`, `:1514-1535`), and the child brief's `source_observations` is this list (stop 01 note 1.9: two such rows, two duplicates). The duplicate pair stop 01 found (same `spec_hash` twice) is allowed by `observation_errors` only across different queries; `_unreported_ids` folds same-key calls (`:845-852`), so the duplicate came through the model's own observations. Worth a check at stop 24, which copies them.
5. D-096 masking (`number_hits`/`mask_hits :1294-1412`) replaces every unverified prose number with `<n>` in what is stored and passed on; stop 07 note 1.8's "unfilled placeholders" in run_102's claim rationale are this. The rule is right (a model number nobody can trace is not kept); its output is a claim rationale with holes that 1a copies "unchanged" into the card and the analyst of the child reads back. Nothing marks the holes as masked in the brief or the card.
6. `retry-analyst` (D-202) is sound and narrow: under the lock, eight refusals (`RC:2654-2696`: ownership, `done`, last run, `completed`, no refold, no review state, both flags on, within budget) plus a dry queue save (`:2719-2724`), an archive numbered past any folder (`:2711-2715`), a partial copy rolled back (`:2732-2735`), the live files cleared with the stage's own helper (`:2736`). The budget counts the first pass (`:2691-2696`, runbook `:967-970`), so after run_102's two passes (1.53 M of 1.8 M, stop 05b note 1.5) a third would be refused. Each retry re-runs regroup, rewriting the run's memory, KB entry and scoreboard (runbook `:1000-1003`); the first reading survives only in `retry_<n>/`. For autonomy: the hand rejection is the only quality feedback on the analyst, it costs about 3.6 USD (stop 00 note 1.7), and nothing records why the first reading was rejected except the queue note's `superseded`.
7. A refused first answer plus an exhausted run budget ends the run `rejected_budget_exceeded` before the retry (`:4926`, `:5021-5034`): a run whose backtests are paid and graded can end "rejected" because the analyst's second session would not fit the budget. Rare; the retry's cost is one prompt, so the budget rule bites only after a hand retry.
8. The reading is written in the five-readers' v3 shape: `MAX_SIDE_FINDINGS = 2` (`reader_proposals.py:83`), a mandatory `scores` block, rubric names per category, the envelope keys (`:118-148`), `flatten_reading` with a legacy `patch` branch (`:554-560`). One lens writes one claim or none; the container is sized for five readers with two findings each. Harmless; weight.
9. The audit keys (`RP:4935`) distinguish the in-stage re-ask (`_retry1`) from the D-202 pass (`attempt_<n>`), as stop 00 note 1.7 read them. Each is a full prompt (note 21a 1.2).

### (2) Legacy or simplifiable (leads)

1. `_record_side_finding_merges` (`RP:5260-5285`): no caller (grep over `workflow/` and `tools/`: definition only), as its docstring says. Delete with `reader_findings.side_finding_merges`, `merges_doc`, `merge_index` and `MERGES_ARTIFACT` (`side_finding_merges.yaml` in `_SPECIALIST_READERS_RUN_SCOPED_FILES`, `:4448`). Not checked: tests pinning them.
2. `_review_written_reading`'s `tests_none` branch and `test_request_row` (`RP:5196-5198`, `reader_findings.py:147-156`): unreachable for an analyst reading, since `check_answer` refuses `tests: none` first (`:1681-1683`); the row writer still labels `stage: "specialist_readers"` (`:150`), the source of the stale rows at stop 09 lead 2.7.
3. Readers-era shape kept for two lenses (note 1.8): `READER_RUBRIC_VERSIONS_V3`, `_LEGACY_READING_KEYS`, the `patch` branches of `check_reading` (`:420-445`) and `flatten_reading`, the E-072 and readers entries of `SKIP_RULES` (`:108-117`), `_reader_strictness` under `score_provenance` (`RP:5037-5047`). A reading of one claim would be a smaller object.
4. The retry prompt's 40,000-character log cap (`:1853-1854`) names omitted entries; a second session with a long first log re-runs queries it cannot see. Fine as a cap; recorded because the second pass is the expensive one.

### (3) Disagreements between the speech and the element

1. Step 5, "A change to position sizing is kept as an observation ... never a claim": a sizing vehicle is a refusal of the claim (`:1804-1808`); the model must answer again with it as an observation. Refused, not converted.
2. Step 7, "A date inside the sealed holdout is refused": any date at or after the holdout start's month (`:556-558`), which includes dates past the holdout. Wording.
3. Step 3, "a test that ever measured the opposite of its direction": any run of that test in this session's log, by floorless identity (`:1726-1729`), not earlier runs. Fine.
4. Step 11, "Accepted: warnings are noted ... never blocking": `_review_written_reading :5176-5213`; correct, and its `tests_none` request row cannot fire (lead 2.2), which section 6 states.
5. Step 12's refusal list: matches `:2654-2696` and adds the queue-save refusal (`:2719-2724`) only in the runbook (`:987-988`). The speech's "budget left" is "within its weighted token budget, the first pass counted" (`:2691-2696`).
6. Section 6, "The in-run merge of findings has no caller": confirmed by grep (lead 2.1). "The analyst's audit lines are still named after the deleted stage": `:4935`; confirmed.
7. Reading map verified: `RP:4885-5018` (`:4926`, `:4935-4944`, `:4945-4952`, `:4955-4964`, `:4966-4986`, `:4987-5010`, `:4867`, `:5012-5018`, `:5243`), `:5062-5150`, `:5153-5169`, `:5176-5213`, `:5260`, `:5027-5047`; `analyst_session.py:1553-1850` (no claim `:1598-1664`, claim `:1665-1850`), `:526-558`, `:575-621`, `:624-648`, `:836-919` (`:855`, `:881`, `:895`), `:922-1036` (`angle_of :1029`), `:1063-1141`, `:1472-1534`, `:1288-1412`, `:1537-1550`, `:1853-1886`; `reader_proposals.py:82-148`, `:337-445`, `:554`, `:607`; `reader_findings.py:40`, `:79`, `:108`, `:147`; `RC:2628-2651`, `:2654-2696`, `:2699-2766`, `:5971-5991`; `RUNBOOK.md:965-1012`.
