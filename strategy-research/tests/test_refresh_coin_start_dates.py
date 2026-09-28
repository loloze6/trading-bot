"""
Unit tests for tools/refresh_coin_start_dates.py (fix/layer1-per-coin-start-dates).

All filesystem interaction is against tmp_path fixtures -- never against the
real trading-bot/local_data/ or strategy-research/config/ files, so these
tests never touch real cache data or the real venue_data_capability.yaml.
"""
import csv
import datetime
import sys
from pathlib import Path

import pytest
import yaml

_TOOLS = str(Path(__file__).resolve().parent.parent / "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import refresh_coin_start_dates as rcs  # noqa: E402


# ---------------------------------------------------------------------------
# first_row_date -- header + first data row only
# ---------------------------------------------------------------------------

def _write_csv(path: Path, header: list, rows: list):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def test_first_row_date_reads_the_first_data_row(tmp_path):
    csv_path = tmp_path / "kraken_SOLUSD_1h.csv"
    _write_csv(csv_path, ["timestamp", "open", "high", "low", "close", "volume"],
               [["2021-06-17 00:00:00", 1, 1, 1, 1, 1],
                ["2021-06-17 01:00:00", 1, 1, 1, 1, 1]])
    assert rcs.first_row_date(str(csv_path)) == "2021-06-17"


def test_first_row_date_missing_file_returns_none(tmp_path):
    assert rcs.first_row_date(str(tmp_path / "does_not_exist.csv")) is None


def test_first_row_date_no_data_rows_returns_none(tmp_path):
    csv_path = tmp_path / "empty.csv"
    _write_csv(csv_path, ["timestamp", "open"], [])
    assert rcs.first_row_date(str(csv_path)) is None


def test_first_row_date_no_timestamp_column_returns_none(tmp_path):
    csv_path = tmp_path / "no_ts.csv"
    _write_csv(csv_path, ["date", "open"], [["2021-06-17", 1]])
    assert rcs.first_row_date(str(csv_path)) is None


def test_first_row_date_never_reads_past_the_first_data_row(tmp_path, monkeypatch):
    """Regression guard for the SAFETY requirement: construct a file where
    every row after the first is a value that would raise if ever parsed as
    a date, and confirm the function still returns cleanly using only the
    first row."""
    csv_path = tmp_path / "big.csv"
    rows = [["2021-06-17 00:00:00", 1]] + [["NOT-A-DATE-AND-SHOULD-NEVER-BE-READ", 1]] * 50_000
    _write_csv(csv_path, ["timestamp", "open"], rows)
    assert rcs.first_row_date(str(csv_path)) == "2021-06-17"


# ---------------------------------------------------------------------------
# kraken_symbol_from_cache_key
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cache_key,expected", [
    ("kraken_SOLUSD_1h", "SOLUSD"),
    ("kraken_SUIUSD_1h", "SUIUSD"),
    ("kraken_BTCUSD_1d", "BTCUSD"),
    ("BTCUSDT_1h", None),        # not kraken-prefixed
    ("kraken_1h", None),         # no symbol between prefix and timeframe
])
def test_kraken_symbol_from_cache_key(cache_key, expected):
    assert rcs.kraken_symbol_from_cache_key(cache_key) == expected


# ---------------------------------------------------------------------------
# iter_coin_universe_entries -- default/override resolution
# ---------------------------------------------------------------------------

def test_iter_coin_universe_entries_binance_default_cache_key_derived():
    coin_universe = {
        "default_exchange": "binance",
        "default_timeframe": "1h",
        "categories": {"cat": {"coins": [{"symbol": "DOTUSDT", "data_cached": False}]}},
    }
    entries = rcs.iter_coin_universe_entries(coin_universe)
    assert entries == [rcs.CoinEntry(symbol="DOTUSDT", exchange="binance", cache_key="DOTUSDT_1h")]


def test_iter_coin_universe_entries_kraken_explicit_cache_key_respected():
    coin_universe = {
        "default_exchange": "binance",
        "default_timeframe": "1h",
        "categories": {"cat": {"coins": [{
            "symbol": "SOLUSDT", "exchange": "kraken", "cache_key": "kraken_SOLUSD_1h",
        }]}},
    }
    entries = rcs.iter_coin_universe_entries(coin_universe)
    assert entries == [rcs.CoinEntry(symbol="SOLUSDT", exchange="kraken", cache_key="kraken_SOLUSD_1h")]


def test_iter_coin_universe_entries_kraken_without_explicit_cache_key_derives_prefixed():
    coin_universe = {
        "default_exchange": "binance",
        "default_timeframe": "1h",
        "categories": {"cat": {"coins": [{"symbol": "FOOUSDT", "exchange": "kraken"}]}},
    }
    entries = rcs.iter_coin_universe_entries(coin_universe)
    assert entries == [rcs.CoinEntry(symbol="FOOUSDT", exchange="kraken", cache_key="kraken_FOOUSDT_1h")]


# ---------------------------------------------------------------------------
# holdout_start / sealed-date refusal
# ---------------------------------------------------------------------------

def _write_policy(tmp_path: Path, holdout_range) -> Path:
    path = tmp_path / "campaign_data_policy.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"holdout_range": list(holdout_range)}, f)
    return path


def test_holdout_start_reads_from_policy(tmp_path):
    # A synthetic, deliberately non-real holdout window -- this pins that
    # holdout_start() reads whatever the policy file says rather than
    # hardcoding the real seal, so the fixture must not reuse the real dates.
    policy_path = _write_policy(tmp_path, ["2030-01-01", "2030-06-30"])
    assert rcs.holdout_start(str(policy_path)) == datetime.date(2030, 1, 1)


def _full_refresh_fixture(tmp_path):
    """Build a self-contained coin_universe.yaml + venue_data_capability.yaml
    + local_data dir + policy, all under tmp_path -- refresh() never touches
    the real repo files when every path is passed explicitly. Uses a
    synthetic, deliberately non-real holdout window (year 2030, not the real
    campaign seal) so this file never carries a literal sealed-range date --
    the refusal LOGIC is what's under test, not the real boundary."""
    local_data_dir = tmp_path / "local_data"
    local_data_dir.mkdir()

    coin_universe_path = tmp_path / "coin_universe.yaml"
    with open(coin_universe_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({
            "default_exchange": "binance",
            "default_timeframe": "1h",
            "categories": {
                "cat": {"coins": [
                    {"symbol": "SOLUSDT", "exchange": "kraken", "cache_key": "kraken_SOLUSD_1h"},
                    {"symbol": "DOTUSDT"},  # binance default, no local file -> no_local_file
                ]},
            },
        }, f)

    venue_capability_path = tmp_path / "venue_data_capability.yaml"
    venue_capability_path.write_text(
        "version: \"1.0\"\n"
        "venues:\n"
        "  kraken:\n"
        "    spot:\n"
        "      symbols:\n"
        "        confirmed_universe:\n"
        "          [SOLUSD]\n"
        "        pattern: >\n"
        "          19-pair breadth universe currently declared in\n"
        "          coin_universe.yaml.\n",
        encoding="utf-8",
    )

    policy_path = _write_policy(tmp_path, ["2030-01-01", "2030-06-30"])

    return coin_universe_path, venue_capability_path, policy_path, local_data_dir


def test_refresh_writes_kraken_date_and_reports_missing_file(tmp_path):
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    _write_csv(local_data_dir / "kraken_SOLUSD_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2021-06-17 00:00:00", 1, 1, 1, 1, 1]])

    result = rcs.refresh(
        coin_universe_path=str(coin_universe_path),
        venue_capability_path=str(venue_capability_path),
        policy_path=str(policy_path),
        local_data_dir=str(local_data_dir),
    )

    assert result.written == {"SOLUSD": "2021-06-17"}
    assert ("DOTUSDT", "binance", "DOTUSDT_1h") in result.no_local_file
    assert result.refused_sealed == []

    written_yaml = yaml.safe_load(venue_capability_path.read_text(encoding="utf-8"))
    assert written_yaml["venues"]["kraken"]["spot"]["symbols"]["earliest_ohlcv_utc"] == {
        "SOLUSD": "2021-06-17T00:00:00Z",
    }
    # The pre-existing content around the splice point must be untouched.
    assert written_yaml["venues"]["kraken"]["spot"]["symbols"]["confirmed_universe"] == ["SOLUSD"]
    assert "19-pair breadth universe" in written_yaml["venues"]["kraken"]["spot"]["symbols"]["pattern"]


def test_refresh_refuses_to_write_a_sealed_date(tmp_path):
    """Uses the fixture's synthetic 2030 holdout window (see
    _full_refresh_fixture), not the real seal -- the refusal MECHANISM is
    what's under test: it must key off whatever holdout_range the policy file
    says, not a value baked into this test."""
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    # First row falls ON the synthetic holdout start -- must be refused, not written.
    _write_csv(local_data_dir / "kraken_SOLUSD_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2030-01-01 00:00:00", 1, 1, 1, 1, 1]])

    before_text = venue_capability_path.read_text(encoding="utf-8")
    result = rcs.refresh(
        coin_universe_path=str(coin_universe_path),
        venue_capability_path=str(venue_capability_path),
        policy_path=str(policy_path),
        local_data_dir=str(local_data_dir),
    )

    assert result.written == {}
    assert result.refused_sealed == [("SOLUSDT", "kraken", "kraken_SOLUSD_1h", "2030-01-01")]
    # Nothing written at all -- file byte-identical to before the run.
    assert venue_capability_path.read_text(encoding="utf-8") == before_text


def test_refresh_a_date_one_day_before_the_seal_is_written_not_refused(tmp_path):
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    _write_csv(local_data_dir / "kraken_SOLUSD_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2029-12-31 23:00:00", 1, 1, 1, 1, 1]])

    result = rcs.refresh(
        coin_universe_path=str(coin_universe_path),
        venue_capability_path=str(venue_capability_path),
        policy_path=str(policy_path),
        local_data_dir=str(local_data_dir),
    )
    assert result.written == {"SOLUSD": "2029-12-31"}
    assert result.refused_sealed == []


def test_refresh_dry_run_does_not_write_the_file(tmp_path):
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    _write_csv(local_data_dir / "kraken_SOLUSD_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2021-06-17 00:00:00", 1, 1, 1, 1, 1]])
    before_text = venue_capability_path.read_text(encoding="utf-8")

    result = rcs.refresh(
        coin_universe_path=str(coin_universe_path),
        venue_capability_path=str(venue_capability_path),
        policy_path=str(policy_path),
        local_data_dir=str(local_data_dir),
        dry_run=True,
    )
    assert result.written == {"SOLUSD": "2021-06-17"}
    assert venue_capability_path.read_text(encoding="utf-8") == before_text


def test_refresh_is_idempotent_on_repeated_runs(tmp_path):
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    _write_csv(local_data_dir / "kraken_SOLUSD_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2021-06-17 00:00:00", 1, 1, 1, 1, 1]])

    for _ in range(2):
        rcs.refresh(
            coin_universe_path=str(coin_universe_path),
            venue_capability_path=str(venue_capability_path),
            policy_path=str(policy_path),
            local_data_dir=str(local_data_dir),
        )

    text = venue_capability_path.read_text(encoding="utf-8")
    assert text.count("BEGIN GENERATED") == 1
    assert text.count("END GENERATED") == 1
    written_yaml = yaml.safe_load(text)
    assert written_yaml["venues"]["kraken"]["spot"]["symbols"]["earliest_ohlcv_utc"] == {
        "SOLUSD": "2021-06-17T00:00:00Z",
    }


def test_refresh_binance_coin_with_local_file_is_reported_not_written(tmp_path):
    """A Binance coin the tool finds a local file for, but which has no
    existing earliest_ohlcv_utc entry, is reported -- never auto-written
    (venue_data_capability.yaml's 5 Binance dates are live-probed, a
    stronger source than a local cache's observed first row)."""
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    with open(coin_universe_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({
            "default_exchange": "binance", "default_timeframe": "1h",
            "categories": {"cat": {"coins": [{"symbol": "AVAXUSDT"}]}},
        }, f)
    _write_csv(local_data_dir / "AVAXUSDT_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2020-09-22 00:00:00", 1, 1, 1, 1, 1]])

    result = rcs.refresh(
        coin_universe_path=str(coin_universe_path),
        venue_capability_path=str(venue_capability_path),
        policy_path=str(policy_path),
        local_data_dir=str(local_data_dir),
    )
    assert result.written == {}
    assert result.binance_reported_not_written == [("AVAXUSDT", "AVAXUSDT_1h")]


def test_refresh_splice_raises_if_anchor_and_markers_both_missing(tmp_path):
    """Fail loud, not silent, if venue_data_capability.yaml's structure ever
    changes enough that neither the markers nor the anchor can be found."""
    coin_universe_path, venue_capability_path, policy_path, local_data_dir = _full_refresh_fixture(tmp_path)
    venue_capability_path.write_text("version: \"1.0\"\nvenues: {}\n", encoding="utf-8")
    _write_csv(local_data_dir / "kraken_SOLUSD_1h.csv",
               ["timestamp", "open", "high", "low", "close", "volume"],
               [["2021-06-17 00:00:00", 1, 1, 1, 1, 1]])

    with pytest.raises(ValueError, match="anchor"):
        rcs.refresh(
            coin_universe_path=str(coin_universe_path),
            venue_capability_path=str(venue_capability_path),
            policy_path=str(policy_path),
            local_data_dir=str(local_data_dir),
        )
