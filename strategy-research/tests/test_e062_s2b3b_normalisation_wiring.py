"""
E-062 S2b-3b -- flag wiring of the D-047 partial-coverage normalisation
(engineering/DECISION_LOG.md D-047 / D-042; engineering/roadmap/E-062/
S2B3_FINDINGS.md Q2 sites 1-10, Q3, Q4, Q6, Q7, Q8 row S2b-3b, G4/G7/G8/G9/G10/
G13/G14).

Covers:
  1. Flag off: the M1 cap is unchanged (NOT_EVALUABLE time-dependent bars,
     never passing, the grid kwarg still passed, the normalisation never
     computed).
  2. Flag on: a 60%-coverage asset variant (run_053's last 58 of 96 windows =
     1767 / 2922 days) is graded on 61 trades and a 15.55 drawdown limit,
     `detail.normalisation` on each normalised row, the cost-ratio trade floor
     normalised too; just above passes (and raises profit_bars_reached), just
     below fails.
  3. Full coverage (f == 1): byte-identical rows, the normalisation never
     entered.
  4. The floor binds when 100 * f < 60.
  5. sign_consistent_by_era: fewer than 2 represented eras -> INCONCLUSIVE on
     every variant under v2 (base variants too); two eras graded as before;
     flag off unchanged. protocol_execution passes the kwarg and drops the M1
     grid cap only under v2.
  6. Legacy promote path: still capped with v2 on (G9).
  7. The spend re-derives the normalised thresholds (bars_changed otherwise)
     from the evaluation read back from disk, and from 5a's frozen run
     protocol only: never re-resolving the shared protocol, never writing
     pipeline_state; normalisation_unverifiable when the frozen copy is
     missing / altered / predates review fix 1. 7b: 5a freezes it. 7c: the
     grid's profit-bars grader holds a partial column NOT_EVALUABLE.
     Review round 1 also: an unmeasurable coverage reads NOT_EVALUABLE
     `coverage_unmeasurable:` (never raises); a zero-median single era stays
     FAIL.
  8. The loader: trade_count_min_floor required under v2 (int >= 1, <= both
     bases); the committed bars file carries 60.
"""
import asyncio
import json
import math
import sys
from datetime import date
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import variant_coin as vc  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID, _grid, _seed, _set_orchestrator  # noqa: E402
from test_profit_bars_every_backtest import VARIANT_LOOP_ON, _seed_dsr_ledger  # noqa: E402
from test_e062_s2b1_profit_bars_v2 import (  # noqa: E402
    FULL_ON, V1_BARS, V2_BARS, V2_ON, _attach_whole_test, _build, _default_strat, _trade,
    _write_bars, _write_cost_model)
from test_grid_evaluation import _menu_shaped_pre_reg, _protocol_result, _window  # noqa: E402

RUN053 = SR_ROOT / "protocols" / "run_053_generated.json"
N_COVERED = 58                        # run_053 58/96 (S2B3_FINDINGS.md Q3)
COVERED_DAYS, FULL_DAYS = 1767, 2922  # its nominal calendar days (S2b-3a)
LIMIT_60 = 20.0 * math.sqrt(COVERED_DAYS / FULL_DAYS)  # 15.5527...
TIME_ROWS = ("trade_count_min", "max_drawdown_pct_max", "cost_edge_ratio_min")
V2_LOOP = {**V2_ON, **VARIANT_LOOP_ON}
V1_LOOP = {**FULL_ON, **VARIANT_LOOP_ON}
SCE = {"id": "sce", "metric": "net_return_pct", "source": "window",
       "reducer": "sign_consistent_by_era", "floor": {"min_windows": 1}}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# Fixture: a per-coin run whose asset variant covers the last `covered` of
# run_053's 96 windows
# ---------------------------------------------------------------------------

def _add_signal_trades(out_dir: Path, pr: dict, extra: int) -> None:
    """`extra` more non-forced trades in the first window (records AND its
    core.trade_count, so the pair stays consistent)."""
    path = out_dir / "trade_diagnostics.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    first = pr["results"][0]
    doc["trades"] += [_trade(first["symbol"], first["window"], "signal_flip", 0.45, 15.0)
                      for _ in range(extra)]
    first["core"]["trade_count"] += extra
    path.write_text(json.dumps(doc), encoding="utf-8")


def _drawdown_strat(first_label: str, r: float, n: int = 10):
    """n losing days of -r at the start of the first window, then gains:
    chained drawdown 100 * (1 - (1 - r) ** n)."""
    def strat(label, k):
        if label == first_label and 1 <= k <= n:
            return -r
        return _default_strat(label, k)
    return strat


_REAL_RESOLVE = rpr._resolve_protocol_path  # the real resolver, before any stub


def _no_resolve(*_a, **_k):
    raise AssertionError("grading / the spend must never re-resolve the shared run protocol "
                         "(review fix 1): they read 5a's frozen copy")


def _run_proto_path() -> Path:
    return rpr.ROOT / "protocols" / "run_053_generated.json"


def _partial_run(monkeypatch, *, orchestrator=None, bars=None, trades=61, covered=N_COVERED,
                 dd=None, with_base=False) -> Path:
    """A per-coin run as 5a leaves it: the asset variant covers the last
    `covered` of run_053's windows; `with_base` adds a full-coverage BTCUSDT
    base column. 5a's own _freeze_run_protocol writes the frozen run protocol
    (review fix 1); afterwards the shared-protocol resolver is a trap."""
    _set_orchestrator(V2_LOOP if orchestrator is None else orchestrator)
    _write_bars(V2_BARS if bars is None else bars)
    _write_cost_model()
    run_dir = _seed(variant_loop=True)
    arts = run_dir / "artifacts"
    source = json.loads(RUN053.read_text(encoding="utf-8"))
    run_proto = _run_proto_path()
    run_proto.parent.mkdir(parents=True, exist_ok=True)
    run_proto.write_text(json.dumps(source, indent=2), encoding="utf-8")
    monkeypatch.setattr(rpr, "_resolve_protocol_path", lambda rd, rid: run_proto)
    _, run_sha = rpr._freeze_run_protocol(run_dir, RUN_ID)  # the real 5a helper
    labels = [w["label"] for w in source["windows"]]
    run_labels = labels[len(labels) - covered:]
    specs = {"asset": ("SOLUSDT", run_labels if covered < len(labels) else None, trades)}
    if with_base:
        specs["base"] = ("BTCUSDT", None, 100)
    index, prs, rows = {}, {}, []
    for vid, (coin, wr, n_trades) in specs.items():
        vproto = vc.variant_protocol(source, symbol=coin, windows_run=wr)
        vpath = arts / "variants" / vid / vc.VARIANT_PROTOCOL_FILENAME
        vpath.parent.mkdir(parents=True, exist_ok=True)
        raw = json.dumps(vproto, indent=2).encode("utf-8")
        vpath.write_bytes(raw)
        index[vid] = {
            "status": "validated", "config_path": f"artifacts/variants/{vid}/strategy_config.json",
            "kind": vid, "symbol": coin,
            **({"coverage": {"windows_run": run_labels, "windows_total": len(labels)}}
               if vid == "asset" else {}),
            "protocol_path": f"artifacts/variants/{vid}/{vc.VARIANT_PROTOCOL_FILENAME}",
            "protocol_sha256": vc.protocol_sha256(raw), rpr.RUN_PROTOCOL_SHA_KEY: run_sha}
        windows = [(w["label"], date.fromisoformat(w["test"]["start"]),
                    date.fromisoformat(w["test"]["end"])) for w in vproto["windows"]]
        out_dir = run_dir / "variants" / vid
        kw = ({"strat": _drawdown_strat(windows[0][0], dd)}
              if dd is not None and vid == "asset" else {})
        pr = _build(out_dir, coins=(coin,), windows=windows, n_signal=1, **kw)
        _add_signal_trades(out_dir, pr, n_trades - len(windows))
        pr["protocol_file"] = str(vpath)
        rpr.save_yaml(arts / "variants" / vid / "protocol_result.yaml", pr)
        prs[f"{RUN_ID}:{vid}"] = pr
        rows.append({"trial_id": f"{RUN_ID}:{vid}", "source": "backtest", "sharpe": 0.3,
                     "forecast_hash": f"fh-{vid}"})
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    rpr.save_yaml(arts / "grid_evaluation.yaml", _grid(sorted(specs), "validated"))
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [],
                                            "trial_sharpes": rows})
    _seed_dsr_ledger()
    _attach_whole_test(run_dir, prs)
    monkeypatch.setattr(rpr, "_resolve_protocol_path", _no_resolve)
    return run_dir


def _evaluate(run_dir, **kw) -> dict:
    return rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID, **kw)


def _rows(ev, vid="asset") -> dict:
    return {r["name"]: r for r in ev["variants"][vid]["bars"]}


def _r_for(dd_pct: float, n: int = 10) -> float:
    return 1.0 - (1.0 - dd_pct / 100.0) ** (1.0 / n)


# ---------------------------------------------------------------------------
# 1. Flag off: M1 unchanged
# ---------------------------------------------------------------------------

def test_flag_off_the_m1_cap_is_unchanged_and_nothing_is_normalised(monkeypatch):
    run_dir = _partial_run(monkeypatch, orchestrator=V1_LOOP, bars=V1_BARS)

    def _boom(*_a, **_k):
        raise AssertionError("the normalisation must not run flag off")
    monkeypatch.setattr(rpr, "_variant_coverage_days", _boom)
    monkeypatch.setattr(rpr, "_normalised_profit_bars", _boom)
    ev = _evaluate(run_dir)
    assert "bars_definitions" not in ev
    a = ev["variants"]["asset"]
    assert a["result"] == "FAIL" and ev["passing"] == []
    assert "58/96" in a["partial_coverage"] and "E-062 S2b" in a["partial_coverage"]
    rows = _rows(ev)
    for name in vc.D042_TIME_DEPENDENT_BARS:
        assert rows[name]["result"] == "NOT_EVALUABLE"
        assert "temporary until E-062 S2b" in rows[name]["not_evaluable_reason"]
        assert rows[name]["threshold"] == V1_BARS[name]
        assert "normalisation" not in (rows[name].get("detail") or {})
    assert rpr._profit_bars_stop_route(run_dir, RUN_ID) is None


def test_flag_off_candidates_and_the_partial_reason_are_byte_identical(monkeypatch):
    run_dir = _partial_run(monkeypatch, orchestrator=V1_LOOP, bars=V1_BARS)
    cand = rpr._profit_bars_backtest_candidates(run_dir, RUN_ID)["asset"]
    assert "coverage_days" not in cand
    assert cand["partial_coverage"] == (
        "partial coverage: ran on 58/96 run-protocol windows (D-042); its time-dependent bars "
        "are not normalised until E-062 S2b")
    assert rpr._grid_v2_kw() == {}


# ---------------------------------------------------------------------------
# 2. Flag on: the normalisation
# ---------------------------------------------------------------------------

def test_flag_on_60_percent_variant_is_graded_on_61_trades_and_a_15_55_limit(monkeypatch):
    run_dir = _partial_run(monkeypatch, trades=61)
    cand = rpr._profit_bars_backtest_candidates(run_dir, RUN_ID, v2=True)["asset"]
    assert cand["coverage_days"] == (COVERED_DAYS, FULL_DAYS)
    assert "normalised to the covered period (D-047)" in cand["partial_coverage"]
    ev = _evaluate(run_dir)
    assert ev["bars_definitions"] == "v2"
    rows = _rows(ev)
    assert rows["trade_count_min"]["threshold"] == 61
    assert rows["trade_count_min"]["actual"] == 61 and rows["trade_count_min"]["result"] == "PASS"
    assert rows["max_drawdown_pct_max"]["threshold"] == LIMIT_60
    assert round(LIMIT_60, 2) == 15.55
    assert rows["cost_edge_ratio_min"]["threshold"] == 2.2  # the ratio itself unchanged (G6)
    assert rows["cost_edge_ratio_min"]["detail"]["min_trades"] == 61
    assert rows["cost_edge_ratio_min"]["result"] == "PASS"
    common = {"covered_days": COVERED_DAYS, "full_days": FULL_DAYS,
              "f": COVERED_DAYS / FULL_DAYS}
    assert rows["trade_count_min"]["detail"]["normalisation"] == {
        **common, "base": 100, "floor": 60,
        "formula": "max(ceil(trade_count_min * f), trade_count_min_floor)"}
    assert rows["max_drawdown_pct_max"]["detail"]["normalisation"] == {
        **common, "base": 20.0, "floor": None, "formula": "max_drawdown_pct_max * sqrt(f)"}
    assert rows["cost_edge_ratio_min"]["detail"]["normalisation"] == {
        **common, "base": 100, "floor": 60,
        "formula": "min_trades = max(ceil(cost_edge_min_trades * f), trade_count_min_floor)"}
    # G6: every other row carries no normalisation and the bars file's threshold
    for name, row in rows.items():
        if name not in TIME_ROWS:
            assert row["threshold"] == V2_BARS[name]
            assert "normalisation" not in (row.get("detail") or {})
    # all bars pass -> passing -> the branch-3 stop fires on a partial variant
    assert ev["variants"]["asset"]["result"] == "PASS", ev["variants"]["asset"]["reasons"]
    assert ev["passing"] == ["asset"]
    assert rpr._profit_bars_stop_route(run_dir, RUN_ID) == "human_pause"
    text = (run_dir / "artifacts" / "profit_bars_evaluation.yaml").read_text(encoding="utf-8")
    assert "&id" not in text and "*id" not in text  # no YAML alias between rows


def test_flag_on_one_trade_below_the_normalised_minimum_fails(monkeypatch):
    run_dir = _partial_run(monkeypatch, trades=60)
    rows = _rows(_evaluate(run_dir))
    assert rows["trade_count_min"]["threshold"] == 61 and rows["trade_count_min"]["actual"] == 60
    assert rows["trade_count_min"]["result"] == "FAIL"
    # the cost row's normalised floor (61 non-forced trades) is not met either
    cost = rows["cost_edge_ratio_min"]
    assert cost["result"] == "NOT_EVALUABLE" and "61" in cost["not_evaluable_reason"]
    assert cost["detail"]["normalisation"]["floor"] == 60


@pytest.mark.parametrize("dd_pct,expected", [(15.0, "PASS"), (17.0, "FAIL")])
def test_flag_on_drawdown_is_judged_on_the_scaled_limit(monkeypatch, dd_pct, expected):
    """17 % passes the unscaled 20 % limit but not 20 * sqrt(f) = 15.55 %."""
    run_dir = _partial_run(monkeypatch, dd=_r_for(dd_pct))
    row = _rows(_evaluate(run_dir))["max_drawdown_pct_max"]
    assert row["actual"] == pytest.approx(dd_pct, abs=1e-6)
    assert row["threshold"] == LIMIT_60 and row["comparator"] == "<="
    assert row["result"] == expected


def test_flag_on_a_partial_variant_without_its_coverage_days_raises(monkeypatch):
    run_dir = _partial_run(monkeypatch)
    real = rpr._profit_bars_backtest_candidates

    def _no_days(rd, rid, **kw):
        out = real(rd, rid, **kw)
        out["asset"].pop("coverage_days")
        return out
    monkeypatch.setattr(rpr, "_profit_bars_backtest_candidates", _no_days)
    with pytest.raises(ValueError, match="carries no coverage_days"):
        _evaluate(run_dir)


def _assert_coverage_unmeasurable(ev, match: str, vid="asset") -> None:
    """Review fix 2: the variant's three normalised rows read NOT_EVALUABLE
    `coverage_unmeasurable: <reason>`; it never passes."""
    v = ev["variants"][vid]
    assert v["result"] == "FAIL" and vid not in ev["passing"]
    assert match in v["coverage_unmeasurable"]
    rows = _rows(ev, vid)
    for name in TIME_ROWS:
        assert rows[name]["result"] == "NOT_EVALUABLE"
        assert rows[name]["not_evaluable_reason"].startswith(rpr.COVERAGE_UNMEASURABLE_PREFIX)
        assert match in rows[name]["not_evaluable_reason"]
        assert "normalisation" not in (rows[name].get("detail") or {})


@pytest.mark.parametrize("resha,match", [(False, "not the file 5a wrote"),
                                         (True, "not a subsequence")],
                         ids=["altered_after_5a", "windows_outside_the_run_protocol"])
def test_flag_on_an_unusable_variant_protocol_reads_coverage_unmeasurable(monkeypatch, resha,
                                                                          match):
    """Review fix 2 (was: raises). A variant protocol altered after 5a, or (its
    sha re-recorded) whose windows are no longer a subsequence of the run
    protocol's: that variant's normalised rows are NOT_EVALUABLE, grading
    never raises."""
    run_dir = _partial_run(monkeypatch)
    vpath = run_dir / "artifacts" / "variants" / "asset" / vc.VARIANT_PROTOCOL_FILENAME
    doc = json.loads(vpath.read_text(encoding="utf-8"))
    doc["windows"] = list(reversed(doc["windows"]))
    vpath.write_text(json.dumps(doc), encoding="utf-8")
    if resha:
        ipath = run_dir / "artifacts" / "variants" / "index.yaml"
        index = rpr.load_yaml(ipath)
        index["variants"]["asset"]["protocol_sha256"] = vc.protocol_sha256(vpath.read_bytes())
        rpr.save_yaml(ipath, index)
    _assert_coverage_unmeasurable(_evaluate(run_dir), match)


@pytest.mark.parametrize("damage,match", [
    ("delete", "unreadable"), ("alter", "not the file 5a froze"),
    ("pre_fix_index", rpr.RUN_PROTOCOL_SHA_KEY)],
    ids=["frozen_copy_missing", "frozen_copy_altered", "graded_before_the_frozen_copy"])
def test_unmeasurable_coverage_holds_only_that_variant(monkeypatch, damage, match):
    """Review fix 2: the frozen run protocol missing / altered, or an index
    written before it existed: the partial asset's normalised rows read
    NOT_EVALUABLE; the full-coverage base grades normally and passes."""
    run_dir = _partial_run(monkeypatch, with_base=True)
    _damage_frozen(run_dir, damage)
    ev = _evaluate(run_dir)
    _assert_coverage_unmeasurable(ev, match)
    assert ev["variants"]["base"]["result"] == "PASS" and ev["passing"] == ["base"]
    assert "coverage_unmeasurable" not in ev["variants"]["base"]


def test_unusable_index_coverage_record_reads_coverage_unmeasurable_under_v2(monkeypatch):
    run_dir = _partial_run(monkeypatch)
    ipath = run_dir / "artifacts" / "variants" / "index.yaml"
    index = rpr.load_yaml(ipath)
    index["variants"]["asset"]["coverage"]["windows_total"] = "96"
    rpr.save_yaml(ipath, index)
    _assert_coverage_unmeasurable(_evaluate(run_dir), "no usable windows_run")


def _damage_frozen(run_dir: Path, damage: str) -> None:
    frozen = run_dir / rpr.RUN_PROTOCOL_FROZEN_REL
    if damage == "delete":
        frozen.unlink()
    elif damage == "alter":
        doc = json.loads(frozen.read_text(encoding="utf-8"))
        doc["windows"] = doc["windows"][len(doc["windows"]) - N_COVERED:]
        frozen.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    else:  # an index 5a wrote before review fix 1: no run_protocol_sha256
        ipath = run_dir / "artifacts" / "variants" / "index.yaml"
        index = rpr.load_yaml(ipath)
        for info in index["variants"].values():
            info.pop(rpr.RUN_PROTOCOL_SHA_KEY, None)
        rpr.save_yaml(ipath, index)


# ---------------------------------------------------------------------------
# 3. Full coverage: byte-identical (G7)
# ---------------------------------------------------------------------------

def test_full_coverage_rows_are_byte_identical_and_never_normalised(monkeypatch):
    run_dir = _partial_run(monkeypatch, covered=96, trades=100)
    before = _evaluate(run_dir)

    def _boom(*_a, **_k):
        raise AssertionError("a full-coverage variant must not be normalised")
    monkeypatch.setattr(rpr, "_variant_coverage_days", _boom)
    monkeypatch.setattr(rpr, "_normalised_profit_bars", _boom)
    after = _evaluate(run_dir)
    strip = ("generated_at",)
    assert {k: v for k, v in before.items() if k not in strip} == \
        {k: v for k, v in after.items() if k not in strip}
    rows = _rows(after)
    for name in TIME_ROWS:
        assert "normalisation" not in (rows[name].get("detail") or {})
    assert rows["trade_count_min"]["threshold"] == 100
    assert rows["max_drawdown_pct_max"]["threshold"] == 20.0
    assert rows["cost_edge_ratio_min"]["detail"]["min_trades"] == 100
    assert "partial_coverage" not in after["variants"]["asset"]
    assert after["passing"] == ["asset"]


def test_f_equal_one_returns_the_bars_unchanged():
    bars = dict(V2_BARS)
    eff, norm = rpr._normalised_profit_bars(bars, (FULL_DAYS, FULL_DAYS))
    assert eff is bars and norm == {}


# ---------------------------------------------------------------------------
# 4. The floor binds when 100 * f < 60 (constructed: D-042's 0.60 minimum keeps
#    it inert in a real run, X2)
# ---------------------------------------------------------------------------

def test_floor_binds_below_60_percent():
    eff, norm = rpr._normalised_profit_bars(dict(V2_BARS), (50, 100))
    assert eff["trade_count_min"] == 60 and eff["cost_edge_min_trades"] == 60  # not 50
    assert eff["max_drawdown_pct_max"] == 20.0 * math.sqrt(0.5)
    assert norm["trade_count_min"]["floor"] == 60 and norm["trade_count_min"]["f"] == 0.5
    eff, _ = rpr._normalised_profit_bars(dict(V2_BARS), (61, 100))
    assert eff["trade_count_min"] == 61  # the rate term above the floor


def test_floor_binds_in_the_graded_row(monkeypatch):
    run_dir = _partial_run(monkeypatch)
    real = rpr._profit_bars_backtest_candidates

    def _half(rd, rid, **kw):
        out = real(rd, rid, **kw)
        out["asset"]["coverage_days"] = (1461, 2922)  # f = 0.5
        return out
    monkeypatch.setattr(rpr, "_profit_bars_backtest_candidates", _half)
    rows = _rows(_evaluate(run_dir))
    assert rows["trade_count_min"]["threshold"] == 60
    assert rows["cost_edge_ratio_min"]["detail"]["min_trades"] == 60


def test_f_is_the_exact_day_fraction_not_a_rounded_float(monkeypatch):
    """ceil(100 * 7/100) must be 7, not 8 (100 * 0.07 == 7.000000000000001) --
    and the wiring hands the helpers an exact fractions.Fraction, not a float
    (review fix 4: spied on the helpers' own argument)."""
    seen: list = []
    for name in ("normalised_trade_minimum", "scaled_drawdown_limit"):
        real = getattr(vc, name)

        def _spy(*args, _real=real, _name=name):
            seen.append((_name, args[1]))
            return _real(*args)
        monkeypatch.setattr(vc, name, _spy)
    bars = {**V2_BARS, "trade_count_min_floor": 1}
    eff, norm = rpr._normalised_profit_bars(bars, (7, 100))
    assert eff["trade_count_min"] == 7 and norm["trade_count_min"]["covered_days"] == 7
    assert sorted(n for n, _ in seen) == ["normalised_trade_minimum", "normalised_trade_minimum",
                                          "scaled_drawdown_limit"]
    for _, f in seen:
        assert type(f) is Fraction and f == Fraction(7, 100)


# ---------------------------------------------------------------------------
# 5. sign_consistent_by_era: the single-era rule (D-047 (4))
# ---------------------------------------------------------------------------

def _one_era_pr():
    return _protocol_result([_window("BTCUSDT", "2020-01", net_return_pct=1.0),
                             _window("BTCUSDT", "2020-02", net_return_pct=2.0)])


def _two_era_pr(sign2=1.0):
    return _protocol_result([_window("BTCUSDT", "2020-01", net_return_pct=1.0),
                             _window("BTCUSDT", "2024-03", net_return_pct=sign2)])


def test_single_era_base_variant_is_inconclusive_under_v2_only():
    pre = _menu_shaped_pre_reg([SCE])
    off = vce.evaluate_grid({"base": _one_era_pr()}, pre, {}, {})
    assert off["grid"]["sce"]["base"]["result"] == "PASS"  # X1: trivially, flag off
    on = vce.evaluate_grid({"base": _one_era_pr()}, pre, {}, {}, single_era_inconclusive=True)
    cell = on["grid"]["sce"]["base"]
    assert cell["result"] == "INCONCLUSIVE"
    assert cell["reason"] == f"{vc.SINGLE_ERA_REASON_PREFIX} era_2019_2023_full_feed"
    assert on["idea_status"] == "inconclusive"
    # flag off: the keyword absent or False is byte-identical
    assert yaml.safe_dump(vce.evaluate_grid({"base": _one_era_pr()}, pre, {}, {},
                                            single_era_inconclusive=False)) == yaml.safe_dump(off)


def test_single_era_zero_median_stays_fail_under_v2():
    """D-047 (4) as amended by the operator 2026-09-29 (S2b-3b review): a
    single era with a zero median stays FAIL under v2 exactly as flag off; only
    a nonzero single era reads INCONCLUSIVE."""
    pre = _menu_shaped_pre_reg([SCE])
    pr = _protocol_result([_window("BTCUSDT", "2020-01", net_return_pct=1.0),
                           _window("BTCUSDT", "2020-02", net_return_pct=-1.0)])
    off = vce.evaluate_grid({"v": pr}, pre, {}, {})
    on = vce.evaluate_grid({"v": pr}, pre, {}, {}, single_era_inconclusive=True)
    assert off["grid"]["sce"]["v"]["result"] == "FAIL"
    assert on["grid"]["sce"]["v"]["result"] == "FAIL"
    assert on["grid"] == off["grid"] and on["idea_status"] == off["idea_status"]
    # the nonzero single era next to it: INCONCLUSIVE `single_era:` under v2
    nz = vce.evaluate_grid({"v": _one_era_pr()}, pre, {}, {}, single_era_inconclusive=True)
    assert nz["grid"]["sce"]["v"]["result"] == "INCONCLUSIVE"
    assert nz["grid"]["sce"]["v"]["reason"].startswith(vc.SINGLE_ERA_REASON_PREFIX)


@pytest.mark.parametrize("sign2,expected", [(1.0, "PASS"), (-1.0, "FAIL")])
def test_two_eras_are_graded_as_before(sign2, expected):
    pre = _menu_shaped_pre_reg([SCE])
    off = vce.evaluate_grid({"v": _two_era_pr(sign2)}, pre, {}, {})
    on = vce.evaluate_grid({"v": _two_era_pr(sign2)}, pre, {}, {}, single_era_inconclusive=True)
    assert on["grid"]["sce"]["v"]["result"] == expected
    assert on["grid"] == off["grid"]


def test_per_symbol_cells_get_the_single_era_rule_too():
    crit = {**SCE, "symbol_reducer": "per_symbol_all"}
    pr = _protocol_result([_window("BTCUSDT", "2020-01", net_return_pct=1.0),
                           _window("BTCUSDT", "2024-03", net_return_pct=1.0),
                           _window("ETHUSDT", "2020-01", net_return_pct=1.0)])
    on = vce.evaluate_grid({"v": pr}, _menu_shaped_pre_reg([crit]), {}, {},
                           single_era_inconclusive=True)
    cell = on["grid"]["sce"]["v"]
    assert cell["per_symbol"]["BTCUSDT"]["result"] == "PASS"
    assert cell["per_symbol"]["ETHUSDT"]["result"] == "INCONCLUSIVE"
    assert cell["result"] == "INCONCLUSIVE"


def test_the_grid_validates_with_a_partial_column_once_the_cap_is_not_passed():
    pre = _menu_shaped_pre_reg([SCE])
    cols = {"base": _two_era_pr(), "asset": _two_era_pr()}
    capped = vce.evaluate_grid(cols, pre, {}, {},
                               partial_coverage_variants={"asset": "partial coverage: 10/13"})
    assert capped["idea_status"] == "inconclusive"
    assert vce.evaluate_grid(cols, pre, {}, {}, single_era_inconclusive=True)[
        "idea_status"] == "validated"


def test_grid_v2_kw_follows_the_flag():
    _set_orchestrator(V2_ON)
    assert rpr._grid_v2_kw() == {"single_era_inconclusive": True}
    _set_orchestrator(FULL_ON)
    assert rpr._grid_v2_kw() == {}


def _grid_recorder(monkeypatch):
    """Records evaluate_grid's keywords at protocol_execution and grades on a
    menu-shaped sign_consistent_by_era rule (metric `sharpe`: the stub's)."""
    seen: list = []
    real = vce.evaluate_grid
    crit = {**SCE, "metric": "sharpe"}

    def _rec(prs, _pre, brief, menu, **kw):
        seen.append(kw)
        return real(prs, _menu_shaped_pre_reg([crit]), brief, menu, **kw)
    monkeypatch.setattr(vce, "evaluate_grid", _rec)
    monkeypatch.setattr(vce, "_is_menu_shaped_pass_rule", lambda _pr: True)
    monkeypatch.setattr(rpr, "_grid_evaluation_enabled", lambda cfg=None: True)
    return seen


@pytest.mark.parametrize("v2", [False, True])
def test_protocol_execution_lifts_the_grid_cap_and_adds_the_era_rule_only_under_v2(
        monkeypatch, v2):
    import test_e061_c2_s2b_one_coin_per_variant as c2
    c2._set_flags(config_direct_authoring=True, variant_loop=True)
    windows, universe, layer1 = c2._partial_asset_world()
    run_dir, _ = c2._stage_index(f"run_98{int(v2)}", per_coin=True, monkeypatch=monkeypatch,
                                 windows=windows, universe=universe, layer1=layer1)
    monkeypatch.setattr(rpr, "_profit_bars_v2_enabled", lambda cfg=None: v2)
    seen = _grid_recorder(monkeypatch)
    c2._tool_stub(monkeypatch, [])
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_dir.name))
    assert len(seen) == 1
    grid = rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")
    assert sorted(grid["variants"]) == ["asset", "base", "design"]
    if v2:
        assert seen[0].get("single_era_inconclusive") is True
        assert "partial_coverage_variants" not in seen[0]
        assert "partial_coverage_variants" not in grid and grid["idea_status"] == "validated"
    else:
        assert "single_era_inconclusive" not in seen[0]
        assert list(seen[0]["partial_coverage_variants"]) == ["asset"]
        assert grid["idea_status"] == "inconclusive"
        assert list(grid["partial_coverage_variants"]) == ["asset"]


# ---------------------------------------------------------------------------
# 6. Legacy promote path: still capped with v2 on (G9)
# ---------------------------------------------------------------------------

def test_legacy_promote_path_keeps_the_cap_with_v2_on():
    import test_profit_bars_every_backtest as tpb
    tpb._set_orchestrator({**V2_ON, **VARIANT_LOOP_ON})
    tpb._write_bars({**tpb._VALID_BARS, **{k: V2_BARS[k] for k in V2_BARS if k not in V1_BARS}})
    run_dir = tpb._variant_run({"base": False, "design": True})
    arts = run_dir / "artifacts"
    bridge = rpr.load_yaml(arts / "variants" / "design" / "protocol_result.yaml")
    vproto = arts / "variants" / "design" / "protocol.json"
    vproto.write_text("{}", encoding="utf-8")
    bridge["protocol_file"] = str(vproto)
    rpr.save_yaml(arts / "protocol_result.yaml", bridge)
    rpr.save_yaml(arts / "promotion_audit.yaml", {"raw_median_sharpe": 1.4,
                                                  "deflated_sharpe_ratio": 0.99})
    before = rpr._evaluate_profit_bars(run_dir, tpb.RUN_ID, portfolio_basis=True)
    assert before["result"] == "PASS"
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    index["variants"]["design"].update({
        "protocol_path": "artifacts/variants/design/protocol.json",
        "coverage": {"windows_run": ["w1"], "windows_total": 2}})
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    after = rpr._evaluate_profit_bars(run_dir, tpb.RUN_ID, portfolio_basis=True)
    assert after["result"] == "FAIL"
    for b in after["bars"]:
        if b["name"] in vc.D042_TIME_DEPENDENT_BARS:
            assert b["result"] == "NOT_EVALUABLE"
            assert "temporary until E-062 S2b" in b["not_evaluable_reason"]


# ---------------------------------------------------------------------------
# 7. The spend re-derives the normalised thresholds
# ---------------------------------------------------------------------------

def _spend_ready(monkeypatch, run_dir) -> dict:
    """The evaluation (bars sha recorded), the raised stop and a spend decision
    for the partial asset; the spend checks outside this slice are stubbed
    (they have their own suites). Review fix 4: the evaluation is NOT stubbed --
    the spend reads it back from profit_bars_evaluation.yaml (the real save ->
    load YAML round trip) before comparing its rows. Returns the evaluation as
    grading returned it (in memory)."""
    ev = _evaluate(run_dir, record_bars_sha=True)
    stop = ev["generated_at"]
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["profit_bars_stop_evaluation"] = stop
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    monkeypatch.setattr(rpr, "_idea_hypothesis_id", lambda rd: "H-S2B3B")
    monkeypatch.setattr(rpr, "_holdout_already_spent", lambda h: False)
    monkeypatch.setattr(rpr, "_other_pending_spends", lambda rid: [])
    monkeypatch.setattr(rpr, "_dsr_on_current_ledger", lambda *a: {"stub": True})
    (run_dir / "artifacts" / rpr.HOLDOUT_DECISION_FILE).write_text(yaml.safe_dump({
        "decision": "spend", "run_id": RUN_ID, "profit_bars_stop_evaluation": stop,
        "variant_id": "asset", "ratified_by": "operator", "ratified_at": "2020-01-01",
        "trial_ledgers_merged": True}), encoding="utf-8")
    return ev


def _saved_evaluation_path(run_dir: Path) -> Path:
    return run_dir / "artifacts" / "profit_bars_evaluation.yaml"


def _validate(run_dir):
    return rpr._validate_holdout_decision(run_dir, RUN_ID,
                                          rpr.load_yaml(run_dir / "pipeline_state.yaml"))


def test_spend_accepts_the_thresholds_its_coverage_gives(monkeypatch):
    run_dir = _partial_run(monkeypatch)
    ev = _spend_ready(monkeypatch, run_dir)
    assert ev["passing"] == ["asset"]
    # the spend compares the rows as they come back from disk
    saved = rpr.load_yaml(_saved_evaluation_path(run_dir))
    assert _rows(saved)["trade_count_min"]["detail"]["normalisation"] == \
        _rows(ev)["trade_count_min"]["detail"]["normalisation"]
    record = _validate(run_dir)
    assert record["decision"] == "spend" and record["variant_id"] == "asset"
    assert "normalisation" not in json.dumps(record)  # the record's shape is unchanged


@pytest.mark.parametrize("row,field,value", [
    ("trade_count_min", "threshold", 100),                  # the full-coverage minimum
    ("max_drawdown_pct_max", "threshold", 20.0),            # the full-coverage limit
    ("cost_edge_ratio_min", "min_trades", 100),             # the full-coverage floor
    ("trade_count_min", "normalisation", None),             # normalisation dropped
])
def test_spend_refuses_a_silent_full_coverage_threshold(monkeypatch, row, field, value):
    """The saved evaluation edited on disk (the spend reads it back)."""
    run_dir = _partial_run(monkeypatch)
    _spend_ready(monkeypatch, run_dir)
    path = _saved_evaluation_path(run_dir)
    saved = rpr.load_yaml(path)
    r = _rows(saved)[row]
    if field == "threshold":
        r["threshold"] = value
    elif field == "min_trades":
        r["detail"]["min_trades"] = value
    else:
        r["detail"].pop("normalisation")
    rpr.save_yaml(path, saved)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        _validate(run_dir)
    assert exc.value.code == "bars_changed" and row in exc.value.detail


def test_spend_refuses_when_the_coverage_changed_since_grading(monkeypatch):
    """The index now says full coverage: the graded normalised thresholds no
    longer match what the coverage gives -> refused."""
    run_dir = _partial_run(monkeypatch)
    _spend_ready(monkeypatch, run_dir)
    path = run_dir / "artifacts" / "variants" / "index.yaml"
    index = rpr.load_yaml(path)
    index["variants"]["asset"]["coverage"]["windows_total"] = N_COVERED
    rpr.save_yaml(path, index)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        _validate(run_dir)
    assert exc.value.code == "bars_changed" and "trade_count_min" in exc.value.detail


def test_spend_refuses_when_the_coverage_cannot_be_re_derived(monkeypatch):
    """Review fix 1 (declared): the variant's protocol gone -> the new code
    normalisation_unverifiable (was bars_changed): the thresholds cannot be
    re-derived, nothing was shown to have changed."""
    run_dir = _partial_run(monkeypatch)
    _spend_ready(monkeypatch, run_dir)
    (run_dir / "artifacts" / "variants" / "asset" / vc.VARIANT_PROTOCOL_FILENAME).unlink()
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        _validate(run_dir)
    assert exc.value.code == "normalisation_unverifiable"
    assert "cannot be re-derived" in exc.value.detail


def test_spend_ignores_the_shared_protocol_edited_after_grading(monkeypatch):
    """Review fix 1: the shared protocols/*.json edited after grading (here:
    cut to the asset's own 58 windows, so a re-resolution would read f == 1
    and full-coverage thresholds) -- the spend still derives the graded
    thresholds from 5a's frozen copy and accepts. Pre-fix it re-resolved the
    shared file and refused."""
    run_dir = _partial_run(monkeypatch)
    _spend_ready(monkeypatch, run_dir)
    shared = _run_proto_path()
    doc = json.loads(shared.read_text(encoding="utf-8"))
    doc["windows"] = doc["windows"][len(doc["windows"]) - N_COVERED:]
    shared.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    monkeypatch.setattr(rpr, "_resolve_protocol_path", lambda rd, rid: shared)
    assert _validate(run_dir)["variant_id"] == "asset"
    # the frozen copy is what grading measured against
    rows = _rows(rpr.load_yaml(_saved_evaluation_path(run_dir)))
    assert rows["trade_count_min"]["threshold"] == 61
    assert rows["trade_count_min"]["detail"]["normalisation"]["full_days"] == FULL_DAYS


def test_spend_is_side_effect_free_when_a_later_run_claimed_the_escalation(monkeypatch):
    """Review fix 1: campaign_state.last_escalation claimed by a LATER run (the
    real resolver would flag stale_escalation_unclaimed on THIS run's
    pipeline_state and raise). The spend never calls the resolver: it
    accepts, and pipeline_state.yaml is byte-for-byte untouched."""
    run_dir = _partial_run(monkeypatch)
    _spend_ready(monkeypatch, run_dir)
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    state["last_escalation"] = {"target": "timeframe", "detail": "4h",
                                "protocol_path": str(_run_proto_path()),
                                "claimed_by_run": "run_999"}
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    calls: list = []

    def _spy(rd, rid):
        calls.append(rid)
        return _REAL_RESOLVE(rd, rid)
    monkeypatch.setattr(rpr, "_resolve_protocol_path", _spy)
    ps = run_dir / "pipeline_state.yaml"
    before = ps.read_bytes()
    assert _validate(run_dir)["variant_id"] == "asset"
    assert calls == [] and ps.read_bytes() == before
    # the scenario is live: the real resolver WOULD have written the flag
    with pytest.raises(RuntimeError, match="B10"):
        _REAL_RESOLVE(run_dir, RUN_ID)
    assert rpr.load_yaml(ps)["flags"]["stale_escalation_unclaimed"] is True


@pytest.mark.parametrize("damage", ["delete", "alter", "pre_fix_index"],
                         ids=["frozen_copy_missing", "frozen_copy_altered",
                              "graded_before_the_frozen_copy"])
def test_spend_refuses_normalisation_unverifiable_without_the_frozen_copy(monkeypatch, damage):
    """Review fix 1: the frozen run protocol missing or altered after grading,
    or a run graded before it existed (its index records no
    run_protocol_sha256) -> normalisation_unverifiable, never a silent
    full-coverage threshold and never bars_changed."""
    run_dir = _partial_run(monkeypatch)
    ev = _spend_ready(monkeypatch, run_dir)
    assert ev["passing"] == ["asset"]
    _damage_frozen(run_dir, damage)
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        _validate(run_dir)
    assert exc.value.code == "normalisation_unverifiable"
    assert "cannot be re-derived" in exc.value.detail


def test_spend_of_a_full_coverage_variant_passes_the_recheck(monkeypatch):
    run_dir = _partial_run(monkeypatch, covered=96, trades=100)
    _spend_ready(monkeypatch, run_dir)
    assert _validate(run_dir)["variant_id"] == "asset"


# ---------------------------------------------------------------------------
# 7b. Review fix 1 at 5a: the run protocol is resolved once and frozen
# ---------------------------------------------------------------------------

def test_5a_freezes_the_run_protocol_once_and_records_its_sha(monkeypatch):
    import test_e061_c2_s2b_one_coin_per_variant as c2
    c2._set_flags(config_direct_authoring=True, variant_loop=True)
    c2._copy_coin_configs()
    source_path = c2._run_protocol_file(monkeypatch, c2._months("2022-01", 6))
    calls: list = []
    monkeypatch.setattr(rpr, "_resolve_protocol_path",
                        lambda rd, rid: (calls.append(rid), source_path)[1])
    c2._ok_subprocess(monkeypatch)
    run_dir = c2._run_5a("run_970", c2.PER_COIN_PATCHES)
    assert calls == ["run_970"]  # resolved ONCE, by the freeze
    raw = source_path.read_bytes()
    frozen = run_dir / rpr.RUN_PROTOCOL_FROZEN_REL
    assert frozen.read_bytes() == raw
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    for vid in ("base", "design", "asset"):
        assert index[vid][rpr.RUN_PROTOCOL_SHA_KEY] == vc.protocol_sha256(raw)
    # the shared protocol edited after 5a: coverage still reads the frozen copy
    source_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rpr, "_resolve_protocol_path", _no_resolve)
    covered, full = rpr._variant_coverage_days(run_dir, "run_970", index["base"])
    assert covered == full > 0


def test_5a_without_per_coin_mode_freezes_nothing(monkeypatch):
    import test_e061_c2_s2b_one_coin_per_variant as c2
    c2._set_flags(config_direct_authoring=True, variant_loop=True)
    c2._run_protocol_file(monkeypatch, c2._months("2022-01", 6))
    monkeypatch.setattr(rpr, "_freeze_run_protocol", _no_resolve)
    c2._ok_subprocess(monkeypatch)
    run_dir = c2._run_5a("run_971", c2._strip_coin(c2.PER_COIN_PATCHES))
    assert not (run_dir / rpr.RUN_PROTOCOL_FROZEN_REL).exists()
    index = rpr.load_yaml(run_dir / "artifacts" / "variants" / "index.yaml")["variants"]
    assert all(rpr.RUN_PROTOCOL_SHA_KEY not in e for e in index.values())


# ---------------------------------------------------------------------------
# 7c. Review fix 4: the grid's profit-bars grader never grades a partial
#     column on un-normalised bars
# ---------------------------------------------------------------------------

def test_grid_grader_holds_a_partial_column_not_evaluable_under_v2(monkeypatch):
    """100 trades and a 17 % drawdown: on the un-normalised bars (limit 20 %)
    the grid grader would PASS the partial asset (pre-fix); its D-047 rows now
    read NOT_EVALUABLE and the profit_bars cell INCONCLUSIVE."""
    run_dir = _partial_run(monkeypatch, trades=100, dd=_r_for(17.0))
    graded = rpr._profit_bars_grid_grader(run_dir, RUN_ID)("asset")
    rows = {r["name"]: r for r in graded["bars"]}
    for name in TIME_ROWS:
        assert rows[name]["result"] == "NOT_EVALUABLE"
        assert "does not normalise" in rows[name]["not_evaluable_reason"]
    assert graded["result"] == "FAIL"
    cell = vce._evaluate_profit_bars_cell({"id": "pb"}, "asset", lambda vid: graded)
    assert cell["result"] == "INCONCLUSIVE"
    # branch 3, which normalises, FAILs it on the scaled 15.55 % limit
    assert _rows(_evaluate(run_dir))["max_drawdown_pct_max"]["result"] == "FAIL"


def test_grid_grader_full_coverage_column_unchanged_under_v2(monkeypatch):
    run_dir = _partial_run(monkeypatch, covered=96, trades=100)
    graded = rpr._profit_bars_grid_grader(run_dir, RUN_ID)("asset")
    assert graded["result"] == "PASS"
    assert all(r["result"] == "PASS" for r in graded["bars"])


def test_grid_grader_flag_off_reads_no_index(monkeypatch):
    run_dir = _partial_run(monkeypatch, orchestrator=V1_LOOP, bars=V1_BARS)
    monkeypatch.setattr(rpr, "_hold_rows_not_evaluable", _no_resolve)
    graded = rpr._profit_bars_grid_grader(run_dir, RUN_ID)("asset")
    assert all(r.get("not_evaluable_reason") is None or "does not normalise" not in
               r["not_evaluable_reason"] for r in graded["bars"])


# ---------------------------------------------------------------------------
# 8. The loader key
# ---------------------------------------------------------------------------

def test_v2_loader_refuses_a_bars_file_without_the_floor_loudly():
    path = _write_bars({k: v for k, v in V2_BARS.items() if k != "trade_count_min_floor"})
    assert rpr._load_profitability_bars(path)["sharpe_min"] == 1.0  # v1 ignores it
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="trade_count_min_floor"):
        rpr._load_profitability_bars(path, v2=True)


def test_v2_evaluation_without_the_floor_fails_before_grading(monkeypatch):
    run_dir = _partial_run(monkeypatch)
    _write_bars({k: v for k, v in V2_BARS.items() if k != "trade_count_min_floor"})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="trade_count_min_floor"):
        _evaluate(run_dir)
    assert not (run_dir / "artifacts" / "profit_bars_evaluation.yaml").exists()


@pytest.mark.parametrize("bad", [0, -1, 101, True, 60.0, "60", None])
def test_v2_loader_refuses_a_bad_floor(bad):
    path = _write_bars({**V2_BARS, "trade_count_min_floor": bad})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="trade_count_min_floor"):
        rpr._load_profitability_bars(path, v2=True)


def test_v2_loader_refuses_a_floor_above_the_cost_floor():
    path = _write_bars({**V2_BARS, "cost_edge_min_trades": 50, "trade_count_min_floor": 60})
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="trade_count_min_floor"):
        rpr._load_profitability_bars(path, v2=True)


def test_committed_bars_file_carries_the_floor_60_unsigned():
    real = SR_ROOT / "config" / "profitability_bars.yaml"
    doc = rpr._load_profitability_bars(real, v2=True)
    assert doc["trade_count_min_floor"] == 60
    assert doc["ratified_by"] is None and doc["ratified_at"] is None
