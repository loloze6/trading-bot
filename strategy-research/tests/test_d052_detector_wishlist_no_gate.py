"""
D-052: the "no regime-gated hypotheses" rule (A2.3) is deleted. Its only code
hook was the campaign wishlist gate: a campaign_review reframe/escalation
naming a config/detector_wishlist.yaml family paused the campaign until that
family's trigger fired. Detector families no longer gate (the file stays as a
list of parked ideas); feed_wishlist.yaml entries still do. The withdrawn KB
verdict leaves the exhausted_mechanisms veto list.
"""
import sys
from pathlib import Path

import yaml

SR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_campaign as camp  # noqa: E402


def _root(tmp_path):
    (tmp_path / "config").mkdir()
    (tmp_path / "campaign_record").mkdir()
    (tmp_path / "config" / "detector_wishlist.yaml").write_text(yaml.safe_dump(
        {"candidates": [{"family": "daily_timeframe_er_overlay"}]}), encoding="utf-8")
    (tmp_path / "campaign_record" / "feed_wishlist.yaml").write_text(yaml.safe_dump(
        {"wishlist": [{"feed_name": "open_interest"}]}), encoding="utf-8")
    return tmp_path


def _review(text):
    return {"recommendation": "reframe", "recommendation_rationale": text,
            "next_research_question": {"strategy_domain": text}}


def test_a_detector_family_no_longer_gates(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", _root(tmp_path))
    assert camp._check_wishlist_trigger(_review("daily timeframe er overlay looks good")) is None
    assert camp._check_wishlist_trigger(_review("try daily_timeframe_er_overlay")) is None


def test_a_feed_wishlist_name_still_gates(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", _root(tmp_path))
    assert camp._check_wishlist_trigger(_review("an open interest signal")) == "open_interest"


def test_the_detector_wishlist_is_still_listed_as_ideas(monkeypatch, tmp_path):
    monkeypatch.setattr(camp, "ROOT", _root(tmp_path))
    assert camp._wishlist_family_names() == ["daily_timeframe_er_overlay", "open_interest"]
    assert camp._gating_wishlist_names() == ["open_interest"]


def test_the_withdrawn_kb_verdict_is_not_a_veto():
    kb = yaml.safe_load((SR / "campaign_record" / "campaign_knowledge_base.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in kb["findings"] if f["id"] == "er_detector_unusable_btc_eth_1h")
    assert entry["exhausted"] is False
    assert "WITHDRAWN" in entry["policy_consequence"] and "readjudication_20261001" in entry
    assert "er_detector_unusable_btc_eth_1h" not in [e["id"] for e in kb["exhausted_mechanisms"]]
