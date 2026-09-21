"""
E-056 S2 Slice 3a: sync guard for strategy-research/docs/STRATEGY_DESIGN_GUIDE.md's
§4 component catalog against the real component classes in
trading-bot/strategies/strategy_components.py.

This is a REAL sync check (re-derives both sides mechanically at test time),
not a hardcoded count -- the same class of drift that could have silently hit
trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md (nothing enforced its catalog stayed
in sync with the code) must not recur for the new design guide.

Two things are checked:
1. The class-name SET in the guide's §4 catalog tables equals the class-name
   SET found by grepping `^class.*SubStrategyComponent` in
   strategy_components.py -- add/remove/rename a component on either side and
   this test fails, naming exactly what's out of sync.
2. The catalog's own count matches `len()` of that grepped set (redundant
   with #1 for a well-formed table, but catches an accidentally-duplicated
   row that #1's set-equality would silently absorb).
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
DESIGN_GUIDE_PATH = REPO_ROOT / "strategy-research" / "docs" / "STRATEGY_DESIGN_GUIDE.md"
STRATEGY_COMPONENTS_PATH = REPO_ROOT / "trading-bot" / "strategies" / "strategy_components.py"

_CLASS_DEF_RE = re.compile(r"^class\s+(\w+)\(SubStrategyComponent\):", re.MULTILINE)
# Catalog table rows look like: | `EfficiencyRatioRegimeComponent` | period(24)... |
_CATALOG_ROW_RE = re.compile(r"^\|\s*`(\w+)`\s*\|", re.MULTILINE)


def _real_component_classes() -> set:
    src = STRATEGY_COMPONENTS_PATH.read_text(encoding="utf-8")
    return set(_CLASS_DEF_RE.findall(src))


def _guide_catalog_section() -> str:
    """Isolate §4 (the component catalog) from the rest of the guide, so a
    class name mentioned in prose elsewhere (worked example, variant
    patterns) can't accidentally satisfy the sync check without being a real
    catalog row."""
    text = DESIGN_GUIDE_PATH.read_text(encoding="utf-8")
    start = text.index("## 4. Component catalog")
    end = text.index("### Component variant patterns")
    assert start < end, "expected §4 catalog to precede 'Component variant patterns'"
    return text[start:end]


def _guide_catalog_classes() -> list:
    return _CATALOG_ROW_RE.findall(_guide_catalog_section())


def test_strategy_components_file_exists():
    assert STRATEGY_COMPONENTS_PATH.exists(), (
        f"expected {STRATEGY_COMPONENTS_PATH} to exist"
    )


def test_design_guide_exists():
    assert DESIGN_GUIDE_PATH.exists(), f"expected {DESIGN_GUIDE_PATH} to exist"


def test_component_count_is_24_today():
    """Non-regression pin on the count this guide's own header text and
    CLAUDE.fork.md both cite, re-derived mechanically (not trusted from
    either doc)."""
    real = _real_component_classes()
    assert len(real) == 24, (
        f"grep-equivalent count of '^class.*SubStrategyComponent' in "
        f"{STRATEGY_COMPONENTS_PATH} is {len(real)}, expected 24 "
        f"(strategies.strategy_components.py). If this legitimately changed, "
        f"update STRATEGY_DESIGN_GUIDE.md §4 AND CLAUDE.fork.md's component-count "
        f"note in the same change."
    )


def test_design_guide_catalog_matches_real_component_classes():
    real = _real_component_classes()
    guide_list = _guide_catalog_classes()
    guide_set = set(guide_list)

    missing_from_guide = real - guide_set
    extra_in_guide = guide_set - real

    assert not missing_from_guide, (
        f"STRATEGY_DESIGN_GUIDE.md §4 is missing component class(es) present in "
        f"{STRATEGY_COMPONENTS_PATH}: {sorted(missing_from_guide)}"
    )
    assert not extra_in_guide, (
        f"STRATEGY_DESIGN_GUIDE.md §4 lists component class(es) that no longer "
        f"exist (or never existed) in {STRATEGY_COMPONENTS_PATH}: "
        f"{sorted(extra_in_guide)}"
    )


def test_design_guide_catalog_has_no_duplicate_rows():
    guide_list = _guide_catalog_classes()
    duplicates = {name for name in guide_list if guide_list.count(name) > 1}
    assert not duplicates, (
        f"STRATEGY_DESIGN_GUIDE.md §4 lists the same component class more than "
        f"once: {sorted(duplicates)}"
    )


def test_design_guide_catalog_count_matches_real_count():
    real = _real_component_classes()
    guide_list = _guide_catalog_classes()
    assert len(guide_list) == len(real), (
        f"STRATEGY_DESIGN_GUIDE.md §4 lists {len(guide_list)} component rows, "
        f"but {STRATEGY_COMPONENTS_PATH} defines {len(real)} component classes. "
        f"(Individual name mismatches, if any, are reported by "
        f"test_design_guide_catalog_matches_real_component_classes.)"
    )
