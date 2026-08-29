"""
Unit tests for risk/portfolio_risk_gate.py (fix/risk-layer, PR-1).

Covers the absolute_allocation_cap clamp, the shared validate_portfolio_controls
rule set (fail-loud on bad shapes / ranges / unknown keys), and the gate ctor's
defense-in-depth validation. Pure units -- no backtest, no I/O. The end-to-end
bit-identity and cap-bite-through-the-engine contracts live in
tests/test_risk_layer_bit_identical.py.

No-lookahead rationale (hard rule 3): PortfolioRiskGate.apply reads ONLY its
`target_allocation` argument, which is this bar's forecast->allocation output
(core/trading_bot.py:225, derived from data timestamped <= this bar's close). It
holds no prior-bar or future state in PR-1, so it cannot introduce look-ahead by
construction; test_apply_is_pure_function_of_its_argument pins that (same cap,
same input -> same output, independent of call order/history).
"""

from pathlib import Path

import pytest

from risk.portfolio_risk_gate import PortfolioRiskGate, validate_portfolio_controls

# pytest.ini sets pythonpath = ., so trading-bot/ is importable without a sys.path hack.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

pytestmark = pytest.mark.unit


# --- validate_portfolio_controls ---


def test_empty_block_is_valid():
    assert validate_portfolio_controls({}) == []


def test_valid_cap_block_is_valid():
    assert validate_portfolio_controls({"absolute_allocation_cap": {"cap": 1.0}}) == []


def test_non_dict_block_fails():
    errs = validate_portfolio_controls([("absolute_allocation_cap", 1.0)])
    assert len(errs) == 1 and "must be a dict" in errs[0]


def test_unknown_control_key_fails():
    # max_drawdown_kill is a PR-2 control -- unknown in PR-1, must fail loud rather
    # than silently arm a do-nothing kill switch.
    errs = validate_portfolio_controls({"max_drawdown_kill": {"threshold": 0.25}})
    assert any("unknown portfolio_controls key" in e for e in errs)


def test_unknown_cap_subkey_fails():
    errs = validate_portfolio_controls({"absolute_allocation_cap": {"capp": 1.0}})
    # "capp" is unknown AND "cap" is missing -> two distinct fail-loud signals.
    assert any("unknown absolute_allocation_cap key" in e for e in errs)
    assert any('requires a "cap"' in e for e in errs)


def test_cap_must_be_present():
    errs = validate_portfolio_controls({"absolute_allocation_cap": {}})
    assert any('requires a "cap"' in e for e in errs)


@pytest.mark.parametrize("bad", [0, -1.0, float("inf"), float("nan"), "1.0", True, None])
def test_cap_value_range_and_type(bad):
    errs = validate_portfolio_controls({"absolute_allocation_cap": {"cap": bad}})
    assert any("finite number > 0" in e for e in errs), f"{bad!r} should be rejected"


def test_cap_subblock_must_be_dict():
    errs = validate_portfolio_controls({"absolute_allocation_cap": 1.0})
    assert any("must be a dict" in e for e in errs)


# --- gate ctor ---


def test_ctor_rejects_invalid_config():
    with pytest.raises(ValueError, match="invalid portfolio_controls"):
        PortfolioRiskGate({"absolute_allocation_cap": {"cap": -1.0}})


def test_ctor_stores_effective_config_verbatim():
    cfg = {"absolute_allocation_cap": {"cap": 0.75}}
    gate = PortfolioRiskGate(cfg)
    assert gate.config == cfg
    # a copy, not the caller's dict (mutating the source must not change provenance)
    cfg["absolute_allocation_cap"]["cap"] = 9.0
    assert gate.config["absolute_allocation_cap"]["cap"] == 0.75


def test_ctor_no_cap_leaves_cap_none():
    gate = PortfolioRiskGate({})
    assert gate.cap is None


# --- apply: the cap clamp ---


def test_cap_clamps_positive_over_limit():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    # forecast +20 -> target +2.0 (the /10 map's default max) -> clamped to +1.0
    final, extras = gate.apply(2.0)
    assert final == 1.0
    assert extras == {"risk_target_raw": 2.0, "risk_cap_clamped": True}


def test_cap_clamps_negative_over_limit():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    final, extras = gate.apply(-2.0)
    assert final == -1.0
    assert extras["risk_cap_clamped"] is True


def test_cap_passes_target_within_limit_untouched():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    final, extras = gate.apply(0.5)
    assert final == 0.5
    assert extras == {"risk_target_raw": 0.5, "risk_cap_clamped": False}


def test_cap_boundary_is_not_clamped():
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    final, extras = gate.apply(1.0)
    assert final == 1.0
    assert extras["risk_cap_clamped"] is False


def test_apply_raises_on_nan_target():
    # Fail-loud on degenerate input: a NaN target would pass any clamp unchanged and
    # mislabel risk_cap_clamped True (nan != nan). Raises with or without a cap.
    for cfg in ({"absolute_allocation_cap": {"cap": 1.0}}, {}):
        gate = PortfolioRiskGate(cfg)
        with pytest.raises(ValueError, match="NaN target_allocation"):
            gate.apply(float("nan"))


def test_apply_clamps_inf_target_when_capped():
    # inf is NOT rejected -- the cap clamps it (reviewer-blessed). Guards against the
    # NaN check being widened to reject all non-finite values.
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    assert gate.apply(float("inf"))[0] == 1.0
    assert gate.apply(float("-inf"))[0] == -1.0


def test_apply_no_cap_is_identity():
    gate = PortfolioRiskGate({})
    final, extras = gate.apply(2.0)
    assert final == 2.0
    assert extras == {"risk_target_raw": 2.0, "risk_cap_clamped": False}


def test_apply_is_pure_function_of_its_argument():
    # No-lookahead / statelessness pin: repeated and interleaved calls never let one
    # bar's target influence another's result.
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 1.0}})
    assert gate.apply(2.0)[0] == 1.0
    assert gate.apply(0.3)[0] == 0.3
    assert gate.apply(2.0)[0] == 1.0
    assert gate.apply(-5.0)[0] == -1.0


# --- provenance fold recipe (pure, no backtest) ---


def test_provenance_fold_changes_run_hash(tmp_path):
    """The 8-char config hash new_run_dir stamps on a run dir must differ once the
    risk_management block is folded in, and be deterministic for a fixed config -- the
    property the gate-on/gate-off distinguishability contract rests on."""
    from reporting.run_artifact import new_run_dir

    cfg = {"strategies": {"a": 1}, "regime_detector": {"b": 2}}
    folded = {
        **cfg,
        "risk_management": {"portfolio_controls": {"absolute_allocation_cap": {"cap": 1.0}}},
    }

    def _hash(root, c):
        return new_run_dir(str(tmp_path / root), c).name.split("_")[-1]

    h_base = _hash("a", cfg)
    h_base_again = _hash("b", cfg)
    h_folded = _hash("c", folded)

    assert h_base == h_base_again  # deterministic recipe
    assert h_base != h_folded  # the fold moves run identity


# --- validation wired into both entry points ---


def test_config_manager_validate_rejects_bad_portfolio_controls():
    """ConfigManager.validate (the config.json entry point) fails loud on a bad
    portfolio_controls block. Mutation: drop the validate_portfolio_controls call in
    settings.py -> this returns True."""
    from config.settings import ConfigManager

    cm = ConfigManager("config.json")
    cm.config = {
        "trading": {"symbols": ["BTCUSDT"]},
        "risk_management": {"portfolio_controls": {"absolute_allocation_cap": {"cap": -1.0}}},
    }
    assert cm.validate() is False

    cm.config["risk_management"]["portfolio_controls"] = {"absolute_allocation_cap": {"cap": 1.0}}
    assert cm.validate() is True


def test_run_backtest_rejects_bad_risk_controls_override(tmp_path):
    """run_backtest (the override entry point) raises fail-loud BEFORE any data load on
    an invalid risk_controls dict -- the override bypasses ConfigManager.validate, so it
    validates independently."""
    from core.launcher import run_backtest

    with pytest.raises(ValueError, match="Invalid risk_controls override"):
        run_backtest(
            config_path=str(PROJECT_ROOT / "strategy_config.json"),
            symbol="BTCUSDT",
            start="2024-04-01",
            end="2024-05-30",
            results_root=str(tmp_path),
            trades_log_file=str(tmp_path / "t.json"),
            risk_controls={"absolute_allocation_cap": {"cap": 0}},
        )
