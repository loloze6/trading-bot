"""
Which config a reading's `patch` is resolved against (run_phase1_research._reader_base_config_rel).

run_065 and run_066: both trade_efficiency readers proposed a `patch` on a component and a
setting that do not exist. A reading is checked against this run's BASE config: the base
variant's strategy_config.json when the variant loop wrote artifacts/variants/index.yaml, else
candidate_strategy_config.json -- the same base decide_next.resolve_patch reads.

D-198: the five readers (their handoff, prompt and SKILLs, which this file once also tested) are
deleted; the analyst's lenses still use the base-config rule, so its tests stay.
"""
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402

from _reader_test_helpers import RUN_ID  # noqa: E402


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _write_index(run_dir: Path, variants: dict, create_configs: bool = True) -> None:
    """index.yaml plus (by default) each variant's config file, as 5a writes them."""
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "index.yaml", {"variants": variants})
    if create_configs:
        for vid, info in variants.items():
            rel = (info or {}).get("config_path") or f"artifacts/variants/{vid}/strategy_config.json"
            path = run_dir / str(rel).replace("\\", "/")
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text('{"marker": "%s"}\n' % vid, encoding="utf-8")


def test_the_config_is_the_base_variants_when_the_variant_loop_ran(tmp_path):
    run_dir = tmp_path / "runs" / RUN_ID
    _write_index(run_dir, {
        "base": {"config_path": "artifacts\\variants\\base\\strategy_config.json"},
        "design_1": {"config_path": "artifacts\\variants\\design_1\\strategy_config.json"}})
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/variants/base/strategy_config.json"


def test_without_a_base_id_the_sorted_first_variant_is_the_base(tmp_path):
    """json_pointer.base_variant_id's rule -- the base decide_next resolves against."""
    run_dir = tmp_path / "runs" / RUN_ID
    _write_index(run_dir, {"zeta": {"config_path": "artifacts/variants/zeta/strategy_config.json"},
                           "alpha": {}})
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/variants/alpha/strategy_config.json"


@pytest.mark.parametrize("ids", [["base", "design_1", "asset_1"], ["zeta", "alpha"]])
def test_the_readers_base_is_the_base_decide_next_resolves_patches_against(tmp_path, ids):
    """decide_next.resolve_patch reads the config_ref of decide_next._base_variant;
    the reading must be checked against that same config."""
    import decide_next
    run_dir = tmp_path / "runs" / RUN_ID
    rels = {v: f"artifacts\\variants\\{v}\\strategy_config.json" for v in ids}  # as written on Windows
    _write_index(run_dir, {v: {"config_path": rel} for v, rel in rels.items()})
    entry = {"run_id": RUN_ID,
             "variants": {v: {"config_ref": f"runs/{RUN_ID}/" + rel.replace("\\", "/")}
                          for v, rel in rels.items()}}
    _vid, base = decide_next._base_variant(entry)
    assert base["config_ref"] == f"runs/{RUN_ID}/" + rpr._reader_base_config_rel(run_dir)


def test_without_the_variant_loop_the_config_is_the_candidate_config(tmp_path):
    run_dir = tmp_path / "runs" / RUN_ID
    (run_dir / "artifacts").mkdir(parents=True)
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/candidate_strategy_config.json"
    assert rpr._reader_base_config_rel(None) == "artifacts/candidate_strategy_config.json"


def test_a_base_refused_before_its_config_was_written_falls_back_to_the_candidate(tmp_path):
    """review 2026-10-03: base not_tested with no config file on disk -> the candidate config
    instead of a missing input."""
    run_dir = tmp_path / "runs" / RUN_ID
    _write_index(run_dir, {"base": {"status": "not_tested"},
                           "design_1": {"config_path": "artifacts/variants/design_1/strategy_config.json"}},
                 create_configs=False)
    assert not (run_dir / "artifacts/variants/base/strategy_config.json").exists()
    assert rpr._reader_base_config_rel(run_dir) == "artifacts/candidate_strategy_config.json"
