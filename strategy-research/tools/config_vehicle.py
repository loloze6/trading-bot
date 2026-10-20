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
  5. D-161 (vehicle-format V2-1), once 1-4 pass, against the SOURCE run (source_fit_errors;
     the caller reads the source's base config and block_manifest.yaml): a source without a
     block manifest is refused; every `scaffolding` pointer of the manifest must hold the same
     value in the config as in the base config (scaffolding_errors); and the source manifest,
     relabelled where a regime gate moved the trading regime (derived_manifest), must fit the
     config by block_manifest.check_manifest, the function D-110's exact-config 1b runs -- and,
     with combines_as regime_gate, once the config fits, its ungated twin too (the run's design
     variant, which D-110's route runs with the same manifest).
  Before step 1, a config that refers to itself (a YAML alias cycle) is refused (cycle_error;
  D-161 lead decision): V2-2 writes the config into the brief as JSON.

How the scaffolding rule tells the V1d gate form from a scaffolding rewrite (operator ruling
2026-10-20): the gate form is defined positively, as three allowances that are REVERTED in a
copy of the config before it is compared with the base config, and only with
`combines_as: regime_gate`: (a) regime_detector.rules, .vetoes and .default_regime take the
base config's values; (b) detector components the source does not have (their `id`s absent from
the source's components) are removed when they all come AFTER the source's components (the
vehicle's first entries are the source's, ids in order) and a rule condition or a veto of the
vehicle reads each of them (reading B); (c) when the source and the vehicle each have exactly one trading regime and
they differ, the two regime names are swapped back (the relabel). Whatever still differs under
a scaffolding pointer is the scaffolding rewrite: a mode change, a source detector component
changed, removed or reordered (a swap), an added component nothing reads or placed before or
between the source's components, or any other key
(min_score, ...) -- refused, with its label. Every other combines_as gets no allowance.

Pure apart from reading the trading-bot sources (the registry and validate_config loaded by
file path, the component module read with ast) and the component catalogue.
"""
from __future__ import annotations

import copy
import importlib.util
import json
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
                      f"empty, missing or not a list; write the gate, or choose another "
                      f"combines_as")
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


def cycle_error(config, where: str):
    """D-161 lead decision: the refusal for a config that refers to itself (a YAML alias
    cycle, which yaml.safe_load builds), else None. The config is round-tripped through
    json.dumps(..., default=str), as V2-2's brief writes it; only the cycle (ValueError) is
    a refusal here; anything else json.dumps raises on is left to the later steps, as
    before (this adds no crash). Pure."""
    try:
        json.dumps(config, default=str)
    except ValueError:      # "Circular reference detected"
        return (f"{where}: the config refers to itself (a YAML alias cycle); write it out "
                f"in full")
    except (TypeError, RecursionError):
        return None
    return None


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
    cycle = cycle_error(config, f"{where}.config")
    if cycle:
        # D-161 lead decision: refused before any other step (each would walk the cycle);
        # V2-2 writes the config into the brief as JSON, which a cycle cannot be
        return [cycle]
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


# ---------------------------------------------------------------------------
# D-161 (vehicle-format V2-1): the scaffolding rule, against the source run
# ---------------------------------------------------------------------------
# the gate keys a regime gate may change (allowance (a)); D-160's ungated twin rewrites the same
GATE_KEYS = ("rules", "vetoes", "default_regime")
MAX_SCAFFOLDING_DIFFS = 8      # differences listed per vehicle; the rest are counted
MAX_VALUE_CHARS = 80           # a differing value is shown as JSON, cut to this length
GATE_SUFFIX = ("; a regime gate (D-160) may change only regime_detector.rules, "
               "regime_detector.vetoes and regime_detector.default_regime, and add detector "
               "components its rules or vetoes read after the source's detector components, "
               "every source detector component kept as it is")


def _detector(config):
    rd = config.get("regime_detector") if isinstance(config, dict) else None
    return rd if isinstance(rd, dict) else None


def _component_ids(rd) -> set:
    """The string `id`s of a detector's components (a malformed entry has none)."""
    comps = rd.get("components") if isinstance(rd, dict) else None
    return {c["id"] for c in comps if isinstance(c, dict) and isinstance(c.get("id"), str)} \
        if isinstance(comps, list) else set()


def read_detector_ids(rd) -> set:
    """The component ids a detector's gate reads: the `id` of every threshold_rules rule
    condition (rules[*].any_of[*][*].id, as regime_engine._eval_cond reads it) and of every
    veto (vetoes[*].id). Malformed entries read nothing."""
    rd = rd if isinstance(rd, dict) else {}
    ids = set()
    rules = rd.get("rules")
    for rule in rules if isinstance(rules, list) else []:
        any_of = rule.get("any_of") if isinstance(rule, dict) else None
        for conds in any_of if isinstance(any_of, list) else []:
            for cond in conds if isinstance(conds, list) else []:
                if isinstance(cond, dict) and isinstance(cond.get("id"), str):
                    ids.add(cond["id"])
    vetoes = rd.get("vetoes")
    for veto in vetoes if isinstance(vetoes, list) else []:
        if isinstance(veto, dict) and isinstance(veto.get("id"), str):
            ids.add(veto["id"])
    return ids


def regime_relabel(base, config, combines_as):
    """Q1 (D-161): (r_src, r_v) when a regime gate moved the source's trading regime, i.e.
    combines_as regime_gate, exactly one non-null strategies.regimes entry on each side, and
    the two differ; else None."""
    if combines_as != REGIME_GATE:
        return None
    src, veh = _trading_regimes(base), _trading_regimes(config)
    if len(src) == 1 and len(veh) == 1 and src[0] != veh[0]:
        return src[0], veh[0]
    return None


def _with_mode(config):
    """A deep copy with a missing regime_detector.mode read as threshold_rules (the
    default regime_engine.py applies), so writing the default is no difference."""
    out = copy.deepcopy(config)
    rd = _detector(out)
    if rd is not None:
        rd.setdefault("mode", GATE_MODE)
    return out


def _source_view(base, config, combines_as):
    """The vehicle config with the regime gate's allowances reverted (module docstring:
    (a) gate keys, (b) added components the gate reads, (c) the relabel), in the source's
    regime names; with any other combines_as, the config itself. A deep copy, mode
    defaulted."""
    view = _with_mode(config)
    if combines_as != REGIME_GATE or not isinstance(view, dict):
        return view
    relabel = regime_relabel(base, config, combines_as)
    if relabel:
        swap = {relabel[0]: relabel[1], relabel[1]: relabel[0]}
        regimes = view["strategies"]["regimes"]     # a dict: it has a trading regime
        view["strategies"]["regimes"] = {swap.get(k, k): v for k, v in regimes.items()}
    rd, brd = _detector(view), _detector(base)
    if rd is None:
        return view
    for key in GATE_KEYS:
        if brd is not None and key in brd:
            rd[key] = copy.deepcopy(brd[key])
        else:
            rd.pop(key, None)
    comps = rd.get("components")
    if isinstance(comps, list) and _added_after_source(brd, comps, _detector(config)):
        rd["components"] = comps[:len(_component_list(brd))]
    return view


def _component_list(rd) -> list:
    comps = rd.get("components") if isinstance(rd, dict) else None
    return comps if isinstance(comps, list) else []


def _id_of(comp):
    return comp.get("id") if isinstance(comp, dict) else None


def _added_after_source(brd, comps: list, vehicle_rd) -> bool:
    """Allowance (b) (D-161): True when `comps` (the vehicle's detector components) is the
    source's components, ids in order, followed by at least one entry, each an added
    component (a string id the source does not have) that a rule or veto of the vehicle
    reads. An added component anywhere else (before or between the source's) gets no
    allowance."""
    src = _component_list(brd)
    k = len(src)
    if len(comps) <= k or [_id_of(c) for c in comps[:k]] != [_id_of(c) for c in src]:
        return False
    read, source_ids = read_detector_ids(vehicle_rd), _component_ids(brd)
    return all(isinstance(_id_of(c), str) and _id_of(c) in read and _id_of(c) not in source_ids
               for c in comps[k:])


def _value_at(config, path: str) -> tuple:
    """(found, value) at a JSON pointer; (False, None) when it does not resolve."""
    import json_pointer as jp
    if not jp.json_pointer_exists(config, path):
        return False, None
    return True, jp.resolve_json_pointer(config, path)


def _shown(found: bool, value) -> tuple:
    """(text, truncated) of one differing value: JSON, cut to MAX_VALUE_CHARS."""
    if not found:
        return "(absent)", False
    try:
        text = json.dumps(value, sort_keys=True, default=str)
    except (TypeError, ValueError):    # a model-written mapping with mixed key types
        text = repr(value)
    return _cut(text)


def _cut(text: str) -> tuple:
    """(text, truncated): cut to MAX_VALUE_CHARS (values and pointers alike)."""
    if len(text) > MAX_VALUE_CHARS:
        return text[:MAX_VALUE_CHARS - 3] + "...", True
    return text, False


def _added_label(added: set, read: set, combines_as) -> str:
    """The label of a detector component the source does not have."""
    if combines_as != REGIME_GATE:
        return f"added detector component {sorted(added)}"
    unread = sorted(added - read)
    if unread:
        return f"added detector component that no rule or veto reads {unread}"
    return "added detector component must follow the source's components"


def _label(path: str, src, view, combines_as, config=None) -> str:
    """What a difference at `path` (source regime names) is, for the refusal. `config`: the
    vehicle config itself, whose rules and vetoes say which added components are read (None:
    none read)."""
    import json_pointer as jp  # tools/ sibling
    segs = jp.split_json_pointer(path)
    if segs[0] != "regime_detector" or len(segs) == 1:
        return "structure change"
    key = segs[1]
    if key == "mode":
        return "mode change"
    if key in GATE_KEYS:     # only reachable without combines_as regime_gate (else reverted)
        return f"gate change, which only combines_as {REGIME_GATE} (D-160) may make"
    if key != "components":
        return "structure change"
    srd, vrd = _detector(src), _detector(view)
    src_ids, view_ids = _component_ids(srd), _component_ids(vrd)
    added, read = view_ids - src_ids, read_detector_ids(_detector(config))
    if len(segs) > 2:
        # one entry differs: the same id there is a change of that component (class, params,
        # ...); a different id is a removal, an added component, or a swap
        idx = int(segs[2]) if segs[2].isascii() and segs[2].isdigit() else -1
        s_list, v_list = _component_list(srd), _component_list(vrd)
        s_id = _id_of(s_list[idx]) if 0 <= idx < len(s_list) else None
        v_id = _id_of(v_list[idx]) if 0 <= idx < len(v_list) else None
        if isinstance(s_id, str) and s_id == v_id:
            return "detector component change"
        if src_ids - view_ids:
            return "detector component removal"
        if isinstance(v_id, str) and v_id in added:
            return _added_label(added, read, combines_as)
        return "detector component swap"
    if src_ids - view_ids:
        return "detector component removal"
    if added:
        return _added_label(added, read, combines_as)
    return "detector component swap"


def _vehicle_pointer(path: str, relabel) -> str:
    """`path` (source regime names) in the vehicle's regime names."""
    import json_pointer as jp
    if not relabel:
        return path
    try:
        segs = jp.split_json_pointer(path)
    except jp.JsonPointerError:
        return path
    swap = {relabel[0]: relabel[1], relabel[1]: relabel[0]}
    if len(segs) >= 3 and segs[:2] == ["strategies", "regimes"] and segs[2] in swap:
        segs[2] = swap[segs[2]]
        return "/" + "/".join(str(s).replace("~", "~0").replace("/", "~1") for s in segs)
    return path


def scaffolding_errors(config, base, manifest, combines_as, where: str) -> list:
    """D-161: the refusals for a config vehicle that changes the source run's scaffolding
    ([] when it keeps it). For each `scaffolding` pointer p of the source's block manifest,
    base@p is compared with config@p by nearest_build.config_diff, after the allowances of a
    regime gate are reverted (_source_view; a missing mode read as threshold_rules on both
    sides). One message per differing leaf, at most MAX_SCAFFOLDING_DIFFS (the rest counted);
    values are shown as JSON, and values and pointers cut to MAX_VALUE_CHARS (and said so).
    Pure."""
    import json_pointer as jp
    import nearest_build as nb
    src, view = _with_mode(base), _source_view(base, config, combines_as)
    relabel = regime_relabel(base, config, combines_as)
    diffs = []
    scaff = manifest.get("scaffolding") if isinstance(manifest, dict) else None
    for p in scaff if isinstance(scaff, list) else []:
        if not isinstance(p, str):
            continue
        in_src, in_view = jp.json_pointer_exists(src, p), jp.json_pointer_exists(view, p)
        if not (in_src and in_view):
            if in_src or in_view:
                diffs.append((p, p))
            continue
        diffs += [(p, d["path"]) for d in nb.config_diff(jp.resolve_json_pointer(src, p),
                                                          jp.resolve_json_pointer(view, p), p)]
    errors = []
    for p, path in diffs[:MAX_SCAFFOLDING_DIFFS]:
        before, cut_b = _shown(*_value_at(src, path))
        after, cut_a = _shown(*_value_at(view, path))
        at, cut_at = _cut(_vehicle_pointer(path, relabel))
        under, cut_under = _cut(p)
        cut = (", values truncated" if cut_b or cut_a else "") + (
            ", pointers truncated" if cut_at and cut_under
            else ", pointer truncated" if cut_at or cut_under else "")
        errors.append(
            f"{where}.config: {at} differs from the source run's base "
            f"config ({before} -> {after}{cut}): "
            f"{_label(path, src, view, combines_as, config)} under "
            f"{under}, which the source's block_manifest.yaml lists as scaffolding (not part of "
            f"the idea); keep the source's scaffolding unchanged"
            + (GATE_SUFFIX if combines_as == REGIME_GATE else ""))
    if len(diffs) > MAX_SCAFFOLDING_DIFFS:
        errors.append(f"{where}.config: and {len(diffs) - MAX_SCAFFOLDING_DIFFS} more "
                      f"difference(s) under the source's scaffolding (not listed)")
    return errors


def derived_manifest(base_manifest: dict, base_config, config, combines_as) -> dict:
    """Q1 (D-161): the block manifest the vehicle config runs with, derived by code and never
    stored here: a deep copy of the source's manifest; when a regime gate moved the trading
    regime (regime_relabel -> (r_src, r_v)), every block and scaffolding pointer under
    /strategies/regimes/r_src is renamed to r_v and every one under /strategies/regimes/r_v
    to r_src -- a swap, so a null slot the source lists as scaffolding follows the relabel
    and never overlaps the moved block. Otherwise the source's manifest unchanged. Pure."""
    out = copy.deepcopy(base_manifest)
    relabel = regime_relabel(base_config, config, combines_as)
    if relabel is None or not isinstance(out, dict):
        return out
    block = out.get("block")
    if isinstance(block, dict) and isinstance(block.get("config_paths"), list):
        block["config_paths"] = [_vehicle_pointer(p, relabel) if isinstance(p, str) else p
                                 for p in block["config_paths"]]
    if isinstance(out.get("scaffolding"), list):
        out["scaffolding"] = [_vehicle_pointer(p, relabel) if isinstance(p, str) else p
                              for p in out["scaffolding"]]
    return out


def source_fit_errors(config, base, manifest, combines_as, where: str) -> list:
    """D-161, step 5: the refusals for a config vehicle measured against its source run
    ([] when it fits). `manifest` None (the source has no block_manifest.yaml): refused, the
    exact-config route (D-110) cannot carry it. Else scaffolding_errors, then the derived
    manifest checked against the config by block_manifest.check_manifest (Q3: the function
    D-110's exact-config 1b runs), then, for combines_as regime_gate and once the config fits,
    against its ungated twin. `where` as config_vehicle_errors'. Pure."""
    import block_manifest as bm  # tools/ sibling
    if manifest is None:
        return [f"{where}: the source run has no block manifest (artifacts/block_manifest.yaml), "
                f"so its scaffolding cannot be told from its idea and the exact-config route "
                f"(D-110) cannot carry a config vehicle; write the vehicle as a list of config "
                f"changes instead"]
    errors = scaffolding_errors(config, base, manifest, combines_as, where)
    relabel = regime_relabel(base, config, combines_as)
    named = ("the source run's block_manifest.yaml"
             + (f" with regime {relabel[0]!r} relabelled {relabel[1]!r} (D-161)" if relabel else "")
             + ", checked against this config as the next run's base config")
    derived = derived_manifest(manifest, base, config, combines_as)
    checked = [(named, config)]
    if combines_as == REGIME_GATE:
        # the ungated twin is the run's design variant (D-160), and D-110's route runs it with
        # the same manifest: a pointer under the gate (/regime_detector/vetoes, .../rules/0)
        # resolves in the config and not in the twin. The gate form is config_vehicle_errors'
        # step 4 (the caller runs this only once that passes); a config without it has no twin
        try:
            checked.append((named + " (ungated twin)", ungated_twin(config)))
        except ValueError:
            pass
    for name, cfg in checked:
        try:
            bm.check_manifest(derived, cfg, where=name, error_cls=ValueError)
        except ValueError as exc:
            errors.append(f"{where}.config: {exc}; keep every block and scaffolding path the "
                          f"source's manifest lists (D-110 runs this config with that manifest)")
            # the twin is checked once the config passes: it names only what the derivation
            # itself breaks, never a fault of the config twice (as config_vehicle_errors)
            break
    return errors
