"""
E-061 C1.7 -- the first-run kit (delivery_plan_v26_continuation.md C1.7; review
finding A6). Docs + a template only, no engine code changed. This test proves
the ONE artifact that could silently rot -- config/templates/
research_brief_new_pipeline.yaml -- still registers cleanly through the REAL
`run_campaign.py` register path (register_hypothesis / _register_from_cli),
the same path RUNBOOK.md's new "Start a campaign on the new pipeline" section
tells an operator to use, against a hermetic sandbox that never touches the
real strategy-research/config/campaign_queue.yaml.

Fixture pattern (campaign_root) reused verbatim from
tests/test_halt_quarantine_policy.py, the same hermetic setup
tests/test_e059_s2b_briefs.py already reuses for register_hypothesis calls:
nothing here touches the real repository, and no LLM or subprocess is spawned.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_campaign as camp  # noqa: E402
import run_phase1_research as orch  # noqa: E402
import protocol_resolution as protres  # noqa: E402

from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401

_TEMPLATE_PATH = _SR / "config" / "templates" / "research_brief_new_pipeline.yaml"
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)

# The five protocols A3 §3.3 measured as NOT carrying the abolished generic
# promotion block (see the template's own comment for the full citation).
_SAFE_PROTOCOLS = (
    "diagnostic_btceth_4h", "funding_mr_4h_retest_v1", "funding_mr_daily_retest_v1",
    "h041c_v2_backext", "ts_trend_daily_v1",
)


def _frontmatter_block(text: str) -> str:
    m = _FRONTMATTER_RE.match(text)
    assert m, "template must start with a '---'-delimited YAML frontmatter block"
    return m.group(1)


def test_template_file_exists_and_is_well_formed():
    assert _TEMPLATE_PATH.exists(), _TEMPLATE_PATH
    text = _TEMPLATE_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(_frontmatter_block(text))
    assert data["brief_status"] == "open"
    assert data["criteria_from"] == orch.PASS_RULE_PENDING_AT_1A == "hypothesis_generation"
    mc = data["machine_constraints"]
    assert mc["protocol_ref"] == "protocols/diagnostic_btceth_4h.json"
    # placeholders are clearly marked and every required key is present (even
    # if unfilled) -- registration checks presence/truthiness, not content.
    for key in ("strategy_domain", "market_universe", "timeframe",
                "research_goal", "venue", "product"):
        assert data.get(key), f"placeholder field {key!r} must be present and non-empty"
    placeholder_fields = ("strategy_domain", "timeframe", "venue", "product", "research_goal")
    for key in placeholder_fields:
        assert "<FILL IN" in data[key], f"{key} must carry a clearly marked placeholder"
    assert "<FILL IN" in data["market_universe"][0]


def test_chosen_protocol_carries_no_unratified_generic_promotion():
    """The K3/D-3 gate this template exists to route around: the pinned
    protocol_ref must not be one of the 8/13 carrying the abolished generic
    promotion block with no ratified_by (A3 §3.3)."""
    for name in _SAFE_PROTOCOLS:
        protres.assert_promotion_ratified(_SR / "protocols" / f"{name}.json")  # must not raise


def test_protocol_ref_content_hash_matches_the_pinned_file():
    """1a-bis point 4: protocol_ref_content_hash is a STRUCTURAL hash, not a
    file digest, and must equal _compute_protocol_content_hash(path). A stale
    value here would halt an operator's very first launch."""
    data = yaml.safe_load(_frontmatter_block(_TEMPLATE_PATH.read_text(encoding="utf-8")))
    mc = data["machine_constraints"]
    ref_path = _SR / "protocols" / Path(mc["protocol_ref"]).name
    actual = orch._compute_protocol_content_hash(ref_path)
    assert actual == mc["protocol_ref_content_hash"]


def test_machine_constraints_passes_the_k3_protocol_selection_lint():
    data = yaml.safe_load(_frontmatter_block(_TEMPLATE_PATH.read_text(encoding="utf-8")))
    violations = orch._lint_machine_constraints_protocol_selection(
        data["machine_constraints"], data.get("pass_rule")
    )
    assert violations == []


def test_template_registers_through_the_real_register_path(campaign_root):
    """Copies the template's exact bytes into a briefs/*.md file inside the
    hermetic sandbox and registers it via run_campaign.register_hypothesis --
    the same function _register_from_cli (the `register` sub-command) and the
    RUNBOOK's new section both call. Never touches the real
    strategy-research/config/campaign_queue.yaml (campaign_root monkeypatches
    camp.ROOT/camp.QUEUE_PATH to a tmp_path)."""
    root = campaign_root["root"]
    briefs_dir = root / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / "my_first_new_pipeline_idea.md"
    brief_path.write_text(_TEMPLATE_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    rc = camp.register_hypothesis(brief_path, priority=1, notes="first new-pipeline brief")
    assert rc == 0

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entries = queue["queue"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["id"] == "my_first_new_pipeline_idea"
    assert entry["status"] == "ready"
    assert entry["brief_path"].replace("\\", "/") == "briefs/my_first_new_pipeline_idea.md"

    # Confirm _parse_brief_frontmatter (what registration and materialization
    # both actually read) round-trips the template's own fields, unmutated.
    parsed = camp._parse_brief_frontmatter(brief_path)
    assert parsed["criteria_from"] == "hypothesis_generation"
    assert parsed["machine_constraints"]["protocol_ref"] == "protocols/diagnostic_btceth_4h.json"


def test_register_from_cli_path_also_accepts_the_template(campaign_root):
    """_register_from_cli is the literal `register` sub-command RUNBOOK.md's
    new section tells an operator to invoke. Runs it under decide_next OFF
    (the default -- see A3 §1's flag table) to match a fresh clone's actual
    starting state."""
    briefs_dir = campaign_root["root"] / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / "my_first_new_pipeline_idea.md"
    brief_path.write_text(_TEMPLATE_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    assert orch._decide_next_enabled() is False  # sandbox has no campaign_config.yaml -> off
    rc = camp._register_from_cli(brief_path, 1, "n")
    assert rc == 0

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entry = queue["queue"][0]
    # decide_next off -> exactly the call made before E-059 S2b (no brief_status
    # override; register_hypothesis's own default is untouched by _register_from_cli).
    assert "brief_status" not in entry
