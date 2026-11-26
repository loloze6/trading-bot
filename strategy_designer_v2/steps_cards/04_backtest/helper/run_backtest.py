"""Backtest helper, step 4. Runs one step 3 test plan through the bot's own backtest, unchanged, and stores the
engine's record in the backtests folder.

  python run_backtest.py path/to/PLAN.md --python path/to/venv/bin/python
Options: --out-root (default: ../backtests next to this folder), --force (rerun even when nothing the engine reads
has changed), --windows FILE (a JSON list of windows run in place of the plan's folds: the same plan on other dates),
--coins "ADA, DOGE" (these coins in place of the plan's: the same plan on other coins, common/unseen_coins.md),
--data-use FILE (a run's data_use.json, common/data_use.md: the run's research coins on the research windows, in place
of the plan's coins and folds; a coin is left out of a window by data_use.md's section 3, counted in run.md).

What it does, in order:
  1. Reads the plan's header: coins, bar size, fold, outcome. A plan whose outcome is untestable or missing-components
     is not run; its index line says so. A plan whose config and data are those of its stored record is not rerun.
  2. Maps each coin to the venue the engine can reach here (Kraken, USD-quoted: BTC -> BTCUSD) and builds the
     protocol the pipeline's backtest wrapper reads: the fold's windows from trading-bot/backtest/research_folds.py
     (which refuses any window touching the sealed holdout), the bar size, and the venue keys from
     trading-bot/backtest/venue_resolver.py. The protocol is written to a temporary folder only: it holds dates.
  3. Runs trading-bot/backtest/run_protocol.py (the pipeline's wrapper around the bot's run_backtest, with warm-up
     prefetch and the holdout guard) once per coin and fold, on the fold's windows (with --windows: once per coin), so
     Python and the bot load once per call. That call is used only when every window got its own run folder. The
     engine names a run folder after the current second, so two windows finishing in the same second share one; and
     the wrapper stops at the first window that fails. In either case the call's windows are run again once per
     window, each in its own folder (the way every coin ran before 2026-11-16). A coin or window without data does
     not stop the others.
     The calls run at the same time, as many at once as the machine has cores (2026-11-16, change 2 of
     topics/33_review/duration/3_plan.md; one call per coin and fold since 2026-11-20, change C of 12_round2_plan.md, so
     6 coins no longer run in two waves on 4 cores). Each call is a separate process with its own output folder, and
     the wrapper gives each call its own interim trades file (--trades-file-in-out-dir).
  4. Keeps the engine's files per coin and window (metrics.json, manifest.json, forecast_distribution.csv, and
     bars.csv and trades.json gzipped). The wrapper call's own protocol_summary.json and trade_diagnostics.json
     (gzipped) and its log (engine_log.txt) go in the call's folder (<coin>/fold_<X>/, or <coin>/windows/ with
     --windows), or in the window's folder when its windows ran once per window. It drops tradesxl.xlsx and
     portfolio_states.csv, which repeat what bars.csv and trades.json hold.
     Windows are named w1..wN in the folds' order.
  5. Writes run.md for the plan and its line in the backtests folder's INDEX.md.

This script does not open the price data itself: only the engine reads bars.
"""
import argparse, gzip, json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
from lib import write_atomic  # noqa: E402  (shared helpers, common/lib.py)
import coins as coin_rules  # noqa: E402  (the coin groups and data rules, common/coins.py)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BT = REPO / "trading-bot" / "backtest"   # the backtest wrapper and its helpers (moved from strategy-research/tools/, 2026-11-16)
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


def protocol(python, symbol, bar, folds, windows=None):
    """The protocol dict, built by the pipeline's own fold loader and venue resolver (run in the venv). Several folds:
    their windows one after the other, in the order given. Windows given (--windows): those, in place of the folds'."""
    wins = (f"{windows!r}" if windows is not None
            else f"[w for f in {folds!r} for w in rf.fold_windows(rf.load_folds(), f)]")
    code = (
        "import json, sys; sys.path.insert(0, '.'); sys.path.insert(0, '..');"
        "import research_folds as rf, venue_resolver as vr;"
        f"p = {{'symbols': [{symbol!r}], 'timeframe': {bar!r}, 'windows': {wins}}};"
        f"p.update(vr.resolve({VENUE[0]!r}, {VENUE[1]!r})); print(json.dumps(p))")
    r = subprocess.run([python, "-c", code], cwd=BT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"could not build the protocol: {r.stderr[-500:]}")
    return json.loads(r.stdout)


def call_protocol(python, config_path, proto, windows, tmp):
    """One call of the pipeline's wrapper on these windows, in its own temporary folder.
    Returns (exit code, log without dates, the call's output folder)."""
    (tmp / "protocol.json").write_text(json.dumps(dict(proto, windows=windows)))
    r = subprocess.run([python, "run_protocol.py", str(config_path), str(tmp / "protocol.json"),
                        "--out-dir", str(tmp / "out"), "--legacy-verdict-retired", "--trades-file-in-out-dir"],
                       cwd=BT, capture_output=True, text=True, timeout=6 * 3600)
    return r.returncode, re.sub(r"20\d\d-\d\d(-\d\d)?", "<date>", (r.stdout + r.stderr)), tmp / "out"   # no dates stored


def coin_runs(rc, out, windows):
    """The run folder of each window, in the windows' order, from one wrapper call on all of them. None when the call
    cannot be used: it failed, or a window has no run folder of its own (the engine names a run folder after the
    current second and the config's hash, so two windows finishing in the same second share one, and the second
    overwrites the first)."""
    if rc:
        return None
    try:
        results = json.loads((out / "protocol_summary.json").read_text(encoding="utf-8"))["results"]
        folders = [out / "results" / r["run_id"] for r in results]
        labels = [r["window"] for r in results]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if (labels != [w["label"] for w in windows] or len(set(folders)) != len(windows)
            or not all((f / "metrics.json").exists() for f in folders)
            or len(list((out / "results").glob("*/metrics.json"))) != len(windows)):
        return None
    return folders


def keep_window(src, wdir, k):
    """Keeps one window's engine files (src: its run folder) in wdir; returns its row of the run.md table."""
    wdir.mkdir(parents=True)
    for f in KEEP:
        if (src / f).exists():
            shutil.copy(src / f, wdir / f)
    for f in KEEP_GZ:
        if (src / f).exists():
            with open(src / f, "rb") as fi, gzip.open(wdir / (f + ".gz"), "wb") as fo:
                shutil.copyfileobj(fi, fo)
    c = json.loads((src / "metrics.json").read_text())["core"]
    return k, c.get("trade_count"), c.get("forecast_return_corr_all_bars"), c.get("net_return_pct")


def keep_call(out, log, folder):
    """Keeps one wrapper call's own files in folder: its summary and trade diagnostics (gzipped) and its log."""
    for f in ["protocol_summary.json", "trade_diagnostics.json"]:
        if (out / f).exists():
            with open(out / f, "rb") as fi, gzip.open(folder / (f + ".gz"), "wb") as fo:
                shutil.copyfileobj(fi, fo)
    (folder / "engine_log.txt").write_text(log)


def cores():
    """How many coins run at once: the cores this process may use."""
    return len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else (os.cpu_count() or 1)


def parts(python, symbol, bar, folds, windows=None):
    """The coin's windows, split into the wrapper calls that run them: one call per fold (2026-11-20, topic 33,
    `topics/33_review/duration/12_round2_plan.md`, change C), or one call on the windows of --windows.
    Returns [(part name, its protocol, the number of the coin's windows before it)]."""
    out, before = [], 0
    for name, fs in ([("windows", folds)] if windows is not None else [(f"fold_{f}", [f]) for f in folds]):
        proto = protocol(python, symbol, bar, fs, windows)
        out.append((name, proto, before))
        before += len(proto["windows"])
    return out


def run_part(python, config_path, proto, numbers, cdir, pdir):
    """Runs one call's windows into cdir, window i named w<numbers[i]> (the coin's windows in order, those left out by
    the data use skipped); the call's own files go in pdir. Returns (the rows of the windows run, the windows not
    run)."""
    windows = proto["windows"]
    rows, failed, folders = [], [], None
    # One wrapper call for the part's windows: Python and the bot load once per call. Its record is used only when
    # every window has its own run folder (coin_runs); otherwise the part is run again one window at a time, below.
    if windows:
        with tempfile.TemporaryDirectory() as tmp:
            rc, log, out = call_protocol(python, config_path, proto, windows, Path(tmp))
            folders = coin_runs(rc, out, windows)
            if folders:
                for k, src in zip(numbers, folders):
                    rows.append(keep_window(src, cdir / f"w{k}", k))
                pdir.mkdir(parents=True, exist_ok=True)
                keep_call(out, log, pdir)
    # One wrapper call per window, each in its own folder (the way every coin ran before 2026-11-16). Used
    # when the part's call failed (the wrapper stops at the first window that fails, so the later ones would be
    # lost) or two of its windows shared one run folder. The record is then exactly that of a run made
    # this way from the start.
    for k, window in ([] if folders else zip(numbers, windows)):
        with tempfile.TemporaryDirectory() as tmp:
            rc, log, out = call_protocol(python, config_path, proto, [window], Path(tmp))
            runs = list((out / "results").glob("*/metrics.json")) if (out / "results").exists() else []
            if rc or len(runs) != 1:
                failed.append((k, "the dates were not fetched (run the data tool)" if "DataNotFetched" in log
                               else "no historical data on the venue" if "No historical data" in log else "the engine stopped",
                               "\n".join(log.strip().splitlines()[-4:])))
                continue
            wdir = cdir / f"w{k}"
            rows.append(keep_window(runs[0].parent, wdir, k))
            keep_call(out, log, wdir)
    return rows, failed


def index_line(index_path, plan_id, line):
    lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(plan_id + ":")]
    write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [line])))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("plan", type=Path)
    a.add_argument("--python", required=True, help="the interpreter of a venv with trading-bot/requirements.txt")
    a.add_argument("--out-root", type=Path, default=HERE.parent / "backtests")
    a.add_argument("--force", action="store_true")
    a.add_argument("--windows", type=Path, help="a JSON file of windows ([{label, test: {start, end}}, ...]) to run "
                   "in place of the plan's folds (a test on other dates, the same plan and config)")
    a.add_argument("--coins", help="coins (\"ADA, DOGE\") run in place of the plan's data-instruments (a test on other "
                   "coins, the same plan, config and folds)")
    a.add_argument("--data-use", type=Path, help="a run's data_use.json (common/data_use.md): its research coins on its "
                   "research windows, in place of the plan's coins and folds")
    args = a.parse_args()
    du = json.loads(args.data_use.read_text(encoding="utf-8")) if args.data_use else None

    plan_path = args.plan.resolve()
    plan_id, text = plan_path.stem, plan_path.read_text()
    h = plan_header(text)
    bar, period = h["data-bar"], h["data-period"]
    instruments = args.coins or h["data-instruments"]   # other coins than the plan's: the record names them
    folds, windows = None, None
    if du:   # the new data use: the run's coins and windows decide, whatever the plan names (common/data_use.md)
        instruments = ", ".join(du["research_coins"])
        windows_file = coin_rules.STEPS / du["windows"]
        windows = json.loads(windows_file.read_text(encoding="utf-8"))
        period = f"windows {windows_file.stem}, data use {du['version']}"
    else:
        m = re.fullmatch(r"folds? ([A-Z](?:, [A-Z])*)", period)   # "fold A", or "folds A, B, C, D"
        if not m:
            sys.exit(f"unreadable data-period: {period!r}")
        folds = m.group(1).split(", ")
    if args.windows and not du:   # other dates than the plan's folds: the record names the windows file in place of the folds
        windows = json.loads(args.windows.read_text(encoding="utf-8"))
        period = f"windows {args.windows.stem}"
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
    data_line = f"- Data: {instruments} as "
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
    if du:   # the record says which data use it was run in: steps 5 and 7 read their halves from it (common/lib.py)
        write_atomic(dest / "data_use.json", json.dumps(du, indent=1) + "\n")
    report, summary, proto = [], [], None
    symbols = [f"{base}USD" for base in coins(instruments)]
    # The calls at the same time, as many as the machine has cores: one call per coin and fold (change C, 2026-11-20:
    # 6 coins on 4 cores ran in two waves when a call held a whole coin). Each call is a separate process with its own
    # folders. The record is written in the coins' and windows' order, whichever call finishes first.
    # The new data use: a coin is left out of a window by data_use.md's section 3 (its first 90 days, a hole of more
    # than one day), decided from its daily file's dates before the engine runs; the windows kept keep their numbers.
    kept = {s: list(range(1, len(windows) + 1)) for s in symbols} if windows is not None else {}
    left = {s: [] for s in symbols}
    for symbol, base in zip(symbols, coins(instruments)):
        if du:
            days = coin_rules.dates(base)
            why = [coin_rules.left_out(base, w["test"]["start"], w["test"]["end"], days=days) for w in windows]
            kept[symbol] = [k for k, y in enumerate(why, 1) if y is None]
            left[symbol] = [(k, y) for k, y in enumerate(why, 1) if y is not None]
    with ThreadPoolExecutor(max_workers=max(1, min(len(symbols), cores()))) as pool:
        coin_parts = list(pool.map(lambda sym: parts(args.python, sym, bar, folds, windows), symbols))
    calls = []
    for symbol, ps in zip(symbols, coin_parts):
        for name, proto, before in ps:
            numbers = list(range(before + 1, before + 1 + len(proto["windows"])))
            if du:
                numbers = kept[symbol]
                proto = dict(proto, windows=[windows[k - 1] for k in numbers])
            if numbers:
                calls.append((symbol, name, proto, numbers))
    with ThreadPoolExecutor(max_workers=max(1, min(len(calls), cores()))) as pool:
        runs = [pool.submit(run_part, args.python, config_path, proto, numbers, dest / symbol, dest / symbol / name)
                for symbol, name, proto, numbers in calls]
        done = [r.result() for r in runs]
    results = []
    for symbol, ps in zip(symbols, coin_parts):
        mine = [d for (sym, *_), d in zip(calls, done) if sym == symbol]
        results.append(({**ps[0][1], "windows": [w for _, p, _ in ps for w in p["windows"]]} if ps else None,
                        [r for rows, _ in mine for r in rows], [f for _, failed in mine for f in failed]))
    for symbol, (proto, rows, failed) in zip(symbols, results):
        windows = proto["windows"]
        part = f"- {symbol}: {len(rows)} of {len(windows)} windows run."
        if left[symbol]:
            why = {}
            for k, y in left[symbol]:
                why.setdefault(y, []).append(f"w{k}")
            part += f" {len(left[symbol])} left out by the data use (common/data_use.md, section 3): " + "; ".join(
                f"{', '.join(ws)} ({y})" for y, ws in why.items()) + "."
        if rows:
            part += ("\n\n| window | trades | forecast vs next return (all bars) | net return % |\n|---|---|---|---|\n"
                     + "".join(f"| w{k} | {t} | {fc} | {nr} |\n" for k, t, fc, nr in rows))
        for k, reason, tail in failed:
            part += f"\n- w{k} not run: {reason}.\n\n```\n{tail}\n```\n"
        report.append(part)
        lo = f" ({len(left[symbol])} left out by the data use)" if left[symbol] else ""
        if rows:
            summary.append(f"{symbol} {len(rows)}/{len(windows)}" + (f" ({len(failed)} not run: {failed[0][1]})" if failed else "") + lo)
        else:
            summary.append(f"{symbol} not run ({failed[0][1] if failed else 'no window'})" + lo)
    venue = proto["venue"]["label"] if proto else ""
    write_atomic(dest / "run.md", f"# Backtest of {plan_id}\n\n"
                 f"- Plan: `{os.path.relpath(plan_path, dest)}`\n- Config: `config.json` (a copy of the plan's config)\n"
                 f"- Data: {instruments} as {', '.join(f'{b}USD' for b in coins(instruments))}; {bar} bars; {period}\n"
                 f"- Venue: {venue}\n- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window\n\n"
                 + "\n".join(report) + "\n")
    ran = any(" not run" not in s for s in summary)
    index_line(index_path, plan_id, f"{plan_id}: {'ran' if ran else 'not run'}: {'; '.join(summary)} [{bar}, {period}]")
    print(f"{plan_id}: {'; '.join(summary)}")


if __name__ == "__main__":
    main()
