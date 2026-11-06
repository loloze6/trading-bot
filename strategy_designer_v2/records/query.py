"""One query over v2's records: every run, its claims, verdicts, engine results and model cost.
Usage: python3 records/query.py [--md]   (prints a table; --md prints markdown). Code only."""
import sys, pathlib, yaml

HERE = pathlib.Path(__file__).resolve().parent.parent


def runs():
    for brief_dir in sorted((HERE / "runs").glob("*/")):
        for run_dir in sorted(brief_dir.glob("*/")):
            if not (run_dir / "claims.yaml").exists():
                continue
            claims, verdicts = [], {}
            for cp in sorted(run_dir.glob("claims*.yaml")):
                vp = run_dir / ("verdicts.yaml" if cp.stem == "claims" else f"verdicts_{cp.stem}.yaml")
                if not vp.exists():
                    continue
                v = yaml.safe_load(vp.read_text()); vd = v["ideas"]; verdicts.update(vd)
                claims += [{"id": i["id"], "round": cp.stem, "measure": i["claim"]["measure"], "verdict": vd[i["id"]]["verdict"]}
                           for i in yaml.safe_load(cp.read_text())["ideas"]]
            cost = sum((r.get("cost_usd") or 0) for r in (yaml.safe_load((run_dir / "model_calls.yaml").read_text()) if (run_dir / "model_calls.yaml").exists() else []))
            engine = {p.parent.name: yaml.safe_load(p.read_text()) for p in run_dir.glob("engine_*/engine_verdict.yaml")}
            fold = None
            if (run_dir / "record.yaml").exists():
                fold = yaml.safe_load((run_dir / "record.yaml").read_text()).get("fold")
            yield {"run": f"{brief_dir.name}/{run_dir.name}", "fold": fold, "done": (run_dir / "DONE").exists(), "claims": claims,
                   "passes": [c["id"] for c in claims if c["verdict"] == "pass"], "cost_usd": round(cost, 2), "engine": engine}


def main():
    md = "--md" in sys.argv
    rows = list(runs())
    head = ["run", "fold", "claims", "pass", "engine", "cost USD", "done"]
    out = []
    for r in rows:
        eng = ", ".join(f"{k.split('_', 2)[-1]}: {v['verdict']} (net {v['fold_totals']['net_return']:+.1%}, sharpe {v['fold_totals']['median_window_sharpe']})"
                        for k, v in r["engine"].items()) or "-"
        out.append([r["run"], r["fold"] or "?", str(len(r["claims"])), ", ".join(r["passes"]) or "0", eng, f"{r['cost_usd']:.2f}", "yes" if r["done"] else "no"])
    if md:
        print("| " + " | ".join(head) + " |"); print("|" + "---|" * len(head))
        for o in out: print("| " + " | ".join(o) + " |")
    else:
        for o in out: print("  ".join(o))
    tot_claims = sum(len(r["claims"]) for r in rows); tot_pass = sum(len(r["passes"]) for r in rows); tot_cost = sum(r["cost_usd"] for r in rows)
    print(f"\nruns {len(rows)}, claims {tot_claims}, pass {tot_pass}, model cost {tot_cost:.2f} USD")
    shelf = yaml.safe_load((HERE / "records" / "shelf.yaml").read_text())["validated"] if (HERE / "records" / "shelf.yaml").exists() else []
    print(f"shelf: {len(shelf)} validated ({sum(1 for s in shelf if s['kind']=='book')} books, {sum(1 for s in shelf if s['kind']=='filter')} filters)")


if __name__ == "__main__":
    main()
