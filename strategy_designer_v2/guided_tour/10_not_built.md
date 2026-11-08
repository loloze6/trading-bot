# Stop 10 of 10 (was 12): What is not built

## Speech (verbatim)

Stop 10 of 10 (was 12): What is not built. The closing stop, renumbered by Rectification 1. Open on the side: `strategy_designer_v2/README.md` ("Status", and "The two rules", "The scars"); `strategy_designer_v2/night_2026-11-06/README.md` ("Open asks"); `guided_tour/_post_tour/session_analysis.md` ("What the session does not prove"); `strategy_designer_v2/guided_tour/00_itinerary.md` (row 12).

### What is not built
Each piece in one line, with where it is named. "Not in code" means a search of `run.py` and `steps/` finds nothing for it.

| Missing piece | What it would cover, in one line | Where it is named |
|---|---|---|
| The holdout path | No step runs a claim on the sealed months; nothing has touched the sealed store | `README.md`, "Status"; night `README.md`, "Open asks"; `session_analysis.md`; itinerary row 12 |
| A fold draw for child claims | The analyst's claims run on the same fold as the first round (the runner's `--fold`) | `README.md`, "Status" ("a fold draw for child claims"); `session_analysis.md` ("no fold draw across a lineage"); itinerary row 12 |
| A use for validated filters | A claim that passes branch 1 but trades no profitable book has no further step | `README.md`, "Status"; night `README.md`, "Open asks" ("A validated filter waits for a book"); itinerary row 12 |
| Replication as the engine on other coins | The same claim code run through the engine on coins outside the brief | `README.md`, "Status"; itinerary row 12 |
| Tests | No test files in `strategy_designer_v2/` | `README.md`, "Status"; `session_analysis.md`; itinerary row 12 |
| A faster engine | The engine is the only reader of bars; run 003 spent 868 seconds in it | `README.md`, "The two rules" ("if the engine is too slow, make the engine faster") and "Status"; itinerary row 12 |
| A budget per lineage and per day | Not in code; the analyst is capped only by `--rounds` | `README.md`, "The scars", 6; `session_analysis.md` ("no budget per day") |
| A queue of briefs | One run of `run.py` takes one brief | `session_analysis.md` ("no queue of briefs") |
| A memory of the operator's own words | Not in code | `session_analysis.md` |
| A significance floor for branch 1 | The t-statistic is written and is "information only" (`judge.py`); a floor is "the operator's ruling" | night `README.md`, "Open asks" |
| Daily claims with year-long windows near the start of a coin's history | Refused by the engine's warm-up, not scored | night `README.md`, "Open asks" |

One line in `session_analysis.md`, "no record query", is now built: `records/query.py` (stop 09).

### Reading map
| Part | File and section | One line |
|---|---|---|
| The list as v2 states it | `strategy_designer_v2/README.md`, "Status", last sentences | Holdout, fold draw, filters, replication, tests, faster engine |
| The engine-speed rule | `README.md`, "The two rules" | "make the engine faster" |
| Budget | `README.md`, "The scars", 6 | Per lineage and per day; analyst capped |
| Open asks | `strategy_designer_v2/night_2026-11-06/README.md`, "Open asks (recorded, not built)" | Four items |
| Readiness list | `guided_tour/_post_tour/session_analysis.md`, "What the session does not prove" | Seven items, one since built |
| The tour's own list | `strategy_designer_v2/guided_tour/00_itinerary.md`, row 12 | Six items |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Next close. What's next and how to best utilize this tour feedback from feedback analyzis approach ?

## Inspector notes

1. The two rules at the close (`V2/README.md` "The two rules"): across the ten stops no step reads the price cache beside the engine, and no component is on-off by construction: the rules hold as the files stand. They hold by the model's manners in two places and by an engine constant in a third: the claim's code runs inside the engine behind a regex that stops neither `pd.read_csv` nor `__import__` nor most forward-looking forms (stop 04, notes 1 and 2); nothing checks that a strength is continuous (stop 03); and the cap at twice the target makes 6% to 70% of bars a switch, which nothing bounds (stop 04, note 3). The speech's table lists none of these three as "not built"; they are the missing pieces that belong to the rules themselves.
2. The list against the code (`README.md` "Status"; `night_2026-11-06/README.md` "Open asks"; `session_analysis.md`; the speech's table): the table is right on what it names; it misses what the stops found missing. Not built and named nowhere: a per-brief fold line (stop 01, note 4; the queue in the table cannot exist without it); a brief format and check (stop 01, note 5); a void mark or purge in `claims_tried.yaml`, whose 574 void rows steer the live ideas call (stop 03, note 6; stop 09, note 7); run and brief names on the live ledger rows and a row for refusals (scar 5; stop 05, note 2); `DONE` on refusal or a resume rule that skips `REFUSED` (stop 09, note 3); the book summary to the analyst on failed claims and `exposure_pct`, `cost_drag_pct` left in what it sees (stop 08, notes 2 and 3); the analyst-round horizon in `summarise.py` (stop 08, note 4, now in the guide's correction); a floor or a fixed value for `min_effect` (stop 03, note 4); a slot in the records for a finding about the pipeline (stop 08, note 5). All are lines, not builds.
3. Scars with no code (`README.md` "The scars" 4 and 6): "every state write is atomic" and "a budget per lineage and per day" are written as rules learned and are implemented nowhere (checked at stops 00, 02, 05, 09: every write is `write_text`, no cap but `--rounds`). The speech's table names the budget; it does not name atomic writes. A rule on the first page that the code does not keep is the drift the README itself diagnosed ("a rule that is not written is not a rule" has a twin: a rule written and not kept).
4. What the pipeline already found and nothing acts on (the operator's working rule: "build only what a run asked for; what one change would a practitioner make to this book"): run 003's own rows say every book is 97 to 99% exposed and pays 5% to 134% of gross in fees; the engine has a rebalance band and a smoothing op the v2 config leaves unused, and the claim's horizon reaches neither (stops 04 and 07). The analyst found twice that pooled IC hides within-window consistency (stop 08, note 5). These are the run's asks, in the files, and the records have no place to hold them, so the "not built" list is written from memory, not from the runs. The night's `ANALYSIS.md` had such a section ("What it asked for and did not get"); the live loop writes none.
5. Simplifiable at the close, the full list of what the stops found dead or doubled: `steps/ideas/check_claims.py` (stale format, no caller); the `horizon` parameter of the component (stored, unread); the format's `brief:` field and `how_it_trades` line (read by nothing); `compared_to` (no code computes a baseline); `spaced()` and the sparse example in `CLAIM_FORMAT.md` (the shape the same page warns against); `ALLOC` in `summarise.py`; `--max-claims` and `--windows` (test knobs); the fee stated three ways; "dense strength" and the common rule stated twice each; two "already tried" mechanisms; one model named under two keys; 19 night shell scripts and 40 void run folders beside the live ones in `runs/`, 40 void briefs beside 5 live ones in `briefs/`; two record eras in each record file. None of it is large; together it is most of what a reader of v2 has to learn to ignore.
6. Speech against element: the eleven rows match their sources; "no record query" correctly struck. One row is thin: "Tests: no test files" is true (no `test_*.py` under `V2/` outside `runs/`), and the stops found the one test that matters cheaply available and unrun: the lookahead check by re-running a claim's code on the buffer minus its last bar (stop 04, note 2). The speech does not say that "the holdout path" is also the only piece on the list the operator has reserved for themselves (README "The path" step 7), so it is not "not built" in the same sense as the others.
7. On the operator's closing question (what next, how to use the tour's feedback), from the files and the operator's own working rules only: the rules say rulings are batched per run, one review, one decision set, one build window. The tour is the review; the inspector notes across the ten stops are one list of about seventy numbered items, each with a file and a line, most of them one-line changes and a few of them rulings (the measure of branch 1 on `strength` or `forecast`; pooled or per-window IC; a `min_effect` floor; smoothing or a band in the book; one size or two; the drawdown bar against the brief; the fee's one source). The way to use it that the working rules already prescribe: sort the items into defects a run revealed (fix in the build window), rulings (the decision set), and pages to correct (README "Status", "The path" steps 2 and 3, the brief's format, the shelf note), then run the operator's brief once more on fold A and read the equity curve and the exposure before the bars. The inspector does not rule.

Running view, closed. v2 is small, and its spine is sound: one claim, one strength, one fixed template, one engine run, two code verdicts and one reading, recorded. The two rules hold today because the model behaves, not because the system makes them hold. The pages are behind the code in four places (README "Status", "The path" steps 2 and 3, the shelf note, the brief's "four lines"), the records carry two eras without a mark, the loop runs one brief and stops, and the one step built to read the book is handed the book only when the book is no longer the question. Every result so far is one fold, one brief, no pass. Nothing in the files says the goal is out of reach; the files say the pipeline has not yet been allowed to look where its own rows point.
