"""
Remote-side manifest for shard retrieval (dispatch W15 step 4).
================================================================

    python -m recorder.retrieval_manifest --out DIR

Prints one JSON object to stdout: `{relative_path: {"sha256", "bytes",
["prefix": true]}}` for every compacted shard and the coverage journal under
`DIR`. Run on the CAPTURE host (over SSH, by `retrieve_shards.py`) so the
analysis host has something independently computed to verify a transfer
against, rather than trusting the transfer's own protocol alone.

WHY COMPACTED SHARDS ONLY, NOT RAW `.ndjson`
---------------------------------------------
A raw shard for the CURRENT open period is being appended to right now.
Hashing it is hashing a moving target: the manifest would be stale before the
transfer even starts, and the mismatch would look like corruption when it is
actually just growth. Compacted `.zst` archives are the right unit instead —
`compaction.py` never produces one until the period is closed AND it has
already been byte-verified once (compress -> decompress -> compare), so a
`.zst` on disk is immutable and safe to hash and ship. A shard that has not
been compacted yet yields nothing to retrieve for that period; it will
appear once the next hourly roll compacts it. This is a retrieval-ordering
constraint, not data loss — the raw shard is still safe on the capture host.

WHY THE JOURNAL IS DIFFERENT: A PREFIX HASH, NOT A FULL HASH
--------------------------------------------------------------
The coverage journal (`_session.ndjson`) is append-only and, unlike a shard,
is NEVER closed while the recorder runs — attestation would be meaningless
if retrieval had to wait for it to stop growing. So its manifest entry is
`{"sha256": sha256_of_first_N_bytes, "bytes": N, "prefix": true}` rather than
a whole-file hash. Receiving at least the first N bytes intact is exactly
what `retrieve_shards.py` verifies; anything the journal gained after this
manifest was taken is simply not claimed here; a later manifest with a larger
N claims it, and journal.py's own `load_records` already tolerates a torn
final line if a pull lands mid-write of record N+1 — see journal.py's
`torn_tail`. Consequently `retrieve_shards.py` never re-transfers journal
bytes it has already confirmed: an appended journal only requires shipping
the delta past the previous manifest's N.

WHY THE ANALYSIS HOST NEVER RECOMPUTES A REMOTE HASH ITSELF
--------------------------------------------------------------
This module runs where the data lives (over SSH), rather than the analysis
host reading the remote file over the network to hash it locally, so a
transport-layer defect (corruption in the very transfer this module's output
is meant to catch) cannot also corrupt the reference value being checked
against.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict

if __package__ in (None, ""):  # allow direct execution
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.journal import JOURNAL_FILENAME  # type: ignore
    from recorder.record_kraken_ws import DEFAULT_OUT  # type: ignore
else:
    from .journal import JOURNAL_FILENAME
    from .record_kraken_ws import DEFAULT_OUT

#: Streamed in chunks so hashing a multi-hundred-MB archive never needs the
#: whole file resident.
_CHUNK = 1 << 20


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(_CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def sha256_of_prefix(path: Path, n: int) -> str:
    """sha256 of the first `n` bytes of `path`. Raises if the file is shorter."""
    h = hashlib.sha256()
    remaining = n
    with open(path, "rb") as fh:
        while remaining > 0:
            chunk = fh.read(min(_CHUNK, remaining))
            if not chunk:
                raise ValueError(
                    f"{path}: file is shorter than the requested prefix "
                    f"({n} bytes) — has it shrunk since the manifest was made?"
                )
            h.update(chunk)
            remaining -= len(chunk)
    return h.hexdigest()


def build_manifest(out_dir: Path) -> Dict[str, Dict[str, Any]]:
    """
    Manifest for every `*.ndjson.zst` archive plus the coverage journal,
    keyed by path relative to `out_dir` with forward slashes (so a Windows
    analysis host and a Linux capture host agree on the key spelling).
    """
    out_dir = Path(out_dir)
    manifest: Dict[str, Dict[str, Any]] = {}

    for p in sorted(out_dir.rglob("*.ndjson.zst")):
        rel = p.relative_to(out_dir).as_posix()
        manifest[rel] = {
            "sha256": sha256_of_file(p),
            "bytes": p.stat().st_size,
        }

    journal_path = out_dir / JOURNAL_FILENAME
    if journal_path.exists():
        size = journal_path.stat().st_size
        manifest[JOURNAL_FILENAME] = {
            "sha256": sha256_of_prefix(journal_path, size),
            "bytes": size,
            "prefix": True,
        }

    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Emit a JSON manifest of retrievable recorder output (W15 step 4)"
    )
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)

    manifest = build_manifest(Path(args.out))
    json.dump(manifest, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
