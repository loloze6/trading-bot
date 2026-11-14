"""Backtest helper, step 4. Runs one step 3 test plan through the bot's own backtest, unchanged, and stores the
engine's record in the backtests folder.

  python run_backtest.py path/to/PLAN.md --python path/to/venv/bin/python
Options: --out-root (default: ../backtests next to this folder), --force (rerun even when nothing the engine reads
has changed).

What it does, in order:
  1. Reads the plan's header: coins, bar size, fold, outcome. A plan whose outcome is untestable or missing-components
     is not run; its index line says so. A plan whose config and data are those of its stored record is not rerun.
  2. Maps each coin to the venue the engine can reach here (Kraken, USD-quoted: BTC -> BTCUSD) and builds the
     protocol the pipeline's backtest wrapper reads: the fold's windows from strategy-research/tools/research_folds.py
     (which refuses any window touching the sealed holdout), the bar size, and the venue keys from
     strategy-research/tools/venue_resolver.py. The protocol is written to a temporary folder only: it holds dates.
  3. Runs strategy-research/tools/run_protocol.py (the pipeline's wrapper around the bot's run_backtest, with warm-up
     prefetch and the holdout guard) once per coin and window, each in its own folder: the engine names a run
     folder after the current second, so two windows finishing in the same second would otherwise share one.
     A coin or window without data does not stop the others.
  4. Keeps the engine's files per coin and window (metrics.json, manifest.json, forecast_distribution.csv, and
     bars.csv and trades.json gzipped), plus the window's protocol_summary.json and trade_diagnostics.json, gzipped. It drops tradesxl.xlsx and
     portfolio_states.csv, which repeat what bars.csv and trades.json hold. Windows are named w1..wN in the fold's order.
  5. Writes run.md for the plan and its line in the backtests folder's INDEX.md.

This script does not open the price data itself: only the engine reads bars.
"""
import argparse, gzip, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SR = REPO / "strategy-research"
KEEP = ["metrics.json", "manifest.json", "forecast_distribution.csv"]
KEEP_GZ = ["bars.csv", "trades.json"]   # the large ones, gzipped
CATALOGUE = HERE.parents[1] / "03_test_plan" / "helper" / "reference" / "component_catalogue.md"
VENUE = ("kraken", "perp")   # Binance is not reachable from this environment (HTTP 451); Kraken is


def _defaults():
    """Class name -> {param: default value}, from the catalogue rows ("`period` (14)")."""
    text = CATALOGUE.read_text()
    rows = text[text.index("### Regime measures"):]
    out = {}
    for name, params in re.findall(r"^\| `(\w+)` \| ([^|]*) \|", rows, re.M):
        d = {}
        for k, v in re.findall(r"`(\w+)` \(([^)]*)\)", params):
            v = v.split(",")[0].strip().strip('"')
            try:
                d[k] = json.loads(v.lower() if v.lower() in ("true", "false") else v)
            except ValueError:
                d[k] = v
        out[name] = d
    return out


def canonical(config):
    """What the engine computes, without its labels: component ids replaced by their position, and params written at
    their catalogue default removed. Two configs equal here give the same backtest."""
    defaults, cfg = _defaults(), json.loads(json.dumps(config))
    ren = {}
    for i, c in enumerate(cfg.get("regime_detector", {}).get("components", [])):
        ren[c.get("id")] = f"d{i}"
    def clean(c):
        cls = str(c.get("class", "")).split(".")[-1]
        c["params"] = {k: v for k, v in (c.get("params") or {}).items() if defaults.get(cls, {}).get(k, object()) != v}
    rd = cfg.get("regime_detector", {})
    for c in rd.get("components", []):
        clean(c); c["id"] = ren[c.get("id")]
    for v in rd.get("vetoes", []):
        v["id"] = ren.get(v.get("id"), v.get("id"))
    for rule in rd.get("rules", []):
        for group in rule.get("any_of", []):
            for cond in group:
                cond["id"] = ren.get(cond.get("id"), cond.get("id"))
    for reg in (rd.get("regimes") or {}).values():
        for e in (reg or {}).get("components", []):
            e["id"] = ren.get(e.get("id"), e.get("id"))
    for name, reg in (cfg.get("strategies", {}).get("regimes") or {}).items():
        for i, c in enumerate((reg or {}).get("components", [])):
            clean(c); c["id"] = f"{name}{i}"
    return cfg


def plan_header(text):
    m = re.match(r"\s*---\n(.*?)---\n", text, re.S)
    if not m:
        sys.exit("the plan does not start with a --- header")
    return {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)}


def coins(instruments):
    """'BTC, ETH, BNB' or 'BTC/USDT' -> ['BTC', 'ETH', 'BNB']."""
    out = []
    for part in instruments.split(","):
        base = re.split(r"[/\s-]", part.strip())[0].upper()
        base = re.sub(r"(USDT|USD)$", "", base) or base
        if base and base not in out:
            out.append(base)
    return out


def protocol(python, symbol, bar, folds):
    """The protocol dict, built by the pipeline's own fold loader and venue resolver (run in the venv). Several folds:
    their windows one after the other, in the order given."""
    code = (
        "import json, sys; sys.path.insert(0, 'tools'); sys.path.insert(0, '../trading-bot');"
        "import research_folds as rf, venue_resolver as vr;"
        f"p = {{'symbols': [{symbol!r}], 'timeframe': {bar!r}, 'windows': [w for f in {folds!r} for w in rf.fold_windows(rf.load_folds(), f)]}};"
        f"p.update(vr.resolve({VENUE[0]!r}, {VENUE[1]!r})); print(json.dumps(p))")
    r = subprocess.run([python, "-c", code], cwd=SR, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"could not build the protocol: {r.stderr[-500:]}")
    return json.loads(r.stdout)


def write_atomic(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def index_line(index_path, plan_id, line):
    lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(plan_id + ":")]
    write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [line])))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("plan", type=Path)
    a.add_argument("--python", required=True, help="the interpreter of a venv with trading-bot/requirements.txt")
    a.add_argument("--out-root", type=Path, default=HERE.parent / "backtests")
    a.add_argument("--force", action="store_true")
    args = a.parse_args()

    plan_path = args.plan.resolve()
    plan_id, text = plan_path.stem, plan_path.read_text()
    h = plan_header(text)
    bar, period = h["data-bar"], h["data-period"]
    m = re.fullmatch(r"folds? ([A-Z](?:, [A-Z])*)", period)   # "fold A", or "folds A, B, C, D"
    if not m:
        sys.exit(f"unreadable data-period: {period!r}")
    folds = m.group(1).split(", ")
    out_root = args.out_root.resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    index_path = out_root / "INDEX.md"
    dest = out_root / plan_id
    # The plan's outcome: the header (step 3 with the fidelity rule), or the old "Untestable:" line.
    outcome = h.get("outcome") or ("untestable" if "\nUntestable:" in text else "plan")
    if outcome != "plan":
        if dest.exists():
            shutil.rmtree(dest)   # a record left from an earlier version of the plan no longer belongs to it
        index_line(index_path, plan_id, f"{plan_id}: not run: the plan is {outcome} [{bar}, {period}]")
        print(f"not run ({outcome}): {plan_id}")
        return
    config_path = plan_path.with_name(plan_id + "_config.json")
    # Rerun only when what the engine reads has changed: the config (labels and default-valued params aside) and the
    # data (coins, bar size, fold).
    # The plan's other fields (fidelity, forecast in words, criterion) do not change the backtest.
    data_line = f"- Data: {h['data-instruments']} as "
    if (not args.force and (dest / "config.json").exists() and (dest / "run.md").exists()
            and canonical(json.loads((dest / "config.json").read_text())) == canonical(json.loads(config_path.read_text()))
            and data_line in (dest / "run.md").read_text() and f"; {bar} bars; {period}\n" in (dest / "run.md").read_text()
            and index_path.exists() and any(l.startswith(plan_id + ": ran") for l in index_path.read_text().splitlines())):
        print(f"unchanged, record kept: {plan_id}")
        return

    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copy(config_path, dest / "config.json")
    report, summary, proto = [], [], None
    for base in coins(h["data-instruments"]):
        symbol = f"{base}USD"
        proto = protocol(args.python, symbol, bar, folds)
        windows = proto["windows"]
        cdir = dest / symbol
        rows, failed = [], []
        # One wrapper call per window, each in its own folder: the engine names a run folder after the current
        # second and the config's hash, so two windows finishing in the same second would share (overwrite) one.
        for k, window in enumerate(windows, 1):
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                (tmp / "protocol.json").write_text(json.dumps(dict(proto, windows=[window])))
                r = subprocess.run([args.python, "tools/run_protocol.py", str(config_path), str(tmp / "protocol.json"),
                                    "--out-dir", str(tmp / "out"), "--legacy-verdict-retired"],
                                   cwd=SR, capture_output=True, text=True, timeout=6 * 3600)
                log = re.sub(r"20\d\d-\d\d(-\d\d)?", "<date>", (r.stdout + r.stderr))   # no dates in what we store
                runs = list((tmp / "out" / "results").glob("*/metrics.json")) if (tmp / "out" / "results").exists() else []
                if r.returncode or len(runs) != 1:
                    failed.append((k, "no historical data on the venue" if "No historical data" in log else "the engine stopped",
                                   "\n".join(log.strip().splitlines()[-4:])))
                    continue
                src = runs[0].parent
                wdir = cdir / f"w{k}"
                wdir.mkdir(parents=True)
                for f in KEEP:
                    if (src / f).exists():
                        shutil.copy(src / f, wdir / f)
                for f in KEEP_GZ:
                    if (src / f).exists():
                        with open(src / f, "rb") as fi, gzip.open(wdir / (f + ".gz"), "wb") as fo:
                            shutil.copyfileobj(fi, fo)
                for f in ["protocol_summary.json", "trade_diagnostics.json"]:
                    if (tmp / "out" / f).exists():
                        with open(tmp / "out" / f, "rb") as fi, gzip.open(wdir / (f + ".gz"), "wb") as fo:
                            shutil.copyfileobj(fi, fo)
                (wdir / "engine_log.txt").write_text(log)
                c = json.loads(runs[0].read_text())["core"]
                rows.append((k, c.get("trade_count"), c.get("forecast_return_corr_all_bars"), c.get("net_return_pct")))
        part = f"- {symbol}: {len(rows)} of {len(windows)} windows run."
        if rows:
            part += ("\n\n| window | trades | forecast vs next return (all bars) | net return % |\n|---|---|---|---|\n"
                     + "".join(f"| w{k} | {t} | {fc} | {nr} |\n" for k, t, fc, nr in rows))
        for k, reason, tail in failed:
            part += f"\n- w{k} not run: {reason}.\n\n```\n{tail}\n```\n"
        report.append(part)
        if rows:
            summary.append(f"{symbol} {len(rows)}/{len(windows)}" + (f" ({len(failed)} not run: {failed[0][1]})" if failed else ""))
        else:
            summary.append(f"{symbol} not run ({failed[0][1] if failed else 'no window'})")
    venue = proto["venue"]["label"] if proto else ""
    write_atomic(dest / "run.md", f"# Backtest of {plan_id}\n\n"
                 f"- Plan: `{os.path.relpath(plan_path, dest)}`\n- Config: `config.json` (a copy of the plan's config)\n"
                 f"- Data: {h['data-instruments']} as {', '.join(f'{b}USD' for b in coins(h['data-instruments']))}; {bar} bars; {period}\n"
                 f"- Venue: {venue}\n- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window\n\n"
                 + "\n".join(report) + "\n")
    ran = any(" not run" not in s for s in summary)
    index_line(index_path, plan_id, f"{plan_id}: {'ran' if ran else 'not run'}: {'; '.join(summary)} [{bar}, {period}]")
    print(f"{plan_id}: {'; '.join(summary)}")


if __name__ == "__main__":
    main()
