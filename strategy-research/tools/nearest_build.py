"""
E-068 (operator, 2026-10-05): step 1b builds the nearest version of an idea
instead of parking it, under orchestrator.nearest_build.enabled (off by
default; requires config_direct_authoring, the flow 1b runs in).

When a clause of the idea cannot be built exactly, 1b builds the closest
config the catalogue's components and transforms allow, answers spec_ready,
and lists each difference in decision.yaml `deviations` (clause, built_instead,
missing, effect) -- the `DEVIATION:` lines of backtest_spec.yaml's
config_rationale stay as well. It answers component_gap only when nothing it
can build keeps the claim's core, with `core_lost` naming the claim clause that
cannot be approximated and why (what it tried is the O-21 `tried` list).

This module is pure (no orchestrator state): it parses those answers into
artifacts/deviations.yaml, builds the component-request rows for the missing
pieces (kind `deviation`: they never feed --unpark, the quarantine cap or
decide-next's request count), and the prominent "approximation" block the
finding, the readers' digest and the findings summary show first.
INFORMATION ONLY: nothing here stops, parks or reroutes a run.
"""
from __future__ import annotations

from pathlib import Path

import yaml

DEVIATIONS_FILE = "deviations.yaml"
SCHEMA_VERSION = 1
STATUS_APPROXIMATION = "approximation"   # spec_ready with at least one deviation
STATUS_EXACT = "exact"                   # spec_ready, nothing deviates
STATUS_PARKED = "parked"                 # component_gap: the core could not be kept
REQUEST_KIND = "deviation"
DEVIATION_PREFIX = "DEVIATION:"
APPROX_LINE = "this run tested an approximation of the idea: "
_ITEM_KEYS = ("clause", "built_instead", "missing", "effect")
# Review round 1: 1b's answer is model-written and lands in campaign memory, the
# readers' prompts and component_requests.yaml -- bounded here, once.
MAX_ITEMS = 10
MAX_CHARS = 300


def _text(v) -> str | None:
    if v is None:
        return None
    s = " ".join(str(v).split())
    if len(s) > MAX_CHARS:
        s = s[:MAX_CHARS - 3] + "..."
    return s or None


def _deviation_items(decision) -> list:
    raw = decision.get("deviations") if isinstance(decision, dict) else None
    out = []
    for item in raw if isinstance(raw, list) else []:
        if isinstance(item, dict):
            row = {k: _text(item.get(k)) for k in _ITEM_KEYS}
        else:
            row = {"clause": _text(item), "built_instead": None, "missing": None, "effect": None}
        if any(row.values()):
            out.append(row)
    return out


def structured_deviations(decision) -> list:
    """decision.yaml `deviations`, normalised to {clause, built_instead, missing,
    effect} (strings or None, each at most MAX_CHARS); anything that is not a
    mapping is kept as a clause. At most MAX_ITEMS (build_record counts the rest)."""
    return _deviation_items(decision)[:MAX_ITEMS]


def rationale_deviation_lines(backtest_spec) -> list:
    """The config_rationale entries whose config_choice starts with DEVIATION:
    (the O-7 fidelity rule), as {clause, text}; at most MAX_ITEMS."""
    return _all_rationale_lines(backtest_spec)[:MAX_ITEMS]


def _all_rationale_lines(backtest_spec) -> list:
    rationale = backtest_spec.get("config_rationale") if isinstance(backtest_spec, dict) else None
    out = []
    for entry in rationale if isinstance(rationale, list) else []:
        if not isinstance(entry, dict):
            continue
        choice = _text(entry.get("config_choice"))
        if choice and choice.upper().startswith(DEVIATION_PREFIX):
            out.append({"clause": _text(entry.get("hypothesis_claim")),
                        "text": _text(choice[len(DEVIATION_PREFIX):])})
    return out


def core_lost_problem(decision) -> str | None:
    """None when a component_gap names the claim clause that cannot be
    approximated and why (`core_lost: {clause, why}`); else the retry message."""
    core = decision.get("core_lost") if isinstance(decision, dict) else None
    if isinstance(core, dict) and _text(core.get("clause")) and _text(core.get("why")):
        return None
    return ("component_gap without `core_lost`: under orchestrator.nearest_build you build the "
            "nearest version of the idea (spec_ready, each difference listed in decision.yaml "
            "`deviations`). Answer component_gap only when nothing you can build keeps the "
            "claim's core, and then name it: `core_lost: {clause: <the claim clause that cannot "
            "be approximated>, why: <why no composition approximates it>}` (what you tried stays "
            "in `tried`)")


def core_lost_of(decision) -> dict | None:
    core = decision.get("core_lost") if isinstance(decision, dict) else None
    if not isinstance(core, dict):
        return None
    out = {"clause": _text(core.get("clause")), "why": _text(core.get("why"))}
    return out if any(out.values()) else None


def build_record(run_id: str, decision, backtest_spec) -> dict:
    """artifacts/deviations.yaml's content for 1b's answer."""
    status = str((decision or {}).get("status") or "").strip().lower()
    items = structured_deviations(decision)
    lines = rationale_deviation_lines(backtest_spec)
    if status == "component_gap":
        state = STATUS_PARKED
    else:
        state = STATUS_APPROXIMATION if (items or lines) else STATUS_EXACT
    rec = {"schema_version": SCHEMA_VERSION, "run_id": run_id, "status": state,
           "information_only": True, "deviations": items, "config_rationale_lines": lines}
    # Beyond MAX_ITEMS: counted for whichever list the approximation block shows
    # (the structured items when 1b wrote any, else the DEVIATION: lines).
    dropped = (len(_deviation_items(decision)) - len(items) if items
               else len(_all_rationale_lines(backtest_spec)) - len(lines))
    if dropped > 0:
        rec["deviations_not_listed"] = dropped
    if state == STATUS_PARKED:
        rec["core_lost"] = core_lost_of(decision)
        rec["tried"] = (decision or {}).get("tried") or []
    return rec


def approximation_block(record) -> dict | None:
    """The prominent block shown FIRST in the finding and the readers' digest,
    or None when the run tested the idea as written (or nothing is recorded)."""
    if not isinstance(record, dict) or record.get("status") != STATUS_APPROXIMATION:
        return None
    items = record.get("deviations") or []
    if items:
        parts = [f"{i.get('clause') or '(clause not named)'} -> "
                 f"{i.get('built_instead') or '(not built)'}" for i in items]
        compact = [{k: i.get(k) for k in _ITEM_KEYS} for i in items]
    else:
        lines = record.get("config_rationale_lines") or []
        parts = [f"{ln.get('clause') or '(clause not named)'} -> {ln.get('text') or ''}"
                 for ln in lines]
        compact = [{"clause": ln.get("clause"), "built_instead": ln.get("text"),
                    "missing": None, "effect": None} for ln in lines]
    if not parts:
        return None
    more = record.get("deviations_not_listed") or 0
    line = APPROX_LINE + "; ".join(parts) + (f"; and {more} more (not listed)" if more else "")
    return {"line": line, "n_deviations": len(parts) + more,
            "deviations": compact, "ref": f"artifacts/{DEVIATIONS_FILE}"}


def load_record(arts: Path):
    """deviations.yaml or None (absent, unreadable or not a mapping)."""
    path = Path(arts) / DEVIATIONS_FILE
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) else None


def request_rows(run_id: str, record) -> list:
    """One component-request row per deviation that names a missing piece,
    marked kind `deviation` / run_continued (never an --unpark or cap input)."""
    if not isinstance(record, dict) or record.get("status") != STATUS_APPROXIMATION:
        return []
    rows = []
    for item in record.get("deviations") or []:
        missing = item.get("missing")
        if not missing:
            continue
        rows.append({"run_id": run_id, "stage": "strategy_config_authoring", "variant_id": None,
                     "kind": REQUEST_KIND, "run_continued": True,
                     "reason": f"deviation: {missing}", "clause": item.get("clause"),
                     "built_instead": item.get("built_instead")})
    return rows


def is_deviation_row(row) -> bool:
    return isinstance(row, dict) and row.get("kind") == REQUEST_KIND


# ---------------------------------------------------------------------------
# CUL-412 (operator, 2026-10-06): a reader's side finding starts 1b from the
# source run's config. Code compares what 1b built with that start, so every
# change is a structured deviation even when 1b does not list it.
# ---------------------------------------------------------------------------
START_CONFIG_FILE = "start_config.json"
START_MANIFEST_FILE = "start_block_manifest.yaml"
START_DIFF_SOURCE = "code_diff_from_start_config"


def _pointer_escape(key) -> str:
    return str(key).replace("~", "~0").replace("/", "~1")


def config_diff(old, new, path: str = "") -> list:
    """Every leaf that differs between two JSON configs, as {path, before,
    after} (JSON pointers; `before`/`after` None for an added/removed key). A
    list whose length changed is one changed leaf (its whole value). Pure."""
    if isinstance(old, dict) and isinstance(new, dict):
        out = []
        for k in sorted(set(old) | set(new), key=str):
            p = f"{path}/{_pointer_escape(k)}"
            if k not in old:
                out.append({"path": p, "before": None, "after": new[k]})
            elif k not in new:
                out.append({"path": p, "before": old[k], "after": None})
            else:
                out += config_diff(old[k], new[k], p)
        return out
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        out = []
        for i, (a, b) in enumerate(zip(old, new)):
            out += config_diff(a, b, f"{path}/{i}")
        return out
    return [] if old == new else [{"path": path or "/", "before": old, "after": new}]


def _short(v) -> str:
    return _text(repr(v)) or "None"


def start_deviation_items(start_config, built_config, start_manifest, built_manifest) -> list:
    """The deviations from the start config, as D-075 items (clause,
    built_instead, missing: None, effect) tagged `source`: one per changed
    leaf, plus one when the block manifest's block or scaffolding changed."""
    effect = ("1b changed the block the claim is about (CUL-412); the claim's tests measure "
              "the config as built")
    items = []
    for d in config_diff(start_config, built_config):
        items.append({"clause": _text(f"the source config at {d['path']}"),
                      "built_instead": _text(f"{_short(d['before'])} -> {_short(d['after'])}"),
                      "missing": None, "effect": effect, "source": START_DIFF_SOURCE})
    if isinstance(start_manifest, dict) and isinstance(built_manifest, dict):
        for key in ("block", "scaffolding"):
            if start_manifest.get(key) != built_manifest.get(key):
                items.append({"clause": _text(f"the source block manifest's {key}"),
                              "built_instead": _text(f"{_short(start_manifest.get(key))} -> "
                                                     f"{_short(built_manifest.get(key))}"),
                              "missing": None, "effect": effect, "source": START_DIFF_SOURCE})
    return items


def merge_start_deviations(record, run_id: str, items: list) -> dict:
    """deviations.yaml's content with the start-config items added (to an
    existing nearest-build record, or a new one). Items beyond MAX_ITEMS are
    counted in `deviations_not_listed`; an empty `items` list leaves the
    record as it is (or an `exact` record when there was none). Idempotent:
    earlier start items are replaced, never repeated. Review: when 1b wrote
    only `DEVIATION:` rationale lines, they become items first, so the
    approximation block (which shows the items when there are any) still
    shows them."""
    rec = dict(record) if isinstance(record, dict) else {
        "schema_version": SCHEMA_VERSION, "run_id": run_id, "status": STATUS_EXACT,
        "information_only": True, "deviations": [], "config_rationale_lines": []}
    have = [i for i in rec.get("deviations") or []
            if not (isinstance(i, dict) and i.get("source") == START_DIFF_SOURCE)]
    if not items:
        if have != list(rec.get("deviations") or []):
            rec["deviations"] = have
        return rec
    if not have:
        have = [{"clause": ln.get("clause"), "built_instead": ln.get("text"), "missing": None,
                 "effect": None, "source": "config_rationale_line"}
                for ln in rec.get("config_rationale_lines") or [] if isinstance(ln, dict)]
    room = max(0, MAX_ITEMS - len(have))
    rec["deviations"] = have + items[:room]
    dropped = len(items) - min(len(items), room)
    if dropped:
        rec["deviations_not_listed"] = (rec.get("deviations_not_listed") or 0) + dropped
    if rec.get("status") != STATUS_PARKED:
        rec["status"] = STATUS_APPROXIMATION
    return rec
