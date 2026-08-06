"""
Cadence modes: snapshot-frame construction, and the non-negotiable property
that DELTA mode is unchanged.

The second half of this file is the regression guard for the whole feature. A
storage option that quietly altered the default capture would have spent the
recorder's fidelity to buy disk, which is the one trade this change must not
make.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from recorder.book_state import BookBook, BookState
from recorder.kraken_crc import book_checksum, verify_book_frame
from recorder.record_kraken_ws import (
    BOOK_MODES,
    MODE_DELTA,
    MODE_SNAPSHOT,
    Recorder,
)
from recorder.shard_writer import ShardWriter, read_shard

SNAP = {
    "channel": "book",
    "type": "snapshot",
    "data": [
        {
            "symbol": "BTC/USD",
            "bids": [{"price": "45283.5", "qty": "0.10000000"},
                     {"price": "45283.0", "qty": "1.00000000"}],
            "asks": [{"price": "45284.0", "qty": "2.50000000"},
                     {"price": "45284.5", "qty": "0.20000000"}],
            "checksum": 111,
            "timestamp": "2026-07-26T12:00:00.000000Z",
        }
    ],
}


def _update(bids=None, asks=None, checksum=222, ts="2026-07-26T12:00:01.000000Z"):
    return {
        "channel": "book",
        "type": "update",
        "data": [{
            "symbol": "BTC/USD",
            "bids": bids or [],
            "asks": asks or [],
            "checksum": checksum,
            "timestamp": ts,
        }],
    }


# ------------------------------------------------------- book reconstruction


def test_snapshot_establishes_the_book():
    bb = BookBook(depth=10)
    bb.apply_frame(SNAP)
    st = bb.state("BTC/USD")
    assert st.ready
    lv = st.levels()
    assert [l["price"] for l in lv["bids"]] == ["45283.5", "45283.0"]
    assert [l["price"] for l in lv["asks"]] == ["45284.0", "45284.5"]


def test_update_merges_and_qty_zero_deletes():
    bb = BookBook(depth=10)
    bb.apply_frame(SNAP)
    bb.apply_frame(_update(bids=[{"price": "45283.5", "qty": "0"}]))
    prices = [l["price"] for l in bb.state("BTC/USD").levels()["bids"]]
    assert prices == ["45283.0"], "qty 0 must remove the level, not store a zero"


def test_update_revises_an_existing_level_in_place():
    bb = BookBook(depth=10)
    bb.apply_frame(SNAP)
    bb.apply_frame(_update(bids=[{"price": "45283.5", "qty": "9.99000000"}]))
    top = bb.state("BTC/USD").levels()["bids"][0]
    assert top == {"price": "45283.5", "qty": "9.99000000"}


def test_bids_descend_and_asks_ascend_regardless_of_arrival_order():
    bb = BookBook(depth=10)
    bb.apply_frame(SNAP)
    bb.apply_frame(_update(
        bids=[{"price": "45285.0", "qty": "1"}],   # new best bid, arrives last
        asks=[{"price": "45283.9", "qty": "1"}],   # new best ask
    ))
    lv = bb.state("BTC/USD").levels()
    assert lv["bids"][0]["price"] == "45285.0"
    assert lv["asks"][0]["price"] == "45283.9"


def test_book_is_truncated_to_the_subscribed_depth():
    st = BookState(depth=2)
    st.apply(SNAP["data"][0], "snapshot")
    st.apply({"bids": [{"price": "45290.0", "qty": "1"}],
              "asks": [{"price": "45280.0", "qty": "1"}]}, "update")
    lv = st.levels()
    assert len(lv["bids"]) == 2 and len(lv["asks"]) == 2
    assert [l["price"] for l in lv["bids"]] == ["45290.0", "45283.5"]


def test_a_later_snapshot_replaces_rather_than_merges():
    st = BookState(depth=10)
    st.apply(SNAP["data"][0], "snapshot")
    st.apply({"bids": [{"price": "1.0", "qty": "1"}],
              "asks": [{"price": "2.0", "qty": "1"}]}, "snapshot")
    assert [l["price"] for l in st.levels()["bids"]] == ["1.0"]


def test_venue_decimal_strings_survive_verbatim():
    """
    `0.10000000` must not become `0.1`. The CRC32 padding rule is computed over
    the venue's own rendering, so a normalising reconstruction would silently
    destroy verifiability — the same constraint that forces verbatim splicing
    in shard_writer.py.
    """
    st = BookState(depth=10)
    st.apply(SNAP["data"][0], "snapshot")
    payload = st.snapshot_payload("BTC/USD")
    text = json.dumps(payload)
    assert '"qty": "0.10000000"' in text or '"qty":"0.10000000"' in text
    assert all(isinstance(l["qty"], str) for l in payload["data"][0]["bids"])


# ------------------------------------------------------------ emitted frames


def test_emitted_frame_is_marked_synthetic():
    st = BookState(depth=10)
    st.apply(SNAP["data"][0], "snapshot")
    payload = st.snapshot_payload("BTC/USD")
    assert payload["synthetic"] is True
    assert payload["channel"] == "book" and payload["type"] == "snapshot"
    assert payload["data"][0]["symbol"] == "BTC/USD"


def test_emitted_frame_carries_the_last_venue_checksum_and_timestamp():
    st = BookState(depth=10)
    st.apply(SNAP["data"][0], "snapshot")
    st.apply(_update(checksum=999, ts="2026-07-26T12:00:09.000000Z")["data"][0],
             "update")
    d = st.snapshot_payload("BTC/USD")["data"][0]
    assert d["checksum"] == 999
    assert d["timestamp"] == "2026-07-26T12:00:09.000000Z"


def test_a_synthesised_snapshot_still_verifies_against_the_venue_crc32():
    """
    The claim in book_state.py's docstring, tested: because emission happens
    between applications, the emitted book is exactly the book the last venue
    checksum covers, so snapshot-mode data remains CRC-verifiable.
    """
    bids = [{"price": f"{45283 - i}.0", "qty": "1.00000000"} for i in range(10)]
    asks = [{"price": f"{45284 + i}.0", "qty": "2.00000000"} for i in range(10)]
    crc = book_checksum(asks, bids, price_precision=1, qty_precision=8)

    st = BookState(depth=10)
    st.apply({"symbol": "BTC/USD", "bids": bids, "asks": asks, "checksum": crc},
             "snapshot")
    emitted = st.snapshot_payload("BTC/USD")["data"][0]

    assert verify_book_frame(emitted, price_precision=1, qty_precision=8)


def test_updates_applied_counts_the_interval_and_resets_on_emit():
    st = BookState(depth=10)
    st.apply(SNAP["data"][0], "snapshot")
    st.apply(_update(bids=[{"price": "45283.4", "qty": "1"}])["data"][0], "update")
    assert st.snapshot_payload("BTC/USD")["data"][0]["updates_applied"] == 2
    st.mark_emitted()
    assert st.snapshot_payload("BTC/USD")["data"][0]["updates_applied"] == 0


def test_a_quiet_interval_still_emits_so_quiet_is_distinguishable(tmp_path):
    rec = Recorder(out_dir=tmp_path, symbols=["BTC/USD"],
                   book_mode=MODE_SNAPSHOT, snapshot_interval_s=1.0,
                   compress=False)
    try:
        rec._books.apply_frame(SNAP)
        assert rec.emit_snapshots() == 1
        assert rec.emit_snapshots() == 1, "a still book must still be attested"
        shard = next((tmp_path / "book_d10" / "BTCUSD").glob("*.ndjson"))
        envs = list(read_shard(shard))
        assert [e["raw"]["data"][0]["updates_applied"] for e in envs] == [1, 0]
    finally:
        rec.writer.close()
        rec.journal.close()


def test_symbols_without_a_venue_snapshot_are_not_emitted_empty(tmp_path):
    rec = Recorder(out_dir=tmp_path, symbols=["BTC/USD", "ETH/USD"],
                   book_mode=MODE_SNAPSHOT, compress=False)
    try:
        rec._books.apply_frame(SNAP)
        assert rec.emit_snapshots() == 1, "ETH/USD has no book yet"
        assert not (tmp_path / "book_d10" / "ETHUSD").exists()
    finally:
        rec.writer.close()
        rec.journal.close()


def test_snapshot_mode_envelope_is_flagged(tmp_path):
    rec = Recorder(out_dir=tmp_path, symbols=["BTC/USD"],
                   book_mode=MODE_SNAPSHOT, snapshot_interval_s=7.0,
                   compress=False)
    try:
        rec._books.apply_frame(SNAP)
        rec.emit_snapshots()
        shard = next((tmp_path / "book_d10" / "BTCUSD").glob("*.ndjson"))
        env = list(read_shard(shard))[0]
        assert env["synth"] == "book_snapshot"
        assert env["interval_s"] == 7.0
    finally:
        rec.writer.close()
        rec.journal.close()


def test_snapshot_mode_does_not_write_book_deltas(tmp_path):
    rec = Recorder(out_dir=tmp_path, symbols=["BTC/USD"],
                   book_mode=MODE_SNAPSHOT, compress=False)
    try:
        rec._handle(json.dumps(SNAP))
        rec._handle(json.dumps(_update(bids=[{"price": "45283.4", "qty": "1"}])))
        assert not (tmp_path / "book_d10" / "BTCUSD").exists(), \
            "deltas must be folded, not written, in snapshot mode"
        assert rec._book_frames_folded == 2
    finally:
        rec.writer.close()
        rec.journal.close()


def test_snapshot_mode_still_captures_trades_verbatim(tmp_path):
    trade = ('{"channel":"trade","type":"update","data":[{"symbol":"BTC/USD",'
             '"side":"buy","qty":0.5,"price":2450.12,"trade_id":1}]}')
    rec = Recorder(out_dir=tmp_path, symbols=["BTC/USD"],
                   book_mode=MODE_SNAPSHOT, compress=False)
    try:
        rec._handle(trade)
        shard = next((tmp_path / "trades" / "BTCUSD").glob("*.ndjson"))
        assert trade in shard.read_text("utf-8"), "trades are never downsampled"
    finally:
        rec.writer.close()
        rec.journal.close()


# ================================================================= THE GUARD
# DELTA MODE MUST BE BYTE-IDENTICAL TO PRE-CHANGE BEHAVIOUR
# ===========================================================================

#: The envelope this writer produced before the cadence option existed. Pinned
#: literally: asserting against a regenerated string would pass even if both
#: sides drifted together.
PRE_CHANGE_ENVELOPE = re.compile(
    r'^\{"recv_ts":"(?P<recv>[0-9T:.\-]+Z)",'
    r'"mono":(?P<mono>-?\d+\.\d{6}),'
    r'"run_id":"(?P<run>[^"]*)",'
    r'"seq":(?P<seq>\d+),'
    r'"raw":(?P<raw>.*)\}$'
)

RAW_BOOK = (
    '{"channel":"book","type":"snapshot","data":[{"symbol":"BTC/USD",'
    '"bids":[{"price":45283.5,"qty":0.10000000}],'
    '"asks":[{"price":45284.0,"qty":2.50000000}],'
    '"checksum":3315296300,"timestamp":"2026-07-26T12:00:00.123456Z"}]}'
)


def test_delta_mode_line_matches_the_pre_change_envelope_exactly(tmp_path):
    w = ShardWriter(tmp_path, run_id="run-xyz", compress=False)
    w.write_frame("book_d10", "BTCUSD", RAW_BOOK)
    w.close()

    line = next((tmp_path / "book_d10" / "BTCUSD").glob("*.ndjson")).read_text(
        "utf-8"
    ).splitlines()[0]

    m = PRE_CHANGE_ENVELOPE.match(line)
    assert m is not None, f"envelope shape changed: {line[:160]}"
    assert m.group("raw") == RAW_BOOK, "frame is no longer spliced verbatim"
    assert m.group("run") == "run-xyz"
    assert m.group("seq") == "1"

    # No field was added anywhere: the key set is exactly the pre-change one.
    assert set(json.loads(line)) == {"recv_ts", "mono", "run_id", "seq", "raw"}


def test_delta_mode_is_byte_identical_to_a_reconstruction_of_the_old_format(
    tmp_path,
):
    """
    Reconstruct the pre-change line from the envelope's own recv_ts/mono/seq
    and require the bytes on disk to equal it. Anything the new code inserts —
    a flag, a reordered key, a changed float format — breaks this.
    """
    w = ShardWriter(tmp_path, run_id="r1", compress=False)
    for _ in range(3):
        w.write_frame("trades", "ETHUSD", RAW_BOOK)
    w.close()

    for line in next(
        (tmp_path / "trades" / "ETHUSD").glob("*.ndjson")
    ).read_text("utf-8").splitlines():
        env = json.loads(line)
        expected = (
            '{"recv_ts":"%s","mono":%.6f,"run_id":"%s","seq":%d,"raw":%s}'
            % (env["recv_ts"], env["mono"], env["run_id"], env["seq"], RAW_BOOK)
        )
        assert line == expected


def test_extra_is_the_only_way_to_add_fields_and_delta_never_uses_it(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1", compress=False)
    w.write_frame("meta", "_session", RAW_BOOK)                       # delta path
    w.write_frame("meta", "_session", RAW_BOOK, extra={"synth": "x"})  # opt-in
    w.close()
    a, b = next((tmp_path / "meta" / "_session").glob("*.ndjson")).read_text(
        "utf-8"
    ).splitlines()
    assert "synth" not in a
    assert json.loads(b)["synth"] == "x"
    assert json.loads(b)["raw"] == json.loads(RAW_BOOK)


def test_delta_is_the_default_everywhere(tmp_path):
    assert BOOK_MODES[0] == MODE_DELTA
    rec = Recorder(out_dir=tmp_path, symbols=["BTC/USD"], compress=False)
    try:
        assert rec.book_mode == MODE_DELTA
        assert rec._books is None, "no book is reconstructed in delta mode"
        rec._handle(json.dumps(SNAP))
        rec._handle(json.dumps(_update(bids=[{"price": "45283.4", "qty": "1"}])))
        shard = next((tmp_path / "book_d10" / "BTCUSD").glob("*.ndjson"))
        lines = shard.read_text("utf-8").splitlines()
        assert len(lines) == 2, "every book frame must be written in delta mode"
        assert json.loads(lines[0])["raw"] == SNAP
    finally:
        rec.writer.close()
        rec.journal.close()


def test_invalid_mode_is_rejected_rather_than_defaulted(tmp_path):
    with pytest.raises(ValueError, match="book_mode"):
        Recorder(out_dir=tmp_path, book_mode="hourly")
    with pytest.raises(ValueError, match="snapshot_interval_s"):
        Recorder(out_dir=tmp_path, book_mode=MODE_SNAPSHOT, snapshot_interval_s=0)
