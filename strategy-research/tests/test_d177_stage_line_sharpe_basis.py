"""D-177 -- the campaign log STAGE line names the basis and sample of median_sharpe.

Print only: _extract_run_numbers' numeric median_sharpe is unchanged.
"""
import sys
from pathlib import Path

import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_campaign as camp  # noqa: E402
import run_protocol as rp  # noqa: E402


def _seed(root: Path, sharpes: list) -> None:
    art = root / "runs" / "run_777" / "artifacts"
    art.mkdir(parents=True, exist_ok=True)
    results = [{"symbol": "BTCUSDT", "window": f"w{i}", "core": {"sharpe": s}}
               for i, s in enumerate(sharpes)]
    vals = [s for s in sharpes if s is not None]
    pss = {"BTCUSDT": {"median_sharpe": vals[0] if vals else None}}
    (art / "protocol_result.yaml").write_text(
        yaml.safe_dump({"results": results, "per_symbol_summary": pss}), encoding="utf-8")


def _stage_line(monkeypatch) -> str:
    lines = []
    monkeypatch.setattr(camp, "_log", lambda line, dry_run=False: lines.append(line))
    camp._log_transition({"id": "entry_x"}, "run_777",
                         {"pending_stage": "completed_refuted", "status": "completed"})
    return lines[0]


def test_stage_line_names_basis_and_one_of_six(monkeypatch):
    _seed(camp.ROOT, [7.033, None, None, None, None, None])
    line = _stage_line(monkeypatch)
    assert "median_sharpe=7.033 [" in line
    assert "per-window trade Sharpe" in line
    assert f"windows with >= {rp._SPARSE_TRADE_FLOOR} trades: 1 of 6" in line
    assert "mean over 1 symbol(s) with a value" in line


def test_numeric_field_unchanged_and_basis_key_not_printed(monkeypatch):
    _seed(camp.ROOT, [7.033, None, None, None, None, None])
    nums = camp._extract_run_numbers(camp.ROOT / "runs" / "run_777")
    assert nums["median_sharpe"] == 7.033
    assert "_sharpe_basis" in nums  # consumed (popped) by _log_transition only
    assert "_sharpe_basis" not in _stage_line(monkeypatch)


def test_no_value_keeps_todays_behaviour(monkeypatch):
    _seed(camp.ROOT, [None, None])
    line = _stage_line(monkeypatch)
    assert "median_sharpe" not in line
    assert "no scored artifacts yet" in line
