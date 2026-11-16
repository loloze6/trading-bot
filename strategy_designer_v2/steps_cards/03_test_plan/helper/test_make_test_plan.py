"""Tests of step 3's code rules: the sizing block every config gets, and the windows of a period."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3] / "trading-bot"))
import make_test_plan as m  # noqa: E402
from strategies.registry import sizing_block_errors  # noqa: E402


def test_sizing_is_60_days_and_2_percent_a_day_on_any_bar_size():
    for bar, window in (("1d", 60), ("4h", 360), ("1h", 1440)):
        s = m.add_sizing({"strategies": {"regimes": {}}}, bar)["strategies"]["sizing"]
        assert s["window"] == window and s["periods_per_year"] == m.PERIODS_PER_YEAR[bar]
        assert math.isclose(s["target_annual_vol"], 0.02 * math.sqrt(365), rel_tol=1e-5)
        assert s["kind"] == "vol_target" and s["max_allocation"] == 2
        assert sizing_block_errors(s) == []


def test_sizing_overwrites_a_block_the_model_wrote():
    cfg = {"strategies": {"regimes": {}, "sizing": {"kind": "vol_target", "window": 5, "target_annual_vol": 9,
                                                    "periods_per_year": 365}}}
    assert m.add_sizing(cfg, "1d")["strategies"]["sizing"]["window"] == 60


def test_the_prompt_has_no_placeholder_left():
    assert "{{" not in (HERE / "system_prompt.md").read_text()
