# E-012 — Two-bars manifest/loop defect

**State:** new
**Owner:** Jeremy + Dorian
**Updated:** 2026-08-04

## Why

Source: Notion ticket `3ae1d1fb05a281cf8ff8f281e409741c` ("Backtests never
trade the last two fetched bars"). Not sourced to Slack prose — W30 found
Dorian's Slack account of this does not reconcile to the board.

MEASURED figures only:

- Root cause: `reporting/run_artifact.py` builds the manifest from the
  LOADED frame, so it reports rows loaded, not bars replayed. Two independent,
  additive off-by-ones in the replay loop itself: `has_more_data`
  (`data_manager.py:816`) exits parked on the final in-memory row before it is
  fed, and a candle only completes when a *later* row arrives (`:355`/`:364`),
  so the last fed row opens a candle that never closes.
- Fork reference run: manifest reports 1440, `bars.csv` holds 1438.
- 41 of 46 archived upstream runs show delta exactly 2; all 46 end at 21:00.
- Upstream `SESSION_LOG` recorded the symptom unremarked and unactioned
  (2026-07-26).

## Done when

**Left blank.** This needs a joint Jeremy/Dorian decision (E-004 precedent —
shared record taxonomy). A criterion invented here, before that decision, would
be fiction: whether the manifest fix and the loop fix land together or
separately, and how the pre-fix/post-fix baselines are dated apart, are calls
neither person owns unilaterally.

## Stories

- [ ] S1 — **MEASURE FIRST, before any fix is designed.** Run the reference
      backtest with and without the loop fix; compare all five artifact files;
      record the P&L delta. Rationale: fix-forward invalidates cross-line
      comparisons, and every pre-registered pass rule is pinned to pre-fix
      baselines (e.g. P4_ts_trend against run_054: BTCUSDT >= 0.5791,
      ETHUSDT >= 0.0318 median Sharpe). If the delta is negligible, those
      thresholds survive; if not, they must be re-derived. The director's
      expectation that 2/1440 bars is negligible is an ESTIMATE and must not
      be recorded as a finding.
- [ ] S2 — Fix the manifest to report bars replayed rather than rows loaded.
      Changes no trade, return, or Sharpe — metadata only.
- [ ] S3 — Fix the loop's two off-by-one errors. Operator ruling: fix forward,
      do NOT re-run history. Record a dated line in the sand — results before
      it used the truncated behaviour and stay comparable among themselves.
- [ ] S4 — Sequence against E-010 (slippage model), whose Done-when pins
      `config_sha 5ccbec42` / `data_sha 5a75366c`. Either fix here breaks
      those pins.

## Log

- 2026-08-04 — `new`. Filed as an epic (dispatch W31): the fix touches shared
  structure (manifest semantics in `run_artifact.py`, the replay loop) and
  needs more than one dispatch. Done-when left unwritten pending the joint
  decision noted above.
