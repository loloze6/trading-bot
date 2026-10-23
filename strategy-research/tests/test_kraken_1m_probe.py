"""
Tests for tools/kraken_1m_probe.py (one-coin, one-day Kraken 1m probe).

Synthetic data only: every fixture day is in 2019. Where a test needs the sealed
holdout start it derives it AT RUN TIME from the sandbox policy copy (conftest
seeds one per test) and asserts on counts / booleans only -- nothing here prints
or hard-codes a holdout bound. The suite's conftest blocks the network; the
trades path is driven through a fake exchange object.
"""
from __future__ import annotations

import gzip
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import ccxt
import numpy as np
import pandas as pd
import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import holdout_policy as hp  # noqa: E402
import kraken_1m_probe as kp  # noqa: E402

T0 = int(datetime(2019, 3, 15, tzinfo=timezone.utc).timestamp())
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


@pytest.fixture(autouse=True)
def _policy(_sandbox_by_default, monkeypatch):
    path = _sandbox_by_default / "config" / "campaign_data_policy.yaml"
    monkeypatch.setattr(kp, "POLICY_PATH_OVERRIDE", path)
    return path


def _holdout_start_date(policy_path) -> date:
    start, _ = hp.load_holdout_range(policy_path)
    return date.fromisoformat(start)


def _epoch(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())


def _frame(offsets_min, **over):
    n = len(offsets_min)
    df = pd.DataFrame({
        "timestamp": [T0 + 60 * m for m in offsets_min],
        "open": [100.0] * n, "high": [101.0] * n, "low": [99.0] * n, "close": [100.5] * n,
        "volume": [1.0] * n, "trade_count": [3] * n,
    })
    for k, v in over.items():
        df[k] = v
    return df


def _clean():
    return _frame([0, 1, 2, 3, 4])


# --------------------------------------------------------------------------- validation
def test_clean_frame_passes_and_all_counters_zero():
    rep = kp.validate_minute_frame(_clean())
    assert rep["passed"] is True
    assert all(rep[k] == 0 for k in kp._DEFECT_KEYS)
    assert rep["rows"] == 5 and rep["missing_minutes"] == 0
    assert rep["first_timestamp"] == "2019-03-15T00:00:00Z"
    assert rep["last_timestamp"] == "2019-03-15T00:04:00Z"
    assert rep["longest_gap_minutes"] == 0 and rep["longest_gap_starts_after"] is None


def _planted(kw):
    df = _clean()
    for (i, col), v in kw.items():
        df.loc[i, col] = v
    return kp.validate_minute_frame(df)


def test_off_grid_and_non_integer_timestamps():
    df = _clean()
    df["timestamp"] = df["timestamp"].astype("float64")
    df.loc[2, "timestamp"] = T0 + 120 + 7
    df.loc[3, "timestamp"] = T0 + 180 + 0.5
    rep = kp.validate_minute_frame(df)
    assert rep["off_grid_timestamps"] == 2
    assert rep["non_integer_timestamps"] == 1
    assert rep["passed"] is False


def test_non_increasing_and_duplicates():
    df = _frame([0, 1, 1, 3, 2])
    rep = kp.validate_minute_frame(df)
    assert rep["duplicate_timestamps"] == 1
    assert rep["non_increasing_steps"] == 2  # 1->1 and 3->2
    assert rep["passed"] is False


@pytest.mark.parametrize("col,val", [
    ("low", 100.2),    # low > min(open, close)
    ("high", 100.0),   # high < max(open, close)
])
def test_ohlc_violation_planted(col, val):
    rep = _planted({(1, col): val})
    assert rep["ohlc_violations"] == 1 and rep["passed"] is False


def test_ohlc_low_above_high_and_nonpositive_price():
    df = _clean()
    df.loc[0, ["open", "high", "low", "close"]] = [100.0, 98.0, 99.0, 100.0]
    df.loc[1, "open"] = 0.0
    df.loc[2, "close"] = -1.0
    rep = kp.validate_minute_frame(df)
    assert rep["ohlc_violations"] == 3


def test_negative_volume_and_bad_trade_count_and_nan():
    df = _clean()
    df["trade_count"] = df["trade_count"].astype("float64")
    df.loc[0, "volume"] = -0.1
    df.loc[1, "trade_count"] = 0
    df.loc[2, "trade_count"] = 2.5
    df.loc[3, "close"] = np.nan
    rep = kp.validate_minute_frame(df)
    assert rep["negative_volume"] == 1
    assert rep["bad_trade_count"] == 2
    assert rep["nan_rows"] == 1
    assert rep["passed"] is False


def test_gap_histogram_longest_gap_and_missing_not_a_failure():
    df = _frame([0, 1, 3, 7, 14, 100, 2000])
    rep = kp.validate_minute_frame(df)
    assert rep["gap_histogram"] == {"1": 1, "2-5": 1, "6-60": 1, "61-1440": 1, ">1440": 1}
    assert rep["missing_minutes"] == 1 + 3 + 6 + 85 + 1899
    assert rep["longest_gap_minutes"] == 1899
    assert rep["longest_gap_starts_after"] == kp._iso(T0 + 100 * 60)
    assert rep["passed"] is True  # missing minutes are reported, not a failure


def test_streaming_validator_matches_single_frame():
    df = _frame([0, 1, 3, 7, 14, 100, 2000])
    v = kp.MinuteValidator()
    v.update(df.iloc[:3])
    v.update(df.iloc[3:])
    assert v.report() == kp.validate_minute_frame(df)


# --------------------------------------------------------------------------- holdout guard
def test_sealed_row_count_counts_rows_at_or_after_start(_policy):
    start = _epoch(_holdout_start_date(_policy))
    ts = pd.Series([start - 120, start - 60, start - 1, start, start + 60, start + 86400])
    assert kp.sealed_row_count(ts, policy_path=_policy) == 3
    assert kp.sealed_row_count(ts) == 3  # override path
    assert kp.sealed_row_count(pd.Series([T0, T0 + 60]), policy_path=_policy) == 0


def test_day_guard_boundaries_and_message_has_no_date(_policy):
    s = _holdout_start_date(_policy)
    day_before = (s - timedelta(days=1)).isoformat()
    d0, d1 = kp.assert_day_before_holdout(day_before, _policy)  # whole day ends at the start
    assert d1 - d0 == 86400
    for bad in (s.isoformat(), (s + timedelta(days=3)).isoformat()):
        with pytest.raises(kp.ProbeRefusal) as ei:
            kp.assert_day_before_holdout(bad, _policy)
        leaked = bool(_DATE_RE.search(str(ei.value)))
        assert not leaked
    with pytest.raises(kp.ProbeRefusal):
        kp.assert_day_before_holdout("2019-3-15", _policy)  # not a strict day


def test_unreadable_policy_refuses_without_leaking(tmp_path):
    bad = tmp_path / "nope.yaml"
    with pytest.raises(kp.ProbeRefusal):
        kp.assert_day_before_holdout("2019-03-15", bad)


# --------------------------------------------------------------------------- candles
def _trade(price, vol, t, tid):
    return [str(price), str(vol), t, "b", "l", "", tid]


def test_candles_from_trades_hand_computed():
    trades = [
        _trade(100.0, 1.0, T0 + 5, 1),
        _trade(105.0, 0.5, T0 + 10, 2),
        _trade(95.0, 0.25, T0 + 30.5, 3),
        _trade(101.0, 2.0, T0 + 59.9, 4),
        # minute T0+60 has no trades -> no row
        _trade(50.0, 0.1, T0 + 120, 5),
        _trade(51.0, 0.2, T0 + 179.999, 6),
    ]
    df = kp.candles_from_trades(trades)
    assert list(df["timestamp"]) == [T0, T0 + 120]
    r0, r1 = df.iloc[0], df.iloc[1]
    assert (r0.open, r0.high, r0.low, r0.close) == (100.0, 105.0, 95.0, 101.0)
    assert r0.volume == pytest.approx(3.75) and r0.trade_count == 4
    assert (r1.open, r1.high, r1.low, r1.close) == (50.0, 51.0, 50.0, 51.0)
    assert r1.volume == pytest.approx(0.3) and r1.trade_count == 2


def test_candles_from_no_trades_is_empty_frame_with_columns():
    df = kp.candles_from_trades([])
    assert list(df.columns) == kp.COLUMNS and len(df) == 0


# --------------------------------------------------------------------------- compare
def test_compare_identical_frames():
    rep = kp.compare_minute_frames(_clean(), _clean())
    assert rep["minutes_in_both"] == 5
    assert rep["minutes_only_in_archive"] == 0 and rep["minutes_only_in_trades"] == 0
    assert all(v == 0 for v in rep["mismatches_by_field"].values())
    assert rep["example_mismatches"] == []


def test_compare_planted_mismatches_and_one_sided_minutes():
    a = _frame([0, 1, 2, 3, 4, 5])
    b = _frame([1, 2, 3, 4, 5, 6])
    b.loc[b.timestamp == T0 + 120, "close"] = 100.6        # close mismatch
    b.loc[b.timestamp == T0 + 180, "volume"] = 1.0 + 1e-6  # volume mismatch
    b.loc[b.timestamp == T0 + 240, "trade_count"] = 4      # count mismatch
    b.loc[b.timestamp == T0 + 300, "volume"] = 1.0 + 1e-12  # inside tolerance
    rep = kp.compare_minute_frames(a, b)
    assert rep["minutes_only_in_archive"] == 1 and rep["minutes_only_in_trades"] == 1
    assert rep["minutes_in_both"] == 5
    m = rep["mismatches_by_field"]
    assert m["close"] == 1 and m["volume"] == 1 and m["trade_count"] == 1
    assert m["open"] == 0 and m["high"] == 0 and m["low"] == 0
    assert rep["minutes_with_any_mismatch"] == 3
    assert len(rep["example_mismatches"]) == 3
    ex = {e["minute"]: e["fields"] for e in rep["example_mismatches"]}
    assert ex[kp._iso(T0 + 120)]["close"] == {"archive": 100.5, "trades": 100.6}


def test_compare_examples_capped_at_five():
    a = _frame(list(range(10)))
    b = _frame(list(range(10)), close=99.9)
    rep = kp.compare_minute_frames(a, b)
    assert rep["mismatches_by_field"]["close"] == 10
    assert len(rep["example_mismatches"]) == 5


# --------------------------------------------------------------------------- provenance
def test_provenance_sidecar_contents(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_bytes(b"hello")
    arch = tmp_path / "arch.csv"
    arch.write_bytes(b"1,2,3\n")
    doc = kp.write_provenance(tmp_path / "p.json", source="s", url_or_endpoint="u",
                              local_path=str(arch), fetched_or_read_utc="2019-01-01T00:00:00Z",
                              output_files=[f1], request_count=7, elapsed_seconds=1.5,
                              ccxt_version="x", rate_limit_ms=1000, archive_copy_path=arch)
    on_disk = json.loads((tmp_path / "p.json").read_text())
    assert on_disk == doc
    import hashlib
    assert on_disk["output_files"][0]["sha256"] == hashlib.sha256(b"hello").hexdigest()
    assert on_disk["output_files"][0]["bytes"] == 5
    assert on_disk["archive_copy"]["bytes"] == 6
    assert on_disk["archive_copy"]["sha256"] == hashlib.sha256(b"1,2,3\n").hexdigest()
    assert on_disk["archive_copy"]["mtime_utc"].endswith("Z")
    assert on_disk["tool_git_blob_sha"] and re.fullmatch(r"[0-9a-f]{40}", on_disk["tool_git_blob_sha"])
    assert on_disk["request_count"] == 7 and on_disk["rate_limit_ms"] == 1000


# --------------------------------------------------------------------------- trades path
class FakeKraken:
    rateLimit = 1000

    def __init__(self, pages, fail_first=True):
        self.pages = pages  # since -> (trades, last)
        self.calls = []
        self.fail_first = fail_first

    def publicGetTrades(self, params):
        self.calls.append(dict(params))
        if self.fail_first and len(self.calls) == 1:
            raise ccxt.RateLimitExceeded('kraken {"error":["EAPI:Rate limit exceeded"]}')
        trades, last = self.pages[params["since"]]
        return {"error": [], "result": {"XXBTZUSD": trades, "last": last}}


def _pages():
    since0 = str(T0 * 10**9)
    p1 = [_trade(100.0, 1.0, T0 + 5.25, 10), _trade(101.0, 1.0, T0 + 61.5, 11)]
    p2 = [_trade(101.0, 1.0, T0 + 61.5, 11),            # repeated id across pages
          _trade(102.0, 2.0, T0 + 86399.5, 12),
          _trade(999.0, 9.0, T0 + 86400 + 3, 13),       # outside the day
          _trade(998.0, 9.0, T0 + 86400 + 9, 14)]
    return {since0: (p1, "CURSOR1"), "CURSOR1": (p2, "CURSOR2")}


def test_fetch_pages_with_cursor_retry_on_429_and_filters_day():
    ex = FakeKraken(_pages())
    sleeps = []
    stats = kp.fetch_trades_for_day(ex, "XBTUSD", T0, T0 + 86400, sleep=sleeps.append,
                                    network_errors=(ccxt.NetworkError,))
    assert stats["requests"] == 3 and stats["retries"] == 1
    assert 2 in sleeps  # first backoff step
    assert len(stats["errors"]) == 1 and "EAPI" in stats["errors"][0]
    assert [t[6] for t in stats["trades"]] == [10, 11, 12]
    assert stats["duplicate_trade_ids"] == 1
    assert stats["reached_day_end"] is True and stats["hit_request_cap"] is False
    assert [c["since"] for c in ex.calls] == [str(T0 * 10**9), str(T0 * 10**9), "CURSOR1"]
    assert all(c["pair"] == "XBTUSD" and c["count"] == 1000 for c in ex.calls)


def test_fetch_hard_cap_on_requests():
    class Endless:
        n = 0

        def publicGetTrades(self, params):
            self.n += 1
            return {"result": {"X": [_trade(1.0, 1.0, T0 + self.n, self.n)], "last": f"C{self.n}"}}

    ex = Endless()
    stats = kp.fetch_trades_for_day(ex, "XBTUSD", T0, T0 + 86400, sleep=lambda s: None,
                                    max_requests=4, network_errors=(ccxt.NetworkError,))
    assert stats["requests"] == 4 and ex.n == 4
    assert stats["hit_request_cap"] is True and stats["reached_day_end"] is False


def test_fetch_gives_up_after_backoff_steps():
    class Down:
        n = 0

        def publicGetTrades(self, params):
            self.n += 1
            raise ccxt.NetworkError("down")

    ex = Down()
    sleeps = []
    with pytest.raises(ccxt.NetworkError):
        kp.fetch_trades_for_day(ex, "XBTUSD", T0, T0 + 86400, sleep=sleeps.append,
                                network_errors=(ccxt.NetworkError,))
    assert ex.n == 5  # first try + 4 retries
    assert [s for s in sleeps if s in (2, 4, 8, 16)] == [2, 4, 8, 16]


def test_cli_trades_end_to_end_with_fake_exchange(tmp_path, capsys):
    out = tmp_path / "trades_out"
    ex = FakeKraken(_pages())
    rc = kp.main(["trades", "--pair", "XBTUSD", "--day", "2019-03-15", "--out", str(out)],
                 exchange_factory=lambda: ex, sleep=lambda s: None)
    assert rc == 0
    names = sorted(p.name for p in out.iterdir())
    assert names == ["XBTUSD_1m_2019-03-15_trades.csv.gz",
                     "XBTUSD_1m_2019-03-15_trades_validation.yaml",
                     "XBTUSD_trades_2019-03-15.jsonl.gz",
                     "provenance_trades.json", "trades_progress.log"]
    assert all((out / n).stat().st_size > 0 for n in names)
    raw = [json.loads(line) for line in
           gzip.open(out / "XBTUSD_trades_2019-03-15.jsonl.gz", "rt").read().splitlines()]
    assert [r[6] for r in raw] == [10, 11, 12]
    bars = kp.read_minute_csv_gz(out / "XBTUSD_1m_2019-03-15_trades.csv.gz")
    assert list(bars["timestamp"]) == [T0, T0 + 60, T0 + 86340]
    prov = json.loads((out / "provenance_trades.json").read_text())
    assert prov["request_count"] == 3
    assert len(prov["extra"]["errors_429_or_eapi"]) == 1
    rep = yaml.safe_load((out / "XBTUSD_1m_2019-03-15_trades_validation.yaml").read_text())
    assert rep["trades_in_day"] == 3 and rep["fetch_complete"] is True


# --------------------------------------------------------------------------- archive + compare CLI
def _write_source(path: Path, rows):
    path.write_text("".join(",".join(str(x) for x in r) + "\n" for r in rows))


def _src_rows():
    rows = []
    for m in (0, 1, 2, 5, 6):  # minutes 3-4 missing
        rows.append((T0 + 60 * m, 100.0, 101.0, 99.0, 100.5, 1.5, 4))
    day_before = T0 - 86400
    rows.insert(0, (day_before, 90.0, 91.0, 89.0, 90.5, 1.0, 2))
    rows.append((T0 + 86400 + 120, 95.0, 96.0, 94.0, 95.5, 1.0, 2))
    return sorted(rows)


def test_cli_archive_writes_day_only_and_reports(tmp_path):
    src = tmp_path / "XBTUSD_1.csv"
    _write_source(src, _src_rows())
    out = tmp_path / "arch_out"
    rc = kp.main(["archive", "--pair", "XBTUSD", "--day", "2019-03-15", "--source", str(src),
                  "--out", str(out)])
    assert rc == 0
    day = kp.read_minute_csv_gz(out / "XBTUSD_1m_2019-03-15_archive.csv.gz")
    assert list(day["timestamp"]) == [T0 + 60 * m for m in (0, 1, 2, 5, 6)]
    header = gzip.open(out / "XBTUSD_1m_2019-03-15_archive.csv.gz", "rt").readline().strip()
    assert header == "timestamp,open,high,low,close,volume,trade_count"
    d = yaml.safe_load((out / "XBTUSD_1m_2019-03-15_archive_day_validation.yaml").read_text())
    assert d["rows"] == 5 and d["missing_minutes"] == 2 and d["day_missing_minutes"] == 1435
    w = yaml.safe_load((out / "XBTUSD_1m_whole_file_validation.yaml").read_text())
    assert w["rows"] == 7 and w["sealed_rows"] == 0
    prov = json.loads((out / "provenance_archive.json").read_text())
    assert prov["archive_copy"]["bytes"] == src.stat().st_size
    assert all(f["bytes"] > 0 for f in prov["output_files"])


def test_cli_archive_stops_and_writes_nothing_when_sealed_rows_present(tmp_path, _policy, capsys):
    start = _epoch(_holdout_start_date(_policy))
    rows = _src_rows() + [(start + 60, 1.0, 2.0, 0.5, 1.5, 1.0, 1), (start + 120, 1.0, 2.0, 0.5, 1.5, 1.0, 1)]
    src = tmp_path / "XBTUSD_1.csv"
    _write_source(src, rows)
    out = tmp_path / "arch_out"
    rc = kp.main(["archive", "--pair", "XBTUSD", "--day", "2019-03-15", "--source", str(src),
                  "--out", str(out)])
    assert rc == 3
    text = capsys.readouterr().out
    assert "sealed_rows=2" in text
    leaked = bool(_DATE_RE.search(text))
    assert not leaked
    assert list(out.iterdir()) == []


def test_cli_compare_end_to_end(tmp_path):
    src = tmp_path / "XBTUSD_1.csv"
    _write_source(src, _src_rows())
    kp.main(["archive", "--pair", "XBTUSD", "--day", "2019-03-15", "--source", str(src),
             "--out", str(tmp_path / "a")])
    trades = [_trade(100.0, 1.0, T0 + 1, 1), _trade(101.0, 0.5, T0 + 2, 2),
              _trade(99.0, 0.5, T0 + 3, 3), _trade(100.5, 0.5, T0 + 4, 4),   # minute 0: 4 trades
              _trade(10.0, 1.0, T0 + 3 * 60, 5)]                           # minute 3: extra
    bars = kp.candles_from_trades(trades)
    (tmp_path / "t").mkdir()
    kp.write_minute_csv_gz(bars, tmp_path / "t" / "XBTUSD_1m_2019-03-15_trades.csv.gz")
    rc = kp.main(["compare", "--pair", "XBTUSD", "--day", "2019-03-15",
                  "--archive-dir", str(tmp_path / "a"), "--trades-dir", str(tmp_path / "t"),
                  "--out", str(tmp_path / "c")])
    assert rc == 0
    rep = yaml.safe_load((tmp_path / "c" / "compare_report.yaml").read_text())
    assert rep["minutes_in_both"] == 1
    assert rep["minutes_only_in_archive"] == 4 and rep["minutes_only_in_trades"] == 1
    assert rep["mismatches_by_field"]["volume"] == 1  # 2.5 vs 1.5 ... planted by construction
    assert rep["mismatches_by_field"]["open"] == 0


# --------------------------------------------------------------------------- CLI refusals
def _day_args(out):
    return ["trades", "--pair", "XBTUSD", "--day", "2019-03-15", "--out", str(out)]


def test_cli_refuses_out_inside_git_repo(tmp_path, capsys):
    (tmp_path / "repo" / ".git").mkdir(parents=True)
    out = tmp_path / "repo" / "sub" / "o"
    ex = FakeKraken(_pages())
    assert kp.main(_day_args(out), exchange_factory=lambda: ex, sleep=lambda s: None) == 2
    assert ex.calls == [] and not out.exists()


def test_cli_refuses_out_inside_local_data(tmp_path):
    out = tmp_path / "local_data" / "o"
    ex = FakeKraken(_pages())
    assert kp.main(_day_args(out), exchange_factory=lambda: ex, sleep=lambda s: None) == 2
    assert ex.calls == [] and not out.exists()


def test_cli_refuses_non_empty_out(tmp_path):
    out = tmp_path / "o"
    out.mkdir()
    (out / "x.txt").write_text("x")
    ex = FakeKraken(_pages())
    assert kp.main(_day_args(out), exchange_factory=lambda: ex, sleep=lambda s: None) == 2
    assert ex.calls == []
    assert [p.name for p in out.iterdir()] == ["x.txt"]


def test_cli_refuses_day_at_or_after_holdout_start_with_no_date_in_message(tmp_path, capsys, _policy):
    s = _holdout_start_date(_policy)
    ex = FakeKraken(_pages())
    for d in (s, s + timedelta(days=10)):
        out = tmp_path / f"o{(d - s).days}"
        rc = kp.main(["trades", "--pair", "XBTUSD", "--day", d.isoformat(), "--out", str(out)],
                     exchange_factory=lambda: ex, sleep=lambda s_: None)
        cap = capsys.readouterr()
        assert rc == 2
        leaked = bool(_DATE_RE.search(cap.out + cap.err))
        assert not leaked
        assert "REFUSED" in cap.err
        assert ex.calls == [] and not out.exists()
    # archive: refuses before opening the source
    rc = kp.main(["archive", "--pair", "XBTUSD", "--day", s.isoformat(),
                  "--source", str(tmp_path / "does_not_exist.csv"), "--out", str(tmp_path / "oa")])
    assert rc == 2


# --------------------------------------------------------------------------- sizes
def test_sizes_counts_bytes_lines_and_gzip_ratio(tmp_path):
    src = tmp_path / "q4"
    src.mkdir()
    (src / "XBTUSD_1.csv").write_bytes(b"1,2,3\n4,5,6\n7,8,9")  # unterminated last line
    (src / "UNIUSD_1.csv").write_bytes(b"a\nb\n")
    (src / "UNITEUSD_1.csv").write_bytes(b"decoy\n" * 100)      # must not be picked up
    out = tmp_path / "sizes_out"
    rc = kp.main(["sizes", "--source-dir", str(src), "--out", str(out)])
    assert rc == 0
    rep = yaml.safe_load((out / "archive_1m_sizes.yaml").read_text())
    assert rep["files"]["XBTUSD"] == {"bytes": 17, "lines": 3}
    assert rep["files"]["UNIUSD"] == {"bytes": 4, "lines": 2}
    assert rep["files"]["ADAUSD"] == {"missing": True}
    assert rep["totals"] == {"files_found": 2, "bytes": 21, "lines": 5}
    g = rep["gzip_xbtusd_1"]
    assert g["raw_bytes"] == 17 and g["gzip_bytes"] > 0
    assert sorted(p.name for p in out.iterdir()) == ["archive_1m_sizes.yaml", "provenance_sizes.json"]
    assert len(kp.SIZE_PAIRS) == 19
