"""
Maintained local depth-N book — the state behind SNAPSHOT cadence mode.
======================================================================

The recorder's default is DELTA mode: every book frame the venue sends is
written verbatim, and the book is never reconstructed. That is the highest
fidelity capture available and it stays the default.

SNAPSHOT mode is a *storage cadence* option: instead of writing every delta, the
recorder applies the deltas to a local book and writes one full depth-N book
every N seconds. This module is that local book.

WHAT IS LOST, STATED PLAINLY
----------------------------
Snapshot mode is lossy and irreversibly so. Between two emissions the book may
have moved many times; only the final state survives. Any question that depends
on intra-interval sequencing — queue position, the order of a cancel relative to
a trade, sub-second book pressure — is unanswerable from snapshot-mode data, and
no later processing can recover it, because the deltas were never written. It
buys storage and nothing else. This is why it is not the default and why the
choice of cadence is an operator decision, not a code default.

WHAT IS PRESERVED
-----------------
Two things, deliberately:

1. **Verbatim decimal strings.** Price and qty are kept as the exact text the
   venue sent (dict keys are the raw price strings). They are never routed
   through `float`. `kraken_crc.render_token` depends on the venue's own decimal
   rendering — a `0.12340` rewritten as `0.1234` breaks the checksum's
   precision-padding rule — so a reconstruction that normalised them would
   silently destroy verifiability. See `shard_writer.py`'s splicing rationale;
   the same constraint applies to a synthesised frame.

2. **Checksum verifiability.** An emitted snapshot carries the `checksum` and
   `timestamp` of the LAST venue frame applied to it. Because emission happens
   between applications, never during one, the emitted book is exactly the book
   that checksum covers, so `kraken_crc.verify_book_frame` verifies a
   synthesised snapshot just as it verifies a venue one. A snapshot-mode capture
   is therefore still checkable against the venue's own CRC32 — it is lossy in
   time, not unverified.

SYNTHESISED FRAMES ARE MARKED AS SUCH
-------------------------------------
Every emitted frame carries `"synthetic":true` in the payload and `"synth"` in
the envelope. A capture is a claim about what the venue sent; a reconstruction
that is indistinguishable from a verbatim frame would corrupt that claim for
every future consumer. Nothing here is written into a shard without the mark.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Mapping, Optional, Sequence


def _price_key(entry: Mapping[str, Any]) -> str:
    """The venue's price rendering, verbatim, used as the level key."""
    return str(entry["price"])


def _is_zero(qty: Any) -> bool:
    try:
        return Decimal(str(qty)) == 0
    except Exception:  # noqa: BLE001 - an unparseable qty is not a deletion
        return False


class BookState:
    """
    One symbol's local depth-N book.

    Levels are `{price_text: qty_text}`. Ordering is re-derived from
    `Decimal(price)` on every emission rather than maintained incrementally:
    the venue's own ordering is the thing a desync corrupts, so deriving it is
    the point (same argument as `kraken_crc.checksum_payload`).
    """

    __slots__ = ("depth", "bids", "asks", "checksum", "timestamp",
                 "applied", "applied_since_emit", "have_snapshot")

    def __init__(self, depth: int = 10):
        self.depth = depth
        self.bids: Dict[str, Any] = {}
        self.asks: Dict[str, Any] = {}
        self.checksum: Optional[int] = None
        self.timestamp: Optional[str] = None
        self.applied = 0
        self.applied_since_emit = 0
        self.have_snapshot = False

    # -- mutation ----------------------------------------------------------

    def apply(self, entry: Mapping[str, Any], frame_type: str) -> None:
        """
        Apply one `data[]` item from a book frame.

        `snapshot` replaces both sides outright; `update` merges, treating
        `qty == 0` as a deletion (the venue's documented removal encoding).
        Both sides are then truncated to `depth` best levels — a depth-N
        subscription is a window, and a level pushed out of that window is gone
        whether or not the venue also sent an explicit removal for it.
        """
        if frame_type == "snapshot":
            self.bids = {}
            self.asks = {}
            self.have_snapshot = True
        for side_name, side in (("bids", self.bids), ("asks", self.asks)):
            for lvl in entry.get(side_name) or []:
                if not isinstance(lvl, Mapping) or "price" not in lvl:
                    continue
                key = _price_key(lvl)
                qty = lvl.get("qty")
                if frame_type != "snapshot" and _is_zero(qty):
                    side.pop(key, None)
                else:
                    side[key] = qty
        self._truncate()
        if "checksum" in entry:
            try:
                self.checksum = int(entry["checksum"]) & 0xFFFFFFFF
            except (TypeError, ValueError):
                self.checksum = None
        self.timestamp = entry.get("timestamp", self.timestamp)
        self.applied += 1
        self.applied_since_emit += 1

    def _truncate(self) -> None:
        if len(self.bids) > self.depth:
            keep = self._sorted(self.bids, reverse=True)[: self.depth]
            self.bids = {k: self.bids[k] for k in keep}
        if len(self.asks) > self.depth:
            keep = self._sorted(self.asks, reverse=False)[: self.depth]
            self.asks = {k: self.asks[k] for k in keep}

    @staticmethod
    def _sorted(side: Dict[str, Any], reverse: bool) -> List[str]:
        return sorted(side, key=lambda p: Decimal(p), reverse=reverse)

    # -- emission ----------------------------------------------------------

    def levels(self) -> Dict[str, List[Dict[str, Any]]]:
        """Top-`depth` levels per side: bids price-descending, asks ascending."""
        return {
            "bids": [
                {"price": p, "qty": self.bids[p]}
                for p in self._sorted(self.bids, reverse=True)[: self.depth]
            ],
            "asks": [
                {"price": p, "qty": self.asks[p]}
                for p in self._sorted(self.asks, reverse=False)[: self.depth]
            ],
        }

    def snapshot_payload(self, symbol: str) -> Dict[str, Any]:
        """
        A full depth-N book as a Kraken-v2-shaped `book`/`snapshot` frame,
        marked `synthetic` and carrying the provenance a consumer needs to
        judge it.

        `updates_applied` is the count of venue frames folded in since the last
        emission. Zero means the book genuinely did not move in that interval —
        the snapshot-mode analogue of COVERED-AND-QUIET, and the reason the
        emitter writes a frame every interval rather than only on change.
        """
        payload = {
            "channel": "book",
            "type": "snapshot",
            "synthetic": True,
            "data": [
                {
                    "symbol": symbol,
                    **self.levels(),
                    "checksum": self.checksum,
                    "timestamp": self.timestamp,
                    "updates_applied": self.applied_since_emit,
                }
            ],
        }
        return payload

    def mark_emitted(self) -> None:
        self.applied_since_emit = 0

    @property
    def ready(self) -> bool:
        """True once a venue snapshot has established the book."""
        return self.have_snapshot and bool(self.bids) and bool(self.asks)


class BookBook:
    """All symbols' `BookState`, keyed by the venue symbol (`BTC/USD`)."""

    def __init__(self, depth: int = 10):
        self.depth = depth
        self._states: Dict[str, BookState] = {}

    def state(self, symbol: str) -> BookState:
        st = self._states.get(symbol)
        if st is None:
            st = BookState(depth=self.depth)
            self._states[symbol] = st
        return st

    def apply_frame(self, msg: Mapping[str, Any]) -> List[str]:
        """Apply a whole book frame; returns the symbols it touched."""
        ftype = str(msg.get("type") or "update")
        data = msg.get("data")
        items: Sequence[Any] = data if isinstance(data, list) else []
        touched: List[str] = []
        for item in items:
            if not isinstance(item, Mapping):
                continue
            sym = item.get("symbol")
            if not sym:
                continue
            self.state(str(sym)).apply(item, ftype)
            touched.append(str(sym))
        return touched

    def ready_symbols(self) -> List[str]:
        return [s for s, st in self._states.items() if st.ready]
