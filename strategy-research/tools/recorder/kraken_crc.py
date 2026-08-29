"""
Kraken WS v2 L2 book CRC32 checksum.
====================================

The build spec's case for depth 10 rests on one property: "the CRC32 checksum
covers **exactly the top 10 levels**, so at depth 10 the entire captured book
is checksum-verifiable" (§4). This module is that verifier.

Live verification (maintaining a local book) is deferred out of MVP per §5.3.
What is NOT deferred is *retaining the ability* to verify: the recorder writes
every frame verbatim, so `checksum` survives byte-exact, and this function can
be replayed over the shards at any later date.

VERBATIM CAPTURE IS LOAD-BEARING HERE, and the reason is subtle enough to
state: the checksum is computed over *decimal string* renderings of price and
qty. If the recorder had re-serialised frames through `json.dumps`, a price
that arrived as `0.12340` could be written back as `0.1234`, and the trailing
zero — which the checksum depends on via the precision-padding rule — would be
gone. Splicing the raw frame text (see `shard_writer.py`) preserves it.

The second prerequisite is the per-pair `price_precision` / `qty_precision`,
which the book frames do NOT carry. They come from the public `instrument`
channel, which the recorder subscribes to for exactly this reason. Without it
§5.3's "verification is fully available as a post-hoc replay pass" would be
false, because the padding rule would be uncomputable.

ALGORITHM (Kraken WS v2, book channel)
--------------------------------------
1. Take the top 10 asks, price-ascending.
2. For each level, render `price` to `price_precision` decimals and `qty` to
   `qty_precision` decimals; delete the decimal point; delete leading zeros.
   Concatenate price-token then qty-token.
3. Repeat for the top 10 bids, price-descending.
4. CRC32 the resulting ASCII string; compare to the frame's `checksum` as an
   unsigned 32-bit integer.

NO VENUE-SUPPLIED GOLDEN VECTOR IS EMBEDDED IN THIS REPO. The unit tests cover
the deterministic parts (token rendering, ordering sensitivity, unsignedness).
End-to-end agreement was checked against live frames at build time and the
result is reported in the build commit; the captured frames themselves are not
committed, because recorded data is reserved (see `__init__.py`).
"""

from __future__ import annotations

import zlib
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Mapping, Sequence, Tuple


class ChecksumInputError(ValueError):
    """Inputs cannot produce a meaningful checksum (missing precision, etc.)."""


def render_token(value: Any, precision: int) -> str:
    """
    One checksum token: fixed-precision decimal, point removed, leading zeros
    removed.

        render_token("0.05005", 5) -> "5005"
        render_token("4", 8)       -> "400000000"

    `Decimal(str(value))` rather than `float` because binary floats cannot
    represent the decimal ladder the venue is checksumming; a float round-trip
    on a price like 0.1 would silently change the token.

    Values carrying more decimals than `precision` are rounded half-up rather
    than rejected. That case should not occur — the venue quotes on its own
    precision grid — and if it does, the resulting mismatch is loud, which is
    the behaviour we want.
    """
    if precision < 0:
        raise ChecksumInputError(f"negative precision: {precision}")
    try:
        d = Decimal(str(value))
    except Exception as exc:  # noqa: BLE001 - surface the offending value
        raise ChecksumInputError(f"un-decimal-able value {value!r}") from exc
    if d < 0:
        raise ChecksumInputError(f"negative book value {value!r}")
    quantum = Decimal(1).scaleb(-precision)
    fixed = format(d.quantize(quantum, rounding=ROUND_HALF_UP), "f")
    return fixed.replace(".", "").lstrip("0")


def _level(entry: Any) -> Tuple[Any, Any]:
    """Accept both the v2 object form and a bare (price, qty) pair."""
    if isinstance(entry, Mapping):
        if "price" not in entry or "qty" not in entry:
            raise ChecksumInputError(f"book level missing price/qty: {entry!r}")
        return entry["price"], entry["qty"]
    if isinstance(entry, Sequence) and not isinstance(entry, (str, bytes)):
        if len(entry) < 2:
            raise ChecksumInputError(f"book level too short: {entry!r}")
        return entry[0], entry[1]
    raise ChecksumInputError(f"unrecognised book level: {entry!r}")


def checksum_payload(
    asks: Sequence[Any],
    bids: Sequence[Any],
    price_precision: int,
    qty_precision: int,
    depth: int = 10,
) -> str:
    """
    Build the pre-CRC ASCII string. Exposed separately from :func:`book_checksum`
    so a mismatch can be debugged without re-deriving the ordering rules.

    Sorting is applied here rather than trusted from the caller: the frame's
    own ordering is what a desync would corrupt, so re-deriving it from prices
    is the point.
    """
    if len(asks) < depth or len(bids) < depth:
        raise ChecksumInputError(f"need {depth} levels per side to checksum; got {len(asks)} asks / {len(bids)} bids")
    asks_sorted = sorted(asks, key=lambda e: Decimal(str(_level(e)[0])))[:depth]
    bids_sorted = sorted(bids, key=lambda e: Decimal(str(_level(e)[0])), reverse=True)[:depth]

    parts = []
    for side in (asks_sorted, bids_sorted):
        for entry in side:
            price, qty = _level(entry)
            parts.append(render_token(price, price_precision))
            parts.append(render_token(qty, qty_precision))
    return "".join(parts)


def book_checksum(
    asks: Sequence[Any],
    bids: Sequence[Any],
    price_precision: int,
    qty_precision: int,
    depth: int = 10,
) -> int:
    """CRC32 of :func:`checksum_payload`, as an unsigned 32-bit integer."""
    payload = checksum_payload(asks, bids, price_precision, qty_precision, depth)
    return zlib.crc32(payload.encode("ascii")) & 0xFFFFFFFF


def verify_book_frame(
    book: Mapping[str, Any],
    price_precision: int,
    qty_precision: int,
    depth: int = 10,
) -> bool:
    """
    True iff the frame's own `checksum` matches a recomputation.

    A False here is a real book desync and, once live verification lands, must
    produce a `CHECKSUM_MISMATCH` journal record plus a forced resubscribe, with
    `[mismatch_ts, resnapshot_ts]` journaled as DEGRADED — a third coverage
    state, distinct from both UNCAPTURED and QUIET (build spec §5.3).
    """
    if "checksum" not in book:
        raise ChecksumInputError("frame carries no 'checksum' field")
    expected = int(book["checksum"]) & 0xFFFFFFFF
    actual = book_checksum(
        book.get("asks", []),
        book.get("bids", []),
        price_precision,
        qty_precision,
        depth,
    )
    return actual == expected
