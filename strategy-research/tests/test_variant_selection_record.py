"""
E-034 S2 -- record which backtest_specification variant was chosen, and
persist the discards.

Sandboxing: relies on tests/conftest.py's autouse _sandbox_by_default fixture
for rpr.ROOT (already redirected to a per-test tmp_path sandbox before any
test body runs) -- same precedent test_exclusion_digest_input.py /
test_halt_quarantine_policy.py established for this exact
orchestrator.<name>.enabled flag shape.

Off-by-default acceptance bar (per the dispatching session's brief, "prove
flag-off is a genuine no-op ... compare actual pipeline state/output before
and after, not just assert the code path is skipped"): _record_variant_
selection() only ever WRITES new artifact files (variant_selection.yaml /
variants_not_pursued.yaml) -- it never mutates backtest_spec.yaml,
decision.yaml, or anything else a later stage reads. So the acceptance bar
here is a full artifacts-directory snapshot (file set + byte content) taken
before and after a flag-off call: must be identical, and the two new files
must not exist.

Regression fixture: run_019's REAL expanded_hypothesis_card.yaml
expanded_variants (three real threshold variants: V2-THRESHOLD-17p5/20p0/
22p5, frozen verbatim below from runs/run_019/artifacts/
expanded_hypothesis_card.yaml, 2026-08-xx), per this project's standing rule
that regression tests use real recorded evidence over synthetic-only
fixtures. run_019's real backtest_spec.yaml predates this feature and has no
selected_variant_id -- the fixture below adds ONLY that one field (set to the
real chosen value, confirmed by S1's spot check: decision.yaml's rationale
names "V2-THRESHOLD-20p0" as the config actually implemented), synthetically,
since no historical run carries it yet.
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _set_flag(root: Path, enabled) -> None:
    """enabled: True, False, or None (key/section absent entirely)."""
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    if enabled is None:
        (config_dir / "campaign_config.yaml").write_text(
            "orchestrator: {}\n", encoding="utf-8"
        )
        return
    with open(config_dir / "campaign_config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(
            {"orchestrator": {"variant_selection_record": {"enabled": bool(enabled)}}},
            f,
        )


def _write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def _minimal_run(
    root: Path,
    run_id: str,
    *,
    expanded_variants,
    selected_variant_id="present",
    base_hypothesis_id="H-TEST",
    hypothesis_id="H-TEST",
    target_market="BTCUSDT",
    timeframe="1h",
    omit_selected_variant_id=False,
) -> Path:
    run_dir = root / "runs" / run_id
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    _write_yaml(
        artifacts / "expanded_hypothesis_card.yaml",
        {
            "base_hypothesis_id": base_hypothesis_id,
            "expanded_variants": expanded_variants,
        },
    )
    _write_yaml(
        artifacts / "hypothesis_card.yaml",
        {
            "hypothesis_id": hypothesis_id,
            "target_market": target_market,
            "timeframe": timeframe,
        },
    )
    spec = {
        "hypothesis_id": hypothesis_id,
        "status": "spec_ready",
        "config": {"regime_detector": {}},
        "config_rationale": [{"hypothesis_claim": "x", "config_choice": "y"}],
    }
    if not omit_selected_variant_id:
        spec["selected_variant_id"] = selected_variant_id
    _write_yaml(artifacts / "backtest_spec.yaml", spec)
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


def _snapshot(run_dir: Path) -> dict:
    """file path (relative to run_dir) -> raw bytes, for every file under
    run_dir/artifacts. Used to prove flag-off writes nothing and mutates
    nothing."""
    artifacts = run_dir / "artifacts"
    return {
        str(p.relative_to(run_dir)): p.read_bytes()
        for p in sorted(artifacts.rglob("*"))
        if p.is_file()
    }


# ---------------------------------------------------------------------------
# _variant_selection_record_enabled
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "enabled,expected", [(True, True), (False, False), (None, False)]
)
def test_variant_selection_record_enabled_reads_flag(enabled, expected):
    root = rpr.ROOT
    _set_flag(root, enabled)
    assert rpr._variant_selection_record_enabled() is expected


def test_variant_selection_record_enabled_false_when_config_file_absent():
    # deliberately do not create config/campaign_config.yaml
    assert rpr._variant_selection_record_enabled() is False


# ---------------------------------------------------------------------------
# _derive_variant_id -- the derivation rule (S1 Task 3 / S2 Task 2)
# ---------------------------------------------------------------------------


def test_derive_variant_id_dict_with_variant_id_uses_it_verbatim():
    variant = {
        "variant_id": "V2-THRESHOLD-20p0",
        "label": "ignored",
        "id": "also-ignored",
    }
    assert rpr._derive_variant_id(variant, 0) == "V2-THRESHOLD-20p0"


def test_derive_variant_id_dict_without_variant_id_falls_through_priority_chain():
    # no variant_id, no id -> falls to name
    variant = {"name": "the-name", "label": "the-label"}
    assert rpr._derive_variant_id(variant, 3) == "the-name"

    # no variant_id, no id, no name -> falls to label
    variant2 = {"label": "the-label"}
    assert rpr._derive_variant_id(variant2, 3) == "the-label"

    # id present (no variant_id) -> id wins over name/label
    variant3 = {"id": "the-id", "name": "the-name", "label": "the-label"}
    assert rpr._derive_variant_id(variant3, 3) == "the-id"


def test_derive_variant_id_bare_string_gets_positional_hash_id():
    vid = rpr._derive_variant_id("just a bare string variant", 5)
    assert vid.startswith("str_5_")
    assert len(vid) == len("str_5_") + 8  # 8-char hex digest


def test_derive_variant_id_bare_string_is_stable_across_calls():
    vid1 = rpr._derive_variant_id("same text", 2)
    vid2 = rpr._derive_variant_id("same text", 2)
    assert vid1 == vid2


def test_derive_variant_id_bare_string_distinct_for_same_text_different_index():
    vid1 = rpr._derive_variant_id("same text", 0)
    vid2 = rpr._derive_variant_id("same text", 1)
    assert vid1 != vid2


def test_derive_variant_id_dict_with_no_id_like_key_falls_back_to_content_hash():
    variant = {"parameters": {"x": 1}}  # no variant_id/id/name/variant_name/label
    vid = rpr._derive_variant_id(variant, 7)
    assert vid.startswith("str_7_")


# ---------------------------------------------------------------------------
# _record_variant_selection -- flag off: genuine no-op
# ---------------------------------------------------------------------------


def test_flag_off_writes_nothing_and_mutates_nothing():
    root = rpr.ROOT
    _set_flag(root, False)
    run_dir = _minimal_run(
        root,
        "run_900",
        expanded_variants=[{"variant_id": "V1"}, {"variant_id": "V2"}],
        selected_variant_id="V1",
    )
    before = _snapshot(run_dir)
    rpr._record_variant_selection(run_dir)
    after = _snapshot(run_dir)
    assert after == before, "flag-off must not write or mutate any artifact file"
    assert not (run_dir / "artifacts" / "variant_selection.yaml").exists()
    assert not (run_dir / "artifacts" / "variants_not_pursued.yaml").exists()


def test_flag_off_is_a_noop_even_when_selected_variant_id_is_missing():
    """Flag off must short-circuit before even checking selected_variant_id --
    a run with a genuinely broken backtest_spec.yaml must not raise while the
    feature is off."""
    root = rpr.ROOT
    _set_flag(root, False)
    run_dir = _minimal_run(
        root,
        "run_901",
        expanded_variants=[{"variant_id": "V1"}],
        omit_selected_variant_id=True,
    )
    rpr._record_variant_selection(run_dir)  # must not raise
    assert not (run_dir / "artifacts" / "variant_selection.yaml").exists()


def test_flag_none_absent_is_also_a_noop():
    root = rpr.ROOT
    _set_flag(root, None)
    run_dir = _minimal_run(
        root,
        "run_902",
        expanded_variants=[{"variant_id": "V1"}],
        selected_variant_id="V1",
    )
    before = _snapshot(run_dir)
    rpr._record_variant_selection(run_dir)
    after = _snapshot(run_dir)
    assert after == before


# ---------------------------------------------------------------------------
# _record_variant_selection -- fail-loud paths (flag ON)
# ---------------------------------------------------------------------------


def test_missing_selected_variant_id_raises():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(
        root,
        "run_903",
        expanded_variants=[{"variant_id": "V1"}],
        omit_selected_variant_id=True,
    )
    with pytest.raises(RuntimeError, match="selected_variant_id"):
        rpr._record_variant_selection(run_dir)
    assert not (run_dir / "artifacts" / "variant_selection.yaml").exists()


def test_selected_variant_id_not_in_menu_raises():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(
        root,
        "run_904",
        expanded_variants=[{"variant_id": "V1"}, {"variant_id": "V2"}],
        selected_variant_id="V-DOES-NOT-EXIST",
    )
    with pytest.raises(RuntimeError, match="does not match any"):
        rpr._record_variant_selection(run_dir)
    assert not (run_dir / "artifacts" / "variant_selection.yaml").exists()


# ---------------------------------------------------------------------------
# _record_variant_selection -- correct recording (flag ON)
# ---------------------------------------------------------------------------


def test_dict_variant_with_variant_id_recorded_correctly():
    root = rpr.ROOT
    _set_flag(root, True)
    v1 = {"variant_id": "V1", "parameters": {"threshold": 1.0}}
    v2 = {"variant_id": "V2", "parameters": {"threshold": 2.0}}
    run_dir = _minimal_run(
        root,
        "run_905",
        expanded_variants=[v1, v2],
        selected_variant_id="V2",
        hypothesis_id="H-905",
        base_hypothesis_id="H-905",
    )
    rpr._record_variant_selection(run_dir)

    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["run_id"] == "run_905"
    assert selection["hypothesis_id"] == "H-905"
    assert selection["selected_variant_id"] == "V2"
    assert selection["variant_definition"] == v2
    assert selection["instrument"] == "BTCUSDT"
    assert selection["timeframe"] == "1h"
    assert selection["chosen_rationale"] == [
        {"hypothesis_claim": "x", "config_choice": "y"}
    ]

    not_pursued = yaml.safe_load(
        (run_dir / "artifacts" / "variants_not_pursued.yaml").read_text(
            encoding="utf-8"
        )
    )
    entries = not_pursued["variants_not_pursued"]
    assert len(entries) == 1
    assert entries[0]["variant_id"] == "V1"
    assert entries[0]["variant_definition"] == v1
    assert entries[0]["run_id"] == "run_905"
    assert entries[0]["hypothesis_id"] == "H-905"


def test_bare_string_variant_gets_derived_id_and_is_selectable():
    root = rpr.ROOT
    _set_flag(root, True)
    bare = "a bare string variant description"
    dict_variant = {"variant_id": "V-OTHER"}
    run_dir = _minimal_run(
        root,
        "run_906",
        expanded_variants=[bare, dict_variant],
    )
    derived_id = rpr._derive_variant_id(bare, 0)
    # overwrite backtest_spec.yaml's selected_variant_id to the derived id
    spec_path = run_dir / "artifacts" / "backtest_spec.yaml"
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    spec["selected_variant_id"] = derived_id
    _write_yaml(spec_path, spec)

    rpr._record_variant_selection(run_dir)

    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["selected_variant_id"] == derived_id
    assert selection["variant_definition"] == bare

    not_pursued = yaml.safe_load(
        (run_dir / "artifacts" / "variants_not_pursued.yaml").read_text(
            encoding="utf-8"
        )
    )
    entries = not_pursued["variants_not_pursued"]
    assert len(entries) == 1
    assert entries[0]["variant_definition"] == dict_variant


def test_dict_with_id_but_no_variant_id_falls_through_priority_chain_end_to_end():
    root = rpr.ROOT
    _set_flag(root, True)
    v_with_id = {"id": "ID-ONLY", "parameters": {"x": 1}}
    v_other = {"variant_id": "V-OTHER"}
    run_dir = _minimal_run(
        root,
        "run_907",
        expanded_variants=[v_with_id, v_other],
        selected_variant_id="ID-ONLY",
    )
    rpr._record_variant_selection(run_dir)
    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["variant_definition"] == v_with_id


def test_instrument_timeframe_fall_back_to_parent_card_when_variant_has_no_override():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(
        root,
        "run_908",
        expanded_variants=[
            {"variant_id": "V1"}
        ],  # no target_market/timeframe on the variant
        selected_variant_id="V1",
        target_market="ETHUSDT",
        timeframe="4h",
    )
    rpr._record_variant_selection(run_dir)
    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["instrument"] == "ETHUSDT"
    assert selection["timeframe"] == "4h"


def test_instrument_timeframe_variant_override_wins_over_parent_card():
    root = rpr.ROOT
    _set_flag(root, True)
    variant = {"variant_id": "V1", "target_market": "SOLUSDT", "timeframe": "15m"}
    run_dir = _minimal_run(
        root,
        "run_909",
        expanded_variants=[variant],
        selected_variant_id="V1",
        target_market="ETHUSDT",
        timeframe="4h",
    )
    rpr._record_variant_selection(run_dir)
    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["instrument"] == "SOLUSDT"
    assert selection["timeframe"] == "15m"


def test_variants_not_pursued_excludes_selected_none_dropped_none_duplicated():
    root = rpr.ROOT
    _set_flag(root, True)
    variants = [{"variant_id": f"V{i}"} for i in range(5)]
    run_dir = _minimal_run(
        root,
        "run_910",
        expanded_variants=variants,
        selected_variant_id="V2",
    )
    rpr._record_variant_selection(run_dir)
    not_pursued = yaml.safe_load(
        (run_dir / "artifacts" / "variants_not_pursued.yaml").read_text(
            encoding="utf-8"
        )
    )
    ids = [e["variant_id"] for e in not_pursued["variants_not_pursued"]]
    assert sorted(ids) == ["V0", "V1", "V3", "V4"]
    assert "V2" not in ids
    assert len(ids) == len(set(ids)) == 4


def test_lost_reason_carried_when_present_never_fabricated_when_absent():
    root = rpr.ROOT
    _set_flag(root, True)
    variants = [
        {"variant_id": "V1"},  # no lost_reason
        {"variant_id": "V2", "lost_reason": "dominated by V1 on expected trade count"},
        {"variant_id": "V3"},
    ]
    run_dir = _minimal_run(
        root,
        "run_911",
        expanded_variants=variants,
        selected_variant_id="V3",
    )
    rpr._record_variant_selection(run_dir)
    not_pursued = yaml.safe_load(
        (run_dir / "artifacts" / "variants_not_pursued.yaml").read_text(
            encoding="utf-8"
        )
    )
    by_id = {e["variant_id"]: e for e in not_pursued["variants_not_pursued"]}
    assert "lost_reason" not in by_id["V1"]
    assert by_id["V2"]["lost_reason"] == "dominated by V1 on expected trade count"


# ---------------------------------------------------------------------------
# Regression fixture: run_019's REAL expanded_variants (3 real threshold
# variants), frozen verbatim from runs/run_019/artifacts/
# expanded_hypothesis_card.yaml. Only the (synthetic, this feature predates
# the field) selected_variant_id is added to backtest_spec.yaml.
# ---------------------------------------------------------------------------

RUN_019_EXPANDED_VARIANTS = [
    {
        "variant_id": "V2-THRESHOLD-17p5",
        "label": "Conservative threshold",
        "description": "min_abs=17.5 (16% stricter than baseline 15.0; tests necessity of full 20.0 jump)",
        "parameters": {
            "rsi_period": 14,
            "min_abs_threshold": 17.5,
            "regime_filter": "TRENDING (ER >= 0.50 AND VR >= 1.20)",
            "overbought_level": 70,
            "oversold_level": 30,
        },
        "rationale": "Incremental threshold increase; expect 20-25% trade reduction vs baseline, cost_drag ~200-210%.",
        "expected_outcome": "Trade count ~60-70% of V2-CONSERVATIVE; sharpe negative or marginal; cost_drag > 150%. If positive, indicates 20.0 is too aggressive.",
    },
    {
        "variant_id": "V2-THRESHOLD-20p0",
        "label": "Target threshold (as specified in brief)",
        "description": "min_abs=20.0 (33% stricter than baseline 15.0; primary hypothesis from refinement diagnosis)",
        "parameters": {
            "rsi_period": 14,
            "min_abs_threshold": 20.0,
            "regime_filter": "TRENDING (ER >= 0.50 AND VR >= 1.20)",
            "overbought_level": 70,
            "oversold_level": 30,
        },
        "rationale": "Targets 40-50% trade reduction; cost_drag <150% while preserving gross_pnl signal (21.62 median). Net PnL becomes positive post-fees.",
        "expected_outcome": "Trade count ~40-50% of V2-CONSERVATIVE; cost_drag 130-180%; sharpe >= 0.10 if trade count >= 20/window.",
    },
    {
        "variant_id": "V2-THRESHOLD-22p5",
        "label": "Aggressive threshold",
        "description": "min_abs=22.5 (50% stricter than baseline 15.0; tests if even stricter improves net PnL)",
        "parameters": {
            "rsi_period": 14,
            "min_abs_threshold": 22.5,
            "regime_filter": "TRENDING (ER >= 0.50 AND VR >= 1.20)",
            "overbought_level": 70,
            "oversold_level": 30,
        },
        "rationale": "Maximum threshold to test hypothesis that fewer, higher-conviction trades improve net PnL further. Risk: trade count drops below significance (< 20/window).",
        "expected_outcome": "Trade count ~30-35% of V2-CONSERVATIVE; lowest fee drag but potential for Sharpe invalidity. Contingency: fallback to 18.0 or 20.0 if insignificant.",
    },
]


def test_run_019_real_corpus_regression_fixture():
    root = rpr.ROOT
    _set_flag(root, True)
    run_dir = _minimal_run(
        root,
        "run_019",
        expanded_variants=RUN_019_EXPANDED_VARIANTS,
        selected_variant_id="V2-THRESHOLD-20p0",  # per S1's spot check: decision.yaml's
        # rationale names this as the config actually implemented.
        hypothesis_id="V2-PIVOT-A-THRESHOLD",
        base_hypothesis_id="V2-PIVOT-A-THRESHOLD",
        target_market="BTCUSDT",
        timeframe="1h",
    )
    rpr._record_variant_selection(run_dir)

    selection = yaml.safe_load(
        (run_dir / "artifacts" / "variant_selection.yaml").read_text(encoding="utf-8")
    )
    assert selection["selected_variant_id"] == "V2-THRESHOLD-20p0"
    assert selection["variant_definition"] == RUN_019_EXPANDED_VARIANTS[1]
    assert selection["instrument"] == "BTCUSDT"
    assert selection["timeframe"] == "1h"

    not_pursued = yaml.safe_load(
        (run_dir / "artifacts" / "variants_not_pursued.yaml").read_text(
            encoding="utf-8"
        )
    )
    ids = {e["variant_id"] for e in not_pursued["variants_not_pursued"]}
    assert ids == {"V2-THRESHOLD-17p5", "V2-THRESHOLD-22p5"}
    assert len(not_pursued["variants_not_pursued"]) == 2
