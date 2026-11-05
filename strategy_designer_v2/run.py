"""The v2 loop for one brief: ideas -> judge -> profit -> record -> analyst -> next claim -> judge, until the
analyst says none or the round budget is spent. Every step writes a file; a step whose file exists is skipped,
so the run resumes from wherever it stopped. Usage: python3 run.py briefs/<brief>.md [--fold A] [--rounds 2]
The operator decides: the brief, the fold, the budget. The pipeline discovers the rest."""
import sys, re, argparse, pathlib, datetime as dt, yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "steps")); sys.path.insert(0, str(HERE / "steps" / "judge")); sys.path.insert(0, str(HERE / "steps" / "engine"))
import ask as A, judge as J, backtest as E  # noqa: E402

MODELS = {"ideas": "claude-opus-5-5", "analyst": "claude-opus-5-5"}
RETURN_MEASURES = {"mean_diff", "hit_rate", "net_return"}
RECORDS = HERE / "records"


def read_brief(path):
    text = path.read_text(encoding="utf-8")
    fm = yaml.safe_load(text.split("---")[1]) if text.startswith("---") else {}
    symbols = [s.replace("/", "").upper() for s in re.findall(r"([A-Z]{3,5}/USD)", fm.get("product", ""))]
    return fm, symbols or ["BTCUSD"], str(fm.get("bar_size", "1h"))


def prompt_of(*paths, extra=""):
    parts = [f"# FILE {p.name}\n\n{pathlib.Path(p).read_text(encoding='utf-8')}" for p in paths]
    return "\n\n".join(parts) + ("\n\n" + extra if extra else "") + "\n\nAnswer with the YAML file only, nothing else."


def tried_for(brief_name):
    f = RECORDS / "claims_tried.yaml"
    doc = yaml.safe_load(f.read_text()) if f.exists() else {}
    return doc.get(brief_name, [])


def remember(brief_name, ideas, verdicts, run_name):
    f = RECORDS / "claims_tried.yaml"
    doc = yaml.safe_load(f.read_text()) if f.exists() else {}
    rows = doc.setdefault(brief_name, [])
    for i in ideas:
        rows.append({"id": i["id"], "belief": i["belief"], "measure": i["claim"]["measure"], "verdict": verdicts["ideas"][i["id"]]["verdict"], "run": run_name})
    f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    shelf = RECORDS / "shelf.yaml"
    sdoc = yaml.safe_load(shelf.read_text()) if shelf.exists() else {"validated": []}
    for i in ideas:
        if verdicts["ideas"][i["id"]]["verdict"] == "pass":
            kind = "book" if i["claim"]["measure"] in RETURN_MEASURES else "filter"
            sdoc["validated"].append({"id": i["id"], "brief": brief_name, "run": run_name, "kind": kind, "belief": i["belief"]})
    shelf.write_text(yaml.safe_dump(sdoc, sort_keys=False, allow_unicode=True), encoding="utf-8")


def record_of(brief_name, fold, symbols, bar_size, claims_doc, verdicts, profits, run_dir=None):
    rec = {"brief": brief_name, "fold": fold, "symbols": symbols, "bar_size": bar_size, "claims": [], "profit": profits or "none: no return claim passed"}
    for c in claims_doc["ideas"]:
        v = verdicts["ideas"][c["id"]]
        rec["claims"].append({"id": c["id"], "belief": c["belief"], "measure": c["claim"]["measure"], "horizon_bars": c["claim"]["horizon_bars"],
                              "direction": c["claim"]["direction"], "min_effect": c["claim"]["min_effect"], "verdict": v["verdict"],
                              "by_symbol": {s: {k: x.get(k) for k in ("effect", "n_a", "n_b", "windows", "verdict", "why")} for s, x in v["by_symbol"].items()},
                              "code": c["claim"]["code"]})
    if run_dir is not None:
        (run_dir / "record.yaml").write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return rec


def judge_and_profit(claims_path, fold, bar_size, symbols, run_name, run_dir, label):
    vpath = claims_path.parent / ("verdicts.yaml" if claims_path.stem == "claims" else f"verdicts_{claims_path.stem}.yaml")
    verdicts = yaml.safe_load(vpath.read_text()) if vpath.exists() else J.judge_file(claims_path, fold, bar_size, symbols, try_name=run_name)
    claims_doc = yaml.safe_load(claims_path.read_text())
    profits = {}
    for c in claims_doc["ideas"]:
        if verdicts["ideas"][c["id"]]["verdict"] == "pass" and c["claim"]["measure"] in RETURN_MEASURES:
            for s in symbols:   # branch 3 is the engine's backtest, one folder per claim and symbol
                out_dir = run_dir / f"engine_{label}_{c['id']}_{s}"; done = out_dir / "engine_verdict.yaml"
                profits[f"{c['id']}/{s}"] = yaml.safe_load(done.read_text()) if done.exists() else \
                    E.backtest_claim(claims_path, c["id"], fold, bar_size, s, out_dir=out_dir)
    return claims_doc, verdicts, profits


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("brief"); ap.add_argument("--fold", default="A"); ap.add_argument("--rounds", type=int, default=2)
    args = ap.parse_args()
    brief = pathlib.Path(args.brief).resolve(); fm, symbols, bar_size = read_brief(brief)
    runs = HERE / "runs" / brief.stem; runs.mkdir(parents=True, exist_ok=True)
    existing = sorted(p for p in runs.iterdir() if p.is_dir())
    run_dir = existing[-1] if existing and not (existing[-1] / "DONE").exists() else runs / f"{len(existing) + 1:03d}"
    run_dir.mkdir(exist_ok=True); run_name = f"{brief.stem}/{run_dir.name}"
    log = run_dir / "model_calls.yaml"
    print(f"run {run_name}: fold {args.fold}, {bar_size}, {symbols}")

    # 1. ideas
    steps = HERE / "steps"; claims = run_dir / "claims.yaml"
    tried = tried_for(brief.name)
    extra = ("already_tried (do not repeat these):\n" + yaml.safe_dump(tried, allow_unicode=True)) if tried else ""
    if not A.ask(prompt_of(steps / "ideas" / "PROMPT.md", steps / "ideas" / "CLAIM_FORMAT.md", brief, extra=extra), claims, MODELS["ideas"], log):
        return 3
    # 2-4. judge, profit, record
    claims_doc, verdicts, profits = judge_and_profit(claims, args.fold, bar_size, symbols, run_name, run_dir, "r0")
    if not (run_dir / "tried.flag").exists():
        remember(brief.name, claims_doc["ideas"], verdicts, run_name); (run_dir / "tried.flag").write_text("x")
    rec = record_of(brief.name, args.fold, symbols, bar_size, claims_doc, verdicts, profits, run_dir)
    # 5-7. analyst, next claim, judge; repeat
    for r in range(1, args.rounds + 1):
        analysis = run_dir / f"analysis_r{r}.yaml"
        if not A.ask(prompt_of(steps / "analyst" / "PROMPT.md", steps / "ideas" / "CLAIM_FORMAT.md", brief, run_dir / "record.yaml"), analysis, MODELS["analyst"], log):
            return 3
        a = yaml.safe_load(analysis.read_text()); nc = a.get("next_claim")
        if not isinstance(nc, dict):
            print(f"round {r}: analyst says none: {a.get('why')}"); break
        next_claims = run_dir / f"claims_r{r}.yaml"
        if not next_claims.exists():
            next_claims.write_text(yaml.safe_dump({"brief": brief.name, "source": f"analyst round {r}", "ideas": [nc]}, sort_keys=False, allow_unicode=True))
        cd, vd, pf = judge_and_profit(next_claims, args.fold, bar_size, symbols, run_name, run_dir, f"r{r}")
        if not (run_dir / f"tried_r{r}.flag").exists():
            remember(brief.name, cd["ideas"], vd, run_name); (run_dir / f"tried_r{r}.flag").write_text("x")
        rec["claims"] += record_of(brief.name, args.fold, symbols, bar_size, cd, vd, pf)["claims"]
        rec["profit"] = {**(rec["profit"] if isinstance(rec["profit"], dict) else {}), **pf} or rec["profit"]
        (run_dir / "record.yaml").write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    (run_dir / "DONE").write_text(dt.datetime.now(dt.timezone.utc).isoformat())
    print(f"run {run_name} done: {sum(1 for c in rec['claims'] if c['verdict']=='pass')} pass of {len(rec['claims'])} claims")
    return 0


if __name__ == "__main__":
    sys.exit(main())
