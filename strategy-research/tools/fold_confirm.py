"""E-077 PR-2 (D-087): confirm a claim on the fold of the run built from it.

Under orchestrator.folds.enabled only (run_phase1_research wires it; nothing here
reads a flag). Design: engineering/delivery_plan_readers.md Amendment 1, Step 11 and
A1.11 (final Stage 1, items 2 and 3); engineering/roadmap/E-075/ITERATIVE_PLAN_JUDGEMENT.md
sections 1 (Q1 gaps a-c), 3 (the noise rule) and 4 (PR-2).

A claim is never confirmed inside the run that inspired it. A reader (later an
analyst) proposes a claim with a VEHICLE -- the strategy change its own run
backtests. If decide-next picks it, the CHILD run backtests the source run's config
with the vehicle applied, on a fold its source run was not on (D-123; PR-1, D-085).
After that backtest `confirm_on_fold` measures the claim's tests -- the SOURCE
proposal's tests, found by the child brief's `candidate.source.proposal_ref` and
identified by spec_hash -- on the child's saved bars over the child's fold, and
writes one row to campaign_record/confirmations.yaml.

How it finds things
-------------------
  source claim    research_brief.yaml candidate.source.proposal_ref
                  ("runs/<src>/artifacts/proposals/<category>.yaml#<proposal id>"), loaded
                  with reader_proposals.load_proposals; only a side finding is a claim
                  (a child built from a patch or a new block returns None: no claim).
  vehicle variant the child variant that carries the vehicle. decide-next gives the
                  child the source run's base config WITH the vehicle applied (step 1b
                  starts from it, candidate.start_config), so that is the child's own
                  `base` variant; callers may name another one.
  base variant    the child's base variant, recorded beside the vehicle variant. No
                  test slot compares one variant with another today (the baselines
                  `complement`, `placebo` and `other_selector` are all inside one
                  variant's bars), so it is passed to a custom `measure` hook and
                  recorded, and the default measurement does not need it.
  the fold        the fold in the child's pre_registration (research_folds); the
                  child's protocol windows must be exactly that fold's blocks.

The statuses
------------
  confirmed       THE NOISE RULE (below) holds for every test of the claim.
  not_confirmed   a test was measured and the rule fails: the claim is refuted on this
                  fold (kept as knowledge).
  not_measurable  no events, an unreadable source or bars, a vehicle variant that was not
                  backtested, a measured variant whose strategy config does not carry the
                  vehicle (`vehicle_not_in_measured_config`: step 1b may have changed the
                  config the child started from), the claim's own floor not met (R5), or
                  too few of the fold's windows with a value to grade (R5: fewer than the
                  fold's windows minus WINDOWS_ALLOWED_AGAINST; a fold of SOL/UNI has almost
                  no 2018-2021 bars). Kept as knowledge; the look is counted when the
                  selector was actually run.
  not_comparable  the child's card tests (spec_hash) are not the source claim's: the run
                  was not built for this claim (the spec-hash rule of explore_confirm's
                  resolve_pending, kept). Nothing is measured.

THE NOISE RULE -- a noise rule, NOT a size rule and NOT a cost rule
-------------------------------------------------------------------
R5 (operator ruling 2026-10-19 on engineering/FOLD-FLOORS-2026-10-19/REPORT.md), for one
test, in this order:
  (0) THE CLAIM'S FLOOR, read as claim_measure computes it (pooled per horizon over the
      fold's windows, `floor_not_met` of the measured result): any entry at any horizon
      -> not_measurable, reason "floor not met: ...", never confirmed.
  (1) THE COUNT IS OVER THE FOLD'S WINDOWS (fold_blocks; confirm_on_fold passes them):
      a window with no value -- no bars on the fold's window, or no event there --
      counts AGAINST, exactly like a window with the wrong sign. A horizon is judged
      only when at least (fold windows - WINDOWS_ALLOWED_AGAINST) of the fold's windows
      have a value (and never fewer than MIN_WINDOWS, see the constant); a horizon with
      fewer is too short to grade.
  (2) at EVERY judged horizon: the pooled oriented effect is > 0 (the claimed sign
      holds), AND the windows against (wrong sign, a zero, or no value) are at most
      WINDOWS_ALLOWED_AGAINST. A judged horizon failing either part is a real refutation:
      not_confirmed (it fails only through a window WITH a value of the wrong sign beyond
      the allowance, or a non-positive pooled value).
Horizons that are judged are judged first: a refutation there is not_confirmed even when
another horizon is too short to grade (that horizon makes the test not_measurable only
when every judged horizon holds).
A claim is confirmed only if every one of its tests (at most 3) is confirmed.
Why it exists: a claim with no effect points the right way by luck about half the time
(explore_confirm.test_sign needs only a positive pooled value), so "the sign held" would
put about half of all null claims into the registry as building blocks. With six
windows, under a symmetric null the chance that at least 5 of 6 share the claimed sign
is 7/64 = about 11% per fold, and 6 of 6 about 1.6%; a lineage confirmed on two folds is
near 1%. Windows of one fold share a market phase, so the true chance is somewhat higher.
Counting an empty window against (R5) keeps a fold with 1 or 2 empty windows near or
below that chance (measured 0.03-0.04 and 0.000, REPORT.md section 4.2) instead of the
0.19-0.29 of counting only the windows with a value.
SEVERAL COINS (operator, 2026-10-08, option C; D-089): in each window the coins are pooled
into ONE value first (the test's statistic over every coin's bars or trades of that window,
exactly as claim_measure pools a coin's windows), then "all but one window" is applied over
the fold's windows -- so a 3-coin claim faces the same ~11% chance per fold as a one-coin
claim, not 17 of 18 symbol-window cells. One coin is measured exactly as before (its cells
ARE its windows). Every look is counted in the ledger. It uses numbers every measurement already has
(claim_measure.measure_test: the pooled oriented value and the per-window values). The
EFFECT SIZE and the agreement count (k of the fold's windows) are recorded for every horizon of every
claim; NO COST appears anywhere: whether an effect survives costs is judged where a
strategy is assembled, not here.

WHY THIS CANNOT LEAK (no lookahead): the measurement reads only the child run's own saved
bars.csv (claim_measure / claim_tests, unchanged), restricted to the fold's windows, and
refuses any bar at or after the holdout start. The fold's dates come from
config/folds.yaml, which research_folds validates against the data policy (research
period only; never the validation period or the holdout).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

CONFIRMED = "confirmed"
NOT_CONFIRMED = "not_confirmed"
NOT_MEASURABLE = "not_measurable"
NOT_COMPARABLE = "not_comparable"
STATUSES = (CONFIRMED, NOT_CONFIRMED, NOT_MEASURABLE, NOT_COMPARABLE)

BASIS_CHILD_RUN = "child_run"
ROW_ARTIFACT = "fold_confirmation.yaml"      # artifacts/ of the child run
SCHEMA_VERSION = 1

#: THE NOISE RULE's two numbers (see the module docstring).
#: R5: the windows needed with a value are max(MIN_WINDOWS, fold windows -
#: WINDOWS_ALLOWED_AGAINST). On every fold of config/folds.yaml (6 blocks) that is 5, so
#: MIN_WINDOWS has no separate role there (REPORT.md section 4.1); it is kept only as a
#: backstop for a fold of 4 or fewer windows (never graded on fewer than 4 windows with a
#: value; folds below 4 blocks were not measured) and because the row records it.
MIN_WINDOWS = 4
WINDOWS_ALLOWED_AGAINST = 1   # windows against (wrong sign or no value) allowed, of the fold's

#: option C (D-089): the per-window values pooled over the coins, beside per_window
POOLED_KEY = "per_window_coins_pooled"

RULE_NAME = "noise_rule"
RULE_TEXT = ("NOISE RULE, not a size rule and no cost comparison: not measurable when the claim's own "
             "floor is not met at any horizon (pooled over the fold's windows, as claim_measure "
             "computes it); else confirmed when, at every horizon with a value, the pooled effect has "
             "the claimed sign AND the claimed sign holds in all but at most "
             f"{WINDOWS_ALLOWED_AGAINST} of the fold's windows, a window with no value counting "
             f"against (fewer of the fold's windows with a value than all but "
             f"{WINDOWS_ALLOWED_AGAINST}, or than {MIN_WINDOWS}: not measurable). About an 11% "
             "chance per fold for a claim with no effect (6 windows), about 1% after two folds; every "
             "look is counted. Measured on the run built from the claim, on a fold its source run was "
             "not on; not proven.")

_REF_RE = re.compile(r"runs/(?P<run>[^/]+)/artifacts/proposals/(?P<cat>[^/]+)\.yaml#(?P<pid>.+)")


# ---------------------------------------------------------------------------
# The rule, on one measure_test result
# ---------------------------------------------------------------------------

def grade_test(result: dict, fold_windows=None) -> dict:
    """{status, reason, horizons} of ONE claim_measure.measure_test result under the
    noise rule, R5 (module docstring). `fold_windows`: the fold's window labels
    (fold_blocks; confirm_on_fold passes them), over which the all-but-one count runs --
    a fold window the measurement has no value for counts against. None (or empty): the
    windows the measurement itself carries (its per-window cells), so a cell with no value
    still counts against but a window with no bars at all cannot be seen.
    `horizons`: per horizon with a pooled value, {effect, oriented, n_events,
    windows_claimed_sign (k), windows_with_value (n), windows_in_fold, windows_against
    (windows_in_fold - k), windows_without_value (labels), windows_needed_with_value,
    per_window (oriented value per measured cell, as before), events_per_window (the
    cell's n_events, same keys as per_window: claim_tests' selected events with an outcome
    in that window; for coins pooled per window, the sum over the coins), pooled_sign_held,
    windows_rule_held}. Pure."""
    import claim_measure as cmeas
    st = result.get("status")
    if st == cmeas.NO_EVENTS:
        return {"status": NOT_MEASURABLE,
                "reason": "no events: the selector matched no bar on the fold's windows"}
    if st != cmeas.MEASURED:
        why = result.get("detail") or result.get("reason")
        return {"status": NOT_MEASURABLE, "reason": f"not measured: {why}"}
    fold = [str(w) for w in fold_windows] if fold_windows else None
    horizons, coins_error = {}, None
    for h, r in sorted((result.get("horizons") or {}).items(), key=lambda kv: float(kv[0])):
        oriented = r.get("oriented")
        if oriented is None:
            continue
        cells = r.get(POOLED_KEY)
        if cells is None and len(_coins(r.get("per_window"))) > 1:
            # option C needs the coins pooled per window BEFORE the rule: a measurement that
            # carries only symbol-window cells cannot be graded (never graded per cell)
            coins_error = (f"several coins {_coins(r.get('per_window'))} but no per-window "
                           f"value pooled over the coins ({POOLED_KEY}): the noise rule "
                           f"counts windows, not coin-window cells")
            break
        src = cells if cells is not None else r.get("per_window") or {}
        per_window = {str(w): c.get("oriented") for w, c in src.items()}
        # what was measured in each window, kept whatever the status (operator 2026-10-19):
        # same keys as per_window; a window with no cell is absent from both
        events_per_window = {str(w): c.get("n_events") for w, c in src.items()}
        # one value per window: a pooled cell is keyed by the window, a one-coin cell by
        # "<symbol>/<window>" (claim_tests.Window.label)
        by_window = {w.rsplit("/", 1)[-1]: v for w, v in per_window.items()}
        # the fold's windows, then any measured window outside them (confirm_on_fold never
        # produces one: it checks the protocol windows are exactly the fold's blocks)
        counted = list(dict.fromkeys((fold or []) + list(by_window)))
        k = sum(1 for w in counted if by_window.get(w) is not None and by_window[w] > 0)
        n = sum(1 for w in counted if by_window.get(w) is not None)
        need = max(MIN_WINDOWS, len(counted) - WINDOWS_ALLOWED_AGAINST)
        horizons[str(h)] = {"effect": r.get("value"), "oriented": oriented,
                            "n_events": r.get("n_events"),
                            "windows_claimed_sign": k, "windows_with_value": n,
                            "windows_in_fold": len(counted),
                            "windows_against": len(counted) - k,
                            "windows_without_value": [w for w in counted
                                                      if by_window.get(w) is None],
                            "windows_needed_with_value": need,
                            "per_window": per_window,
                            "events_per_window": events_per_window,
                            "pooled_sign_held": oriented > 0,
                            "windows_rule_held": (n >= need and len(counted) - k
                                                  <= WINDOWS_ALLOWED_AGAINST)}
    # (0) the claim's own floor, before any count (R5): never confirmed below it
    floor_not_met = [str(x) for x in (result.get("floor_not_met") or [])]
    if floor_not_met:
        out = {"status": NOT_MEASURABLE,
               "reason": "floor not met: " + "; ".join(floor_not_met)}
        if coins_error is None:
            out["horizons"] = horizons
        return out
    if coins_error is not None:
        return {"status": NOT_MEASURABLE, "reason": coins_error}
    if not horizons:
        return {"status": NOT_MEASURABLE, "reason": "no horizon has a pooled value on the fold",
                "horizons": horizons}
    # horizons with enough of the fold's windows with a value are judged FIRST: a refutation
    # there stands whatever a thinner horizon could say (a claim refuted 0 of 6 at h=1 is not
    # "unmeasurable" because h=24 has 3 windows). A judged horizon can fail only through a
    # window WITH a value of the wrong sign beyond the allowance, or a non-positive pooled
    # value: a real refutation.
    judged = {h: x for h, x in horizons.items()
              if x["windows_with_value"] >= x["windows_needed_with_value"]}
    bad = [f"h={h}: pooled {'held' if x['pooled_sign_held'] else 'NOT held'}, windows "
           f"{x['windows_claimed_sign']} of {x['windows_in_fold']}"
           + (f" ({len(x['windows_without_value'])} without a value)"
              if x["windows_without_value"] else "")
           for h, x in judged.items() if not (x["pooled_sign_held"] and x["windows_rule_held"])]
    if bad:
        return {"status": NOT_CONFIRMED, "horizons": horizons,
                "reason": "the noise rule fails: " + "; ".join(bad)}
    short = [f"h={h}: {x['windows_with_value']} of the fold's {x['windows_in_fold']} windows "
             f"with a value, {x['windows_needed_with_value']} needed"
             for h, x in horizons.items() if h not in judged]
    if short:
        return {"status": NOT_MEASURABLE, "horizons": horizons,
                "reason": ("too few of the fold's windows with a value to grade (all but "
                           f"{WINDOWS_ALLOWED_AGAINST}, and at least {MIN_WINDOWS}; an empty "
                           "window counts against): " + "; ".join(short))}
    return {"status": CONFIRMED, "horizons": horizons,
            "reason": ("the pooled sign held at every horizon and the claimed sign held in all but "
                       "at most one of the fold's windows: " + "; ".join(
                           f"h={h} {x['windows_claimed_sign']} of {x['windows_in_fold']}"
                           for h, x in horizons.items()))}


def row_test_entry(result: dict, graded: dict) -> dict:
    """One test's entry in the fold_confirmation row: its spec_hash, grade_test's output, and
    the claim's floor exactly as claim_measure.measure_test read it (the result's `floor`, a
    copy), kept whatever the status (operator 2026-10-19). A result claim_measure never
    produced (not measured: an error, no bars) carries no floor and the entry none. Pure."""
    entry = {"spec_hash": (result or {}).get("spec_hash"), **graded}
    floor = (result or {}).get("floor")
    if isinstance(floor, dict):
        entry["floor"] = dict(floor)
    return entry


def _coins(per_window) -> list:
    """The coins of a measurement's per-window cells (labels "<symbol>/<window>"; the window
    never holds a "/", so the coin is everything before the LAST one). A label without "/"
    names no coin."""
    return sorted({str(k).rsplit("/", 1)[0] for k in (per_window or {}) if "/" in str(k)})


def pooled_per_window(per: list, spec, h: int) -> dict:
    """{window: {value, oriented, n_events, coins}}: option C (D-089). In each window the
    test's statistic over every coin's events of that window, pooled exactly as
    claim_measure._per_coin pools one coin's windows (claim_tests._pooled); `per` is
    claim_tests.effect_sizes' prepared data (bar or trade windows). Pure."""
    import claim_tests as ct
    import numpy as np
    stat = ct.STATISTICS[spec.statistic]
    out = {}
    for win in dict.fromkeys(p["w"].window for p in per):
        sub = [p for p in per if p["w"].window == win]
        raw, oriented = stat(*ct._pooled(sub, h), spec.direction)
        events = [p["mask"] & np.isfinite(p["ys"][h]) for p in sub]
        if spec.statistic == "rank_ic":
            events = [ev & np.isfinite(p["fc"]) for ev, p in zip(events, sub)]
        out[str(win)] = {"value": _finite(raw), "oriented": _finite(oriented),
                         "n_events": int(sum(int(ev.sum()) for ev in events)),
                         "coins": sorted({p["w"].symbol for p in sub})}
    return out


def _finite(v):
    import math
    return None if v is None or not math.isfinite(float(v)) else float(v)


def measure_on_fold(run_dir: Path, vid: str, tests: list, windows, eras, holdout_start: str,
                    *, trade_tests: bool = False):
    """The default measurement of confirm_on_fold: explore_confirm.measure_on_windows (one
    coin: nothing else, exactly as before), and when the windows hold SEVERAL coins, each
    measured test's horizons also carry POOLED_KEY, the coins pooled per window (option C,
    D-089), which grade_test counts instead of the symbol-window cells. Same signature and
    return shape as measure_on_windows.
    `trade_tests` (D-091, orchestrator.analyst.enabled): a test of the trade-level family is
    measured on the variant's TradeWindows over the same windows (claim_measure.measure_test
    with the family on), and pooled per window the same way. Off: every test goes through
    measure_on_windows exactly as before (a trade test is then recorded as an error there)."""
    import claim_measure as cmeas
    import claim_tests as ct
    import explore_confirm as ec
    trade = ({str(t.get("name")) for t in tests if cmeas._is_trade_test(t)}
             if trade_tests else set())
    bar_tests = [t for t in tests if not (isinstance(t, dict) and str(t.get("name")) in trade)]
    keep = set(windows)
    if bar_tests or not trade:
        results, measured = ec.measure_on_windows(run_dir, vid, bar_tests, windows, eras,
                                                  holdout_start)
    else:
        results, measured = {}, []
    tws = []
    if trade:
        tws = [tw for tw in ct.load_variant_trade_windows(Path(run_dir), vid) if tw.window in keep]
        if not tws:
            raise ValueError(f"variant {vid!r} has no trades or bars on the windows {sorted(keep)}")
        cmeas.check_before_holdout(tws, holdout_start)
        for t in tests:
            name = str(t.get("name")) if isinstance(t, dict) else "None"
            if name not in trade:
                continue
            try:
                results[name] = cmeas.measure_test(tws, t, eras, True)
            except Exception as exc:  # noqa: BLE001 -- recorded per test, as measure_on_windows does
                results[name] = {"name": name, "status": cmeas.NOT_MEASURED, "reason": ec.ERROR,
                                 "detail": f"{type(exc).__name__}: {exc}"}
        measured = measured or [tw.label for tw in tws]
    ws = [w for w in ct.load_variant_bars(Path(run_dir), vid) if w.window in keep]
    if len({w.symbol for w in ws}) < 2:
        return results, measured
    by_name = {str(t.get("name")): t for t in tests if isinstance(t, dict)}
    for name, res in results.items():
        if res.get("status") != cmeas.MEASURED or name not in by_name:
            continue
        try:
            is_trade = name in trade
            spec, _h = cmeas.test_spec(by_name[name], is_trade)
            per, _out_h, hz, _rng = ct.effect_sizes(tws if is_trade else ws, spec, eras)
            pooled = {h: pooled_per_window(per, spec, h) for h in hz}
        except Exception as exc:  # noqa: BLE001 -- recorded per test, as measure_on_windows does
            results[name] = {"name": name, "status": cmeas.NOT_MEASURED, "reason": ec.ERROR,
                             "spec_hash": res.get("spec_hash"),
                             "detail": f"pooling the coins per window: {type(exc).__name__}: {exc}"}
            continue
        for h, cells in pooled.items():
            if h in res.get("horizons", {}):
                res["horizons"][h][POOLED_KEY] = cells
    return results, measured


def combine(graded: dict) -> tuple:
    """(status, reason) of a claim from {test name: grade_test(...)}. Confirmed only if
    EVERY test is (claim_tests.combine, D-014); not_confirmed as soon as one measured
    test fails the rule, whatever the others say; else not_measurable."""
    if not graded:
        return NOT_MEASURABLE, "the claim has no test to measure"
    statuses = {n: g["status"] for n, g in graded.items()}
    if all(s == CONFIRMED for s in statuses.values()):
        return CONFIRMED, "every test of the claim passed the noise rule"
    failed = sorted(n for n, s in statuses.items() if s == NOT_CONFIRMED)
    if failed:
        return NOT_CONFIRMED, "; ".join(f"{n}: {graded[n]['reason']}" for n in failed)
    return NOT_MEASURABLE, "; ".join(f"{n}: {graded[n]['reason']}" for n, s in sorted(statuses.items())
                                     if s != CONFIRMED)


# ---------------------------------------------------------------------------
# The source claim
# ---------------------------------------------------------------------------

def source_ref(arts: Path):
    """(source run, category, proposal id) from the brief's candidate.source.proposal_ref,
    or None when the run was not built from a reader proposal."""
    path = Path(arts) / "research_brief.yaml"
    if not path.exists():
        return None
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    ref = (((doc.get("candidate") or {}).get("source") or {}).get("proposal_ref")
           if isinstance(doc, dict) else None)
    m = _REF_RE.fullmatch(ref.replace("\\", "/")) if isinstance(ref, str) else None
    return (m.group("run"), m.group("cat"), m.group("pid")) if m else None


def source_item(root: Path, ref: tuple):
    """The flattened reader proposal the ref names (reader_proposals.load_proposals), or None
    when the file has no such proposal. Raises ProposalError / OSError when unreadable."""
    import reader_proposals as rp
    run, _cat, pid = ref
    items = rp.load_proposals(Path(root) / "runs" / run / "artifacts" / "proposals",
                              list(rp.READER_RUBRIC_VERSIONS))
    for cat_items in items.values():
        for item in cat_items:
            if item.get("proposal_id") == pid:
                return item
    return None


def vehicle_missing(config, vehicle) -> list:
    """The vehicle changes {component_id, field, before, after} that `config` (a strategy
    config dict) does not carry: [] when every one is present with its `after` value. Same
    resolution as decide_next.resolve_patch -- exactly one component with that id, the field
    inside it -- but the value read must equal `after`, not `before`. Each missing change is
    a string naming it and what was found. Pure."""
    import decide_next as dn
    import json_pointer as jp
    missing = []
    for k, item in enumerate(vehicle or []):
        label = f"vehicle[{k}] {item.get('component_id')}.{item.get('field')} -> {item.get('after')!r}"
        ptrs = dn._component_pointers(config, item.get("component_id"))
        if len(ptrs) != 1:
            missing.append(f"{label}: {len(ptrs)} components with that id in the measured config")
            continue
        try:
            current = jp.resolve_json_pointer(config, ptrs[0] + dn.field_to_pointer_suffix(item.get("field")))
        except (dn.DecideNextError, jp.JsonPointerError) as exc:
            missing.append(f"{label}: the field does not resolve in the measured config ({exc})")
            continue
        if current != item.get("after"):
            missing.append(f"{label}: the measured config has {current!r}")
    return missing


MAX_CONFIG_DIFFS_SHOWN = 3     # differing leaves named in a config vehicle's reason


def config_vehicle_missing(config, vehicle: dict) -> list:
    """D-162: a CONFIG vehicle (a mapping, D-159) is in `config` (the measured strategy
    config) when the whole config is the same: one string per leaf that differs
    (nearest_build.config_diff, CUL-412's definition, so 1 and 1.0 are equal), naming the
    vehicle's value and the measured one; [] when they are the same. Pure."""
    import nearest_build as nb
    return [f"{d['path']}: the vehicle has {d['before']!r}, the measured config has "
            f"{d['after']!r}" for d in nb.config_diff(vehicle.get("config"), config)]


def _start_config_changed(arts: Path, vid: str):
    """None when variant `vid`'s strategy_config.json has the same values as the config
    decide-next started the child from (research_brief.yaml candidate.start_config), else
    why not: the leaves that differ (nearest_build.config_diff, CUL-412's own definition of
    "1b changed it", so 1 and 1.0 are equal), or either side unreadable / absent."""
    import nearest_build as nb
    try:
        brief = yaml.safe_load((arts / "research_brief.yaml").read_text(encoding="utf-8")) or {}
        start = (brief.get("candidate") or {}).get("start_config")
        cfg = json.loads((arts / "variants" / vid / "strategy_config.json").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 -- recorded
        return f"the start config or the measured config cannot be read ({type(exc).__name__}: {exc})"
    if not isinstance(start, dict):
        return "the brief carries no candidate.start_config to compare with"
    diff = nb.config_diff(start, cfg)
    if not diff:
        return None
    more = f" (+{len(diff) - 3} more)" if len(diff) > 3 else ""
    return (f"variant {vid!r} ran another config than the source config the claim is about: "
            + "; ".join(f"{d['path']}: {d['before']!r} -> {d['after']!r}" for d in diff[:3]) + more)


def _spec_hashes(res) -> list:
    return sorted(t["spec_hash"] for t in res.tests if t.get("spec_hash"))


# ---------------------------------------------------------------------------
# confirm_on_fold
# ---------------------------------------------------------------------------

def _row_base(child: str, ref: tuple, item: dict | None, fold: str | None) -> dict:
    claim = (item or {}).get("claim") or {}
    row = {"schema_version": SCHEMA_VERSION, "finding_id": ref[2], "category": ref[1],
           "source_run": ref[0], "run_id": child, "basis": BASIS_CHILD_RUN, "fold": fold,
           "kind": claim.get("kind"), "statement": claim.get("statement"),
           "rule": {"name": RULE_NAME, "min_windows": MIN_WINDOWS,
                    "windows_allowed_against": WINDOWS_ALLOWED_AGAINST, "text": RULE_TEXT}}
    for key in ("vehicle", "combines_as", "fold_observed"):
        if item and key in item:
            row[key] = item[key]
    if isinstance(row.get("vehicle"), dict):
        # Q4 (D-162): a config vehicle is kept slim, with a pointer to the full config (the
        # child's brief carries it as candidate.start_config)
        import decide_next as dn
        row["vehicle"] = dn.slim_vehicle(
            row["vehicle"], f"runs/{child}/artifacts/research_brief.yaml#"
                            f"{dn.START_CONFIG_POINTER}")
    return row


def _finish(row: dict, status: str, reason: str, **extra) -> dict:
    row.update({"status": status, "reason": reason, **extra})
    return row


def confirm_on_fold(run_dir: Path, run_id: str, *, root: Path, folds_doc: dict | None = None,
                    eras, holdout_start: str, vehicle_variant: str | None = None,
                    base_variant: str | None = None, fresh_variants=None,
                    measure=None, folds_path=None, policy_path=None, trade_tests: bool = False):
    """Measure the source claim's tests on the child run `run_id`'s vehicle variant over
    its fold, and return the ledger row (explore_confirm.record_fold_confirmation writes
    it). None when the run was not built from a side finding (nothing to confirm). Never
    raises for a content problem: it is a row with a status and a reason.

    `fresh_variants`: the variants backtested in THIS attempt (None: every graded one).
    `measure(run_dir, variant, tests, window_labels, eras, holdout_start) ->
    ({test name: measure_test-shaped result}, [windows measured])`: default measure_on_fold
    (explore_confirm.measure_on_windows, plus the coins pooled per window when there are
    several, D-089), which also measures the trade-level family when `trade_tests` is on.
    `trade_tests` (D-091, orchestrator.analyst.enabled): the source claim and the child's card
    are checked with the trade-level family, and `measure` gets trade_tests as a keyword (only
    when on, so a custom hook is called as before)."""
    import claim_card as cc
    import claim_tests as ct
    import explore_confirm as ec
    import json_pointer as jp
    import reader_proposals as rp
    import research_folds as rf
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    ref = source_ref(arts)
    if ref is None:
        return None
    try:
        item = source_item(root, ref)
    except Exception as exc:  # noqa: BLE001 -- a row, not a crash
        return _finish(_row_base(run_id, ref, None, None), NOT_MEASURABLE,
                       f"the source proposal cannot be read ({type(exc).__name__}: {exc})")
    if item is None:
        return _finish(_row_base(run_id, ref, None, None), NOT_MEASURABLE,
                       f"the proposal_ref names {ref[2]!r}, which is not in the source run's "
                       f"proposals")
    if item.get("kind") != rp.SIDE_FINDING:
        return None                      # a patch or a new block: no claim to confirm
    try:
        fold = rf.fold_of_run_dir(run_dir)
    except rf.FoldsError as exc:
        fold = None
        fold_error = str(exc)
    else:
        fold_error = None
    row = _row_base(run_id, ref, item, fold)
    if fold is None:
        return _finish(row, NOT_MEASURABLE,
                       fold_error or "this run carries no fold in its pre_registration "
                       "(machine_constraints.protocol.fold): it was not placed on a fold, so "
                       "nothing is measured")
    # the source claim and its tests
    claim = item.get("claim")
    tt = {"trade_tests": True} if trade_tests else {}     # D-091
    res = cc.check_claim(claim, folds=True, **tt)
    if res.errors:
        return _finish(row, NOT_MEASURABLE, "the source claim is refused by check_claim: "
                       + "; ".join(res.errors))
    if res.tests_none:
        return _finish(row, NOT_MEASURABLE,
                       f"tests: none (missing block {res.missing_block!r}): a trade-level or other "
                       f"test family the slots cannot express yet; recorded as knowledge")
    source_hashes = _spec_hashes(res)
    row["spec_hashes"] = source_hashes
    names = {t["name"] for t in res.tests}
    tests = [t for t in claim["tests"] if isinstance(t, dict) and t.get("name") in names]
    # the spec-hash rule (explore_confirm.resolve_pending, kept): the child's own card must
    # carry the same tests, else it was not built for this claim
    card_path = arts / "hypothesis_card.yaml"
    try:
        card = yaml.safe_load(card_path.read_text(encoding="utf-8")) if card_path.exists() else None
        own = cc.check_claim((card or {}).get("claim") if isinstance(card, dict) else None,
                             cc.card_criteria_ids(card if isinstance(card, dict) else {}),
                             folds=True, **tt)
        own_hashes = [] if own.errors else _spec_hashes(own)
    except Exception as exc:  # noqa: BLE001 -- recorded
        own_hashes = []
        row["own_card_error"] = f"{type(exc).__name__}: {exc}"
    if set(own_hashes) != set(source_hashes):
        return _finish(row, NOT_COMPARABLE,
                       "not comparable: the run built from this claim carries other tests "
                       "(spec_hash differs from the claim's, or its card has none); nothing is "
                       "measured",
                       own_spec_hashes=own_hashes)
    # the fold and the child's protocol must agree
    try:
        doc = folds_doc if folds_doc is not None else rf.load_folds(folds_path, policy_path=policy_path)
        blocks = doc["folds"][fold]
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE, f"config/folds.yaml cannot be used ({type(exc).__name__}: {exc})")
    block_rows = [dict(b) for b in blocks]
    row["fold_blocks"] = [b["label"] for b in block_rows]
    row["confirmation_set"] = ec.set_key(block_rows)
    try:
        proto = {w["label"]: (w["start"], w["end"]) for w in ec.protocol_windows(arts)}
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE,
                       f"the run's protocol windows cannot be read ({type(exc).__name__}: {exc})")
    want = {b["label"]: (b["start"], b["end"]) for b in block_rows}
    if proto != want:
        return _finish(row, NOT_MEASURABLE,
                       f"the run's protocol windows {sorted(proto.items())} are not exactly fold "
                       f"{fold}'s blocks {sorted(want.items())}: the claim is not measured on a "
                       f"fold it was not run on")
    # the variants
    try:
        graded = ct.graded_variants(run_dir)[0]
        base = base_variant or jp.base_variant_id(graded)
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE, f"no graded variant ({type(exc).__name__}: {exc})")
    vehicle_vid = vehicle_variant or base
    row.update({"vehicle_variant": vehicle_vid, "base_variant": base})
    usable = set(graded if fresh_variants is None else fresh_variants) & set(graded)
    if vehicle_vid not in usable:
        return _finish(row, NOT_MEASURABLE,
                       f"the vehicle variant {vehicle_vid!r} was not backtested in this attempt "
                       f"(graded now: {sorted(usable)})")
    # the vehicle must be in the config that was actually measured: step 1b (or anything
    # between decide-next and the backtest) may have changed it, and a claim measured on a
    # strategy without its vehicle is not the claim the run was built for
    vehicle = item.get("vehicle") or item.get("config_change") or []
    if not vehicle:
        # D-089 (a): an empty vehicle claims TODAY's strategy, unchanged: the measured config
        # must be the one decide-next started the child from (candidate.source
        # .start_config_sha256), else step 1b changed it and this is not the claim's strategy
        changed = _start_config_changed(arts, vehicle_vid)
        if changed:
            return _finish(row, NOT_MEASURABLE, f"strategy_changed_since_the_claim: {changed}")
    if vehicle:
        cfg_path = arts / "variants" / vehicle_vid / "strategy_config.json"
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            # D-162: a config vehicle is compared whole (it IS the measured config)
            missing = (config_vehicle_missing(cfg, vehicle) if isinstance(vehicle, dict)
                       else vehicle_missing(cfg, vehicle))
        except Exception as exc:  # noqa: BLE001 -- recorded
            missing = [f"the variant's strategy_config.json cannot be read "
                       f"({type(exc).__name__}: {exc})"]
        if missing:
            row["vehicle_missing"] = missing
            shown = missing
            if isinstance(vehicle, dict) and len(missing) > MAX_CONFIG_DIFFS_SHOWN:
                shown = missing[:MAX_CONFIG_DIFFS_SHOWN] + [
                    f"(+{len(missing) - MAX_CONFIG_DIFFS_SHOWN} more)"]
            return _finish(row, NOT_MEASURABLE,
                           f"vehicle_not_in_measured_config: variant {vehicle_vid!r} does not "
                           f"carry the claim's vehicle: " + "; ".join(shown))
    # the generic measurement, over the fold's windows only
    measure = measure or measure_on_fold
    try:
        results, measured = measure(run_dir, vehicle_vid, tests, [b["label"] for b in block_rows],
                                    eras, holdout_start, **tt)
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE,
                       f"the bars could not be measured ({type(exc).__name__}: {exc})")
    fold_windows = [b["label"] for b in block_rows]           # R5: the count's windows
    graded_tests = {n: grade_test(r, fold_windows) for n, r in sorted(results.items())}
    status, reason = combine(graded_tests)
    row["tests"] = {n: row_test_entry(results[n], g) for n, g in graded_tests.items()}
    row["windows_measured"] = list(measured)
    if any(POOLED_KEY in (x or {}) for r in results.values()
           for x in ((r or {}).get("horizons") or {}).values()):
        row["window_basis"] = "coins_pooled_per_window"      # option C, D-089 (several coins)
    # the numbers every row carries, for any status that measured something
    row["effect"] = {n: {h: x["effect"] for h, x in g.get("horizons", {}).items()}
                     for n, g in graded_tests.items() if g.get("horizons")}
    row["agreement"] = {n: {h: f"{x['windows_claimed_sign']} of {x['windows_in_fold']}"   # R5
                            for h, x in g.get("horizons", {}).items()}
                        for n, g in graded_tests.items() if g.get("horizons")}
    row["_comparisons"] = ec.comparisons_of(results)
    return _finish(row, status, reason)
