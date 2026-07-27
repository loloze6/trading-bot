"""
Shard reader — the read side of the forward recorder.
=====================================================

`shard_writer.py` puts frames on disk verbatim. This module is the only
supported way to get them back off, in timestamp order, across pairs, with the
coverage journal read ALONGSIDE rather than after the fact.

THREE PROPERTIES, EACH LOAD-BEARING
-----------------------------------

**1. Gaps are EXPOSED, never interpolated.**
    A recorded stream has no sequence numbers on the book channel
    (`journal.py`), so an absence of frames is ambiguous between "quiet market"
    and "not captured". The journal manufactures that distinction, and this
    reader refuses to hide it: :meth:`ShardReader.read` interleaves :class:`Gap`
    objects INTO the record stream, in timestamp order, at the position where
    the uncaptured span falls. A consumer iterating the stream cannot fail to
    see one — it does not have to remember to ask.

    This is deliberately different from `journal.assert_covered()`, which
    RAISES. Both exist because they answer different questions. `assert_covered`
    is for a consumer that requires a fully-attested window and should refuse to
    run otherwise. The inline :class:`Gap` is for a consumer — like the whale
    features — that legitimately computes over a partially-covered span and must
    MARK the affected outputs rather than emit them as if they were clean. What
    neither offers is the third option of quietly bridging the gap.

    `emit_gaps=False` exists, but it is not a way to make gaps go away: it is
    for a caller that has already called `assert_covered` and proven there are
    none. It is not the default.

**2. A truncated final shard is normal, not an error.**
    The recorder is always mid-write. The newest shard's last line is routinely
    a partial JSON object, and a reader that treated that as corruption would be
    unusable against live capture. So: an unparseable line that is the LAST
    line of a file is tolerated and RECORDED (:attr:`ShardReader.truncations`);
    an unparseable line with data after it is a real corruption and raises. Same
    treatment `journal.read_tail_state` gives its own torn tail — reported, not
    repaired, because it is evidence.

**3. Deny by default on record shape.**
    An unrecognised record shape RAISES :class:`ShardReadError`. It is never
    skipped. A reader that skips what it does not understand silently narrows
    the dataset every time the venue adds a field or the writer changes, and
    reports success while doing it — the `FetchGapError` failure shape
    (`base_fetcher.py:42-61`) in a new costume.

READ ORDER
----------
Records are ordered by `recv_ts`, the recorder's own receive clock. That is the
only clock common to every pair, and it is the one the writer's `seq` counter
agrees with. Venue event time (`raw.data[].timestamp`) is the right clock for
ECONOMICS and is what :func:`iter_trades` bins on — but it is per-pair, is set
by the venue, and cannot order two pairs' frames against each other.

RESERVED DATA
-------------
Everything under `local_data/recorded_reserved/` is deny-by-default
(`campaign_data_policy.yaml:kraken_ws_forward_recorder`, status
`configured_reserved_undesignated`). This module is a mechanism, not a licence:
it will happily read a path you hand it, and the gate that keeps that data out
of a backtest lives at the consumer boundary — see
`trading-bot/data/fetchers/whale_footprint_fetcher.py`, which refuses to serve
an undesignated window.
"""

from __future__ import annotations

import heapq
import io
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple, Union

if __package__ in (None, ""):  # allow direct execution
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.journal import (  # type: ignore
        JOURNAL_FILENAME,
        Interval,
        coverage_intervals,
        load_records,
        parse_iso,
        uncovered,
    )
else:
    from .journal import (
        JOURNAL_FILENAME,
        Interval,
        coverage_intervals,
        load_records,
        parse_iso,
        uncovered,
    )

#: On-disk stream directory -> the venue channel names legitimately found in it.
#: Deny by default: a frame whose `raw.channel` is not listed for the stream it
#: was read from raises rather than being skipped.
STREAM_CHANNELS: Dict[str, Set[str]] = {
    "book_d10": {"book"},
    "trades": {"trade"},
    "meta": {"status", "instrument", "heartbeat"},
}

#: Kraken WS v2 payload types. `snapshot` is the initial (or post-resubscribe)
#: full state; `update` is incremental.
MESSAGE_TYPES: Set[str] = {"snapshot", "update"}

#: Envelope fields `shard_writer.write_frame` always emits.
_REQUIRED_ENVELOPE_FIELDS = ("recv_ts", "mono", "run_id", "seq", "raw")

#: Envelope fields `write_frame(extra=...)` may add. `synth` is set by
#: snapshot-cadence mode (`record_kraken_ws.py:365`) to mark a book frame the
#: recorder synthesised rather than received. Anything NOT in this set is an
#: unrecognised shape and raises.
_OPTIONAL_ENVELOPE_FIELDS = frozenset({"raw_is_string", "synth"})

#: Trade payload keys required by :func:`iter_trades`. Kraken WS v2 `trade`.
_REQUIRED_TRADE_FIELDS = ("symbol", "side", "price", "qty", "ord_type", "trade_id", "timestamp")

#: Taker side as published by the venue. `side` is the AGGRESSOR's side: `buy`
#: means a taker lifted the offer. This is what makes signed volume meaningful;
#: a maker-side convention would invert every sign in `whale_features`.
TAKER_SIDES = {"buy": 1, "sell": -1}


class ShardReadError(RuntimeError):
    """
    Raised on a record whose shape this reader does not recognise.

    Deliberately NOT a skip. See property 3 in the module docstring: a reader
    that drops what it cannot parse under-reports the dataset and announces
    success while doing so.
    """


def disk_symbol(ws_symbol: str) -> str:
    """Venue `BTC/USD` -> on-disk `BTCUSD`. Mirrors `shard_writer.disk_symbol`."""
    return ws_symbol.replace("/", "").upper()


def ws_symbol(disk: str, quote: str = "USD") -> str:
    """On-disk `BTCUSD` -> venue `BTC/USD`, the spelling the journal records."""
    d = disk.upper()
    if d.endswith(quote) and len(d) > len(quote):
        return f"{d[: -len(quote)]}/{quote}"
    return d


@dataclass(frozen=True)
class Envelope:
    """One recorded frame: the writer's envelope plus its verbatim payload."""

    recv_ts: datetime
    mono: float
    run_id: str
    seq: int
    stream: str
    symbol: str  # on-disk spelling, e.g. 'BTCUSD'
    channel: str  # 'book' | 'trade' | 'status' | 'instrument' | 'heartbeat'
    msg_type: str  # 'snapshot' | 'update'
    data: List[Dict[str, Any]]
    path: Path
    synth: Optional[str] = None  # set by snapshot-cadence mode
    raw_is_string: bool = False

    #: sort key for the cross-pair merge
    @property
    def order_key(self) -> Tuple[datetime, int]:
        return (self.recv_ts, self.seq)


@dataclass(frozen=True)
class Gap:
    """
    An uncaptured span, yielded INLINE in the record stream.

    `start`/`end` bound wall-clock time the coverage journal does not attest for
    this (symbol, channel). A consumer that computes a value spanning a Gap must
    mark that value; it must not emit it as though the span were quiet.
    """

    symbol: str  # on-disk spelling
    channel: str
    start: datetime
    end: datetime
    cause: str  # 'not_yet_started' | 'after_last_attested' | 'between_intervals'

    @property
    def order_key(self) -> Tuple[datetime, int]:
        # -1 sorts a Gap ahead of any Envelope sharing its instant: the gap ends
        # where coverage resumes, so the first covered record belongs after it.
        return (self.start, -1)

    @property
    def duration_s(self) -> float:
        return (self.end - self.start).total_seconds()


@dataclass(frozen=True)
class Trade:
    """One public trade, as published. `side` is the TAKER's side."""

    ts: datetime  # venue event time
    recv_ts: datetime  # recorder receive time
    symbol: str  # on-disk spelling
    price: float
    qty: float
    side: str
    ord_type: str
    trade_id: int
    from_snapshot: bool  # True if it arrived in a `snapshot` payload (backfill)

    @property
    def notional(self) -> float:
        """Quote-currency size. The comparable measure of 'large' across pairs."""
        return self.price * self.qty

    @property
    def sign(self) -> int:
        return TAKER_SIDES[self.side]

    @property
    def signed_notional(self) -> float:
        return self.sign * self.notional


@dataclass(frozen=True)
class Manifest:
    """What is actually on disk under a capture root."""

    root: Path
    journal_path: Path
    files: List[Path]
    total_bytes: int
    streams: Dict[str, List[str]]  # stream -> sorted on-disk symbols
    period_keys: List[str]  # sorted shard period stems, e.g. ['2026-07-26']
    compressed_files: int

    def render(self) -> str:
        lines = [
            f"root            {self.root}",
            f"files           {len(self.files)} ({self.compressed_files} zstd-compacted)",
            f"bytes           {self.total_bytes:,}",
            f"journal         {self.journal_path.name} "
            f"({'present' if self.journal_path.exists() else 'ABSENT'})",
            f"period keys     {self.period_keys[0] if self.period_keys else '-'}"
            f" .. {self.period_keys[-1] if self.period_keys else '-'}",
        ]
        for stream in sorted(self.streams):
            syms = self.streams[stream]
            lines.append(f"  {stream:<10} {len(syms):>3} symbols  {', '.join(syms)}")
        return "\n".join(lines)


class ShardReader:
    """
    Reads a capture root: shards + the coverage journal that makes them
    interpretable.

    The journal is not optional. Without it there is no way to tell an
    uncaptured hour from a quiet one, so a root with no journal is refused
    outright rather than read on a best-effort basis.
    """

    def __init__(self, root: Path, journal_path: Optional[Path] = None):
        self.root = Path(root)
        if not self.root.is_dir():
            raise ShardReadError(f"capture root does not exist: {self.root}")
        self.journal_path = Path(journal_path) if journal_path else self.root / JOURNAL_FILENAME
        if not self.journal_path.exists():
            raise ShardReadError(
                f"no coverage journal at {self.journal_path}. Shards without a journal "
                "cannot distinguish an uncaptured span from a quiet market; refusing "
                "to read them as if they could."
            )
        #: path -> 1-based line number of the tolerated unparseable final line.
        self.truncations: Dict[Path, int] = {}
        self._records: Optional[List[Dict[str, Any]]] = None
        self._coverage: Optional[Dict[Tuple[str, str], List[Interval]]] = None

    # -- journal -----------------------------------------------------------

    def journal_records(self) -> List[Dict[str, Any]]:
        if self._records is None:
            self._records = load_records(self.journal_path)
        return self._records

    def coverage(self) -> Dict[Tuple[str, str], List[Interval]]:
        """Attested spans, keyed by (venue symbol, channel) as the journal spells them."""
        if self._coverage is None:
            self._coverage = coverage_intervals(self.journal_records())
        return self._coverage

    def journal_extent(self) -> Optional[Tuple[datetime, datetime]]:
        """(first, last) journal record timestamps, or None for an empty journal."""
        stamps = [parse_iso(r["ts"]) for r in self.journal_records() if r.get("ts")]
        return (min(stamps), max(stamps)) if stamps else None

    def gaps(
        self, symbol: str, channel: str, start: datetime, end: datetime
    ) -> List[Gap]:
        """
        Uncaptured sub-spans of [start, end] for one (symbol, channel).

        `symbol` is the on-disk spelling; the journal's venue spelling is
        derived. An empty list means fully attested.
        """
        key = (ws_symbol(symbol), channel)
        ivs = self.coverage().get(key, [])
        out: List[Gap] = []
        for gs, ge in uncovered(ivs, start, end):
            if not ivs:
                cause = "not_yet_started"
            elif gs >= max(i.end for i in ivs):
                cause = "after_last_attested"
            elif ge <= min(i.start for i in ivs):
                cause = "not_yet_started"
            else:
                cause = "between_intervals"
            out.append(Gap(symbol=symbol, channel=channel, start=gs, end=ge, cause=cause))
        return out

    # -- manifest ----------------------------------------------------------

    def manifest(self) -> Manifest:
        files = sorted(p for p in self.root.rglob("*") if p.is_file())
        streams: Dict[str, List[str]] = {}
        periods: Set[str] = set()
        for p in files:
            rel = p.relative_to(self.root)
            if len(rel.parts) != 3:
                continue  # the root-level journal, or anything else not a shard
            stream, symbol, name = rel.parts
            streams.setdefault(stream, [])
            if symbol not in streams[stream]:
                streams[stream].append(symbol)
            periods.add(name.split(".")[0])
        for stream in streams:
            streams[stream].sort()
        return Manifest(
            root=self.root,
            journal_path=self.journal_path,
            files=files,
            total_bytes=sum(p.stat().st_size for p in files),
            streams=streams,
            period_keys=sorted(periods),
            compressed_files=sum(1 for p in files if p.suffix == ".zst"),
        )

    def shard_paths(self, stream: str, symbol: str) -> List[Path]:
        """Every shard for one (stream, symbol), in period order.

        Both spellings of the same period (`.ndjson` and `.ndjson.zst`) can
        coexist while a compaction job is in flight; the compacted copy wins,
        because `compaction.compress_shard` only removes the plain file after a
        verified byte-compare.
        """
        d = self.root / stream / symbol
        if not d.is_dir():
            return []
        by_period: Dict[str, Path] = {}
        for p in sorted(d.iterdir()):
            if not p.is_file() or ".ndjson" not in p.name:
                continue
            if p.name.endswith(".part"):
                continue  # an in-flight compaction temp file, not data
            period = p.name.split(".")[0]
            if period in by_period and by_period[period].suffix == ".zst":
                continue
            by_period[period] = p
        return [by_period[k] for k in sorted(by_period)]

    # -- raw line reading --------------------------------------------------

    def _iter_lines(self, path: Path) -> Iterator[Tuple[int, str]]:
        """
        Yield (1-based line number, text) from a `.ndjson` or `.ndjson.zst`
        shard.

        A `.zst` frame whose tail was never flushed raises inside the
        decompressor. That is the compacted spelling of a truncated final shard
        and is treated identically — recorded, not raised — but ONLY once at
        least one line has been read. A file that fails on its very first byte
        is corrupt, not truncated.
        """
        if path.suffix == ".zst":
            import zstandard as zstd  # local: only compacted reads need it

            n = 0
            try:
                with open(path, "rb") as fh:
                    with zstd.ZstdDecompressor().stream_reader(fh) as reader:
                        for line in io.TextIOWrapper(reader, encoding="utf-8"):
                            n += 1
                            yield n, line
            except zstd.ZstdError:
                if n == 0:
                    raise ShardReadError(
                        f"{path}: zstd frame is unreadable from its first byte. "
                        "That is corruption, not the mid-write truncation a live "
                        "recorder produces."
                    )
                self.truncations[path] = n
            return
        with open(path, "r", encoding="utf-8") as fh:
            for n, line in enumerate(fh, start=1):
                yield n, line

    def read_shard(self, path: Path, stream: str, symbol: str) -> Iterator[Envelope]:
        """
        Parse one shard.

        Truncation handling is a one-line lookahead: an unparseable line is held
        back, and only turns into a :class:`ShardReadError` if another line
        follows it. Reaching EOF with a held-back line records a truncation.
        """
        pending: Optional[Tuple[int, str]] = None
        for lineno, text in self._iter_lines(path):
            text = text.strip()
            if not text:
                continue
            if pending is not None:
                raise ShardReadError(
                    f"{path}:{pending[0]}: unparseable line with {lineno - pending[0]} "
                    "or more line(s) of data after it. A torn tail is the last line of "
                    "a shard by definition; this is corruption in the middle of one."
                )
            try:
                rec = json.loads(text)
            except json.JSONDecodeError:
                pending = (lineno, text)
                continue
            yield self._to_envelope(rec, path, stream, symbol, lineno)
        if pending is not None:
            self.truncations[path] = pending[0]

    def _to_envelope(
        self, rec: Any, path: Path, stream: str, symbol: str, lineno: int
    ) -> Envelope:
        where = f"{path}:{lineno}"
        if not isinstance(rec, dict):
            raise ShardReadError(f"{where}: record is {type(rec).__name__}, expected object")
        missing = [k for k in _REQUIRED_ENVELOPE_FIELDS if k not in rec]
        if missing:
            raise ShardReadError(f"{where}: envelope is missing {missing}")
        unknown = set(rec) - set(_REQUIRED_ENVELOPE_FIELDS) - _OPTIONAL_ENVELOPE_FIELDS
        if unknown:
            raise ShardReadError(
                f"{where}: unrecognised envelope field(s) {sorted(unknown)}. Deny by "
                "default: a new field means the writer changed and this reader has "
                "not been taught what it means."
            )

        raw_is_string = bool(rec.get("raw_is_string"))
        raw = rec["raw"]
        if raw_is_string:
            # `shard_writer` sets this only for a frame carrying an embedded
            # newline, which Kraken does not send. Surfaced as an Envelope with
            # no payload so a consumer can see it existed; `iter_trades` refuses
            # to guess at its contents.
            if not isinstance(raw, str):
                raise ShardReadError(f"{where}: raw_is_string set but raw is not a string")
            return Envelope(
                recv_ts=parse_iso(rec["recv_ts"]),
                mono=float(rec["mono"]),
                run_id=str(rec["run_id"]),
                seq=int(rec["seq"]),
                stream=stream,
                symbol=symbol,
                channel="",
                msg_type="",
                data=[],
                path=path,
                synth=rec.get("synth"),
                raw_is_string=True,
            )

        if not isinstance(raw, dict):
            raise ShardReadError(f"{where}: raw is {type(raw).__name__}, expected object")
        channel = raw.get("channel")
        msg_type = raw.get("type")
        data = raw.get("data")
        if not isinstance(channel, str) or not isinstance(msg_type, str):
            raise ShardReadError(f"{where}: raw is missing a string channel/type")
        allowed = STREAM_CHANNELS.get(stream)
        if allowed is None:
            raise ShardReadError(
                f"{where}: stream {stream!r} is not one of {sorted(STREAM_CHANNELS)}"
            )
        if channel not in allowed:
            raise ShardReadError(
                f"{where}: channel {channel!r} in stream {stream!r}, which carries "
                f"{sorted(allowed)}"
            )
        if msg_type not in MESSAGE_TYPES:
            raise ShardReadError(
                f"{where}: message type {msg_type!r} is not one of {sorted(MESSAGE_TYPES)}"
            )
        if not isinstance(data, list):
            raise ShardReadError(f"{where}: raw.data is {type(data).__name__}, expected array")

        return Envelope(
            recv_ts=parse_iso(rec["recv_ts"]),
            mono=float(rec["mono"]),
            run_id=str(rec["run_id"]),
            seq=int(rec["seq"]),
            stream=stream,
            symbol=symbol,
            channel=channel,
            msg_type=msg_type,
            data=data,
            path=path,
            synth=rec.get("synth"),
        )

    # -- ordered reading ---------------------------------------------------

    def read(
        self,
        stream: str,
        symbols: Optional[Sequence[str]] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        emit_gaps: bool = True,
    ) -> Iterator[Union[Envelope, Gap]]:
        """
        Yield every record of `stream` across `symbols`, ordered by `recv_ts`,
        with :class:`Gap` markers interleaved at their position in that order.

        `symbols` defaults to every symbol present for the stream. `start`/`end`
        default to the journal's own extent — coverage is attested only up to
        the newest journal record, never to "now" (`journal.coverage_intervals`,
        OPEN_TAIL), so that is the widest window about which anything can be
        said.

        `emit_gaps=False` suppresses the markers. Use it only after
        `journal.assert_covered()` has proven the window clean; it does not make
        an uncaptured span captured.
        """
        if stream not in STREAM_CHANNELS:
            raise ShardReadError(f"unknown stream {stream!r}")
        man = self.manifest()
        syms = list(symbols) if symbols is not None else man.streams.get(stream, [])
        # Gap markers need a single channel to look coverage up under. `book_d10`
        # and `trades` have one each. `meta` carries three (status, instrument,
        # heartbeat) and the recorder issues SUBSCRIBE_ACK for `book` and `trade`
        # ONLY, so the journal attests no coverage for meta at all — there is
        # nothing to report, which is different from choosing not to report it.
        # A meta consumer that needs coverage must ask about the channel whose
        # subscription actually carried the frame.
        channel = sorted(STREAM_CHANNELS[stream])[0] if len(STREAM_CHANNELS[stream]) == 1 else None

        if start is None or end is None:
            extent = self.journal_extent()
            if extent is None:
                raise ShardReadError("journal is empty: no window to read")
            start = start or extent[0]
            end = end or extent[1]
        if end < start:
            raise ValueError("end precedes start")

        streams_in: List[Iterable[Union[Envelope, Gap]]] = []
        for sym in syms:
            streams_in.append(self._symbol_stream(stream, sym, start, end))
            if emit_gaps and channel is not None:
                streams_in.append(iter(self.gaps(sym, channel, start, end)))

        for item in heapq.merge(*streams_in, key=lambda x: x.order_key):
            yield item

    def _symbol_stream(
        self, stream: str, symbol: str, start: datetime, end: datetime
    ) -> Iterator[Envelope]:
        for path in self.shard_paths(stream, symbol):
            for env in self.read_shard(path, stream, symbol):
                if env.recv_ts < start:
                    continue
                if env.recv_ts > end:
                    return
                yield env

    # -- trades ------------------------------------------------------------

    def iter_trades(
        self,
        symbols: Optional[Sequence[str]] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        emit_gaps: bool = True,
    ) -> Iterator[Union[Trade, Gap]]:
        """
        Yield individual :class:`Trade` objects (and :class:`Gap` markers) from
        the `trades` stream.

        DEDUPLICATION is on (symbol, trade_id) and is not optional. A
        `RESUBSCRIBE` after a reconnect re-delivers a `snapshot` payload whose
        trades overlap what was already captured — the baseline capture contains
        exactly one such record — and counting those twice would inflate every
        volume figure downstream.

        `from_snapshot` is carried through rather than filtered. A snapshot
        payload BACKFILLS trades from before the subscription was acked (the
        baseline capture's BTC/USD snapshot reaches ~53 s back), so those trades
        are real but fall in wall-clock time the journal does NOT attest. That
        is not a reason to drop them; it is a reason the bar they land in gets
        marked, which `whale_features` does off the Gap markers.
        """
        seen: Set[Tuple[str, int]] = set()
        for item in self.read("trades", symbols, start, end, emit_gaps=emit_gaps):
            if isinstance(item, Gap):
                yield item
                continue
            if item.raw_is_string:
                raise ShardReadError(
                    f"{item.path}: trade frame stored as raw_is_string (seq={item.seq}). "
                    "Its payload was not round-trippable through the envelope and this "
                    "reader will not guess at it."
                )
            for entry in item.data:
                trade = self._to_trade(entry, item)
                key = (trade.symbol, trade.trade_id)
                if key in seen:
                    continue
                seen.add(key)
                yield trade

    @staticmethod
    def _to_trade(entry: Any, env: Envelope) -> Trade:
        where = f"{env.path} seq={env.seq}"
        if not isinstance(entry, dict):
            raise ShardReadError(f"{where}: trade entry is {type(entry).__name__}")
        missing = [k for k in _REQUIRED_TRADE_FIELDS if k not in entry]
        if missing:
            raise ShardReadError(f"{where}: trade entry is missing {missing}")
        side = entry["side"]
        if side not in TAKER_SIDES:
            raise ShardReadError(
                f"{where}: trade side {side!r} is not one of {sorted(TAKER_SIDES)}"
            )
        try:
            price = float(entry["price"])
            qty = float(entry["qty"])
            trade_id = int(entry["trade_id"])
        except (TypeError, ValueError) as exc:
            raise ShardReadError(f"{where}: non-numeric price/qty/trade_id: {exc}") from exc
        if not (price > 0.0 and qty > 0.0):
            raise ShardReadError(
                f"{where}: trade_id={trade_id} has price={price} qty={qty}; a public "
                "trade with a non-positive price or size is not a shape this reader "
                "will pass on as if it were valid."
            )
        if disk_symbol(entry["symbol"]) != env.symbol:
            raise ShardReadError(
                f"{where}: payload symbol {entry['symbol']!r} does not match the shard "
                f"it was read from ({env.symbol})."
            )
        return Trade(
            ts=parse_iso(entry["timestamp"]),
            recv_ts=env.recv_ts,
            symbol=env.symbol,
            price=price,
            qty=qty,
            side=side,
            ord_type=str(entry["ord_type"]),
            trade_id=trade_id,
            from_snapshot=env.msg_type == "snapshot",
        )


def as_naive_utc(dt: datetime) -> datetime:
    """
    Drop the tzinfo after normalising to UTC.

    The bot's cache convention is naive-UTC and `base_fetcher._load_local`
    RAISES on a tz-aware `timestamp` column (base_fetcher.py:263-269). Every
    timestamp leaving this package for the bot tree passes through here.
    """
    return dt.astimezone(timezone.utc).replace(tzinfo=None)
