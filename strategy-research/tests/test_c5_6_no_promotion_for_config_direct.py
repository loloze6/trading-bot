"""
C5.6 (delivery_plan_v26_continuation.md C5.6, decision D-043) -- new-pipeline
runs need no promotion block.

A protocol's `promotion` block feeds only tools/run_protocol.py's legacy
top-level promote/kill/refine verdict, which decides nothing once BOTH
orchestrator.config_direct_authoring and orchestrator.verdict_routing_retired
are on (the grid and the profit bars decide; the legacy verdict_interpreter
route is retired). Under that condition ("promotion retired",
run_phase1_research._promotion_retired_enabled):

  * G7 (_require_pre_registered_promotion) is skipped and a generated protocol
    carries NO `promotion` key -- whatever the brief pre-registered is dropped
    (at materialization, from pre_registration.yaml, and again by the
    generator), never copied, never invented;
  * registration refuses the abolished generic block and a present-but-empty
    block, and accepts any other with a logged note;
  * run_tool_worker passes --legacy-verdict-retired to run_protocol.py, which
    then records `verdict: null` and reads no promotion block.

config_direct_authoring alone (verdict routing live) keeps G7. Flag off: G7,
D-3 and the registration lint are exactly as before, and the flag-off generator
reads no config before G7. run_protocol.py without --legacy-verdict-retired
refuses a missing/empty/partial block before any backtest (it used to raise
KeyError after every window had been spent).

Hermetic: the conftest sandbox is ROOT, run_loop is stubbed, no LLM, no real
backtest.
"""
import ast
import json
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import protocol_resolution as protres  # noqa: E402
import run_protocol as rp  # noqa: E402
import composite_cache as cc  # noqa: E402

from test_e061_c1_4_5_pauses_preflight import (  # noqa: E402
    RUN, _NON_GENERIC, _Reached, _entries, _entry, _log_text, _protocol, _queue,
    _reach_run_loop, _scaffold, _set_pre_registration, _write_config)

_GENERATED_KEYS_FLAG_OFF = ["symbols", "timeframe", "windows", "holdout", "promotion"]
_GENERATED_KEYS_RETIRED = ["symbols", "timeframe", "windows", "holdout"]
_PARTIAL = {"median_sharpe_gt": 0.5}

# The flag set under which the promotion block is retired, with every
# dependency verdict_routing_retired's strict reader checks.
_RETIRED_FLAGS = {name: {"enabled": True} for name in (
    "config_direct_authoring", "verdict_routing_retired", "decide_next", "regroup_record",
    "specialist_readers", "grid_evaluation", "category_reports",
    "profit_bars_every_backtest", "profit_bars_file")}


def _constraints(promotion="absent", **over) -> dict:
    proto = {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
             "end": "2022-03-01"}
    if promotion != "absent":
        proto["promotion"] = promotion
    proto.update(over)
    return {"protocol": proto}


@pytest.fixture
def config_direct_only(monkeypatch):
    monkeypatch.setattr(rpr, "_config_direct_authoring_enabled", lambda cfg=None: True)


@pytest.fixture
def retired(monkeypatch):
    monkeypatch.setattr(rpr, "_config_direct_authoring_enabled", lambda cfg=None: True)
    monkeypatch.setattr(rpr, "_verdict_routing_retired_enabled", lambda cfg=None: True)


def _generated_path(run_id: str = RUN) -> Path:
    return rpr.ROOT / "protocols" / f"{run_id}_generated.json"


def _no_config_reads(monkeypatch):
    """Every way the orchestrator reads config/campaign_config.yaml fails the test."""
    def _boom(*a, **k):
        raise AssertionError("config/campaign_config.yaml was read")
    for name in ("_orchestrator_config", "_strict_orchestrator_flag",
                 "_config_direct_authoring_enabled", "_verdict_routing_retired_enabled",
                 "_promotion_retired_enabled"):
        monkeypatch.setattr(rpr, name, _boom)


# ---------------------------------------------------------------------------
# The condition (review fix 1)
# ---------------------------------------------------------------------------

def test_promotion_retired_needs_both_flags():
    _write_config(None)
    assert rpr._promotion_retired_enabled() is False
    _write_config({"config_direct_authoring": {"enabled": True}})
    assert rpr._promotion_retired_enabled() is False
    _write_config(_RETIRED_FLAGS)
    assert rpr._promotion_retired_enabled() is True
    cfg = {"orchestrator": _RETIRED_FLAGS}
    assert camp._promotion_retired_from({n: True for n in _RETIRED_FLAGS}, None) is True
    assert camp._promotion_retired_from({n: True for n in _RETIRED_FLAGS}, "refused") is False
    assert camp._promotion_retired_from({"config_direct_authoring": True,
                                         "verdict_routing_retired": False}, None) is False
    assert rpr._promotion_retired_enabled(cfg) is True


def test_config_direct_alone_keeps_g7(config_direct_only, monkeypatch):
    """config_direct_authoring with verdict routing live: the legacy verdict
    still decides, so G7 is kept -- the generator, the pre-flight (through
    process_once's own flag reading) and run_protocol's arguments."""
    assert rpr._promotion_retired_enabled() is False
    run_dir = _scaffold(constraints=_constraints())
    with pytest.raises(rpr.UngatedProtocolError, match=r"\[G7\]"):
        rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(),
                                              promotion_retired=rpr._promotion_retired_enabled)
    assert not _generated_path().exists()
    assert rpr._legacy_verdict_args() == []
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: pytest.fail("run_loop reached"))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == f"paused:{camp.PROTOCOL_PREFLIGHT_HALT}"
    assert "[G7]" in _log_text() and "cannot generate a protocol" in _log_text()
    # ... and a pre-registered block is still copied verbatim (G7's own output)
    constraints = _constraints(_NON_GENERIC)
    _set_pre_registration(run_dir, constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints,
                                                 promotion_retired=rpr._promotion_retired_enabled)
    assert json.loads(path.read_text(encoding="utf-8"))["promotion"] == _NON_GENERIC


def test_legacy_verdict_args_only_under_the_full_condition(monkeypatch):
    assert rpr._legacy_verdict_args() == []
    monkeypatch.setattr(rpr, "_config_direct_authoring_enabled", lambda cfg=None: True)
    assert rpr._legacy_verdict_args() == []
    monkeypatch.setattr(rpr, "_verdict_routing_retired_enabled", lambda cfg=None: True)
    assert rpr._legacy_verdict_args() == ["--legacy-verdict-retired"]


# ---------------------------------------------------------------------------
# G7 -- the generator (review fixes 3 and 6)
# ---------------------------------------------------------------------------

def test_flag_off_g7_still_refuses_a_generated_protocol_without_promotion():
    assert rpr._config_direct_authoring_enabled() is False
    run_dir = _scaffold(constraints=_constraints())
    with pytest.raises(rpr.UngatedProtocolError, match=r"\[G7\]"):
        rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    assert not _generated_path().exists()
    with pytest.raises(rpr.UngatedProtocolError, match=r"\[G7\]"):
        camp._expected_generated_protocol(_constraints()["protocol"], RUN,
                                          promotion_retired=False)


@pytest.mark.parametrize("promotion", ["absent", {}, None], ids=["absent", "empty", "null"])
def test_flag_off_generator_reads_no_config_before_g7(monkeypatch, promotion):
    """Review fix 6: the flag-off generator's I/O and failure mode are
    master's: no config read at all (a malformed config file is not even
    opened), and G7's exact error."""
    _write_config({"config_direct_authoring": {"enabled": "false"}})  # would raise if read
    _no_config_reads(monkeypatch)
    run_dir = _scaffold(constraints=_constraints(promotion))
    master_message = (
        f"[G7] run {RUN}: machine_constraints.protocol has no pre-registered "
        f"`promotion` block. Refusing to substitute generic thresholds -- a "
        f"protocol materialized from defaults is structurally ungated, and any "
        f"verdict computed against it would misrepresent invented thresholds as "
        f"pre-registered ones. Add an explicit `promotion` block (B11 total "
        f"mapping) to the brief's machine_constraints, then re-run.")
    with pytest.raises(rpr.UngatedProtocolError) as exc:
        rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(promotion))
    assert str(exc.value) == master_message
    with pytest.raises(rpr.UngatedProtocolError) as exc:
        camp._expected_generated_protocol(_constraints(promotion)["protocol"], RUN,
                                          promotion_retired=False)
    assert str(exc.value) == master_message
    assert not _generated_path().exists()


def test_flag_off_generated_protocol_is_unchanged_key_for_key_and_in_order(monkeypatch):
    """Byte-identity of the flag-off generator: same keys, same order (promotion
    last), the brief's block verbatim -- and no config read."""
    _no_config_reads(monkeypatch)
    constraints = _constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    written = json.loads(path.read_text(encoding="utf-8"))
    assert list(written) == _GENERATED_KEYS_FLAG_OFF
    assert written["promotion"] == _NON_GENERIC
    expected_bytes = json.dumps({
        "symbols": ["BTCUSDT"], "timeframe": "1h",
        "windows": rpr._generate_monthly_windows("2022-01-01", "2022-03-01"),
        "holdout": rpr._generated_protocol_holdout_block(constraints["protocol"]),
        "promotion": _NON_GENERIC}, indent=2)
    assert path.read_text(encoding="utf-8") == expected_bytes


def test_the_reader_is_called_only_when_a_protocol_is_generated():
    constraints = _constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)

    def _boom():
        raise AssertionError("flags read for an already-generated protocol")
    assert rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints,
                                                 promotion_retired=_boom) == path


@pytest.mark.parametrize("promotion", ["absent", _NON_GENERIC, _PARTIAL,
                                       dict(rpr._GENERIC_PROMOTION), {}, None],
                         ids=["absent", "real", "partial", "generic", "empty", "null"])
def test_retired_generates_a_protocol_with_no_promotion_key(retired, promotion, capsys):
    """Review fix 3: under the condition no pre-registered block is ever copied
    -- a partial one no longer rides along to crash run_protocol after spend."""
    constraints = _constraints(promotion)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints,
                                                 promotion_retired=rpr._promotion_retired_enabled)
    written = json.loads(path.read_text(encoding="utf-8"))
    assert list(written) == _GENERATED_KEYS_RETIRED
    assert camp._expected_generated_protocol(constraints["protocol"], RUN,
                                             promotion_retired=True) == written
    noted = "promotion is ignored and not copied" in capsys.readouterr().out
    assert noted is (promotion != "absent")
    run_ctx = yaml.safe_load((run_dir / "artifacts" / "run_context.yaml").read_text(encoding="utf-8"))
    assert run_ctx == {"run_type": "forced_diagnostic", "protocol": path.name}


# ---------------------------------------------------------------------------
# Materialization: pre_registration.yaml (an LLM context file, and decide_next's
# source of a candidate's machine_constraints) never carries the retired block
# ---------------------------------------------------------------------------

def _brief(promotion) -> dict:
    return {"strategy_domain": "crypto_directional", "market_universe": ["BTCUSDT"],
            "timeframe": "1h", "research_goal": "g", "venue": "binance", "product": "spot",
            "machine_constraints": _constraints(promotion)}


@pytest.mark.parametrize("retired_flag", [False, True])
def test_materialize_drops_the_block_only_when_retired(retired_flag):
    run_dir = _scaffold("run_050")
    camp._materialize_run("run_050", _brief(_NON_GENERIC), promotion_retired=retired_flag)
    pre = yaml.safe_load((run_dir / "artifacts" / "pre_registration.yaml")
                         .read_text(encoding="utf-8"))
    proto = pre["machine_constraints"]["protocol"]
    if retired_flag:
        assert "promotion" not in proto
        assert proto == {k: v for k, v in _constraints()["protocol"].items()}
        assert "PROMOTION run_050: machine_constraints.protocol.promotion dropped" in _log_text()
    else:
        assert proto["promotion"] == _NON_GENERIC
        assert "PROMOTION run_050" not in _log_text()


# ---------------------------------------------------------------------------
# The launch pre-flight (review fixes 5 and 9) and D-3 (kept)
# ---------------------------------------------------------------------------

def test_retired_no_promotion_protocol_passes_every_resolution(retired, monkeypatch):
    run_dir = _scaffold(constraints=_constraints())
    assert camp._protocol_preflight(run_dir, RUN, promotion_retired=True) == (None, None)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(),
                                                 promotion_retired=True)
    assert camp._protocol_preflight(run_dir, RUN, promotion_retired=True) == (None, None)
    protres.assert_promotion_ratified(path)
    assert rpr._resolve_protocol_path(run_dir, RUN) == path          # 5a / data gate / backtest
    assert protres.resolve_protocol_path(run_dir, RUN, rpr.ROOT / "protocols") == path
    _queue([_entry()])
    _reach_run_loop(monkeypatch)
    with pytest.raises(_Reached):
        camp.process_once()
    assert _entries()[0]["status"] == "in_progress"


def test_the_preflight_reads_no_config(monkeypatch):
    """Review fix 5: the pre-flight's promotion decision comes from the caller's
    single parsed reading -- the plan itself reads no config."""
    _no_config_reads(monkeypatch)
    run_dir = _scaffold(constraints=_constraints())
    assert camp._protocol_preflight(run_dir, RUN, promotion_retired=True) == (None, None)
    refusal, _ = camp._protocol_preflight(run_dir, RUN, promotion_retired=False)
    assert "[G7]" in refusal and "cannot generate a protocol" in refusal


def test_a_config_error_is_a_flag_refusal_not_a_generation_error(monkeypatch):
    """Review fix 5: a malformed config pauses as flag_misconfiguration, never
    as "pre_registration.yaml's machine_constraints.protocol cannot generate"."""
    _write_config({"config_direct_authoring": {"enabled": "true"}})
    _scaffold(constraints=_constraints())
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: pytest.fail("run_loop reached"))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == f"paused:{camp.FLAG_PREFLIGHT_HALT}"
    assert "cannot generate" not in _log_text()
    assert "config_direct_authoring.enabled='true'" in _log_text()


@pytest.mark.parametrize("on_disk", [None, {}], ids=["null", "empty"])
def test_absent_null_and_empty_compare_equal_in_the_regeneration_diff(on_disk):
    """Review fix 9: a generated file whose promotion is null or {} and an
    expected protocol with none are the same "no block" -- no regeneration."""
    run_dir = _scaffold(constraints=_constraints())
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(),
                                                 promotion_retired=True)
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["promotion"] = on_disk
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    assert camp._protocol_preflight(run_dir, RUN, promotion_retired=True) == (None, None)


def test_retired_regenerates_a_file_written_earlier_with_a_block(monkeypatch):
    """A protocol generated before the flags were both on (block copied by G7)
    is regenerated without it before any spend; windows etc. untouched."""
    constraints = _constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN, promotion_retired=True)
    assert refusal is None and regeneration["differing"] == ["promotion"]
    assert "promotion" not in regeneration["doc"]
    assert regeneration["path"] == path


def test_generic_block_refusal_message_is_master_text_whatever_the_flags():
    run_dir = _scaffold(constraints=_constraints(dict(rpr._GENERIC_PROMOTION)))
    refusal, _ = camp._protocol_preflight(run_dir, RUN, promotion_retired=False)
    assert refusal.endswith("pre_registration.yaml's machine_constraints.protocol.promotion")
    assert "C5.6" not in refusal
    # under the condition the generic block is dropped, never judged
    assert camp._protocol_preflight(run_dir, RUN, promotion_retired=True) == (None, None)


@pytest.mark.parametrize("retired_flag", [False, True])
def test_pinned_unratified_generic_protocol_is_refused_either_way(retired_flag):
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    run_dir = _scaffold(constraints={"protocol_ref": "protocols/generic.json"})
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN,
                                                     promotion_retired=retired_flag)
    assert regeneration is None and "[G7/D-3]" in refusal and "generic.json" in refusal


# ---------------------------------------------------------------------------
# run_protocol.py -- the legacy top-level verdict (review fixes 2 and 7)
# ---------------------------------------------------------------------------

class _StubBacktest:
    def __init__(self, root: Path):
        self.root, self.calls = root, 0

    def __call__(self, cfg_path, symbol, start, end, results_root, **kwargs):
        self.calls += 1
        rd = self.root / f"stub_run_{self.calls}"
        rd.mkdir(parents=True, exist_ok=True)
        (rd / "metrics.json").write_text(json.dumps({"core": {
            "trade_count": 12, "net_pnl": 1.0, "sharpe": 0.4, "win_rate": 0.5,
            "max_drawdown_pct": -2.0, "forecast_return_corr": 0.03, "gross_pnl": 2.0,
            "cost_drag_pct": 40.0, "avg_trade_duration_bars": 6}}), encoding="utf-8")
        return rd


def _run_protocol(monkeypatch, tmp_path, promotion, *extra) -> tuple:
    stub = _StubBacktest(tmp_path / "sandbox_runs")
    monkeypatch.setattr(rp, "run_backtest", stub)
    monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
    protocol = {"symbols": ["BTCUSDT"],
                "windows": [{"label": f"w{i}", "test": {"start": f"2022-0{i}-01",
                                                        "end": f"2022-0{i}-02"}}
                            for i in (1, 2)]}
    if promotion != "absent":
        protocol["promotion"] = promotion
    (tmp_path / "protocol.json").write_text(json.dumps(protocol), encoding="utf-8")
    (tmp_path / "config.json").write_text(json.dumps({"dummy": True}), encoding="utf-8")
    out = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", ["run_protocol.py", str(tmp_path / "config.json"),
                                      str(tmp_path / "protocol.json"), "--out-dir", str(out),
                                      *extra])
    rp.main()
    return json.loads((out / "protocol_summary.json").read_text(encoding="utf-8")), stub


@pytest.mark.parametrize("promotion", ["absent", {}, None, _PARTIAL],
                         ids=["absent", "empty", "null", "partial"])
@pytest.mark.parametrize("extra", [(), ("--diagnostics-only",)])
def test_run_protocol_refuses_an_unusable_block_before_any_backtest(monkeypatch, tmp_path,
                                                                    capsys, promotion, extra):
    """Review fix 2: without --legacy-verdict-retired the block is required, as
    on master -- but refused before any window runs (master raised KeyError
    after every window, the holdout's included, had been spent)."""
    with pytest.raises(SystemExit) as exc:
        _run_protocol(monkeypatch, tmp_path, promotion, *extra)
    assert exc.value.code == rp.EXIT_NO_DATA_TOUCHED
    assert capsys.readouterr().err.startswith(rp.NO_DATA_TOUCHED_TOKEN)
    assert not (tmp_path / "out" / "protocol_summary.json").exists()
    assert not (tmp_path / "sandbox_runs").exists()  # no backtest ran


@pytest.mark.parametrize("promotion", ["absent", _PARTIAL, _NON_GENERIC],
                         ids=["absent", "partial", "real"])
def test_run_protocol_retired_flag_records_a_null_verdict_and_reads_no_block(
        monkeypatch, tmp_path, promotion):
    summary, stub = _run_protocol(monkeypatch, tmp_path, promotion,
                                  "--diagnostics-only", "--legacy-verdict-retired")
    assert stub.calls == 2
    assert summary["verdict"] is None
    assert summary["verdict_reason"] == rp.LEGACY_VERDICT_RETIRED_REASON
    # everything config-direct consumers read is still there
    assert summary["per_symbol_summary"]["BTCUSDT"]["median_sharpe"] == 0.4
    assert len(summary["results"]) == 2
    assert summary["hypothesis_verdict"]["diagnostics"]["median_cost_drag_pct"] == 40.0


def test_run_protocol_with_promotion_cites_the_protocols_own_thresholds(monkeypatch, tmp_path):
    """Review fix 7: the reason used to print the generic >0 / <30 / >=20
    whatever the protocol registered (this test froze that false text)."""
    summary, _ = _run_protocol(monkeypatch, tmp_path, {
        "median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 25,
        "min_trade_count_gte": 1, "kill_median_sharpe_lt": -1})
    assert summary["verdict"] == "promote"
    assert summary["verdict_reason"] == ("BTCUSDT: median_sharpe=0.400>0 max_dd=2.0%<25 "
                                         "min_trades=12>=1")


_PS = {"BTCUSDT": {"median_sharpe": 0.4, "max_abs_drawdown_pct": 2.0, "min_trade_count": 12},
       "ETHUSDT": {"median_sharpe": -1.7, "max_abs_drawdown_pct": 41.0, "min_trade_count": 3}}


def test_legacy_verdict_reason_cites_real_thresholds_for_every_outcome():
    promo = {"median_sharpe_gt": 0.3, "max_abs_drawdown_pct_lt": 40,
             "min_trade_count_gte": 10, "kill_median_sharpe_lt": -1.5}
    assert rp.legacy_top_level_verdict(_PS, ["BTCUSDT"], promo) == (
        "promote", "BTCUSDT: median_sharpe=0.400>0.3 max_dd=2.0%<40 min_trades=12>=10")
    assert rp.legacy_top_level_verdict(_PS, ["ETHUSDT"], promo) == (
        "kill", "every symbol below the kill threshold: ETHUSDT: median_sharpe=-1.700<-1.5")
    assert rp.legacy_top_level_verdict(_PS, ["BTCUSDT", "ETHUSDT"], promo) == (
        "refine", "ETHUSDT: median_sharpe=-1.700<=0.3, max_dd=41.0%>=40, min_trades=3<10")


def test_composite_runner_passes_the_retired_flag(monkeypatch, tmp_path):
    """The composite exists only under composition_runs, which requires both
    flags -- its run_protocol.py call must not be refused for want of a block."""
    calls = []

    class _Done:
        returncode, stdout, stderr = 0, "", ""
    monkeypatch.setattr(cc.subprocess, "run",
                        lambda cmd, *a, **k: calls.append([str(c) for c in cmd]) or _Done())
    cc.subprocess_runner("py")(tmp_path / "c.json", tmp_path / "p.json", tmp_path / "o")
    (argv,) = calls
    assert "--legacy-verdict-retired" in argv


# ---------------------------------------------------------------------------
# Consumers: nothing but the gates, the materialization drop and the legacy
# verdict touches a `promotion` key (review fix 4)
# ---------------------------------------------------------------------------

# Every function in workflow/ and tools/ that touches a `promotion` key by any of
# x["promotion"], x.get/pop/setdefault("promotion", ...), "promotion" in/not in x.
# A new reader must be added here deliberately.
_PROMOTION_READERS = {
    ("run_protocol.py", "main"),                                          # legacy verdict
    ("protocol_resolution.py", "assert_promotion_ratified"),              # D-3
    ("run_phase1_research.py", "_assert_promotion_ratified"),             # D-3 (orchestrator copy)
    ("run_phase1_research.py", "_require_pre_registered_promotion"),      # G7
    ("run_phase1_research.py", "_generated_protocol_promotion"),          # C5.6 generator
    ("run_campaign.py", "_generated_protocol_plan"),                      # D-3 pre-flight
    ("run_campaign.py", "_check_generate_protocol_has_promotion"),        # registration (G7)
    ("run_campaign.py", "_check_retired_generate_protocol_promotion"),    # registration (C5.6)
    ("run_campaign.py", "_without_retired_promotion"),                    # C5.6 materialization
}
_KEY_METHODS = ("get", "pop", "setdefault")


def _promotion_reads(path: Path) -> set:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = set()

    def _is_key(node) -> bool:
        return isinstance(node, ast.Constant) and node.value == "promotion"

    def visit(node, func):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func = node.name if func is None else func
        hit = (
            (isinstance(node, ast.Subscript) and _is_key(node.slice))
            or (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in _KEY_METHODS and node.args and _is_key(node.args[0]))
            or (isinstance(node, ast.Compare) and _is_key(node.left)
                and any(isinstance(op, (ast.In, ast.NotIn)) for op in node.ops))
        )
        if hit:
            found.add((path.name, func))
        for child in ast.iter_child_nodes(node):
            visit(child, func)

    visit(tree, None)
    return found


def test_the_scan_catches_every_access_shape(tmp_path):
    shapes = {"sub": "x['promotion']", "get": "x.get('promotion')",
              "pop": "x.pop('promotion', None)", "setdefault": "x.setdefault('promotion', {})",
              "in": "'promotion' in x", "not_in": "'promotion' not in x"}
    src = "\n".join(f"def f_{name}(x):\n    return {expr}\n" for name, expr in shapes.items())
    src += "def clean(x):\n    return x.get('symbols'), 'promotion' == x, x['windows']\n"
    (tmp_path / "m.py").write_text(src, encoding="utf-8")
    assert _promotion_reads(tmp_path / "m.py") == {("m.py", f"f_{n}") for n in shapes}


def test_only_the_gates_and_the_legacy_verdict_touch_a_promotion_block():
    found = set()
    for sub in ("workflow", "tools"):
        for path in (_SR / sub).rglob("*.py"):
            found |= _promotion_reads(path)
    assert found == _PROMOTION_READERS


def _summary(verdict, reason):
    return {"config_sha256": "x", "protocol_file": "p", "verdict": verdict,
            "verdict_reason": reason,
            "results": [{"symbol": "BTCUSDT", "window": f"w{i}", "run_id": f"r{i}",
                         "core": {"trade_count": 12, "sharpe": 0.4}} for i in range(4)],
            "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.4, "max_abs_drawdown_pct": 2.0,
                                               "min_trade_count": 12, "zero_trade_slot_pct": 0.0}},
            "hypothesis_verdict": None}


def test_trial_rows_do_not_depend_on_the_legacy_verdict(tmp_path):
    cfg = tmp_path / "c.json"
    cfg.write_text("{}", encoding="utf-8")
    rpr._record_backtest_trial("run_a", _summary("promote", "legacy"), cfg)
    rpr._record_backtest_trial("run_b", _summary(None, rp.LEGACY_VERDICT_RETIRED_REASON), cfg)
    rows = {r["trial_id"]: {k: v for k, v in r.items() if k != "trial_id"}
            for r in rpr.load_campaign_state()["trial_sharpes"]}
    assert rows["run_a"] == rows["run_b"]


def test_profitability_report_does_not_depend_on_the_legacy_verdict():
    import build_reports as br
    a = br.build_profitability_report({"protocol_result": _summary("kill", "legacy")})
    b = br.build_profitability_report({"protocol_result": _summary(None, "none")})
    assert a == b
