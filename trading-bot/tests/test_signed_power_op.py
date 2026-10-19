"""
signed_power transform op (registry.TRANSFORM_OPS_REGISTRY["signed_power"]), CUL-354.

    out = pivot * sign(v) * (|v| / pivot) ** exponent

Pins: the formula on hand-computed cases (exponent 1 is the identity; 5 / 10 / 15
at exponent 2; sign and zero survive; a non-default pivot); the param check
(signed_power_param_errors) and that the op and V16 refuse exactly the same
params; V16 is silent for a config without the op; the op is a scalar op with a
min-periods entry of 1; and a pipeline without the op is unchanged.

All data is synthetic.
"""
import math

import numpy as np
import pandas as pd
import pytest
from strategies.registry import (
    HISTORY_OPS,
    TRANSFORM_MIN_PERIODS,
    TRANSFORM_OPS_REGISTRY,
    apply_transform_pipeline,
    signed_power_param_errors,
    transform_min_periods,
)
from tools.validate_config import validate

SMA = "strategies.strategy_components.SmaTrendLongOnlyComponent"
UNGATED = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}
H = pd.Series([1.0, -2.0, 3.0, 0.5, 4.0])  # the op ignores the history


def _op(v, params):
    return TRANSFORM_OPS_REGISTRY["signed_power"](v, H, params, None)


# --- formula, hand computed ---------------------------------------------------

@pytest.mark.parametrize("v", [-19.0, -10.0, -5.0, -0.3, 0.0, 0.3, 5.0, 10.0, 15.0, 20.0])
def test_exponent_one_is_the_identity(v):
    assert _op(v, {"exponent": 1}) == pytest.approx(v, abs=1e-12)


@pytest.mark.parametrize("v,expected", [(5.0, 2.5), (10.0, 10.0), (15.0, 22.5)])
def test_exponent_two_at_the_default_pivot(v, expected):
    # 10 * (|v| / 10) ** 2
    assert _op(v, {"exponent": 2}) == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize("v,expected", [(-5.0, -2.5), (-10.0, -10.0), (-15.0, -22.5)])
def test_the_sign_is_preserved(v, expected):
    assert _op(v, {"exponent": 2}) == pytest.approx(expected, abs=1e-12)


def test_zero_stays_zero():
    assert _op(0.0, {"exponent": 2}) == 0.0
    assert _op(0.0, {"exponent": 3.5, "pivot": 4}) == 0.0


@pytest.mark.parametrize(
    "v,exponent,expected",
    [
        (float("nan"), 2, float("nan")),
        (float("inf"), 2, float("inf")),
        (float("-inf"), 2, float("-inf")),
        (-5.0, 2.5, -10 * (0.5 ** 2.5)),  # about -1.7678
        (1e200, 2, float("inf")),  # overflows to +inf, no exception
    ],
)
def test_edge_values_at_the_default_pivot(v, exponent, expected):
    with np.errstate(over="ignore"):
        out = _op(v, {"exponent": exponent})
    if math.isnan(expected):
        assert math.isnan(out)
    elif math.isinf(expected):
        assert out == expected
    else:
        assert out == pytest.approx(expected, abs=1e-12)


def test_a_non_default_pivot():
    # 5 * (10 / 5) ** 2 = 20; 5 * (2.5 / 5) ** 2 = 1.25
    assert _op(10.0, {"exponent": 2, "pivot": 5}) == pytest.approx(20.0, abs=1e-12)
    assert _op(-10.0, {"exponent": 2, "pivot": 5}) == pytest.approx(-20.0, abs=1e-12)
    assert _op(2.5, {"exponent": 2, "pivot": 5}) == pytest.approx(1.25, abs=1e-12)


def test_the_pivot_is_a_fixed_point_and_a_fractional_exponent_works():
    assert _op(7.0, {"exponent": 2.5, "pivot": 7}) == pytest.approx(7.0, abs=1e-12)
    # 10 * (4 / 10) ** 1.5
    assert _op(4.0, {"exponent": 1.5}) == pytest.approx(10 * 0.4 ** 1.5, abs=1e-12)


def test_a_weak_value_shrinks_and_a_strong_one_grows():
    for v in (1.0, 4.0, 9.0):
        assert abs(_op(v, {"exponent": 2})) < v
    for v in (11.0, 15.0, 20.0):
        assert abs(_op(v, {"exponent": 2})) > v


def test_the_result_is_a_python_float():
    assert type(_op(5, {"exponent": 2})) is float


# --- param check ----------------------------------------------------------------

def test_valid_params_give_no_errors():
    for params in ({"exponent": 1}, {"exponent": 2}, {"exponent": 2.5, "pivot": 5},
                   {"exponent": 1.0, "pivot": 0.001}, {"exponent": 3, "pivot": 10}):
        assert signed_power_param_errors(params) == [], params


@pytest.mark.parametrize("params,fragment", [
    ({}, "missing param 'exponent'"),
    ({"pivot": 10}, "missing param 'exponent'"),
    ({"exponent": 0.99}, "exponent must be a finite number >= 1"),
    ({"exponent": 0}, "exponent must be a finite number >= 1"),
    ({"exponent": -2}, "exponent must be a finite number >= 1"),
    ({"exponent": True}, "exponent must be a finite number >= 1"),
    ({"exponent": False}, "exponent must be a finite number >= 1"),
    ({"exponent": "2"}, "exponent must be a finite number >= 1"),
    ({"exponent": None}, "exponent must be a finite number >= 1"),
    ({"exponent": float("inf")}, "exponent must be a finite number >= 1"),
    ({"exponent": float("nan")}, "exponent must be a finite number >= 1"),
    ({"exponent": 2, "pivot": 0}, "pivot must be a finite number > 0"),
    ({"exponent": 2, "pivot": -5}, "pivot must be a finite number > 0"),
    ({"exponent": 2, "pivot": "10"}, "pivot must be a finite number > 0"),
    ({"exponent": 2, "pivot": True}, "pivot must be a finite number > 0"),
    ({"exponent": 2, "pivot": None}, "pivot must be a finite number > 0"),
    ({"exponent": 2, "pivot": float("inf")}, "pivot must be a finite number > 0"),
    ({"exponent": 2, "pivot": float("nan")}, "pivot must be a finite number > 0"),
])
def test_param_check_refuses(params, fragment):
    errors = signed_power_param_errors(params)
    assert len(errors) == 1 and fragment in errors[0], errors


@pytest.mark.parametrize("params", [None, [], [("exponent", 2)], "exponent", 2, 2.0])
def test_param_check_refuses_a_non_mapping(params):
    errors = signed_power_param_errors(params)
    assert len(errors) == 1 and errors[0].startswith("params must be a mapping, got "), errors


def test_param_check_lists_both_problems():
    errors = signed_power_param_errors({"exponent": 0.5, "pivot": -1})
    assert len(errors) == 2


_BAD = [{}, {"pivot": 10}, {"exponent": 0.5}, {"exponent": True}, {"exponent": "2"},
        {"exponent": float("inf")}, {"exponent": float("nan")}, {"exponent": 2, "pivot": 0},
        {"exponent": 2, "pivot": -1}, {"exponent": 2, "pivot": "x"}, {"exponent": 2, "pivot": float("nan")}]


@pytest.mark.parametrize("params", _BAD)
def test_the_op_raises_value_error_on_invalid_params(params):
    with pytest.raises(ValueError, match="signed_power"):
        _op(5.0, params)


@pytest.mark.parametrize("params", [None, [], "x"])
def test_the_op_raises_value_error_on_non_dict_params(params):
    with pytest.raises(ValueError, match="signed_power"):
        _op(5.0, params)


def test_the_op_error_carries_the_param_check_messages():
    params = {"exponent": 0.5, "pivot": -1}
    with pytest.raises(ValueError) as ei:
        _op(5.0, params)
    for msg in signed_power_param_errors(params):
        assert msg in str(ei.value)


def test_the_pipeline_raises_on_invalid_params():
    with pytest.raises(ValueError, match="signed_power"):
        apply_transform_pipeline(H, [{"op": "scale", "params": {"factor": 1}}, {"op": "signed_power"}])


# --- V16 ------------------------------------------------------------------------

def _full(transforms, key="transforms"):
    return {"regime_detector": UNGATED, "strategies": {"regimes": {
        "unknown": {"components": [{"id": "s", "class": SMA, "params": {"lookback_L": 50},
                                    "weight": 1.0, key: transforms}]},
        "trending": None, "mean_reversion": None, "chop": None}}}


def _v(violations, code):
    return [v for v in violations if v.startswith(f"VIOLATION {code}")]


LOC = "strategies.regimes.unknown.components[0].transforms[1].params"
STD = {"op": "standardise", "params": {"window": 20, "min_periods": 5}}


def test_v16_valid_params_give_no_violation():
    assert validate(_full([STD, {"op": "signed_power", "params": {"exponent": 2}}])) == []
    assert validate(_full([STD, {"op": "signed_power", "params": {"exponent": 2.5, "pivot": 5}},
                           {"op": "clip", "params": {"min": -20, "max": 20}}])) == []


def test_v16_reports_exactly_what_the_param_check_refuses():
    for params in _BAD + [None, [], "x"]:
        step = {"op": "signed_power"} if params is None else {"op": "signed_power", "params": params}
        got = _v(validate(_full([STD, step])), "V16")
        expected = [f"VIOLATION V16 {LOC}: {m}" for m in signed_power_param_errors(
            {} if params is None else params)]
        assert got == expected, params


def test_v16_line_format():
    assert _v(validate(_full([STD, {"op": "signed_power", "params": {"exponent": 0.5, "pivot": 0}}])), "V16") == [
        f"VIOLATION V16 {LOC}: exponent must be a finite number >= 1, got 0.5",
        f"VIOLATION V16 {LOC}: pivot must be a finite number > 0, got 0",
    ]
    assert _v(validate(_full([STD, {"op": "signed_power"}])), "V16") == [
        f"VIOLATION V16 {LOC}: missing param 'exponent'"]


def test_v16_also_checks_history_transforms():
    cfg = _full([{"op": "signed_power", "params": {"exponent": 0}}], key="history_transforms")
    assert _v(validate(cfg), "V16") == [
        "VIOLATION V16 strategies.regimes.unknown.components[0].history_transforms[0].params: "
        "exponent must be a finite number >= 1, got 0"]


def test_v16_is_silent_without_the_op():
    for transforms in ([STD], [STD, {"op": "negate"}],
                       [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 5}}],
                       [{"op": "zscore"}, {"op": "clip", "params": {"min": -2, "max": 2}}]):
        assert _v(validate(_full(transforms)), "V16") == []
    assert validate(_full([STD, {"op": "clip", "params": {"min": -10, "max": 10}}])) == []


def test_v16_has_no_placement_rule_for_a_scalar_op():
    # signed_power before standardise is a V5 matter (a history op after a scalar op), not V16
    got = validate(_full([{"op": "signed_power", "params": {"exponent": 2}}, STD]))
    assert _v(got, "V16") == []
    assert _v(got, "V5")


# --- registry membership ----------------------------------------------------------

def test_the_op_is_registered_and_scalar():
    assert "signed_power" in TRANSFORM_OPS_REGISTRY
    assert "signed_power" not in HISTORY_OPS


def test_transform_min_periods_is_one():
    assert TRANSFORM_MIN_PERIODS["signed_power"] == 1
    assert transform_min_periods("signed_power", {"exponent": 2}) == 1
    assert transform_min_periods("signed_power", {}) == 1


def test_pipeline_after_standardise_then_signed_power():
    # past = [1, -2, 3, -4] -> mean |past| = 2.5; current 2 -> standardise 8.0; then 10 * (0.8) ** 2 = 6.4
    h = pd.Series([1.0, -2.0, 3.0, -4.0, 2.0])
    steps = [{"op": "standardise", "params": {"window": 4, "min_periods": 2}},
             {"op": "signed_power", "params": {"exponent": 2}}]
    assert apply_transform_pipeline(h, steps) == pytest.approx(6.4, abs=1e-12)
    h = pd.Series([1.0, -2.0, 3.0, -4.0, -2.0])
    assert apply_transform_pipeline(h, steps) == pytest.approx(-6.4, abs=1e-12)


# --- configs without the op are unchanged -------------------------------------------

def test_pipelines_without_the_op_are_unchanged():
    h = pd.Series([1.0, -2.0, 3.0, 0.5, 4.0])
    assert apply_transform_pipeline(h, [{"op": "ratio_to_mean"}]) == 4.0 / h.abs().mean()
    z = (4.0 - h.mean()) / h.std()
    assert apply_transform_pipeline(h, [{"op": "zscore"}, {"op": "scale", "params": {"factor": 10}}]) \
        == pytest.approx(10 * z, abs=0)
    # identity -> 4.0, negate -> -4.0, clip to [-3, 3] -> -3.0
    assert apply_transform_pipeline(h, [{"op": "identity"}, {"op": "negate"},
                                        {"op": "clip", "params": {"min": -3, "max": 3}}]) == -3.0


def test_every_other_scalar_op_value_is_unchanged_by_the_new_entry():
    rng = np.random.default_rng(3)
    h = pd.Series(rng.normal(0, 3, 50))
    params = {"factor": 3, "min_abs": 1, "min": -2, "max": 2}
    for op in ("scale", "threshold_filter", "clip", "sigmoid", "negate"):
        for v in (-7.5, -0.4, 0.0, 0.4, 7.5):
            out = TRANSFORM_OPS_REGISTRY[op](v, h, params, None)
            expected = {"scale": v * 3, "threshold_filter": v if abs(v) >= 1 else 0.0,
                        "clip": min(max(v, -2), 2), "sigmoid": 1 / (1 + math.exp(-v)), "negate": -v}[op]
            assert out == pytest.approx(expected, abs=1e-12), (op, v)
