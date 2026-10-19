"""
signed_power transform op (registry.TRANSFORM_OPS_REGISTRY["signed_power"]), CUL-354.

    out = pivot * sign(v) * (|v| / pivot) ** exponent

Pins: the formula on hand-computed cases (exponent 1 is the identity; 5 / 10 / 15
at exponent 2; sign and zero survive; a non-default pivot); the operator bounds
(ruling 2026-10-19: 1 <= exponent <= 3, 10 <= pivot <= 20, inclusive; worst case
20 -> 80 at pivot 10, exponent 3; a non-finite input or output raises as in
vol_target); the param check (signed_power_param_errors) and that the op and V16
refuse exactly the same params; V16 refuses the op outside a strategies component's
`transforms` in a regime without `blocks` (the V14 pattern) but sets no position within
that list; V16 is silent for a config without the op; the op is a scalar op with a
min-periods entry of 1; and a pipeline without the op is unchanged.

All data is synthetic.
"""
import math

import numpy as np
import pandas as pd
import pytest
from strategies.registry import (
    HISTORY_OPS,
    SIGNED_POWER_BOUNDS,
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
    assert _op(0.0, {"exponent": 2.5, "pivot": 15}) == 0.0
    assert _op(0.0, {"exponent": 3, "pivot": 10}) == 0.0


@pytest.mark.parametrize("v", [float("nan"), float("inf"), float("-inf")])
def test_a_non_finite_input_raises(v):
    # fail loud, as vol_target: inside the pipeline this is the component error path
    with pytest.raises(ValueError, match="not finite"):
        _op(v, {"exponent": 2})


@pytest.mark.parametrize("v", [1e200, -1e200])
def test_a_huge_finite_input_whose_power_overflows_raises(v):
    # an unscaled raw value: (1e200 / 10) ** 2 overflows to +-inf, which is refused, not passed on
    with np.errstate(over="ignore"):
        with pytest.raises(ValueError, match="output is not finite"):
            _op(v, {"exponent": 2})


def test_a_fractional_exponent_at_the_default_pivot():
    assert _op(-5.0, {"exponent": 2.5}) == pytest.approx(-10 * (0.5 ** 2.5), abs=1e-12)  # about -1.7678


def test_a_non_default_pivot():
    # pivot 20: 20 * (20 / 20) ** 2 = 20 (the fixed point); 20 * (10 / 20) ** 2 = 5; 20 * (5 / 20) ** 2 = 1.25
    assert _op(20.0, {"exponent": 2, "pivot": 20}) == pytest.approx(20.0, abs=1e-12)
    assert _op(10.0, {"exponent": 2, "pivot": 20}) == pytest.approx(5.0, abs=1e-12)
    assert _op(-10.0, {"exponent": 2, "pivot": 20}) == pytest.approx(-5.0, abs=1e-12)
    assert _op(5.0, {"exponent": 2, "pivot": 20}) == pytest.approx(1.25, abs=1e-12)


def test_the_pivot_is_a_fixed_point_and_a_fractional_exponent_works():
    assert _op(15.0, {"exponent": 2.5, "pivot": 15}) == pytest.approx(15.0, abs=1e-12)
    # 15 * (6 / 15) ** 1.5
    assert _op(6.0, {"exponent": 1.5, "pivot": 15}) == pytest.approx(15 * 0.4 ** 1.5, abs=1e-12)
    # 10 * (4 / 10) ** 1.5
    assert _op(4.0, {"exponent": 1.5}) == pytest.approx(10 * 0.4 ** 1.5, abs=1e-12)


def test_the_worst_case_turns_20_into_80():
    # pivot 10 (the floor), exponent 3 (the ceiling): 10 * (20 / 10) ** 3 = 80, and the sign survives
    assert _op(20.0, {"exponent": 3, "pivot": 10}) == pytest.approx(80.0, abs=1e-9)
    assert _op(-20.0, {"exponent": 3, "pivot": 10}) == pytest.approx(-80.0, abs=1e-9)


def test_the_output_stays_within_80_over_the_whole_bounded_grid():
    # |v| <= 20 (standardise's cap) over the whole bounded (exponent, pivot) grid: finite, |out| <= 80
    worst = 0.0
    for exponent in np.linspace(1.0, 3.0, 21):
        for pivot in np.linspace(10.0, 20.0, 21):
            for v in np.linspace(-20.0, 20.0, 81):
                out = _op(float(v), {"exponent": float(exponent), "pivot": float(pivot)})
                assert math.isfinite(out) and -80.0 - 1e-9 <= out <= 80.0 + 1e-9, (exponent, pivot, v, out)
                worst = max(worst, abs(out))
    assert worst == pytest.approx(80.0, abs=1e-9)  # reached at pivot 10, exponent 3, |v| 20


def test_a_weak_value_shrinks_and_a_strong_one_grows():
    for v in (1.0, 4.0, 9.0):
        assert abs(_op(v, {"exponent": 2})) < v
    for v in (11.0, 15.0, 20.0):
        assert abs(_op(v, {"exponent": 2})) > v


def test_the_result_is_a_python_float():
    assert type(_op(5, {"exponent": 2})) is float


# --- param check ----------------------------------------------------------------

def test_valid_params_give_no_errors():
    for params in ({"exponent": 1}, {"exponent": 2}, {"exponent": 2.5, "pivot": 15},
                   {"exponent": 1.0, "pivot": 10}, {"exponent": 3, "pivot": 10},
                   {"exponent": 3, "pivot": 20}, {"exponent": 1.5, "pivot": 12.5}):
        assert signed_power_param_errors(params) == [], params


def test_the_bounds_constant_matches_the_ruling():
    assert SIGNED_POWER_BOUNDS == {"exponent": (1.0, 3.0), "pivot": (10.0, 20.0)}


# the exponent and pivot bounds are inclusive (operator ruling 2026-10-19)
@pytest.mark.parametrize("params", [
    {"exponent": 1}, {"exponent": 1.0}, {"exponent": 3}, {"exponent": 3.0},
    {"exponent": 2, "pivot": 10}, {"exponent": 2, "pivot": 10.0},
    {"exponent": 2, "pivot": 20}, {"exponent": 2, "pivot": 20.0},
    {"exponent": 1, "pivot": 10}, {"exponent": 3, "pivot": 20},
])
def test_the_bounds_are_inclusive(params):
    assert signed_power_param_errors(params) == []
    assert math.isfinite(_op(5.0, params))  # the op accepts them too


_EXP_MSG = "exponent must be a finite number with 1 <= exponent <= 3 (1 is the identity, above 3 over-amplifies), got "
_PIV_MSG = "pivot must be a finite number with 10 <= pivot <= 20 (the standardise target to its cap), got "


@pytest.mark.parametrize("params", [
    {"exponent": 0.999}, {"exponent": 3.001}, {"exponent": 0.999, "pivot": 15},
    {"exponent": 3.001, "pivot": 15}, {"exponent": 100},
])
def test_an_exponent_just_outside_the_bounds_is_refused(params):
    errors = signed_power_param_errors(params)
    assert len(errors) == 1 and errors[0].startswith(_EXP_MSG), errors
    with pytest.raises(ValueError, match="signed_power: exponent must be a finite number with 1 <= exponent <= 3"):
        _op(5.0, params)


@pytest.mark.parametrize("params", [
    {"exponent": 2, "pivot": 9.999}, {"exponent": 2, "pivot": 20.001},
    {"exponent": 2, "pivot": 8}, {"exponent": 2, "pivot": 5}, {"exponent": 2, "pivot": 0.001},
    {"exponent": 2, "pivot": 100},
])
def test_a_pivot_just_outside_the_bounds_is_refused(params):
    errors = signed_power_param_errors(params)
    assert len(errors) == 1 and errors[0].startswith(_PIV_MSG), errors
    with pytest.raises(ValueError, match="signed_power: pivot must be a finite number with 10 <= pivot <= 20"):
        _op(5.0, params)


@pytest.mark.parametrize("params,fragment", [
    ({}, "missing param 'exponent'"),
    ({"pivot": 10}, "missing param 'exponent'"),
    ({"exponent": 0.99}, _EXP_MSG),
    ({"exponent": 0}, _EXP_MSG),
    ({"exponent": -2}, _EXP_MSG),
    ({"exponent": 3.5}, _EXP_MSG),
    ({"exponent": True}, _EXP_MSG),
    ({"exponent": False}, _EXP_MSG),
    ({"exponent": "2"}, _EXP_MSG),
    ({"exponent": None}, _EXP_MSG),
    ({"exponent": float("inf")}, _EXP_MSG),
    ({"exponent": float("nan")}, _EXP_MSG),
    ({"exponent": 2, "pivot": 0}, _PIV_MSG),
    ({"exponent": 2, "pivot": -5}, _PIV_MSG),
    ({"exponent": 2, "pivot": 5}, _PIV_MSG),
    ({"exponent": 2, "pivot": 25}, _PIV_MSG),
    ({"exponent": 2, "pivot": "10"}, _PIV_MSG),
    ({"exponent": 2, "pivot": True}, _PIV_MSG),
    ({"exponent": 2, "pivot": None}, _PIV_MSG),
    ({"exponent": 2, "pivot": float("inf")}, _PIV_MSG),
    ({"exponent": 2, "pivot": float("nan")}, _PIV_MSG),
])
def test_param_check_refuses(params, fragment):
    errors = signed_power_param_errors(params)
    assert len(errors) == 1 and fragment in errors[0], errors


@pytest.mark.parametrize("params", [None, [], [("exponent", 2)], "exponent", 2, 2.0])
def test_param_check_refuses_a_non_mapping(params):
    errors = signed_power_param_errors(params)
    assert len(errors) == 1 and errors[0].startswith("params must be a mapping, got "), errors


def test_param_check_lists_both_problems():
    errors = signed_power_param_errors({"exponent": 0.5, "pivot": 5})
    assert len(errors) == 2
    assert errors[0].startswith(_EXP_MSG) and errors[1].startswith(_PIV_MSG)
    assert len(signed_power_param_errors({"exponent": 4, "pivot": 25})) == 2


_BAD = [{}, {"pivot": 10}, {"exponent": 0.5}, {"exponent": 3.5}, {"exponent": True}, {"exponent": "2"},
        {"exponent": float("inf")}, {"exponent": float("nan")}, {"exponent": 2, "pivot": 0},
        {"exponent": 2, "pivot": -1}, {"exponent": 2, "pivot": 5}, {"exponent": 2, "pivot": 20.5},
        {"exponent": 2, "pivot": "x"}, {"exponent": 2, "pivot": float("nan")}]


@pytest.mark.parametrize("params", _BAD)
def test_the_op_raises_value_error_on_invalid_params(params):
    with pytest.raises(ValueError, match="signed_power"):
        _op(5.0, params)


@pytest.mark.parametrize("params", [None, [], "x"])
def test_the_op_raises_value_error_on_non_dict_params(params):
    with pytest.raises(ValueError, match="signed_power"):
        _op(5.0, params)


def test_the_op_error_carries_the_param_check_messages():
    params = {"exponent": 0.5, "pivot": 5}
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
    assert validate(_full([STD, {"op": "signed_power", "params": {"exponent": 2.5, "pivot": 15}},
                           {"op": "clip", "params": {"min": -20, "max": 20}}])) == []
    # the bounds themselves are valid
    for params in ({"exponent": 1, "pivot": 10}, {"exponent": 3, "pivot": 10},
                   {"exponent": 1, "pivot": 20}, {"exponent": 3, "pivot": 20}):
        assert validate(_full([STD, {"op": "signed_power", "params": params}])) == [], params


@pytest.mark.parametrize("params", [
    {"exponent": 0.999}, {"exponent": 3.001}, {"exponent": 2, "pivot": 9.999},
    {"exponent": 2, "pivot": 20.001}, {"exponent": 4, "pivot": 5},
])
def test_v16_reports_a_bound_violation(params):
    got = _v(validate(_full([STD, {"op": "signed_power", "params": params}])), "V16")
    assert got == [f"VIOLATION V16 {LOC}: {m}" for m in signed_power_param_errors(params)]
    assert 1 <= len(got) <= 2


def test_v16_reports_exactly_what_the_param_check_refuses():
    for params in _BAD + [None, [], "x"]:
        step = {"op": "signed_power"} if params is None else {"op": "signed_power", "params": params}
        got = _v(validate(_full([STD, step])), "V16")
        expected = [f"VIOLATION V16 {LOC}: {m}" for m in signed_power_param_errors(
            {} if params is None else params)]
        assert got == expected, params


def test_v16_line_format():
    assert _v(validate(_full([STD, {"op": "signed_power", "params": {"exponent": 0.5, "pivot": 0}}])), "V16") == [
        f"VIOLATION V16 {LOC}: exponent must be a finite number with 1 <= exponent <= 3 "
        "(1 is the identity, above 3 over-amplifies), got 0.5",
        f"VIOLATION V16 {LOC}: pivot must be a finite number with 10 <= pivot <= 20 "
        "(the standardise target to its cap), got 0",
    ]
    assert _v(validate(_full([STD, {"op": "signed_power"}])), "V16") == [
        f"VIOLATION V16 {LOC}: missing param 'exponent'"]


def test_v16_refuses_history_transforms_and_still_checks_its_params():
    # placement rule (operator ruling 2026-10-19, the V14 pattern); the params are
    # still checked there, as V14 does for vol_target
    cfg = _full([{"op": "signed_power", "params": {"exponent": 0}}], key="history_transforms")
    assert _v(validate(cfg), "V16") == [
        "VIOLATION V16 strategies.regimes.unknown.components[0].history_transforms[0]: "
        "signed_power is allowed only in a strategies component's `transforms`, in a regime "
        "without `blocks` (a value it refuses raises there, inside generate_signals' guard)",
        "VIOLATION V16 strategies.regimes.unknown.components[0].history_transforms[0].params: "
        "exponent must be a finite number with 1 <= exponent <= 3 "
        "(1 is the identity, above 3 over-amplifies), got 0"]


def test_v16_is_silent_without_the_op():
    for transforms in ([STD], [STD, {"op": "negate"}],
                       [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 5}}],
                       [{"op": "zscore"}, {"op": "clip", "params": {"min": -2, "max": 2}}]):
        assert _v(validate(_full(transforms)), "V16") == []
    assert validate(_full([STD, {"op": "clip", "params": {"min": -10, "max": 10}}])) == []


def test_v16_has_no_position_rule_within_transforms():
    # placement is ruled (strategies `transforms`, no `blocks`), the position in the list
    # is not: signed_power before standardise is a V5 matter (a history op after a scalar
    # op), not V16
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
