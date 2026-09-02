import sys
from pathlib import Path

# strategy-research/ on the path so `recorder.*` imports resolve without an
# installed package. The recorder is standalone: nothing here touches
# trading-bot/, and no test reads any recorded, archived or holdout data.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# CUL-198: this subtree has its own conftest, so the fast-suite outbound-network
# block from strategy-research/tests/conftest.py does NOT reach it. Wire in the
# same shared block (tests/_net_guard.py) so a recorder test that touches the
# network fails loud on every machine, not just on the CI runners.
_SR_TESTS = Path(__file__).resolve().parents[3] / "tests"
if str(_SR_TESTS) not in sys.path:
    sys.path.insert(0, str(_SR_TESTS))

import pytest  # noqa: E402
from _net_guard import install_network_block, register_network_marker  # noqa: E402


def pytest_configure(config):
    register_network_marker(config)


@pytest.fixture(autouse=True)
def _block_network(request, monkeypatch):
    """Fail loud on any outbound network connect from a recorder fast-suite test.

    Same guard as the main sr suite (tests/_net_guard.py); loopback and AF_UNIX
    stay reachable. Opt out with @pytest.mark.network.
    """
    install_network_block(request, monkeypatch)
