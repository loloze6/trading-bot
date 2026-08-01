"""
Liveness under hourly rolling and compaction.

Both new behaviours make the naive "total bytes went up" test wrong once an
hour, and the snapshot cadence makes the frame counter stop meaning what the
check assumed it meant. Neither may be allowed to turn into a false HEALTHY or a
false UNHEALTHY.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from recorder.journal import JOURNAL_FILENAME
from recorder.liveness import check, growth_bytes, shard_sizes


def test_growth_counts_new_files_and_per_file_increases(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    before = {a: 100}
    after = {a: 180, b: 50}
    assert growth_bytes(before, after) == 130


def test_an_hourly_roll_is_not_read_as_death(tmp_path):
    """The old hour stops growing and a new shard appears — that is health."""
    old, new = tmp_path / "T10.ndjson", tmp_path / "T11.ndjson"
    assert growth_bytes({old: 5_000_000}, {old: 5_000_000, new: 12_345}) == 12_345


def test_compaction_shrinking_the_total_is_not_read_as_death(tmp_path):
    """
    A 360 MB raw shard becoming a 40 MB archive drops the total sharply. A check
    that differenced totals would report UNHEALTHY once an hour, forever.
    """
    raw = tmp_path / "T10.ndjson"
    arc = tmp_path / "T10.ndjson.zst"
    cur = tmp_path / "T11.ndjson"
    before = {raw: 360_000_000, cur: 1_000}
    after = {arc: 40_000_000, cur: 400_000}
    assert sum(after.values()) < sum(before.values()), "total must fall here"
    assert growth_bytes(before, after) == 40_000_000 + 399_000  # archive is new


def test_no_new_bytes_is_still_a_failure():
    p = Path("x")
    assert growth_bytes({p: 100}, {p: 100}) == 0


def test_shard_sizes_counts_archives_and_skips_the_journal(tmp_path):
    d = tmp_path / "book_d10" / "BTCUSD"
    d.mkdir(parents=True)
    (d / "2026-07-26T10.ndjson.zst").write_bytes(b"x" * 10)
    (d / "2026-07-26T11.ndjson").write_bytes(b"y" * 20)
    (tmp_path / JOURNAL_FILENAME).write_bytes(b"z" * 99)
    sizes = shard_sizes(tmp_path)
    assert sum(sizes.values()) == 30
    assert not any(p.name == JOURNAL_FILENAME for p in sizes)


# ------------------------------------------------------------ snapshot mode


def _journal(tmp_path: Path, rollup_extra: dict) -> None:
    import json

    now = datetime.now(timezone.utc)
    recs = [
        {"jseq": 1, "run_id": "r", "ts": _iso(now - timedelta(seconds=90)),
         "type": "RECORDER_START"},
    ]
    for i, sym in enumerate(["BTC/USD"], start=2):
        recs.append({"jseq": i, "run_id": "r",
                     "ts": _iso(now - timedelta(seconds=89)),
                     "type": "SUBSCRIBE_ACK", "symbol": sym, "channel": "book"})
    rollup = {"jseq": 50, "run_id": "r", "ts": _iso(now - timedelta(seconds=5)),
              "type": "HEARTBEAT_ROLLUP", "heartbeats": 60,
              "frames_total": 19, "symbols_seen": 1}
    rollup.update(rollup_extra)
    recs.append(rollup)
    (tmp_path / JOURNAL_FILENAME).write_text(
        "".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8"
    )


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def _shard(tmp_path: Path) -> Path:
    d = tmp_path / "book_d10" / "BTCUSD"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "2026-07-26T11.ndjson"
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(
            '{"recv_ts":"%s","mono":1.0,"run_id":"r","seq":1,"raw":{}}\n'
            % _iso(datetime.now(timezone.utc))
        )
    return p


def _run_check(tmp_path: Path):
    """Run `check` with the shard genuinely growing inside the sleep window."""
    import threading

    p = _shard(tmp_path)

    def append():
        # Must be a well-formed envelope: the FRESH check reads the shard's
        # last line for `recv_ts`, so padding bytes would fail a check this
        # test is not about.
        with open(p, "a", encoding="utf-8") as fh:
            for _ in range(40):
                fh.write(
                    '{"recv_ts":"%s","mono":2.0,"run_id":"r","seq":2,"raw":{}}\n'
                    % _iso(datetime.now(timezone.utc))
                )

    timer = threading.Timer(0.05, append)
    timer.start()
    try:
        return check(tmp_path, window_s=0.4, expect_symbols=1,
                     max_staleness_s=30.0)
    finally:
        timer.cancel()


def test_snapshot_mode_with_a_dead_feed_is_unhealthy(tmp_path):
    """
    The emitter keeps writing books from a stale local state, so `frames_total`
    looks fine. `book_frames_folded == 0` is the only thing that shows the venue
    stopped sending, and it must fail the check.
    """
    _journal(tmp_path, {"book_mode": "snapshot", "snapshot_interval_s": 5.0,
                        "book_frames_folded": 0})
    ok, lines = _run_check(tmp_path)
    assert not ok
    assert any("feed is dead" in ln for ln in lines), lines
    # and it failed for that reason, not because growth was missing
    assert any(ln.startswith("ok    growth") for ln in lines), lines


def test_snapshot_mode_with_a_live_feed_is_healthy(tmp_path):
    _journal(tmp_path, {"book_mode": "snapshot", "snapshot_interval_s": 5.0,
                        "book_frames_folded": 4210})
    ok, lines = _run_check(tmp_path)
    assert ok, lines


def test_delta_mode_rollup_is_unaffected_by_the_snapshot_check(tmp_path):
    _journal(tmp_path, {})          # no book_mode key at all — delta
    ok, lines = _run_check(tmp_path)
    assert ok, lines
