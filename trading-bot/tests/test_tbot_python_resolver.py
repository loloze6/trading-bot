"""
The strategy-research scripts must find a runnable trading-bot interpreter — FORK-ONLY.

Four sites hardcoded `Path("..") / "venv" / "Scripts" / "python.exe"`
(`workflow/run_phase1_research.py:990,1462,4889`, `tools/retune_regime_detector.py:486`),
which is upstream's Windows layout and resolves to nothing runnable on macOS. Both
files now call a `_resolve_tbot_python()` that tries the Windows layout first and
this fork's `.venv/bin/python` second.

Windows-first is not cosmetic: it is what keeps upstream's tree resolving to the
exact interpreter it always has. But existence alone is the wrong test here, and
that is measured, not theoretical — upstream's Windows venv is COMMITTED to this
repository (449 tracked files under `venv/`, `venv/Scripts/python.exe` at mode
100644, `PE32+ executable for MS Windows`). `.gitignore` lists `venv/` but the
files predate the rule, so gitignore cannot untrack them and every checkout —
including this Mac — carries them. From `strategy-research/`, that path
`.exists()` on macOS and running it raises `PermissionError`. An existence-only
resolver would therefore hand macOS a Windows PE binary and the port would be a
silent no-op. So a candidate must be a regular file AND pass
`os.access(..., os.X_OK)`. That is STRICTER than the stdlib's own
`shutil._access_check`, which pairs the same X_OK test with a merely
not-a-directory clause where this requires `is_file()`; the extra strictness is
deliberate, because a directory is searchable and therefore passes X_OK on its
own — one sitting at the Windows candidate would shadow a working macOS
interpreter and then die at spawn with the same `PermissionError [Errno 13]` the
PE binary gives, never reaching the RuntimeError below. On Windows `os.access`
reports existence for X_OK, so upstream is unaffected. A `chmod +x`'d PE file
would still be selected and then fail at spawn with an exec format error — loud,
and deliberately not guarded against.

The two copies anchor differently, which is why every behavioural test below runs
against BOTH:

  run_phase1_research.py     CWD-relative (`Path("..")`), because the script itself
                             is CWD-relative (`ROOT = Path(".")`, :58) and is run
                             from `strategy-research/`.
  retune_regime_detector.py  anchored at its own `_REPO` absolute. Keeping this one
                             CWD-relative would NOT have preserved behaviour: it is
                             documented as run from the repo root (:23) but passes
                             `cwd=_SR` to the subprocess, and ON POSIX a relative
                             exec path is resolved against the CHILD's cwd (measured
                             here) — so the old hardcoded path only ever worked
                             because the child, not the parent, resolved it. Windows
                             is the opposite: CreateProcess resolves against the
                             PARENT's cwd, which means the old hardcode was likely
                             already broken there from the documented repo-root
                             invocation. The absolute anchor is right under either
                             semantics. A parent-side existence check against the
                             repo-root CWD would look one level above the repo.

There is deliberately no textual drift guard between the copies: they are no
longer identical, so comparing their source would only ever assert something
false. The guard is behavioural instead — every case below is parametrized over
both files, so a divergence in one copy fails that copy's parametrization.

These tests never import either module. `run_phase1_research.py` imports
`claude_agent_sdk` and `google.genai` at module level, neither of which belongs in
a fast unit test. Instead the resolver is located by name in the shipped source
with `ast`, its own source segment is compiled and executed in a fresh namespace,
and that real function is driven against fake trees. The code under test is the
code that ships; nothing here is a re-implementation.
"""

import ast
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
RESOLVER_NAME = "_resolve_tbot_python"

CWD_RELATIVE = "cwd"
REPO_ANCHORED = "repo"
# The one path segment that only ever appears in an interpreter candidate.
PATH_LITERAL = "Scripts"

LAYOUTS = (
    (REPO_ROOT / "strategy-research" / "workflow" / "run_phase1_research.py", CWD_RELATIVE),
    (REPO_ROOT / "strategy-research" / "tools" / "retune_regime_detector.py", REPO_ANCHORED),
)
ANCHORED_LAYOUTS = tuple(layout for layout in LAYOUTS if layout[1] == REPO_ANCHORED)
# An empty parametrize list collects zero cases and reports green, so the filter
# has to prove it selected something.
assert ANCHORED_LAYOUTS, "no REPO_ANCHORED layout — the anchored test would vanish"


def _module_tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


def _resolver_defs(tree: ast.Module) -> list:
    return [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == RESOLVER_NAME]


def _resolver_source(path: Path) -> str:
    """The resolver's own source text, located by name in the shipped file."""
    source = path.read_text(encoding="utf-8")
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name == RESOLVER_NAME:
            segment = ast.get_source_segment(source, node)
            assert segment and segment.startswith(f"def {RESOLVER_NAME}"), (
                f"extracted an empty or wrong segment for {RESOLVER_NAME} in {path} — "
                f"every assertion downstream would be vacuous"
            )
            return segment
    raise AssertionError(
        f"no module-level {RESOLVER_NAME}() in {path}; the four hardcoded "
        f"Windows interpreter paths are unported or the resolver was renamed"
    )


def _load_resolver(path: Path, repo_root: Path):
    """Compile and execute only the resolver, with no import of its module.

    Both anchors are supplied — `_REPO` here, the CWD via `monkeypatch.chdir` in
    the tests — so one helper drives either copy; each uses the one it references.
    """
    namespace = {"Path": Path, "os": os, "_REPO": str(repo_root)}
    exec(compile(_resolver_source(path), str(path), "exec"), namespace)
    return namespace[RESOLVER_NAME]


def _make_tree(
    tmp_path: Path, *, windows: bool, mac: bool, windows_executable: bool = True, windows_as_dir: bool = False
) -> Path:
    """Build a fake repo root and return the CWD the scripts are run from."""
    cwd = tmp_path / "strategy-research"
    cwd.mkdir()
    if windows:
        target = tmp_path / "venv" / "Scripts" / "python.exe"
        target.parent.mkdir(parents=True)
        if windows_as_dir:
            target.mkdir()
        else:
            target.write_text("")
            target.chmod(0o755 if windows_executable else 0o644)
    if mac:
        target = tmp_path / ".venv" / "bin" / "python"
        target.parent.mkdir(parents=True)
        target.write_text("")
        target.chmod(0o755)
    return cwd


def _tried_paths(mode: str, tmp_path: Path):
    """The candidate strings the failure message is required to name."""
    base = Path("..") if mode == CWD_RELATIVE else tmp_path
    return (base / "venv" / "Scripts" / "python.exe", base / ".venv" / "bin" / "python")


def _ids(value):
    return value.name if isinstance(value, Path) else value


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_windows_layout_alone_resolves_to_it(source, mode, tmp_path, monkeypatch):
    monkeypatch.chdir(_make_tree(tmp_path, windows=True, mac=False))

    resolved = Path(_load_resolver(source, tmp_path)()).resolve()

    assert resolved == (tmp_path / "venv" / "Scripts" / "python.exe").resolve()


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_mac_layout_alone_resolves_to_it(source, mode, tmp_path, monkeypatch):
    monkeypatch.chdir(_make_tree(tmp_path, windows=False, mac=True))

    resolved = Path(_load_resolver(source, tmp_path)()).resolve()

    assert resolved == (tmp_path / ".venv" / "bin" / "python").resolve()


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_windows_wins_when_both_layouts_are_present(source, mode, tmp_path, monkeypatch):
    """Upstream's tree must resolve exactly as it does today.

    The Windows candidate is created executable because that is what upstream's
    checkout looks like from Windows, where `os.access(existing_file, X_OK)` is
    true. This is the test that pins "Jeremy's tree behaves identically".
    """
    monkeypatch.chdir(_make_tree(tmp_path, windows=True, mac=True))

    resolved = Path(_load_resolver(source, tmp_path)()).resolve()

    assert resolved == (tmp_path / "venv" / "Scripts" / "python.exe").resolve()


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Fixture premise unconstructible on Windows: chmod(0o644) "
    "yields mode 0o100777 and os.access(X_OK) is unconditionally "
    "True for any existing file, so a present-but-unrunnable "
    "candidate cannot be built. The guard this exercises is "
    "macOS-specific (upstream's committed Windows venv).",
)
@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_unrunnable_windows_candidate_does_not_shadow_the_mac_one(source, mode, tmp_path, monkeypatch):
    """The committed-Windows-venv case: present, so `.exists()`, but not runnable."""
    monkeypatch.chdir(_make_tree(tmp_path, windows=True, mac=True, windows_executable=False))

    resolved = Path(_load_resolver(source, tmp_path)()).resolve()

    assert resolved == (tmp_path / ".venv" / "bin" / "python").resolve()


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_no_candidate_raises_naming_both_tried_paths(source, mode, tmp_path, monkeypatch):
    monkeypatch.chdir(_make_tree(tmp_path, windows=False, mac=False))

    with pytest.raises(RuntimeError) as excinfo:
        _load_resolver(source, tmp_path)()

    message = str(excinfo.value)
    for candidate in _tried_paths(mode, tmp_path):
        assert str(candidate) in message, (
            f"the failure must name every path it tried; {candidate} is missing from: {message}"
        )


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_a_directory_at_a_candidate_path_is_not_selected(source, mode, tmp_path, monkeypatch):
    """Directories are searchable, so a directory passes `os.access(X_OK)`.

    Without a file-ness check a directory sitting at the Windows candidate is
    selected and shadows a perfectly good macOS interpreter, then dies at spawn
    with `PermissionError [Errno 13]` — the same errno the committed PE binary
    produces, and reached without ever raising the resolver's own RuntimeError.
    """
    monkeypatch.chdir(_make_tree(tmp_path, windows=True, mac=True, windows_as_dir=True))

    resolved = Path(_load_resolver(source, tmp_path)()).resolve()

    assert resolved == (tmp_path / ".venv" / "bin" / "python").resolve()


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_a_directory_as_the_only_candidate_raises(source, mode, tmp_path, monkeypatch):
    """No usable interpreter must stay loud, not degrade into returning a directory."""
    monkeypatch.chdir(_make_tree(tmp_path, windows=True, mac=False, windows_as_dir=True))

    with pytest.raises(RuntimeError):
        _load_resolver(source, tmp_path)()


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_no_interpreter_path_literal_outside_the_resolver(source, mode):
    """Upstream still carries all four hardcodes, so every merge conflicts here.

    A conflict resolved toward upstream silently reinstates
    `Path("..") / "venv" / "Scripts" / "python.exe"` at a call site, and nothing
    else in this suite would notice: the resolver stays correct, it is simply
    bypassed. Only string Constants EQUAL to the literal count — the docstrings
    name the path in prose, which is a substring, not an equal literal.
    """
    tree = _module_tree(source)
    spans = [(node.lineno, node.end_lineno) for node in _resolver_defs(tree)]
    assert spans, f"no module-level {RESOLVER_NAME}() in {source}"

    inside, outside = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and node.value == PATH_LITERAL:
            target = inside if any(lo <= node.lineno <= hi for lo, hi in spans) else outside
            target.append(node.lineno)

    assert inside, (
        f"no {PATH_LITERAL!r} literal inside {RESOLVER_NAME}() in {source} — the "
        f"resolver stopped naming the Windows layout, so this guard would pass "
        f"vacuously no matter what the call sites do"
    )
    assert not outside, (
        f"interpreter path literal {PATH_LITERAL!r} at {source.name}:{outside}, "
        f"outside {RESOLVER_NAME}(); a call site has been re-hardcoded and now "
        f"bypasses the resolver without failing anything else"
    )


@pytest.mark.parametrize(("source", "mode"), LAYOUTS, ids=_ids)
def test_exactly_one_module_level_resolver_is_defined(source, mode):
    """A bad merge could duplicate the def, decoupling what is tested from what runs.

    Python honours the LAST definition at runtime while this file's `ast` lookup
    takes the FIRST, so a duplicate would leave every test above green while
    exercising dead code.
    """
    defs = _resolver_defs(_module_tree(source))

    assert len(defs) == 1, (
        f"{len(defs)} module-level {RESOLVER_NAME}() definitions in {source} at "
        f"lines {[node.lineno for node in defs]}; runtime uses the last, this "
        f"file's extraction uses the first"
    )


@pytest.mark.parametrize(("source", "mode"), ANCHORED_LAYOUTS, ids=_ids)
def test_the_repo_anchored_copy_ignores_the_cwd(source, mode, tmp_path, monkeypatch):
    """`retune`'s resolver must not change answer with the invocation directory.

    Its two documented CWDs — repo root and `strategy-research/` — are the whole
    reason it is anchored, so the same interpreter must come back from anywhere.
    Parametrized over the anchored files only: generating a CWD-relative case just
    to skip it would leave a permanent skip in every run, and a skip that can never
    turn into a pass is indistinguishable from a test that has quietly died.
    """
    cwd = _make_tree(tmp_path, windows=False, mac=True)
    resolver = _load_resolver(source, tmp_path)
    expected = (tmp_path / ".venv" / "bin" / "python").resolve()

    for invocation_dir in (cwd, tmp_path, tmp_path.parent):
        monkeypatch.chdir(invocation_dir)
        assert Path(resolver()).resolve() == expected, (
            f"anchored resolver changed answer when run from {invocation_dir}"
        )
