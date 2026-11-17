"""Proof that a change to shared code leaves the backtest unchanged (CLAUDE.md, "Shared code").

    python live/proof/backtest_fingerprint.py run OUT_DIR       # run the fixed backtests, keep their files
    python live/proof/backtest_fingerprint.py compare DIR_A DIR_B   # file by file; prints every difference

Fixed inputs (same every time, all read from the committed caches in local_data/):
  kraken_1d    the first live strategy on BTCUSD, Kraken, daily bars, the first two windows of fold A,
               exactly as the step-4 card calls the engine (warm-up loaded, bar equity, Kraken futures costs)
  kraken_1h_1d the same strategy and first window, hourly candles combined into daily bars
               (fetch_interval_seconds=3600): the path live uses
Run from trading-bot/ with the venv's python. Window dates are read from the fold files, never written here.
"""
import json
import shutil
import sys
from pathlib import Path

BOT = Path(__file__).resolve().parents[2]
REPO = BOT.parent
sys.path.insert(0, str(BOT))
sys.path.insert(0, str(BOT / "backtest"))

LIVE_STRATEGY = (REPO / "strategy_designer_v2" / "steps_cards" / "04_backtest" / "night_013_run" / "backtests"
                 / "013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month"
                   ".d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d" / "config.json")

# Fields that legitimately differ between two runs of the same input: when and from which commit it ran.
ALLOWED_JSON_KEYS = {"created_utc", "timestamp", "run_timestamp", "git_sha", "git_dirty", "utc", "started_utc",
                     "finished_utc", "duration_seconds", "run_id"}


def _cases():
    import research_folds as rf
    from data.data_manager import _holdout_bounds
    windows = rf.fold_windows(rf.load_folds(), "A")
    holdout_start = _holdout_bounds()[0].strftime("%Y-%m-%d")
    kraken = dict(config_path=str(LIVE_STRATEGY), symbol="BTCUSD", interval_seconds=86400, warmup_prefetch=True,
                  bar_equity=True, holdout_start=holdout_start, exchange="kraken", market_type="futures")
    cases = {}
    cases["kraken_1d"] = [dict(kraken, start=w["test"]["start"], end=w["test"]["end"]) for w in windows[:2]]
    cases["kraken_1h_1d"] = [dict(kraken, start=windows[0]["test"]["start"], end=windows[0]["test"]["end"],
                                  fetch_interval_seconds=3600)]
    return cases


def run(out_dir):
    from core.launcher import run_backtest
    out = Path(out_dir)
    if out.exists():
        sys.exit(f"{out} exists; give a new folder")
    for name, calls in _cases().items():
        for i, kw in enumerate(calls):
            dest = out / f"{name}_{i}"
            dest.mkdir(parents=True)
            rd = run_backtest(results_root=str(dest / "results"),
                              trades_log_file=str(dest / "interim_trades.json"), **kw)
            shutil.copytree(rd, dest / "run")
            shutil.rmtree(dest / "results", ignore_errors=True)
            print(f"{name}_{i}: {len(list((dest / 'run').rglob('*')))} files")


ALLOWED_SEEN = set()


def _xlsx_cells(path):
    """An .xlsx is a zip stamped with its creation time: compare the cells, not the bytes."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


def _json_diff(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k in ALLOWED_JSON_KEYS:
                if a.get(k) != b.get(k):
                    ALLOWED_SEEN.add(f"{path}.{k}")
                continue
            out += _json_diff(a.get(k), b.get(k), f"{path}.{k}")
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in _json_diff(x, y, f"{path}[{i}]")]
    return [] if a == b else [f"{path}: {str(a)[:80]} != {str(b)[:80]}"]


def compare(dir_a, dir_b):
    a, b = Path(dir_a), Path(dir_b)
    fa = {p.relative_to(a) for p in a.rglob("*") if p.is_file()}
    fb = {p.relative_to(b) for p in b.rglob("*") if p.is_file()}
    problems = [f"only in A: {p}" for p in sorted(fa - fb)] + [f"only in B: {p}" for p in sorted(fb - fa)]
    same = 0
    for rel in sorted(fa & fb):
        xa, xb = (a / rel).read_bytes(), (b / rel).read_bytes()
        if xa == xb:
            same += 1
            continue
        if rel.suffix == ".json":
            diffs = _json_diff(json.loads(xa), json.loads(xb))
            if not diffs:
                print(f"same except allowed run fields: {rel}")
                same += 1
                continue
            problems += [f"{rel} {d}" for d in diffs]
        elif rel.suffix == ".xlsx" and _xlsx_cells(a / rel) == _xlsx_cells(b / rel):
            print(f"same cells (file stamp aside): {rel}")
            same += 1
        else:
            problems.append(f"differs: {rel}")
    print(f"{len(fa & fb)} files in both, {same} identical (allowed fields aside), {len(problems)} problems")
    for p in problems:
        print("  " + p)
    print("allowed fields that differed:", sorted(ALLOWED_SEEN) or "none")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "run":
        run(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "compare":
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    else:
        sys.exit(__doc__)
