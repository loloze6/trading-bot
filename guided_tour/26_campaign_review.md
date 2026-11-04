# Stop 26: The campaign review (stage 12)

## Speech (verbatim)

**Stop 26 of 29: The campaign review (stage 12).** Open on the side: `workflow_artifacts/skills/campaign-review/SKILL.md`, `workflow_artifacts/skills/campaign-review/RETIRED_ROUTING.md`, `tools/campaign_review_retired.py`, `campaign_record/campaign_review_log.yaml`, `run_phase1_research.py`, `run_campaign.py`.

**In one sentence.**
The campaign review is a periodic step back: after every six recorded runs, one AI call reads a summary of the recent runs and says whether to carry on, change the research question, or stop the campaign.

**Why it exists.**
Each run judges one idea; nothing inside a run looks at the series. Without a step back, the campaign could keep testing variations that all fail for the same reason.
The review is the one place that looks across runs. It never changes an idea's result: that stays with the grid (the pre-registered pass/fail table). It never picks the next run: that stays with decide-next (the code that proposes the next run at the end of each run).

**What comes in, what goes out.**
- In: a digest of the campaign memory (the per-run record), written by code; the run's brief and pre-registration; the knowledge base (tested mechanisms and bans) when it exists; the skill, its note for the current routing, and the quant basics rulebook.
- Out: the review file with one of five recommendations; a line in the review log; for "reframe", a new candidate brief; for "terminate", an event in the campaign decision file and a stop; for "escalate component", a line in the component requests list.

**What happens here, step by step.**
1. At the end of a run, after the profit-bars stop (the pause when a variant beat every campaign-wide profit bar) and after the grid has ended the run, code counts the recorded runs no completed review has covered yet. Broken runs (an engineering fault) do not count.
2. Fewer than six: no review, the run ends. Six or more: the run passes through the review first. The six is read from the campaign state file.
3. Code writes the digest: every uncovered run in full, counts for the earlier ones, the last completed review. It writes the call's instructions and marks the run "review triggered". A review reached without that mark pauses before any spend.
4. One AI call, on the default model, with no tools: it sees only what is pasted into its prompt. It writes the pattern it sees, the evidence, a recommendation, a rationale, and answers to three knowledge-base questions (untested cells, banned cells, combinations worth trying).
5. What each recommendation does. Continue, escalate instrument: recorded only. Escalate component: the rationale goes to the component requests list. Reframe: the new question becomes a brief in the candidate briefs folder; code adds that criteria are chosen fresh at step 1a and pins the source run's test protocol; a reframe that reopens a closed knowledge-base finding pauses instead. Terminate: an event goes into the campaign decision file and the run pauses; if the operator resumes anyway, an "override, continue" event is added.
6. Only then is the review logged as completed, with the runs it covered. A review that never completed (budget stop, crash) is due again next run.
7. The run still ends with the grid's status. At the end-of-run step, the launcher registers a reframe brief in the queue, held for approval like decide-next's candidates when approval mode is on.

Example: run_102's review handoff is not in this checkout. The committed review log (up to run_097) holds three completed reviews, at run_074, run_083 and run_094, all "continue", covering 6, 6 and 9 runs. In the committed memory (24 runs), run_095 to run_097 are counted and not yet covered.

**What is switched off or not used here.**
- This checkout's switchboard file (master) has the switches this stop relies on set off; the speech follows the tour's flag set (stop 03), where they are on.
- The older trigger (two failed families, or a run count that is a multiple of six) and the older route after a review are not reached under the current flags, skipped at RP:16296.
- The cadence default in the switchboard has no reader in the workflow (stop 03); the cadence comes from the campaign state file.
- The note tells the model not to use the skill's diagnostics log, failed families or old terminate guard.
- No reframe brief and no campaign decision file exist in this checkout.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Skill | `workflow_artifacts/skills/campaign-review/SKILL.md:1-245` | Mission, inputs, output fields (`:23-39`), four patterns (`:47-72`), feed-wishlist gate (`:74-119`), KB reactivation gate (`:121-155`), fragment-pattern ideation (`:157-196`), checklist (`:198-210`), forbidden (`:212-236`), context rule (`:238-245`) |
| Note under retired routing | `workflow_artifacts/skills/campaign-review/RETIRED_ROUTING.md:1-60` | When it is added (`:3-8`), what changed (`:10-28`), effect table (`:30-38`), reframe rules (`:40-52`), terminate rules (`:54-60`) |
| Registry and skill | `run_phase1_research.py:246-250`, `:1026` | `campaign_review` entry; skill `campaign-review` |
| Extra inputs | `run_phase1_research.py:3092-3096` with `:3116-3133` (pre-registration, brief verbatim); `:3213` (quant-fundamentals); `:8995-9030` (memory file, skipped when the trigger mark is set), called `:9715` | Inputs added at call time |
| Design comment, constants | `run_phase1_research.py:7694-7741` | Cadence, outcomes; state keys, origin, digest file name |
| Cadence | `run_phase1_research.py:7751-7756` | `review_every_n_runs` from `campaign_state.yaml` |
| Trigger | `run_phase1_research.py:7759-7778` | Runs since the last completed review |
| Digest | `run_phase1_research.py:7781-7812` | `artifacts/campaign_review_digest.yaml` |
| Handoff | `run_phase1_research.py:7815-7864` | Written in full under the flag (KB optional) |
| Route into the review | `run_phase1_research.py:7867-7882`, called `:20611` | Marks `campaign_review_trigger` |
| Note added at call | `run_phase1_research.py:7891-7907`, called `:9719` | `RETIRED_ROUTING.md` as a required input |
| Guards | `run_phase1_research.py:19911-19937` | Flag off with a mark: fail; flag on without a mark: pause |
| Skip and parse check | `run_phase1_research.py:20002-20013`, `:20140-20151` | Valid file not re-run; YAML parse error stops |
| Route after the review | `run_phase1_research.py:20613-20621` → `:16292-16297` → `:8065-8119` | The five recommendations |
| Grid status kept | `run_phase1_research.py:7910-7916` | `completed_<idea_status>` re-read |
| Escalate component | `run_phase1_research.py:7919-7928` | Row in `component_requests.yaml` |
| Reframe brief | `run_phase1_research.py:7931-8001`; KB check `:8096-8107` → `:11441` | `candidate_briefs/<run_id>__reframe.md`, protocol pin, refusals |
| Terminate | `run_phase1_research.py:8004-8048` | Decision event, pause, override on resume |
| Completion | `run_phase1_research.py:8051-8062` | Review log entry |
| Shared module | `tools/campaign_review_retired.py:29-38`, `:71-123`, `:130-175`, `:182-205` | Required brief keys and file names; requests appender; cadence and review log; decision file |
| Review log | `campaign_record/campaign_review_log.yaml:1-38` | 3 completed reviews (committed copy, up to run_097) |
| Cadence value | `campaign_record/campaign_state.yaml:641` | `review_every_n_runs: 6` |
| Reframe registration | `run_campaign.py:4812-4831`, `:5552-5577`, `:5580-5612`; halt `:134`, resume check `:321-323` | Queue entry, origin `campaign_review`, status from approval mode |
| Stop classification | `run_campaign.py:1541-1542`, `:1732-1739`; wishlist check `:1741-1765` → `:1458-1487` | `campaign_review_terminate`; budget stop of a pending review |
| Older path | `run_phase1_research.py:12977-12998`, `:16275-16284` (in `determine_post_verdict_route`), `:16298-16459` | Not reached under the current flags |
| Template | `workflow_artifacts/templates/handoffs/campaign_review.yaml` (40 lines) | Older handoff; replaced in full under the flag |
| Operator rows | `docs/RUNBOOK.md:731`, `:732` | Refusal and terminate rows |

Remarks: send them as "stop 26: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; the committed review log (3 reviews) and memory (24 entries) were read; `verdict_routing_retired` is off in the committed switchboard. Notes judge the mechanism under the tour's flag set.)

### (1) Design and mechanism

1. The cadence is built right: a review is due when at least `review_every_n_runs` memory runs without a fault are not covered by a completed review; only completion resets the count, so a missed review carries forward and none fires twice (`campaign_review_retired.py:137-158`, `RP:7759-7778`, `_complete_retired_review :8051-8062`). The digest is code-written from the memory (`:7789-7812`), the retired-routing note wins over the skill (`RETIRED_ROUTING.md:7-8`), the grid status is re-read and never changed (`_review_idea_terminal :7911-7916`), `continue` and `escalate_*` are recorded only, `reframe` becomes a held brief with criteria at 1a and the source run's protocol pin (`:7931-8001`), `terminate` is a real stop with a recorded override on resume (`:8004-8048`). Every branch ends in a known state. Sound.
2. What the review has done in 21 runs: three reviews, all `continue`, covering 6, 6 and 9 runs (`campaign_review_log.yaml:1-38`). Its mission is to detect "multiple hypothesis families failing for the same root cause" (`SKILL.md:10-13`), and what it is given is the memory's one word per run with grid counts (`_write_review_digest :7795-7805`; stop 22a note 2): no reason beyond the evaluator's constant sentence, no claim results, no analyst prose. The skill's checklist asks for trends in `forecast_return_corr` and `cost_drag_pct` across runs (`:204-207`) that the digest does not carry (the grid cells hold the IC values, nothing holds cost drag). A reviewer asked to find a pattern in a list of `refuted` cannot; `continue` three times is the honest answer to that input.
3. The one AI step whose job is to step back runs on the default model (Haiku; `campaign_review` is not in `stage_models`, stop 03a) while 1a and 1b run on Sonnet. A fact for the operator's model table.
4. The review's only lever that could redirect the campaign without a person, `reframe`, writes a brief that is then held for approval (`RC:5580-5612`, `_approval_status`), pinned to the triggering run's protocol (`_source_protocol_pin :7931-7945`: the same fold as the run that asked for a change of question) with criteria chosen at 1a (the constant judge, stop 08 note 1.4). So under the live flags the review can propose, and the operator approves; `terminate` stops the campaign until the operator overrides. The autonomy valve is closed here too (stop 24a note 2).
5. The skill text and the note contradict each other where the note does not override: the skill requires `campaign_state.yaml` (`:15-17`) and says "Read campaign_state.yaml and research_brief.yaml only" (`:238-245`), the note forbids reasoning from it (`:20-27`); the skill's terminate guard (`:213-215`) is replaced (`:54-60`); the skill asks for `budget_assessment` against a `campaign_budget` (`:38-39`) that no file carries. A model reconciles by the "this note wins" sentence; a reader learns the flag-off review.
6. The guards are complete: a trigger-marked run with the flag off fails loudly, an unmarked run with the flag on pauses before any spend (`RP:19911-19937`); a present valid review file is not re-run; a YAML parse error stops (map rows). The reframe registration checks the flag, the file and id collisions before writing (`RC:5552-5577`).

### (2) Legacy or simplifiable (leads)

1. `SKILL.md`'s flag-off content: required inputs (`:15-17`), the `diagnostics_log` and family checklist (`:198-210`), the escalation-era terminate guard and the verdict-interpreter sentence (`:212-236`), the context rule (`:238-245`), `fragment_patterns.yaml` ideation (`:157-196`), `budget_assessment`. With the flag folded, the note's content is the skill.
2. `templates/handoffs/campaign_review.yaml` (40 lines): replaced in full under the flag (`:7815-7864`); copied into every run by `setup_run.py`.
3. The older trigger and route: `_should_trigger_campaign_review` (`:12977`), `determine_post_campaign_review_route`'s body after its first line (`:16298-16459`), `_route_campaign_terminate` (`:12029`), the wishlist pause (`RC:1741-1765`, `:1458-1487`), `campaign_decision.yaml`'s `legacy_decision` wrapper (`campaign_review_retired.py:189-191`).
4. `review_every_n_runs_default` in the switchboard (dead key, stop 03a lead 2.1) beside the live `campaign_state.yaml:641`.
5. The digest pastes every uncovered memory entry in full (about 280 lines each, stop 22a note 7): a review over nine runs reads about 2,500 lines of YAML to produce five words.

### (3) Disagreements between the speech and the element

1. Step 4, "It writes the pattern it sees, the evidence, a recommendation, a rationale, and answers to three knowledge-base questions": the output fields (`SKILL.md:23-39`) match; the KB questions are the skill's gate section (`:121-155`), not re-read in detail here.
2. Step 5, every effect: verified against `_route_retired_campaign_review :8065-8119` (`continue`/`escalate_*` `:8080-8087`, `reframe` `:8088-8110` with the KB refusal `:8096-8107`, `terminate` `:8111-8115`).
3. Step 1-2 and 6: verified (`:7759-7778`, `:7751-7756`, `:8051-8062`). Step 7: verified (`RC:4812-4831`, `:5580-5612`).
4. Example: three completed reviews at run_074, run_083, run_094, all `continue`, covering 6, 6, 9 (log `:3-38`); 24 memory entries minus 21 covered leaves 3 uncovered (run_095 to run_097): verified.
5. Section 6, "skipped at RP:16296": `:16296-16297`; verified. "The cadence default in the switchboard has no reader": stop 03a; verified.
6. Section 3's "In" list says "the knowledge base (tested mechanisms and bans) when it exists": the KB's `exhausted_mechanisms` is empty by construction (stop 22b note 4), so the "bans" the review is asked to respect (`SKILL.md:227-232`) are none. Omission.
7. Reading map verified: `SKILL.md:1-45`, `:198-245`; `RETIRED_ROUTING.md` whole; `campaign_review_retired.py:29-38`, `:71-80`, `:130-205`; `RP:7694-7741`, `:7751-7756`, `:7759-7778`, `:7781-7812`, `:7826-7850`, `:7867-7882`, `:7891-7935`, `:7936-8001`, `:8004-8062`, `:8065-8119`, `:19911-19937`, `:20613-20624`, `:16290-16297`; `RC:5552-5612`, `:4812-4831`; `RUNBOOK.md:731-732`; `campaign_review_log.yaml`; `campaign_state.yaml:641`. Not opened: `RP:246-250`, `:1026`, `:3092-3133`, `:3213`, `:9715`, `:9719`, `:20002-20013`, `:20140-20151`, `:12977-12998`, `:16275-16284`, `:16298-16459`; `RC:134`, `:321-323`, `:1541-1542`, `:1732-1739`, `:1458-1487`; the template file.
