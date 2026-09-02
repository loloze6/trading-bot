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

_TESTS_DIR = Path(__file__).parent

# The ONE legitimate @pytest.mark.network without a cache guard: the probe just
# below that proves the opt-out MECHANISM works. It asserts the guard was not
# installed and never touches the network, so it needs no cache. Everything else
# that opts out of the socket block runs the real engine and MUST guard its
# caches or it silently live-fetches on a cache-less tree (CUL-221).
_NETWORK_WITHOUT_CACHE_ALLOWED = {
    ("test_cache_network_guard.py", "test_network_marker_opts_out"),
}


def _decorator_source_names(func):
    names = set()
    for dec in func.decorator_list:
        node = dec.func if isinstance(dec, ast.Call) else dec
        names.add(ast.unparse(node))
    return names


def test_no_network_marker_without_cache_guard():
    """Any sr test opting out of the CUL-198 socket block via @pytest.mark.network
    must also carry a @requires_cache guard, else it silently live-fetches (and
    writes caches into local_data) on a tree without the BTCUSDT caches -- the
    CUL-221 defect. The only exception is the opt-out mechanism probe itself."""
    offenders = []
    for path in sorted(_TESTS_DIR.glob("test_*.py")):
        # utf-8-sig: at least one test module in this tree carries a UTF-8 BOM
        # (a Windows artifact); ast.parse chokes on a raw U+FEFF otherwise.
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for func in ast.walk(tree):
            if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            names = _decorator_source_names(func)
            if not any(n.endswith("mark.network") for n in names):
                continue
            if any("requires_cache" in n for n in names):
                continue
            if (path.name, func.name) in _NETWORK_WITHOUT_CACHE_ALLOWED:
                continue
            offenders.append(f"{path.name}::{func.name}")
    assert not offenders, (
        "test(s) opt out of the CUL-198 socket block with @pytest.mark.network "
        "but lack a @requires_cache guard, so they live-fetch on a cache-less "
        "tree (CUL-221): " + ", ".join(offenders)
    )
