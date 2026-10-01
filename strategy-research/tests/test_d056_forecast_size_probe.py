"""
D-056 / O-10: the forecast-size probe (tools/forecast_size_probe.py) and its
wiring (orchestrator.forecast_size_probe.enabled, off by default).

C4 run_061: `vol_adjusted` on a percent-unit component shrank the forecast to
~1e-5, so the variant made 0 trades in 95 windows and nothing flagged it. The
probe refuses a config whose forecast can almost never reach the rebalance
floor, right after 1b and in step 5a.

Covers: the pure size verdict; the sample never reaching 2024; the threshold
read from trading-bot/config.json (fail loud when missing); the flag (off =
nothing run); the subprocess helper (refusal message, record, crash raises);
the post-1b route (refusal -> back to 1b) and step 5a (refused variant ->
not_tested with the D-051/D-053 reason, so the existing retry applies).
No backtest here: the real-engine check is the manual smoke recorded in the PR.
tests/conftest.py sandboxes rpr.ROOT.
"""
import json
import math
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import forecast_size_probe as fsp  # noqa: E402

from test_d051_d053_forecast_rules import (  # noqa: E402
    CONFIG, COMP0, _authored_1b, _design, _refusals, _run_5a)
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402


# ---------------------------------------------------------------------------
# 1. The pure verdict
# ---------------------------------------------------------------------------

def test_a_microscopic_forecast_is_refused():
    out = fsp.assess([4e-5, -3e-5, 1e-6] * 500, threshold=2.0)
    assert out["status"] == "refuse" and out["share_tradable"] == 0.0
    assert "too small to ever trade" in out["message"] and "vol_adjusted" in out["message"]


def test_a_normal_forecast_passes():
    out = fsp.assess([0.5, -3.0, 12.0, -20.0, 1.0] * 100, threshold=2.0)
    assert out["status"] == "ok" and out["share_tradable"] == pytest.approx(0.6)
    assert out["max_abs"] == 20.0


def test_every_forecast_nan_is_refused():
    out = fsp.assess([math.nan, None, float("inf")], threshold=2.0)
    assert out["status"] == "refuse" and out["n_bars"] == 0 and "NaN" in out["message"]


def test_the_one_percent_boundary():
    at = [2.0] * 1 + [0.0] * 99           # exactly 1% -> ok
    below = [2.0] * 1 + [0.0] * 100       # < 1% -> refuse
    assert fsp.assess(at, 2.0)["status"] == "ok"
    assert fsp.assess(below, 2.0)["status"] == "refuse"


def test_nan_bars_are_counted_but_not_in_the_share():
    out = fsp.assess([5.0, math.nan, 0.0], 2.0)
    assert out["n_nan"] == 1 and out["n_bars"] == 2 and out["share_tradable"] == 0.5


# ---------------------------------------------------------------------------
# 2. Sample and threshold
# ---------------------------------------------------------------------------

def _monthly(first_year: int, last_year: int) -> dict:
    windows = []
    for y in range(first_year, last_year + 1):
        for m in range(1, 13):
            ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
            windows.append({"label": f"{y}-{m:02d}",
                            "test": {"start": f"{y}-{m:02d}-01", "end": f"{ny}-{nm:02d}-01"}})
    return {"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": windows}


def test_one_window_per_training_era_never_reaching_2024():
    picked = fsp.sample_windows(_monthly(2018, 2025))
    assert [w["label"] for w in picked] == ["2018-01", "2021-01", "2023-01"]
    assert all(w["test"]["end"] < fsp.PROBE_CUTOFF for w in picked)


def test_the_last_2023_window_is_excluded_because_it_ends_on_the_cutoff():
    proto = {"symbols": ["X"], "windows": [
        {"label": "2023-12", "test": {"start": "2023-12-01", "end": "2024-01-01"}}]}
    assert fsp.sample_windows(proto) == []


def test_a_validation_only_protocol_is_skipped_not_refused():
    out = fsp.probe(Path("unused.json"), _monthly(2024, 2025))
    assert out["status"] == "skipped" and "2024-01-01" in out["message"]


def test_threshold_is_ten_times_the_live_rebalance_floor():
    cfg = json.loads(fsp.CONFIG_JSON.read_text(encoding="utf-8"))
    floor = cfg["risk_management"]["controls"]["min_allocation_change"]["threshold"]
    assert fsp.forecast_threshold() == pytest.approx(10 * floor)


@pytest.mark.parametrize("body", [{}, {"risk_management": {"controls": {}}},
                                  {"risk_management": {"controls": {
                                      "min_allocation_change": {"threshold": -0.1}}}}])
def test_a_missing_or_bad_floor_fails_loud(tmp_path, body):
    path = tmp_path / "config.json"
    path.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(ValueError):
        fsp.forecast_threshold(path)


# ---------------------------------------------------------------------------
# 3. Flag and subprocess helper
# ---------------------------------------------------------------------------

def test_flag_off_runs_nothing(monkeypatch, tmp_path):
    _set_orchestrator({})
    assert rpr._forecast_size_probe_enabled() is False
    monkeypatch.setattr(rpr.subprocess, "run", lambda *a, **k: pytest.fail("must not run"))
    assert rpr._forecast_size_violations(CONFIG, tmp_path / "p.json", tmp_path, "s", "v") == []


def test_the_real_campaign_config_keeps_the_flag_off():
    import yaml
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["forecast_size_probe"]["enabled"] is False


def test_a_non_bool_flag_raises():
    _set_orchestrator({"forecast_size_probe": {"enabled": "true"}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._forecast_size_probe_enabled()


def _fake_probe(result: dict, returncode: int = 0):
    calls = []

    def run(cmd, **kw):
        calls.append(cmd)
        if returncode == 0:
            out = Path(cmd[cmd.index("--json-out") + 1])
            out.write_text(json.dumps(result), encoding="utf-8")

        class _R:
            pass
        r = _R()
        r.returncode, r.stdout, r.stderr = returncode, "", "boom: engine failed"
        return r
    return run, calls


def test_helper_returns_the_refusal_and_records_every_probe(monkeypatch, tmp_path):
    _set_orchestrator({"forecast_size_probe": {"enabled": True}})
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    run_dir = tmp_path / "run_x"
    (run_dir / "artifacts").mkdir(parents=True)
    (tmp_path / "p.json").write_text("{}", encoding="utf-8")
    fake, calls = _fake_probe({"status": "refuse", "message": "too small"})
    monkeypatch.setattr(rpr.subprocess, "run", fake)
    msgs = rpr._forecast_size_violations(CONFIG, tmp_path / "p.json", run_dir, "st", "base")
    assert msgs == ["forecast size (D-056): too small"]
    assert calls and "forecast_size_probe.py" in calls[0][1]
    fake_ok, _ = _fake_probe({"status": "ok", "share_tradable": 0.5})
    monkeypatch.setattr(rpr.subprocess, "run", fake_ok)
    other = {**CONFIG, "strategies": {**CONFIG["strategies"], "warmup": 99}}  # not cached
    assert rpr._forecast_size_violations(other, tmp_path / "p.json", run_dir, "st", "v2") == []
    probes = rpr.load_yaml(run_dir / "artifacts" / rpr.FORECAST_SIZE_PROBE_FILE)["probes"]
    assert [(p["variant_id"], p["status"]) for p in probes] == [("base", "refuse"), ("v2", "ok")]


def test_a_crashed_probe_raises(monkeypatch, tmp_path):
    _set_orchestrator({"forecast_size_probe": {"enabled": True}})
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    (tmp_path / "p.json").write_text("{}", encoding="utf-8")
    fake, _ = _fake_probe({}, returncode=1)
    monkeypatch.setattr(rpr.subprocess, "run", fake)
    with pytest.raises(RuntimeError, match="forecast_size_probe failed.*boom"):
        rpr._forecast_size_violations(CONFIG, tmp_path / "p.json", tmp_path, "st", "base")


# ---------------------------------------------------------------------------
# 4. Wiring: right after 1b, and step 5a
# ---------------------------------------------------------------------------

def _validator(monkeypatch, returncode: int = 0):
    """Stub the validate_config.py subprocess the 1b size check runs first."""
    class _R:
        stdout, stderr = "", ""
    r = _R()
    r.returncode = returncode
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    monkeypatch.setattr(rpr.subprocess, "run", lambda *a, **k: r)


def _stub_probe(monkeypatch, refuse_ids: set, seen: list, crash_ids: set = frozenset()):
    def fake(config, protocol_path, run_dir, stage, variant_id):
        seen.append((stage, variant_id))
        if variant_id in crash_ids:
            raise RuntimeError("forecast_size_probe failed: No historical data")
        return [f"forecast size (D-056): {variant_id} too small"] if variant_id in refuse_ids else []
    monkeypatch.setattr(rpr, "_forecast_size_violations", fake)
    monkeypatch.setattr(rpr, "_resolve_protocol_path", lambda run_dir, run_id: Path("proto.json"))


def test_post_1b_a_refused_size_goes_back_to_1b(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True},
                       "forecast_size_probe": {"enabled": True}})
    seen = []
    _validator(monkeypatch)
    _stub_probe(monkeypatch, {"base"}, seen)
    run_dir = _authored_1b("run_960", CONFIG)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]
    assert retry["attempts"] == 1 and "forecast size (D-056)" in retry["last_error"]
    assert seen == [("strategy_config_authoring", "base")]
    assert _refusals(run_dir)[0]["violations"] == ["forecast size (D-056): base too small"]


def test_post_1b_flag_off_never_probes(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    monkeypatch.setattr(rpr, "_resolve_protocol_path",
                        lambda *a: pytest.fail("flag off must not resolve or probe"))
    run_dir = _authored_1b("run_961", CONFIG)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


def test_5a_a_refused_size_is_a_config_error_and_others_go_on(monkeypatch):
    _set_orchestrator({"forecast_size_probe": {"enabled": True}})
    seen = []
    _stub_probe(monkeypatch, {"tiny"}, seen)
    variants = _run_5a(monkeypatch, "run_962", CONFIG, [
        _design("tiny", [{"path": COMP0 + "/params/period", "value": 21}]),
        _design("fine", [{"path": COMP0 + "/params/period", "value": 30}]),
    ])
    assert variants["base"]["status"] == "validated"
    assert variants["fine"]["status"] == "validated"
    assert variants["tiny"]["status"] == "not_tested"
    assert variants["tiny"]["reason"] == rpr.FORECAST_RULE_REASON
    assert "forecast size (D-056)" in variants["tiny"]["report"]
    assert dict(rpr._variant_config_errors(variants)).keys() == {"tiny"}
    assert sorted(v for s, v in seen) == ["base", "fine", "tiny"]
    assert {s for s, v in seen} == {"backtest_specification"}


# ---------------------------------------------------------------------------
# 5. Review fixes: strategy floor, 1b skip rules, 5a crash, cache, engine call
# ---------------------------------------------------------------------------

def test_the_strategy_config_floor_overrides_config_json():
    cfg = {"strategies": {"min_allocation_change": 0.05}}
    assert fsp.forecast_threshold(strategy_config=cfg) == pytest.approx(0.5)


def test_a_zero_strategy_floor_means_any_nonzero_forecast_trades():
    thr = fsp.forecast_threshold(strategy_config={"strategies": {"min_allocation_change": 0}})
    assert thr == 0.0
    assert fsp.assess([0.0] * 99 + [1e-6], thr)["status"] == "ok"
    assert fsp.assess([0.0] * 100, thr)["status"] == "refuse"


def test_a_negative_strategy_floor_fails_loud():
    with pytest.raises(ValueError, match="non-negative"):
        fsp.forecast_threshold(strategy_config={"strategies": {"min_allocation_change": -1}})


def test_post_1b_skips_the_probe_when_the_config_does_not_validate(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True},
                       "forecast_size_probe": {"enabled": True}})
    seen = []
    _validator(monkeypatch, returncode=1)
    _stub_probe(monkeypatch, {"base"}, seen)
    run_dir = _authored_1b("run_963", CONFIG)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert seen == []


def test_post_1b_a_probe_that_cannot_run_is_recorded_and_left_to_5a(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True},
                       "forecast_size_probe": {"enabled": True}})
    seen = []
    _validator(monkeypatch)
    _stub_probe(monkeypatch, set(), seen, crash_ids={"base"})
    run_dir = _authored_1b("run_964", CONFIG)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    probes = rpr.load_yaml(run_dir / "artifacts" / rpr.FORECAST_SIZE_PROBE_FILE)["probes"]
    assert probes[0]["status"] == "error" and "No historical data" in probes[0]["message"]


def test_post_1b_a_manifest_error_is_never_probed(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True},
                       "forecast_size_probe": {"enabled": True}})
    seen = []
    _validator(monkeypatch)
    _stub_probe(monkeypatch, {"base"}, seen)
    run_dir = _authored_1b("run_965", CONFIG, manifest=None)
    rpr.determine_post_strategy_config_authoring_route(run_dir)
    assert seen == []


def test_5a_a_probe_that_cannot_run_marks_only_that_variant(monkeypatch):
    _set_orchestrator({"forecast_size_probe": {"enabled": True}})
    seen = []
    _stub_probe(monkeypatch, set(), seen, crash_ids={"nodata"})
    variants = _run_5a(monkeypatch, "run_966", CONFIG, [
        _design("nodata", [{"path": COMP0 + "/params/period", "value": 21}]),
        _design("fine", [{"path": COMP0 + "/params/period", "value": 30}]),
    ])
    assert variants["nodata"]["status"] == "not_tested"
    assert variants["nodata"]["reason"] == rpr.FORECAST_SIZE_PROBE_ERROR_REASON
    assert variants["fine"]["status"] == "validated" and variants["base"]["status"] == "validated"
    assert "nodata" not in dict(rpr._variant_config_errors(variants))  # not a Step 2 fix


def test_the_same_config_and_protocol_is_probed_once(monkeypatch, tmp_path):
    _set_orchestrator({"forecast_size_probe": {"enabled": True}})
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    run_dir = tmp_path / "run_y"
    (run_dir / "artifacts").mkdir(parents=True)
    proto = tmp_path / "p.json"
    proto.write_text('{"symbols": ["BTCUSDT"]}', encoding="utf-8")
    fake, calls = _fake_probe({"status": "refuse", "message": "too small"})
    monkeypatch.setattr(rpr.subprocess, "run", fake)
    first = rpr._forecast_size_violations(CONFIG, proto, run_dir, "strategy_config_authoring", "base")
    again = rpr._forecast_size_violations(CONFIG, proto, run_dir, "backtest_specification", "base")
    assert first == again == ["forecast size (D-056): too small"] and len(calls) == 1
    proto.write_text('{"symbols": ["ETHUSDT"]}', encoding="utf-8")  # other protocol: new probe
    rpr._forecast_size_violations(CONFIG, proto, run_dir, "backtest_specification", "base")
    assert len(calls) == 2


HOLDOUT_SENTINEL = "HOLDOUT-START-SENTINEL"  # a marker, never a real date


def test_the_engine_call_is_sealed_and_holdout_guarded(monkeypatch, tmp_path):
    """_run_sample with run_backtest stubbed: holdout_start passed, warmup on,
    every output under the temp dir, feed caches never written, and only the
    forecast column is read."""
    import types
    calls = []

    def fake_run_backtest(config_path, symbol, start, end, results_root, **kw):
        calls.append({"symbol": symbol, "start": start, "end": end,
                      "results_root": results_root, **kw})
        rd = Path(results_root) / f"r{len(calls)}"
        rd.mkdir(parents=True)
        (rd / "bars.csv").write_text("timestamp,forecast,net_pnl\n1,5.0,999\n2,0.0,-999\n",
                                     encoding="utf-8")
        return rd

    fake_rp = types.SimpleNamespace(
        _load_policy_or_refuse=lambda: {"policy": True},
        _training_holdout_start=lambda protocol, policy: HOLDOUT_SENTINEL,
        _preflight_training_windows=lambda protocol, hs: calls.append({"preflight": hs}))
    fake_launcher = types.ModuleType("core.launcher")
    fake_launcher.run_backtest = fake_run_backtest
    fake_launcher.parse_interval_seconds = lambda tf: 86400
    monkeypatch.setitem(sys.modules, "run_protocol", fake_rp)
    monkeypatch.setitem(sys.modules, "core", types.ModuleType("core"))
    monkeypatch.setitem(sys.modules, "core.launcher", fake_launcher)
    protocol = _monthly(2018, 2025)
    windows = fsp.sample_windows(protocol)
    forecasts = fsp._run_sample(Path("cfg.json"), protocol, windows, tmp_path)
    assert forecasts == [5.0, 0.0] * 3
    runs = [c for c in calls if "symbol" in c]
    assert calls[0] == {"preflight": HOLDOUT_SENTINEL} and len(runs) == 3
    for c in runs:
        assert c["holdout_start"] == HOLDOUT_SENTINEL and c["warmup_prefetch"] is True
        assert c["feed_local_storage"] is False
        assert Path(c["runs_root"]) == tmp_path and Path(c["results_root"]) == tmp_path
        assert Path(c["trades_log_file"]).parent == tmp_path
        assert c["end"] < fsp.PROBE_CUTOFF and c["exchange"] == "binance"
