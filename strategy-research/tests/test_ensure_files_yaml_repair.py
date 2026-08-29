"""
F4 (P1a shakedown, 2026-07-04) regression test.

ensure_files() previously did a bare yaml.safe_load() with no repair path, unlike
load_yaml() (used for handoffs/state), which retries via _repair_yaml(). This is what
crashed run_044's innovation_expansion stage: an unquoted colon inside a value
("library_category: structural_rate (composite: structural_rate + volatility via
filter)") — exactly the failure mode every skill file explicitly warns about, and the
one YAML-reading path with no safety net for it.

Fixture: run_044's ACTUAL broken expanded_hypothesis_card.yaml, frozen verbatim into
tests/fixtures/ (the live runs/run_044/artifacts/ copy was legitimately overwritten by
the subsequent successful relaunch — this fixture is deliberately independent of that
directory's current contents so the regression test doesn't silently go stale).
"""

import shutil
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

from run_phase1_research import ensure_files

_RUN_044_BROKEN_FIXTURE = Path(__file__).parent / "fixtures" / "run_044_broken_expanded_hypothesis_card.yaml"


@pytest.fixture
def broken_copy(tmp_path):
    dest = tmp_path / "expanded_hypothesis_card.yaml"
    shutil.copy(_RUN_044_BROKEN_FIXTURE, dest)
    return dest


def test_fixture_is_genuinely_broken_before_the_fix(broken_copy):
    """Sanity check: confirm the fixture actually reproduces the original crash mode
    (a bare yaml.safe_load must fail) — otherwise this test proves nothing."""
    content = broken_copy.read_text(encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(content)


def test_ensure_files_repairs_run_044s_actual_broken_output(broken_copy):
    """THE regression: this used to raise ValueError('YAML parse error...') and crash
    the whole pipeline run. Must now repair silently."""
    ensure_files([broken_copy])  # must not raise

    repaired_content = broken_copy.read_text(encoding="utf-8")
    parsed = yaml.safe_load(repaired_content)  # must now parse cleanly
    assert parsed is not None

    v2 = next(v for v in parsed["regime_specific_variants"] if v["variant_id"] == "V2")
    assert "structural_rate" in v2["library_category"]
    assert "volatility" in v2["library_category"]


def test_ensure_files_persists_the_repair_to_disk(broken_copy):
    """Unlike load_yaml() (in-memory only), ensure_files() must write the repaired
    content back — it validates freshly-produced deliverables nothing else has read yet."""
    original = broken_copy.read_text(encoding="utf-8")
    ensure_files([broken_copy])
    repaired = broken_copy.read_text(encoding="utf-8")
    assert repaired != original
    yaml.safe_load(repaired)  # re-confirm on the persisted content, not just the return value


def test_ensure_files_still_rejects_genuinely_unrepairable_yaml(tmp_path):
    """Must not silently swallow real structural errors — only the specific
    unquoted-colon-in-value class that _repair_yaml() targets."""
    bad = tmp_path / "unrepairable.yaml"
    bad.write_text("key: [unclosed list\n  - still broken\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unrepairable"):
        ensure_files([bad])
