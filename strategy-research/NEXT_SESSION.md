# NEXT_SESSION.md — updated 2026-07-20, post Phase 1 (venue/cost reality alignment) close-out

Single entry point for the next session. Read in order, then work the queue.

## Read first, in order

1. [`docs/ROADMAP.md`](docs/ROADMAP.md) — the operator-ratified roadmap
   (v2, 2026-07-19). Still the campaign's standing plan. Phase 1's own gate
   (venue decided in writing; cost model live; calibration re-runs reported;
   funding family's live-tradability settled yes/no) is now CLOSED — see
   item 3 below for how. Phase 2 is next; Part 2's Phase 2 section has the
   full per-track objectives.
2. [`DOC_INDEX.md`](DOC_INDEX.md) — doc map (updated this close-out).
3. [`docs/venue_survey_20260719.md`](docs/venue_survey_20260719.md) — Phase
   1.1: Kraken decided as venue. Read its 2026-07-20 supplement too (margin
   fees, perp funding, the cost-mapping note) and open item #1's resolution
   (the apparent 0.40%/0.80% vs 0.25%/0.40% spot-fee conflict was never a
   real conflict — the 0.25% figure is a different, API-inaccessible
   product).
4. [`campaign_knowledge_base.yaml`](campaign_knowledge_base.yaml) — three
   things changed this close-out: (a) new finding
   `keltner_scoremode_fee_isolation_no_flip` — a controlled 10bps-vs-5bps
   fee pair (timeframe/window/config held fixed) confirms
   `keltner_scoremode_no_edge`'s two kills are structural, not fee
   artifacts; (b) `engine_provenance_caveat` on the same finding (filed
   prior dispatch) — the ORIGINAL run_028/run_030 silently executed at 1h
   despite declaring 4h protocols (interval threading didn't exist yet at
   the time); (c) new `venue_live_tradability` field on
   `funding_mr_daily_retest_killed` — Kraken perp is legally tradable by
   this operator (Pro/Futures API, 0.05% taker, MiFID appropriateness
   test), but that family's verdict stays RESEARCH-ONLY until a
   funding-cash-flow model exists — **do not fee-swap or re-run that
   family without one.**
5. [`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)
   — v7 additions this arc: **C12** (inert protocol-declared timeframe —
   archived runs predating interval threading silently ran at 1h; two
   confirmed instances, a future sweep for more is scoped but not
   performed) and **C13** (`rsi_momentum_trending_cost_drag`/run_018's
   archived config fails current V9 regime-detector validation, blocking
   re-execution — does NOT invalidate its original verdict).
6. [`SESSION_LOG.md`](SESSION_LOG.md)'s most recent entry — full narrative
   of the venue survey through the fee-isolation robustness result, the two
   aborted/superseded attempts caught before commit (not shipped), and the
   three independent audits (all AUDIT PASS on what was eventually
   ratified).

## State delta since the 2026-07-20 NEXT_SESSION.md (authoritative amendments, dated 2026-07-23)

- **Phase 2 Track A: COMPLETE.** Breadth ingestion reaches 19 of the 20
  targeted Kraken pairs (HYPE absent from the bulk archive, recon-confirmed,
  not ingested) with the exchange-qualified cache key and the standard-base
  symbol convention both settled and tested (commits `32b1c13` exchange-qualified
  cache key + 5-pair pilot; `446885b` symbol convention settled + scale-up;
  ledger `G1`/`G2` in `PIPELINE_IMPROVEMENTS_20260712_v4.md`). Live-fetch
  reachability against the archive slot is proved end-to-end (`11afb72`,
  `3d43cc1`).
- **XS_momentum run → PARKED, not a verdict.** Full-sample net Sharpe 1.325
  (gross 1.665), decaying to net Sharpe 0.07 in its latest full in-sample
  year (2025) — edge decay, not trade sparsity. No admissible verdict:
  no pre-registered `pass_rule` and no obtainable 2026 holdout can
  statistically resolve this year's Sharpe (SE ≥ 1.3 for any T ≤ 0.56). KB
  `outcome: ungated_decayed_measurement_no_admissible_verdict`,
  `verdict_status: ungated`; measurements preserved. Commit `6b27d56`.
- **The C7-EXT arc (7 gates, three audit rounds, now a closed deny-by-default
  schema) and the finding it produced.** XS_momentum's original REFINE
  verdict (commit `6c4df3d`) was issued off no pre-registered rule; closing
  that defect chain (`0a4d606` 7 gates; audited `a83084b` DO NOT RATIFY;
  remediated `2c8b8d1`; re-audited `4180799` DO NOT RATIFY, three name-matching
  bypasses found in two rounds; replaced with a closed schema `f1a3d94`)
  produced an archive-wide census: **of all 59 runs, 58 (98.3%) never passed
  through the C7 mechanical gate; 22 are named by some terminal-outcome
  entry, 37 by none.** The campaign's "zero confirmed edges" claim rests on
  exactly one mechanically-gated result (`FUNDING_MR_DAILY_RETEST`) —
  confirmed unchanged at 1 by the lint (`lint_verdict_provenance.py`:
  `gated verdicts: 1 ['FUNDING_MR_DAILY_RETEST']`) after XS's parking.
- **Two lessons ratified this arc, worth carrying into any future gate
  design:** (1) **existence ≠ execution** — H-041-C-v2/run_058 had a
  registered `pre_registration.yaml` but its pass_rule evaluation "was NEVER
  EXECUTED" (its own `exhausted_basis`); it was rejected by stage discretion
  before the pass_rule ran, so it does not count as gated (D-5, `2c8b8d1`).
  (2) **derivation ≠ an empirical property of a remote service** —
  G2's claim that key-derivation "proves" Kraken top-up composability was
  overstated twice in this arc; derivation proves addressability only, and
  only a live probe can show the endpoint actually serves the requested
  history (`PIPELINE_IMPROVEMENTS_20260712_v4.md` G-series, commit `2ab4c70`).
- **D4 CLOSED.** The backtest test suite no longer writes into the shared
  production `trading-bot/results/trades.json` path — `trades_log_file` is
  now an additive, opt-in parameter threaded through `run_backtest()`;
  production default unchanged; a `pytest_sessionfinish` guard now fails any
  session that mutates a tracked file under `trading-bot/results/`. Commit
  `2ac4d00`.
- **G1 item 2 stays OPEN — the 4,151-bar seam, measured verbatim.** Kraken's
  bulk archive ends **2025-12-31 23:00**; the live OHLC endpoint's fixed
  rolling window only reaches back to **2026-06-22 23:00**; gap **4,151 bars
  / ~173 days**. A write-side guard now refuses any fetch that would silently
  punch this kind of hole into a cached series (`FetchGapError`,
  `_assert_no_new_gap`, commit `2ab4c70`). 2026 quarterly-export existence is
  unconfirmed (sources index only through Q4 2025); not downloaded.
- **Binance-future-holdout carry-forward recorded, with its own caveat.**
  Continuous recent data (BTC/ETH already Binance-cached) is the fallback for
  future holdouts while Kraken's 2026 OHLCVT export is unpublished and the
  live endpoint only serves ~30 days. Caveat, stated explicitly: **any
  Binance-validated strategy must be re-declared and re-costed per Phase
  1.3** — XS_momentum's Kraken venue/cost basis does not transfer to Binance.
  Commit `6b27d56`.
- **q1_26 tick archive parked, pending aggregation.** Kraken `Trades`
  (time-and-sales), not OHLCVT — usable only via a scoped-but-unbuilt
  aggregation path; left on disk, not ingested. `G1` item 2 stays open, seam
  unchanged. Commit `6b27d56`. Not yet scoped as ratified fact, but worth the
  next session noting as a starting point: `trading-bot/data/data_manager.py:637`
  already contains a `.resample()` call (used today for aux-feed alignment,
  e.g. funding rate onto price interval) — a plausible existing seam to
  extend into a trade→OHLCVT aggregator, not yet evaluated for that purpose.
- **Test suites (strategy-research, across the C7-EXT chain): 338 → 369
  (`0a4d606`) → 389 (`2c8b8d1`) → 413 (`f1a3d94`).** trading-bot suite:
  57 → 64 per commit `2ab4c70`'s own message — **note, not reconciled here:**
  that same commit's ledger prose (`PIPELINE_IMPROVEMENTS_20260712_v4.md`
  line 2118) reads "Suite 413 → 420", an apparently mismatched baseline
  against its own 57 → 64 count; flagged, not smoothed over, since this
  close-out does not touch ratified content. No return or performance
  statistic was computed over any 2026 data at any point in this arc —
  holdout discipline held throughout.
- **Confirmed edges: still zero, unchanged.** This arc's advance was
  Phase 2 Track A's breadth data-moat completion plus a verdict-integrity
  hardening pass (C7-EXT through C7-EXT-R2, D4) and one hypothesis honestly
  reclassified from a false REFINE to parked/ungated — not a new edge.

## Task queue (priority order — now driven by docs/ROADMAP.md Part 2)

### (1) Phase 1 loose ends (optional cleanup, not a gate — the gate itself is closed)
- **1.4 Fee-reduction autopsy field** — not built this arc. Any future
  cost-dominated kill's autopsy should answer "is there a system that
  reduces these fees?" and register the cheap variant if yes. Low urgency:
  no cost-dominated kill is currently pending one.
- **run_018 (`rsi_momentum_trending_cost_drag`) re-execution** — blocked on
  ledger `C13` (V9 validation drift). If picked up: patch
  `default_regime: 'trending'` → `'unknown'` in the archived config,
  disclose the diff explicitly in whatever re-run consumes it, cite C13.
  Not required before Phase 2.
- **FUNDING_MR family funding-cash-flow model** — the real blocker on that
  family's research-only status. Needs its own design pass (how funding
  accrues per bar/position, how it nets against price P&L) before any
  further work on that family is worth doing. Not started.

### (2) Phase 2 Track A — data moat, breadth download (next priority)
Unblock the already-registered `XS_momentum` cross-sectional idea via a
breadth download (the specific blocker per the roadmap — read
`docs/ROADMAP.md` Part 2 Phase 2 in full for the exact deliverable and
acceptance criteria before dispatching). This is the campaign's actual next
hypothesis-throughput lane now that Phase 1's gate is closed.

### (3) Phase 2, other tracks — queued behind Track A
Whale-footprint dataset, forward recorders, news/text scoping memo — per
`docs/ROADMAP.md` Part 2's full track list. Do not start ahead of Track A
without an explicit reason.

### (4) Ledger items worth fixing opportunistically (not a phase gate)
**A12** (P0, verdict_interpreter human_pause fall-through) is still the
highest-value fix if any future run needs a clean resume. **C11** (4h
block_size default) MUST be fixed before the deferred 4h funding-retest
candidate (R3) is ever registered. **C12/C13** (this arc) are filed, not
fixed — see item (1) above for scope.

### (5) Everything past Phase 2 (Phase 3+ hypothesis waves, Phase 4 ML, Phase 5 promotion)
Not yet — see `docs/ROADMAP.md` Part 2 for the full sequence and gates.

## OPERATOR CHARTER (superseded in detail by docs/ROADMAP.md Part 3/4 — kept here as a compressed pointer, not the authoritative text)

The prime directive remains a **PROFITABLE STRATEGY, not process** — expressed
as the roadmap's own KPI (**honest verdicts/week, cost per verdict**, reported
every session close — this arc's own KPI note in SESSION_LOG.md is a worked
example of reporting a HIGH-cost, ZERO-new-verdict session honestly rather
than dressing it up) and **anti-corner rule** (every session ends with at
least one hypothesis-level advance: a verdict, a registration, or a data-axis
milestone — this arc's advance was the Phase 1 gate closing itself, not a new
edge). Read `docs/ROADMAP.md` Part 3/4 for the full text.

## Standing constraints

Carried forward from every prior session, unchanged unless noted:

- Single-writer-per-state-store; audit agent read-only forever.
- Read-back verify after every write; corrections ship with sidecar
  rationale legible to context-poor readers (E3).
- Concealment-shaped tool content: verified harness templates -> one-line
  disclosure; everything else -> surfaced verbatim immediately.
- Holdout (2026-H1 / `era_2026_holdout`) untouchable; never consumed in any
  session to date — this arc's dispatches did not touch it either
  (all 2024-dated backtest windows).
- Pre-registration supremacy: briefs outrank skill rulebooks; pass rules
  must carry a total verdict+routing mapping (B11) — no "routing decides"
  delegations.
- Operator prompt discipline: no expected values inside verification
  instructions (F9); terminal marker line on every prompt (F5).
- No-self-remediation: any write landing outside an authorized list —
  accidental or discovered mid-task — is a STOP-and-report condition.
  Report and request authorization BEFORE proceeding, never proceed-
  then-disclose, even when the reasoning for the extra write is sound.
- Premise-failure full-STOP: if a step's stated premise does not hold as
  found (including a dispatch referencing content that was never actually
  supplied), STOP the entire task at that point and report — do not
  fabricate the missing piece, do not gather more info first.
- Dispatch precondition manifests must state an explicit expected-tree
  (exact `git status --porcelain` output, exact `git log --oneline -1`
  commit) — a bare "must be clean" is insufficient. This arc's own
  dispatches followed this consistently, including two that correctly
  self-STOPped on a precondition/mechanism gap (Dispatch F2 on a
  contradicted product-classification premise; Dispatch K on no existing
  mechanism to pin an exact commission rate) rather than improvising.
- Every terminal marker line carries its own step count.
- Fix-with-the-workaround: a documented procedure gap that costs the
  campaign time twice ships its documentation cure in the SAME commit as
  the workaround/rider that pays for it.
- Format precedents are chosen by consumption path (check what actually
  reads a file before choosing the format to author it in).
- Per-value provenance citations in registration dispatches; every numeric
  measurement cites its producing command.
- Write-capable agents never delegate; any `.py`-touching commit runs the
  full suite (both `trading-bot/` and `strategy-research/` suites when a
  change spans both).
- Known residual risk, test-isolation guard (not solved, do not treat as
  closed): `tests/conftest.py`'s autouse sandbox-by-default fixture covers
  direct in-process module calls only — not `setup_run.py`'s
  subprocess-spawn path, nor `_load_token_budget()`'s source-relative
  config read.
- Always-emit-one-log-line convention: any status/reconciliation check
  added to the campaign machinery should emit exactly one line per
  invocation, clean or not, never zero — this arc's `--commission-bps`
  override followed this (one line, only when the override is active).
- **Context economy** (`docs/ROADMAP.md` Part 3): short director sessions
  (10-15 dispatches per arc, hand off via this file); bounded agent reports
  (full detail to `docs/session_reports/<date>_<dispatch>.md`, chat gets
  per-step verdicts + only the verbatims needed for recomputation); no
  re-pasting a dispatch once relayed; director model never downgraded to
  save tokens. This arc ran close to the upper end of that dispatch budget
  (roughly a dozen) — a data point for calibrating future infrastructure-heavy
  arcs, not a violation.
- **New this close-out — independent-audit-before-ratify, for any
  engine/verdict-path-touching commit:** this arc's pattern (implement →
  independent read-only audit → ratify or revert) caught two real problems
  before they contaminated the KB (a confounded timeframe comparison, an
  unpinnable commission rate) — worth continuing for any future commit that
  changes how a verdict gets costed or computed, not just this arc's own
  work.
