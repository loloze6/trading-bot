"""
CUL-331: recording the holdout consume marker must not strip
campaign_data_policy.yaml's comments -- and must NEVER be less safe than the
save_yaml writer it replaces. The marker is written after the seal is spent, so
it never refuses: any shape the in-place edit cannot handle falls back to
master's full rewrite (with a WARNING that comments were lost).

The marker (holdout_consumed_by) used to be written by save_yaml() of the
whole parsed dict. _mark_holdout_consumed -- the only writer of that file,
reached by the legacy holdout gate (_route_holdout_evaluation step 4) and the
verdict_routing_retired record paths (_record_spent_holdout and the S2d unlock,
via _mark_holdout_consumed_if_absent) -- now edits the value in place when it
safely can.

Every test here writes a COPY of the policy: conftest's autouse sandbox
redirects rpr._DATA_POLICY_PATH into tmp_path and seeds it with a verbatim copy
of the real file; the real tracked file is only ever read. No holdout range is
written literally anywhere in this file.
"""
from __future__ import annotations

import os
import stat
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
LOST = "comments were LOST"


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


def _only_policy_left(path: Path) -> None:
    """No temp file and no lock file left behind."""
    assert sorted(p.name for p in path.parent.iterdir()) == [path.name]


def _comments(blob: bytes) -> int:
    return sum(1 for ln in blob.splitlines() if ln.lstrip().startswith(b"#"))


# ---------------------------------------------------------------------------
# 1. The regression: every other byte of the real policy survives a record
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("newline", [None, "\r\n", "\n"], ids=["as_checked_out", "crlf", "lf"])
def test_marker_write_keeps_every_other_byte_of_the_real_policy(tmp_path, newline, capsys):
    """THE regression (fails on the save_yaml writer: every comment line lost).
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
    assert _comments(after) == _comments(before) > 200
    new_doc = yaml.safe_load(after.decode("utf-8"))
    assert new_doc == {**old_doc, KEY: [HYP]}
    assert list(new_doc) == list(old_doc)
    assert "WARNING" not in capsys.readouterr().out
    _only_policy_left(path)


def test_marker_write_through_load_yaml_is_the_consumed_list(tmp_path):
    """The readers (load_yaml / _holdout_already_spent) see the spend."""
    _sandbox_policy(tmp_path, _real_bytes())
    rpr._mark_holdout_consumed_if_absent(HYP)
    assert rpr._holdout_already_spent(HYP)
    assert rpr._load_data_policy()[KEY] == [HYP]


# ---------------------------------------------------------------------------
# 2. Shapes the in-place edit handles (no WARNING, only the value changes)
# ---------------------------------------------------------------------------

_HEAD = "# head comment\nholdout_range: [a, b]  # range comment\n\n"
_TAIL = "\n# tail comment\nholdout_failure_is_terminal: true\n"


def _in_place(tmp_path, capsys, value_text: str, consumed, expected_value_text: str,
              hyp=HYP, newline="\n"):
    text = (_HEAD + value_text + _TAIL).replace("\n", newline)
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, consumed, hyp)
    assert "WARNING" not in capsys.readouterr().out
    expected = (_HEAD + expected_value_text + _TAIL).replace("\n", newline)
    assert path.read_bytes().decode() == expected
    _only_policy_left(path)
    return yaml.safe_load(expected)[KEY]


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_block_list_gets_one_new_item_line(tmp_path, capsys, newline):
    """A block list (what save_yaml writes) gains one `- id` line, at the
    items' own indent, after the last item; nothing else moves."""
    got = _in_place(tmp_path, capsys, f"{KEY}:\n  - H-OTHER  # first\n  - 'H-2'\n",
                    ["H-OTHER", "H-2"],
                    f"{KEY}:\n  - H-OTHER  # first\n  - 'H-2'\n  - {HYP}\n", newline=newline)
    assert got == ["H-OTHER", "H-2", HYP]


def test_block_list_with_comments_and_blanks_around_items(tmp_path, capsys):
    """Review 1+2: a comment on the key line, a comment/blank line before the
    items and comments between items are kept; the new item goes last."""
    value = (f"{KEY}:   # spent ids\n\n  # first spend\n  - H-A\n  # second spend\n"
             f"\n  - H-B\n# a column-0 note after the list\n")
    got = _in_place(tmp_path, capsys, value, ["H-A", "H-B"],
                    value.replace("  - H-B\n", f"  - H-B\n  - {HYP}\n"))
    assert got == ["H-A", "H-B", HYP]


def test_flow_list_append_keeps_quoting_and_spacing(tmp_path, capsys):
    """Review 6: `, id` goes before the closing bracket; the existing ids,
    their quoting and spacing, the key spacing and the comment are untouched."""
    value = f"{KEY} :   [ 'H-A' ,\"H-B\",H-C  ]   # spent ids ('#' inside: fine)\n"
    got = _in_place(tmp_path, capsys, value, ["H-A", "H-B", "H-C"],
                    value.replace("H-C  ]", f"H-C, {HYP}  ]"))
    assert got == ["H-A", "H-B", "H-C", HYP]


@pytest.mark.parametrize("value,expected", [
    (f"{KEY}: []\n", f"{KEY}: [{HYP}]\n"),
    (f"{KEY}: [ ]  # none yet\n", f"{KEY}: [ {HYP}]  # none yet\n"),
    (f"{KEY}:\n", f"{KEY}: [{HYP}]\n"),
    (f"{KEY}: null\n", f"{KEY}: [{HYP}]\n"),
    (f"{KEY}: ~   # nothing\n", f"{KEY}: [{HYP}]   # nothing\n"),
    (f"{KEY}:  # nothing\n", f"{KEY}: [{HYP}]  # nothing\n"),
])
def test_empty_and_null_values(tmp_path, capsys, value, expected):
    assert _in_place(tmp_path, capsys, value, [], expected) == [HYP]


def test_scalar_string_value_becomes_a_list_keeping_the_old_spend(tmp_path, capsys):
    """Review 3: `holdout_consumed_by: H-1` is ["H-1"]; the old spend is kept."""
    got = _in_place(tmp_path, capsys, f"{KEY}: H-1\n", "H-1", f"{KEY}: [H-1, {HYP}]\n")
    assert got == ["H-1", HYP]


def test_absent_key_is_appended_at_the_end(tmp_path, capsys):
    text = _HEAD + "holdout_failure_is_terminal: true"  # no final newline either
    path = _sandbox_policy(tmp_path, text.encode())
    rpr._mark_holdout_consumed({}, [], HYP)
    assert "WARNING" not in capsys.readouterr().out
    assert path.read_bytes().decode() == (
        _HEAD + "holdout_failure_is_terminal: true\n" + f"{KEY}: [{HYP}]\n")


def test_an_id_that_needs_quoting_is_quoted(tmp_path, capsys):
    odd = "H: #1"
    got = _in_place(tmp_path, capsys, f"{KEY}:\n- H-OTHER\n", ["H-OTHER"],
                    f"{KEY}:\n- H-OTHER\n- 'H: #1'\n", hyp=odd)
    assert got == ["H-OTHER", odd]


def test_missing_policy_file_is_created_exactly_as_save_yaml_did(tmp_path):
    """Unchanged: no file -> master's save_yaml bytes of the caller's policy."""
    path = rpr._DATA_POLICY_PATH
    assert tmp_path.resolve() in path.resolve().parents
    path.unlink(missing_ok=True)
    policy = {"holdout_range": ["a", "b"]}
    rpr._mark_holdout_consumed(policy, [], HYP)
    assert path.read_bytes() == rpr._yaml_file_bytes({"holdout_range": ["a", "b"], KEY: [HYP]})
    assert policy == {"holdout_range": ["a", "b"], KEY: [HYP]}  # caller's dict updated, as before
    _only_policy_left(path)


# ---------------------------------------------------------------------------
# 3. Shapes the edit cannot handle: master's full rewrite + a loud WARNING
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text,consumed,expected_list", [
    (f"{KEY}: [H-A]\nx: 1\n{KEY}: []\n", [], [HYP]),                 # key twice
    (f'"{KEY}": [H-A]  # quoted key\nx: 1\n', ["H-A"], ["H-A", HYP]),
    (f"# c\n{KEY}: [H-A,\n  H-B]\nx: 1\n", ["H-A", "H-B"], ["H-A", "H-B", HYP]),  # multi-line flow
    (f"{KEY}:\n  - H-A: note\n    more: x\n", [{"H-A": "note", "more": "x"}],
     [{"H-A": "note", "more": "x"}, HYP]),                           # multi-line item
    (f"# c\nnote: colon: inside\n{KEY}: [H-A]\n", ["H-A"], ["H-A", HYP]),  # repair-only
])
def test_unhandled_shapes_still_record_via_full_rewrite(tmp_path, capsys, text, consumed,
                                                        expected_list):
    """Review 1+2: never refuse after the spend. The file is rewritten as
    save_yaml wrote it (load_yaml's parse + the marker) and says so loudly."""
    path = _sandbox_policy(tmp_path, text.encode())
    base = rpr.load_yaml(path)
    rpr._mark_holdout_consumed({}, consumed, HYP)
    out = capsys.readouterr().out
    assert "WARNING (CUL-331)" in out and LOST in out
    assert path.read_bytes() == rpr._yaml_file_bytes({**base, KEY: expected_list})
    assert rpr.load_yaml(path)[KEY] == expected_list
    _only_policy_left(path)


@pytest.mark.parametrize("value,kept", [
    ({"H-A": "note"}, str({"H-A": "note"})),
    (7, "7"),
    (True, "True"),
])
def test_non_list_value_is_never_erased(tmp_path, capsys, value, kept):
    """Review 3: a mapping or other non-list, non-string value is kept,
    stringified, at the head of the new list (full rewrite, WARNING)."""
    path = _sandbox_policy(tmp_path, yaml.safe_dump({"holdout_range": ["a", "b"], KEY: value},
                                                    sort_keys=False).encode())
    rpr._mark_holdout_consumed({}, [], HYP)
    out = capsys.readouterr().out
    assert "was a" in out and LOST in out
    assert rpr.load_yaml(path)[KEY] == [kept, HYP]
    assert rpr.load_yaml(path)["holdout_range"] == ["a", "b"]


def test_unparseable_policy_falls_back_to_the_callers_view(tmp_path, capsys):
    """Even a file no parse can read gets the marker: master's behaviour
    (the caller's policy dict + the marker), never a refusal."""
    path = _sandbox_policy(tmp_path, b"holdout_range: [a, b\n{{{\n")
    rpr._mark_holdout_consumed({"holdout_range": ["a", "b"]}, [], HYP)
    assert LOST in capsys.readouterr().out
    assert rpr.load_yaml(path) == {"holdout_range": ["a", "b"], KEY: [HYP]}
    # the caller's view already listing the id is no reason to leave the file unreadable
    path.write_bytes(b"holdout_range: [a, b\n{{{\n")
    rpr._mark_holdout_consumed({KEY: [HYP]}, [HYP], HYP)
    assert rpr.load_yaml(path) == {KEY: [HYP]}


# ---------------------------------------------------------------------------
# 4. Never drop, never double (single-use semantics unchanged)
# ---------------------------------------------------------------------------

def test_a_stale_caller_view_is_merged_not_overwritten(tmp_path, capsys):
    """Master wrote consumed + [hyp] and dropped another writer's entry; now
    the on-disk list is kept and the caller's ids are added."""
    path = _sandbox_policy(tmp_path, f"{KEY}: [H-OTHER]\n".encode())
    rpr._mark_holdout_consumed({}, ["H-MINE"], HYP)
    assert "WARNING" not in capsys.readouterr().out
    assert path.read_bytes() == f"{KEY}: [H-OTHER, H-MINE, {HYP}]\n".encode()


def test_an_id_already_on_disk_is_not_written_twice(tmp_path):
    text = f"# c\n{KEY}: [{HYP}]\n"
    path = _sandbox_policy(tmp_path, text.encode())
    policy = {}
    rpr._mark_holdout_consumed(policy, [], HYP)
    assert path.read_bytes() == text.encode()
    assert policy[KEY] == [HYP]
    _only_policy_left(path)


def test_already_spent_is_exact_membership_never_a_substring():
    """Review 3: a scalar string must not substring-match."""
    policy = {KEY: "H-10"}
    assert not rpr._holdout_already_spent("H-1", policy)
    assert rpr._holdout_already_spent("H-10", policy)
    assert not rpr._holdout_already_spent("H-1", {KEY: None})
    assert rpr._holdout_already_spent("H-1", {KEY: ["H-1"]})


def test_other_pending_spends_reads_a_scalar_as_one_id():
    """The pending-spend reader normalises the same way (one id, not chars)."""
    rpr._DATA_POLICY_PATH.write_text(f"{KEY}: H-10\n", encoding="utf-8")
    pending = rpr._other_pending_spends("run_none")
    assert any("['H-10']" in p for p in pending), pending


# ---------------------------------------------------------------------------
# 5. Atomic, durable, locked, and re-applied on a concurrent change
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
    _only_policy_left(path)  # no temp file, and the lock was released


def test_the_temp_file_is_fsynced_before_the_replace(tmp_path, monkeypatch):
    path = _sandbox_policy(tmp_path, _real_bytes())
    events = []
    real_fsync, real_replace = os.fsync, os.replace
    monkeypatch.setattr(rpr.os, "fsync", lambda fd: (events.append("fsync"), real_fsync(fd))[1])
    monkeypatch.setattr(rpr.os, "replace", lambda a, b: (events.append("replace"),
                                                         real_replace(a, b))[1])
    rpr._mark_holdout_consumed_if_absent(HYP)
    assert events[:2] == ["fsync", "replace"]
    assert rpr._holdout_already_spent(HYP)
    assert path.exists()


@pytest.mark.skipif(os.name == "nt", reason="POSIX file modes and directory fsync")
def test_posix_mode_is_kept_and_the_directory_is_fsynced(tmp_path, monkeypatch):
    path = _sandbox_policy(tmp_path, _real_bytes())
    path.chmod(0o644)
    opened = []
    real_open = os.open
    monkeypatch.setattr(rpr.os, "open", lambda p, *a, **k: (opened.append(p), real_open(p, *a, **k))[1])
    rpr._mark_holdout_consumed_if_absent(HYP)
    assert stat.S_IMODE(path.stat().st_mode) == 0o644
    assert str(path.parent) in opened


def test_a_concurrent_append_is_re_read_and_re_applied(tmp_path, monkeypatch, capsys):
    """Review 5: another writer lands between our read and our replace; the
    bytes check sees it, re-reads and re-applies -- both entries survive."""
    text = f"# policy\n{KEY}: []\nx: 1\n"
    path = _sandbox_policy(tmp_path, text.encode())
    real_mkstemp = rpr.tempfile.mkstemp
    fired = []

    def _mkstemp(*a, **k):
        if not fired:
            fired.append(1)
            path.write_bytes(text.replace(f"{KEY}: []", f"{KEY}: [H-OTHER]").encode())
        return real_mkstemp(*a, **k)
    monkeypatch.setattr(rpr.tempfile, "mkstemp", _mkstemp)
    rpr._mark_holdout_consumed({}, [], HYP)
    assert "re-applying" in capsys.readouterr().out
    assert path.read_bytes() == f"# policy\n{KEY}: [H-OTHER, {HYP}]\nx: 1\n".encode()
    _only_policy_left(path)


def test_the_write_runs_under_the_policy_lock(tmp_path, monkeypatch):
    path = _sandbox_policy(tmp_path, _real_bytes())
    lock = path.parent / rpr._POLICY_LOCK_FILENAME
    seen = []
    real = rpr._atomic_write_bytes

    def _spy(*a, **k):
        seen.append(lock.exists())
        return real(*a, **k)
    monkeypatch.setattr(rpr, "_atomic_write_bytes", _spy)
    rpr._mark_holdout_consumed_if_absent(HYP)
    assert seen == [True]
    assert not lock.exists()


def test_a_held_lock_never_blocks_the_record(tmp_path, monkeypatch, capsys):
    """A lock that cannot be taken (live holder, bounded wait) -> WARNING and
    the marker is recorded anyway, as master's lock-free writer always did."""
    import campaign_lock
    cm = rpr._campaign_memory_module()
    monkeypatch.setattr(cm, "MEMORY_LOCK_WAIT_SECONDS", 0.2)
    path = _sandbox_policy(tmp_path, _real_bytes())
    lock = path.parent / rpr._POLICY_LOCK_FILENAME
    campaign_lock.acquire(lock)  # held by this (live) process
    try:
        rpr._mark_holdout_consumed_if_absent(HYP)
    finally:
        campaign_lock.release(lock)
    assert "could not lock" in capsys.readouterr().out
    assert rpr._holdout_already_spent(HYP)


@pytest.mark.parametrize("doc", [
    {"a": 1, "b": [1, 2], "c": {"d": "é → ü"}, "e": None},
    {"run_id": "run_1", "flags": {}, "text": "line1\nline2\n", "n": 1.5},
    [1, "two", {"three": 3}],
])
def test_save_yaml_bytes_are_unchanged(tmp_path, doc):
    """Review 8: save_yaml now goes through _atomic_write_bytes; its bytes
    are exactly what the old text-mode safe_dump wrote."""
    ref = tmp_path / "ref.yaml"
    with open(ref, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True)
    out = tmp_path / "sub" / "out.yaml"
    rpr.save_yaml(out, doc)
    assert out.read_bytes() == ref.read_bytes()
    assert sorted(p.name for p in out.parent.iterdir()) == ["out.yaml"]


# ---------------------------------------------------------------------------
# 6. Both writer paths go through the new writer; double consume refused
# ---------------------------------------------------------------------------

def _spy(monkeypatch) -> list:
    calls = []
    real = rpr._write_consumed_marker

    def _wrapped(path, policy, consumed, hyp_id):
        calls.append(hyp_id)
        return real(path, policy, consumed, hyp_id)
    monkeypatch.setattr(rpr, "_write_consumed_marker", _wrapped)
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


@pytest.mark.parametrize("shape", ["[]", "", " ~", " null"])
def test_legacy_gate_records_on_every_empty_shape_and_refuses_a_second_spend(
        tmp_path, monkeypatch, shape, capsys):
    """Review 4: null / ~ / empty values end to end through the legacy gate
    (master crashed on list(None) there, after the spend)."""
    real = _real_bytes()
    line = f"{KEY}: []".encode()
    assert real.count(line) == 1
    before = real.replace(line, f"{KEY}:{shape if shape != '[]' else ' []'}".encode())
    path = _sandbox_policy(tmp_path, before)
    calls = _spy(monkeypatch)
    run_dir = _legacy_run_dir(tmp_path / "run_x", HYP)

    assert rpr._route_holdout_evaluation(run_dir, "run_x") == "completed_rejected"
    assert calls == [HYP]
    after = path.read_bytes()
    assert "WARNING" not in capsys.readouterr().out
    assert yaml.safe_load(after.decode("utf-8"))[KEY] == [HYP]
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    k = _key_line_idx(old_lines)
    assert [ln for i, ln in enumerate(new_lines) if i != k] == \
        [ln for i, ln in enumerate(old_lines) if i != k]

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
    """No save_yaml(_DATA_POLICY_PATH, ...) is left anywhere in the workflow:
    the one writer is _write_consumed_marker, called from
    _mark_holdout_consumed; save_yaml shares its atomic write helper."""
    src = Path(rpr.__file__).read_text(encoding="utf-8")
    assert src.count("save_yaml(_DATA_POLICY_PATH") == 0
    body = src.split("def _mark_holdout_consumed(", 1)[1].split("\ndef ", 1)[0]
    assert "_write_consumed_marker(_DATA_POLICY_PATH" in body
    save = src.split("def save_yaml(", 1)[1].split("\ndef ", 1)[0]
    assert "_atomic_write_bytes(path, _yaml_file_bytes(data))" in save
