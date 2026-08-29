"""
Dispatch W14 step 2 regression: `prescreen_signal._merge_aux_feeds`
(prescreen_signal.py:176-225 before this change) recognised only
"funding_rate" and "fear_greed" and silently dropped anything else — no
column, no warning, no error. A config listing an unsupported feed name
proceeded as though the strategy would receive that column, when it silently
never would.

This is now DENY BY DEFAULT: any name outside `_KNOWN_AUX_FEEDS` raises
`UnrecognizedAuxFeedError` before any merge is attempted, naming the feed.
Not whale-specific — the fix is the general guarantee.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import prescreen_signal as ps  # noqa: E402

_SYMBOL = "NOT_A_REAL_SYMBOL_FIXTURE"


def _bars(n: int = 5) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "volume": 1.0,
        }
    )


def test_unknown_feed_raises_and_names_the_feed():
    with pytest.raises(ps.UnrecognizedAuxFeedError, match="not_a_registered_feed"):
        ps._merge_aux_feeds(
            _bars(), ["not_a_registered_feed"], _SYMBOL, "2024-01-01", "2024-01-06"
        )


def test_unknown_feed_raises_even_mixed_with_a_known_one():
    """The deny check runs BEFORE any merge is attempted -- a mix of one known
    and one unknown name must still raise, not silently merge the known one
    and drop the other."""
    with pytest.raises(ps.UnrecognizedAuxFeedError, match="not_a_registered_feed"):
        ps._merge_aux_feeds(
            _bars(),
            ["funding_rate", "not_a_registered_feed"],
            _SYMBOL,
            "2024-01-01",
            "2024-01-06",
        )


def test_multiple_unknown_feeds_are_all_named_in_one_error():
    with pytest.raises(ps.UnrecognizedAuxFeedError) as excinfo:
        ps._merge_aux_feeds(
            _bars(), ["bogus_a", "bogus_b"], _SYMBOL, "2024-01-01", "2024-01-06"
        )
    msg = str(excinfo.value)
    assert "bogus_a" in msg and "bogus_b" in msg


def test_whale_feed_names_are_not_special_cased_and_still_raise():
    """Explicit non-goal check: step 2 is a general guarantee, not whale-
    specific handling. A whale-footprint column name is just another name this
    loader cannot deliver."""
    with pytest.raises(ps.UnrecognizedAuxFeedError, match="whale_lt_imbalance"):
        ps._merge_aux_feeds(
            _bars(), ["whale_lt_imbalance"], _SYMBOL, "2024-01-01", "2024-01-06"
        )


def test_empty_aux_feeds_list_still_merges_unchanged():
    """No feeds requested -- no raise, no columns added, bars pass through."""
    bars = _bars()
    result = ps._merge_aux_feeds(bars, [], _SYMBOL, "2024-01-01", "2024-01-06")
    assert list(result.columns) == list(bars.columns)
    assert len(result) == len(bars)


def test_known_feed_still_merges_without_raising():
    """A recognised feed name must not be affected by the deny-by-default
    check -- it takes the existing merge path (here: no local data for this
    fixture symbol, so the column is added as NaN, exactly as before this
    change; see FundingRateMeanReversionComponent tests for the real-data
    merge path, which is unaffected by this change and still passes)."""
    result = ps._merge_aux_feeds(
        _bars(), ["funding_rate"], _SYMBOL, "2024-01-01", "2024-01-06"
    )
    assert "funding_rate" in result.columns
    assert result["funding_rate"].isna().all()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
