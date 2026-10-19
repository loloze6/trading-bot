"""FOLD-FLOORS-2026-10-19 (ii): re-grade the three recorded fold confirmations with each
claim's own floor applied. No backtest, no record changed, nothing written except --out.

Reads, for each child run, COPIES of its saved outputs (point --runs at a folder holding
<run>/artifacts/{hypothesis_card.yaml, fold_confirmation.yaml, variants/base/protocol_result.yaml}
and <run>/variants/base/{trade_diagnostics.json, results/<rid>/{bars.csv, trades.json}}).
Re-measures the claim's test with the UNCHANGED claim_measure.measure_test (trade family on,
as fold_confirm.measure_on_fold does for one coin), asserts that every per-window and pooled
value equals the recorded fold_confirmation.yaml, then adds what the record does not carry:
the per-window counts (selected trades with an outcome, baseline trades with an outcome) and
applies the candidate rules of fold_floor_sim.py.

Run (from the repo root, the venv's interpreter):
  python strategy-research/engineering/FOLD-FLOORS-2026-10-19/regrade.py --runs <copies> --out <file>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[1] / "tools"
for p in (str(TOOLS), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import claim_measure as cmeas  # noqa: E402
import claim_tests as ct  # noqa: E402
import fold_confirm as fcf  # noqa: E402
import fold_floor_sim as sim  # noqa: E402

RUNS = ("run_096", "run_079", "run_078")
VID = "base"


def regrade(run_dir: Path) -> dict:
    arts = run_dir / "artifacts"
    card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
    rec = yaml.safe_load((arts / "fold_confirmation.yaml").read_text(encoding="utf-8"))
    (test,) = card["claim"]["tests"]
    floor = dict(test["floor"])
    tws = ct.load_variant_trade_windows(run_dir, VID)
    keep = set(rec["fold_blocks"])
    tws = [tw for tw in tws if tw.window in keep]
    res = cmeas.measure_test(tws, test, None, True)
    spec, _h = cmeas.test_spec(test, True)
    per, _out_h, horizons, _rng = ct.effect_sizes(tws, spec, None)
    graded = fcf.grade_test(res)
    rtest = rec["tests"][test["name"]]
    # 1. the re-measurement IS the recorded one
    assert graded["status"] == rtest["status"] == fcf.CONFIRMED, (graded["status"], rtest["status"])
    for h, x in graded["horizons"].items():
        rx = rtest["horizons"][str(h)]
        assert x["n_events"] == rx["n_events"], (h, x["n_events"], rx["n_events"])
        assert abs(x["oriented"] - rx["oriented"]) < 1e-12
        for lab, v in x["per_window"].items():
            assert abs(v - rx["per_window"][lab]) < 1e-12, (h, lab)
    # 2. the per-window counts the record does not carry
    out_h, sim_h = {}, {}
    for h in horizons:
        rows, nev, nref = {}, {}, {}
        for p in per:
            y = p["ys"][h]
            ns = int((p["mask"] & np.isfinite(y)).sum())
            nr = int(((p["wref"] > 0) & np.isfinite(y)).sum())
            o = res["horizons"][h]["per_window"][p["w"].label]["oriented"]
            rows[p["w"].label] = {"n_selected": ns, "n_baseline": nr, "oriented": o,
                                  "claimed_sign": None if o is None else bool(o > 0)}
            nev[p["w"].label], nref[p["w"].label] = ns, nr
        r = res["horizons"][h]
        out_h[str(h)] = {"pooled_oriented": r["oriented"], "n_events": r["n_events"],
                         "n_windows_with_events": r["n_windows_with_events"], "windows": rows}
        sim_h[h] = {"oriented": r["oriented"], "n_events": r["n_events"],
                    "n_windows_with_events": r["n_windows_with_events"],
                    "per_window": {k: {"oriented": v["oriented"]} for k, v in rows.items()},
                    "_nev": nev, "_nref": nref}
    sres = {"status": res["status"], "horizons": sim_h}
    n_fold = len(rec["fold_blocks"])
    m_claim = -(-floor["min_events"] // n_fold)          # ceil(min_events / fold windows)
    rules = {
        "R0_current": sim.rule_r0(res),
        "R5_pooled_floor_fold_denominator": sim.rule_window_floor(sres, 1, n_fold, True, floor=floor),
        "R1_pooled_floor": sim.rule_pooled_floor(sres, floor),
        "R2_window_floor_against_m10": sim.rule_window_floor(sres, 10, n_fold, True, floor=floor),
        f"R2_window_floor_against_m{m_claim}": sim.rule_window_floor(sres, m_claim, n_fold, True,
                                                                     floor=floor),
        f"R3_window_floor_dropped_m{m_claim}": sim.rule_window_floor(sres, m_claim, n_fold, False,
                                                                     floor=floor),
        "R2_window_floor_against_m100": sim.rule_window_floor(sres, floor["min_events"], n_fold,
                                                              True, floor=floor),
        "R4_all_windows": sim.rule_all_windows(sres),
    }
    return {"claim": rec["finding_id"], "run": rec["run_id"], "fold": rec.get("fold"),
            "test": test["name"], "statistic": test["statistic"], "direction": test["direction"],
            "outcome": test["outcome"]["kind"], "floor": floor,
            "claim_measure_floor_not_met": res["floor_not_met"],
            "recorded_status": rec["status"], "remeasured_equal_to_record": True,
            "horizons": out_h, "rules": {k: "confirmed" if v else "not confirmed"
                                         for k, v in rules.items()}}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    out = [regrade(a.runs / r) for r in RUNS]
    a.out.write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
    for r in out:
        print(r["claim"], r["run"], r["rules"])
        for h, x in r["horizons"].items():
            print(f"  h={h} pooled {x['pooled_oriented']:+.5f} n={x['n_events']} ",
                  {k.split('/')[-1]: (v['n_selected'], v['n_baseline'], v['claimed_sign'])
                   for k, v in x["windows"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
