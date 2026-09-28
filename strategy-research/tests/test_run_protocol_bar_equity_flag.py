"""
E-041 S3: run_protocol.py's two run_backtest() call sites (holdout and
walk-forward) must pass bar_equity=True.

WHY THIS EXISTS
---------------
run_protocol.py was the "only caller that matters" (E-041/EPIC.md) that never
requested the bar-level equity block -- so bar_equity defaulted off in every
real campaign run despite being built, tested and bit-identity-proven since
2026-07-31 (tests/test_bar_equity_bit_identical.py, trading-bot/). Every
research verdict to date was decided on trade-exit Sharpe/maxDD instead of the
bar-level numbers that block exists specifically to provide (reference figures,
same run: bar-level Sharpe -5.12 vs trade-exit -5.65; bar-level maxDD -24.77%
vs trade-exit -24.59%).

E-041's decision (Jérémy, 2026-09-01): a finished, tested feature defaults ON;
staying off needs a stated reason. bar_equity has none, so it is switched on
here -- the first of the epic's flags, agreed with Dorian as the pilot because
its bit-identity proof already existed on both sides.

This test is the regression guard: it does not re-prove bar_equity is
additive/correct (trading-bot/tests/test_bar_equity_bit_identical.py already
does, and is untouched by this change -- the ENGINE's default stays False, only
this campaign-level call site changed). It proves the call site cannot silently
drift back to the old default.

Reuses the recording-stub pattern from test_run_protocol_exchange_flag.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402


class _RecordingRunBacktest:
    """Records every run_backtest() call's kwargs; writes a minimal-but-complete
    metrics.json so main()'s post-run bookkeeping succeeds without touching the
    real repo. See test_run_protocol_exchange_flag.py for the original."""

    def __init__(self, sandbox_dir):
        self.calls = []
        self._sandbox_dir = Path(sandbox_dir)

    def __call__(self, config_path, symbol, start, end, results_root,
                 runs_root=None, interval_seconds=None, warmup_prefetch=False,
                 holdout_start=None, commission_rate=None, trades_log_file=None,
                 bar_equity=False, exchange=None, drop_feeds=None):
        self.calls.append({"symbol": symbol, "bar_equity": bar_equity})
        run_dir = self._sandbox_dir / f"stub_run_{len(self.calls)}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(json.dumps({
            "core": {
                "trade_count": 1, "net_pnl": 0.0, "sharpe": 0.0,
                "win_rate": 0.5, "max_drawdown_pct": 0.0,
                "forecast_return_corr": None,
            },
        }))
        return run_dir


def _write_protocol(tmp_path, **extra):
    protocol = {
        "symbols": ["BTCUSDT"],
        "windows": [{"label": "w1", "test": {"start": "2022-01-01", "end": "2022-01-02"}}],
        "promotion": {
            "median_sharpe_gt": -999, "max_abs_drawdown_pct_lt": 999,
            "min_trade_count_gte": 0, "kill_median_sharpe_lt": -999999,
        },
        **extra,
    }
    p = tmp_path / "protocol.json"
    p.write_text(json.dumps(protocol))
    return p


def _write_config(tmp_path):
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"dummy": True}))
    return p


@pytest.fixture
def run_main(monkeypatch, tmp_path):
    def _run(holdout=False):
        sandbox = tmp_path / "sandbox_runs"
        stub = _RecordingRunBacktest(sandbox)
        monkeypatch.setattr(rp, "run_backtest", stub)
        monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
        # CUL-339: --holdout takes its range ONLY from the policy's holdout_range and
        # refuses a disagreeing protocol block, so sandbox a policy that agrees with
        # this test's synthetic block (also the walk-forward guard's upper bound).
        _policy = tmp_path / "campaign_data_policy.yaml"
        _policy.write_text('holdout_range: ["2022-02-01", "2022-02-02"]\n'
                           'holdout_consumed_by: []\n', encoding="utf-8")
        monkeypatch.setattr(rp, "_DATA_POLICY_PATH", _policy)

        protocol_extra = {}
        if holdout:
            protocol_extra["holdout"] = {"start": "2022-02-01", "end": "2022-02-02"}
        protocol_path = _write_protocol(tmp_path, **protocol_extra)
        config_path = _write_config(tmp_path)

        argv = ["run_protocol.py", str(config_path), str(protocol_path),
                "--out-dir", str(tmp_path / "out")]
        if holdout:
            argv += ["--holdout", "--i-understand", "--hypothesis-id", "H-FLAG-TEST"]
        monkeypatch.setattr(sys, "argv", argv)
        rp.main()
        return stub.calls
    return _run


def test_bar_equity_true_at_walk_forward_call_site(run_main):
    calls = run_main(holdout=False)
    assert calls, "run_backtest was never called"
    assert all(c["bar_equity"] is True for c in calls), (
        "run_protocol.py's walk-forward call site must pass bar_equity=True "
        "(E-041) -- got False, the pre-2026-09-02 default that left every "
        "campaign run without the bar-level equity block."
    )


def test_bar_equity_true_at_holdout_call_site(run_main):
    calls = run_main(holdout=True)
    assert calls, "run_backtest was never called"
    assert all(c["bar_equity"] is True for c in calls), (
        "run_protocol.py's holdout call site must pass bar_equity=True (E-041)."
    )
