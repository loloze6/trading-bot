"""
Hourly roll + compaction, with the ordering that matters: VERIFY BEFORE DELETE.

Compaction is the only destructive step in the recorder, operating on data that
has no upstream to re-fetch. So the tests that matter here are not "does it
compress" but "what is on disk when verification fails".
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

zstd = pytest.importorskip("zstandard")

from recorder import compaction
from recorder.compaction import (
    ShardVerificationError,
    compress_shard,
    compressed_path,
    find_rollable,
    part_path,
    sweep,
    verify_against,
)
from recorder.shard_writer import ShardWriter, read_shard

RAW = (
    '{"channel":"book","type":"update","data":[{"symbol":"BTC/USD",'
    '"bids":[{"price":45283.5,"qty":0.10000000}],"asks":[],'
    '"checksum":3315296300,"timestamp":"2026-07-26T12:00:00.123456Z"}]}'
)


def _shard(tmp_path: Path, name: str = "2026-07-26T11.ndjson", n: int = 200) -> Path:
    p = tmp_path / "book_d10" / "BTCUSD" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(RAW + "\n" for _ in range(n)), encoding="utf-8")
    return p


# --------------------------------------------------------------- verification


def test_verify_accepts_a_faithful_archive(tmp_path):
    src = _shard(tmp_path)
    arc = tmp_path / "a.zst"
    arc.write_bytes(zstd.ZstdCompressor().compress(src.read_bytes()))
    verify_against(arc, src)  # must not raise


def test_verify_rejects_an_archive_of_different_content(tmp_path):
    src = _shard(tmp_path)
    other = src.read_bytes().replace(b"45283.5", b"45283.6")
    arc = tmp_path / "a.zst"
    arc.write_bytes(zstd.ZstdCompressor().compress(other))
    with pytest.raises(ShardVerificationError, match="byte mismatch"):
        verify_against(arc, src)


def test_verify_rejects_a_truncated_archive(tmp_path):
    src = _shard(tmp_path)
    arc = tmp_path / "a.zst"
    arc.write_bytes(zstd.ZstdCompressor().compress(src.read_bytes()[:-500]))
    with pytest.raises(ShardVerificationError, match="TRUNCATED"):
        verify_against(arc, src)


def test_verify_rejects_an_over_long_archive(tmp_path):
    src = _shard(tmp_path)
    arc = tmp_path / "a.zst"
    arc.write_bytes(zstd.ZstdCompressor().compress(src.read_bytes() + b"extra\n"))
    with pytest.raises(ShardVerificationError, match="longer than"):
        verify_against(arc, src)


# ------------------------------------------------------- compress_shard paths


def test_compress_replaces_the_raw_only_after_verifying(tmp_path):
    src = _shard(tmp_path)
    original = src.read_bytes()
    arc = compress_shard(src)

    assert arc == compressed_path(src)
    assert arc.exists()
    assert not src.exists(), "raw must be gone once the archive verified"
    assert not part_path(src).exists()
    assert zstd.ZstdDecompressor().decompress(arc.read_bytes(), max_output_size=len(original) * 2) == original
    assert arc.stat().st_size < len(original)


def test_failed_verification_leaves_the_raw_shard_intact(tmp_path, monkeypatch):
    """
    THE test for this feature. A verification failure must abort with the raw
    shard exactly where it was and no archive left claiming to replace it.
    """
    src = _shard(tmp_path)
    before = src.read_bytes()

    def boom(archive, source):
        raise ShardVerificationError("simulated bad block")

    monkeypatch.setattr(compaction, "verify_against", boom)

    with pytest.raises(ShardVerificationError, match="simulated bad block"):
        compress_shard(src)

    assert src.exists(), "raw shard was deleted despite a failed verification"
    assert src.read_bytes() == before, "raw shard was modified"
    assert not compressed_path(src).exists(), "unverified archive was published"
    assert not part_path(src).exists(), "partial archive left behind"


def test_compress_is_a_noop_on_a_missing_shard(tmp_path):
    assert compress_shard(tmp_path / "gone.ndjson") is None


def test_existing_archive_is_not_silently_replaced(tmp_path):
    src = _shard(tmp_path)
    compress_shard(src)
    again = _shard(tmp_path)  # a raw shard reappears alongside the archive
    out = compress_shard(again)
    assert out == compressed_path(again)
    assert again.exists(), "raw kept: this process verified no deletion of it"


def test_stale_part_file_is_cleared_before_recompressing(tmp_path):
    src = _shard(tmp_path)
    part_path(src).write_bytes(b"garbage from a killed process")
    arc = compress_shard(src)
    assert arc.exists() and not part_path(src).exists()


# --------------------------------------------------------------------- sweep


def test_sweep_compacts_closed_periods_and_spares_the_open_one(tmp_path):
    closed = _shard(tmp_path, "2026-07-26T10.ndjson")
    current = _shard(tmp_path, "2026-07-26T11.ndjson")

    made = sweep(tmp_path, current_keys=["2026-07-26T11"])

    assert made == [compressed_path(closed)]
    assert not closed.exists()
    assert current.exists(), "the open period must never be compacted"


def test_sweep_skips_the_coverage_journal(tmp_path):
    journal = tmp_path / "_session.ndjson"
    journal.write_text('{"jseq":1}\n', encoding="utf-8")
    _shard(tmp_path, "2026-07-26T10.ndjson")
    sweep(tmp_path, current_keys=["2026-07-26T11"])
    assert journal.exists() and not compressed_path(journal).exists()


def test_sweep_removes_stale_part_files(tmp_path):
    src = _shard(tmp_path, "2026-07-26T10.ndjson")
    orphan = part_path(tmp_path / "book_d10" / "BTCUSD" / "2026-07-26T09.ndjson")
    orphan.write_bytes(b"junk")
    sweep(tmp_path, current_keys=["2026-07-26T11"])
    assert not orphan.exists()


def test_find_rollable_excludes_open_keys(tmp_path):
    _shard(tmp_path, "2026-07-26T09.ndjson")
    _shard(tmp_path, "2026-07-26T10.ndjson")
    got = {p.stem for p in find_rollable(tmp_path, ["2026-07-26T10"])}
    assert got == {"2026-07-26T09"}


def test_sweep_leaves_shards_from_another_roll_regime_alone(tmp_path):
    """
    The output tree still holds DAILY-named shards from the first deployment,
    and those are reserved, already-attested captures. An hourly sweep must not
    rewrite them just because it does not recognise the name: that would be a
    silent modification of reserved data triggered by an unrelated startup.
    """
    legacy = _shard(tmp_path, "2026-07-26.ndjson")  # daily regime
    stale_hour = _shard(tmp_path, "2026-07-26T10.ndjson")

    made = sweep(tmp_path, current_keys=["2026-07-26T11"], roll="hour")

    assert made == [compressed_path(stale_hour)]
    assert legacy.exists(), "a daily-regime shard was rewritten by an hourly sweep"
    assert not compressed_path(legacy).exists()


def test_a_day_roll_sweep_ignores_hourly_shards(tmp_path):
    hourly = _shard(tmp_path, "2026-07-26T10.ndjson")
    daily = _shard(tmp_path, "2026-07-25.ndjson")
    made = sweep(tmp_path, current_keys=["2026-07-26"], roll="day")
    assert made == [compressed_path(daily)]
    assert hourly.exists()


def test_unrecognised_shard_names_are_never_compacted(tmp_path):
    odd = _shard(tmp_path, "backfill_2026Q1.ndjson")
    sweep(tmp_path, current_keys=["2026-07-26T11"], roll="hour")
    assert odd.exists()


# ------------------------------------------------- writer-driven hourly roll


def test_writer_rolls_hourly_and_compacts_the_closed_hour(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1", roll="hour")
    keys = iter(["2026-07-26T10"] * 3 + ["2026-07-26T11"] * 3)
    w.period_key = lambda when=None: next(keys)  # type: ignore[assignment]

    for _ in range(3):
        w.write_frame("book_d10", "BTCUSD", RAW)  # hour 10
    w.write_frame("book_d10", "BTCUSD", RAW)  # rolls into hour 11
    w.close()

    d = tmp_path / "book_d10" / "BTCUSD"
    assert (d / "2026-07-26T10.ndjson.zst").exists(), "closed hour not compacted"
    assert not (d / "2026-07-26T10.ndjson").exists(), "raw of closed hour retained"
    assert (d / "2026-07-26T11.ndjson").exists(), "open hour must stay raw"
    assert not (d / "2026-07-26T11.ndjson.zst").exists()

    envs = list(read_shard(d / "2026-07-26T10.ndjson.zst"))
    assert [e["seq"] for e in envs] == [1, 2, 3]


def test_close_does_not_compact_the_open_hour_so_a_restart_can_append(tmp_path):
    """
    A recorder restarted inside the same hour must extend the shard it left.
    Compacting on close would strand it behind an archive.
    """
    w1 = ShardWriter(tmp_path, run_id="r1", roll="hour")
    w1.period_key = lambda when=None: "2026-07-26T11"  # type: ignore[assignment]
    w1.write_frame("trades", "ETHUSD", RAW)
    w1.close()

    p = tmp_path / "trades" / "ETHUSD" / "2026-07-26T11.ndjson"
    assert p.exists() and not compressed_path(p).exists()

    w2 = ShardWriter(tmp_path, run_id="r2", roll="hour")
    w2.period_key = lambda when=None: "2026-07-26T11"  # type: ignore[assignment]
    w2.write_frame("trades", "ETHUSD", RAW)
    w2.close()

    assert [e["run_id"] for e in read_shard(p)] == ["r1", "r2"]


def test_read_shard_finds_a_shard_that_compaction_has_moved(tmp_path):
    """Consumers ask for `<hour>.ndjson`; compaction must not break that."""
    src = _shard(tmp_path, "2026-07-26T10.ndjson", n=5)
    compress_shard(src)
    assert not src.exists()
    assert len(list(read_shard(src))) == 5


def test_compress_disabled_leaves_everything_raw(tmp_path):
    w = ShardWriter(tmp_path, run_id="r1", roll="hour", compress=False)
    keys = iter(["2026-07-26T10", "2026-07-26T11"])
    w.period_key = lambda when=None: next(keys)  # type: ignore[assignment]
    w.write_frame("book_d10", "BTCUSD", RAW)
    w.write_frame("book_d10", "BTCUSD", RAW)
    w.close()
    d = tmp_path / "book_d10" / "BTCUSD"
    assert (d / "2026-07-26T10.ndjson").exists()
    assert not list(d.glob("*.zst"))


def test_writer_surfaces_a_compaction_failure_rather_than_swallowing_it(tmp_path, monkeypatch):
    def boom(archive, source):
        raise ShardVerificationError("simulated")

    monkeypatch.setattr(compaction, "verify_against", boom)

    w = ShardWriter(tmp_path, run_id="r1", roll="hour")
    keys = iter(["2026-07-26T10", "2026-07-26T11"])
    w.period_key = lambda when=None: next(keys)  # type: ignore[assignment]
    w.write_frame("book_d10", "BTCUSD", RAW)
    w.write_frame("book_d10", "BTCUSD", RAW)
    w.close()

    errs = w.compaction_errors()
    assert len(errs) == 1 and isinstance(errs[0], ShardVerificationError)
    assert (tmp_path / "book_d10" / "BTCUSD" / "2026-07-26T10.ndjson").exists()
