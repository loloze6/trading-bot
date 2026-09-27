"""
CUL-331: recording the holdout consume marker must not strip
campaign_data_policy.yaml's comments.

The marker (holdout_consumed_by) used to be written by save_yaml() of the
whole parsed dict, which dropped every comment line of the tracked policy file
on each record. _mark_holdout_consumed -- the only writer of that file, reached
by the legacy holdout gate (_route_holdout_evaluation step 4) and by the
verdict_routing_retired record paths (_record_spent_holdout and the S2d unlock,
both via _mark_holdout_consumed_if_absent) -- now edits the value in place.

Every test here writes a COPY of the policy: conftest's autouse sandbox
redirects rpr._DATA_POLICY_PATH into tmp_path and seeds it with a verbatim copy
of the real file; the real tracked file is only ever read. No holdout range is
written literally anywhere in this file.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402

_REAL_POLICY = _SR / "config" / "campaign_data_policy.yaml"
KEY = "holdout_consumed_by"
HYP = "H-CUL331"


def _real_bytes(newline: str | None = None) -> bytes:
    """The real policy file's bytes (read-only), optionally re-terminated."""
    raw = _REAL_POLICY.read_bytes()
    if newline is None:
        return raw
    return raw.replace(b"\r\n", b"\n").replace(b"\n", newline.encode())


def _sandbox_policy(tmp_path, content: bytes) -> Path:
    """Point the writer at a tmp copy, never the tracked file."""
    path = rpr._DATA_POLICY_PATH
    assert path.resolve() != _REAL_POLICY.resolve()
    assert tmp_path.resolve() in path.resolve().parents
    path.write_bytes(content)
    return path


def _key_line_idx(lines: list) -> int:
    idx = [i for i, ln in enumerate(lines) if ln.startswith(KEY.encode() + b":")]
    assert len(idx) == 1
    return idx[0]


# ---------------------------------------------------------------------------
# 1. The regression: every other byte of the real policy survives a record
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("newline", [None, "\r\n", "\n"], ids=["as_checked_out", "crlf", "lf"])
def test_marker_write_keeps_every_other_byte_of_the_real_policy(tmp_path, newline):
    """THE regression (fails on the save_yaml writer: ~248 comment lines lost).
    Only the key line changes; comments, blank lines, order, quoting and line
    endings are byte-identical; the parse equals the old document + marker."""
    before = _real_bytes(newline)
    old_doc = yaml.safe_load(before.decode("utf-8"))
    assert old_doc.get(KEY) in ([], None)  # the precondition the real file ships with
    path = _sandbox_policy(tmp_path, before)

    assert rpr._mark_holdout_consumed_if_absent(HYP) is True

    after = path.read_bytes()
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    assert len(new_lines) == len(old_lines)
    k = _key_line_idx(old_lines)
    for i, (a, b) in enumerate(zip(old_lines, new_lines)):
        if i != k:
            assert a == b, f"line {i + 1} changed"
    ending = old_lines[k][len(old_lines[k].rstrip(b"\r\n")):]
    assert new_lines[k] == f"{KEY}: [{HYP}]".encode() + ending
    comments = lambda blob: sum(1 for ln in blob.splitlines() if ln.lstrip().startswith(b"#"))  # noqa: E731
    assert comments(after) == comments(before) > 200
    new_doc = yaml.safe_load(after.decode("utf-8"))
    assert new_doc == {**old_doc, KEY: [HYP]}
    assert list(new_doc) == list(old_doc)


def test_marker_write_through_load_yaml_is_the_consumed_list(tmp_path):
    """The readers (load_yaml / _holdout_already_spent) see the spend."""
    _sandbox_policy(tmp_path, _real_bytes())
    rpr._mark_holdout_consumed_if_absent(HYP)
    assert rpr._holdout_already_spent(HYP)
    assert rpr._load_data_policy()[KEY] == [HYP]


# ---------------------------------------------------------------------------
# 2. Shapes of the value
# ---------------------------------------------------------------------------

_HEAD = "# head comment\nholdout_range: [a, b]  # range comment\n\n"
_TAIL = "\n# tail comment\nholdout_failure_is_terminal: true\n"


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_block_list_gets_one_new_item_line(tmp_path, newline):
    """A block list (what save_yaml writes) gains one `- id` line, at the
    items' own indent, after the last item; nothing else moves."""
    text = _HEAD + f"{KEY}:\n  - H-OTHER  # first\n  - 'H-2'\n" + _TAIL
    text = text.replace("\n", newline)
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, ["H-OTHER", "H-2"], HYP)
    expected = text.replace(f"  - 'H-2'{newline}", f"  - 'H-2'{newline}  - {HYP}{newline}")
    assert path.read_bytes() == expected.encode()


def test_flow_list_keeps_its_trailing_comment(tmp_path):
    text = _HEAD + f"{KEY}: [H-OTHER]   # spent ids ('#' inside: fine)\n" + _TAIL
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, ["H-OTHER"], HYP)
    assert path.read_bytes().decode() == text.replace(
        f"{KEY}: [H-OTHER]   #", f"{KEY}: [H-OTHER, {HYP}]   #")


@pytest.mark.parametrize("value", ["", " null", " ~"])
def test_null_value_becomes_a_one_item_list(tmp_path, value):
    text = _HEAD + f"{KEY}:{value}\n" + _TAIL
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, [], HYP)
    assert path.read_bytes().decode() == text.replace(f"{KEY}:{value}\n", f"{KEY}: [{HYP}]\n")


@pytest.mark.parametrize("ends_with_newline", [True, False])
def test_absent_key_is_appended_at_the_end(tmp_path, ends_with_newline):
    """Absent key: appended last (save_yaml's key order too)."""
    text = _HEAD + "holdout_failure_is_terminal: true" + ("\n" if ends_with_newline else "")
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, [], HYP)
    assert path.read_bytes().decode() == (
        _HEAD + "holdout_failure_is_terminal: true\n" + f"{KEY}: [{HYP}]\n")
    assert list(yaml.safe_load(path.read_text()))[-1] == KEY


def test_an_id_that_needs_quoting_is_quoted(tmp_path):
    odd = "H: #1"
    text = _HEAD + f"{KEY}:\n- H-OTHER\n" + _TAIL
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, ["H-OTHER"], odd)
    assert yaml.safe_load(path.read_text())[KEY] == ["H-OTHER", odd]


def test_missing_policy_file_is_still_created_as_before(tmp_path):
    """Unchanged: no file -> save_yaml creates it with just the marker."""
    path = rpr._DATA_POLICY_PATH
    assert tmp_path.resolve() in path.resolve().parents
    path.unlink(missing_ok=True)
    policy = {}
    rpr._mark_holdout_consumed(policy, [], HYP)
    assert yaml.safe_load(path.read_text()) == {KEY: [HYP]}
    assert policy == {KEY: [HYP]}  # the caller's dict is updated, as before


# ---------------------------------------------------------------------------
# 3. Refusals: raise, write nothing
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text,consumed,match", [
    (f"{KEY}: []\nx: 1\n{KEY}: []\n", [], "2 top-level"),
    (f'"{KEY}": []\nx: 1\n', [], "cannot locate"),
    (f"{KEY}: [H-OTHER]\n", [], "changed underneath"),          # stale caller view
    (f"{KEY}: [{HYP}]\n", [HYP], "already in"),                  # never double
    (f"{KEY}: [a,\n  b]\n", ["a", "b"], "did not parse back|YAML error"),  # multi-line flow
    (f"{KEY}:\n  # note\n  - a\n", ["a"], "did not parse back|YAML error"),
    ("key: [unclosed\n", [], "YAML error"),
])
def test_edit_refuses_and_leaves_the_file_untouched(tmp_path, text, consumed, match):
    path = _sandbox_policy(tmp_path, text.encode())
    with pytest.raises(ValueError, match=match):
        rpr._mark_holdout_consumed({}, consumed, HYP)
    assert path.read_bytes() == text.encode()
    assert sorted(p.name for p in path.parent.iterdir()) == [path.name]


# ---------------------------------------------------------------------------
# 4. Atomic: a failure mid-write leaves the original intact
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("fail_at", ["fsync", "replace"])
def test_failure_mid_write_leaves_the_original_intact(tmp_path, monkeypatch, fail_at):
    before = _real_bytes()
    path = _sandbox_policy(tmp_path, before)

    def _boom(*a, **k):
        raise OSError(f"simulated failure at {fail_at}")
    monkeypatch.setattr(rpr.os, fail_at, _boom)
    with pytest.raises(OSError, match="simulated"):
        rpr._mark_holdout_consumed_if_absent(HYP)
    assert path.read_bytes() == before
    assert sorted(p.name for p in path.parent.iterdir()) == [path.name]  # no temp left


# ---------------------------------------------------------------------------
# 5. Both writer paths go through the in-place edit; double consume refused
# ---------------------------------------------------------------------------

def _spy(monkeypatch) -> list:
    calls = []
    real = rpr._write_consumed_marker_in_place

    def _wrapped(path, consumed, hyp_id):
        calls.append(hyp_id)
        return real(path, consumed, hyp_id)
    monkeypatch.setattr(rpr, "_write_consumed_marker_in_place", _wrapped)
    return calls


def _legacy_run_dir(root: Path, hyp: str) -> Path:
    art = root / "artifacts"
    art.mkdir(parents=True)
    (root / "pipeline_state.yaml").write_text(yaml.safe_dump({"run_id": "run_x", "flags": {}}),
                                              encoding="utf-8")
    (art / "promotion_audit.yaml").write_text(yaml.safe_dump({"hypothesis_id": hyp}),
                                              encoding="utf-8")
    (art / "research_brief.yaml").write_text(yaml.safe_dump({"research_only": False}),
                                             encoding="utf-8")
    (art / "holdout_result.yaml").write_text(yaml.safe_dump({"status": "fail"}), encoding="utf-8")
    return root


def test_legacy_gate_writes_the_marker_in_place_and_refuses_a_second_spend(tmp_path, monkeypatch):
    before = _real_bytes()
    path = _sandbox_policy(tmp_path, before)
    calls = _spy(monkeypatch)
    run_dir = _legacy_run_dir(tmp_path / "run_x", HYP)

    assert rpr._route_holdout_evaluation(run_dir, "run_x") == "completed_rejected"
    assert calls == [HYP]
    after = path.read_bytes()
    assert yaml.safe_load(after.decode("utf-8"))[KEY] == [HYP]
    assert after.count(b"#") == before.count(b"#")

    # the second attempt is refused at step 2 and never writes
    assert rpr._route_holdout_evaluation(run_dir, "run_x") == "completed_rejected"
    assert calls == [HYP]
    assert path.read_bytes() == after


def test_retired_routing_record_path_writes_the_marker_in_place(tmp_path, monkeypatch):
    """The verdict_routing_retired / S2d record path (_mark_holdout_consumed_if_absent,
    record-first) on the real policy copy: marker written once, comments kept,
    never doubled on a re-entry."""
    from test_e059_6c_s2d_holdout_unlock import (  # noqa: E402
        _stopped_run, _decision, _resume, _result, _state, HYP as S2D_HYP, RUN_ID)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    run_dir = _stopped_run("validated")          # seeds a plain-dumped policy ...
    before = _real_bytes()
    path = _sandbox_policy(tmp_path, before)     # ... replaced by the real copy
    calls = _spy(monkeypatch)
    _decision(run_dir, "spend")
    _resume(run_dir)                              # awaiting the manual backtest
    assert path.read_bytes() == before            # nothing spent yet
    _result(run_dir, "pass")
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_promoted"
    assert state[rpr.HOLDOUT_CONSUME_RECORD_KEY]["hypothesis_id"] == S2D_HYP  # intent first
    assert calls == [S2D_HYP]
    after = path.read_bytes()
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    k = _key_line_idx(old_lines)
    assert [ln for i, ln in enumerate(new_lines) if i != k] == \
        [ln for i, ln in enumerate(old_lines) if i != k]
    assert yaml.safe_load(after.decode("utf-8"))[KEY] == [S2D_HYP]

    # a stray re-entry never writes the marker again
    rpr.update_state(path=run_dir, status="active", pending_stage="holdout_evaluation")
    rpr.run_loop(RUN_ID)
    assert calls == [S2D_HYP]
    assert path.read_bytes() == after


def test_the_only_writer_of_the_policy_file_is_the_marker():
    """Every save_yaml(_DATA_POLICY_PATH, ...) in the workflow is the
    missing-file branch of _mark_holdout_consumed: no other writer can strip
    the comments again."""
    src = Path(rpr.__file__).read_text(encoding="utf-8")
    assert src.count("save_yaml(_DATA_POLICY_PATH") == 1
    body = src.split("def _mark_holdout_consumed(", 1)[1].split("\ndef ", 1)[0]
    assert "save_yaml(_DATA_POLICY_PATH" in body
    assert "_write_consumed_marker_in_place(_DATA_POLICY_PATH" in body
