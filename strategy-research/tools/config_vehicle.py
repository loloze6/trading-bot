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
     module imported and has no such attribute. Nothing else is exempt (V4-V18 included),
     and validate_config.py itself is unchanged: whatever rules it holds when this runs
     (D-158's detector-component transforms rule included, once merged) apply.
  3. tools/forecast_rules.py strategies_violations (D-051 graded forecasts, D-149
     standardised forecast).
  A config that validate_config or forecast_rules cannot check (it raises) is a refusal,
  not a crash.
  4. D-160 (vehicle-format V1d): with `combines_as: regime_gate`, the gate form
     (gate_form_errors): mode threshold_rules, a non-empty `regime_detector.rules` or
     `regime_detector.vetoes`, and exactly one non-null `strategies.regimes` entry. Once the
     config passes 1-3 and the form, its ungated twin (ungated_twin, D-052) is checked by
     steps 2-3 exactly like the config (the same `requires` exemptions); a twin failure is a
     refusal naming the twin. The twin is derived by code and never stored.

Pure apart from reading the trading-bot sources (the registry and validate_config loaded by
file path, the component module read with ast) and the component catalogue.
"""
from __future__ import annotations

import copy
import importlib.util
import re
from pathlib import Path

TBOT_ROOT = Path(__file__).resolve().parents[2] / "trading-bot"
# validate_config.py's V3 and V12 lines, as it writes them (validate_config.py:106-108, :325)
_V3_RE = re.compile(r"^VIOLATION V3 \S+\.op: '(.*)' not in TRANSFORM_OPS_REGISTRY$")
_V12_RE = re.compile(r"^VIOLATION V12 \S+\.class: cannot load '([^']+)': (.*)$")
_TRANSFORM_KEYS = ("transforms", "history_transforms")
_modules: dict = {}
# D-160: the combines_as word (reader_proposals.COMBINES_AS) whose config vehicle must have the
# gate form, and the one detector mode whose gate the D-052 twin recipe removes
REGIME_GATE = "regime_gate"
GATE_MODE = "threshold_rules"


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


def _trading_regimes(config) -> list:
    """The `strategies.regimes` names whose value is not null, in config order."""
    strat = config.get("strategies") if isinstance(config, dict) else None
    regimes = strat.get("regimes") if isinstance(strat, dict) else None
    return [r for r, v in regimes.items() if v is not None] if isinstance(regimes, dict) else []


def gate_form_errors(config, where: str) -> list:
    """D-160: the form of a config whose idea combines as a regime gate ([] when it has it).
    `where` names the config (e.g. "side_findings[0].vehicle.config"). The gate is
    `regime_detector.rules` or `regime_detector.vetoes`, at least one non-empty; the strategy is
    exactly one non-null `strategies.regimes` entry (the regime the gate trades in). The mode
    is threshold_rules (absent = threshold_rules, as regime_engine.py reads it): the ungated
    twin (D-052) empties the rules and sets default_regime, and only that mode reads them, so
    in score / score_product mode the twin would still be gated."""
    rd = config.get("regime_detector") if isinstance(config, dict) else None
    rd = rd if isinstance(rd, dict) else {}
    errors = []
    mode = rd.get("mode", GATE_MODE)
    if mode != GATE_MODE:
        errors.append(f"{where}.regime_detector.mode={mode!r}: combines_as {REGIME_GATE} needs "
                      f"mode {GATE_MODE} (the default): its ungated twin (D-052) empties the "
                      f"rules and sets default_regime, which only {GATE_MODE} mode reads")
    rules, vetoes = rd.get("rules"), rd.get("vetoes")
    if not (isinstance(rules, list) and rules) and not (isinstance(vetoes, list) and vetoes):
        errors.append(f"{where}.regime_detector: combines_as {REGIME_GATE} needs the gate, a "
                      f"non-empty regime_detector.rules or regime_detector.vetoes, and both are "
                      f"empty or missing; write the gate, or choose another combines_as")
    trading = _trading_regimes(config)
    if len(trading) != 1:
        errors.append(f"{where}.strategies.regimes: combines_as {REGIME_GATE} needs exactly one "
                      f"non-null regime (the regime the gate trades in), and this config has "
                      f"{len(trading)} {trading}; set every other regime to null")
    return errors


def ungated_twin(config: dict) -> dict:
    """D-052 / D-160: the ungated version of a regime-gated config, derived by code. A deep
    copy with `regime_detector.rules` emptied ([]), `regime_detector.vetoes` dropped (the key
    removed: regime_engine.py and validate_config.py both read a missing key as [], and the
    twin has no veto at all rather than an empty one), and `regime_detector.default_regime`
    set to the single non-null `strategies.regimes` entry; the detector components and
    everything else kept, so the twin warms up exactly like the gated config and every bar
    trades the same strategy. Pure; `config` is not changed. Raises ValueError, with the
    gate_form_errors messages, when the config does not have the gate form."""
    errors = gate_form_errors(config, "config")
    if errors:
        raise ValueError("; ".join(errors))
    twin = copy.deepcopy(config)
    rd = twin["regime_detector"]
    rd["rules"] = []
    rd.pop("vetoes", None)
    rd["default_regime"] = _trading_regimes(config)[0]
    return twin


def _content_errors(config, where: str, vc, fr, on_off, req_ops: set, req_classes: set,
                    run_validate: bool) -> list:
    """Steps 2-3 for one config (the vehicle's, or its ungated twin), every line prefixed
    with `where`; a checker that raises is a refusal, not a crash."""
    checker = "validate_config"
    try:
        # run_validate False (a class outside COMPONENT_MODULE): validate() is NOT run, since
        # its V12 imports each `class` module, a model-chosen import at reading time
        lines = vc.validate(config) if run_validate else []
        checker = "forecast_rules"
        msgs = fr.strategies_violations(config,
                                        fr.on_off_classes() if on_off is None else on_off)
    except Exception as exc:  # noqa: BLE001 -- a malformed model-written config is a refusal
        return [f"{where}: {checker} cannot check it "
                f"({type(exc).__name__}: {str(exc)[:200]}); write the complete strategy "
                f"config, regime_detector and strategies, as the base config has them"]
    return ([f"{where}: {ln}" for ln in lines if not _exempt(ln, req_ops, req_classes)]
            + [f"{where}: {m}" for m in msgs])


def config_vehicle_errors(vehicle: dict, where: str, *, trading_bot_root: Path = TBOT_ROOT,
                          on_off=None, combines_as=None) -> list:
    """The refusal messages for one shape-checked config vehicle ([] when it passes).
    `where` prefixes every message (e.g. "side_findings[0].vehicle"). `on_off`: the D-051
    on/off class names (None: forecast_rules.on_off_classes(), the catalogue).
    `combines_as`: the side finding's word; REGIME_GATE adds step 4 (D-160)."""
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
    errors += _content_errors(config, f"{where}.config", vc, fr, on_off, req_ops, req_classes,
                              run_validate=not invalid)
    if combines_as != REGIME_GATE:
        return errors
    errors += gate_form_errors(config, f"{where}.config")
    if errors:
        # the twin differs from the config only in the detector's rules, vetoes and
        # default_regime: checked once the config passes, it names only what the
        # derivation itself breaks, never a fault of the config twice
        return errors
    twin = ungated_twin(config)
    tw = (f"{where}.config ungated twin (D-052: rules [], vetoes dropped, default_regime "
          f"{twin['regime_detector']['default_regime']!r})")
    return _content_errors(twin, tw, vc, fr, on_off, req_ops, req_classes, run_validate=True)
