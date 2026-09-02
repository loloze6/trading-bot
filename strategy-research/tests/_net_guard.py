"""Shared outbound-network block for the sr fast suites (CUL-198).

The fast suite must be hermetic on every machine, not just on the cache-less,
geo-blocked CI runners -- two same-day CI catches (2026-09-01) were network/
cache-dependent tests that passed locally by accident. This module holds the
socket-block machinery so it is IDENTICAL in both sr test subtrees:

  * strategy-research/tests/conftest.py
  * strategy-research/tools/recorder/tests/conftest.py

Each conftest wires it into its own autouse fixture + marker registration. It
lives in a uniquely-named module (not the conftests themselves) because a
conftest cannot be imported by name -- so this is the clean alternative to
copy-pasting ~40 lines into the second subtree.
"""

import socket as _socket


class NetworkBlockedInTestError(RuntimeError):
    """Raised when a fast-suite test attempts an outbound network connect.

    Opt a test out with ``@pytest.mark.network`` (there should be zero such
    tests in the fast suite today).
    """


# Loopback / AF_UNIX stay reachable so the block never breaks legitimate
# in-process use (a local server, multiprocessing). Only genuine outbound
# connects are blocked.
_ALLOWED_CONNECT_HOSTS = frozenset({"127.0.0.1", "::1", "localhost", "0.0.0.0"})


def _connect_is_blocked(address):
    if isinstance(address, (str, bytes)):
        return False  # AF_UNIX path -- local, never blocked
    try:
        host = address[0]
    except (TypeError, IndexError):
        return False
    return host not in _ALLOWED_CONNECT_HOSTS


def _make_connect_guard(real_method, method_name):
    def _guard(self, address, *args, **kwargs):
        if _connect_is_blocked(address):
            raise NetworkBlockedInTestError(
                f"socket.{method_name}({address!r}) blocked in the fast suite. "
                "A test must not touch the network; if this call is genuinely "
                "needed, mark the test @pytest.mark.network."
            )
        return real_method(self, address, *args, **kwargs)

    _guard._is_network_guard = True  # identity tag the probe/opt-out tests assert on
    return _guard


_NETWORK_MARKER = (
    "network: opt OUT of the fast-suite outbound-network block. Only for a test "
    "that legitimately reaches a real host; there should be zero such tests in "
    "the fast suite today. A marked test loses the loud-failure guard, so it "
    "must handle its own network errors and CI absence."
)


def register_network_marker(config):
    """Register the ``network`` opt-out marker (call from pytest_configure)."""
    config.addinivalue_line("markers", _NETWORK_MARKER)


def install_network_block(request, monkeypatch):
    """Patch socket connect/connect_ex to fail loud, unless @pytest.mark.network.

    Call from an autouse fixture; monkeypatch restores the originals on
    teardown. Loopback and AF_UNIX stay reachable.
    """
    if request.node.get_closest_marker("network"):
        return
    monkeypatch.setattr(
        _socket.socket,
        "connect",
        _make_connect_guard(_socket.socket.connect, "connect"),
    )
    monkeypatch.setattr(
        _socket.socket,
        "connect_ex",
        _make_connect_guard(_socket.socket.connect_ex, "connect_ex"),
    )
