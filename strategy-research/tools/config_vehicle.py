"""
config_vehicle -- the content check of a config vehicle (D-159, vehicle-format V1c).

A side finding's vehicle may be the complete strategy config instead of a patch list
(reader_proposals.CONFIG_VEHICLE_SHAPE; the shape is reader_proposals.check_config_vehicle).
This module checks its CONTENT where the reading is checked
(run_phase1_research._reading_content_errors), so a failure is a refusal with its message
and the analyst retries in the existing loop:

  1. `requires` (V1b): each listed op or component must be absent today (an op not in
     trading-bot/strategies/registry.py TRANSFORM_OPS_REGISTRY; a component class path that
     decide_next.component_class_status reads `missing`) and used by the config (an `op` of
     a transforms / history_transforms step, or a `class` value, anywhere in it); and every
     absent piece the config uses must be listed. A `class` outside
     strategies.strategy_components (component_class_status `invalid`) is refused, and
     step 2 is then not run, so no model-chosen module is imported at reading time.
  2. trading-bot/tools/validate_config.py validate(config), every rule, with exactly two
     kinds of line dropped: a V3 line naming an op listed in `requires`, and a V12
     cannot-load line naming a class listed in `requires` whose loader message says the
     module imported and has no such attribute. Nothing else is exempt (V4-V17 included),
     and validate_config.py itself is unchanged: whatever rules it holds when this runs
     (D-158's detector-component transforms rule included, once merged) apply.
  3. tools/forecast_rules.py strategies_violations (D-051 graded forecasts, D-149
     standardised forecast).
  A config that validate_config or forecast_rules cannot check (it raises) is a refusal,
  not a crash.

Pure apart from reading the trading-bot sources (the registry and validate_config loaded by
file path, the component module read with ast) and the component catalogue.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

TBOT_ROOT = Path(__file__).resolve().parents[2] / "trading-bot"
# validate_config.py's V3 and V12 lines, as it writes them (validate_config.py:106-108, :325)
_V3_RE = re.compile(r"^VIOLATION V3 \S+\.op: '(.*)' not in TRANSFORM_OPS_REGISTRY$")
_V12_RE = re.compile(r"^VIOLATION V12 \S+\.class: cannot load '([^']+)': (.*)$")
_TRANSFORM_KEYS = ("transforms", "history_transforms")
_modules: dict = {}


def _validate_config_module(trading_bot_root: Path):
    """trading-bot/tools/validate_config.py, loaded by file path (as tools/composition.py
    does: `tools` is also this directory's name); once per root."""
    root = str(Path(trading_bot_root).resolve())
    if root not in _modules:
        path = Path(root) / "tools" / "validate_config.py"
        spec = importlib.util.spec_from_file_location("_tbot_validate_config_vehicle", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _modules[root] = mod
    return _modules[root]


def used_pieces(config) -> tuple:
    """(ops, classes) the config names: every string `op` of a step in a `transforms` or
    `history_transforms` list, and every string `class` value, anywhere in the config
    (block source detectors included). Each dict and list is walked once (by id), so a
    self-referential YAML alias cannot loop."""
    ops, classes, stack, seen = set(), set(), [config], set()
    while stack:
        node = stack.pop()
        if isinstance(node, (dict, list)):
            if id(node) in seen:
                continue
            seen.add(id(node))
        if isinstance(node, dict):
            for key, value in node.items():
                if key in _TRANSFORM_KEYS and isinstance(value, list):
                    ops.update(step["op"] for step in value
                               if isinstance(step, dict) and isinstance(step.get("op"), str))
                if key == "class" and isinstance(value, str):
                    classes.add(value)
                stack.append(value)
        elif isinstance(node, list):
            stack.extend(node)
    return ops, classes


def _exempt(line: str, req_ops: set, req_classes: set) -> bool:
    m = _V3_RE.match(line)
    if m:
        return m.group(1) in req_ops
    m = _V12_RE.match(line)
    if m and m.group(1) in req_classes:
        module, _, name = m.group(1).rpartition(".")
        return f"module '{module}' has no attribute '{name}'" in m.group(2)
    return False


def config_vehicle_errors(vehicle: dict, where: str, *, trading_bot_root: Path = TBOT_ROOT,
                          on_off=None) -> list:
    """The refusal messages for one shape-checked config vehicle ([] when it passes).
    `where` prefixes every message (e.g. "side_findings[0].vehicle"). `on_off`: the D-051
    on/off class names (None: forecast_rules.on_off_classes(), the catalogue)."""
    import decide_next as dn  # tools/ siblings
    import forecast_rules as fr
    config = vehicle["config"]
    requires = vehicle.get("requires") or []
    vc = _validate_config_module(trading_bot_root)
    registry = set(vc.TRANSFORM_OPS_REGISTRY)
    ops, classes = used_pieces(config)
    status = {c: dn.component_class_status(trading_bot_root, c) for c in classes}
    req_ops = {r["name"] for r in requires if r["kind"] == "op"}
    req_classes = {r["name"] for r in requires if r["kind"] == "component"}
    errors = []
    for k, r in enumerate(requires):
        w, name = f"{where}.requires[{k}]", r["name"]
        if r["kind"] == "op":
            if name in registry:
                errors.append(f"{w}: op {name!r} exists today (TRANSFORM_OPS_REGISTRY); remove "
                              f"it from requires")
            elif name not in ops:
                errors.append(f"{w}: op {name!r} is not used by the config (no transforms or "
                              f"history_transforms step has op {name!r}); list only the "
                              f"missing pieces the config uses")
            continue
        st = status.get(name) or dn.component_class_status(trading_bot_root, name)
        if st == "defined":
            errors.append(f"{w}: component {name!r} exists today; remove it from requires")
        elif st == "invalid":
            errors.append(f"{w}: component {name!r} must be a dotted class path in "
                          f"{dn.COMPONENT_MODULE} (as the config's `class` writes it, "
                          f"{dn.COMPONENT_MODULE}.<ClassName>)")
        elif name not in classes:
            errors.append(f"{w}: component {name!r} is not used by the config (no component "
                          f"has class {name!r}); list only the missing pieces the config uses")
    for op in sorted(ops - registry - req_ops):
        errors.append(f"{where}.config: op {op!r} does not exist today (not in "
                      f"TRANSFORM_OPS_REGISTRY) and is not listed in requires: use an existing "
                      f"op, or list it as {{kind: op, name: {op}, spec, example}}")
    for cls in sorted(c for c in classes if status[c] == "missing" and c not in req_classes):
        errors.append(f"{where}.config: component class {cls!r} does not exist today and is "
                      f"not listed in requires: use an existing component, or list it as "
                      f"{{kind: component, name: {cls}, spec, example}}")
    invalid = sorted(c for c in classes if status[c] == "invalid")
    for cls in invalid:
        if cls not in req_classes:   # a listed one is already refused above (requires branch)
            errors.append(f"{where}.config: component class {cls!r} must be a dotted class path "
                          f"in {dn.COMPONENT_MODULE} (as the config's `class` writes it, "
                          f"{dn.COMPONENT_MODULE}.<ClassName>)")
    checker = "validate_config"
    try:
        # with any class outside COMPONENT_MODULE, validate() is NOT run: its V12 imports each
        # `class` module, and that would be a model-chosen import at reading time
        lines = [] if invalid else vc.validate(config)
        checker = "forecast_rules"
        msgs = fr.strategies_violations(config,
                                        fr.on_off_classes() if on_off is None else on_off)
    except Exception as exc:  # noqa: BLE001 -- a malformed model-written config is a refusal
        errors.append(f"{where}.config: {checker} cannot check it "
                      f"({type(exc).__name__}: {str(exc)[:200]}); write the complete strategy "
                      f"config, regime_detector and strategies, as the base config has them")
    else:
        errors += [f"{where}.config: {ln}" for ln in lines
                   if not _exempt(ln, req_ops, req_classes)]
        errors += [f"{where}.config: {m}" for m in msgs]
    return errors
