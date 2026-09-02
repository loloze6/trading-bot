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

import socket

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
