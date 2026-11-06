"""The morning file, generated from the records. Numbers only, no advice. Usage: python3 night_2026-11-06/make_readme.py"""
import sys, pathlib, datetime as dt, yaml, re
V2 = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(V2 / "records")); import query as Q  # noqa: E402

runs = list(Q.runs())
night = [r for r in runs if not r["run"].startswith(("fake_", "real_01_daily_breadth_fold_a/", "try"))]
lines = ["# Night of 2026-11-06: what ran, what passed, what it cost", "",
         f"Generated {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC by `night_2026-11-06/make_readme.py` from the records. Numbers only. "
         "The operator delegated the night: briefs by the delegate, runs by the pipeline, no holdout spent, no git until morning.", ""]
tot_claims = sum(len(r["claims"]) for r in runs); tot_pass = sum(len(r["passes"]) for r in runs); tot_cost = sum(r["cost_usd"] for r in runs)
eng_pass = [(r["run"], k, v) for r in runs for k, v in r["engine"].items() if v.get("verdict") == "pass"]
eng_all = [(r["run"], k, v) for r in runs for k, v in r["engine"].items()]
lines += ["## Totals", "", "| runs | claims judged | judge passes | engine runs | engine passes | model cost USD |", "|---|---|---|---|---|---|",
          f"| {len(runs)} | {tot_claims} | {tot_pass} ({tot_pass / max(1, tot_claims):.1%}) | {len(eng_all)} | {len(eng_pass)} | {tot_cost:.2f} |", "",
          "The judge's pass rate sits near the 5% noise floor of its own rule (the claim's number on the fold, same sign in 5 of 6 windows). "
          "A judge pass is an event mean on one fold; the engine's bar is the book: net positive in 5 of 6 windows, median window Sharpe at least 1.0, worst window drawdown at most 20%, at full size or at a fixed 20% volatility target.", ""]
lines += ["## Every run", "", "| run | fold | claims | judge passes | engine (per symbol) | cost USD |", "|---|---|---|---|---|---|"]
for r in runs:
    eng = "; ".join(f"{k.split('_', 2)[-1]}: {v['verdict']}" + (f" ({v.get('passed_as') or 'full'}, net {v['fold_totals']['net_return']:+.0%}, Sharpe {v['fold_totals']['median_window_sharpe'] if v['fold_totals']['median_window_sharpe'] is None else round(v['fold_totals']['median_window_sharpe'], 2)}, dd {v['fold_totals']['worst_window_drawdown']})" if v["verdict"] != "refused" else "")
                    for k, v in r["engine"].items()) or "-"
    lines.append(f"| {r['run']} | {r['fold'] or '?'} | {len(r['claims'])} | {', '.join(r['passes']) or '0'} | {eng} | {r['cost_usd']:.2f} |")
lines += ["", "## Engine passes (a book that passed the profit bar on its fold, at either size)", ""]
for run, k, v in eng_pass:
    t = v["fold_totals"]
    lines.append(f"- {v['claim']} on {v['symbol']} ({v['bar_size']}, fold {v['fold']}), {run}, passed as {v.get('passed_as') or 'full size'}: net {t['net_return']:+.1%}, median window Sharpe {round(t['median_window_sharpe'], 2)}, worst window drawdown {t['worst_window_drawdown']:.1%}, trades {t['trades']}")
lines += ["", "## Replications (same claim code, other coins, same fold, no model call)", "", "| claim | fold | symbol | judge | engine |", "|---|---|---|---|---|"]
for d in sorted((V2 / "runs" / "_replications").glob("*/")):
    vp = d / "verdicts.yaml"
    if not vp.exists():
        continue
    v = yaml.safe_load(vp.read_text()); cid = list(v["ideas"])[0]
    for s, r in v["ideas"][cid]["by_symbol"].items():
        ep = d / f"engine_{cid}_{s}" / "engine_verdict.yaml"
        e = yaml.safe_load(ep.read_text()) if ep.exists() else None
        es = "-" if e is None else (e["verdict"] + (f" ({e.get('passed_as') or 'full'}, Sharpe {round(e['fold_totals']['median_window_sharpe'], 2)})" if e["verdict"] == "pass" else (": " + re.sub(r'\d{4}-\d{2}-\d{2}', '<date>', e.get("why", ""))[:80] if e["verdict"] == "refused" else "")))
        lines.append(f"| {cid} | {v['fold']} | {s} | {r['verdict']} ({'effect ' + format(r['effect'], '+.4f') if r.get('effect') is not None else r.get('why', '')[:60]}, {r.get('agreeing_windows', '')}) | {es} |")
lb = V2 / "records" / "lite_books.yaml"
if lb.exists():
    rows = yaml.safe_load(lb.read_text()); ok = [x for x in rows if x["lite_verdict"] == "pass"]
    lines += ["", "## Lite book check on every judge-passed return claim (information; close-to-close, full size, 0.15% cost)", "",
              f"{len(rows)} judge-passed books checked, {len(ok)} pass the same bar in the lite check: " + ", ".join(f"{x['claim']} on {x['symbol']} (Sharpe {x['lite_sharpe']})" for x in ok), ""]
tried = yaml.safe_load((V2 / "records" / "claims_tried.yaml").read_text())
lines += ["## Looks per brief (claims tried; at a 5% noise rate expect one false pass per twenty)", "", ", ".join(f"{k.split('.')[0]}: {len(v)}" for k, v in tried.items()), ""]
sb = (V2 / "STEPBACK.md").read_text()
fixes = re.findall(r"^1\. \*\*Whose job is this\?\*\* (.*)$", sb, flags=re.M)
lines += ["## Defects the runs revealed and the fixes (from STEPBACK.md, in order)", ""] + [f"- {f}" for f in fixes[-14:]] + [""]
lines += ["## Open asks (recorded, not built)", "",
          "- Daily claims with year-long windows cannot reach the engine on folds whose first window starts near the start of a coin's cache (the engine's warm-up wants twice the claim's history): refused, not scored.",
          "- A validated filter waits for a book; the shelf holds filters that no book has used.",
          "- A significance floor for the judge is the operator's ruling; the t-statistic is recorded next to each effect since 01:35.",
          "- The holdout path is not built; nothing touched the sealed store.", ""]
lines += ["## Files", "", "`records/query.py` (this table), `records/shelf.yaml`, `records/claims_tried.yaml`, `records/trials.yaml`, `records/lite_books.yaml`, `runs/<brief>/<n>/` (claims, verdicts, analyses, engine folders), `runs/_replications/`, `STEPBACK.md`, `CHANGES.md`."]
(V2 / "night_2026-11-06" / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"README written: {len(runs)} runs, {tot_claims} claims, {tot_pass} judge passes, {len(eng_pass)} engine passes, {tot_cost:.2f} USD")
