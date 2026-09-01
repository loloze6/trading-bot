"""
CUL-165 / upstream GH#79 (Sites 1-2): the research-side `_config_sha` stamp must
certify the EXACT config bytes the run actually parsed, not a separate disk read
that a mid-run rewrite can desync. Same defect class as the engine-side CUL-27
(`core/backtester.py::_source_provenance_config`); these are the two research-tool
siblings. Site 3 (`run_phase1_research.py::_compute_forecast_hash`) is out of
scope here (rides with E-025).

The fix snapshots the config bytes once at tool start, hashes those bytes, writes
them verbatim to `<out_dir>/config.snapshot.json`, and points every downstream
run at the snapshot. Hash and run then derive from the same frozen bytes.

Three tests:
  - S1 drift: run_protocol.main() -- a run_backtest that rewrites the original
    config mid-run must not change what protocol_summary.json's config_sha256
    certifies.
  - S2 drift: prescreen_signal.run_prescreen() -- same, via _extract_forecasts.
  - canonicalization pin (delta-3): `_config_sha(bytes)` must json.loads+
    canonicalize identically to the path overload AND to the engine manifest
    formula, on a NON-canonical (pretty, unsorted) fixture. Bites a raw-bytes
    regression that the two self-consistent drift tests would miss.
"""
import json
import sys
from hashlib import sha256
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
TBOT_PATH = ROOT.parent / "trading-bot"
for _p in (TOOLS_PATH, TBOT_PATH):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import run_protocol as rp  # noqa: E402
import prescreen_signal as ps  # noqa: E402

_OHLCV = TBOT_PATH / "local_data" / "BTCUSDT_1h.csv"
_FUNDING = TBOT_PATH / "local_data" / "BTCUSDT_funding_8h.csv"


def _canonical_sha256(path) -> str:
    """The one canonicalization formula shared by the engine manifest
    (reporting/run_artifact.py) and both research _config_sha helpers:
    json.load -> json.dumps(sort_keys, compact) -> sha256 hexdigest."""
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    return _canonical_sha256_of_obj(cfg)


def _canonical_sha256_of_obj(obj) -> str:
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()


# ---------------------------------------------------------------------------
# S1 -- run_protocol.py: whole-protocol-run drift window
# ---------------------------------------------------------------------------

def test_s1_run_protocol_stamp_certifies_what_ran(monkeypatch, tmp_path):
    """A run_backtest that rewrites the ORIGINAL config file the moment it is
    invoked must not desync protocol_summary.json's config_sha256 from the
    config the run actually parsed. The fix passes an immutable snapshot path,
    so the recorded 'what ran' hash equals the stamp; the pre-fix code passes
    the original path and the stub reads the rewritten bytes -> mismatch."""
    config_a = {"dummy": True, "z": 1, "a": {"b": 2}}
    config_b = {"dummy": False, "z": 99, "a": {"b": 7}}
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_a), encoding="utf-8")
    sha_a = _canonical_sha256(config_path)

    protocol = {
        "symbols": ["BTCUSDT"],
        "windows": [{"label": "w1", "test": {"start": "2022-01-01", "end": "2022-01-02"}}],
        "promotion": {
            "median_sharpe_gt": -999, "max_abs_drawdown_pct_lt": 999,
            "min_trade_count_gte": 0, "kill_median_sharpe_lt": -999999,
        },
    }
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")

    recorded = {}
    sandbox = tmp_path / "sandbox_runs"
    sandbox.mkdir(parents=True, exist_ok=True)

    def _stub_run_backtest(cfg_path, symbol, start, end, results_root, **kwargs):
        # Rewrite the ORIGINAL config the instant the run starts: the mid-run
        # rewrite a separate stamp-read cannot see.
        config_path.write_text(json.dumps(config_b), encoding="utf-8")
        # Record the canonical hash of whatever path we were actually handed --
        # the snapshot (fix) or the now-rewritten original (pre-fix).
        recorded["ran_sha"] = _canonical_sha256(cfg_path)
        run_dir = sandbox / f"stub_run_{len(list(sandbox.glob('stub_run_*'))) + 1}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(json.dumps({
            "core": {
                "trade_count": 1, "net_pnl": 0.0, "sharpe": 0.0,
                "win_rate": 0.5, "max_drawdown_pct": 0.0,
                "forecast_return_corr": None,
            },
        }))
        return run_dir

    monkeypatch.setattr(rp, "run_backtest", _stub_run_backtest)
    monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
    out_dir = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", [
        "run_protocol.py", str(config_path), str(protocol_path), "--out-dir", str(out_dir),
    ])
    rp.main()

    summary = json.loads((out_dir / "protocol_summary.json").read_text(encoding="utf-8"))
    assert recorded["ran_sha"] == sha_a, (
        "run_backtest parsed a different config than the stamp certifies -- "
        "config-hash drift (the stamp was read separately from what ran)."
    )
    assert summary["config_sha256"] == sha_a
    snapshot = out_dir / "config.snapshot.json"
    assert snapshot.exists()
    assert json.loads(snapshot.read_text(encoding="utf-8")) == config_a


# ---------------------------------------------------------------------------
# S2 -- prescreen_signal.py: full-prescreen-sweep drift window
# ---------------------------------------------------------------------------

_S2_CONFIG_A = {
    "aux_feeds": ["funding_rate"],
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": 3, "regimes": {
        "unknown": {"components": [{
            "id": "funding_mr",
            "class": "strategies.strategy_components.FundingRateMeanReversionComponent",
            "weight": 1.0, "transforms": [], "params": {"threshold": 0.0002, "scaling_factor": 10.0},
        }]},
        "trending": None, "mean_reversion": None, "chop": None,
    }},
}


@pytest.mark.skipif(not _OHLCV.exists() or not _FUNDING.exists(), reason="local_data fixtures not present")
def test_s2_prescreen_stamp_certifies_what_ran(monkeypatch, tmp_path):
    """_extract_forecasts rewrites the original config the moment it is invoked;
    prescreen_result.yaml's config_sha8 must still certify the config the signal
    extraction actually parsed. Delegates to the real _extract_forecasts so the
    full IC pipeline runs on real data."""
    config_a = json.loads(json.dumps(_S2_CONFIG_A))
    config_b = json.loads(json.dumps(_S2_CONFIG_A))
    config_b["strategies"]["regimes"]["unknown"]["components"][0]["params"] = {
        "threshold": 0.0009, "scaling_factor": 4.0,
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_a), encoding="utf-8")
    sha_a = _canonical_sha256(config_path)
    assert _canonical_sha256_of_obj(config_b) != sha_a  # B genuinely differs

    protocol = {
        "symbols": ["BTCUSDT"],
        "timeframe": "1h",
        "windows": [{"label": "test", "test": {"start": "2019-09-10", "end": "2020-01-01"}}],
    }
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")

    recorded = {}
    _orig_extract = ps._extract_forecasts

    def _stub_extract(cfg_path, bars_df, expected_step=None):
        config_path.write_text(json.dumps(config_b), encoding="utf-8")
        recorded["ran_sha"] = _canonical_sha256(cfg_path)
        return _orig_extract(cfg_path, bars_df, expected_step=expected_step)

    monkeypatch.setattr(ps, "_extract_forecasts", _stub_extract)
    result = ps.run_prescreen(str(config_path), str(protocol_path),
                              run_id="cul165_s2", out_dir=tmp_path)

    assert recorded["ran_sha"] == sha_a, (
        "_extract_forecasts parsed a different config than config_sha8 certifies "
        "-- config-hash drift."
    )
    assert result["config_sha8"] == sha_a[:8]
    snapshot = tmp_path / "config.snapshot.json"
    assert snapshot.exists()
    assert json.loads(snapshot.read_text(encoding="utf-8")) == config_a


# ---------------------------------------------------------------------------
# delta-3 -- canonicalization pin (the test that bites a raw-bytes regression)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mod", [rp, ps], ids=["run_protocol", "prescreen_signal"])
def test_config_sha_bytes_overload_canonicalizes_like_path_and_engine(mod, tmp_path):
    """`_config_sha(bytes)` must json.loads then canonicalize (sort_keys, compact)
    -- the SAME value as the path overload and the engine manifest formula
    (reporting/run_artifact.py). Fixture is deliberately NON-canonical (pretty-
    printed, unsorted keys) so a `sha256(raw_bytes)` implementation of the bytes
    branch diverges from the path branch and this test fails."""
    non_canonical = '{\n  "z": 1,\n  "a": {\n    "b": 2,\n    "aa": 3\n  }\n}\n'
    config_path = tmp_path / "noncanon.json"
    config_path.write_text(non_canonical, encoding="utf-8")
    raw = config_path.read_bytes()
    assert raw != json.dumps(json.loads(raw), sort_keys=True,
                             separators=(",", ":")).encode()  # fixture really is non-canonical

    from_path = mod._config_sha(str(config_path))
    from_bytes = mod._config_sha(raw)
    engine_sha = _canonical_sha256(config_path)

    assert from_bytes == from_path
    assert from_bytes[0] == engine_sha
    assert from_bytes[1] == engine_sha[:8]
