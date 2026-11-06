"""Information for the record: the lite book check (steps/profit/profit.py, enter at the event bar's close, hold the
horizon, pay the cost) for every judge-passed return claim of every run, per symbol. Seconds per claim, no model, no engine.
Asked by the night's runs: ten judge passes failed the engine; this number says in advance which are worth the engine's time."""
import sys, pathlib, yaml
HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "steps" / "profit")); sys.path.insert(0, str(HERE / "steps" / "judge"))
import profit as P  # noqa: E402

RETURN = {"mean_diff", "hit_rate", "net_return"}
rows = []
for run_dir in sorted(HERE.glob("runs/*/*/")):
    if not (run_dir / "record.yaml").exists():
        continue
    rec = yaml.safe_load((run_dir / "record.yaml").read_text()); fold, bar = rec.get("fold"), rec.get("bar_size")
    for cp in sorted(run_dir.glob("claims*.yaml")):
        vp = run_dir / ("verdicts.yaml" if cp.stem == "claims" else f"verdicts_{cp.stem}.yaml")
        if not vp.exists():
            continue
        v = yaml.safe_load(vp.read_text())["ideas"]
        for i in yaml.safe_load(cp.read_text())["ideas"]:
            if not isinstance(i, dict) or not isinstance(i.get("claim"), dict) or i["claim"].get("measure") not in RETURN:
                continue
            for s, r in v.get(i.get("id"), {}).get("by_symbol", {}).items():
                if r.get("verdict") != "pass":
                    continue
                out = run_dir / f"lite_{cp.stem}_{i['id']}_{s}.yaml"
                try:
                    res = yaml.safe_load(out.read_text()) if out.exists() else P.profit_claim(cp, i["id"], fold, bar, s, out_path=out, try_name=f"lite/{run_dir.parent.name}")
                    t = res["fold_totals"]; rows.append((run_dir.parent.name, i["id"], s, t["sharpe"], t["net_return"], t["max_drawdown"], res["verdict"]))
                except Exception as exc:  # noqa: BLE001
                    rows.append((run_dir.parent.name, i["id"], s, None, None, None, f"error: {type(exc).__name__}"))
(HERE / "records" / "lite_books.yaml").write_text(yaml.safe_dump([{"run": a, "claim": b, "symbol": c, "lite_sharpe": d, "lite_net": e, "lite_dd": f, "lite_verdict": g} for a, b, c, d, e, f, g in rows], sort_keys=False))
for r in rows:
    print(f"{r[0]:45s} {r[1]:45s} {r[2]:8s} sharpe={r[3]} net={r[4]} dd={r[5]} {r[6]}")
print(f"{len(rows)} judge-passed books checked")
