# E-068 design proposal: every run produces a proven finding and the next test to run

**Status:** PROPOSAL, document only. Nothing here is built. Written 2026-10-02 for operator review.
**Inputs:** OBSERVATIONS_QUEUE O-16, O-17, O-18, O-19 (and O-9); Linear E-068 / CUL-381; runs
run_065 and run_066; review_2026-09-27 A2 cards A-N; roadmap_review_2026-09-16; delivery_plan_v26
§1, Slices 2 and 5; DECISION_LOG D-014, D-017, D-021, D-042, D-055..D-063.
**Out of scope:** E-065 (done), E-066 (wider coins/periods), E-067 (trust results before holdout).

---

## 0. The proposal in ten lines

1. An **idea** becomes a **claim card**: one sentence in plain words, its **kind** (O-18's list),
   a **test** (what is measured, against which baseline, what result would prove it false), and
   the **rationale** that links the test to the claim.
2. Step 1a writes the claim card. It picks the test from a **small library of test templates**
   and fills in the parameters. **Code** computes the test; the agent never writes test code.
3. Code checks the card mechanically. An optional review call checks that the test fits the
   claim. It is **record-only first**, and becomes a gate only if the record shows it catches
   real problems.
4. The grid grades the **claim test** as one more criterion (same rules as today: every
   variant, floors, a FAIL dominates). It writes a **claim status** (supported, refuted or
   inconclusive) next to today's idea status.
5. The regroup step stores the result as a **finding**: claim, kind, test, scope, numbers and
   verdict, reusable later. Findings are information, never bans (D-055).
6. Readers become **real readers**. They get the claim, the manifest, the real config and all
   the evidence. They write: what the evidence says about the claim, **side findings each with a
   next test**, and optionally one patch checked against the real config.
7. Everything sits behind new flags, off by default. With the flags off, output is
   byte-identical.

---

## 1. The problem, in two real runs

| | run_065 (Donchian 1d) | run_066 (vol-managed Keltner 1h) |
|---|---|---|
| Claim (hypothesis_card) | A close above the 80th percentile of the 20-day range brings continuation over **bars 1-5** after the breakout | Multi-week momentum, sized by inverse volatility, captures trend continuation and cuts crash losses |
| What the grid tested | edge-to-cost > 2.2; residual IC > 0.02 over **all bars** | edge-to-cost; sign by era; residual IC over all bars |
| Result | refuted (residual IC: -0.024 / -0.037 / +0.038) | refuted (edge-to-cost 1.33 / 1.28 / 2.19) |
| Was the claim tested? | **No.** A 1-5 bar effect after an event is diluted in an all-bar linear IC (O-16) | **Partly.** "Cuts crash losses" was never measured, and the vol scaling could not be expressed in config |
| Readers | 2 proposals, both unusable: a stop-loss setting that does not exist; a detector "fix" based on another run's file (CUL-381) | 2 proposals, both unusable: a setting that does not exist (`entry_lookahead_bars`, which would also be lookahead); same stale detector file |
| What we learned, stored | "refuted", plus a grid summary | same |

**Root causes:**

- The criterion menu holds four tests: edge-to-cost, sign by era, residual IC (code-added) and
  profit bars (`config/criterion_menu.yaml`). None measures "what happens after an event",
  "does it work only in condition X", or "how long does the effect last". So 1a pre-registers
  what exists, not what the claim needs. The grid applied that faithfully (O-16: a design gap,
  not a bug).
- Readers were blind (O-19). They had no claim, no config and no catalogue. D-062 and D-063
  fix the inputs; this proposal fixes what readers are asked to produce.
- Nothing stores "what did we learn" in a form that can be reused or combined.

---

## 2. What an idea is: the claim card

A new `claim` block in `hypothesis_card.yaml`, written by step 1a. Worked example, run_065
written the new way:

```yaml
claim:
  statement: >
    After a daily close in the top 20% of its 20-day range, BTC and ETH returns over
    the next 1 to 5 days are higher than on other days.
  kind: conditional_behaviour       # one of the O-18 kinds, closed list (section 2.1)
  test:
    template: event_forward_return  # from config/claim_tests.yaml (section 3)
    params:
      event: {field: forecast, op: ">=", value: 12}   # top 20% of the range = forecast >= 12
      horizons_bars: [1, 2, 3, 4, 5]
      baseline: all_other_bars       # same coins, same windows, same period
      direction: greater
    pass_if: "mean forward return after the event exceeds the baseline at every horizon 1-5, one-sided p < 0.05 (block bootstrap), same sign in at least 2 of the eras covered"
    fail_if: "the difference is <= 0, or p >= 0.05, with at least the floor of events"
    floor: {min_events: 100, min_eras: 2}
  rationale: >
    If herding drives continuation after a breakout, returns in the days just after the
    breakout must beat ordinary days over the stated horizon. A linear IC over all days
    would dilute an effect that lives only on breakout days.
```

**Plain meaning of each field:**

| Field | What it is | Why it is needed |
|---|---|---|
| `statement` | The claim, in words a new joiner can read | It is what we store and reuse |
| `kind` | Which question it answers (state, direction, condition, horizon, ...) | Picks which templates are allowed; groups findings |
| `test.template` | The name of a measurement code already knows how to compute | The agent never writes measurement code (lookahead and forking-paths risk) |
| `test.params` | The few numbers the template needs (event, horizon, baseline) | This is the only part the agent chooses |
| `pass_if` / `fail_if` | What result supports the claim, and what result refutes it | A claim that cannot fail is not tested |
| `floor` | Minimum sample before a verdict is allowed | Below it: inconclusive, never pass |
| `rationale` | Why this test answers this claim | Checked by the review (section 4) |

### 2.1 Kinds (O-18's list) and which tests serve them

| Kind (O-18) | First test template | Available in v1? |
|---|---|---|
| Regime classifier ★ | `regime_separation`: forward return or volatility differs between labels, compared with shuffled labels | yes |
| Regime transition / early warning ★ | `event_forward_return` with event = label change; outcome = the trend ends (sign of trailing return flips) | yes (event on the `regime` column) |
| Direction forecast | existing `residual_ic` and `realized_edge_to_cost_ratio`; or `event_forward_return` | yes (exists today) |
| Volatility / risk forecast | `vol_forecast_ic`: rank IC of the forecast against forward realized volatility | yes |
| Event / tail behaviour | `event_forward_return` with a tail outcome (worst-decile return) | partly: events that need new data (liquidations) park as a feed request |
| Conditional behaviour ★ | `conditional_ic`: IC inside the condition minus IC outside it | yes |
| Horizon / decay | `horizon_decay`: IC or mean return at horizons 1..H; where it crosses zero | yes |
| Calendar / time effects | `event_forward_return` with event on the timestamp (hour, weekday) | yes |
| Redundancy / added information | existing `residual_ic` against the registry composite | yes (exists, needs `composition_runs`) |
| Lead-lag / cross-asset | `lead_lag_ic`: one coin's forecast against another coin's forward return | no: needs aligned multi-coin bars; parked (v2) |
| Data-feed value | `residual_ic` of a feed-based block against a price-only composite | partly: needs a registered price composite |
| Cost / turnover | existing `realized_edge_to_cost_ratio` | yes (exists) |
| Robustness / generality | existing `sign_consistent_by_era`; the asset variant (card D) | yes (exists) |

So **five new templates** (`event_forward_return`, `conditional_ic`, `horizon_decay`,
`regime_separation`, `vol_forecast_ic`) plus the existing criteria cover 11 of 13 kinds. They
also cover the three criterion types card B.2 listed and never built: IC, correlation and
regime-conditional effect.

### 2.2 Why this cannot leak (rule 3, no lookahead)

- Every template reads only `bars.csv`, which the backtest already writes per window and per
  variant (`timestamp, close, forecast, regime, ...`; the engine produced these columns bar by
  bar, causally).
- The **event or condition** may only name columns at bar *t* (`forecast`, `regime`, the
  timestamp, a lag of `close`). The parameter grammar has no field that reads bar *t+1* or
  later, and code checks it.
- The **outcome** (forward return or volatility over *h* bars) is the label being predicted. It
  is computed by the template, never by the agent, and never fed back into a decision.
- Tests run on the pre-registered windows only, the same ones the backtest used. The holdout is
  never touched (E-067 still gates any holdout spend).

---

## 3. How the test is computed and graded

- **New tool `tools/claim_tests.py`.** One pure function per template:
  `bars per window -> {value, p_value, n, n_eff, per_era, reason}`. It writes
  `artifacts/claim_test.yaml` per variant. This is exactly the pattern `tools/residual_ic.py`
  already follows (artifact, then grid).
- **Statistics.** Overlapping horizons are autocorrelated, so p-values use a block bootstrap
  or an effective sample size (`n_eff`, as residual IC already reports). Every template has a
  floor, so a thin sample gives **inconclusive**, never a pass.
- **The grid.** `claim_test` becomes one more criterion in the grid
  (`tools/verdict_criteria_evaluator.py::evaluate_grid`). It is graded with today's rules
  unchanged: every variant, floors, a FAIL dominates INCONCLUSIVE (D-014), no averaging. No AI
  decides anything here (card C).
- **Two statuses, kept separate:**
  - `claim_status` (supported / refuted / inconclusive) comes **only** from the claim test.
    Answer to: "is the claim true on this data?"
  - `idea_status` stays what it is today: the menu criteria (edge-to-cost and the rest),
    graded the same way. Answer to: "is this a usable block?"
- **Why both.** A supported claim with a failed cost test is still knowledge: "the signal is
  real, but not tradeable alone, so combine it". Today that case reads only "refuted". A regime
  classifier claim makes no trades at all, so edge-to-cost does not apply to it; its
  `idea_status` would rest on the regime criteria (and on card F composition for regime blocks).

**Template parameters are bounded:** a closed list of fields, operators and horizon ranges, in
`config/claim_tests.yaml`, version-pinned like `criterion_menu.yaml`. 1a may set only what a
template declares as settable (the menu's `card_overridable` idea).

---

## 4. How step 1a writes it, and how the test is checked

**Step 1a** (`hypothesis-design/SKILL.md`, `schemas/hypothesis_card.schema.json`) gains:

- a required `claim` block (under the flag), with `kind` from the closed list;
- the instruction: pick a template that fits the kind, fill its parameters, and state
  `pass_if`, `fail_if` and `rationale` in plain words. If **no template fits**, write the test in
  words and mark `test.template: none`.

**Checks, cheapest first:**

1. **Code (always on, before any spend).** The schema is valid; the template exists and allows
   this kind; the parameters are in the declared ranges; the event names only bar-*t* fields;
   the horizon is shorter than a window; there is a floor; `pass_if` and `fail_if` are both
   present. On failure: one retry for 1a with the error, as every stage has today.
2. **`template: none`.** The idea is **parked, not stopped**, and a `test_request` is appended to
   `campaign_record/test_requests.yaml`. This is card J's component-gap pattern (park, don't
   stop), reused. A human, or a later slice, adds the template, then `--unpark`. The agent never
   free-hands a test that gets graded.
3. **Review call (optional, one LLM call, flag `claim_test_review.mode`).** A fixed O-18
   checklist:
   - Does the test measure *this* claim?
   - Can it fail?
   - Is the baseline fair (same coins, same period)?
   - Is the threshold set before any data?
   - Is the floor reachable with these windows?

   It outputs `ok` or a list of issues.
   - `record` mode (the default once the flag is on): the result is stored and nothing is
     blocked.
   - `gate` mode: one revision round for 1a; if the issues remain, the idea is parked with the
     reason.

**Challenge to your lean (agent proposes, review sub-step).** I agree the agent should propose,
with templates where they fit. I would add two limits:

- **"Templates where they fit" should mean "templates for anything that gets graded".** An
  agent-written test that the grid then grades is a free-handed criterion. That re-opens what
  card B closed ("pick from a table, don't free-hand"), and it gives the campaign an unlimited
  number of ways to find a pass by chance. The agent still proposes freely: the claim, the
  kind, the parameters, and new templates via `test_requests.yaml`.
- **The review sub-step is close to the deleted `validation` stage.** That stage was "pressure
  test the design: approve / refine (budget two) / reject", deleted on 2026-09-18 because its
  catches were design-guide problems, not controls to keep (engineering_roadmap.html:600). To
  avoid re-creating it, the review only checks the **test against the claim**. It never judges
  the idea, the config or the design, it has at most one round, and it can park but never
  reject. It also starts record-only. Turn on `gate` only if a few runs show it catching real
  problems that the code checks miss.

---

## 5. How a verdict becomes a reusable finding

The regroup step (`_run_regroup_record_stage`, card H: memory is written before any decision)
writes a **finding record** into the run's `campaign_memory.yaml` entry:

```yaml
finding:
  finding_id: F-run_065-1
  statement: "After a daily close in the top 20% of its 20-day range, ..."
  kind: conditional_behaviour
  test: {template: event_forward_return, params: {...}, template_version: 1, test_hash: <sha>}
  scope: {venue: kraken, product: perp, symbols: [BTCUSD, ETHUSD], timeframe: 1d,
          windows_sha: <sha>, period: 2022-01..2023-12}
  result: {per_variant: {base: {value: ..., p_value: ..., n_events: ...}, ...}, eras: {...}}
  claim_status: refuted | supported | inconclusive
  trial_ids: [run_065:base, ...]
  source: {run_id: run_065, hypothesis_id: ..., parent_finding: null}
```

- **One place.** It goes in the memory entry, not a new store; regroup is already its only
  writer. A small code-built **findings summary** (like `registry_summary.yaml`) gives 1a and
  the readers a compact "what we know" view.
- **Reuse rule.** A finding is information, never a ban (D-055). A refuted claim blocks only
  the exact same test on the exact same scope. That is today's novelty key, extended with
  `test_hash`.
- **Combination.** A supported regime-classifier finding plus a supported conditional finding
  ("X works in trends") is the raw material for composition (card F). This proposal only makes
  findings **storable and queryable**. Automatic combination rules are a later epic, so that
  E-068 stays buildable.
- **Counting (selection honesty).** Every graded claim test is an attempt. Today's trial rows
  count backtested variants. Claim tests add statistical tests, so the findings summary reports
  "best of N claim tests tried" per kind. Without that, 13 kinds times several templates turn
  noise into findings.

---

## 6. Readers as real readers

**Inputs** (D-062/D-063 already deliver most of this):

- the claim card;
- the block manifest;
- the real base config;
- the component catalogue and the design guide;
- the five category reports;
- the grid, plus the claim test result;
- the findings summary.

**Output** (proposal schema v3; the patch stays optional):

```yaml
- reading_id: <category>-<run_id>-1
  claim_reading:                 # what the evidence says about the claim; never a verdict
    says: supports | contradicts | silent
    summary: "plain words"
    evidence: ["variants.base.slices.per_window[...] = ..."]    # cited fields, checked as today
  side_findings:                 # things noticed that are not the claim
    - statement: "Entries lag the breakout by about 0.8% on 99% of trades"
      kind: horizon_decay
      next_test: {template: horizon_decay, params: {...}}       # must be a library template
      evidence: [...]
  patch: null | {component_id, field, before, after}            # checked at write time against
                                                                # the real config (resolve_patch)
  scores: {confidence_real, distance_to_profitable, mechanism_plausibility}   # card I, unchanged
```

- `claim_reading` **never changes `claim_status` or `idea_status`**. The grid decides; the AI
  explains (card C, D-009).
- A side finding with a `next_test` becomes a decide-next candidate: a brief whose claim card
  is pre-filled. 1a then only checks it for completeness (card N, one entry point). Scores rank
  it (card I, D-017) and code gates it (novelty, feasibility).
- The patch check at write time is the safety net from the 2026-10-02 discussion (deferred
  check (b)). It lives here, as part of the new output.
- **No hindsight proposals.** run_066's "enter 1 bar earlier" came from the trade_efficiency
  report's `enter_earlier.pct_better_entry_1bar_earlier`, a hindsight statistic. The SKILL says
  so; the template grammar cannot express it; and the report field gets a "hindsight, not a
  setting" note.
- **The SKILLs are rewritten, not patched.** Today's 240-300 line reader SKILLs carry the old
  verdict-interpreter rule sets ("Rule N fires, so propose this change"). They become short:
  read the claim, read the evidence, say what it shows, propose tests.

**One reader or five?** This is your decision (target cards H and I describe one reader per
report).

| Option | What | Pros | Cons |
|---|---|---|---|
| A. Five lenses (today's shape) | One reader per report, new output | No card change; each prompt is small | No reader sees the whole picture (run_065: forecast_power said nothing while regime_power blamed the detector); five SKILLs to keep in sync |
| B. One reader | All five reports in one call | Sees cross-report patterns; one SKILL; simpler code | Changes cards H/I (a target-design decision); one bigger prompt (~45k tokens of reports) |
| C. Five extractors + one synthesizer | Cheap lenses summarize, a strong model reads the claim | Quality where it matters | Most code; two layers to debug |

**I recommend B** on a strong model, because the job is now judgement about one claim, not
pattern matching per report.

---

## 7. Model choice for readers (cost and quality)

**Measured today** (run_066 audit log, Haiku 4.5): five reader calls cost **$0.44**, out of
$0.90 for the whole run. That was about 96k input tokens (cache writes) and 43k output tokens.
D-063 adds about 16k input tokens per reader call. **Prices** (Claude API reference, cached
2026-09-25), input / output per million tokens: Haiku 4.5 $1 / $5; Sonnet 5.5 $2 / $10;
Opus 5.5 $4 / $20; Fable 5.1 $10 / $50.

| Option | Estimated reader cost per run | Notes |
|---|---|---|
| 5 x Haiku 4.5 (today, with D-063 inputs) | ~$0.55 | measured $0.44 + ~$0.10 for the new inputs |
| 5 x Sonnet 5.5 | ~$1.1 | about 2x Haiku per token |
| 5 x Opus 5.5 | ~$2.2 | about 4x |
| **1 x Opus 5.5, combined (option B)** | **~$0.65** | ~70k input once + ~15k output; inputs not repeated five times |
| 1 x Fable 5.1, combined | ~$1.6 | most capable; 2.5x Opus 5.5 per token |

**These are estimates, not measurements.** Output length depends on the model, and thinking
cannot be turned off on Sonnet 5.5 or Opus 5.5; it is controlled by effort instead. The first
real run on the chosen option measures it.

Today every AI stage uses one constant (`_CLAUDE_WORKER_MODEL`, Haiku). This proposal adds a
per-stage setting, `orchestrator.specialist_readers.model`. Score provenance (C5.7b) already
records which model answered.

**I recommend option B on Opus 5.5:** about the cost of today's five Haiku calls, a much
stronger reader, and one prompt to maintain. Keep 1a on its current model until the claim
review record shows whether 1a writes good tests.

---

## 8. Flags and migration

| Flag (all off by default) | Does | Requires |
|---|---|---|
| `orchestrator.claim_tests.enabled` | 1a writes `claim`; code checks; `claim_tests.py` runs; the grid grades `claim_test`; `claim_status` is written | grid_evaluation, config_direct_authoring |
| `orchestrator.claim_test_review.mode` (`off`, `record`, `gate`) | the optional review call | claim_tests |
| `orchestrator.findings.enabled` | regroup writes `finding`; findings summary; novelty key includes `test_hash` | claim_tests, regroup_record |
| `orchestrator.reader_findings.enabled` | reader output v3 (claim_reading, side_findings, checked patch); decide-next takes side findings | claim_tests, specialist_readers |
| `orchestrator.specialist_readers.mode` (`per_category`, `combined`) and `.model` | the reader shape and model of section 6 | specialist_readers |

- **Flags off:** byte-identical. A test for each flag proves it, the repo's usual rule.
- **Old runs:** not back-filled automatically. run_065 and run_066 are re-graded offline as the
  first acceptance test. Their `bars.csv` already exists, so this costs no new backtest or AI
  call and touches no new data. Expected: run_065's claim test either supports or refutes the
  1-5 day continuation. The "refuted" we have today never answered that question.
- **Old proposals:** still load (non-strict loading in decide-next and campaign memory); v2 and
  v3 proposals coexist.
- **No campaign runs until slices 1-3 below are built and reviewed** (the R2 queue entries stay
  `blocked_on_e068`).

**Suggested slices** (each its own PR, two-phase):

1. `claim_tests.py` with two templates (`event_forward_return`, `conditional_ic`), plus the
   offline re-grade of run_065 and run_066.
2. The 1a claim block, schema, code checks and the `test_requests.yaml` park.
3. Grid `claim_test` criterion and `claim_status`.
4. Finding record and findings summary.
5. Reader v3 output and SKILL rewrite.
6. Reader mode and model.
7. The remaining three templates.
8. The review call (record mode).

---

## 9. What it replaces, checked against the target cards

**Replaces:**

| Today | Becomes |
|---|---|
| Reader rule sets inherited from verdict-interpreter (Rule 4, Improvement 02, ...) in five long SKILLs | A short "read the claim, read the evidence" SKILL |
| Reader output: config edits only (`patch` / `new_block`) | Claim reading + side findings with tests; the patch is optional and checked |
| Judging an idea only by the four menu tests | Its own claim test plus the menu tests, as two separate statuses |
| "What we learned" = idea status + grid summary | A finding record |

**Kept unchanged:**

- the grid mechanics (card C, D-014);
- one entry point at 1a (card N);
- code gates and code ranking in decide-next, with scores that only rank (card I, D-009);
- the block registry (card A);
- profit bars, branch 3, hypothesis-blind (card B.7, D-021);
- the manual holdout;
- park-don't-stop (card J), reused for test requests.

**Must not re-create** (checked):

| Retired machinery | Why this proposal does not bring it back |
|---|---|
| Verdict routing (refine / pivot / kill), card G | `claim_status` routes nothing; decide-next stays a separate step |
| LLM verdict (verdict_interpreter, D-008/D-009) | Readers never set either status |
| The `validation` stage, deleted 2026-09-18 | The review checks only the test against the claim; one round; record-first; never rejects |
| Family / neighbour bans (D-055) | Findings are information; only an exact test on an exact scope is a repeat |
| Free-hand criteria, card B | Graded tests come only from the template library |

**Builds on:** card B.2's missing criterion types (now templates); `residual_ic`'s
artifact-then-grid seam; D-017's distance rubric (unchanged); card J's parking pattern;
D-062/D-063's reader inputs.

---

## 10. Decisions needed from you

1. **Graded tests: templates only** (agent proposes parameters and new templates), or should an
   agent-written test ever be graded? I recommend templates only.
2. **Review call:** start `record` and promote to `gate` on evidence, or `gate` from the start?
3. **Two statuses** (`claim_status` next to `idea_status`), or should the claim test replace the
   menu tests?
4. **Readers:** five lenses, one combined reader, or extractors plus a synthesizer? I recommend
   one combined reader.
5. **Reader model:** Haiku 4.5 (today), Sonnet 5.5, Opus 5.5 or Fable 5.1? I recommend Opus 5.5
   if readers are combined.
6. **First templates** for slice 1: `event_forward_return` and `conditional_ic`? These cover
   run_065's claim and the ★ conditional kind.
7. **Combination of findings:** confirm it is a later epic, not E-068.
