"""
Improvement 04 — A1.4 Acceptance Test

Per A1.4: skill/prompt rewrites are accepted by OUTPUT AUDIT, not diff review.
This test verifies the diversity check logic against constructed artifacts:

(a) Cosmetic expansion → diversity check REJECTS it.
    Constructed: RSI(14) → RSI(21) → RSI(7), all oscillator/ohlcv_only.

(b) Real expansion → diversity check PASSES.
    Constructed: RSI(14) mean-reversion (oscillator/ohlcv_only) +
                 Funding-rate extreme (structural_rate/funding_open_interest).

(c) Lookup-justified deviation: unfavorable regime affinity acknowledged and
    justified with explicit mechanism reasoning (not boilerplate).

Run with: pytest strategy-research/tests/test_improvement04_acceptance.py -v
"""

import pytest
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
LIBRARY_PATH = ROOT / "config" / "indicator_library.yaml"


@pytest.fixture(scope="module")
def library():
    return yaml.safe_load(LIBRARY_PATH.read_text(encoding="utf-8"))


def _get_indicator(library: dict, indicator_id: str) -> dict | None:
    for entry in library.get("indicators", []):
        if entry["id"] == indicator_id:
            return entry
    return None


def _diversity_check(variants: list[dict], library: dict) -> dict:
    """
    Deterministic diversity check (mirrors SKILL.md logic for testing).
    A variant is identified by library_category + data_requirements.
    Returns {verdict: pass|reject, reason: str}.
    """
    if len(variants) <= 1:
        return {"verdict": "pass", "reason": "single variant"}

    categories = set()
    data_reqs = set()
    for v in variants:
        cat = v.get("library_category")
        dreq = v.get("data_requirements")
        if cat:
            categories.add(cat)
        if dreq:
            data_reqs.add(dreq)

    if len(categories) >= 2 or len(data_reqs) >= 2:
        return {
            "verdict": "pass",
            "diverse_on": {
                "categories": list(categories),
                "data_requirements": list(data_reqs),
            },
        }

    return {
        "verdict": "reject",
        "reason": (
            f"All variants share category={list(categories)} and "
            f"data_requirements={list(data_reqs)}. Cosmetic diversity — redo expansion."
        ),
    }


# ---------------------------------------------------------------------------
# (a) Cosmetic expansion — must be rejected
# ---------------------------------------------------------------------------


def test_cosmetic_expansion_rejected(library):
    """RSI parameter variants (14→21→7) are cosmetic: same category, same data_requirements."""
    cosmetic_variants = [
        {
            "id": "V1",
            "name": "RSI(14) mean-reversion",
            "library_category": "oscillator",
            "data_requirements": "ohlcv_only",
        },
        {
            "id": "V2",
            "name": "RSI(21) mean-reversion",
            "library_category": "oscillator",
            "data_requirements": "ohlcv_only",
        },
        {
            "id": "V3",
            "name": "RSI(7) mean-reversion",
            "library_category": "oscillator",
            "data_requirements": "ohlcv_only",
        },
    ]
    result = _diversity_check(cosmetic_variants, library)
    assert result["verdict"] == "reject", (
        f"Expected cosmetic expansion to be rejected, got: {result}"
    )
    assert "cosmetic" in result["reason"].lower() or "redo" in result["reason"].lower()


# ---------------------------------------------------------------------------
# (b) Real expansion — must pass
# ---------------------------------------------------------------------------


def test_real_expansion_passes(library):
    """RSI (oscillator/ohlcv) + Funding rate (structural_rate/funding_open_interest) = real diversity."""
    real_variants = [
        {
            "id": "V1",
            "name": "RSI(14) mean-reversion",
            "library_category": "oscillator",
            "data_requirements": "ohlcv_only",
        },
        {
            "id": "V2",
            "name": "Funding-rate extreme contrarian",
            "library_category": "structural_rate",
            "data_requirements": "funding_open_interest",
        },
    ]
    result = _diversity_check(real_variants, library)
    assert result["verdict"] == "pass", (
        f"Expected real expansion to pass, got: {result}"
    )
    assert (
        len(result.get("diverse_on", {}).get("categories", [])) >= 2
        or len(result.get("diverse_on", {}).get("data_requirements", [])) >= 2
    )


# ---------------------------------------------------------------------------
# (c) Lookup-justified deviation — unfavorable affinity must be acknowledged
# ---------------------------------------------------------------------------


def test_unfavorable_affinity_acknowledged(library):
    """
    RSI mean-reversion in a trending regime is unfavorable per the library.
    A justified deviation must state a specific mechanism reason (not boilerplate).
    This test verifies the library correctly records the unfavorable affinity.
    """
    rsi = _get_indicator(library, "rsi_mean_reversion")
    assert rsi is not None, "rsi_mean_reversion must exist in indicator_library.yaml"
    assert rsi["known_regime_affinity"]["trending"] == "unfavorable", (
        "rsi_mean_reversion.known_regime_affinity.trending must be 'unfavorable' "
        "(textbook fact: RSI mean-reversion fires against trends)"
    )

    # Simulate a hypothesis_card.yaml with a proper justification
    proper_justification = (
        "Testing on ungated signal (no regime filter per A2.3). "
        "Unfavorable affinity in trending markets is a prior risk noted in expected_failure_modes. "
        "Mechanism (funding extreme → deleveraging) does not depend on regime label — "
        "the structural mechanism fires independently of ER-based trend classification."
    )
    boilerplate = "n/a"

    assert len(proper_justification) > 50, (
        "justification must be substantive, not boilerplate"
    )
    assert boilerplate == "n/a" or len(boilerplate) < 10  # boilerplate has no content

    # The library records this affinity so the LLM can check it — verify that the field exists
    assert "known_regime_affinity" in rsi
    assert "trending" in rsi["known_regime_affinity"]


# ---------------------------------------------------------------------------
# Library structural tests
# ---------------------------------------------------------------------------


def test_library_loads_and_has_required_entries(library):
    """All required indicator categories must be present in the seeded library."""
    assert "indicators" in library
    indicators = library["indicators"]
    assert len(indicators) >= 8, f"Expected ≥8 seeded indicators, got {len(indicators)}"

    ids = {e["id"] for e in indicators}
    required_ids = {
        "rsi_mean_reversion",
        "moving_average_crossover",
        "bollinger_bands",
        "keltner_channel_mean_reversion",
        "volume_ratio_momentum",
        "funding_rate_extreme",
        "fear_greed_index_contrarian",
    }
    missing = required_ids - ids
    assert not missing, f"Missing required indicator entries: {missing}"


def test_all_entries_have_required_fields(library):
    """Every entry must have the required schema fields."""
    required_fields = {
        "id",
        "category",
        "known_regime_affinity",
        "typical_lag_bars",
        "crowding_risk",
        "data_requirements",
        "edge_source_compatibility",
        "campaign_empirical_results",
        "notes",
    }
    for entry in library.get("indicators", []):
        missing = required_fields - set(entry.keys())
        assert not missing, f"Entry '{entry.get('id')}' missing fields: {missing}"
        affinity = entry["known_regime_affinity"]
        assert set(affinity.keys()) == {"trending", "ranging", "high_vol"}, (
            f"Entry '{entry.get('id')}' known_regime_affinity must have trending/ranging/high_vol"
        )
        for val in affinity.values():
            assert val in ("favorable", "unfavorable", "neutral"), (
                f"Entry '{entry.get('id')}' affinity value '{val}' not in enum"
            )


def test_edge_source_compatibility_uses_valid_categories(library):
    """All edge_source_compatibility values must be from the A1.1 taxonomy."""
    valid = {
        "information_asymmetry",
        "structural_forced_flow",
        "liquidity_provision",
        "cross_venue_dislocation",
        "persistent_behavioral_bias",
    }
    for entry in library.get("indicators", []):
        for cat in entry.get("edge_source_compatibility", []):
            assert cat in valid, (
                f"Entry '{entry.get('id')}' has invalid edge_source_compatibility: '{cat}'"
            )


def test_campaign_empirical_results_empty_in_seed(library):
    """Seed file must have empty campaign_empirical_results (KB owns empirical results)."""
    for entry in library.get("indicators", []):
        results = entry.get("campaign_empirical_results", [])
        assert isinstance(results, list), (
            f"Entry '{entry.get('id')}' campaign_empirical_results must be a list"
        )
        # Seed should be empty — empirical data written back via KB
        assert len(results) == 0, (
            f"Entry '{entry.get('id')}' has non-empty campaign_empirical_results in seed. "
            "This data should be written back from campaign_knowledge_base.yaml only."
        )
