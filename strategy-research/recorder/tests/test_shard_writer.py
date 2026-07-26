"""
NDJSON round-trip.

The contract: whatever the venue sent comes back out byte-identical, and the
receive metadata needed to order frames and align them with the coverage
journal survives with it.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from recorder.shard_writer import ShardWriter, disk_symbol, read_shard

RAW_BOOK = (
    '{"channel":"book","type":"snapshot","data":[{"symbol":"BTC/USD",'
    '"bids":[{"price":45283.5,"qty":0.10000000}],'
    '"asks":[{"price":45284.0,"qty":2.50000000}],'
    '"checksum":3315296300,"timestamp":"2026-07-26T12:00:00.123456Z"}]}'
)
RAW_TRADE = (
    '{"channel":"trade","type":"update","data":[{"symbol":"ETH/USD","side":"buy",'
    '"qty":0.5,"price":2450.12,"ord_type":"market","trade_id":98765,'
    '"timestamp":"2026-07-26T12:00:01.000000Z"}]}'
)


def _today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def test_disk_symbol_matches_the_on_disk_breadth_convention():
    assert disk_symbol("BTC/USD") == "BTCUSD"
    assert disk_symbol("ondo/usd") == "ONDOUSD"


def test_round_trip_preserves_the_frame_exactly(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1")
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.close()

    path = tmp_path / "book_d10" / "BTCUSD" / f"{_today()}.ndjson"
    envelopes = list(read_shard(path))
    assert len(envelopes) == 1
    assert envelopes[0]["raw"] == json.loads(RAW_BOOK)

    # and byte-exact, not merely equal-after-parsing
    assert RAW_BOOK in path.read_text(encoding="utf-8")


def test_trailing_zeros_survive_the_round_trip(tmp_path):
    """
    `0.10000000` must not come back as `0.1`.

    The CRC32 padding rule is computed over decimal renderings, so a
    re-serialising writer would destroy the ability to verify the book later —
    the exact thing the spec's deferral of live verification relies on.
    """
    w = ShardWriter(tmp_path, run_id="r1")
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.close()
    text = (tmp_path / "book_d10" / "BTCUSD" / f"{_today()}.ndjson").read_text("utf-8")
    assert '"qty":0.10000000' in text
    assert '"qty":2.50000000' in text


def test_each_frame_is_exactly_one_line(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1")
    for _ in range(5):
        w.write_frame("trades", "ETHUSD", RAW_TRADE)
    w.close()
    lines = (tmp_path / "trades" / "ETHUSD" / f"{_today()}.ndjson").read_text(
        "utf-8"
    ).splitlines()
    assert len(lines) == 5
    for line in lines:
        json.loads(line)  # each line independently parseable


def test_envelope_carries_recv_ts_seq_and_run_id(tmp_path):
    w = ShardWriter(tmp_path, run_id="run-xyz")
    w.write_frame("trades", "ETHUSD", RAW_TRADE)
    w.write_frame("trades", "ETHUSD", RAW_TRADE)
    w.close()
    envs = list(read_shard(tmp_path / "trades" / "ETHUSD" / f"{_today()}.ndjson"))
    assert [e["seq"] for e in envs] == [1, 2]
    assert all(e["run_id"] == "run-xyz" for e in envs)
    assert all(e["recv_ts"].endswith("Z") for e in envs)
    assert all(isinstance(e["mono"], float) for e in envs)


def test_seq_is_global_across_streams_so_receive_order_is_recoverable(tmp_path):
    """
    Book updates have no venue sequence number and must be replayed in receive
    order. Splitting shards per symbol destroys line-order as a proxy, so the
    order has to live in the envelope.
    """
    w = ShardWriter(tmp_path, run_id="r1")
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.write_frame("trades", "ETHUSD", RAW_TRADE)
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.close()
    book = list(read_shard(tmp_path / "book_d10" / "BTCUSD" / f"{_today()}.ndjson"))
    trade = list(read_shard(tmp_path / "trades" / "ETHUSD" / f"{_today()}.ndjson"))
    assert [e["seq"] for e in book] == [1, 3]
    assert [e["seq"] for e in trade] == [2]


def test_frame_containing_a_newline_falls_back_to_string_encoding(tmp_path):
    """NDJSON cannot carry an embedded newline; the fallback must stay lossless."""
    nasty = '{"channel":"meta","note":"line1\\nline2"}'
    raw_with_real_newline = '{"channel":"meta",\n"note":"x"}'
    w = ShardWriter(tmp_path, run_id="r1")
    w.write_frame("meta", "_session", nasty)                 # escaped \n: spliced
    w.write_frame("meta", "_session", raw_with_real_newline)  # real \n: stringified
    w.close()

    path = tmp_path / "meta" / "_session" / f"{_today()}.ndjson"
    assert len(path.read_text("utf-8").splitlines()) == 2
    envs = list(read_shard(path))
    assert envs[0]["raw"] == json.loads(nasty)
    assert envs[1]["raw"] == raw_with_real_newline  # exact original text


def test_counts_are_per_symbol_and_reset_on_drain(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1")
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.write_frame("trades", "ETHUSD", RAW_TRADE)
    assert w.drain_counts() == {"BTCUSD": 2, "ETHUSD": 1}
    assert w.drain_counts() == {}
    w.close()


def test_appending_after_reopen_does_not_truncate(tmp_path):
    """A restart must extend today's shard, never clobber it."""
    w1 = ShardWriter(tmp_path, run_id="r1")
    w1.write_frame("trades", "ETHUSD", RAW_TRADE)
    w1.close()
    w2 = ShardWriter(tmp_path, run_id="r2")
    w2.write_frame("trades", "ETHUSD", RAW_TRADE)
    w2.close()

    envs = list(read_shard(tmp_path / "trades" / "ETHUSD" / f"{_today()}.ndjson"))
    assert [e["run_id"] for e in envs] == ["r1", "r2"]
    assert [e["seq"] for e in envs] == [1, 1]  # seq is per-process; run_id disambiguates


def test_shard_layout_is_stream_symbol_day(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1")
    w.write_frame("book_d10", "SOLUSD", RAW_BOOK)
    w.close()
    assert (tmp_path / "book_d10" / "SOLUSD" / f"{_today()}.ndjson").exists()


def test_read_shard_on_missing_file_yields_nothing(tmp_path):
    assert list(read_shard(tmp_path / "nope" / "x" / "2026-07-26.ndjson")) == []
