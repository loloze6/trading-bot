"""D-125 (ruling 2 item (4), operator 2026-10-13): an append-only block status record in
campaign_record/block_registry.yaml. A block's current status is its LAST record; voided
blocks are left out of composition and of the readers' registry_summary; no record: every
reader gets the document unchanged. The schema accepts `statuses` and the operator's
`marks`. Written only by `python tools/block_registry.py status ...`.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "tools"))
sys.path.insert(0, str(SR / "workflow"))

import block_registry as br  # noqa: E402
from test_e061_c2_s2e_distance_rubric import _block, _doc, _run  # noqa: E402

SCHEMA = json.loads((SR / "workflow_artifacts" / "schemas" / "block_registry.schema.json")
                    .read_text(encoding="utf-8"))
A, B = "L1_A:run_083", "L1_B:run_089"


def _write(tmp_path, doc) -> Path:
    p = tmp_path / "campaign_record" / "block_registry.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return p


def _rec(bid, status="voided", reason="r"):
    return {"block_id": bid, "status": status, "reason": reason, "by": "operator",
            "at": "2026-10-14T00:00:00+00:00"}


def test_no_status_record_every_reader_gets_the_document_unchanged(tmp_path):
    p = _write(tmp_path, _doc(_block(A), _block(B)))
    doc = br.load_registry(p)
    assert br.voided_block_ids(doc) == set()
    assert br.active_view(doc) is doc
    assert br.load_active_registry(p) == doc


def test_the_last_record_per_block_is_its_status(tmp_path):
    doc = {**_doc(_block(A), _block(B)),
           "statuses": [_rec(A), _rec(B), _rec(B, status="active")]}
    p = _write(tmp_path, doc)
    loaded = br.load_registry(p)
    assert br.voided_block_ids(loaded) == {A}
    view = br.load_active_registry(p)
    assert [b["block_id"] for b in view["blocks"]] == [B]
    assert [b["block_id"] for b in br.load_registry(p)["blocks"]] == [A, B]  # never removed
    assert view["revision"] == loaded["revision"]


@pytest.mark.parametrize("bad, match", [
    ("not a list", "is not a list"),
    ([{"block_id": A, "status": "voided"}], "must be exactly"),
    ([_rec("X:run_1")], "not a registered block"),
    ([_rec(A, status="retired")], "not one of"),
    ([_rec(A, reason=" ")], "reason is empty"),
])
def test_a_malformed_status_list_raises(tmp_path, bad, match):
    p = _write(tmp_path, {**_doc(_block(A)), "statuses": bad})
    with pytest.raises(br.BlockRegistryError, match=match):
        br.load_registry(p)


def test_set_status_appends_and_changes_nothing_else(tmp_path):
    doc = {**_doc(_block(A), _block(B)),
           "marks": [{"block_id": B, "date": "2026-10-12", "note": "n"}]}
    p = _write(tmp_path, doc)
    rec = br.set_status(p, A, "voided", "graded under step-1a criteria", "operator")
    after = br.load_registry(p)
    assert after["statuses"] == [rec] and rec["block_id"] == A and rec["at"]
    assert after["blocks"] == doc["blocks"] and after["revision"] == doc["revision"]
    assert after["marks"] == doc["marks"]
    br.set_status(p, A, "active", "reinstated", "operator")
    assert len(br.load_registry(p)["statuses"]) == 2           # append-only
    assert br.voided_block_ids(br.load_registry(p)) == set()   # the last record wins


@pytest.mark.parametrize("args, match", [
    ((B.replace("089", "999"), "voided", "r", "op"), "not a registered block"),
    ((A, "voided", "", "op"), "reason is empty"),
    ((A, "voided", "r", ""), "by is empty"),
    ((A, "gone", "r", "op"), "not one of"),
])
def test_set_status_refuses_and_writes_nothing(tmp_path, args, match):
    p = _write(tmp_path, _doc(_block(A)))
    before = p.read_bytes()
    with pytest.raises(br.BlockRegistryError, match=match):
        br.set_status(p, *args)
    assert p.read_bytes() == before


def test_set_status_needs_a_registry(tmp_path):
    with pytest.raises(br.BlockRegistryError, match="no registry"):
        br.set_status(tmp_path / "none.yaml", A, "voided", "r", "op")


def test_a_later_registration_keeps_the_status_records(tmp_path):
    """record_run's append path keeps the whole document (statuses, marks)."""
    p = _write(tmp_path, {**_doc(_block(A)), "statuses": [_rec(A)],
                          "marks": [{"block_id": A, "note": "n"}]})
    br._append(p, "run_090", [_block("L1_C:run_090")])
    after = br.load_registry(p)
    assert after["statuses"] == [_rec(A)] and after["marks"] == [{"block_id": A, "note": "n"}]
    assert [b["block_id"] for b in br.load_active_registry(p)["blocks"]] == ["L1_C:run_090"]


def test_the_schema_accepts_statuses_and_the_operators_marks():
    doc = {**_doc(_block(A)), "statuses": [_rec(A)],
           "marks": [{"block_id": A, "date": "2026-10-12", "note": "registered by the grid ..."}]}
    jsonschema.validate(doc, SCHEMA)
    for bad in ({**doc, "statuses": [{**_rec(A), "extra": 1}]},
                {**doc, "statuses": [_rec(A, status="x")]},
                {**doc, "marks": [{"note": "no block id"}]}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(bad, SCHEMA)


def test_the_readers_summary_leaves_a_voided_block_out(tmp_path):
    run_dir = _run(tmp_path)
    doc = {**_doc(_block(A), _block(B)), "statuses": [_rec(A)]}
    full = br.registry_summary(_doc(_block(A), _block(B)), run_dir)
    active = br.registry_summary(br.active_view(doc), run_dir)
    assert full["registry"]["n_blocks"] == 2 and active["registry"]["n_blocks"] == 1


def test_every_composition_and_summary_reader_reads_the_active_view():
    """Static: the four registry readers that feed composition or the readers' summary."""
    src = {f: (SR / f).read_text(encoding="utf-8") for f in (
        "tools/decide_next.py", "tools/composite_cache.py", "workflow/run_phase1_research.py")}
    assert "registry = _br.load_active_registry(root / \"campaign_record\" / \"block_registry.yaml\")" \
        in src["tools/decide_next.py"]
    assert "resolve_current_composite(_br.load_active_registry(registry_path)" \
        in src["tools/composite_cache.py"]
    rpr = src["workflow/run_phase1_research.py"]
    assert "return _br.load_active_registry(_block_registry_path())" in rpr  # composition checks
    assert "registry_summary(_br.load_active_registry(_block_registry_path())" in rpr
    for f, s in src.items():
        assert "load_registry(" not in s.replace("load_active_registry(", "").replace(
            "_br.load_registry(_block_registry_path())", ""), f


def test_the_cli(tmp_path):
    p = _write(tmp_path, _doc(_block(A)))
    cmd = [sys.executable, str(SR / "tools" / "block_registry.py"), "status", "--registry", str(p),
           "--block-id", A, "--status", "voided", "--reason", "graded under step-1a criteria",
           "--by", "operator"]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert out.returncode == 0 and "STATUS appended" in out.stdout
    assert br.voided_block_ids(br.load_registry(p)) == {A}
    bad = subprocess.run(cmd[:5] + ["--block-id", "nope:run_1"] + cmd[7:], capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    assert bad.returncode == 1 and "REFUSED" in bad.stdout
