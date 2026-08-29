"""
E-034 S3 -- the NEW, LATER anti-adjacency gate call site, right after
variant_selection.yaml exists.

Closes the OPEN DEFECT logged in E-032/EPIC.md on 2026-08-24: the ONLY
existing gate call site (_route_post_innovation_expansion, tested in
test_anti_adjacency_retry_policy.py) runs BEFORE `validation`, reading the
pre-expansion PARENT hypothesis_card.yaml -- it structurally cannot see what
innovation_expansion invented, and it runs before backtest_specification has
chosen a variant at all. This file proves the NEW call site
(_route_post_variant_selection, called right after _record_variant_selection
succeeds) actually gates the CHOSEN VARIANT, and that the defect is closed
end-to-end -- not just theoretically -- via
test_pivot_away_from_clean_parent_is_caught_only_by_the_new_call_site below,
which is the direct, executable proof: same run, same parent card, the OLD
gate ADMITs and the NEW gate REFUSEs, because only the NEW gate ever sees
where the chosen variant actually landed.

Sandboxing: tests/conftest.py's autouse _sandbox_by_default fixture redirects
rpr.ROOT and camp.ROOT into a per-test tmp_path sandbox before any test body
runs -- same precedent as test_anti_adjacency_retry_policy.py /
test_variant_selection_record.py.

Realism: every test that needs a variant_selection.yaml builds one by calling
the REAL rpr._record_variant_selection() against real expanded_hypothesis_
card.yaml / backtest_spec.yaml / hypothesis_card.yaml / decision.yaml
fixtures (same fixture shape as test_variant_selection_record.py), then feeds
that real artifact into rpr._route_post_variant_selection() -- never a
hand-typed variant_selection.yaml -- so the gate is proven "through
orchestration," the same bar test_anti_adjacency_retry_policy.py's own
calibration-case test set for S2c.
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
import build_exclusion_digest as bed  # noqa: E402

_SR = Path(__file__).parent.parent
_REAL_KB_PATH = _SR / "campaign_record" / "campaign_knowledge_base.yaml"
_REAL_RUN_059_DIR = _SR / "runs" / "run_059"


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


def _write_digest(root: Path, families: dict) -> None:
    _write_yaml(
        root / "campaign_record" / "exclusion_digest.yaml",
        {
            "families": families,
            "failed_families_passthrough": [],
            "components_built_passthrough": [],
        },
    )


def _kc_digest(*instrument_run_pairs, timeframe="4h") -> dict:
    """Coarse-fidelity entries (no fingerprint) -- exactly the shape a
    pre-E-036 digest, or a run with no candidate_strategy_config.json, has.
    E-036 S2 design point 3: a coarse match can never produce REPEAT, only
    NEIGHBOUR -- so a bare (family, instrument, timeframe) collision built
    with this helper ADMITs (as a neighbour), it does not REFUSE."""
    return {
        "keltner_channel": {
            "confidence": "structural_indicator_id",
            "triples": [
                {
                    "instrument": inst,
                    "timeframe": timeframe,
                    "fidelity": "coarse",
                    "fingerprint": None,
                    "run_ids": [run_id],
                }
                for inst, run_id in instrument_run_pairs
            ],
        }
    }


def _keltner_config(atr_mult: float = 2.0, regime: str = "mean_reversion") -> dict:
    """A candidate_strategy_config.json-shaped dict, minimal but realistic
    (same shape as runs/run_016/artifacts/candidate_strategy_config.json)."""
    return {
        "regime_detector": {"mode": "threshold_rules", "rules": [{"regime": regime}]},
        "strategies": {
            "regimes": {
                regime: {
                    "components": [
                        {
                            "id": "keltner",
                            "class": "strategies.strategy_components.KeltnerBreakoutComponent",
                            "params": {"atr_multiplier": atr_mult, "ema_period": 20},
                            "weight": 1.0,
                            "transforms": [],
                        },
                    ]
                }
            }
        },
    }


def _kc_digest_structured(
    instrument: str, timeframe: str, run_id: str, config: dict
) -> dict:
    """A fidelity=structured digest entry carrying the REAL composition
    fingerprint of `config` -- used to build a genuine REPEAT (identical
    fingerprint), as opposed to _kc_digest's coarse, collision-only shape."""
    fingerprint = bed.composition_fingerprint(config)
    return {
        "keltner_channel": {
            "confidence": "structural_indicator_id",
            "triples": [
                {
                    "instrument": instrument,
                    "timeframe": timeframe,
                    "fidelity": "structured",
                    "fingerprint": fingerprint,
                    "run_ids": [run_id],
                },
            ],
        }
    }


def _write_empty_kb(root: Path) -> None:
    _write_yaml(
        root / "campaign_record" / "campaign_knowledge_base.yaml", {"findings": []}
    )


def _full_run(
    root: Path,
    run_id: str,
    *,
    hypothesis_card: dict,
    expanded_variants: list,
    selected_variant_id: str,
    config_rationale=None,
    config: dict = None,
) -> Path:
    """Same fixture shape as test_variant_selection_record.py's _minimal_run,
    generalized to accept an arbitrary hypothesis_card dict (library_lookup /
    edge_source / thesis / target_market / timeframe) so tests can build
    realistic, classify_family()-resolvable candidates.

    config (E-036 S2): backtest_spec.yaml's own `config` field --
    _route_post_variant_selection reads this as the candidate's structured
    composition (see that function's own comment for why: it is the exact
    dict later copied verbatim to candidate_strategy_config.json). Defaults
    to the pre-E-036 trivial `{"regime_detector": {}}` shape so every
    existing test that does not care about composition is unaffected;
    tests that need a genuine REPEAT pass a real one (see
    _keltner_config())."""
    run_dir = root / "runs" / run_id
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    hid = hypothesis_card.get("hypothesis_id", "H-TEST")
    _write_yaml(
        artifacts / "expanded_hypothesis_card.yaml",
        {
            "base_hypothesis_id": hid,
            "expanded_variants": expanded_variants,
        },
    )
    _write_yaml(artifacts / "hypothesis_card.yaml", hypothesis_card)
    _write_yaml(
        artifacts / "backtest_spec.yaml",
        {
            "hypothesis_id": hid,
            "status": "spec_ready",
            "config": config if config is not None else {"regime_detector": {}},
            "config_rationale": config_rationale
            or [{"hypothesis_claim": "x", "config_choice": "y"}],
            "selected_variant_id": selected_variant_id,
        },
    )
    _write_yaml(
        artifacts / "decision.yaml",
        {
            "stage": "backtest_specification",
            "status": "spec_ready",
            "rationale": "test rationale",
            "blocking_issues": [],
        },
    )
    return run_dir


def _record_selection(root: Path, run_dir: Path) -> None:
    """Produce a REAL variant_selection.yaml via the actual S2 function,
    flipping the flag on for the duration of the call and back off after --
    tests that want variant_anti_adjacency_gate OFF (or a different
    variant_selection_record setting) set their own flags afterward."""
    _set_flags(root, variant_record=True)
    rpr._record_variant_selection(run_dir)


# ---------------------------------------------------------------------------
# _variant_anti_adjacency_gate_enabled -- same 4-case shape as the other
# five orchestrator.<name>.enabled flags.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "enabled,expected", [(True, True), (False, False), (None, False)]
)
def test_variant_anti_adjacency_gate_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_flags(root, variant_gate=enabled)
    assert rpr._variant_anti_adjacency_gate_enabled() is expected


def test_variant_anti_adjacency_gate_enabled_false_when_config_file_absent():
    assert rpr._variant_anti_adjacency_gate_enabled() is False


# ---------------------------------------------------------------------------
# Flag-off bit-identity: compare actual output, not just assert the flag is
# False -- same acceptance bar every prior story in this chain set for
# itself (S2a/b/c, E-034 S2).
# ---------------------------------------------------------------------------


def test_flag_off_returns_none_and_writes_nothing():
    root = rpr.ROOT
    card = {
        "hypothesis_id": "KELTNER_PIVOT_TEST",
        "target_market": "AVAXUSDT",
        "timeframe": "4h",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "thesis": "Keltner channel mean reversion.",
    }
    run_dir = _full_run(
        root,
        "run_950",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    _record_selection(root, run_dir)
    # Digest shaped to REFUSE if the gate were ever consulted -- proves
    # flag-off isn't merely "nothing to refuse", it's "the gate is never
    # even invoked".
    _write_digest(root, _kc_digest(("AVAXUSDT", "run_030")))
    _write_empty_kb(root)
    _set_flags(root, variant_gate=False, variant_record=True)

    state_path = run_dir / "pipeline_state.yaml"
    if not state_path.exists():
        _write_yaml(
            state_path,
            {"run_id": "run_950", "status": "active", "flags": {}, "audit_log": {}},
        )
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
    run_dir = _full_run(
        root,
        "run_951",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    _record_selection(root, run_dir)
    _set_flags(
        root, variant_gate=None, variant_record=True
    )  # variant_gate key absent entirely

    assert rpr._route_post_variant_selection(run_dir, "run_951") is None
    assert not (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").exists()


# ---------------------------------------------------------------------------
# Dependency: enabling this gate without its producer must fail loud, not
# silently no-op and not silently ADMIT.
# ---------------------------------------------------------------------------


def test_flag_on_without_variant_selection_record_flag_raises():
    root = rpr.ROOT
    card = {"hypothesis_id": "X", "target_market": "BTCUSDT", "timeframe": "1h"}
    run_dir = _full_run(
        root,
        "run_952",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
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
    run_dir = _full_run(
        root,
        "run_953",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    _set_flags(root, variant_gate=True, variant_record=True)

    with pytest.raises(RuntimeError, match="variant_selection.yaml"):
        rpr._route_post_variant_selection(run_dir, "run_953")


def test_flag_on_raises_when_digest_genuinely_absent():
    root = rpr.ROOT
    card = {"hypothesis_id": "X", "target_market": "BTCUSDT", "timeframe": "1h"}
    run_dir = _full_run(
        root,
        "run_954",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    _record_selection(root, run_dir)
    _write_empty_kb(root)
    # Deliberately do NOT call _write_digest.
    _set_flags(root, variant_gate=True, variant_record=True)

    with pytest.raises(RuntimeError, match="exclusion_digest.yaml"):
        rpr._route_post_variant_selection(run_dir, "run_954")


def test_flag_on_raises_when_kb_genuinely_absent():
    root = rpr.ROOT
    card = {"hypothesis_id": "X", "target_market": "BTCUSDT", "timeframe": "1h"}
    run_dir = _full_run(
        root,
        "run_955",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    _record_selection(root, run_dir)
    _write_digest(root, {})
    # Deliberately do NOT call _write_empty_kb.
    _set_flags(root, variant_gate=True, variant_record=True)

    with pytest.raises(RuntimeError, match="campaign_knowledge_base.yaml"):
        rpr._route_post_variant_selection(run_dir, "run_955")


# ---------------------------------------------------------------------------
# ADMIT case: a clean variant, not excluded, ADMITs and leaves next_stage
# untouched.
# ---------------------------------------------------------------------------


def test_admit_returns_none_and_writes_result_artifact():
    root = rpr.ROOT
    card = {
        "hypothesis_id": "FEAR_GREED_NOVEL_ANGLE",
        "target_market": "DOTUSDT",
        "timeframe": "1h",
        "thesis": "Fear & Greed index contrarian positioning on DOT, never tried.",
    }
    run_dir = _full_run(
        root,
        "run_956",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    _record_selection(root, run_dir)
    _write_digest(root, {})
    _write_empty_kb(root)
    _set_flags(root, variant_gate=True, variant_record=True)

    result = rpr._route_post_variant_selection(run_dir, "run_956")

    assert result is None
    written = yaml.safe_load(
        (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert written["route"] == "admit"


# ---------------------------------------------------------------------------
# THE key test: a candidate that pivoted instrument/timeframe away from a
# CLEAN parent card. The OLD call site (_route_post_innovation_expansion,
# reading only the parent hypothesis_card.yaml) ADMITs -- it never sees the
# variant. The NEW call site (_route_post_variant_selection, reading the
# variant's own resolved instrument/timeframe from variant_selection.yaml)
# REFUSEs the very same run. This is the direct, executable proof the
# 2026-08-24 defect is closed: the OLD gate is demonstrated blind to a
# collision the NEW gate catches.
# ---------------------------------------------------------------------------


def test_pivot_away_from_clean_parent_is_caught_only_by_the_new_call_site():
    """E-036 S2 update: the digest/config here now carry a GENUINE repeat
    (fidelity=structured, identical composition fingerprint on both sides)
    rather than a bare triple collision -- since E-036, a bare collision can
    only ever ADMIT as a NEIGHBOUR (see test_multi_symbol_parent_card_
    checks_every_instrument_not_just_one for that case), so keeping the
    REFUSE contrast this test exists to prove requires a fixture the new
    gate would ALSO recognize as a real repeat, not merely an adjacent
    triple. The thing under test -- the OLD call site structurally cannot
    see the pivot, the NEW one does -- is unchanged."""
    root = rpr.ROOT
    # Parent card: keltner_channel on BTCUSDT/1h -- CLEAN, nothing in the
    # digest matches this triple.
    clean_card = {
        "hypothesis_id": "KELTNER_PIVOT_PARENT",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": "BTCUSDT",
        "timeframe": "1h",
        "thesis": "Keltner channel mean reversion on BTC, 1h.",
    }
    # The variant that innovation_expansion/backtest_specification actually
    # picked pivots to AVAXUSDT/4h -- which DOES collide with the digest,
    # with the IDENTICAL composition (atr_mult=2.0) as run_030.
    pivoted_config = _keltner_config(atr_mult=2.0)
    pivoted_variant = {
        "variant_id": "V-PIVOT",
        "target_market": "AVAXUSDT",
        "timeframe": "4h",
    }
    run_id = "run_957"
    run_dir = _full_run(
        root,
        run_id,
        hypothesis_card=clean_card,
        expanded_variants=[pivoted_variant],
        selected_variant_id="V-PIVOT",
        config=pivoted_config,
    )
    _record_selection(root, run_dir)

    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["instrument"] == "AVAXUSDT"
    assert selection["timeframe"] == "4h"

    _write_digest(
        root, _kc_digest_structured("AVAXUSDT", "4h", "run_030", pivoted_config)
    )
    _write_empty_kb(root)

    # OLD call site: only ever sees the PARENT card -- clean -- ADMITs.
    old_state = {
        "run_id": run_id,
        "status": "active",
        "flags": {},
        "audit_log": {},
        "counters": {"refinements_used": 0},
    }
    _write_yaml(run_dir / "pipeline_state.yaml", old_state)
    _write_yaml(
        root / "config" / "campaign_config.yaml",
        {
            "orchestrator": {
                "variant_selection_record": {"enabled": True},
                "anti_adjacency_retry": {"enabled": True},
                "variant_anti_adjacency_gate": {"enabled": False},
            }
        },
    )

    old_route = rpr._route_post_innovation_expansion(
        run_dir,
        run_id,
        yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8")),
    )
    assert old_route == "validation", (
        "the OLD, pre-existing gate call site reads only the parent card and "
        "must ADMIT here -- it structurally cannot see the pivot"
    )

    # NEW call site: sees the CHOSEN VARIANT's resolved instrument/timeframe
    # (AVAXUSDT/4h) -- collides with the digest -- REFUSEs.
    _write_yaml(
        root / "config" / "campaign_config.yaml",
        {
            "orchestrator": {
                "variant_selection_record": {"enabled": True},
                "anti_adjacency_retry": {"enabled": True},
                "variant_anti_adjacency_gate": {"enabled": True},
            }
        },
    )

    new_route = rpr._route_post_variant_selection(run_dir, run_id)
    assert new_route == "human_pause", (
        "the NEW gate call site must REFUSE the same run the old one just "
        "ADMITted -- this is the direct proof the 2026-08-24 defect is closed"
    )
    result = yaml.safe_load(
        (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert result["route"] == "refuse"
    assert result["layer"] == "digest"
    assert result["outcome"] == "repeat", (
        "E-036 S2: REFUSE must only ever be reached via a genuine REPEAT "
        "(identical composition fingerprint), never a bare triple collision"
    )
    # Success signal (E-034/EPIC.md): the result artifact must reference the
    # CHOSEN VARIANT's own identifier, not just the base hypothesis id.
    assert result["selected_variant_id"] == "V-PIVOT"

    state = yaml.safe_load(
        (run_dir / "pipeline_state.yaml").read_text(encoding="utf-8")
    )
    assert state["status"] == "paused_for_human"
    assert state["flags"]["variant_anti_adjacency_gate_refused"] is True


# ---------------------------------------------------------------------------
# Calibration case (S1/S2a/S2c): the 4h funding retest ADMITs; a naive
# flat-list gate would REFUSE it -- still holds through THIS new call site,
# using a variant_selection.yaml-shaped candidate produced by the real
# _record_variant_selection(), not a hand-typed hypothesis_card.yaml.
# ---------------------------------------------------------------------------


def test_calibration_case_still_admits_through_the_new_call_site():
    root = rpr.ROOT
    kb_dest = root / "campaign_record" / "campaign_knowledge_base.yaml"
    kb_dest.parent.mkdir(parents=True, exist_ok=True)
    kb_dest.write_bytes(_REAL_KB_PATH.read_bytes())
    _write_digest(root, {})

    run_059_dest = root / "runs" / "run_059" / "artifacts"
    run_059_dest.mkdir(parents=True, exist_ok=True)
    for name in ("hypothesis_card.yaml", "pass_rule_evaluation.yaml"):
        src = _REAL_RUN_059_DIR / "artifacts" / name
        if src.exists():
            (run_059_dest / name).write_bytes(src.read_bytes())

    funding_4h_card = {
        "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED_4H_RETEST",
        "edge_source": {
            "evidence_type": "funding_open_interest",
            "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at 4h.",
        },
        "target_market": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "4h",
        "thesis": "Re-test the identical continuous funding-rate mean-reversion mechanism at 4h bars.",
    }
    run_id = "run_926"
    run_dir = _full_run(
        root,
        run_id,
        hypothesis_card=funding_4h_card,
        expanded_variants=[{"variant_id": "V-4H-RETEST"}],
        selected_variant_id="V-4H-RETEST",
    )
    _record_selection(root, run_dir)
    _set_flags(root, variant_gate=True, variant_record=True)

    result_route = rpr._route_post_variant_selection(run_dir, run_id)

    assert result_route is None, (
        "the calibration case must still ADMIT (route None = unchanged "
        "next_stage) when routed through the NEW E-034 S3 call site, not "
        "only at the gate's own unit-test level or through the OLD S2c "
        "call site"
    )
    result = yaml.safe_load(
        (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert result["route"] == "admit"
    assert result["layer"] == "kb"
    assert result["selected_variant_id"] == "V-4H-RETEST"


# ---------------------------------------------------------------------------
# REFUSE policy, tested end to end: immediate escalation (no retry), a
# DISTINCT flag from anti_adjacency_gate_exhausted, and classified correctly
# by the project's existing escalation mechanism.
# ---------------------------------------------------------------------------


def test_refuse_escalates_immediately_no_retry_state_written():
    """E-036 S2: REFUSE now requires a genuine repeat (identical composition
    fingerprint), not a bare triple collision -- see _kc_digest_structured.
    The policy under test (immediate escalation, distinct flag, no retry
    state) is unchanged; only the fixture needed to reach REFUSE changed."""
    root = rpr.ROOT
    card = {
        "hypothesis_id": "KELTNER_REFUSE_TEST",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": "SOLUSDT",
        "timeframe": "4h",
        "thesis": "Keltner channel on SOL, 4h.",
    }
    sol_config = _keltner_config(atr_mult=2.5)
    run_dir = _full_run(
        root,
        "run_958",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
        config=sol_config,
    )
    _record_selection(root, run_dir)
    _write_digest(root, _kc_digest_structured("SOLUSDT", "4h", "run_031", sol_config))
    _write_empty_kb(root)
    _write_yaml(
        run_dir / "pipeline_state.yaml",
        {"run_id": "run_958", "status": "active", "flags": {}, "audit_log": {}},
    )
    _set_flags(root, variant_gate=True, variant_record=True)

    route = rpr._route_post_variant_selection(run_dir, "run_958")

    assert route == "human_pause"
    state = yaml.safe_load(
        (run_dir / "pipeline_state.yaml").read_text(encoding="utf-8")
    )
    # No retry counter/attempt machinery -- unlike anti_adjacency_gate_retry,
    # this checkpoint has no bounded-retry state at all: it escalates on the
    # FIRST refusal.
    assert "anti_adjacency_gate_retry" not in state
    assert state["flags"]["variant_anti_adjacency_gate_refused"] is True
    assert state["flags"].get("anti_adjacency_gate_exhausted") is not True, (
        "must be a DISTINCT flag from the earlier checkpoint's exhaustion "
        "flag -- an operator must be able to tell 'refused early, cheap' "
        "apart from 'refused late, after two stages spend'"
    )


def test_refuse_classifies_via_existing_run_campaign_mechanism_and_is_not_quarantine_safe():
    """E-036 S2: same fixture upgrade as test_refuse_escalates_immediately_
    no_retry_state_written -- REFUSE now requires a genuine repeat."""
    root = rpr.ROOT
    card = {
        "hypothesis_id": "KELTNER_REFUSE_CLASSIFY_TEST",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": "ADAUSDT",
        "timeframe": "4h",
        "thesis": "Keltner channel on ADA, 4h.",
    }
    ada_config = _keltner_config(atr_mult=1.8)
    run_dir = _full_run(
        root,
        "run_959",
        hypothesis_card=card,
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
        config=ada_config,
    )
    _record_selection(root, run_dir)
    _write_digest(root, _kc_digest_structured("ADAUSDT", "4h", "run_032", ada_config))
    _write_empty_kb(root)
    _write_yaml(
        run_dir / "pipeline_state.yaml",
        {"run_id": "run_959", "status": "active", "flags": {}, "audit_log": {}},
    )
    _set_flags(root, variant_gate=True, variant_record=True)

    rpr._route_post_variant_selection(run_dir, "run_959")

    state = yaml.safe_load(
        (run_dir / "pipeline_state.yaml").read_text(encoding="utf-8")
    )
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
    assert (
        mapped["variant_anti_adjacency_gate_refused"]
        == "variant_anti_adjacency_gate_refused"
    )


# ---------------------------------------------------------------------------
# Post-merge review fix (2026-08-25, MEASURED not theoretical): hypothesis_
# card.yaml's target_market is a LIST for 10 of 46 sampled corpus cards
# (['BTCUSDT', 'ETHUSDT']) despite the schema declaring it a string. A list
# used to flow straight into evaluate_candidate()'s instrument= override,
# where it silently compared False against every digest triple.string --
# Layer-2 matching quietly never fired for real multi-symbol hypotheses, no
# error anywhere. Fixed: _coerce_scalar_instrument preserves a clean list of
# instrument strings as real data; _route_post_variant_selection evaluates
# EVERY named instrument and REFUSEs if any one of them collides.
# ---------------------------------------------------------------------------


def test_multi_symbol_parent_card_checks_every_instrument_not_just_one():
    """E-036 S2 update: _kc_digest is coarse (no fingerprint), so a
    collision on ETHUSDT alone can no longer REFUSE -- it can only ADMIT as
    a NEIGHBOUR (design point 3: a coarse match never produces REPEAT). The
    thing this test exists to prove -- that EVERY named instrument is
    actually checked, not just element 0 -- still holds and is now proven a
    different way: the ETHUSDT collision must still show up as a neighbour
    in the result artifact, not silently vanish because BTCUSDT (checked
    first) came back NOVEL. Before the three-way-outcome-aware selection
    fix in _route_post_variant_selection, `next((r for r in results if
    r.route == 'refuse'), results[0])` would have picked BTCUSDT's NOVEL
    result and discarded the ETHUSDT NEIGHBOUR entirely."""
    root = rpr.ROOT
    multi_symbol_card = {
        "hypothesis_id": "MULTI_SYM_PARENT",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "4h",
        "thesis": "Keltner channel mean reversion, BTC and ETH, 4h.",
    }
    run_id = "run_960"
    run_dir = _full_run(
        root,
        run_id,
        hypothesis_card=multi_symbol_card,
        expanded_variants=[{"variant_id": "V-BOTH"}],
        selected_variant_id="V-BOTH",
    )
    _record_selection(root, run_dir)

    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["instrument"] == ["BTCUSDT", "ETHUSDT"], (
        "a clean multi-symbol list must be preserved verbatim, not collapsed "
        "to a single element -- collapsing would silently stop checking "
        "whichever symbol got dropped"
    )

    # Only ETHUSDT collides in the digest (coarse -- no fingerprint).
    _write_digest(root, _kc_digest(("ETHUSDT", "run_030")))
    _write_empty_kb(root)
    _write_yaml(
        run_dir / "pipeline_state.yaml",
        {"run_id": run_id, "status": "active", "flags": {}, "audit_log": {}},
    )
    _set_flags(root, variant_gate=True, variant_record=True)

    route = rpr._route_post_variant_selection(run_dir, run_id)
    assert route is None, (
        "a coarse collision (no composition evidence on either side) must "
        "ADMIT as a NEIGHBOUR, not REFUSE -- this is the E-036 fix, not a "
        "regression of the 'check every instrument' guarantee"
    )
    result = yaml.safe_load(
        (run_dir / "artifacts" / "variant_anti_adjacency_result.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert result["route"] == "admit"
    assert result["outcome"] == "neighbour", (
        "the ETHUSDT collision must still be visible as a neighbour in the "
        "recorded result -- checking only element 0 (BTCUSDT, which is "
        "NOVEL) would have silently discarded it"
    )
    assert any("run_030" in n["run_ids"] for n in result["neighbours"])


def test_multi_symbol_parent_card_admits_when_no_instrument_collides():
    root = rpr.ROOT
    multi_symbol_card = {
        "hypothesis_id": "MULTI_SYM_CLEAN",
        "library_lookup": {"indicator_id": "keltner_channel"},
        "target_market": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "4h",
        "thesis": "Keltner channel mean reversion, BTC and ETH, 4h.",
    }
    run_id = "run_961"
    run_dir = _full_run(
        root,
        run_id,
        hypothesis_card=multi_symbol_card,
        expanded_variants=[{"variant_id": "V-BOTH"}],
        selected_variant_id="V-BOTH",
    )
    _record_selection(root, run_dir)

    _write_digest(root, _kc_digest(("ADAUSDT", "run_032")))  # collides with neither
    _write_empty_kb(root)
    _set_flags(root, variant_gate=True, variant_record=True)

    route = rpr._route_post_variant_selection(run_dir, run_id)
    assert route is None, "no collision on any named instrument -- must ADMIT"


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
    run_dir = _full_run(
        root,
        run_id,
        hypothesis_card=dict_card,
        expanded_variants=[{"variant_id": "V-ONE"}],
        selected_variant_id="V-ONE",
    )
    _record_selection(root, run_dir)

    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
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
    run_dir = _full_run(
        root,
        run_id,
        hypothesis_card=bad_card,
        expanded_variants=[{"variant_id": "V-ONE"}],
        selected_variant_id="V-ONE",
    )
    _set_flags(root, variant_record=True)
    with pytest.raises(RuntimeError, match="cannot resolve an instrument"):
        rpr._record_variant_selection(run_dir)
