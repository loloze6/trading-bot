"""
E-068 continuation 2, PR A (operator decisions, 2026-10-06; delivery plan v26
continuation 2 section 9).

CUL-412: a reader side finding starts from the source run's base config and
block manifest. decide-next carries them in the brief (candidate.start_config /
start_manifest -- never `config`/`manifest`, which mark a pass-through); 1b gets
them as inputs, and every difference between what 1b built and the start is a
structured deviation (D-075) in deviations.yaml, listed by 1b or not.

One kind of reader proposal: a v3 reader writes side findings only; a config
change rides inside the side finding (`config_change`) and the candidate applies
it to the source config. A legacy reading with a stand-alone patch still loads.

--relaunch follow-ups: a legacy split child and a run that already queued extra
cards are refused with by-hand steps; ORPHANED_README.md is written only after
the queue save succeeded.

No real LLM call, no backtest, no market data.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import reader_proposals as rp  # noqa: E402
import decide_next as dn  # noqa: E402
import nearest_build as nb  # noqa: E402

from test_e068_5_readers_v3 import (  # noqa: E402
    RUN_ID, _claim, _fenced, _memory_entry, _patch, _reading, _run070_shaped, _scores,
    _seed_run, _side, _side_with_change, _src, _inputs, _write)
from test_e068_7_block_test_variants_relaunch import _failed_entry, _queue  # noqa: E402
from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401  (fixture)

CHANGE = _patch()["patch"]   # shock_reversal params.period 1 -> 2, valid on run_070's config


def _changed(cat="trade_efficiency", n=1, change=None) -> dict:
    return {**_side(cat, n), "config_change": copy.deepcopy(change or CHANGE)}


def _cand(p, src=None, inputs=None):
    src = src or _src([p])
    return dn._candidate("run_070", _memory_entry(), src, p["proposal_id"].split("-")[0], p,
                         inputs or _inputs(), {})


def _brief_front(p):
    src = _src([{"category": "trade_efficiency", "proposal": p}])
    inputs = _inputs(runs={"run_070": src})
    cand = dn._candidate("run_070", _memory_entry(), src, "trade_efficiency", p, inputs, {})
    record = {"picked": {"candidate_id": cand["candidate_id"], "brief_path": "x/y.md"},
              "candidates": [cand]}
    _rel, text = dn.candidate_brief(record, inputs, decision_ref="d")
    return yaml.safe_load(text.split("---\n")[1])


# ---------------------------------------------------------------------------
# side_finding_start
# ---------------------------------------------------------------------------

def test_no_change_starts_from_the_source_config_unchanged():
    src = _src()
    start = dn.side_finding_start(_side(), src)
    assert start == {"config": src["base_config"], "manifest": src["manifest"], "ops": [],
                     "reason": None}
    start["config"]["x"] = 1                      # a copy: the source is never mutated
    assert "x" not in src["base_config"]


def test_a_config_change_is_applied_to_the_source_config():
    src = _src()
    start = dn.side_finding_start(_changed(), src)
    assert start["reason"] is None and len(start["ops"]) == 1
    assert start["config"] != src["base_config"]
    diff = nb.config_diff(src["base_config"], start["config"])
    assert [(d["before"], d["after"]) for d in diff] == [(1, 2)]
    assert diff[0]["path"] == start["ops"][0]["path"]


def test_a_composite_source_carries_nothing_and_refuses_a_change():
    src = {**_src(), "composition_manifest": {"members": []}}
    assert dn.side_finding_start(_side(), src) == {"config": None, "manifest": None,
                                                   "ops": [], "reason": None}
    start = dn.side_finding_start(_changed(), src)        # review: never silently dropped
    assert start["config"] is None
    assert start["reason"].startswith("config_change_on_composition")


@pytest.mark.parametrize("drop", ["base_config", "manifest"])
def test_a_missing_source_config_or_manifest_is_a_reason(drop):
    src = {**_src(), drop: None}
    start = dn.side_finding_start(_side(), src)
    assert start["config"] is None and start["reason"].startswith("source_config_missing")


def test_an_unresolvable_change_is_a_reason():
    bad = [{**CHANGE[0], "before": 5}]
    start = dn.side_finding_start(_changed(change=bad), _src())
    assert start["config"] is None and start["reason"].startswith("config_change: stale_before")


# ---------------------------------------------------------------------------
# the candidate
# ---------------------------------------------------------------------------

def test_an_unchanged_start_is_eligible_and_not_a_config_novelty():
    cand = _cand(_side())
    assert cand["eligible"] is True and cand["gates"]["feasibility"]["result"] == "UNKNOWN"
    nov = cand["gates"]["novelty"]
    assert nov["exact_match"] == "NOT_APPLICABLE" and "unchanged" in nov["note"]
    assert "starts from the source run's config" in cand["gates"]["feasibility"]["reasons"][0]


def test_a_config_change_gets_a_novelty_key_like_a_patch():
    p = _changed()
    cand = _cand(p)
    assert cand["eligible"] is True
    nov = cand["gates"]["novelty"]
    assert nov["exact_match"] == "NOVEL" and len(nov["spec_hashes"]) == 1
    # the same change already run: REPEAT, as for a patch
    sha = dn.config_sha256(dn.side_finding_start(p, _src())["config"])
    key = dn.novelty_key(sha, ["BTCUSD"], _memory_entry(), {})
    cand2 = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                          _inputs(), {key: ["run_060"]})
    assert cand2["gates"]["novelty"]["exact_match"] == "REPEAT"
    assert cand2["gates"]["novelty"]["matched_runs"] == ["run_060"]


@pytest.mark.parametrize("src_over,reason", [
    ({"base_config": None}, "source_config_missing"),
    ({}, "config_change: stale_before"),
])
def test_an_unusable_start_makes_the_candidate_infeasible(src_over, reason):
    p = _changed(change=[{**CHANGE[0], "before": 5}]) if not src_over else _side()
    cand = _cand(p, src={**_src([p]), **src_over})
    assert cand["eligible"] is False
    assert any(r.startswith(reason) for r in cand["gates"]["feasibility"]["reasons"])


def test_same_tests_collapse_only_on_the_same_config():
    a, b, c = _changed("trade_efficiency"), _changed("profitability"), _side("forecast_power")
    b["scores"] = _scores(3)
    cands = [_cand(p) for p in (a, b, c)]
    out = dn._collapse(cands)
    assert sorted(x["candidate_id"] for x in out) == ["forecast_power-run_070-1",
                                                      "profitability-run_070-1"]


def test_the_same_test_from_two_source_runs_never_collapses():
    """Review: without a change, each finding starts from ITS run's config."""
    a = _side("trade_efficiency")
    other = _src([a])
    other["base_config"] = {**copy.deepcopy(other["base_config"]), "note": "run_072's block"}
    b = {**_side("trade_efficiency"), "proposal_id": "trade_efficiency-run_072-1"}
    ca = dn._candidate("run_070", _memory_entry(), _src([a]), "trade_efficiency", a,
                       _inputs(), {})
    cb = dn._candidate("run_072", _memory_entry(), other, "trade_efficiency", b, _inputs(), {})
    assert len(dn._collapse([ca, cb])) == 2


def test_the_same_test_from_two_composite_runs_never_collapses():
    """Review round 2: a composite carries no start config; the run keys it."""
    comp = {"members": []}
    a = _side("trade_efficiency")
    b = {**_side("trade_efficiency"), "proposal_id": "trade_efficiency-run_072-1"}
    cands = [dn._candidate(rid, _memory_entry(), {**_src([p]), "composition_manifest": comp},
                           "trade_efficiency", p, _inputs(), {})
             for rid, p in (("run_070", a), ("run_072", b))]
    assert [c["eligible"] for c in cands] == [True, True]
    assert len(dn._collapse(cands)) == 2


# ---------------------------------------------------------------------------
# the brief
# ---------------------------------------------------------------------------

def test_the_brief_carries_the_start_config_and_no_pass_through_keys():
    front = _brief_front(_side())
    cand, source = front["candidate"], front["candidate"]["source"]
    base = _src()["base_config"]
    assert cand["start_config"] == base and cand["start_manifest"] == _src()["manifest"]
    assert "config" not in cand and "manifest" not in cand
    assert "expected_config_sha256" not in source           # the CUL-405 pass-through guard
    assert source["start_config_sha256"] == dn.config_sha256(base)
    assert source["base_config_ref"].endswith("strategy_config.json")
    assert "config_change_ops" not in source
    assert "base config (candidate.start_config) -- the block" in front["research_goal"]


def test_the_brief_of_a_change_carries_the_changed_config_and_its_ops():
    p = _changed()
    front = _brief_front(p)
    start = dn.side_finding_start(p, _src())
    source = front["candidate"]["source"]
    assert front["candidate"]["start_config"] == start["config"]
    assert source["config_change_ops"] == start["ops"]
    assert source["proposal"]["config_change"] == CHANGE
    assert start["ops"][0]["path"] in front["research_goal"]


# ---------------------------------------------------------------------------
# 1b: the inputs and the deviations
# ---------------------------------------------------------------------------

def _brief_with_start(run_dir, start=None, manifest=None):
    cand = {"claim": _claim()}
    if start is not None:
        cand["start_config"] = start
        cand["start_manifest"] = manifest
    _write(run_dir / "artifacts" / "research_brief.yaml", {"candidate": cand})


def test_1b_gets_the_start_config_only_for_a_side_finding_brief(monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    arts = run_dir / "artifacts"
    src = _src()
    _brief_with_start(run_dir)                                # no start config
    handoff = {"required_inputs": []}
    rpr._apply_start_config_context("strategy_config_authoring", handoff, run_dir)
    assert handoff["required_inputs"] == [] and not (arts / nb.START_CONFIG_FILE).exists()

    _brief_with_start(run_dir, src["base_config"], src["manifest"])
    for stage in ("hypothesis_generation", "backtest_execution"):   # only 1b
        rpr._apply_start_config_context(stage, handoff, run_dir)
    assert handoff["required_inputs"] == []
    rpr._apply_start_config_context("strategy_config_authoring", handoff, run_dir)
    rpr._apply_start_config_context("strategy_config_authoring", handoff, run_dir)  # no dupes
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert paths == [rpr.START_FROM_CONFIG_NOTE, f"artifacts/{nb.START_CONFIG_FILE}",
                     f"artifacts/{nb.START_MANIFEST_FILE}"]
    assert (SR_ROOT / "runs" / RUN_ID / rpr.START_FROM_CONFIG_NOTE).resolve().exists()
    assert json.loads((arts / nb.START_CONFIG_FILE).read_text(encoding="utf-8")) == \
        src["base_config"]
    assert yaml.safe_load((arts / nb.START_MANIFEST_FILE).read_text(encoding="utf-8")) == \
        src["manifest"]


def _built(run_dir, config, manifest):
    arts = run_dir / "artifacts"
    _write(arts / "backtest_spec.yaml", {"config": config})
    _write(arts / "block_manifest.yaml", manifest)


def _start(run_dir, config, manifest):
    arts = run_dir / "artifacts"
    (arts / nb.START_CONFIG_FILE).write_text(json.dumps(config), encoding="utf-8")
    _write(arts / nb.START_MANIFEST_FILE, manifest)


def _devs(run_dir):
    path = run_dir / "artifacts" / nb.DEVIATIONS_FILE
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None


def test_an_unchanged_build_records_an_exact_record(monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    src = _src()
    _start(run_dir, src["base_config"], src["manifest"])
    _built(run_dir, src["base_config"], src["manifest"])
    rpr._record_start_config_deviations(run_dir)
    rec = _devs(run_dir)
    assert rec["status"] == nb.STATUS_EXACT and rec["deviations"] == []


def test_every_change_from_the_start_is_a_deviation_listed_or_not(monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    src = _src()
    changed = dn.side_finding_start(_changed(), src)["config"]
    manifest = copy.deepcopy(src["manifest"])
    manifest["block"] = ["/somewhere/else"]
    _start(run_dir, src["base_config"], src["manifest"])
    _built(run_dir, changed, manifest)
    # 1b listed one deviation of its own (nearest build): kept, start items added
    own = {"clause": "c", "built_instead": "b", "missing": None, "effect": "e"}
    _write(run_dir / "artifacts" / nb.DEVIATIONS_FILE,
           {"schema_version": nb.SCHEMA_VERSION, "run_id": RUN_ID, "status": nb.STATUS_EXACT,
            "information_only": True, "deviations": [own], "config_rationale_lines": []})
    rpr._record_start_config_deviations(run_dir)
    rec = _devs(run_dir)
    assert rec["status"] == nb.STATUS_APPROXIMATION
    assert rec["deviations"][0] == own
    added = rec["deviations"][1:]
    assert [d["source"] for d in added] == [nb.START_DIFF_SOURCE] * 2
    assert "1 -> 2" in added[0]["built_instead"]
    assert "block manifest's block" in added[1]["clause"]


def test_no_start_config_is_a_no_op_and_a_broken_file_never_raises(monkeypatch, capsys):
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    rpr._record_start_config_deviations(run_dir)
    assert _devs(run_dir) is None
    (run_dir / "artifacts" / nb.START_CONFIG_FILE).write_text("{not json", encoding="utf-8")
    rpr._record_start_config_deviations(run_dir)                 # information only
    assert "could not be recorded" in capsys.readouterr().out


def test_merge_keeps_1bs_deviation_lines_and_is_idempotent():
    """Review: 1b's DEVIATION: lines stay visible once code adds start items."""
    line = {"clause": "the idea's exit", "text": "a time stop instead"}
    rec = {"schema_version": nb.SCHEMA_VERSION, "run_id": "run_x",
           "status": nb.STATUS_APPROXIMATION, "information_only": True, "deviations": [],
           "config_rationale_lines": [line]}
    item = {"clause": "c", "built_instead": "1 -> 2", "missing": None, "effect": "e",
            "source": nb.START_DIFF_SOURCE}
    once = nb.merge_start_deviations(rec, "run_x", [item])
    assert [d["clause"] for d in once["deviations"]] == ["the idea's exit", "c"]
    block = nb.approximation_block(once)
    assert "a time stop instead" in block["line"] and "1 -> 2" in block["line"]
    assert nb.merge_start_deviations(once, "run_x", [item]) == once          # no repeat
    assert all(d.get("source") != nb.START_DIFF_SOURCE
               for d in nb.merge_start_deviations(once, "run_x", [])["deviations"])


def test_merge_counts_once_and_a_reverted_change_is_exact_again():
    """Review round 2: the not-listed count never grows on a re-merge, and a
    record whose only deviations were start items is exact once they are gone."""
    full = [{"clause": str(i), "source": "x"} for i in range(nb.MAX_ITEMS)]
    rec = {"status": nb.STATUS_APPROXIMATION, "deviations": full, "deviations_not_listed": 2,
           "config_rationale_lines": []}
    start = [{"clause": "s", "source": nb.START_DIFF_SOURCE}] * 3
    once = nb.merge_start_deviations(rec, "run_x", start)
    assert once["deviations_not_listed"] == 5
    assert nb.merge_start_deviations(once, "run_x", start)["deviations_not_listed"] == 5
    back = nb.merge_start_deviations(once, "run_x", [])
    assert back["deviations_not_listed"] == 2 and "start_items_not_listed" not in back
    only = nb.merge_start_deviations(None, "run_x", start[:1])
    assert only["status"] == nb.STATUS_APPROXIMATION
    gone = nb.merge_start_deviations(only, "run_x", [])
    assert gone["status"] == nb.STATUS_EXACT and gone["deviations"] == []


def test_merge_caps_the_list_and_keeps_a_park():
    items = [{"clause": str(i)} for i in range(nb.MAX_ITEMS + 3)]
    rec = nb.merge_start_deviations(None, "run_x", items)
    assert len(rec["deviations"]) == nb.MAX_ITEMS and rec["deviations_not_listed"] == 3
    parked = {"status": nb.STATUS_PARKED, "deviations": []}
    assert nb.merge_start_deviations(parked, "run_x", items[:1])["status"] == nb.STATUS_PARKED
    assert nb.merge_start_deviations(parked, "run_x", []) == parked


def test_config_diff_leaves_and_lists():
    a = {"x": {"y": 1, "z": [1, 2]}, "gone": 1, "a/b": 0}
    b = {"x": {"y": 2, "z": [1, 3, 4]}, "new": 1, "a/b": 0}
    assert nb.config_diff(a, b) == [
        {"path": "/gone", "before": 1, "after": None},
        {"path": "/new", "before": None, "after": 1},
        {"path": "/x/y", "before": 1, "after": 2},
        {"path": "/x/z", "before": [1, 2], "after": [1, 3, 4]}]
    assert nb.config_diff(a, a) == []


# ---------------------------------------------------------------------------
# one proposal kind
# ---------------------------------------------------------------------------

def test_salvage_drops_a_model_written_patch_and_says_why(monkeypatch):
    run_dir = _run070_shaped(monkeypatch)
    doc = _reading(patch=_patch())
    body, err = rpr._validate_reader_output(_fenced(doc), "trade_efficiency", run_dir)
    assert err and "stand-alone `patch` is removed" in err
    salvaged = rpr._salvage_reading_output(_fenced(doc), "trade_efficiency", run_dir)
    assert salvaged is not None
    kept_body, dropped = salvaged[0], salvaged[1]
    kept = yaml.safe_load(kept_body)
    assert "patch" not in kept and len(kept["side_findings"]) == 1
    assert any("stand-alone `patch` is removed" in str(d) for d in dropped)


def test_a_model_written_null_patch_is_accepted():
    """Review: `patch: null` proposes nothing, so it costs no retry."""
    rp.check_reading({**_reading(), "patch": None}, "trade_efficiency", "w", from_model=True)


def test_a_side_finding_with_a_change_flattens_with_it(tmp_path):
    doc = _reading(sides=[_side_with_change()])
    _write(tmp_path / "trade_efficiency.yaml", doc)
    (item,) = rp.load_proposals(tmp_path, ["trade_efficiency"])["trade_efficiency"]
    assert item["kind"] == rp.SIDE_FINDING and item["config_change"] == CHANGE


# ---------------------------------------------------------------------------
# --relaunch follow-ups
# ---------------------------------------------------------------------------

def _split_entry(campaign_root):
    _failed_entry(campaign_root)
    q = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    q["queue"][0]["id"] = "P__split_1"
    campaign_root["queue_path"].write_text(yaml.safe_dump(q), encoding="utf-8")


def test_relaunch_refuses_a_legacy_split_child(campaign_root, capsys):
    _split_entry(campaign_root)
    assert camp._relaunch_entry("P__split_1") is False
    out = capsys.readouterr().out
    assert "legacy split child" in out and "continue run_900 instead" in out
    (entry,) = _queue(campaign_root)
    assert entry["run_ids"] == ["run_900"]
    assert not (campaign_root["root"] / "runs" / "run_900" / camp.ORPHANED_README).exists()


def test_relaunch_refuses_a_run_with_queued_card_entries(campaign_root, capsys):
    _failed_entry(campaign_root)
    q = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    q["queue"].append({"id": "P__h2", "brief_path": "briefs/P.md", "status": "queued",
                       "priority": 999, "source": "agent", "notes": "", "run_ids": []})
    campaign_root["queue_path"].write_text(yaml.safe_dump(q), encoding="utf-8")
    assert camp._relaunch_entry("P") is False
    out = capsys.readouterr().out
    assert "already wrote extra card(s) ['P__h2']" in out and "continue run_900" in out
    assert not (campaign_root["root"] / "runs" / "run_900" / camp.ORPHANED_README).exists()


def test_relaunch_refuses_a_run_whose_file_lists_cards(campaign_root, capsys):
    _failed_entry(campaign_root)
    arts = campaign_root["root"] / "runs" / "run_900" / "artifacts"
    _write(arts / dn.QUEUED_HYPOTHESES_FILE, {"cards": [{"n": 2, "card_ref": "c2"},
                                                        {"n": 3, "card_ref": "c3"}]})
    assert camp._relaunch_entry("P") is False
    assert "['P__h2', 'P__h3']" in capsys.readouterr().out


def test_relaunch_accepts_an_empty_queued_file(campaign_root):
    _failed_entry(campaign_root)
    arts = campaign_root["root"] / "runs" / "run_900" / "artifacts"
    _write(arts / dn.QUEUED_HYPOTHESES_FILE, {"cards": []})
    assert camp._relaunch_entry("P") is True


def test_a_failed_queue_save_writes_no_readme(campaign_root, monkeypatch):
    _failed_entry(campaign_root)

    def boom(_queue):
        raise OSError("disk full")
    monkeypatch.setattr(camp, "_save_queue", boom)
    with pytest.raises(OSError):
        camp._relaunch_entry("P")
    assert not (campaign_root["root"] / "runs" / "run_900" / camp.ORPHANED_README).exists()


def test_a_failed_readme_write_is_reported_after_the_save(campaign_root, monkeypatch, capsys):
    _failed_entry(campaign_root)
    real_write = Path.write_text

    def write(self, *a, **k):
        if self.name == camp.ORPHANED_README:
            raise OSError("read-only")
        return real_write(self, *a, **k)
    monkeypatch.setattr(Path, "write_text", write)
    assert camp._relaunch_entry("P") is True
    (entry,) = _queue(campaign_root)
    assert entry["status"] == "ready" and entry["run_ids"] == []
    assert "could NOT be written" in capsys.readouterr().out
    # review: the saved note never cites a README that was not written
    assert "could NOT be written" in entry["notes"] and "kept as a record" not in entry["notes"]
