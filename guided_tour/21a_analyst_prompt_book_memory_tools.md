# Stop 21, part a: the analyst, what it is given

## Speech (verbatim)

**Stop 21 of 29, part a: the analyst, what it is given.** Open on the side: `strategy-research/workflow_artifacts/skills/analyst/` (SKILL.md, forecast.md, trade_efficiency.md), `tools/analyst_session.py`, `tools/analyst_queries.py`, `tools/analyst_memory_view.py`, `tools/catalogue_section.py`, `docs/DATA_DICTIONARY.md`, `workflow/run_phase1_research.py`. Two parts: 21a, what the analyst is given (this speech); 21b, what happens to its answer (next).

**In one sentence.**
The analyst is the second judge after a backtest (a simulation of the strategy on past bars): two AI investigators, called lenses, dig into the run's own bars and trades with seven fixed measuring tools, and each ends with one testable idea for a next run, or none.

**Why it exists.**
The pass/fail grid (stop 19) says whether the idea held; the profit bars (stop 20) say whether money was made. Neither says why, nor what to try next.
The analyst looks for the why, and proposes; it decides nothing. It sees only this run's data, through tools that log every look, and earlier claims without their flattering numbers. Unfenced, an AI tells a story fitted to what it saw, and the campaign spends runs chasing it.

**What comes in, what goes out.**
- In: the run's bars and trades (stop 14), config and variant edits (stops 10, 15), its verdicts (stops 09, 19, 20), the campaign memory (stop 22).
- Out: one prompt per lens; a log of every tool call.
- Next: the answer and its checks (21b).

run_102's prompts and query logs are not in this checkout. Its later brief (stop 01) cites the forecast lens's query q9: an effect of 0.0308 at 6 hours, 0.0851 at 24.

**What happens here, step by step.**
1. After the backtests, with its switch on, the conductor moves to the analyst. If an indicator errored, no lens runs and the run later pauses for a person; the idea's status file must also be valid.
2. Two lenses run in turn: trade efficiency, then the forecast. A reading already there (a resume) is checked, not redone; an operator re-run on another fold gets a "skipped" reading. The token budget is checked before each.
3. Code builds the whole prompt; the session opens no file. It holds the method, the lens's question, the run context, the catalogue of parts a change may name, the data dictionary (each column's meaning and when it is known), the claim-test vocabularies, the memory view.
4. The run context: fold (a fixed set of test months), coins, bar size, windows, base config, variant edits, cost model, and the run's book: a code-written summary of its results (grid, status, profit bars, fold confirmation; per variant, Sharpe ratio, drawdown, costs, claim-test effects). Nothing is recomputed; a missing file is named missing.
5. The memory view lists earlier claims with kind, fold and status (confirmed, not confirmed, not measurable, pending). Effect numbers appear only for confirmed claims; numbers in statements are masked. Each shows the strategy it came from. The newest 100 measurements with no change attached appear as "observed, no vehicle yet".
6. The session has one AI model and the seven tools; any other tool is denied, and a session reporting one stops the stage.
7. The tools describe columns, measure a conditional effect (the return after bars meeting a condition, against the other bars, per horizon and window, given back as a ready test), slice the lots (matched trades), study entries, and total each window's costs. Each call is logged before its reply, with an id (q1, q2, ...), and counted. The tools read only this run, refuse the sealed holdout, and take as conditions only data known at the bar's close.
8. The method: know the machine first (forecast size, share at the ±20 cap, each variant's costs); find a surprise; name a mechanism; test what it predicts; rule out rivals; end with one claim and its test, or none, plus a four-line next-steps ledger.

**What it costs and how long it takes.**
Per lens (code defaults; the config sets none): 40 turns, 3 USD, 15 minutes, 150 comparisons.
run_102: 7 analyst calls, 6.50 USD, two readings (its audit log, as quoted at stop 05a).
Memory view from the committed record (up to run_097): 25 earlier claims, 3 confirmed, 5 not measurable, 17 pending, no observation rows (read-only script).

**What is switched off or not used here.**
- In this checkout (master) the analyst switch reads off, register state "off, incomplete"; the tour's flag set (stop 03a) has it on.
- The stage's instruction file serves only a check that the backtest result exists; the prompt ignores it.
- Three older reader categories are written by no lens; their names stay so old runs load.
- The config's comment says six query tools; the code has seven.
- A smoke command (one lens on a copy of a run) is off the campaign path.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Stage entry in the registry | `workflow/run_phase1_research.py:221-234` | `analyst`, handoff `protocol_to_analyst.yaml`, no `skill` key |
| Switch | `run_phase1_research.py:4169`; `config/campaign_config.yaml:843-877` | `_analyst_enabled` (needs folds); `enabled`, `model: claude-sonnet-5-5`, caps as comments |
| Route in and out | `run_phase1_research.py:20177-20187` | backtests → analyst → record-keeping or grid route |
| Entry checks | `run_phase1_research.py:19832-19843`, `:19942-19944` | Flag off on resume → failed; handoff written; its required input must exist |
| Handoff | `run_phase1_research.py:4539-4566` | `_ensure_analyst_handoff`, written once at entry |
| Clearing on a backtest re-run | `run_phase1_research.py:4455`, `:4480-4498`, `:1826-1830` | Query logs, records, the two readings |
| Stage | `run_phase1_research.py:5323-5370` | `_run_analyst_stage`: component errors, grid-route checks (`:5379-5386`), resume, refold skip (`:5232`), budget, two lenses |
| Lens categories | `tools/reader_categories.py:23-28` | `ANALYST_LENS_CATEGORIES` (trade_efficiency, forecast_power); three older names kept for loading old runs |
| Worker set-up | `run_phase1_research.py:4885-4923` | Query engine, fold, prompt, settings (config + book figures) |
| Caps | `run_phase1_research.py:4699`, `:4726-4743` | 40 turns, 3 USD, 15 minutes; model |
| Tool schemas and help | `run_phase1_research.py:4746-4791` | Typed arguments only, no path |
| Tool wrappers, deny hook | `run_phase1_research.py:4794-4831` | Seven tools; any other name denied and recorded |
| Session | `run_phase1_research.py:4834-4864`; `:1245-1253` | One session, timeout; closed-book options plus the seven tools |
| Skill | `workflow_artifacts/skills/analyst/SKILL.md` (396 lines) | What you have `:20`, method `:70`, worked examples `:147`, `:165`, vehicle `:191`, answer `:242`, guard rails `:366` |
| Lenses | `skills/analyst/forecast.md` (22), `trade_efficiency.md` (28) | Each lens's question |
| Names, tools | `tools/analyst_session.py:48-59` | Lens → category, seven tool names, record and log folders |
| Prompt | `tools/analyst_session.py:417-435` | `build_prompt`: skill, lens, context, catalogue, dictionary, claim vocabularies, memory view, tools |
| Run context | `tools/analyst_session.py:382-414` | Coins, windows with bar counts, horizon, sizing line, config, patches, book, cost model |
| Run's book | `tools/analyst_session.py:142-379` | `run_book :246`, `book_settings :366` |
| Tool-list check | `tools/analyst_session.py:651-660` | `tool_list_errors` |
| Catalogue | `tools/catalogue_section.py:185` | Components and ops from the catalogue and design guide |
| Dictionary | `docs/DATA_DICTIONARY.md` (696 lines) | How to read `:18`, §1-5 `:79-366`, §7 `:372`, §9 `:437`, §10 `:465`, not recorded `:554`, audit `:584` |
| Memory view | `tools/analyst_memory_view.py` | Docstring `:1-64`, `NOTE :94`, `OBSERVATION_ROWS_MAX :116`, `build_memory_view :405-444`, `load_memory_view :447-474` |
| Query engine | `tools/analyst_queries.py` | Docstring `:1-130`, caps `:146-154`, `QueryLog :356-418`, `QueryEngine :421`, logging `:498-529`, budget `:546-555` |
| Smoke command | `tools/analyst_session.py:1892-1933` | One lens on a copy of a run |

Remarks: send them as "stop 21a: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; the committed `campaign_config.yaml` has `analyst` and `folds` off (`:844`, `:895`). Notes judge the mechanism under the tour's flag set.)

### (1) Design and mechanism

1. The fence is real and layered, and it is the best-fenced AI call in the pipeline: `tools=[]`, `setting_sources=[]`, `strict_mcp_config`, one in-process MCP server with the seven tools, `permission_mode dontAsk`, a `PreToolUse` hook that denies and records any other name (`RP:1225-1256`, `:4818-4831`); the CLI's own init tool list is checked and the stage stops if it names anything else (`:4945-4952`, `analyst_session.py:651-660`); the engine resolves every file inside the run, refuses `local_data`/`holdout_sealed` path parts and any bar at or after the holdout start (`analyst_queries.py:48-72`, `:432-437`), takes typed values from closed vocabularies (no path, no code), and writes every call to the log before returning its result (`:498-531`). For "without fooling ourselves" this is the right shape: what the model saw is on disk before it can cite it.
2. The prompt is everything, pasted: the skill (396 lines) and lens, the run context with the base config, the patches, the code-built book and the whole `config/cost_model.yaml` (`analyst_session.py:403-413`), the catalogue rendered from the two design docs (`catalogue_section.py:185-263`), the whole data dictionary (696 lines, audit findings included, `:427-428`), three claim-vocabulary files (`:429-430`), the memory view with up to 100 observation rows (`:431-432`, `analyst_memory_view.py:117`). That is the ~95-100k cache-creation tokens per lens of stop 00 note 1.7, and the cost (about 1 USD per call) follows. One pasted input is wrong for the live run: `config/cost_model.yaml` is labelled "a measurement of this run" (`:412`), but the fee the backtest charged came from `trading-bot/config/cost_model.json` through the venue block (stop 18 note 1.2, 3.1); the research yaml's `default` figure is the stale 18.5 bps that `post_backtest_cost_check` also prints. The analyst is handed two cost sources and told one is this run's.
3. The memory view's headline status is "confirmed on any fold wins": `_FOLD_STATUS_ORDER = (CONFIRMED, NOT_CONFIRMED, NOT_MEASURABLE)` (`analyst_memory_view.py:119-120`, docstring `:50-57`, operator 2026-10-08), the refutations kept under `folds`. With the noise rule at roughly 11% per fold and no correction for repeated looks (stop 19 note 1.8), a null claim measured on two or three folds has a fair chance of one confirmation, after which the skill tells the analyst "A claim confirmed on this strategy is settled" (`SKILL.md:41`). The data is honest (every fold's status is listed); the one word the skill reasons from is the optimistic one.
4. On the live loop the analyst is the pipeline's only source of new ideas (stop 07 note 1.1: 1a copies; stop 15 note 1.3: step 2 halves a weight), and its ideas are local by construction: a vehicle must resolve against the base config, or be a whole config naming catalogue classes, with any new piece parked in `requires` until a human builds it (`SKILL.md:191-240`); an empty vehicle is refused (`:225-226`). The method (orient, cost, surprise, why, rivals, one claim) is a disciplined local search around the strategy the brief started from. For the goal this means the campaign refines; it does not restart from a different idea unless the operator writes a brief. Consistent with "the operator deciding, the pipeline discovering", and worth saying plainly: discovery here is a neighbourhood.
5. The book (D-203, `run_book :246-363`) gives the analyst the grid, the status, the bars, the fold confirmation and every claim-test effect as code-written text, and `book_settings` (`:366-372`) whitelists those figures so the prose check does not mask them. Sound. It also means the analyst reads the profit-bars verdict before investigating; the skill's guard rail that cost is evidence and never the claim (`SKILL.md:382-387`) is what keeps the reading from becoming "it lost money".
6. Caps are code defaults (`_ANALYST_DEFAULT_CAPS :4699`: 40 turns, 3 USD, 15 min) with the config's keys as comments (stop 03a lead 2.10), plus 150 comparisons per lens (`analyst_queries.py:149`); the run's weighted budget is checked before each lens and before the retry (`:5027-5034`, `:4926`), the second budget of stop 05a note 1.3. A `conditional_effect` by window on six windows and two horizons costs 12, so a lens has about twelve such looks; the mandatory orient steps cost 0. Tight on purpose.
7. Order and preconditions are right: `_grid_route_entry_checks` demands a valid `idea_status.yaml` before any model call (`:5346-5347`), component errors skip both lenses (`:5342-5345`), a present reading is validated not re-run (`:5355-5358`), the refold gets a code-written skip (`:5359-5364`), the clearing at a backtest re-run removes the lenses' files (`:4480-4498`, `:1826-1830`).
8. The `<n>` placeholders that stop 07 note 1.8 and stop 01 note 1.8 found in run_102's claim rationale are this element's doing, by design: D-096 masks every prose number the session did not cite (`SKILL.md:347-349`, `:376-379`) in "everything kept and passed on", and the masked text is what decide-next copies into the child's brief and 1a copies into the card. Not an omission by the model; a code rule whose output reads like one two stops downstream.

### (2) Legacy or simplifiable (leads)

1. The three legacy reader categories: `LEGACY_READER_CATEGORIES` (`reader_categories.py:28`), `REPLACED_RULE` (`analyst_session.py:50`) and `replaced_by_analyst` in `SKIP_RULES` (`reader_proposals.py:115`); the config says they "are code-skipped (rule replaced_by_analyst)" (`campaign_config.yaml:869-870`), but no writer of that rule exists (grep: the constant and comments only) and the stage loops over the two lens categories only (`:5353`), loading all five for old runs (`:5352`, `:5356`). Keep the five names in the loader; delete the rule and the comment.
2. `campaign_config.yaml:865` "six query tools" (seven); the caps as comments (`:874-877`).
3. The audit key prefix `specialist_readers_analyst_` (`RP:4935`; the smoke filter `analyst_session.py:1925`): stop 00 lead 2.10, now located. `_clear_specialist_readers_artifacts` and its two constants (`:4448-4478`) beside `_clear_analyst_artifacts` (`:4480-4498`): two clearers, the first named for the deleted stage and still removing `reports/`.
4. `DATA_DICTIONARY.md` pasted whole (`:427-428`): the `BR` source row for the deleted `build_reports.py` (`:334`), audit findings A10, A11, A15 about `BR` functions, "## 6. (removed)", "## 8. (removed)" and the 2026-10-08 audit narrative (`:584-696`) go into every analyst prompt. The `bars.csv` table is a code contract (parsed by `analyst_queries.py`, `:276`); the rest is history. Trim to the tables and the "Not recorded" list.
5. `config/cost_model.yaml` in the prompt (`:412-413`): 280 lines, of which the `execution_style` and `perp.funding` blocks are unread by any code (stop 18 lead 2.6). Paste the run's manifest `cost_model` block instead (stop 14 note 1.1).
6. The smoke CLI monkeypatches two flag readers in process (`analyst_session.py:1915-1920`): a test harness inside a tool module.

### (3) Disagreements between the speech and the element

1. Step 4, "the cost model" in the run context: it is `config/cost_model.yaml` whole, not the fee this run charged (note 1.2). Omission that matters for the reader of the analyst's cost reasoning.
2. Step 5, the four statuses: correct; the "confirmed on any fold wins" precedence (note 1.3) is not stated.
3. Step 2, "trade efficiency, then the forecast": `ANALYST_LENS_CATEGORIES` order (`reader_categories.py:26`); correct. Step 6 and 7: verified against `:4818-4831`, `analyst_queries.py:1-130`. Step 8: the method's six steps match `SKILL.md:70-145`.
4. "Per lens (code defaults; the config sets none): 40 turns, 3 USD, 15 minutes, 150 comparisons": verified. "25 earlier claims, 3 confirmed, 5 not measurable, 17 pending": not recounted here (it needs the view built); the committed ledger's four fold rows (3 confirmed, 1 `not_comparable`, shown as not measurable) agree with the 3.
5. Section 6, "Three older reader categories are written by no lens": correct, with the addition that the config comment claims a code skip that does not happen (lead 2.1). "The config's comment says six query tools": `:865`; correct. "In this checkout the analyst switch reads off": `:844`; the register's state was not checked beyond its entry (`feature_flag_register.yaml:643`).
6. Reading map verified: `RP:221-234`, `:4169`, `:20177-20187` (stop 05b), `:19832-19843`, `:19940-19946`, `:4539-4566`, `:4455`, `:4480-4498`, `:1826-1830`, `:5323-5370`, `:5379-5386`, `:5232`, `:4885-4923`, `:4699`, `:4726-4743`, `:4746-4791`, `:4794-4831`, `:4834-4864`, `:1245-1253`; `reader_categories.py:23-28`; `analyst_session.py:48-59`, `:142-379`, `:246`, `:366`, `:382-414`, `:417-435`, `:651-660`, `:1892-1933`; `catalogue_section.py:185`; `analyst_memory_view.py:1-64`, `:94`, `:116`, `:405-444`, `:447-474`; `analyst_queries.py:1-130`, `:146-154`, `:356-418`, `:421`, `:498-529`, `:546-555`; `SKILL.md:20`, `:70`, `:147`, `:165`, `:191`, `:242`, `:366`; `DATA_DICTIONARY.md:18`, `:79`, `:372`, `:437`, `:465`, `:554`, `:584`.
