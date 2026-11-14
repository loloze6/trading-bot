"""The v2 loop for one brief, the engine the only reader of bars: ideas -> engine (branch 3 + branch 1) -> book summary
-> record -> analyst -> next claim -> engine, until the analyst says none or the rounds are spent. Every step writes a
file; a step whose file exists is skipped, so a run resumes. Usage:
python3 run.py briefs/<brief>.md [--fold A] [--rounds 2] [--max-claims N]   (the operator's knobs, nothing else)"""
import sys, re, argparse, pathlib, datetime as dt, yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "steps")); sys.path.insert(0, str(HERE / "steps" / "engine")); sys.path.insert(0, str(HERE / "steps" / "analyst"))
import ask as A, backtest as E, summarise as S  # noqa: E402

MODELS = {"ideas": "claude-opus-5-5", "analyst": "claude-opus-5-5"}
RECORDS = HERE / "records"
NO_HISTORY = ("No historical data", "warmup_prefetch")


def read_brief(path):
    text = path.read_text(encoding="utf-8")
    fm = yaml.safe_load(text.split("---")[1]) if text.startswith("---") else {}
    symbols = [s.replace("/", "").upper() for s in re.findall(r"([A-Z]{3,5}/USD)", fm.get("product", ""))]
    return fm, symbols or ["BTCUSD"], str(fm.get("bar_size", "1h"))


def prompt_of(*paths, extra=""):
    parts = [f"# FILE {p.name}\n\n{pathlib.Path(p).read_text(encoding='utf-8')}" for p in paths]
    return "\n\n".join(parts) + ("\n\n" + extra if extra else "") + "\n\nAnswer with the YAML file only, nothing else."


def load(path, default):
    return yaml.safe_load(path.read_text()) if path.exists() else default


def dump(path, doc):
    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")


def valid(i):
    c = i.get("claim") if isinstance(i, dict) else None
    return isinstance(c, dict) and isinstance(i.get("id"), str) and all(k in c for k in ("code", "horizon_bars", "min_effect"))


def engine_claim(claims_path, c, label, fold, bar_size, symbols, run_dir):
    """Branch 3 and branch 1 for one claim on every symbol (skip marker: engine_verdict.yaml). Returns {symbol: (dir, engine)}."""
    out = {}
    for s in symbols:
        d = run_dir / f"engine_{label}_{c['id']}_{s}"; marker = d / "engine_verdict.yaml"
        if not marker.exists():
            d.mkdir(exist_ok=True)
            try:
                if not valid(c):
                    raise ValueError("malformed claim: needs id, claim.code, claim.horizon_bars, claim.min_effect")
                E.backtest_claim(claims_path, c["id"], fold, bar_size, s, out_dir=d)
            except Exception as exc:  # noqa: BLE001  a code error of the claim: record it and go on
                if not marker.exists():
                    dump(marker, {"claim": c.get("id"), "symbol": s, "verdict": "refused", "why": f"{type(exc).__name__}: {str(exc)[:200]}"})
        ev = yaml.safe_load(marker.read_text())
        if ev["verdict"] != "refused" and not (d / "book_summary.yaml").exists():
            dump(d / "book_summary.yaml", S.summarise_engine_run(d))
        out[s] = (d, ev)
    return out


def entry_of(c, per_symbol):
    """The record of one claim: branch 1 and branch 3 per symbol, and the claim-level verdicts (pass only if every symbol passes)."""
    cl = c.get("claim") if isinstance(c.get("claim"), dict) else {}
    e = {"id": c.get("id", "?"), "belief": c.get("belief", ""), "horizon": cl.get("horizon_bars"), "min_effect": cl.get("min_effect"), "by_symbol": {}}
    for s, (d, ev) in per_symbol.items():
        jp = d / "judge_verdict.yaml"; j = load(jp, {"verdict": "refused", "why": ev.get("why", "no judge verdict")}); ft, t3 = j.get("fold_totals") or {}, ev.get("fold_totals") or {}
        e["by_symbol"][s] = {"branch1": {"fold_correlation": ft.get("ic_event"), "t_stat": j.get("t_stat"), "verdict": j["verdict"]},
                             "branch3": {"net": t3.get("net_return"), "median_window_sharpe": t3.get("median_window_sharpe"), "worst_drawdown": t3.get("worst_window_drawdown"),
                                         "passed_as": ev.get("passed_as"), "verdict": ev["verdict"]},
                             "why": ev.get("why") or j.get("why"), "folder": str(d.relative_to(HERE))}
    for k, b in (("branch1", "verdict_branch1"), ("branch3", "verdict_branch3")):
        vs = [x[k]["verdict"] for x in e["by_symbol"].values()]
        e[b] = "pass" if vs and all(v == "pass" for v in vs) else ("refused" if all(v == "refused" for v in vs) else "fail")
    return e


def remember(brief_name, entries, run_name):
    f = RECORDS / "claims_tried.yaml"; doc = load(f, {}); rows = doc.setdefault(brief_name, [])
    sh = RECORDS / "shelf.yaml"; sdoc = load(sh, {"validated": []})
    for e in entries:
        if not any(r.get("id") == e["id"] and r.get("run") == run_name for r in rows):
            rows.append({"id": e["id"], "belief": e["belief"], "branch1": e["verdict_branch1"], "branch3": e["verdict_branch3"], "run": run_name})
        if e["verdict_branch1"] == "pass":
            row = next((r for r in sdoc["validated"] if r["id"] == e["id"] and r.get("run") == run_name), None)
            if row is None:
                row = {"id": e["id"], "brief": brief_name, "run": run_name, "belief": e["belief"]}; sdoc["validated"].append(row)
            row["status"] = "profitable" if e["verdict_branch3"] == "pass" else "validated"
    dump(f, doc); dump(sh, sdoc)


def analyst_extra(round_entries, round_ideas):
    """Compact inputs: each claim's code and numbers, the verdicts, and book_summary.yaml only where branch 1 passed."""
    keep = lambda r: {k: v for k, v in r.items() if k in ("window", "net_return", "trades", "sharpe", "max_drawdown")}
    parts = []
    for e, idea in zip(round_entries, round_ideas):
        parts.append(f"## claim {e['id']}\n" + yaml.safe_dump({"belief": e["belief"], "claim": idea.get("claim")}, allow_unicode=True))
        for s, x in e["by_symbol"].items():
            d = HERE / x["folder"]; ev = load(d / "engine_verdict.yaml", {})
            slim = {k: ev.get(k) for k in ("verdict", "passed_as", "fold_totals", "why")}
            for size in ("full_size", "vol_target"):
                if isinstance(ev.get(size), dict):
                    slim[size] = {"fold_totals": ev[size]["fold_totals"], "checks": ev[size]["checks"], "windows": [keep(r) for r in ev[size]["windows"]]}
            parts.append(f"### {s} judge_verdict.yaml\n{yaml.safe_dump(load(d / 'judge_verdict.yaml', {'verdict': 'refused'}))}\n### {s} engine_verdict.yaml\n{yaml.safe_dump(slim)}")
            if x["branch1"]["verdict"] == "pass" and (d / "book_summary.yaml").exists():
                parts.append(f"### {s} book_summary.yaml\n{(d / 'book_summary.yaml').read_text()}")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("brief"); ap.add_argument("--fold", default="A"); ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--max-claims", type=int, default=None)
    args = ap.parse_args()
    brief = pathlib.Path(args.brief).resolve(); fm, symbols, bar_size = read_brief(brief)
    runs = HERE / "runs" / brief.stem; runs.mkdir(parents=True, exist_ok=True)
    existing = sorted(p for p in runs.iterdir() if p.is_dir())
    run_dir = existing[-1] if existing and not (existing[-1] / "DONE").exists() else runs / f"{len(existing) + 1:03d}"
    run_dir.mkdir(exist_ok=True); run_name = f"{brief.stem}/{run_dir.name}"
    log, steps = run_dir / "model_calls.yaml", HERE / "steps"
    print(f"run {run_name}: fold {args.fold}, {bar_size}, {symbols}")
    record = {"brief": brief.name, "fold": args.fold, "symbols": symbols, "bar_size": bar_size, "claims": []}
    claims_path, label, counts = run_dir / "claims.yaml", "r0", {"claims": 0, "b1": 0, "b3": 0, "refused": 0}
    tried = load(RECORDS / "claims_tried.yaml", {}).get(brief.name, [])
    extra = ("already_tried (do not repeat these):\n" + yaml.safe_dump(tried, allow_unicode=True)) if tried else ""
    if not A.ask(prompt_of(steps / "ideas" / "PROMPT.md", steps / "ideas" / "CLAIM_FORMAT.md", brief, extra=extra), claims_path, MODELS["ideas"], log):
        return 3
    for r in range(0, args.rounds + 1):
        ideas = [i if isinstance(i, dict) else {"id": f"malformed_{n}"} for n, i in enumerate(yaml.safe_load(claims_path.read_text())["ideas"])]
        for n, i in enumerate(ideas):
            i.setdefault("id", f"unnamed_{n}")
        if r == 0 and args.max_claims:
            ideas = ideas[:args.max_claims]
        entries = []
        for n, c in enumerate(ideas):
            per = engine_claim(claims_path, c, label, args.fold, bar_size, symbols, run_dir)
            if r == 0 and n == 0:   # a fold the coins do not cover costs one ideas call and nothing more
                bad = [(s, ev["why"]) for s, (d, ev) in per.items() if ev["verdict"] == "refused" and any(m in ev.get("why", "") for m in NO_HISTORY)]
                if bad:
                    (run_dir / "REFUSED").write_text("; ".join(f"{s}: {w}" for s, w in bad)); print(f"REFUSED: {bad[0][0]}: {bad[0][1]}")
                    return 2
            e = entry_of(c, per); entries.append(e); counts["claims"] += 1
            counts["b1"] += e["verdict_branch1"] == "pass"; counts["b3"] += e["verdict_branch3"] == "pass"; counts["refused"] += e["verdict_branch3"] == "refused"
            for s, x in e["by_symbol"].items():
                b1, b3 = x["branch1"], x["branch3"]
                print(f"{e['id']} {s}: branch1 {b1['verdict']} (ic {b1['fold_correlation']}, t {b1['t_stat']}) | branch3 {b3['verdict']} (net {b3['net']}, sharpe {b3['median_window_sharpe']}, dd {b3['worst_drawdown']})"
                      + (f" | {x['why']}" if b3["verdict"] == "refused" else ""))
        record["claims"] += entries; dump(run_dir / "record.yaml", record); remember(brief.name, entries, run_name)
        if r == args.rounds:
            break
        analysis = run_dir / f"analysis_r{r + 1}.yaml"
        reached = [(e, i) for e, i in zip(entries, ideas) if e["verdict_branch3"] != "refused"]
        if not A.ask(prompt_of(steps / "analyst" / "PROMPT.md", steps / "ideas" / "CLAIM_FORMAT.md", brief,
                               extra=analyst_extra([e for e, _ in reached], [i for _, i in reached])), analysis, MODELS["analyst"], log):
            return 3
        a = yaml.safe_load(analysis.read_text()); nc = a.get("next_claim")
        if not isinstance(nc, dict):
            print(f"round {r + 1}: analyst says none: {a.get('why')}"); break
        claims_path, label = run_dir / f"claims_r{r + 1}.yaml", f"r{r + 1}"
        if not claims_path.exists():
            dump(claims_path, {"brief": brief.name, "source": f"analyst round {r + 1}", "ideas": [nc]})
    (run_dir / "DONE").write_text(dt.datetime.now(dt.timezone.utc).isoformat())
    print(f"run {run_name} done: {counts['claims']} claims, branch 1 pass {counts['b1']}, branch 3 pass {counts['b3']}, refused {counts['refused']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
