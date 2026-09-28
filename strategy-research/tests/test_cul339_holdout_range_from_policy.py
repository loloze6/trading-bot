"""
CUL-339: `run_protocol.py --holdout` takes its range ONLY from
campaign_data_policy.yaml's holdout_range, and the walk-forward training guard
is never looser than it.

THE BUG
-------
Holdout mode read `protocol["holdout"]` -- with `end: null` meaning
`date.today()`. Several committed protocols carry a block starting a year
before the seal with an open end, which would have scored the validation year,
the whole sealed window and post-holdout data in one irreversible look. The
RUNBOOK told the operator to use the policy's range; nothing enforced it.

HOW THESE TESTS STAY SAFE
-------------------------
run_backtest is replaced by a recorder in every test (no engine, no fetch, no
cache read), _RESULTS_ROOT and --out-dir point into tmp_path, and the policy is
a sandboxed file whose dates are computed here at runtime -- far from the real
seal. The one test that reads the REAL policy reads only that YAML (normal
reading per the policy's own rules) and asserts a refusal, so run_backtest is
never reached. No test names a date inside the sealed window.
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402
from protocol_refusal import (  # noqa: E402
    EXIT_NO_DATA_TOUCHED, stderr_declares_no_data_touched,
)

# Sandbox seal: computed, historical, nowhere near the real one.
_SANDBOX_START = date(2021, 3, 1)
_SANDBOX_END = _SANDBOX_START + timedelta(days=45)
S_START, S_END = _SANDBOX_START.isoformat(), _SANDBOX_END.isoformat()


class _RecordingRunBacktest:
    """Records every call; writes the minimal metrics.json main() reads back."""

    def __init__(self, sandbox_dir: Path):
        self.calls: list[dict] = []
        self._dir = sandbox_dir

    def __call__(self, config_path, symbol, start, end, results_root, **kwargs):
        self.calls.append({"symbol": symbol, "start": start, "end": end, **kwargs})
        run_dir = self._dir / f"stub_run_{len(self.calls)}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(json.dumps({"core": {
            "trade_count": 1, "net_pnl": 0.0, "sharpe": 0.0, "win_rate": 0.5,
            "max_drawdown_pct": 0.0, "forecast_return_corr": None}}))
        return run_dir


def _write_policy(tmp_path: Path, holdout_range) -> Path:
    """A sandboxed copy of the real policy with holdout_range replaced (or
    removed when holdout_range is ...)."""
    real = yaml.safe_load((ROOT / "config" / "campaign_data_policy.yaml").read_text(
        encoding="utf-8")) or {}
    if holdout_range is ...:
        real.pop("holdout_range", None)
    else:
        real["holdout_range"] = holdout_range
    p = tmp_path / "campaign_data_policy.yaml"
    p.write_text(yaml.safe_dump(real, sort_keys=False), encoding="utf-8")
    return p


def _day(d: date, delta: int = 0) -> str:
    return (d + timedelta(days=delta)).isoformat()


@pytest.fixture
def run_main(monkeypatch, tmp_path):
    """rp.main() end to end with a sandboxed policy and a recording run_backtest.
    Returns (calls, out_dir, exit_code) -- exit_code None when main() returned."""
    def _run(*, holdout_block=..., windows=None, holdout=True,
             policy_range=(S_START, S_END), use_real_policy=False):
        stub = _RecordingRunBacktest(tmp_path / "sandbox_runs")
        monkeypatch.setattr(rp, "run_backtest", stub)
        monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
        if not use_real_policy:
            monkeypatch.setattr(rp, "_DATA_POLICY_PATH", _write_policy(tmp_path, policy_range))

        protocol = {
            "symbols": ["BTCUSDT"],
            "windows": windows or [{"label": "w1",
                                    "test": {"start": "2019-01-01", "end": "2019-02-01"}}],
            "promotion": {"median_sharpe_gt": -999, "max_abs_drawdown_pct_lt": 999,
                          "min_trade_count_gte": 0, "kill_median_sharpe_lt": -999999},
        }
        if holdout_block is not ...:
            protocol["holdout"] = holdout_block
        protocol_path = tmp_path / "protocol.json"
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"dummy": True}), encoding="utf-8")
        out_dir = tmp_path / "out"

        argv = ["run_protocol.py", str(config_path), str(protocol_path),
                "--out-dir", str(out_dir)]
        if holdout:
            argv += ["--holdout", "--i-understand"]
        monkeypatch.setattr(sys, "argv", argv)
        code = None
        try:
            rp.main()
        except SystemExit as exc:
            code = exc.code
        return stub.calls, out_dir, code
    return _run


def _assert_refused_untouched(calls, out_dir, code, capsys):
    assert code == EXIT_NO_DATA_TOUCHED
    assert stderr_declares_no_data_touched(capsys.readouterr().err)
    assert calls == [], "run_backtest must never be called on a refused run"
    assert not out_dir.exists(), "refusal must precede every side effect, out_dir included"


# ---------------------------------------------------------------------------
# --holdout: range from the policy only
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("block", [
    pytest.param({"start": _day(_SANDBOX_START, -365), "end": None}, id="validation-year-start-open-end"),
    pytest.param({"start": S_START, "end": None}, id="open-end"),
    pytest.param({"start": _day(_SANDBOX_START, -1), "end": S_END}, id="start-earlier"),
    pytest.param({"start": _day(_SANDBOX_START, 1), "end": S_END}, id="start-later"),
    pytest.param({"start": S_START, "end": _day(_SANDBOX_END, 1)}, id="end-later"),
    pytest.param({"start": S_START, "end": _day(_SANDBOX_END, -1)}, id="end-earlier"),
    pytest.param({"start": S_START}, id="end-missing"),
    pytest.param({}, id="empty-block"),
    pytest.param({"start": S_START + "T00:00:00", "end": S_END}, id="timestamp-not-day"),
    pytest.param([S_START, S_END], id="not-a-mapping"),
])
def test_disagreeing_protocol_block_refused_before_any_fetch(run_main, capsys, block):
    calls, out_dir, code = run_main(holdout_block=block)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_real_policy_refuses_the_committed_open_ended_block_shape(run_main, capsys):
    """The exact shape baseline_v1.json & co. carry -- a start one year before
    the REAL seal and `end: null` -- against the REAL policy: refused, and
    run_backtest (the only path to data) is never reached."""
    real_start = yaml.safe_load((ROOT / "config" / "campaign_data_policy.yaml").read_text(
        encoding="utf-8"))["holdout_range"][0]
    y = int(str(real_start)[:4])
    block = {"start": f"{y - 1:04d}-01-01", "end": None}
    calls, out_dir, code = run_main(holdout_block=block, use_real_policy=True)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_no_protocol_block_uses_policy_range(run_main):
    calls, out_dir, code = run_main()
    assert code is None
    assert [(c["start"], c["end"]) for c in calls] == [(S_START, S_END)]
    payload = json.loads((out_dir / "holdout_result.json").read_text(encoding="utf-8"))
    assert payload["holdout_window"] == {"start": S_START, "end": S_END}


def test_null_protocol_block_is_treated_as_absent(run_main):
    calls, _, code = run_main(holdout_block=None)
    assert code is None
    assert [(c["start"], c["end"]) for c in calls] == [(S_START, S_END)]


def test_agreeing_protocol_block_runs_on_policy_range(run_main):
    calls, _, code = run_main(holdout_block={"start": S_START, "end": S_END})
    assert code is None
    assert [(c["start"], c["end"]) for c in calls] == [(S_START, S_END)]


@pytest.mark.parametrize("policy_range", [
    pytest.param([S_START, None], id="null-end"),
    pytest.param([S_START, ""], id="empty-end"),
    pytest.param([S_START], id="one-element"),
    pytest.param([None, S_END], id="null-start"),
    pytest.param([S_END, S_START], id="end-before-start"),
    pytest.param(None, id="null-range"),
    pytest.param(..., id="missing-key"),
])
def test_unusable_policy_range_refused(run_main, capsys, policy_range):
    # no protocol block: the policy is the only source, so it alone decides
    calls, out_dir, code = run_main(policy_range=policy_range)
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_missing_policy_file_refused(run_main, monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(rp, "_DATA_POLICY_PATH", tmp_path / "nope" / "policy.yaml")
    calls, out_dir, code = run_main(use_real_policy=True)  # keep the patched path
    _assert_refused_untouched(calls, out_dir, code, capsys)


# ---------------------------------------------------------------------------
# walk-forward training guard: min(protocol start, policy start)
# ---------------------------------------------------------------------------

def _wf(run_main, **kw):
    return run_main(holdout=False, **kw)


def test_training_guard_uses_policy_start_when_protocol_start_is_later(run_main):
    later = _day(_SANDBOX_START, 30)
    calls, _, code = _wf(run_main, holdout_block={"start": later, "end": None})
    assert code is None and calls
    assert all(c["holdout_start"] == S_START for c in calls)


def test_training_guard_keeps_stricter_protocol_start(run_main):
    earlier = _day(_SANDBOX_START, -30)
    calls, _, code = _wf(run_main, holdout_block={"start": earlier, "end": None})
    assert code is None and calls
    assert all(c["holdout_start"] == earlier for c in calls)


def test_training_guard_uses_policy_start_without_protocol_block(run_main):
    calls, _, code = _wf(run_main)
    assert code is None and calls
    assert all(c["holdout_start"] == S_START for c in calls)


def test_training_window_past_policy_start_refused_even_if_protocol_allows_it(run_main):
    """The block's start is AFTER the policy's, so the old guard (protocol
    start only) let this window through into the sealed range."""
    later = _day(_SANDBOX_START, 30)
    window = {"label": "leaky", "test": {"start": _day(_SANDBOX_START, -10),
                                         "end": _day(_SANDBOX_START, 5)}}
    with pytest.raises(AssertionError, match="holdout_start"):
        _wf(run_main, holdout_block={"start": later, "end": None}, windows=[window])


def test_training_window_ending_on_policy_start_refused(run_main):
    window = {"label": "edge", "test": {"start": _day(_SANDBOX_START, -10), "end": S_START}}
    with pytest.raises(AssertionError, match="holdout_start"):
        _wf(run_main, windows=[window])


def test_training_malformed_protocol_start_refused(run_main, capsys):
    calls, out_dir, code = _wf(run_main, holdout_block={"start": "soon", "end": None})
    _assert_refused_untouched(calls, out_dir, code, capsys)


def test_training_unusable_policy_refused(run_main, capsys):
    calls, out_dir, code = _wf(run_main, policy_range=[S_START, None])
    _assert_refused_untouched(calls, out_dir, code, capsys)


# ---------------------------------------------------------------------------
# source hygiene
# ---------------------------------------------------------------------------

def test_no_code_subscripts_protocol_holdout_or_calls_today():
    """AST, not text: comments may describe the old bug. The only readers of
    the protocol block left are the two resolvers (via .get), and nothing may
    derive a range end from the wall clock."""
    import ast
    tree = ast.parse((TOOLS_PATH / "run_protocol.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant):
            assert node.slice.value != "holdout", f"line {node.lineno}: X['holdout'] subscript"
        if isinstance(node, ast.Attribute) and node.attr == "today":
            assert not (isinstance(node.value, ast.Name) and node.value.id == "date"), (
                f"line {node.lineno}: date.today()")
    readers = [n.lineno for n in ast.walk(tree)
               if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "get" and n.args
               and isinstance(n.args[0], ast.Constant) and n.args[0].value == "holdout"]
    assert len(readers) == 2, f"expected the two resolvers only, got lines {readers}"


@pytest.mark.parametrize("value,expected", [
    ("2020-02-29", "2020-02-29"),
    (date(2020, 2, 29), "2020-02-29"),
    ("2021-02-29", None),
    ("2020-02-29T00:00:00", None),
    (" 2020-02-29", None),
    (None, None),
    ("", None),
    (20200229, None),
])
def test_iso_day(value, expected):
    assert rp._iso_day(value) == expected
