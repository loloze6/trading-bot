import sys
import os
import json
from typing import Any, Dict, List

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from strategies.registry import HISTORY_OPS, TRANSFORM_OPS_REGISTRY, transform_min_periods, _load_class

_VALID_REGIMES = {"trending", "mean_reversion", "chop", "unknown"}


def _all_transform_lists(config: dict):
    """Yield (location_path, transforms_list) for every transforms/history_transforms list in config."""
    rd = config.get("regime_detector", {})

    for i, veto in enumerate(rd.get("vetoes", [])):
        tfs = veto.get("transforms", [])
        if tfs:
            yield f"regime_detector.vetoes[{i}].transforms", tfs

    for rname, rcfg in rd.get("regimes", {}).items():
        if rcfg is None:
            continue
        for j, comp in enumerate(rcfg.get("components", [])):
            tfs = comp.get("transforms", [])
            if tfs:
                yield f"regime_detector.regimes.{rname}.components[{j}].transforms", tfs
            htfs = comp.get("history_transforms", [])
            if htfs:
                yield f"regime_detector.regimes.{rname}.components[{j}].history_transforms", htfs

    strat = config.get("strategies", {})
    for rname, rcfg in strat.get("regimes", {}).items():
        if rcfg is None:
            continue
        for j, comp in enumerate(rcfg.get("components", [])):
            tfs = comp.get("transforms", [])
            if tfs:
                yield f"strategies.regimes.{rname}.components[{j}].transforms", tfs
            htfs = comp.get("history_transforms", [])
            if htfs:
                yield f"strategies.regimes.{rname}.components[{j}].history_transforms", htfs


def validate(config: dict) -> List[str]:
    violations: List[str] = []

    # V1: structure
    if "regime_detector" not in config:
        violations.append("VIOLATION V1 config: missing top-level key 'regime_detector'")
    if "strategies" not in config:
        violations.append("VIOLATION V1 config: missing top-level key 'strategies'")

    if "strategies" in config:
        for rname, rval in config["strategies"].get("regimes", {}).items():
            if rval is not None and not isinstance(rval, dict):
                violations.append(
                    f"VIOLATION V1 strategies.regimes.{rname}: value must be object or null, got {type(rval).__name__}"
                )

    # Abort early if top-level structure is broken — later checks assume it
    if violations:
        return violations

    rd = config["regime_detector"]
    component_ids = {c["id"] for c in rd.get("components", [])}

    # V2: every veto id, rule condition id, and score-mode component id declared in components
    for i, veto in enumerate(rd.get("vetoes", [])):
        vid = veto.get("id")
        if vid not in component_ids:
            violations.append(
                f"VIOLATION V2 regime_detector.vetoes[{i}].id: '{vid}' not declared in regime_detector.components"
            )

    for i, rule in enumerate(rd.get("rules", [])):
        for j, cond_set in enumerate(rule.get("any_of", [])):
            for k, cond in enumerate(cond_set):
                cid = cond.get("id")
                if cid and cid not in component_ids:
                    violations.append(
                        f"VIOLATION V2 regime_detector.rules[{i}].any_of[{j}][{k}].id:"
                        f" '{cid}' not declared in regime_detector.components"
                    )

    for rname, rcfg in rd.get("regimes", {}).items():
        if rcfg is None:
            continue
        for j, comp in enumerate(rcfg.get("components", [])):
            cid = comp.get("id")
            if cid not in component_ids:
                violations.append(
                    f"VIOLATION V2 regime_detector.regimes.{rname}.components[{j}].id:"
                    f" '{cid}' not declared in regime_detector.components"
                )

    # V3: every transforms/history_transforms op exists in TRANSFORM_OPS_REGISTRY
    for loc, transforms in _all_transform_lists(config):
        for k, step in enumerate(transforms):
            op = step.get("op")
            if op not in TRANSFORM_OPS_REGISTRY:
                violations.append(
                    f"VIOLATION V3 {loc}[{k}].op: '{op}' not in TRANSFORM_OPS_REGISTRY"
                )

    # V4: every op has a TRANSFORM_MIN_PERIODS entry
    for loc, transforms in _all_transform_lists(config):
        for k, step in enumerate(transforms):
            op = step.get("op")
            if op in TRANSFORM_OPS_REGISTRY:
                try:
                    transform_min_periods(op, step.get("params", {}))
                except KeyError:
                    violations.append(
                        f"VIOLATION V4 {loc}[{k}].op: '{op}' has no TRANSFORM_MIN_PERIODS entry"
                    )

    # V5: in every transforms list, no history-based op appears after a scalar/data-aware op
    for loc, transforms in _all_transform_lists(config):
        seen_non_history = False
        for k, step in enumerate(transforms):
            op = step.get("op", "")
            if op in HISTORY_OPS:
                if seen_non_history:
                    violations.append(
                        f"VIOLATION V5 {loc}[{k}]: history-based op '{op}' appears after scalar/data-aware op"
                    )
                    break
            else:
                seen_non_history = True

    # V6: per-component lookback override, if present, >= max transform_min_periods
    def _check_lookback(loc: str, comp_spec: dict) -> None:
        lookback = comp_spec.get("lookback")
        if lookback is None:
            return
        all_steps = comp_spec.get("transforms", []) + comp_spec.get("history_transforms", [])
        known = [s for s in all_steps if s.get("op") in TRANSFORM_OPS_REGISTRY]
        if not known:
            return
        try:
            min_needed = max(transform_min_periods(s["op"], s.get("params", {})) for s in known)
        except KeyError:
            return  # V4 already flagged missing entry
        if lookback < min_needed:
            violations.append(
                f"VIOLATION V6 {loc}: lookback={lookback} < transform min_periods={min_needed}"
            )

    for rname, rcfg in rd.get("regimes", {}).items():
        if rcfg is None:
            continue
        for j, comp in enumerate(rcfg.get("components", [])):
            _check_lookback(f"regime_detector.regimes.{rname}.components[{j}]", comp)

    for rname, rcfg in config["strategies"].get("regimes", {}).items():
        if rcfg is None:
            continue
        for j, comp in enumerate(rcfg.get("components", [])):
            _check_lookback(f"strategies.regimes.{rname}.components[{j}]", comp)

    # V7: every regime name used anywhere is valid
    for i, rule in enumerate(rd.get("rules", [])):
        rname = rule.get("regime")
        if rname not in _VALID_REGIMES:
            violations.append(
                f"VIOLATION V7 regime_detector.rules[{i}].regime: '{rname}' not in {sorted(_VALID_REGIMES)}"
            )

    for i, veto in enumerate(rd.get("vetoes", [])):
        rname = veto.get("result")
        if rname not in _VALID_REGIMES:
            violations.append(
                f"VIOLATION V7 regime_detector.vetoes[{i}].result: '{rname}' not in {sorted(_VALID_REGIMES)}"
            )

    # An ABSENT key means "unknown" — regime_engine.py:70 reads it as
    # config.get("default_regime", "unknown") — so mirror that default here rather
    # than skipping the check on None. An EXPLICIT null is a different thing: not a
    # regime name, and it maps to no _REGIME_MAP entry.
    default_regime = rd.get("default_regime", "unknown")
    if default_regime not in _VALID_REGIMES:
        violations.append(
            f"VIOLATION V7 regime_detector.default_regime: '{default_regime}' not in {sorted(_VALID_REGIMES)}"
        )

    for rname in rd.get("regimes", {}).keys():
        if rname not in _VALID_REGIMES:
            violations.append(
                f"VIOLATION V7 regime_detector.regimes.{rname}: regime name '{rname}' not in {sorted(_VALID_REGIMES)}"
            )

    for rname in config["strategies"].get("regimes", {}).keys():
        if rname not in _VALID_REGIMES:
            violations.append(
                f"VIOLATION V7 strategies.regimes.{rname}: regime name '{rname}' not in {sorted(_VALID_REGIMES)}"
            )

    # V9: default_regime must not alias a "real" trading regime (trending, mean_reversion,
    # chop) WHILE rules is non-empty — that combination bypasses the regime gate: every bar
    # that fails all the rules still gets classified as that regime and traded, silently
    # defeating the gate's entire purpose.
    #
    # This restriction does NOT apply when rules == [] (and components == []): that is the
    # canonical fully-ungated pattern (F1, 2026-07-04 — see
    # tests/test_ungated_config_pattern.py and workflow_artifacts/skills/backtest-engineering/SKILL.md
    # "Ungated hypotheses" section). With no rules to bypass, default_regime is a pure,
    # empirically-verified label with no behavioral effect — it may be any of the four
    # valid names, including trending/mean_reversion/chop. Forbidding it unconditionally
    # (the previous version of this check) blocked "trending" even in the fully-ungated
    # case for no behavioral reason, while never actually checking "mean_reversion" or
    # "chop" for the genuine bypass case this rule exists to prevent — both gaps are
    # closed by conditioning on `rules`.
    mode = rd.get("mode", "threshold_rules")
    # Same mirror as V7 above: an absent key means "unknown", so V9 and V10 judge the
    # regime the engine will actually resolve to. An explicit null still yields None
    # here (.get substitutes only for a MISSING key), which V7 has already rejected —
    # that is what keeps V10's `is not None` guard below meaningful instead of
    # emitting a second, garbled violation for the same fault.
    default_regime_val = rd.get("default_regime", "unknown")
    rules_nonempty = bool(rd.get("rules"))
    if (
        mode in ("threshold_rules", "score_product")
        and rules_nonempty
        and default_regime_val in ("trending", "mean_reversion", "chop")
    ):
        violations.append(
            f"VIOLATION V9 regime_detector.default_regime: '{default_regime_val}' is forbidden "
            f"in mode '{mode}' while regime_detector.rules is non-empty. Bars that fail every "
            "rule still get classified as this regime and traded, bypassing the gate. Set "
            "default_regime to 'unknown', or — if no rules/gate is intended at all — clear "
            "regime_detector.rules and regime_detector.components entirely (fully-ungated "
            "pattern; default_regime may then be any of the four valid names)."
        )

    # V10: a declared fully-ungated regime_detector (components == [] AND rules == []) must
    # not point default_regime at a null strategies.regimes entry — that combination is a
    # "dead" config that forecasts 0.0 on every bar forever, with no error anywhere to say
    # so. This is the concrete mistake the canonical ungated pattern must guard against
    # (moving default_regime without moving the components block that goes with it).
    fully_ungated = rd.get("components", []) == [] and rd.get("rules", []) == []
    if fully_ungated and default_regime_val is not None:
        strat_regimes = config["strategies"].get("regimes", {})
        target_block = strat_regimes.get(default_regime_val)
        if target_block is None:
            violations.append(
                f"VIOLATION V10 strategies.regimes.{default_regime_val}: regime_detector is "
                "fully ungated (components=[] and rules=[]), so EVERY bar resolves to "
                f"default_regime='{default_regime_val}' — but strategies.regimes.{default_regime_val} "
                "is null or missing. This config forecasts 0.0 on every bar; move the real "
                "components block to this key."
            )

    # V8: every strategy-engine component has numeric weight; per-regime total > 0
    for rname, rcfg in config["strategies"].get("regimes", {}).items():
        if rcfg is None:
            continue
        total_weight = 0.0
        all_numeric = True
        for j, comp in enumerate(rcfg.get("components", [])):
            w = comp.get("weight")
            if not isinstance(w, (int, float)):
                violations.append(
                    f"VIOLATION V8 strategies.regimes.{rname}.components[{j}].weight:"
                    f" must be numeric, got {type(w).__name__}"
                )
                all_numeric = False
            else:
                total_weight += float(w)
        if all_numeric and total_weight <= 0:
            violations.append(
                f"VIOLATION V8 strategies.regimes.{rname}: total weight {total_weight} is not > 0"
            )

    # V11: strategies.min_allocation_change, if present, overrides RiskManager's
    # min_allocation_change.threshold control (config.json's risk_management.controls)
    # for this strategy's runs. RiskManager compares abs(allocation_change) against
    # it, so it must be a non-negative number.
    if "min_allocation_change" in config["strategies"]:
        mac = config["strategies"]["min_allocation_change"]
        if isinstance(mac, bool) or not isinstance(mac, (int, float)) or mac < 0:
            violations.append(
                f"VIOLATION V11 strategies.min_allocation_change: must be a non-negative "
                f"number, got {mac!r}"
            )

    # V12: every declared component's 'class' dotted path must resolve to a real,
    # importable class in strategies.strategy_components (or wherever it actually
    # points). Today (pre-V12), an invented/typo'd class name is never caught here
    # -- it only fails much later, at engine startup, via
    # strategies.registry._load_class raising ValueError -- after a full backtest
    # has already been launched and its data fetched. Reuses _load_class itself
    # (rather than re-implementing the resolution) so V12 fails on EXACTLY the
    # same set of configs the engine would refuse to start on, no more, no less.
    #
    # Only the two locations that actually declare a 'class' key are checked:
    # regime_detector.components[] (shared by rules/vetoes/score-mode regimes,
    # which reference these by 'id', not by their own 'class') and
    # strategies.regimes.*.components[] (the per-regime forecast ensemble).
    # score-mode/score_product-mode regime_detector.regimes.*.components[] entries
    # have no 'class' of their own -- see STRATEGY_DESIGN_GUIDE.md 'Regime detector' -- so
    # there is nothing to check there.
    def _check_component_class(loc: str, comp: dict) -> None:
        class_path = comp.get("class")
        if not class_path:
            violations.append(
                f"VIOLATION V12 {loc}: missing required 'class' key"
            )
            return
        try:
            _load_class(class_path)
        except ValueError as e:
            # CODE-REVIEW FIX (2026-09-21): a dotless class_path (e.g.
            # "RSIPullbackComponent" with no module prefix) makes
            # _load_class's own `class_path.rsplit(".", 1)` unpacking raise
            # a bare ValueError ("not enough values to unpack") that never
            # names class_path at all -- confirmed by direct execution.
            # Always include class_path explicitly here so the violation is
            # actionable regardless of which failure mode inside
            # _load_class produced `e`.
            violations.append(f"VIOLATION V12 {loc}.class: cannot load {class_path!r}: {e}")

    for i, comp in enumerate(rd.get("components", [])):
        _check_component_class(f"regime_detector.components[{i}]", comp)

    for rname, rcfg in config["strategies"].get("regimes", {}).items():
        if rcfg is None:
            continue
        for j, comp in enumerate(rcfg.get("components", [])):
            _check_component_class(f"strategies.regimes.{rname}.components[{j}]", comp)

    # V13 (E-060 S3a): the opt-in block combiner (`blocks` +
    # `block_standardisation` on a strategies regime). Silent for every regime
    # that uses neither key. Reuses the engine's own check, so V13 fails on
    # exactly the configs the engine refuses to construct.
    from strategies.strategy_engine import validate_block_combiner
    for rname, rcfg in config["strategies"].get("regimes", {}).items():
        for msg in validate_block_combiner(rname, rcfg):
            violations.append(f"VIOLATION V13 {msg}")

    # V14: every vol_target op carries valid params (window, target_annual_vol,
    # periods_per_year) and sits in a strategies component's final `transforms`
    # in a regime without `blocks` -- the one place the engine's required
    # periods cover its window + 1 closes (strategy_engine._data_periods). In
    # the regime detector, in `history_transforms` (applied from the
    # component's own period) or in a block regime (its own buffer) it would
    # raise on short data. Silent for every config without vol_target. Reuses
    # the op's own param check, so V14 fails on exactly the params the op refuses.
    from strategies.registry import vol_target_param_errors
    strat_regimes = config["strategies"].get("regimes", {})

    def _in_strategy_transforms(loc: str) -> bool:
        # A strategies component's `transforms`, in a regime without `blocks`
        # (shared by V14 and V16).
        parts = loc.split(".")
        return (parts[0] == "strategies" and loc.endswith("].transforms")
                and "blocks" not in (strat_regimes.get(parts[2]) or {}))

    for loc, transforms in _all_transform_lists(config):
        allowed = _in_strategy_transforms(loc)
        for k, step in enumerate(transforms):
            if step.get("op") == "vol_target":
                if not allowed:
                    violations.append(
                        f"VIOLATION V14 {loc}[{k}]: vol_target is allowed only in a strategies "
                        f"component's `transforms`, in a regime without `blocks`")
                for msg in vol_target_param_errors(step.get("params", {})):
                    violations.append(f"VIOLATION V14 {loc}[{k}].params: {msg}")

    # V15: every standardise op has valid params (window int >= 2, 2 <= min_periods
    # <= window, target / cap finite > 0). Reuses the op's own param check, so V15
    # fails on exactly the params the op refuses. Silent for every config without it.
    # Placement: standardise is the first step of a `transforms` list and the only
    # history op in it -- a history op reads the raw history and ignores the running
    # value (registry.apply_transform_pipeline), so any other history op in the list
    # would discard standardise's output or be discarded by it.
    from strategies.registry import standardise_param_errors
    for loc, transforms in _all_transform_lists(config):
        ops = [step.get("op") for step in transforms]
        for k, step in enumerate(transforms):
            if step.get("op") != "standardise":
                continue
            if not loc.endswith(".transforms"):
                violations.append(
                    f"VIOLATION V15 {loc}[{k}]: standardise belongs in `transforms`, as its first "
                    f"step; here it sees one value at a time and always gives 0")
            elif k != 0:
                violations.append(
                    f"VIOLATION V15 {loc}[{k}]: standardise must be the first step of `transforms` "
                    f"(it reads the raw history and ignores the steps before it)")
            others = sorted({o for o in ops if o in HISTORY_OPS and o != "standardise"})
            if others and loc.endswith(".transforms"):
                violations.append(
                    f"VIOLATION V15 {loc}[{k}]: standardise must be the only history op in "
                    f"`transforms`; remove {', '.join(others)} (a history op reads the raw history "
                    f"and ignores the running value, so the two cannot be combined)")
            for msg in standardise_param_errors(step.get("params", {})):
                violations.append(f"VIOLATION V15 {loc}[{k}].params: {msg}")

    # V16 (CUL-354): every signed_power op has valid params (exponent a finite
    # number with 1 <= exponent <= 3, required; pivot, if given, a finite number
    # with 10 <= pivot <= 20; registry.SIGNED_POWER_BOUNDS). Reuses the op's
    # own param check, so V16 fails on exactly the params the op refuses.
    # Placement (operator ruling 2026-10-19, the V14 pattern): only in a strategies
    # component's `transforms`, in a regime without `blocks` -- the one place a
    # value the op refuses lands in generate_signals' try (forecast 0.0, regime
    # ERROR). In `history_transforms` it would abort the rest of
    # strategy_engine.update for the bar (later components' histories fall out
    # of step); in the regime detector it would escape generate_signals. No
    # position rule within the list (standardise, signed_power, clip is fine).
    # Silent for every config without signed_power.
    from strategies.registry import signed_power_param_errors
    for loc, transforms in _all_transform_lists(config):
        allowed = _in_strategy_transforms(loc)
        for k, step in enumerate(transforms):
            if step.get("op") == "signed_power":
                if not allowed:
                    violations.append(
                        f"VIOLATION V16 {loc}[{k}]: signed_power is allowed only in a strategies "
                        f"component's `transforms`, in a regime without `blocks` (a value it "
                        f"refuses raises there, inside generate_signals' guard)")
                for msg in signed_power_param_errors(step.get("params", {})):
                    violations.append(f"VIOLATION V16 {loc}[{k}].params: {msg}")

    return violations


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_config.py <config_path>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        cfg = json.load(f)

    errs = validate(cfg)
    for e in errs:
        print(e)
    sys.exit(1 if errs else 0)
