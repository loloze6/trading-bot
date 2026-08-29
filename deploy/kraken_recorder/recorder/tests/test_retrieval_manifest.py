"""retrieval_manifest.py: what gets hashed, and how the journal differs."""

from __future__ import annotations

import hashlib
from pathlib import Path

from recorder.journal import JOURNAL_FILENAME
from recorder.retrieval_manifest import (
    build_manifest,
    sha256_of_file,
    sha256_of_prefix,
)


def test_compacted_shards_get_a_full_file_hash(tmp_path):
    shard = tmp_path / "book_d10" / "BTCUSD" / "2026-07-26T00.ndjson.zst"
    shard.parent.mkdir(parents=True)
    shard.write_bytes(b"fake zstd bytes")

    manifest = build_manifest(tmp_path)

    rel = "book_d10/BTCUSD/2026-07-26T00.ndjson.zst"
    assert rel in manifest
    assert manifest[rel]["sha256"] == hashlib.sha256(b"fake zstd bytes").hexdigest()
    assert manifest[rel]["bytes"] == len(b"fake zstd bytes")
    assert "prefix" not in manifest[rel]


def test_raw_open_shards_are_never_in_the_manifest(tmp_path):
    raw = tmp_path / "book_d10" / "BTCUSD" / "2026-07-28T20.ndjson"
    raw.parent.mkdir(parents=True)
    raw.write_bytes(b"still being appended to")

    manifest = build_manifest(tmp_path)

    assert manifest == {}


def test_journal_gets_a_prefix_hash_not_a_full_hash(tmp_path):
    journal = tmp_path / JOURNAL_FILENAME
    journal.write_bytes(b'{"type":"RECORDER_START"}\n{"type":"SUBSCRIBE_ACK"}\n')

    manifest = build_manifest(tmp_path)

    entry = manifest[JOURNAL_FILENAME]
    assert entry["prefix"] is True
    assert entry["bytes"] == journal.stat().st_size
    assert entry["sha256"] == sha256_of_file(
        journal
    )  # whole file == its own full prefix here


def test_sha256_of_prefix_matches_a_slice_of_a_larger_file(tmp_path):
    p = tmp_path / "grows.ndjson"
    p.write_bytes(b"AAAA" * 100)
    prefix_hash_at_100 = sha256_of_prefix(p, 100)

    # Simulate the file growing after the manifest snapshot was taken.
    with open(p, "ab") as fh:
        fh.write(b"more data appended later")

    assert sha256_of_prefix(p, 100) == prefix_hash_at_100
    assert sha256_of_prefix(p, 100) == hashlib.sha256((b"AAAA" * 25)).hexdigest()


def test_sha256_of_prefix_raises_if_file_shrunk_below_the_requested_length(tmp_path):
    p = tmp_path / "shrunk.ndjson"
    p.write_bytes(b"short")
    try:
        sha256_of_prefix(p, 1000)
        assert False, "expected ValueError"
    except ValueError:
        pass
