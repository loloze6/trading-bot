# E-014 — Venue-parameterized cost model + calibration re-runs

**State:** in-progress
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §1.2, verbatim: "**Venue-parameterized cost model +
calibration re-runs.** Objective: backtests price the venue we'd actually
use. Deliverable: the cost model takes the venue's real fee schedule (incl.
maker-order assumptions where realistic); then **3 automated calibration
re-runs** of already-tested ideas (the funding retest + 2 archived
near-misses) under the new fee model — objective of these runs: measure how
much verdicts move on fees alone, i.e. how many 'kills' were venue
artifacts."

**VERIFIED (dispatch W38, tree audit) — this work already partially shipped
before this epic existed:**

- A Kraken perp fee block shipped 2026-07-20 (`d86f0d0`), selected via
  `run_protocol.py`'s `--cost-product` flag (`_commission_rate_for_symbol`),
  with 8 tests (`tests/test_run_protocol_perp_cost_wiring.py`). This is a
  hardcoded *alternate venue*, not a parameter: `--cost-product` accepts
  exactly `{spot, perp}`, and `perp` resolves to one fixed Kraken block in
  `config/cost_model.yaml`. Done-when #1 ("takes a venue-specific fee
  schedule as a parameter") is NOT met by this — there is one venue swap
  hardcoded, not a parameterization over venues.
- `config/cost_model.yaml`'s `execution_style` block (maker/taker variants)
  exists on disk but is NOT read by any code path — the file's own header
  comment states the top-level keys "are the only keys `prescreen_signal.py`
  and `run_protocol.py` consume today (taker path)." The maker-order
  assumption half of Done-when #1 is unwired.
- `run_028`/`run_030`'s perp-cost recalibrations (also under `d86f0d0`) DID
  execute, but were independently AUDIT FAILED
  (`docs/session_reports/20260720_perp_calibration_audit.md`, Dispatch J):
  the candle interval silently moved 1h→4h between the original runs and the
  perp re-run (a pre-existing `run_protocol.py` timeframe-threading gap,
  unrelated to the fee change), so neither re-run isolates the fee effect —
  its own verdict line reads "AUDIT FAIL... neither is ratifiable as a
  measurement of the cost change's effect." These do NOT satisfy Done-when
  #2/#3.
- A later, separate, genuinely clean experiment exists —
  `keltner_scoremode_fee_isolation_no_flip` (`campaign_knowledge_base.yaml`)
  — which holds timeframe/window/config fixed and varies only the commission
  rate via `run_protocol.py`'s `--commission-bps` override (commit
  `e3bcbb0`), independently audited PASS
  (`docs/session_reports/20260720_pairs_audit.md`, Dispatch M). This is a
  real, ratifiable result, but it is a bps-sensitivity probe on `run_028`/
  `run_030` only — it is not "the funding retest + 2 archived near-misses"
  the source text describes (no funding-costed re-run exists; perp funding
  cash flows are explicitly NOT modeled per `cost_model.yaml`'s own note),
  and it does not by itself satisfy "under the new fee model" (it never
  invokes `--cost-product=perp`; it overrides a flat bps instead). It should
  not be read as closing Done-when #2/#3.

**Dependency on E-010 — VOID, now OPEN:** the prior text asserted E-014
needed E-010's fee/slippage-attribution seam first (director's sequencing
call, recorded when this epic was created 2026-08-05). That reasoning is
void: the 2026-07-20 work above shipped a full year-quarter before E-010 was
even surfaced (E-010 was created 2026-08-03, still `new`/unstarted per its
own EPIC.md as of this correction) and did so without any fee/slippage
attribution seam from E-010. Whether E-014's *remaining* work should still
sequence behind E-010 is OPEN and unresolved — not decided here.

## Done when

1. The cost model takes a venue-specific fee schedule as a genuine
   *parameter* (today: one hardcoded alternate venue, Kraken perp, selected
   by a two-value flag) — including wiring the existing but unread
   `execution_style` maker/taker block into an actual code path.
2. The two archived near-misses are re-run under the parameterized venue fee
   model WITHOUT the 1h→4h interval confound that invalidated the original
   `run_028`/`run_030` perp recalibrations (i.e., redo Dispatch J's audit-failed
   re-runs correctly — hold timeframe fixed, as `keltner_scoremode_fee_isolation_no_flip`
   already demonstrates is achievable).
3. The funding retest executes under a fee model that includes funding cash
   flows, not fee-only pricing — `cost_model.yaml`'s `perp.funding.modeled` is
   currently `false`; a funding-costed re-run does not yet exist and is
   in scope here.
4. For each of the 3 re-runs, the verdict movement attributable to fees alone
   (or, for the funding retest, fees+funding) is measured and recorded.

## Stories

- [ ] S1 — Turn the venue fee schedule into a real parameter (not a
      `{spot, perp}` flag) and wire `execution_style` maker/taker into the
      code path that consumes it.
- [ ] S2 — Redo the two archived-near-miss re-runs under the parameterized
      model without the interval confound (building on the
      `--commission-bps`-controlled-pair method already proven clean by
      Dispatch M).
- [ ] S3 — Build and run the funding-costed retest (the perp `funding` block
      is currently off-by-default and unexercised); record its verdict delta.

## Log

- 2026-08-05 — `new`. Created from E-013 S1's audit of `docs/ROADMAP.md` §1.2
  (dispatch W35). Dependency on E-010 recorded per the audit's sequencing
  finding; not started.
- 2026-08-05 — `new` → `in-progress` (dispatch W38). Tree audit found S1's
  cost-parameterization work partially shipped (`d86f0d0`) before this epic
  existed, and found the epic's own claimed calibration re-runs (`run_028`/
  `run_030` perp recalibration) independently AUDIT FAILED for an interval
  confound — not usable as evidence toward Done-when #2. The E-010 dependency
  claim was deleted as void (work shipped before E-010 existed); whether it
  should still apply to the *remaining* work is left OPEN. Done-when rewritten
  to name the real gaps: venue as a parameter (not a hardcoded flag),
  `execution_style` wiring, a confound-free redo of the near-miss re-runs, and
  a funding-costed retest that doesn't yet exist.
