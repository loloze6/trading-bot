# E-068 design proposal: every run produces a proven finding and the next test to run

**Status:** PROPOSAL, document only. Nothing here is built. Written 2026-10-02, revised
2026-10-03 after operator review (section 11).

**Inputs:**
- OBSERVATIONS_QUEUE O-16, O-17, O-18, O-19 (and O-9);
- Linear E-068 / CUL-381;
- runs run_065 and run_066;
- review_2026-09-27 A2 cards A-N;
- roadmap_review_2026-09-16;
- delivery_plan_v26 §1, Slices 2 and 5;
- DECISION_LOG D-014, D-017, D-021, D-042, D-055..D-063.

**Out of scope:** E-065 (done), E-066 (wider coins/periods), E-067 (trust results before holdout).

---

## 0. The proposal in ten lines

1. **Claim card.** An idea becomes a claim card: one sentence in plain words, its **kind**
   (O-18's list), a **test**, and the **rationale** linking the test to the claim. The test says
   what is measured, against which baseline, and what result would prove the claim false.
2. **Tests are composed, not free-written.** Step 1a writes the claim card and composes its
   test from **four slots**: which bars (selector), what happens next (outcome), compared with
   what (baseline), measured how (statistic). Each slot has a few small building blocks that
   **code** computes. The agent fills in a form; it never writes test code.
3. **Card checks.** Code checks the card mechanically. An optional review call checks that the
   test fits the claim. It is **record-only first**, and becomes a gate only on evidence.
4. **The grid is the only judge of the claim (branch 1).** It grades the claim test as one more
   criterion and writes a **claim status** (supported / refuted / inconclusive) next to today's
   idea status.
5. **Findings.** The regroup step stores the result as a **finding**: reusable later,
   information only, never a ban (D-055).
6. **Readers never judge the claim.** They **explain** the grid's result from the evidence and
   propose **side findings, each with a next test**. They may also propose one patch, checked
   against the real config.
7. **Flags.** Everything sits behind new flags, off by default. Flags off is byte-identical.

---

## 1. The problem, in two real runs

| | run_065 (Donchian 1d) | run_066 (vol-managed Keltner 1h) |
|---|---|---|
| Claim (hypothesis_card) | A close above the 80th percentile of the 20-day range brings continuation over **bars 1-5** after the breakout | Multi-week momentum, sized by inverse volatility, captures trend continuation and cuts crash losses |
| What the grid tested | edge-to-cost > 2.2; residual IC > 0.02 over **all bars** | edge-to-cost; sign by era; residual IC over all bars |
| Result | refuted (residual IC -0.024 / -0.037 / +0.038) | refuted (edge-to-cost 1.33 / 1.28 / 2.19) |
| Was the claim tested? | **No.** A 1-5 bar effect after an event is diluted in an all-bar linear IC (O-16) | **Partly.** "Cuts crash losses" was never measured |
| Readers | 2 proposals, both unusable (a stop-loss setting that does not exist; a detector "fix" based on another run's file) | 2 proposals, both unusable (a setting that does not exist and would be lookahead; same stale file) |
| What we learned, stored | "refuted", plus a grid summary | same |

**Root causes:**

- **The tests are generic.** The criterion menu holds four tests, none of which measures "what
  happens after an event", "only in condition X", or "how long the effect lasts". So 1a
  pre-registers what exists, not what the claim needs (O-16: a design gap, not a bug).
- **The readers were blind** (O-19). D-062 and D-063 fixed their inputs; this proposal fixes
  what they are asked to produce.
- **Nothing is reusable.** Nothing stores "what we learned" in a form that can be reused or
  combined.

---

## 2. What an idea is: the claim card

A new `claim` block in `hypothesis_card.yaml`, written by step 1a. Here is run_065, written the
new way:

```yaml
claim:
  statement: >
    After a daily close in the top 20% of its 20-day range, BTC and ETH returns over
    the next 1 to 5 days are higher than on other days.
  kind: conditional_behaviour            # O-18 list, closed (section 2.2)
  test:                                  # composed from the four slots (section 3)
    selector:  {kind: event, field: forecast, op: ">=", value: 12}   # top 20% of the range
    outcome:   {kind: fwd_return, horizons: [1, 2, 3, 4, 5]}
    baseline:  {kind: complement}        # all other bars, same coins, windows and period
    statistic: mean_diff
    direction: greater
    pass_if: "mean_diff > 0 at every horizon, one-sided p < 0.05, same sign in >= 2 eras"
    fail_if: "mean_diff <= 0 or p >= 0.05, with at least the floor of events"
    floor: {min_events: 100, min_eras: 2}
  rationale: >
    If herding drives continuation after a breakout, the days just after it must beat
    ordinary days over the stated horizon. A linear IC over all days would dilute an effect
    that lives only on breakout days.
```

| Field | What it is | Why |
|---|---|---|
| `statement` | The claim, in words a new joiner can read | It is what we store and reuse |
| `kind` | Which question it answers | Groups findings; tells the review what to expect |
| `test` slots | Which bars, what next, compared with what, measured how | Code computes it; the agent only fills the form |
| `pass_if` / `fail_if` | What supports the claim, and what refutes it | A claim that cannot fail is not tested |
| `floor` | Minimum sample before any verdict | Below it the result is inconclusive, never a pass |
| `rationale` | Why this test answers this claim | Checked by the review (section 4) |

### 2.1 Why this cannot leak (no lookahead)

- **The selector** may read only bar *t*: `forecast`, `regime`, the timestamp, and lags of
  `close`. That rule is enforced once, inside the selector building blocks, not test by test.
- **The outcome** (the future: forward return, volatility, drawdown) is the label being
  predicted. Code computes it, and it never feeds a decision.
- **Data.** Everything is read from the `bars.csv` the backtest already wrote, on the
  pre-registered windows only. The holdout is never touched; E-067 still gates any holdout
  spend.

### 2.2 Kinds (O-18) and the slot combinations that test them

| Kind (O-18) | Example test (selector + outcome + baseline + statistic) | v1? |
|---|---|---|
| Regime classifier ★ | `regime == X` + `fwd_return(h)` or `fwd_volatility(h)` + `complement` + `mean_diff` (does the label separate markets?) | yes |
| Regime transition / early warning ★ | `regime_change(to=X)` + `trend_ends(h)` + `placebo` + `hit_rate` | yes |
| Direction forecast | `all` + `fwd_return(h)` + `complement` + `rank_ic`; or the existing `residual_ic` | yes |
| Volatility / risk forecast | `all` + `fwd_volatility(h)` + `complement` + `rank_ic` | yes |
| Event / tail behaviour | `event(...)` + `fwd_max_drawdown(h)` + `placebo` + `mean_diff` | yes (price events); new-data events park as a feed request |
| Conditional behaviour ★ | `regime == trending` + `fwd_return(h)` + `complement` + `rank_ic` | yes |
| Horizon / decay | `event(...)` + `fwd_return(1..H)` + `complement` + `decay_curve` | yes |
| Calendar / time effects | `calendar(weekday in [Sat, Sun])` + `fwd_volatility(24)` + `complement` + `mean_diff` | yes |
| Redundancy / added information | existing `residual_ic` (needs `composition_runs`) | yes (exists) |
| Lead-lag / cross-asset | `all` + `fwd_return_of(other_symbol, h)` + ... | no: one new outcome block, added when a claim needs it |
| Data-feed value | `residual_ic` against a price-only composite | partly |
| Cost / turnover | existing `realized_edge_to_cost_ratio` | yes (exists) |
| Robustness / generality | existing `sign_consistent_by_era`; the asset variant (card D) | yes (exists) |

The v1 blocks, together with the existing criteria, cover 11 of the 13 kinds. They also cover
the three criterion types card B.2 listed and never built: IC, correlation and
regime-conditional effect.

---

## 3. The test engine: four slots, small building blocks

**Composed, not listed.** A test is not a template from a list; it is a sentence built from
four slots:

> **On these bars** (selector), **what happens next** (outcome) is **different from these
> other bars** (baseline), **measured like this** (statistic).

| Slot | v1 building blocks |
|---|---|
| **selector**: which bars | `event(field op value)`, `regime == X`, `regime_change(to=X)`, `calendar(hour/weekday)`, `quantile(field, top/bottom q)`, `all` |
| **outcome**: what happens next | `fwd_return(h)`, `fwd_volatility(h)`, `fwd_max_drawdown(h)`, `trend_ends(h)` |
| **baseline**: compared with | `complement` (all other bars), `placebo` (same number of random bars, block-shuffled), `other_selector` |
| **statistic** | `mean_diff`, `rank_ic`, `hit_rate`, `decay_curve` |

About 15 building blocks give hundreds of valid tests. In a new tool,
`tools/claim_tests.py`:

```python
@dataclass(frozen=True)
class TestSpec:
    selector: dict    # {"kind": "event", "field": "forecast", "op": ">=", "value": 12}
    outcome: dict     # {"kind": "fwd_return", "horizons": [1, 2, 3, 4, 5]}
    baseline: dict    # {"kind": "complement"}
    statistic: str    # "mean_diff"
    floor: dict       # {"min_events": 100, "min_eras": 2}

SELECTORS  = {"event": sel_event, "regime": sel_regime, "regime_change": sel_regime_change,
              "calendar": sel_calendar, "quantile": sel_quantile, "all": sel_all}
OUTCOMES   = {"fwd_return": out_fwd_return, "fwd_volatility": out_fwd_vol,
              "fwd_max_drawdown": out_fwd_mdd, "trend_ends": out_trend_ends}
BASELINES  = {"complement": base_complement, "placebo": base_block_placebo,
              "other_selector": base_other_selector}
STATISTICS = {"mean_diff": st_mean_diff, "rank_ic": st_rank_ic,
              "hit_rate": st_hit_rate, "decay_curve": st_decay}

def check_spec(spec: TestSpec) -> list[str]:
    """Before any data: every slot names a known block, parameters in range,
    selectors read only bar-t fields, horizon < window, floor present."""

def run_test(bars, spec: TestSpec) -> dict:
    mask = SELECTORS[spec.selector["kind"]](bars, spec.selector)     # bar t only
    y    = OUTCOMES[spec.outcome["kind"]](bars, spec.outcome)        # the future = the label
    ref  = BASELINES[spec.baseline["kind"]](bars, mask, spec.baseline)
    return STATISTICS[spec.statistic](y, mask, ref, floor=spec.floor)
    # -> {value, p_value, n_events, n_eff, per_era, reason}

def spec_hash(spec: TestSpec) -> str: ...   # identity of a test, for findings and novelty
```

- **Output and grading.** The tool writes `artifacts/claim_test.yaml` per variant. This is the
  artifact-then-grid seam `tools/residual_ic.py` already uses.
- **Statistics.** Overlapping horizons are autocorrelated, so p-values come from a block
  bootstrap or an effective sample size (`n_eff`, as residual IC reports). Below the floor, the
  result is **inconclusive**, never a pass.
- **The grid** (`tools/verdict_criteria_evaluator.py::evaluate_grid`) grades `claim_test` with
  today's rules unchanged: every variant, floors, a FAIL dominates INCONCLUSIVE (D-014), no
  averaging, no AI.

**Two statuses, kept separate:**

- **`claim_status`** (supported / refuted / inconclusive) comes **only** from the claim test.
  It answers "is the claim true on this data?"
- **`idea_status`** stays today's: the menu criteria, graded the same way. It answers "is this
  a usable block?"

A supported claim with a failed cost test is still knowledge: "real, but not tradeable alone,
so combine it". Today that case reads only "refuted".

**How the library grows: on demand, never in advance.**

- An idea whose test the slots cannot express is **parked**, not stopped. A `test_request` names
  the missing building block (for example "outcome `fwd_return_of(other_symbol)`") and goes to
  `campaign_record/test_requests.yaml`. This is card J's park-don't-stop pattern.
- A person adds that one small function, the idea is un-parked, and every later idea can use
  the block too. One block multiplies coverage.

**The catch: freedom means more chances of a lucky pass.** Hundreds of combinations make it
easy to find a "significant" result by chance. Three protections:

1. The test is fixed at 1a, **before any data**, and stored with its `spec_hash`.
2. Every graded test is **counted**, and findings report "best of N tests tried" per kind.
3. `placebo` is offered as the default baseline whenever the claim has no natural comparison.

---

## 4. How step 1a writes it, and how the test is checked

**Step 1a** (`hypothesis-design/SKILL.md`, `schemas/hypothesis_card.schema.json`) gains:

- a required `claim` block (under the flag), with `kind` from the closed list;
- the instruction: compose the test from the slots, and state `pass_if`, `fail_if` and
  `rationale` in plain words. If the slots cannot express the test, describe it in words and
  set `test: none` with `missing_block: "<what is needed>"`.

**Checks, cheapest first:**

1. **Code (always, before any spend).** `check_spec`: known blocks, parameters in range,
   bar-*t* selectors only, horizon shorter than a window, floor present, `pass_if` and
   `fail_if` present. On failure, 1a gets one retry with the error, as every stage has today.
2. **`test: none`.** The idea is parked and a `test_request` is appended (section 3). The agent
   never free-hands a graded test.
3. **Review call** (optional, one LLM call, flag `claim_test_review.mode`). It runs a fixed
   O-18 checklist:
   - Does the test measure *this* claim?
   - Can it fail?
   - Is the baseline fair?
   - Is the threshold set before any data?
   - Is the floor reachable with these windows?

   It returns `ok` or a list of issues.
   - **`record` mode** (the default): store the result, block nothing.
   - **`gate` mode**: 1a gets one revision; if the issues remain, the idea is parked with the
     reason.

**This must not become the deleted `validation` stage.** That stage was "pressure-test the
design: approve / refine (budget two) / reject", deleted on 2026-09-18 (engineering_roadmap.html:600).
The review checks only the **test against the claim**:

- never the idea, the config or the design;
- at most one round;
- it can park, never reject;
- record-only until a few runs show it catches problems the code checks miss.

---

## 5. How a verdict becomes a reusable finding

The regroup step (`_run_regroup_record_stage`, card H: memory is written before any decision)
writes a **finding** into the run's `campaign_memory.yaml` entry:

```yaml
finding:
  finding_id: F-run_065-1
  statement: "After a daily close in the top 20% of its 20-day range, ..."
  kind: conditional_behaviour
  test: {spec: {...}, spec_hash: <sha>, engine_version: 1}
  scope: {venue: kraken, product: perp, symbols: [BTCUSD, ETHUSD], timeframe: 1d,
          windows_sha: <sha>, period: 2022-01..2023-12}
  result: {per_variant: {base: {value: ..., p_value: ..., n_events: ...}, ...}, eras: {...}}
  claim_status: supported | refuted | inconclusive
  trial_ids: [run_065:base, ...]
  source: {run_id: run_065, hypothesis_id: ..., parent_finding: null}
```

- **One place.** The memory entry; regroup is already its only writer. A small code-built
  **findings summary** (like `registry_summary.yaml`) gives 1a and the readers a compact
  "what we know" view.
- **Reuse.** A finding is information, never a ban (D-055). Only the same `spec_hash` on the
  same scope counts as a repeat; this extends today's novelty key.
- **Combination is already built (E-060) and E-068 plugs into it.** E-060 registers validated
  blocks (`block_registry.record_run`, only when `idea_status == validated`), and a registry
  change triggers a composition run (rule R1) that combines them. Regime blocks are tested
  there as "gated beats ungated, and the label passes health checks". The missing link today:
  a regime idea can never reach the registry. decide-next refuses it
  (`regime_block_needs_composition`, `decide_next.py:1405`), and nothing can prove a label
  standalone. E-068 closes that loop with no new combination engine:
  - a registry entry carries its finding (`statement`, `kind`, `claim_status`), so a composite
    knows what each block claims;
  - a **supported regime-classifier claim** (its composed test, section 3) is the label health
    check E-060 asks for. It makes the regime block eligible for the next composition run,
    where E-060's gated-vs-ungated test decides whether it is kept;
  - this is its own slice (section 8), so a regime idea runs end to end:
    claim, then finding, then registry, then composition.

---

## 6. Readers explain and propose; they never judge the claim

Branch 1, the grid, is the only judge of the claim. Readers are branch 2.

- **Inputs:** already delivered by D-062 and D-063: the claim card, the manifest, the real
  config, the catalogue and the design guide. Added here: all five reports, the grid with the
  claim test result, and the findings summary.
- **Output** (proposal schema v3):

```yaml
- reading_id: <category>-<run_id>-1
  explanation: >                 # why the grid's result came out this way -- never a verdict
    "The day-1 edge exists but reverses by day 3; the 5-day test averages it away."
  evidence: ["variants.base.slices.per_window[...] = ..."]     # cited fields, checked as today
  side_findings:                 # what else the evidence shows, each with a next test
    - statement: "Entries lag the move: price is ~0.8% past the trigger on 99% of trades"
      kind: horizon_decay
      next_test: {selector: {kind: event, ...}, outcome: {kind: fwd_return, horizons: [1, 2, 3]},
                  baseline: {kind: complement}, statistic: decay_curve}
      evidence: [...]
  patch: null | {component_id, field, before, after}   # optional; resolved against the real
                                                        # config when written (resolve_patch)
  scores: {confidence_real, distance_to_profitable, mechanism_plausibility}   # card I, unchanged
```

- **No verdict field.** There is no `supports` or `refutes`: a reader cannot set or contradict
  `claim_status` or `idea_status`. The grid decides; the AI explains (card C, D-009).
- **Side findings feed the next run.** A side finding with a `next_test` becomes a decide-next
  candidate: a brief whose claim card is pre-filled, which 1a only checks for completeness
  (card N). Scores rank it (card I, D-017) and code gates it (novelty, feasibility). A
  `next_test` must pass `check_spec`; otherwise it is recorded as a test request.
- **No hindsight proposals.** The SKILL says so, the selector grammar cannot express acting
  before a bar closes, and the trade_efficiency report's `enter_earlier` field gets a
  "hindsight, not a setting" note.
- **The SKILL is rewritten short:** "Read the claim. Read the grid's result and the evidence.
  Explain the result. List what else you noticed, each with a test composed from the slots."

**Five readers, kept** (operator, 2026-10-03). Each reader keeps its own focus (profitability,
forecast power, regime power, component attribution, trade efficiency); combining them would
blur that focus. The table below is kept for the record.


| Option | Pros | Cons |
|---|---|---|
| A. Five lenses (today) | No card change; small prompts | No reader sees the whole picture; five SKILLs to sync |
| B. One reader, all five reports (rejected) | Sees cross-report patterns; one SKILL; simpler | A target change to cards H/I; one prompt of ~45k tokens of reports |
| C. Five extractors + one synthesizer | Quality where it matters | Most code; two layers |

---

## 7. Model choice for readers (cost and quality)

**Measured** on run_066 with Haiku 4.5: five reader calls cost **$0.44**, out of $0.90 for the
whole run. D-063 adds about 16-20k input tokens per call.

**Prices**, input / output per million tokens: Haiku 4.5 $1 / $5; Sonnet 5.5 $2 / $10;
Opus 5.5 $4 / $20; Fable 5.1 $10 / $50.

| Option | Estimated reader cost per run |
|---|---|
| 5 x Haiku 4.5 (today, with D-063 inputs) | ~$0.55 |
| 5 x Sonnet 5.5 | ~$1.1 |
| 5 x Opus 5.5 | ~$2.2 |
| **1 x Opus 5.5, combined (option B)** | **~$0.65** |
| 1 x Fable 5.1, combined | ~$1.6 |

These are estimates. Thinking cannot be turned off on Sonnet or Opus 5.5 (effort is the
control), so output length varies.

**Decided (operator, 2026-10-03): readers stay on today's model** for E-068. A per-stage model
setting is parked as its own epic, **E-069 · Each AI step can use its own model** (Linear
P-CUL-77).

---

## 8. Flags and migration

| Flag (all off by default) | Does | Requires |
|---|---|---|
| `orchestrator.claim_tests.enabled` | 1a writes `claim`; `check_spec`; `claim_tests.py` runs; grid grades `claim_test`; `claim_status` | grid_evaluation, config_direct_authoring |
| `orchestrator.claim_test_review.mode` (`off`, `record`, `gate`) | optional review call | claim_tests |
| `orchestrator.findings.enabled` | regroup writes `finding`; findings summary; novelty key gets `spec_hash` | claim_tests, regroup_record |
| `orchestrator.reader_findings.enabled` | reader output v3; decide-next takes side findings | claim_tests, specialist_readers |

- **Flags off:** byte-identical, proven per flag by a test.
- **Old runs** are not back-filled. run_065 and run_066 are re-graded **offline** as the first
  acceptance test, from the `bars.csv` they already saved: no new backtest, no AI call, no new
  data.
- **Old proposals** still load (non-strict); v2 and v3 coexist.
- **No campaign runs** until slices 1-3 are built and reviewed.

**Slices** (each its own PR, two-phase):

1. **Test engine:** `claim_tests.py` with the four slots and the v1 blocks; `check_spec`,
   `run_test`, `spec_hash`; then the offline re-grade of run_065 and run_066.
2. **Step 1a claim block:** the schema, the code checks, and the `test_requests.yaml` park.
3. **Grid:** the `claim_test` criterion and `claim_status`.
4. **Findings:** the finding record and the findings summary.
5. **Readers:** v3 output and the short SKILL.
6. **Findings into the existing combination (E-060):** registry entries carry their finding; a
   supported regime-classifier claim makes the regime block eligible for composition.
7. **Review call** (record mode).
8. **New building blocks:** only when a test request needs them.

---

## 9. What it replaces, checked against the target cards

**Replaces:**

| Today | Becomes |
|---|---|
| Reader rule sets inherited from verdict-interpreter, in five long SKILLs | Five short SKILLs (one focus each): "explain the result, propose findings with tests" |
| Reader output: config edits only | Explanation, side findings with tests, optional checked patch |
| Ideas judged only by four generic tests | Their own composed claim test, plus the menu tests (two statuses) |
| "What we learned" = idea status | A finding record |

**Kept:**

- grid mechanics (card C, D-014);
- one entry point at 1a (card N);
- code gates and code ranking, with scores that rank only (card I, D-009);
- the block registry (card A);
- profit bars (card B.7, D-021);
- the manual holdout;
- park-don't-stop (card J).

**Must not re-create:**

| Retired | Why not here |
|---|---|
| Verdict routing (card G) | `claim_status` routes nothing |
| LLM verdict (D-008/D-009) | Readers never set or contradict a status |
| The `validation` stage (deleted 2026-09-18) | The review checks only test-vs-claim, one round, record-first, never rejects |
| Family / neighbour bans (D-055) | Findings are information; only the same `spec_hash` on the same scope is a repeat |
| Free-hand criteria (card B) | A graded test is always a composition of code-defined blocks |

---

## 10. Decisions still needed

None. All decisions are recorded in section 11.

---

## 11. Decided by the operator (2026-10-03)

- **Readers never test or verify the claim.** That is branch 1, the grid. Readers explain the
  grid's result and propose new findings, each with a next test (section 6; the earlier
  `claim_reading: supports | contradicts` field is removed).
- **The test library is composable** (section 3): four slots, about 15 small code-defined
  blocks, grown on demand through parked test requests, never written by the agent, and not
  enlarged in anticipation.
- **Two statuses, both kept:** `claim_status` (is the claim true?) and `idea_status` (is it a
  usable block?). The second is what the registry binds on later.
- **Five readers kept,** each with its own focus, on today's model. Per-stage models are
  parked: E-069.
- **Combination stays in E-068's scope** as the connection to E-060's registry and
  composition (section 5, slice 6), so the loop works end to end.
- **Review call starts in `record` mode:** it stores its comments and blocks nothing;
  `gate` only if the record shows real catches the code checks miss.
