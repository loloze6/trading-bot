"""Tests of step 4's helper: when one wrapper call per coin is used, the fallback to one call per window, and the
coins at the same time. The wrapper is replaced by a fake that writes run folders; no engine runs, no data is read."""
import json
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_backtest as rb  # noqa: E402

WINDOWS = [{"label": f"W{i}", "test": {"start": "s", "end": "e"}} for i in (1, 2, 3)]


def fake_call(out, windows, run_ids=None, rc=0, summary=True, log="log"):
    """What one wrapper call leaves in its output folder: one run folder per run id, and the summary."""
    run_ids = run_ids or [f"run_{w['label']}" for w in windows]
    for i, rid in enumerate(run_ids):
        d = out / "results" / rid
        d.mkdir(parents=True, exist_ok=True)
        (d / "metrics.json").write_text(json.dumps({"core": {"trade_count": i, "forecast_return_corr_all_bars": 0.1,
                                                              "net_return_pct": 1.0}}))
        (d / "bars.csv").write_text(f"bars of {rid}\n")
    if summary:
        (out / "protocol_summary.json").write_text(json.dumps(
            {"results": [{"window": w["label"], "run_id": rid} for w, rid in zip(windows, run_ids)]}))
    return rc, log, out


# --- coin_runs: when the coin's call can be used -------------------------------------------------------------------

def test_coin_call_used_when_every_window_has_its_own_folder(tmp_path):
    rc, _, out = fake_call(tmp_path, WINDOWS)
    assert rb.coin_runs(rc, out, WINDOWS) == [out / "results" / f"run_W{i}" for i in (1, 2, 3)]


def test_not_used_when_the_call_failed(tmp_path):
    rc, _, out = fake_call(tmp_path, WINDOWS, rc=1)
    assert rb.coin_runs(rc, out, WINDOWS) is None


def test_not_used_when_two_windows_share_a_run_folder(tmp_path):
    # same second, same config hash: one folder for two windows
    rc, _, out = fake_call(tmp_path, WINDOWS, run_ids=["run_a", "run_a", "run_b"])
    assert rb.coin_runs(rc, out, WINDOWS) is None


def test_not_used_without_a_summary(tmp_path):
    rc, _, out = fake_call(tmp_path, WINDOWS, summary=False)
    assert rb.coin_runs(rc, out, WINDOWS) is None


def test_not_used_when_the_summary_lists_other_windows(tmp_path):
    rc, _, out = fake_call(tmp_path, WINDOWS)
    assert rb.coin_runs(rc, out, WINDOWS[:2]) is None          # three folders for two windows
    assert rb.coin_runs(rc, out, list(reversed(WINDOWS))) is None   # another order


def test_not_used_when_a_run_folder_has_no_metrics(tmp_path):
    rc, _, out = fake_call(tmp_path, WINDOWS)
    (out / "results" / "run_W2" / "metrics.json").unlink()
    assert rb.coin_runs(rc, out, WINDOWS) is None


# --- main: the record, with the coin's call and with the fallback --------------------------------------------------

@pytest.fixture
def plan(tmp_path):
    p = tmp_path / "plans" / "001-01_some-idea_1d.md"
    p.parent.mkdir()
    p.write_text("---\ndata-instruments: BTC, ETH\ndata-bar: 1d\ndata-period: fold A\noutcome: plan\n---\nbody\n")
    (p.parent / "001-01_some-idea_1d_config.json").write_text("{}")
    return p


def run_main(monkeypatch, plan, out_root, wrapper):
    calls = []   # (coin, windows) per call; the coins run at the same time, so only each coin's own order is fixed

    def call_protocol(python, config_path, proto, windows, tmp):
        calls.append((proto["symbols"][0], [w["label"] for w in windows]))
        return wrapper(proto["symbols"][0], windows, tmp / "out")

    monkeypatch.setattr(rb, "protocol", lambda python, symbol, bar, folds, windows=None: {
        "symbols": [symbol], "windows": WINDOWS, "venue": {"label": "Kraken spot"}})
    monkeypatch.setattr(rb, "call_protocol", call_protocol)
    monkeypatch.setattr(sys, "argv", ["run_backtest.py", str(plan), "--python", "py", "--out-root", str(out_root), "--force"])
    rb.main()
    return calls


def test_one_call_per_coin_and_fallback_for_a_coin_whose_call_fails(monkeypatch, plan, tmp_path):
    def wrapper(symbol, windows, out):
        if symbol == "ETHUSD" and any(w["label"] == "W2" for w in windows):
            # the wrapper stops at W2: the coin's call fails, and so does W2 on its own
            return 1, "Traceback\nRuntimeError: No historical data for ETHUSD", out
        return fake_call(out, windows, log=f"log of {symbol} {[w['label'] for w in windows]}")

    out_root = tmp_path / "backtests"
    calls = run_main(monkeypatch, plan, out_root, wrapper)
    assert [w for c, w in calls if c == "BTCUSD"] == [["W1", "W2", "W3"]]
    assert [w for c, w in calls if c == "ETHUSD"] == [["W1", "W2", "W3"], ["W1"], ["W2"], ["W3"]]

    rec = out_root / "001-01_some-idea_1d"
    # BTC: one call; window files per window, the call's files in the call's folder
    for k in (1, 2, 3):
        assert (rec / "BTCUSD" / f"w{k}" / "bars.csv.gz").exists()
        assert (rec / "BTCUSD" / f"w{k}" / "metrics.json").exists()
        assert not (rec / "BTCUSD" / f"w{k}" / "engine_log.txt").exists()
    assert (rec / "BTCUSD" / "fold_A" / "engine_log.txt").read_text() == "log of BTCUSD ['W1', 'W2', 'W3']"
    assert (rec / "BTCUSD" / "fold_A" / "protocol_summary.json.gz").exists()
    # ETH: one call per window, as before 2026-11-16; nothing left from the failed coin call
    assert sorted(p.name for p in (rec / "ETHUSD").iterdir()) == ["w1", "w3"]
    assert (rec / "ETHUSD" / "w1" / "engine_log.txt").read_text() == "log of ETHUSD ['W1']"
    assert (rec / "ETHUSD" / "w3" / "protocol_summary.json.gz").exists()

    run_md = (rec / "run.md").read_text()
    assert "- BTCUSD: 3 of 3 windows run." in run_md
    assert "- ETHUSD: 2 of 3 windows run." in run_md
    assert "- w2 not run: no historical data on the venue." in run_md
    assert (out_root / "INDEX.md").read_text() == (
        "001-01_some-idea_1d: ran: BTCUSD 3/3; ETHUSD 2/3 (1 not run: no historical data on the venue) [1d, fold A]\n")


def test_fallback_when_two_windows_share_a_run_folder(monkeypatch, plan, tmp_path):
    def wrapper(symbol, windows, out):
        if len(windows) > 1:
            return fake_call(out, windows, run_ids=["run_x", "run_x", "run_y"])
        return fake_call(out, windows)

    out_root = tmp_path / "backtests"
    calls = run_main(monkeypatch, plan, out_root, wrapper)
    for coin in ("BTCUSD", "ETHUSD"):
        assert [len(w) for c, w in calls if c == coin] == [3, 1, 1, 1]
    rec = out_root / "001-01_some-idea_1d"
    for coin in ("BTCUSD", "ETHUSD"):
        assert sorted(p.name for p in (rec / coin).iterdir()) == ["w1", "w2", "w3"]
        assert (rec / coin / "w2" / "bars.csv.gz").exists()
    assert "BTCUSD 3/3; ETHUSD 3/3" in (out_root / "INDEX.md").read_text()


# --- the coins at the same time ------------------------------------------------------------------------------------

def test_one_call_per_coin_and_fold_windows_numbered_in_the_folds_order(monkeypatch, plan, tmp_path):
    plan.write_text(plan.read_text().replace("fold A", "folds A, B"))

    def wrapper(symbol, windows, out):
        return fake_call(out, windows, log=f"log of {symbol} {[w['label'] for w in windows]}")

    out_root = tmp_path / "backtests"
    calls = run_main(monkeypatch, plan, out_root, wrapper)
    for coin in ("BTCUSD", "ETHUSD"):
        assert [w for c, w in calls if c == coin] == [["W1", "W2", "W3"], ["W1", "W2", "W3"]]   # fold A, fold B
    rec = out_root / "001-01_some-idea_1d"
    assert sorted(p.name for p in (rec / "BTCUSD").iterdir()) == ["fold_A", "fold_B", "w1", "w2", "w3", "w4", "w5", "w6"]
    assert (rec / "BTCUSD" / "fold_B" / "protocol_summary.json.gz").exists()
    assert (rec / "BTCUSD" / "w4" / "bars.csv.gz").exists()
    run_md = (rec / "run.md").read_text()
    assert "- BTCUSD: 6 of 6 windows run." in run_md and "| w6 |" in run_md
    assert "BTCUSD 6/6; ETHUSD 6/6 [1d, folds A, B]" in (out_root / "INDEX.md").read_text()


def test_coins_run_at_the_same_time_up_to_the_cores(monkeypatch, plan, tmp_path):
    plan.write_text(plan.read_text().replace("BTC, ETH", "BTC, ETH, LTC, XMR, XRP, ZEC"))
    monkeypatch.setattr(rb, "cores", lambda: 4)
    running, most = [0], [0]
    lock = threading.Lock()

    def wrapper(symbol, windows, out):
        with lock:
            running[0] += 1
            most[0] = max(most[0], running[0])
        time.sleep(0.05)
        with lock:
            running[0] -= 1
        return fake_call(out, windows)

    run_main(monkeypatch, plan, tmp_path / "backtests", wrapper)
    assert most[0] == 4          # 6 coins, 4 cores: 4 at once, never more


def test_the_record_keeps_the_coins_order_whatever_finishes_first(monkeypatch, plan, tmp_path):
    plan.write_text(plan.read_text().replace("BTC, ETH", "BTC, ETH, LTC"))
    monkeypatch.setattr(rb, "cores", lambda: 3)

    def wrapper(symbol, windows, out):
        time.sleep({"BTCUSD": 0.2, "ETHUSD": 0.1, "LTCUSD": 0.0}[symbol])   # BTC finishes last
        return fake_call(out, windows)

    out_root = tmp_path / "backtests"
    run_main(monkeypatch, plan, out_root, wrapper)
    run_md = (out_root / "001-01_some-idea_1d" / "run.md").read_text()
    assert run_md.index("- BTCUSD:") < run_md.index("- ETHUSD:") < run_md.index("- LTCUSD:")
    assert "BTCUSD 3/3; ETHUSD 3/3; LTCUSD 3/3" in (out_root / "INDEX.md").read_text()


def test_each_call_has_its_own_interim_trades_file(monkeypatch, tmp_path):
    seen = []
    monkeypatch.setattr(rb.subprocess, "run", lambda cmd, **kw: seen.append(cmd) or
                        type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})())
    rb.call_protocol("py", tmp_path / "c.json", {"symbols": ["BTCUSD"]}, WINDOWS, tmp_path)
    assert "--trades-file-in-out-dir" in seen[0]


def test_coins_in_place_of_the_plans(monkeypatch, plan, tmp_path):
    """--coins: the same plan, config and folds on other coins; the record names them, and its rerun check reads them."""
    seen = []
    monkeypatch.setattr(rb, "protocol", lambda python, symbol, bar, folds, windows=None: seen.append((symbol, folds)) or {
        "symbols": [symbol], "windows": WINDOWS, "venue": {"label": "Kraken spot"}})
    monkeypatch.setattr(rb, "call_protocol", lambda python, config_path, proto, windows, tmp: fake_call(tmp / "out", windows))
    out_root = tmp_path / "backtests"
    monkeypatch.setattr(sys, "argv", ["run_backtest.py", str(plan), "--python", "py", "--out-root", str(out_root),
                                      "--coins", "ADA, SOL"])
    rb.main()
    assert sorted(seen) == [("ADAUSD", ["A"]), ("SOLUSD", ["A"])]
    rec = out_root / "001-01_some-idea_1d"
    assert "- Data: ADA, SOL as ADAUSD, SOLUSD; 1d bars; fold A\n" in (rec / "run.md").read_text()
    assert sorted(p.name for p in rec.iterdir() if p.is_dir()) == ["ADAUSD", "SOLUSD"]
    seen.clear()
    rb.main()                                        # the same coins again: the record is kept
    assert seen == []
    monkeypatch.setattr(sys, "argv", ["run_backtest.py", str(plan), "--python", "py", "--out-root", str(out_root)])
    rb.main()                                        # the plan's own coins: another record, so it runs
    assert sorted(seen) == [("BTCUSD", ["A"]), ("ETHUSD", ["A"])]
