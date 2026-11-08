# Stop 00 of 12: Orientation — the two rules, the spine, the history

## Speech (verbatim)

Stop 00 of 12: Orientation — the two rules, the spine, the history. Open on the side: `strategy_designer_v2/README.md`, `strategy_designer_v2/CHANGES.md`, `strategy_designer_v2/STEPBACK.md` (last three entries), `CLAUDE.md` (root, "Hard rules"), `guided_tour/_post_tour/overall_review.md` ("Level 0") and `guided_tour/_post_tour/session_analysis.md`.

Note on a path: the itinerary places `_post_tour/` under `strategy_designer_v2/guided_tour/`; on this branch it sits at the repository root, `guided_tour/_post_tour/`.

### 1. In one sentence
strategy_designer_v2 ("v2") takes the operator's research goal, has a model write testable trading ideas, tests each in the bot's own backtester and records whether it worked; it never trades live.

### 2. Why it exists
The goal: a pipeline that finds a profitable strategy by itself, runs on its own and does not fool itself; the operator decides, the pipeline discovers. The reviewer after the v1 tour (`overall_review.md`, Level 0) found v1 "a careful, well-guarded backtesting loop that does not yet discover" and named one change: the path from idea to verdict, with the idea's own testable sentence as judge. The operator ruled v2 from scratch, fresh record, nothing copied by default (`session_analysis.md`, "Rulings"). A v1 piece enters only by hand, with a reason, when a v2 run asks; each addition is logged in `CHANGES.md`.

### 3. What comes in, what goes out
In: the operator's brief (goal, venue, product, strategy domain), the bot's backtester (the "engine", in `trading-bot/`), and a fold (a fixed set of test months the idea has never seen). Out: the ideas, one engine run per idea and coin, three answers per idea, rows in `records/`.

### 4. What happens here, step by step
The spine (README "The path"; itinerary "The live path"). The operator writes a brief. One model call turns it into many claims: a claim is one measurable sentence with its own pass number. The engine runs each claim on every window of the fold, at two position sizes. Branch 1, "was the idea right?": code, from the engine's per-bar output, as IC (a rank correlation between the signal and the return that follows). Branch 3, "is the book profitable?": code, from the engine's per-window metrics. Branch 2, "what did the book do?": the analyst, a second model call, reads a numeric summary of the run and proposes one next claim or none, which goes through the engine again. Everything is recorded.

The history, from `CHANGES.md` and `STEPBACK.md`. On 2026-11-05 v2 was built in eight tries; a night of runs followed. By then it had drifted: the judge read the stored prices directly, a quick profit check and a replication ran beside the engine, one engine component was on-off. On 2026-11-06 morning the operator wrote two rules on the README's first page; everything built against them was deleted, its results void, the shelf of validated claims included. Tries 09 to 12 rebuilt the pieces under the rules. Then run 003: the operator's daily breadth brief, BTC and ADA, fold A, ten claims, nothing validated, nothing profitable. `STEPBACK.md` ends there, naming this tour next.

Live today: brief, ideas, engine step, branch 1, branch 3, analyst, runner, records. Not built (README, "Status"): the holdout path, a fold draw for child claims, a use for validated filters, replication on other coins, tests, a faster engine.

### 5. What it costs
Run 003's model calls (`runs/real_01_daily_breadth_fold_a/003/model_calls.yaml`): ideas 0.19 USD, analyst rounds 0.31 and 0.12 USD; 0.63 USD in all. Engine time: stop 05.

### 6. How it stands against the two rules
Rule 1, the engine is the only reader of bars (a bar is one price candle; daily here): branches 1 and 3 come from the engine's outputs; nothing else reads stored prices; no quick check beside it. Rule 2, forecasts are linear: a claim carries a continuous strength, never a direction switch, graded by the engine's standardise step (it rescales a raw strength against its own recent past into a bounded forecast); no on-off book. This stop is documents only: it reads no bars and holds nothing on-off.

### Reading map
| Part | File and section | One line |
|---|---|---|
| Goal and v2's rule | `strategy_designer_v2/README.md`, title and "The rule of v2" | Starts empty; a v1 piece enters by hand, with a reason |
| The two rules | `README.md`, "The two rules that come before everything else" | Engine the only reader of bars; linear forecasts |
| The scars | `README.md`, "The scars" | Seven rules kept from v1: no lookahead, sealed holdout, one fold one verdict, and more |
| The spine | `README.md`, "The path"; `00_itinerary.md`, "The live path" | Brief → ideas → engine → three answers → record → next idea |
| What stands | `README.md`, "Status" | Live pieces, deleted pieces, not built |
| Every addition | `strategy_designer_v2/CHANGES.md` | What, which run asked, why, in order |
| The step-backs | `strategy_designer_v2/STEPBACK.md`, last three entries | Five questions before each try; ends at run 003 |
| Repo hard rules | root `CLAUDE.md`, "Hard rules" | No secrets, no lookahead, every trial ledgered, holdout sealed |
| Why v2 | `guided_tour/_post_tour/overall_review.md`, "Level 0"; `session_analysis.md` | v1 did not discover; rebuild the idea-to-verdict path |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Next

## Inspector notes

1. The two rules (`V2/README.md`, "The two rules"; `V2/CHANGES.md`; `V2/STEPBACK.md` last three entries): documents only, clean. The speech's claim that today "nothing else reads stored prices" is not checkable at this stop; a grep of `V2/run.py`, `V2/steps/ask.py`, `V2/steps/engine/backtest.py`, `V2/steps/judge/judge.py` shows the only market-data entry point is `backtest.py` via `research_folds.load_fold_windows` and the bot's `run_backtest`, and `judge.py` imports only numpy, pandas, yaml. Held open until stops 05 to 09.
2. Rules without code behind them (`V2/README.md`, "The scars" 4 and 6): "every state write is atomic" and "a budget per lineage and per day; the analyst is capped". No `os.replace`, temp-file write, budget or cap appears in the four v2 code files (grep: the only "cap" is the standardise cap in `backtest.py`). `guided_tour/_post_tour/session_analysis.md` ("What the session does not prove") itself lists "no budget per day" as not built. The README states as scars two things the pipeline does not do; to verify at stops 02 and 09.
3. The record of additions is incomplete (`V2/CHANGES.md` against `V2/STEPBACK.md`): CHANGES has no entry between try 08 and the 2026-11-06 clean-up, yet STEPBACK "03:50" lists about 350 lines added during the night (coverage check, per-symbol refusal, two-size engine run, t-statistic, replication step, lite-book sweep, record query, morning-file generator). Several of these survive the clean-up (two sizes, coverage check, per-symbol refusal, t-stat, `records/query.py`, `night_2026-11-06/make_readme.py`) and have no CHANGES line naming the run that asked. The README's "every addition names the run" does not hold for them.
4. Stale lines in `V2/README.md` "Status": the paragraph first says the runner "does not run until branch 1 is rebuilt" and the ideas step is "to be changed so a claim carries a continuous strength", then says both were done (tries 09 to 12). The first sentences are the morning's state and were not updated in the evening. A reader of the first page gets two states of the same file.
5. "Only a run asks" versus "the operator rules" (`V2/README.md`, "The rule of v2"; `V2/CHANGES.md` entries of 2026-11-06): every rebuilt piece names "the operator" as asker, not a run. That is right (the rules came from a ruling), but the page says a piece enters "when a v2 run asks for it"; the second trigger, an operator ruling, is not written. Small; same lesson as STEPBACK "Why did it drift?": a rule not written is not a rule.
6. Void history lives beside live results (`V2/runs/`, `V2/records/shelf.yaml`): `runs/` holds 40 `n*` night folders, 17 `_batch*.sh`, three `_night_*.sh` and `_replications`, all void, in the same directory `records/query.py` and `night_2026-11-06/make_readme.py` scan (`make_readme.py` line 7 picks the night by excluding `fake_`, `real_01_...`, `try`). `shelf.yaml` carries 26 entries marked void and one `status: validated` (a filter from a fake brief, `thin_volume_drift_reverts`); STEPBACK's last entry says so. Nothing redundant yet, but the live namespace and the void one are the same folder; to watch at stops 10 and 11.
7. Design (`guided_tour/_post_tour/overall_review.md`, Level 0; `V2/CHANGES.md` try 09): the review's one change was "let the claim, the idea's own testable sentence, be the judge of its run". After try 09 every claim is graded by "one fixed rank-correlation measure" of forecast against forward return. The claim's own pass condition is then a threshold on a shared measure, not its own sentence. This may be the right trade for linearity, but it is a change from the review's Level 0 that no page names; to check at stops 03 and 06.
8. Speech against element: (a) costs 0.19 + 0.31 + 0.12 USD match `runs/real_01_daily_breadth_fold_a/003/model_calls.yaml`; (b) "the shelf of validated claims included" was voided: true of the night's entries, but one validated entry stands, so "the shelf is void" would be wrong and the speech does not say it; (c) the speech says v2 was "built in eight tries" on 2026-11-05: CHANGES agrees; (d) the itinerary says thirteen stops, the speech says "Stop 00 of 12": numbering, not a disagreement. No disagreement of substance at this stop.

Running view after stop 00: the first page is right in its rules and stale in its status; the change log skipped the night; two scars are written as rules with no code. The two rules themselves are untested until the code stops.
