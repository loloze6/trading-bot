"""
forecast_rules -- the D-051, D-053 and D-149 config checks (DECISION_LOG.md).

Pure helpers, no I/O beyond reading the component catalogue. Used by
run_phase1_research under orchestrator.config_direct_authoring: right after
1b (strategy_config_authoring) on the base config, and in step 5a (the
tool-only backtest_specification) on every variant's config AFTER its patch is
applied -- so a patch that removes a banned piece passes, and one that adds it
is refused.

  * D-051 (graded forecasts only): a component in `strategies` must not be an
    on/off class (COMPONENT_CATALOG.md, Kind column), and its `transforms` /
    `history_transforms` must not use the dead-zone ops `threshold_filter` or
    `volume_filter`. The regime detector is not checked: an on/off condition
    belongs there.
  * D-053 (a design variant keeps the idea): a variant's component classes
    equal the base config's -- the regime detector's components and each
    strategy regime's components, in order. A parameter or transform change
    passes; adding, removing or replacing a component, or setting a regime to
    null, does not.
  * D-149 (standardised forecast, strict): every component in `strategies`
    passes only when its `transforms` holds `standardise` and no `scale` op, or
    holds `vol_target`, or its regime has both `blocks` and
    `block_standardisation`. Anything else is refused -- a bare `scale` or
    `scaling_factor`, a component with no scale at all (its class default scale
    is not standardised), and `standardise` together with `scale` in one
    `transforms` list. That `standardise` is the FIRST step is validate_config.py's
    V15, not this module's. The regime detector is not checked.

Classes are matched by their bare class name (the last segment of the dotted
`class` path): every component lives in strategies.strategy_components, and
whether the path loads at all is validate_config.py's V12, not this module's.
Malformed pieces (a non-dict component, a non-list transforms) are skipped
here for D-051: validate_config.py reports them. D-149 skips a non-dict
component but refuses a dict one whose transforms is not a list (it holds no
standardise or vol_target).
"""
from __future__ import annotations

import re
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parents[1] / "docs" / "COMPONENT_CATALOG.md"
_START_MARKER = "<!-- CATALOG:START -->"
_END_MARKER = "<!-- CATALOG:END -->"
_ROW_RE = re.compile(r"^\|\s*`(\w+)`\s*\|", re.MULTILINE)
_KIND_CELL = 4  # class, params, exact output, range & sign, KIND, ...
ON_OFF_KIND = "on/off"
DEAD_ZONE_OPS = ("threshold_filter", "volume_filter")
RULE_SENTENCE = (
    "Standardised forecast (hard rule). Every component in strategies puts standardise first in "
    "its transforms, and no scale op after it (standardise: past values only, target 10, cap 20, "
    "window, min_periods), unless its scale is set by vol_target or the regime is a blocks regime "
    "with block_standardisation. Any other component, including one whose only scale is a bare "
    "scale or scaling_factor, is refused after 1b and again at 5a.")


class CatalogError(RuntimeError):
    """COMPONENT_CATALOG.md is missing or cannot be read as the kind table."""


def catalog_rows(catalog_path: Path = CATALOG_PATH) -> list:
    """The component rows between the catalogue markers, as lists of stripped
    cells (class cell first, backticks kept), in file order. Raises
    CatalogError when the catalogue is missing, has no marked table, or has no
    component row."""
    path = Path(catalog_path)
    if not path.is_file():
        raise CatalogError(f"{path}: component catalogue not found (D-051 needs its Kind column)")
    text = path.read_text(encoding="utf-8")
    start, end = text.find(_START_MARKER), text.find(_END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise CatalogError(f"{path}: no {_START_MARKER} ... {_END_MARKER} table")
    rows = [line for line in text[start:end].splitlines() if _ROW_RE.match(line)]
    if not rows:
        raise CatalogError(f"{path}: no component rows between the catalogue markers")
    return [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]


def on_off_classes(catalog_path: Path = CATALOG_PATH) -> frozenset:
    """The class names whose catalogue Kind is `on/off`. Raises CatalogError
    when the catalogue is missing, has no marked table, has a row without a
    Kind cell, or lists no on/off class at all (an empty set would silently
    let every on/off component through)."""
    path = Path(catalog_path)
    on_off = set()
    for cells in catalog_rows(path):
        if len(cells) <= _KIND_CELL or not cells[_KIND_CELL]:
            raise CatalogError(f"{path}: row without a Kind cell: {'| '.join(cells)[:120]!r}")
        if cells[_KIND_CELL] == ON_OFF_KIND:
            on_off.add(cells[0].strip("`"))
    if not on_off:
        raise CatalogError(f"{path}: no row has Kind {ON_OFF_KIND!r}")
    return frozenset(on_off)


def _class_name(class_path) -> str | None:
    if not isinstance(class_path, str) or not class_path:
        return None
    return class_path.rsplit(".", 1)[-1]


def _strategy_components(config):
    """Yield (regime name, index, component dict) for strategies.regimes.*.components[*]."""
    strategies = config.get("strategies") if isinstance(config, dict) else None
    regimes = strategies.get("regimes") if isinstance(strategies, dict) else None
    if not isinstance(regimes, dict):
        return
    for rname, rcfg in regimes.items():
        comps = rcfg.get("components") if isinstance(rcfg, dict) else None
        if not isinstance(comps, list):
            continue
        for j, comp in enumerate(comps):
            if isinstance(comp, dict):
                yield rname, j, comp


def _ops(pipeline) -> set:
    """The op names in a transform list (a non-list or non-dict step is skipped)."""
    if not isinstance(pipeline, list):
        return set()
    return {step.get("op") for step in pipeline if isinstance(step, dict)}


def _not_standardised(comp, regime_cfg) -> bool:
    """D-149 (strict): True unless the component's `transforms` holds `standardise`
    and no `scale`, or holds `vol_target`, or its regime is a blocks regime with
    block_standardisation."""
    if isinstance(regime_cfg, dict) and "blocks" in regime_cfg and "block_standardisation" in regime_cfg:
        return False
    tf = _ops(comp.get("transforms"))
    return not ("vol_target" in tf or ("standardise" in tf and "scale" not in tf))


def strategies_violations(config, on_off) -> list:
    """D-051 and D-149 messages for `config` (empty when it passes)."""
    out = []
    strategies = config.get("strategies") if isinstance(config, dict) else None
    regimes = strategies.get("regimes") if isinstance(strategies, dict) else {}
    for rname, j, comp in _strategy_components(config):
        loc = f"strategies.regimes.{rname}.components[{j}]"
        name = _class_name(comp.get("class"))
        if name in on_off:
            out.append(
                f"D-051: on/off class {name} at {loc} (id {comp.get('id')!r}) -- a forecast "
                f"component must be graded (COMPONENT_CATALOG.md Kind 'graded'); an on/off "
                f"condition belongs in the regime detector")
        for key in ("history_transforms", "transforms"):
            pipeline = comp.get(key)
            if not isinstance(pipeline, list):
                continue
            for k, step in enumerate(pipeline):
                op = step.get("op") if isinstance(step, dict) else None
                if op in DEAD_ZONE_OPS:
                    out.append(
                        f"D-051: dead-zone op {op!r} at {loc}.{key}[{k}] -- threshold_filter "
                        f"and volume_filter are not allowed on a forecast component (a "
                        f"'strong enough' or 'volume above average' condition belongs in the "
                        f"regime detector)")
        if _not_standardised(comp, regimes.get(rname)):
            out.append(f"D-149: {loc} (id {comp.get('id')!r}) -- " + RULE_SENTENCE)
    return out


def class_signature(config) -> dict:
    """The component classes of `config`, by place: the regime detector's
    components in order, and each strategy regime's components in order (a
    regime whose value is null stays None)."""
    rd = config.get("regime_detector") if isinstance(config, dict) else None
    rd_comps = rd.get("components") if isinstance(rd, dict) else None
    detector = ([_class_name(c.get("class")) if isinstance(c, dict) else None for c in rd_comps]
                if isinstance(rd_comps, list) else None)
    strategies = config.get("strategies") if isinstance(config, dict) else None
    regimes = strategies.get("regimes") if isinstance(strategies, dict) else None
    per_regime = {}
    if isinstance(regimes, dict):
        for rname, rcfg in regimes.items():
            comps = rcfg.get("components") if isinstance(rcfg, dict) else None
            per_regime[rname] = ([_class_name(c.get("class")) if isinstance(c, dict) else None
                                  for c in comps] if isinstance(comps, list) else None)
    return {"regime_detector": detector, "strategies": per_regime}


def class_mismatch(base_config, variant_config) -> list:
    """D-053 messages: every place where the variant's component classes differ
    from the base config's (empty when they are equal)."""
    base, var = class_signature(base_config), class_signature(variant_config)
    out = []
    if base["regime_detector"] != var["regime_detector"]:
        out.append(f"regime_detector.components: base {base['regime_detector']} vs variant "
                   f"{var['regime_detector']}")
    for rname in sorted(set(base["strategies"]) | set(var["strategies"]), key=str):
        b = base["strategies"].get(rname, "<absent>")
        v = var["strategies"].get(rname, "<absent>")
        if b != v:
            out.append(f"strategies.regimes.{rname}.components: base {b} vs variant {v}")
    return [f"D-053: the variant changes the component classes -- {d}; a design variant "
            f"changes one parameter or transform, never adds, removes or replaces a component"
            for d in out]
