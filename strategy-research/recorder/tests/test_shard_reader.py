"""
Shard reader: gap exposure, truncation tolerance, deny-by-default.

Two fixture families. Synthetic shards written by `ShardWriter` itself (so the
reader is tested against the real writer, not against a hand-rolled idea of its
output), and — where it exists — the real baseline capture, which is the only
place a genuinely truncated shard and a real multi-run coverage gap can be
found. The real-data tests SKIP when the capture is absent so the suite runs on
a clean clone.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from recorder.journal import CoverageJournal, assert_covered, CoverageGapError
from recorder.shard_reader import (
    Gap,
    ShardReadError,
    ShardReader,
    Trade,
    as_naive_utc,
    disk_symbol,
    ws_symbol,
)
from recorder.shard_writer import ShardWriter

BASELINE_CAPTURE = (
    Path(__file__).resolve().parents[3]
    / "trading-bot" / "local_data" / "recorded_reserved" / "kraken_ws_v2"
)

T0 = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)


def _trade_frame(symbol="BTC/USD", trade_id=1, side="buy", price=64000.0,
                 qty=0.5, ts=None, msg_type="update"):
    ts = ts or T0
    return json.dumps({
        "channel": "trade",
        "type": msg_type,
        "data": [{
            "symbol": symbol,
            "side": side,
            "price": price,
            "qty": qty,
            "ord_type": "market",
            "trade_id": trade_id,
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
        }],
    }, separators=(",", ":"))


def _capture(tmp_path, frames, *, subscribe=("BTC/USD",), channels=("trade",),
             stop=True, roll="day"):
    """
    Build a small capture root: shards plus a coverage journal that attests
    them. `frames` is a list of (stream, disk_symbol, raw_text).
    """
    j = CoverageJournal(tmp_path)
    j.record_start()
    j.write("WS_CONNECT", connection_id=1)
    for sym in subscribe:
        for chan in channels:
            j.write("SUBSCRIBE_ACK", symbol=sym, channel=chan)

    w = ShardWriter(tmp_path, run_id=j.run_id, compress=False, roll=roll)
    for stream, sym, raw in frames:
        w.write_frame(stream, sym, raw)
    w.close()

    if stop:
        j.write("RECORDER_STOP")
    j.close()
    return tmp_path


# ---------------------------------------------------------------------------
# symbol spelling
# ---------------------------------------------------------------------------


def test_symbol_spellings_round_trip():
    assert disk_symbol("BTC/USD") == "BTCUSD"
    assert ws_symbol("BTCUSD") == "BTC/USD"
    assert ws_symbol(disk_symbol("ONDO/USD")) == "ONDO/USD"


def test_as_naive_utc_matches_the_cache_convention():
    # base_fetcher._load_local RAISES on a tz-aware timestamp column.
    out = as_naive_utc(datetime(2026, 7, 26, 12, 0, tzinfo=timezone.utc))
    assert out.tzinfo is None and out.hour == 12


# ---------------------------------------------------------------------------
# a journal is mandatory
# ---------------------------------------------------------------------------


def test_root_without_a_journal_is_refused(tmp_path):
    (tmp_path / "trades" / "BTCUSD").mkdir(parents=True)
    with pytest.raises(ShardReadError, match="no coverage journal"):
        ShardReader(tmp_path)


def test_missing_root_is_refused(tmp_path):
    with pytest.raises(ShardReadError, match="does not exist"):
        ShardReader(tmp_path / "nope")


# ---------------------------------------------------------------------------
# reading
# ---------------------------------------------------------------------------


def test_reads_trades_and_preserves_the_payload(tmp_path):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame(trade_id=7))])
    trades = [x for x in ShardReader(root).iter_trades() if isinstance(x, Trade)]
    assert len(trades) == 1
    t = trades[0]
    assert (t.trade_id, t.side, t.price, t.qty) == (7, "buy", 64000.0, 0.5)
    assert t.notional == pytest.approx(32000.0)
    assert t.signed_notional == pytest.approx(32000.0)
    assert t.symbol == "BTCUSD"


def test_sell_side_signs_negative(tmp_path):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame(side="sell"))])
    t = [x for x in ShardReader(root).iter_trades() if isinstance(x, Trade)][0]
    assert t.sign == -1 and t.signed_notional < 0


def test_records_are_ordered_across_pairs(tmp_path):
    frames = []
    for i in range(6):
        sym = "BTC/USD" if i % 2 == 0 else "ETH/USD"
        frames.append(("trades", disk_symbol(sym), _trade_frame(symbol=sym, trade_id=i)))
    root = _capture(tmp_path, frames, subscribe=("BTC/USD", "ETH/USD"))
    got = [x for x in ShardReader(root).iter_trades() if isinstance(x, Trade)]
    assert len(got) == 6
    recv = [t.recv_ts for t in got]
    assert recv == sorted(recv)


def test_duplicate_trade_ids_are_deduplicated(tmp_path):
    # A resubscribe re-delivers a snapshot whose trades overlap what was already
    # captured. Counting them twice would inflate every volume figure.
    root = _capture(tmp_path, [
        ("trades", "BTCUSD", _trade_frame(trade_id=42)),
        ("trades", "BTCUSD", _trade_frame(trade_id=42, msg_type="snapshot")),
        ("trades", "BTCUSD", _trade_frame(trade_id=43)),
    ])
    trades = [x for x in ShardReader(root).iter_trades() if isinstance(x, Trade)]
    assert sorted(t.trade_id for t in trades) == [42, 43]


def test_snapshot_provenance_is_carried_not_dropped(tmp_path):
    root = _capture(tmp_path, [
        ("trades", "BTCUSD", _trade_frame(trade_id=1, msg_type="snapshot")),
        ("trades", "BTCUSD", _trade_frame(trade_id=2)),
    ])
    trades = {t.trade_id: t for t in ShardReader(root).iter_trades()
              if isinstance(t, Trade)}
    assert trades[1].from_snapshot is True
    assert trades[2].from_snapshot is False


# ---------------------------------------------------------------------------
# gaps are exposed, not interpolated
# ---------------------------------------------------------------------------


def test_gap_is_yielded_inline_when_coverage_does_not_reach_the_window(tmp_path):
    """
    Two runs with a hole between them: the journal attests run 1 and run 2 but
    nothing in between, and the reader must SAY so in the stream rather than
    hand back a contiguous-looking list of trades.
    """
    j = CoverageJournal(tmp_path)
    j.record_start()
    j.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="trade")
    w = ShardWriter(tmp_path, run_id=j.run_id, compress=False, roll="day")
    w.write_frame("trades", "BTCUSD", _trade_frame(trade_id=1))
    w.close()
    j.write("RECORDER_STOP")
    j.close()

    first_end = datetime.now(timezone.utc)

    # a second run, after a hole
    j2 = CoverageJournal(tmp_path)
    j2.record_start()
    j2.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="trade")
    w2 = ShardWriter(tmp_path, run_id=j2.run_id, compress=False, roll="day")
    w2.write_frame("trades", "BTCUSD", _trade_frame(trade_id=2))
    w2.close()
    j2.write("RECORDER_STOP")
    j2.close()

    reader = ShardReader(tmp_path)
    items = list(reader.iter_trades())
    gaps = [x for x in items if isinstance(x, Gap)]
    trades = [x for x in items if isinstance(x, Trade)]

    assert len(trades) == 2
    assert len(gaps) >= 1, "the hole between the two runs must be exposed"
    assert all(g.symbol == "BTCUSD" and g.channel == "trade" for g in gaps)
    assert any(g.start >= first_end - timedelta(seconds=5) for g in gaps)

    # The stream is ordered, and the hole sits BETWEEN the two trades. Note the
    # reader also exposes a leading gap: coverage opens at SUBSCRIBE_ACK, a few
    # hundred microseconds after RECORDER_START, and the window starts at the
    # earlier of the two. That sliver is genuinely unattested and reporting it
    # is correct, so the assertion is positional rather than a gap count.
    order = [type(x).__name__ for x in items]
    first_trade = order.index("Trade")
    last_trade = len(order) - 1 - order[::-1].index("Trade")
    assert "Gap" in order[first_trade:last_trade], (
        f"the between-runs hole must land between the two trades, got {order}"
    )


def test_emit_gaps_false_suppresses_the_markers_but_not_the_gap(tmp_path):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame())])
    reader = ShardReader(root)
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    end = datetime(2026, 7, 2, tzinfo=timezone.utc)

    assert len(reader.gaps("BTCUSD", "trade", start, end)) == 1
    silent = list(reader.iter_trades(start=start, end=end, emit_gaps=False))
    assert not any(isinstance(x, Gap) for x in silent)
    # the journal still refuses the window when asked directly
    with pytest.raises(CoverageGapError):
        assert_covered(reader.journal_path, "BTC/USD", "trade", start, end)


def test_gap_causes_are_distinguished(tmp_path):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame())])
    reader = ShardReader(root)
    ivs = reader.coverage()[("BTC/USD", "trade")]
    before = reader.gaps("BTCUSD", "trade",
                         ivs[0].start - timedelta(hours=2), ivs[0].start)
    after = reader.gaps("BTCUSD", "trade",
                        ivs[0].end, ivs[0].end + timedelta(hours=2))
    assert before and before[0].cause == "not_yet_started"
    assert after and after[0].cause == "after_last_attested"
    assert after[0].duration_s == pytest.approx(7200, abs=1)


def test_fully_covered_window_yields_no_gap(tmp_path):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame())])
    reader = ShardReader(root)
    iv = reader.coverage()[("BTC/USD", "trade")][0]
    assert reader.gaps("BTCUSD", "trade", iv.start, iv.end) == []


# ---------------------------------------------------------------------------
# truncation
# ---------------------------------------------------------------------------


def test_truncated_final_line_is_tolerated_and_recorded(tmp_path):
    root = _capture(tmp_path, [
        ("trades", "BTCUSD", _trade_frame(trade_id=1)),
        ("trades", "BTCUSD", _trade_frame(trade_id=2)),
    ])
    path = ShardReader(root).shard_paths("trades", "BTCUSD")[0]
    with open(path, "a", encoding="utf-8") as fh:
        fh.write('{"recv_ts":"2026-07-26T12:00:02.0Z","mono":1.0,"run_i')

    reader = ShardReader(root)
    trades = [x for x in reader.iter_trades() if isinstance(x, Trade)]
    assert [t.trade_id for t in trades] == [1, 2]
    assert reader.truncations == {path: 3}


def test_unparseable_line_in_the_middle_raises(tmp_path):
    root = _capture(tmp_path, [
        ("trades", "BTCUSD", _trade_frame(trade_id=1)),
        ("trades", "BTCUSD", _trade_frame(trade_id=2)),
    ])
    path = ShardReader(root).shard_paths("trades", "BTCUSD")[0]
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join([lines[0], '{"recv_ts":"2026-07', lines[1]]) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ShardReadError, match="corruption in the middle"):
        list(ShardReader(root).iter_trades())


# ---------------------------------------------------------------------------
# deny by default
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mutate,match", [
    (lambda r: r.pop("seq"), "missing"),
    (lambda r: r.update(surprise=1), "unrecognised envelope field"),
    (lambda r: r.update(raw={"channel": "ticker", "type": "update", "data": []}),
     "channel 'ticker'"),
    (lambda r: r.update(raw={"channel": "trade", "type": "delta", "data": []}),
     "message type 'delta'"),
    (lambda r: r.update(raw={"channel": "trade", "type": "update", "data": {}}),
     "raw.data is dict"),
])
def test_unrecognised_record_shapes_raise_rather_than_skip(tmp_path, mutate, match):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame())])
    path = ShardReader(root).shard_paths("trades", "BTCUSD")[0]
    rec = json.loads(path.read_text(encoding="utf-8").strip())
    mutate(rec)
    path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    with pytest.raises(ShardReadError, match=match):
        list(ShardReader(root).iter_trades())


@pytest.mark.parametrize("entry,match", [
    ({"symbol": "BTC/USD", "side": "buy", "price": 1.0, "qty": 1.0,
      "ord_type": "market", "trade_id": 1}, "missing"),
    ({"symbol": "BTC/USD", "side": "maker", "price": 1.0, "qty": 1.0,
      "ord_type": "market", "trade_id": 1, "timestamp": "2026-07-26T12:00:00.0Z"},
     "side 'maker'"),
    ({"symbol": "BTC/USD", "side": "buy", "price": 0.0, "qty": 1.0,
      "ord_type": "market", "trade_id": 1, "timestamp": "2026-07-26T12:00:00.0Z"},
     "non-positive price"),
    ({"symbol": "ETH/USD", "side": "buy", "price": 1.0, "qty": 1.0,
      "ord_type": "market", "trade_id": 1, "timestamp": "2026-07-26T12:00:00.0Z"},
     "does not match the shard"),
])
def test_bad_trade_payloads_raise(tmp_path, entry, match):
    raw = json.dumps({"channel": "trade", "type": "update", "data": [entry]})
    root = _capture(tmp_path, [("trades", "BTCUSD", raw)])
    with pytest.raises(ShardReadError, match=match):
        list(ShardReader(root).iter_trades())


def test_unknown_stream_raises(tmp_path):
    root = _capture(tmp_path, [("trades", "BTCUSD", _trade_frame())])
    with pytest.raises(ShardReadError, match="unknown stream"):
        list(ShardReader(root).read("orderflow"))


def test_snapshot_cadence_extra_field_is_accepted(tmp_path):
    """`synth` is a field the writer legitimately emits (record_kraken_ws.py:365).
    Deny-by-default must not reject the recorder's own output."""
    j = CoverageJournal(tmp_path)
    j.record_start()
    j.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="book")
    w = ShardWriter(tmp_path, run_id=j.run_id, compress=False, roll="day")
    w.write_frame(
        "book_d10", "BTCUSD",
        '{"channel":"book","type":"snapshot","data":[{"symbol":"BTC/USD",'
        '"bids":[],"asks":[],"checksum":1,"timestamp":"2026-07-26T12:00:00.0Z"}]}',
        extra={"synth": "book_snapshot"},
    )
    w.close()
    j.write("RECORDER_STOP")
    j.close()

    envs = [x for x in ShardReader(tmp_path).read("book_d10") if not isinstance(x, Gap)]
    assert len(envs) == 1 and envs[0].synth == "book_snapshot"


# ---------------------------------------------------------------------------
# compaction
# ---------------------------------------------------------------------------


def test_compacted_shard_reads_identically(tmp_path):
    from recorder.compaction import compress_shard

    root = _capture(tmp_path, [
        ("trades", "BTCUSD", _trade_frame(trade_id=i)) for i in range(1, 4)
    ])
    path = ShardReader(root).shard_paths("trades", "BTCUSD")[0]
    plain = [t.trade_id for t in ShardReader(root).iter_trades() if isinstance(t, Trade)]

    compress_shard(path)
    reader = ShardReader(root)
    assert reader.shard_paths("trades", "BTCUSD")[0].suffix == ".zst"
    assert [t.trade_id for t in reader.iter_trades() if isinstance(t, Trade)] == plain


# ---------------------------------------------------------------------------
# the real baseline capture
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not BASELINE_CAPTURE.is_dir(), reason="baseline capture absent")
def test_baseline_capture_manifest_is_readable():
    man = ShardReader(BASELINE_CAPTURE).manifest()
    assert man.total_bytes > 0
    assert len(man.streams["trades"]) == 19
    assert len(man.streams["book_d10"]) == 19


@pytest.mark.skipif(not BASELINE_CAPTURE.is_dir(), reason="baseline capture absent")
def test_baseline_capture_trades_parse_under_deny_by_default():
    """
    Every trade record in a real pair's shards satisfies the strict shape rules.
    If the venue ever adds a field this fails, which is the intent.
    """
    reader = ShardReader(BASELINE_CAPTURE)
    trades = [x for x in reader.iter_trades(symbols=["BTCUSD"]) if isinstance(x, Trade)]
    assert trades, "the baseline capture has BTC trades"
    assert all(t.notional > 0 for t in trades)
    assert all(t.side in ("buy", "sell") for t in trades)
    ids = [t.trade_id for t in trades]
    assert len(ids) == len(set(ids)), "dedupe leaves no duplicate trade_id"


@pytest.mark.skipif(not BASELINE_CAPTURE.is_dir(), reason="baseline capture absent")
def test_baseline_capture_exposes_its_real_coverage_gap():
    """
    The baseline capture's first run ended without a RECORDER_STOP, so coverage
    closes at OPEN_TAIL and any later window is genuinely unattested. The reader
    must expose that rather than serving the shards as if they were continuous.
    """
    reader = ShardReader(BASELINE_CAPTURE)
    extent = reader.journal_extent()
    assert extent is not None
    gaps = reader.gaps("BTCUSD", "trade", extent[0], extent[1])
    assert gaps, "unattested time inside the journal extent must surface"
    assert all(g.duration_s > 0 for g in gaps)
