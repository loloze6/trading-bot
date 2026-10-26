"""
D-198: the kept run-file and request-summary code, restored after test_e068_8_clarity.py went.

From origin/master's sections 2 (claim_measurement.yaml) and 4 (requests in one place):
the measurement run file's two names, the old-name read of an older run, the detector wishlist's
location, and the campaign summary's "Requests" section.

Dropped as tests of deleted code: the flag-on instruction-file wording checks (the readers'
SKILLs and the reading contract are deleted), the readers' digest (`claim_result_digest`,
deleted: the findings builder is the reader of the run file now) and the v3 handoff, the
safety-net / variant-missing digest assertions, section 3 (the digest's statistic labels and the
reading contract). No LLM.
"""
import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import claim_findings as cf  # noqa: E402
import claim_measure as cm  # noqa: E402

from test_e068_s3_claim_measure import ON, UP, _claim, _fixture_run  # noqa: E402
from _reader_test_helpers import _set_orchestrator  # noqa: E402

FIX4 = SR_ROOT / "tests" / "fixtures" / "e068_4" / "run_070"


# ---------------------------------------------------------------------------
# claim_measurement.yaml
# ---------------------------------------------------------------------------

def test_run_file_names():
    assert cm.RUN_FILE == "claim_measurement.yaml"
    assert cm.OLD_RUN_FILE == "claim_status.yaml"
    assert cm.RUN_FILES == (cm.RUN_FILE, cm.OLD_RUN_FILE)


@pytest.mark.parametrize("present,want", [
    ((), "claim_measurement.yaml"),
    (("claim_status.yaml",), "claim_status.yaml"),
    (("claim_measurement.yaml",), "claim_measurement.yaml"),
    (("claim_status.yaml", "claim_measurement.yaml"), "claim_measurement.yaml"),
], ids=["none", "old_only", "new_only", "both"])
def test_run_file_path_reads_the_new_name_else_the_old(tmp_path, present, want):
    for name in present:
        (tmp_path / name).write_text("x: 1\n", encoding="utf-8")
    assert cm.run_file_path(tmp_path) == tmp_path / want


def test_measurement_writes_only_the_new_name():
    _set_orchestrator(ON)
    run_dir = _fixture_run("run_981", claim=_claim([UP]))
    rpr._measure_claim_tests_after_backtests(run_dir, "run_981")
    arts = run_dir / "artifacts"
    assert rpr.load_yaml(arts / "claim_measurement.yaml")["claim_status"] == "measured"
    assert not (arts / "claim_status.yaml").exists()


def test_clearing_removes_both_names_only_with_the_flag_on():
    run_dir = _fixture_run("run_983", claim=_claim([UP]))
    arts = run_dir / "artifacts"
    files = [arts / "claim_measurement.yaml", arts / "claim_status.yaml",
             arts / "variants" / "base" / "claim_test.yaml"]
    for p in files:
        p.write_text("stale\n", encoding="utf-8")
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    rpr._clear_claim_measure_files(run_dir)
    assert all(p.exists() for p in files)
    _set_orchestrator(ON)
    rpr._clear_claim_measure_files(run_dir)
    assert not any(p.exists() for p in files)


@pytest.fixture
def run070(tmp_path) -> Path:
    dst = tmp_path / "run_070"
    shutil.copytree(FIX4, dst)
    return dst


def _entry(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "memory_entry.yaml").read_text(encoding="utf-8"))


def _rename_to_new(run_dir: Path) -> None:
    arts = run_dir / "artifacts"
    old, new = arts / "claim_status.yaml", arts / "claim_measurement.yaml"
    st = os.stat(old)
    old.rename(new)
    os.utime(new, ns=(st.st_atime_ns, st.st_mtime_ns))   # same attempt, same age


def test_an_old_run_with_only_claim_status_is_still_read(run070):
    """run_070 was measured before D-077: only claim_status.yaml."""
    assert (run070 / "artifacts" / "claim_status.yaml").exists()
    assert not (run070 / "artifacts" / "claim_measurement.yaml").exists()
    finding = cf.build_finding(run070, "run_070", _entry(run070))
    assert finding["status"] == "measured"
    assert finding["source"]["claim_status_ref"] == "runs/run_070/artifacts/claim_status.yaml"
    assert set(finding["result"]["per_variant"]) == {"base", "shock_lookback_250",
                                                     "sol_generalization", "uni_defi"}


def test_the_new_name_wins_over_an_old_copy(run070):
    _rename_to_new(run070)
    (run070 / "artifacts" / "claim_status.yaml").write_text(
        yaml.safe_dump({"claim_status": "not_measured", "reason": "old_copy", "variants": {}}),
        encoding="utf-8")
    finding = cf.build_finding(run070, "run_070", _entry(run070))
    assert finding["status"] == "measured"
    assert finding["source"]["claim_status_ref"] == "runs/run_070/artifacts/claim_measurement.yaml"



# ---------------------------------------------------------------------------
# Requests in one place
# ---------------------------------------------------------------------------

def test_the_detector_wishlist_lives_in_campaign_record():
    assert (SR_ROOT / "campaign_record" / "detector_wishlist.yaml").exists()
    assert not (SR_ROOT / "config" / "detector_wishlist.yaml").exists()
    assert camp.DETECTOR_WISHLIST_REL == "campaign_record/detector_wishlist.yaml"


def _wl(root: Path, rel: str, family: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"candidates": [{"family": family}]}), encoding="utf-8")
    return path


@pytest.mark.parametrize("present,want", [
    ((), "campaign_record/detector_wishlist.yaml"),
    (("config/detector_wishlist.yaml",), "config/detector_wishlist.yaml"),
    (("campaign_record/detector_wishlist.yaml",), "campaign_record/detector_wishlist.yaml"),
    (("config/detector_wishlist.yaml", "campaign_record/detector_wishlist.yaml"),
     "campaign_record/detector_wishlist.yaml"),
], ids=["none", "old_checkout", "new", "both"])
def test_the_detector_wishlist_path_falls_back_for_older_checkouts(monkeypatch, tmp_path,
                                                                   present, want):
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    for rel in present:
        _wl(tmp_path, rel, rel.split("/")[0])
    assert camp._detector_wishlist_path() == tmp_path / want


def test_the_wishlist_readers_read_campaign_record(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    _wl(tmp_path, "campaign_record/detector_wishlist.yaml", "new_family")
    _wl(tmp_path, "config/detector_wishlist.yaml", "old_family")
    assert camp._wishlist_family_names() == ["new_family"]
    assert camp._find_wishlist_entry("new_family") == {"family": "new_family"}
    assert camp._find_wishlist_entry("old_family") is None


def test_the_trigger_status_is_written_back_to_campaign_record(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    (tmp_path / "campaign_record").mkdir()
    (tmp_path / "campaign_record" / "campaign_knowledge_base.yaml").write_text(
        yaml.safe_dump({"findings": [{"id": "f1", "outcome": "no_edge_observed"}]}),
        encoding="utf-8")
    path = tmp_path / "campaign_record" / "detector_wishlist.yaml"
    path.write_text(yaml.safe_dump({"candidates": [{"family": "fam", "trigger_condition": {
        "predicate": {"source": "kb_finding", "all_of": [
            {"field": "outcome", "op": "==", "value": "kill"}]}}}]}), encoding="utf-8")
    camp.evaluate_and_persist_wishlist_predicate("fam")
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc["candidates"][0]["trigger_condition"]["status"] == "not_triggered"
    assert not (tmp_path / "config" / "detector_wishlist.yaml").exists()


def _summary() -> str:
    camp._regenerate_summary({"version": "1.0", "queue": []})
    return camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")


def _write(rel: str, doc) -> None:
    path = camp.ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def test_no_requests_section_without_a_request_file():
    assert camp._summary_request_lines() == []
    text = _summary()
    assert "Requests" not in text


def test_the_requests_section_counts_open_rows_and_shows_the_newest():
    _write("campaign_record/component_requests.yaml", {"requests": [
        {"run_id": f"run_00{i}", "stage": "strategy_config_authoring", "variant_id": None,
         "reason": f"component gap number {i}"} for i in range(1, 6)]})
    _write("campaign_record/test_requests.yaml", {"requests": [
        {"run_id": "run_010", "stage": "hypothesis_generation", "hypothesis_id": "H-1",
         "missing_block": "outcome fwd_return_of(other_symbol, h)"}]})
    _write("campaign_record/feed_wishlist.yaml", {"version": "1.0", "wishlist": [
        {"feed_name": "liquidation_data", "priority_rationale": "resolves   volume\nambiguity"}]})
    _write("campaign_record/detector_wishlist.yaml", {"candidates": [
        {"family": "adx_threshold", "description": "ADX gate", "trigger_condition":
         {"status": "not_triggered"}}]})
    text = _summary()
    block = text[text.index("## Requests"):text.index("## Scoreboard")]
    assert "Open = every row" in block
    lines = block.splitlines()
    i = lines.index("- `component_requests.yaml`: 5 open")
    assert lines[i + 1:i + 4] == [
        f"  - run_00{n} (strategy_config_authoring): component gap number {n}" for n in (3, 4, 5)]
    assert "run_001" not in block and "run_002" not in block
    assert "- `test_requests.yaml`: 1 open" in lines
    assert "  - run_010 (hypothesis_generation): outcome fwd_return_of(other_symbol, h)" in lines
    assert "- `feed_wishlist.yaml`: 1 open" in lines
    assert "  - liquidation_data: resolves volume ambiguity" in lines
    assert "- `detector_wishlist.yaml`: 1 open" in lines
    assert "  - adx_threshold: ADX gate" in lines
    assert "data_requests.yaml" not in block       # absent file: not listed
    order = [ln.split("`")[1] for ln in lines if ln.startswith("- `")]
    assert order == ["component_requests.yaml", "test_requests.yaml", "feed_wishlist.yaml",
                     "detector_wishlist.yaml"]


def test_an_older_checkouts_detector_wishlist_is_counted():
    _write("config/detector_wishlist.yaml", {"candidates": [{"family": "a"}, {"family": "b"}]})
    assert "- `detector_wishlist.yaml`: 2 open" in camp._summary_request_lines()


def test_a_bad_request_file_never_breaks_the_summary():
    (camp.ROOT / "campaign_record").mkdir(parents=True, exist_ok=True)
    (camp.ROOT / "campaign_record" / "data_requests.yaml").write_text("requests: [unclosed",
                                                                       encoding="utf-8")
    _write("campaign_record/test_requests.yaml", {"requests": {"not": "a list"}})
    _write("campaign_record/component_requests.yaml", ["a", "list"])
    lines = camp._summary_request_lines()
    assert any(ln.startswith("- `data_requests.yaml`: unreadable") for ln in lines)
    assert any(ln.startswith("- `test_requests.yaml`: unreadable") for ln in lines)
    assert any(ln.startswith("- `component_requests.yaml`: unreadable") for ln in lines)
    assert "## Requests" in _summary()


def test_an_empty_request_file_counts_zero():
    _write("campaign_record/component_requests.yaml", None)
    assert "- `component_requests.yaml`: 0 open" in camp._summary_request_lines()


def test_a_long_request_row_is_one_short_line():
    line = camp._summary_request_row({"run_id": "run_1", "reason": "a | b\n" + "x " * 200})
    assert line.startswith("run_1: a / b x x")       # a table-safe line, whitespace folded
    assert len(line) == camp._SUMMARY_REQUEST_LINE_CHARS and line.endswith("...")
    assert "\n" not in line and "|" not in line
    assert camp._summary_request_row({"run_id": "run_2"}) == "run_2"
    assert camp._summary_request_row("bare text") == "bare text"
