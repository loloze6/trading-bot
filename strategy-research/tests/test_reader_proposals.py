"""
tools/reader_proposals.py: load + validate the readers' proposal files.

The loader and proposal.schema.json must agree: every schema-valid example
from the 5b-i test suite loads, and every malformed case below is rejected
by BOTH (where the schema can express the rule).
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

import reader_proposals as rp  # noqa: E402
import build_reports  # noqa: E402
from test_e046a_slice5b_i_reader_skills import _VALID_EXAMPLES  # noqa: E402

CATEGORIES = list(build_reports.REPORT_CATEGORIES)
SCHEMA = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" / "proposal.schema.json")
                    .read_text(encoding="utf-8"))


def _schema_ok(p) -> bool:
    return not list(jsonschema.Draft202012Validator(SCHEMA).iter_errors(p))


def _write(tmp_path, files: dict) -> Path:
    d = tmp_path / "proposals"
    d.mkdir()
    for name, text in files.items():
        (d / name).write_text(text, encoding="utf-8")
    return d


def _with_id(example: dict, cat: str) -> dict:
    p = copy.deepcopy(example)
    p["proposal_id"] = f"{cat}-run_test-1"
    return p


def test_categories_match_the_five_readers():
    assert CATEGORIES == ["profitability", "trade_efficiency", "forecast_power",
                          "regime_power", "component_attribution"]


def test_every_schema_valid_example_loads(tmp_path):
    files = {}
    for cat, ex in _VALID_EXAMPLES.items():
        p = _with_id(ex, cat)
        assert _schema_ok(p)
        files[f"{cat}.yaml"] = yaml.safe_dump([p])
    out = rp.load_proposals(_write(tmp_path, files), CATEGORIES)
    assert all(len(out[c]) == 1 for c in _VALID_EXAMPLES)


def test_missing_dir_missing_file_and_empty_list_mean_no_proposals(tmp_path):
    assert rp.load_proposals(tmp_path / "absent", CATEGORIES) == {c: [] for c in CATEGORIES}
    out = rp.load_proposals(_write(tmp_path, {"profitability.yaml": "[]"}), CATEGORIES)
    assert out == {c: [] for c in CATEGORIES}


def _mutated(mutator):
    p = _with_id(_VALID_EXAMPLES["profitability"], "profitability")
    mutator(p)
    return p


_BAD_ENTRIES = {
    "smuggled_routing_field": lambda p: p.__setitem__("hypothesis_verdict", "promote"),
    "unknown_kind": lambda p: p.__setitem__("kind", "tweak"),
    "patch_and_block": lambda p: p.__setitem__("block", {"kind": "forecast", "config_paths": ["x"],
                                                         "rationale": "r"}),
    "empty_patch": lambda p: p.__setitem__("patch", []),
    "patch_item_without_field": lambda p: p.__setitem__(
        "patch", [{"component": "keltner", "param": "atr_multiplier", "before": 2.0, "after": 2.5}]),
    "empty_evidence": lambda p: p.__setitem__("evidence", []),
    "score_out_of_range": lambda p: p["scores"].__setitem__("confidence_real", 4),
    "score_bool": lambda p: p["scores"].__setitem__("confidence_real", True),
    "score_float": lambda p: p["scores"].__setitem__("confidence_real", 2.0),
    "score_missing": lambda p: p["scores"].pop("mechanism_plausibility"),
    "missing_model_id": lambda p: p.pop("model_id"),
    "bad_id_pattern": lambda p: p.__setitem__("proposal_id", "profitability-run_1"),
}


@pytest.mark.parametrize("name", sorted(_BAD_ENTRIES))
def test_malformed_entry_is_rejected_by_loader_and_schema(tmp_path, name):
    bad = _mutated(_BAD_ENTRIES[name])
    with pytest.raises(rp.ProposalError):
        rp.load_proposals(_write(tmp_path, {"profitability.yaml": yaml.safe_dump([bad])}), CATEGORIES)
    if name not in ("score_float",):  # JSON Schema treats 2.0 as an integer; the loader is stricter
        assert not _schema_ok(bad), f"schema accepted {name}"


@pytest.mark.parametrize("files", [
    {"profitability.yaml": "key: [unclosed"},                          # unparseable
    {"profitability.yaml": ""},                                        # empty document
    {"profitability.yaml": "a: 1"},                                    # not a list
    {"profitability.yaml": yaml.safe_dump(["just a string"])},         # entry not a mapping
    {"profitability.yaml": "[]", "profitability_v2.yaml": "[]"},       # unexpected file
    {"profitability.yml": "[]"},                                       # wrong extension
], ids=["unparseable", "empty_file", "mapping", "entry_not_mapping", "unexpected_file",
        "wrong_extension"])
def test_malformed_file_fails_loud(tmp_path, files):
    with pytest.raises(rp.ProposalError):
        rp.load_proposals(_write(tmp_path, files), CATEGORIES)


def test_foreign_category_id_is_rejected(tmp_path):
    foreign = _with_id(_VALID_EXAMPLES["profitability"], "regime_power")
    with pytest.raises(rp.ProposalError):
        rp.load_proposals(_write(tmp_path, {"profitability.yaml": yaml.safe_dump([foreign])}),
                          CATEGORIES)


def test_duplicate_id_is_rejected(tmp_path):
    p = _with_id(_VALID_EXAMPLES["profitability"], "profitability")
    with pytest.raises(rp.ProposalError, match="duplicate"):
        rp.load_proposals(_write(tmp_path, {"profitability.yaml": yaml.safe_dump([p, p])}),
                          CATEGORIES)


@pytest.mark.parametrize("litter", [".DS_Store", "profitability.yaml~", "notes.txt"])
def test_os_and_editor_litter_is_ignored(tmp_path, litter):
    out = rp.load_proposals(_write(tmp_path, {"profitability.yaml": "[]", litter: "junk"}), CATEGORIES)
    assert out["profitability"] == []
