"""
The stage-deliverable block parser (run_phase1_research._DELIVERABLE_BLOCK_RE).

run_062 (C4, 2026-09-30): step 1a gave a legitimate "brief exhausted" answer
but labelled its block `# artifacts/brief_status.yaml` -- the path the prompt
itself uses (hypothesis-design/BRIEF_HYPOTHESES.md). The parser accepted bare
file names only, so the block was dropped and the run halted on a missing
hypothesis_card.yaml. The fix accepts exactly one optional prefix,
`artifacts/` (or `artifacts\\`); every other path still does not match, and
headers without the prefix parse exactly as before.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
from test_c5_7b1_model_id_stamp import DATED, _run_1a  # noqa: E402

# The pattern before this fix, kept here only to prove unchanged behaviour.
_OLD = r"```yaml\s*#\s*([a-zA-Z0-9_.]+\.yaml)\s*(.*?)```"

# The shape of run_062's real answer (abridged): prose, a prefixed brief_status
# block, and a block that tries to append outside the run directory.
RUN_062_SHAPE = (
    "# Analysis\n\nThe brief cannot be funded.\n\n"
    "```yaml\n# artifacts/brief_status.yaml\nbrief_status: exhausted\n"
    "reason: \"momentum IC too low for 1h costs\"\n```\n\n"
    "```yaml\n# append to ../../campaign_record/feed_wishlist.yaml\n"
    "- feed_name: liquidation_data\n  evidence_type: liquidation_data\n```\n"
)

UNPREFIXED_SAMPLES = [
    "```yaml\n# hypothesis_card.yaml\nhypothesis_id: H-1\n```\n",
    "text\n```yaml\n# backtest_spec.yaml\na: 1\n```\nmore\n```yaml\n# decision.yaml\nstatus: ok\n```\n",
    "```yaml\n#hypothesis_card_2.yaml\nx: [1, 2]\n```",
    "```yaml\n# extra_card_scores.yaml\ncards: []\n```\n```yaml\nno_header: true\n```\n",
    "no blocks at all",
]


@pytest.mark.parametrize("text", UNPREFIXED_SAMPLES)
def test_headers_without_prefix_parse_exactly_as_before(text):
    assert rpr._DELIVERABLE_BLOCK_RE.findall(text) == re.findall(_OLD, text, re.DOTALL)


@pytest.mark.parametrize("prefix", ["artifacts/", "artifacts\\"])
def test_artifacts_prefix_parses_to_the_bare_file_name(prefix):
    text = f"```yaml\n# {prefix}brief_status.yaml\nbrief_status: exhausted\n```\n"
    assert re.findall(_OLD, text, re.DOTALL) == []  # the bug: dropped before
    [(name, body)] = rpr._DELIVERABLE_BLOCK_RE.findall(text)
    assert name == "brief_status.yaml"
    assert body.strip() == "brief_status: exhausted"


@pytest.mark.parametrize("header", [
    "# ../../campaign_record/feed_wishlist.yaml",
    "# append to ../../campaign_record/feed_wishlist.yaml",
    "# other/brief_status.yaml",
    "# runs/run_1/artifacts/brief_status.yaml",
    "# /abs/brief_status.yaml",
    "# artifacts/../brief_status.yaml",
])
def test_any_other_path_still_does_not_match(header):
    text = f"```yaml\n{header}\nx: 1\n```\n"
    assert rpr._DELIVERABLE_BLOCK_RE.findall(text) == []


def test_run_062_shape_keeps_brief_status_and_ignores_the_outside_append():
    found = rpr._DELIVERABLE_BLOCK_RE.findall(RUN_062_SHAPE)
    assert [name for name, _ in found] == ["brief_status.yaml"]


def test_worker_saves_the_prefixed_block_inside_artifacts_only(monkeypatch, tmp_path):
    """Through the real run_claude_worker: the prefixed brief_status block is
    written to the run's artifacts/, and nothing is written anywhere else."""
    run_dir, entry = _run_1a(monkeypatch, tmp_path, RUN_062_SHAPE, [DATED])
    saved = rpr.load_yaml(run_dir / "artifacts" / "brief_status.yaml")
    assert saved["brief_status"] == "exhausted"
    assert not (run_dir / "artifacts" / "debug_validation_raw_output.txt").exists()
    # tests/conftest.py's autouse sandbox writes its own config copies under
    # tmp_path/_default_test_sandbox/ before the test runs; everything else
    # under tmp_path must be this run's own files.
    written = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*")
                     if p.is_file() and not p.relative_to(tmp_path).as_posix()
                     .startswith("_default_test_sandbox/config/"))
    assert written == ["runs/run_c57/artifacts/brief_status.yaml",
                       "runs/run_c57/pipeline_state.yaml"], written
    assert not any("feed_wishlist" in p for p in written)
    assert entry["num_turns"] == 1
