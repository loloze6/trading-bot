"""D-141 (direction ruling 2026-10-15; D-101 applied to D-121's grid path): a variant whose
account was ruined (equity <= 0 after a positive peak, no liquidation in the engine) FAILs the
menu criterion whole_test_sharpe_positive, with the ruin recorded in the cell. Before, the
PortfolioRuined raised by tools/portfolio_daily.py escaped run_phase1_research.
_with_whole_test_sharpe (which caught PortfolioNotEvaluable only) and halted the stage; run_096's
asset_XRPUSDT was the case. The two rejected alternatives both read a measured loss as unknown:
value None -> INCONCLUSIVE, or "failed, not graded".

Fixtures (tests/fixtures/d141/, equity and close columns only, copied as they are):
  run_095_base/            run_095's `base` variant: six windows, no ruin (byte-identity)
  run_096_asset_XRPUSDT/   run_096's asset_XRPUSDT: window 1 (first rows) and window 2 up to
                           just past the ruin; windows 3-6 are never reached, load_windows
                           raises on window 2.
"""
from __future__ import annotations

import copy
import csv
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import workflow_artifact_validation as wav  # noqa: E402

MENU = yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
FIX = SR / "tests" / "fixtures" / "d141"
CID = "whole_test_sharpe_positive"

# What master (origin/master ec7efd26, before this change) computes on the run_095 fixture,
# measured by running master's own _with_whole_test_sharpe + evaluate_grid on it.
MASTER_SHARPE = -1.0306224217274345
MASTER_CELL = {"result": "FAIL", "value": MASTER_SHARPE, "threshold": 0.0, "comparator": ">",
               "n_windows": 6, "n_trades": 0}
MASTER_DIAGNOSTICS = {"median_gross_pnl": -289.2967, "whole_test_sharpe": MASTER_SHARPE}


def _rule():
    return rpr._pass_rule_from_menu_ids({"criteria": [{"id": CID}]}, MENU)


def _fixture_pr(name: str) -> tuple:
    d = FIX / name
    pr = {"results": json.loads((d / "results.json").read_text(encoding="utf-8")),
          "hypothesis_verdict": {"verdict": None, "diagnostics": {"median_gross_pnl": -289.2967}}}
    if (d / "protocol.json").exists():
        pr["protocol_file"] = str(d / "protocol.json")
    return d, pr


def _grade(summaries: dict, run_dir: Path) -> tuple:
    rule = _rule()
    injected = rpr._with_whole_test_sharpe(summaries, run_dir, rule)
    grid = vce.evaluate_grid(injected, {"pass_rule": rule}, {}, MENU)
    return injected, grid


def _write_window(run_dir: Path, run_id: str, equities: list) -> Path:
    path = run_dir / "results" / run_id / "portfolio_states.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["timestamp", "close", "regime", "total_portfolio_value",
                    "postRebalance_total_value"])
        for i, eq in enumerate(equities):
            w.writerow([f"2020-{1 + i // 28:02d}-{1 + i % 28:02d}", 100.0 + i, "unknown",
                        eq, eq])
    return path


def _ruined_equities(ruin_equity: float = -50.0) -> list:
    return [1000.0 + 10.0 * i for i in range(30)] + [900.0, 400.0, ruin_equity, -80.0]


def _single_window_pr(run_id: str = "r1") -> dict:
    return {"results": [{"symbol": "XRPUSD", "window": "w1", "run_id": run_id}],
            "hypothesis_verdict": {"diagnostics": {}}}


# -- (a) byte-identity: no ruin, nothing new is written anywhere -----------------------------


def test_no_ruin_is_byte_identical_to_master_on_run_095_windows():
    d, pr = _fixture_pr("run_095_base")
    before = copy.deepcopy(pr)
    injected, grid = _grade({"base": pr}, d)
    diag = injected["base"]["hypothesis_verdict"]["diagnostics"]
    assert diag == MASTER_DIAGNOSTICS                       # same number, no ruin key
    assert diag["whole_test_sharpe"] == MASTER_SHARPE       # exact, not approx
    assert vce.WHOLE_TEST_SHARPE_RUIN_KEY not in diag
    cell = grid["grid"][CID]["base"]
    assert cell == MASTER_CELL                              # no detail, no reason, nothing new
    assert "detail" not in cell and "reason" not in cell
    assert grid["idea_status"] == "refuted"                 # as on master (a Sharpe below 0)
    assert pr == before                                     # the input summary is not touched


def test_no_ruin_summary_differs_from_input_only_by_the_one_diagnostic():
    d, pr = _fixture_pr("run_095_base")
    out = rpr._with_whole_test_sharpe({"base": pr}, d, _rule())["base"]
    expected = copy.deepcopy(pr)
    expected["hypothesis_verdict"]["diagnostics"]["whole_test_sharpe"] = MASTER_SHARPE
    assert out == expected


def test_a_rule_without_the_criterion_still_returns_the_summaries_untouched(tmp_path):
    summaries = {"base": {"results": []}}
    rule = {"criteria": [{"id": "sign_consistent_by_era", "metric": "net_return_pct"}]}
    assert rpr._with_whole_test_sharpe(summaries, tmp_path, rule) is summaries


def test_the_two_modules_spell_the_metric_and_the_ruin_key_alike():
    assert rpr._WHOLE_TEST_SHARPE_METRIC == vce.WHOLE_TEST_SHARPE_METRIC == "whole_test_sharpe"
    assert rpr._WHOLE_TEST_SHARPE_RUIN_KEY == vce.WHOLE_TEST_SHARPE_RUIN_KEY \
        == "whole_test_sharpe_ruin"


# -- (b) a ruined window grades FAIL with the ruin recorded ----------------------------------


def test_a_ruined_window_fails_with_the_ruin_in_the_cell(tmp_path):
    path = _write_window(tmp_path, "r1", _ruined_equities(-50.0))
    pr = _single_window_pr()
    injected, grid = _grade({"v": pr}, tmp_path)            # nothing raises
    ruin = {"file": str(path), "timestamp": "2020-02-05", "equity": -50.0}
    diag = injected["v"]["hypothesis_verdict"]["diagnostics"]
    assert diag["whole_test_sharpe"] is None                # no fake number
    assert diag["whole_test_sharpe_ruin"] == ruin
    cell = grid["grid"][CID]["v"]
    assert cell["result"] == "FAIL"
    assert cell["value"] is None
    assert cell["detail"] == {"ruin": ruin}
    assert cell["threshold"] == 0.0 and cell["comparator"] == ">"
    assert cell["n_windows"] == 1 and cell["n_trades"] == 0
    assert "account ruined" in cell["reason"] and "D-101" in cell["reason"]
    assert str(path) in cell["reason"] and "-50.0" in cell["reason"]
    assert grid["result"] == "GRID_EVALUATED" and grid["idea_status"] == "refuted"


def test_an_equity_of_exactly_zero_is_a_ruin_too(tmp_path):
    _write_window(tmp_path, "r1", _ruined_equities(0.0))
    _injected, grid = _grade({"v": _single_window_pr()}, tmp_path)
    cell = grid["grid"][CID]["v"]
    assert cell["result"] == "FAIL" and cell["detail"]["ruin"]["equity"] == 0.0


def test_the_ruin_is_never_read_as_unknown(tmp_path):
    """The point of the ruling: not INCONCLUSIVE (None as unknown) and not a raise."""
    _write_window(tmp_path, "r1", _ruined_equities())
    _injected, grid = _grade({"v": _single_window_pr()}, tmp_path)
    assert grid["grid"][CID]["v"]["result"] not in ("INCONCLUSIVE", "SPEC_ERROR")
    assert grid["idea_status"] != "inconclusive"


def test_a_ruined_variant_does_not_change_a_healthy_variants_cell(tmp_path):
    root = tmp_path / "run"
    shutil.copytree(FIX / "run_095_base", root)
    path = _write_window(root / "variants" / "ruined", "rz", _ruined_equities(-7.5))
    _d, healthy = _fixture_pr("run_095_base")
    healthy["protocol_file"] = str(root / "protocol.json")
    _injected, grid = _grade({"healthy": healthy, "ruined": _single_window_pr("rz")}, root)
    row = grid["grid"][CID]
    assert row["healthy"] == MASTER_CELL
    assert row["ruined"]["result"] == "FAIL"
    assert row["ruined"]["detail"]["ruin"] == {"file": str(path), "timestamp": "2020-02-05",
                                               "equity": -7.5}


def test_the_ruin_cell_validates_against_the_grid_schema(tmp_path):
    import jsonschema
    _write_window(tmp_path, "r1", _ruined_equities())
    _injected, grid = _grade({"v": _single_window_pr()}, tmp_path)
    schema = json.loads((SR / "workflow_artifacts" / "schemas" / "grid_evaluation.schema.json")
                        .read_text(encoding="utf-8"))
    cell_schema = {"$ref": "#/definitions/cell", "definitions": schema["definitions"]}
    jsonschema.validate(grid["grid"][CID]["v"], cell_schema)
    assert "D-141" in schema["definitions"]["cell"]["properties"]["detail"]["description"]
    # and the whole result, as run_phase1_research writes it, against the full schema
    doc = {**grid, "evaluated_at": "2020-01-01T00:00:00+00:00"}
    wav._make_validator(jsonschema, schema).validate(doc)


def test_the_ruin_branch_reads_only_the_whole_test_sharpe_metric():
    """A ruin record on the summary does not touch a criterion on another metric."""
    summary = {"hypothesis_verdict": {"diagnostics": {
        "median_gross_pnl": -3.0,
        "whole_test_sharpe_ruin": {"file": "f.csv", "timestamp": "t", "equity": -1.0}}}}
    crit = {"id": "x", "metric": "median_gross_pnl", "source": "pooled", "comparator": ">",
            "threshold": 0.0, "floor": {}}
    cell = vce._evaluate_grid_cell_for_symbol(crit, summary, [], None)
    assert cell["result"] == "FAIL" and cell["value"] == -3.0 and "detail" not in cell


def test_a_per_symbol_cell_is_unchanged_the_ruin_is_a_pooled_record():
    """whole_test_sharpe_positive has symbol_reducer null and card_overridable [], so it is only
    ever graded pooled; the per-symbol path reads per_symbol_summary, where the pipeline never
    injects the metric. Pinned as it is today: the per-symbol read does not turn a ruin into
    anything."""
    summary = {"hypothesis_verdict": {"diagnostics": {
        "whole_test_sharpe": None,
        "whole_test_sharpe_ruin": {"file": "f.csv", "timestamp": "t", "equity": -1.0}}}}
    crit = next(c for c in MENU["criteria"] if c["id"] == CID)
    assert crit["symbol_reducer"] is None and crit["card_overridable"] == []
    cell = vce._evaluate_grid_cell_for_symbol(crit, summary, [], "XRPUSD")
    assert cell["result"] == "INCONCLUSIVE"


# -- (c) replay of run_096 asset_XRPUSDT -----------------------------------------------------


def test_run_096_asset_xrpusdt_replay_grades_fail_not_a_halt():
    d, pr = _fixture_pr("run_096_asset_XRPUSDT")
    # the old code's failure, for the record: the reader raises PortfolioRuined
    with pytest.raises(rpr._pd.PortfolioRuined) as raised:
        rpr._whole_test_chain(d, pr)
    assert raised.value.equity == -589.6624712066816
    injected, grid = _grade({"asset_XRPUSDT": pr}, d)       # and the grid path no longer raises
    cell = grid["grid"][CID]["asset_XRPUSDT"]
    assert cell["result"] == "FAIL" and cell["value"] is None
    ruin = cell["detail"]["ruin"]
    assert ruin["equity"] == -589.6624712066816
    assert ruin["timestamp"] == "2018-09-21"
    assert Path(ruin["file"]).as_posix().endswith(
        "variants/asset_XRPUSDT/results/20261015T201304Z_2ddd79e8/portfolio_states.csv")
    assert injected["asset_XRPUSDT"]["hypothesis_verdict"]["diagnostics"][
        "whole_test_sharpe_ruin"] == ruin
    assert "-589.6624712066816" in cell["reason"]
    assert grid["idea_status"] == "refuted"


def test_a_not_evaluable_variant_is_still_inconclusive_and_never_inherits_a_ruin(tmp_path):
    """The neighbouring branch (D-121) is unchanged, and a ruin does not leak from one variant
    of the loop to the next: a variant with no equity file reads None -> INCONCLUSIVE, with no
    ruin record, even when the variant before it was ruined."""
    _write_window(tmp_path, "r1", _ruined_equities())
    missing = {"results": [{"symbol": "XRPUSD", "window": "w1", "run_id": "nowhere"}],
               "hypothesis_verdict": {"diagnostics": {}}}
    injected, grid = _grade({"ruined": _single_window_pr(), "missing": missing}, tmp_path)
    diag = injected["missing"]["hypothesis_verdict"]["diagnostics"]
    assert diag == {"whole_test_sharpe": None}
    assert grid["grid"][CID]["missing"]["result"] == "INCONCLUSIVE"
    assert grid["grid"][CID]["ruined"]["result"] == "FAIL"
