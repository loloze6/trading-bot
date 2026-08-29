"""
Ticket 13 campaign path (fix/exchange-plumbing-campaign-aux, commit C3):
run_protocol.py's --exchange flag / protocol "exchange" field, Option Y
(locked 2026-08-09): a campaign resolves `--exchange` -> protocol field ->
explicit "binance", and NEVER passes None to run_backtest -- ambient
config.json cannot leak into a campaign's venue (plan §3.3).

run_backtest is monkeypatched to a recording stub -- these tests prove
run_protocol.py's own resolution and threading, not the trading-bot engine
(that is core/launcher.py's tests/test_exchange_selection.py's job). The stub
writes its output under a tmp_path sandbox it controls directly, never under
the real strategy-research/results/ tree, regardless of what results_root/
runs_root main() happens to pass it.
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
    """Stands in for core.launcher.run_backtest: records every call's kwargs
    and writes a minimal-but-complete metrics.json into a sandbox directory
    it owns, so main()'s post-run bookkeeping (holdout: read metrics.json,
    append holdout_log.jsonl; walk-forward: promotion + trade diagnostics)
    succeeds without touching the real repo."""

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
        self.calls.append({"symbol": symbol, "start": start, "exchange": exchange})
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
        "windows": [
            {"label": "w1", "test": {"start": "2022-01-01", "end": "2022-01-02"}}
        ],
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
    """Runs rp.main() end to end (holdout or walk-forward, chosen by cli_extra)
    against a synthetic protocol, with run_backtest and _RESULTS_ROOT sandboxed.
    Returns the recording stub's list of {symbol, start, exchange} calls."""

    def _run(protocol_extra=None, cli_extra=None, holdout=False):
        sandbox = tmp_path / "sandbox_runs"
        stub = _RecordingRunBacktest(sandbox)
        monkeypatch.setattr(rp, "run_backtest", stub)
        monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))

        if holdout:
            protocol_extra = {
                **(protocol_extra or {}),
                "holdout": {"start": "2022-02-01", "end": "2022-02-02"},
            }
        protocol_path = _write_protocol(tmp_path, **(protocol_extra or {}))
        config_path = _write_config(tmp_path)

        argv = [
            "run_protocol.py",
            str(config_path),
            str(protocol_path),
            "--out-dir",
            str(tmp_path / "out"),
        ]
        if holdout:
            argv += ["--holdout", "--i-understand"]
        argv += cli_extra or []
        monkeypatch.setattr(sys, "argv", argv)
        rp.main()
        return stub.calls

    return _run


# ---------------------------------------------------------------------------
# T-17: protocol-file "exchange" field threads to both call sites
# ---------------------------------------------------------------------------


def test_protocol_exchange_field_threads_to_walk_forward_run_backtest(run_main):
    calls = run_main(protocol_extra={"exchange": "kraken"})
    assert calls, "run_backtest was never called"
    assert all(c["exchange"] == "kraken" for c in calls)


def test_protocol_exchange_field_threads_to_holdout_run_backtest(run_main):
    calls = run_main(protocol_extra={"exchange": "kraken"}, holdout=True)
    assert calls, "run_backtest was never called"
    assert all(c["exchange"] == "kraken" for c in calls)


# ---------------------------------------------------------------------------
# T-18: --exchange CLI flag overrides the protocol field
# ---------------------------------------------------------------------------


def test_cli_exchange_flag_overrides_protocol_field_walk_forward(run_main):
    calls = run_main(
        protocol_extra={"exchange": "kraken"}, cli_extra=["--exchange", "binance"]
    )
    assert all(c["exchange"] == "binance" for c in calls)


def test_cli_exchange_flag_overrides_protocol_field_holdout(run_main):
    calls = run_main(
        protocol_extra={"exchange": "kraken"},
        cli_extra=["--exchange", "binance"],
        holdout=True,
    )
    assert all(c["exchange"] == "binance" for c in calls)


# ---------------------------------------------------------------------------
# T-19 [critic-1]: both absent -> explicit "binance" at BOTH call sites
# ---------------------------------------------------------------------------


def test_both_absent_resolves_to_explicit_binance_walk_forward(run_main):
    """No protocol field, no --exchange flag: the campaign must still pass an
    EXPLICIT 'binance' to run_backtest -- never None, which would let the
    ambient config.json's trading.exchange leak into the campaign (Option Y,
    the whole point of C3)."""
    calls = run_main()
    assert calls, "run_backtest was never called"
    assert all(c["exchange"] == "binance" for c in calls)


def test_both_absent_resolves_to_explicit_binance_holdout(run_main):
    calls = run_main(holdout=True)
    assert calls, "run_backtest was never called"
    assert all(c["exchange"] == "binance" for c in calls)


# ---------------------------------------------------------------------------
# CLI declaration (mirrors --commission-bps's own unit test style)
# ---------------------------------------------------------------------------


def test_cli_exchange_defaults_to_none():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--exchange", default=None)
    args = parser.parse_args([])
    assert args.exchange is None


def test_cli_exchange_parses_string():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--exchange", default=None)
    args = parser.parse_args(["--exchange", "kraken"])
    assert args.exchange == "kraken"


# ---------------------------------------------------------------------------
# reviewer-48 §2: explicit-empty fails loud (preserved); absent coalesces
# ---------------------------------------------------------------------------


def test_explicit_empty_exchange_is_preserved_not_swallowed_to_binance(run_main):
    """An EXPLICIT empty venue ("exchange": "") must reach run_backtest as ""
    so _validated_exchange rejects it (sys.exit 1) -- not be silently coerced
    to "binance". The pre-fix `or`-chain swallowed the empty string; Option Y
    now resolves with `is not None` (reviewer-48 §2)."""
    calls = run_main(protocol_extra={"exchange": ""})
    assert calls, "run_backtest was never called"
    assert all(c["exchange"] == "" for c in calls)


def test_null_exchange_field_still_coalesces_to_binance_no_config_leak(run_main):
    """A JSON null venue ("exchange": null -> None) is a genuine ABSENCE and
    must coalesce to explicit "binance" -- never pass None through to
    run_backtest's config.json-read arm. The `is not None` refactor must not
    reopen the ambient-config leak Option Y closes (this passes on both the
    pre- and post-fix forms; it pins the no-leak property against a future
    "simplification" to a single leaky ternary)."""
    calls = run_main(protocol_extra={"exchange": None})
    assert calls, "run_backtest was never called"
    assert all(c["exchange"] == "binance" for c in calls)
