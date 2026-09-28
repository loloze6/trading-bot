"""
C5.6 (delivery_plan_v26_continuation.md C5.6, decision D-043) -- config-direct
runs need no promotion block.

Under orchestrator.config_direct_authoring.enabled nothing that decides reads a
protocol's `promotion` block (the grid and the profit bars decide; the legacy
top-level verdict of tools/run_protocol.py is read by nothing on that path).
So under the flag:

  * G7 (_require_pre_registered_promotion) is skipped: a generated protocol
    with no pre-registered block carries NO `promotion` key -- nothing is
    invented. A block the brief does carry is copied verbatim.
  * The D-3 guard (protocol_resolution.assert_promotion_ratified) is KEPT, at
    the launch pre-flight and at every protocol resolution: it never refused a
    missing block (promotion_is_generic(None) is False), and it still refuses
    an unratified generic block, so stale generic thresholds cannot ride along.
  * run_protocol.py with no promotion block records `verdict: null` with
    NO_PROMOTION_VERDICT_REASON instead of raising KeyError.

Flag off: G7, D-3 and the registration lint behave exactly as before (pinned
below and by the pre-existing suites). Hermetic: the conftest sandbox is ROOT,
run_loop is stubbed, no LLM, no real backtest.
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

from test_e061_c1_4_5_pauses_preflight import (  # noqa: E402
    RUN, _NON_GENERIC, _Reached, _entries, _entry, _log_text, _protocol, _queue,
    _reach_run_loop, _scaffold, _set_pre_registration)

_GENERATED_KEYS_FLAG_OFF = ["symbols", "timeframe", "windows", "holdout", "promotion"]


def _constraints(promotion=None, **over) -> dict:
    proto = {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
             "end": "2022-03-01"}
    if promotion is not None:
        proto["promotion"] = promotion
    proto.update(over)
    return {"protocol": proto}


@pytest.fixture
def config_direct(monkeypatch):
    monkeypatch.setattr(rpr, "_config_direct_authoring_enabled", lambda cfg=None: True)


def _generated_path(run_id: str = RUN) -> Path:
    return rpr.ROOT / "protocols" / f"{run_id}_generated.json"


# ---------------------------------------------------------------------------
# G7 -- the generator
# ---------------------------------------------------------------------------

def test_flag_off_g7_still_refuses_a_generated_protocol_without_promotion():
    assert rpr._config_direct_authoring_enabled() is False
    run_dir = _scaffold(constraints=_constraints())
    with pytest.raises(rpr.UngatedProtocolError, match=r"\[G7\]"):
        rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    assert not _generated_path().exists()
    with pytest.raises(rpr.UngatedProtocolError, match=r"\[G7\]"):
        camp._expected_generated_protocol(_constraints()["protocol"], RUN)


def test_flag_off_generated_protocol_is_unchanged_key_for_key_and_in_order():
    """Byte-identity of the flag-off generator: same keys, same order (promotion
    last), the brief's block verbatim."""
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


def test_config_direct_generates_a_protocol_with_no_promotion_key(config_direct):
    run_dir = _scaffold(constraints=_constraints())
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    written = json.loads(path.read_text(encoding="utf-8"))
    assert list(written) == ["symbols", "timeframe", "windows", "holdout"]
    assert camp._expected_generated_protocol(_constraints()["protocol"], RUN) == written
    run_ctx = yaml.safe_load((run_dir / "artifacts" / "run_context.yaml").read_text(encoding="utf-8"))
    assert run_ctx == {"run_type": "forced_diagnostic", "protocol": path.name}


@pytest.mark.parametrize("empty", [{}, None])
def test_config_direct_treats_an_empty_block_as_absent(config_direct, empty):
    gen = {"symbols": ["BTCUSDT"], "start": "2022-01-01", "end": "2022-03-01", "promotion": empty}
    assert "promotion" not in camp._expected_generated_protocol(gen, RUN)


def test_config_direct_copies_a_pre_registered_block_verbatim(config_direct):
    constraints = _constraints(_NON_GENERIC)
    run_dir = _scaffold(constraints=constraints)
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, constraints)
    written = json.loads(path.read_text(encoding="utf-8"))
    assert list(written) == _GENERATED_KEYS_FLAG_OFF and written["promotion"] == _NON_GENERIC


# ---------------------------------------------------------------------------
# D-3 -- kept: a missing block passes, an unratified generic block is refused
# ---------------------------------------------------------------------------

def test_config_direct_no_promotion_protocol_passes_every_resolution(config_direct, monkeypatch):
    run_dir = _scaffold(constraints=_constraints())
    assert camp._protocol_preflight(run_dir, RUN) == (None, None)  # before generation
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    assert camp._protocol_preflight(run_dir, RUN) == (None, None)  # after
    protres.assert_promotion_ratified(path)
    assert rpr._resolve_protocol_path(run_dir, RUN) == path          # 5a / data gate / backtest
    assert protres.resolve_protocol_path(run_dir, RUN, rpr.ROOT / "protocols") == path
    _queue([_entry()])
    _reach_run_loop(monkeypatch)
    with pytest.raises(_Reached):
        camp.process_once()
    assert _entries()[0]["status"] == "in_progress"


def test_config_direct_generic_block_in_the_brief_is_refused_before_run_loop(config_direct,
                                                                             monkeypatch):
    generic = dict(rpr._GENERIC_PROMOTION)
    run_dir = _scaffold(constraints=_constraints(generic))
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
    assert regeneration is None
    assert "[G7/D-3]" in refusal and "C5.6" in refusal and "delete that block" in refusal
    _queue([_entry()])
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: pytest.fail("run_loop reached"))
    assert camp.process_once() is False
    assert _entries()[0]["status"] == "paused:protocol_promotion_unratified"
    # generated anyway (e.g. by hand): every resolution refuses it
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(generic))
    assert json.loads(path.read_text(encoding="utf-8"))["promotion"] == generic
    with pytest.raises(rpr.UngatedProtocolError, match="ratified_by"):
        rpr._resolve_protocol_path(run_dir, RUN)


def test_flag_off_generic_refusal_message_is_unchanged():
    run_dir = _scaffold(constraints=_constraints(dict(rpr._GENERIC_PROMOTION)))
    refusal, _ = camp._protocol_preflight(run_dir, RUN)
    assert refusal.endswith("pre_registration.yaml's machine_constraints.protocol.promotion")
    assert "C5.6" not in refusal


@pytest.mark.parametrize("flag_on", [False, True])
def test_pinned_unratified_generic_protocol_is_refused_with_the_flag_on_or_off(monkeypatch,
                                                                               flag_on):
    if flag_on:
        monkeypatch.setattr(rpr, "_config_direct_authoring_enabled", lambda cfg=None: True)
    _protocol("generic.json", dict(rpr._GENERIC_PROMOTION))
    run_dir = _scaffold(constraints={"protocol_ref": "protocols/generic.json"})
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
    assert regeneration is None and "[G7/D-3]" in refusal and "generic.json" in refusal


def test_config_direct_dropping_a_block_before_spend_regenerates_without_it(config_direct,
                                                                            monkeypatch):
    run_dir = _scaffold(constraints=_constraints(_NON_GENERIC))
    path = rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints(_NON_GENERIC))
    _set_pre_registration(run_dir, _constraints())
    refusal, regeneration = camp._protocol_preflight(run_dir, RUN)
    assert refusal is None and regeneration["differing"] == ["promotion"]
    _queue([_entry()])
    _reach_run_loop(monkeypatch)
    with pytest.raises(_Reached):
        camp.process_once()
    assert "promotion" not in json.loads(path.read_text(encoding="utf-8"))
    assert "regenerated before any spend -- field(s) ['promotion']" in _log_text()


# ---------------------------------------------------------------------------
# run_protocol.py -- the legacy top-level verdict with no promotion block
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


def _run_protocol(monkeypatch, tmp_path, promotion, *extra) -> dict:
    monkeypatch.setattr(rp, "run_backtest", _StubBacktest(tmp_path / "sandbox_runs"))
    monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
    protocol = {"symbols": ["BTCUSDT"],
                "windows": [{"label": f"w{i}", "test": {"start": f"2022-0{i}-01",
                                                        "end": f"2022-0{i}-02"}}
                            for i in (1, 2)]}
    if promotion is not None:
        protocol["promotion"] = promotion
    (tmp_path / "protocol.json").write_text(json.dumps(protocol), encoding="utf-8")
    (tmp_path / "config.json").write_text(json.dumps({"dummy": True}), encoding="utf-8")
    out = tmp_path / "out"
    monkeypatch.setattr(sys, "argv", ["run_protocol.py", str(tmp_path / "config.json"),
                                      str(tmp_path / "protocol.json"), "--out-dir", str(out),
                                      *extra])
    rp.main()
    return json.loads((out / "protocol_summary.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("extra", [(), ("--diagnostics-only",)])
def test_run_protocol_without_promotion_records_a_null_verdict(monkeypatch, tmp_path, extra):
    summary = _run_protocol(monkeypatch, tmp_path, None, *extra)
    assert summary["verdict"] is None
    assert summary["verdict_reason"] == rp.NO_PROMOTION_VERDICT_REASON
    # everything config-direct consumers read is still there
    assert summary["per_symbol_summary"]["BTCUSDT"]["median_sharpe"] == 0.4
    assert len(summary["results"]) == 2
    if extra:
        assert summary["hypothesis_verdict"]["diagnostics"]["median_cost_drag_pct"] == 40.0


def test_run_protocol_with_promotion_is_unchanged(monkeypatch, tmp_path):
    summary = _run_protocol(monkeypatch, tmp_path, {
        "median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 25,
        "min_trade_count_gte": 1, "kill_median_sharpe_lt": -1})
    assert summary["verdict"] == "promote"
    assert summary["verdict_reason"] == ("BTCUSDT: median_sharpe=0.400>0 max_dd=2.0%<30 "
                                         "min_trades=12>=20")


# ---------------------------------------------------------------------------
# Consumers: nothing on the config-direct path reads the promotion block or
# the legacy top-level verdict
# ---------------------------------------------------------------------------

# Every function in workflow/ and tools/ that reads a `promotion` key
# (x["promotion"] or x.get("promotion")). All are the gates themselves plus the
# legacy verdict; a new reader must be added here deliberately.
_PROMOTION_READERS = {
    ("run_protocol.py", "main"),                                         # legacy verdict
    ("protocol_resolution.py", "assert_promotion_ratified"),             # D-3
    ("run_phase1_research.py", "_assert_promotion_ratified"),            # D-3 (orchestrator copy)
    ("run_phase1_research.py", "_require_pre_registered_promotion"),     # G7
    ("run_phase1_research.py", "_generated_protocol_promotion"),         # C5.6 generator
    ("run_campaign.py", "_generated_protocol_plan"),                     # D-3 pre-flight
    ("run_campaign.py", "_check_generate_protocol_promotion_not_generic"),  # registration lint
}


def _promotion_reads(path: Path) -> set:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = set()

    def visit(node, func):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func = node.name if func is None else func
        is_sub = (isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant)
                  and node.slice.value == "promotion")
        is_get = (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                  and node.func.attr == "get" and node.args
                  and isinstance(node.args[0], ast.Constant) and node.args[0].value == "promotion")
        if is_sub or is_get:
            found.add((path.name, func))
        for child in ast.iter_child_nodes(node):
            visit(child, func)

    visit(tree, None)
    return found


def test_only_the_gates_and_the_legacy_verdict_read_a_promotion_block():
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
    rpr._record_backtest_trial("run_b", _summary(None, rp.NO_PROMOTION_VERDICT_REASON), cfg)
    rows = {r["trial_id"]: {k: v for k, v in r.items() if k != "trial_id"}
            for r in rpr.load_campaign_state()["trial_sharpes"]}
    assert rows["run_a"] == rows["run_b"]


def test_profitability_report_does_not_depend_on_the_legacy_verdict():
    import build_reports as br
    a = br.build_profitability_report({"protocol_result": _summary("kill", "legacy")})
    b = br.build_profitability_report({"protocol_result": _summary(None, "none")})
    assert a == b
