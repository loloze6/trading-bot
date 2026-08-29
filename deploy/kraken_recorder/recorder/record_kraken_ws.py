"""
Kraken WS v2 forward recorder — minimal viable daemon.
======================================================

Captures, verbatim, from `wss://ws.kraken.com/v2`:
  * `book`  depth 10, snapshot on subscribe, for all 19 breadth pairs
  * `trade` full public trade feed, same 19 pairs
  * `instrument` snapshot (price/qty precision) — see WHY below
  * `status` and `heartbeat`, which arrive unsolicited on any subscription

19 symbols x 2 channels is one connection with ~90% headroom against the
documented 200-symbol limit, so there is no sharding logic here.

WHY `instrument` IS SUBSCRIBED
------------------------------
The build spec defers live CRC32 verification (§5.3) on the grounds that
"checksums are captured verbatim, so this is recoverable as a replay pass".
That claim is only true if the replay can also recover each pair's
`price_precision` / `qty_precision` — the checksum's padding rule is
uncomputable without them, and book frames do not carry them. They live on the
public `instrument` channel. One extra subscription, one snapshot, a few KB;
without it the deferral would be a quiet one-way door rather than a deferral.
This is an addition to the spec's channel list and is called out as such.

OUTPUT OWNERSHIP
----------------
Output lands under `--out` (default: `data/kraken_ws_v2` inside this bundle).
This daemon reads no historical data of any kind — everything it writes is
newly captured from here forward. See README.md for what to do with the
output once it exists; it is not this process's job to analyze it.

DISK FLOOR
----------
A free-space floor is enforced by this process, on a timer, for the whole run —
see `disk_guard.py`. A breach flushes, writes `DISK_GUARD_ABORT` to the
coverage journal and exits `EXIT_DISK_GUARD_ABORT`, which `supervise.sh` reads
as "do not relaunch". Every other non-zero exit is relaunched.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    import websockets
except ImportError:  # pragma: no cover - operator-facing
    sys.exit(
        "websockets is not installed. Run:  python -m pip install -r requirements.txt"
    )

if __package__ in (None, ""):  # allow `python record_kraken_ws.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.book_state import BookBook  # type: ignore
    from recorder.compaction import DEFAULT_LEVEL, sweep  # type: ignore
    from recorder.disk_guard import (  # type: ignore
        DEFAULT_CHECK_INTERVAL_S,
        DEFAULT_MIN_FREE_GB,
        EXIT_DISK_GUARD_ABORT,
        DiskGuard,
        GB,
    )
    from recorder.journal import CoverageJournal  # type: ignore
    from recorder.shard_writer import ShardWriter, disk_symbol  # type: ignore
else:
    from .book_state import BookBook
    from .compaction import DEFAULT_LEVEL, sweep
    from .disk_guard import (
        DEFAULT_CHECK_INTERVAL_S,
        DEFAULT_MIN_FREE_GB,
        EXIT_DISK_GUARD_ABORT,
        DiskGuard,
        GB,
    )
    from .journal import CoverageJournal
    from .shard_writer import ShardWriter, disk_symbol

#: Operational log. Low volume by design: boot, subscription, one heartbeat per
#: rollup (1/min), guard state changes, disconnects, stop. The JOURNAL remains
#: the record of coverage — this exists so that `recorder.log` stops being
#: 0 bytes and an operator can see the process is alive without running a
#: separate check. Judging health by this log alone is still wrong; run
#: `python -m recorder.liveness` — see README.md "Is it working?".
log = logging.getLogger("recorder")

WS_URL = "wss://ws.kraken.com/v2"

#: The 19 pairs this recorder captures.
#: Quote is USD, not USDT — a documented venue divergence, not a typo. WS v2 uses
#: 'BTC/USD', not the legacy 'XBT' spelling.
BREADTH_BASES = [
    "BTC",
    "ETH",
    "XRP",
    "SOL",
    "ADA",
    "SUI",
    "ZEC",
    "DOGE",
    "XMR",
    "LTC",
    "ONDO",
    "NEAR",
    "LINK",
    "TAO",
    "AVAX",
    "TRX",
    "AAVE",
    "INJ",
    "UNI",
]
SYMBOLS = [f"{b}/USD" for b in BREADTH_BASES]

BOOK_DEPTH = 10
#: Heartbeat is ~1/s whenever nothing else is flowing, so any silence this long
#: across ALL channels means the socket is dead, not that the market is quiet.
#: Without this watchdog a half-open TCP socket yields a multi-hour hole with no
#: error anywhere — the exact defect `FetchGapError` was written to forbid.
HEARTBEAT_TIMEOUT_S = 10.0
ROLLUP_INTERVAL_S = 60.0
#: Kraken guidance: instant retry a handful of times on a random drop, then no
#: faster than once per 5s. Cloudflare bans ~150 connect attempts / 10 min / IP.
INSTANT_RETRIES = 3
BACKOFF_S = 5.0

#: bundle_root/data/kraken_ws_v2 — self-contained; nothing outside this bundle
#: is assumed to exist. Override with --out.
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "data" / "kraken_ws_v2"

#: Channel -> shard stream directory. Everything not listed is control traffic.
STREAM_FOR_CHANNEL = {"book": "book_d10", "trade": "trades"}
META_STREAM = "meta"
META_SYMBOL = "_session"

#: Book capture cadence. DELTA is the default and must stay the default: it is
#: the only lossless option, and SNAPSHOT cannot be converted back into it. See
#: `book_state.py` for exactly what SNAPSHOT discards.
MODE_DELTA = "delta"
MODE_SNAPSHOT = "snapshot"
BOOK_MODES = (MODE_DELTA, MODE_SNAPSHOT)
DEFAULT_SNAPSHOT_INTERVAL_S = 5.0


class Recorder:
    def __init__(
        self,
        out_dir: Path = DEFAULT_OUT,
        symbols: Optional[List[str]] = None,
        depth: int = BOOK_DEPTH,
        book_mode: str = MODE_DELTA,
        snapshot_interval_s: float = DEFAULT_SNAPSHOT_INTERVAL_S,
        roll: str = "hour",
        compress: bool = True,
        compress_level: int = DEFAULT_LEVEL,
        min_free_gb: float = DEFAULT_MIN_FREE_GB,
        disk_check_interval_s: float = DEFAULT_CHECK_INTERVAL_S,
        disk_probe=None,
    ):
        if book_mode not in BOOK_MODES:
            raise ValueError(
                f"book_mode must be one of {BOOK_MODES}, got {book_mode!r}"
            )
        if snapshot_interval_s <= 0:
            raise ValueError("snapshot_interval_s must be > 0")
        if disk_check_interval_s <= 0:
            raise ValueError("disk_check_interval_s must be > 0")
        self.out_dir = Path(out_dir)
        self.symbols = list(symbols or SYMBOLS)
        self.depth = depth
        self.book_mode = book_mode
        self.snapshot_interval_s = float(snapshot_interval_s)
        self.journal = CoverageJournal(self.out_dir)
        self.writer = ShardWriter(
            self.out_dir,
            run_id=self.journal.run_id,
            roll=roll,
            compress=compress,
            compress_level=compress_level,
        )
        self._books = BookBook(depth=depth) if book_mode == MODE_SNAPSHOT else None
        self._stop = asyncio.Event()
        self._last_frame_mono = time.monotonic()
        self._heartbeats = 0
        self._book_frames_folded = 0
        self._connection_id: Optional[Any] = None
        self.disk_check_interval_s = float(disk_check_interval_s)
        self.guard = DiskGuard(
            self.out_dir,
            min_free_gb=min_free_gb,
            **({"probe": disk_probe} if disk_probe is not None else {}),
        )
        #: True once the floor has been breached and attested. It is one-way:
        #: the guard never re-arms, because "there was room again a minute
        #: later" is not a reason to resume writing into a volume that already
        #: crossed the floor once.
        self._guard_abort = False
        self._acks = 0
        self._subscription_logged = False

    # -- frame handling ----------------------------------------------------

    def _route(self, msg: Dict[str, Any]) -> List[tuple]:
        """
        (stream, disk_symbol) targets for one frame, from a minimal peek.

        Only `channel` and the symbols inside `data` are read; nothing else is
        interpreted and nothing is rewritten. A frame carrying more than one
        symbol (the venue does not currently emit these on book/trade, but
        nothing documents that it cannot) goes to a `_multi` bucket rather than
        being duplicated or silently dropped — duplication would corrupt frame
        counts, dropping would lose data, and a bucket is visible.
        """
        channel = msg.get("channel")
        stream = STREAM_FOR_CHANNEL.get(channel)
        if stream is None:
            return [(META_STREAM, META_SYMBOL)]
        data = msg.get("data")
        syms: Set[str] = set()
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("symbol"):
                    syms.add(str(item["symbol"]))
        elif isinstance(data, dict) and data.get("symbol"):
            syms.add(str(data["symbol"]))
        if len(syms) == 1:
            return [(stream, disk_symbol(next(iter(syms))))]
        if not syms:
            return [(META_STREAM, META_SYMBOL)]
        return [(stream, "_multi")]

    def _handle(self, raw: str) -> None:
        self._last_frame_mono = time.monotonic()
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            # Unparseable frames are still captured; classification is the only
            # thing lost, and discarding evidence of a venue anomaly would be
            # worse than a misfiled line.
            self.writer.write_frame(META_STREAM, META_SYMBOL, raw)
            return

        if isinstance(msg, dict) and msg.get("channel") == "heartbeat":
            self._heartbeats += 1
            return  # ~1/s x hours; counted in the rollup, not written to disk

        if (
            self._books is not None
            and isinstance(msg, dict)
            and msg.get("channel") == "book"
        ):
            # SNAPSHOT cadence: the delta is folded into the local book and is
            # NOT written. The emitter task writes the book instead. Trades and
            # meta are untouched and stay verbatim in every mode.
            self._books.apply_frame(msg)
            self._book_frames_folded += 1
            return

        for stream, sym in self._route(msg):
            self.writer.write_frame(stream, sym, raw)

        if isinstance(msg, dict) and msg.get("channel") == "status":
            data = msg.get("data") or []
            entry = data[0] if isinstance(data, list) and data else {}
            if isinstance(entry, dict):
                self._connection_id = entry.get("connection_id", self._connection_id)
                self.journal.write(
                    "STATUS_CHANGE",
                    system=entry.get("system"),
                    api_version=entry.get("api_version"),
                    version=entry.get("version"),
                    connection_id=entry.get("connection_id"),
                )

    def _handle_sub_ack(self, msg: Dict[str, Any]) -> None:
        """Journal SUBSCRIBE_ACK per (symbol, channel) — this OPENS coverage."""
        if msg.get("method") != "subscribe":
            return
        result = msg.get("result") or {}
        channel = result.get("channel") or (msg.get("params") or {}).get("channel")
        symbol = result.get("symbol")
        ok = bool(msg.get("success"))
        if not ok:
            self.journal.write(
                "RECONNECT_ATTEMPT",
                attempt=-1,
                backoff_s=0,
                note=f"subscribe FAILED: {msg.get('error')!r} channel={channel} symbol={symbol}",
            )
            return
        if symbol and channel:
            self.journal.write("SUBSCRIBE_ACK", symbol=symbol, channel=channel)
            self._acks += 1
            # book + trade, one ack per (symbol, channel). `instrument` is not
            # per-symbol and does not count towards this.
            expected = len(self.symbols) * 2
            if self._acks >= expected and not self._subscription_logged:
                self._subscription_logged = True
                log.info(
                    "subscription complete: %d/%d (symbol, channel) acks",
                    self._acks,
                    expected,
                )

    # -- disk guard --------------------------------------------------------

    def check_disk(self) -> bool:
        """
        Evaluate the free-space floor. Returns True to keep running.

        On breach the ordering is fixed and is the whole point of doing this
        inside the recorder: **flush and fsync open shards first, then attest,
        then stop**. Attesting before the data is durable would be the journal
        over-claiming coverage it does not have, which `journal.py` calls a
        correctness event as opposed to a data-quality one.
        """
        if self._guard_abort:
            return False
        reading = self.guard.check()
        if reading.ok:
            return True

        try:
            self.writer.sync()
        except OSError as exc:  # a full disk is exactly where fsync fails
            log.error("disk guard: flush failed during abort: %r", exc)
        self.journal.write("DISK_GUARD_ABORT", **reading.as_journal_fields())
        self._guard_abort = True
        log.error(
            "DISK GUARD ABORT: %s — flushed, attested, stopping (exit %d)",
            reading.summary(),
            EXIT_DISK_GUARD_ABORT,
        )
        self._stop.set()
        return False

    async def _disk_guard_loop(self) -> None:
        """
        Re-read free space for the whole life of the process.

        A startup-only check answers the wrong question: the disk is not full
        when a twelve-month capture begins, it becomes full weeks in.
        """
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(
                    self._stop.wait(), timeout=self.disk_check_interval_s
                )
                return
            except asyncio.TimeoutError:
                pass
            self.check_disk()

    # -- tasks -------------------------------------------------------------

    def emit_snapshots(self) -> int:
        """
        Write one synthesised full depth-N book per ready symbol. Returns the
        number written.

        Called on a fixed cadence, including when nothing moved: an interval
        with `updates_applied: 0` is the snapshot-mode statement of
        COVERED-AND-QUIET, and dropping it would make "quiet" and "not captured"
        indistinguishable again — the exact ambiguity `journal.py` exists to
        remove.

        Symbols with no venue snapshot yet are skipped rather than emitted
        empty; an empty book is not a fact about the market.
        """
        if self._books is None:
            return 0
        written = 0
        for symbol in self.symbols:
            st = self._books.state(symbol)
            if not st.ready:
                continue
            payload = st.snapshot_payload(symbol)
            self.writer.write_frame(
                STREAM_FOR_CHANNEL["book"],
                disk_symbol(symbol),
                json.dumps(payload, separators=(",", ":")),
                extra={
                    "synth": "book_snapshot",
                    "interval_s": self.snapshot_interval_s,
                },
            )
            st.mark_emitted()
            written += 1
        return written

    async def _snapshot_loop(self) -> None:
        """Fixed-cadence book emission; inert in delta mode."""
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(
                    self._stop.wait(), timeout=self.snapshot_interval_s
                )
                return
            except asyncio.TimeoutError:
                pass
            self.emit_snapshots()

    async def _rollup_loop(self) -> None:
        """
        One HEARTBEAT_ROLLUP per minute: per-symbol frame counts plus the
        heartbeat tally. This is what makes "covered and quiet" a statement a
        consumer can verify rather than an assumption — a minute inside a
        coverage interval with zero frames but a non-zero heartbeat count is
        attested-quiet; the same minute with zero heartbeats is a dead socket.
        """
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=ROLLUP_INTERVAL_S)
                return
            except asyncio.TimeoutError:
                pass
            counts = self.writer.drain_counts()
            written = self.writer.drain_bytes()
            hb = self._heartbeats
            self._heartbeats = 0
            self.writer.sync()
            extra: Dict[str, Any] = {}
            if self._books is not None:
                # In snapshot mode `frames_total` counts EMITTED books, not
                # venue frames, so the venue-side count is reported separately.
                # Without it a rollup could show healthy frame counts while the
                # socket had gone silent, since emission continues regardless.
                extra["book_mode"] = MODE_SNAPSHOT
                extra["snapshot_interval_s"] = self.snapshot_interval_s
                extra["book_frames_folded"] = self._book_frames_folded
                self._book_frames_folded = 0
            for err in self.writer.compaction_errors():
                # A failed verification leaves the raw shard intact (see
                # compaction.py); it is surfaced, never retried silently.
                self.journal.write(
                    "RECONNECT_ATTEMPT",
                    attempt=-2,
                    backoff_s=0,
                    note=f"COMPACTION FAILED, raw shard retained: {err!r}",
                )
            self.journal.write(
                "HEARTBEAT_ROLLUP",
                window_s=ROLLUP_INTERVAL_S,
                heartbeats=hb,
                frames_total=sum(counts.values()),
                symbols_seen=len([s for s in counts if not s.startswith("_")]),
                frames_by_symbol=counts,
                bytes_written=written,
                **extra,
            )
            free = self.guard.check()
            log.info(
                "heartbeat: frames=%d symbols=%d heartbeats=%d bytes=%d (%.1f kB/s) "
                "free=%s guard=%s",
                sum(counts.values()),
                len([s for s in counts if not s.startswith("_")]),
                hb,
                written,
                written / ROLLUP_INTERVAL_S / 1000.0,
                "unknown" if free.free_gb is None else f"{free.free_gb:.2f}GB",
                "OK" if free.ok else "BREACH",
            )

    async def _session(self) -> None:
        """One connect → subscribe → read-until-death cycle."""
        async with websockets.connect(WS_URL, ping_interval=None, max_size=None) as ws:
            self.journal.write("WS_CONNECT", url=WS_URL)
            self._last_frame_mono = time.monotonic()

            subs = [
                {
                    "method": "subscribe",
                    "params": {
                        "channel": "book",
                        "symbol": self.symbols,
                        "depth": self.depth,
                        "snapshot": True,
                    },
                },
                {
                    "method": "subscribe",
                    "params": {
                        "channel": "trade",
                        "symbol": self.symbols,
                        "snapshot": True,
                    },
                },
                {"method": "subscribe", "params": {"channel": "instrument"}},
            ]
            self.journal.write(
                "RESUBSCRIBE",
                channels=["book", "trade", "instrument"],
                depth=self.depth,
                n_symbols=len(self.symbols),
            )
            for sub in subs:
                await ws.send(json.dumps(sub))
            self._acks = 0
            self._subscription_logged = False
            log.info(
                "ws connected, subscriptions sent: channels=book,trade,instrument "
                "symbols=%d depth=%d",
                len(self.symbols),
                self.depth,
            )

            while not self._stop.is_set():
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=HEARTBEAT_TIMEOUT_S)
                except asyncio.TimeoutError:
                    # Measured, not the configured constant: if the process itself
                    # was suspended (system sleep) rather than merely the socket
                    # going quiet, the real gap since the last frame can be far
                    # longer than HEARTBEAT_TIMEOUT_S, and the journal must attest
                    # what actually happened, not the threshold that triggered it.
                    self.journal.write(
                        "WS_DISCONNECT",
                        code=None,
                        reason="heartbeat_timeout",
                        silent_s=time.monotonic() - self._last_frame_mono,
                        connection_id=self._connection_id,
                    )
                    log.warning(
                        "ws silent for %.0fs — heartbeat watchdog fired",
                        HEARTBEAT_TIMEOUT_S,
                    )
                    await ws.close()
                    return
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                try:
                    peek = json.loads(raw)
                except json.JSONDecodeError:
                    peek = None
                if isinstance(peek, dict) and "method" in peek:
                    self._handle_sub_ack(peek)
                self._handle(raw)

    async def run(self) -> int:
        self.journal.record_start(
            symbols=self.symbols,
            depth=self.depth,
            channels=["book", "trade", "instrument"],
            out_dir=str(self.out_dir),
            book_mode=self.book_mode,
            snapshot_interval_s=(
                self.snapshot_interval_s if self.book_mode == MODE_SNAPSHOT else None
            ),
            roll=self.writer.roll,
            compress=self.writer.compress,
            min_free_gb=self.guard.min_free_bytes / GB,
        )
        boot = self.guard.check()
        log.info(
            "recorder start: out=%s mode=%s%s symbols=%d depth=%d roll=%s compress=%s "
            "floor=%.2fGB %s",
            self.out_dir,
            self.book_mode,
            f" interval={self.snapshot_interval_s}s"
            if self.book_mode == MODE_SNAPSHOT
            else "",
            len(self.symbols),
            self.depth,
            self.writer.roll,
            self.writer.compress,
            self.guard.min_free_bytes / GB,
            boot.summary(),
        )
        # Before the startup sweep, not after: compaction writes a `.part` file
        # the size of an hour of capture, so a boot that is already under the
        # floor must not be allowed to spend more space proving it.
        if not self.check_disk():
            self.writer.close()
            self.journal.close()
            return EXIT_DISK_GUARD_ABORT

        # Pick up shards orphaned by a predecessor that died mid-hour. Done
        # before any capture starts so a verification failure aborts the boot
        # rather than surfacing an hour later.
        if self.writer.compress:
            try:
                made = sweep(
                    self.out_dir,
                    self.writer.open_keys(),
                    level=self.writer.compress_level,
                    roll=self.writer.roll,
                )
                if made:
                    self.journal.write(
                        "RESUBSCRIBE",
                        channels=[],
                        depth=self.depth,
                        n_symbols=0,
                        note=f"startup compaction swept {len(made)} orphaned shard(s)",
                    )
            except Exception as exc:  # noqa: BLE001 - surfaced, never swallowed
                self.journal.write(
                    "RECONNECT_ATTEMPT",
                    attempt=-2,
                    backoff_s=0,
                    note=f"STARTUP COMPACTION FAILED, raw retained: {exc!r}",
                )
                raise
        attempt = 0
        tasks: List[asyncio.Task] = []
        try:
            rollup = asyncio.create_task(self._rollup_loop())
            tasks.append(rollup)
            tasks.append(asyncio.create_task(self._disk_guard_loop()))
            if self.book_mode == MODE_SNAPSHOT:
                tasks.append(asyncio.create_task(self._snapshot_loop()))
            while not self._stop.is_set():
                try:
                    await self._session()
                    if self._stop.is_set():
                        break
                except Exception as exc:  # noqa: BLE001 - any failure is a gap
                    self.journal.write(
                        "WS_DISCONNECT",
                        code=getattr(exc, "code", None),
                        reason=f"{type(exc).__name__}: {exc}",
                        connection_id=self._connection_id,
                    )
                    log.warning("ws disconnect: %s: %s", type(exc).__name__, exc)
                if self._stop.is_set():
                    break
                attempt += 1
                backoff = 0.0 if attempt <= INSTANT_RETRIES else BACKOFF_S
                self.journal.write(
                    "RECONNECT_ATTEMPT", attempt=attempt, backoff_s=backoff
                )
                log.info("reconnect attempt %d in %.0fs", attempt, backoff)
                if backoff:
                    try:
                        await asyncio.wait_for(self._stop.wait(), timeout=backoff)
                    except asyncio.TimeoutError:
                        pass
            for task in tasks:
                task.cancel()
        finally:
            # A guard abort already wrote its own terminal, interval-closing
            # record. Adding RECORDER_STOP on top would make the journal end in
            # a record that reads as a clean operator stop, which is precisely
            # the distinction the supervisor and the gap report depend on.
            if not self._guard_abort:
                self.journal.write("RECORDER_STOP", reason="signal_or_eof")
                log.info("recorder stop: clean")
            self.writer.close()
            for err in self.writer.compaction_errors():
                self.journal.write(
                    "RECONNECT_ATTEMPT",
                    attempt=-2,
                    backoff_s=0,
                    note=f"COMPACTION FAILED, raw shard retained: {err!r}",
                )
            self.journal.close()
        return EXIT_DISK_GUARD_ABORT if self._guard_abort else 0

    def request_stop(self) -> None:
        self._stop.set()


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------


async def selftest(timeout_s: float = 30.0, symbols: Optional[List[str]] = None) -> int:
    """
    Connect, subscribe, and require >=1 book snapshot **per symbol** inside
    `timeout_s`. Exit non-zero otherwise.

    Run before trusting any deploy. This is the one check that fails loudly on
    a symbol the venue silently does not serve — a case that would otherwise
    show up months later as an 18-of-19 panel with no error anywhere.
    """
    syms = list(symbols or SYMBOLS)
    seen: Set[str] = set()
    deadline = time.monotonic() + timeout_s
    try:
        async with websockets.connect(WS_URL, ping_interval=None, max_size=None) as ws:
            await ws.send(
                json.dumps(
                    {
                        "method": "subscribe",
                        "params": {
                            "channel": "book",
                            "symbol": syms,
                            "depth": BOOK_DEPTH,
                            "snapshot": True,
                        },
                    }
                )
            )
            while time.monotonic() < deadline and len(seen) < len(syms):
                try:
                    raw = await asyncio.wait_for(
                        ws.recv(), timeout=max(0.1, deadline - time.monotonic())
                    )
                except asyncio.TimeoutError:
                    break
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if msg.get("channel") == "book" and msg.get("type") == "snapshot":
                    for item in msg.get("data") or []:
                        if isinstance(item, dict) and item.get("symbol"):
                            seen.add(item["symbol"])
    except Exception as exc:  # noqa: BLE001
        print(f"SELFTEST FAIL: connection error: {type(exc).__name__}: {exc}")
        return 2

    missing = sorted(set(syms) - seen)
    print(f"snapshots received: {len(seen)}/{len(syms)}")
    if missing:
        print(f"SELFTEST FAIL: no snapshot within {timeout_s:.0f}s for: {missing}")
        return 1
    print("SELFTEST PASS")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO) -> None:
    """
    stderr always, plus an optional file. UTC timestamps, because every other
    time in this system (journal `ts`, shard names, `recv_ts`) is UTC and a log
    in local time cannot be lined up against any of them.

    Appends a handler set rather than calling basicConfig so that a caller which
    already configured logging is not silently overridden.
    """
    fmt = logging.Formatter(
        "%(asctime)s.%(msecs)03dZ %(levelname)-7s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    fmt.converter = time.gmtime
    log.setLevel(level)
    log.handlers.clear()
    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(fmt)
    log.addHandler(stream)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        log.addHandler(fh)
    log.propagate = False


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Kraken WS v2 forward recorder")
    ap.add_argument("mode", choices=["run", "selftest"])
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    ap.add_argument(
        "--depth", type=int, default=BOOK_DEPTH, choices=[10, 25, 100, 500, 1000]
    )
    ap.add_argument("--timeout", type=float, default=30.0, help="selftest timeout (s)")
    ap.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="run mode: stop after N seconds (0 = forever)",
    )
    ap.add_argument(
        "--book-mode",
        choices=list(BOOK_MODES),
        default=MODE_DELTA,
        help="delta (default, lossless: every book frame verbatim) or snapshot "
        "(lossy: one synthesised full depth book per --snapshot-interval). "
        "SNAPSHOT DISCARDS INTRA-INTERVAL BOOK HISTORY IRRECOVERABLY.",
    )
    ap.add_argument(
        "--snapshot-interval",
        type=float,
        default=DEFAULT_SNAPSHOT_INTERVAL_S,
        help="seconds between synthesised book snapshots (--book-mode snapshot)",
    )
    ap.add_argument(
        "--roll",
        choices=["hour", "day"],
        default="hour",
        help="shard roll period (default hour)",
    )
    ap.add_argument(
        "--no-compress", action="store_true", help="do not zstd-compact closed shards"
    )
    ap.add_argument("--compress-level", type=int, default=DEFAULT_LEVEL)
    ap.add_argument(
        "--min-free-gb",
        type=float,
        default=DEFAULT_MIN_FREE_GB,
        help=f"free-space floor in decimal GB (default {DEFAULT_MIN_FREE_GB}). On "
        f"breach the recorder flushes, writes DISK_GUARD_ABORT to the coverage "
        f"journal and exits {EXIT_DISK_GUARD_ABORT}. Cannot be disabled.",
    )
    ap.add_argument(
        "--disk-check-interval",
        type=float,
        default=DEFAULT_CHECK_INTERVAL_S,
        help=f"seconds between free-space checks while running "
        f"(default {DEFAULT_CHECK_INTERVAL_S})",
    )
    ap.add_argument(
        "--log-file",
        default=None,
        help="append operational logging here as well as stderr",
    )
    args = ap.parse_args(argv)

    setup_logging(args.log_file)

    if args.mode == "selftest":
        return asyncio.run(selftest(args.timeout))

    rec = Recorder(
        out_dir=Path(args.out),
        depth=args.depth,
        book_mode=args.book_mode,
        snapshot_interval_s=args.snapshot_interval,
        roll=args.roll,
        compress=not args.no_compress,
        compress_level=args.compress_level,
        min_free_gb=args.min_free_gb,
        disk_check_interval_s=args.disk_check_interval,
    )

    async def _drive() -> int:
        loop = asyncio.get_running_loop()
        for signame in ("SIGINT", "SIGTERM", "SIGBREAK"):
            sig = getattr(signal, signame, None)
            if sig is None:
                continue
            try:
                loop.add_signal_handler(sig, rec.request_stop)
            except (NotImplementedError, RuntimeError, ValueError):
                # Windows ProactorEventLoop has no add_signal_handler; the
                # KeyboardInterrupt path below covers Ctrl-C there, and the
                # `finally` in run() still journals RECORDER_STOP.
                try:
                    signal.signal(sig, lambda *_: rec.request_stop())
                except (ValueError, OSError):
                    pass
        if args.duration > 0:
            loop.call_later(args.duration, rec.request_stop)
        return await rec.run()

    try:
        return asyncio.run(_drive())
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
