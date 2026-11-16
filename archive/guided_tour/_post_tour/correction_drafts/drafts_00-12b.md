# Correction drafts, stops 00, 01, 02, 03a, 03b, 04, 05a, 05b, 06, 07, 08, 09, 10, 11, 12a, 12b

## Stop 00
Items: 00-1
**Correction (<date>).** The header says "Stop 00 of 29". The tour has thirty stops, numbered 00 to 29 (`guided_tour/00_itinerary.md:80`, "Thirty stops"), held in 36 stop files because six stops are split in two parts (03, 05, 12, 21, 22, 24). "Of 29" is the number of the last stop, not the count of stops; the header form was set by the guide's instructions (`guided_tour/00_guide_opening_prompt.md:86`), so every stop header reads the same way.

Items: 00-3, 00-4
**Correction (<date>).** Two points in part 2.
1. Part 2 says the stage objectives table has "fourteen rows", then lists fifteen. The table has fifteen rows, the fifteen the speech names (`SR/docs/USER_GUIDE.md:307-321`, header row at `:305`).
2. Part 2 gives the guide's "ground truth" (the stage list, the handoff templates and the routing functions, `USER_GUIDE.md:163-166`) without saying that the stage list itself still holds the old order. Its usual next stage after step 2 is validation (`run_phase1_research.py:181`) and after the backtests the verdict interpreter (`:214`). The route runs actually take is set by overrides inside the run loop: after step 2 the run goes to variant building under config-direct authoring (`:20233-20234`), and after the backtests to the analyst, the record-keeping or the grid route (`:20181-20183`); the comment at `:20168-20171` says the verdict interpreter "becomes unreached, not deleted". Read alone, the stage list describes the switched-off route, not run_102's.

Items: 00-5, 00-6
**Correction (<date>).** Two points in part 3.
1. Part 3 says the counters "are covered at stops 04 and 05". They are not: stop 04 says "stop 00 named what reads them" (`guided_tour/04_launch.md:52`), and no speech of stop 05a or 05b names them. The facts: the two counters are written at setup (`SR/workflow/setup_run.py:77-80`). The refinement counter is read only in the validation route and the old refine route (`run_phase1_research.py:9797`, `:11791`), neither reached under the current switches, and is copied as text into each stage's handoff (`:19990`), where no code reads it; an AI stage sees it only because the whole handoff is put into its prompt (`:1092-1093`). The rerun counter has no reader. A campaign halt record copies the whole counters block as a snapshot (`run_campaign.py:1816`) and decides nothing from it.
2. Part 3 describes the audit log as "cost, tokens, model per AI call". An analyst entry holds more: time stamp, engine, duration, cost, number of turns, how the call ended, tokens, number of tool calls, tools refused, tools offered, and the models used, as a list rather than one model field (`run_phase1_research.py:4937-4944`). Its name also tells two kinds of retry apart: `specialist_readers_analyst_<lens>_attempt_<n>`, where n is the stage's attempt number, with `_retry1` added when the analyst is asked again inside the same attempt (`:4935`, loop at `:4924`); a stage retried as a whole gets a new n.

## Stop 01
Items: 01-1
**Correction (<date>).** The header says "Stop 01 of 29". The tour has thirty stops, numbered 00 to 29 (`guided_tour/00_itinerary.md:80`), held in 36 stop files; "of 29" is the last stop's number, in the header form the guide was given (`guided_tour/00_guide_opening_prompt.md:86`).

Items: 01-4
**Correction (<date>).** Part 3 notes that the start manifest's rationale still names the old weight, without saying why. When decide-next applies a config change, it takes the source run's manifest (`SR/tools/decide_next.py:1978`) and returns an unchanged copy of it (`:2001`); the candidate brief writes that copy as `start_manifest` (`:2764`). No code in decide-next rewrites a manifest's rationale, so the text still describes the source run's config, not the changed one.

Items: 01-5, 01-7
**Correction (<date>).** Two points in part 4.
1. Part 4 says the 1a model reads the brief's `scope` and `available_data` only as text. Not said: the 1a skill names the scope block as an input ("`research_brief.yaml`, with its scope block", `SR/workflow_artifacts/skills/hypothesis-design/SKILL.md:10`) and asks for formulas "computable from the feeds in the brief's scope block" (`:31`), while a decide-next brief has no scope block, because decide-next copies five keys only (`decide_next.py:2664-2665`). On a decide-next run the skill points the model at a block that is not there.
2. Part 4 says `source.start_config_sha256` is read by `SR/tools/fold_confirm.py:634`. No code reads that key: it is written at `decide_next.py:2740` and `:2766`, and `fold_confirm.py:634` is a comment that names it. The check made there (`_start_config_changed`, `fold_confirm.py:454-473`, called at `:635`) compares the brief's `candidate.start_config` (`:462`) with the variant's strategy config (`:463`) value by value, not by fingerprint. The rest of the line holds: `source.expected_config_sha256` is read at `run_phase1_research.py:6261`, `:8500` and `:16584`.

## Stop 02
Items: 02-1, 02-2, 02-3
**Correction (<date>).** Three points in "What happens here, step by step".
1. Step 6 says every line is checked against "a fixed vocabulary of states and labels". The labels are fixed lists (source, relation, brief status, origin; `SR/tools/record_schema.py:123-133`, applied at `:379-381`). The states are not: a pattern accepts five fixed words plus any "paused:<text>" and any "blocked_on_<text>" (`record_schema.py:113-114`, applied at `:376`). The first queue line's state, `blocked_on_daily_bar_ingest` (`SR/config/campaign_queue.yaml:6`), passes only through that open pattern, and no code sets it.
2. Step 2 says the registrar refuses a brief that still holds the template's blanks. The same check runs every time a brief is read: at registration (`run_campaign.py:981`), at the launch of a new brief or of a saved extra idea (`:4412`, `:4429`) and in the dry run (`:5865`); the check itself is at `:719-727`. Stop 01 part 4 says so.
3. The speech says registration "takes no lock" and stops there. Not said: registration reads the queue, appends its line and rewrites the whole file (`run_campaign.py:996`, `:1022`) outside the campaign lock (it exits at `:5983-5984`, before the lock at `:6014-6024`), while the running campaign also rewrites the whole file at its state changes (`_save_queue`, `:191-214`), whose own note calls the queue "the clearest concurrent-writer-risk file in this repo" (`:194-198`). Several runner paths re-read the queue just before they save (for example `:2410`, `:4314`); whether a line registered during a run can be lost was not traced, so this is a risk the code names, not a loss observed.

## Stop 03a
Items: 03a-3
**Correction (<date>).** Section 6 names three switch comments that still say "held off" although the switch is on (profit bars file, config-direct authoring, variant loop) and says "several" comments say "today's default". Other comments are also out of date against the files. The profit bars file comment says the bars file ships unratified with placeholder thresholds (`SR/config/campaign_config.yaml:376-383`), and the every-backtest bars comment says "Still blocked on ratified bar values" (`:421`), while the bars file now carries its ratification fields (`SR/config/profitability_bars.yaml:338-339`). The grid comment says its routing is "NOT yet wired" and "Blocked on E-046b" (`campaign_config.yaml:340-348`), while the run loop routes on the grid when the switch is on (`run_phase1_research.py:20177-20187`, `:20660-20675`). "Today's default" appears once (`campaign_config.yaml:169-170`), not several times.

## Stop 03b
Items: 03b-1, 03b-4
**Correction (<date>).** Two points on the register's test.
1. Step 4 of the register lists what its test checks, correctly, but not what it leaves out: the test asks for a "waiting for" text only on lines marked off (`SR/tests/test_feature_flag_register.py:187-198`), and no test reads the reader, the criterion or the "waiting for" text of a line marked on. That is why lines switched on can keep an old "waiting for" text, as section 6 reports. (The count of 25 such lines was not re-checked on this checkout.)
2. Section 6 says the quarantine switch has no register line, without the reason. The register test collects only the switches under `orchestrator:` whose block has an `enabled` key (`test_feature_flag_register.py:78-83`); the quarantine switch sits elsewhere, as `halt_policy.quarantine_enabled` (`SR/config/campaign_config.yaml:121-122`), so no test asks for its line. The register mentions quarantine once, in a comment (`SR/config/feature_flag_register.yaml:443`).

## Stop 04
Items: 04-1, 04-2
**Correction (<date>).** Two points in "What happens here, step by step".
1. Step 12 says that before any AI call the launcher checks that no two test windows share a day and that none touches the validation period. For a new run, whose protocol file does not exist yet, only the second check is made then: the expected windows are rebuilt from the pre-registration and checked against the validation period (`run_campaign.py:3914`, reached from `:4045-4047`, before the "no file yet" return at `:4059`). The shared-day check reads an existing protocol file (`:3958-3967`), so it is skipped; on that path the first shared-day check is made when the backtests start (`SR/tools/run_protocol.py:2151`), after steps 1a, 1b and 2 have been paid for. The windows a new run builds cannot share a day by construction: consecutive windows cut from the start to the end date, or fold blocks that the folds loader checks (`SR/tools/research_folds.py:153-215`).
2. Step 8 says the launcher records whether the operator may trade that exchange and product. Not said: that mark changes nothing in the research loop. It is written at launch (`run_campaign.py:787-792`) and read only on the holdout paths, through the hold at `run_phase1_research.py:15626`, called at `:7614`, `:7655` and `:15772`; its other uses are the pause label for that hold (`run_campaign.py:1509-1510`, `:1911`).

Items: 04-3
**Correction (<date>).** Section 6 says the state file's template fields are written at setup and "stop 00 named what reads them". Stop 00 did not: it sent them on to stops 04 and 05 (`guided_tour/00_orientation.md:49`). The readers are these. The refinement limit (`max_refinements_after_validation`) is read at `run_phase1_research.py:9798` and `:11792`, and the refinement counter at `:9797` and `:11791`, all in the validation route and the old refine route, which the current switches do not reach; the refinement counter is also copied into each handoff as text (`:19990`). The other three limits (`max_hypothesis_variants_per_cycle`, `max_reruns_after_analysis`, `max_required_reads_per_stage`), the rerun counter and the flags `holdout_reserved` and `screening_passed` have no reader outside the setup that writes them (`SR/workflow/setup_run.py:64-88`); the flags `validation_approved` and `walk_forward_passed` are set later (`run_phase1_research.py:9812`, `:16052`) and never read.

## Stop 05a
Items: 05a-2, 05a-3, 05a-8
**Correction (<date>).** Three points in "What happens here, step by step".
1. Step 3 says the added inputs exist only in memory and the handoff file on disk stays the copied template. The added inputs are in memory only (`run_phase1_research.py:9693-9737`), but the file does not stay the template: before every stage the loop writes the run id and an "injected context" block (the stage's attempt number, the refinement counter, whether a person's context was added) into the run's handoff file and saves it (`:19980-19997`).
2. Step 10 says a schema mismatch is logged, not blocked. Not said: the warning goes only to the program's error output and is written to no file of the run (`SR/tools/workflow_artifact_validation.py:32`, `:117`, `:129-130`; the pipeline sets up no log file), and the blocking mode exists only when the setting `WORKFLOW_ARTIFACT_VALIDATION=raise` is given (`:37`, `:46`), which no runner does.
3. Step 9 says an answer that misses a file is retried once. Not for step 1a when some of its files were saved: there, a missing card is also how a split into several cards or an exhausted brief reaches its handler, so the retry is skipped and the error is raised at once (`run_phase1_research.py:909-916`, raised at `:929`).

## Stop 05b
Items: 05b-1, 05b-2, 05b-4
**Correction (<date>).** Three points in "What happens here, step by step" and the handoffs paragraph.
1. Step 3 lists the endings that stop the loop by their first word ("completed", "rejected", a pause, a failed validation; `run_phase1_research.py:19771`). Not said: two "completed" endings leave the run's status "active". The status is set to completed only for the three grid endings and the refold ending (`:20684-20686`; endings at `:5683-5684` and `:5218`). The other two are "brief exhausted" (`:20163-20164`) and "no new hypothesis", set after 1a (`:20165-20166`) and also after 5a when every variant would be an exact repeat (`:19440-19446`, returned at `:9667`).
2. Step 7's chain is right but leaves out three turns. After the backtests the next stage is first set to the analyst (`:20177-20183`), and the variant-loop branch can then turn it into a pause for a person (from `:20453`, pause at `:20520`). Between "is a holdout decision waiting" and the grid route, a refold run (a re-run on another fold, profit bars only) stops at its own ending (`:20593-20595`). And after the grid route, a run ending on one of the three grid verdicts goes to the campaign review instead when a review is due (`:20610-20611`, `_retired_review_route` at `:7867`).
3. The handoffs paragraph says the five handoffs the loop writes are written "the first time their stage starts". That holds for the analyst's and the record-keeping's (`:4547`, `:8838`). The variant-building, data-check and backtests handoffs are rewritten from the current switches at every entry into their stage (`:19830`, writing at `:10057-10059`); the reading-map row "written once per run" is wrong in the same way.

Items: 05b-5
**Correction (<date>).** Section 6 says a run left at the deleted "specialist readers" stage is resumed "into the analyst or the route". Under the tour's switches (analyst and record-keeping both on) it resumes into the analyst when a lens reading is missing, and otherwise into the record-keeping stage; it goes straight to the route only when record-keeping is off (`run_phase1_research.py:5389-5400`, called at `:19781`). The reading-map row ("analyst / regroup / route") is right.

## Stop 06
Items: 06-1
**Correction (<date>).** Step 5 says the fold of a follow-up run is drawn among the folds the source run is not on. That is right, and it is the only exclusion: the draw looks at the windows of the one source run (`SR/tools/research_folds.py:294-303`; decide-next passes one run id, `SR/tools/decide_next.py:1887-1890`), not at the runs before it. So a follow-up of a follow-up can draw the fold an earlier run of the same idea was on. The opening sentence, "never on the months where it was found", holds one generation deep only.

## Stop 07
Items: 07-1
**Correction (<date>).** Step 7 says a pre-filled claim is written into the card by code, unchanged. Only when that claim passes the claim check: if it has errors or no test, or if there is no card, code leaves the AI's own claim in place (`run_phase1_research.py:17338-17344`; the copy at `:17346-17348`).

Items: 07-6
**Correction (<date>).** The reading map points the overlap criterion (the residual IC added by code) at `run_phase1_research.py:5913`. That function serves a run whose pass rule 1a wrote itself; it is called only when the pass rule was not built from the card and combinations are switched on (`:20127-20131`). When 1a picks the criteria (a decide-next candidate whose criteria wait for 1a, or a brief that leaves them to 1a), the overlap criterion is added inside the pass-rule writer (`:8424-8429`, within the row "Pass rule from the card"). A decide-next candidate whose brief fixed its criteria returns before that point (`:8411-8416`) and gets the overlap criterion from neither path at 1a.

## Stop 08
Items: 08-1, 08-3
**Correction (<date>).** Two points in "What happens here, step by step".
1. Step 1's figures are right. Not said: the entry's own notes read the daily results as inconclusive. On daily bars there is too little data to say whether the criterion separates good ideas from bad, and the three daily passes come from one strategy that failed every profit bar (`SR/config/criterion_menu.yaml:207-216`).
2. Step 3 says the whole-test Sharpe is "for a brief only, not for step 1a". Not said: the entry has no minimum sample (`floor: {}`, `criterion_menu.yaml:141`); only computability stands, at least 30 daily returns (`:131-132`). And "not for step 1a" is a written rule, given to 1a in its skill (`SR/workflow_artifacts/skills/hypothesis-design/SKILL.md:47`) and in the menu's comment (`criterion_menu.yaml:124`); no code refuses it on a 1a card, whose check refuses only unknown ids, entries retired for blocks and bad overrides (`run_phase1_research.py:8216-8290`).

Items: 08-6
**Correction (<date>).** The reading map's "Readers" row lists six files. `SR/tools/protocol_resolution.py` is not a reader: its only mention is an error message that names the file (`:328`). `SR/tools/explore_confirm.py` is a reader and is missing: it reads the run's criteria from the pre-registration and the menu (`:374`, `:389`). `SR/tools/structure_key.py` reads only the pre-registration's protocol reference (`:316-324`), not the criteria.

## Stop 09
Items: 09-1, 09-3
**Correction (<date>).** Two points in "What happens here, step by step".
1. Step 1 lists six kinds of bar selection; there are seven. The seventh, "all of", keeps the bars where two or three other selections all hold (`SR/tools/claim_tests.py:704-721`). The reading map names it.
2. Step 4 says an AI may rewrite the tests once. Not said: that call runs on the default model, Haiku 5.5, not on 1a's Sonnet 5.5 (`_claim_llm_call`, `run_phase1_research.py:17989`, through `_invoke_reader_llm`, `:4660-4668`, with the default model at `:1140`); only steps 1a and 1b have a model of their own (`SR/config/campaign_config.yaml:878-880`). And "a pre-filled claim is never revised" holds with the folds switch on, for a candidate that carries both a claim and a link to its proposal (`run_phase1_research.py:18153-18171`).

## Stop 10
Items: 10-2, 10-3
**Correction (<date>).** Two points in "What happens here, step by step".
1. Step 5 says a failed check sends 1b back once and a second failure pauses the run. There are three outcomes. A second failure of the graded/standardised rules or of the size check pauses the run (`run_phase1_research.py:16613-16630`). A second invalid block manifest raises an error, which ends the run as failed, not paused (`:16643-16646`; the loop's error handling at `:20710-20713`). And a decide-next config that 1b must copy unchanged gets no retry at all: a rule failure pauses at once (`:16613`), a manifest failure fails the run at once (`:16636-16642`).
2. Step 7 says that, with an exact config in the brief, code replays "the AI's config" against it. On that path there is no AI config: with the exact-config switch on, 1b is code that saves the brief's config unchanged (`:17078-17086`, called at `:20081-20083`, saved at `:17136`), and the replay gate then compares that copy with the brief's config (`:17186-17220`, called at `:18922-18923`). The gate checks code against its own input.

## Stop 11
Items: 11-1, 11-2, 11-3, 11-4, 11-6
**Correction (<date>).** Five points on who reads the five documents.
1. Step 3 says "code groups tried ideas by that name" (the indicator library entry a card names). No code groups the tried ideas the AI steps see: their list has no family grouping (`SR/tools/campaign_memory.py:926`). The one grouping by that name is the old family digest (`SR/tools/build_exclusion_digest.py:151-154`), built on demand into `SR/campaign_record/exclusion_digest.yaml`, which the campaign does not rebuild; decide-next reads it for an information-only note on each candidate, never a refusal (`SR/tools/decide_next.py:1576-1590`, `:1800-1801`). The speech's sentence repeats the 1a skill (`hypothesis-design/SKILL.md:76`).
2. "Read by" says step 2 reads data availability and code reads the indicator library. Step 2 does not receive `DATA_AVAILABILITY.md`: its template gives it the indicator library (`hypothesis_to_innovation_expansion.yaml:11-12`), and code adds the coin universe (`run_phase1_research.py:3167-3171`) and, under a switch, the guide and the catalogue (`:9071-9091`). Step 1b gets data availability as an optional input only (`hypothesis_to_strategy_config_authoring.yaml:21-23`). No code opens the indicator library; code reads only the entry name a card gives, through the digest note of point 1.
3. The reading map's "Library readers" names `SR/tools/campaign_memory.py`, which never mentions the library or its entries. The readers are the 1a template (`research_brief_to_hypothesis.yaml:9-10`), the step-2 template (`hypothesis_to_innovation_expansion.yaml:11-12`) and the digest of point 1.
4. The reading map's "Who injects them ... `:3181-3190` (data availability)" points at the input lists of validation (`run_phase1_research.py:3181`) and of variant building as an AI stage (`:3188`). Under config-direct authoring, validation is not reached and variant building is a code-only stage (`:20225-20234`); the live injection of data availability is 1b's optional input, which the same row also names.
5. Section 6 does not say that the indicator library has no code reader (point 2), nor that BTC and ETH in the coin universe carry no exchange and so, by the file's own rule, point to the Binance cache (`SR/config/coin_universe.yaml:7`, `:16-24`; `SR/tools/refresh_coin_start_dates.py:126`, `:132`). The live asset-variant check does not use that default: a coin with no exchange takes the run's exchange, or the brief's venue when one is declared, and Binance only when neither is given (`SR/tools/variant_coin.py:642-655`).

## Stop 12a
Items: 12a-1
**Correction (<date>).** Step 3 names fifteen of the 18 transform ops. The registry's three groups hold 7 history ops, 6 value ops and 5 bar-reading ops (`TB/strategies/registry.py:312-350`); the sentence leaves out `identity` and `negate_percentile` (history) and `vol_adjusted` (bar-reading). The count of 18 is right.

## Stop 12b
Items: 12b-1, 12b-2, 12b-5
**Correction (<date>).** Three points in "What happens here, step by step" and the validator paragraph.
1. Step 2 calls its figure "how many bars it needs before its first forecast". The figure itself is right (the longest warm-up among components and transforms, at least 24, at least the sizing window plus one; `TB/strategies/main_strategy.py:69-80`, `TB/strategies/strategy_engine.py:571-585`), but the first forecast comes later. A component adds values to its history only once it has its own warm-up (`strategy_engine.py:420-425`), and the strategy is ready only when every component of the bar's state holds that figure of history values (capped by the smallest history size; `:566-569`, `:405`). So the first forecast comes after a component's own warm-up plus up to that figure again.
2. Step 3 says a component error is counted and sampled, not hidden. True of errors while updating (`main_strategy.py:178-199`). An error while forecasting is caught one layer up and returns forecast 0 with the label "error" (`TB/strategies/strategy_base.py:398-406`), as step 8 says, but it is not counted: the error count the backtest saves is the update count only (`main_strategy.py:191`; `TB/core/backtester.py:676-678`).
3. The validator paragraph says "weights positive". Rule V8 asks that each weight be a number and that the weights of a state add up to more than 0 (`TB/tools/validate_config.py:270-290`); a single negative weight is allowed, as the design guide says (`SR/docs/STRATEGY_DESIGN_GUIDE.md:239`).

Items: 12b-6
**Correction (<date>).** Section 6 says no research call site passes the regrid's two arguments, as the constructor's note says. The note is out of date: the backtest launcher passes both (`TB/core/launcher.py:933-937`). The regrid still stays off in research runs, because the second argument is empty unless the launcher's indicator-fill option is set (`:631`, `:931-932`), and no research caller sets it (`SR/tools/run_protocol.py:2609-2615`, `:2682-2688`).

## Not drafted
06-6: The speech's figures are right (`SR/config/folds.yaml` has 66 lines by `wc -l`; the inspector's 67 is wrong). What remains is line drift only (the draw ends at `research_folds.py:317`, the map says `:321`; the map's `run_protocol.py:2163-2178` lies inside the function that starts at `:2156`), and line drift is not a correction under the brief.
07-8: Nothing in the speech is wrong. The skill file lengths it gives match this checkout (SKILL.md 84, BRIEF_HYPOTHESES.md 83, CLAIM_TESTS.md 237, CLAIM_TESTS_TRADE.md 135, CLAIM_TESTS_EXECUTION.md 16, PREFILLED_CLAIM.md 20, DECIDE_NEXT_CANDIDATES.md 51); the inspector's "short by one" is wrong; the run_102 cost figures cannot be checked here.
10-6: Nothing in the speech is wrong on a fact. The line counts are right (SKILL.md 317, CLAIM_NOTE.md 13, NEAREST_BUILD.md 38, START_FROM_CONFIG.md 18, quant-fundamentals SKILL.md 171); the `forecast_rules.py` ranges differ by a line or two (the speech's `:131-170` covers both functions at `:131-138` and `:141-168`; the rule sentence is `:56-61`, not `:55-60`), which is line drift only.
