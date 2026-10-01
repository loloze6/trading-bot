"""
O-6 (2026-10-01): a variant-floor park or pause names every not-tested
variant as blocking or non-blocking, with its reason, and says the idea is
capped at INCONCLUSIVE while asset variants stay untested. run_063 parked as
"missing class(es): FearGreedComponent" although the other refused variants
failed on data -- one reason pointed the operator at the wrong fix.
"""
import sys
from pathlib import Path

SR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))
sys.path.insert(0, str(SR / "tests"))

import run_phase1_research as rpr  # noqa: E402
from test_e059_6c_s2c_parked_states import (  # noqa: E402
    DATA, FOO, _gate_run, _nt, _ok, _state, _v12, _write_variant_gate,
)


def _coverage_skip():
    prefix = rpr._variant_coin_module().COVERAGE_REASON_PREFIX
    return _nt(prefix + " SOLUSDT covers 3/5 windows (60%)")


def test_detail_lists_every_variant_by_kind():
    detail = rpr._variant_shortfall_detail({
        "base": _ok(), "design_v2": _v12(), "data_v3": _nt(DATA), "asset_sol": _coverage_skip()})
    assert detail.startswith("blocking: ")
    assert f"design_v2 (missing class {FOO})" in detail
    assert "data_v3 (data_availability_gate outcome=decline" in detail
    assert "non-blocking, not counted: asset_sol (insufficient_coverage" in detail
    assert detail.endswith("the idea is capped at INCONCLUSIVE while asset variants stay untested")
    assert "base" not in detail


def test_no_skip_no_cap_sentence():
    detail = rpr._variant_shortfall_detail({"base": _ok(), "design_v2": _v12()})
    assert "INCONCLUSIVE" not in detail and "non-blocking" not in detail


def test_the_park_record_names_every_variant(monkeypatch):
    run_dir = _gate_run(monkeypatch, "run_961", variant_loop=True)
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": {
        "base": _ok(), "design_v2": _nt(DATA), "asset_v2": _v12(), "asset_sol": _coverage_skip()}})
    _write_variant_gate(run_dir, "design_v2")
    rpr.run_loop("run_961")
    marker = _state(run_dir)[rpr.PARKED_KEY]
    assert marker["kind"] == "component"
    reason = marker["reason"]
    for part in ("asset_v2 (missing class", "design_v2 (data_availability_gate",
                 "non-blocking, not counted: asset_sol", "capped at INCONCLUSIVE"):
        assert part in reason, (part, reason)
