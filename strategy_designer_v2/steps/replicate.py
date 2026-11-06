"""Replicate one validated claim, same code, on other symbols: judge, then the engine where it passes. No model call.
Usage: python3 steps/replicate.py <claims.yaml> <claim_id> <fold> <bar_size> <out_dir> SYMBOL [SYMBOL ...]
Asked by batch 7 (fresh ideas on other coins found nothing; the exact claim had not been measured there)."""
import sys, pathlib, yaml
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "judge")); sys.path.insert(0, str(HERE / "engine"))
import judge as J, backtest as E  # noqa: E402

claims_path, cid, fold, bar_size, out_dir, symbols = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], sys.argv[4], pathlib.Path(sys.argv[5]).resolve(), sys.argv[6:]
def _find(cid, path):
    """The claim may live in claims.yaml or in an analyst round's claims_rN.yaml of the same run folder."""
    for cp in sorted(path.parent.glob("claims*.yaml")):
        for i in yaml.safe_load(cp.read_text())["ideas"]:
            if isinstance(i, dict) and i.get("id") == cid:
                return i
    raise SystemExit(f"claim {cid} not found in {path.parent}")
idea = _find(cid, claims_path)
out_dir.mkdir(parents=True, exist_ok=True)
one = out_dir / "claims.yaml"
one.write_text(yaml.safe_dump({"brief": f"replication of {cid} from {claims_path.parent.name}", "source": str(claims_path), "ideas": [idea]}, sort_keys=False, allow_unicode=True))
v = J.judge_file(one, fold, bar_size, symbols, try_name=f"replicate/{cid}")
for s in symbols:
    r = v["ideas"][cid]["by_symbol"][s]
    if r["verdict"] == "pass" and idea["claim"]["measure"] in ("mean_diff", "hit_rate", "net_return"):
        E.backtest_claim(one, cid, fold, bar_size, s, out_dir=out_dir / f"engine_{cid}_{s}")
