"""Probe tests for the CUL-198 fast-suite cache + network guards (conftest.py).

These prove the guards actually BITE. A guard that never fires verifies
nothing -- and the whole reason CUL-198 exists is that the per-file skipif
convention silently didn't (two same-day CI catches, 2026-09-01).

Mutation coverage (run by the executor lane, must fail when the guard breaks):
  * disable _block_network (drop the two monkeypatch.setattr) ->
    test_socket_block_bites_on_unmarked_test fails (guard not installed).
  * make cache_is_available return a bare Path(path).exists() ->
    test_cache_available_rejects_degenerate fails (an empty file "exists").
"""

import ast
import socket
from pathlib import Path

import pytest
from _cache_guard import cache_is_available, requires_cache
from _net_guard import NetworkBlockedInTestError

# RFC 5737 TEST-NET-1: guaranteed unroutable, so if the block were ever
# disabled this connect fails fast on its own rather than reaching a real host.
_UNROUTABLE = ("192.0.2.1", 80)


def test_socket_block_bites_on_unmarked_test():
    assert getattr(socket.socket.connect, "_is_network_guard", False), (
        "network guard was not installed on an unmarked fast-suite test"
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.05)
    try:
        with pytest.raises(NetworkBlockedInTestError):
            s.connect(_UNROUTABLE)
    finally:
        s.close()


@pytest.mark.network
def test_network_marker_opts_out():
    # No real connect is attempted: asserting the guard was NOT installed proves
    # the opt-out path works without touching the network.
    assert not getattr(socket.socket.connect, "_is_network_guard", False)


def test_loopback_connect_is_allowed():
    # Loopback must stay reachable so the block never breaks legitimate
    # in-process use (a local server, multiprocessing).
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cli.connect(("127.0.0.1", port))  # must NOT raise
    finally:
        cli.close()
        srv.close()


def test_cache_available_missing(tmp_path):
    assert cache_is_available(tmp_path / "nope.csv") is False


def test_cache_available_rejects_degenerate(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_bytes(b"")
    assert cache_is_available(empty) is False

    header_only = tmp_path / "header.csv"
    header_only.write_text("timestamp,open,high,low,close,volume\n")
    assert cache_is_available(header_only) is False  # below the byte floor

    real = tmp_path / "real.csv"
    real.write_bytes(b"x" * 4096)
    assert cache_is_available(real) is True


def test_cache_available_min_rows(tmp_path):
    thin = tmp_path / "thin.csv"
    thin.write_bytes(b"x" * 4096)  # passes the byte floor
    thin.write_text("h\n" + "r\n")  # but only 2 lines
    assert cache_is_available(thin, min_bytes=0, min_rows=100) is False
    assert cache_is_available(thin, min_bytes=0, min_rows=2) is True


def test_requires_cache_marks_skip_for_degenerate(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_bytes(b"")
    mark = requires_cache(empty)
    assert mark.name == "skipif"
    # skipif's condition is the first positional arg; truthy -> the test skips.
    assert bool(mark.args[0]) is True

    real = tmp_path / "real.csv"
    real.write_bytes(b"x" * 4096)
    assert bool(requires_cache(real).args[0]) is False


# ---------------------------------------------------------------------------
# Structural guard: a @pytest.mark.network opt-out must pair with @requires_cache
# ---------------------------------------------------------------------------

_SR_ROOT = Path(__file__).resolve().parents[1]  # strategy-research/
# Both sr test subtrees wire the CUL-198 socket block via their own conftest, so
# both must be scanned -- the recorder tree carries its own @network probe.
_SCAN_DIRS = (_SR_ROOT / "tests", _SR_ROOT / "tools" / "recorder" / "tests")

# The ONLY legitimate @pytest.mark.network without a cache guard: the probes that
# prove the opt-out MECHANISM works. Each asserts the guard was NOT installed and
# never touches the network, so it needs no cache. Everything else that opts out
# of the socket block runs the real engine and MUST guard its caches or it
# silently live-fetches on a cache-less tree (CUL-221). Keyed by path relative to
# the sr root so the two same-family probes stay explicit and unambiguous.
_NETWORK_WITHOUT_CACHE_ALLOWED = {
    ("tests/test_cache_network_guard.py", "test_network_marker_opts_out"),
    ("tools/recorder/tests/test_net_guard_probe.py", "test_network_marker_opts_out_in_recorder_subtree"),
}


def _pytest_aliases(tree):
    """Names bound to the ``pytest`` module and to ``pytest.mark`` in a module,
    so aliased opt-outs (``import pytest as pt`` / ``from pytest import mark as m``)
    are resolved, not just the literal ``pytest.mark.network``."""
    pytest_names, mark_names = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name == "pytest":
                    pytest_names.add(a.asname or "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for a in node.names:
                if a.name == "mark":
                    mark_names.add(a.asname or "mark")
    return pytest_names, mark_names


def _is_network_marker(node, pytest_names, mark_names):
    """True if ``node`` is a ``network`` marker expression: ``<pytest>.mark.network``
    or ``<mark_alias>.network`` (a bare call form ``...network()`` unwraps first)."""
    node = node.func if isinstance(node, ast.Call) else node
    if not (isinstance(node, ast.Attribute) and node.attr == "network"):
        return False
    val = node.value
    if isinstance(val, ast.Name) and val.id in mark_names:
        return True  # <mark_alias>.network
    # <pytest_alias>.mark.network
    return (
        isinstance(val, ast.Attribute)
        and val.attr == "mark"
        and isinstance(val.value, ast.Name)
        and val.value.id in pytest_names
    )


def _has_requires_cache(decorators):
    for dec in decorators:
        node = dec.func if isinstance(dec, ast.Call) else dec
        name = node.id if isinstance(node, ast.Name) else (node.attr if isinstance(node, ast.Attribute) else "")
        if name == "requires_cache":
            return True
    return False


def _module_pytestmark_markers(tree):
    """Marker expressions assigned to a module-level ``pytestmark`` -- both the
    single-marker (``pytestmark = m``) and list/tuple (``pytestmark = [m, ...]``)
    forms, which opt EVERY test in the module out of the block."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets):
            continue
        val = node.value
        if isinstance(val, (ast.List, ast.Tuple)):
            yield from val.elts
        else:
            yield val


def test_no_network_marker_without_cache_guard():
    """Any sr test opting out of the CUL-198 socket block via the ``network``
    marker must also carry a ``@requires_cache`` guard, else it silently live-
    fetches (and writes caches into local_data) on a cache-less tree -- the
    CUL-221 defect. Catches function decorators, module-level ``pytestmark``
    (single and list), and aliased ``pytest.mark`` forms, across BOTH sr test
    subtrees. The only exceptions are the opt-out mechanism probes themselves."""
    offenders = []
    for scan_dir in _SCAN_DIRS:
        for path in sorted(scan_dir.glob("test_*.py")):
            rel = path.relative_to(_SR_ROOT).as_posix()
            # utf-8-sig: at least one module in this tree carries a UTF-8 BOM
            # (a Windows artifact); ast.parse chokes on a raw U+FEFF otherwise.
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            pytest_names, mark_names = _pytest_aliases(tree)
            # A module-level network pytestmark opts out every test in the file;
            # there is no legitimate one, so any is an offender.
            for m in _module_pytestmark_markers(tree):
                if _is_network_marker(m, pytest_names, mark_names):
                    offenders.append(f"{rel}::<module pytestmark>")
            for func in ast.walk(tree):
                if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                decs = func.decorator_list
                if not any(_is_network_marker(d, pytest_names, mark_names) for d in decs):
                    continue
                if _has_requires_cache(decs):
                    continue
                if (rel, func.name) in _NETWORK_WITHOUT_CACHE_ALLOWED:
                    continue
                offenders.append(f"{rel}::{func.name}")
    assert not offenders, (
        "test(s) opt out of the CUL-198 socket block with the network marker "
        "but lack a @requires_cache guard, so they live-fetch on a cache-less "
        "tree (CUL-221): " + ", ".join(offenders)
    )
