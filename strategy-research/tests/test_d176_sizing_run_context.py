"""
D-176 (e): the analyst's run context names the base config's strategies.sizing block, in one line,
when there is one; and says nothing when there is not (run_084's and run_099's configs carry none).

No LLM, no backtest.
"""
import json
import sys
from pathlib import Path

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402

FIXTURES = SR_ROOT / "tests" / "fixtures"
RUN_084 = FIXTURES / "d142" / "run_084_BTCUSD_2018-05" / "strategy_config.json"
RUN_099 = FIXTURES / "d176" / "run_099_strategy_config.json"
BLOCK = {"kind": "vol_target", "window": 60, "target_annual_vol": 0.2, "periods_per_year": 365,
         "max_allocation": 1.5}


def _run_dir(tmp_path, cfg):
    (tmp_path / "base.json").write_text(json.dumps(cfg), encoding="utf-8")
    return tmp_path


def _sizing_lines(text):
    return [x for x in text.split("\n") if x.startswith("sizing:")]


def test_a_sizing_block_adds_one_line_naming_it(tmp_path):
    cfg = json.loads(RUN_084.read_text())
    cfg["strategies"]["sizing"] = dict(BLOCK)
    lines = _sizing_lines(asm.run_context(_run_dir(tmp_path, cfg), "base.json", None))
    assert len(lines) == 1
    line = lines[0]
    for part in ("vol_target", "window=60", "target_annual_vol=0.2", "periods_per_year=365",
                 "max_allocation=1.5", "forecast column is the unsized signal"):
        assert part in line
    assert "(default)" not in line


def test_a_block_without_max_allocation_names_the_default(tmp_path):
    cfg = json.loads(RUN_084.read_text())
    cfg["strategies"]["sizing"] = {k: v for k, v in BLOCK.items() if k != "max_allocation"}
    [line] = _sizing_lines(asm.run_context(_run_dir(tmp_path, cfg), "base.json", None))
    assert "max_allocation=2.0 (default)" in line


def test_the_line_sits_before_the_config_section(tmp_path):
    cfg = json.loads(RUN_084.read_text())
    cfg["strategies"]["sizing"] = dict(BLOCK)
    text = asm.run_context(_run_dir(tmp_path, cfg), "base.json", None)
    assert text.index("sizing: vol_target") < text.index("## Base strategy config (base.json)")


def test_no_block_no_line_for_run_084_and_run_099(tmp_path):
    for name, path in (("a", RUN_084), ("b", RUN_099)):
        d = tmp_path / name
        d.mkdir()
        text = asm.run_context(_run_dir(d, json.loads(path.read_text())), "base.json", None)
        assert _sizing_lines(text) == []
        assert "sizing" not in text.split("## Base strategy config")[0]
        assert asm._sizing_line(path.read_text()) is None


def test_unreadable_or_odd_configs_give_no_line_and_no_crash(tmp_path):
    assert asm._sizing_line(None) is None
    assert asm._sizing_line("") is None
    assert asm._sizing_line("{not json") is None
    assert asm._sizing_line(json.dumps({"strategies": {"sizing": "vol_target"}})) is None
    assert asm._sizing_line(json.dumps({"strategies": None})) is None
    assert "(absent)" in asm.run_context(tmp_path, "missing.json", None)
