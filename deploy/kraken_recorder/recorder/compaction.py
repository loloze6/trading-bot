"""
Shard compaction — zstd at roll, verified before the raw is deleted.
====================================================================

Compaction runs at the hourly roll, not nightly.

WHY HOURLY AND NOT NIGHTLY
--------------------------
The measured raw rate is ~100.5 kB/s (19 pairs, book depth 10 + full trades),
which is ~8.7 GB/day. A nightly roll therefore keeps up to a full day of raw on
disk before it ever compresses anything. On the volume this runs on that is not
a tuning preference — a nightly roll alone can consume more than half the free
space between two compactions. Hourly caps the uncompressed working set at
roughly one hour (~360 MB) plus whatever the compressor has not yet caught up
on.

VERIFY BEFORE DELETE — THE ONLY ORDERING THAT IS SAFE
-----------------------------------------------------
Compression here is a *destructive* step: it ends with `unlink()` on the only
copy of data that can never be re-fetched, because a forward recording of an
event stream has no upstream to re-read. So the ordering is fixed:

    compress -> decompress -> byte-compare against the source -> THEN unlink

and never any other order. A failed comparison raises
:class:`ShardVerificationError`, removes the partial `.zst`, and leaves the raw
shard **exactly where it was**. There is no repair path and no retry-in-place:
a shard that fails verification is evidence of a real fault (bad block, a
truncated write, a compressor bug), and silently retrying it is how that fault
becomes data loss. This mirrors the journal's doctrine — see
`journal.py:CoverageGapError` — that a defect must announce itself rather than
be smoothed over.

The comparison is a true byte-for-byte compare of the decompressed stream
against the source file, chunk by chunk, including a length check. It is not a
size check and not a checksum of the compressor's own framing: zstd's internal
content checksum would only prove the compressor round-tripped its own input,
which is the assumption under test.

WHY A `.part` FILE
------------------
The compressed output is written to `<shard>.ndjson.zst.part` and renamed to
`<shard>.ndjson.zst` only after verification passes. A crash at any instant
therefore leaves either (raw) or (raw + .part) or (raw + .zst) or (.zst) — never
a `.zst` that has not been verified, and never a window in which neither exists.
:func:`sweep` deletes stale `.part` files on startup for exactly this reason.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable, List, Optional

try:
    import zstandard as zstd
except ImportError:  # pragma: no cover - operator-facing
    zstd = None  # type: ignore

#: Level 10 measured on real shards: near-max ratio at a fraction of the cost of
#: 19+. See the cadence ladder report for the measured per-mode ratios.
DEFAULT_LEVEL = 10
CHUNK = 1 << 20  # 1 MiB
SUFFIX = ".zst"
PART_SUFFIX = ".zst.part"

#: A shard is only a candidate for compaction if its name matches the roll
#: scheme currently in force. This is a safety boundary, not tidiness: the
#: output tree can contain shards written under an EARLIER regime — the first
#: deployment rolled daily (`2026-07-26.ndjson`) — and those are reserved,
#: already-attested captures. A sweep that rewrote them because it did not
#: recognise the name would be modifying reserved data as a side effect of an
#: unrelated startup. Unrecognised names are left strictly alone.
PERIOD_PATTERNS = {
    "hour": re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}$"),
    "day": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
}


class ShardVerificationError(RuntimeError):
    """
    A compressed shard did not decompress back to its source, byte for byte.

    Raised *before* anything is deleted. The raw shard is intact when this
    propagates; the partial `.zst` has been removed. Do not retry automatically
    — see the module docstring.
    """


def _require_zstd() -> None:
    if zstd is None:  # pragma: no cover
        raise RuntimeError("zstandard is not installed. Run:  python -m pip install -r requirements.txt")


def compressed_path(shard: Path) -> Path:
    return Path(str(shard) + SUFFIX)


def part_path(shard: Path) -> Path:
    return Path(str(shard) + PART_SUFFIX)


def verify_against(archive: Path, source: Path) -> None:
    """
    Byte-compare the decompressed `archive` against `source`; raise on any
    difference, including a length difference in either direction.

    Streamed in `CHUNK`-sized pieces so an hour of DOGE book deltas (~100 MB)
    never needs to be resident twice.
    """
    _require_zstd()
    dctx = zstd.ZstdDecompressor()
    pos = 0
    with open(archive, "rb") as afh, open(source, "rb") as sfh:
        with dctx.stream_reader(afh) as reader:
            while True:
                got = reader.read(CHUNK)
                if not got:
                    break
                want = sfh.read(len(got))
                if got != want:
                    if len(got) != len(want):
                        raise ShardVerificationError(
                            f"{archive.name}: decompressed stream is longer than the source at byte {pos + len(want)}"
                        )
                    off = next(i for i in range(len(got)) if got[i] != want[i])
                    raise ShardVerificationError(
                        f"{archive.name}: byte mismatch at offset {pos + off} (got {got[off]!r}, source {want[off]!r})"
                    )
                pos += len(got)
        if sfh.read(1):
            raise ShardVerificationError(
                f"{archive.name}: decompressed stream ended at byte {pos} but "
                f"the source has more data — the archive is TRUNCATED"
            )


def compress_shard(
    shard: Path,
    level: int = DEFAULT_LEVEL,
    delete_source: bool = True,
) -> Optional[Path]:
    """
    Compress one completed shard to `<shard>.zst`, verify it, then (only then)
    delete the raw.

    Returns the archive path, or None if there was nothing to do (shard gone, or
    already compressed). Raises :class:`ShardVerificationError` with the raw
    shard untouched if verification fails.
    """
    _require_zstd()
    shard = Path(shard)
    if not shard.exists():
        return None
    dest = compressed_path(shard)
    if dest.exists():
        # A previous run already produced a verified archive for this shard. The
        # raw is the redundant copy at this point, but deleting it here would be
        # a delete we did not verify in this process, so leave it and report.
        return dest
    part = part_path(shard)
    if part.exists():
        part.unlink()

    cctx = zstd.ZstdCompressor(level=level)
    with open(shard, "rb") as src, open(part, "wb") as out:
        cctx.copy_stream(src, out, read_size=CHUNK, write_size=CHUNK)
        out.flush()
        os.fsync(out.fileno())

    try:
        verify_against(part, shard)
    except Exception:
        # Leave the raw shard exactly as it was; drop the unverified archive.
        try:
            part.unlink()
        except OSError:
            pass
        raise

    os.replace(part, dest)
    if delete_source:
        shard.unlink()
    return dest


def find_rollable(
    out_dir: Path,
    current_keys: Iterable[str],
    roll: str = "hour",
) -> List[Path]:
    """
    Raw `.ndjson` shards eligible for compaction: name matches the `roll`
    scheme's period format, and the period is not one of `current_keys`.

    Used both on the roll path and as a startup sweep, so a shard orphaned by a
    `kill -9` mid-hour is picked up by the successor rather than sitting raw
    forever.

    Shards whose names do NOT match `roll`'s format are skipped — see
    PERIOD_PATTERNS. They belong to another regime and are not this sweep's to
    rewrite.
    """
    live = set(current_keys)
    pattern = PERIOD_PATTERNS.get(roll)
    if pattern is None:
        raise ValueError(f"unknown roll period {roll!r}")
    out: List[Path] = []
    for p in sorted(Path(out_dir).rglob("*.ndjson")):
        if p.name.startswith("_"):
            continue
        if not pattern.match(p.stem):
            continue
        if p.stem in live:
            continue
        out.append(p)
    return out


def sweep(
    out_dir: Path,
    current_keys: Iterable[str],
    level: int = DEFAULT_LEVEL,
    roll: str = "hour",
) -> List[Path]:
    """
    Compress every closed-period raw shard under `out_dir`; also clears stale
    `.part` files from an interrupted compression.

    Returns the archives produced. Propagates ShardVerificationError — a sweep
    that hits a bad shard STOPS rather than continuing past it.
    """
    for stale in Path(out_dir).rglob("*" + PART_SUFFIX):
        stale.unlink()
    made: List[Path] = []
    for shard in find_rollable(out_dir, current_keys, roll=roll):
        archive = compress_shard(shard, level=level)
        if archive is not None:
            made.append(archive)
    return made
