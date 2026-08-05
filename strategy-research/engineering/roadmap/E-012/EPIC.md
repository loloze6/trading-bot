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

- [x] S1 — **MEASURE FIRST, before any fix is designed.** Run the reference
      backtest with and without the loop fix; compare all five artifact files;
      record the P&L delta. Rationale: fix-forward invalidates cross-line
      comparisons, and every pre-registered pass rule is pinned to pre-fix
      baselines (e.g. P4_ts_trend against run_054: BTCUSDT >= 0.5791,
      ETHUSDT >= 0.0318 median Sharpe). If the delta is negligible, those
      thresholds survive; if not, they must be re-derived. The director's
      expectation that 2/1440 bars is negligible is an ESTIMATE and must not
      be recorded as a finding.

      **DONE, by the fork.** FALSIFIED: measured on the position-ending
      window (below), not negligible. The "2 bars in 1440 is noise" estimate
      does not hold whenever the window ends holding a position.
- [ ] S2 — Fix the manifest to report bars replayed rather than rows loaded.
      Changes no trade, return, or Sharpe — metadata only.
- [ ] S3 — Fix the loop's two off-by-one errors. Operator ruling: fix forward,
      do NOT re-run history. Record a dated line in the sand — results before
      it used the truncated behaviour and stay comparable among themselves.

      **Ruling unchanged, now rests on measurement rather than instinct** (S1
      delta below), not on the original fix-forward instinct alone.
- [ ] S4 — Sequence against E-010 (slippage model), whose Done-when pins
      `config_sha 5ccbec42` / `data_sha 5a75366c`. Either fix here breaks
      those pins.
- [ ] S5 — Re-derive the run_054 baselines under the fixed loop, BEFORE any
      P4 evaluation. See "P4 threshold invalidation" and "Anti-fitting
      guardrail" below.

## P4 threshold invalidation (2026-08-05)

**Measured:** 15 of 30 run_054 windows end holding a position (BTCUSDT 8
flat / 7 holding, ETHUSDT 7 flat / 8 holding). Method: a genuine
`_close_all_positions_at_end` leaves `exit_forecast:null` on the trade plus a
duplicate-timestamp `bars.csv` row with a blank forecast and
`trade_type CLOSE`; a signal exit landing on the final bar writes a single
row with a populated forecast. Worked example: window
`20260709T134348Z_d01f26e1`.

**Consequence:** the pre-registered pass rule pinned to run_054
(BTCUSDT >= 0.5791, ETHUSDT >= 0.0318 median Sharpe) was computed with half
its windows containing an artificial force-close. Those thresholds do NOT
survive the loop fix and must be re-derived.

**Direction unknown per window.** The director's hypothesis: a strategy's
own signal exit should on average beat an arbitrary forced one, so
re-derived thresholds may rise. This is a HYPOTHESIS, not measured.

## Anti-fitting guardrail (S5)

Re-deriving a threshold that a strategy will then be tested against is
structurally identical to fitting unless the ORDER is enforced. Therefore:

- The re-derivation is mechanical: rerun run_054 under the fixed loop,
  recompute the same medians over the same 15-window sets, change nothing
  else.
- The new thresholds are FROZEN and recorded BEFORE P4 is run.
- No P4 result may be compared against a threshold derived after seeing it.

This is NOT a relaxation: the coverage floor, min-N, and `persistence_bars`
are untouched and remain non-negotiable. Any session that proposes loosening
them is refused.

## S1 measurement (2026-08-05, fork)

Source: fork probe branch `lab/e012-s1-probe` (probe commit `23aa31e6`, parent
`a233030c`, never merged), TRIALS `T003`/`T004`, fork `research/LEDGER.md`
2026-08-05 (afternoon) entry, recorded to git at commit `5724a3f9`, mirrored
to the E-012 Notion ticket. Triple-verified: executor, independent verifier
regeneration, red-team re-run; no lookahead (funding-boundary discriminating
test passed).

**The delta is CONDITIONAL on how the window ends — it is not one number.**

- **Flat-ending reference window (T003):** bookkeeping only. `trades.json`
  byte-identical; `config_sha`/`data_sha` both unchanged; manifest `bar_count`
  finally reconciles with `bars.csv` at 1440 (was 1438). Only the
  off-by-default `bar_equity` block moves: `exposure_pct` 3.7908 → 3.785.
- **Position-ending window, 2024-09-15 → 10-05 (T004):** the two dropped bars
  carried a genuine exit signal. Unpatched force-closes at a STALE 21:00
  price (61857.64) with 22:00/23:00 sitting unread; patched self-exits on a
  real signal at 22:00 (62039.52). Net −8.446 → −7.907, Sharpe −7.585 →
  −7.018, win rate 41.18 → 47.06 — same 17 trades, same maxDD both legs.

**The fix is THREE edits, not two.** The previously characterized pair
(relax `has_more_data`; flush the end-of-replay candle through
`close_final_candle`/`_complete_candle`) does not terminate on its own:
`advance()` parks the cursor ON the last row, so relaxing `has_more_data`
alone re-feeds that final row indefinitely and corrupts the final candle's
volume/tick count (proven by bounded simulation). The third edit parks the
cursor past the end.

**Rebaseline scope is 10 tests, not 9:** the 9 fast tests in
`test_close_positions_at_end` plus the slow `bar_equity` reference test.
**Trap recorded:** post-fix, that file's fixture window no longer ends
holding a position — its premise dissolves, so its two nominal
"survive" tests would pass VACUOUSLY, silently dropping the only coverage
for the two `_close_all_positions_at_end` NameErrors. A new
position-ending fixture window is required before the fix lands, not
after.

## Log

- 2026-08-04 — `new`. Filed as an epic (dispatch W31): the fix touches shared
  structure (manifest semantics in `run_artifact.py`, the replay loop) and
  needs more than one dispatch. Done-when left unwritten pending the joint
  decision noted above.
- 2026-08-05 — S1 measurement recorded (dispatch W40) from the fork's
  triple-verified delta. See "S1 measurement" above. S3's fix-forward ruling
  stands, now evidenced rather than assumed.
- 2026-08-05 — P4 threshold invalidation and S5 anti-fitting guardrail
  recorded (dispatch W41). run_054's pass-rule thresholds are invalid
  post-loop-fix and must be re-derived under the frozen-before-P4 order
  above; not yet done.
