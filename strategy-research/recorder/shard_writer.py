"""
Verbatim NDJSON shard writer.
=============================

One line per received websocket frame. The line is an envelope carrying local
receive metadata plus the frame **byte-for-byte as it arrived**:

    {"recv_ts":"...","mono":12.34,"run_id":"...","seq":91,"raw":<frame text>}

`raw` is *spliced*, not re-serialised. A frame is already valid JSON, so its
text drops straight into the envelope, and the bytes on disk are the bytes off
the wire. This is not fussiness: `kraken_crc.py` needs the venue's exact
decimal renderings (a `0.12340` that a `json.dumps` round-trip would rewrite as
`0.1234` breaks the checksum's precision-padding rule), and more generally, a
recorder that reinterprets its input has already made the recording a
derivative rather than a capture. There is no schema, no parsing beyond the
routing peek below, and no normalisation.

If a frame ever contains a raw newline (Kraken does not send one; NDJSON cannot
survive one) the writer falls back to embedding it as a JSON *string* and sets
`"raw_is_string":true`. Lossless either way, and the flag tells a reader which
shape it is holding.

LAYOUT
    {out_dir}/{stream}/{SYMBOL}/{YYYY-MM-DD}.ndjson

`SYMBOL` is the venue's `BTC/USD` mapped to `BTCUSD`, matching the on-disk
convention of the 19 breadth pairs (`kraken_<BASE>USD_1h.csv`). Path components
keep the `kraken_` exchange qualification of `ccxt_fetcher.py:120-121` at the
root of `out_dir`, so no future venue can collide into this namespace.

DURABILITY
    `flush()` per line, `fsync` periodically. A flushed line survives process
    death (the OS holds it); only a machine-level crash can lose the unsynced
    window. The *journal* is fsynced per record instead, because it is the
    thing that must never over-attest. Losing a few frames while the journal
    correctly reports the interval as covered is a data-quality event; losing
    journal records while frames survive is a correctness event.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, TextIO, Tuple

#: Venue symbol 'BTC/USD' -> on-disk 'BTCUSD'.
def disk_symbol(ws_symbol: str) -> str:
    return ws_symbol.replace("/", "").upper()


class ShardWriter:
    """Daily-rotated, per-(stream, symbol) NDJSON shards."""

    def __init__(self, out_dir: Path, run_id: str, fsync_interval_s: float = 5.0):
        self.out_dir = Path(out_dir)
        self.run_id = run_id
        self.fsync_interval_s = fsync_interval_s
        self._t0 = time.monotonic()
        self._files: Dict[Tuple[str, str], Tuple[str, TextIO]] = {}
        self._seq = 0
        self._last_fsync = time.monotonic()
        #: frames written per disk-symbol since the last :meth:`drain_counts`
        self._counts: Dict[str, int] = {}

    # -- paths -------------------------------------------------------------

    def shard_path(self, stream: str, symbol: str, day: str) -> Path:
        return self.out_dir / stream / symbol / f"{day}.ndjson"

    def _handle(self, stream: str, symbol: str, day: str) -> TextIO:
        key = (stream, symbol)
        cached = self._files.get(key)
        if cached is not None:
            cached_day, fh = cached
            if cached_day == day:
                return fh
            fh.flush()
            os.fsync(fh.fileno())
            fh.close()
        path = self.shard_path(stream, symbol, day)
        path.parent.mkdir(parents=True, exist_ok=True)
        fh = open(path, "a", encoding="utf-8", newline="\n")
        self._files[key] = (day, fh)
        return fh

    # -- writing -----------------------------------------------------------

    def write_frame(self, stream: str, symbol: str, raw: str) -> int:
        """
        Append one verbatim frame. Returns the envelope sequence number.

        `seq` is per-process and strictly increasing in *receive order*. Kraken
        book updates carry no sequence numbers and the venue requires that
        "updates should always be processed in sequence", so receive order is
        the only ordering a consumer can reconstruct — it must be recorded
        explicitly rather than inferred from line position, which shard
        rotation and per-symbol splitting would otherwise scramble.
        """
        now = datetime.now(timezone.utc)
        day = now.strftime("%Y-%m-%d")
        self._seq += 1
        text = raw.strip()

        head = (
            '{"recv_ts":"%s","mono":%.6f,"run_id":"%s","seq":%d,'
            % (
                now.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
                time.monotonic() - self._t0,
                self.run_id,
                self._seq,
            )
        )
        if "\n" in text or "\r" in text:
            line = head + '"raw_is_string":true,"raw":' + json.dumps(text) + "}"
        else:
            line = head + '"raw":' + text + "}"

        fh = self._handle(stream, symbol, day)
        fh.write(line + "\n")
        fh.flush()
        self._counts[symbol] = self._counts.get(symbol, 0) + 1

        if time.monotonic() - self._last_fsync >= self.fsync_interval_s:
            self.sync()
        return self._seq

    def drain_counts(self) -> Dict[str, int]:
        """Frame counts per symbol since the last call; resets the tally."""
        counts = self._counts
        self._counts = {}
        return counts

    def current_shards(self) -> Dict[Tuple[str, str], Path]:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return {
            key: self.shard_path(key[0], key[1], day) for key in self._files
        }

    def sync(self) -> None:
        for _day, fh in self._files.values():
            fh.flush()
            os.fsync(fh.fileno())
        self._last_fsync = time.monotonic()

    def close(self) -> None:
        for _day, fh in self._files.values():
            try:
                fh.flush()
                os.fsync(fh.fileno())
            finally:
                fh.close()
        self._files.clear()


# ---------------------------------------------------------------------------
# Read side
# ---------------------------------------------------------------------------


def read_shard(path: Path):
    """
    Yield parsed envelopes from a shard.

    Deliberately returns the envelope, not the payload: a consumer that never
    sees `recv_ts`/`seq` cannot order frames across shards and cannot align
    them against the coverage journal, which is the only thing that makes an
    absence of frames interpretable.

    `raw` is a parsed object in the normal (spliced) case and the exact
    original TEXT when `raw_is_string` is set. It is not re-parsed in the
    latter case: that fallback exists precisely because the frame was not
    something we could round-trip through the envelope's JSON, so re-decoding
    it would discard the original bytes the fallback was there to keep.
    `raw_is_string` is the flag a consumer switches on.
    """
    p = Path(path)
    if not p.exists():
        return
    with open(p, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
