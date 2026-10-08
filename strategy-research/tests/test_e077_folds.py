"""
E-077 PR-1 (CUL-419, D-085) -- fixed folds and a validation-period guard, flag off.

Proven here, all with synthetic inputs (no LLM, no backtest, no market data, no
holdout bar):
  1. config/folds.yaml: three folds, six exact 4-month blocks each, every block
     inside the research period and outside validation and holdout (dates read
     from config/campaign_data_policy.yaml), B and C interleaved so each has a
     block in every year of 2018-2021, fold A == the six windows of runs 065-074;
     load_folds refuses every way the file can go wrong.
  2. decide-next under the flag: a child of a fold-A run gets fold B, of a fold-B
     run fold C, a lineage that used A, B and C is INFEASIBLE (never an exception,
     the campaign goes on); an "unfolded" parent (windows matching no fold) gets
     the first fold its windows do not overlap; an unreadable lineage and a pinned
     source protocol are refused with a reason, never guessed.
  3. The child's machine_constraints: window keys replaced, everything else
     copied; the generator turns `fold` into the fold's exact windows, run_context,
     memory entry and trial rows carry it.
  4. The novelty key differs across folds and matches within one; the repeat gate
     is per (config, fold).
  5. The validation guard: any window overlapping the validation period raises
     under the flag (generator and pre-flight), message names the future
     validation stage; flag off is as today.
  6. Flag off is byte-identical: no `folds` input, no `fold_assignment`, the child's
     machine_constraints equal the parent's, no `fold` anywhere.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import decide_next as dn  # noqa: E402
import campaign_memory as cm  # noqa: E402
import novelty as nov  # noqa: E402
import research_folds as rf  # noqa: E402

import test_e059_s2a_decide_next as t59  # noqa: E402  (synthetic decide-next inputs)
import test_e036_s2a_exact_match_gate as t36  # noqa: E402  (runs recorded through the real writers)
from test_k3_protocol_pinning import _minimal_run  # noqa: E402

REAL_POLICY = SR_ROOT / "config" / "campaign_data_policy.yaml"
REAL_FOLDS = SR_ROOT / "config" / "folds.yaml"
DOC = rf.load_folds(REAL_FOLDS, policy_path=REAL_POLICY)
FOLD_A = rf.windows_ranges(rf.fold_windows(DOC, "A"))
FOLD_B = rf.windows_ranges(rf.fold_windows(DOC, "B"))
FOLD_C = rf.windows_ranges(rf.fold_windows(DOC, "C"))
RUN_074_WINDOWS = [  # protocols/run_074_generated.json, verbatim
    {"label": "2022-01", "test": {"start": "2022-01-01", "end": "2022-04-30"}},
    {"label": "2022-05", "test": {"start": "2022-05-01", "end": "2022-08-31"}},
    {"label": "2022-09", "test": {"start": "2022-09-01", "end": "2022-12-31"}},
    {"label": "2023-01", "test": {"start": "2023-01-01", "end": "2023-04-30"}},
    {"label": "2023-05", "test": {"start": "2023-05-01", "end": "2023-08-31"}},
    {"label": "2023-09", "test": {"start": "2023-09-01", "end": "2023-12-31"}},
]
PROMOTION = {"median_sharpe_gt": 0.1, "max_abs_drawdown_pct_lt": 25, "min_trade_count_gte": 30,
             "kill_median_sharpe_lt": -0.5}


# ---------------------------------------------------------------------------
# 1. config/folds.yaml
# ---------------------------------------------------------------------------

def _range(w):
    return (w["test"]["start"], w["test"]["end"])


def test_the_real_file_has_three_folds_of_six_exact_blocks():
    assert DOC["order"] == ["A", "B", "C"]
    assert {f: len(b) for f, b in DOC["folds"].items()} == {"A": 6, "B": 6, "C": 6}
    labels = {f: [b["label"] for b in blocks] for f, blocks in DOC["folds"].items()}
    assert labels["A"] == ["2022-01", "2022-05", "2022-09", "2023-01", "2023-05", "2023-09"]
    assert labels["B"] == ["2018-01", "2018-09", "2019-05", "2020-01", "2020-09", "2021-05"]
    assert labels["C"] == ["2018-05", "2019-01", "2019-09", "2020-05", "2021-01", "2021-09"]
    ends = {"01": "04-30", "05": "08-31", "09": "12-31"}
    for blocks in DOC["folds"].values():
        for b in blocks:
            y, m = b["label"].split("-")
            assert (b["start"], b["end"]) == (f"{y}-{m}-01", f"{y}-{ends[m]}")


def test_the_eighteen_blocks_tile_the_research_period_exactly_once():
    all_labels = sorted(b["label"] for blocks in DOC["folds"].values() for b in blocks)
    expected = [f"{y}-{m}" for y in range(2018, 2024) for m in ("01", "05", "09")]
    assert all_labels == expected


def test_b_and_c_are_interleaved_a_block_in_every_year_and_a_covers_both_of_its_years():
    for fold, years in (("A", {2022, 2023}), ("B", {2018, 2019, 2020, 2021}),
                        ("C", {2018, 2019, 2020, 2021})):
        assert {int(b["label"][:4]) for b in DOC["folds"][fold]} == years
    # no fold is a contiguous half of 2018-2021: each takes both early and late blocks
    for fold in ("B", "C"):
        starts = [b["label"] for b in DOC["folds"][fold]]
        assert starts[0] < "2019" and starts[-1] > "2021"


def test_fold_a_is_exactly_the_windows_of_runs_065_to_074():
    assert rf.fold_windows(DOC, "A") == RUN_074_WINDOWS
    real = SR_ROOT / "protocols" / "run_074_generated.json"
    if real.exists():  # the saved protocol (not in the repo): if present, it must agree
        assert json.loads(real.read_text(encoding="utf-8"))["windows"] == RUN_074_WINDOWS


def test_every_block_is_inside_research_and_outside_validation_and_holdout_per_the_policy():
    ranges = rf.policy_ranges(REAL_POLICY)
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    assert tuple(ranges["holdout"]) == tuple(policy["holdout_range"])
    r_start, r_end = ranges["research"]
    v_start, v_end = ranges["validation"]
    assert (v_start, v_end) == ("2024-01-01", "2025-12-31")  # 2024-2025 per CLAUDE.fork.md
    assert r_end < v_start  # research ends before validation starts
    for blocks in DOC["folds"].values():
        for b in blocks:
            assert r_start <= b["start"] and b["end"] <= r_end
            for name in ("validation", "holdout"):
                lo, hi = ranges[name]
                assert b["end"] < lo or b["start"] > hi, (b, name)


def _write_folds(tmp_path, mutate):
    doc = yaml.safe_load(REAL_FOLDS.read_text(encoding="utf-8"))
    mutate(doc)
    p = tmp_path / "folds.yaml"
    p.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return p


def _block(label, start, end):
    return {"label": label, "start": start, "end": end}


@pytest.mark.parametrize("why,mutate,match", [
    ("a block inside validation",
     lambda d: d["folds"]["A"].__setitem__(5, _block("2024-01", "2024-01-01", "2024-04-30")),
     "outside the research period|overlaps the validation"),
    ("a block ending past the research period",
     lambda d: d["folds"]["A"].__setitem__(5, _block("2023-09", "2023-09-01", "2024-01-31")),
     "must run"),
    ("an end that is not the last included day",
     lambda d: d["folds"]["A"].__setitem__(0, _block("2022-01", "2022-01-01", "2022-05-01")),
     "must run"),
    ("a month that is not 01/05/09",
     lambda d: d["folds"]["A"].__setitem__(0, _block("2022-02", "2022-02-01", "2022-05-31")),
     "label"),
    ("a fold with five blocks", lambda d: d["folds"]["B"].pop(), "exactly 6 blocks"),
    ("the same block in two folds",
     lambda d: d["folds"]["C"].__setitem__(0, _block("2018-01", "2018-01-01", "2018-04-30")),
     "is in fold B and fold C"),
    ("blocks out of order",
     lambda d: d["folds"]["B"].reverse(), "ascending"),
    ("another fold order", lambda d: d.__setitem__("order", ["B", "A", "C"]), "order must be exactly"),
    ("an extra key on a block",
     lambda d: d["folds"]["A"][0].__setitem__("note", "x"), "exactly"),
])
def test_load_folds_refuses_a_bad_file(tmp_path, why, mutate, match):
    p = _write_folds(tmp_path, mutate)
    with pytest.raises(rf.FoldsError, match=match):
        rf.load_folds(p, policy_path=REAL_POLICY)


def test_load_folds_refuses_a_block_inside_the_holdout_of_a_policy(tmp_path):
    """The holdout is read from the policy, not from the folds file: a policy whose
    holdout covered fold A's last block makes that block illegal (a synthetic
    range, so no sealed date is written here)."""
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    policy["holdout_range"] = ["2023-09-01", "2023-11-30"]
    pp = tmp_path / "policy.yaml"
    pp.write_text(yaml.safe_dump(policy), encoding="utf-8")
    with pytest.raises(rf.FoldsError, match="holdout"):
        rf.load_folds(REAL_FOLDS, policy_path=pp)


def test_load_folds_refuses_a_policy_it_cannot_read_ranges_from(tmp_path):
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    del policy["walk_forward_extension"]
    pp = tmp_path / "policy.yaml"
    pp.write_text(yaml.safe_dump(policy), encoding="utf-8")
    with pytest.raises(rf.FoldsError):
        rf.load_folds(REAL_FOLDS, policy_path=pp)
    with pytest.raises(rf.FoldsError, match="cannot read"):
        rf.load_folds(tmp_path / "missing.yaml", policy_path=REAL_POLICY)


def test_a_policy_with_a_gap_between_research_and_validation_is_refused(tmp_path):
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    policy["backward_extension"]["BTCUSDT_1h"] = ["2018-01-01", "2023-11-30"]
    pp = tmp_path / "policy.yaml"
    pp.write_text(yaml.safe_dump(policy), encoding="utf-8")
    with pytest.raises(rf.FoldsError, match="contiguous"):
        rf.load_folds(REAL_FOLDS, policy_path=pp)


# ---------------------------------------------------------------------------
# 2. decide-next: which fold a child gets
# ---------------------------------------------------------------------------

GEN_PROTOCOL = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h", "start": "2022-01-01",
                "end": "2023-12-31", "window_months": 4, "promotion": copy.deepcopy(PROMOTION)}


def _memory(run_id, hyp, ref=None, **kw):
    return t59._memory_entry(run_id, hyp=hyp, protocol_ref=ref or f"protocols/{run_id}.json", **kw)


def _scenario(source, hyp, lineage, *, protocol=GEN_PROTOCOL, pinned=False, folds=True,
              others=None, specs=None):
    """A decide-next input where `source` (whose memory hypothesis_id is `hyp`) proposed
    one patch. `lineage` = {run_id: ranges-or-None | (ranges, hyp)} for the runs named in
    `hyp` (and `source` itself must be a key)."""
    pid = f"profitability-{source}-1"
    src = t59._src([t59._patch(pid)])
    mc = ({"protocol_ref": "protocols/pinned.json"} if pinned
          else {"protocol": copy.deepcopy(protocol)})
    src["pre_registration"]["machine_constraints"] = mc
    memory = {source: _memory(source, hyp, proposal_ids=[pid])}
    ranges = {}
    for rid, rng in lineage.items():
        ranges[rid] = rng
        if rid != source:
            memory[rid] = _memory(rid, "ROOT")
    memory.update(others or {})
    inputs = t59._inputs({source: src}, memory)
    inputs["protocol_specs"] = specs or {}
    if folds:
        inputs["folds"] = {"doc": copy.deepcopy(DOC), "run_ranges": ranges}
    return inputs, pid


def _decide(inputs, source):
    return dn.decide(inputs, now="2026-10-08T00:00:00+00:00",
                     trigger={"after_run": source, "after_entry": "E", "idea_status": "refuted"})


def _cand(record, pid):
    return t59._by_id(record)[pid]


def _front(inputs, record):
    rel, text = dn.candidate_brief(record, inputs, decision_ref="runs/x/artifacts/decision_record.yaml")
    return yaml.safe_load(text.split("---", 2)[1])


def test_a_child_of_a_fold_a_run_gets_fold_b():
    inputs, pid = _scenario("run_074", "ROOT__x-run_070-1", {"run_074": FOLD_A, "run_070": FOLD_A})
    record = _decide(inputs, "run_074")
    cand = _cand(record, pid)
    assert cand["eligible"] and cand["gates"]["feasibility"]["result"] == "FEASIBLE"
    assert cand["fold_assignment"] == {"fold": "B", "lineage": ["run_074", "run_070"],
                                       "used": {"run_074": ["A"], "run_070": ["A"]}}
    front = _front(inputs, record)
    proto = front["machine_constraints"]["protocol"]
    assert proto["fold"] == "B"
    assert (proto["start"], proto["end"]) == ("2018-01-01", "2021-08-31")
    assert proto["window_months"] == 4
    assert "fold B" in front["research_goal"] and "2018-09" in front["research_goal"]


def test_a_child_of_a_fold_b_run_gets_fold_c():
    # run_080 (this lineage's second generation) ran on fold B; its root ran on A
    inputs, pid = _scenario("run_080", "ROOT__x-run_074-1",
                            {"run_080": FOLD_B, "run_074": FOLD_A})
    record = _decide(inputs, "run_080")
    assert _cand(record, pid)["fold_assignment"]["fold"] == "C"
    proto = _front(inputs, record)["machine_constraints"]["protocol"]
    assert proto["fold"] == "C" and (proto["start"], proto["end"]) == ("2018-05-01", "2021-12-31")


def test_the_first_generation_child_skips_a_fold_only_its_own_lineage_used():
    """The lineage is the source-run chain, not every run in the campaign: a fold used by
    an unrelated run is still free for this idea."""
    other = {"run_090": _memory("run_090", "OTHER")}
    inputs, pid = _scenario("run_074", "ROOT", {"run_074": FOLD_A}, others=other)
    inputs["folds"]["run_ranges"]["run_090"] = FOLD_B  # unrelated run on B
    record = _decide(inputs, "run_074")
    assert _cand(record, pid)["fold_assignment"]["fold"] == "B"


def test_a_lineage_that_used_all_three_folds_is_infeasible_and_the_campaign_goes_on():
    inputs, pid = _scenario("run_081", "ROOT__x-run_074-1__y-run_080-1",
                            {"run_081": FOLD_C, "run_080": FOLD_B, "run_074": FOLD_A})
    record = _decide(inputs, "run_081")  # must not raise
    cand = _cand(record, pid)
    assert not cand["eligible"]
    feas = cand["gates"]["feasibility"]
    assert feas["result"] == "INFEASIBLE"
    assert any(r.startswith("folds_exhausted") and "validation" in r for r in feas["reasons"])
    assert cand["fold_assignment"]["fold"] is None
    assert record["picked"] is None or "candidate_id" not in record["picked"]
    assert record["stop"]["reason"] == "no_eligible_candidate"  # the existing stop, not a crash


def test_one_run_covering_all_three_folds_exhausts_the_lineage_by_itself():
    wide = [("2018-01-01", "2023-12-31")]
    inputs, pid = _scenario("run_082", "ROOT", {"run_082": wide})
    cand = _cand(_decide(inputs, "run_082"), pid)
    assert cand["fold_assignment"]["used"] == {"run_082": ["A", "B", "C"]}
    assert cand["gates"]["feasibility"]["result"] == "INFEASIBLE"


def test_runs_065_to_074_count_as_fold_a_without_a_special_case():
    rngs = rf.windows_ranges(RUN_074_WINDOWS)
    assert rf.folds_used_by(DOC, rngs) == ["A"]


def test_an_unfolded_parent_gets_the_first_fold_its_windows_do_not_overlap():
    # 2021 in monthly tiles: overlaps fold B (2021-05) and fold C (2021-01, 2021-09), not A
    monthly_2021 = [(f"2021-{m:02d}-01", f"2021-{m:02d}-28") for m in range(1, 13)]
    inputs, pid = _scenario("run_083", "ROOT", {"run_083": monthly_2021})
    cand = _cand(_decide(inputs, "run_083"), pid)
    assert cand["fold_assignment"] == {"fold": "A", "lineage": ["run_083"],
                                       "used": {"run_083": ["B", "C"]}}


def test_a_parent_whose_windows_overlap_no_fold_has_used_none():
    in_validation = [("2024-02-01", "2024-02-28")]  # a legacy run; overlaps no fold
    inputs, pid = _scenario("run_084", "ROOT", {"run_084": in_validation})
    cand = _cand(_decide(inputs, "run_084"), pid)
    assert cand["fold_assignment"]["fold"] == "A" and cand["fold_assignment"]["used"] == {"run_084": []}


def test_an_overlap_of_one_day_counts_as_using_the_fold():
    one_day = [("2018-04-30", "2018-04-30")]  # last day of fold B's first block
    assert rf.folds_used_by(DOC, one_day) == ["B"]
    assert rf.folds_used_by(DOC, [("2018-05-01", "2018-05-01")]) == ["C"]
    assert rf.folds_used_by(DOC, [("2018-04-30", "2018-05-01")]) == ["B", "C"]


def test_a_lineage_run_whose_windows_cannot_be_read_is_refused_not_guessed():
    inputs, pid = _scenario("run_085", "ROOT__x-run_070-1", {"run_085": FOLD_A, "run_070": None})
    cand = _cand(_decide(inputs, "run_085"), pid)
    assert cand["fold_assignment"]["fold"] is None
    reasons = cand["gates"]["feasibility"]["reasons"]
    assert any(r.startswith("fold_lineage_unreadable") and "run_070" in r for r in reasons)
    assert cand["gates"]["feasibility"]["result"] == "INFEASIBLE"


def test_a_lineage_run_missing_from_memory_is_refused_not_guessed():
    inputs, pid = _scenario("run_086", "ROOT__x-run_011-1", {"run_086": FOLD_A})
    cand = _cand(_decide(inputs, "run_086"), pid)
    assert cand["fold_assignment"]["fold"] is None
    assert any("run_011 (not in campaign memory)" in r
               for r in cand["gates"]["feasibility"]["reasons"])


def test_a_source_that_pins_a_protocol_file_cannot_take_a_fold():
    inputs, pid = _scenario("run_087", "ROOT", {"run_087": FOLD_A}, pinned=True)
    cand = _cand(_decide(inputs, "run_087"), pid)
    assert cand["gates"]["feasibility"]["result"] == "INFEASIBLE"
    assert any(r.startswith("fold_needs_generated_protocol")
               for r in cand["gates"]["feasibility"]["reasons"])


def test_lineage_run_ids_reads_the_source_chain_out_of_the_hypothesis_id():
    assert rf.lineage_run_ids("run_074", "H__trade_efficiency-run_070-1__profitability-run_073-1") \
        == ["run_074", "run_070", "run_073"]
    assert rf.lineage_run_ids("run_070", "HOURLY_SHOCK_REVERSAL") == ["run_070"]
    assert rf.lineage_run_ids("run_070", None) == ["run_070"]
    assert rf.lineage_run_ids("run_074", "H__a-run_074-1") == ["run_074"]  # no duplicate


def test_the_child_keeps_every_other_part_of_the_parents_machine_constraints():
    proto = {**GEN_PROTOCOL, "per_symbol_start": {"BTCUSDT": "2022-01-01"}, "holdout": None,
             "extra_key": {"keep": [1, 2]}}
    inputs, pid = _scenario("run_074", "ROOT", {"run_074": FOLD_A}, protocol=proto)
    inputs["runs"]["run_074"]["pre_registration"]["machine_constraints"]["significance_methodology"] = "x"
    child = _front(inputs, _decide(inputs, "run_074"))["machine_constraints"]
    parent = copy.deepcopy(inputs["runs"]["run_074"]["pre_registration"]["machine_constraints"])
    assert child["significance_methodology"] == "x"
    cp, pp = child["protocol"], parent["protocol"]
    for key in ("symbols", "timeframe", "promotion", "holdout", "extra_key"):
        assert cp[key] == pp[key], key
    assert "per_symbol_start" not in cp  # a window-defining key: the fold replaces it
    assert set(cp) == (set(pp) - {"per_symbol_start"}) | {"fold"}
    # the other machine_constraints keys, symbols and timeframe survive untouched


# ---------------------------------------------------------------------------
# 3. the novelty key: per (config, fold)
# ---------------------------------------------------------------------------

def _protocol_file(root: Path, name: str, windows):
    p = root / "protocols" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": windows}),
                 encoding="utf-8")
    return f"protocols/{name}"


def test_the_novelty_key_differs_across_folds_and_matches_within_one(tmp_path):
    refs = {
        "a1": _protocol_file(tmp_path, "run_a1.json", rf.fold_windows(DOC, "A")),
        "a2": _protocol_file(tmp_path, "run_a2.json", rf.fold_windows(DOC, "A")),
        "b1": _protocol_file(tmp_path, "run_b1.json", rf.fold_windows(DOC, "B")),
        "c1": _protocol_file(tmp_path, "run_c1.json", rf.fold_windows(DOC, "C")),
    }
    specs = nov.protocol_specs(tmp_path, {"runs": {k: {"protocol_ref": r} for k, r in refs.items()}})
    key = {k: nov.novelty_key("h" * 64, ["BTCUSDT"], {"protocol_ref": r}, specs)
           for k, r in refs.items()}
    assert key["a1"] == key["a2"]                         # same fold, two runs -> one key
    assert len({key["a1"], key["b1"], key["c1"]}) == 3    # three folds -> three keys
    # and the sha decide-next uses for a not-yet-run child equals the one a run on that fold gets
    for fold, k in (("A", "a1"), ("B", "b1"), ("C", "c1")):
        assert specs[refs[k]]["windows_sha256"] == rf.fold_windows_sha256(DOC, fold)


def _repeat_scenario(prior_fold_ranges, prior_windows_sha):
    """run_074 (on fold A) proposed a patch; a DIFFERENT run, run_090, already ran that exact
    patched config on the windows `prior_windows_sha`."""
    inputs, pid = _scenario("run_074", "ROOT", {"run_074": FOLD_A})
    src = inputs["runs"]["run_074"]
    _, patched, _ = dn.resolve_patch(t59._patch(pid), src["base_config"])
    prior = _memory("run_090", "OTHER", fh=dn.config_sha256(patched), symbols=("BTCUSDT",))
    inputs["memory"]["runs"]["run_090"] = prior
    inputs["protocol_specs"] = {
        "protocols/run_074.json": {"timeframe": "1h", "windows_sha256": rf.fold_windows_sha256(DOC, "A")},
        "protocols/run_090.json": {"timeframe": "1h", "windows_sha256": prior_windows_sha},
    }
    inputs["folds"]["run_ranges"]["run_090"] = prior_fold_ranges
    return inputs, pid


def test_the_repeat_gate_is_per_config_and_fold():
    # run_090 ran this config on fold B; the child would run it on fold B -> REPEAT
    inputs, pid = _repeat_scenario(FOLD_B, rf.fold_windows_sha256(DOC, "B"))
    cand = _cand(_decide(inputs, "run_074"), pid)
    assert cand["fold_assignment"]["fold"] == "B"
    assert cand["gates"]["novelty"]["exact_match"] == "REPEAT"
    assert cand["gates"]["novelty"]["matched_runs"] == ["run_090"] and not cand["eligible"]
    # run_090 ran it on fold C; the child runs on B -> a different key, NOVEL
    inputs, pid = _repeat_scenario(FOLD_C, rf.fold_windows_sha256(DOC, "C"))
    cand = _cand(_decide(inputs, "run_074"), pid)
    assert cand["gates"]["novelty"]["exact_match"] == "NOVEL" and cand["eligible"]


# ---------------------------------------------------------------------------
# 4. the generator, run_context, memory and trial rows (real writers)
# ---------------------------------------------------------------------------

@pytest.fixture
def sandbox_folds():
    (rpr.ROOT / "config").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REAL_FOLDS, rpr.ROOT / "config" / "folds.yaml")
    return rpr.ROOT


def _child_constraints(fold="B"):
    inputs, pid = _scenario("run_074", "ROOT__x-run_070-1" if fold == "B" else "ROOT",
                            {"run_074": FOLD_A, "run_070": FOLD_A} if fold == "B" else {"run_074": FOLD_A})
    record = _decide(inputs, "run_074")
    return _front(inputs, record)["machine_constraints"]


def test_the_generator_writes_the_folds_exact_windows_and_run_context_records_the_fold(sandbox_folds):
    mc = _child_constraints()
    run_dir = _minimal_run(rpr.ROOT, "run_900")
    path = rpr._ensure_protocol_from_constraints(run_dir, "run_900", mc, folds_enabled=True)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["windows"] == rf.fold_windows(DOC, "B")
    assert nov._canonical_sha(doc["windows"]) == rf.fold_windows_sha256(DOC, "B")
    ctx = yaml.safe_load((run_dir / "artifacts" / "run_context.yaml").read_text(encoding="utf-8"))
    assert ctx == {"run_type": "forced_diagnostic", "protocol": "run_900_generated.json", "fold": "B"}
    # the launch pre-flight mirrors the generator window for window
    expected = camp._expected_generated_protocol(mc["protocol"], "run_900", promotion_retired=False,
                                                 folds_enabled=True)
    assert expected["windows"] == doc["windows"]


def test_without_a_fold_key_the_generator_and_run_context_are_as_before(sandbox_folds):
    constraints = {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
                                "end": "2022-08-31", "window_months": 4, "promotion": PROMOTION}}
    run_dir = _minimal_run(rpr.ROOT, "run_901")
    path = rpr._ensure_protocol_from_constraints(run_dir, "run_901", constraints)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["windows"] == rpr._generate_monthly_windows("2022-01-01", "2022-08-31", window_months=4)
    ctx = yaml.safe_load((run_dir / "artifacts" / "run_context.yaml").read_text(encoding="utf-8"))
    assert ctx == {"run_type": "forced_diagnostic", "protocol": "run_901_generated.json"}


def test_a_fold_key_with_an_unknown_fold_is_refused(sandbox_folds):
    mc = _child_constraints()
    mc["protocol"]["fold"] = "D"
    run_dir = _minimal_run(rpr.ROOT, "run_902")
    with pytest.raises(rf.FoldsError, match="not one of"):
        rpr._ensure_protocol_from_constraints(run_dir, "run_902", mc, folds_enabled=True)


def _prior_run_on_fold(run_id, fold, mc):
    """A finished run recorded through the real writers (trial row, memory entry), whose
    pre-registration carries machine_constraints `mc`."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    if mc is not None:
        rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                      {"run_id": run_id, "machine_constraints": mc})
    return t36._prior_run_in_memory(run_id, t36._config(), protocol_name=f"{run_id}.json")


def test_trial_rows_and_the_memory_entry_carry_the_fold(sandbox_folds):
    mc = _child_constraints()
    entry = _prior_run_on_fold("run_903", "B", mc)
    assert entry["fold"] == "B"
    rows = [t for t in rpr.load_campaign_state()["trial_sharpes"] if t["trial_id"] == "run_903"]
    assert rows and all(t["fold"] == "B" for t in rows)
    # the failed-backtest row too (the killed-run accounting path)
    cfg = rpr.ROOT / "artifacts" / "candidate_strategy_config.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text("{}", encoding="utf-8")
    run_dir = _minimal_run(rpr.ROOT, "run_904")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  {"run_id": "run_904", "machine_constraints": mc})
    rpr._record_failed_backtest_trial("run_904", cfg, "boom")
    failed = [t for t in rpr.load_campaign_state()["trial_sharpes"] if t["trial_id"] == "run_904"]
    assert failed and failed[0]["source"] == "backtest_failed" and failed[0]["fold"] == "B"


def test_the_memory_file_with_a_fold_validates_against_the_schema(sandbox_folds):
    import jsonschema
    _prior_run_on_fold("run_905", "B", _child_constraints())
    _prior_run_on_fold("run_906", None, None)
    memory = yaml.safe_load(t36._memory_path().read_text(encoding="utf-8"))
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                         "campaign_memory.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(memory, schema)
    assert memory["runs"]["run_905"]["fold"] == "B"
    assert "fold" not in memory["runs"]["run_906"]            # absent, not null
    memory["runs"]["run_905"]["fold"] = "D"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(memory, schema)


def test_a_run_with_no_fold_has_no_fold_in_any_artifact(sandbox_folds):
    entry = _prior_run_on_fold("run_907", None, {"protocol": {"symbols": ["BTCUSDT"]}})
    assert "fold" not in entry
    rows = [t for t in rpr.load_campaign_state()["trial_sharpes"] if t["trial_id"] == "run_907"]
    assert rows and all("fold" not in t for t in rows)


def test_decision_record_schema_accepts_the_fold_assignment():
    import jsonschema
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                         "decision_record.schema.json").read_text(encoding="utf-8"))
    sub = schema["$defs"]["candidate"]["properties"]["fold_assignment"]
    ok = {"fold": "B", "lineage": ["run_074"], "used": {"run_074": ["A"]}}
    jsonschema.validate(ok, sub)
    jsonschema.validate({**ok, "fold": None}, sub)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**ok, "fold": "Z"}, sub)


# ---------------------------------------------------------------------------
# 5. the validation guard
# ---------------------------------------------------------------------------

def _gen(start, end, *, flag, months=4, name="run_910", pre_flight=False):
    constraints = {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": start,
                                "end": end, "window_months": months, "promotion": PROMOTION}}
    if pre_flight:
        return camp._expected_generated_protocol(constraints["protocol"], name,
                                                 promotion_retired=False, folds_enabled=flag)
    run_dir = _minimal_run(rpr.ROOT, name)
    return rpr._ensure_protocol_from_constraints(run_dir, name, constraints, folds_enabled=flag)


@pytest.mark.parametrize("pre_flight", [False, True])
def test_a_2024_window_raises_under_the_flag_in_generation_and_in_the_pre_flight(pre_flight):
    with pytest.raises(rf.ValidationBoundaryBreach, match="validation") as exc:
        _gen("2023-09-01", "2024-04-30", flag=True, pre_flight=pre_flight)
    assert "2024-01-01..2025-12-31" in str(exc.value)
    assert "validation stage" in str(exc.value) and "does not exist yet" in str(exc.value)
    assert "2024-01" in str(exc.value)  # names the window


def test_a_window_straddling_the_start_of_validation_raises():
    with pytest.raises(rf.ValidationBoundaryBreach):
        _gen("2023-12-01", "2024-01-31", flag=True, months=1)


def test_a_window_inside_2025_raises_and_the_last_research_day_does_not():
    with pytest.raises(rf.ValidationBoundaryBreach):
        _gen("2025-05-01", "2025-08-31", flag=True)
    path = _gen("2023-09-01", "2023-12-31", flag=True, name="run_911")  # ends on the last research day
    assert json.loads(path.read_text(encoding="utf-8"))["windows"][-1]["test"]["end"] == "2023-12-31"


def test_flag_off_the_same_2024_window_is_generated_as_today():
    path = _gen("2023-09-01", "2024-04-30", flag=False, name="run_912")
    windows = json.loads(path.read_text(encoding="utf-8"))["windows"]
    assert [w["label"] for w in windows] == ["2023-09", "2024-01"]
    assert _gen("2023-09-01", "2024-04-30", flag=False, pre_flight=True)["windows"] == windows


def _preflight(constraints, name, folds_enabled):
    run_dir = _minimal_run(rpr.ROOT, name)
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  {"run_id": name, "machine_constraints": constraints})
    return camp._protocol_preflight(run_dir, name, promotion_retired=False,
                                    folds_enabled=folds_enabled)


def test_the_launch_preflight_refuses_a_validation_window_only_under_the_flag():
    """Before any LLM call: the pre-flight reads the flag from the caller's one parsed
    reading (folds_enabled), never from the config."""
    constraints = {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2023-09-01",
                                "end": "2024-04-30", "window_months": 4, "promotion": PROMOTION}}
    refusal, regen = _preflight(constraints, "run_913", True)
    assert regen is None and "validation period" in refusal and "cannot generate a protocol" in refusal
    assert _preflight(constraints, "run_914", False) == (None, None)  # flag off: as today


def test_the_preflight_flag_comes_from_the_single_parsed_reading():
    assert camp._folds_from({"folds": True}, None) is True
    assert camp._folds_from({"folds": False}, None) is False
    assert camp._folds_from({}, None) is False
    assert camp._folds_from({"folds": True}, "a refusal") is False   # a refused set launches nothing


def test_the_guard_unit_edges():
    v = ("2024-01-01", "2025-12-31")
    w = lambda s, e: [{"label": "x", "test": {"start": s, "end": e}}]  # noqa: E731
    rf.assert_windows_clear_of_validation(w("2023-09-01", "2023-12-31"), v)
    for s, e in (("2023-12-31", "2024-01-01"), ("2024-01-01", "2024-01-01"),
                 ("2025-12-31", "2025-12-31"), ("2023-01-01", "2026-12-31")):
        with pytest.raises(rf.ValidationBoundaryBreach):
            rf.assert_windows_clear_of_validation(w(s, e), v)


def test_a_policy_without_validation_keys_makes_the_guard_raise_not_pass(monkeypatch, tmp_path):
    policy = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    del policy["burned_ranges"]
    pp = tmp_path / "policy.yaml"
    pp.write_text(yaml.safe_dump(policy), encoding="utf-8")
    monkeypatch.setattr(rpr, "_DATA_POLICY_PATH", pp)
    with pytest.raises(rf.ValidationBoundaryBreach, match="unknown validation period"):
        rpr._assert_windows_clear_of_validation(rf.fold_windows(DOC, "A"))


def test_every_fold_passes_the_guard_and_the_holdout_assert():
    hs, he = rpr._load_holdout_range()
    for fold in DOC["order"]:
        windows = rf.fold_windows(DOC, fold)
        rpr._assert_windows_clear_of_validation(windows)
        rpr._assert_windows_clear_of_holdout(windows, hs, he)


# ---------------------------------------------------------------------------
# 6. the flag, and flag-off identity
# ---------------------------------------------------------------------------

def test_the_flag_defaults_off_and_is_registered_everywhere():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["folds"] == {"enabled": False}
    assert rpr._folds_enabled({}) is False
    assert rpr._folds_enabled({"orchestrator": {"folds": {"enabled": True}}}) is True
    for bad in ("true", 1, None):
        with pytest.raises(ValueError, match="orchestrator.folds.enabled"):
            rpr._folds_enabled({"orchestrator": {"folds": {"enabled": bad}}})
    register = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml")
                              .read_text(encoding="utf-8"))
    rows = [f for f in register["flags"] if f["name"] == "folds"]
    assert len(rows) == 1 and rows[0]["config_key"] == "orchestrator.folds.enabled"
    assert rows[0]["reader"] == "run_phase1_research._folds_enabled"
    src = (SR_ROOT / "workflow" / "run_campaign.py").read_text(encoding="utf-8")
    assert '"folds": orch._folds_enabled' in src


def test_flag_off_decide_next_adds_nothing_and_copies_the_parents_windows():
    inputs, pid = _scenario("run_074", "ROOT__x-run_070-1", {"run_074": FOLD_A, "run_070": FOLD_A},
                            folds=False)
    assert "folds" not in inputs
    record = _decide(inputs, "run_074")
    cand = _cand(record, pid)
    assert "fold_assignment" not in cand and "fold" not in json.dumps(record["candidates"])
    front = _front(inputs, record)
    parent_mc = copy.deepcopy(inputs["runs"]["run_074"]["pre_registration"]["machine_constraints"])
    assert front["machine_constraints"] == parent_mc            # byte-for-byte the deep copy
    assert "folds.yaml" not in front["research_goal"]
    # the candidate's key set is exactly the pre-E-077 one
    assert set(cand) == {"candidate_id", "origin", "kind", "category", "source_run",
                         "parent_hypothesis_id", "hypothesis_id", "proposal_ref",
                         "collapsed_sources", "scores", "resolved_config_sha256", "gates",
                         "eligible", "cost", "rank"}


def test_flag_on_and_off_agree_on_everything_but_the_windows_for_the_same_input():
    off, pid = _scenario("run_074", "ROOT", {"run_074": FOLD_A}, folds=False)
    on, _ = _scenario("run_074", "ROOT", {"run_074": FOLD_A}, folds=True)
    c_off, c_on = _cand(_decide(off, "run_074"), pid), _cand(_decide(on, "run_074"), pid)
    c_on = {k: v for k, v in c_on.items() if k != "fold_assignment"}
    assert c_on == c_off                                         # ranking inputs unchanged


def test_load_inputs_reads_run_windows_only_under_the_folds_kwarg(tmp_path):
    root = tmp_path
    (root / "campaign_record").mkdir()
    ref = _protocol_file(root, "run_074_generated.json", RUN_074_WINDOWS)
    mem = {"schema_version": cm.SCHEMA_VERSION, "legacy_note": "x", "runs": {
        "run_074": {"run_id": "run_074", "protocol_ref": ref},
        "run_075": {"run_id": "run_075", "protocol_ref": "protocols/missing.json"},
        "run_076": {"run_id": "run_076", "protocol_ref": None}}}
    (root / "campaign_record" / "campaign_memory.yaml").write_text(yaml.safe_dump(mem), encoding="utf-8")
    off = dn.load_inputs(root, {"queue": []}, categories=t59.CATS)
    assert "folds" not in off
    on = dn.load_inputs(root, {"queue": []}, categories=t59.CATS, folds=DOC)
    assert on["folds"]["doc"] == DOC
    assert on["folds"]["run_ranges"] == {
        "run_074": [(s, e) for s, e in FOLD_A], "run_075": None, "run_076": None}
    assert {k: v for k, v in on.items() if k != "folds"}.keys() == off.keys()


def test_runs_are_treated_as_a_chain_decide_next_to_the_generator_end_to_end(sandbox_folds):
    """decide-next's brief -> the generator -> the same windows the novelty key was
    computed for (so the repeat gate compares like with like)."""
    inputs, pid = _scenario("run_074", "ROOT", {"run_074": FOLD_A})
    cand = _cand(_decide(inputs, "run_074"), pid)
    mc = _front(inputs, _decide(inputs, "run_074"))["machine_constraints"]
    run_dir = _minimal_run(rpr.ROOT, "run_920")
    path = rpr._ensure_protocol_from_constraints(run_dir, "run_920", mc, folds_enabled=True)
    windows = json.loads(path.read_text(encoding="utf-8"))["windows"]
    assert nov._canonical_sha(windows) == rf.fold_windows_sha256(DOC, cand["fold_assignment"]["fold"])
