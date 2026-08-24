"""
E-032 S2a, Task 1/3 -- tests for tools/build_exclusion_digest.py.

Covers:
  - classify_family()'s priority order and the false-positive it was built
    to avoid (run_048/run_058: Fear & Greed hypotheses whose free-text
    rationale mentions "funding" while discussing an unrelated structural
    cause -- naive full-text keyword search over rationale reproduces
    exactly this bug; classify_family() must not).
  - extract_instruments()/extract_timeframes() against the real shapes
    hypothesis_card.yaml has used across the campaign's history (list vs.
    comma-string vs. descriptive-prose target_market; short-token vs.
    sentence-embedded timeframe).
  - scan_run_triples() end-to-end against a synthetic runs/ tree.
  - Digest freshness (E-032 S2a Task 3's 4th requirement): a fact present in
    run artifacts but absent from campaign_state.yaml's stale flat lists
    appears in the digest.
  - A read-only regression check against the REAL repository's
    runs/ + campaign_record/campaign_knowledge_base.yaml: the funding family
    triples are exactly {1h, 1d}, never 4h -- the concrete claim S1's
    narrative rests on, re-derived fresh rather than merely cited.
"""
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import build_exclusion_digest as bed  # noqa: E402


# ---------------------------------------------------------------------------
# classify_family
# ---------------------------------------------------------------------------

def test_classify_family_prefers_library_lookup_indicator_id():
    card = {
        "hypothesis_id": "ANYTHING",
        "library_lookup": {"indicator_id": "keltner_channel_mean_reversion"},
        "edge_source": {"evidence_type": "fear_and_greed"},  # would say fear_greed if reached
    }
    family, confidence = bed.classify_family(card)
    assert family == "keltner_channel_mean_reversion"
    assert confidence == "structural_indicator_id"


def test_classify_family_falls_back_to_evidence_type_fear_and_greed():
    card = {"hypothesis_id": "H-041-C", "edge_source": {"evidence_type": "fear_and_greed"}}
    family, confidence = bed.classify_family(card)
    assert family == "fear_greed_index_contrarian"
    assert confidence == "structural_evidence_type"


def test_classify_family_keyword_bounded_uses_hypothesis_id():
    card = {"hypothesis_id": "V3-ESCALATE-4H-KELTNER"}
    family, confidence = bed.classify_family(card)
    assert family == "keltner_channel"
    assert confidence == "keyword_bounded"


def test_classify_family_unclassified_when_nothing_matches():
    card = {"hypothesis_id": "POSITION_SIZING_TIMEFRAME_COUPLING"}
    family, confidence = bed.classify_family(card)
    assert family == "unclassified:position_sizing_timeframe_coupling"
    assert confidence == "unclassified"


def test_classify_family_never_scans_rationale_the_run048_058_false_positive():
    """The concrete bug this restriction closes: run_048/run_058 are Fear &
    Greed hypotheses (edge_source.evidence_type=fear_and_greed) whose free
    text RATIONALE happens to mention 'funding' while explaining an
    unrelated structural cause of era-instability
    ('...funding rate availability, margin policy...'). A classifier that
    scans rationale would mislabel them as the funding family -- exactly
    what s1_measure_idea_generation.py's own free-text 'mentions funding'
    search did (confirmed independently while building this digest)."""
    card = {
        "hypothesis_id": "H-041-C-v2",
        "edge_source": {"evidence_type": "fear_and_greed"},
        "thesis": "Extreme Fear & Greed Index readings predict contrarian mean-reversion.",
        "rationale": (
            "The KB's era-breakdown reveals the sign flips in 2024-2025 -- this "
            "reflects structural market changes (funding rate availability, "
            "margin policy, leverage capacity)."
        ),
    }
    family, confidence = bed.classify_family(card)
    assert family == "fear_greed_index_contrarian", (
        "rationale's incidental 'funding rate' mention must never leak into family "
        f"classification; got {family!r}"
    )


def test_classify_family_keyword_bounded_reads_thesis_first_sentence_only():
    """Complement of the above: the keyword path DOES look at thesis's first
    sentence (this is where run_033's actual signal identity lives, since it
    predates library_lookup/edge_source), but must ignore everything after
    the first sentence boundary."""
    card = {
        "hypothesis_id": "RUN017_REPLICATION_DIAGNOSTIC",
        "thesis": (
            "KeltnerBreakout signal filtered to trending regimes reproduces "
            "positive edge on current market windows. "
            "This run also incidentally discusses funding rate settlement costs."
        ),
    }
    family, confidence = bed.classify_family(card)
    assert family == "keltner_channel"


# ---------------------------------------------------------------------------
# extract_instruments / extract_timeframes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("target_market,expected", [
    (["BTCUSDT", "ETHUSDT"], ["BTCUSDT", "ETHUSDT"]),
    ("BTCUSDT, ETHUSDT", ["BTCUSDT", "ETHUSDT"]),
    ("BTC/USDT and ETH/USDT (Binance 1h perpetuals)", ["BTCUSDT", "ETHUSDT"]),
    (None, []),
])
def test_extract_instruments_shapes(target_market, expected):
    card = {"target_market": target_market} if target_market is not None else {}
    assert bed.extract_instruments(card) == expected


@pytest.mark.parametrize("timeframe,expected", [
    ("1h", ["1h"]),
    ("1d", ["1d"]),
    ("1h (30-min bars for secondary signal)", ["1h", "30m"]),
    ("1h candles. Daily sentiment signal fires at UTC 00:00 bar; forecast holds "
     "across all 24 bars in that calendar day until next signal.", ["1h"]),
])
def test_extract_timeframes_shapes(timeframe, expected):
    assert bed.extract_timeframes({"timeframe": timeframe}) == expected


# ---------------------------------------------------------------------------
# scan_run_triples (synthetic tree)
# ---------------------------------------------------------------------------

def _write_card(runs_dir: Path, run_id: str, card: dict) -> None:
    artifacts = runs_dir / run_id / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    with open(artifacts / "hypothesis_card.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(card, f)


def test_scan_run_triples_groups_by_family_not_flat(tmp_path):
    runs_dir = tmp_path / "runs"
    _write_card(runs_dir, "run_100", {
        "hypothesis_id": "FUNDING_A", "target_market": ["BTCUSDT"], "timeframe": "1h",
        "library_lookup": {"indicator_id": "funding_rate_extreme"},
    })
    _write_card(runs_dir, "run_101", {
        "hypothesis_id": "KELTNER_A", "target_market": ["BTCUSDT"], "timeframe": "4h",
        "library_lookup": {"indicator_id": "keltner_channel_trend"},
    })

    result = bed.scan_run_triples(runs_dir)
    assert result["runs_scanned"] == 2
    assert result["skipped_runs"] == []
    families = result["families"]
    assert set(families.keys()) == {"funding_rate_extreme", "keltner_channel_trend"}

    funding_triples = families["funding_rate_extreme"]["triples"]
    assert funding_triples == [{"instrument": "BTCUSDT", "timeframe": "1h", "run_ids": ["run_100"]}]
    # The 4h entry belongs ONLY to keltner -- it must never appear under funding.
    assert all(t["timeframe"] != "4h" for t in funding_triples)


def test_scan_run_triples_skips_unparseable_card_without_crashing(tmp_path):
    runs_dir = tmp_path / "runs"
    artifacts = runs_dir / "run_200" / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "hypothesis_card.yaml").write_text("not: valid: yaml: [", encoding="utf-8")

    result = bed.scan_run_triples(runs_dir)
    assert result["runs_scanned"] == 0
    assert len(result["skipped_runs"]) == 1
    assert result["skipped_runs"][0]["run_id"] == "run_200"


def test_scan_run_triples_deterministic_across_repeated_calls(tmp_path):
    runs_dir = tmp_path / "runs"
    _write_card(runs_dir, "run_300", {
        "hypothesis_id": "FUNDING_B", "target_market": ["BTCUSDT", "ETHUSDT"], "timeframe": "1h",
        "library_lookup": {"indicator_id": "funding_rate_extreme"},
    })
    first = bed.scan_run_triples(runs_dir)
    second = bed.scan_run_triples(runs_dir)
    assert first == second


# ---------------------------------------------------------------------------
# _refresh_failed_families: re-keying onto the digest's family vocabulary
# ---------------------------------------------------------------------------

def test_refresh_failed_families_rekeys_onto_digest_canonical_name():
    """FIX 4 (review, 2026-08-24): the docstring promises re-keying onto
    digest_families's own vocabulary where a name matches (case/whitespace-
    normalized), but the body used to never reference digest_families at
    all -- the raw campaign_state string passed straight through. A
    differently-cased/spaced campaign_state entry that normalizes onto a
    real digest family key must come out carrying the DIGEST's canonical
    spelling, not the raw string."""
    campaign_state = {"failed_families": [
        {"name": "Keltner  Channel", "evidence_window": "2024-01:2024-06", "root_cause": "no edge"},
        "  RSI_Mean_Reversion ",
    ]}
    digest_families = {"keltner_channel": {}, "rsi_mean_reversion": {}}

    refreshed = bed._refresh_failed_families(campaign_state, digest_families)

    assert refreshed[0]["family"] == "keltner_channel", (
        f"expected the digest's canonical name, got {refreshed[0]['family']!r}"
    )
    assert refreshed[0]["detail"] == "dict_entry"
    assert refreshed[1]["family"] == "rsi_mean_reversion"
    assert refreshed[1]["detail"] == "bare_string_low_detail"


def test_refresh_failed_families_passes_through_unchanged_on_no_match():
    """Regression coverage for the existing best-effort-passthrough behavior:
    a campaign_state family name with no corresponding digest_families key
    must keep its raw string, exactly as before this fix."""
    campaign_state = {"failed_families": [
        {"name": "some_totally_unrelated_family", "evidence_window": None, "root_cause": None},
        "another_unmatched_bare_string",
    ]}
    digest_families = {"keltner_channel": {}}

    refreshed = bed._refresh_failed_families(campaign_state, digest_families)

    assert refreshed[0]["family"] == "some_totally_unrelated_family"
    assert refreshed[1]["family"] == "another_unmatched_bare_string"


# ---------------------------------------------------------------------------
# Freshness: a fact in run artifacts, absent from stale campaign_state lists
# ---------------------------------------------------------------------------

def test_digest_surfaces_a_fact_absent_from_stale_campaign_state(tmp_path):
    """E-032 S2a Task 3's 4th requirement. campaign_state.yaml's
    instruments_tried is seeded WITHOUT SOLUSDT; a run that actually used
    SOLUSDT must appear in the digest's family triples regardless -- the
    digest is derived fresh from runs/, never from the stale field."""
    runs_dir = tmp_path / "runs"
    _write_card(runs_dir, "run_400", {
        "hypothesis_id": "XS_MOM_SOL", "target_market": ["SOLUSDT"], "timeframe": "1h",
        "library_lookup": {"indicator_id": "volume_ratio_momentum"},
    })

    campaign_state_path = tmp_path / "campaign_state.yaml"
    with open(campaign_state_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({
            "instruments_tried": ["BTCUSDT", "ETHUSDT"],   # deliberately stale: no SOLUSDT
            "timeframes_tried": ["1h"],
            "failed_families": [],
        }, f)

    digest = bed.build_digest(runs_dir=runs_dir, campaign_state_path=campaign_state_path)
    triples = digest["families"]["volume_ratio_momentum"]["triples"]
    assert {"instrument": "SOLUSDT", "timeframe": "1h", "run_ids": ["run_400"]} in triples, (
        "SOLUSDT must be visible via the fresh scan even though it is absent "
        "from campaign_state.yaml's stale instruments_tried"
    )


# ---------------------------------------------------------------------------
# Real-repo regression: the funding family is {1h, 1d}, never 4h
# ---------------------------------------------------------------------------

def test_real_repo_funding_family_never_has_4h():
    """Re-derives, from the real committed runs/ tree, the concrete claim
    the epic's calibration case depends on: the funding_rate_extreme family
    has been run at 1h and 1d only. The '4h' entry in campaign_state.yaml's
    flat timeframes_tried list must come from elsewhere (keltner).

    No @real_repo_readonly marker needed: build_exclusion_digest.py's
    default paths are computed from Path(__file__), never from
    run_phase1_research.ROOT/run_campaign.ROOT -- the autouse sandbox
    fixture never touches them (see tests/conftest.py's own module
    docstring, same reasoning it documents for test_kb_reactivation_gate.py
    and friends)."""
    digest = bed.build_digest()
    funding = digest["families"].get("funding_rate_extreme")
    assert funding is not None, "expected the real repo to have funding_rate_extreme-classified runs"
    timeframes = {t["timeframe"] for t in funding["triples"]}
    assert timeframes == {"1h", "1d"}, f"funding family timeframes drifted: {timeframes}"

    keltner = digest["families"].get("keltner_channel")
    assert keltner is not None
    keltner_timeframes = {t["timeframe"] for t in keltner["triples"]}
    assert "4h" in keltner_timeframes, (
        "expected keltner_channel to be the source of the 4h entry"
    )

    # And the run_048/run_058 false-positive this digest was built to avoid:
    fear_greed = digest["families"].get("fear_greed_index_contrarian")
    assert fear_greed is not None
    fear_greed_run_ids = {rid for t in fear_greed["triples"] for rid in t["run_ids"]}
    assert "run_048" in fear_greed_run_ids and "run_058" in fear_greed_run_ids
    funding_run_ids = {rid for t in funding["triples"] for rid in t["run_ids"]}
    assert "run_048" not in funding_run_ids and "run_058" not in funding_run_ids, (
        "run_048/run_058 are Fear & Greed hypotheses and must never be counted "
        "as funding family evidence"
    )
