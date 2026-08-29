"""
F2 (P1a shakedown, 2026-07-04): drift guard between the component catalog and its
documentation, same philosophy as strategy-research/tests/test_campaign_config_sync.py
(config vs code constants) — here it's code vs doc.

Root cause this guards against: FundingRateMeanReversionComponent and
FearGreedContrarianComponent were added to strategy_components.py (Improvement 01) but
never added to DOC/STRATEGY_CONFIG_REFERENCE.md or docs/WORKFLOW_CAPABILITIES.md. Both
components already had working reference configs (run_041, run_042) — the docs were
just never updated. The backtest_specification skill instructs the LLM to declare
component_gap for anything "not in STRATEGY_CONFIG_REFERENCE.md" (correct, conservative
behavior given stale docs) — run_044 (2026-07-04) hit exactly this: a false
component_gap on an already-working component, purely because of the doc gap.

This test does not care WHERE in the doc a class is mentioned (catalog table vs a
prose note) — it only asserts the bare class name appears somewhere, which is enough
to stop an LLM reading top-to-bottom from concluding "not in STRATEGY_CONFIG_REFERENCE.md
== doesn't exist."
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
STRATEGY_COMPONENTS_PATH = PROJECT_ROOT / "strategies" / "strategy_components.py"
REFERENCE_DOC_PATH = PROJECT_ROOT / "DOC" / "STRATEGY_CONFIG_REFERENCE.md"

_CLASS_RE = re.compile(r"^class (\w+)\(SubStrategyComponent\):", re.MULTILINE)


def _all_component_classes() -> set:
    src = STRATEGY_COMPONENTS_PATH.read_text(encoding="utf-8")
    return set(_CLASS_RE.findall(src))


def test_every_component_class_is_documented_in_reference():
    classes = _all_component_classes()
    assert classes, (
        "no component classes found — regex or path is stale, fix the test first"
    )

    doc = REFERENCE_DOC_PATH.read_text(encoding="utf-8")
    missing = sorted(cls for cls in classes if cls not in doc)

    assert not missing, (
        f"Component class(es) exist in strategy_components.py but are not mentioned "
        f"anywhere in {REFERENCE_DOC_PATH.name}: {missing}. This produces false "
        f"component_gap verdicts in backtest_specification (see run_044, 2026-07-04) — "
        f"add each to the catalog (or a dedicated section) before landing new components."
    )


def test_known_previously_missing_components_are_now_present():
    """Named regression for the specific run_044 fixture — fails loudly and specifically
    if either of these two regress out of the doc again, independent of the generic
    scan above."""
    doc = REFERENCE_DOC_PATH.read_text(encoding="utf-8")
    for cls in ("FundingRateMeanReversionComponent", "FearGreedContrarianComponent"):
        assert cls in doc, (
            f"{cls} missing from {REFERENCE_DOC_PATH.name} (run_044 regression)"
        )
