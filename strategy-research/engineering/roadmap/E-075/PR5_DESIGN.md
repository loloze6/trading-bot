# E-075 PR-5: the analyst's wiring and skill (both lenses), design for the operator's nod

**Ticket:** CUL-423 (E-075, P-CUL-83). **Status:** design only, nothing built.
**Plan:** `delivery_plan_readers.md` A1.11 items 5-6, Steps 9-11.
**Done-when:** `ITERATIVE_PLAN_JUDGEMENT.md` section 4 (PR-5), as the session brief of 2026-10-08 restates it.
**Builds on:**
- #355, the six tools and the memory view;
- #356 (D-090), post-merge fixes;
- #357 (D-089), the empty vehicle and the several-coin pooling;
- #354, `confirm_on_fold`.

## 0. In one paragraph

- When `orchestrator.analyst.enabled` is on, the reader stage stops calling today's five readers.
- It runs **two analyst sessions instead**, one per lens: forecast, then trade efficiency.
- Each session is one Claude call that may use **only the six query tools** (`tools/analyst_queries.py`), on this run's own bars and trades, with every call logged.
- The analyst ends with one strategy claim, or "no claim".
- Code turns its answer into an ordinary **v3 reading file** (`artifacts/proposals/<category>.yaml`), so decide-next reads it as it reads a reader's side finding today.
- Before the file is written, code checks the answer:
  - the claim (`check_claim(trade_tests=True, folds=True)`);
  - every citation against the query log;
  - the vehicle;
  - that the claim's test and the "why" query were really run;
  - that no sealed date appears.
- One retry with the error. A second failure is a code-written "skipped" reading.
- Flag off: nothing changes, byte for byte.

## 1. A gap that blocks the trade-efficiency lens (decision 1)

**What I found while preparing this design.** A trade-level claim (selector `trade`, D-086) is accepted only where a caller passes `trade_tests=True`. Today **no pipeline caller passes it**.

So a trade claim written by the analyst would be:

| # | Where | What happens | Code site |
|---|---|---|---|
| 1 | Decide-next | refused (`next_test_refused`) | `reader_findings.side_finding_review` calls `check_claim` without `trade_tests` |
| 2 | Step 1a of the child | refused, so the child's card cannot carry it | the card check `check_claim(..., **_claim_check_folds())`, `run_phase1_research.py` ~16785, 16925, 17442, 17828 |
| 3 | The child's own claim measurement | not measured | `claim_measure.measure_variant` without `trade_tests` |
| 4 | Fold confirmation | `not_measurable` | `fold_confirm.confirm_on_fold`: `check_claim(folds=True)` without `trade_tests`, and `explore_confirm.measure_on_windows` calls `measure_test` without it |

The trade-efficiency lens exists to make exactly these claims. Without this, its claims can never be confirmed.

**Proposal:**
- Pass `trade_tests=True` at these four places, under `orchestrator.analyst.enabled` only, through one helper next to `_claim_check_folds`.
- At site 4, the measurement loads the variant's trade windows for a trade test (`ct.load_variant_trade_windows`). `pooled_per_window` (D-089) already works on trade windows.

**Recommendation: a separate small PR ("PR-5a") before PR-5.** It is a different change (the trade family reaching the pipeline), it is testable without any SDK, and it keeps PR-5 to the wiring and the skill. The alternative is to include it in PR-5, which makes PR-5 larger.

## 2. Where the analyst sits

**In the run:** in the `specialist_readers` stage (`_run_specialist_readers`). It still runs after `protocol_execution`. Everything after it is unchanged:
- the regroup record;
- side-finding merges;
- the confirmation ledger;
- decide-next.

**Categories (decision 2).** decide-next and every loader expect one file per reader category: `profitability`, `forecast_power`, `regime_power`, `component_attribution`, `trade_efficiency` (`load_proposals` raises if one is missing). So:

| Category | Written by, under the flag |
|---|---|
| `forecast_power.yaml` | the **forecast** lens |
| `trade_efficiency.yaml` | the **trade-efficiency** lens |
| `profitability.yaml`, `regime_power.yaml`, `component_attribution.yaml` | code, as a `skipped` reading with a new rule `replaced_by_analyst` (no model call) |

- Nothing that reads proposals changes.
- Adding a lens later is one more mapping line plus its lens text.

**Flag dependencies (refused at pre-flight, before any spend):** `orchestrator.analyst.enabled` needs all three of:
- `specialist_readers` (the stage);
- `reader_findings` (the v3 reading shape);
- `folds`, because every claim is confirmed on a fold, and without `folds` the envelope (`vehicle`, `combines_as`, `fold_observed`) is refused from a model.

**Today's readers under `folds` (unchanged):** they still produce no side findings (D-087). Under `analyst` they are not called at all.

## 3. One session

**Model and caps (decision 5)** (config keys under `orchestrator.analyst`, defaults shown):

| Setting | Value |
|---|---|
| Model | `claude-sonnet-5-5` |
| `max_turns` | 40 |
| `max_budget_usd` | 1.50 per session |
| Wall-clock timeout | 15 minutes |

The run's existing weighted token budget is checked before each session, as for readers.

**Options:** one construction site, `_stage_agent_options(*, analyst=None)` (PHASE_A 1.3). With `analyst=None` it returns exactly today's object. With an analyst spec it adds, on the same closed-book base:
- `tools=[]`, so no built-in tool exists;
- `setting_sources=[]`;
- `strict_mcp_config=True`;
- `mcp_servers={"analyst": create_sdk_mcp_server(...)}` and nothing else;
- `allowed_tools` = exactly the six names;
- `permission_mode="dontAsk"`;
- a `PreToolUse` hook that denies any other tool name and logs the attempt;
- `max_turns` and `max_budget_usd`;
- the neutral cwd, and auto-memory off.

**The six tools:** thin `@tool` wrappers in `run_phase1_research.py` (still the only SDK importer) call one `QueryEngine` on this run's directory.
- Each wrapper takes typed parameters only.
- It returns the engine's dict as JSON text.
- A refusal is returned as a normal result with its reason, never as an exception.

**The query log (decision 4):**
- one log per lens: `artifacts/analyst_queries/<lens>.yaml`;
- each lens gets its own 150-comparison budget;
- query ids are `q1, q2, ...` per lens;
- the run's total looks = the sum of the two logs.

The alternative is one shared `artifacts/analyst_queries.yaml` with 150 for both lenses together: the forecast lens, which runs first, could then spend the trade lens's budget.

**A retry** is a second session with the same prompt, the refusal text appended, and the same log, so ids and the budget continue.

**What the session receives (its prompt):**
- the skill (section 5) and its lens text;
- **the run context**, from files code reads:
  - the base strategy config and each variant's patch;
  - coins, venue, timeframe;
  - the fold label and its windows;
  - the cost model (fee and slippage per side, for reference only: the skill says no cost judgement);
- **the data dictionary** (bars and trades tables, `docs/DATA_DICTIONARY.md`);
- **the claim-test vocabulary:** `CLAIM_TESTS.md`, `CLAIM_TESTS_TRADE.md`, `CLAIM_TESTS_EXECUTION.md`;
- **the memory view** (`analyst_memory_view.load_memory_view(ROOT)`, rendered as YAML): earlier claims with status and fold, numbers only for confirmed ones;
- **the comparison costs** (D-090): grouping by hour, weekday or regime costs one comparison per group.

**Not given** (ANALYST_SKILL_REVIEW_1 3.2):
- the grid verdict text;
- the five category reports' prose;
- reader explanations;
- the claim digest's exploratory numbers.

The grid's numbers are reachable through the tools if the analyst asks.

## 4. What the model writes, and what code makes of it

**The model writes exactly one fenced YAML block:**

```yaml
outcome: claim            # or: no_claim
claim:                    # the claim block of CLAIM_TESTS.md, checked by check_claim
  statement: ...
  kind: execution_behaviour   # or any CLAIM_KINDS kind
  tests: [ ... ]          # 1..3 tests in the slots (bar or trade family)
  pass_if: ...
  fail_if: ...            # the falsifier, in words
  rationale: ...          # the why: market or mechanical
why_query: q9             # the second query the mechanism predicted
evidence:                 # citations: query id, a path in that result, the value
  - q7:horizons.24.effect=0.0012
  - q9:groups.long.trade_net_return_mean=-0.0008
vehicle: []               # [] only for execution_behaviour; else [{component_id, field, before, after}]
combines_as: execution_rule
# for no_claim instead of claim/why_query/vehicle/combines_as:
no_claim:
  reason: ...
  best_rejected: {statement: ..., killed_by: q12}
```

**Code turns it into the v3 reading `artifacts/proposals/<category>.yaml`:**
- `reading_id` = `<category>-<run_id>`;
- `model_id`: what the SDK reported;
- `rubric_version` = `<category>-analyst-v1` (decision 3: added beside the readers' `-reading-v1` in the accepted set);
- `explanation`: the rationale, or the no-claim reason;
- `evidence`: the citations;
- `side_findings`: one item, or `[]` for no claim. The item holds `proposal_id <category>-<run_id>-1`, the claim, the citations as its evidence, the scores, `vehicle`, `combines_as`, and **`fold_observed` written by code** (the run's own fold).

**The scores (decision 3):**
- the reading shape requires `confidence_real`, `distance_to_profitable` and `mechanism_plausibility`;
- the skill forbids any profit or cost judgement, so **code writes fixed neutral scores** (1, 1, 1) and records `scores: code_neutral` in the audit entry;
- decide-next then ranks the analyst candidates by its existing tie-breaks (cost in backtests, then id);
- Stage 2 replaces this with a code-computed effect ranking.

**Beside the reading, code writes `artifacts/analyst/<lens>.yaml`**, the full record:
- the model's answer;
- `why_query`;
- the no-claim block;
- what was examined (the `spec_hash` of every `conditional_effect` in the log);
- looks (calls, comparisons);
- cost, turns, the result subtype (`error_max_turns`, `error_max_budget_usd` recorded);
- every tool name the hook saw.

## 5. The validation (before the reading file is written)

1. **Shape:** exactly one YAML block, with `outcome` and the fields of section 4.
2. **The claim:** `check_claim(claim, trade_tests=True, folds=True)`.
3. **The envelope:** `reader_proposals.check_reading(..., from_model=True, envelope=True)`, which includes D-089's empty-vehicle rule. The vehicle must resolve against this run's base config (`resolve_patch`, never under a scaffolding path): the existing `_reading_content_errors`.
4. **Citations:** each `q<n>:<path>=<value>`:
   - names a query id of **this lens's log** with status `ok`;
   - the dotted path exists in that logged result;
   - the value equals the logged value (numbers compared at the logged 8 significant digits).

   This is the E-073 step-2 rule (D-083), applied to the log.
5. **The test was really run:** every test of the claim has a `spec_hash` equal to that of a logged `conditional_effect` result (its `spec_hash` field).
6. **The why was really asked:** `why_query` is an `ok` entry of the log, other than the claim's own test query.
7. **No sealed date:** the answer text is scanned with the seal-date regex (`trading-bot/tests/test_no_sealed_date_literals.py`'s pattern, `(?<!\d)\d{4}-\d{2}-\d{2}`, plus month forms), refusing any date at or after the holdout start read from the data policy. The literal holdout start is never written in code.
8. **For no claim:** a reason, and a `best_rejected` whose `killed_by` is a logged query.

A failure gets one retry with the messages. A second failure gives a code-written `skipped` reading (rule `output_refused_after_retry`, already in `SKIP_RULES`), and the record keeps both answers.

## 6. The skill (both lenses)

`workflow_artifacts/skills/analyst/SKILL.md` (shared), plus `analyst/forecast.md` and `analyst/trade_efficiency.md` (one lens text each). The text comes from ANALYST_SKILL_REVIEW_1 section 3 (v3), simplified by Steps 10-11:

1. **Objective (first line):**
   > "You observe one finished backtest on one fold. With your fixed tools you dig into its bars and trades, ask why, and end with ONE strategy claim or no claim. A claim says how this strategy behaves in the market, or how a change to it would behave, and comes with the test a later backtest on a fold you have not seen must pass or fail. You are not asked to improve this strategy or to find profit. Confirmed and refuted claims are the knowledge the campaign builds strategies from."
2. **Method:**
   - orient (`list_columns`, `describe`, `trade_slice` by exit cause);
   - find the surprise (a conditional difference, not a level);
   - ask why, and run the second query the mechanism predicts;
   - rule out rivals (one window, one coin, a data gap, the strategy's own mechanics);
   - write the claim with its test, or stop with no claim.
3. **Market observations stay in your reasoning** (Step 11). The output is a strategy claim with its vehicle:
   - a config change that exploits the observation; or
   - `vehicle: []` for an `execution_behaviour` claim about today's strategy as it is (D-089).
4. **Claim fields:** statement, kind, tests in the slots (bar or trade family), pass_if, fail_if (the falsifier), rationale (the why), why_query, evidence (citations), vehicle, combines_as.
5. **No claim:** the reason and the best rejected candidate with the query that killed it. A no-claim with a full trail is a good session.
6. **Guard rails:**
   - only the six tools, and every call is counted;
   - cite only query ids of this session;
   - the observation may read any column, but a vehicle acts only on fields known at the close or the fill;
   - no profit or cost judgement;
   - one claim or none;
   - stop when the comparison budget says so;
   - no dates past the research period;
   - no regime claims while every bar is `unknown`.
7. **Removed from v3** (by Steps 10-11 and A1.11):
   - the relevance floor and `confirmed_small` (no cost anywhere);
   - market claims as output, and piggyback confirmation;
   - `relevance_floor` / `confirm_if` in cost units;
   - self-scores;
   - `discarded` as a field (it is the no-claim's `best_rejected`).
8. **Lens texts:** v3 section 3.7, with the market-claim sentence of the forecast lens rewritten. A forecast observation becomes a strategy claim through its vehicle (e.g. a gate or a band on the forecast).

## 7. Flags and registration

**`orchestrator.analyst.enabled`** (off), plus `model`, `max_turns`, `max_budget_usd` and `timeout_minutes` under the same section. Registered where recent flags are:
- `config/campaign_config.yaml`;
- `config/feature_flag_register.yaml`;
- `run_campaign._flag_readers`;
- `TARGET_FLAGS` in `tests/test_e061_end_to_end_wiring.py`.

**Pre-flight refusal:** analyst on without `specialist_readers`, `reader_findings` and `folds`.

## 8. Tests (stubbed session, no API key)

- **Flag off, byte identity:**
  - `_stage_agent_options()` is unchanged;
  - the readers stage prompt, the calls and every written file are identical to master on the existing readers-stage fixtures.
- **CUL-336, changed deliberately:**
  - "exactly two `query(...)` calls" becomes three, with `_invoke_analyst_llm` added to the set;
  - every call still passes a `_stage_agent_options(...)` call;
  - one `ClaudeAgentOptions(...)` construction;
  - the SDK is still imported by `run_phase1_research.py` only.
- **New tests:**
  - the analyst CLI command read off the installed SDK: `--tools ""`, `--strict-mcp-config`, `--setting-sources=`, `--mcp-config` with only `analyst`, `--allowedTools` = the six, `--permission-mode dontAsk`, `--max-turns 40`, `--max-budget-usd 1.5`;
  - the hook denies `Read`, `Bash`, `WebFetch` and an unknown name, and records each.
- **A stubbed session** (a fake `query` that calls the real tool handlers, so the real log is written, then returns a canned answer):
  - the reading lands at the right path;
  - decide-next picks it;
  - `candidate_brief` gives a **fold-B** child brief, with the claim and the vehicle;
  - for the trade lens, needs decision 1.
- **Validation, one test per rule of section 5:** a refusal, then the retry, then `skipped` after the second.
- **Guard tests:** each with a mutation check (anchor once, restore byte for byte).

## 9. The runbook (for the operator's machine; not run here)

Written as `roadmap/E-075/PR5_RUNBOOK.md` in the build PR.

**Smoke session (about $1-3):**
1. Copy one saved run (run_074) into a scratch campaign root. Saved runs are never written to.
2. Run one lens with a small CLI, `tools/analyst_session.py --run <copy> --lens forecast`. It runs the real stage function on that run.
3. Check four things:
   - the tool-name form (`mcp__analyst__<name>`);
   - that the init message lists only the six tools;
   - that the model id is accepted;
   - the cost record.
4. Repeat for the trade lens.

**Pilot:** both lenses on saved runs 065-074 (fold A), then decide-next onto fold B, graded by `confirm_on_fold`.
- It needs real child backtests, which means campaign runs with `folds` and `analyst` on, launched by you.
- The runbook gives the commands and the budget (estimate: 20 sessions × about $0.7-1.2, plus the child runs' backtests).
- It also lists the process checks of D4: claims pass the checks, citations resolve, hold rates per fold are reported as information.
- **A pilot runner (PHASE_A slice 3) is not in PR-5** (decision 6).

## 10. Decisions for the operator (my recommendation first)

1. **Trade tests through the pipeline:** a separate PR-5a before PR-5 *(recommended)*, or inside PR-5.
2. **Lenses map onto the existing category files**, and the other three categories are code-skipped (`replaced_by_analyst`) *(recommended)*, or new category names, which would change every loader.
3. **No self-scores:** code writes neutral scores and the rubric `<category>-analyst-v1` *(recommended)*, or the analyst scores `confidence_real` and `mechanism_plausibility` (not `distance_to_profitable`).
4. **One query log and budget per lens** (`artifacts/analyst_queries/<lens>.yaml`, 150 each) *(recommended)*, or one shared log with 150 for the run.
5. **Model and caps:** Sonnet 5.5, 40 turns, $1.50, 15 minutes, one retry *(recommended)*.
6. **Pilot runner:** not in PR-5; the pilot is run as campaign runs from the runbook *(recommended)*, or a pilot-runner PR after PR-5.
