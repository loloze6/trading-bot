"""
fix/feed-dependency-safety Step 2: run_protocol.py's --drop-feeds flag /
protocol "drop_feeds" field. Resolution shape mirrors --exchange
(test_run_protocol_exchange_flag.py) with ONE deliberate difference: the
fallback terminates in None ("drop nothing", the pre-existing default), NOT a
forced "binance"-style coalesce -- None IS the correct value here, so a campaign
that names no feed to drop stays byte-identical to today.

run_backtest is monkeypatched to a recording stub -- these tests prove
run_protocol.py's own resolution and threading to BOTH call sites (holdout arm
and walk-forward arm), not the trading-bot engine (that is core/launcher.py's
job, tests/test_feed_dependencies.py).
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402 -- also puts trading-bot/ on sys.path as a side effect


class _RecordingRunBacktest:
    """Stands in for core.launcher.run_backtest: records each call's drop_feeds
    (and symbol) and writes a minimal-but-complete metrics.json into a sandbox
    directory it owns, so main()'s post-run bookkeeping succeeds without touching
    the real repo."""

    def __init__(self, sandbox_dir):
        self.calls = []
        self._sandbox_dir = Path(sandbox_dir)

    def __call__(
        self,
        config_path,
        symbol,
        start,
        end,
        results_root,
        runs_root=None,
        interval_seconds=None,
        warmup_prefetch=False,
        holdout_start=None,
        commission_rate=None,
        trades_log_file=None,
        bar_equity=False,
        exchange=None,
        drop_feeds=None,
    ):
        self.calls.append({"symbol": symbol, "drop_feeds": drop_feeds})
        run_dir = self._sandbox_dir / f"stub_run_{len(self.calls)}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(
            json.dumps(
                {
                    "core": {
                        "trade_count": 1,
                        "net_pnl": 0.0,
                        "sharpe": 0.0,
                        "win_rate": 0.5,
                        "max_drawdown_pct": 0.0,
                        "forecast_return_corr": None,
                    },
                }
            )
        )
        return run_dir


def _write_protocol(tmp_path, **extra):
    protocol = {
        "symbols": ["BTCUSDT"],
        "windows": [{"label": "w1", "test": {"start": "2022-01-01", "end": "2022-01-02"}}],
        "promotion": {
            "median_sharpe_gt": -999,
            "max_abs_drawdown_pct_lt": 999,
            "min_trade_count_gte": 0,
            "kill_median_sharpe_lt": -999999,
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
    """Runs rp.main() end to end (holdout or walk-forward, chosen by holdout=)
    against a synthetic protocol, with run_backtest and _RESULTS_ROOT sandboxed.
    Returns the recording stub's list of {symbol, drop_feeds} calls."""

    def _run(protocol_extra=None, cli_extra=None, holdout=False):
        sandbox = tmp_path / "sandbox_runs"
        stub = _RecordingRunBacktest(sandbox)
        monkeypatch.setattr(rp, "run_backtest", stub)
        monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))

        if holdout:
            protocol_extra = {**(protocol_extra or {}), "holdout": {"start": "2022-02-01", "end": "2022-02-02"}}
        protocol_path = _write_protocol(tmp_path, **(protocol_extra or {}))
        config_path = _write_config(tmp_path)

        argv = ["run_protocol.py", str(config_path), str(protocol_path), "--out-dir", str(tmp_path / "out")]
        if holdout:
            argv += ["--holdout", "--i-understand"]
        argv += cli_extra or []
        monkeypatch.setattr(sys, "argv", argv)
        rp.main()
        return stub.calls

    return _run


# ---------------------------------------------------------------------------
# protocol "drop_feeds" field threads to BOTH call sites
# ---------------------------------------------------------------------------


def test_protocol_drop_feeds_field_threads_to_walk_forward(run_main):
    calls = run_main(protocol_extra={"drop_feeds": ["fear_greed"]})
    assert calls, "run_backtest was never called"
    assert all(c["drop_feeds"] == ["fear_greed"] for c in calls)


def test_protocol_drop_feeds_field_threads_to_holdout(run_main):
    calls = run_main(protocol_extra={"drop_feeds": ["fear_greed"]}, holdout=True)
    assert calls, "run_backtest was never called"
    assert all(c["drop_feeds"] == ["fear_greed"] for c in calls)


# ---------------------------------------------------------------------------
# --drop-feeds CLI flag overrides the protocol field
# ---------------------------------------------------------------------------


def test_cli_drop_feeds_overrides_protocol_field_walk_forward(run_main):
    calls = run_main(protocol_extra={"drop_feeds": ["fear_greed"]}, cli_extra=["--drop-feeds", "funding_rate"])
    assert all(c["drop_feeds"] == ["funding_rate"] for c in calls)


def test_cli_drop_feeds_overrides_protocol_field_holdout(run_main):
    calls = run_main(
        protocol_extra={"drop_feeds": ["fear_greed"]}, cli_extra=["--drop-feeds", "funding_rate"], holdout=True
    )
    assert all(c["drop_feeds"] == ["funding_rate"] for c in calls)


# ---------------------------------------------------------------------------
# both absent -> None ("drop nothing", NOT coalesced) at BOTH call sites.
# This is the deliberate contrast with --exchange (which forces "binance"):
# None IS the correct "no drop" value, so an unspecified campaign is
# byte-identical to before Step 2 existed.
# ---------------------------------------------------------------------------


def test_both_absent_resolves_to_none_walk_forward(run_main):
    calls = run_main()
    assert calls, "run_backtest was never called"
    assert all(c["drop_feeds"] is None for c in calls)


def test_both_absent_resolves_to_none_holdout(run_main):
    calls = run_main(holdout=True)
    assert calls, "run_backtest was never called"
    assert all(c["drop_feeds"] is None for c in calls)


# ---------------------------------------------------------------------------
# --drop-feeds parses a comma-separated list
# ---------------------------------------------------------------------------


def test_cli_drop_feeds_parses_comma_separated_list(run_main):
    calls = run_main(cli_extra=["--drop-feeds", "funding_rate,fear_greed"])
    assert calls, "run_backtest was never called"
    assert all(c["drop_feeds"] == ["funding_rate", "fear_greed"] for c in calls)


# ---------------------------------------------------------------------------
# CLI declaration (mirrors --exchange's own unit test style)
# ---------------------------------------------------------------------------


def test_cli_drop_feeds_defaults_to_none():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--drop-feeds", default=None)
    args = parser.parse_args([])
    assert args.drop_feeds is None


def test_cli_drop_feeds_parses_string():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--drop-feeds", default=None)
    args = parser.parse_args(["--drop-feeds", "funding_rate,fear_greed"])
    assert args.drop_feeds == "funding_rate,fear_greed"
