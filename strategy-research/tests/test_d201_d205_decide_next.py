"""
D-201 and D-205 (decide-next, 2026-10-28), pinned on run_102's real case.

  D-201  A side-finding candidate whose resolved config, coins and bar size were already
         measured on OTHER windows (another fold) is a REPEAT, not NOVEL. The exact key (window
         set included) is unchanged: this is a second lookup after it misses, made only when a
         fold is drawn (orchestrator.folds.enabled). The 5a gate is not touched.
  D-205  candidate_brief carries the source run's memory-entry observations in
         candidate.source_observations (statement, variant, measured, floors_met, vehicle).

Fixture tests/fixtures/d201_run_102/: run_102's base config and block manifest, its
trade_efficiency side finding, and the fields decide-next reads from the memory entries of
run_101 and run_102. Window labels and dates are not in it; the window fingerprints are the
real ones (hashes). Fold A's and D's fingerprints are the ones research_folds gives for them.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import decide_next as dn  # noqa: E402
import novelty as nov  # noqa: E402
import run_campaign as camp  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "d201_run_102"
RUN, CAT, PID = "run_102", "trade_efficiency", "trade_efficiency-run_102-1"
REPEATED_CONFIG = "b45d1013d9eabd228bdf3e1eb80917ef5c8651bdb64f72dcdd645f1fc1702b18"
# the window fingerprints of fold A (run_101's), fold B (run_102's) and fold D (the candidate's
# draw), as research_folds.fold_windows_sha256 gives them for config/folds.yaml
FOLD_A_SHA = "d931dfa50fb1aaddde738abd5eb1b2f9011df7e1c49fbc0ea7b0b87d492fb289"
FOLD_B_SHA = "7a83cc6c53bba25fc1540b1a62d6a3d016c4ff6fbefe440eb2de44e4564081ae"
FOLD_D_SHA = "589df2bf29686ac77bc2af0573a4921337904d353892012f671ec064f0639642"
SPECS = {
    "protocols/run_101_generated.json": {"timeframe": "1h", "windows_sha256": FOLD_A_SHA},
    "protocols/run_102_generated.json": {"timeframe": "1h", "windows_sha256": FOLD_B_SHA},
}
NOTE_A = "same config measured on fold A: a refold is the operator's command (D-122)"


def _yaml(name):
    return yaml.safe_load((FIX / name).read_text(encoding="utf-8"))


def _memory():
    return _yaml("memory.yaml")


def _proposal(after=1.0):
    p = _yaml("proposal.yaml")
    p["config_change"][0]["after"] = after
    return p


def _src(p):
    return {"proposals": [{"category": CAT, "proposal": p}], "base_variant": "base",
            "base_config": json.loads((FIX / "base_config.json").read_text(encoding="utf-8")),
            "base_config_ref": f"runs/{RUN}/artifacts/variants/base/strategy_config.json",
            "manifest": _yaml("block_manifest.yaml"),
            "pre_registration": {"machine_constraints": {"protocol_ref": "protocols/p.json"}},
            "research_brief": {"strategy_domain": "d", "market_universe": ["BTCUSDT"],
                               "timeframe": "1h", "venue": "kraken", "product": "perp"},
            "card": None, "card_text": None}


def _inputs(src, memory=None, folds=True):
    out = {"memory": memory if memory is not None else _memory(), "queue": {"queue": []},
           "existing_candidate_briefs": [], "known_classes": None, "feed_set": None,
           "digest": None, "protocol_specs": copy.deepcopy(SPECS), "runs": {RUN: src}}
    if folds:
        out["folds"] = {"doc": {}, "run_ranges": {}, "data": None}
    return out


def _draw(fold, sha):
    return lambda *a, **k: {"fold": fold, "windows_sha256": sha, "source_folds": ["B"],
                            "drawn_from": ["A", "C", "D"], "seed": 7, "reason": None}


def _cand(monkeypatch, p=None, memory=None, fold="D", sha=FOLD_D_SHA, folds=True):
    p = p or _proposal()
    src = _src(p)
    inputs = _inputs(src, memory, folds)
    if folds:
        monkeypatch.setattr(dn, "_fold_assignment_for", _draw(fold, sha))
    memory = inputs["memory"]
    exact = dn._exact_index(memory, inputs["protocol_specs"])
    cand = dn._candidate(RUN, memory["runs"][RUN], src, CAT, p, inputs, exact)
    return cand, exact


# ---------------------------------------------------------------------------
# D-201: the helper
# ---------------------------------------------------------------------------

def test_window_free_key_drops_only_the_window_set():
    key = ("h", ("BTCUSD",), "1h", f"windows:{FOLD_A_SHA}")
    assert nov.window_free_key(key) == ("h", ("BTCUSD",), "1h")


def test_matches_on_other_windows_matches_all_but_the_window_set():
    a = ("h", ("BTCUSD",), "1h", "windows:aa")
    b = ("h", ("BTCUSD",), "1h", "windows:bb")
    index = {a: ["run_001", "run_003"], b: ["run_003", "run_002"],
             ("h", ("ETHUSD",), "1h", "windows:aa"): ["run_004"],
             ("h", ("BTCUSD",), "4h", "windows:aa"): ["run_005"],
             ("g", ("BTCUSD",), "1h", "windows:aa"): ["run_006"]}
    probe = ("h", ("BTCUSD",), "1h", "windows:cc")
    assert nov.matches_on_other_windows(probe, index) == ["run_001", "run_003", "run_002"]
    assert nov.matches_on_other_windows(("h", ("SOLUSD",), "1h", "x"), index) == []


# ---------------------------------------------------------------------------
# D-201: run_102's candidate
# ---------------------------------------------------------------------------

def test_the_fixture_is_run_102s_case(monkeypatch):
    cand, exact = _cand(monkeypatch)
    assert cand["resolved_config_sha256"] == REPEATED_CONFIG
    # run_101's tested BTCUSD base is in the index under fold A's window set, not fold D's
    key_a = (REPEATED_CONFIG, ("BTCUSD",), "1h", f"windows:{FOLD_A_SHA}")
    key_d = (REPEATED_CONFIG, ("BTCUSD",), "1h", f"windows:{FOLD_D_SHA}")
    assert exact[key_a] == ["run_101"] and key_d not in exact


def test_same_config_on_fold_d_reads_repeat_matched_run_101(monkeypatch):
    cand, _exact = _cand(monkeypatch)
    nv = cand["gates"]["novelty"]
    assert nv["exact_match"] == "REPEAT"
    assert nv["matched_runs"] == ["run_101"]
    assert nv["note"] == NOTE_A
    assert nv["spec_hashes"]
    assert cand["eligible"] is False


def test_another_config_on_fold_d_stays_novel(monkeypatch):
    cand, _exact = _cand(monkeypatch, p=_proposal(after=2.0))
    assert cand["resolved_config_sha256"] != REPEATED_CONFIG
    nv = cand["gates"]["novelty"]
    assert nv["exact_match"] == "NOVEL" and nv["matched_runs"] == [] and "note" not in nv
    assert cand["eligible"] is True


def test_same_config_on_other_coins_stays_novel(monkeypatch):
    memory = _memory()
    memory["runs"][RUN]["variants"]["base"]["symbols"] = ["ETHUSD"]
    cand, _exact = _cand(monkeypatch, memory=memory)
    assert cand["resolved_config_sha256"] == REPEATED_CONFIG
    assert cand["gates"]["novelty"]["exact_match"] == "NOVEL"


def test_same_config_on_the_same_fold_is_the_exact_repeat_with_no_note(monkeypatch):
    cand, _exact = _cand(monkeypatch, fold="A", sha=FOLD_A_SHA)
    nv = cand["gates"]["novelty"]
    assert nv["exact_match"] == "REPEAT" and nv["matched_runs"] == ["run_101"]
    assert "note" not in nv


def test_without_a_drawn_fold_nothing_changes(monkeypatch):
    # orchestrator.folds.enabled off: no inputs["folds"], the window set is the parent's own
    cand, _exact = _cand(monkeypatch, folds=False)
    nv = cand["gates"]["novelty"]
    assert nv["exact_match"] == "NOVEL" and nv["matched_runs"] == [] and "note" not in nv


def test_the_note_names_the_fold_or_says_it_is_not_recorded():
    mem = {"runs": {"run_001": {"fold": "A"}, "run_002": {"fold": "C"}, "run_003": {},
                    "run_004": {"fold": "A"}}}
    f = dn._same_config_other_fold_note
    assert f(["run_001"], mem) == NOTE_A
    assert f(["run_001", "run_004"], mem) == NOTE_A
    assert f(["run_001", "run_002"], mem).startswith("same config measured on folds A, C: ")
    assert f(["run_003"], mem).startswith(
        "same config measured on another window set (fold not recorded): ")
    assert f(["run_009"], None).startswith("same config measured on another window set")


def test_the_exact_index_and_the_5a_gate_are_not_changed():
    # the exact lookup stays window-exact; the wildcard is a separate helper the gate never uses
    memory = _memory()
    key_d = (REPEATED_CONFIG, ("BTCUSD",), "1h", f"windows:{FOLD_D_SHA}")
    assert nov.lookup(key_d, memory, SPECS) == nov.NOVEL
    assert dn._exact_index(memory, SPECS).get(key_d) is None
    for rel in ("tools/anti_adjacency_gate.py", "workflow/run_phase1_research.py"):
        text = (SR_ROOT / rel).read_text(encoding="utf-8")
        assert "matches_on_other_windows" not in text and "window_free_key" not in text


# ---------------------------------------------------------------------------
# D-205: source_observations in the brief
# ---------------------------------------------------------------------------

def _brief_front(tmp_path, memory=None):
    p = _proposal(after=2.0)             # a NOVEL candidate: the picked one
    src = _src(p)
    inputs = _inputs(src, memory, folds=False)
    exact = dn._exact_index(inputs["memory"], inputs["protocol_specs"])
    cand = dn._candidate(RUN, inputs["memory"]["runs"][RUN], src, CAT, p, inputs, exact)
    record = {"picked": {"candidate_id": PID, "brief_path": "campaign_record/x/y.md"},
              "candidates": [cand]}
    _rel, text = dn.candidate_brief(record, inputs, decision_ref="d")
    path = tmp_path / "brief.md"
    path.write_text(text, encoding="utf-8")
    return camp._parse_brief_frontmatter(path)       # the registration-time brief check


def test_the_brief_carries_the_source_observations_verbatim(tmp_path):
    front = _brief_front(tmp_path)
    mem = _memory()["runs"][RUN]["observations"]
    got = front["candidate"]["source_observations"]
    assert len(got) == 2
    # the first carries all five keys, the memory entry's values untouched
    assert got[0] == {k: mem[0][k] for k in ("statement", "variant", "measured",
                                              "floors_met", "vehicle")}
    # an entry without `variant`/`measured`/`vehicle` (an old one) gets only what it has
    assert got[1] == {"statement": mem[1]["statement"], "floors_met": True}
    # nothing else of the observation is copied
    for row in got:
        assert not set(row) - set(dn.SOURCE_OBSERVATION_KEYS)
    assert front["candidate"]["source"]["source_run"] == RUN


def test_the_brief_has_no_section_when_the_source_has_no_observations(tmp_path):
    memory = _memory()
    del memory["runs"][RUN]["observations"]
    front = _brief_front(tmp_path, memory)
    assert "source_observations" not in front["candidate"]
    assert "source_observations" not in yaml.safe_dump(front)


def test_source_observations_of_an_entry_that_is_missing():
    assert dn.source_observations({"memory": {"runs": {}}}, RUN) == []
    assert dn.source_observations({}, RUN) == []
    assert dn.source_observations({"memory": {"runs": {RUN: {"observations": [{"lens": "x"}]}}}},
                                  RUN) == []
