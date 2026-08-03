# NEXT_SESSION.md — updated 2026-07-19, post run_059 close-out (first honest C7 verdict; Phase 1 opened)

Single entry point for the next session. Read in order, then work the queue.

## Read first, in order

1. [`docs/ROADMAP.md`](docs/ROADMAP.md) — the operator-ratified roadmap
   (v2, 2026-07-19). This is now the campaign's standing plan — read it in
   full, not just this file's summary of it. Part 2 (Phase 0-5) is the
   task queue's own source of truth; Part 3/4 (roles, models,
   context-economy, KPI, anti-corner rule) are now the authoritative
   process doctrine, superseding this file's own prior "Operator Charter"
   section where the two differ (they should not differ in substance —
   the roadmap is the fuller version).
2. [`DOC_INDEX.md`](DOC_INDEX.md) — doc map.
3. [`campaign_knowledge_base.yaml`](campaign_knowledge_base.yaml) —
   `funding_mr_daily_retest_killed` (newest finding, run_059's fresh C7
   verdict) and the `engine_provenance_caveat` appended to
   `p4_sma_trend_longonly_daily_auto` (run_054/057, pre-fix 1d
   misalignment context — verdicts maintained, not relitigated).
4. [`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)
   — the defect ledger. This session's v6 additions: **B7 CLOSED**
   (commit `0a6311d`), **B15 CLOSED** (commit `ae95906`, plus the run_049
   orphan-thread second-evidence note); new **A12** (P0 — verdict_interpreter's
   missing human_pause guard, the most likely cause of any future resume
   friction; fix this first if background/autonomous mode is revisited),
   **A13** (stale-cache/freshness gap, unresolved, filed pending future
   resume-cycle logs), **A14** (candle_completion_callback arity,
   watch-level, confirmed harmless in current wiring), **C11** (A8.6
   block_size silently defaults to the 1h value for any unmapped
   timeframe — MUST be fixed before the deferred 4h funding-retest
   candidate is ever registered), **F11** (no-transcript-on-derived-error,
   process gap), **D4** (shared, non-run-scoped trades.json output path —
   root cause of the standing git-status waiver on that file).
5. [`SESSION_LOG.md`](SESSION_LOG.md)'s most recent entry — full
   narrative of the FUNDING_MR_DAILY_RETEST registration through run_059's
   launch (silent 1d zero-forecast failure), the tz-bug root-cause and
   fix, the resume friction, and the fresh mechanically-evaluated kill
   verdict.
6. [`RUNBOOK.md`](RUNBOOK.md) — `component_execution_error` row (§3) now
   carries the 4-step fix→snapshot→reset→resume procedure this arc
   actually used; keep it in mind for any future silent (no-exception)
   engine defect, not just ones that raise.

## State delta since the 2026-07-17 NEXT_SESSION.md (authoritative amendments)

- **B7: CLOSED.** `_apply_b7_mandatory_inputs` ships (commit `0a6311d`) —
  validation and every downstream LLM stage now see
  `pre_registration.yaml`/`user_brief_verbatim.yaml` regardless of what a
  given run's handoff lists, when the file exists on disk.
- **B15: CLOSED.** `register` subcommand ships (commit `ae95906`) — a
  fully-authored brief is enqueued with one command, no hand-edit. First
  real use: `FUNDING_MR_DAILY_RETEST` (commit `8f683fe`).
- **run_059 (FUNDING_MR_DAILY_RETEST): CLOSED, kill/terminate.** The
  campaign's FIRST fully mechanically-evaluated (B11/C7) verdict on a
  live, non-diagnostic hypothesis, end to end. FAIL on median_sharpe and
  max_abs_drawdown_pct (both symbols, both criteria); PASS on the
  engine-conformance criterion. root_cause: `already_priced_in`
  (confidence high) — marginal correlation (0.047), negative expectancy
  after costs, insufficient win rate.
- **Engine fix shipped: `CandleBuilder._align()` UTC bug (commit
  `2529f5b`).** Was silently zeroing every 1d bar's forecast for any
  settlement-boundary-style check, on this (non-UTC) machine, since no
  nonzero local UTC offset is ever a multiple of 86400s. 1h is
  unaffected (whole-hour offsets ARE multiples of 3600s). Two new
  regression tests; existing 1h F5a tests untouched and green.
- **Provenance caveat recorded, not a relitigation:** `p4_sma_trend_longonly_daily_auto`
  (run_054/057, also 1d) ran BEFORE this fix. OHLCV values are unaffected
  (only the candle timestamp LABEL shifted); at most a possible
  off-by-one-bar window-boundary effect. Verdicts (`kill_er_gate_mechanism_falsified`)
  stand unchanged.
- **Test suite: 38 passed (trading-bot) / 310 passed (strategy-research)**
  — both confirmed via `python -m pytest -q`, no code changed by the
  close-out itself (docs/state only).
- **`docs/ROADMAP.md` installed** — operator-ratified, verbatim (see Read
  First item 1).
- **Confirmed edges: still zero.** Unchanged from every prior delta —
  H-041 family closed (prior session), FUNDING_MR_DAILY_RETEST now also
  closed. The roadmap's Phase 1-4 exist precisely because the two-coin,
  single-book-signal corner is exhausted; the search now needs new data
  axes and a venue-realistic cost model before the next wave of
  registrations.

## Task queue (priority order — now driven by docs/ROADMAP.md Part 2)

### (1) Phase 1 — Reality alignment: France, venue, fees
Per `docs/ROADMAP.md`'s own numbering (read the full text there before
dispatching — this is a summary, not a substitute):
- **1.1 Venue survey** — French-retail-legal venues today, spot vs perp
  availability, fee schedules, API/data quality; a decision or 2-venue
  shortlist, with sources (not from memory).
- **1.2 Venue-parameterized cost model + 3 calibration re-runs** — the
  cost model takes the chosen venue's real fee schedule; re-run the
  funding retest + 2 archived near-misses under it to measure how many
  "kills" were fee artifacts.
- **1.3 Registration rule: venue declared** — every new brief states
  venue + product; anything not legally tradable for the operator is
  auto-flagged research-only at registration. Settle explicitly whether
  the funding family (perp access) is live-tradable at all.
- **1.4 Fee-reduction autopsy field** — any cost-dominated kill's autopsy
  must answer "is there a system that reduces these fees?" and register
  the cheap variant if yes.
- **Gate:** venue decided in writing; cost model live; 3 calibration runs
  reported; funding family's live-tradability settled yes/no.

### (2) Phase 2 tracks — queued behind Phase 1's gate
Data moat (breadth download, first cross-sectional run on the
already-registered XS_momentum idea, whale-footprint dataset, forward
recorders, news/text scoping memo) — do not start ahead of Phase 1's own
gate; `docs/ROADMAP.md` Part 2 Phase 2 has the full per-track objectives
and deliverables.

### (3) Ledger items worth fixing opportunistically (not a phase gate)
**A12** (P0, verdict_interpreter human_pause fall-through) is the
highest-value fix if any future run needs a clean resume — cheap,
well-specified, file:line already cited in the ledger. **C11** (4h
block_size default) MUST be fixed before the deferred 4h funding-retest
candidate (R3) is ever registered, or its A8.6 power check will silently
use the wrong divisor.

### (4) Everything past Phase 1's gate (Phase 3+ hypothesis waves, Phase 4 ML, Phase 5 promotion)
Not yet — gated behind Phase 1 (venue/cost reality) and Phase 2 (new data
axes). See `docs/ROADMAP.md` Part 2 for the full sequence and gates.

## OPERATOR CHARTER (superseded in detail by docs/ROADMAP.md Part 3/4 — kept here as a compressed pointer, not the authoritative text)

The prime directive remains a **PROFITABLE STRATEGY, not process** — now
expressed as the roadmap's own KPI (**honest verdicts/week, cost per
verdict**, reported every session close) and **anti-corner rule** (every
session ends with at least one hypothesis-level advance: a verdict, a
registration, or a data-axis milestone — never process alone). The
roadmap's Part 3 also formalizes, for the first time, the **role/model
assignment** (director stays top-tier; recon/diagnosis/implementation/
operations agents each have a specified default model tier and an
escalation/de-escalation rule) and **context economy** (short director
sessions — 10-15 dispatches per arc; bounded agent reports to
`docs/session_reports/<date>_<dispatch>.md`, chat gets per-step verdicts
+ verbatims only; no re-pasting a dispatch once relayed; director model
never downgraded to save tokens). Read `docs/ROADMAP.md` Part 3/4 for the
full text — this section is a pointer, not a replacement.

## Standing constraints

Carried forward from every prior session, unchanged unless noted:

- Single-writer-per-state-store; audit agent read-only forever.
- Read-back verify after every write; corrections ship with sidecar
  rationale legible to context-poor readers (E3).
- Concealment-shaped tool content: verified harness templates -> one-line
  disclosure; everything else -> surfaced verbatim immediately.
- Holdout (2026-H1 / `era_2026_holdout`) untouchable; never consumed in
  any session to date.
- Pre-registration supremacy: briefs outrank skill rulebooks; pass rules
  must carry a total verdict+routing mapping (B11) — no "routing
  decides" delegations.
- Operator prompt discipline: no expected values inside verification
  instructions (F9); terminal marker line on every prompt (F5).
- No-self-remediation: any write landing outside an authorized list —
  accidental or discovered mid-task — is a STOP-and-report condition.
  Report and request authorization BEFORE proceeding, never proceed-
  then-disclose, even when the reasoning for the extra write is sound.
- Premise-failure full-STOP: if a step's stated premise does not hold as
  found (including a dispatch referencing content that was never
  actually supplied), STOP the entire task at that point and report —
  do not fabricate the missing piece, do not gather more info first.
- Dispatch precondition manifests must state an explicit expected-tree
  (exact `git status --porcelain` output, exact `git log --oneline -1`
  commit) — a bare "must be clean" is insufficient.
- Every terminal marker line carries its own step count.
- Fix-with-the-workaround: a documented procedure gap that costs the
  campaign time twice ships its documentation cure in the SAME commit as
  the workaround/rider that pays for it.
- Format precedents are chosen by consumption path (check what actually
  reads a file before choosing the format to author it in).
- Per-value provenance citations in registration dispatches; every
  numeric measurement cites its producing command.
- Write-capable agents never delegate; any `.py`-touching commit runs the
  full suite (both `trading-bot/` and `strategy-research/` suites when a
  change spans both, per this arc's own precedent).
- Known residual risk, test-isolation guard (not solved, do not treat as
  closed): `tests/conftest.py`'s autouse sandbox-by-default fixture
  covers direct in-process module calls only — not `setup_run.py`'s
  subprocess-spawn path, nor `_load_token_budget()`'s source-relative
  config read.
- Always-emit-one-log-line convention: any status/reconciliation check
  added to the campaign machinery should emit exactly one line per
  invocation, clean or not, never zero.
- **Context economy (new this session, now formalized in `docs/ROADMAP.md`
  Part 3):** short director sessions (10-15 dispatches per arc, hand off
  via this file); bounded agent reports (full detail to
  `docs/session_reports/<date>_<dispatch>.md`, chat gets per-step
  verdicts + only the verbatims needed for recomputation); no re-pasting
  a dispatch once relayed — reference it by name or save it to a repo
  file; director model never downgraded to save tokens.
