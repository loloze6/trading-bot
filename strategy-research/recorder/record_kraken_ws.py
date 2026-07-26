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

DATA IS RESERVED
----------------
Output lands in `trading-bot/local_data/recorded_reserved/`, excluded from
publication by `.gitignore`'s `trading-bot/local_data/*/`. No stage, prescreen
or diagnostic may read any window of it until an explicit, separately-committed
designation releases it. It is the only renewable source of genuinely unseen
out-of-sample this campaign has; spending it by accident is irreversible.

HOLDOUT
-------
Capture begins 2026-07-26, strictly after `holdout_range` end 2026-06-30. No
overlap, no seal interaction. This daemon reads no historical data of any kind.
"""

from __future__ import annotations

import argparse
import asyncio
import json
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
        "websockets is not installed. Run:  python -m pip install websockets\n"
        "(pinned in strategy-research/recorder/requirements.txt)"
    )

if __package__ in (None, ""):  # allow `python record_kraken_ws.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.journal import CoverageJournal  # type: ignore
    from recorder.shard_writer import ShardWriter, disk_symbol  # type: ignore
else:
    from .journal import CoverageJournal
    from .shard_writer import ShardWriter, disk_symbol

WS_URL = "wss://ws.kraken.com/v2"

#: The 19 Kraken breadth bases (campaign_data_policy.yaml:kraken_breadth_19pair).
#: Quote is USD, not USDT — a documented venue divergence, not a typo. WS v2 uses
#: 'BTC/USD', not the legacy 'XBT' spelling.
BREADTH_BASES = [
    "BTC", "ETH", "XRP", "SOL", "ADA", "SUI", "ZEC", "DOGE", "XMR", "LTC",
    "ONDO", "NEAR", "LINK", "TAO", "AVAX", "TRX", "AAVE", "INJ", "UNI",
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

DEFAULT_OUT = (
    Path(__file__).resolve().parents[2]
    / "trading-bot" / "local_data" / "recorded_reserved" / "kraken_ws_v2"
)

#: Channel -> shard stream directory. Everything not listed is control traffic.
STREAM_FOR_CHANNEL = {"book": "book_d10", "trade": "trades"}
META_STREAM = "meta"
META_SYMBOL = "_session"


class Recorder:
    def __init__(
        self,
        out_dir: Path = DEFAULT_OUT,
        symbols: Optional[List[str]] = None,
        depth: int = BOOK_DEPTH,
    ):
        self.out_dir = Path(out_dir)
        self.symbols = list(symbols or SYMBOLS)
        self.depth = depth
        self.journal = CoverageJournal(self.out_dir)
        self.writer = ShardWriter(self.out_dir, run_id=self.journal.run_id)
        self._stop = asyncio.Event()
        self._last_frame_mono = time.monotonic()
        self._heartbeats = 0
        self._connection_id: Optional[Any] = None

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

    # -- tasks -------------------------------------------------------------

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
            hb = self._heartbeats
            self._heartbeats = 0
            self.writer.sync()
            self.journal.write(
                "HEARTBEAT_ROLLUP",
                window_s=ROLLUP_INTERVAL_S,
                heartbeats=hb,
                frames_total=sum(counts.values()),
                symbols_seen=len([s for s in counts if not s.startswith("_")]),
                frames_by_symbol=counts,
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

            while not self._stop.is_set():
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=HEARTBEAT_TIMEOUT_S)
                except asyncio.TimeoutError:
                    self.journal.write(
                        "WS_DISCONNECT",
                        code=None,
                        reason="heartbeat_timeout",
                        silent_s=HEARTBEAT_TIMEOUT_S,
                        connection_id=self._connection_id,
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
        )
        attempt = 0
        try:
            rollup = asyncio.create_task(self._rollup_loop())
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
                if self._stop.is_set():
                    break
                attempt += 1
                backoff = 0.0 if attempt <= INSTANT_RETRIES else BACKOFF_S
                self.journal.write(
                    "RECONNECT_ATTEMPT", attempt=attempt, backoff_s=backoff
                )
                if backoff:
                    try:
                        await asyncio.wait_for(self._stop.wait(), timeout=backoff)
                    except asyncio.TimeoutError:
                        pass
            rollup.cancel()
        finally:
            self.journal.write("RECORDER_STOP", reason="signal_or_eof")
            self.writer.close()
            self.journal.close()
        return 0

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
            await ws.send(json.dumps({
                "method": "subscribe",
                "params": {"channel": "book", "symbol": syms,
                           "depth": BOOK_DEPTH, "snapshot": True},
            }))
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


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Kraken WS v2 forward recorder")
    ap.add_argument("mode", choices=["run", "selftest"])
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    ap.add_argument("--depth", type=int, default=BOOK_DEPTH, choices=[10, 25, 100, 500, 1000])
    ap.add_argument("--timeout", type=float, default=30.0, help="selftest timeout (s)")
    ap.add_argument("--duration", type=float, default=0.0,
                    help="run mode: stop after N seconds (0 = forever)")
    args = ap.parse_args(argv)

    if args.mode == "selftest":
        return asyncio.run(selftest(args.timeout))

    rec = Recorder(out_dir=Path(args.out), depth=args.depth)

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
