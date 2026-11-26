"""common_record: a candidate's common record (common/data_use.md, step 9). One plan, its config unchanged, on every
portfolio coin (common/coins.py, portfolio_group(): 25 coins) over the 32 windows of
04_backtest/windows/research_2016.json, a (coin, window) pair only when coins.usable(coin, window start) (after the
coin's first 90 days); then the record's chart files, step 5's measure (the plan's own measure.py, no model call:
information) and step 6's check.

  python3 common_record.py PLAN --run NAME_run --python VENV_PYTHON
  python3 common_record.py --register --shard i/n --python VENV_PYTHON

PLAN is a plan in 03_test_plan/<run>/plans/; its in-sample measure.py is read from 05_verification/<run>/verdicts/<id>/.
--register: every `paying` book of orchestration/ideas_similarities_check/register/books.json (its plan from its run),
in the register's key order, shard i of n (the books whose position p, from 0, has p % n == i - 1); a book whose result
exists is not run again (resumable).

The files (the fixed interface, read by the portfolio's builders):
  04_backtest/<run>/common/backtests/<id>/        the record (run.md, config.json, <SYMBOL>/wK/, chart_bars.csv.gz,
                                                  chart_trades.csv.gz); wK is the K-th window of research_2016.json
                                                  for every coin, so one K is one period
  05_verification/<run>/common/verdicts/<id>/     step 5 (result.json, verdict.md, measure.py)
  06_profitability/<run>/common/checks/<id>/      step 6 (result.json, check.md)
  orchestration/common_record/<run>/<id>.json     the result; orchestration/common_record/INDEX.md, one line per record
A step whose output exists is not called again. Prints one last line: the result as JSON.

Why this cannot leak: no bar is read here; the engine runs each window as step 4 does (its own dates and warm-up), and
the 90-day rule reads only each coin's first day. The final group's coins are never read: the coins come from
portfolio_group(), which leaves them out.
"""
import argparse, contextlib, fcntl, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
REPO = STEPS.parents[1]
sys.path.insert(0, str(STEPS / "common"))
sys.path.insert(0, str(STEPS / "04_backtest" / "helper"))
from lib import write_atomic, utc_now, header_fields  # noqa: E402
import coins  # noqa: E402  (the coin groups and the 90-day rule)
import run_backtest as rb  # noqa: E402  (step 4's own calls of the engine, used unchanged)

WINDOWS = STEPS / "04_backtest" / "windows" / "research_2016.json"
NAME = "common"     # the folder of the common records in each step's run folder
REGISTER = STEPS / "orchestration" / "ideas_similarities_check" / "register" / "books.json"


def folders(run, steps=None):
    s = steps or STEPS
    return {"backtests": s / "04_backtest" / run / NAME / "backtests",
            "verdicts": s / "05_verification" / run / NAME / "verdicts",
            "checks": s / "06_profitability" / run / NAME / "checks",
            "result": s / "orchestration" / "common_record" / run}


@contextlib.contextmanager
def lock(name):
    """Shards run at the same time on one machine: an index (read, a line changed, written) is updated by one at a
    time. The lock file is in the system's temporary folder, outside the repository."""
    with open(Path(tempfile.gettempdir()) / f"common_record_{name}.lock", "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def coin_windows(windows, coin_list, usable=coins.usable):
    """{coin: (K before its first window, its windows)}: each coin's windows that start after its first 90 days. A
    coin's first usable day is fixed, so its usable windows are the last ones of the file: K continues the file's
    numbering (w1 = the file's first window for every coin)."""
    out = {}
    for c in coin_list:
        keep = [k for k, w in enumerate(windows) if usable(c, w["test"]["start"])]
        if keep:
            out[c] = (keep[0], windows[keep[0]:])
    return out


def backtest(plan, python, dest, windows, coin_list, usable=coins.usable):
    """Step 4 on the common data: one wrapper call per coin on its usable windows, the calls at the same time, with
    step 4's own run_part (each window its own run_backtest call, warm-up and holdout guard). Writes run.md in step 4's
    shape and returns the index line."""
    plan_id, h = plan.stem, header_fields(plan.read_text(encoding="utf-8"))
    bar = h["data-bar"]
    per = coin_windows(windows, coin_list, usable)
    config_path = plan.with_name(plan_id + "_config.json")
    if dest.exists():
        import shutil
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    (dest / "config.json").write_bytes(config_path.read_bytes())
    syms = {c: f"{c}USD" for c in coin_list}
    protos = {c: rb.protocol(python, syms[c], bar, None, ws) for c, (_, ws) in per.items()}
    with ThreadPoolExecutor(max_workers=max(1, min(len(protos), rb.cores()))) as pool:
        futs = {c: pool.submit(rb.run_part, python, config_path, protos[c], per[c][0], dest / syms[c],
                               dest / syms[c] / "windows") for c in protos}
        done = {c: f.result() for c, f in futs.items()}
    report, summary = [], []
    for c in coin_list:
        sym = syms[c]
        if c not in per:
            report.append(f"- {sym}: 0 of 0 windows run (every window starts before the coin's 91st day).")
            summary.append(f"{sym} not run (every window before its 91st day)")
            continue
        before, ws = per[c]
        rows, failed = done[c]
        part = f"- {sym}: {len(rows)} of {len(ws)} windows run."
        if before:
            part += f" w1 to w{before} not used: they start before the coin's 91st day (common/data_use.md)."
        if rows:
            part += ("\n\n| window | trades | forecast vs next return (all bars) | net return % |\n|---|---|---|---|\n"
                     + "".join(f"| w{k} | {t} | {fc} | {nr} |\n" for k, t, fc, nr in rows))
        for k, reason, tail in failed:
            part += f"\n- w{k} not run: {reason}.\n\n```\n{tail}\n```\n"
        report.append(part)
        summary.append(f"{sym} {len(rows)}/{len(ws)}" + (f" ({len(failed)} not run: {failed[0][1]})" if failed else "")
                       if rows else f"{sym} not run ({failed[0][1] if failed else 'no window'})")
    venue = next(iter(protos.values()))["venue"]["label"] if protos else ""
    instruments = ", ".join(coin_list)
    write_atomic(dest / "run.md", f"# Backtest of {plan_id}\n\n"
                 f"- Plan: `{os.path.relpath(plan, dest)}`\n- Config: `config.json` (a copy of the plan's config)\n"
                 f"- Data: {instruments} as {', '.join(syms[c] for c in coin_list)}; {bar} bars; windows {WINDOWS.stem}"
                 f" (the common record: every portfolio coin, each window after the coin's first 90 days)\n"
                 f"- Venue: {venue}\n- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, "
                 f"unchanged; warm-up loaded before each window\n\n" + "\n".join(report) + "\n")
    ran = any(" not run" not in s for s in summary)
    return f"{plan_id}: {'ran' if ran else 'not run'}: {'; '.join(summary)} [{bar}, windows {WINDOWS.stem}]"


def ran(record):
    """Step 4's output exists: run.md and at least one window run."""
    return (record / "run.md").exists() and any(record.glob("*/w*/metrics.json"))


def call(cmd):
    """One step's helper; its whole output printed (the caller's log keeps it)."""
    r = subprocess.run([sys.executable] + [str(c) for c in cmd], capture_output=True, text=True)
    print(f"--- {Path(str(cmd[0])).name} (exit {r.returncode})\n{(r.stdout + r.stderr).strip()}", flush=True)
    return r.returncode


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def commit():
    r = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True)
    d = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"],
                       capture_output=True, text=True)
    return r.stdout.strip() + ("-dirty" if d.stdout.strip() else "")


def coverage(record):
    """{symbol: windows run} of a record."""
    return {d.name: len(list(d.glob("w*/metrics.json"))) for d in sorted(record.iterdir())
            if d.is_dir() and any(d.glob("w*/metrics.json"))} if record.is_dir() else {}


def index_line(rel_id, r):
    s5, s6 = r["step5"], r["step6"]
    sh = {m["measure"]: m["value"] for m in (s6.get("measures") or [])}
    f = lambda x: "-" if x is None else f"{x:+.2f}"
    return (f"{rel_id}: {len(r['coins_run'])} of {len(r['coins_asked'])} coins, {r['windows_run']} coin-windows; "
            f"step 5 {s5.get('status')} (main {s5.get('main')}); step 6 {s6.get('status')} "
            f"(Sharpe {f(sh.get('sharpe_min'))}, minus holding {f(sh.get('sharpe_vs_hold_min'))}, "
            f"Calmar {f(sh.get('calmar_min'))}); {r['seconds']:.0f} s")


def record_one(plan, run, python, steps=None, coin_list=None, usable=coins.usable):
    """The common record of one plan, every step skipped whose output exists. Returns the result."""
    steps = steps or STEPS
    plan = Path(plan).resolve()
    rid = plan.stem
    f = folders(run, steps)
    out_file = f["result"] / f"{rid}.json"
    measure_py = steps / "05_verification" / run / "verdicts" / rid / "measure.py"
    if not measure_py.exists():
        sys.exit(f"no in-sample measure.py for {rid} in {run}")
    coin_list = coin_list or coins.portfolio_group()
    windows = json.loads(WINDOWS.read_text(encoding="utf-8"))
    t0, made_by = time.time(), commit()      # the code, read before this call writes any (tracked) index
    record = f["backtests"] / rid
    for k in ("backtests", "verdicts", "checks", "result"):
        f[k].mkdir(parents=True, exist_ok=True)
    if not ran(record):
        line = backtest(plan, python, record, windows, coin_list, usable)
        with lock(run):
            rb.index_line(f["backtests"] / "INDEX.md", rid, line)
        print(line, flush=True)
    if ran(record) and not (record / "chart_bars.csv.gz").exists():
        call([steps / "04_backtest/helper/chart_files.py", record])        # committed names: a candidate's record
    with lock(run):                                                         # steps 5 and 6 write their INDEX.md
        if ran(record) and not (f["verdicts"] / rid / "result.json").exists():
            call([steps / "05_verification/helper/make_verdict.py", plan, "--python", python, "--records-root",
                  f["backtests"], "--verdicts-dir", f["verdicts"], "--measure", measure_py])
        if ran(record) and not (f["checks"] / rid / "result.json").exists():
            call([steps / "06_profitability/helper/check_profitability.py", record, "--checks-dir", f["checks"]])
    v, c = load(f["verdicts"] / rid / "result.json"), load(f["checks"] / rid / "result.json")
    cov = coverage(record)
    mm = (v or {}).get("main_measure") or {}
    st = mm.get("statistic")
    old = load(out_file) or {}
    res = {"plan": os.path.relpath(plan, steps), "run": run, "id": rid,
           "record": os.path.relpath(record, steps), "windows_file": os.path.relpath(WINDOWS, steps),
           "coins_asked": [f"{x}USD" for x in coin_list], "coins_run": sorted(cov), "coin_windows": cov,
           "windows_run": sum(cov.values()),
           "step5": {"status": (v or {}).get("status", "no verdict"), "main": mm.get("value"),
                     "statistic": st.get("value") if isinstance(st, dict) else None},
           "step6": {"status": (c or {}).get("status", "not checked"), "measures": (c or {}).get("measures", []),
                     "informative": (c or {}).get("informative")},
           "seconds": round(time.time() - t0 + (old.get("seconds") or 0.0), 1),     # every call's time, a resume's added
           "made_utc": old.get("made_utc") or utc_now(), "commit": old.get("commit") or made_by}
    write_atomic(out_file, json.dumps(res, indent=2) + "\n")
    index = steps / "orchestration" / "common_record" / "INDEX.md"
    key = f"{run}/{rid}"
    with lock("index"):
        lines = [l for l in (index.read_text(encoding="utf-8").splitlines() if index.exists() else [])
                 if ": " in l and not l.startswith(("#", key + ":"))]
        write_atomic(index, "# Common records (orchestration/common_record/card.md): one line per record\n\n"
                     + "".join(l + "\n" for l in sorted(lines + [index_line(key, res)])))
    return res


def paying_books(register=REGISTER):
    """The register's paying books, in its key order."""
    return sorted((b for b in json.loads(Path(register).read_text(encoding="utf-8")) if b.get("kind") == "paying"),
                  key=lambda b: b["key"])


def shard(items, i, n):
    return [x for p, x in enumerate(items) if p % n == i - 1]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("plan", type=Path, nargs="?")
    a.add_argument("--run")
    a.add_argument("--python", required=True)
    a.add_argument("--register", action="store_true", help="every paying book of the similarity register")
    a.add_argument("--shard", default="1/1", help="i/n: shard i of n of the register's paying books")
    a.add_argument("--only", help="with --register: these register keys only (comma-separated), within the shard")
    args = a.parse_args()
    if args.register:
        i, n = (int(x) for x in args.shard.split("/"))
        books = shard(paying_books(), i, n)
        if args.only:
            books = [b for b in books if b["key"] in set(args.only.split(","))]
        print(f"shard {i}/{n}: {len(books)} paying books", flush=True)
        for b in books:
            if (folders(b["run"])["result"] / f"{b['id']}.json").exists():
                print(f"{b['key']}: record exists, not run again", flush=True)
                continue
            t0 = time.time()
            r = record_one(STEPS / "03_test_plan" / b["run"] / "plans" / f"{b['id']}.md", b["run"], args.python)
            print(f"{b['key']}: {time.time() - t0:.0f} s; {json.dumps({'step6': r['step6']['status']})}", flush=True)
        return
    if not args.plan or not args.run:
        a.error("give a PLAN and --run, or --register")
    r = record_one(args.plan, args.run, args.python)
    print(json.dumps({"common_record": index_line(f"{args.run}/{r['id']}", r)}))


if __name__ == "__main__":
    main()
