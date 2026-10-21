"""
PR-9 (D-167, run_098 defect): a generated protocol carries a REFERENCE to the
data policy's holdout_range -- {"ref": holdout_policy.HOLDOUT_RANGE_REF} --
never the sealed dates.

What is pinned here:
  * no generated protocol (the generator's file, run_campaign's expected
    protocol, a per-coin variant copy, a promotion-only regeneration) contains
    a YYYY-MM-DD day inside the policy's holdout_range;
  * a generated file written before PR-9 (literal {start, end} block equal to
    the policy) is still accepted by the pre-flight, unchanged; a literal block
    that disagrees is still refused; a promotion-only regeneration keeps the
    file's own holdout block;
  * the holdout pause prints the reference, never the dates;
  * check_data.py resolves the reference (no silent skip of its mismatch
    warning) and warns on an unknown one.

SEALED-WINDOW HYGIENE: the range is computed in-process from the conftest
sandbox's verbatim policy copy and only ever COMPARED -- every assertion is
on a count or a bool computed beforehand, so a failing assertion cannot print
a sealed date. check_data.py prints the ranges it compares, so its tests use a
synthetic sandbox policy far from the real seal.
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import holdout_policy as hp  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import variant_coin as vc  # noqa: E402

from test_e061_c1_4_5_pauses_preflight import RUN, _NON_GENERIC, _scaffold  # noqa: E402

_REF = {"ref": hp.HOLDOUT_RANGE_REF}
_OTHER = {**_NON_GENERIC, "min_trade_count_gte": 30}
_DAY = re.compile(r"(?<![0-9])([0-9]{4}-[0-9]{2}-[0-9]{2})(?![0-9])")


def _days_inside_seal(text: str) -> int:
    """How many YYYY-MM-DD days in `text` fall inside the policy's closed
    holdout_range. A count, never the days themselves."""
    hs, he = rpr._load_holdout_range()
    return sum(1 for d in _DAY.findall(text) if hs <= d <= he)


def _constraints(promotion=_NON_GENERIC, **over) -> dict:
    proto = {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
             "end": "2022-02-28", "promotion": promotion}
    proto.update(over)
    return {"protocol": proto}


def _generated_path() -> Path:
    return rpr.ROOT / "protocols" / f"{RUN}_generated.json"


def _legacy_literal_block() -> dict:
    """The block the pre-PR-9 generator wrote: the policy's own days."""
    hs, he = rpr._load_holdout_range()
    return {"start": hs, "end": he}


def _rewrite_as_pre_pr9(path: Path, block: dict) -> bytes:
    """`path` rewritten as the pre-PR-9 generator wrote it (same keys, same
    order, indent=2) with `block` as its holdout; returns the new bytes."""
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["holdout"] = block
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path.read_bytes()


def test_the_detector_sees_a_literal_block():
    """Guard on the guard: the pre-PR-9 literal block is caught (2 days)."""
    n = _days_inside_seal(json.dumps(_legacy_literal_block()))
    assert n == 2


@pytest.mark.parametrize("override", ["absent", None, "literal", "reference"])
def test_no_generated_protocol_contains_a_date_inside_the_holdout_range(override):
    over = {}
    if override == "literal":
        over["holdout"] = _legacy_literal_block()
    elif override == "reference":
        over["holdout"] = dict(_REF)
    elif override is None:
        over["holdout"] = None
    constraints = _constraints(**over)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    text = path.read_text(encoding="utf-8")
    written = json.loads(text)
    is_ref = hp.is_holdout_ref(written["holdout"])
    assert is_ref
    n_file = _days_inside_seal(text)
    assert n_file == 0
    expected = camp._expected_generated_protocol(constraints["protocol"], RUN,
                                                 promotion_retired=False, run_dir=run_dir)
    same = expected == written
    assert same
    n_expected = _days_inside_seal(json.dumps(expected))
    assert n_expected == 0
    variant = vc.variant_protocol(written, symbol="ETHUSDT")
    variant_is_ref = hp.is_holdout_ref(variant["holdout"])
    assert variant_is_ref
    assert vc.check_variant_protocol(variant, written) == []
    n_variant = _days_inside_seal(json.dumps(variant))
    assert n_variant == 0


def test_the_generator_still_refuses_without_a_usable_policy(tmp_path, monkeypatch):
    """The reference does not loosen generation: the policy is still loaded
    and validated, and a missing one refuses."""
    monkeypatch.setattr(rpr, "_DATA_POLICY_PATH", tmp_path / "missing.yaml")
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._generated_protocol_holdout_block({})


def test_a_pre_pr9_literal_generated_file_is_still_accepted_unchanged():
    constraints = _constraints()
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    before = _rewrite_as_pre_pr9(path, _legacy_literal_block())
    refusal, regeneration = camp._generated_protocol_plan(
        run_dir, RUN, constraints["protocol"], {}, promotion_retired=False)
    assert refusal is None and regeneration is None
    unchanged = path.read_bytes() == before
    assert unchanged


@pytest.mark.parametrize("shift", ["start", "end"])
def test_a_literal_block_that_disagrees_with_the_policy_is_still_refused(shift):
    constraints = _constraints()
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    block = _legacy_literal_block()
    block[shift] = (date.fromisoformat(block[shift]) + timedelta(days=1)).isoformat()
    _rewrite_as_pre_pr9(path, block)
    refusal, regeneration = camp._generated_protocol_plan(
        run_dir, RUN, constraints["protocol"], {}, promotion_retired=False)
    assert regeneration is None
    names_holdout = refusal is not None and "['holdout']" in refusal
    assert names_holdout


@pytest.mark.parametrize("stored", ["literal", "reference"])
def test_a_promotion_only_regeneration_keeps_the_files_own_holdout_block(stored):
    old = _constraints(_OTHER)
    run_dir = _scaffold(constraints=old)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, old)
    block = _legacy_literal_block() if stored == "literal" else dict(_REF)
    _rewrite_as_pre_pr9(path, block)
    new = _constraints(_NON_GENERIC)
    (run_dir / "artifacts" / "pre_registration.yaml").write_text(
        yaml.safe_dump({"machine_constraints": new}), encoding="utf-8")
    refusal, regeneration = camp._generated_protocol_plan(
        run_dir, RUN, new["protocol"], {}, promotion_retired=False)
    assert refusal is None and regeneration is not None
    assert regeneration["differing"] == ["promotion"]
    kept = regeneration["doc"]["holdout"] == block
    assert kept
    assert regeneration["doc"]["promotion"] == _NON_GENERIC
    assert list(regeneration["doc"]) == list(json.loads(path.read_text(encoding="utf-8")))


def test_the_holdout_pause_prints_the_reference_not_the_dates(tmp_path, capsys):
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(parents=True)
    (tmp_path / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": "run_test", "flags": {}}), encoding="utf-8")
    (artifacts / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "run_test"}), encoding="utf-8")
    (artifacts / "research_brief.yaml").write_text(
        yaml.safe_dump({"research_only": False}), encoding="utf-8")
    assert rpr._route_holdout_evaluation(tmp_path, "run_test") == "human_pause"
    out = capsys.readouterr().out
    reached = "holdout_result.yaml not yet present" in out
    assert reached
    names_ref = hp.HOLDOUT_RANGE_REF in out
    assert names_ref
    n_out = _days_inside_seal(out)
    assert n_out == 0


# ---------------------------------------------------------------------------
# check_data.py -- synthetic sandbox policy only (it prints what it compares)
# ---------------------------------------------------------------------------

_S_START, _S_END = "2021-03-01", "2021-04-15"
_PROTO_WINDOWS = [{"label": "w1", "test": {"start": "2019-01-01", "end": "2019-01-31"}}]


@pytest.fixture
def check_data():
    import check_data as cd
    return cd


@pytest.mark.parametrize("block,warns", [
    pytest.param(dict(_REF), False, id="reference"),
    pytest.param({"start": _S_START, "end": _S_END}, False, id="literal-agreeing"),
    pytest.param({"start": _S_START, "end": "2021-04-16"}, True, id="literal-disagreeing"),
    pytest.param({"ref": "config/campaign_data_policy.yaml#validation_range"}, True,
                 id="unknown-reference"),
    pytest.param({**_REF, "start": _S_START}, True, id="reference-plus-dates"),
])
def test_check_data_resolves_the_reference(check_data, capsys, block, warns):
    policy = {"holdout_range": [_S_START, _S_END]}
    protocol = {"windows": _PROTO_WINDOWS, "holdout": block}
    assert check_data.check_holdout_overlap(protocol, policy) is True
    out = capsys.readouterr().out
    assert ("WARNING" in out) is warns
