"""
Soft patch (b) (P1a shakedown, 2026-07-04) regression test.

Fixture: run_044's real hypothesis_card.yaml. It declares is_market_wide=false
(correctly — funding rate is per-symbol, not a shared index like Fear & Greed) but then
applies a correlation discount anyway in its own prose ("n_eff_symbols ≈ sqrt(2) /
(1 + 0.82) ≈ 1.1"), landing at a self-reported n_eff≈100.4 against the machine's actual
n_eff=182.5 for the same inputs (activation_rate=0.125, n_bars=17520, n_symbols=2,
is_market_wide=false). This was never caught live because the run crashed one stage
earlier (innovation_expansion YAML error) before _run_a86_power_check ever ran on it.
"""

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr

_RUN_044_HYPOTHESIS_CARD = Path(__file__).parent.parent / "runs" / "run_044" / "artifacts" / "hypothesis_card.yaml"


@pytest.fixture
def temp_log(tmp_path, monkeypatch):
    log_path = tmp_path / "power_check_discrepancy_log.yaml"
    monkeypatch.setattr(rpr, "_POWER_DISCREPANCY_LOG_PATH", log_path)
    return log_path


def test_run_044_fixture_extraction_finds_the_self_contradiction():
    if not _RUN_044_HYPOTHESIS_CARD.exists():
        pytest.skip("run_044 hypothesis_card.yaml not present on disk")
    card = yaml.safe_load(_RUN_044_HYPOTHESIS_CARD.read_text(encoding="utf-8"))
    llm_reported = rpr._extract_llm_reported_power(card)

    assert llm_reported.get("n_symbols_effective") == pytest.approx(1.1)
    assert llm_reported.get("expected_n_eff") == pytest.approx(100.4, abs=0.5)
    assert llm_reported.get("min_detectable_ic") == pytest.approx(0.10, abs=0.01)


def test_run_044_fixture_produces_a_logged_discrepancy(temp_log):
    if not _RUN_044_HYPOTHESIS_CARD.exists():
        pytest.skip("run_044 hypothesis_card.yaml not present on disk")
    card = yaml.safe_load(_RUN_044_HYPOTHESIS_CARD.read_text(encoding="utf-8"))

    # Machine result at the SAME inputs (is_market_wide=false -> no rho discount).
    machine = {
        "verdict": "power_adequate",
        "expected_n_eff": 182.5,
        "min_detectable_ic": 0.0746,
    }

    rpr._compare_llm_vs_machine_power("run_044", "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION", machine, card)

    assert temp_log.exists(), "a material discrepancy must be logged"
    log = yaml.safe_load(temp_log.read_text(encoding="utf-8"))
    entry = log["entries"][0]
    assert entry["run_id"] == "run_044"
    joined = " ".join(entry["discrepancies"])
    assert "is_market_wide=false but n_symbols_effective=1.1" in joined
    assert "expected_n_eff" in joined  # the ~100 vs ~182 divergence must also be flagged


def test_no_discrepancy_logged_when_llm_and_machine_agree(temp_log):
    card = {
        "hypothesis_id": "AGREES",
        "power_parameters": {
            "is_market_wide": False,
            "n_symbols": 2,
            "n_symbols_effective": 2.0,
            "a_priori_calculation": "expected_n_eff = 182.5; min_detectable_ic ≈ 0.0746",
        },
    }
    machine = {"verdict": "power_adequate", "expected_n_eff": 182.5, "min_detectable_ic": 0.0746}
    rpr._compare_llm_vs_machine_power("run_999", "AGREES", machine, card)
    assert not temp_log.exists(), "agreement must not produce a log entry"


def test_no_extraction_means_no_crash_and_no_log(temp_log):
    """A card with no self-computed power numbers at all (schema-minimal) must not
    error and must not produce a spurious log entry."""
    card = {"hypothesis_id": "MINIMAL", "power_parameters": {"is_market_wide": False, "n_symbols": 2}}
    machine = {"verdict": "power_adequate", "expected_n_eff": 100.0, "min_detectable_ic": 0.1}
    rpr._compare_llm_vs_machine_power("run_998", "MINIMAL", machine, card)
    assert not temp_log.exists()
