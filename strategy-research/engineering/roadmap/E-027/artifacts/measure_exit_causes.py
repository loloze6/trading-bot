"""
Decompose every APPROVED allocation move recorded in a run's bars.csv.

Reads only artifacts every backtest already writes -- no engine change, no
re-run. Written as the evidence for E-027; the shipped instrument replaces it.

WHY THE TAXONOMY IS MOVE-SHAPED, NOT EXIT-SHAPED (corrected 2026-08-21):
an earlier version of this script counted only "position went to exactly zero"
and called that an exit. That is close to circular -- target allocation is a
linear function of the forecast through the origin, so realized allocation can
only reach zero when the forecast is zero. It measured a definition and
reported it as a finding. The engine expresses a changed view three other ways,
all of which are real exits or partial exits and none of which touch zero:

  sign_flip        pre and post have opposite signs -- the strategy reversed.
                   In LIFO trade terms this is a full close plus an open.
  partial_reduce   |post| < |pre|, same sign -- the forecast fell, so part of
                   the position was closed.
  increase         |post| > |pre|, same sign -- added to the position.
  open_from_flat   pre == 0, post != 0.
  full_exit_to_zero post == 0 -- the only category where the forecast must have
                   been zero. THREE different causes collapse into it and the
                   artifacts cannot separate them:
                     (a) regime has no strategy block
                         -> strategy_engine.py `if cfg is None: return 0.0`
                     (b) a component in a MAPPED regime is not ready
                         -> `return 0.0, {"not_ready_component": cid}`
                     (c) the ensemble genuinely computed 0.0
                   Separating them is E-027's deliverable, not something this
                   script can do from bars.csv.

Usage:  python engineering/roadmap/E-027/artifacts/measure_exit_causes.py <run_id> [...]
        (cwd = strategy-research/)
"""

import csv
import glob
import sys


def _f(row, key):
    try:
        return float(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


CATS = ("open_from_flat", "full_exit_to_zero", "sign_flip", "partial_reduce", "increase")


def measure(run, quiet=False):
    t = {c: 0 for c in CATS}
    bars = switches = attempts = refused = off_bars = moves = nonzero_fc_moves = 0
    zero_labels = {}
    mapped_zero_bars = 0

    for path in sorted(glob.glob(f"runs/{run}/results/*/bars.csv")):
        prev_regime = None
        with open(path, encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                bars += 1
                regime = (row.get("regime") or "").strip()
                if regime in ("unknown", "NOT_READY", ""):
                    off_bars += 1
                if prev_regime is not None and regime != prev_regime:
                    switches += 1
                prev_regime = regime

                approved = (row.get("approved_rebalance") or "").strip().lower() in ("true", "1")
                if _f(row, "allocation_change") != 0.0:
                    attempts += 1
                    if not approved:
                        refused += 1
                if regime not in ("unknown", "NOT_READY", "") and _f(row, "forecast") == 0.0:
                    mapped_zero_bars += 1
                if not approved:
                    continue

                pre, post, fc = (
                    _f(row, "previous_allocation"),
                    _f(row, "postRebalance_current_allocation"),
                    _f(row, "forecast"),
                )
                if abs(pre - post) < 1e-12:
                    continue
                moves += 1
                if fc != 0.0:
                    nonzero_fc_moves += 1

                if abs(pre) < 1e-9 and abs(post) > 1e-9:
                    t["open_from_flat"] += 1
                elif abs(post) < 1e-9:
                    t["full_exit_to_zero"] += 1
                    key = (regime, (row.get("strategy") or "").strip() or "<none>")
                    zero_labels[key] = zero_labels.get(key, 0) + 1
                elif pre * post < 0:
                    t["sign_flip"] += 1
                elif abs(post) < abs(pre):
                    t["partial_reduce"] += 1
                else:
                    t["increase"] += 1

    if not quiet:
        pct = lambda n, d: (100.0 * n / d) if d else 0.0
        print(f"{run}: bars={bars}  regime_switches={switches}  strategy_off={pct(off_bars, bars):.0f}% of bars")
        print(f"   approved allocation moves = {moves}")
        for c in CATS:
            print(f"     {c:18s}: {t[c]} ({pct(t[c], moves):.0f}%)")
        print(f"   moves made with a NONZERO forecast: {nonzero_fc_moves} ({pct(nonzero_fc_moves, moves):.0f}%)")
        print(f"   rebalance attempts={attempts}  refused_by_risk_band={refused} ({pct(refused, attempts):.0f}%)")
        print(f"   regime label at each full_exit_to_zero: {zero_labels}")
        print(f"   CONTROL -- bars in a MAPPED regime whose forecast was 0.0: {mapped_zero_bars}")
        print()
    return t, moves, nonzero_fc_moves, attempts, refused


if __name__ == "__main__":
    ids = sys.argv[1:]
    agg = {c: 0 for c in CATS}
    m = nz = at = rf = 0
    for run_id in ids:
        t, mo, n, a, r = measure(run_id)
        for c in CATS:
            agg[c] += t[c]
        m += mo
        nz += n
        at += a
        rf += r
    if len(ids) > 1:
        pct = lambda n_, d_: (100.0 * n_ / d_) if d_ else 0.0
        print("=" * 62)
        print(f"AGGREGATE over {len(ids)} runs")
        print(f"  approved allocation moves          : {m}")
        for c in CATS:
            print(f"    {c:18s}: {agg[c]} ({pct(agg[c], m):.0f}%)")
        print(f"  moves with a NONZERO forecast      : {nz} ({pct(nz, m):.0f}%)")
        print(f"  rebalance attempts / refused       : {at} / {rf} ({pct(rf, at):.0f}%)")
