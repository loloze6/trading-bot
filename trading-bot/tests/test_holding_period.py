"""core/holding_period.py, case by case (strategy_designer_v2/steps_cards/topics/30_review/opt2_cases.py): each case's
position, bar by bar, as the definition expects it (common/forecast.md 7), through the module and a small driver that
applies the band the way core/trading_bot.py and risk/risk_manager.py do (a trade passes when the signal moved at
least the band since the position was last set, or the sized change reaches it) and the forced flats."""
import math
import pytest
from core.holding_period import HoldingPeriod

BAND = 0.2


def drive(forecasts, N, k=None, forced=(), cap=2.0):
    hp = HoldingPeriod(N, BAND)
    k = k or [1.0] * len(forecasts)
    pos, held_sig, out = 0.0, 0.0, []
    for t, f in enumerate(forecasts):
        nan = not math.isfinite(f)
        target = pos if nan else max(-cap, min(cap, f / 10 * k[t]))
        target = hp.apply("X", f, target, pos)
        if t in forced:
            pos, held_sig = 0.0, 0.0
        else:
            ch = target - pos
            if not nan and ch != 0 and (abs(f / 10 - held_sig) >= BAND - 1e-6 or abs(ch) >= BAND - 1e-6):
                pos, held_sig = target, f / 10
        out.append(round(pos, 3))
    return out


CASES = [
    ("the operator's example", [10, 5, 15, 0, 0, 0], None, 3, (), [1, 1, 1.5, 1, 1, 0]),
    ("short mirror", [-10, -5, -15, 0, 0, 0], None, 3, (), [-1, -1, -1.5, -1, -1, 0]),
    ("a one-moment signal", [0, 12, 0, 0, 0, 0], None, 3, (), [0, 1.2, 1.2, 1.2, 0, 0]),
    ("a fall within the horizon", [10, 10, 6, 6, 6], None, 3, (), [1, 1, 1, 0.6, 0.6]),
    ("volatility alone: no bet", [10] * 6, [1, 1, 1.5, 1, 1, 1], 3, (), [1, 1, 1.5, 1, 1, 1]),
    ("an old short, then +20 while volatility drifts", [-10, 20, 20, 20, 20, 20, 20], [1, 1, .99, .98, .97, .96, .95],
     3, (), [-1, -1, -1, 1.96, 1.96, 1.96, 1.96]),
    ("a side switch: no flat bar", [10, 10, -10, -10, -10, -10], None, 3, (), [1, 1, 1, -1, -1, -1]),
    ("rises below the band are noise", [10, 10.5, 11, 11.5, 0, 0], None, 3, (), [1, 1, 1, 1, 0, 0]),
    ("rises of the band are bets", [10, 12, 14, 0, 0, 0, 0], None, 3, (), [1, 1.2, 1.4, 0.4, 0.2, 0, 0]),
    ("a forced flat is not held", [10] * 5, None, 3, (2,), [1, 1, 0, 1, 1]),
    ("a NaN forecast: no bet, state kept", [10, float("nan"), 0, 0, 0], None, 3, (), [1, 1, 1, 0, 0]),
]


@pytest.mark.parametrize("name,fc,k,N,forced,expected", CASES, ids=[c[0] for c in CASES])
def test_case(name, fc, k, N, forced, expected):
    assert drive(fc, N, k, forced) == pytest.approx(expected, abs=0.011)


def test_symbols_are_independent():
    hp = HoldingPeriod(3, BAND)
    assert hp.apply("A", 10, 1.0, 0.0) == 1.0
    assert hp.apply("B", 0, 0.0, 0.0) == 0.0
    assert hp.apply("A", 0, 0.0, 1.0) == 1.0          # A's bet is held; B's bar did not touch it
