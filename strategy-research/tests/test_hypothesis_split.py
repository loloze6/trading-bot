"""
Architecture rule (2026-07-06, run_054 postmortem): ONE hypothesis per run.

run_054 was scaffolded from run_053's (invalid — see test_kb_reactivation_gate.py)
campaign_review reframe, whose research_goal asked to "Test both mechanisms
ungated on extended data" (H-041-A funding-rate AND H-041-C fear/greed).
hypothesis_generation reasonably wrote TWO deliverables,
hypothesis_card_H041A_extended.yaml and hypothesis_card_H041C_extended.yaml,
instead of the single hypothesis_card.yaml every downstream stage (and
ensure_files' own contract) expects — crashing run_loop with a bare
FileNotFoundError ("Missing files: [...hypothesis_card.yaml]").

NOTE ON THE FIXTURE: run_054's actual two files were deleted (per the operator's
explicit instruction, after the KB-reactivation root cause was fixed) before their
exact byte content was frozen for a test — this project's standing rule of using
the real historical artifact as fixture could not be followed here. The two card
fixtures below are reconstructed to be representative of the real shape (same
mechanism split, same general content pattern as every other hypothesis_card in
this campaign) rather than byte-identical to the deleted originals. What IS
exercised exactly as it happened: ensure_files() raising FileNotFoundError for a
missing hypothesis_card.yaml while multiple hypothesis_card_*.yaml siblings exist.

Fix: _handle_hypothesis_generation_multi_card_split (run_phase1_research.py) —
the first card becomes this run's hypothesis_card.yaml (unchanged downstream
behavior); every additional card gets its own freshly-scaffolded sibling run,
already past hypothesis_generation, recorded in campaign_state.yaml's
hypothesis_splits. workflow/run_campaign.py reads that list to give each sibling
its own queue entry rather than treating it as the same brief's lineage.
"""

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

# Representative reconstruction of run_054's real two-card output (see module
# docstring — the originals were deleted before being frozen as a fixture).
CARD_H041A = """\
hypothesis_id: H-041-A-extended
edge_source:
  evidence_type: funding_open_interest
  category: structural_forced_flow
signal_concept: Funding-rate extreme -> contrarian mean-reversion, backward-extended window
power_parameters:
  activation_rate: 0.125
  plausible_ic_upper: 0.20
  n_bars: 61320
  n_symbols: 2
  is_market_wide: false
"""

CARD_H041C = """\
hypothesis_id: H-041-C-extended
edge_source:
  evidence_type: fear_and_greed
  category: persistent_behavioral_bias
signal_concept: Fear/greed extreme -> contrarian mean-reversion, backward-extended window
power_parameters:
  activation_rate: 0.218
  plausible_ic_upper: 0.15
  n_bars: 61320
  n_symbols: 2
  is_market_wide: true
"""


def _fake_scaffold_next_run(next_run_id: str):
    """Stand-in for _scaffold_next_run: the real one shells out to setup_run.py as a
    SEPARATE process, whose own ROOT = Path(__file__).parent.parent would resolve
    against the real project directory regardless of any monkeypatch in this test
    process — it must not run for real here. Mirrors setup_run.py's actual output
    shape closely enough for the split logic to operate on."""
    run_dir = rpr.ROOT / "runs" / next_run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "handoffs").mkdir(parents=True)
    rpr.save_yaml(
        run_dir / "pipeline_state.yaml",
        {
            "run_id": next_run_id,
            "status": "active",
            "current_stage": None,
            "pending_stage": "hypothesis_generation",
            "completed_stages": [],
            "artifacts": {},
            "counters": {"refinements_used": 0, "reruns_used": 0},
            "flags": {},
            "audit_log": {},
        },
    )


@pytest.fixture
def campaign_dir(tmp_path, monkeypatch):
    (tmp_path / "runs").mkdir()
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    monkeypatch.setattr(rpr, "_scaffold_next_run", _fake_scaffold_next_run)
    return tmp_path


def _make_parent_run_with_two_cards(tmp_path: Path, run_id: str = "run_054") -> Path:
    run_dir = tmp_path / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "research_brief.yaml").write_text(
        "strategy_domain: structural_and_behavioral_signals\n", encoding="utf-8"
    )
    (run_dir / "artifacts" / "hypothesis_card_H041A_extended.yaml").write_text(
        CARD_H041A, encoding="utf-8"
    )
    (run_dir / "artifacts" / "hypothesis_card_H041C_extended.yaml").write_text(
        CARD_H041C, encoding="utf-8"
    )
    return run_dir


def test_real_run_054_style_missing_file_error_is_reproduced_by_ensure_files(
    campaign_dir,
):
    """Establishes the actual failure this fix addresses: ensure_files() raises
    FileNotFoundError, exactly as it did live for run_054, when hypothesis_card.yaml
    is absent but sibling cards exist."""
    run_dir = _make_parent_run_with_two_cards(campaign_dir)
    with pytest.raises(FileNotFoundError, match="hypothesis_card.yaml"):
        rpr.ensure_files([run_dir / "artifacts" / "hypothesis_card.yaml"])


def test_split_gives_parent_the_first_card_and_scaffolds_one_sibling_per_extra_card(
    campaign_dir,
):
    run_dir = _make_parent_run_with_two_cards(campaign_dir)

    handled = rpr._handle_hypothesis_generation_multi_card_split("run_054", run_dir)
    assert handled is True

    # Parent keeps the alphabetically-first card as its own hypothesis_card.yaml —
    # downstream stages (ensure_files, innovation_expansion, ...) see no difference
    # from a normal single-hypothesis run.
    parent_card = yaml.safe_load(
        (run_dir / "artifacts" / "hypothesis_card.yaml").read_text(encoding="utf-8")
    )
    assert parent_card["hypothesis_id"] == "H-041-A-extended"

    # Exactly one sibling scaffolded for the one extra card.
    campaign = yaml.safe_load(
        (campaign_dir / "campaign_state.yaml").read_text(encoding="utf-8")
    )
    splits = campaign["hypothesis_splits"]
    assert len(splits) == 1
    assert splits[0]["parent_run"] == "run_054"
    children = splits[0]["children"]
    assert len(children) == 1

    child_dir = campaign_dir / "runs" / children[0]
    assert child_dir.exists()
    child_card = yaml.safe_load(
        (child_dir / "artifacts" / "hypothesis_card.yaml").read_text(encoding="utf-8")
    )
    assert child_card["hypothesis_id"] == "H-041-C-extended"

    # Sibling carries the SAME research_brief (same underlying reframe) and is
    # already past hypothesis_generation — must not be regenerated.
    child_brief = (child_dir / "artifacts" / "research_brief.yaml").read_text(
        encoding="utf-8"
    )
    assert "structural_and_behavioral_signals" in child_brief
    child_state = yaml.safe_load(
        (child_dir / "pipeline_state.yaml").read_text(encoding="utf-8")
    )
    assert child_state["pending_stage"] == "innovation_expansion"
    assert child_state["completed_stages"] == ["hypothesis_generation"]


def test_single_card_is_not_treated_as_a_split(campaign_dir):
    """Sanity: a genuinely single-hypothesis run (the overwhelming common case) must
    not be affected — split handling only fires with 2+ sibling cards present."""
    run_dir = campaign_dir / "runs" / "run_100"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "hypothesis_card_SOMETHING.yaml").write_text(
        CARD_H041A, encoding="utf-8"
    )

    handled = rpr._handle_hypothesis_generation_multi_card_split("run_100", run_dir)
    assert handled is False  # caller must re-raise the original FileNotFoundError


def test_genuinely_missing_file_with_no_cards_at_all_is_not_a_split(campaign_dir):
    run_dir = campaign_dir / "runs" / "run_101"
    (run_dir / "artifacts").mkdir(parents=True)

    handled = rpr._handle_hypothesis_generation_multi_card_split("run_101", run_dir)
    assert handled is False


def test_already_present_hypothesis_card_short_circuits(campaign_dir):
    """If hypothesis_card.yaml actually exists, ensure_files() would not have raised
    for IT — the missing file must have been something else entirely, so this is
    never a split situation regardless of what else sits in artifacts/."""
    run_dir = _make_parent_run_with_two_cards(campaign_dir)
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        CARD_H041A, encoding="utf-8"
    )

    handled = rpr._handle_hypothesis_generation_multi_card_split("run_054", run_dir)
    assert handled is False
