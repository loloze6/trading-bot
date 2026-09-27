"""
E-034 S3 -- the LATER anti-adjacency gate call site, right after
variant_selection.yaml exists (_route_post_variant_selection), REDESIGNED by
E-036 S2a (2026-09-27, engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md and
its operator decision).

E-036 S2a NOTE (applies to this whole file): the gate is now the binary
exact-match check (tools/novelty.py key, looked up in
campaign_record/campaign_memory.yaml). Every fixture that used to build a
family digest (campaign_record/exclusion_digest.yaml) now builds a memory
entry through the REAL writers instead (test_e036_s2a_exact_match_gate.
_prior_run_in_memory), and the candidate's key is computed by the gate from
the run's own candidate_strategy_config.json and pinned protocol. Retired
here, each with its reason:
  * test_flag_on_raises_when_digest_genuinely_absent -- the digest is no
    longer read; its fail-loud successor is
    test_flag_on_raises_when_memory_absent_and_regroup_record_off.
  * test_flag_on_raises_when_kb_genuinely_absent -- Layer 1 is advisory
    (operator decision 4), so a missing KB is recorded as
    `layer1_advisory.status: not_evaluated`, not a refusal to run; repointed
    as test_missing_kb_is_recorded_not_fatal.
  * test_pivot_away_from_clean_parent_is_caught_only_by_the_new_call_site
    -- its subject was the contrast with the pre-validation call site
    (_route_post_innovation_expansion), which is removed with
    anti_adjacency_retry.
  * test_multi_symbol_parent_card_checks_every_instrument_not_just_one and
    test_multi_symbol_parent_card_admits_when_no_instrument_collides -- the
    gate no longer iterates variant_selection.yaml's instruments: symbols
    come from the protocol the run executes, as a sorted set in one key
    (test_e036_s2a_exact_match_gate.test_novelty_symbols_compare_sorted and
    the two-symbol end-to-end repeats there).

Sandboxing: tests/conftest.py's autouse _sandbox_by_default fixture redirects
rpr.ROOT and camp.ROOT into a per-test tmp_path sandbox before any test body
runs.

Realism: every test that needs a variant_selection.yaml builds one by calling
the REAL rpr._record_variant_selection() -- never a hand-typed
variant_selection.yaml.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

from test_e036_s2a_exact_match_gate import (  # noqa: E402
    _config, _prior_run_in_memory, _protocol, _write_json)

_SR = Path(__file__).parent.parent
_REAL_KB_PATH = _SR / "campaign_record" / "campaign_knowledge_base.yaml"


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _set_flags(root: Path, *, variant_gate=None, variant_record=None) -> None:
    """None means the key is omitted entirely (absent-key-and-section case)."""
    orchestrator = {}
    if variant_record is not None:
        orchestrator["variant_selection_record"] = {"enabled": bool(variant_record)}
    if variant_gate is not None:
        orchestrator["variant_anti_adjacency_gate"] = {"enabled": bool(variant_gate)}
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    _write_yaml(config_dir / "campaign_config.yaml", {"orchestrator": orchestrator})


def _write_empty_kb(root: Path) -> None:
    _write_yaml(root / "campaign_record" / "campaign_knowledge_base.yaml", {"findings": []})


def _full_run(root: Path, run_id: str, *, hypothesis_card: dict, expanded_variants: list,
              selected_variant_id: str, config_rationale=None, config: dict = None) -> Path:
    """Same fixture shape as test_variant_selection_record.py's _minimal_run,
    plus (E-036 S2a) what run_loop has on disk when it calls the gate: the
    pinned protocol and candidate_strategy_config.json (backtest_spec.yaml's
    config, written the way run_loop writes it)."""
    run_dir = root / "runs" / run_id
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    config = config if config is not None else _config()

    hid = hypothesis_card.get("hypothesis_id", "H-TEST")
    _write_yaml(artifacts / "expanded_hypothesis_card.yaml", {
        "base_hypothesis_id": hid,
        "expanded_variants": expanded_variants,
    })
    _write_yaml(artifacts / "hypothesis_card.yaml", hypothesis_card)
    _write_yaml(artifacts / "backtest_spec.yaml", {
        "hypothesis_id": hid,
        "status": "spec_ready",
        "config": config,
        "config_rationale": config_rationale or [{"hypothesis_claim": "x", "config_choice": "y"}],
        "selected_variant_id": selected_variant_id,
    })
    _write_yaml(artifacts / "decision.yaml", {
        "stage": "backtest_specification", "status": "spec_ready",
        "rationale": "test rationale", "blocking_issues": [],
    })
    _protocol(f"{run_id}_generated.json")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id,
                                    {"protocol_ref": f"protocols/{run_id}_generated.json"})
    _write_json(artifacts / "candidate_strategy_config.json", config)
    return run_dir


def _record_selection(root: Path, run_dir: Path) -> None:
    """Produce a REAL variant_selection.yaml via the actual S2 function,
    flipping the flag on for the duration of the call -- tests that want
    variant_anti_adjacency_gate OFF (or a different variant_selection_record
    setting) set their own flags afterward."""
    _set_flags(root, variant_record=True)
    rpr._record_variant_selection(run_dir)


_CARD = {"hypothesis_id": "KELTNER_TEST", "target_market": "BTCUSDT", "timeframe": "1h",
         "library_lookup": {"indicator_id": "keltner_channel"},
         "thesis": "Keltner channel mean reversion."}


# ---------------------------------------------------------------------------
# _variant_anti_adjacency_gate_enabled -- same 4-case shape as the other
# orchestrator.<name>.enabled flags.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("enabled,expected", [(True, True), (False, False), (None, False)])
def test_variant_anti_adjacency_gate_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_flags(root, variant_gate=enabled)
    assert rpr._variant_anti_adjacency_gate_enabled() is expected


def test_variant_anti_adjacency_gate_enabled_false_when_config_file_absent():
    assert rpr._variant_anti_adjacency_gate_enabled() is False


# ---------------------------------------------------------------------------
# Flag-off bit-identity: compare actual output, not just assert the flag is
# False.
# ---------------------------------------------------------------------------

def test_flag_off_returns_none_and_writes_nothing():
    root = rpr.ROOT
    run_dir = _full_run(root, "run_950", hypothesis_card=_CARD,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    _record_selection(root, run_dir)
    # Memory shaped to REFUSE if the gate were ever consulted (an exact
    # repeat) -- proves flag-off isn't merely "nothing to refuse", it's "the
    # gate is never even invoked".
    _prior_run_in_memory("run_030", _config(), protocol_name="run_030_generated.json")
    _write_empty_kb(root)
    _set_flags(root, variant_gate=False, variant_record=True)

    state_path = run_dir / "pipeline_state.yaml"
    if not state_path.exists():
        _write_yaml(state_path, {"run_id": "run_950", "status": "active", "flags": {}, "audit_log": {}})
    before = state_path.read_bytes()

    result = rpr._route_post_variant_selection(run_dir, "run_950")

    assert result is None
    assert state_path.read_bytes() == before, (
        "flag-off must not write to pipeline_state.yaml at all"
    )
    assert not (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").exists()


def test_flag_off_key_and_section_absent_also_a_noop():
    root = rpr.ROOT
    card = {"hypothesis_id": "X", "target_market": "BTCUSDT", "timeframe": "1h"}
    run_dir = _full_run(root, "run_951", hypothesis_card=card,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    _record_selection(root, run_dir)
    _set_flags(root, variant_gate=None, variant_record=True)  # variant_gate key absent entirely

    assert rpr._route_post_variant_selection(run_dir, "run_951") is None
    assert not (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").exists()


# ---------------------------------------------------------------------------
# Dependencies: enabling this gate without its inputs must fail loud, not
# silently no-op and not silently ADMIT.
# ---------------------------------------------------------------------------

def test_flag_on_without_variant_selection_record_flag_raises():
    root = rpr.ROOT
    card = {"hypothesis_id": "X", "target_market": "BTCUSDT", "timeframe": "1h"}
    run_dir = _full_run(root, "run_952", hypothesis_card=card,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    # Deliberately do NOT produce variant_selection.yaml.
    _set_flags(root, variant_gate=True, variant_record=False)

    with pytest.raises(RuntimeError, match="variant_selection_record.enabled"):
        rpr._route_post_variant_selection(run_dir, "run_952")


def test_flag_on_missing_variant_selection_yaml_raises_caller_ordering_error():
    """Both flags true, variant_selection.yaml genuinely absent (e.g. a
    caller-ordering bug, or component_gap where _record_variant_selection
    was never reached) -- must raise, not silently ADMIT."""
    root = rpr.ROOT
    card = {"hypothesis_id": "X", "target_market": "BTCUSDT", "timeframe": "1h"}
    run_dir = _full_run(root, "run_953", hypothesis_card=card,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    _set_flags(root, variant_gate=True, variant_record=True)

    with pytest.raises(RuntimeError, match="variant_selection.yaml"):
        rpr._route_post_variant_selection(run_dir, "run_953")


def test_flag_on_raises_when_memory_absent_and_regroup_record_off():
    """E-036 S2a successor of test_flag_on_raises_when_digest_genuinely_absent:
    the gate reads campaign_memory.yaml, which only regroup_record writes."""
    root = rpr.ROOT
    run_dir = _full_run(root, "run_954", hypothesis_card=_CARD,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    _record_selection(root, run_dir)
    _write_empty_kb(root)
    _set_flags(root, variant_gate=True, variant_record=True)

    with pytest.raises(RuntimeError, match="campaign_memory.yaml"):
        rpr._route_post_variant_selection(run_dir, "run_954")


def test_missing_kb_is_recorded_not_fatal():
    """Repointed from test_flag_on_raises_when_kb_genuinely_absent: Layer 1 is
    advisory only since E-036 S2a, so the gate runs and records it."""
    root = rpr.ROOT
    _prior_run_in_memory("run_031", _config(0.9), protocol_name="run_031_generated.json")
    run_dir = _full_run(root, "run_955", hypothesis_card=_CARD,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    _record_selection(root, run_dir)
    # Deliberately do NOT call _write_empty_kb.
    _set_flags(root, variant_gate=True, variant_record=True)

    assert rpr._route_post_variant_selection(run_dir, "run_955") is None
    result = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert result["layer1_advisory"]["status"] == "not_evaluated"


# ---------------------------------------------------------------------------
# ADMIT case: a variant that is not an exact repeat ADMITs and leaves
# next_stage untouched.
# ---------------------------------------------------------------------------

def test_admit_returns_none_and_writes_result_artifact():
    root = rpr.ROOT
    _prior_run_in_memory("run_031", _config(0.9), protocol_name="run_031_generated.json")
    run_dir = _full_run(root, "run_956", hypothesis_card=_CARD,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1")
    _record_selection(root, run_dir)
    _write_empty_kb(root)
    _set_flags(root, variant_gate=True, variant_record=True)

    result = rpr._route_post_variant_selection(run_dir, "run_956")

    assert result is None
    written = yaml.safe_load(
        (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").read_text(encoding="utf-8"))
    assert written["route"] == "admit"
    assert written["outcome"] == "novel"
    assert written["selected_variant_id"] == "V1"


# ---------------------------------------------------------------------------
# Calibration case (S1/S2a/S2c): the 4h funding retest -- since E-036 S2a,
# Layer 1's verdict is recorded as an advisory next to the result.
# ---------------------------------------------------------------------------

def test_calibration_case_still_admits_through_the_new_call_site():
    """Repointed (E-036 S2a): the result's layer is the exact-match check;
    the KB calibration verdict (ADMIT for the open 4h branch) is recorded as
    `layer1_advisory`."""
    root = rpr.ROOT
    kb_dest = root / "campaign_record" / "campaign_knowledge_base.yaml"
    kb_dest.parent.mkdir(parents=True, exist_ok=True)
    kb_dest.write_bytes(_REAL_KB_PATH.read_bytes())
    _prior_run_in_memory("run_031", _config(0.9), protocol_name="run_031_generated.json")

    funding_4h_card = {
        "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED_4H_RETEST",
        "edge_source": {"evidence_type": "funding_open_interest",
                        "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at 4h."},
        "target_market": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "4h",
        "thesis": "Re-test the identical continuous funding-rate mean-reversion mechanism at 4h bars.",
    }
    run_id = "run_926"
    run_dir = _full_run(root, run_id, hypothesis_card=funding_4h_card,
                        expanded_variants=[{"variant_id": "V-4H-RETEST"}],
                        selected_variant_id="V-4H-RETEST")
    # the protocol this retest runs is 4h (the advisory reads its timeframe)
    _protocol(f"{run_id}_generated.json", timeframe="4h")
    _record_selection(root, run_dir)
    _set_flags(root, variant_gate=True, variant_record=True)

    assert rpr._route_post_variant_selection(run_dir, run_id) is None
    result = yaml.safe_load(
        (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").read_text(encoding="utf-8"))
    assert result["route"] == "admit"
    assert result["layer"] == "exact_match"
    assert result["layer1_advisory"]["status"] == "admit"
    assert result["selected_variant_id"] == "V-4H-RETEST"


# ---------------------------------------------------------------------------
# REFUSE policy, tested end to end: immediate escalation (no retry), a
# DISTINCT flag from anti_adjacency_gate_exhausted, and classified correctly
# by the project's existing escalation mechanism.
# ---------------------------------------------------------------------------

def test_refuse_escalates_immediately_no_retry_state_written():
    """Repointed (E-036 S2a): REFUSE requires an exact repeat of a tested
    variant in campaign memory; the policy under test is unchanged."""
    root = rpr.ROOT
    _prior_run_in_memory("run_031", _config(0.5), protocol_name="run_031_generated.json")
    run_dir = _full_run(root, "run_958", hypothesis_card=_CARD,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1",
                        config=_config(0.5))
    _record_selection(root, run_dir)
    _write_empty_kb(root)
    _write_yaml(run_dir / "pipeline_state.yaml",
                {"run_id": "run_958", "status": "active", "flags": {}, "audit_log": {}})
    _set_flags(root, variant_gate=True, variant_record=True)

    route = rpr._route_post_variant_selection(run_dir, "run_958")

    assert route == "human_pause"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    # No retry counter/attempt machinery: this checkpoint escalates on the
    # FIRST refusal.
    assert "anti_adjacency_gate_retry" not in state
    assert state["flags"]["variant_anti_adjacency_gate_refused"] is True
    assert state["flags"].get("anti_adjacency_gate_exhausted") is not True
    result = rpr.load_yaml(run_dir / "artifacts" / "variant_anti_adjacency_result.yaml")
    assert result["outcome"] == "repeat"
    assert result["matched"] == [{"run_id": "run_031", "variant_id": "run_031"}]


def test_refuse_classifies_via_existing_run_campaign_mechanism_and_is_not_quarantine_safe():
    """Repointed (E-036 S2a): same fixture change as the test above."""
    root = rpr.ROOT
    _prior_run_in_memory("run_032", _config(0.5), protocol_name="run_032_generated.json")
    run_dir = _full_run(root, "run_959", hypothesis_card=_CARD,
                        expanded_variants=[{"variant_id": "V1"}], selected_variant_id="V1",
                        config=_config(0.5))
    _record_selection(root, run_dir)
    _write_empty_kb(root)
    _write_yaml(run_dir / "pipeline_state.yaml",
                {"run_id": "run_959", "status": "active", "flags": {}, "audit_log": {}})
    _set_flags(root, variant_gate=True, variant_record=True)

    rpr._route_post_variant_selection(run_dir, "run_959")

    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    reason = camp._classify_human_pause(run_dir, state)
    assert reason == "variant_anti_adjacency_gate_refused"
    assert reason != "anti_adjacency_gate_exhausted"
    assert reason not in camp._QUARANTINE_SAFE_REASONS, (
        "a genuine must-escalate -- never auto-quarantined/auto-continued"
    )
    assert reason not in camp._REQUEUEABLE_QUARANTINE_REASONS


def test_flag_table_carries_the_new_flag():
    """R11 cross-check (FIX 6 precedent, 2026-08-24): the table must not
    rot away from _classify_human_pause for THIS flag either."""
    table_flags = {flag for flag, _ in camp._PAUSE_FLAG_TO_REASON}
    assert "variant_anti_adjacency_gate_refused" in table_flags
    mapped = dict(camp._PAUSE_FLAG_TO_REASON)
    assert mapped["variant_anti_adjacency_gate_refused"] == "variant_anti_adjacency_gate_refused"


# ---------------------------------------------------------------------------
# _record_variant_selection's target_market shapes (E-034 S3 review fix,
# 2026-08-25) -- unchanged by E-036 S2a.
# ---------------------------------------------------------------------------

def test_dict_target_market_with_asset_key_resolves_to_a_scalar():
    root = rpr.ROOT
    dict_card = {
        "hypothesis_id": "DICT_SHAPE_PARENT",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": {"asset": "BTCUSDT", "venue": "spot"},
        "timeframe": "1h",
        "thesis": "Keltner channel, structured target_market shape.",
    }
    run_id = "run_962"
    run_dir = _full_run(root, run_id, hypothesis_card=dict_card,
                        expanded_variants=[{"variant_id": "V-ONE"}],
                        selected_variant_id="V-ONE")
    _record_selection(root, run_dir)

    selection = yaml.safe_load((run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8"))
    assert selection["instrument"] == "BTCUSDT"


def test_unresolvable_target_market_shape_raises_not_silently_admits():
    root = rpr.ROOT
    bad_card = {
        "hypothesis_id": "BAD_SHAPE_PARENT",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": {"unrelated_key": "no asset here"},
        "timeframe": "1h",
        "thesis": "Keltner channel, unresolvable target_market shape.",
    }
    run_id = "run_963"
    run_dir = _full_run(root, run_id, hypothesis_card=bad_card,
                        expanded_variants=[{"variant_id": "V-ONE"}],
                        selected_variant_id="V-ONE")
    _set_flags(root, variant_record=True)
    with pytest.raises(RuntimeError, match="cannot resolve an instrument"):
        rpr._record_variant_selection(run_dir)
