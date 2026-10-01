"""
The dry run's wishlist self-test (run_campaign._dry_run_wishlist_probe).

D-052 made the probe use the first feed_wishlist entry. A feed with no machine
predicate yet (liquidation_data on 2026-10-01) is correctly caught with the
pause reason `wishlist_trigger_data_gap`, but the probe accepted only
`wishlist_trigger` -- so `run_campaign.py --dry-run` failed on a correct
detection. Every outcome that proves detection is accepted now; a family that
is not detected still fails loud.
"""
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "workflow"))
import run_campaign as camp  # noqa: E402


def _sandbox(tmp_path, monkeypatch, feed_entries):
    (tmp_path / "campaign_record").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "campaign_record" / "feed_wishlist.yaml").write_text(
        yaml.safe_dump({"wishlist": feed_entries}), encoding="utf-8")
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    run_dir = tmp_path / "runs" / "run_dryrun_verify"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump(
        {"status": "active", "pending_stage": "hypothesis_generation", "flags": {}}),
        encoding="utf-8")
    return run_dir


def test_a_feed_without_a_predicate_is_a_detected_data_gap(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, [{"feed_name": "liquidation_data"}])
    line = camp._dry_run_wishlist_probe(run_dir)
    assert "wishlist_trigger_data_gap" in line and "OK" in line
    review = yaml.safe_load((run_dir / "artifacts" / "campaign_review.yaml").read_text())
    assert review["next_research_question"]["strategy_domain"] == "liquidation_data"


def test_a_predicate_that_evaluates_false_is_a_detected_trigger(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, [{"feed_name": "open_interest"}])
    monkeypatch.setattr(camp, "evaluate_wishlist_predicate",
                        lambda name: {"result": "false", "detail": "not yet"})
    assert "'wishlist_trigger'" in camp._dry_run_wishlist_probe(run_dir)


def test_a_predicate_that_fired_does_not_pause_and_passes(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, [{"feed_name": "open_interest"}])
    monkeypatch.setattr(camp, "evaluate_wishlist_predicate",
                        lambda name: {"result": "true", "detail": "fired"})
    assert "predicate fired" in camp._dry_run_wishlist_probe(run_dir)


def test_an_undetected_family_still_fails_loud(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, [{"feed_name": "open_interest"}])
    monkeypatch.setattr(camp, "_check_wishlist_trigger", lambda review: None)
    with pytest.raises(AssertionError, match="not detected"):
        camp._dry_run_wishlist_probe(run_dir)


def test_a_wrong_pause_reason_still_fails_loud(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, [{"feed_name": "open_interest"}])
    monkeypatch.setattr(camp, "_hard_pause_reason", lambda d, s: ("no_signal_artifact", ""))
    with pytest.raises(AssertionError, match="not detected"):
        camp._dry_run_wishlist_probe(run_dir)


def test_no_feed_wishlist_entry_skips_the_probe(tmp_path, monkeypatch):
    run_dir = _sandbox(tmp_path, monkeypatch, [])
    assert "skipped" in camp._dry_run_wishlist_probe(run_dir)


def test_a_fired_predicate_still_requires_the_family_to_be_detected(tmp_path, monkeypatch):
    """With a fired predicate there is no pause to inspect, so the explicit
    match check is the only proof of detection."""
    run_dir = _sandbox(tmp_path, monkeypatch, [{"feed_name": "open_interest"}])
    monkeypatch.setattr(camp, "evaluate_wishlist_predicate",
                        lambda name: {"result": "true", "detail": "fired"})
    monkeypatch.setattr(camp, "_check_wishlist_trigger", lambda review: None)
    with pytest.raises(AssertionError, match="not detected"):
        camp._dry_run_wishlist_probe(run_dir)
