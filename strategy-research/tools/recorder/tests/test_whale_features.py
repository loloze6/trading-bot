"""
Whale-footprint features: each definition, and the bar driver's marking rules.

The three feature functions are tested against hand-computed values, not against
each other — a test that only asserts self-consistency would pass on a
uniformly-wrong definition.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

import numpy as np
import pytest

from recorder.shard_reader import Gap, Trade
from recorder.whale_features import (
    DEFAULT_BAR_SECONDS,
    DEFAULT_BASELINE_SECONDS,
    DEFAULT_LARGE_QUANTILE,
    DEFAULT_MIN_BAR_TRADES,
    DEFAULT_MIN_BASELINE_TRADES,
    FEATURE_COLUMNS,
    bar_floor,
    cumulative_volume_delta,
    large_trade_imbalance,
    size_threshold,
    trade_size_shift,
    whale_bar_features,
)

T0 = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)


def mk(price=100.0, qty=1.0, side="buy", ts=None, trade_id=0, symbol="BTCUSD"):
    ts = ts or T0
    return Trade(
        ts=ts,
        recv_ts=ts,
        symbol=symbol,
        price=price,
        qty=qty,
        side=side,
        ord_type="market",
        trade_id=trade_id,
        from_snapshot=False,
    )


# ---------------------------------------------------------------------------
# defaults are the documented ones
# ---------------------------------------------------------------------------


def test_documented_defaults():
    assert DEFAULT_BAR_SECONDS == 3600  # the pipeline's bar
    assert DEFAULT_LARGE_QUANTILE == 0.99  # top 1% of the pair's own trades
    assert DEFAULT_BASELINE_SECONDS == 86400  # one diurnal cycle
    assert DEFAULT_MIN_BASELINE_TRADES == 200
    assert DEFAULT_MIN_BAR_TRADES == 10


# ---------------------------------------------------------------------------
# tau: a quantile of the pair's OWN distribution
# ---------------------------------------------------------------------------


def test_threshold_is_a_quantile_of_the_baseline():
    base = [float(i) for i in range(1, 1001)]  # 1..1000
    tau = size_threshold(base, quantile=0.99, min_samples=200)
    assert tau == pytest.approx(np.quantile(base, 0.99))
    assert 985 < tau < 1000


def test_threshold_is_relative_so_pairs_with_different_scales_agree():
    small = [float(i) for i in range(1, 1001)]
    big = [1e6 * i for i in range(1, 1001)]
    # the same trade RANK is selected in both, which is the whole point of
    # expressing the threshold as a quantile rather than an absolute figure
    assert size_threshold(big, 0.99, 200) == pytest.approx(1e6 * size_threshold(small, 0.99, 200))


def test_threshold_is_nan_below_the_sample_floor():
    assert math.isnan(size_threshold([1.0] * 199, 0.99, min_samples=200))
    assert not math.isnan(size_threshold([1.0] * 200, 0.99, min_samples=200))


@pytest.mark.parametrize("q", [0.0, 1.0, -0.1, 1.5])
def test_threshold_rejects_a_degenerate_quantile(q):
    with pytest.raises(ValueError):
        size_threshold([1.0] * 500, quantile=q)


# ---------------------------------------------------------------------------
# (a) large-trade imbalance
# ---------------------------------------------------------------------------


def test_large_trade_imbalance_ignores_everything_below_the_threshold():
    trades = [
        mk(price=100.0, qty=1.0, side="buy", trade_id=1),  # notional 100, small
        mk(price=100.0, qty=100.0, side="buy", trade_id=2),  # notional 10_000, large
        mk(price=100.0, qty=50.0, side="sell", trade_id=3),  # notional 5_000, large
    ]
    r = large_trade_imbalance(trades, threshold=1000.0)
    assert r.count == 2
    assert r.gross_notional == pytest.approx(15000.0)
    # (+10000 - 5000) / 15000
    assert r.value == pytest.approx(1.0 / 3.0)


def test_large_trade_imbalance_is_plus_one_when_all_whales_buy():
    trades = [mk(qty=100.0, side="buy", trade_id=i) for i in range(3)]
    assert large_trade_imbalance(trades, 1000.0).value == pytest.approx(1.0)


def test_large_trade_imbalance_is_minus_one_when_all_whales_sell():
    trades = [mk(qty=100.0, side="sell", trade_id=i) for i in range(3)]
    assert large_trade_imbalance(trades, 1000.0).value == pytest.approx(-1.0)


def test_large_trade_imbalance_is_nan_not_zero_when_nothing_qualifies():
    """
    Zero would assert that whale flow was balanced. There was no whale flow.
    `count` is what tells the two apart.
    """
    r = large_trade_imbalance([mk(qty=0.001, trade_id=1)], threshold=1e9)
    assert math.isnan(r.value) and r.count == 0

    balanced = large_trade_imbalance(
        [mk(qty=100.0, side="buy", trade_id=1), mk(qty=100.0, side="sell", trade_id=2)],
        threshold=1000.0,
    )
    assert balanced.value == pytest.approx(0.0) and balanced.count == 2


def test_large_trade_imbalance_is_nan_when_the_threshold_is_undefined():
    r = large_trade_imbalance([mk(qty=100.0, trade_id=1)], threshold=math.nan)
    assert math.isnan(r.value) and r.count == 0


def test_large_trade_imbalance_stays_within_bounds():
    rng = np.random.default_rng(7)
    trades = [
        mk(
            price=float(rng.uniform(1, 1e4)),
            qty=float(rng.uniform(0.01, 50)),
            side="buy" if rng.random() < 0.5 else "sell",
            trade_id=i,
        )
        for i in range(500)
    ]
    v = large_trade_imbalance(trades, threshold=1.0).value
    assert -1.0 <= v <= 1.0


# ---------------------------------------------------------------------------
# (b) cumulative volume delta
# ---------------------------------------------------------------------------


def test_cvd_is_buy_notional_minus_sell_notional():
    trades = [
        mk(price=100.0, qty=3.0, side="buy", trade_id=1),  # +300
        mk(price=50.0, qty=4.0, side="sell", trade_id=2),  # -200
    ]
    assert cumulative_volume_delta(trades) == pytest.approx(100.0)


def test_cvd_is_notional_not_base_quantity():
    # 1 unit at 100 must outweigh 10 units at 1
    trades = [mk(price=100.0, qty=1.0, side="buy", trade_id=1), mk(price=1.0, qty=10.0, side="sell", trade_id=2)]
    assert cumulative_volume_delta(trades) == pytest.approx(90.0)


def test_cvd_of_an_empty_window_is_zero():
    assert cumulative_volume_delta([]) == 0.0


def test_cvd_is_additive_so_the_running_total_is_a_cumsum():
    a = [mk(qty=1.0, side="buy", trade_id=1)]
    b = [mk(qty=2.0, side="sell", trade_id=2)]
    assert cumulative_volume_delta(a + b) == pytest.approx(cumulative_volume_delta(a) + cumulative_volume_delta(b))


# ---------------------------------------------------------------------------
# (c) trade-size distribution shift
# ---------------------------------------------------------------------------


def test_size_shift_is_the_log_ratio_of_medians():
    baseline = [100.0] * 500
    trades = [mk(price=100.0, qty=2.0, trade_id=i) for i in range(20)]  # notional 200
    assert trade_size_shift(trades, baseline) == pytest.approx(math.log(2.0))


def test_size_shift_is_zero_when_the_distribution_has_not_moved():
    baseline = [100.0] * 500
    trades = [mk(price=100.0, qty=1.0, trade_id=i) for i in range(20)]
    assert trade_size_shift(trades, baseline) == pytest.approx(0.0)


def test_size_shift_is_symmetric_under_inversion():
    baseline = [100.0] * 500
    doubled = [mk(price=100.0, qty=2.0, trade_id=i) for i in range(20)]
    halved = [mk(price=100.0, qty=0.5, trade_id=i) for i in range(20)]
    assert trade_size_shift(doubled, baseline) == pytest.approx(-trade_size_shift(halved, baseline))


def test_size_shift_uses_the_median_so_one_whale_does_not_move_it():
    """
    The separation from feature (a) is the point: a single huge print is what
    (a) measures, and (c) must not be a second, noisier copy of it.
    """
    baseline = [100.0] * 500
    ordinary = [mk(price=100.0, qty=1.0, trade_id=i) for i in range(20)]
    with_whale = ordinary + [mk(price=100.0, qty=1e6, trade_id=99)]
    assert trade_size_shift(with_whale, baseline) == pytest.approx(trade_size_shift(ordinary, baseline), abs=0.05)


def test_size_shift_is_nan_below_either_sample_floor():
    baseline = [100.0] * 500
    assert math.isnan(trade_size_shift([mk(trade_id=i) for i in range(9)], baseline, min_bar_trades=10))
    assert math.isnan(trade_size_shift([mk(trade_id=i) for i in range(20)], [100.0] * 199, min_baseline_trades=200))


# ---------------------------------------------------------------------------
# bar grid
# ---------------------------------------------------------------------------


def test_bar_floor_snaps_to_the_epoch_grid():
    assert bar_floor(datetime(2026, 7, 26, 12, 34, 56, tzinfo=timezone.utc), 3600) == datetime(
        2026, 7, 26, 12, 0, tzinfo=timezone.utc
    )
    assert bar_floor(datetime(2026, 7, 26, 12, 34, 56, tzinfo=timezone.utc), 60) == datetime(
        2026, 7, 26, 12, 34, tzinfo=timezone.utc
    )


def test_driver_emits_a_complete_bar_grid_including_empty_bars():
    """
    A missing row is indistinguishable from a bar nobody asked about, and
    merge_asof(direction='backward') would carry a neighbour's value across the
    hole. Every bar gets a row.
    """
    trades = [mk(ts=T0, trade_id=1), mk(ts=T0 + timedelta(hours=3), trade_id=2)]
    df = whale_bar_features(trades, bar_seconds=3600)
    assert len(df) == 4
    assert list(df.columns) == ["timestamp", *FEATURE_COLUMNS]
    assert list(df["whale_trade_count"]) == [1.0, 0.0, 0.0, 1.0]
    assert df["timestamp"].dt.tz is None, "the cache convention is naive-UTC"


def test_driver_bins_trades_by_venue_event_time():
    trades = [
        mk(ts=T0 + timedelta(minutes=10), price=100.0, qty=1.0, side="buy", trade_id=1),
        mk(ts=T0 + timedelta(minutes=70), price=100.0, qty=2.0, side="sell", trade_id=2),
    ]
    df = whale_bar_features(trades, bar_seconds=3600)
    assert list(df["whale_cvd_delta"]) == pytest.approx([100.0, -200.0])


def test_empty_stream_yields_an_empty_frame_with_the_right_columns():
    df = whale_bar_features([])
    assert df.empty and list(df.columns) == ["timestamp", *FEATURE_COLUMNS]


def test_driver_rejects_a_stream_that_is_not_trades_or_gaps():
    with pytest.raises(TypeError, match="expected Trade or Gap"):
        whale_bar_features([object()])


# ---------------------------------------------------------------------------
# gap marking
# ---------------------------------------------------------------------------


def test_a_bar_touching_a_gap_is_marked_and_its_values_nan_ed():
    trades = [mk(ts=T0 + timedelta(minutes=i), qty=1.0, trade_id=i) for i in range(30)]
    gap = Gap(
        symbol="BTCUSD",
        channel="trade",
        start=T0 + timedelta(minutes=40),
        end=T0 + timedelta(minutes=50),
        cause="between_intervals",
    )
    df = whale_bar_features(
        list(trades) + [gap],
        bar_seconds=3600,
        min_baseline_trades=1,
        min_bar_trades=1,
    )
    assert list(df["whale_attested"]) == [0.0]
    # the trades were captured, and are still counted — but no VALUE is served
    assert df["whale_trade_count"].iloc[0] == 30.0
    assert math.isnan(df["whale_cvd_delta"].iloc[0])
    assert math.isnan(df["whale_lt_imbalance"].iloc[0])
    assert math.isnan(df["whale_size_shift"].iloc[0])


def test_a_partially_covered_bar_is_not_a_partial_measurement():
    """90% captured is not 90% of a number: the missing 10% is where the whale
    print would be, and a served value is indistinguishable from a clean one."""
    trades = [mk(ts=T0 + timedelta(minutes=i), trade_id=i) for i in range(54)]
    gap = Gap(
        symbol="BTCUSD",
        channel="trade",
        start=T0 + timedelta(minutes=54),
        end=T0 + timedelta(minutes=60),
        cause="between_intervals",
    )
    df = whale_bar_features(trades + [gap], bar_seconds=3600, min_baseline_trades=1, min_bar_trades=1)
    assert df["whale_attested"].iloc[0] == 0.0


def test_a_quiet_but_attested_bar_is_scored_normally():
    """Attested-and-quiet is not a gap. The differential-guard property."""
    trades = [mk(ts=T0, trade_id=1), mk(ts=T0 + timedelta(hours=2), trade_id=2)]
    df = whale_bar_features(trades, bar_seconds=3600)
    assert list(df["whale_attested"]) == [1.0, 1.0, 1.0]
    assert df["whale_trade_count"].iloc[1] == 0.0
    assert df["whale_cvd_delta"].iloc[1] == 0.0  # a real measurement: no flow


def test_a_gap_marks_only_the_bars_it_actually_intersects():
    trades = [mk(ts=T0, trade_id=1)]
    gap = Gap(
        symbol="BTCUSD",
        channel="trade",
        start=T0 + timedelta(hours=5),
        end=T0 + timedelta(hours=6),
        cause="after_last_attested",
    )
    df = whale_bar_features(trades + [gap], bar_seconds=3600)
    # Bars 0..4 are clean, bar 5 ([+5h,+6h)) is the gap, and bar 6 — emitted
    # because [start, end] is inclusive and end == +6h — is clean again: the
    # gap CLOSES at +6h, so it does not reach into the bar starting there.
    assert list(df["whale_attested"]) == [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]


# ---------------------------------------------------------------------------
# the trailing baseline
# ---------------------------------------------------------------------------


def test_baseline_is_strictly_before_the_bar():
    """
    The bar's own whale print must not raise the threshold meant to detect it.
    Bar 1 has only its own trades available as baseline (none), so it is
    unscored; bar 2 is scored against bar 1.
    """
    b1 = [mk(ts=T0 + timedelta(seconds=i), qty=1.0, trade_id=i) for i in range(300)]
    b2 = [mk(ts=T0 + timedelta(hours=1, seconds=i), qty=1.0, trade_id=1000 + i) for i in range(300)]
    df = whale_bar_features(b1 + b2, bar_seconds=3600, min_baseline_trades=200, min_bar_trades=10)
    assert math.isnan(df["whale_lt_imbalance"].iloc[0]), "no baseline yet"
    assert math.isnan(df["whale_size_shift"].iloc[0])
    assert not math.isnan(df["whale_size_shift"].iloc[1]), "bar 1 is bar 2's baseline"


def test_baseline_rolls_out_after_baseline_seconds():
    """
    `baseline_seconds` decides what a bar is compared against, and the two
    settings must disagree exactly where the older trades fall in or out.
    """
    old = [mk(ts=T0, price=100.0, qty=1.0, trade_id=i) for i in range(300)]
    recent = [mk(ts=T0 + timedelta(hours=3), price=100.0, qty=10.0, trade_id=1000 + i) for i in range(300)]
    scored = [mk(ts=T0 + timedelta(hours=4), price=100.0, qty=10.0, trade_id=2000 + i) for i in range(300)]
    short = whale_bar_features(
        old + recent + scored, bar_seconds=3600, baseline_seconds=2 * 3600, min_baseline_trades=200
    )
    long = whale_bar_features(
        old + recent + scored, bar_seconds=3600, baseline_seconds=24 * 3600, min_baseline_trades=200
    )

    # Hour 4, 2h baseline: only the hour-3 trades (notional 1000) are in scope,
    # and the scored bar matches them exactly.
    assert short["whale_size_shift"].iloc[4] == pytest.approx(0.0)
    # Hour 4, 24h baseline: 300 trades at 100 AND 300 at 1000 are in scope, so
    # the baseline median sits between them at 550.
    assert long["whale_size_shift"].iloc[4] == pytest.approx(math.log(1000 / 550))
    # Hour 3, 24h baseline: only the hour-0 trades have rolled in yet.
    assert long["whale_size_shift"].iloc[3] == pytest.approx(math.log(10.0))
    # Hour 3, 2h baseline: the hour-0 trades already rolled out, leaving nothing.
    assert math.isnan(short["whale_size_shift"].iloc[3])


def test_a_whale_bar_scores_positive_against_an_ordinary_baseline():
    """End-to-end sanity of the composition, on data whose answer is known."""
    # A DISPERSED baseline: sizes 1.0 .. 4.59 in 0.01 steps, so the 0.99
    # quantile lands strictly between observations rather than on a repeated
    # value (see the degeneracy test below for what happens when it does not).
    baseline = [mk(ts=T0 + timedelta(seconds=i * 10), price=100.0, qty=1.0 + i * 0.01, trade_id=i) for i in range(360)]
    whale_bar = [
        mk(ts=T0 + timedelta(hours=1, seconds=i), price=100.0, qty=1.0, trade_id=1000 + i) for i in range(50)
    ] + [mk(ts=T0 + timedelta(hours=1, minutes=30), price=100.0, qty=500.0, side="buy", trade_id=2000)]
    df = whale_bar_features(
        baseline + whale_bar, bar_seconds=3600, large_quantile=0.99, min_baseline_trades=200, min_bar_trades=10
    )
    row = df.iloc[1]
    assert row["whale_lt_count"] == 1.0, "only the whale clears the top-1% threshold"
    assert row["whale_lt_imbalance"] == pytest.approx(1.0)  # the one whale bought
    assert row["whale_cvd_delta"] == pytest.approx(50 * 100.0 + 500.0 * 100.0)
    # the bar's MEDIAN trade is an ordinary 100.0 against a baseline median of
    # ~279.5, so the size shift is negative even though a whale printed: (a) and
    # (c) are measuring different things, which is the point of using a median.
    assert row["whale_size_shift"] < 0.0


def test_a_threshold_landing_on_a_repeated_size_admits_every_copy():
    """
    The documented degeneracy, pinned so it stays a known property rather than
    becoming a surprise. A perfectly lumpy baseline puts tau exactly on the
    modal size, and `>=` then admits all of it. `whale_lt_count` vs
    `whale_trade_count` is the diagnostic that makes this visible.
    """
    baseline = [mk(ts=T0 + timedelta(seconds=i * 10), price=100.0, qty=1.0, trade_id=i) for i in range(360)]
    bar = [mk(ts=T0 + timedelta(hours=1, seconds=i), price=100.0, qty=1.0, trade_id=1000 + i) for i in range(50)]
    df = whale_bar_features(
        baseline + bar, bar_seconds=3600, large_quantile=0.99, min_baseline_trades=200, min_bar_trades=10
    )
    row = df.iloc[1]
    assert row["whale_lt_count"] == 50.0 == row["whale_trade_count"]
    assert row["whale_lt_imbalance"] == pytest.approx(1.0)
