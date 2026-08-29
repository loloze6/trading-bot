"""
F4c (2026-07-05): the token circuit breaker summed raw tokens, treating a
heavily-discounted cache_read token as equally expensive as a fresh output
token. run_047's real validation stage reported 836,461 cache_read tokens
(the claude_agent_sdk ResultMessage.usage field is CUMULATIVE FOR THE SESSION,
i.e. across every internal turn the model took — not a single-call snapshot)
against a real dollar cost of just $0.35, but tripped the old 300,000-raw-token
breaker at a run total of 1,018,898. Fixture: the actual audit_log entries from
run_047's pipeline_state.yaml (frozen — see this project's standing rule that
regression fixtures use the real historical failure, frozen so a later
successful re-run of the live directory can't invalidate the test).
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

# Frozen real audit_log from run_047 (2026-07-05), pre-F4c format (no `weighted`
# field yet — exercises the backward-compatible derivation path).
RUN_047_REAL_AUDIT_LOG = {
    "hypothesis_generation_attempt_0": {
        "cost_usd": 0.08771495,
        "tokens": {"input": 10, "output": 6257, "cache_read": 13337, "cache_creation": 26441, "total": 46045},
    },
    "innovation_expansion_attempt_0": {
        "cost_usd": 0.07643845,
        "tokens": {"input": 10, "output": 8680, "cache_read": 13337, "cache_creation": 16047, "total": 38074},
    },
    "validation_attempt_0": {
        "cost_usd": 0.3512201,
        "tokens": {"input": 164, "output": 37610, "cache_read": 836461, "cache_creation": 60544, "total": 934779},
    },
}


def test_weighted_token_units_known_values():
    # input=100, output=100, cache_read=100, cache_creation=100
    # -> 100*1.0 + 100*5.0 + 100*0.1 + 100*1.25 = 100+500+10+125 = 735
    assert rpr._weighted_token_units(100, 100, 100, 100) == pytest.approx(735.0)


def test_run_047_raw_total_matches_what_actually_tripped_the_old_breaker():
    """Sanity check the fixture itself: raw sum must reproduce the real
    1,018,898 total that tripped the old (pre-F4c) 300,000 raw-token breaker."""
    raw_total = sum(e["tokens"]["total"] for e in RUN_047_REAL_AUDIT_LOG.values())
    assert raw_total == 1018898


def test_weighted_total_is_materially_lower_than_raw_for_run_047():
    weighted_total, breakdown = rpr._compute_weighted_budget_usage(RUN_047_REAL_AUDIT_LOG)
    raw_total = sum(e["tokens"]["total"] for e in RUN_047_REAL_AUDIT_LOG.values())

    assert weighted_total < raw_total
    # The dominant validation-stage cache_read (836,461, heavily discounted)
    # should shrink the total by a large factor, not a marginal amount.
    assert raw_total / weighted_total > 1.5
    assert len(breakdown) == 3


def test_run_047_real_case_and_new_budget():
    """The actual real-world case that motivated F4c: confirm the new default
    budget (config/campaign_config.yaml orchestrator.token_budget_per_run_weighted_units)
    clears this run's real, legitimately-approved 3-stage weighted total, where
    the OLD raw-token budget (300,000) did not."""
    weighted_total, _ = rpr._compute_weighted_budget_usage(RUN_047_REAL_AUDIT_LOG)
    budget = rpr._load_token_budget()

    old_raw_budget = 300000
    raw_total = sum(e["tokens"]["total"] for e in RUN_047_REAL_AUDIT_LOG.values())
    assert raw_total > old_raw_budget, "the old breaker genuinely did trip on this real data"
    assert weighted_total < budget, "the new weighted breaker must clear this real, legitimate run"


def test_backward_compatible_with_post_f4c_entries_carrying_weighted_field():
    """A post-F4c audit_log entry already has a `weighted` field baked in —
    must be used directly, not recomputed (avoids double-applying weights)."""
    audit_log = {
        "some_stage_attempt_0": {
            "tokens": {
                "input": 10,
                "output": 10,
                "cache_read": 10,
                "cache_creation": 10,
                "total": 40,
                "weighted": 999.0,
            },
        },
    }
    weighted_total, breakdown = rpr._compute_weighted_budget_usage(audit_log)
    assert weighted_total == 999.0


def test_load_token_budget_reads_campaign_config():
    cfg_path = ROOT / "config" / "campaign_config.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    expected = cfg["orchestrator"]["token_budget_per_run_weighted_units"]
    assert rpr._load_token_budget() == expected
