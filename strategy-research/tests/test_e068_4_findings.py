"""
E-068 slice 4 -- the finding in campaign_memory.yaml and
artifacts/findings_summary.yaml (tools/claim_findings.py), under
orchestrator.claim_tests.enabled only. DESIGN_PROPOSAL.md sections 5 and 8.

Covers:
  1. Record shape on run_070's real artifacts (tests/fixtures/e068_4/run_070:
     the card, manifest, claim_status.yaml and the four claim_test.yaml files
     copied verbatim; protocol.json without its holdout block;
     protocol_result.yaml trimmed to its result run ids; the real memory
     entry). Numbers match VALIDATION_RUN.md; detail stays by reference.
  2. Size: the finding stays under a stated bound on run_070.
  3. Same attempt or no numbers: other bars, another spec_hash, a variant
     claim_measure skipped, a variant missing from claim_status.yaml, no
     claim_status.yaml at all -> not_measured, never old numbers.
  4. The window fingerprint is the novelty key's (non-partial run).
  5. No verdict words in any code-written string.
  6. The summary: built from run_070, deterministic, capped, same_spec_hash.
  7. The stage: flag off never calls the new code and writes the same bytes;
     flag on writes the finding + summary and validates against the schema;
     every failure is recorded and the stage still returns.
"""
import copy
import json
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
import campaign_memory as cm  # noqa: E402
import claim_findings as cf  # noqa: E402
import novelty as nv  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e058_s2a_regroup_record import ALL_ON, _seed, _memory_path, _memory  # noqa: E402

FIXTURE = SR_ROOT / "tests" / "fixtures" / "e068_4" / "run_070"
VIDS = ["base", "shock_lookback_250", "sol_generalization", "uni_defi"]
HIGH, LOW = "high_close_shock_reversion", "low_close_shock_reversion"
HIGH_HASH = "c688b1863f8cb3ff4d3a3bb05e0c15d5b885d27a65d3b805ad1990263fa83a99"
LOW_HASH = "859161e14578a12522d303685d6abad3614c0a94d27555c235ff660e2a850211"
# measured 2026-10-05 with novelty.protocol_spec on protocols/run_070_generated.json
NOVELTY_WINDOWS_SHA = "d931dfa50fb1aaddde738abd5eb1b2f9011df7e1c49fbc0ea7b0b87d492fb289"
FINDING_MAX_BYTES = 16_000      # the stated bound (run_070's finding is ~11.3 KB)
CLAIMS_ON = {**ALL_ON, "config_direct_authoring": {"enabled": True},
             "claim_tests": {"enabled": True}}
VERDICT_WORDS = re.compile(r"\b(supported|refuted|supports|refutes)\b", re.IGNORECASE)


@pytest.fixture
def run070(tmp_path) -> Path:
    dst = tmp_path / "run_070"
    shutil.copytree(FIXTURE, dst)
    return dst


def _entry(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "memory_entry.yaml").read_text(encoding="utf-8"))


def _build(run_dir: Path, **kw) -> dict:
    return cf.build_finding(run_dir, "run_070", kw.pop("entry", None) or _entry(run_dir), **kw)


def _edit_yaml(path: Path, fn) -> None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    fn(doc)
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _strings(obj, skip=("statement",)):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k)
            if k not in skip:
                yield from _strings(v, skip)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v, skip)
    elif isinstance(obj, str):
        yield obj


# ---------------------------------------------------------------------------
# 1-2. Record shape and size on run_070
# ---------------------------------------------------------------------------

def test_record_shape_on_run_070(run070):
    f = _build(run070)
    assert list(f) == ["finding_id", "label", "status", "reason", "information_only",
                       "statement", "kind", "block_visibility", "manifest_kind",
                       "claim_revision", "tests", "scope", "result", "trial_ids", "source"]
    assert f["finding_id"] == "F-run_070-1"
    assert f["label"] == "measured, not proven" and f["information_only"] is True
    assert (f["status"], f["reason"]) == ("measured", None)
    assert f["statement"].startswith("Unusually large 1-hour moves on BTC/ETH")
    assert f["kind"] == "event_behaviour"
    # run_070's tests read price level only: they cannot see the forecast block
    assert (f["block_visibility"], f["manifest_kind"]) == ("blind", "forecast")
    assert f["claim_revision"] is None
    assert [(t["name"], t["spec_hash"]) for t in f["tests"]] == [(HIGH, HIGH_HASH), (LOW, LOW_HASH)]
    assert f["tests"][0]["spec"]["selector"] == {"kind": "quantile", "field": "close",
                                                 "side": "top", "q": 0.1, "lookback": 100}
    assert f["scope"] == {"venue": "kraken", "product": "perp", "price_proxy": True,
                          "funding_modelled": False, "timeframe": "1h",
                          "symbols": ["BTCUSD", "SOLUSD", "UNIUSD"],
                          "period": {"start": "2022-01-01", "end": "2023-12-31"},
                          "windows_sha256": NOVELTY_WINDOWS_SHA, "windows_vary": False}
    assert f["trial_ids"] == [f"run_070:{v}" for v in VIDS]
    assert f["source"] == {
        "run_id": "run_070", "hypothesis_id": "HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH",
        "claim_status_ref": "runs/run_070/artifacts/claim_status.yaml",
        "claim_test_refs": {v: f"runs/run_070/artifacts/variants/{v}/claim_test.yaml"
                            for v in VIDS}}
    pv = f["result"]["per_variant"]
    assert sorted(pv) == VIDS and all(pv[v]["status"] == "measured" for v in VIDS)


def test_numbers_match_validation_run(run070):
    """VALIDATION_RUN.md's table (basis points, claimed sign / windows)."""
    pv = _build(run070)["result"]["per_variant"]
    cell = lambda v, t, h: pv[v]["tests"][t]["horizons"][h]  # noqa: E731
    assert round(cell("base", HIGH, "1")["effect"] * 1e4, 1) == 1.5
    assert (cell("base", HIGH, "1")["windows_claimed_sign"],
            cell("base", HIGH, "1")["windows_with_value"]) == (0, 6)
    assert round(cell("uni_defi", HIGH, "4")["effect"] * 1e4, 1) == -15.4
    assert cell("uni_defi", HIGH, "4")["windows_claimed_sign"] == 6
    assert round(cell("sol_generalization", LOW, "12")["effect"] * 1e4, 1) == -42.6
    assert cell("uni_defi", HIGH, "1")["n_events"] == 3110
    # base and the design variant measure the same (the tests are blind)
    assert pv["base"]["tests"] == pv["shock_lookback_250"]["tests"]
    # copied from claim_test.yaml: the horizon with the largest oriented effect
    assert pv["base"]["tests"][HIGH]["peak_horizon"] == 1
    assert pv["uni_defi"]["tests"][HIGH]["peak_horizon"] == 12


def test_detail_stays_by_reference(run070):
    f = _build(run070)
    text = yaml.safe_dump(f)
    for key in ("per_window", "per_era", "description", "oriented"):
        assert key not in text
    # one coin per variant: per_coin would only repeat the row
    assert "per_coin" not in text


def test_per_coin_kept_for_a_multi_coin_variant(run070):
    path = run070 / "artifacts" / "variants" / "base" / "claim_test.yaml"
    _edit_yaml(path, lambda d: d["tests"][HIGH]["horizons"][1]["per_coin"].update(
        {"ETHUSD": {"value": 0.5, "n_events": 7, "windows_with_claimed_sign": 1,
                    "windows_with_a_value": 2}}))
    row = _build(run070)["result"]["per_variant"]["base"]["tests"][HIGH]["horizons"]["1"]
    assert row["per_coin"]["ETHUSD"] == {"effect": 0.5, "n_events": 7,
                                         "windows_claimed_sign": 1, "windows_with_value": 2}


def test_finding_stays_under_the_stated_size(run070):
    entry = _entry(run070)
    f = _build(run070, entry=entry)
    size = len(yaml.safe_dump(f, sort_keys=False).encode("utf-8"))
    assert size <= FINDING_MAX_BYTES, size
    # and smaller than the full claim_test.yaml files it points to
    detail = sum(p.stat().st_size for p in run070.glob("artifacts/variants/*/claim_test.yaml"))
    assert size < detail / 4


# ---------------------------------------------------------------------------
# 3. Same attempt, or no numbers
# ---------------------------------------------------------------------------

def _assert_no_numbers(rec):
    assert rec["status"] == "not_measured" and "tests" not in rec


def test_other_bars_are_stale(run070):
    _edit_yaml(run070 / "artifacts" / "variants" / "uni_defi" / "protocol_result.yaml",
               lambda d: d["results"][0].update(run_id="20991231T000000Z_new"))
    f = _build(run070)
    rec = f["result"]["per_variant"]["uni_defi"]
    _assert_no_numbers(rec)
    assert rec["reason"] == "stale" and "other bars" in rec["detail"]
    assert rec["trial_id"] == "run_070:uni_defi"
    assert "run_070:uni_defi" not in f["trial_ids"] and "uni_defi" not in f["source"]["claim_test_refs"]
    assert f["status"] == "measured"            # the other three are bound
    assert "UNIUSD" not in f["scope"]["symbols"]


def test_all_stale_means_not_measured_stale(run070):
    for v in VIDS:
        _edit_yaml(run070 / "artifacts" / "variants" / v / "protocol_result.yaml",
                   lambda d: d["results"].pop())
    f = _build(run070)
    assert (f["status"], f["reason"]) == ("not_measured", "stale")
    assert f["trial_ids"] == [] and f["source"]["claim_test_refs"] == {}
    for v in VIDS:
        _assert_no_numbers(f["result"]["per_variant"][v])
    assert "effect" not in yaml.safe_dump(f)


def test_changed_spec_hash_is_stale(run070):
    _edit_yaml(run070 / "artifacts" / "hypothesis_card.yaml",
               lambda d: d["claim"]["tests"][0]["selector"].update(q=0.2))
    f = _build(run070)
    assert (f["status"], f["reason"]) == ("not_measured", "stale")
    assert all("spec_hash differs" in f["result"]["per_variant"][v]["detail"] for v in VIDS)


def test_claim_measure_skip_reason_passes_through(run070):
    _edit_yaml(run070 / "artifacts" / "claim_status.yaml", lambda d: d["variants"].update(
        base={"status": "not_measured", "reason": "stale_result", "file": None}))
    rec = _build(run070)["result"]["per_variant"]["base"]
    _assert_no_numbers(rec)
    assert rec["reason"] == "stale_result"


def test_variant_absent_from_claim_status_is_stale(run070):
    _edit_yaml(run070 / "artifacts" / "claim_status.yaml", lambda d: d["variants"].pop("base"))
    rec = _build(run070)["result"]["per_variant"]["base"]
    _assert_no_numbers(rec)
    assert rec["reason"] == "stale"


def test_untested_variant(run070):
    entry = _entry(run070)
    entry["variants"]["base"]["status"] = "failed"
    rec = _build(run070, entry=entry)["result"]["per_variant"]["base"]
    _assert_no_numbers(rec)
    assert rec["reason"] == "variant_failed"


def test_no_claim_status_file(run070):
    (run070 / "artifacts" / "claim_status.yaml").unlink()
    f = _build(run070)
    assert (f["status"], f["reason"]) == ("not_measured", "claim_status_absent")
    assert f["source"]["claim_status_ref"] is None


def test_run_level_gap_reason(run070):
    _edit_yaml(run070 / "artifacts" / "claim_status.yaml", lambda d: d.update(
        claim_status="not_measured", reason="tests_none", variants={}, tests=[]))
    f = _build(run070)
    assert (f["status"], f["reason"]) == ("not_measured", "tests_none")
    assert {r["reason"] for r in f["result"]["per_variant"].values()} == {"tests_none"}


def test_no_events(run070):
    for v in VIDS:
        def _empty(d):
            d.update(status="not_measured", reason="no_events")
            for t in d["tests"].values():
                t.update(status="no_events", reason="the selector matched no bars")
        _edit_yaml(run070 / "artifacts" / "variants" / v / "claim_test.yaml", _empty)
    f = _build(run070)
    assert (f["status"], f["reason"]) == ("no_events", "the selector matched no bars")
    rec = f["result"]["per_variant"]["base"]
    assert rec["status"] == "no_events" and "horizons" not in rec["tests"][HIGH]


def test_bars_missing_only_when_really_missing(run070):
    def _missing(d):
        d.pop("bars", None)
        d.update(status="not_measured", reason="bars_missing")
    _edit_yaml(run070 / "artifacts" / "variants" / "base" / "claim_test.yaml", _missing)
    assert _build(run070)["result"]["per_variant"]["base"]["reason"] == "bars_missing"
    # every bars file the current protocol_result names exists: not this attempt's
    for rel in cf._expected_bars(run070, "base"):
        (run070 / rel).parent.mkdir(parents=True, exist_ok=True)
        (run070 / rel).write_text("ts\n", encoding="utf-8")
    assert _build(run070)["result"]["per_variant"]["base"]["reason"] == "stale"


def test_exempt_card_is_not_applicable(run070):
    assert _build(run070, exempt="composition run")["block_visibility"] == "not_applicable"


def test_claim_revision_status_copied(run070):
    rpr.save_yaml(run070 / "artifacts" / "claim_revision.yaml", {"status": "accepted"})
    assert _build(run070)["claim_revision"] == "accepted"


# ---------------------------------------------------------------------------
# 4. The window fingerprint is the novelty key's
# ---------------------------------------------------------------------------

def test_windows_sha256_is_the_novelty_fingerprint(run070):
    f = _build(run070)
    for v in VIDS:
        p = json.loads((run070 / "artifacts" / "variants" / v / "protocol.json").read_text())
        assert f["result"]["per_variant"][v]["windows_sha256"] == nv.windows_fingerprint(
            p["windows"]) == NOVELTY_WINDOWS_SHA


def test_partial_windows_vary(run070):
    path = run070 / "artifacts" / "variants" / "uni_defi" / "protocol.json"
    p = json.loads(path.read_text())
    p["windows"] = p["windows"][:3]
    path.write_text(json.dumps(p))
    f = _build(run070)
    assert f["scope"]["windows_sha256"] is None and f["scope"]["windows_vary"] is True
    assert f["result"]["per_variant"]["uni_defi"]["windows_sha256"] == nv.windows_fingerprint(
        p["windows"])


# ---------------------------------------------------------------------------
# 5. No verdict words in code-written strings
# ---------------------------------------------------------------------------

def test_no_verdict_words(run070):
    entry = _entry(run070)
    f = _build(run070, entry=entry)
    summary = cf.findings_summary({"runs": {"run_070": {**entry, "finding": f}}}, "run_070")
    for s in list(_strings(f)) + list(_strings(summary)):
        assert not VERDICT_WORDS.search(s), s
    for s in _strings(rpr._claim_finding_error("run_070", ValueError("x"))):
        assert not VERDICT_WORDS.search(s), s
    assert not VERDICT_WORDS.search((SR_ROOT / "tools" / "claim_findings.py").read_text(
        encoding="utf-8"))


# ---------------------------------------------------------------------------
# 6. The summary
# ---------------------------------------------------------------------------

def _memory_with(run070, n=1) -> dict:
    entry = _entry(run070)
    f = _build(run070, entry=entry)
    runs = {}
    for i in range(n):
        rid = "run_070" if i == 0 else f"run_9{i:02d}"
        e = copy.deepcopy({**entry, "finding": f, "run_id": rid,
                           "recorded_at": f"2025-01-{i + 1:02d}T00:00:00+00:00"})
        runs[rid] = e
    return {"schema_version": 1, "runs": runs}


def test_summary_from_run_070(run070):
    s = cf.findings_summary(_memory_with(run070), "run_070")
    assert (s["n_findings"], s["n_listed"]) == (1, 1)
    assert s["by_status"] == {"measured": 1} and s["by_kind"] == {"event_behaviour": 1}
    assert s["label"] == "measured, not proven" and s["information_only"] is True
    row = s["findings"][0]
    assert row["finding_id"] == "F-run_070-1" and row["block_visibility"] == "blind"
    assert len(row["statement"]) <= cf.STATEMENT_CHARS
    assert row["scope"]["symbols"] == ["BTCUSD", "SOLUSD", "UNIUSD"]
    t = row["tests"][0]
    assert (t["name"], t["spec_hash"], t["direction"]) == (HIGH, HIGH_HASH, "less")
    assert t["by_variant"]["uni_defi"]["claimed_sign_windows"]["4"] == "6/6"
    assert round(t["by_variant"]["base"]["effect"]["1"] * 1e4, 1) == 1.5
    assert s["same_spec_hash"] == []


def test_summary_is_deterministic_and_ignores_runs_without_a_finding(run070):
    mem = _memory_with(run070)
    mem["runs"]["run_001"] = {"run_id": "run_001", "recorded_at": "2024-01-01"}
    a = yaml.safe_dump(cf.findings_summary(mem, "run_070"))
    b = yaml.safe_dump(cf.findings_summary(copy.deepcopy(mem), "run_070"))
    assert a == b and "run_001" not in a


def test_summary_newest_first_capped_and_repeats_listed(run070):
    mem = _memory_with(run070, n=3)
    mem["runs"]["run_902"]["finding"] = {"finding_id": "F-run_902-1", "status": "error",
                                         "label": "measured, not proven",
                                         "information_only": True}
    s = cf.findings_summary(mem, "run_902", max_rows=2)
    assert (s["n_findings"], s["n_listed"]) == (3, 2)
    assert [r["run_id"] for r in s["findings"]] == ["run_902", "run_901"]
    assert s["by_status"] == {"error": 1, "measured": 2}
    assert s["same_spec_hash"] == [{"spec_hash": h, "run_ids": ["run_070", "run_901"]}
                                   for h in sorted([HIGH_HASH, LOW_HASH])]


# ---------------------------------------------------------------------------
# 7. The stage
# ---------------------------------------------------------------------------

@pytest.fixture
def fixed_clock(monkeypatch):
    monkeypatch.setattr(cm, "_now", lambda r: r or "2025-01-01T00:00:00+00:00")


def _forbid_new_code(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("slice-4 code reached with the flag off")
    monkeypatch.setattr(rpr, "_claim_finding", boom)
    monkeypatch.setattr(rpr, "_write_findings_summary", boom)


@pytest.mark.parametrize("orch", [ALL_ON, {**ALL_ON, "config_direct_authoring": {"enabled": True},
                                           "claim_tests": {"enabled": False}}])
def test_flag_off_never_calls_the_new_code_and_writes_the_same_bytes(orch, monkeypatch,
                                                                      fixed_clock):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(variant_loop=True)
    rpr._run_regroup_record_stage("run_980", run_dir)
    reference = _memory_path().read_bytes()
    _memory_path().unlink()
    _forbid_new_code(monkeypatch)
    _set_orchestrator(orch)
    rpr._run_regroup_record_stage("run_980", run_dir)
    assert _memory_path().read_bytes() == reference
    assert "finding" not in _memory()["runs"]["run_980"]
    assert not (run_dir / "artifacts" / cf.SUMMARY_ARTIFACT).exists()


def test_flag_on_writes_finding_and_summary_and_matches_schema(fixed_clock):
    jsonschema = pytest.importorskip("jsonschema")
    _set_orchestrator(CLAIMS_ON)
    run_dir = _seed(variant_loop=True)
    out = rpr._run_regroup_record_stage("run_980", run_dir)
    f = _memory()["runs"]["run_980"]["finding"]
    assert out["entry"]["finding"] == f
    # the seeded run has no claim files: recorded, never guessed
    assert (f["status"], f["reason"]) == ("not_measured", "claim_status_absent")
    summary = yaml.safe_load((run_dir / "artifacts" / cf.SUMMARY_ARTIFACT).read_text())
    assert summary["n_findings"] == 1 and summary["findings"][0]["run_id"] == "run_980"
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" /
                         "campaign_memory.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(_memory(), schema)
    bad = copy.deepcopy(_memory())
    bad["runs"]["run_980"]["finding"]["status"] = "supported"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)


def test_flag_on_leaves_registry_and_kb_untouched(fixed_clock):
    _set_orchestrator(ALL_ON)
    run_dir = _seed(variant_loop=True, idea_status="validated")
    off = rpr._run_regroup_record_stage("run_980", run_dir)["entry"]
    _set_orchestrator(CLAIMS_ON)
    on = rpr._run_regroup_record_stage("run_980", run_dir)["entry"]
    assert on["registry"] == off["registry"] and on["kb_entry_id"] == off["kb_entry_id"]
    assert {k: v for k, v in on.items() if k != "finding"} == off


@pytest.mark.parametrize("where", ["build", "module", "retired"])
def test_a_finding_failure_is_recorded_and_the_stage_returns(where, monkeypatch, fixed_clock):
    _set_orchestrator(CLAIMS_ON)
    run_dir = _seed(variant_loop=True)
    if where == "build":
        monkeypatch.setattr(cf, "build_finding",
                            lambda *a, **k: (_ for _ in ()).throw(RuntimeError("bad file")))
    elif where == "module":
        monkeypatch.setattr(rpr, "_claim_findings_module",
                            lambda: (_ for _ in ()).throw(ImportError("no module")))
    else:
        monkeypatch.setattr(cf, "build_finding", lambda *a, **k: {
            "finding_id": "F-run_980-1", "status": "measured", "altitude": 3})
    out = rpr._run_regroup_record_stage("run_980", run_dir)
    f = _memory()["runs"]["run_980"]["finding"]
    assert out["entry"]["finding"] == f
    assert (f["status"], f["reason"], f["information_only"]) == ("error", "error", True)
    assert f["label"] == "measured, not proven"
    assert _memory()["runs"]["run_980"]["idea_status"] == "refuted"


def test_a_summary_failure_is_printed_and_the_stage_returns(monkeypatch, fixed_clock, capsys):
    _set_orchestrator(CLAIMS_ON)
    run_dir = _seed(variant_loop=True)
    monkeypatch.setattr(cf, "findings_summary",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("summary bug")))
    rpr._run_regroup_record_stage("run_980", run_dir)
    assert "finding" in _memory()["runs"]["run_980"]
    assert not (run_dir / "artifacts" / cf.SUMMARY_ARTIFACT).exists()
    assert "findings summary NOT written" in capsys.readouterr().out


def test_an_unreadable_flag_skips_the_finding(fixed_clock):
    _set_orchestrator({**ALL_ON, "config_direct_authoring": {"enabled": True},
                       "claim_tests": {"enabled": "yes"}})
    run_dir = _seed(variant_loop=True)
    rpr._run_regroup_record_stage("run_980", run_dir)
    assert "finding" not in _memory()["runs"]["run_980"]


def test_fault_entry_gets_no_finding(fixed_clock):
    _set_orchestrator(CLAIMS_ON)
    run_dir = _seed(variant_loop=True, errors_count=2)
    rpr._run_regroup_record_stage("run_980", run_dir)
    assert "finding" not in _memory()["runs"]["run_980"]
    assert not (run_dir / "artifacts" / cf.SUMMARY_ARTIFACT).exists()
