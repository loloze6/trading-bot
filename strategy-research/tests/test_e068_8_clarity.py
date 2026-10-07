"""
E-068 PR B "clarity" (D-077; delivery plan v26 continuation 2, section 9,
items 1, 4, 6).

Sections:
  1. No claim verdict in the running pipeline: the flag-on instruction files
     carry no verdict wording; tools/claim_tests.py marks its verdict path
     PARKED (CUL-394); the measurement note names no verdict.
  2. The run file is claim_measurement.yaml: written under the new name only,
     read by the findings, the readers' digest and the v3 handoff, an older
     run's claim_status.yaml still read, both names cleared.
  3. CUL-413: every number in the readers' digest names its statistic; the
     forecast_power report labels its Pearson correlation (v3 readers only);
     the reading contract asks for the exact statistic.
  4. Requests in one place: the detector wishlist lives in campaign_record/
     (an older checkout's config/ copy still read); the campaign summary's
     "Requests" section (only when a request file exists).
"""
import os
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import build_reports as br  # noqa: E402
import claim_findings as cf  # noqa: E402
import claim_measure as cm  # noqa: E402
import claim_tests as ct  # noqa: E402
import reader_findings as rf  # noqa: E402

from test_e068_s3_claim_measure import ON, UP, _claim, _fixture_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e068_5_readers_v3 import V3_ON  # noqa: E402

SKILLS = SR_ROOT / "workflow_artifacts" / "skills"
FIX4 = SR_ROOT / "tests" / "fixtures" / "e068_4" / "run_070"


# ---------------------------------------------------------------------------
# 1. No claim verdict in the running pipeline
# ---------------------------------------------------------------------------

# The flag-on-only inputs that tell a model about the claim (added to
# required_inputs only under orchestrator.claim_tests / reader_findings).
FLAG_ON_INSTRUCTIONS = [
    "hypothesis-design/CLAIM_TESTS.md",
    "hypothesis-design/PREFILLED_CLAIM.md",
    "claim-revision/SKILL.md",
    "readers_v3/READING_CONTRACT.md",
    *[f"readers_v3/{c}-reader/SKILL.md" for c in
      ("profitability", "forecast_power", "regime_power", "component_attribution",
       "trade_efficiency")],
]
VERDICT_WORDING = re.compile(
    r"\b(verdicts?|supported|supports?|refuted|refutes?|proven|proves?|confirm\w*|"
    r"inconclusive|significant\w*|significance|pass(?:es|ed)?|fail(?:s|ed)?|true|false|"
    r"grade[sd]?)\b", re.IGNORECASE)
# Explicit allowlist: field names and fixed phrases that are not a verdict.
ALLOWED = ("pass_if", "fail_if", "pass_through", "pass-through", "`significance`",
           "measured, not proven", "the claim is not graded", "nothing you write grades the claim",
           "graded variant")


def _verdict_hits(text: str) -> list:
    for phrase in ALLOWED:
        text = text.replace(phrase, " ")
    return sorted({m.group(0) for m in VERDICT_WORDING.finditer(text)})


@pytest.mark.parametrize("rel", FLAG_ON_INSTRUCTIONS)
def test_flag_on_instruction_files_carry_no_claim_verdict_wording(rel):
    text = (SKILLS / rel).read_text(encoding="utf-8")
    assert _verdict_hits(text) == [], rel


def test_the_wording_check_catches_verdict_words():
    assert _verdict_hits("the claim is supported only if ALL pass") == ["pass", "supported"]
    assert _verdict_hits("write pass_if and fail_if for a pass-through card") == []
    assert _verdict_hits("`verdict_possible: false`") == ["false"]


def test_the_instruction_files_are_flag_on_only_inputs():
    """No flag-off SKILL (the 1a/1b skills, the v2 readers, ...) names them:
    they reach a prompt only through the flag-on input lists."""
    skills = list(SKILLS.glob("*/SKILL.md")) + list(SKILLS.glob("readers/*/SKILL.md"))
    assert len(skills) > 10
    for skill in skills:
        if skill.parent.name == "claim-revision":
            continue
        text = skill.read_text(encoding="utf-8")
        for name in ("CLAIM_TESTS", "READING_CONTRACT", "PREFILLED_CLAIM", "claim-revision"):
            assert name not in text, (skill, name)


def test_claim_tests_marks_its_verdict_path_parked():
    doc = ct.__doc__
    assert "PARKED (CUL-394" in doc and "D-077" in doc
    head = doc[doc.index("PARKED (CUL-394"):doc.index("OPERATOR RULES")]
    for name in ("_graded", "_a851a_horizon", "fake_window", "combine", "run_test",
                 "CALIBRATION_GATE", "judge_calibration_row", "passed_calibrations",
                 "calibration_for", "grade_claim_file", "main", "SIGNIFICANCE_METHODS"):
        assert name in head, name
        assert hasattr(ct, name), name
    assert "profit bars" in head and "holdout" in head


def test_the_measurement_note_names_no_verdict():
    for text in (cm.NOTE, cm.LABEL, rf.NOTE, rf.STATISTICS_NOTE):
        assert "verdict" not in text.lower()
    assert "not graded" in cm.NOTE


# ---------------------------------------------------------------------------
# 2. claim_measurement.yaml
# ---------------------------------------------------------------------------

def test_run_file_names():
    assert cm.RUN_FILE == "claim_measurement.yaml"
    assert cm.OLD_RUN_FILE == "claim_status.yaml"
    assert cm.RUN_FILES == (cm.RUN_FILE, cm.OLD_RUN_FILE)


@pytest.mark.parametrize("present,want", [
    ((), "claim_measurement.yaml"),
    (("claim_status.yaml",), "claim_status.yaml"),
    (("claim_measurement.yaml",), "claim_measurement.yaml"),
    (("claim_status.yaml", "claim_measurement.yaml"), "claim_measurement.yaml"),
], ids=["none", "old_only", "new_only", "both"])
def test_run_file_path_reads_the_new_name_else_the_old(tmp_path, present, want):
    for name in present:
        (tmp_path / name).write_text("x: 1\n", encoding="utf-8")
    assert cm.run_file_path(tmp_path) == tmp_path / want
    assert rpr._claim_measurement_name(None) == "claim_measurement.yaml"


def test_measurement_writes_only_the_new_name():
    _set_orchestrator(ON)
    run_dir = _fixture_run("run_981", claim=_claim([UP]))
    rpr._measure_claim_tests_after_backtests(run_dir, "run_981")
    arts = run_dir / "artifacts"
    assert rpr.load_yaml(arts / "claim_measurement.yaml")["claim_status"] == "measured"
    assert not (arts / "claim_status.yaml").exists()


def test_the_safety_net_writes_the_new_name(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _fixture_run("run_982", claim=_claim([UP]))

    def _boom(*a, **k):
        raise RuntimeError("measure bug")
    monkeypatch.setattr(rpr, "_measure_claim_tests", _boom)
    rpr._measure_claim_tests_after_backtests(run_dir, "run_982")
    arts = run_dir / "artifacts"
    doc = rpr.load_yaml(arts / "claim_measurement.yaml")
    assert (doc["claim_status"], doc["reason"]) == ("not_measured", "error")
    assert not (arts / "claim_status.yaml").exists()


def test_clearing_removes_both_names_only_with_the_flag_on():
    run_dir = _fixture_run("run_983", claim=_claim([UP]))
    arts = run_dir / "artifacts"
    files = [arts / "claim_measurement.yaml", arts / "claim_status.yaml",
             arts / "variants" / "base" / "claim_test.yaml"]
    for p in files:
        p.write_text("stale\n", encoding="utf-8")
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    rpr._clear_claim_measure_files(run_dir)
    assert all(p.exists() for p in files)
    _set_orchestrator(ON)
    rpr._clear_claim_measure_files(run_dir)
    assert not any(p.exists() for p in files)


@pytest.fixture
def run070(tmp_path) -> Path:
    dst = tmp_path / "run_070"
    shutil.copytree(FIX4, dst)
    return dst


def _entry(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "memory_entry.yaml").read_text(encoding="utf-8"))


def _rename_to_new(run_dir: Path) -> None:
    arts = run_dir / "artifacts"
    old, new = arts / "claim_status.yaml", arts / "claim_measurement.yaml"
    st = os.stat(old)
    old.rename(new)
    os.utime(new, ns=(st.st_atime_ns, st.st_mtime_ns))   # same attempt, same age


def test_an_old_run_with_only_claim_status_is_still_read(run070):
    """run_070 was measured before D-077: only claim_status.yaml."""
    assert (run070 / "artifacts" / "claim_status.yaml").exists()
    assert not (run070 / "artifacts" / "claim_measurement.yaml").exists()
    finding = cf.build_finding(run070, "run_070", _entry(run070))
    digest = rf.claim_result_digest(run070)
    assert finding["status"] == "measured"
    assert finding["source"]["claim_status_ref"] == "runs/run_070/artifacts/claim_status.yaml"
    assert digest["claim_status"] == "measured" and "status" not in digest
    assert set(digest["variants"]) == {"base", "shock_lookback_250", "sol_generalization",
                                       "uni_defi"}
    assert digest["variants"]["uni_defi"]["status"] == "measured"


def test_the_new_name_gives_the_same_finding_and_digest(run070):
    finding_old = cf.build_finding(run070, "run_070", _entry(run070))
    digest_old = rf.claim_result_digest(run070)
    _rename_to_new(run070)
    finding_new = cf.build_finding(run070, "run_070", _entry(run070))
    digest_new = rf.claim_result_digest(run070)
    assert digest_new == digest_old
    assert finding_new["source"]["claim_status_ref"] == \
        "runs/run_070/artifacts/claim_measurement.yaml"
    finding_new["source"]["claim_status_ref"] = finding_old["source"]["claim_status_ref"]
    assert finding_new == finding_old


def test_the_new_name_wins_over_an_old_copy(run070):
    _rename_to_new(run070)
    (run070 / "artifacts" / "claim_status.yaml").write_text(
        yaml.safe_dump({"claim_status": "not_measured", "reason": "old_copy", "variants": {}}),
        encoding="utf-8")
    assert rf.claim_result_digest(run070)["claim_status"] == "measured"
    assert cf.build_finding(run070, "run_070", _entry(run070))["status"] == "measured"


def test_a_variant_missing_from_the_run_file_names_that_file(run070):
    _rename_to_new(run070)
    path = run070 / "artifacts" / "claim_measurement.yaml"
    st = os.stat(path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["variants"].pop("base")
    path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns))
    digest = rf.claim_result_digest(run070)
    assert digest["variants"].get("base") is None
    finding = cf.build_finding(run070, "run_070", _entry(run070))
    assert "claim_measurement.yaml" in finding["result"]["per_variant"]["base"]["detail"]
    assert rf._variant_digest(run070, "base", None, {}, run_file="claim_measurement.yaml") == \
        {"status": "not_measured", "reason": "not in claim_measurement.yaml"}


def test_the_v3_handoff_names_the_file_the_run_has(tmp_path):
    run_dir = tmp_path / "run_x"
    arts = run_dir / "artifacts"
    arts.mkdir(parents=True)
    assert rpr._claim_measurement_name(run_dir) == "claim_measurement.yaml"
    (arts / "claim_status.yaml").write_text("x: 1\n", encoding="utf-8")
    assert rpr._claim_measurement_name(run_dir) == "claim_status.yaml"
    (arts / "claim_measurement.yaml").write_text("x: 1\n", encoding="utf-8")
    assert rpr._claim_measurement_name(run_dir) == "claim_measurement.yaml"


def test_the_v3_handoff_lists_the_measurement_file(monkeypatch):
    from test_e068_5_readers_v3 import RUN_ID, _run070_shaped
    run_dir = _run070_shaped(monkeypatch)
    arts = run_dir / "artifacts"

    def _optional():
        h = rpr._reader_handoff("profitability", RUN_ID, 0, run_dir)
        return [r["path"] for r in h["optional_inputs"]]
    assert _optional()[-1] == "artifacts/claim_measurement.yaml"
    (arts / "claim_status.yaml").write_text("claim_status: measured\n", encoding="utf-8")
    assert _optional()[-1] == "artifacts/claim_status.yaml"


# ---------------------------------------------------------------------------
# 3. CUL-413: every statistic named
# ---------------------------------------------------------------------------

def test_every_claim_statistic_has_a_label():
    assert set(rf.STATISTIC_LABELS) == set(ct.STATISTICS)
    assert "Spearman" in rf.STATISTIC_LABELS["rank_ic"]
    assert "rank IC" in rf.STATISTIC_LABELS["rank_ic"]
    for name in ("mean_diff", "hit_rate", "decay_curve"):
        assert "not a correlation" in rf.STATISTIC_LABELS[name], name
    for label in rf.STATISTIC_LABELS.values():
        assert "horizons in bars" in label and "Pearson" not in label
    assert "no label" in rf.statistic_label("moon")
    assert rf.statistic_label("rank_ic") == rf.STATISTIC_LABELS["rank_ic"]


def test_the_digest_labels_every_test_and_every_number(run070):
    d = rf.claim_result_digest(run070)
    assert "Pearson" in d["statistics_note"] and "forecast_return_corr" in d["statistics_note"]
    assert d["tests"] and all(t["statistic_label"] == rf.STATISTIC_LABELS[t["statistic"]]
                              for t in d["tests"])
    stats = {t["name"]: t["statistic"] for t in d["tests"]}
    n = 0
    for vid, v in d["variants"].items():
        for name, t in (v.get("tests") or {}).items():
            assert t["statistic_label"] == rf.STATISTIC_LABELS[stats[name]], (vid, name)
            n += 1
    assert n == 8      # four variants, two tests each


def test_earlier_runs_findings_are_labelled_too(monkeypatch):
    """Review: the v3 readers' earlier-findings file labels each test's effect."""
    tests = [{"name": "t", "spec_hash": "h", "statistic": "rank_ic", "direction": "greater",
              "by_variant": {}}]
    memory = {"runs": {"run_060": {cf.FINDING_KEY: {"status": "measured", "tests": []}}}}
    monkeypatch.setattr(cf, "findings_summary", lambda m, r, max_rows=10: {
        "findings": [{"run_id": "run_060", "tests": tests}], "n_findings": 1,
        "by_status": {}, "by_kind": {}, "same_spec_hash": []})
    s = rf.reader_findings_summary(memory, "run_071")
    assert s["statistic_labels"] == {"rank_ic": rf.STATISTIC_LABELS["rank_ic"]}
    assert s["findings"][0]["tests"][0]["statistic"] == "rank_ic"


def test_forecast_power_labels_only_when_asked(monkeypatch, tmp_path):
    monkeypatch.setattr(br, "load_run_sources", lambda run_dir: {})
    monkeypatch.setattr(br, "BUILDERS", {c: (lambda s, c=c: {"category": c, "slices": {}})
                                         for c in br.REPORT_CATEGORIES})
    plain = br.build_reports(tmp_path, write=False)
    labelled = br.build_reports(tmp_path, write=False, label_statistics=True)
    assert "statistic_labels" not in plain["forecast_power"]
    assert labelled["forecast_power"]["statistic_labels"] == br.FORECAST_POWER_STATISTIC_LABELS
    def _same(d):
        return {k: v for k, v in d.items() if k not in ("generated_at", "statistic_labels")}
    for c in br.REPORT_CATEGORIES:
        assert _same(labelled[c]) == _same(plain[c])
        assert ("statistic_labels" in labelled[c]) is (c == "forecast_power")


def test_forecast_power_labels_say_pearson():
    labels = br.FORECAST_POWER_STATISTIC_LABELS
    assert set(labels) == {"forecast_return_corr", "forecast_return_corr_pvalue",
                           "median_forecast_return_corr",
                           "prescreen_pooled_ic"}
    pre = labels["prescreen_pooled_ic"]
    assert "Spearman" in pre and "not by the claim test" in pre
    assert "inside prescreen_backtest_cross_check" in pre
    assert "Pearson" in labels["forecast_return_corr"]
    assert "next bar's return" in labels["forecast_return_corr"]
    assert "active bars" in labels["forecast_return_corr"]
    assert "Pearson" in labels["median_forecast_return_corr"]


def test_the_report_label_is_passed_under_reader_findings_only(monkeypatch):
    _set_orchestrator(None)
    assert rpr._report_statistic_labels_kw() == {}
    _set_orchestrator(V3_ON)
    assert rpr._report_statistic_labels_kw() == {"label_statistics": True}
    _set_orchestrator({"reader_findings": {"enabled": "yes"}})
    assert rpr._report_statistic_labels_kw() == {}


def test_the_reading_contract_asks_for_the_exact_statistic():
    text = (SKILLS / "readers_v3" / "READING_CONTRACT.md").read_text(encoding="utf-8")
    assert "cites the digest's numbers and names the statistic exactly" in text
    assert "`statistic_label`" in text
    fp = (SKILLS / "readers_v3" / "forecast_power-reader" / "SKILL.md").read_text(encoding="utf-8")
    assert "Pearson" in fp and "rank IC, hit rates" not in fp


# ---------------------------------------------------------------------------
# 4. Requests in one place
# ---------------------------------------------------------------------------

def test_the_detector_wishlist_lives_in_campaign_record():
    assert (SR_ROOT / "campaign_record" / "detector_wishlist.yaml").exists()
    assert not (SR_ROOT / "config" / "detector_wishlist.yaml").exists()
    assert camp.DETECTOR_WISHLIST_REL == "campaign_record/detector_wishlist.yaml"


def _wl(root: Path, rel: str, family: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"candidates": [{"family": family}]}), encoding="utf-8")
    return path


@pytest.mark.parametrize("present,want", [
    ((), "campaign_record/detector_wishlist.yaml"),
    (("config/detector_wishlist.yaml",), "config/detector_wishlist.yaml"),
    (("campaign_record/detector_wishlist.yaml",), "campaign_record/detector_wishlist.yaml"),
    (("config/detector_wishlist.yaml", "campaign_record/detector_wishlist.yaml"),
     "campaign_record/detector_wishlist.yaml"),
], ids=["none", "old_checkout", "new", "both"])
def test_the_detector_wishlist_path_falls_back_for_older_checkouts(monkeypatch, tmp_path,
                                                                   present, want):
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    for rel in present:
        _wl(tmp_path, rel, rel.split("/")[0])
    assert camp._detector_wishlist_path() == tmp_path / want


def test_the_wishlist_readers_read_campaign_record(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    _wl(tmp_path, "campaign_record/detector_wishlist.yaml", "new_family")
    _wl(tmp_path, "config/detector_wishlist.yaml", "old_family")
    assert camp._wishlist_family_names() == ["new_family"]
    assert camp._find_wishlist_entry("new_family") == {"family": "new_family"}
    assert camp._find_wishlist_entry("old_family") is None


def test_the_trigger_status_is_written_back_to_campaign_record(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    (tmp_path / "campaign_record").mkdir()
    (tmp_path / "campaign_record" / "campaign_knowledge_base.yaml").write_text(
        yaml.safe_dump({"findings": [{"id": "f1", "outcome": "no_edge_observed"}]}),
        encoding="utf-8")
    path = tmp_path / "campaign_record" / "detector_wishlist.yaml"
    path.write_text(yaml.safe_dump({"candidates": [{"family": "fam", "trigger_condition": {
        "predicate": {"source": "kb_finding", "all_of": [
            {"field": "outcome", "op": "==", "value": "kill"}]}}}]}), encoding="utf-8")
    camp.evaluate_and_persist_wishlist_predicate("fam")
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc["candidates"][0]["trigger_condition"]["status"] == "not_triggered"
    assert not (tmp_path / "config" / "detector_wishlist.yaml").exists()


def _summary() -> str:
    camp._regenerate_summary({"version": "1.0", "queue": []})
    return camp.CAMPAIGN_SUMMARY_PATH.read_text(encoding="utf-8")


def _write(rel: str, doc) -> None:
    path = camp.ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def test_no_requests_section_without_a_request_file():
    assert camp._summary_request_lines() == []
    text = _summary()
    assert "Requests" not in text


def test_the_requests_section_counts_open_rows_and_shows_the_newest():
    _write("campaign_record/component_requests.yaml", {"requests": [
        {"run_id": f"run_00{i}", "stage": "strategy_config_authoring", "variant_id": None,
         "reason": f"component gap number {i}"} for i in range(1, 6)]})
    _write("campaign_record/test_requests.yaml", {"requests": [
        {"run_id": "run_010", "stage": "hypothesis_generation", "hypothesis_id": "H-1",
         "missing_block": "outcome fwd_return_of(other_symbol, h)"}]})
    _write("campaign_record/feed_wishlist.yaml", {"version": "1.0", "wishlist": [
        {"feed_name": "liquidation_data", "priority_rationale": "resolves   volume\nambiguity"}]})
    _write("campaign_record/detector_wishlist.yaml", {"candidates": [
        {"family": "adx_threshold", "description": "ADX gate", "trigger_condition":
         {"status": "not_triggered"}}]})
    text = _summary()
    block = text[text.index("## Requests"):text.index("## Scoreboard")]
    assert "Open = every row" in block
    lines = block.splitlines()
    i = lines.index("- `component_requests.yaml`: 5 open")
    assert lines[i + 1:i + 4] == [
        f"  - run_00{n} (strategy_config_authoring): component gap number {n}" for n in (3, 4, 5)]
    assert "run_001" not in block and "run_002" not in block
    assert "- `test_requests.yaml`: 1 open" in lines
    assert "  - run_010 (hypothesis_generation): outcome fwd_return_of(other_symbol, h)" in lines
    assert "- `feed_wishlist.yaml`: 1 open" in lines
    assert "  - liquidation_data: resolves volume ambiguity" in lines
    assert "- `detector_wishlist.yaml`: 1 open" in lines
    assert "  - adx_threshold: ADX gate" in lines
    assert "data_requests.yaml" not in block       # absent file: not listed
    order = [ln.split("`")[1] for ln in lines if ln.startswith("- `")]
    assert order == ["component_requests.yaml", "test_requests.yaml", "feed_wishlist.yaml",
                     "detector_wishlist.yaml"]


def test_an_older_checkouts_detector_wishlist_is_counted():
    _write("config/detector_wishlist.yaml", {"candidates": [{"family": "a"}, {"family": "b"}]})
    assert "- `detector_wishlist.yaml`: 2 open" in camp._summary_request_lines()


def test_a_bad_request_file_never_breaks_the_summary():
    (camp.ROOT / "campaign_record").mkdir(parents=True, exist_ok=True)
    (camp.ROOT / "campaign_record" / "data_requests.yaml").write_text("requests: [unclosed",
                                                                       encoding="utf-8")
    _write("campaign_record/test_requests.yaml", {"requests": {"not": "a list"}})
    _write("campaign_record/component_requests.yaml", ["a", "list"])
    lines = camp._summary_request_lines()
    assert any(ln.startswith("- `data_requests.yaml`: unreadable") for ln in lines)
    assert any(ln.startswith("- `test_requests.yaml`: unreadable") for ln in lines)
    assert any(ln.startswith("- `component_requests.yaml`: unreadable") for ln in lines)
    assert "## Requests" in _summary()


def test_an_empty_request_file_counts_zero():
    _write("campaign_record/component_requests.yaml", None)
    assert "- `component_requests.yaml`: 0 open" in camp._summary_request_lines()


def test_a_long_request_row_is_one_short_line():
    line = camp._summary_request_row({"run_id": "run_1", "reason": "a | b\n" + "x " * 200})
    assert line.startswith("run_1: a / b x x")       # a table-safe line, whitespace folded
    assert len(line) == camp._SUMMARY_REQUEST_LINE_CHARS and line.endswith("...")
    assert "\n" not in line and "|" not in line
    assert camp._summary_request_row({"run_id": "run_2"}) == "run_2"
    assert camp._summary_request_row("bare text") == "bare text"
