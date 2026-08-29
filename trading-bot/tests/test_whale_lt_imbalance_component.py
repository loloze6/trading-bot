"""
Wiring proof for `WhaleLargeTradeImbalanceComponent` (dispatch W13 step 3).

FIXTURES ONLY. Every whale feature value below is synthetic and planted, with a
known intended answer. Nothing here reads
`trading-bot/local_data/recorded_reserved/`, constructs a
`WhaleFootprintFetcher`, or touches the campaign_data_policy designation gate --
and nothing here computes a forward return, a correlation, an IC or a P&L
against a whale feature. That question is separately gated
(`strategy-research/protocols/prereg_whale_footprint_v2.yaml`) and answering it
inside a wiring test would produce an ungated verdict on reserved data.

What is proved:
  1. Through the REAL strategy path (`AdvancedStrategy` + the config-driven
     engine, the same path `prescreen_signal.py::_extract_forecasts` drives):
     a strong sustained POSITIVE imbalance yields a positive forecast, a strong
     sustained NEGATIVE one yields a negative forecast, and an unattested bar
     yields NO forecast (NaN) -- not zero, and not the previous bar's value.
  2. The stale-carry failure specifically: the forecast on an abstained bar is
     not the last attested bar's forecast.
  3. 0.0 is emitted ONLY when the whole persistence window was measured and was
     not sustainedly imbalanced -- the one case where zero is a measurement.
  4. The component consumes the column through the REAL aux-feed merge
     (`DataManager.register_feed` -> `_premerge_aux_feeds` ->
     `_merge_asof_with_causality_guard`) under the W9 `window_seconds`
     declaration registered for the whale feeds, and the guard rejects a
     mis-declared wider window.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import AuxFeedCausalityError, DataManager  # noqa: E402
from data.feed_registry import FEED_WINDOW_SECONDS, WHALE_FOOTPRINT_FEEDS  # noqa: E402
from strategies.main_strategy import AdvancedStrategy  # noqa: E402
from strategies.strategy_components import (  # noqa: E402
    WHALE_ATTESTED_COLUMN,
    WHALE_LT_IMBALANCE_COLUMN,
    WhaleLargeTradeImbalanceComponent,
)

PERSISTENCE_BARS = 3
SCALING_FACTOR = 10.0
MIN_ABS_IMBALANCE = 0.5
INTERVAL_SECONDS = 3600
SYMBOL = "BTCUSD"

# `AdvancedStrategy.required_bars` is floored at the 24-bar stddev period
# regardless of the component's own 3, so the fixture must be longer than that
# before any bar is even a candidate for a forecast.
_REQUIRED_BARS = 24


# ---------------------------------------------------------------------------
# Fixture construction
# ---------------------------------------------------------------------------


def _whale_component(**overrides) -> WhaleLargeTradeImbalanceComponent:
    params = {
        "persistence_bars": PERSISTENCE_BARS,
        "min_abs_imbalance": MIN_ABS_IMBALANCE,
        "scaling_factor": SCALING_FACTOR,
    }
    params.update(overrides)
    return WhaleLargeTradeImbalanceComponent(parameters=params)


def _pattern_a_config(warmup: int = 3) -> dict:
    """The canonical ungated pattern established by
    `tests/test_ungated_config_pattern.py`: empty regime rules/components,
    `default_regime="unknown"` (the one choice whose readiness check is
    non-vacuous), and the real signal as the SOLE component of that regime.

    Sole component on purpose: this component abstains with NaN, and NaN
    propagates to the whole ensemble sum -- a univariate test is the only
    configuration in which that is the intended meaning.
    """
    return {
        "regime_detector": {
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": "unknown",
        },
        "strategies": {
            "warmup": warmup,
            "regimes": {
                "trending": None,
                "mean_reversion": None,
                "chop": None,
                "unknown": {
                    "components": [
                        {
                            "id": "whale_lti",
                            "class": "strategies.strategy_components.WhaleLargeTradeImbalanceComponent",
                            "weight": 1.0,
                            "params": {
                                "persistence_bars": PERSISTENCE_BARS,
                                "min_abs_imbalance": MIN_ABS_IMBALANCE,
                                "scaling_factor": SCALING_FACTOR,
                            },
                            "transforms": [{"op": "identity"}],
                        }
                    ],
                },
            },
        },
    }


def _bars(imbalance, attested, n_pad: int = 30) -> pd.DataFrame:
    """Synthetic OHLCV carrying planted whale columns.

    `imbalance` / `attested` are the values for the FINAL `len(imbalance)` bars;
    the preceding `n_pad` bars are attested-but-unmeasured (NaN imbalance) so
    they can never themselves manufacture a signal -- every fired forecast in
    these tests comes from the planted tail alone.
    """
    tail = len(imbalance)
    n = n_pad + tail
    close = 100.0 + np.arange(n, dtype=float) * 0.01
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-07-27", periods=n, freq="h", tz=None),
            "open": close,
            "high": close + 0.5,
            "low": close - 0.5,
            "close": close,
            "volume": 1.0,
            WHALE_LT_IMBALANCE_COLUMN: [np.nan] * n_pad + list(imbalance),
            WHALE_ATTESTED_COLUMN: [1.0] * n_pad + list(attested),
        }
    )


def _forecast_sequence(bars: pd.DataFrame, warmup: int = 3) -> list:
    """Drive the REAL strategy path bar by bar; return the forecast at every bar
    where the strategy reports ready, `None` where it does not. Index-aligned to
    `bars`. This is the same loop `prescreen_signal.py::_extract_forecasts`
    (prescreen_signal.py:302-324) runs."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(_pattern_a_config(warmup), f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        out = []
        for i in range(1, len(bars) + 1):
            strat.update(bars.iloc[i - 1 : i])
            out.append(strat.generate_forecast()[0] if strat.is_ready() else None)
        return out
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# 1. Direction: strong positive -> positive, strong negative -> negative
# ---------------------------------------------------------------------------


def test_sustained_positive_imbalance_yields_positive_forecast():
    bars = _bars([0.9, 0.9, 0.9], [1.0, 1.0, 1.0])
    seq = _forecast_sequence(bars)
    final = seq[-1]
    assert final is not None, "strategy never became ready — widen the fixture"
    assert not np.isnan(final), "sustained, fully attested window must produce a forecast"
    assert final > 0.0, f"positive sustained imbalance must forecast long, got {final}"
    assert final == pytest.approx(0.9 * SCALING_FACTOR), (
        "forecast must be mean(imbalance) x scaling_factor — continuation, sign NOT inverted"
    )
    assert -20.0 <= final <= 20.0, "forecast must respect the -20..+20 pipeline convention"


def test_sustained_negative_imbalance_yields_negative_forecast():
    bars = _bars([-0.9, -0.9, -0.9], [1.0, 1.0, 1.0])
    final = _forecast_sequence(bars)[-1]
    assert final is not None and not np.isnan(final)
    assert final < 0.0, f"negative sustained imbalance must forecast short, got {final}"
    assert final == pytest.approx(-0.9 * SCALING_FACTOR)
    assert -20.0 <= final <= 20.0


# ---------------------------------------------------------------------------
# 2. Abstention: an unattested bar yields NO forecast, and no stale carry
# ---------------------------------------------------------------------------


def test_unattested_bar_yields_no_forecast_not_zero_and_not_stale():
    """THE central NaN requirement. Bars 0-2 are a strong, fully attested
    positive run (forecast fires). Bar 3 is UNATTESTED. Its forecast must be
    NaN — not 0.0 (which would assert balanced whale flow on a bar with no
    usable measurement) and not the +9.0 carried from bar 2."""
    bars = _bars([0.9, 0.9, 0.9, 0.9], [1.0, 1.0, 1.0, 0.0])
    seq = _forecast_sequence(bars)
    fired, abstained = seq[-2], seq[-1]

    assert fired is not None and fired == pytest.approx(0.9 * SCALING_FACTOR), (
        "the attested run must fire first — otherwise the abstention below proves nothing"
    )
    assert abstained is not None, "strategy readiness must not itself hide the abstention"
    assert np.isnan(abstained), f"an unattested bar must produce NO forecast; got {abstained!r}"
    assert abstained != 0.0, "zero would assert 'balanced', which is a claim"
    assert not (abstained == fired), "the abstained bar must not carry the prior forecast"


def test_unattested_bar_earlier_in_the_window_also_abstains():
    """The persistence claim spans the whole window: a gap two bars back makes
    'sustained' unverifiable even though the current bar is attested."""
    bars = _bars([0.9, 0.9, 0.9], [0.0, 1.0, 1.0])
    final = _forecast_sequence(bars)[-1]
    assert final is not None and np.isnan(final), (
        f"an unattested bar anywhere in the persistence window must abstain; got {final!r}"
    )


def test_attested_but_unmeasured_bar_abstains():
    """`whale_lt_imbalance` is NaN when no trade reached the pair's own tau, even
    on a fully attested bar (whale_features.py definition (a)). Nothing was
    measured, so nothing is asserted."""
    bars = _bars([0.9, np.nan, 0.9], [1.0, 1.0, 1.0])
    final = _forecast_sequence(bars)[-1]
    assert final is not None and np.isnan(final)


def test_missing_aux_columns_abstain_rather_than_read_as_balanced():
    """A wiring failure must not become a scientific result."""
    comp = _whale_component()
    plain = _bars([0.9, 0.9, 0.9], [1.0, 1.0, 1.0]).drop(columns=[WHALE_LT_IMBALANCE_COLUMN, WHALE_ATTESTED_COLUMN])
    comp.update(plain)
    assert np.isnan(comp.raw_value()), "absent aux columns must abstain, not emit 0.0"
    assert comp.debug_info["abstain_reason"] == "aux_feed_columns_absent"


# ---------------------------------------------------------------------------
# 3. Zero is a measurement, and only where it is one
# ---------------------------------------------------------------------------


def test_measured_but_not_sustained_yields_exactly_zero():
    """Fully attested, fully measured, sign flips inside the window: the flow WAS
    measured and was not sustainedly one-directional. That is the one place 0.0
    is correct — and it must be distinguishable from the NaN cases above."""
    comp = _whale_component()
    comp.update(_bars([0.9, -0.9, 0.9], [1.0, 1.0, 1.0]))
    assert comp.raw_value() == 0.0
    assert comp.debug_info["abstained"] is False
    assert comp.debug_info["same_sign"] is False


def test_measured_below_magnitude_threshold_yields_exactly_zero():
    comp = _whale_component()
    comp.update(_bars([0.2, 0.2, 0.2], [1.0, 1.0, 1.0]))
    assert comp.raw_value() == 0.0
    assert comp.debug_info["all_above_threshold"] is False


def test_abstention_and_measured_zero_are_distinguishable():
    """The whole point of the NaN convention: the two must never collapse."""
    unattested = _whale_component()
    unattested.update(_bars([0.9, 0.9, 0.9], [1.0, 1.0, 0.0]))
    measured_flat = _whale_component()
    measured_flat.update(_bars([0.2, 0.2, 0.2], [1.0, 1.0, 1.0]))

    assert np.isnan(unattested.raw_value())
    assert measured_flat.raw_value() == 0.0
    assert unattested.debug_info["abstained"] is True
    assert measured_flat.debug_info["abstained"] is False


def test_component_abstains_before_its_first_update():
    """A freshly constructed component has measured nothing; 0.0 would be a
    claim about that nothing."""
    assert np.isnan(_whale_component().raw_value())


def test_readiness_is_bar_count_only_so_abstentions_still_reach_history():
    """`is_ready()` must not consult attestation — a not-ready bar appends
    nothing to the engine history and the next forecast would be seeded from the
    last ATTESTED value (registry.py:105), i.e. a silent stale carry."""
    comp = _whale_component()
    unattested = _bars([0.9, 0.9, 0.9], [0.0, 0.0, 0.0])
    comp.update(unattested)
    assert comp.is_ready(), (
        "component went not-ready on unattested bars — the engine would skip the "
        "append and the forecast would stale-carry"
    )
    assert np.isnan(comp.raw_value())


def test_persistence_bars_must_be_positive():
    with pytest.raises(ValueError, match="persistence_bars"):
        _whale_component(persistence_bars=0)


# ---------------------------------------------------------------------------
# 4. The real aux-feed path and the W9 causality declaration
# ---------------------------------------------------------------------------


class _StubWhaleFetcher:
    """Matches the `feed.fetcher.get_data(symbol)` contract `_premerge_aux_feeds`
    expects (data_manager.py:729) — the same minimal stand-in
    `tests/test_aux_feed_causality_canary.py::_CanaryFetcher` uses. Deliberately
    NOT `WhaleFootprintFetcher`: constructing that would hit the reserved-data
    designation gate, which is exactly what a fixture must not do."""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def get_data(self, symbol=None):
        return self._df


def test_whale_feeds_declare_their_forward_bar_window():
    """W9 registration invariant: every whale feed declares
    `window_seconds == bar_seconds`, the forward window
    `[timestamp, timestamp + bar_seconds)` the features actually aggregate."""
    from data.fetchers.whale_footprint_fetcher import DEFAULT_BAR_SECONDS

    for name in WHALE_FOOTPRINT_FEEDS:
        assert FEED_WINDOW_SECONDS[name] == DEFAULT_BAR_SECONDS, (
            f"{name} lost its window_seconds declaration — register_feed() would "
            "reject it, or worse, a future default would let it merge untested"
        )
    assert WHALE_LT_IMBALANCE_COLUMN in WHALE_FOOTPRINT_FEEDS
    assert WHALE_ATTESTED_COLUMN in WHALE_FOOTPRINT_FEEDS


def _premerge(window_seconds: float) -> pd.DataFrame:
    """Run the REAL merge path for both whale columns at the given declared
    window, returning the enriched bar frame."""
    n = 6
    ts = pd.date_range("2026-07-27", periods=n, freq="h")
    price = pd.DataFrame({"timestamp": ts, "close": 100.0 + np.arange(n)})
    feed = pd.DataFrame(
        {
            "timestamp": ts,
            WHALE_LT_IMBALANCE_COLUMN: [0.9, 0.9, 0.9, -0.9, -0.9, -0.9],
            WHALE_ATTESTED_COLUMN: [1.0] * n,
        }
    )

    dm = DataManager(symbols=[SYMBOL], interval_seconds=INTERVAL_SECONDS, mode="backtest")
    for name in (WHALE_LT_IMBALANCE_COLUMN, WHALE_ATTESTED_COLUMN):
        dm.register_feed(name, _StubWhaleFetcher(feed), window_seconds=window_seconds, agg="last")
    return dm._premerge_aux_feeds(SYMBOL, price)


def test_real_aux_merge_attaches_each_bars_own_value():
    """`window_seconds == interval_seconds` is the honest declaration for a
    same-grid forward-window feature: the guard allows it (equality is allowed)
    and each bar receives its OWN value, never the next bar's."""
    enriched = _premerge(INTERVAL_SECONDS)
    assert list(enriched[WHALE_LT_IMBALANCE_COLUMN]) == [0.9, 0.9, 0.9, -0.9, -0.9, -0.9]
    assert enriched[WHALE_ATTESTED_COLUMN].eq(1.0).all()


def test_real_aux_merge_rejects_a_wider_declared_window():
    """The W9 guard is live on this feed: a value whose declared window would run
    past the bar's own close is refused rather than attached."""
    with pytest.raises(AuxFeedCausalityError, match="ends after bar"):
        _premerge(2 * INTERVAL_SECONDS)


def test_component_reads_the_merged_columns_end_to_end():
    """Merge through the real path, then feed the merged frame to the component:
    the sustained negative tail must produce a negative forecast, proving the
    component consumes what `_premerge_aux_feeds` actually produces (column
    names and dtypes included) rather than a hand-built frame."""
    enriched = _premerge(INTERVAL_SECONDS).sort_values("timestamp").reset_index(drop=True)
    comp = _whale_component()
    comp.update(enriched)
    assert comp.raw_value() == pytest.approx(-0.9 * SCALING_FACTOR)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
