"""
D-185 (operator direction 2026-10-24, PR-2) -- the deflated Sharpe's N by structure,
behind orchestrator.dsr_same_structure (off by default).

Covers:
  1. structure_hash: invariant to every parameter value; sensitive to the detector
     mode, component class order and class, transform op names and order (both
     lists), the sign of a weight, of a scaling_factor and of a `scale` factor, and
     the sizing kind.
  2. timeframe: one bar size, one string ("1h" / "60m" / 3600).
  3. The flag reader.
  4. Trial rows: flag off, every row exactly as before; flag on, exactly two more
     keys (structure_hash, timeframe) at the three row sites, a superseded attempt
     keeps the key; a protocol_execution run writes the protocol's timeframe.
  5. N and K by key: only (hash, timeframe) rows after exclusion and dedup (the dedup
     key carries the timeframe, direction d1), unkeyed rows in no key's N, N >= K, the
     candidate's own row in its key's N.
  6. Branch 3 end to end: flag off dsr_basis and the DSR row as before; flag on the
     key and both counts in dsr_basis and in the DSR row; an unkeyed candidate falls
     back to the campaign-wide counts (and keeps the N >= 2 rule); a keyed candidate alone on
     its key (N = 1) is graded at SR0 = 0 (direction a); N = 2 is unchanged.
  7. The holdout spend keeps the campaign-wide N.
  8. The backfill tool: a dry run writes nothing, --write appends to the overlay only,
     rows without a saved config stay unkeyed, a re-run changes nothing; the dry run
     prints the four counts (keyed, unkeyed, distinct keys, singleton keys) and nothing
     else; the DSR reads the overlay under the flag.
"""
import copy
import hashlib
import json
import math
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import backfill_structure_hash as bsh  # noqa: E402
import deflate_sharpe as ds  # noqa: E402
import portfolio_whole_test as pwt  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import structure_key as sk  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e062_s2b1_profit_bars_v2 import V2_ON  # noqa: E402
from test_e062_s2b2b_dsr_wiring import (  # noqa: E402
    _block, _dsr_row, _edit_rows, _evaluate, _hand_dsr, _own_row, _run_protocol_execution, _state,
    _v2_run, _z)

SS_ON = {**V2_ON, "dsr_same_structure": {"enabled": True}}
H1, H2 = "a" * 64, "b" * 64


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# 1. structure_hash
# ---------------------------------------------------------------------------

def _config() -> dict:
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown", "er_period": 20},
        "strategies": {
            "warmup": 51,
            "sizing": {"kind": "vol_target", "window": 60, "target_annual_vol": 0.2,
                       "periods_per_year": 365, "max_allocation": 2},
            "regimes": {
                "unknown": {"components": [
                    {"id": "a", "class": "strategies.strategy_components.DonchianBreakoutComponent",
                     "params": {"period": 250, "scaling_factor": 1.5}, "weight": 0.7, "lookback": 500,
                     "transforms": [{"op": "standardise", "params": {"window": 250}},
                                    {"op": "clip", "params": {"min": 0, "max": 20}},
                                    {"op": "scale", "params": {"factor": 10.0}}],
                     "history_transforms": [{"op": "vol_normalize"}]},
                    {"id": "b", "class": "strategies.strategy_components.PriceEvolutionComponent",
                     "params": {"period": 1, "scaling_factor": 2.0}, "weight": 0.3,
                     "transforms": [{"op": "zscore"}, {"op": "negate"}]},
                ]},
                "trending": None, "mean_reversion": None, "chop": None,
            }},
        "aux_feeds": [],
    }


def _h(cfg) -> str:
    return sk.compute_structure_hash(cfg)


def test_hash_is_a_sha256_and_the_orchestrator_wrapper_agrees():
    cfg = _config()
    assert len(_h(cfg)) == 64 and set(_h(cfg)) <= set("0123456789abcdef")
    assert rpr._compute_structure_hash(cfg) == _h(cfg)


def test_hash_is_invariant_to_every_parameter_value():
    base = _h(_config())
    c = _config()
    c["regime_detector"]["er_period"] = 5
    c["regime_detector"]["rules"] = [{"x": 1}]
    s = c["strategies"]
    s["warmup"] = 2
    s["sizing"].update(window=20, target_annual_vol=0.5, periods_per_year=8760, max_allocation=3)
    comp_a, comp_b = s["regimes"]["unknown"]["components"]
    comp_a["params"].update(period=10, scaling_factor=99.0)          # magnitude only
    comp_a["weight"] = 123.4                                         # magnitude only
    comp_a["lookback"] = 9
    comp_a["id"], comp_b["id"] = "renamed_a", "renamed_b"            # ids are labels
    comp_a["transforms"][0]["params"]["window"] = 3
    comp_a["transforms"][1]["params"] = {"min": -5, "max": 5}
    comp_a["transforms"][2]["params"]["factor"] = 0.001              # positive magnitude only
    comp_b["params"]["period"] = 77
    comp_b["weight"] = 1e-9
    c["aux_feeds"] = ["funding_rate"]                                # outside the recipe
    assert _h(c) == base


def test_hash_is_invariant_to_key_order_and_regime_order_in_the_file():
    cfg = _config()
    shuffled = json.loads(json.dumps(cfg, sort_keys=True))
    shuffled["strategies"]["regimes"] = dict(reversed(list(shuffled["strategies"]["regimes"].items())))
    assert _h(shuffled) == _h(cfg)
    # a null regime is not part of the structure
    del cfg["strategies"]["regimes"]["chop"]
    assert _h(cfg) == _h(_config())


@pytest.mark.parametrize("edit,why", [
    (lambda c: c["regime_detector"].update(mode="er_vol"), "detector mode"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"].reverse(), "component order"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].update(
        {"class": "strategies.strategy_components.KeltnerComponent"}), "component class"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"].pop(), "component count"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["transforms"].reverse(),
     "op order"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["transforms"][1].update(op="sigmoid"),
     "op name"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["transforms"].pop(), "op count"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].update(
        history_transforms=[{"op": "ema"}]), "history op name"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["transforms"].append(
        c["strategies"]["regimes"]["unknown"]["components"][0].pop("history_transforms")[0]),
     "an op moved between the two lists"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].update(weight=-0.7), "weight sign"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].update(weight=0), "weight zero"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["params"].update(
        scaling_factor=-1.5), "scaling_factor sign"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["params"].update(
        scaling_factor=0), "scaling_factor zero"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["params"].update(
        scaling_factor="x"), "scaling_factor not a number"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].pop("weight"),
     "weight absent (no default: the engine indexes cfg['weight'])"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["transforms"][2]["params"].update(
        factor=-10.0), "scale factor sign"),
    (lambda c: c["strategies"]["sizing"].update(kind="other_kind"), "sizing kind"),
    (lambda c: c["strategies"].pop("sizing"), "sizing absent"),
    (lambda c: c["strategies"]["regimes"].update(
        trending={"components": [{"id": "t", "class": "x.Y", "weight": 1, "transforms": []}]}),
     "a component in another regime"),
])
def test_hash_is_sensitive_to_structure(edit, why):
    cfg = _config()
    edit(cfg)
    assert _h(cfg) != _h(_config()), why


def test_a_missing_scaling_factor_hashes_as_the_positive_default():
    # Every component class defaults scaling_factor to a positive number
    # (strategy_components.py:234-693), so absent == an explicit positive value (any magnitude);
    # absent != an explicit negative (that flips the bet). A missing weight has no default.
    comp = lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]  # noqa: E731
    absent = _config()
    comp(absent)["params"].pop("scaling_factor")
    assert _h(absent) == _h(_config())                    # 1.5 in the base config
    assert sk.structure_dict(absent)["regimes"]["unknown"][0]["scaling_factor_sign"] == 1
    no_params = _config()
    del comp(no_params)["params"]
    assert _h(no_params) == _h(_config())
    negative = _config()
    comp(negative)["params"]["scaling_factor"] = -1.5
    assert _h(negative) != _h(absent)
    gone = _config()
    del comp(gone)["weight"]
    assert sk.structure_dict(gone)["regimes"]["unknown"][0]["weight_sign"] is None


def test_every_component_default_scaling_factor_is_positive():
    # The premise of the +1 above, read from the source rather than assumed.
    import re
    src = (SR_ROOT.parent / "trading-bot" / "strategies" / "strategy_components.py").read_text(
        encoding="utf-8").splitlines()[233:693]
    defaults = [float(m.group(1)) for line in src
                for m in [re.search(r"get\('scaling_factor',\s*([-0-9.]+)\)", line)] if m]
    assert len(defaults) == 11 and all(d > 0 for d in defaults), defaults


def test_hash_of_a_real_config_ignores_its_parameters():
    fixture = SR_ROOT / "tests" / "fixtures" / "d176" / "run_099_strategy_config.json"
    cfg = json.loads(fixture.read_text(encoding="utf-8"))
    changed = copy.deepcopy(cfg)
    comp = changed["strategies"]["regimes"]["unknown"]["components"][0]
    comp["params"]["period"] = 40
    for step in comp["transforms"]:
        for k, v in (step.get("params") or {}).items():
            if isinstance(v, (int, float)) and v > 0:
                step["params"][k] = v + 1
    assert _h(changed) == _h(cfg)


def test_hash_refuses_a_non_mapping():
    with pytest.raises(ValueError, match="mapping"):
        sk.compute_structure_hash([])


# ---------------------------------------------------------------------------
# 2. timeframe
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tf,want", [
    ("1h", "1h"), ("60m", "1h"), (3600, "1h"), (" 1H ", "1h"), ("4h", "4h"), ("240m", "4h"),
    ("1d", "1d"), ("24h", "1d"), ("1w", "1w"), ("15m", "15m"), ("90m", "90m"), ("30s", "30s"),
])
def test_one_bar_size_has_one_string(tf, want):
    assert sk.canonical_timeframe(tf) == want


@pytest.mark.parametrize("bad", ["", "abc", None, True, -5, 0, 0.4, [], "1x"])
def test_an_unparseable_timeframe_is_none(bad):
    assert sk.canonical_timeframe(bad) is None


def test_protocol_timeframe_defaults_to_1h_like_run_protocol(tmp_path):
    assert sk.protocol_timeframe({"symbols": ["BTCUSDT"]}) == "1h"
    assert sk.protocol_timeframe({"timeframe": "60m"}) == "1h"
    assert sk.protocol_timeframe({"timeframe": "garbage"}) is None
    assert sk.protocol_timeframe("not a mapping") is None
    for name, text in (("p.json", json.dumps({"timeframe": "4h"})), ("p.yaml", "timeframe: 4h\n")):
        (tmp_path / name).write_text(text, encoding="utf-8")
        assert sk.read_protocol_timeframe(tmp_path / name) == "4h"
    assert sk.read_protocol_timeframe(tmp_path / "missing.json") is None
    (tmp_path / "bad.json").write_text("{not json", encoding="utf-8")
    assert sk.read_protocol_timeframe(tmp_path / "bad.json") is None


# ---------------------------------------------------------------------------
# 3. the flag reader
# ---------------------------------------------------------------------------

def test_flag_is_off_when_absent_and_a_non_bool_raises():
    _set_orchestrator(None)
    assert rpr._dsr_same_structure_enabled() is False
    _set_orchestrator({"dsr_same_structure": {}})
    assert rpr._dsr_same_structure_enabled() is False
    _set_orchestrator({"dsr_same_structure": {"enabled": False}})
    assert rpr._dsr_same_structure_enabled() is False
    _set_orchestrator({"dsr_same_structure": {"enabled": True}})
    assert rpr._dsr_same_structure_enabled() is True
    _set_orchestrator({"dsr_same_structure": {"enabled": "true"}})
    with pytest.raises(ValueError, match="dsr_same_structure"):
        rpr._dsr_same_structure_enabled()


def test_committed_config_has_the_flag_off_and_the_preflight_reads_it():
    doc = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert doc["orchestrator"]["dsr_same_structure"] == {"enabled": False}
    import run_campaign
    assert run_campaign._flag_readers()["dsr_same_structure"] is rpr._dsr_same_structure_enabled


# ---------------------------------------------------------------------------
# 4. trial rows
# ---------------------------------------------------------------------------

LEGACY_BACKTEST_KEYS = {"trial_id", "source", "sharpe", "expectancy_bps", "n_trades",
                        "statistic_valid", "below_floor_pct", "forecast_hash"}
LEGACY_FAILED_KEYS = {"trial_id", "source", "sharpe", "expectancy_bps", "n_trades",
                      "statistic_valid", "forecast_hash", "error"}


def _fresh_ledger():
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": []})


def _cfg_file(tmp_path, name="cfg.json", cfg=None) -> Path:
    p = tmp_path / name
    p.write_text(json.dumps(cfg if cfg is not None else _config()), encoding="utf-8")
    return p


def _record(tmp_path, with_flag, run_id="run_001", **kw):
    _set_orchestrator({"dsr_same_structure": {"enabled": True}} if with_flag else None)
    _fresh_ledger()
    rpr._record_backtest_trial(run_id, {"per_symbol_summary": {}}, _cfg_file(tmp_path), **kw)
    return _state()["trial_sharpes"][0]


def test_backtest_row_flag_off_is_the_legacy_row_and_flag_on_adds_exactly_the_key(tmp_path):
    off = _record(tmp_path, False, timeframe="60m")  # even handed a timeframe: off writes nothing
    assert set(off) == LEGACY_BACKTEST_KEYS
    on = _record(tmp_path, True, timeframe="60m")
    assert set(on) == LEGACY_BACKTEST_KEYS | {"structure_hash", "timeframe"}
    assert {k: v for k, v in on.items() if k not in ("structure_hash", "timeframe")} == off
    assert on["structure_hash"] == _h(_config()) and on["timeframe"] == "1h"


def test_backtest_row_flag_on_without_a_timeframe_is_half_keyed_and_so_unkeyed(tmp_path):
    row = _record(tmp_path, True)
    assert row["structure_hash"] == _h(_config()) and "timeframe" not in row
    assert sk.row_structure_key(row) is None


def test_failed_row_flag_off_is_the_legacy_row_and_flag_on_adds_the_key(tmp_path):
    for with_flag in (False, True):
        _set_orchestrator({"dsr_same_structure": {"enabled": True}} if with_flag else None)
        _fresh_ledger()
        rpr._record_failed_backtest_trial("run_002", _cfg_file(tmp_path), "boom", timeframe="4h")
        row = _state()["trial_sharpes"][0]
        want = LEGACY_FAILED_KEYS | ({"structure_hash", "timeframe"} if with_flag else set())
        assert set(row) == want
    assert row["timeframe"] == "4h" and row["structure_hash"] == _h(_config())


def test_failed_row_whose_config_is_unreadable_is_unkeyed_not_a_crash(tmp_path):
    _set_orchestrator({"dsr_same_structure": {"enabled": True}})
    _fresh_ledger()
    rpr._record_failed_backtest_trial("run_002", tmp_path / "no_such_dir", "boom", timeframe="4h")
    row = _state()["trial_sharpes"][0]
    assert "structure_hash" not in row and row["timeframe"] == "4h"
    assert sk.row_structure_key(row) is None


def test_a_replaced_attempt_keeps_the_key_only_with_the_flag(tmp_path):
    old = {"trial_id": "run_001", "source": "backtest", "protocol_run_id": "p1", "sharpe": 0.5,
           "forecast_hash": "fh", "whole_test": {"status": "ok", "reason": None},
           "structure_hash": H1, "timeframe": "1h"}
    _set_orchestrator(None)
    off = rpr._superseded_attempt(old)
    assert set(off) == {"protocol_run_id", "sharpe", "forecast_hash", "whole_test_status",
                        "whole_test_reason"}
    _set_orchestrator({"dsr_same_structure": {"enabled": True}})
    on = rpr._superseded_attempt(old)
    assert {k: v for k, v in on.items() if k not in ("structure_hash", "timeframe")} == off
    assert on["structure_hash"] == H1 and on["timeframe"] == "1h"
    legacy_old = {k: v for k, v in old.items() if k not in ("structure_hash", "timeframe")}
    assert rpr._superseded_attempt(legacy_old) == off  # a row with no key: nothing invented


def test_trial_timeframe_kw_reads_the_protocol_file_only_with_the_flag(tmp_path):
    proto = tmp_path / "p.json"
    proto.write_text(json.dumps({"symbols": ["BTCUSDT"], "timeframe": "240m", "windows": []}),
                     encoding="utf-8")
    _set_orchestrator(None)
    assert rpr._trial_timeframe_kw(proto) == {}
    _set_orchestrator({"dsr_same_structure": {"enabled": True}})
    assert rpr._trial_timeframe_kw(proto) == {"timeframe": "4h"}
    assert rpr._trial_timeframe_kw(tmp_path / "missing.json") == {"timeframe": None}


def test_protocol_execution_writes_the_protocols_timeframe_with_the_flag(monkeypatch):
    # The flag is patched at its reader (as the neighbours patch profit_bars_v2): the full
    # flag set would switch on stages this test does not build.
    _run_protocol_execution(monkeypatch, "run_931", v2=False)
    off = _own_row("run_931")
    assert "structure_hash" not in off and "timeframe" not in off
    monkeypatch.setattr(rpr, "_dsr_same_structure_enabled", lambda cfg=None: True)
    _run_protocol_execution(monkeypatch, "run_932", v2=False)
    on = _own_row("run_932")
    assert on["timeframe"] == "1d"  # _write_protocol's protocol
    assert on["structure_hash"] == _h({})  # the stub candidate config is {}
    assert set(on) - {"structure_hash", "timeframe"} == set(off)


# ---------------------------------------------------------------------------
# 5. N and K by key
# ---------------------------------------------------------------------------

def _row(tid, h=H1, tf="1h", sr=0.01, fh=None, **extra):
    r = {"trial_id": tid, "source": "backtest", "statistic_valid": "sharpe", "sharpe": 0.1,
         "forecast_hash": fh or f"fh-{tid}", "whole_test": _block(sr)}
    if h is not None:
        r["structure_hash"] = h
    if tf is not None:
        r["timeframe"] = tf
    r.update(extra)
    return r


def test_n_counts_only_the_same_hash_and_timeframe_after_exclusion_and_dedup():
    rows = [
        _row("r1", H1, "1h"), _row("r2", H1, "1h"), _row("r3", H1, "1h"),     # the key: N 3
        _row("r4", H2, "1h"), _row("r5", H1, "4h"),                           # other keys
        _row("r6", None, None), _row("r7", H1, None), _row("r8", None, "1h"),  # unkeyed
        _row("r9", H1, "1h", invalidated_artifact=True),                      # excluded first
        _row("r10", H1, "1h", fh="fh-r1"),                                    # dedup onto r1
        {"trial_id": "r11", "source": "prescreen", "statistic_valid": "sharpe", "sharpe": 0.2,
         "forecast_hash": "fh-r11", "structure_hash": H1, "timeframe": "1h"},  # counts in N, not K
    ]
    got = ds.select_same_structure_sample(rows, (H1, "1h"))
    assert got["N"] == 4 and got["K"] == 3 and got["N"] >= got["K"]
    assert [x["trial_id"] for x in got["rows"]] == ["r1", "r2", "r3"]
    assert got["srs"] == [0.01, 0.01, 0.01]
    assert got["key"] == (H1, "1h")
    full = ds.select_same_basis_sample(rows)
    assert got["N_campaign"] == full["N"] and got["K_campaign"] == full["K"]
    assert got["N"] < full["N"] and got["K"] < full["K"]
    for key, n in (((H2, "1h"), 1), ((H1, "4h"), 1), (("c" * 64, "1h"), 0)):
        assert ds.select_same_structure_sample(rows, key)["N"] == n


def test_same_config_and_fold_on_two_bar_sizes_counts_in_each_own_key():
    # D-185 direction d1: the same-structure dedup key carries the row's canonical timeframe,
    # so one forecast_hash + fold on 1h and on 4h are two trials, each in its own key.
    rows = [_row("r1", H1, "1h", fh="same", fold="fold_a"),
            _row("r2", H1, "4h", fh="same", fold="fold_a")]
    for key in ((H1, "1h"), (H1, "4h")):
        got = ds.select_same_structure_sample(rows, key)
        assert got["N"] == 1 and got["K"] == 1
    # the campaign-wide count (and so the spend) still collapses them: held, not built
    assert ds.select_same_basis_sample(rows)["N"] == 1
    assert ds.select_same_structure_sample(rows, (H1, "1h"))["N_campaign"] == 1
    # a true duplicate (same config, fold AND timeframe) still collapses in the key
    dup = rows + [_row("r3", H1, "60m", fh="same", fold="fold_a")]  # "60m" is "1h"
    assert ds.select_same_structure_sample(dup, (H1, "1h"))["N"] == 1


def test_the_timeframe_in_the_dedup_key_never_splits_a_row_without_one():
    rows = [_row("r1", None, None, fh="same"), _row("r2", None, None, fh="same")]
    kept, removed = ds.deduplicate_trials(rows, timeframe_in_key=True)
    assert [r["trial_id"] for r in kept] == ["r1"] and removed == 1
    assert ds.deduplicate_trials(rows) == (kept, removed)
    with pytest.raises(ValueError, match="D-185"):
        ds.deduplicate_trials([_row("r1", H1, "xyz", fh="same")], timeframe_in_key=True)


def test_the_campaign_wide_dedup_default_is_unchanged():
    rows = [_row("r1", H1, "1h", fh="same"), _row("r2", H1, "4h", fh="same"),
            _row("r3", H2, "1h", fh="other")]
    kept, removed = ds.deduplicate_trials(rows)
    assert [r["trial_id"] for r in kept] == ["r1", "r3"] and removed == 1
    assert ds.select_same_basis_sample(rows)["N"] == 2


def test_the_candidates_own_row_is_in_its_keys_n_and_the_record_says_so():
    # the candidate backtested on 4h, the same config + fold also on 1h earlier
    rows = [_row("r1", H1, "1h", fh="same"), _row("cand", H1, "4h", fh="same"),
            _row("r3", H1, "4h", fh="other")]
    got = ds.select_same_structure_sample(rows, (H1, "4h"))
    assert "cand" in [x["trial_id"] for x in got["rows"]]
    assert got["N"] == got["K"] == 2 and got["N_campaign"] == 2


def test_n_is_never_below_k_and_compute_dsr_accepts_it():
    rows = [_row(f"r{i}", H1, "1h", sr=0.001 * i) for i in range(6)]
    s =ds.select_same_structure_sample(rows, (H1, "1h"))
    assert s["N"] == s["K"] == 6
    stats = {"sr_daily": 0.1, "T": 400, "skew": 0.0, "kurtosis_raw": 3.0}
    out = ds.compute_dsr_whole_test(stats, s["srs"], s["N"], 10)
    assert out["N"] == 6 and out["K"] == 6


@pytest.mark.parametrize("key", [None, ("a",), (H1, ""), (H1, None), [H1, "1h"], "x"])
def test_a_bad_key_raises(key):
    with pytest.raises(ValueError, match="key"):
        ds.select_same_structure_sample([_row("r1")], key)


@pytest.mark.parametrize("bad", [{"structure_hash": "nothex", "timeframe": "1h"},
                                 {"structure_hash": H1, "timeframe": 3600},
                                 {"structure_hash": H1.upper(), "timeframe": "1h"}])
def test_a_malformed_key_field_raises(bad):
    with pytest.raises(ValueError, match="D-185"):
        sk.row_structure_key({"trial_id": "r", **bad})


def test_a_timeframe_written_two_ways_is_one_key():
    rows = [_row("r1", H1, "1h"), _row("r2", H1, "60m"), _row("r3", H1, "3600s")]
    assert {sk.row_structure_key(r) for r in rows} == {(H1, "1h")}
    assert ds.select_same_structure_sample(rows, (H1, "1h"))["N"] == 3


# ---------------------------------------------------------------------------
# 6. branch 3, end to end
# ---------------------------------------------------------------------------

def _key_row(trial_id, h, tf, source="backtest"):
    def _fn(rows):
        for r in rows:
            if r["trial_id"] == trial_id and r["source"] == source:
                r["structure_hash"], r["timeframe"] = h, tf
    _edit_rows(_fn)


def _add_rows(n, h, tf, start):
    _edit_rows(lambda rows: rows.extend(
        _row(f"run_{start + i}", h, tf, sr=-0.05 + 0.01 * i, fh=f"fh-ss-{start + i}") for i in range(n)))


def _keyed_run(candidate_key=(H1, "1h")):
    """A graded v2 run: the candidate keyed (or not), 4 more rows on its key, 3 on another
    hash, 2 on another timeframe, 3 unkeyed, 1 invalidated and 1 duplicate on its key."""
    run_dir = _v2_run()
    if candidate_key is not None:
        _key_row(RUN_ID, *candidate_key)
    _add_rows(4, H1, "1h", 700)
    _add_rows(3, H2, "1h", 720)
    _add_rows(2, H1, "4h", 740)
    _add_rows(3, None, None, 760)
    _edit_rows(lambda rows: rows.extend([
        _row("run_780", H1, "1h", fh="fh-ss-780", invalidated_artifact=True),
        _row("run_781", H1, "1h", fh="fh-ss-700")]))  # dedups onto run_700
    return run_dir


def test_flag_off_dsr_basis_and_dsr_row_are_the_pre_d185_shapes():
    run_dir = _keyed_run()
    ev = _evaluate(run_dir)  # V2_ON, no dsr_same_structure key at all
    basis = ev["dsr_basis"]
    assert set(basis) == {"n_dsr_total", "n_trials", "sharpe_basis", "n_same_basis",
                          "min_same_basis", "basis_overlay"}
    d = _dsr_row(ev)["detail"]
    assert "same_structure" not in d and "D-185" not in _dsr_row(ev)["note"]
    campaign_n = rpr._whole_test_dsr_context()["n_dsr_total"]
    assert basis["n_dsr_total"] == d["N"] == campaign_n
    assert d["K"] == basis["n_same_basis"]
    # an explicit enabled: false is the same file as an absent key
    _set_orchestrator({**V2_ON, "dsr_same_structure": {"enabled": False}})
    off = _evaluate(run_dir)
    off["generated_at"] = ev["generated_at"]
    assert off == ev


def test_flag_off_never_reads_the_new_row_fields(monkeypatch):
    run_dir = _keyed_run()
    ev = _evaluate(run_dir)

    def _boom(*_a, **_k):
        raise AssertionError("the flag-off path read structure_key")
    monkeypatch.setattr(sk, "row_structure_key", _boom)
    monkeypatch.setattr(sk, "apply_structure_overlay", _boom)
    again = _evaluate(run_dir)
    again["generated_at"] = ev["generated_at"]
    assert again == ev


def test_flag_on_counts_n_and_k_by_key_and_records_both_counts():
    run_dir = _keyed_run()
    campaign = rpr._whole_test_dsr_context()
    _set_orchestrator(SS_ON)
    ev = _evaluate(run_dir)
    row = _dsr_row(ev)
    d = row["detail"]
    # candidate + run_700..703 on (H1, 1h); the invalidated and the duplicate row are out
    assert d["N"] == 5 and d["K"] == 5
    rec = {"status": "keyed", "structure_hash": H1, "timeframe": "1h", "n_same_structure": 5,
           "k_same_structure": 5, "n_campaign_wide": campaign["n_dsr_total"],
           "k_campaign_wide": campaign["sample"]["K"]}
    assert d["same_structure"] == rec
    assert ev["dsr_basis"]["same_structure"] == {"enabled": True, "by_variant": {RUN_ID: rec}}
    # the campaign-wide fields of dsr_basis are unchanged by the flag
    assert ev["dsr_basis"]["n_dsr_total"] == campaign["n_dsr_total"] > 5
    assert ev["dsr_basis"]["n_same_basis"] == campaign["sample"]["K"] > 5
    # the DSR is graded on the same-structure N: K 5 < 10, so SR0 = sigma_null * Z(5)
    assert d["sr0"] == pytest.approx(d["sigma_null"] * _z(5), abs=1e-15)
    assert "campaign-wide N=" in row["note"] and "N=5" in row["note"]


def test_flag_on_lowers_n_so_the_dsr_rises_against_the_flag_off_grade():
    run_dir = _keyed_run()
    off = _dsr_row(_evaluate(run_dir))
    _set_orchestrator(SS_ON)
    on = _dsr_row(_evaluate(run_dir))
    assert on["detail"]["N"] < off["detail"]["N"]
    assert on["actual"] > off["actual"]


def test_flag_on_unkeyed_candidate_falls_back_to_the_campaign_wide_counts_and_says_so():
    run_dir = _keyed_run(candidate_key=None)
    off = _evaluate(run_dir)
    _set_orchestrator(SS_ON)
    ev = _evaluate(run_dir)
    d = _dsr_row(ev)["detail"]
    assert (d["N"], d["K"]) == (_dsr_row(off)["detail"]["N"], _dsr_row(off)["detail"]["K"])
    assert _dsr_row(ev)["actual"] == _dsr_row(off)["actual"]
    rec = ev["dsr_basis"]["same_structure"]["by_variant"][RUN_ID]
    assert rec["status"] == "unkeyed" and "structure_hash and no timeframe" in rec["reason"]
    assert rec["n_campaign_wide"] == d["N"] and rec["k_campaign_wide"] == d["K"]
    assert d["same_structure"] == rec


def test_flag_on_half_keyed_candidate_is_unkeyed_too():
    run_dir = _keyed_run(candidate_key=None)
    _edit_rows(lambda rows: [r.update(structure_hash=H1) for r in rows if r["trial_id"] == RUN_ID])
    _set_orchestrator(SS_ON)
    rec = _evaluate(run_dir)["dsr_basis"]["same_structure"]["by_variant"][RUN_ID]
    assert rec["status"] == "unkeyed" and "no timeframe" in rec["reason"]


def test_unkeyed_ledger_rows_are_never_counted_in_a_keys_n():
    run_dir = _keyed_run()
    _set_orchestrator(SS_ON)
    n_before = _dsr_row(_evaluate(run_dir))["detail"]["N"]
    _add_rows(5, None, None, 800)  # five more unkeyed rows: the campaign grows, the key does not
    ev = _evaluate(run_dir)
    assert _dsr_row(ev)["detail"]["N"] == n_before == 5
    assert ev["dsr_basis"]["n_dsr_total"] > ev["dsr_basis"]["same_structure"]["by_variant"][RUN_ID][
        "n_same_structure"]


def test_a_candidate_alone_on_its_key_is_graded_at_sr0_zero():
    # D-185 direction (a): at N = 1 on the same-structure path no selection happened, so the
    # published formula's N = 1 case applies: SR0 = 0, DSR = PSR against zero.
    run_dir = _v2_run()
    _key_row(RUN_ID, H2, "1h")
    _set_orchestrator(SS_ON)
    ev = _evaluate(run_dir)
    row = _dsr_row(ev)
    d = row["detail"]
    assert d["N"] == 1 and d["status"] == "ok" and d["reason"] == "N = 1: no selection correction"
    assert (d["sr0"], d["z_expected_max"], d["sigma_source"]) == (0.0, 0.0, "none")
    assert row["actual"] is not None and row["actual"] == d["dsr"]
    assert row["actual"] == pytest.approx(
        _hand_dsr(d["sr_daily"], d["T"], _own_row()["whole_test"]["skew"],
                  _own_row()["whole_test"]["kurtosis"], 0.0), abs=1e-12)
    assert "not_evaluable_reason" not in row or row["not_evaluable_reason"] is None
    assert "N = 1: no selection correction" in row["note"]
    rec = ev["dsr_basis"]["same_structure"]["by_variant"][RUN_ID]
    assert rec["status"] == "keyed" and rec["n_same_structure"] == 1


def test_two_trials_on_the_key_keep_the_n_2_rule():
    run_dir = _v2_run()
    _key_row(RUN_ID, H2, "1h")
    _add_rows(1, H2, "1h", 700)
    _set_orchestrator(SS_ON)
    d = _dsr_row(_evaluate(run_dir))["detail"]
    assert d["N"] == 2 and d["reason"] is None and d["sigma_source"] == "null"
    assert d["z_expected_max"] == pytest.approx(_z(2), abs=1e-15)
    assert d["sr0"] == pytest.approx(d["sigma_null"] * _z(2), abs=1e-15)


def test_an_unkeyed_candidate_at_campaign_wide_n_1_is_still_not_evaluable():
    # The unkeyed fallback is campaign-wide, so it keeps the campaign-wide N >= 2 rule.
    run_dir = _v2_run()
    _edit_rows(lambda rows: rows.__setitem__(
        slice(None), [r for r in rows if r["trial_id"] == RUN_ID and r["source"] == "backtest"]))
    for flag in (False, True):
        _set_orchestrator(SS_ON if flag else V2_ON)
        row = _dsr_row(_evaluate(run_dir))
        assert row["detail"]["N"] == 1 and row["actual"] is None, flag
        assert "N=1" in row["not_evaluable_reason"], flag


def test_compute_dsr_whole_test_n1_branch_only_with_the_keyword():
    stats = {"sr_daily": 0.1, "T": 400, "skew": -0.2, "kurtosis_raw": 4.0}
    off = ds.compute_dsr_whole_test(stats, [0.1], 1, 10)
    assert off["status"] == "not_evaluable" and off["dsr"] is None and "N >= 2" in off["reason"]
    on = ds.compute_dsr_whole_test(stats, [0.1], 1, 10, n1_no_selection=True)
    assert on["status"] == "ok" and on["reason"] == "N = 1: no selection correction"
    assert (on["sr0"], on["z_expected_max"], on["sigma_source"], on["sigma_used"]) == (0.0, 0.0, "none", None)
    assert on["N"] == 1 and on["K"] == 1 and on["T"] == 400
    assert on["sigma_null"] == pytest.approx(1 / math.sqrt(399))
    assert on["dsr"] == pytest.approx(_hand_dsr(0.1, 400, -0.2, 4.0, 0.0), abs=1e-12)
    # still NOT_EVALUABLE with the keyword at N = 0, on a short T and on a bad denominator
    assert ds.compute_dsr_whole_test(stats, [], 0, 10, n1_no_selection=True)["dsr"] is None
    short = ds.compute_dsr_whole_test({**stats, "T": 5}, [0.1], 1, 10, n1_no_selection=True)
    assert short["dsr"] is None and short["status"] == "not_evaluable"
    kurt = 10.0 * (1 - 5e-10)          # the Pearson floor 1 + skew^2, within the validator's tolerance
    bad = ds.compute_dsr_whole_test(
        {"sr_daily": 6.0 / (kurt - 1), "T": 400, "skew": 3.0, "kurtosis_raw": kurt},
        [0.5], 1, 10, n1_no_selection=True)  # 1 - skew*SR + ((kurt-1)/4)SR^2 is just below 0
    assert bad["dsr"] is None and bad["status"] == "not_evaluable" and "denominator" in bad["reason"]


def test_compute_dsr_whole_test_n2_and_above_ignore_the_keyword():
    stats = {"sr_daily": 0.1, "T": 400, "skew": -0.2, "kurtosis_raw": 4.0}
    for n, srs in ((2, [0.1, 0.0]), (5, [0.1, 0.0, 0.05]), (12, [0.01 * i for i in range(12)])):
        assert (ds.compute_dsr_whole_test(stats, srs, n, 10, n1_no_selection=True)
                == ds.compute_dsr_whole_test(stats, srs, n, 10))


def test_the_spend_and_every_non_same_structure_caller_never_pass_the_n1_keyword():
    import inspect
    assert "n1_no_selection" not in inspect.getsource(rpr._dsr_on_current_ledger_v2)
    src = inspect.getsource(rpr._whole_test_dsr_candidate)
    # the keyword is passed from inside the same_structure branch, and only for a keyed candidate
    assert src.index("if same_structure:") < src.index('n1_no_selection=record["status"] == "keyed"')
    assert src.count("n1_no_selection=") == 2  # the docstring mention + the one call
    for fn in (rpr._whole_test_dsr_candidate_on, rpr._dsr_not_evaluable):
        assert "n1_no_selection=True" not in inspect.getsource(fn)


def test_flag_on_without_v2_leaves_the_legacy_dsr_basis_alone():
    run_dir = _keyed_run()
    _set_orchestrator({k: v for k, v in SS_ON.items() if k != "profit_bars_v2"})
    from test_e062_s2b1_profit_bars_v2 import V1_BARS, _write_bars
    _write_bars(V1_BARS)
    ev = _evaluate(run_dir)
    assert set(ev["dsr_basis"]) == {"n_dsr_total", "n_trials"}


def test_the_grid_grader_grades_on_the_same_structure_n_like_branch_3():
    # The setup of test_e062_s2b2b's grid-grader test (variant loop on, two variants), the
    # two variants keyed (H1, 1h) and two more rows on that key.
    from test_profit_bars_every_backtest import VARIANT_LOOP_ON, _seed_dsr_ledger
    from test_e062_s2b1_profit_bars_v2 import V2_BARS, _attach_whole_test, _build, _write_bars, _write_cost_model
    from test_e058_s2a_regroup_record import _seed
    _set_orchestrator({**V2_ON, **VARIANT_LOOP_ON})
    _write_bars(V2_BARS)
    _write_cost_model()
    run_dir = _seed(variant_loop=True)
    arts = run_dir / "artifacts"
    vids = ["base", "design"]
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": {
        v: {"status": "validated", "config_path": f"artifacts/variants/{v}/strategy_config.json"}
        for v in vids}})
    prs = {}
    for v in vids:
        prs[f"{RUN_ID}:{v}"] = _build(run_dir / "variants" / v)
        rpr.save_yaml(arts / "variants" / v / "protocol_result.yaml", prs[f"{RUN_ID}:{v}"])
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"campaign_id": "t", "runs": [], "trial_sharpes": [
        {"trial_id": f"{RUN_ID}:{v}", "source": "backtest", "sharpe": 0.3, "forecast_hash": f"fh-{v}",
         "structure_hash": H1, "timeframe": "1h"} for v in vids]})
    _seed_dsr_ledger()
    _attach_whole_test(run_dir, prs)
    _add_rows(2, H1, "1h", 700)
    _set_orchestrator({**SS_ON, **VARIANT_LOOP_ON})
    cell = rpr._profit_bars_grid_grader(run_dir, RUN_ID)("base")
    dsr = {r["name"]: r for r in cell["bars"]}["deflated_sharpe_threshold"]
    ev = _evaluate(run_dir)
    assert dsr["detail"]["N"] == _dsr_row(ev, "base")["detail"]["N"] == 4
    assert dsr == _dsr_row(ev, "base")
    assert set(ev["dsr_basis"]["same_structure"]["by_variant"]) == {"base", "design"}


# ---------------------------------------------------------------------------
# 7. the holdout spend keeps the campaign-wide N
# ---------------------------------------------------------------------------

def test_the_holdout_spend_keeps_the_campaign_wide_n_with_the_flag_on():
    run_dir = _keyed_run()
    ev_off = _evaluate(run_dir, record_bars_sha=True)
    bars = rpr._evaluation_under_current_bars(ev_off)
    spend_off = rpr._dsr_on_current_ledger(run_dir, RUN_ID, ev_off["variants"][RUN_ID], bars, ev_off)

    _set_orchestrator(SS_ON)
    ev_on = _evaluate(run_dir, record_bars_sha=True)
    assert _dsr_row(ev_on)["detail"]["N"] == 5 < ev_off["dsr_basis"]["n_dsr_total"]  # graded by structure
    bars = rpr._evaluation_under_current_bars(ev_on)
    spend_on = rpr._dsr_on_current_ledger(run_dir, RUN_ID, ev_on["variants"][RUN_ID], bars, ev_on)

    campaign_n = rpr._whole_test_dsr_context()["n_dsr_total"]
    assert spend_on["n_dsr_total"] == spend_off["n_dsr_total"] == campaign_n
    assert spend_on["n_same_basis"] == spend_off["n_same_basis"]
    assert spend_on["deflated_sharpe_ratio"] == spend_off["deflated_sharpe_ratio"]  # campaign-wide DSR
    assert spend_on["deflated_sharpe_ratio"] != _dsr_row(ev_on)["actual"]            # not the graded one


def test_the_spend_does_not_call_the_overlay_loader_or_pass_the_keyword():
    import inspect
    src = inspect.getsource(rpr._dsr_on_current_ledger_v2)
    assert "same_structure=" not in src and "with_structure_overlay" not in src
    assert "_structure_overlay_kw" not in src


# ---------------------------------------------------------------------------
# 8. the backfill tool and its overlay
# ---------------------------------------------------------------------------

def _make_root(tmp_path) -> Path:
    root = tmp_path / "sr"
    (root / "campaign_record").mkdir(parents=True)
    (root / "protocols").mkdir()

    def _cfg(rel, cfg):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(cfg), encoding="utf-8")
        return p

    other = _config()
    other["strategies"]["regimes"]["unknown"]["components"][0]["weight"] = -1
    p1 = _cfg("runs/run_001/artifacts/candidate_strategy_config.json", _config())
    p2 = _cfg("runs/run_002/artifacts/variants/v1/strategy_config.json", other)
    p4 = _cfg("runs/run_004/artifacts/candidate_strategy_config.json", _config())
    (root / "protocols" / "run_001_generated.json").write_text(
        json.dumps({"symbols": ["BTCUSDT"], "timeframe": "60m", "windows": []}), encoding="utf-8")
    (root / "protocols" / "pinned.json").write_text(json.dumps({"timeframe": "4h"}), encoding="utf-8")
    pre = root / "runs" / "run_002" / "artifacts" / "pre_registration.yaml"
    pre.write_text(yaml.safe_dump({"machine_constraints": {"protocol_ref": "protocols/pinned.json"}}),
                   encoding="utf-8")
    # run_004 has a config but no readable protocol at all
    rows = [
        {"trial_id": "run_001", "source": "backtest", "forecast_hash": rpr._compute_forecast_hash(p1)},
        {"trial_id": "run_001", "source": "prescreen", "forecast_hash": rpr._compute_forecast_hash(p1)},
        {"trial_id": "run_002:v1", "source": "backtest", "forecast_hash": rpr._compute_forecast_hash(p2)},
        {"trial_id": "run_003", "source": "backtest", "forecast_hash": "fh-no-saved-config"},
        {"trial_id": "run_004", "source": "backtest", "forecast_hash": rpr._compute_forecast_hash(p4)},
        {"trial_id": "run_001:ghost", "source": "backtest", "forecast_hash": "fh-ghost"},
        {"trial_id": "run_001", "source": "backtest_failed", "forecast_hash": "fh-edited-config"},
        {"trial_id": "run_002", "source": "backtest", "structure_hash": H1, "timeframe": "1h",
         "forecast_hash": "fh-native"},
    ]
    (root / "campaign_record" / "campaign_state.yaml").write_text(
        yaml.safe_dump({"campaign_id": "t", "trial_sharpes": rows}, sort_keys=False), encoding="utf-8")
    return root


def _snapshot(root) -> dict:
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def test_a_dry_run_writes_nothing_and_counts_what_it_would_key(tmp_path, capsys):
    root = _make_root(tmp_path)
    before = _snapshot(root)
    assert bsh.main(["--root", str(root)]) == 0
    assert _snapshot(root) == before
    assert not (root / bsh.OVERLAY_REL).exists()
    out = capsys.readouterr().out
    assert "dry run" in out and "nothing written" in out
    for secret in ("run_001", "run_002", H1, "fh-"):
        assert secret not in out  # counts only
    plan = bsh.run(root)
    assert plan["counts"] == {
        "rows": 8, "already_keyed": 1, "already_in_overlay": 0, "keyed": 3, "keyed_unverified": 0,
        "unkeyed_no_saved_config": 2,                       # run_003, run_001:ghost
        "unkeyed_no_protocol_timeframe": 1,                 # run_004
        "unkeyed_config_does_not_match_forecast_hash": 1,   # run_001 backtest_failed
    }
    assert plan["written"] is False


def test_the_dry_run_prints_the_four_counts_and_the_unkeyed_reasons_only(tmp_path, capsys):
    root = _make_root(tmp_path)
    before = _snapshot(root)
    assert bsh.main(["--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert _snapshot(root) == before  # read-only against the given root
    assert "rows_keyed=4, rows_unkeyed=4, distinct_keys=3, singleton_keys=2" in out
    assert "unkeyed_no_saved_config=2" in out and "unkeyed_no_protocol_timeframe=1" in out
    # nothing but name=number pairs and the two fixed sentences: no id, path, hash or date
    import re
    assert not re.search(r"[0-9a-f]{12,}|runs/|campaign_record|\d{4}-\d{2}-\d{2}|\.json|\.yaml", out)
    s = bsh.run(root)["summary"]
    assert s == {"rows_keyed": 4, "rows_unkeyed": 4, "distinct_keys": 3, "singleton_keys": 2}


def test_a_dry_run_that_fails_prints_the_exception_class_only(tmp_path, capsys):
    root = _make_root(tmp_path)
    (root / bsh.OVERLAY_REL).write_text(
        yaml.safe_dump({"entries": [{"trial_id": "run_secret_id", "source": "backtest"}]}),
        encoding="utf-8")
    assert bsh.main(["--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert "ValueError" in out and "run_secret_id" not in out
    with pytest.raises(ValueError):  # --write keeps the full error
        bsh.main(["--root", str(root), "--write"])


def test_the_summary_counts_a_singleton_key_after_dedup_with_the_timeframe(tmp_path):
    root = _make_root(tmp_path)
    state = yaml.safe_load((root / bsh.LEDGER_REL).read_text(encoding="utf-8"))
    cfg_h = _h(_config())
    state["trial_sharpes"] = [
        {"trial_id": "x1", "source": "backtest", "forecast_hash": "f", "structure_hash": cfg_h,
         "timeframe": "1h"},
        {"trial_id": "x2", "source": "backtest", "forecast_hash": "f", "structure_hash": cfg_h,
         "timeframe": "4h"},                                  # same config, 4h: its own key
        {"trial_id": "x3", "source": "backtest", "forecast_hash": "f", "structure_hash": cfg_h,
         "timeframe": "60m"},                                 # duplicate of x1 once canonical
        {"trial_id": "x4", "source": "backtest", "forecast_hash": "g", "structure_hash": cfg_h,
         "timeframe": "1h", "invalidated_artifact": True},    # excluded
        {"trial_id": "x5", "source": "backtest", "forecast_hash": "h"},   # unkeyed
    ]
    (root / bsh.LEDGER_REL).write_text(yaml.safe_dump(state), encoding="utf-8")
    assert bsh.run(root)["summary"] == {"rows_keyed": 4, "rows_unkeyed": 1, "distinct_keys": 2,
                                        "singleton_keys": 2}


def test_write_appends_the_overlay_only_keys_rows_with_configs_and_is_idempotent(tmp_path):
    root = _make_root(tmp_path)
    ledger_before = (root / bsh.LEDGER_REL).read_bytes()
    res = bsh.run(root, write=True)
    assert res["written"] is True
    assert (root / bsh.LEDGER_REL).read_bytes() == ledger_before  # the ledger is never edited
    index = sk.load_structure_overlay(root / bsh.OVERLAY_REL)
    assert set(index) == {("run_001", "backtest"), ("run_001", "prescreen"), ("run_002:v1", "backtest")}
    e = index[("run_001", "backtest")]
    assert e["structure_hash"] == _h(_config()) and e["timeframe"] == "1h"       # "60m" -> "1h"
    assert e["config_ref"] == "runs/run_001/artifacts/candidate_strategy_config.json"
    assert e["config_sha256"] == hashlib.sha256((root / e["config_ref"]).read_bytes()).hexdigest()
    assert e["forecast_hash_check"] == "match"  # the row's forecast_hash equals the config's
    assert index[("run_002:v1", "backtest")]["timeframe"] == "4h"                # via protocol_ref
    assert index[("run_002:v1", "backtest")]["structure_hash"] != e["structure_hash"]  # weight sign
    # nothing for the rows that stay unkeyed
    assert not any(k[0] in ("run_003", "run_004", "run_001:ghost") for k in index)
    assert ("run_001", "backtest_failed") not in index and ("run_002", "backtest") not in index

    snap = _snapshot(root)
    again = bsh.run(root, write=True)  # a second write: nothing new, no byte changes
    assert again["entries"] == [] and again["written"] is False
    assert again["counts"]["already_in_overlay"] == 3 and again["counts"]["keyed"] == 0
    assert _snapshot(root) == snap


def test_write_leaves_no_temp_file_and_refuses_a_conflicting_existing_entry(tmp_path):
    root = _make_root(tmp_path)
    bsh.run(root, write=True)
    assert [p.name for p in (root / "campaign_record").iterdir()
            if p.suffix == ".tmp"] == []
    doc = yaml.safe_load((root / bsh.OVERLAY_REL).read_text(encoding="utf-8"))
    bad = copy.deepcopy(doc)
    bad["entries"].append({**bad["entries"][0], "structure_hash": H2})
    (root / bsh.OVERLAY_REL).write_text(yaml.safe_dump(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="two different entries"):
        bsh.run(root, write=True)


def test_a_config_edited_after_its_run_stays_unkeyed(tmp_path):
    root = _make_root(tmp_path)
    p = root / "runs" / "run_001" / "artifacts" / "candidate_strategy_config.json"
    cfg = json.loads(p.read_text(encoding="utf-8"))
    cfg["strategies"]["warmup"] = 999
    p.write_text(json.dumps(cfg), encoding="utf-8")
    plan = bsh.run(root)
    assert plan["counts"]["unkeyed_config_does_not_match_forecast_hash"] == 3  # run_001 x2 + failed
    assert plan["counts"]["keyed"] == 1


def test_a_legacy_row_without_a_forecast_hash_is_keyed_but_counted_apart(tmp_path):
    root = _make_root(tmp_path)
    state = yaml.safe_load((root / bsh.LEDGER_REL).read_text(encoding="utf-8"))
    state["trial_sharpes"] = [{"trial_id": "run_001", "source": "prescreen"}]
    (root / bsh.LEDGER_REL).write_text(yaml.safe_dump(state), encoding="utf-8")
    plan = bsh.run(root)
    c = plan["counts"]
    assert c["keyed"] == 1 and c["keyed_unverified"] == 1
    # D-185 note (direction 2026-10-24): the overlay entry says the row could not be checked
    assert [e["forecast_hash_check"] for e in plan["entries"]] == ["row_has_no_forecast_hash"]
    bsh.run(root, write=True)
    index = sk.load_structure_overlay(root / bsh.OVERLAY_REL)
    assert index[("run_001", "prescreen")]["forecast_hash_check"] == "row_has_no_forecast_hash"


@pytest.mark.parametrize("tid,want", [
    ("run_058", ("run_058", "runs/run_058/artifacts/candidate_strategy_config.json")),
    ("run_058:base", ("run_058", "runs/run_058/artifacts/variants/base/strategy_config.json")),
    ("run_058:../x", (None, None)), ("../run_058", (None, None)), ("", (None, None)),
    (None, (None, None)),
])
def test_config_ref_follows_the_trial_id_and_refuses_path_tricks(tid, want):
    run_id, rel = bsh._config_ref(tid)
    assert (run_id, rel if rel is None else rel.as_posix()) == want


def test_overlay_validation_is_strict():
    good = {"trial_id": "r", "source": "backtest", "structure_hash": H1, "timeframe": "1h",
            "config_sha256": H2, "config_ref": "runs/r/x.json",
            "forecast_hash_check": "match"}
    assert sk.validate_structure_overlay({"entries": [good, dict(good)]}) == {("r", "backtest"): good}
    for bad in ({**good, "extra": 1}, {k: v for k, v in good.items() if k != "timeframe"},
                {**good, "structure_hash": "zz"}, {**good, "trial_id": ""},
                {**good, "forecast_hash_check": "unknown"},
                {k: v for k, v in good.items() if k != "forecast_hash_check"}):
        with pytest.raises(ValueError):
            sk.validate_structure_overlay({"entries": [bad]})
    with pytest.raises(ValueError, match="only 'entries'"):
        sk.validate_structure_overlay({"entries": [], "stamp": "2026"})
    with pytest.raises(ValueError, match="two different"):
        sk.validate_structure_overlay({"entries": [good, {**good, "timeframe": "4h"}]})


def test_apply_overlay_copies_keys_in_never_mutates_and_refuses_conflicts_and_orphans():
    good = {"trial_id": "r1", "source": "backtest", "structure_hash": H1, "timeframe": "1h",
            "config_sha256": H2, "config_ref": "x", "forecast_hash_check": "match"}
    idx = {("r1", "backtest"): good}
    rows = [{"trial_id": "r1", "source": "backtest"}, {"trial_id": "r2", "source": "backtest"}]
    out = sk.apply_structure_overlay(rows, idx)
    assert out[0]["structure_hash"] == H1 and out[0]["timeframe"] == "1h" and out[1] is rows[1]
    assert "structure_hash" not in rows[0]  # the ledger row itself is untouched
    native = [{"trial_id": "r1", "source": "backtest", "structure_hash": H1, "timeframe": "1h"}]
    assert sk.apply_structure_overlay(native, idx)[0] is native[0]
    with pytest.raises(ValueError, match="overlay"):
        sk.apply_structure_overlay([{**native[0], "timeframe": "4h"}], idx)
    with pytest.raises(ValueError, match="absent from the ledger"):
        sk.apply_structure_overlay([rows[1]], idx)


def test_the_dsr_reads_the_overlay_only_under_the_flag():
    run_dir = _v2_run()
    _add_rows(3, None, None, 700)  # three legacy rows, unkeyed in the ledger
    entries = [{"trial_id": f"run_{700 + i}", "source": "backtest", "structure_hash": H1,
                "timeframe": "1h", "config_sha256": H2, "config_ref": f"runs/run_{700 + i}/c.json",
                "forecast_hash_check": "match"}
               for i in range(3)]
    entries.append({**entries[0], "trial_id": RUN_ID})
    rpr.TRIAL_STRUCTURE_KEY_OVERLAY_PATH.write_text(yaml.safe_dump({"entries": entries}),
                                                    encoding="utf-8")
    # flag off: the file is never read (a malformed overlay would otherwise raise)
    off = _evaluate(run_dir)
    assert "same_structure" not in off["dsr_basis"]
    _set_orchestrator(SS_ON)
    on = _evaluate(run_dir)
    rec = on["dsr_basis"]["same_structure"]["by_variant"][RUN_ID]
    assert rec["status"] == "keyed" and rec["n_same_structure"] == 4  # the candidate + three
    # the ledger on disk stayed unkeyed: only the DSR's view carries the overlay
    assert "structure_hash" not in _own_row()
