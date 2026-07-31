"""
The strategy-research scripts must find a runnable trading-bot interpreter — FORK-ONLY.

Four sites hardcoded `Path("..") / "venv" / "Scripts" / "python.exe"`
(`workflow/run_phase1_research.py:990,1462,4889`, `tools/retune_regime_detector.py:486`),
which is upstream's Windows layout and resolves to nothing runnable on macOS. Both
files now call a `_resolve_tbot_python()` that tries the Windows layout first and
this fork's `../.venv/bin/python` second.

Windows-first is not cosmetic: it is what keeps upstream's tree resolving to the
exact interpreter it always has. But existence alone is the wrong test here, and
that is measured, not theoretical — upstream's Windows venv is COMMITTED to this
repository (449 tracked files under `venv/`, `venv/Scripts/python.exe` at mode
100644, `PE32+ executable for MS Windows`). `.gitignore` lists `venv/` but the
files predate the rule, so gitignore cannot untrack them and every checkout —
including this Mac — carries them. From `strategy-research/`, that path
`.exists()` on macOS and running it raises `PermissionError`. An existence-only
resolver would therefore hand macOS a Windows PE binary and the port would be a
silent no-op. So a candidate must also pass `os.access(..., os.X_OK)`, which is
the same predicate the stdlib's own `shutil.which` uses (`shutil._access_check`);
on Windows `os.access` reports existence for X_OK, so upstream is unaffected.

These tests never import either module. `run_phase1_research.py` imports
`claude_agent_sdk` and `google.genai` at module level and constructs a
`genai.Client()` at import-adjacent scope, none of which belongs in a fast unit
test. Instead the resolver is located by name in the shipped source with `ast`,
its own source segment is compiled and executed in a fresh namespace, and that
real function is driven against fake trees. The code under test is the code that
ships; nothing here is a re-implementation.

The two copies are deliberately duplicated (CWD-run scripts in different
directories, no shared importable module between them), so a drift guard pins
their source text to be byte-identical.
"""
import ast
import os
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
RESOLVER_NAME = "_resolve_tbot_python"

SOURCES = (
    REPO_ROOT / "strategy-research" / "workflow" / "run_phase1_research.py",
    REPO_ROOT / "strategy-research" / "tools" / "retune_regime_detector.py",
)

WINDOWS_REL = Path("..") / "venv" / "Scripts" / "python.exe"
MAC_REL = Path("..") / ".venv" / "bin" / "python"


def _resolver_source(path: Path) -> str:
    """The resolver's own source text, located by name in the shipped file."""
    source = path.read_text(encoding="utf-8")
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name == RESOLVER_NAME:
            segment = ast.get_source_segment(source, node)
            assert segment and segment.startswith(f"def {RESOLVER_NAME}"), (
                f"extracted an empty or wrong segment for {RESOLVER_NAME} in {path} — "
                f"every assertion downstream would be vacuous")
            return segment
    raise AssertionError(
        f"no module-level {RESOLVER_NAME}() in {path}; the four hardcoded "
        f"Windows interpreter paths are unported or the resolver was renamed")


def _load_resolver(path: Path):
    """Compile and execute only the resolver, with no import of its module."""
    namespace = {"Path": Path, "os": os}
    exec(compile(_resolver_source(path), str(path), "exec"), namespace)
    return namespace[RESOLVER_NAME]


def _make_tree(tmp_path: Path, *, windows: bool, mac: bool,
               windows_executable: bool = True) -> Path:
    """Build a fake repo root and return the CWD the scripts are run from."""
    cwd = tmp_path / "strategy-research"
    cwd.mkdir()
    if windows:
        target = tmp_path / "venv" / "Scripts" / "python.exe"
        target.parent.mkdir(parents=True)
        target.write_text("")
        target.chmod(0o755 if windows_executable else 0o644)
    if mac:
        target = tmp_path / ".venv" / "bin" / "python"
        target.parent.mkdir(parents=True)
        target.write_text("")
        target.chmod(0o755)
    return cwd


def _ids(path: Path) -> str:
    return path.name


@pytest.mark.parametrize("source", SOURCES, ids=_ids)
def test_windows_layout_alone_resolves_to_it(source, tmp_path, monkeypatch):
    cwd = _make_tree(tmp_path, windows=True, mac=False)
    monkeypatch.chdir(cwd)

    resolved = Path(_load_resolver(source)()).resolve()

    assert resolved == (tmp_path / "venv" / "Scripts" / "python.exe").resolve()


@pytest.mark.parametrize("source", SOURCES, ids=_ids)
def test_mac_layout_alone_resolves_to_it(source, tmp_path, monkeypatch):
    cwd = _make_tree(tmp_path, windows=False, mac=True)
    monkeypatch.chdir(cwd)

    resolved = Path(_load_resolver(source)()).resolve()

    assert resolved == (tmp_path / ".venv" / "bin" / "python").resolve()


@pytest.mark.parametrize("source", SOURCES, ids=_ids)
def test_windows_wins_when_both_layouts_are_present(source, tmp_path, monkeypatch):
    """Upstream's tree must resolve exactly as it does today.

    The Windows candidate is created executable because that is what upstream's
    checkout looks like from Windows, where `os.access(existing_file, X_OK)` is
    true. This is the test that pins "Jeremy's tree behaves identically".
    """
    cwd = _make_tree(tmp_path, windows=True, mac=True)
    monkeypatch.chdir(cwd)

    resolved = Path(_load_resolver(source)()).resolve()

    assert resolved == (tmp_path / "venv" / "Scripts" / "python.exe").resolve()


@pytest.mark.parametrize("source", SOURCES, ids=_ids)
def test_unrunnable_windows_candidate_does_not_shadow_the_mac_one(
        source, tmp_path, monkeypatch):
    """The committed-Windows-venv case: present, so `.exists()`, but not runnable."""
    cwd = _make_tree(tmp_path, windows=True, mac=True, windows_executable=False)
    monkeypatch.chdir(cwd)

    resolved = Path(_load_resolver(source)()).resolve()

    assert resolved == (tmp_path / ".venv" / "bin" / "python").resolve()


@pytest.mark.parametrize("source", SOURCES, ids=_ids)
def test_no_candidate_raises_naming_both_tried_paths(source, tmp_path, monkeypatch):
    cwd = _make_tree(tmp_path, windows=False, mac=False)
    monkeypatch.chdir(cwd)

    with pytest.raises(RuntimeError) as excinfo:
        _load_resolver(source)()

    message = str(excinfo.value)
    for candidate in (WINDOWS_REL, MAC_REL):
        assert str(candidate) in message, (
            f"the failure must name every path it tried; {candidate} is missing "
            f"from: {message}")


def test_the_two_resolver_copies_have_not_drifted():
    """Duplicated on purpose; a divergence would port one script and not the other."""
    first, second = (_resolver_source(path) for path in SOURCES)

    assert first == second, (
        f"{RESOLVER_NAME}() differs between {SOURCES[0].name} and "
        f"{SOURCES[1].name}; these copies are deliberately identical, so an edit "
        f"to one is an edit owed to the other")
