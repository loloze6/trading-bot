"""
D-056 / O-10: the forecast-size probe (tools/forecast_size_probe.py) and its
wiring (orchestrator.forecast_size_probe.enabled, off by default).

C4 run_061: `vol_adjusted` on a percent-unit component shrank the forecast to
~1e-5, so the variant made 0 trades in 95 windows and nothing flagged it. The
probe refuses a config whose forecast is BROKEN IN SIZE (largest |forecast|
below 1/100 of the size needed to trade, or all NaN) -- bug detection only,
never a judgement on how often a strategy trades -- and it runs the real
strategy code on INVENTED data only (operator, 2026-10-02).

Covers: the bug-only verdict (quiet and silent strategies pass); the invented
series (deterministic, every live feed, invented calendar, no real data read);
the run_061 bug refused on invented data with the real strategy code; the
threshold (config.json and the strategy override); the flag (off = nothing
run); the subprocess helper; the post-1b route and step 5a.
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
# 1. The pure verdict: bug-only (operator, 2026-10-02)
# ---------------------------------------------------------------------------

def test_a_microscopic_forecast_is_refused():
    out = fsp.assess([4e-5, -3e-5, 1e-6] * 500, threshold=2.0)
    assert out["status"] == "refuse"
    assert "broken in size" in out["message"] and "vol_adjusted" in out["message"]


def test_a_normal_forecast_passes():
    out = fsp.assess([0.5, -3.0, 12.0, -20.0, 1.0] * 100, threshold=2.0)
    assert out["status"] == "ok" and out["max_abs"] == 20.0


def test_a_quiet_strategy_passes_however_rarely_it_could_trade():
    """Bug-only: one bar of normal size in 10,000 is enough -- how often a
    strategy trades is the backtest's question, not the probe's."""
    assert fsp.assess([0.0] * 9999 + [2.5], 2.0)["status"] == "ok"
    # small forecasts most of the time, never reaching 2.0, still pass above 1/100
    assert fsp.assess([0.03] * 5000, 2.0)["status"] == "ok"


def test_a_forecast_silent_on_every_bar_passes_with_a_note():
    out = fsp.assess([0.0] * 3000, 2.0)
    assert out["status"] == "ok" and "silent" in out["note"]


def test_every_forecast_nan_is_refused():
    out = fsp.assess([math.nan, None, float("inf")], threshold=2.0)
    assert out["status"] == "refuse" and out["n_bars"] == 0 and "NaN" in out["message"]


def test_the_bug_limit_is_one_hundredth_of_the_trading_size():
    assert fsp.BUG_FACTOR == 0.01
    assert fsp.assess([0.0199] * 10, 2.0)["status"] == "refuse"
    assert fsp.assess([0.02] * 10, 2.0)["status"] == "ok"


def test_nan_bars_are_counted_apart():
    out = fsp.assess([5.0, math.nan, 0.0], 2.0)
    assert out["n_nan"] == 1 and out["n_bars"] == 2 and out["share_nonzero"] == 0.5


# ---------------------------------------------------------------------------
# 2. Invented data and threshold
# ---------------------------------------------------------------------------

def test_the_invented_series_is_deterministic_and_carries_every_live_feed():
    a = fsp.synthetic_bars(500, 3600)
    b = fsp.synthetic_bars(500, 3600)
    assert a.equals(b)
    sys.path.insert(0, str(SR_ROOT.parent / "trading-bot"))
    from data.feed_registry import FEED_REGISTRY
    assert set(FEED_REGISTRY) <= set(a.columns)
    assert {"timestamp", "open", "high", "low", "close", "volume"} <= set(a.columns)
    assert a[list(FEED_REGISTRY)].notna().all().all()
    assert (a["high"] >= a[["open", "close"]].max(axis=1)).all()
    assert (a["low"] <= a[["open", "close"]].min(axis=1)).all()


def test_the_invented_calendar_is_far_from_any_real_date():
    ts = fsp.synthetic_bars(3000, 86400)["timestamp"]
    assert ts.min().year == 2000 and ts.max().year < 2010


_OPENED: list = []
_RECORDING = [False]


def _audit(event, args):
    if _RECORDING[0] and event == "open" and args and isinstance(args[0], (str, bytes, Path)):
        _OPENED.append(str(args[0]))


sys.addaudithook(_audit)  # audit hooks cannot be removed; it records only while flagged


def test_no_real_data_is_read():
    """Every file the probe opens (audit hook, so open()/pandas/pyarrow are all
    seen): only the strategy config and trading-bot/config.json -- never a
    cache, never local_data. The engine's data modules are never imported."""
    cfg = SR_ROOT.parent / "trading-bot" / "strategy_config.json"
    _OPENED.clear()
    _RECORDING[0] = True
    try:
        out = fsp.probe(cfg, {"timeframe": "1h"})
    finally:
        _RECORDING[0] = False
    assert out["data"] == "invented" and out["status"] in ("ok", "refuse")
    data_files = [p for p in _OPENED if not p.endswith((".py", ".pyc", ".pyd", ".dll", ".so"))
                  and "site-packages" not in p and "__pycache__" not in p]
    assert all("local_data" not in p for p in _OPENED), _OPENED
    assert {Path(p).name for p in data_files} <= {"strategy_config.json", "config.json"}, data_files


def test_an_unknown_timeframe_fails_loud():
    with pytest.raises(ValueError, match="timeframe"):
        fsp.probe(Path("unused.json"), {"timeframe": "7m"})


def _cfg_file(tmp_path, transforms):
    import copy
    cfg = copy.deepcopy(CONFIG)
    comp = cfg["strategies"]["regimes"]["unknown"]["components"][0]
    comp.update({"class": "strategies.strategy_components.MovingAverageDistanceComponent",
                 "params": {"average": "sma", "period": 50}, "transforms": transforms})
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


def test_the_run_061_units_bug_is_refused_on_invented_data(tmp_path):
    """The real strategy code on the invented series: a percent signal followed
    by vol_adjusted alone is refused; the same signal plainly scaled is not."""
    bad = fsp.probe(_cfg_file(tmp_path, [{"op": "vol_adjusted"}]), {"timeframe": "1h"})
    assert bad["status"] == "refuse" and bad["max_abs"] < 0.02
    good = fsp.probe(_cfg_file(tmp_path, [{"op": "scale", "params": {"factor": 5.0}}]),
                     {"timeframe": "1h"})
    assert good["status"] == "ok" and good["max_abs"] >= 2.0


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
    assert fsp.assess([1e-9] * 100, thr)["status"] == "ok"  # no size bug can exist at floor 0


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
