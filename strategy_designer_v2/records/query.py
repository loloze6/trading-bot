"""One query over v2's records: every run, its claims with branch 1 and branch 3 per symbol, and the model cost.
Usage: python3 records/query.py [--md]. Runs from before the engine-only loop have no branch fields: labelled "old shape"."""
import sys, pathlib, yaml

HERE = pathlib.Path(__file__).resolve().parent.parent
f = lambda x, p=2: "-" if x is None else f"{x:+.{p}f}" if isinstance(x, (int, float)) else str(x)


def rows():
    for rp in sorted((HERE / "runs").glob("*/*/record.yaml")):
        run_dir, rec = rp.parent, yaml.safe_load(rp.read_text()) or {}
        cl = rec.get("claims") or []
        cost = sum((r.get("cost_usd") or 0) for r in (yaml.safe_load((run_dir / "model_calls.yaml").read_text()) if (run_dir / "model_calls.yaml").exists() else []))
        new = bool(cl) and "verdict_branch1" in cl[0]
        det = "; ".join(f"{c['id']} " + ", ".join(f"{s}: b1 {x['branch1']['verdict']} ic {f(x['branch1']['fold_correlation'], 3)} / b3 {x['branch3']['verdict']} net {f(x['branch3']['net'], 3)}"
                                                     for s, x in c["by_symbol"].items()) for c in cl) if new else "old shape"
        yield [f"{rp.parent.parent.name}/{run_dir.name}", str(rec.get("fold") or "?"), str(len(cl)), str(sum(c.get("verdict_branch1") == "pass" for c in cl)) if new else "-",
               str(sum(c.get("verdict_branch3") == "pass" for c in cl)) if new else "-", det, f"{cost:.2f}", "yes" if (run_dir / "DONE").exists() else "no"]


def main():
    head, out = ["run", "fold", "claims", "branch 1 pass", "branch 3 pass", "per claim and symbol", "cost USD", "done"], list(rows())
    if "--md" in sys.argv:
        print("| " + " | ".join(head) + " |"); print("|" + "---|" * len(head))
    for o in out:
        print(("| " + " | ".join(o) + " |") if "--md" in sys.argv else "  ".join(o))
    tried = yaml.safe_load((HERE / "records" / "claims_tried.yaml").read_text()) if (HERE / "records" / "claims_tried.yaml").exists() else {}
    shelf = yaml.safe_load((HERE / "records" / "shelf.yaml").read_text())["validated"] if (HERE / "records" / "shelf.yaml").exists() else []
    print(f"\nruns {len(out)}, claims tried {sum(len(v) for v in tried.values())}, shelf: {sum(s.get('status') == 'validated' for s in shelf)} validated, "
          f"{sum(s.get('status') == 'profitable' for s in shelf)} profitable, model cost {sum(float(o[6]) for o in out):.2f} USD")


if __name__ == "__main__":
    main()
