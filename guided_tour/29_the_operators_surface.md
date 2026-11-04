# Stop 29: The operator's surface

## Speech (verbatim)

**Stop 29 of 29: The operator's surface.** Open on the side: `RUNBOOK.md`, `tools/run_viewer/DESIGN.md`, `campaign_summary.md`, `DECISION_LOG.md`, `EPICS.md`, `PROCESS.md`, `SESSION_LOG.md`, `tasks/todo.md`, `tasks/lessons.md`, the root `CLAUDE.md`, `strategy-research/CLAUDE.md`, `.github/workflows/tests.yml`, `run_tests.py`, `DOC_INDEX.md`.

**In one sentence.**
The operator's surface is what a person reads and types to steer the campaign: a manual, a run viewer, a scoreboard, a decision ledger, an engineering roadmap, a session diary, a plan and a lessons list, the house rules, and an automatic test gate.

**Why it exists.**
The pipeline discovers; the operator decides, and needs the facts without reading code.
Without these pages the operator would rule from memory, re-decide what was decided, or launch on a state nobody checked. The house rules say every review opens with the runs read, the PRs (GitHub pull requests) merged and the proven blocks in the registry.

**What comes in, what goes out.**
- The manual: written by hand in build PRs. Read before a launch, at a pause, to resume.
- The run viewer: writes nothing; reads the runs, the queue, the briefs, four records. Read after a run.
- The campaign summary: rewritten by the launcher (the program that runs the queue). Read to see where the campaign stands.
- The decision log: one row per operator decision (a D-number), added in the decision's PR. Read before ruling.
- The roadmap: one line per epic (an E-number, an engineering project), and its rules. Read when choosing what to build.
- The session log, the plan, the lessons: written by the working sessions; the log is read when the next session starts.
- The house rules: two instruction files every session loads.
- The test gate (CI, continuous integration): runs on every push and PR; read in the PR's checks.

**What happens here, step by step.**
1. Before a launch, the operator follows the manual's preflight and a dry run (no AI spend).
2. When a queue line ends or the campaign halts, the summary is rewritten: the queue, lines awaiting approval, closed briefs, claim tests, claims measured on a new fold (a fixed set of test months), open requests, a scoreboard (trials, failed families, findings, runs, spend).
3. On a pause, the manual's pause table names the reason, and its resume section the command: resume, unpark, relaunch, run the analyst again, approve.
4. The run viewer shows the campaign, a run (twelve step cards), a step's raw files, then one variant in one window: price, forecast, position, trades, equity. Dates inside the sealed holdout (months kept back for one final test) are masked; without the data policy it does not start.
5. The review. At a refuted run, the house rules ask for the equity curve and the exposure first. Rulings are batched: one review, one decision set, one build window per run.
6. Each ruling becomes a decision-log row: date, decision, roadmap card, source, where in code, status (built, built but switched off, not built, superseded). A superseded row stays.
7. The build follows the roadmap's rules: one story is one dispatch and one commit; "done" needs the commit and a verification command with its output.
8. Every push runs the test gate on Ubuntu and Windows: a scan for sealed-window dates (Linux only), a check of the bot's sample config, then both test suites without the slow tests.
9. The session closes with a log entry: hypothesis, result, files touched, and the prompt for the next session. A correction adds a lesson: the pattern, then the rule.

**What it costs and how long it takes.**
Test gate: about 8 minutes on Ubuntu, 14 on Windows, capped at 30 (`strategy-research/CLAUDE.md:111`; `tests.yml:17`).
Summary at its last rewrite in this checkout: 55 runs, 74 trials, estimated spend 62.82 USD (26,078,970 weighted token units) (`campaign_summary.md:146-155`).
208 decision rows, newest D-208; 86 session entries; 190 lessons; manual 1,165 lines (counted by grep and wc).

**What is switched off or not used here.**
- Slow tests (live market data) never run in the gate.
- The roadmap index lists 44 epics, up to E-047; the roadmap folder holds 56 epic folders, the latest E-078.
- Some pointers do not resolve in this checkout: the doc index links the manual, the summary and the session log as if beside it; the manual links the doc index as if beside the manual; the manual's scoreboard command names the summary outside its records folder.
- The viewer never reads the step templates of a run or the local data store.
- run_102's own files are not in this checkout.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Manual header | `strategy-research/docs/RUNBOOK.md:1-32` | Pointer to the doc index; shell, working folder, interpreter, `PYTHONUTF8` |
| Commit gates | `RUNBOOK.md:34-64` (§0) | One-time hook wiring |
| Preflight | `RUNBOOK.md:65-127` (§0b) | Checks before any launch |
| Launch | `RUNBOOK.md:128-509` (§1: dry run `:130`, brief contract `:144`, launches `:204-268`, new pipeline `:269`, test period and windows `:470`) | How to start |
| Status | `RUNBOOK.md:510-561` (§2: queue `:518`, log `:529`, scoreboard `:535-544`, run deep-dive `:546`, run viewer `:556-560`) | How to look |
| Splits | `RUNBOOK.md:562-580` (§2a) | One hypothesis per run |
| Pauses | `RUNBOOK.md:581-742` (§3) | The hard-pause table |
| Resume | `RUNBOOK.md:743-1089` (§4: `--unpark :884`, `--relaunch :931`, `retry-analyst :965`, `--approve :1015`, proposals waiting on a feed `:1055`) | How to restart |
| Stop, standing rules, custody | `RUNBOOK.md:1090-1112` (§5), `:1113-1140`, `:1141-1165` | Clean stop; rules the wrapper keeps; briefs installed verbatim |
| Viewer design | `strategy-research/tools/run_viewer/DESIGN.md:7-24` (hard rules), `:26-34` (data model), `:35-45` (URLs), `:46-70` (12 steps), `:174` (sealed dates, option A) | Read-only, four levels, D-180 |
| Viewer server | `tools/run_viewer/server.py:48-50` (banner), `:229-234` (`--runs`, `--root`, `--host` 127.0.0.1, `--port` 8765) | Local web server |
| Viewer loaders | `tools/run_viewer/loaders.py:748` (campaign), `:1620` (run), `:1660` (step), `:1676` (bars), `:1700` (equity); `STEP_NAMES :72` | One loader per view |
| Viewer mask | `tools/run_viewer/sanitize.py:1-20` | Masks sealed-window dates; fails closed |
| Summary writer | `strategy-research/workflow/run_campaign.py:108` (path), `:3062` (`_regenerate_summary`) | Rewritten at done/halt |
| Summary | `strategy-research/campaign_record/campaign_summary.md` (sections `:5`, `:73`, `:79`, `:94`, `:103`, `:111`, `:121`, `:144`) | Queue, approval, closed briefs, claim tests, readers skipped, fold claims, requests, scoreboard |
| Decision log rules | `strategy-research/engineering/DECISION_LOG.md:3-16` | Same-PR rule, chronological numbering, superseded kept, status legend |
| Decision rows | `DECISION_LOG.md:22` (row format), sections `:20-276`; newest D-199..D-208 `:267-276` | 208 rows |
| Decision trailers | `DECISION_LOG.md:280` (no written source), `:287` (conflicts), `:306` (pending) | Gaps and conflicts |
| Roadmap index | `strategy-research/engineering/roadmap/EPICS.md:1-8`, Active `:10`, Done `:48`, legend `:67` | One line per epic |
| Roadmap rules | `roadmap/PROCESS.md:7` (what is an epic), `:22` (states), `:44` (stories are dispatches), `:89` (done means evidence), `:104` (sealed window), `:114` (template) | How engineering work is organised |
| Session log | `SESSION_LOG.md:3` (entry heading); fields 1-4 per entry | Hypothesis, result, files touched, next-session prompt |
| Plan | `tasks/todo.md:1-3` (current plan header), `:41`, `:115`, `:135`, `:147` | The lead's working plan |
| Lessons | `tasks/lessons.md:1` ("appended after user corrections"); entries from `:3` | Pattern and rule per lesson |
| Other task files | `tasks/d052_inventory.md`, `tasks/o3_inventory.md` | Inventories (not opened for this stop) |
| House rules | `CLAUDE.md:26-30` (hard rules), `:32-40` (working rules) | Secrets, lookahead, trial ledger, holdout; review cadence |
| Test rules | `strategy-research/CLAUDE.md:107-115`; runtime records `:117-120` | Touched files while developing; CI fast suite; slow on purpose |
| CI | `.github/workflows/tests.yml:1-2` (push, PR), `:10-17` (two OS, 30 min), `:58-60` (seal gate), `:61-63` (sample config), `:96-97` (both suites) | The test gate |
| Runner | `run_tests.py:1-60` (why), `:94-95` (markers), `:107` (`main`) | Both suites, each from its own folder |
| Doc index | `strategy-research/DOC_INDEX.md:1-11` (rules), `:13`, `:41`, `:92`, `:299-300` | One line per doc, by question |

Remarks: send them as "stop 29: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

(Checkout note: the committed `campaign_summary.md` is the operator's working-tree summary as of run_097's end; `SESSION_LOG.md`, `tasks/` and the decision log are committed and were read at their heads and tails.)

### (1) Design and mechanism

1. This surface is where the pipeline's missing feedback loops close, by hand. The loop records but does not learn why (stop 22a note 2), does not grade its claims against their own predictions (stop 09 note 1.2), does not propagate a voided validation (stop 22a note 3), cannot choose a second candidate (stop 24a note 5), and stops at every pause (stop 23 note 2). The working rules in the root `CLAUDE.md:32-40` are the operator's answer: read every run, open with runs read and blocks in the registry, rule once per run, strategist first. The surface is sized for that: a 1,165-line manual, a 66-row pause table, a 217-row decision log, an 86-entry session log. It works because one person reads all of it; it is the opposite of "run autonomously".
2. The one spend figure the operator sees is wrong by the analyst's cost: "Estimated spend: $62.82 (26,078,970 weighted token units)" for 55 runs (`campaign_summary.md:155`) is weighted units at a fixed rate, about 1.14 USD a run; run_102 alone metered 8.25 USD, 79% of it the analyst (stop 00 note 1.6, stop 05a). The scoreboard's trial routes are retired labels (`kill_no_ic`, `no_signal_artifact`, `proceed_to_backtest`, `refine_inverted_ic`, `:147-151`) beside `recorded: 62`, and "Distinct failed hypothesis families: 9" reads the retired list. The page the operator opens "to see where the campaign stands" stands in two eras.
3. The decision log is the campaign's real memory of why, and its status column drifts: D-015 ("a variant whose backtest fails can never contribute to a VALIDATED idea") is marked `not built` (`DECISION_LOG.md:30`) while the grid implements it (`vce:2286-2288`, `failed_variants`, E-061 C2 S2a, stop 19 note 1.1). The rule "same PR" (`:5-8`) covers the row's creation, not its status after a later PR. A reader "ruling before reading the log" can rule on a stale status.
4. The run viewer is the best-built operator tool: read-only by test, an allow-list of paths, no templates and no `local_data/`, ids checked against disk, loopback by default, every string through the mask (`DESIGN.md:7-24`, `server.py:48-50`, `:229-234`, `sanitize.py`). It shows the files; it does not compute. Right for D-180.
5. The test gate is partly a documentation gate: `test_feature_flag_register.py`, `test_campaign_config_sync.py`, `test_guide_covers_the_code.py`, `test_design_guide_in_sync.py` (stops 03b, 00, 11) pin prose to code, and CI runs both suites on two systems in about 8 and 14 minutes (`tests.yml:10-17`, `:96-97`; `SR/CLAUDE.md:111`). Slow tests never run in CI (`run_tests.py:94-95`), so the data-fetching paths are tested only by hand. Sound as a gate; its coverage of the market-data side is the operator's.
6. The manual documents both pipelines: §3's 66 rows against about fifteen live reasons (stop 23 note 3), §1's launch section for the new pipeline beside the old (`:128-509`), §4's resets for every pause shape. The pointer graph is broken in places the speech lists (the doc index's `RUNBOOK.md`, `SESSION_LOG.md`, `campaign_summary.md` links; the manual's `DOC_INDEX.md` link resolves to `docs/DOC_INDEX.md`, which does not exist; verified by `ls`). A new joiner who starts where `SR/CLAUDE.md:3` says to start follows dead links on the first page.
7. The session log is a disciplined handover (hypothesis, result, files, next prompt; `SESSION_LOG.md:3-12`) and the lessons file is the one place the operator's corrections become rules (`tasks/lessons.md:1-6`: "Don't propose a control that already exists as a step"). Both are read by the next session, not by the pipeline; the pipeline's own lessons file is the KB, which the live writer fills with one word per run (stop 22b note 5).

### (2) Legacy or simplifiable (leads)

1. `campaign_summary.md`'s scoreboard (`RC:3062-3070`: `trial_sharpes[*].route` counts, `failed_families`, `knowledge-base findings`) and its "Readers skipped by a code rule" section (`:103`): retired labels and a deleted stage in the operator's first page. The spend line's rate (note 2) should be the SDK's metered cost from the audit logs, or dropped.
2. `DOC_INDEX.md` (313 lines; stop 00 lead 2.5): broken relative links, "Where do things stand right now?" pointing at a July improvements file (`:92-93`); the operator's stop-00 remark (delete or maintain) stands, with the eight live pointers to re-point.
3. `RUNBOOK.md` §3 retired rows (`:675`, `:699`, and the reasons stop 23 note 3 lists), §2's `cat campaign_summary.md` path (the file is under `campaign_record/`), §1's flag-off launch text.
4. `DECISION_LOG.md` status column (note 3): a status audit against the code, or drop the column and keep the where-in-code pointer.
5. `engineering/roadmap/EPICS.md` versus the folder (the speech: 44 listed, 56 folders, latest E-078): not re-counted here; if right, the "only mandatory read for an agent starting cold" (`:3-4`) is twelve epics behind.
6. `tasks/todo.md` opens on a plan marked done 2026-10-20 (`:1-3`); a plan file whose header is history.
7. `SR/CLAUDE.md` (stop 00 leads 2.1-2.4, 2.11): the operator's proposed three-part split.

### (3) Disagreements between the speech and the element

1. Section 5, "208 decision rows, newest D-208": the numbering reaches D-208 (`:267-276`); the table has 217 rows beginning `| D-` (some decisions carry more than one row, or the conflicts and pending sections add rows). Counting method; the newest number is right.
2. Section 5, "86 session entries": verified (86 `## ` headings). "190 lessons": not recounted (my coarse count does not isolate lessons). "manual 1,165 lines": consistent with §5 at `:1090` and the custody rule at `:1141-1165`.
3. Section 5, "Summary ... 55 runs, 74 trials, estimated spend 62.82 USD": `:146-155`; verified. Not stated: the figure is an estimate at a fixed rate that undercounts the analyst era (note 2), and the route labels are retired words.
4. Section 5, "Test gate: about 8 minutes on Ubuntu, 14 on Windows, capped at 30": `SR/CLAUDE.md:111`, `tests.yml:17`; verified.
5. Section 6, the broken pointers: verified by `ls` (`strategy-research/RUNBOOK.md`, `campaign_summary.md`, `SESSION_LOG.md`, `docs/DOC_INDEX.md` all absent). "The roadmap index lists 44 epics ... 56 folders": not verified here.
6. Step 6, "Each ruling becomes a decision-log row ... status (built, built but switched off, not built, superseded)": the legend `:14-16`; verified; the drift of note 3 is not stated.
7. Reading map verified: `RUNBOOK.md:1-32`, `:510-561` (headings), `:1090-1112`, `:1113-1140`, `:1141-1165` (headings), §3 and §4 at stop 23; `DESIGN.md:7-24`, `:26-34`, `:35-45`, `:174`; `server.py:48-50`, `:229-234`; `loaders.py:72`, `:748`, `:1620`, `:1660`, `:1676`, `:1700`; `sanitize.py:1-20`; `RC:3062`; `campaign_summary.md` sections `:5`, `:73`, `:79`, `:94`, `:103`, `:111`, `:121`, `:144`; `DECISION_LOG.md:3-16`, `:22`, `:267-276`, `:280`, `:287`, `:306`; `EPICS.md:1-8`; `SESSION_LOG.md:3`; `tasks/todo.md:1-3`; `tasks/lessons.md:1-6`; `CLAUDE.md:26-30`, `:32-40`; `SR/CLAUDE.md:107-120` (stop 00); `tests.yml:1-20`, `:48-63`, `:94-98`; `run_tests.py:1-20`, `:94-110`; `DOC_INDEX.md:1-15`, `:41`, `:92-93`, `:299-300`. Not opened: `DESIGN.md:46-70`, `RC:108`, `PROCESS.md` sections, `EPICS.md:10`, `:48`, `:67`, the two inventory task files, `tasks/todo.md:41-147`.
