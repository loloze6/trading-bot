"""The v2 loop for one brief: ideas -> judge -> profit -> record -> analyst -> next claim -> judge, until the
analyst says none or the round budget is spent. Every step writes a file; a step whose file exists is skipped,
so the run resumes from wherever it stopped. Usage: python3 run.py briefs/<brief>.md [--fold A] [--rounds 2]
The operator decides: the brief, the fold, the budget. The pipeline discovers the rest."""
import sys, re, argparse, pathlib, datetime as dt, yaml
import pandas as pd

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
        cl = i.get("claim") if isinstance(i.get("claim"), dict) else {}
        rows.append({"id": i.get("id", "?"), "belief": i.get("belief", ""), "measure": cl.get("measure"), "verdict": verdicts["ideas"][i.get("id", "?")]["verdict"], "run": run_name})
    f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    shelf = RECORDS / "shelf.yaml"
    sdoc = yaml.safe_load(shelf.read_text()) if shelf.exists() else {"validated": []}
    for i in ideas:
        if verdicts["ideas"][i.get("id", "?")]["verdict"] == "pass":
            kind = "book" if (i.get("claim") or {}).get("measure") in RETURN_MEASURES else "filter"
            sdoc["validated"].append({"id": i["id"], "brief": brief_name, "run": run_name, "kind": kind, "belief": i["belief"]})
    shelf.write_text(yaml.safe_dump(sdoc, sort_keys=False, allow_unicode=True), encoding="utf-8")


def record_of(brief_name, fold, symbols, bar_size, claims_doc, verdicts, profits, run_dir=None):
    rec = {"brief": brief_name, "fold": fold, "symbols": symbols, "bar_size": bar_size, "claims": [], "profit": profits or "none: no return claim passed"}
    for c in claims_doc["ideas"]:
        v = verdicts["ideas"][c.get("id", "?")]; cl = c.get("claim") if isinstance(c.get("claim"), dict) else {}
        rec["claims"].append({"id": c.get("id", "?"), "belief": c.get("belief", ""), "measure": cl.get("measure"), "horizon_bars": cl.get("horizon_bars"),
                              "direction": cl.get("direction"), "min_effect": cl.get("min_effect"), "verdict": v["verdict"],
                              "by_symbol": {s: {k: x.get(k) for k in ("effect", "n_a", "n_b", "windows", "verdict", "why")} for s, x in v["by_symbol"].items()},
                              "code": cl.get("code", "")})
    if run_dir is not None:
        (run_dir / "record.yaml").write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return rec


def judge_and_profit(claims_path, fold, bar_size, symbols, run_name, run_dir, label):
    vpath = claims_path.parent / ("verdicts.yaml" if claims_path.stem == "claims" else f"verdicts_{claims_path.stem}.yaml")
    verdicts = yaml.safe_load(vpath.read_text()) if vpath.exists() else J.judge_file(claims_path, fold, bar_size, symbols, try_name=run_name)
    claims_doc = yaml.safe_load(claims_path.read_text())
    for n, c in enumerate(claims_doc["ideas"]):          # the same ids the judge gave a malformed idea
        if not isinstance(c, dict):
            claims_doc["ideas"][n] = {"id": f"malformed_{n}"}
        else:
            c.setdefault("id", f"unnamed_{n}")
    profits = {}
    for c in claims_doc["ideas"]:
        if verdicts["ideas"][c.get("id", "?")]["verdict"] == "pass" and (c.get("claim") or {}).get("measure") in RETURN_MEASURES:
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
    # Coverage before any model call (asked by run n06: a fold whose windows hold no bars of a young coin).
    windows = J.rf.load_fold_windows(args.fold); short = []
    for s in symbols:
        wn = J.window_numbers(J.load_bars(s, bar_size).dropna(subset=["close"]).index, windows)
        per_bar = {"1h": 24, "1d": 1}[bar_size]
        first = pd.Timestamp(windows[0]["test"]["start"]); bars_before = int((J.load_bars(s, bar_size).dropna(subset=["close"]).index < first).sum())
        if bars_before < 600:
            short.append(f"{s} warm-up: {bars_before} bars before the fold, 600 needed")
        for i, w in enumerate(windows, start=1):
            days = (pd.Timestamp(w["test"]["end"]) - pd.Timestamp(w["test"]["start"])).days + 1
            have = int((wn == i).sum()); need = int(0.8 * days * per_bar)
            if have < need:
                short.append(f"{s} W{i}: {have} of about {days * per_bar} bars")
    if short:
        (run_dir / "REFUSED").write_text("coverage: " + "; ".join(short))
        print("REFUSED before any model call: fold " + args.fold + " lacks bars for " + "; ".join(short) + ". Choose a fold the coins cover.")
        return 2

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
