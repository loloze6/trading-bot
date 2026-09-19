"""
F4d (2026-07-05): run_047 pre-registered "use the 2019-2025 backward-extension
range" and "MANDATORY A8.5.1a" in prose only. Nothing mechanically enforced it:
the (since-removed) signal_prescreen stage silently defaulted to
protocols/baseline_v1.json (the existing 2024-only protocol) and
backtest_specification's LLM stage silently dropped significance_methodology
despite an explicit skill-file instruction. The run completed end-to-end and
wrote a KB finding for H-041-A, but never actually tested the pre-registered
hypothesis.

RELOCATED 2026-09-12 (E-039 step 5): the conformance check now fires after
protocol_execution (_check_protocol_execution_conformance), not the removed
signal_prescreen stage's own _check_prescreen_conformance -- same logic,
"protocol_file" replaces "protocol_version" as the executed-identity field,
and the significance-methodology check now reads a per-symbol
episode_blocked_significance_by_symbol dict (CUL-265) instead of a single
flat significance_methodology_used string, since protocol_execution computes
it per symbol.

Fixture: run_047's REAL actual prescreen_result.yaml fields and the REAL
baseline_v1.json protocol it silently fell back to (frozen — per this project's
standing rule that regression tests use the actual historical failure as
fixture). Verifies the conformance gate would have caught this exact case.
"""
import copy
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

# Frozen real values from run_047 (2026-07-05).
RUN_047_MACHINE_CONSTRAINTS = {
    "significance_methodology": "episode_blocked_a851a",
    "protocol": {
        "symbols": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "1h",
        "per_symbol_start": {"BTCUSDT": "2019-09-10", "ETHUSDT": "2019-11-27"},
        "end": "2025-12-31",
    },
}

# The REAL protocol_result run_047 actually produced (protocol_file replaces
# the removed stage's "protocol_version"; episode_blocked_significance_by_symbol
# replaces the removed stage's flat "significance_methodology_used").
RUN_047_REAL_PROTOCOL_RESULT = {
    "protocol_file": "protocols\\baseline_v1.json",
    "episode_blocked_significance_by_symbol": {
        "BTCUSDT": "block_24_fisher_z", "ETHUSDT": "block_24_fisher_z",
    },
    "route": "kill_no_ic",
}

# The REAL baseline_v1.json protocol content it silently fell back to.
BASELINE_V1_PROTOCOL = {
    "symbols": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "1h",
    "windows": [
        {"label": "2024-01", "test": {"start": "2024-01-01", "end": "2024-02-01"}},
        {"label": "2024-11", "test": {"start": "2024-11-01", "end": "2024-12-01"}},
    ],
}


def test_generate_monthly_windows_covers_full_range_without_overshoot():
    windows = rpr._generate_monthly_windows("2019-09-10", "2025-12-31")
    assert windows[0]["test"]["start"] == "2019-09-01"
    assert windows[-1]["test"]["end"] == "2025-12-31"
    # Every window must be non-overlapping and monotonically increasing.
    for a, b in zip(windows, windows[1:]):
        assert a["test"]["end"] == b["test"]["start"]


def test_conformance_gate_catches_the_real_run_047_protocol_mismatch():
    violations = rpr._check_protocol_execution_conformance(
        RUN_047_REAL_PROTOCOL_RESULT, RUN_047_MACHINE_CONSTRAINTS, BASELINE_V1_PROTOCOL,
    )
    assert len(violations) >= 2  # both the range AND the methodology were wrong
    joined = " ".join(violations)
    assert "episode_blocked_significance_method" in joined
    assert "2024-01" in joined or "start" in joined  # protocol started too late


def test_conformance_gate_passes_when_everything_matches():
    conforming_result = {
        "protocol_file": "protocols/run_047_generated.json",
        "episode_blocked_significance_by_symbol": {
            "BTCUSDT": "episode_block_bootstrap", "ETHUSDT": "episode_block_bootstrap",
        },
        "route": "kill_no_ic",
    }
    conforming_protocol = {
        "symbols": ["BTCUSDT", "ETHUSDT"],
        "timeframe": "1h",
        "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31"),
    }
    violations = rpr._check_protocol_execution_conformance(
        conforming_result, RUN_047_MACHINE_CONSTRAINTS, conforming_protocol,
    )
    assert violations == []


@pytest.mark.parametrize("legitimate_outcome", [
    "episode_block_bootstrap", "episode_bootstrap_insufficient_n", "block_24_dense_fallback",
])
def test_conformance_gate_accepts_every_legitimate_a851a_outcome(legitimate_outcome):
    """Caught during test-writing, fixed before shipping: a literal-equality check
    against the family name "episode_blocked_a851a" would have wrongly flagged the
    legitimate density-fallback (A8.5.1a rule 4) and insufficient-episode (rule 3)
    outcomes as conformance violations, even though both are correct, spec'd
    behavior. The gate must accept ANY member of episode_significance.VALID_METHODS,
    for every symbol."""
    result = {"protocol_file": "protocols/run_test_generated.json",
              "episode_blocked_significance_by_symbol": {
                  "BTCUSDT": legitimate_outcome, "ETHUSDT": legitimate_outcome}}
    protocol = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31")}
    violations = rpr._check_protocol_execution_conformance(result, RUN_047_MACHINE_CONSTRAINTS, protocol)
    assert violations == []


def test_conformance_gate_flags_the_old_default_path_as_a_real_violation():
    """block_24_fisher_z (the removed prescreen stage's own default label) means
    the significance_methodology flag was absent/ignored entirely — this is
    exactly run_047's real failure and MUST be flagged, per-symbol."""
    result = {"protocol_file": "protocols/run_test_generated.json",
              "episode_blocked_significance_by_symbol": {
                  "BTCUSDT": "block_24_fisher_z", "ETHUSDT": "block_24_fisher_z"}}
    protocol = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31")}
    violations = rpr._check_protocol_execution_conformance(result, RUN_047_MACHINE_CONSTRAINTS, protocol)
    assert any("episode_blocked_significance_method" in v for v in violations)


def test_conformance_gate_flags_a_single_bad_symbol_even_if_the_other_conforms():
    """Per-symbol (CUL-265): one symbol conforming must not mask a violation on
    the other -- a violation on ANY symbol is a real conformance failure."""
    result = {"protocol_file": "protocols/run_test_generated.json",
              "episode_blocked_significance_by_symbol": {
                  "BTCUSDT": "episode_block_bootstrap", "ETHUSDT": "block_24_fisher_z"}}
    protocol = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31")}
    violations = rpr._check_protocol_execution_conformance(result, RUN_047_MACHINE_CONSTRAINTS, protocol)
    assert any("ETHUSDT" in v and "episode_blocked_significance_method" in v for v in violations)


def test_conformance_gate_missing_by_symbol_field_entirely_is_a_violation():
    """A run whose protocol_result carries no episode_blocked_significance_by_symbol
    at all (e.g. the field was never computed) must be flagged, not silently
    treated as conforming."""
    result = {"protocol_file": "protocols/run_test_generated.json"}
    protocol = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31")}
    violations = rpr._check_protocol_execution_conformance(result, RUN_047_MACHINE_CONSTRAINTS, protocol)
    assert any("episode_blocked_significance_by_symbol" in v for v in violations)


def test_path_basename_any_os_handles_both_separators_regardless_of_host():
    """E037-11/CUL-186 unit check: Path(...).name only recognizes the host OS's
    own separator, so this must not delegate to it."""
    assert rpr._path_basename_any_os("protocols\\baseline_v1.json") == "baseline_v1.json"
    assert rpr._path_basename_any_os("protocols/baseline_v1.json") == "baseline_v1.json"
    assert rpr._path_basename_any_os("baseline_v1.json") == "baseline_v1.json"
    assert rpr._path_basename_any_os("a/b\\c/baseline_v1.json") == "baseline_v1.json"


def test_conformance_gate_protocol_ref_matches_across_a_windows_written_path():
    """E037-11/CUL-186: protocol_result.protocol_file was recorded on Windows
    ("protocols\\baseline_v1.json", the exact shape run_060 recorded) and is now
    being checked against machine_constraints.protocol_ref on ANY host, including
    POSIX -- pathlib.Path(...).name would mis-parse the Windows path as one long
    name on POSIX and raise a spurious violation. This exercises the protocol_ref
    branch of _check_protocol_execution_conformance at all (it had zero coverage
    before this ticket)."""
    result = {"protocol_file": "protocols\\baseline_v1.json",
              "episode_blocked_significance_by_symbol": {
                  "BTCUSDT": "episode_block_bootstrap", "ETHUSDT": "episode_block_bootstrap"}}
    constraints = {**RUN_047_MACHINE_CONSTRAINTS, "protocol_ref": "protocols/baseline_v1.json"}
    protocol = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31")}
    violations = rpr._check_protocol_execution_conformance(result, constraints, protocol)
    assert not any("protocol_ref" in v for v in violations)


def test_conformance_gate_protocol_ref_still_catches_a_real_mismatch():
    """The fix must not make the check toothless: a genuinely different executed
    protocol is still flagged, cross-platform path spelling aside."""
    result = {"protocol_file": "protocols\\some_other_protocol.json",
              "episode_blocked_significance_by_symbol": {
                  "BTCUSDT": "episode_block_bootstrap", "ETHUSDT": "episode_block_bootstrap"}}
    constraints = {**RUN_047_MACHINE_CONSTRAINTS, "protocol_ref": "protocols/baseline_v1.json"}
    protocol = {"symbols": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
                "windows": rpr._generate_monthly_windows("2019-09-10", "2025-12-31")}
    violations = rpr._check_protocol_execution_conformance(result, constraints, protocol)
    assert any("protocol_ref" in v for v in violations)


def test_g7_run_047_real_constraints_are_now_refused_as_ungated(tmp_path, monkeypatch):
    """C7-EXT/G7 (2026-07-22). run_047's REAL machine_constraints carry no
    `promotion` block — it was materialized against the generic code default
    (median_sharpe_gt=0 / max_abs_drawdown_pct_lt=30 / min_trade_count_gte=20),
    which is the C7 symptom left live in the tree after C7 was recorded closed.
    Kept verbatim above as evidence that the landmine fired on a real run; the
    materializer must now refuse it rather than silently supply thresholds."""
    run_dir = tmp_path / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    monkeypatch.setattr(rpr, "ROOT", tmp_path)

    with pytest.raises(rpr.UngatedProtocolError):
        rpr._ensure_protocol_from_constraints(run_dir, "run_test", RUN_047_MACHINE_CONSTRAINTS)


def test_ensure_protocol_from_constraints_generates_and_is_idempotent(tmp_path, monkeypatch):
    run_dir = tmp_path / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    monkeypatch.setattr(rpr, "ROOT", tmp_path)

    # C7-EXT/G7: a pre-registered `promotion` block is now mandatory. run_047's
    # own constraints lack one (see the test above); this fixture adds an
    # explicit block so the test can go on exercising what it is actually
    # about — window generation, run_context wiring, and idempotency.
    constraints = copy.deepcopy(RUN_047_MACHINE_CONSTRAINTS)
    constraints["protocol"]["promotion"] = {
        "median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 30,
        "min_trade_count_gte": 20, "kill_median_sharpe_lt": -1,
    }

    path = rpr._ensure_protocol_from_constraints(run_dir, "run_test", constraints)
    assert path is not None
    assert path.exists()
    proto = yaml.safe_load(path.read_text(encoding="utf-8")) if path.suffix != ".json" else __import__("json").loads(path.read_text(encoding="utf-8"))
    assert proto["symbols"] == ["BTCUSDT", "ETHUSDT"]
    assert proto["windows"][0]["test"]["start"] == "2019-09-01"
    assert proto["windows"][-1]["test"]["end"] == "2025-12-31"

    run_ctx_path = run_dir / "artifacts" / "run_context.yaml"
    assert run_ctx_path.exists()
    run_ctx = yaml.safe_load(run_ctx_path.read_text(encoding="utf-8"))
    assert run_ctx["protocol"] == path.name
    # run_type MUST be forced_diagnostic — caught live in run_050: without this
    # key, protocol_execution's protocol-resolution silently falls back to
    # campaign_state.last_escalation.protocol_path (stale campaign-wide state from
    # a previous, unrelated run) instead of consulting run_context's `protocol` key.
    assert run_ctx["run_type"] == "forced_diagnostic"

    # Idempotency: mutate the file, re-call, confirm it is NOT clobbered.
    path.write_text("MUTATED", encoding="utf-8")
    rpr._ensure_protocol_from_constraints(run_dir, "run_test", constraints)
    assert path.read_text(encoding="utf-8") == "MUTATED"


def test_mark_trial_invalidated(tmp_path, monkeypatch):
    campaign_path = tmp_path / "campaign_state.yaml"
    campaign_path.write_text(yaml.safe_dump({
        "trial_sharpes": [{"trial_id": "run_test", "route": "kill_no_ic"}],
    }), encoding="utf-8")

    monkeypatch.setattr(rpr, "load_campaign_state", lambda: yaml.safe_load(campaign_path.read_text(encoding="utf-8")))
    monkeypatch.setattr(rpr, "_save_campaign_state", lambda state: campaign_path.write_text(
        yaml.safe_dump(state), encoding="utf-8"
    ))

    marked = rpr._mark_trial_invalidated("run_test", "conformance violation: wrong protocol range")
    assert marked is True

    updated = yaml.safe_load(campaign_path.read_text(encoding="utf-8"))
    trial = updated["trial_sharpes"][0]
    assert trial["invalidated_artifact"] is True
    assert "conformance violation" in trial["invalidation_reason"]
