"""
Sync guard for strategy-research/docs/COMPONENT_CATALOG.md against the real component classes in
trading-bot/strategies/strategy_components.py.

This is a REAL sync check (re-derives both sides mechanically at test time), not a hardcoded count: nothing else
enforces that the catalogue stays in step with the code.

Checked:
1. The class-name SET in the catalogue's rows (between the CATALOG:START / CATALOG:END markers) equals the class-name
   SET found by matching `^class X(SubStrategyComponent):` in strategy_components.py -- add, remove or rename a
   component on either side and this test fails, naming exactly what is out of sync.
2. The row count matches the class count (catches a duplicated row that set equality would absorb).
3. Every row carries a kind from the four the catalogue defines (graded, on/off, constant, regime measure).
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
CATALOG_PATH = REPO_ROOT / "strategy-research" / "docs" / "COMPONENT_CATALOG.md"
STRATEGY_COMPONENTS_PATH = REPO_ROOT / "trading-bot" / "strategies" / "strategy_components.py"

START_MARKER = "<!-- CATALOG:START -->"
END_MARKER = "<!-- CATALOG:END -->"
KINDS = ("graded", "on/off", "constant", "regime measure")

_CLASS_DEF_RE = re.compile(r"^class\s+(\w+)\(SubStrategyComponent\):", re.MULTILINE)
# Catalogue rows start with a backticked class name: | `RSIPullbackComponent` | ...
_CATALOG_ROW_RE = re.compile(r"^\|\s*`(\w+)`\s*\|", re.MULTILINE)


def _real_component_classes() -> set:
    src = STRATEGY_COMPONENTS_PATH.read_text(encoding="utf-8")
    return set(_CLASS_DEF_RE.findall(src))


def _catalog_section() -> str:
    """Only the marked catalogue tables, so a class name mentioned in prose or in the feeds table cannot satisfy the
    sync check without being a real catalogue row."""
    text = CATALOG_PATH.read_text(encoding="utf-8")
    start = text.index(START_MARKER)
    end = text.index(END_MARKER)
    assert start < end, "CATALOG:START must precede CATALOG:END"
    return text[start:end]


def _catalog_classes() -> list:
    return _CATALOG_ROW_RE.findall(_catalog_section())


def _catalog_rows() -> list:
    return [line for line in _catalog_section().splitlines() if _CATALOG_ROW_RE.match(line)]


def test_strategy_components_file_exists():
    assert STRATEGY_COMPONENTS_PATH.exists(), f"expected {STRATEGY_COMPONENTS_PATH} to exist"


def test_catalog_exists():
    assert CATALOG_PATH.exists(), f"expected {CATALOG_PATH} to exist"


def test_component_count_is_24_today():
    """Non-regression pin on the count, re-derived mechanically."""
    real = _real_component_classes()
    assert len(real) == 24, (
        f"'^class X(SubStrategyComponent):' count in {STRATEGY_COMPONENTS_PATH} is {len(real)}, expected 24. If this "
        f"legitimately changed, update COMPONENT_CATALOG.md (and its '24 classes' sentence) in the same change."
    )


def test_catalog_matches_real_component_classes():
    real = _real_component_classes()
    listed = set(_catalog_classes())
    missing_from_catalog = real - listed
    extra_in_catalog = listed - real
    assert not missing_from_catalog, (
        f"COMPONENT_CATALOG.md is missing component class(es) present in {STRATEGY_COMPONENTS_PATH}: "
        f"{sorted(missing_from_catalog)}"
    )
    assert not extra_in_catalog, (
        f"COMPONENT_CATALOG.md lists component class(es) that no longer exist (or never existed) in "
        f"{STRATEGY_COMPONENTS_PATH}: {sorted(extra_in_catalog)}"
    )


def test_catalog_has_no_duplicate_rows():
    listed = _catalog_classes()
    duplicates = {name for name in listed if listed.count(name) > 1}
    assert not duplicates, f"COMPONENT_CATALOG.md lists the same component class more than once: {sorted(duplicates)}"


def test_catalog_row_count_matches_real_count():
    real = _real_component_classes()
    listed = _catalog_classes()
    assert len(listed) == len(real), (
        f"COMPONENT_CATALOG.md has {len(listed)} component rows, but {STRATEGY_COMPONENTS_PATH} defines "
        f"{len(real)} component classes. (Individual name mismatches are reported by "
        f"test_catalog_matches_real_component_classes.)"
    )


def test_every_row_has_one_of_the_four_kinds():
    bad = []
    for row in _catalog_rows():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        name, kind = cells[0].strip("`"), cells[4]
        if kind not in KINDS:
            bad.append((name, kind))
    assert not bad, f"rows whose Kind cell is not one of {KINDS}: {bad}"


def test_kinds_are_the_ones_decided_in_d051():
    """D-051: these seven are on/off, BuyAndHoldStrategy is constant, these four are regime measures (ADXDirectional
    is a bounded signed measure and is listed as a regime measure too); every other class is graded."""
    on_off = {"SmaTrendLongOnlyComponent", "GatedSmaTrendLongOnlyComponent", "FundingRateMeanReversionComponent",
              "FearGreedContrarianComponent", "MacdHistogramCrossoverComponent", "WhaleLargeTradeImbalanceComponent",
              "VolumeExpansionHedgeComponent"}
    measures = {"RSquaredRegimeComponent", "EfficiencyRatioRegimeComponent", "VolatilityPercentileRegimeComponent",
                "VarianceRatioComponent", "ADXDirectionalComponent"}
    got = {}
    for row in _catalog_rows():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        got[cells[0].strip("`")] = cells[4]
    for name, kind in got.items():
        if name in on_off:
            assert kind == "on/off", name
        elif name == "BuyAndHoldStrategy":
            assert kind == "constant", name
        elif name in measures:
            assert kind == "regime measure", name
        else:
            assert kind == "graded", (name, kind)
