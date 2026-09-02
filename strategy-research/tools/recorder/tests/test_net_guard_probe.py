"""Probe that the CUL-198 outbound-network block reaches the recorder subtree.

The recorder tests have their own conftest.py, so the main sr suite's block does
not cover them. This proves the recorder conftest wires in the shared guard and
that it bites. It is deliberately NOT PowerShell-dependent, so it runs on macOS
and CI where most recorder tests (the supervisor suite) are skipped.

Mutation: disable install_network_block in the recorder conftest -> this dies.
"""

import socket

import pytest
from _net_guard import NetworkBlockedInTestError

# RFC 5737 TEST-NET-1: guaranteed unroutable.
_UNROUTABLE = ("192.0.2.1", 80)


def test_socket_block_bites_in_recorder_subtree():
    assert getattr(socket.socket.connect, "_is_network_guard", False), (
        "network guard was not installed on an unmarked recorder test"
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.05)
    try:
        with pytest.raises(NetworkBlockedInTestError):
            s.connect(_UNROUTABLE)
    finally:
        s.close()


@pytest.mark.network
def test_network_marker_opts_out_in_recorder_subtree():
    assert not getattr(socket.socket.connect, "_is_network_guard", False)
