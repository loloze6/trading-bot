"""
WhaleFootprintFetcher: the deny-by-default gate, and the aggregation to bars.

TWO THINGS ARE UNDER TEST AND THEY ARE INDEPENDENT.

1. The GATE. The Kraken WS v2 forward capture is registered
   `configured_reserved_undesignated` (campaign_data_policy.yaml) — "no stage,
   tool, prescreen, diagnostic or backtest may read ANY window until an
   explicit, separately-committed designation releases a named window". These
   tests assert the fetcher refuses to CONSTRUCT against the real policy, and
   that every way of failing to prove a release also denies.

2. The AGGREGATION. Message-level trades -> the 1h bar grid the pipeline
   consumes, with unattested bars marked.

NO TEST HERE READS THE REAL CAPTURE. The gate tests point at the real policy but
never at the data; the aggregation tests build their own capture root under
tmp_path with a fixture policy that designates it. That is not merely hygiene —
a test suite that read reserved out-of-sample on every run would spend it.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REPO_ROOT = PROJECT_ROOT.parent
if str(REPO_ROOT / "strategy-research") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "strategy-research"))

from data.feed_registry import (  # noqa: E402
    FEED_REGISTRY,
    RESERVED_FEED_REGISTRY,
    WHALE_FOOTPRINT_FEEDS,
)
from data.fetchers.whale_footprint_fetcher import (  # noqa: E402
    POLICY_KEY,
    POLICY_PATH,
    ReservedDataError,
    WhaleFootprintFetcher,
    assert_designated,
)
from recorder.journal import CoverageJournal  # noqa: E402
from recorder.shard_writer import ShardWriter  # noqa: E402
from recorder.whale_features import FEATURE_COLUMNS  # noqa: E402

TODAY = datetime.now(timezone.utc)
#: What a real caller passes: a DATE, which parses to midnight and means
#: "through this day" (BaseFetcher's own trim convention, base_fetcher.py:220).
DAY = pd.Timestamp(TODAY.strftime("%Y-%m-%d"))


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------


def _policy(tmp_path, designations=None, key=POLICY_KEY, status="test_fixture"):
    """A minimal policy file. `designations=None` means: release nothing."""
    import yaml

    body = {key: {"status": status}}
    if designations is not None:
        body[key]["designations"] = designations
    path = tmp_path / "policy.yaml"
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    return path


def _capture(root, symbol="BTCUSD", n=60, qty=1.0, price=100.0, whale_qty=None):
    """
    A capture root whose journal attests exactly the span it wrote.

    Frames are written at the CURRENT wall clock (ShardWriter stamps `recv_ts`
    itself), so venue timestamps are set to match — the driver bins on venue
    time and the journal attests recorder time, and a fixture that let them
    drift would test neither.
    """
    root.mkdir(parents=True, exist_ok=True)
    j = CoverageJournal(root)
    j.record_start()
    j.write("WS_CONNECT", connection_id=1)
    j.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="trade")

    w = ShardWriter(root, run_id=j.run_id, compress=False, roll="day")
    now = datetime.now(timezone.utc)
    for i in range(n):
        q = qty if whale_qty is None or i != n - 1 else whale_qty
        raw = (
            '{"channel":"trade","type":"update","data":[{"symbol":"BTC/USD",'
            f'"side":"buy","price":{price},"qty":{q},"ord_type":"market",'
            f'"trade_id":{1000 + i},'
            f'"timestamp":"{now.strftime("%Y-%m-%dT%H:%M:%S.%f")}Z"}}]}}'
        )
        w.write_frame("trades", symbol, raw)
    w.close()
    j.write("RECORDER_STOP")
    j.close()
    return root


# ---------------------------------------------------------------------------
# 1. the gate
# ---------------------------------------------------------------------------


def test_the_real_policy_designates_nothing():
    """
    The standing state. If this test ever fails, a designation was committed —
    which is a ratified decision and fine — but it must be a deliberate one,
    so the change surfaces here rather than silently widening what a backtest
    can read.
    """
    import yaml

    entry = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))[POLICY_KEY]
    assert entry["status"] == "configured_reserved_undesignated"
    assert not entry.get("designations")


def test_fetcher_refuses_to_construct_against_the_real_policy():
    with pytest.raises(ReservedDataError, match="deny-by-default"):
        WhaleFootprintFetcher("2026-07-26", "2026-07-27", symbols=["BTCUSD"])


def test_denies_when_nothing_is_designated(tmp_path):
    with pytest.raises(ReservedDataError, match="no designation covers"):
        assert_designated(pd.Timestamp("2026-07-26"), pd.Timestamp("2026-07-27"),
                          _policy(tmp_path))


def test_denies_when_the_policy_file_is_missing(tmp_path):
    with pytest.raises(ReservedDataError, match="cannot prove"):
        assert_designated(pd.Timestamp("2026-07-26"), pd.Timestamp("2026-07-27"),
                          tmp_path / "absent.yaml")


def test_denies_when_the_policy_does_not_parse(tmp_path):
    bad = tmp_path / "policy.yaml"
    bad.write_text("{[not: yaml", encoding="utf-8")
    with pytest.raises(ReservedDataError, match="did not parse"):
        assert_designated(pd.Timestamp("2026-07-26"), pd.Timestamp("2026-07-27"), bad)


def test_denies_when_the_entry_is_absent(tmp_path):
    with pytest.raises(ReservedDataError, match="has no"):
        assert_designated(pd.Timestamp("2026-07-26"), pd.Timestamp("2026-07-27"),
                          _policy(tmp_path, key="something_else"))


def test_a_covering_designation_releases_the_window(tmp_path):
    policy = _policy(tmp_path, [
        {"start": "2026-07-01", "end": "2026-07-31", "ratified": "2026-07-27"},
    ])
    assert_designated(pd.Timestamp("2026-07-26"), pd.Timestamp("2026-07-27"), policy)


def test_a_partial_overlap_releases_nothing(tmp_path):
    """
    The un-designated remainder would be read alongside the released part, so a
    partial overlap is not a partial release.
    """
    policy = _policy(tmp_path, [
        {"start": "2026-07-01", "end": "2026-07-26", "ratified": "2026-07-27"},
    ])
    with pytest.raises(ReservedDataError):
        assert_designated(pd.Timestamp("2026-07-20"), pd.Timestamp("2026-07-31"), policy)


def test_a_malformed_designation_entry_is_ignored_not_honoured(tmp_path):
    policy = _policy(tmp_path, [{"ratified": "2026-07-27"}, "not-a-mapping"])
    with pytest.raises(ReservedDataError):
        assert_designated(pd.Timestamp("2026-07-26"), pd.Timestamp("2026-07-27"), policy)


# ---------------------------------------------------------------------------
# 2. registry wiring
# ---------------------------------------------------------------------------


def test_every_feature_column_has_its_own_registry_entry():
    """
    DataManager._premerge_aux_feeds attaches only the column whose name equals
    the registered feed name (data_manager.py:622), so a six-column feed that
    registered one name would deliver one column and silently drop five.
    """
    assert set(WHALE_FOOTPRINT_FEEDS) == set(FEATURE_COLUMNS)
    for name in WHALE_FOOTPRINT_FEEDS:
        assert name in RESERVED_FEED_REGISTRY


def test_reserved_feeds_are_not_in_the_default_registry():
    """
    THE LOAD-BEARING ONE. launcher.py:311 and launcher.py:596 pass the whole of
    FEED_REGISTRY as extra_feeds, so membership of that dict means "loaded by
    every backtest". A reserved feed appearing there would either break every
    run or quietly load reserved out-of-sample into all of them; membership IS
    the release decision.
    """
    assert not set(WHALE_FOOTPRINT_FEEDS) & set(FEED_REGISTRY)


def test_the_pre_existing_feeds_are_untouched():
    assert set(FEED_REGISTRY) == {"funding_rate", "fear_greed"}


def test_opting_in_by_name_still_hits_the_gate(tmp_path):
    """Naming a whale feed in extra_feeds must fail LOUDLY, not read reserved data."""
    factory = RESERVED_FEED_REGISTRY["whale_cvd_delta"]
    with pytest.raises(ReservedDataError):
        factory(["BTCUSD"], "2026-07-26", "2026-07-27", str(tmp_path))


# ---------------------------------------------------------------------------
# 3. aggregation to the bar
# ---------------------------------------------------------------------------


def _fetcher(tmp_path, **kw):
    policy = _policy(tmp_path, [
        {"start": "2000-01-01", "end": "2100-01-01", "ratified": "test"},
    ])
    return WhaleFootprintFetcher(
        TODAY.strftime("%Y-%m-%d"), TODAY.strftime("%Y-%m-%d"),
        symbols=["BTCUSD"], data_dir=str(tmp_path / "local_data"),
        capture_root=tmp_path / "capture", policy_path=policy, **kw,
    )


def test_cache_key_follows_the_exchange_qualified_convention(tmp_path):
    f = _fetcher(tmp_path)
    assert f.cache_key("BTCUSD") == "kraken_BTCUSD_whale_1h"
    assert _fetcher(tmp_path, bar_seconds=60).cache_key("ETHUSD") == \
        "kraken_ETHUSD_whale_1m"


def test_fetch_returns_the_documented_columns(tmp_path):
    _capture(tmp_path / "capture")
    df = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)._fetch_remote(
        "BTCUSD", DAY, DAY)
    assert list(df.columns) == ["timestamp", *FEATURE_COLUMNS]
    assert not df.empty
    assert df["timestamp"].dt.tz is None, "base_fetcher raises on tz-aware timestamps"


def test_fetch_counts_every_captured_trade(tmp_path):
    _capture(tmp_path / "capture", n=40)
    df = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)._fetch_remote(
        "BTCUSD", DAY, DAY)
    assert df["whale_trade_count"].sum() == 40.0


def test_fetch_marks_bars_the_journal_does_not_attest(tmp_path):
    """
    The capture covers seconds; the requested window is a whole day. Every bar
    outside the attested span must come back marked, not merely empty.
    """
    _capture(tmp_path / "capture", n=30)
    df = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)._fetch_remote(
        "BTCUSD", DAY, DAY)
    assert (df["whale_attested"] == 0.0).any(), "unattested bars must be marked"
    assert set(df["whale_attested"].unique()) <= {0.0, 1.0}
    # and a marked bar serves no value
    marked = df[df["whale_attested"] == 0.0]
    assert marked["whale_cvd_delta"].isna().all()
    assert marked["whale_lt_imbalance"].isna().all()


def test_fetch_emits_a_complete_bar_grid_with_no_timestamp_gaps(tmp_path):
    """
    Coverage is carried in a COLUMN, never by omitting a row — which is what
    makes BaseFetcher's grid arithmetic safe to point at this output.
    """
    _capture(tmp_path / "capture", n=30)
    df = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)._fetch_remote(
        "BTCUSD", DAY, DAY)
    deltas = df["timestamp"].diff().dropna().unique()
    assert list(deltas) == [pd.Timedelta(hours=1)]


def test_counts_survive_marking_but_values_do_not(tmp_path):
    """
    The fixture writes 300 trades inside a few seconds, so the journal attests
    seconds of an hour-long bar and that bar is correctly UNATTESTED. What the
    consumer gets is the honest combination: the trades are counted, so the
    absence of a value is distinguishable from a quiet bar, but no VALUE is
    served for a bar the journal cannot vouch for.

    The value arithmetic itself is pinned against hand-computed numbers in
    strategy-research/recorder/tests/test_whale_features.py; this test is about
    what survives the fetcher's marking.
    """
    _capture(tmp_path / "capture", n=300, qty=1.0, whale_qty=5000.0)
    df = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)._fetch_remote(
        "BTCUSD", DAY, DAY)
    active = df[df["whale_trade_count"] > 0]
    assert len(active) == 1
    assert active["whale_trade_count"].sum() == 300.0
    assert active["whale_attested"].iloc[0] == 0.0
    assert active["whale_cvd_delta"].isna().all()
    assert active["whale_lt_imbalance"].isna().all()
    assert active["whale_size_shift"].isna().all()


def test_missing_capture_root_returns_empty_without_raising(tmp_path):
    """`_fetch_remote`'s contract: empty on failure, do not raise. The refusal
    that must be loud already happened at construction."""
    f = _fetcher(tmp_path)
    assert f._fetch_remote("BTCUSD", TODAY, TODAY).empty


def test_symbol_with_no_shards_returns_empty_without_raising(tmp_path):
    _capture(tmp_path / "capture")
    assert _fetcher(tmp_path)._fetch_remote("DOGEUSD", TODAY, TODAY).empty


def test_get_data_round_trips_through_the_csv_cache(tmp_path):
    """
    The full BaseFetcher path — fetch, merge, store, reload — which is what the
    backtest actually exercises. `_load_local` raising on a tz-aware timestamp
    column is the assertion that matters here.
    """
    _capture(tmp_path / "capture", n=30)
    (tmp_path / "local_data").mkdir(parents=True, exist_ok=True)
    f = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)
    f.localStorage = True
    df = f.get_data("BTCUSD")
    assert not df.empty
    csv = tmp_path / "local_data" / "kraken_BTCUSD_whale_1h.csv"
    assert csv.exists()

    again = _fetcher(tmp_path, min_baseline_trades=1, min_bar_trades=1)
    again.localStorage = True
    assert list(again.get_data("BTCUSD").columns) == list(df.columns)
