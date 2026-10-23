"""
tools/cache_gap_census.py -- the data-quality audit mode (--audit / --write-census / --run-dir).

All fixtures are built in tmp_path at run time with dates in 2019-2021 only. The
holdout used by the audit tests is a SANDBOX policy written into tmp_path (and
pointed at by both the census and data.data_manager's seal guard); rows at or
after its start are built at run time from that policy's bound. The real
holdout's dates appear nowhere in this file, and no assertion prints a bound.
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))

import pandas as pd  # noqa: E402

import cache_gap_census as cgc  # noqa: E402
import data_availability_gate as gate  # noqa: E402
import holdout_policy as hp  # noqa: E402
import research_folds as rf  # noqa: E402
import seal_safe_cache as ssc  # noqa: E402
from data import data_manager as dm  # noqa: E402

DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")

SANDBOX_POLICY = {
    "holdout_range": ["2021-07-01", "2021-12-31"],
    "eras": [
        {"era_id": "era_pre", "range": ["2018-01-01", "2018-12-31"]},
        {"era_id": "era_a", "range": ["2019-01-01", "2019-01-05"]},
        {"era_id": "era_b", "range": ["2019-01-06", "2019-01-20"]},
        {"era_id": "era_late", "range": ["2019-02-01", "2019-02-28"]},
        {"era_id": "era_straddle", "range": ["2021-06-01", "2021-07-15"]},
        {"era_id": "era_holdout", "range": ["2021-07-01", "2021-12-31"]},
        {"era_id": "era_after", "range": ["2022-01-01", None]},
    ],
}


@pytest.fixture
def policy(tmp_path, monkeypatch):
    """The sandbox policy: written to tmp_path, used by the census AND the seal guard."""
    p = tmp_path / "sandbox_policy.yaml"
    p.write_text(yaml.safe_dump(SANDBOX_POLICY), encoding="utf-8")
    monkeypatch.setattr(dm, "_POLICY_PATH", p)
    return p


def sandbox_start(policy_path) -> pd.Timestamp:
    return pd.Timestamp(hp.holdout_start_of(hp.load_policy(policy_path)))


def write_cache(path: Path, stamps, extra_cols=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({"timestamp": [str(t) for t in stamps]})
    if extra_cols:
        for c in ("open", "high", "low", "close", "volume"):
            df[c] = 1.0
    df.to_csv(path, index=False)


def grid(start, n, freq, skip=()):
    idx = pd.date_range(start, periods=n, freq=freq)
    skip = {pd.Timestamp(s) for s in skip}
    return [t for t in idx if t not in skip]


def folds_doc(a=(("2019-03-01", "2019-03-31"),), d=()):
    def blocks(rows):
        return [{"label": f"w{i}", "start": s, "end": e} for i, (s, e) in enumerate(rows)]
    return {"folds": {"A": blocks(a), "B": blocks(a), "C": blocks(a), "D": blocks(d)}}


def ctx_for(policy_path, warmup_bars=None):
    return cgc._context(policy_path, warmup_bars)


def index_of(stamps):
    return pd.DatetimeIndex(pd.to_datetime(list(stamps)))


# ---------------------------------------------------------------------------
# the default output is unchanged
# ---------------------------------------------------------------------------

def _legacy_fixture(root: Path) -> Path:
    d = root / "legacy_data"
    write_cache(d / "AAAUSDT_1h.csv", grid("2019-01-01", 600, "h", skip=["2019-01-03 05:00"]))
    write_cache(d / "BBBUSDT_1h.csv", grid("2019-02-01", 500, "h", skip=grid("2019-02-04", 30, "h")))
    write_cache(d / "AAAUSDT_1d.csv", grid("2019-01-01", 200, "D", skip=["2019-02-02"]))
    return d


@pytest.mark.parametrize("tf", ["1h", "1d"])
def test_default_output_byte_identical_to_pre_change_tool(tmp_path, capsys, monkeypatch, tf):
    data = _legacy_fixture(tmp_path)
    src = subprocess.run(["git", "show", "origin/master:strategy-research/tools/cache_gap_census.py"],
                         capture_output=True, cwd=str(SR_ROOT))
    if src.returncode != 0:
        pytest.skip("origin/master is not available in this checkout")
    old_file = tmp_path / "old_cache_gap_census.py"
    old_file.write_bytes(src.stdout)
    spec = importlib.util.spec_from_file_location("old_cache_gap_census", old_file)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)

    argv = ["--data-dir", str(data), "--timeframe", tf, "--warmup", "30", "--block", "6"]
    monkeypatch.setattr(sys, "argv", ["census", *argv])
    assert old.main() == 0
    old_out = capsys.readouterr().out
    assert cgc.main(argv) == 0
    new_out = capsys.readouterr().out
    assert old_out == new_out and len(old_out) > 300
    assert "sealed" not in new_out and "census_" not in new_out


PINNED_LEGACY_SHA256 = {
    "1h": "d39785c564ef75f07be7af459650c21df8c001cbb938728cc88897c77b51c472",
    "1d": "44ad80984038672c51fede77c7e854aeb42028506a542988978d8fddfa9c8927",
}


@pytest.mark.parametrize("tf", ["1h", "1d"])
def test_default_output_pinned_hash(tmp_path, capsys, tf):
    """CI-independent pin: the pre-change tool's output on this fixture (captured from
    origin/master:strategy-research/tools/cache_gap_census.py). Survives the merge, when
    the origin/master comparison above becomes a self-comparison."""
    data = _legacy_fixture(tmp_path)
    assert cgc.main(["--data-dir", str(data), "--timeframe", tf, "--warmup", "30", "--block", "6"]) == 0
    out = capsys.readouterr().out
    assert hashlib.sha256(out.encode()).hexdigest() == PINNED_LEGACY_SHA256[tf]


# ---------------------------------------------------------------------------
# the seal
# ---------------------------------------------------------------------------

def _sealed_pair(tmp_path, policy_path):
    """Same in-sample cache with and without rows planted at/after the sandbox start."""
    hs = sandbox_start(policy_path)
    base = grid(hs - pd.Timedelta(hours=300), 300, "h", skip=[hs - pd.Timedelta(hours=100)])
    planted = base + grid(hs, 60, "h") + grid(hs + pd.Timedelta(days=400), 5, "h")
    write_cache(tmp_path / "clean" / "XXXUSDT_1h.csv", base)
    write_cache(tmp_path / "planted" / "XXXUSDT_1h.csv", planted)
    return hs


def test_sealed_rows_are_dropped_before_any_statistic(tmp_path, policy):
    hs = _sealed_pair(tmp_path, policy)
    ctx = ctx_for(policy)
    groups = {"A": [{"label": "w", "test": {"start": "2021-06-20", "end": "2021-06-30"}}]}
    a = cgc.audit_cache_file(tmp_path / "clean" / "XXXUSDT_1h.csv", "1h", ctx, groups)
    b = cgc.audit_cache_file(tmp_path / "planted" / "XXXUSDT_1h.csv", "1h", ctx, groups)
    assert a == b
    assert pd.Timestamp(b["coverage"]["last_in_sample_bar"]) < hs
    assert b["coverage"]["rows"] == 299


def test_sealed_output_has_the_single_line_and_no_date_at_or_after_the_start(tmp_path, policy):
    hs = _sealed_pair(tmp_path, policy)
    census = cgc.run_audit(tmp_path / "planted", ["1h"], policy_path=policy,
                           folds_doc=folds_doc(a=(("2021-06-20", "2021-06-30"),)),
                           now=pd.Timestamp("2020-05-05", tz="UTC").to_pydatetime())
    text = yaml.safe_dump(census, sort_keys=False) + cgc.census_summary(census)
    assert census["sealed"] == "not audited"
    assert text.count("sealed: not audited") == 2  # the yaml key and the summary line
    stamps = [pd.Timestamp(m) for m in DATE.findall(text)]
    assert stamps and all(t < hs for t in stamps)
    assert "holdout" not in text.lower() and "dropped" not in text.lower()


def test_every_read_goes_through_the_seal_safe_reader_with_a_clamped_end(tmp_path, policy, monkeypatch):
    hs = _sealed_pair(tmp_path, policy)
    calls = []
    real = ssc.read_cache_csv

    def spy(path, **kw):
        calls.append(kw.get("end"))
        return real(path, **kw)

    monkeypatch.setattr(ssc, "read_cache_csv", spy)
    cgc.audit_cache_file(tmp_path / "planted" / "XXXUSDT_1h.csv", "1h", ctx_for(policy), {})
    assert len(calls) == 1 and pd.Timestamp(calls[0]) < hs


def test_guard_refusal_is_reported_without_dates(tmp_path, policy, monkeypatch):
    _sealed_pair(tmp_path, policy)

    def boom(*a, **k):
        raise ssc.SealedDataError("2021-07-01 .. 2021-12-31 secret dates")

    monkeypatch.setattr(ssc, "read_cache_csv", boom)
    with pytest.raises(cgc.AuditRefusal) as ei:
        cgc.audit_cache_file(tmp_path / "planted" / "XXXUSDT_1h.csv", "1h", ctx_for(policy), {})
    assert not DATE.search(str(ei.value))


def test_glob_is_non_recursive_and_forbidden_dirs_are_refused(tmp_path, policy):
    d = tmp_path / "data"
    write_cache(d / "AAAUSDT_1d.csv", grid("2019-01-01", 10, "D"))
    sub = d / "holdout_sealed"
    sub.mkdir()
    (sub / "ZZZUSDT_1d.csv").write_text("this is not a csv\x00", encoding="utf-8")  # would blow up if read
    census = cgc.run_audit(d, ["1d"], policy_path=policy, folds_doc=folds_doc())
    assert list(census["timeframes"]["1d"]["files"]) == ["AAAUSDT"]
    with pytest.raises(cgc.AuditRefusal):
        cgc.run_audit(sub, ["1d"], policy_path=policy, folds_doc=folds_doc())
    with pytest.raises(cgc.AuditRefusal):
        cgc.refuse_forbidden_dir(tmp_path / "x" / "recorded_reserved", "d")


# ---------------------------------------------------------------------------
# hand-computed numbers
# ---------------------------------------------------------------------------

def test_within_life_longest_gap_and_eras_hand_computed(tmp_path, policy):
    # daily bars 2019-01-01..2019-01-10 with 01-04, 01-05 (a 2-bar gap) and 01-08 missing
    stamps = grid("2019-01-01", 10, "D", skip=["2019-01-04", "2019-01-05", "2019-01-08"])
    write_cache(tmp_path / "AAAUSDT_1d.csv", stamps)
    r = cgc.audit_cache_file(tmp_path / "AAAUSDT_1d.csv", "1d", ctx_for(policy), {})
    assert r["coverage"] == {"first_bar": "2019-01-01 00:00:00", "last_in_sample_bar": "2019-01-10 00:00:00",
                             "rows": 7, "duplicate_timestamps": 0, "unparseable_timestamps": 0}
    assert r["within_life"] == {"expected_bars": 10, "missing_bars": 3, "missing_pct": 30.0}
    assert r["longest_gap"] == {"bars": 2, "after": "2019-01-03 00:00:00"}
    # era_a 01-01..01-05: 5 expected, 04 and 05 missing -> 2 (40%)
    assert r["by_era"]["era_a"] == {"expected_bars": 5, "missing_bars": 2, "missing_pct": 40.0}
    # era_b 01-06..01-20 intersect life (to 01-10): 5 expected, 01-08 missing -> 1 (20%)
    assert r["by_era"]["era_b"] == {"expected_bars": 5, "missing_bars": 1, "missing_pct": 20.0}
    # before the coin started / after it ended
    assert r["by_era"]["era_pre"] == "not_listed"
    assert r["by_era"]["era_late"] == "not_listed"
    # eras that reach or follow the (sandbox) holdout are skipped by era_id, never listed
    for skipped in ("era_straddle", "era_holdout", "era_after"):
        assert skipped not in r["by_era"]


def test_one_minute_timeframe(tmp_path, policy):
    stamps = grid("2019-05-01 00:00", 180, "min", skip=grid("2019-05-01 01:00", 5, "min"))
    write_cache(tmp_path / "AAAUSDT_1m.csv", stamps)
    r = cgc.audit_cache_file(tmp_path / "AAAUSDT_1m.csv", "1m", ctx_for(policy), {})
    assert r["within_life"] == {"expected_bars": 180, "missing_bars": 5, "missing_pct": round(500 / 180, 6)}
    assert r["longest_gap"] == {"bars": 5, "after": "2019-05-01 00:59:00"}


def test_duplicates_and_unparseable_rows_are_counted_not_folded_in(tmp_path, policy):
    p = tmp_path / "AAAUSDT_1d.csv"
    p.write_text("timestamp,close\n2019-01-01 00:00:00,1\n2019-01-01 00:00:00,1\nnot-a-date,1\n"
                 "2019-01-02 00:00:00,1\n2019-01-03 00:00:00.001000,1\n", encoding="utf-8")
    r = cgc.audit_cache_file(p, "1d", ctx_for(policy), {})
    assert r["coverage"]["rows"] == 3 and r["coverage"]["duplicate_timestamps"] == 1
    assert r["coverage"]["unparseable_timestamps"] == 1


# ---------------------------------------------------------------------------
# per-window view == the gate's own numbers
# ---------------------------------------------------------------------------

def test_window_numbers_equal_the_gates_own_functions(tmp_path, policy):
    import random
    rng = random.Random(7)
    full = grid("2019-02-20", 24 * 60, "h")
    stamps = [t for t in full if rng.random() > 0.04]
    write_cache(tmp_path / "AAAUSDT_1h.csv", stamps)
    windows = [{"label": "m", "test": {"start": "2019-03-01", "end": "2019-03-31"}},
               {"label": "a", "test": {"start": "2019-04-01", "end": "2019-04-30"}}]
    r = cgc.audit_cache_file(tmp_path / "AAAUSDT_1h.csv", "1h", ctx_for(policy), {"A": windows})
    df = pd.DataFrame({"timestamp": index_of(stamps)})
    for rec, w in zip(r["views"]["A"]["windows"], windows):
        s = pd.Timestamp(w["test"]["start"]).to_pydatetime()
        e = gate._measure_end(w["test"]["end"])
        frac = gate._missing_fraction(df, s, e, 3600)
        runs = gate._missing_runs(df, s, e, 3600)
        assert rec["missing_fraction"] == frac
        assert rec["classification"] == gate.classify_missing_fraction(frac)
        assert rec["missing_runs"] == len(runs)
        assert rec["largest_run_bars"] == cgc._num(max(x["bars"] for x in runs))
        assert rec["expected_bars"] == gate._expected_bar_count(s, e, 3600)


def test_fold_counts_gate_outcome_and_d042_reading(tmp_path, policy):
    # March: one hour missing -> 'refine' by fraction, but one short run -> the gate's outcome is validate.
    # April: every 7th hour missing -> decline.  May: no rows at all -> decline.
    mar = grid("2019-03-01", 31 * 24, "h", skip=["2019-03-10 05:00"])
    apr_all = grid("2019-04-01", 30 * 24, "h")
    apr = [t for i, t in enumerate(apr_all) if i % 7 != 3]
    write_cache(tmp_path / "AAAUSDT_1h.csv", mar + apr)
    doc = folds_doc(a=(("2019-03-01", "2019-03-31"), ("2019-04-01", "2019-04-30"), ("2019-05-01", "2019-05-31")))
    census = cgc.run_audit(tmp_path, ["1h"], policy_path=policy, folds_doc=doc)
    a = census["timeframes"]["1h"]["files"]["AAAUSDT"]["folds"]["A"]
    assert [w["classification"] for w in a["windows"]] == ["refine", "decline", "decline"]
    assert [w["gate_outcome"] for w in a["windows"]] == ["validate", "decline", "decline"]
    assert a["windows"][2]["no_rows_in_window"] is True and a["windows"][2]["missing_fraction"] == 1.0
    assert a["counts"] == {"validate": 0, "refine": 1, "decline": 2}
    assert a["counts_gate_outcome"] == {"validate": 1, "refine": 0, "decline": 2}
    d = a["d042_reading"]
    assert d["windows_validate"] == 1 and d["windows_total"] == 3
    assert d["meets_min_window_coverage"] is False  # 1/3 < 0.60
    # fold D has no windows in this doc: reported as an empty view, not an error
    assert census["timeframes"]["1h"]["files"]["AAAUSDT"]["folds"]["D"]["windows"] == []


def test_warmup_reading_boundary(tmp_path, policy):
    write_cache(tmp_path / "AAAUSDT_1d.csv", grid("2019-01-01", 120, "D"))
    win = [{"label": "w", "test": {"start": "2019-03-01", "end": "2019-03-31"}}]
    r59 = cgc.audit_cache_file(tmp_path / "AAAUSDT_1d.csv", "1d", ctx_for(policy, 59), {"A": win})
    r60 = cgc.audit_cache_file(tmp_path / "AAAUSDT_1d.csv", "1d", ctx_for(policy, 60), {"A": win})
    w59, w60 = r59["views"]["A"]["windows"][0], r60["views"]["A"]["windows"][0]
    assert w59["warmup_bars_available"] == 59 == w60["warmup_bars_available"]  # Jan 31 + Feb 28
    assert w59["warmup_ok"] is True and w60["warmup_ok"] is False
    assert w59["warmup_rows_present"] == 59
    assert r60["views"]["A"]["d042_reading"]["windows_validate_and_warm"] == 0
    # off by default: no warm-up keys
    r_off = cgc.audit_cache_file(tmp_path / "AAAUSDT_1d.csv", "1d", ctx_for(policy), {"A": win})
    assert "warmup_ok" not in r_off["views"]["A"]["windows"][0]


def test_a_fold_window_reaching_the_seal_is_refused_not_clipped(tmp_path, policy):
    write_cache(tmp_path / "AAAUSDT_1d.csv", grid("2021-01-01", 100, "D"))
    hs = sandbox_start(policy)
    last_clear = (hs - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    ok = folds_doc(a=(("2021-05-01", last_clear),))
    cgc.run_audit(tmp_path, ["1d"], policy_path=policy, folds_doc=ok)  # ends the day before: fine
    bad = folds_doc(a=(("2021-05-01", hs.strftime("%Y-%m-%d")),))
    with pytest.raises(cgc.AuditRefusal) as ei:
        cgc.run_audit(tmp_path, ["1d"], policy_path=policy, folds_doc=bad)
    assert "fold A window #1" in str(ei.value) and not DATE.search(str(ei.value))


# ---------------------------------------------------------------------------
# Output A
# ---------------------------------------------------------------------------

def test_write_census_header_refuses_overwrite_and_writes_where_pointed(tmp_path, policy):
    write_cache(tmp_path / "data" / "AAAUSDT_1d.csv", grid("2019-01-01", 60, "D"))
    now = pd.Timestamp("2020-02-03 04:05:06", tz="UTC").to_pydatetime()
    census = cgc.run_audit(tmp_path / "data", ["1d"], policy_path=policy, folds_doc=folds_doc(), now=now)
    out_dir = tmp_path / "tmp_campaign_record" / "data_census"
    path = cgc.write_census(census, out_dir)
    assert Path(path).name == "census_20200203T040506Z.yaml"
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    h = doc["header"]
    assert h["tool"] == "strategy-research/tools/cache_gap_census.py"
    assert re.fullmatch(r"[0-9a-f]{40}", h["tool_git_blob_sha"])
    assert h["timeframes"] == ["1d"] and h["utc_run_time"] == "2020-02-03T04:05:06Z"
    assert h["note"] == "read-only for the pipeline: no stage reads this file"
    assert set(h["folds_windows_sha256"]) == {"A", "B", "C", "D"}
    assert h["folds_windows_sha256"]["A"] == rf.fold_windows_sha256(folds_doc(), "A")
    assert doc["sealed"] == "not audited"
    before = Path(path).read_bytes()
    with pytest.raises(cgc.AuditRefusal):
        cgc.write_census(census, out_dir)
    assert Path(path).read_bytes() == before
    assert not (SR_ROOT / "campaign_record" / "data_census" / Path(path).name).exists()


def test_cli_audit_with_the_real_policy_and_folds_prints_summary_and_writes_into_census_dir(tmp_path, capsys):
    """The CLI path (real policy and real folds.yaml, read in code only): fixture rows are 2019-2020."""
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-01-01", 400, "D", skip=["2019-06-01"]))
    write_cache(data / "BBBUSDT_1d.csv", grid("2019-03-01", 300, "D"))
    out_dir = tmp_path / "cr" / "data_census"
    rc = cgc.main(["--audit", "--audit-timeframes", "1d", "--data-dir", str(data),
                   "--write-census", "--census-dir", str(out_dir)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "sealed: not audited" in out and "kraken_AAAUSD" in out and "BBBUSDT" in out
    written = list(out_dir.glob("census_*.yaml"))
    assert len(written) == 1
    doc = yaml.safe_load(written[0].read_text(encoding="utf-8"))
    assert list(doc["timeframes"]["1d"]["files"]) == ["BBBUSDT", "kraken_AAAUSD"]
    assert set(doc["timeframes"]["1d"]["files"]["BBBUSDT"]["folds"]) == {"A", "B", "C", "D"}
    # --write-census alone, and --run-dir with --audit, are refused
    with pytest.raises(SystemExit):
        cgc.main(["--write-census", "--census-dir", str(out_dir)])
    with pytest.raises(SystemExit):
        cgc.main(["--audit", "--run-dir", str(tmp_path)])


# ---------------------------------------------------------------------------
# Output B
# ---------------------------------------------------------------------------

def _run_dir(root: Path, name="run_x", gate_rec=None, protocol=None):
    run = root / name
    v = run / "artifacts" / "variants" / "base"
    v.mkdir(parents=True)
    rec = gate_rec if gate_rec is not None else {
        "schema_version": 1, "exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"],
        "windows": [
            {"label": "w1", "symbol": "AAAUSD", "start": "2019-03-01", "end": "2019-03-31", "outcome": "validate"},
            {"label": "w2", "symbol": "AAAUSD", "start": "2019-04-01", "end": "2019-04-30", "outcome": "validate"}]}
    (v / "data_availability_gate.yaml").write_text(yaml.safe_dump(rec), encoding="utf-8")
    if protocol is not None:
        import json
        (run / "artifacts" / "variants" / "run_protocol.json").write_text(json.dumps(protocol), encoding="utf-8")
    return run


def test_run_dir_writes_data_census_next_to_each_gate_record(tmp_path, policy):
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-02-01", 90, "D"))
    write_cache(data / "AAAUSD_1d.csv", grid("2019-02-01", 5, "D"))  # binance-style name must NOT be used
    run = _run_dir(tmp_path)
    (run / "artifacts" / "variants" / "second").mkdir()
    (run / "artifacts" / "variants" / "second" / "data_availability_gate.yaml").write_text(
        yaml.safe_dump({"exchange": "binance", "timeframe": "1d", "symbols": ["AAAUSD", "NOPEUSD"],
                        "windows": [{"label": "w1", "start": "2019-03-01", "end": "2019-03-31"}]}), encoding="utf-8")
    written = cgc.run_census_for_run(run, data, policy_path=policy,
                                     now=pd.Timestamp("2020-01-02", tz="UTC").to_pydatetime())
    assert sorted(Path(p).parent.name for p in written) == ["base", "second"]
    base = yaml.safe_load((run / "artifacts" / "variants" / "base" / "data_census.yaml").read_text(encoding="utf-8"))
    assert base["header"]["kind"] == "data_census_run" and base["header"]["exchange"] == "kraken"
    assert base["header"]["params_source"]["windows"] == "gate_record"
    assert base["sealed"] == "not audited" and base["header"]["note"].startswith("read-only for the pipeline")
    assert list(base["symbols"]) == ["AAAUSD"] and len(base["windows"]) == 2
    sym = base["symbols"]["AAAUSD"]
    assert sym["file"] == "kraken_AAAUSD_1d.csv" and sym["coverage"]["rows"] == 90
    assert [w["label"] for w in sym["window_view"]["windows"]] == ["w1", "w2"]
    second = yaml.safe_load((run / "artifacts" / "variants" / "second" / "data_census.yaml").read_text(encoding="utf-8"))
    assert second["symbols"]["AAAUSD"]["file"] == "AAAUSD_1d.csv"
    assert second["symbols"]["NOPEUSD"] == {"file": "NOPEUSD_1d.csv", "status": "cache_missing"}
    # refuses to overwrite, and writes nothing new on the refusal
    with pytest.raises(cgc.AuditRefusal):
        cgc.run_census_for_run(run, data, policy_path=policy)


def test_run_dir_falls_back_to_the_run_protocol_only_for_what_the_record_lacks(tmp_path, policy):
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-02-01", 90, "D"))
    rec = {"exchange": "kraken", "symbols": ["AAAUSD"]}  # no timeframe, no windows
    proto = {"exchange": "binance", "timeframe": "1d", "symbols": ["OTHER"],
             "windows": [{"label": "p1", "test": {"start": "2019-03-01", "end": "2019-03-31"}}]}
    run = _run_dir(tmp_path, gate_rec=rec, protocol=proto)
    cgc.run_census_for_run(run, data, policy_path=policy)
    doc = yaml.safe_load((run / "artifacts" / "variants" / "base" / "data_census.yaml").read_text(encoding="utf-8"))
    assert doc["header"]["exchange"] == "kraken" and doc["header"]["symbols"] == ["AAAUSD"]
    assert doc["header"]["params_source"] == {"exchange": "gate_record", "timeframe": "run_protocol",
                                              "symbols": "gate_record", "windows": "run_protocol"}
    assert doc["windows"][0]["label"] == "p1"
    # no protocol and a record that lacks the values -> refused
    run2 = _run_dir(tmp_path, name="run_y", gate_rec={"exchange": "kraken", "symbols": ["AAAUSD"]})
    with pytest.raises(cgc.AuditRefusal):
        cgc.run_census_for_run(run2, data, policy_path=policy)


def test_run_dir_refuses_local_data_and_sealed_paths_and_seal_reaching_windows(tmp_path, policy):
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-02-01", 90, "D"))
    bad_parent = tmp_path / "local_data"
    run = _run_dir(bad_parent)
    with pytest.raises(cgc.AuditRefusal):
        cgc.run_census_for_run(run, data, policy_path=policy)
    assert not (run / "artifacts" / "variants" / "base" / "data_census.yaml").exists()
    with pytest.raises(cgc.AuditRefusal):
        cgc.run_census_for_run(tmp_path / "holdout_sealed" / "run_z", data, policy_path=policy)
    hs = sandbox_start(policy)
    reaching = {"exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"],
                "windows": [{"label": "w", "start": "2021-05-01", "end": hs.strftime("%Y-%m-%d")}]}
    run3 = _run_dir(tmp_path, name="run_w", gate_rec=reaching)
    with pytest.raises(cgc.AuditRefusal) as ei:
        cgc.run_census_for_run(run3, data, policy_path=policy)
    assert not DATE.search(str(ei.value))
    assert not (run3 / "artifacts" / "variants" / "base" / "data_census.yaml").exists()


def test_cache_key_mirrors_ccxt_fetcher_cache_key():
    from data.fetchers.ccxt_fetcher import CcxtFetcher
    for ex, sym, tf in (("binance", "BTCUSDT", "1h"), ("kraken", "BTCUSD", "1d"), ("bybit", "ETHUSDT", "4h")):
        stub = types.SimpleNamespace(exchange_id=ex, ccxt_timeframe=tf)
        assert cgc.cache_key(ex, sym, tf) == CcxtFetcher.cache_key(stub, sym)
    for bad in ("../x", "a/b", "a\\b", ""):
        with pytest.raises(cgc.AuditRefusal):
            cgc.cache_key("binance", bad, "1h")


def test_cli_with_the_real_seal_never_surfaces_a_row_at_or_after_it(tmp_path, capsys):
    """Booleans only: the real bound is read at run time and never printed or asserted by value."""
    hs = pd.Timestamp(hp.holdout_start_of(hp.load_policy()))
    base = grid(hs - pd.Timedelta(days=40), 30, "D")                      # in sample
    planted = base + grid(hs, 20, "D") + grid(hs + pd.Timedelta(days=900), 5, "D")
    write_cache(tmp_path / "data" / "PPPUSDT_1d.csv", planted)
    # the guarded read must not refuse this frame: its kept rows are all in sample
    assert cgc.main(["--audit", "--audit-timeframes", "1d", "--data-dir", str(tmp_path / "data")]) == 0
    out = capsys.readouterr().out
    assert "sealed: not audited" in out and "PPPUSDT" in out
    stamps = [pd.Timestamp(m) for m in DATE.findall(out)]
    assert stamps and all(t < hs for t in stamps)


# ---------------------------------------------------------------------------
# review fixes: census-dir refusal, error hygiene, malformed gate records, row count
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", ["local_data", "holdout_sealed", "recorded_reserved"])
def test_census_dir_in_a_forbidden_place_is_refused_before_any_mkdir(tmp_path, policy, capsys, bad):
    data = tmp_path / "data"
    write_cache(data / "AAAUSDT_1d.csv", grid("2019-01-01", 60, "D"))
    census = cgc.run_audit(data, ["1d"], policy_path=policy, folds_doc=folds_doc())
    target = tmp_path / bad / "sub" / "data_census"
    with pytest.raises(cgc.AuditRefusal):
        cgc.write_census(census, target)
    assert not (tmp_path / bad).exists()
    # the CLI refuses before it audits or creates anything
    with pytest.raises(SystemExit) as ei:
        cgc.main(["--audit", "--audit-timeframes", "1d", "--data-dir", str(data),
                  "--write-census", "--census-dir", str(target)])
    assert str(ei.value).startswith("refused: ") and bad in str(ei.value)
    assert not (tmp_path / bad).exists()
    assert "data census" not in capsys.readouterr().out


@pytest.mark.parametrize("flags", [["--audit", "--audit-timeframes", "1d"], ["--run-dir"]])
def test_a_policy_error_is_refused_naming_only_the_exception_type(tmp_path, monkeypatch, flags):
    bad_policy = tmp_path / "bad_policy.yaml"
    bad_policy.write_text(yaml.safe_dump({"holdout_range": ["not-a-day", "not-a-day"]}), encoding="utf-8")
    monkeypatch.setattr(hp, "POLICY_PATH", bad_policy)
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-02-01", 90, "D"))
    argv = [*flags, "--data-dir", str(data)]
    if flags == ["--run-dir"]:
        argv = ["--run-dir", str(_run_dir(tmp_path)), "--data-dir", str(data)]
    with pytest.raises(SystemExit) as ei:
        cgc.main(argv)
    msg = str(ei.value)
    assert msg.startswith("refused: ") and "HoldoutPolicyError" in msg
    assert "not-a-day" not in msg and not DATE.search(msg)


def _refusal_for_gate_rec(tmp_path, policy, gate_rec, name="run_m"):
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-02-01", 90, "D"))
    run = _run_dir(tmp_path, name=name, gate_rec=gate_rec)
    with pytest.raises(cgc.AuditRefusal) as ei:
        cgc.run_census_for_run(run, data, policy_path=policy)
    assert not (run / "artifacts" / "variants" / "base" / "data_census.yaml").exists()
    return str(ei.value)


@pytest.mark.parametrize("gate_rec, needle", [
    (["not", "a", "mapping"], "not a mapping"),
    ({"exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"],
      "windows": [{"label": "w", "start": "2019-03-01"}]}, "missing key 'end'"),
    ({"exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"],
      "windows": [{"label": "w", "end": "2019-03-31"}]}, "missing key 'start'"),
    ({"exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"], "windows": ["w1"]}, "not a mapping"),
    ({"exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"], "windows": "w1"}, "'windows' is not a list"),
    ({"exchange": "kraken", "timeframe": "1d", "symbols": "AAAUSD",
      "windows": [{"start": "2019-03-01", "end": "2019-03-31"}]}, "'symbols'"),
    ({"exchange": ["kraken"], "timeframe": "1d", "symbols": ["AAAUSD"],
      "windows": [{"start": "2019-03-01", "end": "2019-03-31"}]}, "'exchange'"),
    ({"exchange": "kraken", "timeframe": "1d", "symbols": ["AAAUSD"],
      "windows": [{"start": "2019-03-01", "end": "not-a-day"}]}, "not a parseable date"),
])
def test_a_malformed_gate_record_is_refused_naming_the_variant_and_the_key(tmp_path, policy, gate_rec, needle):
    msg = _refusal_for_gate_rec(tmp_path, policy, gate_rec)
    assert "variant base" in msg and needle in msg
    assert "not-a-day" not in msg and not DATE.search(msg)


def test_check_windows_clear_refuses_malformed_windows_not_a_bare_keyerror(tmp_path, policy):
    ctx = ctx_for(policy)
    for windows, needle in (([{"label": "w"}], "no 'test' mapping"),
                            ([{"test": {"start": "2019-01-01"}}], "'test.end'"),
                            ([{"test": {"end": "2019-01-31"}}], "'test.start'"),
                            ([["not", "a", "dict"]], "no 'test' mapping")):
        with pytest.raises(cgc.AuditRefusal) as ei:
            cgc.check_windows_clear(windows, ctx, "variant v")
        assert "variant v window #1" in str(ei.value) and needle in str(ei.value)


def test_a_malformed_run_protocol_is_refused(tmp_path, policy):
    data = tmp_path / "data"
    write_cache(data / "kraken_AAAUSD_1d.csv", grid("2019-02-01", 90, "D"))
    rec = {"exchange": "kraken", "symbols": ["AAAUSD"]}  # lacks timeframe and windows -> reads the protocol
    for proto, name in (({"timeframe": "1d", "windows": "w1"}, "run_a"),
                        ({"timeframe": "1d", "windows": ["w1"]}, "run_b"),
                        (["not", "a", "mapping"], "run_c")):
        run = _run_dir(tmp_path, name=name, gate_rec=rec, protocol=proto)
        with pytest.raises(cgc.AuditRefusal):
            cgc.run_census_for_run(run, data, policy_path=policy)
        assert not (run / "artifacts" / "variants" / "base" / "data_census.yaml").exists()


def test_window_rows_in_measure_span_includes_the_gates_exclusive_end(tmp_path, policy):
    # March 1..31 in daily bars: 31 expected; the gate measures to Apr 1 00:00 and slices
    # inclusively, so the Apr 1 row is counted and rows exceed expected by one.
    write_cache(tmp_path / "AAAUSDT_1d.csv", grid("2019-02-01", 90, "D"))
    windows = [{"label": "m", "test": {"start": "2019-03-01", "end": "2019-03-31"}}]
    rec = cgc.audit_cache_file(tmp_path / "AAAUSDT_1d.csv", "1d", ctx_for(policy), {"A": windows})
    w = rec["views"]["A"]["windows"][0]
    assert w["expected_bars"] == 31 and w["rows_in_measure_span"] == 32
    assert "rows" not in w
