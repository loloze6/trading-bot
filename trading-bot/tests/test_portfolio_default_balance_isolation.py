"""
#48 F2: MockPortfolioInfo / PortfolioInfo must not share a default balance dict.

`initial_balance={'USDT': {...}}` as a parameter default is evaluated ONCE at
function-definition time, and `update_local_balance` mutates `local_balance` in
place, so every bare-constructed instance shared one dict: trade on the first
and the second starts at the mutated figure.

Inert on master only because all five construction sites pass an explicit
balance. Campaigns build this object repeatedly per process
(run_protocol.main -> run_backtest -> _build_mock_stack), so correctness rested
entirely on that chokepoint passing a fresh literal -- one bare
MockPortfolioInfo() anywhere would have silently shared balances across
backtest runs with nothing to detect it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from execution.portfolio_info import MockPortfolioInfo  # noqa: E402


def test_two_default_instances_do_not_share_the_balance_object():
    a = MockPortfolioInfo()
    b = MockPortfolioInfo()
    assert a.local_balance is not b.local_balance
    assert a.local_balance['USDT'] is not b.local_balance['USDT'], (
        "the nested per-asset dict must be fresh too -- a shallow copy would "
        "still share it, and that is the dict update_local_balance mutates"
    )


def test_mutating_one_instance_does_not_move_the_next_ones_opening_balance():
    """The behavioural form. This is what actually went wrong: it is not about
    identity, it is about instance B opening at 500 instead of 1000."""
    a = MockPortfolioInfo()
    opening = a.local_balance['USDT']['free']
    a.local_balance['USDT']['free'] -= 500

    b = MockPortfolioInfo()
    assert b.local_balance['USDT']['free'] == opening, (
        f"a fresh instance opened at {b.local_balance['USDT']['free']} after "
        f"another instance traded; expected {opening}"
    )


def test_explicit_balance_is_still_honoured_by_reference():
    """No behaviour change for the five existing callers, which all pass an
    explicit balance and may rely on observing their own dict."""
    mine = {'USDT': {'free': 4242, 'locked': 0}}
    p = MockPortfolioInfo(initial_balance=mine)
    assert p.local_balance is mine
    assert p.local_balance['USDT']['free'] == 4242
