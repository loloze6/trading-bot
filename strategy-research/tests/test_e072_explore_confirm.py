"""
E-072 (P-CUL-80, D-080): ideas are confirmed on data the proposer never saw,
behind orchestrator.explore_confirm.enabled (tools/explore_confirm.py).

A synthetic run: 2 coins x 6 four-month windows (2022-01 .. 2023-09), two
graded variants. Every number of a CONFIRMATION window carries the sentinel
919191 and every all-window aggregate the sentinel 828282, so a reader input
that leaks either one is caught by a plain text search. The prices are a
momentum process on the exploration windows and, per test, momentum or
reversal on the confirmation windows, so a pure side finding's sign on the
confirmation windows is known in advance.

Sections:
  1. The flag.
  2. Flag off: byte-identical (handoff, prompts, files, summary, build_reports).
  3. The split.
  4. The readers' inputs carry no confirmation-window number.
  5. Confirmation: pure in-run (held / not held), block pending, looks counted,
     a pending finding resolved by the run built from it.
  6. Old runs and inputs still load.

No LLM: _invoke_reader_llm is replaced wherever it is reached.
"""
import copy
import csv
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import explore_confirm as ec  # noqa: E402
import build_reports as br  # noqa: E402
import claim_measure as cmeas  # noqa: E402
import reader_findings as rf  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import protocol_resolution as pres  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    RUN_ID, _seed_run, _set_orchestrator, _fake_llm)
from test_e068_5_readers_v3 import V3_ON, _seed_v3_docs, _reading, _fenced, _scores  # noqa: E402

EC_ON = {**V3_ON, "variant_loop": {"enabled": True}, "explore_confirm": {"enabled": True}}
EC_OFF = {**V3_ON, "variant_loop": {"enabled": True}}
WINDOWS = [("2022-01", "2022-01-01", "2022-04-30"), ("2022-05", "2022-05-01", "2022-08-31"),
           ("2022-09", "2022-09-01", "2022-12-31"), ("2023-01", "2023-01-01", "2023-04-30"),
           ("2023-05", "2023-05-01", "2023-08-31"), ("2023-09", "2023-09-01", "2023-12-31")]
EXPL = ["2022-01", "2022-05", "2022-09"]
CONF = ["2023-01", "2023-05", "2023-09"]
SYMBOLS = ["BTCUSD", "ETHUSD"]
VARIANTS = ["base", "design"]
SENT_CONF = 919191.0     # every confirmation-window number
SENT_POOL = 828282.0     # every all-window aggregate
SENTINELS = ("919191", "828282")
N_BARS = 110


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _pure_claim() -> dict:
    return {"statement": "After an up day the next day is higher.", "kind": "event_behaviour",
            "tests": [{"name": "up_day_followthrough",
                       "selector": {"kind": "event", "field": "past_return", "bars": 1,
                                    "op": ">", "value": 0.0},
                       "outcome": {"kind": "fwd_return", "horizons": [1]},
                       "baseline": {"kind": "complement"}, "statistic": "mean_diff",
                       "direction": "greater", "floor": {"min_events": 10}}],
            "pass_if": "effect above zero", "fail_if": "effect at or below zero",
            "rationale": "seen on the exploration windows"}


def _block_claim() -> dict:
    return {"statement": "The forecast ranks next-day returns.", "kind": "direction_forecast",
            "tests": [{"name": "forecast_rank", "selector": {"kind": "all"},
                       "outcome": {"kind": "fwd_return", "horizons": [1]},
                       "statistic": "rank_ic", "direction": "greater",
                       "floor": {"min_events": 10}}],
            "pass_if": "rank IC above zero", "fail_if": "rank IC at or below zero",
            "rationale": "the forecast read on the exploration windows"}


def _bars_rows(start: str, sign: float, seed: int, conf: bool) -> list:
    """Daily bars: r[t+1] = 0.004 * sign * sign(r[t]) + noise (momentum when
    sign is +1, reversal when -1). A confirmation window's component value
    carries the sentinel."""
    import pandas as pd
    rng = np.random.default_rng(seed)
    ts = pd.date_range(start, periods=N_BARS, freq="1D", tz="UTC")
    r = np.zeros(N_BARS)
    r[0] = 0.01
    for t in range(N_BARS - 1):
        r[t + 1] = 0.004 * sign * np.sign(r[t]) + rng.normal(0.0, 0.01)
    close = 100.0 * np.cumprod(1.0 + r)
    rows = []
    for t in range(N_BARS):
        rows.append({"timestamp": ts[t].strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "high": f"{close[t] * 1.01:.6f}", "low": f"{close[t] * 0.99:.6f}",
                     "close": f"{close[t]:.6f}", "forecast": f"{r[t] * 100:.6f}",
                     "regime": "unknown" if t < N_BARS - 1 else "",
                     "debug_info.components.c1.value":
                         f"{SENT_CONF:.1f}" if conf else f"{0.5 + t / 1000:.4f}"})
    return rows


def _write_csv(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def _save(path: Path, doc) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


PRE_REG = {"pass_rule": {"criteria": [
    {"id": "c_win", "metric": "sharpe", "source": "window", "reducer": "median",
     "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 1}},
    {"id": "c_pool", "metric": "realized_edge_to_cost_ratio", "source": "pooled",
     "comparator": ">", "threshold": 2.2}]}}


def _eras_holdout():
    return pres.load_policy_eras(rpr._DATA_POLICY_PATH), rpr._load_holdout_range()[0]


def _make_run(run_dir: Path, conf_sign: float = -1.0, windows=WINDOWS, card_claim=None) -> None:
    """The synthetic run's backtest output (no backtest is run)."""
    arts = run_dir / "artifacts"
    arts.mkdir(parents=True, exist_ok=True)
    conf_labels = {w[0] for w in windows[len(windows) // 2:]}
    (run_dir / "protocol.json").write_text(json.dumps({
        "symbols": SYMBOLS, "timeframe": "1d",
        "windows": [{"label": l, "test": {"start": s, "end": e}} for l, s, e in windows]}),
        encoding="utf-8")
    for vi, vid in enumerate(VARIANTS):
        results, trades = [], []
        for si, sym in enumerate(SYMBOLS):
            for wi, (label, start, _end) in enumerate(windows):
                conf = label in conf_labels
                rid = f"{vid}_{sym}_{label}"
                v = SENT_CONF if conf else round(0.1 * (wi + 1) + 0.01 * si, 4)
                results.append({"symbol": sym, "window": label, "run_id": rid,
                                "core": {"sharpe": v, "net_return_pct": v, "trade_count": 20,
                                         "forecast_return_corr": v,
                                         "forecast_return_corr_pvalue": 0.5},
                                "per_regime": {"unknown": {"return_pct": v}},
                                "regime_validity": {"unknown": {"n_bars": N_BARS, "x": v}}})
                _write_csv(run_dir / "variants" / vid / "results" / rid / "bars.csv",
                           _bars_rows(start, conf_sign if conf else 1.0,
                                      seed=1000 * vi + 100 * si + wi, conf=conf))
                for k in range(3):
                    trades.append({"symbol": sym, "window": label, "regime_at_entry": "unknown",
                                   "trade_id": f"{rid}-{k}", "pnl_pct": v, "bars_held": 2})
        pr = {"results": results,
              "hypothesis_verdict": {"verdict": "x", "diagnostics": {
                  "median_forecast_return_corr": SENT_POOL, "median_sharpe": SENT_POOL}},
              "trade_diagnostics_summary": {"realized_edge_to_cost_ratio": SENT_POOL,
                                            "n_trades": 828282},
              "per_symbol_summary": {s: {"sharpe": SENT_POOL} for s in SYMBOLS}}
        _save(arts / "variants" / vid / "protocol_result.yaml", pr)
        (run_dir / "variants" / vid).mkdir(parents=True, exist_ok=True)
        (run_dir / "variants" / vid / "trade_diagnostics.json").write_text(
            json.dumps({"trades": trades}), encoding="utf-8")
    _save(arts / "pre_registration.yaml", PRE_REG)
    _save(arts / "hypothesis_card.yaml", {"hypothesis_id": "H-TEST-1",
                                          "claim": card_claim or _pure_claim()})
    eras, holdout = _eras_holdout()
    card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
    tests = card["claim"]["tests"]
    variants = {}
    for vid in VARIANTS:
        doc = cmeas.measure_variant(run_dir, vid, tests, eras, holdout)
        _save(arts / "variants" / vid / cmeas.VARIANT_FILE, doc)
        variants[vid] = doc
    import claim_card as cc
    status = cc.status_of(cc.check_claim(card["claim"]), None, [])
    _save(arts / cmeas.RUN_FILE, cmeas.run_doc(run_dir.name, status, variants))
    prs = _prs(run_dir)
    grid = vce.evaluate_grid(prs, PRE_REG, None, {})
    _save(arts / "grid_evaluation.yaml", grid)
    br.build_reports(run_dir, write=True, variants=_meta())


def _prs(run_dir: Path) -> dict:
    return {vid: yaml.safe_load((run_dir / "artifacts" / "variants" / vid
                                 / "protocol_result.yaml").read_text(encoding="utf-8"))
            for vid in VARIANTS}


def _meta() -> dict:
    return {vid: {"kind": None, "symbol": None, "status": "graded"} for vid in VARIANTS}


def _ec_run(monkeypatch, flags=EC_ON, conf_sign=-1.0, run_id=RUN_ID, windows=WINDOWS,
            card_claim=None) -> Path:
    _set_orchestrator(flags)
    monkeypatch.chdir(SR_ROOT)
    _seed_v3_docs()
    dst = rpr.ROOT / "workflow_artifacts" / "skills" / "readers_v3" / "EXPLORATION.md"
    shutil.copyfile(SR_ROOT / "workflow_artifacts" / "skills" / "readers_v3" / "EXPLORATION.md",
                    dst)
    run_dir = _seed_run(run_id)
    _make_run(run_dir, conf_sign, windows=windows, card_claim=card_claim)
    monkeypatch.setattr(rpr, "_resolve_protocol_path",
                        lambda rd, rid: Path(rd) / "protocol.json")
    return run_dir


def _protocol_execution_part(run_dir: Path, run_id: str = RUN_ID) -> None:
    """What protocol_execution does under the flag: the split at entry, the
    readers' copies after the reports."""
    rpr._prepare_explore_confirm(run_dir, run_id)
    rpr._write_exploration_views(run_dir, run_id, _prs(run_dir), _meta(),
                                 pre_registration=PRE_REG)


def _readings_llm(prompts: list, sides: dict | None = None):
    sides = sides or {}

    async def _llm(prompt):
        prompts.append(prompt)
        cat = next(c for c in REPORT_CATEGORIES if f"reader_category: {c}\n" in prompt)
        return (_fenced(_reading(cat, sides=sides.get(cat, []))),
                {"usage": {}, "cost_usd": 0.0, "num_turns": 1})
    return _llm


def _sides():
    return {"trade_efficiency": [{"proposal_id": f"trade_efficiency-{RUN_ID}-1",
                                  "claim": _pure_claim(), "evidence": ["exploration only"],
                                  "scores": _scores()}],
            "forecast_power": [{"proposal_id": f"forecast_power-{RUN_ID}-1",
                                "claim": _block_claim(), "evidence": ["exploration only"],
                                "scores": _scores()}]}


def _text_of_tree(root: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(root.rglob("*")) if p.is_file())


def _assert_no_leak(text: str) -> None:
    """No sentinel, no confirmation label, and no decimal number as large as a
    sentinel (an aggregate that mixed one in would be at least ~1e5)."""
    import re
    for s in SENTINELS + tuple(CONF):
        assert s not in text, s
    big = [m for m in re.findall(r"(?<![\w.])(\d{6,})\.\d", text) if float(m) >= 100_000]
    assert not big, big[:5]


# ---------------------------------------------------------------------------
# 1. The flag
# ---------------------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(EC_OFF)
    assert rpr._explore_confirm_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(
        encoding="utf-8"))
    assert shipped["orchestrator"]["explore_confirm"]["enabled"] is False


def test_flag_on_with_its_dependencies():
    _set_orchestrator(EC_ON)
    assert rpr._explore_confirm_enabled() is True


@pytest.mark.parametrize("missing", ["reader_findings", "variant_loop"])
def test_flag_on_without_a_dependency_raises(missing):
    flags = copy.deepcopy(EC_ON)
    flags[missing] = {"enabled": False}
    _set_orchestrator(flags)
    with pytest.raises(ValueError, match=f"orchestrator.{missing}.enabled=true"):
        rpr._explore_confirm_enabled()


@pytest.mark.parametrize("bad", ["true", "false", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**EC_OFF, "explore_confirm": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._explore_confirm_enabled()


def test_the_flag_is_registered_everywhere():
    assert camp._flag_readers()["explore_confirm"] is rpr._explore_confirm_enabled
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(
        encoding="utf-8"))
    rows = [r for r in reg["flags"] if r.get("name") == "explore_confirm"]
    assert len(rows) == 1 and rows[0]["config_key"] == "orchestrator.explore_confirm.enabled"
    from test_e061_end_to_end_wiring import TARGET_FLAGS
    assert TARGET_FLAGS["explore_confirm"] is False


# ---------------------------------------------------------------------------
# 2. Flag off: byte-identical
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_flag_off_handoff_is_exactly_slice_5s(cat, monkeypatch):
    """explore_confirm absent and explicitly false give the same v3 handoff."""
    run_dir = _ec_run(monkeypatch, flags=V3_ON)
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    absent = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    _set_orchestrator({**EC_OFF, "explore_confirm": {"enabled": False}})
    off = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    assert off == absent
    paths = [r["path"] for r in off["required_inputs"]]
    assert f"artifacts/reports/{cat}.yaml" in paths and rpr.READER_V3_EXPLORATION not in paths
    assert "explore_confirm" not in off["injected_context"]
    assert rpr._reader_v3_input_names() == (rf.DIGEST_ARTIFACT, rf.READER_SUMMARY_ARTIFACT)


def test_flag_off_stage_prompts_and_files_are_unchanged(monkeypatch):
    run_dir = _ec_run(monkeypatch, flags=V3_ON)
    prompts_absent = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts_absent, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    arts = run_dir / "artifacts"
    first = {c: (arts / "proposals" / f"{c}.yaml").read_text(encoding="utf-8")
             for c in REPORT_CATEGORIES}
    shutil.rmtree(arts / "proposals")
    _set_orchestrator({**EC_OFF, "explore_confirm": {"enabled": False}})
    prompts_off = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts_off, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert prompts_off == prompts_absent and prompts_off
    # positive control: flag off, the readers DO see confirmation numbers here
    assert any("919191" in p for p in prompts_off) and any("828282" in p for p in prompts_off)
    assert {c: (arts / "proposals" / f"{c}.yaml").read_text(encoding="utf-8")
            for c in REPORT_CATEGORIES} == first
    for name in (ec.SPLIT_ARTIFACT, ec.EXPLORATION_DIR, ec.CONFIRMATION_ARTIFACT):
        assert not (arts / name).exists()
    assert not (rpr.ROOT / ec.LEDGER_REL).exists()
    assert ec.summary_lines(rpr.ROOT) == []


def test_build_reports_without_only_windows_is_unchanged(tmp_path):
    run_dir = tmp_path / "run_x"
    _make_run(run_dir)
    a = br.build_reports(run_dir, write=False, variants=_meta())
    b = br.build_reports(run_dir, write=False, variants=_meta(), only_windows=None)
    for c in REPORT_CATEGORIES:
        a[c].pop("generated_at"), b[c].pop("generated_at")
    assert a == b
    assert all("windows_shown" not in a[c] for c in REPORT_CATEGORIES)
    # the all-window reports DO carry the sentinels: the fixture would catch a leak
    assert all(s in yaml.safe_dump(a) for s in SENTINELS)


def test_campaign_summary_unchanged_without_a_ledger():
    queue = {"version": "1.0", "queue": []}
    camp._regenerate_summary(queue)
    assert "unseen windows" not in camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 3. The split
# ---------------------------------------------------------------------------

def _rows(n):
    return [{"label": f"w{i}", "start": f"2022-{i + 1:02d}-01", "end": f"2022-{i + 1:02d}-28"}
            for i in range(n)]


def test_six_windows_split_three_and_three(tmp_path):
    run_dir = tmp_path / "run_x"
    _make_run(run_dir)
    doc = ec.ensure_split(run_dir / "artifacts", "run_x", extra_files=[run_dir / "protocol.json"])
    assert ec.labels(doc["exploration"]) == EXPL and ec.labels(doc["confirmation"]) == CONF
    assert doc["rule"] == ec.RULE


def test_odd_count_gives_the_extra_window_to_confirmation_and_one_window_refuses():
    s = ec.split_windows(_rows(7))
    assert len(s["exploration"]) == 3 and len(s["confirmation"]) == 4
    with pytest.raises(ec.SplitError, match="at least 2"):
        ec.split_windows(_rows(1))


def test_the_split_is_time_ordered_not_file_ordered(tmp_path):
    arts = tmp_path / "artifacts"
    (arts / "variants" / "v").mkdir(parents=True)
    rows = list(reversed(WINDOWS))
    (arts / "variants" / "v" / "protocol.json").write_text(json.dumps({"windows": [
        {"label": l, "test": {"start": s, "end": e}} for l, s, e in rows]}), encoding="utf-8")
    assert ec.labels(ec.protocol_windows(arts)) == EXPL + CONF


def test_the_split_is_kept_on_a_rerun_and_a_new_window_refuses(tmp_path):
    run_dir = tmp_path / "run_x"
    _make_run(run_dir)
    proto = run_dir / "protocol.json"
    first = ec.ensure_split(run_dir / "artifacts", "run_x", extra_files=[proto])
    assert ec.ensure_split(run_dir / "artifacts", "run_x", extra_files=[proto]) == first
    doc = json.loads(proto.read_text(encoding="utf-8"))
    doc["windows"].append({"label": "2024-01", "test": {"start": "2024-01-01",
                                                        "end": "2024-04-30"}})
    proto.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(ec.SplitError, match="neither half"):
        ec.ensure_split(run_dir / "artifacts", "run_x", extra_files=[proto])


def test_no_protocol_and_conflicting_ranges_refuse(tmp_path):
    with pytest.raises(ec.SplitError, match="no protocol file"):
        ec.protocol_windows(tmp_path)
    p1, p2 = tmp_path / "a.json", tmp_path / "b.json"
    p1.write_text(json.dumps({"windows": [{"label": "w", "test": {"start": "2022-01-01",
                                                                   "end": "2022-02-01"}}]}))
    p2.write_text(json.dumps({"windows": [{"label": "w", "test": {"start": "2022-01-01",
                                                                   "end": "2022-03-01"}}]}))
    with pytest.raises(ec.SplitError, match="two date ranges"):
        ec.protocol_windows(tmp_path, extra_files=[p1, p2])


def test_the_split_is_written_at_stage_entry_before_any_stage_branch():
    """The hook sits in run_tool_worker's entry preamble (next to the other
    protocol_execution clears), before the first stage branch -- so before
    any backtest of protocol_execution."""
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    hook = 'if stage_name == "protocol_execution" and _explore_confirm_enabled():'
    assert src.count(hook) == 1
    entry = src.index(hook)
    assert src.index("async def run_tool_worker(") < entry
    assert entry < src.index('if stage_name == "data_availability_gate" and _variant_loop_enabled()')


# ---------------------------------------------------------------------------
# 4. The readers' inputs carry no confirmation-window number
# ---------------------------------------------------------------------------

def test_exploration_copies_carry_no_confirmation_number(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    rpr._write_registry_summary(run_dir, idea_status="refuted")
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    expl_dir = run_dir / "artifacts" / ec.EXPLORATION_DIR
    names = sorted(p.relative_to(expl_dir).as_posix() for p in expl_dir.rglob("*.yaml"))
    assert names == sorted([f"reports/{c}.yaml" for c in REPORT_CATEGORIES]
                           + ["grid_evaluation.yaml", rf.DIGEST_ARTIFACT,
                              rf.READER_SUMMARY_ARTIFACT, "registry_summary.yaml",
                              "hypothesis_card.yaml"])
    text = _text_of_tree(expl_dir)
    _assert_no_leak(text)
    for label in EXPL:
        assert label in text


def test_reports_keep_the_exploration_windows_and_withhold_pooled_overall(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    d = run_dir / "artifacts" / ec.EXPLORATION_DIR / "reports"
    prof = yaml.safe_load((d / "profitability.yaml").read_text(encoding="utf-8"))
    base = prof["variants"]["base"]["slices"]
    assert sorted({r["window"] for r in base["per_window"]}) == EXPL
    assert base["overall"] == {"unavailable": True, "reason": br.WINDOWS_WITHHELD_REASON}
    assert prof["windows_shown"] == EXPL
    te = yaml.safe_load((d / "trade_efficiency.yaml").read_text(encoding="utf-8"))
    assert sorted(te["variants"]["base"]["slices"]["per_window"]) == EXPL
    ca = yaml.safe_load((d / "component_attribution.yaml").read_text(encoding="utf-8"))
    assert ca["variants"]["base"]["slices"]["overall"]["components_discovered"] == ["c1"]


def test_the_grid_rereduces_window_criteria_and_withholds_the_rest(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    g = yaml.safe_load((run_dir / "artifacts" / ec.EXPLORATION_DIR
                        / "grid_evaluation.yaml").read_text(encoding="utf-8"))
    assert g["idea_status"] == ec.WITHHELD and g["windows_shown"] == EXPL
    for vid, pr in _prs(run_dir).items():
        cut = ec.restrict_protocol_result(pr, EXPL)
        assert g["grid"]["c_win"][vid] == vce._evaluate_grid_cell(
            vce._resolve_grid_criteria(PRE_REG, {})[0], cut, vce._load_campaign_data_policy_eras())
        assert g["grid"]["c_win"][vid]["n_windows"] == 6  # 3 windows x 2 coins
        assert g["grid"]["c_pool"][vid]["result"] == ec.WITHHELD


def test_the_digest_is_measured_on_the_exploration_windows_only(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    rpr._write_registry_summary(run_dir, idea_status="refuted")
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    d = yaml.safe_load((run_dir / "artifacts" / ec.EXPLORATION_DIR
                        / rf.DIGEST_ARTIFACT).read_text(encoding="utf-8"))
    full = rf.claim_result_digest(run_dir)
    eras, holdout = _eras_holdout()
    tests = _pure_claim()["tests"]
    own, measured = ec.measure_on_windows(run_dir, "base", tests, EXPL, eras, holdout)
    assert sorted({m.split("/")[1] for m in measured}) == EXPL
    row = d["variants"]["base"]["tests"]["up_day_followthrough"]["horizons"]["1"]
    expect = own["up_day_followthrough"]["horizons"][1]
    assert row["effect"] == pytest.approx(expect["value"], rel=1e-3)
    assert row["windows_with_value"] == 6
    full_row = full["variants"]["base"]["tests"]["up_day_followthrough"]["horizons"]["1"]
    assert full_row["windows_with_value"] == 12 and full_row["effect"] != row["effect"]
    assert d["statement"] == full["statement"] and d["windows_shown"] == EXPL


def test_earlier_findings_and_registry_numbers_are_withheld():
    summary = {"findings": [{"run_id": "run_1", "tests": [{"name": "t", "by_variant": {
        "base": {"status": "measured", "largest_effect": {"horizon": "1", "effect": SENT_CONF}}}}]}],
        "statistic_labels": {"mean_diff": "x"}}
    out = ec.withhold_findings_numbers(summary)
    assert out["findings"][0]["tests"][0]["by_variant"]["base"]["largest_effect"] == ec.WITHHELD
    assert "919191" not in yaml.safe_dump(out) and summary["findings"][0]["tests"][0][
        "by_variant"]["base"]["largest_effect"]["effect"] == SENT_CONF   # input untouched
    reg = {"this_run": {"idea_status": "validated", "correlation_to_composite": {
        "status": "measured", "by_variant": {"base": SENT_POOL}, "max_abs": SENT_POOL}},
        "blocks": [{"block_id": "B1", "residual_ic": SENT_POOL,
                    "correlation_to_composite": SENT_POOL}],
        "groups": [{"residual_ic_range": [SENT_POOL, SENT_POOL],
                    "abs_correlation_to_composite_range": [SENT_POOL, SENT_POOL]}]}
    out = ec.withhold_registry_numbers(reg)
    assert "828282" not in yaml.safe_dump(out) and "validated" not in yaml.safe_dump(out)
    assert out["blocks"][0]["block_id"] == "B1"


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_the_handoff_points_at_the_exploration_copies(cat, monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    rpr._write_registry_summary(run_dir, idea_status="refuted")
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    h = rpr._reader_handoff(cat, RUN_ID, 0, run_dir)
    req = [r["path"] for r in h["required_inputs"]]
    x = f"artifacts/{ec.EXPLORATION_DIR}"
    for rel in (f"reports/{cat}.yaml", "grid_evaluation.yaml", rf.DIGEST_ARTIFACT,
                rf.READER_SUMMARY_ARTIFACT, "registry_summary.yaml"):
        assert f"{x}/{rel}" in req and f"artifacts/{rel}" not in req
    assert req.index(rpr.READER_V3_EXPLORATION) == req.index(rpr.READER_V3_CONTRACT) + 1
    assert [r["path"] for r in h["optional_inputs"]] == ["artifacts/block_manifest.yaml"]
    assert h["injected_context"]["explore_confirm"]["exploration_windows"] == EXPL
    assert f"artifacts/reports/{cat}.yaml" not in h["objective"]


def test_every_reader_prompt_carries_no_confirmation_number(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert prompts
    for p in prompts:
        _assert_no_leak(p)
        assert "# Exploration windows only (E-072)" in p


def test_a_missing_split_stops_the_reader_never_the_full_files(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    with pytest.raises(ec.SplitError, match="missing"):
        rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)


def test_a_digest_copy_that_cannot_be_written_is_a_gap_never_the_full_file(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    rpr._write_registry_summary(run_dir, idea_status="refuted")

    def _boom(*a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(ec, "exploration_digest", _boom)
    gaps = rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    rel = f"{ec.EXPLORATION_DIR}/{rf.DIGEST_ARTIFACT}"
    assert set(gaps) == {rel}
    assert (run_dir / "artifacts" / rf.DIGEST_ARTIFACT).exists()   # the all-window one
    assert rpr._reader_v3_missing_inputs(run_dir) == [rel]
    h = rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)
    paths = [r["path"] for r in h["required_inputs"] + h["optional_inputs"]]
    assert f"artifacts/{rel}" not in paths and f"artifacts/{rf.DIGEST_ARTIFACT}" not in paths
    assert f"artifacts/{rel}" in h["injected_context"]["missing_inputs"]
    prompt = rpr._build_stage_prompt("specialist_readers", h, run_dir,
                                     skill_file_name=rpr._reader_skill_dir("profitability"))
    _assert_no_leak(prompt)


def test_a_missing_exploration_report_stops_the_prompt(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    rpr._write_registry_summary(run_dir, idea_status="refuted")
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)
    (run_dir / "artifacts" / ec.EXPLORATION_DIR / "reports" / "profitability.yaml").unlink()
    h = rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)
    with pytest.raises(FileNotFoundError, match="profitability.yaml"):
        rpr._build_stage_prompt("specialist_readers", h, run_dir,
                                skill_file_name=rpr._reader_skill_dir("profitability"))


# ---------------------------------------------------------------------------
# 5. Confirmation
# ---------------------------------------------------------------------------

def _confirmation(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "artifacts" / ec.CONFIRMATION_ARTIFACT).read_text(
        encoding="utf-8"))


@pytest.mark.parametrize("conf_sign,held", [(1.0, True), (-1.0, False)])
def test_a_pure_finding_is_measured_in_run_on_the_confirmation_windows(conf_sign, held,
                                                                       monkeypatch):
    run_dir = _ec_run(monkeypatch, conf_sign=conf_sign)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    doc = _confirmation(run_dir)
    assert doc["exploration"] == EXPL and doc["confirmation"] == CONF
    pure = next(r for r in doc["side_findings"]
                if r["finding_id"] == f"trade_efficiency-{RUN_ID}-1")
    assert pure["route"] == ec.IN_RUN and pure["status"] == ec.MEASURED
    assert pure["confirmation_sign_retained"] is held
    assert sorted({w.split("/")[1] for w in pure["windows_measured"]}) == CONF
    assert pure["variant"] == "base" and pure["measured_in_run"] == RUN_ID
    t = pure["tests"]["up_day_followthrough"]
    assert t["sign_held"] is held and (t["horizons"]["1"]["oriented"] > 0) is held
    # the reader saw a positive effect on the exploration windows in both cases
    eras, holdout = _eras_holdout()
    seen, _ = ec.measure_on_windows(run_dir, "base", _pure_claim()["tests"], EXPL, eras, holdout)
    assert seen["up_day_followthrough"]["horizons"][1]["oriented"] > 0
    assert "not proven" in pure["bar"]


def test_a_block_claim_is_pending_and_a_look_is_counted_once(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    doc = _confirmation(run_dir)
    block = next(r for r in doc["side_findings"]
                 if r["finding_id"] == f"forecast_power-{RUN_ID}-1")
    assert block["route"] == ec.PENDING and block["confirmation_sign_retained"] == ec.PENDING
    assert "tests" not in block and "looks" not in block
    assert [r["label"] for r in block["proposer_saw"]] == EXPL
    ledger = ec.load_ledger(rpr.ROOT)
    assert set(ledger["findings"]) == {f"trade_efficiency-{RUN_ID}-1",
                                       f"forecast_power-{RUN_ID}-1"}
    key = ec.set_key(ec.load_split(run_dir / "artifacts")["confirmation"])
    assert ledger["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    pure = ledger["findings"][f"trade_efficiency-{RUN_ID}-1"]
    assert pure["looks"] == {"confirmation_set": key, "n_looks_on_set": 1,
                             "n_comparisons_on_set": 1}
    # a resumed stage (every reading present) does not count the look again
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert ec.load_ledger(rpr.ROOT)["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    lines = ec.summary_lines(rpr.ROOT)
    assert any("pending 1" in x for x in lines) and any("1 look(s)" in x for x in lines)


def test_the_campaign_summary_shows_the_ledger(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    camp._regenerate_summary({"version": "1.0", "queue": []})
    text = camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")
    assert "## Side findings on unseen windows (E-072" in text


def test_routes_of_side_findings():
    assert ec.finding_route({"claim": _pure_claim()})[0] == ec.IN_RUN
    assert ec.finding_route({"claim": _block_claim()})[0] == ec.PENDING
    regime = {**_block_claim(), "kind": "regime_classifier"}
    assert ec.finding_route({"claim": regime})[0] == ec.PENDING
    reads_forecast = copy.deepcopy(_pure_claim())
    reads_forecast["tests"][0]["selector"] = {"kind": "event", "field": "forecast",
                                              "op": ">", "value": 0.0}
    change = [{"component_id": "c", "field": "params.p", "before": 1, "after": 2}]
    assert ec.finding_route({"claim": reads_forecast})[0] == ec.IN_RUN
    assert ec.finding_route({"claim": reads_forecast, "config_change": change})[0] == ec.PENDING
    assert ec.finding_route({"claim": _pure_claim(), "config_change": change})[0] == ec.IN_RUN
    none = {**_pure_claim(), "tests": "none", "missing_block": "x"}
    assert ec.finding_route({"claim": none})[0] == ec.NOT_MEASURABLE


def test_sign_rule():
    def r(*oriented, status=cmeas.MEASURED):
        return {"status": status, "horizons": {i + 1: {"oriented": o}
                                               for i, o in enumerate(oriented)}}
    assert ec.test_sign(r(0.1, 0.2))[0] is True
    assert ec.test_sign(r(0.1, None))[0] is True
    assert ec.test_sign(r(0.1, -0.2))[0] is False
    assert ec.test_sign(r(0.0))[0] is False
    assert ec.test_sign(r(None))[0] is False
    assert ec.test_sign(r(status=cmeas.NO_EVENTS))[0] is False
    assert ec.test_sign({"status": cmeas.NOT_MEASURED, "reason": "error"})[0] is None
    assert ec.finding_sign({"a": r(0.1), "b": r(-0.1)})[0] is False
    assert ec.finding_sign({"a": r(0.1), "b": {"status": "not_measured"}})[0] is None
    assert ec.finding_sign({"a": r(0.1), "b": r(0.3)})[0] is True


def _seed_pending(monkeypatch) -> dict:
    """run_990 proposes a block claim (pending); returns its ledger record."""
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    return ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]


def _child_run(monkeypatch, run_id: str, windows=WINDOWS) -> Path:
    """The run built from forecast_power-run_990-1: its brief names the finding,
    its card carries the block claim."""
    run_dir = _ec_run(monkeypatch, run_id=run_id, windows=windows, card_claim=_block_claim())
    _save(run_dir / "artifacts" / "research_brief.yaml", {"candidate": {"source": {
        "proposal_ref": f"runs/{RUN_ID}/artifacts/proposals/forecast_power.yaml"
                        f"#forecast_power-{RUN_ID}-1"}}})
    return run_dir


def test_the_run_built_from_a_block_claim_resolves_it(monkeypatch):
    pending = _seed_pending(monkeypatch)
    assert pending["confirmation_sign_retained"] == ec.PENDING
    child = _child_run(monkeypatch, "run_991")
    _protocol_execution_part(child, "run_991")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([]))
    rpr._run_specialist_readers_stage("run_991", child)
    rec = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["status"] == ec.MEASURED and rec["measured_in_run"] == "run_991"
    assert rec["confirmation_sign_retained"] in (True, False)
    assert rec["source_run"] == RUN_ID and rec["tests_changed_from_finding"] is False
    eras, holdout = _eras_holdout()
    own, _ = ec.measure_on_windows(child, "base", _block_claim()["tests"], CONF, eras, holdout)
    assert rec["confirmation_sign_retained"] is ec.test_sign(own["forecast_rank"])[0]
    assert _confirmation(child)["resolved_pending"][0]["finding_id"] == f"forecast_power-{RUN_ID}-1"
    key = ec.set_key(ec.load_split(child / "artifacts")["confirmation"])
    assert ec.load_ledger(rpr.ROOT)["by_set"][key]["n_looks"] == 2   # pure (run_990) + this


def test_a_child_whose_confirmation_the_proposer_saw_stays_pending(monkeypatch):
    _seed_pending(monkeypatch)
    # a protocol whose second half is the first half of run_990's: 2022 only
    shifted = [("2021-05", "2021-05-01", "2021-08-31"), ("2021-09", "2021-09-01", "2021-12-31"),
               ("2022-01", "2022-01-01", "2022-04-30"), ("2022-05", "2022-05-01", "2022-08-31")]
    child = _child_run(monkeypatch, "run_992", windows=shifted)
    _protocol_execution_part(child, "run_992")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([]))
    rpr._run_specialist_readers_stage("run_992", child)
    rec = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["confirmation_sign_retained"] == ec.PENDING
    assert "the proposer saw them" in rec["attempts"][-1]["result"]


def test_a_confirmation_error_never_stops_the_run(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)

    def _boom(*a, **k):
        raise RuntimeError("bars unreadable")
    monkeypatch.setattr(ec, "measure_on_windows", _boom)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    pure = next(r for r in _confirmation(run_dir)["side_findings"]
                if r["route"] == ec.IN_RUN)
    assert pure["status"] == ec.ERROR and pure["confirmation_sign_retained"] is None
    assert ec.load_ledger(rpr.ROOT)["by_set"] == {}   # nothing measured: no look


# ---------------------------------------------------------------------------
# 6. Old runs and inputs still load
# ---------------------------------------------------------------------------

def test_an_older_measurement_name_still_gives_an_exploration_digest(tmp_path):
    run_dir = tmp_path / "run_x"
    _make_run(run_dir)
    arts = run_dir / "artifacts"
    (arts / cmeas.RUN_FILE).rename(arts / cmeas.OLD_RUN_FILE)   # a pre-D-077 run
    eras, holdout = _eras_holdout()
    d = ec.exploration_digest(run_dir, EXPL, eras, holdout)
    assert d["claim_status"] == cmeas.MEASURED and set(d["variants"]) == set(VARIANTS)


def test_a_run_without_measurement_gives_an_absent_digest(tmp_path):
    run_dir = tmp_path / "run_x"
    _make_run(run_dir)
    (run_dir / "artifacts" / cmeas.RUN_FILE).unlink()
    eras, holdout = _eras_holdout()
    d = ec.exploration_digest(run_dir, EXPL, eras, holdout)
    assert d["claim_status"] == "absent" and d["variants"] == {}


def test_readings_without_side_findings_and_an_absent_ledger_load(tmp_path):
    assert ec.load_ledger(tmp_path) == {}
    assert ec.side_finding_items({"profitability": _reading("profitability", sides=[]),
                                  "regime_power": {"schema_version": 3,
                                                   "reading_id": f"regime_power-{RUN_ID}",
                                                   "skipped": {"rule": "r", "reason": "x"}}}) == []
    assert ec.source_finding_id(tmp_path) is None


# ---------------------------------------------------------------------------
# 7. Review fixes (PR #340, independent review at 13a88fac)
# ---------------------------------------------------------------------------

def _skips(run_dir: Path) -> dict:
    out = {}
    for c in REPORT_CATEGORIES:
        doc = yaml.safe_load((run_dir / "artifacts" / "proposals" / f"{c}.yaml").read_text(
            encoding="utf-8"))
        out[c] = (doc or {}).get("skipped")
    return out


def _assert_every_reader_skipped_by_e072_rule(run_dir: Path, prompts: list) -> None:
    """No reader called; every reading a code-written skip. The fixture has one
    component, so component_attribution is skipped first by the existing
    single_component rule; every other reader by the E-072 rule."""
    assert prompts == []                       # no reader was called
    expected = {c: rf.SKIP_EXPLORATION_UNAVAILABLE for c in REPORT_CATEGORIES}
    expected["component_attribution"] = rf.SKIP_SINGLE_COMPONENT
    got = {c: (skip or {}).get("rule") for c, skip in _skips(run_dir).items()}
    assert got == expected
    rec = yaml.safe_load((rpr.ROOT / rf.SKIPS_REL).read_text(encoding="utf-8"))
    assert {c: s["rule"] for c, s in rec["runs"][run_dir.name].items()} == expected


# --- finding 1: a follow-up resolution is weak, counted apart ---------------

def test_in_run_measurements_carry_their_basis(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    pure = next(r for r in _confirmation(run_dir)["side_findings"] if r["route"] == ec.IN_RUN)
    assert pure["confirmation_basis"] == ec.BASIS_IN_RUN and "weak" not in pure


def test_a_follow_up_resolution_is_marked_weak_and_counted_apart(monkeypatch):
    _seed_pending(monkeypatch)
    child = _child_run(monkeypatch, "run_991")
    _protocol_execution_part(child, "run_991")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([]))
    rpr._run_specialist_readers_stage("run_991", child)
    rec = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["confirmation_basis"] == ec.BASIS_FOLLOW_UP
    assert rec["proposer_exposure"] == ec.PROPOSER_EXPOSURE_1A and rec["weak"] is True
    assert rec["bar"] == ec.WEAK_BAR and rec["bar"].startswith("WEAK")
    assert rec["confirmation_sign_retained"] in (True, False)
    lines = ec.summary_lines(rpr.ROOT)
    main = next(x for x in lines if x.startswith("- Side findings:"))
    # the clean counts hold only run_990's in-run pure finding (reversal: not held)
    assert "held 0, not held 1, pending 0" in main and "resolved by a follow-up run 1" in main
    follow = next(x for x in lines if "resolved by the run built from them" in x)
    assert "weak" in follow
    held = "held 1, not held 0" if rec["confirmation_sign_retained"] else "held 0, not held 1"
    assert held in follow


def test_a_follow_up_run_with_other_tests_is_not_comparable(monkeypatch):
    _seed_pending(monkeypatch)
    other = copy.deepcopy(_block_claim())
    other["tests"][0]["outcome"]["horizons"] = [1, 2]       # another spec_hash
    run_dir = _ec_run(monkeypatch, run_id="run_993", card_claim=other)
    _save(run_dir / "artifacts" / "research_brief.yaml", {"candidate": {"source": {
        "proposal_ref": f"runs/{RUN_ID}/artifacts/proposals/forecast_power.yaml"
                        f"#forecast_power-{RUN_ID}-1"}}})
    _protocol_execution_part(run_dir, "run_993")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([]))
    rpr._run_specialist_readers_stage("run_993", run_dir)
    rec = ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["tests_changed_from_finding"] is True
    assert rec["confirmation_sign_retained"] == ec.NOT_COMPARABLE
    assert rec["sign_of_own_tests"] in (True, False) and rec["weak"] is True
    lines = ec.summary_lines(rpr.ROOT)
    main = next(x for x in lines if x.startswith("- Side findings:"))
    assert "held 0, not held 1" in main          # run_990's pure finding only
    follow = next(x for x in lines if "resolved by the run built from them" in x)
    assert "held 0, not held 0, not comparable 1" in follow


# --- finding 2: E-072 never stops a run --------------------------------------

def test_fewer_than_two_windows_is_not_applicable_and_the_run_proceeds_flag_off(monkeypatch):
    run_dir = _ec_run(monkeypatch, windows=WINDOWS[:1])
    split = rpr._prepare_explore_confirm(run_dir, RUN_ID)       # never raises
    assert split["status"] == ec.NOT_APPLICABLE and "at least 2" in split["reason"]
    on_disk = yaml.safe_load((run_dir / "artifacts" / ec.SPLIT_ARTIFACT).read_text(
        encoding="utf-8"))
    assert on_disk["effect"] == ec.NOT_APPLICABLE_EFFECT
    assert rpr._explore_confirm_active(run_dir) is False and rpr._explore_confirm_enabled()
    # kept on a re-run
    assert rpr._prepare_explore_confirm(run_dir, RUN_ID)["status"] == ec.NOT_APPLICABLE
    prompts_on = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts_on, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    arts = run_dir / "artifacts"
    assert not (arts / ec.EXPLORATION_DIR).exists()
    assert not (arts / ec.CONFIRMATION_ARTIFACT).exists()
    assert not (rpr.ROOT / ec.LEDGER_REL).exists()
    shutil.rmtree(arts / "proposals")
    _set_orchestrator(EC_OFF)
    prompts_off = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts_off, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert prompts_on == prompts_off and prompts_on      # exactly the flag-off readers


def test_a_split_failure_at_entry_never_raises_and_the_readers_are_skipped(monkeypatch):
    run_dir = _ec_run(monkeypatch)

    def _boom(*a, **k):
        raise ec.SplitError("window 'x' has two date ranges")
    monkeypatch.setattr(ec, "ensure_split", _boom)
    assert rpr._prepare_explore_confirm(run_dir, RUN_ID) is None
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)          # returns: the run continues
    _assert_every_reader_skipped_by_e072_rule(run_dir, prompts)
    assert "split cannot be read" in _skips(run_dir)["profitability"]["reason"]
    assert _confirmation(run_dir)["status"] == "error"


def test_an_exploration_views_failure_does_not_fail_protocol_execution():
    """The protocol_execution hook routes a failure to _exploration_views_failed,
    never into _sr_errors (which fails the stage)."""
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    start = src.index("# E-072: the readers' copies of the reports and the grid")
    end = src.index('print(f"✅ protocol_execution (variant loop)', start)
    block = src[start:end]
    assert "_exploration_views_failed(RUN_DIR, _ec_err)" in block
    assert "_sr_errors.append" not in block and "raise" not in block


def test_after_an_exploration_views_failure_the_readers_are_skipped(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)                 # a partial set is on disk
    rpr._exploration_views_failed(run_dir, OSError("disk full"))
    assert not (run_dir / "artifacts" / ec.EXPLORATION_DIR).exists()
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    _assert_every_reader_skipped_by_e072_rule(run_dir, prompts)
    assert "never given instead" in _skips(run_dir)["profitability"]["reason"]


@pytest.mark.parametrize("which", ["registry_summary.yaml", "hypothesis_card.yaml"])
def test_a_required_copy_that_cannot_be_written_skips_the_readers(which, monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    stale = run_dir / "artifacts" / ec.EXPLORATION_DIR / which
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("older_attempt_copy: {}\n", encoding="utf-8")

    def _boom(*a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(ec, {"registry_summary.yaml": "withhold_registry_numbers",
                             "hypothesis_card.yaml": "reader_card"}[which], _boom)
    rpr._write_registry_summary(run_dir, idea_status="refuted")
    rpr._write_reader_v3_inputs(run_dir, RUN_ID)                 # never raises
    assert not stale.exists()                                    # the older copy is gone
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    _assert_every_reader_skipped_by_e072_rule(run_dir, prompts)
    assert f"{ec.EXPLORATION_DIR}/{which}" in _skips(run_dir)["profitability"]["reason"]


def test_a_run_paused_at_the_readers_when_the_flag_is_turned_on(monkeypatch):
    """protocol_execution ran with the flag off (no split); the flag is turned
    on before the resume: every resume skips the readers, none raises."""
    run_dir = _ec_run(monkeypatch, flags=EC_OFF)
    _set_orchestrator(EC_ON)
    for _ in range(2):
        prompts = []
        monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts, _sides()))
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
        _assert_every_reader_skipped_by_e072_rule(run_dir, prompts)


def test_the_new_skip_rule_is_a_code_rule_a_model_cannot_write():
    import reader_proposals as rp
    assert rf.SKIP_EXPLORATION_UNAVAILABLE == "exploration_inputs_unavailable"
    assert rf.SKIP_EXPLORATION_UNAVAILABLE in rp.SKIP_RULES
    doc = rf.skipped_reading("profitability", RUN_ID, {"rule": rf.SKIP_EXPLORATION_UNAVAILABLE,
                                                       "reason": "copies missing"})
    with pytest.raises(rp.ProposalError):
        rp.check_reading(doc, "profitability", "model output", from_model=True)


# --- finding 3: free text never carries an all-window number -----------------

def _card_with_numbers() -> dict:
    claim = {**_pure_claim(), "rationale": "the all-window effect was 919191.5",
             "pass_if": "above 828282.5", "fail_if": "below 828282.5"}
    return {"hypothesis_id": "H-TEST-1", "thesis": "it returned 919191.5 on 2023-05",
            "rationale": "seen at 828282.5 over every window",
            "edge_source": {"category": "c", "specific_mechanism": "m 919191.5",
                            "why_not_arbitraged": "w", "evidence_type": "e",
                            "measurable_proxy": "p"},
            "assumptions": ["a 919191.5"], "expected_failure_modes": ["f", "g", "h 828282.5"],
            "power_parameters": {"activation_rate": 828282.5, "plausible_ic_upper": 919191.5},
            "signal_concept": "sign of the 1-bar return", "timeframe": "1d",
            "target_market": "BTCUSD", "claim": claim}


def test_the_readers_card_is_a_whitelist():
    out = ec.reader_card(_card_with_numbers())
    _assert_no_leak(yaml.safe_dump(out))
    assert out["claim"] == {k: _pure_claim()[k] for k in ("statement", "kind", "tests")}
    assert out["signal_concept"] == "sign of the 1-bar return"
    assert out["hypothesis_id"] == "H-TEST-1"
    assert {"rationale", "thesis", "power_parameters", "claim.rationale",
            "claim.pass_if"} <= set(out["withheld_fields"]["fields"])


def test_the_card_and_earlier_free_text_never_reach_a_reader_prompt(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _save(run_dir / "artifacts" / "hypothesis_card.yaml", _card_with_numbers())
    _protocol_execution_part(run_dir)
    prompts = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm(prompts, _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert prompts
    for p in prompts:
        _assert_no_leak(p)
        assert "sign of the 1-bar return" in p          # the signal spec is given
    h = rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)
    req = [r["path"] for r in h["required_inputs"]]
    assert f"artifacts/{ec.EXPLORATION_DIR}/hypothesis_card.yaml" in req
    assert "artifacts/hypothesis_card.yaml" not in req


def test_earlier_findings_statement_and_reason_are_withheld():
    summary = {"findings": [{"finding_id": "F-run_1-1", "run_id": "run_1", "kind": "k",
                             "status": "measured", "reason": "seen at 919191.5",
                             "statement": "returned 828282.5 over every window",
                             "tests": [{"name": "t", "selector": {"kind": "all"}}]}]}
    out = ec.withhold_findings_numbers(summary)
    row = out["findings"][0]
    assert "statement" not in row and "reason" not in row
    assert row["finding_id"] == "F-run_1-1" and row["kind"] == "k"
    assert row["tests"][0]["selector"] == {"kind": "all"}
    _assert_no_leak(yaml.safe_dump(out))


def test_the_docs_say_never_saw_means_in_this_pipeline():
    for rel in ("workflow_artifacts/skills/readers_v3/EXPLORATION.md",
                "engineering/roadmap/E-072/PHASE_A.md"):
        text = (SR_ROOT / rel).read_text(encoding="utf-8")
        assert "training period" in text and "in this pipeline" in text, rel


# --- finding 4: the grid copy uses the real grid call's keywords -------------

def test_the_exploration_grid_passes_composition_runs(monkeypatch):
    seen = []
    real = vce._evaluate_grid_cell

    def _spy(*a, **k):
        seen.append(k.get("composition_runs"))
        return real(*a, **k)
    monkeypatch.setattr(vce, "_evaluate_grid_cell", _spy)
    grid_doc = {"criteria": ["c_win"], "variants": ["base"]}
    pr = {"results": [{"window": "2022-01", "symbol": "BTCUSD",
                       "core": {"sharpe": 1.0, "trade_count": 5}}]}
    ec.exploration_grid(grid_doc, {"base": pr}, PRE_REG, {}, ["2022-01"], composition_runs=True)
    ec.exploration_grid(grid_doc, {"base": pr}, PRE_REG, {}, ["2022-01"])
    assert seen == [True, False]


def test_the_views_pass_the_runs_composition_flag(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    seen = {}
    real = ec.exploration_grid

    def _spy(*a, **k):
        seen.update(k)
        return real(*a, **k)
    monkeypatch.setattr(ec, "exploration_grid", _spy)
    monkeypatch.setattr(rpr, "_composition_runs_enabled", lambda *a, **k: True)
    _protocol_execution_part(run_dir)
    assert seen["composition_runs"] is True


# --- finding 6: ledger hygiene ------------------------------------------------

def test_a_rerun_replaces_the_runs_own_entries_and_keeps_its_looks(monkeypatch):
    run_dir = _ec_run(monkeypatch)
    _protocol_execution_part(run_dir)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], _sides()))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    key = ec.set_key(ec.load_split(run_dir / "artifacts")["confirmation"])
    assert ec.load_ledger(rpr.ROOT)["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    # protocol_execution re-runs; this attempt's readers propose the block claim only
    _protocol_execution_part(run_dir)
    shutil.rmtree(run_dir / "artifacts" / "proposals")
    only_block = {"forecast_power": _sides()["forecast_power"]}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([], only_block))
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    ledger = ec.load_ledger(rpr.ROOT)
    assert set(ledger["findings"]) == {f"forecast_power-{RUN_ID}-1"}
    assert [s["finding_id"] for s in ledger["superseded"]] == [f"trade_efficiency-{RUN_ID}-1"]
    # the superseded attempt's look was measured: it stays counted
    assert ledger["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    lines = ec.summary_lines(rpr.ROOT)
    assert any("Side findings: 1 (" in x and "pending 1" in x for x in lines)


def test_a_rerun_never_removes_a_finding_another_run_measured(tmp_path):
    ec.record(tmp_path, "run_1", [{"finding_id": "a", "source_run": "run_1",
                                   "confirmation_sign_retained": True,
                                   "measured_in_run": "run_2"}])
    ec.record(tmp_path, "run_1", [])
    assert "a" in ec.load_ledger(tmp_path)["findings"]


def test_a_resume_after_resolution_keeps_resolved_pending(monkeypatch):
    _seed_pending(monkeypatch)
    child = _child_run(monkeypatch, "run_991")
    _protocol_execution_part(child, "run_991")
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([]))
    rpr._run_specialist_readers_stage("run_991", child)
    first = ec.load_ledger(rpr.ROOT)
    rpr._run_specialist_readers_stage("run_991", child)          # a resume
    doc = _confirmation(child)
    assert [r["finding_id"] for r in doc["resolved_pending"]] == [f"forecast_power-{RUN_ID}-1"]
    again = ec.load_ledger(rpr.ROOT)
    rec = again["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["measured_in_run"] == "run_991" and rec["status"] == ec.MEASURED
    assert [a["run_id"] for a in rec["attempts"]] == ["run_991"]     # replaced, not appended
    assert again["by_set"] == first["by_set"]                        # no look counted twice
    assert rec["confirmation_sign_retained"] == \
        first["findings"][f"forecast_power-{RUN_ID}-1"]["confirmation_sign_retained"]
    assert rec["pending_state"]["confirmation_sign_retained"] == ec.PENDING


def test_the_pending_lookup_reads_the_ledger_under_its_lock(monkeypatch):
    """The lookup reads the findings ec.record hands it under the lock -- not
    an unlocked load_ledger copy (here a stale, empty view)."""
    _seed_pending(monkeypatch)
    child = _child_run(monkeypatch, "run_991")
    _protocol_execution_part(child, "run_991")
    monkeypatch.setattr(ec, "load_ledger", lambda root: {})
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _readings_llm([]))
    rpr._run_specialist_readers_stage("run_991", child)
    assert _confirmation(child)["resolved_pending"][0]["measured_in_run"] == "run_991"
