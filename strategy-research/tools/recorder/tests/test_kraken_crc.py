"""
Kraken v2 book CRC32.

No venue-supplied golden vector is committed here: doing so would mean checking
captured market data into the repo, and recorded data is reserved. What IS
committed is every deterministic property of the algorithm — token rendering,
ordering, depth, unsignedness — so a regression in any of them fails loudly.

End-to-end agreement against live frames is a build-time verification step,
reported in the commit message, and re-runnable with the optional fixture
below. `test_live_fixture_agrees` skips when the (untracked) fixture is absent.
"""

from __future__ import annotations

import json
import zlib
from pathlib import Path

import pytest

from recorder.kraken_crc import (
    ChecksumInputError,
    book_checksum,
    checksum_payload,
    render_token,
    verify_book_frame,
)


def _side(n, price0, step, qty="1.5"):
    return [{"price": round(price0 + i * step, 8), "qty": qty} for i in range(n)]


# ---------------------------------------------------------------------------
# token rendering — the part everything else depends on
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value,precision,expected",
    [
        ("0.05005", 5, "5005"),  # leading zeros stripped, point removed
        ("4", 8, "400000000"),  # padded out to full precision
        ("45283.5", 1, "452835"),
        ("45283.50", 2, "4528350"),  # padding is significant to the checksum
        ("0.00000100", 8, "100"),
        ("1.0", 1, "10"),
        (45283.5, 1, "452835"),  # float input accepted
        ("0.1", 8, "10000000"),  # float(0.1) binary error would break this
    ],
)
def test_render_token(value, precision, expected):
    assert render_token(value, precision) == expected


def test_render_token_is_decimal_not_binary_float():
    """
    2.675 is 2.67499999999999982236431605997495353221893310546875 in binary.
    Rendering through Decimal(str(v)) keeps the venue's decimal; going through
    float would silently emit '267' instead of '268' at precision 2.
    """
    assert render_token("2.675", 2) == "268"


def test_render_token_rejects_negative_and_bad_input():
    with pytest.raises(ChecksumInputError):
        render_token("-1.0", 2)
    with pytest.raises(ChecksumInputError):
        render_token("not-a-number", 2)
    with pytest.raises(ChecksumInputError):
        render_token("1.0", -1)


# ---------------------------------------------------------------------------
# payload construction
# ---------------------------------------------------------------------------


def test_payload_is_asks_ascending_then_bids_descending():
    asks = [{"price": "2.0", "qty": "1"}, {"price": "1.0", "qty": "2"}]
    bids = [{"price": "0.5", "qty": "3"}, {"price": "0.9", "qty": "4"}]
    payload = checksum_payload(asks, bids, price_precision=1, qty_precision=0, depth=2)
    #   asks ascending : 1.0/2 then 2.0/1   -> "10" "2" "20" "1"
    #   bids descending: 0.9/4 then 0.5/3   -> "9"  "4" "5"  "3"
    assert payload == "10" + "2" + "20" + "1" + "9" + "4" + "5" + "3"


def test_payload_ignores_caller_supplied_order():
    """Ordering is re-derived from price, because order is what a desync breaks."""
    asks = _side(10, 100.0, 0.1)
    bids = _side(10, 99.0, -0.1)
    a = checksum_payload(asks, bids, 2, 8)
    b = checksum_payload(list(reversed(asks)), list(reversed(bids)), 2, 8)
    assert a == b


def test_bare_price_qty_pairs_are_accepted():
    obj = [{"price": "1.0", "qty": "2.0"}] * 10
    seq = [["1.0", "2.0"]] * 10
    assert checksum_payload(obj, obj, 1, 1) == checksum_payload(seq, seq, 1, 1)


def test_fewer_than_depth_levels_raises():
    with pytest.raises(ChecksumInputError):
        checksum_payload(_side(9, 100.0, 0.1), _side(10, 99.0, -0.1), 2, 8)


def test_depth_truncates_to_top_10():
    """Only the top 10 per side enter the checksum, whatever else is present."""
    asks10 = _side(10, 100.0, 0.1)
    bids10 = _side(10, 99.0, -0.1)
    deep_asks = asks10 + _side(5, 200.0, 0.1)  # far from the touch
    deep_bids = bids10 + _side(5, 50.0, -0.1)
    assert book_checksum(asks10, bids10, 2, 8) == book_checksum(deep_asks, deep_bids, 2, 8)


# ---------------------------------------------------------------------------
# checksum
# ---------------------------------------------------------------------------


def test_checksum_is_unsigned_crc32_of_the_payload():
    asks, bids = _side(10, 100.0, 0.1), _side(10, 99.0, -0.1)
    payload = checksum_payload(asks, bids, 2, 8)
    expected = zlib.crc32(payload.encode("ascii")) & 0xFFFFFFFF
    got = book_checksum(asks, bids, 2, 8)
    assert got == expected
    assert 0 <= got <= 0xFFFFFFFF


def test_a_single_changed_level_changes_the_checksum():
    asks, bids = _side(10, 100.0, 0.1), _side(10, 99.0, -0.1)
    base = book_checksum(asks, bids, 2, 8)
    tweaked = [dict(l) for l in asks]
    tweaked[4]["qty"] = "1.50000001"
    assert book_checksum(tweaked, bids, 2, 8) != base


def test_precision_changes_the_checksum():
    """Wrong precision -> wrong checksum, which is why `instrument` is captured."""
    asks, bids = _side(10, 100.0, 0.1), _side(10, 99.0, -0.1)
    assert book_checksum(asks, bids, 2, 8) != book_checksum(asks, bids, 3, 8)


def test_verify_book_frame_accepts_matching_and_rejects_corrupt():
    asks, bids = _side(10, 100.0, 0.1), _side(10, 99.0, -0.1)
    good = {"asks": asks, "bids": bids, "checksum": book_checksum(asks, bids, 2, 8)}
    assert verify_book_frame(good, 2, 8) is True

    bad = dict(good, checksum=(good["checksum"] + 1) & 0xFFFFFFFF)
    assert verify_book_frame(bad, 2, 8) is False


def test_verify_book_frame_without_checksum_raises():
    asks, bids = _side(10, 100.0, 0.1), _side(10, 99.0, -0.1)
    with pytest.raises(ChecksumInputError):
        verify_book_frame({"asks": asks, "bids": bids}, 2, 8)


# ---------------------------------------------------------------------------
# optional live fixture (untracked — recorded data is reserved)
# ---------------------------------------------------------------------------

_FIXTURE = Path(__file__).parent / "fixtures" / "live_book_snapshot.json"


@pytest.mark.skipif(not _FIXTURE.exists(), reason="live fixture not present (untracked)")
def test_live_fixture_agrees():
    payload = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    for case in payload["cases"]:
        assert verify_book_frame(case["book"], case["price_precision"], case["qty_precision"]), (
            f"CRC32 mismatch for {case['book'].get('symbol')}"
        )
