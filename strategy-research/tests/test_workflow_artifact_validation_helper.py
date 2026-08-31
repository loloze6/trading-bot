"""CUL-11: the opt-in workflow-artifact schema-validation helper.

Covers: opt-in-by-schema-existence (no-op when no schema matches the stem), valid data
passes, a schema violation warns by default and raises only under the flag, and — the
binding red-team Priority-E requirement — the helper is EXCEPTION-PROOF in warn mode: a
corrupt schema on disk or a non-dict payload is swallowed, never crashing a write path
that works today. Also: loader-agnostic (a JSON-sourced dict and a YAML-sourced dict
validate identically, since the helper never touches the file) and read-side coverage of
an LLM-authored artifact stem via run_phase1_research.load_yaml.
"""

import json
import logging
import sys
from pathlib import Path

import pytest
import yaml

# jsonschema is an undeclared transitive (via mcp); skip cleanly in a leaned-out env
# rather than failing collection (D1 pending with Dorian).
jsonschema = pytest.importorskip("jsonschema")

TOOLS = Path(__file__).parent.parent / "tools"
WORKFLOW = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(WORKFLOW))

import run_phase1_research as rpr  # noqa: E402
import workflow_artifact_validation as wav  # noqa: E402

_SIMPLE = {
    "type": "object",
    "additionalProperties": False,
    "required": ["x"],
    "properties": {"x": {"type": "integer"}},
}


def _install_schema(monkeypatch, tmp_path, stem, schema_text):
    """Point the helper at a tmp schemas dir holding {stem}.schema.json (raw text, so a
    deliberately-corrupt schema can be written)."""
    schemas = tmp_path / "schemas"
    schemas.mkdir(exist_ok=True)
    (schemas / f"{stem}.schema.json").write_text(schema_text, encoding="utf-8")
    monkeypatch.setattr(wav, "_SCHEMAS_DIR", schemas)
    return schemas


def _warn_mode(monkeypatch):
    monkeypatch.delenv("WORKFLOW_ARTIFACT_VALIDATION", raising=False)


def _raise_mode(monkeypatch):
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")


# ---------------------------------------------------------------------------
# Opt-in + happy path
# ---------------------------------------------------------------------------


def test_valid_data_passes(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)  # even in strict mode, valid data does not raise
    wav.validate_workflow_artifact(Path("myart.yaml"), {"x": 1})


def test_no_schema_stem_is_noop_even_in_raise_mode(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)
    # a stem with no matching schema file -> no validation happens at all
    wav.validate_workflow_artifact(Path("pipeline_state.yaml"), {"anything": True})


# ---------------------------------------------------------------------------
# Violation: warn by default, raise only under the flag
# ---------------------------------------------------------------------------


def test_extra_key_warns_by_default(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _warn_mode(monkeypatch)
    # additionalProperties:false violated -> warn, NOT raise
    wav.validate_workflow_artifact(Path("myart.yaml"), {"x": 1, "y": 2})


def test_extra_key_raises_under_flag(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)
    with pytest.raises(jsonschema.ValidationError):
        wav.validate_workflow_artifact(Path("myart.yaml"), {"x": 1, "y": 2})


def test_missing_required_raises_under_flag(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)
    with pytest.raises(jsonschema.ValidationError):
        wav.validate_workflow_artifact(Path("myart.yaml"), {})


# ---------------------------------------------------------------------------
# Loader-agnostic: JSON-sourced and YAML-sourced dicts validate identically.
# ---------------------------------------------------------------------------


def test_loader_agnostic_json_and_yaml(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)
    valid, bad = '{"x": 1}', '{"x": 1, "y": 2}'
    # both parsers -> valid dict -> neither raises
    wav.validate_workflow_artifact(Path("myart.json"), json.loads(valid))
    wav.validate_workflow_artifact(Path("myart.yaml"), yaml.safe_load(valid))
    # both parsers -> invalid dict -> both raise (stem drives schema, not extension)
    for parsed, name in [(json.loads(bad), "myart.json"), (yaml.safe_load(bad), "myart.yaml")]:
        with pytest.raises(jsonschema.ValidationError):
            wav.validate_workflow_artifact(Path(name), parsed)


# ---------------------------------------------------------------------------
# EXCEPTION-PROOF (red-team Priority-E, binding)
# ---------------------------------------------------------------------------


def test_corrupt_schema_warn_mode_survives(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", "{ this is not valid json ")
    _warn_mode(monkeypatch)
    # a malformed schema on disk must be swallowed, never raised, in warn mode
    wav.validate_workflow_artifact(Path("myart.yaml"), {"x": 1})


def test_corrupt_schema_raises_under_flag(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", "{ this is not valid json ")
    _raise_mode(monkeypatch)
    with pytest.raises(json.JSONDecodeError):  # corrupt schema propagates -> write blocked
        wav.validate_workflow_artifact(Path("myart.yaml"), {"x": 1})


def test_non_dict_data_warn_mode_survives(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _warn_mode(monkeypatch)
    for bad in (None, [1, 2, 3], "a string", 42):
        wav.validate_workflow_artifact(Path("myart.yaml"), bad)  # must not raise


def test_save_yaml_write_completes_despite_corrupt_schema(monkeypatch, tmp_path):
    """The whole point of warn-first: a bug in NEW validation code (here, a corrupt
    schema) must never take down a write path that works today."""
    _install_schema(monkeypatch, tmp_path, "myart", "{ corrupt schema ")
    _warn_mode(monkeypatch)
    out = tmp_path / "myart.yaml"
    rpr.save_yaml(out, {"x": 1})
    assert out.exists()
    assert yaml.safe_load(out.read_text(encoding="utf-8")) == {"x": 1}


def test_save_yaml_blocks_write_under_raise_flag(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)
    out = tmp_path / "myart.yaml"
    with pytest.raises(jsonschema.ValidationError):
        rpr.save_yaml(out, {"x": 1, "y": 2})  # violates schema -> raise -> no write
    assert not out.exists()


# ---------------------------------------------------------------------------
# Read-side (load_yaml) coverage — controlled stem + a real LLM-authored stem
# ---------------------------------------------------------------------------


def test_load_yaml_validates_on_read(monkeypatch, tmp_path):
    _install_schema(monkeypatch, tmp_path, "myllm", json.dumps(_SIMPLE))
    p = tmp_path / "myllm.yaml"
    p.write_text(yaml.safe_dump({"x": 1, "extra": 2}), encoding="utf-8")
    # warn mode: still returns the parsed data (drift only logged)
    _warn_mode(monkeypatch)
    assert rpr.load_yaml(p) == {"x": 1, "extra": 2}
    # raise mode: read-side validation blocks
    _raise_mode(monkeypatch)
    with pytest.raises(jsonschema.ValidationError):
        rpr.load_yaml(p)


def test_raw_writer_site_is_wired_deflate_write_yaml(monkeypatch, tmp_path):
    """Representative proof that a raw (non-save_yaml) writer site actually calls the
    helper: deflate_sharpe._write_yaml (insertion point 2). Raise-mode must block its
    write on a schema violation."""
    import deflate_sharpe as ds

    _install_schema(monkeypatch, tmp_path, "myart", json.dumps(_SIMPLE))
    _raise_mode(monkeypatch)
    out = tmp_path / "myart.yaml"
    with pytest.raises(jsonschema.ValidationError):
        ds._write_yaml(out, {"x": 1, "y": 2})
    assert not out.exists()


def test_load_yaml_real_llm_stem_hypothesis_card(monkeypatch, tmp_path):
    """hypothesis_card is an LLM-authored artifact with a real, strict schema and no
    Python writer — validated only on the read path. Uses the REAL schema dir."""
    p = tmp_path / "hypothesis_card.yaml"
    p.write_text(yaml.safe_dump({"not_a_declared_field": 1}), encoding="utf-8")
    _raise_mode(monkeypatch)
    with pytest.raises(jsonschema.ValidationError):
        rpr.load_yaml(p)


# ---------------------------------------------------------------------------
# Cross-file $ref: protocol_result.schema.json references
# trade_diagnostics.schema.json#/properties/summary. Without a registry/resolver
# jsonschema raises Unresolvable — silently skipping validation in warn mode and
# false-blocking a valid artifact in raise mode. Uses the REAL schema dir.
# ---------------------------------------------------------------------------

# run_protocol.py always emits trade_diagnostics_summary in protocol_summary.json, so
# the $ref is exercised on every real protocol_result — this is the load-bearing pin.
_VALID_PROTOCOL_RESULT = {
    "protocol_run_id": "r1",
    "config_sha256": "abc",
    "results": [],
    "per_symbol_summary": {},
    "verdict": "kill",
    "verdict_reason": "test",
    "trade_diagnostics_summary": {"win_rate_net": 0.5},  # reaches the $ref'd sub-schema
}


def test_protocol_result_with_summary_validates_clean(monkeypatch):
    """LOAD-BEARING: a valid protocol_result carrying trade_diagnostics_summary must
    validate CLEAN through the real helper in raise mode — proves the $ref resolves
    (would raise Unresolvable without the registry)."""
    _raise_mode(monkeypatch)
    wav.validate_workflow_artifact(Path("protocol_result.yaml"), _VALID_PROTOCOL_RESULT)


def test_protocol_result_invalid_summary_caught_via_ref(monkeypatch):
    """A summary that violates the $ref'd sub-schema (win_rate_net must be number|null)
    is CAUGHT in raise mode — proves the $ref actually resolves and bites, rather than
    being skipped."""
    _raise_mode(monkeypatch)
    bad = dict(_VALID_PROTOCOL_RESULT, trade_diagnostics_summary={"win_rate_net": "not a number"})
    with pytest.raises(jsonschema.ValidationError):
        wav.validate_workflow_artifact(Path("protocol_result.yaml"), bad)


# ---------------------------------------------------------------------------
# CUL-164: the 0-byte robustness_report.schema.json + template stubs were removed.
# robustness_analysis (workflow stage 9) is aspirational — no producer skill, no template,
# no instance anywhere (incl. runs/), and the schema was 0 bytes since origin. An empty
# schema for a stem is strictly WORSE than absence: as the target stem it hits json.loads
# and, under the raise flag, PROPAGATES JSONDecodeError (blocking the write). Removal
# restores the helper's intended opt-in-by-existence no-op. These two pin that.
# ---------------------------------------------------------------------------


def test_robustness_report_stem_is_clean_noop_after_stub_removal(monkeypatch, caplog):
    """With no schema on disk for the stem (stub removed), a robustness_report-shaped write
    is a clean opt-in no-op through the REAL helper — even in raise mode (schema absent ->
    skip) — and nothing is logged for the stem. RED before removal: the 0-byte file made
    this raise JSONDecodeError under the flag and log a per-write warning in warn mode."""
    _raise_mode(monkeypatch)  # real _SCHEMAS_DIR, no monkeypatch of it
    with caplog.at_level(logging.WARNING):
        wav.validate_workflow_artifact(
            Path("robustness_report.yaml"),
            {"robustness_summary": "anything", "score": 1},
        )
    assert not any("robustness_report" in r.getMessage() for r in caplog.records)


def test_empty_schema_reproduces_raise_mode_landmine(monkeypatch, tmp_path):
    """Mutation/pin for WHY removal was right, scratch-file based so it survives the on-disk
    removal: a 0-byte schema for the stem PROPAGATES JSONDecodeError under the raise flag
    (blocking the write) and is merely swallowed in warn mode. Absence (test above) is a
    clean skip; the empty stub is a landmine."""
    _install_schema(monkeypatch, tmp_path, "robustness_report", "")  # 0-byte stub
    _raise_mode(monkeypatch)
    with pytest.raises(json.JSONDecodeError):
        wav.validate_workflow_artifact(Path("robustness_report.yaml"), {"x": 1})
    _warn_mode(monkeypatch)
    wav.validate_workflow_artifact(Path("robustness_report.yaml"), {"x": 1})  # swallowed
