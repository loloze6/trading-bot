"""
retrieve_shards.py: incremental, resumable, verified pull; prune only
deletes what a fresh re-check confirms.

Exercised against LocalDirTransport (another local directory standing in for
the capture host) so this is a real, fully-executed test of the diff/pull/
verify/ledger/prune logic — the SSH+rsync transport itself is reasoned, not
executed, in this environment; see the W15 session report.
"""

from __future__ import annotations

import json
from pathlib import Path

from recorder.journal import JOURNAL_FILENAME
from recorder.retrieve_shards import (
    LEDGER_FILENAME,
    LocalDirTransport,
    load_ledger,
    prune_confirmed,
    pull,
)


def _write_shard(remote: Path, rel: str, content: bytes) -> None:
    p = remote / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)


def test_first_pull_fetches_and_confirms_everything(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "book_d10/BTCUSD/2026-07-26T00.ndjson.zst", b"archive-one")
    _write_shard(remote, "book_d10/BTCUSD/2026-07-26T01.ndjson.zst", b"archive-two")

    result = pull(LocalDirTransport(remote), local)

    assert set(result.pulled) == {
        "book_d10/BTCUSD/2026-07-26T00.ndjson.zst",
        "book_d10/BTCUSD/2026-07-26T01.ndjson.zst",
    }
    assert result.verified == result.pulled
    assert result.failed == []
    assert (
        local / "book_d10/BTCUSD/2026-07-26T00.ndjson.zst"
    ).read_bytes() == b"archive-one"

    ledger = load_ledger(local)
    assert set(ledger) == set(result.pulled)


def test_second_pull_only_fetches_the_new_shard(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "a.ndjson.zst", b"aaa")
    pull(LocalDirTransport(remote), local)

    _write_shard(remote, "b.ndjson.zst", b"bbb")
    result = pull(LocalDirTransport(remote), local)

    assert result.pulled == ["b.ndjson.zst"]
    assert result.already_confirmed == ["a.ndjson.zst"]


def test_journal_prefix_is_incremental_across_growth(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    remote.mkdir()
    journal = remote / JOURNAL_FILENAME
    journal.write_bytes(b'{"a":1}\n')

    r1 = pull(LocalDirTransport(remote), local)
    assert r1.verified == [JOURNAL_FILENAME]
    ledger_after_1 = load_ledger(local)
    assert ledger_after_1[JOURNAL_FILENAME]["bytes"] == 8

    with open(journal, "ab") as fh:
        fh.write(b'{"a":2}\n')

    r2 = pull(LocalDirTransport(remote), local)
    assert r2.pulled == [JOURNAL_FILENAME]  # re-pulled: manifest hash advanced
    ledger_after_2 = load_ledger(local)
    assert ledger_after_2[JOURNAL_FILENAME]["bytes"] == 16
    assert (local / JOURNAL_FILENAME).read_bytes() == journal.read_bytes()


def test_a_pull_that_fails_verification_is_not_confirmed_and_is_retried(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "a.ndjson.zst", b"correct-bytes")

    class CorruptingTransport(LocalDirTransport):
        def pull(self, relative_path, dest):
            super().pull(relative_path, dest)
            dest.write_bytes(b"CORRUPTED")

    result = pull(CorruptingTransport(remote), local)
    assert result.failed == ["a.ndjson.zst"]
    assert result.verified == []
    assert load_ledger(local) == {}

    # Retry with an honest transport: not shielded by a false "already confirmed".
    result2 = pull(LocalDirTransport(remote), local)
    assert result2.pulled == ["a.ndjson.zst"]
    assert result2.verified == ["a.ndjson.zst"]


def test_pull_never_deletes_anything_on_either_side(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "a.ndjson.zst", b"aaa")
    pull(LocalDirTransport(remote), local)

    assert (remote / "a.ndjson.zst").exists()
    assert (local / "a.ndjson.zst").exists()


def test_prune_deletes_only_confirmed_and_unchanged_shards(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "confirmed.ndjson.zst", b"aaa")
    _write_shard(remote, "never_pulled.ndjson.zst", b"bbb")
    pull(LocalDirTransport(remote), local)  # both get confirmed by this pull

    # Strip never_pulled's ledger entry to simulate a shard prune must never
    # touch because this local process never actually confirmed it.
    ledger = load_ledger(local)
    del ledger[Path("never_pulled.ndjson.zst").as_posix()]
    (local / LEDGER_FILENAME).write_text(json.dumps(ledger), encoding="utf-8")

    result = prune_confirmed(LocalDirTransport(remote), local)

    assert result.deleted == ["confirmed.ndjson.zst"]
    assert result.skipped_not_confirmed == ["never_pulled.ndjson.zst"]
    assert not (remote / "confirmed.ndjson.zst").exists()
    assert (remote / "never_pulled.ndjson.zst").exists()


def test_prune_refuses_a_shard_that_changed_since_confirmation(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "a.ndjson.zst", b"original")
    pull(LocalDirTransport(remote), local)

    # Remote content changed after confirmation (should not happen for a
    # real compacted shard, but prune must not trust the ledger blindly).
    (remote / "a.ndjson.zst").write_bytes(b"different-now")

    result = prune_confirmed(LocalDirTransport(remote), local)

    assert result.deleted == []
    assert result.skipped_changed_since_confirmation == ["a.ndjson.zst"]
    assert (remote / "a.ndjson.zst").exists()


def test_prune_never_deletes_the_coverage_journal(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    remote.mkdir()
    (remote / JOURNAL_FILENAME).write_bytes(b'{"a":1}\n')
    pull(LocalDirTransport(remote), local)

    result = prune_confirmed(LocalDirTransport(remote), local)

    assert result.deleted == []
    assert (remote / JOURNAL_FILENAME).exists()


def test_prune_refuses_if_the_local_copy_no_longer_matches(tmp_path):
    remote = tmp_path / "remote"
    local = tmp_path / "local"
    _write_shard(remote, "a.ndjson.zst", b"aaa")
    pull(LocalDirTransport(remote), local)

    (local / "a.ndjson.zst").write_bytes(b"locally-tampered")

    result = prune_confirmed(LocalDirTransport(remote), local)

    assert result.deleted == []
    assert result.skipped_local_mismatch == ["a.ndjson.zst"]
    assert (remote / "a.ndjson.zst").exists()
