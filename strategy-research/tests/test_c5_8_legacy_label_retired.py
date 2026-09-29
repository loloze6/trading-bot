"""
C5.8 (review finding C13; engineering/C5_8_FINDINGS.md Q4; operator decision
D-050 answering OQ1 yes): under _promotion_retired_enabled (config_direct_authoring
AND verdict_routing_retired), the variant loop of run_tool_worker("protocol_execution")

  * does not write artifacts/pass_rule_evaluation.yaml (C7), and deletes a stale one
    left by an earlier attempt of the run;
  * passes build_reports(legacy_verdict_retired=True), which drops from
    reports/profitability.yaml the legacy label -- verdict/verdict_reason, the three
    route keys of overall.diagnostics and the four route/rationale keys of every
    per_window core and per_symbol row -- and keeps every number.

Gate off, everything is exactly as before (the C7 file, the build_reports call,
the report). The trial ledger is identical row for row with the gate on or off:
that is the trial-accounting proof. The single-run branch is not touched.

Sandboxing: tests/conftest.py's autouse _sandbox_by_default (rpr.ROOT is a
per-test tmp sandbox), as in test_e033_slice4a_variant_loop.py.
"""
import asyncio
import copy
import shutil
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import build_reports as br  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402

# The D-050 key set, spelled out here (not imported), so this file pins it.
VERDICT_KEYS = ("verdict", "verdict_reason")
DIAG_ROUTE_KEYS = ("post_backtest_route_real", "post_backtest_route_real_tied",
                   "cost_dominated_real")
CORE_ROUTE_KEYS = ("post_backtest_route", "post_backtest_route_rationale",
                   "post_backtest_route_real", "post_backtest_route_real_rationale")

_COST_CHECK = {"estimated_gross_edge_bps_per_trade": 4.2, "cost_bps_per_trade": 10.0,
               "edge_to_cost_ratio": 0.42, "safety_factor_required": 2.0, "pass": False}
_PRE_REG = {"pass_rule": {"criteria": [{"id": "c1", "source": "grid", "reducer": "unanimous"}]}}
_FAILING_VARIANT = "broken"
_RUN = "run_960"
_REAL_BUILD_REPORTS = br.build_reports  # captured before any spy


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _set_flags(orchestrator: dict) -> None:
    config_dir = rpr.ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"orchestrator": orchestrator}, f)


def _retire(monkeypatch) -> None:
    """The gate's two flag readers on (the C5.6 test's `retired` fixture): the real
    _promotion_retired_enabled / _legacy_verdict_args then read True."""
    monkeypatch.setattr(rpr, "_config_direct_authoring_enabled", lambda cfg=None: True)
    monkeypatch.setattr(rpr, "_verdict_routing_retired_enabled", lambda cfg=None: True)
    assert rpr._promotion_retired_enabled() is True


def _summary_for(vid: str, sharpe: float = 0.3) -> dict:
    """A protocol summary carrying both legacy label families, with numbers."""
    results = [{
        "symbol": "BTCUSDT", "window": f"w{i}", "run_id": f"{vid}_w{i}",
        "core": {"trade_count": 12 + i, "sharpe": sharpe, "net_return_pct": 0.4,
                 "forecast_return_corr": 0.02, "forecast_return_corr_pvalue": 0.3,
                 "post_backtest_cost_check": dict(_COST_CHECK),
                 "post_backtest_cost_check_real": dict(_COST_CHECK),
                 "post_backtest_route": "kill_cost_hurdle",
                 "post_backtest_route_rationale": "Fix: wider threshold or longer holding",
                 "post_backtest_route_real": "refine_inverted_ic",
                 "post_backtest_route_real_rationale": "flip polarity"},
        "per_regime": {"trending": {"bar_count": 10, "avg_forecast": 0.1}},
    } for i in range(2)]
    return {
        "protocol_run_id": f"stub_{vid}", "config_sha256": f"sha-{vid}", "protocol_file": "p",
        "verdict": "kill", "verdict_reason": "legacy top-level",
        "results": results,
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": sharpe, "max_abs_drawdown_pct": 2.0,
                                           "min_trade_count": 12, "zero_trade_slot_pct": 0.0}},
        "hypothesis_verdict": {
            "verdict": "kill", "verdict_reason": "legacy decision rules",
            "diagnostics": {"median_cost_drag_pct": 40.0, "median_gross_pnl": 1.5,
                            "median_forecast_return_corr": 0.02, "below_floor_pct": 0.0,
                            "per_trade_expectancy_bps": {"mean": 3.0, "se": 1.0,
                                                         "t_stat": 3.0, "n": 25},
                            "post_backtest_route_real": "refine_inverted_ic",
                            "post_backtest_route_real_tied": False,
                            "cost_dominated_real": False},
        },
    }


# ---------------------------------------------------------------------------
# The orchestrator's variant loop
# ---------------------------------------------------------------------------

_SHARPES = {"base": 0.3, "design": 0.1, "asset": -0.2}


def _scaffold_variant_run(run_id: str = _RUN) -> Path:
    _write_protocol(rpr.ROOT, "c5_8.json")
    run_dir = _minimal_run(rpr.ROOT, run_id)
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": "protocols/c5_8.json"})
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", _PRE_REG)
    variants_dir = run_dir / "artifacts" / "variants"
    index = {}
    for vid in (*_SHARPES, _FAILING_VARIANT):
        (variants_dir / vid).mkdir(parents=True, exist_ok=True)
        (variants_dir / vid / "strategy_config.json").write_text(
            rpr.json.dumps({"variant": vid}), encoding="utf-8")
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
    rpr.save_yaml(variants_dir / "index.yaml", {"variants": index})
    return run_dir


def _fake_subprocess_run(cmd, *args, **kwargs):
    vid = Path(cmd[2]).parent.name
    out_dir = Path(cmd[cmd.index("--out-dir") + 1])
    out_dir.mkdir(parents=True, exist_ok=True)

    class _Result:
        stdout = ""
        stderr = ""
        returncode = 0
    if vid == _FAILING_VARIANT:  # a data-touching crash: a backtest_failed row
        _Result.returncode = 1
        _Result.stderr = "Traceback (most recent call last):\nRuntimeError: injected\n"
        return _Result()
    (out_dir / "protocol_summary.json").write_text(
        rpr.json.dumps(_summary_for(vid, _SHARPES[vid])), encoding="utf-8")
    return _Result()


def _run_variant_loop(monkeypatch, run_id: str = _RUN) -> list:
    """Runs the variant loop with a build_reports spy (the real function is still
    called). Returns the spied kwargs of every build_reports call."""
    calls = []
    real = _REAL_BUILD_REPORTS

    def _spy(run_dir, *args, **kwargs):
        calls.append(dict(kwargs))
        return real(run_dir, *args, **kwargs)
    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)
    monkeypatch.setattr(br, "build_reports", _spy)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))
    return calls


def _ledger() -> list:
    return copy.deepcopy(rpr.load_campaign_state().get("trial_sharpes") or [])


_LOOP_FLAGS = {"config_direct_authoring": {"enabled": True}, "variant_loop": {"enabled": True},
               "category_reports": {"enabled": True}}


def test_gate_off_variant_loop_writes_c7_and_calls_build_reports_unchanged(monkeypatch):
    """config_direct + variant_loop, verdict routing live: the C7 file is written
    with exactly today's content (the evaluator on the base summary), the
    build_reports call has exactly the pre-C5.8 kwargs, and the report keeps the
    legacy label."""
    _set_flags(_LOOP_FLAGS)
    assert rpr._promotion_retired_enabled() is False
    run_dir = _scaffold_variant_run()
    calls = _run_variant_loop(monkeypatch)

    written = rpr.load_yaml(run_dir / "artifacts" / "pass_rule_evaluation.yaml")
    assert written.pop("evaluated_at")
    expected = vce.evaluate_pass_rule_criteria(_summary_for("base", _SHARPES["base"]),
                                               _PRE_REG, {})
    expected.pop("evaluated_at", None)
    expected["evaluator_version"] = 2
    assert written == yaml.safe_load(yaml.safe_dump(expected))

    assert [set(c) for c in calls] == [{"write", "variants", "failed_variants",
                                       "untested_variants"}]
    prof = rpr.load_yaml(run_dir / "artifacts" / "reports" / "profitability.yaml")
    overall = prof["variants"]["base"]["slices"]["overall"]
    assert overall["verdict"] == "kill" and overall["verdict_reason"] == "legacy decision rules"
    assert set(DIAG_ROUTE_KEYS) <= set(overall["diagnostics"])
    assert set(CORE_ROUTE_KEYS) <= set(prof["variants"]["base"]["slices"]["per_window"][0]["core"])


def test_gate_off_never_deletes_an_existing_c7_file(monkeypatch):
    """Gate off, nothing is deleted: with C7 raising, a file already on disk is
    left exactly as it was (the pre-C5.8 behaviour)."""
    _set_flags(_LOOP_FLAGS)
    run_dir = _scaffold_variant_run()
    planted = run_dir / "artifacts" / "pass_rule_evaluation.yaml"
    planted.write_text("result: PASS\nplanted: earlier attempt\n", encoding="utf-8")
    before = planted.read_bytes()

    def _raise(*a, **k):
        raise RuntimeError("simulated C7 crash")
    monkeypatch.setattr(vce, "evaluate_pass_rule_criteria", _raise)
    _run_variant_loop(monkeypatch)
    assert planted.read_bytes() == before


def test_gate_on_skips_c7_clears_a_stale_file_strips_the_report_and_keeps_every_trial_row(
        monkeypatch, capsys):
    """The same stubbed variants (three graded, one data-touching crash), gate off
    then gate on, on the same run id: the gate-on attempt writes no C7 file and
    removes a stale one, passes legacy_verdict_retired=True, writes a stripped
    profitability report -- and records a trial ledger equal to the gate-off
    ledger row for row (rows carry no timestamp)."""
    _set_flags(_LOOP_FLAGS)
    run_dir = _scaffold_variant_run()
    _run_variant_loop(monkeypatch)
    ledger_off = _ledger()
    assert sorted((r["trial_id"], r["source"]) for r in ledger_off) == [
        (f"{_RUN}:asset", "backtest"), (f"{_RUN}:base", "backtest"),
        (f"{_RUN}:{_FAILING_VARIANT}", "backtest_failed"), (f"{_RUN}:design", "backtest")]
    assert (run_dir / "artifacts" / "pass_rule_evaluation.yaml").exists()

    # a fresh run dir and an empty ledger, then the same run with the gate on
    shutil.rmtree(run_dir)
    state = rpr.load_campaign_state()
    state["trial_sharpes"] = []
    rpr._save_campaign_state(state)
    run_dir = _scaffold_variant_run()
    stale = run_dir / "artifacts" / "pass_rule_evaluation.yaml"
    stale.write_text("result: PASS\nhypothesis_verdict: promote\n", encoding="utf-8")
    _retire(monkeypatch)
    capsys.readouterr()
    calls = _run_variant_loop(monkeypatch)
    out = capsys.readouterr().out

    assert not stale.exists()
    assert "cleared previous attempt's pass_rule_evaluation.yaml" in out
    assert "[C5.8] pass_rule_evaluation.yaml not written" in out
    assert "[C7]" not in out
    assert [c.get("legacy_verdict_retired") for c in calls] == [True]
    assert set(calls[0]) == {"write", "variants", "failed_variants", "untested_variants",
                             "legacy_verdict_retired"}

    assert _ledger() == ledger_off

    prof = rpr.load_yaml(run_dir / "artifacts" / "reports" / "profitability.yaml")
    assert sorted(prof["variants"]) == sorted(_SHARPES)
    for vid, block in prof["variants"].items():
        slices = block["slices"]
        assert not set(VERDICT_KEYS) & set(slices["overall"]), vid
        assert not set(DIAG_ROUTE_KEYS) & set(slices["overall"]["diagnostics"]), vid
        assert slices["overall"]["diagnostics"]["median_cost_drag_pct"] == 40.0
        for row in slices["per_window"]:
            assert not set(CORE_ROUTE_KEYS) & set(row["core"]), vid
            assert row["core"]["post_backtest_cost_check_real"] == _COST_CHECK
        for row in slices["per_symbol"]["BTCUSDT"]:
            assert not set(CORE_ROUTE_KEYS) & set(row), vid
            assert row["forecast_return_corr"] == 0.02
    # the per-variant protocol results themselves are untouched
    source = rpr.load_yaml(run_dir / "artifacts" / "variants" / "base" / "protocol_result.yaml")
    assert source["hypothesis_verdict"]["verdict"] == "kill"
    assert set(CORE_ROUTE_KEYS) <= set(source["results"][0]["core"])


def test_single_run_branch_untouched_under_the_gate(monkeypatch):
    """Gate on with variant_loop off: the single-run branch still writes the C7
    file (W2) and calls build_reports exactly as before -- its C7 raise is part of
    the pinned accounting contract (test_trial_accounting_characterization)."""
    _set_flags({"category_reports": {"enabled": True}})
    _retire(monkeypatch)
    assert rpr._variant_loop_enabled() is False
    _write_protocol(rpr.ROOT, "single.json")
    run_dir = _minimal_run(rpr.ROOT, "run_970")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, "run_970", {"protocol_ref": "protocols/single.json"})

    def _fake_single(cmd, *args, **kwargs):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps(_summary_for("single")), encoding="utf-8")

        class _Ok:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Ok()

    calls = []
    real = _REAL_BUILD_REPORTS

    def _spy(run_dir_, *args, **kwargs):
        calls.append(dict(kwargs))
        return real(run_dir_, *args, **kwargs)
    monkeypatch.setattr(rpr.subprocess, "run", _fake_single)
    monkeypatch.setattr(br, "build_reports", _spy)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_970"))

    assert (run_dir / "artifacts" / "pass_rule_evaluation.yaml").exists()
    assert calls == [{"write": True}]
    prof = rpr.load_yaml(run_dir / "artifacts" / "reports" / "profitability.yaml")
    assert prof["slices"]["overall"]["verdict"] == "kill"
    rows = rpr.load_campaign_state()["trial_sharpes"]
    assert [(r["trial_id"], r["source"]) for r in rows] == [("run_970", "backtest")]


# ---------------------------------------------------------------------------
# build_reports / _strip_legacy_verdict_fields
# ---------------------------------------------------------------------------

def _builder_run(tmp_path: Path, shape: str) -> tuple:
    run_dir = tmp_path / "run_980"
    if shape == "single":
        (run_dir / "artifacts").mkdir(parents=True)
        (run_dir / "artifacts" / "protocol_result.yaml").write_text(
            yaml.safe_dump(_summary_for("single")), encoding="utf-8")
        return run_dir, {}
    variants = {}
    for vid in ("base", "design"):
        (run_dir / "artifacts" / "variants" / vid).mkdir(parents=True)
        (run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml").write_text(
            yaml.safe_dump(_summary_for(vid)), encoding="utf-8")
        variants[vid] = {"kind": vid, "symbol": "BTCUSDT", "status": "graded"}
    return run_dir, {"variants": variants, "failed_variants": {"x": "backtest_failed: boom"}}


def _no_timestamps(reports: dict) -> dict:
    return {name: {k: v for k, v in r.items() if k != "generated_at"}
            for name, r in reports.items()}


def _all_slices(report: dict) -> list:
    if "slices" in report:
        return [report["slices"]]
    return [block["slices"] for block in report["variants"].values()]


def _expected_stripped(report: dict) -> dict:
    """Independent of the helper: `del` raises if a named key was not there, so
    the comparison below cannot pass vacuously."""
    r = copy.deepcopy(report)
    for s in _all_slices(r):
        for k in VERDICT_KEYS:
            del s["overall"][k]
        for k in DIAG_ROUTE_KEYS:
            del s["overall"]["diagnostics"][k]
        for row in s["per_window"]:
            for k in CORE_ROUTE_KEYS:
                del row["core"][k]
        for rows in s["per_symbol"].values():
            for row in rows:
                for k in CORE_ROUTE_KEYS:
                    del row[k]
    return r


@pytest.mark.parametrize("shape", ["single", "variants"])
def test_builder_default_equals_explicit_false_and_keeps_the_label(tmp_path, shape):
    run_dir, kw = _builder_run(tmp_path, shape)
    default = _no_timestamps(br.build_reports(run_dir, write=False, **kw))
    explicit = _no_timestamps(br.build_reports(run_dir, write=False, legacy_verdict_retired=False,
                                               **kw))
    assert default == explicit
    for s in _all_slices(default["profitability"]):
        assert s["overall"]["verdict"] == "kill"
        assert s["overall"]["verdict_reason"] == "legacy decision rules"
        assert set(DIAG_ROUTE_KEYS) <= set(s["overall"]["diagnostics"])
        assert all(set(CORE_ROUTE_KEYS) <= set(row["core"]) for row in s["per_window"])


@pytest.mark.parametrize("shape", ["single", "variants"])
def test_builder_gate_on_drops_exactly_the_named_keys(tmp_path, shape):
    run_dir, kw = _builder_run(tmp_path, shape)
    off = _no_timestamps(br.build_reports(run_dir, write=False, **kw))
    on = _no_timestamps(br.build_reports(run_dir, write=True, legacy_verdict_retired=True, **kw))
    assert on["profitability"] == _expected_stripped(off["profitability"])
    for name in br.REPORT_CATEGORIES:
        if name != "profitability":
            assert on[name] == off[name], name
    # the written file is the stripped one, with every number kept
    written = yaml.safe_load((run_dir / "artifacts" / "reports" / "profitability.yaml")
                             .read_text(encoding="utf-8"))
    for s in _all_slices(written):
        assert s["overall"]["diagnostics"]["median_forecast_return_corr"] == 0.02
        assert s["overall"]["diagnostics"]["per_trade_expectancy_bps"]["mean"] == 3.0
        for row in s["per_window"]:
            assert not set(CORE_ROUTE_KEYS) & set(row["core"])
            assert row["core"]["post_backtest_cost_check"] == _COST_CHECK
            assert row["core"]["post_backtest_cost_check_real"] == _COST_CHECK
            assert row["core"]["forecast_return_corr_pvalue"] == 0.3
        assert s["per_regime"]["trending"][0]["bar_count"] == 10


def test_strip_helper_is_pure_and_leaves_unavailable_slices_alone(tmp_path):
    run_dir, kw = _builder_run(tmp_path, "variants")
    report = br.build_reports(run_dir, write=False, **kw)["profitability"]
    snapshot = copy.deepcopy(report)
    stripped = br._strip_legacy_verdict_fields(report)
    assert report == snapshot, "the input report was mutated"
    assert stripped != report

    unavailable = br.build_profitability_report({"protocol_result": {"results": []}})
    assert unavailable["slices"]["overall"]["unavailable"] is True
    assert br._strip_legacy_verdict_fields(unavailable) == unavailable
