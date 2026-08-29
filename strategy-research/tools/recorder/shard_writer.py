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
    {out_dir}/{stream}/{SYMBOL}/{YYYY-MM-DDTHH}.ndjson       (roll="hour")
    {out_dir}/{stream}/{SYMBOL}/{YYYY-MM-DD}.ndjson          (roll="day")

`SYMBOL` is the venue's `BTC/USD` mapped to `BTCUSD`, matching the on-disk
convention of the 19 breadth pairs (`kraken_<BASE>USD_1h.csv`). Path components
keep the `kraken_` exchange qualification of `ccxt_fetcher.py:120-121` at the
root of `out_dir`, so no future venue can collide into this namespace.

ROLL PERIOD AND COMPACTION
    The roll is HOURLY by default. That is a change from the original daily
    shard, and it is driven by compaction rather than by taste: raw capture runs
    at ~100.5 kB/s (~8.7 GB/day), so a daily roll leaves up to a full day of
    uncompressed data on disk before anything is ever compressed. Hourly caps
    the raw working set at ~360 MB. See `compaction.py`.

    When the period key changes, the closed shard is handed to a single
    background compression thread. Compression is NOT done inline: an hour of
    DOGE book deltas is ~100 MB and zstd on it takes seconds, and this writer is
    called from the websocket receive path, where a multi-second stall would trip
    the 10 s heartbeat watchdog and be journalled as a disconnect. The worker
    thread is genuinely concurrent because zstandard releases the GIL.

    The shard for the CURRENT period is never compressed, including at
    `close()`. A process that stopped and restarted inside the same hour must be
    able to append to the shard it left; if `close()` had compressed it, the
    successor would start a second shard for a period that already has an
    archive. Leftovers from a period that closed while nothing was running are
    picked up by `compaction.sweep()` at startup.

DURABILITY
    `flush()` per line, `fsync` periodically. A flushed line survives process
    death (the OS holds it); only a machine-level crash can lose the unsynced
    window. The *journal* is fsynced per record instead, because it is the
    thing that must never over-attest. Losing a few frames while the journal
    correctly reports the interval as covered is a data-quality event; losing
    journal records while frames survive is a correctness event.
"""

from __future__ import annotations

import io
import json
import os
import time
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO, Tuple

if __package__ in (None, ""):  # allow direct execution
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.compaction import DEFAULT_LEVEL, compress_shard  # type: ignore
else:
    from .compaction import DEFAULT_LEVEL, compress_shard

#: Period key formats. 'hour' is the default; see ROLL PERIOD above.
PERIOD_FORMATS = {"hour": "%Y-%m-%dT%H", "day": "%Y-%m-%d"}


#: Venue symbol 'BTC/USD' -> on-disk 'BTCUSD'.
def disk_symbol(ws_symbol: str) -> str:
    return ws_symbol.replace("/", "").upper()


class ShardWriter:
    """Hourly-rotated (by default), per-(stream, symbol) NDJSON shards."""

    def __init__(
        self,
        out_dir: Path,
        run_id: str,
        fsync_interval_s: float = 5.0,
        roll: str = "hour",
        compress: bool = True,
        compress_level: int = DEFAULT_LEVEL,
    ):
        if roll not in PERIOD_FORMATS:
            raise ValueError(
                f"roll must be one of {sorted(PERIOD_FORMATS)}, got {roll!r}"
            )
        self.out_dir = Path(out_dir)
        self.run_id = run_id
        self.fsync_interval_s = fsync_interval_s
        self.roll = roll
        self.compress = compress
        self.compress_level = compress_level
        self._t0 = time.monotonic()
        self._files: Dict[Tuple[str, str], Tuple[str, TextIO]] = {}
        self._seq = 0
        self._last_fsync = time.monotonic()
        #: frames written per disk-symbol since the last :meth:`drain_counts`
        self._counts: Dict[str, int] = {}
        #: bytes handed to the OS since the last :meth:`drain_bytes`. Counted at
        #: the writer rather than by stat-ing the tree, so the operational log
        #: reports write THROUGHPUT and stays correct across the hourly roll and
        #: compaction, both of which make on-disk totals fall (see
        #: `liveness.growth_bytes` for the same distinction).
        self._bytes: int = 0
        #: one worker: compaction is I/O+CPU bound and ordering keeps the disk
        #: working set predictable. Never runs on the receive path.
        self._pool: Optional[ThreadPoolExecutor] = (
            ThreadPoolExecutor(max_workers=1, thread_name_prefix="shard-compact")
            if compress
            else None
        )
        self._pending: List[Future] = []

    # -- paths -------------------------------------------------------------

    def period_key(self, when: Optional[datetime] = None) -> str:
        when = when or datetime.now(timezone.utc)
        return when.strftime(PERIOD_FORMATS[self.roll])

    def shard_path(self, stream: str, symbol: str, day: str) -> Path:
        return self.out_dir / stream / symbol / f"{day}.ndjson"

    def open_keys(self) -> List[str]:
        """Period keys with a shard currently open — never compacted."""
        return sorted({day for day, _fh in self._files.values()} | {self.period_key()})

    # -- compaction --------------------------------------------------------

    def _queue_compaction(self, path: Path) -> None:
        if not self.compress or self._pool is None:
            return
        self._pending = [f for f in self._pending if not f.done() or f.exception()]
        self._pending.append(
            self._pool.submit(compress_shard, path, self.compress_level)
        )

    def compaction_errors(self) -> List[BaseException]:
        """Exceptions raised by finished compaction jobs, drained."""
        errs: List[BaseException] = []
        still: List[Future] = []
        for fut in self._pending:
            if not fut.done():
                still.append(fut)
                continue
            exc = fut.exception()
            if exc is not None:
                errs.append(exc)
        self._pending = still
        return errs

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
            # The period just closed for this (stream, symbol): compact it.
            self._queue_compaction(self.shard_path(stream, symbol, cached_day))
        path = self.shard_path(stream, symbol, day)
        path.parent.mkdir(parents=True, exist_ok=True)
        fh = open(path, "a", encoding="utf-8", newline="\n")
        self._files[key] = (day, fh)
        return fh

    # -- writing -----------------------------------------------------------

    def write_frame(
        self,
        stream: str,
        symbol: str,
        raw: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Append one verbatim frame. Returns the envelope sequence number.

        `seq` is per-process and strictly increasing in *receive order*. Kraken
        book updates carry no sequence numbers and the venue requires that
        "updates should always be processed in sequence", so receive order is
        the only ordering a consumer can reconstruct — it must be recorded
        explicitly rather than inferred from line position, which shard
        rotation and per-symbol splitting would otherwise scramble.

        `extra` inserts additional envelope fields and exists solely so
        snapshot-cadence mode can mark a frame as synthesised (see
        `book_state.py`). When it is None — which is every frame in the default
        delta mode — the emitted line is byte-for-byte what this writer produced
        before the option existed. That identity is asserted by
        `tests/test_cadence_modes.py`; the default path must not acquire fields.
        """
        now = datetime.now(timezone.utc)
        day = self.period_key(now)
        self._seq += 1
        text = raw.strip()

        head = '{"recv_ts":"%s","mono":%.6f,"run_id":"%s","seq":%d,' % (
            now.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
            time.monotonic() - self._t0,
            self.run_id,
            self._seq,
        )
        if extra:
            head += (
                json.dumps(extra, separators=(",", ":"), sort_keys=False)[1:-1] + ","
            )
        if "\n" in text or "\r" in text:
            line = head + '"raw_is_string":true,"raw":' + json.dumps(text) + "}"
        else:
            line = head + '"raw":' + text + "}"

        fh = self._handle(stream, symbol, day)
        fh.write(line + "\n")
        fh.flush()
        self._counts[symbol] = self._counts.get(symbol, 0) + 1
        self._bytes += len(line.encode("utf-8")) + 1

        if time.monotonic() - self._last_fsync >= self.fsync_interval_s:
            self.sync()
        return self._seq

    def drain_counts(self) -> Dict[str, int]:
        """Frame counts per symbol since the last call; resets the tally."""
        counts = self._counts
        self._counts = {}
        return counts

    def drain_bytes(self) -> int:
        """Bytes written since the last call; resets the tally."""
        n = self._bytes
        self._bytes = 0
        return n

    def current_shards(self) -> Dict[Tuple[str, str], Path]:
        day = self.period_key()
        return {key: self.shard_path(key[0], key[1], day) for key in self._files}

    def sync(self) -> None:
        for _day, fh in self._files.values():
            fh.flush()
            os.fsync(fh.fileno())
        self._last_fsync = time.monotonic()

    def close(self) -> None:
        """
        Close every open shard and drain compaction.

        The current period's shards are deliberately NOT compacted here — see
        ROLL PERIOD in the module docstring. Pending jobs from earlier rolls are
        waited on so the process does not exit mid-compression and leave a
        `.part` behind for `sweep()` to clean up.
        """
        for _day, fh in self._files.values():
            try:
                fh.flush()
                os.fsync(fh.fileno())
            finally:
                fh.close()
        self._files.clear()
        if self._pool is not None:
            self._pool.shutdown(wait=True)
            self._pool = None


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

    Transparently reads `.ndjson` and compacted `.ndjson.zst`, and accepts
    either path spelling for the same shard, so a consumer never has to know
    whether compaction has caught up with the hour it is asking for.
    """
    p = Path(path)
    if not p.exists():
        alt = Path(str(p) + ".zst") if p.suffix == ".ndjson" else None
        if alt is not None and alt.exists():
            p = alt
        elif p.suffixes[-2:] == [".ndjson", ".zst"]:
            raw = Path(str(p)[: -len(".zst")])
            if not raw.exists():
                return
            p = raw
        else:
            return
    if p.suffix == ".zst":
        import zstandard as zstd  # local: only compacted reads need it

        with open(p, "rb") as fh:
            with zstd.ZstdDecompressor().stream_reader(fh) as reader:
                for line in io.TextIOWrapper(reader, encoding="utf-8"):
                    line = line.strip()
                    if not line:
                        continue
                    yield json.loads(line)
        return
    with open(p, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
