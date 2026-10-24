"""
D-185: the structure key of a trial -- (structure_hash, timeframe) -- that
sizes the deflated Sharpe's N by what a trial tested instead of by how many
trials the campaign ran.

structure_hash is the sha256 of a canonical JSON of the strategy config with
every parameter value removed. It records exactly:

  * the regime detector's mode (`regime_detector.mode`, default
    "threshold_rules" as the engine reads it);
  * per regime (dict regimes only; a null or absent regime is not part of the
    structure), in sorted regime-name order -- the engine looks a regime up by
    name, so the order of the regimes in the file is not semantic -- the list
    of its components IN CONFIG ORDER (the spec names the order), each as
    {class, transforms, history_transforms, weight_sign, scaling_factor_sign,
    scale_factor_signs}:
      - class: the component's dotted class string, as written;
      - transforms / history_transforms: the op names in order. Both lists are
        kept, under their own names: standardise and vol_normalize live in
        history_transforms and change what the signal is, and an op moved
        from one list to the other is a different pipeline;
      - weight_sign, scaling_factor_sign: -1 / 0 / +1 of `weight` and of
        `params.scaling_factor`. The magnitudes are parameters and are removed;
        the sign flips the direction of the bet. A missing `weight` is None
        (the engine has no default weight: strategy_engine.py:229 and :613 index
        cfg["weight"], so no ledger row comes from such a config). A missing
        `params.scaling_factor` is +1, not None: every component class defaults
        it to a positive number (strategy_components.py:234-693), so "absent" and
        "explicit positive" are the same strategy and must share a key (D-185
        fix round, direction sign fix). A present non-number stays None;
      - scale_factor_signs: the sign of each `scale` op's `params.factor`, in
        order (a negative factor flips the signal exactly like a negative
        weight or a `negate` op, which are in the hash; absent: the sign of
        the op's default, +1);
  * the sizing kind (`strategies.sizing.kind`, null when there is no block).

Nothing else is in it: no window, lookback, threshold, span, magnitude of a
weight, id or any other parameter value. Two configs that differ only in
parameter values hash identically; that is the point -- they are the same
idea tried again, and the deflated Sharpe's N should count them together.

timeframe is the protocol's own `timeframe` key (default "1h", as
run_protocol.py reads it), written canonically so one bar size has one string:
"1h", "60m" and 3600 are all "1h".

Why none of this can leak: the key is a function of the strategy config and the
protocol's bar size, both fixed before any bar of a run is read; no market data
enters it.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from timeframe import timeframe_seconds  # tools/ sibling

_UNITS = (("w", 604800), ("d", 86400), ("h", 3600), ("m", 60), ("s", 1))
_DEFAULT_REGIME_MODE = "threshold_rules"  # regime_engine.py: config.get("mode", "threshold_rules")
_DEFAULT_PROTOCOL_TIMEFRAME = "1h"  # run_protocol.py: protocol.get("timeframe", "1h")


def _sign(value):
    """-1 / 0 / +1 for a real number, None for anything else (absent, a bool,
    a string, NaN)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return (value > 0) - (value < 0)


def _op_names(steps) -> list:
    if not isinstance(steps, list):
        return []
    return [s.get("op") if isinstance(s, dict) else None for s in steps]


def _scale_signs(steps) -> list:
    out = []
    for s in steps if isinstance(steps, list) else []:
        if isinstance(s, dict) and s.get("op") == "scale":
            params = s.get("params")
            factor = params.get("factor", 1.0) if isinstance(params, dict) else 1.0
            out.append(_sign(factor))
    return out


def structure_dict(config: dict) -> dict:
    """The parameter-free structure the hash is taken over (see the module
    docstring). Raises ValueError when `config` is not a mapping."""
    if not isinstance(config, dict):
        raise ValueError(f"structure_hash: config must be a mapping, got {type(config).__name__}")
    detector = config.get("regime_detector")
    mode = detector.get("mode", _DEFAULT_REGIME_MODE) if isinstance(detector, dict) \
        else _DEFAULT_REGIME_MODE
    strategies = config.get("strategies")
    strategies = strategies if isinstance(strategies, dict) else {}
    regimes = strategies.get("regimes")
    regimes = regimes if isinstance(regimes, dict) else {}
    out_regimes = {}
    for name in sorted(regimes, key=str):
        rcfg = regimes[name]
        if not isinstance(rcfg, dict):
            continue
        comps = []
        for c in rcfg.get("components") or []:
            c = c if isinstance(c, dict) else {}
            params = c.get("params")
            params = params if isinstance(params, dict) else {}
            comps.append({
                "class": c.get("class"),
                "transforms": _op_names(c.get("transforms")),
                "history_transforms": _op_names(c.get("history_transforms")),
                "weight_sign": _sign(c.get("weight")),
                "scaling_factor_sign": (_sign(params["scaling_factor"])
                                        if "scaling_factor" in params else 1),
                "scale_factor_signs": (_scale_signs(c.get("transforms"))
                                       + _scale_signs(c.get("history_transforms"))),
            })
        out_regimes[str(name)] = comps
    sizing = strategies.get("sizing")
    return {"regime_detector_mode": mode, "regimes": out_regimes,
            "sizing_kind": sizing.get("kind") if isinstance(sizing, dict) else None}


def compute_structure_hash(config: dict) -> str:
    """sha256 hex of the canonical JSON (sorted keys, no whitespace variance) of
    structure_dict(config)."""
    canonical = json.dumps(structure_dict(config), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def canonical_timeframe(timeframe) -> str | None:
    """The one string for a bar size: seconds -> the largest of w/d/h/m/s that
    divides it evenly ("1h", "60m" and 3600 -> "1h"; "90m" -> "90m"). None for
    anything timeframe_seconds refuses."""
    try:
        seconds = timeframe_seconds(timeframe)
    except ValueError:
        return None
    if seconds <= 0:
        return None
    for unit, size in _UNITS:
        if seconds % size == 0:
            return f"{seconds // size}{unit}"
    return None  # unreachable: size 1 divides every integer


def protocol_timeframe(protocol: dict) -> str | None:
    """The canonical timeframe of a parsed protocol (its `timeframe` key,
    default "1h" when the key is absent); None when the value is unparseable
    or `protocol` is not a mapping."""
    if not isinstance(protocol, dict):
        return None
    return canonical_timeframe(protocol.get("timeframe", _DEFAULT_PROTOCOL_TIMEFRAME))


def read_protocol_timeframe(path) -> str | None:
    """protocol_timeframe of the JSON or YAML protocol file at `path`. Reads the
    file for its `timeframe` key only and returns nothing else of it. None when
    the file is missing or unreadable."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
        if p.suffix.lower() in (".yaml", ".yml"):
            import yaml
            doc = yaml.safe_load(text)
        else:
            doc = json.loads(text)
    except Exception:  # noqa: BLE001 -- an unreadable protocol leaves the row unkeyed
        return None
    return protocol_timeframe(doc)


def structure_hash_of_file(config_path) -> str | None:
    """compute_structure_hash of the JSON config at `config_path`; None when the
    file is missing or not a JSON mapping (the row is then left unkeyed)."""
    try:
        return compute_structure_hash(json.loads(Path(config_path).read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001
        return None


def row_structure_key(row) -> tuple | None:
    """(structure_hash, canonical timeframe) of a ledger row, or None when the row
    is unkeyed (either field absent or None). The timeframe is re-canonicalised
    ("60m" -> "1h"), so a hand-written value cannot split a key. A malformed
    field raises ValueError, as the dedupe keys do: a hash that is not a 64-char
    lowercase hex digest, a timeframe that is not a parseable bar-size string."""
    h, tf = row.get("structure_hash"), row.get("timeframe")
    if h is None or tf is None:
        return None
    if not (isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h)):
        raise ValueError(f"trial {row.get('trial_id')!r}: structure_hash {h!r} is not a sha256 "
                         f"hex digest (D-185)")
    canonical = canonical_timeframe(tf) if isinstance(tf, str) else None
    if canonical is None:
        raise ValueError(f"trial {row.get('trial_id')!r}: timeframe {tf!r} is not a parseable "
                         f"bar size string such as '1h' (D-185)")
    return (h, canonical)  # a hand-written "60m" and a written "1h" are one key


# ---------------------------------------------------------------------------
# The backfill overlay: campaign_record/trial_structure_key_overlay.yaml
#
# Append-only, deterministic (no timestamps, so two writers appending the same
# row append the same bytes), exact keys. It keys ledger rows written BEFORE
# D-185 from the config saved in their run's artifacts and the run's protocol
# timeframe (tools/backfill_structure_hash.py). It never edits the ledger: the
# DSR context reads it beside the rows (apply_structure_overlay) under
# orchestrator.dsr_same_structure.
# ---------------------------------------------------------------------------

OVERLAY_KEYS = frozenset({"trial_id", "source", "structure_hash", "timeframe",
                          "config_sha256", "config_ref", "forecast_hash_check"})
# forecast_hash_check (D-185 note, direction 2026-10-24): "match" when the ledger row's
# forecast_hash equals the saved config's, so the config is the one the trial tested;
# "row_has_no_forecast_hash" when the legacy row carries none, so the saved config is the
# run's config but cannot be checked against the trial (the dry run's "keyed_unverified").
FORECAST_HASH_CHECKS = frozenset({"match", "row_has_no_forecast_hash"})
_HEX = frozenset("0123456789abcdef")


def _is_sha(x) -> bool:
    return isinstance(x, str) and len(x) == 64 and set(x) <= _HEX


def validate_structure_overlay(data) -> dict:
    """Validate the parsed overlay YAML and index it: None / empty -> {}; else
    {"entries": [entry, ...]} with every entry holding exactly OVERLAY_KEYS
    (trial_id, source, config_ref, timeframe non-empty strings; structure_hash
    and config_sha256 sha256 hex digests; forecast_hash_check one of
    FORECAST_HASH_CHECKS). The same (trial_id, source) twice is
    kept once when the entries are equal and raises when they differ. Returns
    {(trial_id, source): entry}."""
    if data is None:
        return {}
    if not isinstance(data, dict) or set(data) - {"entries"}:
        raise ValueError(f"structure overlay: top level must be a mapping with only 'entries', "
                         f"got {str(data)[:200]!r}")
    entries = data.get("entries")
    if entries is None:
        return {}
    if not isinstance(entries, list):
        raise ValueError("structure overlay: 'entries' is not a list")
    index: dict = {}
    for i, e in enumerate(entries):
        what = f"structure overlay entry {i}"
        if not isinstance(e, dict) or set(e) != OVERLAY_KEYS:
            raise ValueError(f"{what}: keys must be exactly {sorted(OVERLAY_KEYS)}, got "
                             f"{sorted(e) if isinstance(e, dict) else e!r}")
        for f in ("trial_id", "source", "timeframe", "config_ref"):
            if not isinstance(e[f], str) or not e[f]:
                raise ValueError(f"{what}: {f} {e[f]!r} is not a non-empty string")
        for f in ("structure_hash", "config_sha256"):
            if not _is_sha(e[f]):
                raise ValueError(f"{what}: {f} {e[f]!r} is not a sha256 hex digest")
        if e["forecast_hash_check"] not in FORECAST_HASH_CHECKS:
            raise ValueError(f"{what}: forecast_hash_check {e['forecast_hash_check']!r} is not one "
                             f"of {sorted(FORECAST_HASH_CHECKS)}")
        key = (e["trial_id"], e["source"])
        if key in index:
            if index[key] != e:
                raise ValueError(f"structure overlay: two different entries for {key} -- the "
                                 f"overlay is append-only with deterministic entries; refused")
            continue
        index[key] = dict(e)
    return index


def load_structure_overlay(path) -> dict:
    """Parse and validate the overlay file; a missing file is an empty overlay."""
    import yaml
    p = Path(path)
    if not p.exists():
        return {}
    return validate_structure_overlay(yaml.safe_load(p.read_text(encoding="utf-8")))


def apply_structure_overlay(rows: list, index: dict) -> list:
    """The ledger rows with the overlay's key added to every row that carries none
    of its own: a shallow COPY of such a row gets structure_hash and timeframe;
    every other row is returned as is (the ledger is never mutated). A row with
    a native key (either field) keeps it and is never overwritten: a native
    structure_hash or timeframe that differs from the overlay's raises. An
    overlay entry for a (trial_id, source) absent from the ledger raises (the
    ledger is behind the overlay: not merged), as the basis overlay does."""
    present = {(r.get("trial_id"), r.get("source")) for r in rows if isinstance(r, dict)}
    orphans = sorted(str(k) for k in index if k not in present)
    if orphans:
        raise ValueError(f"structure overlay: entries for rows absent from the ledger: "
                         f"{orphans} -- the ledger is not merged; refused")
    out = []
    for r in rows:
        e = index.get((r.get("trial_id"), r.get("source"))) if isinstance(r, dict) else None
        if e is None:
            out.append(r)
            continue
        for f in ("structure_hash", "timeframe"):
            if r.get(f) is not None and r[f] != e[f]:
                raise ValueError(f"structure overlay: ledger row ({r.get('trial_id')!r}, "
                                 f"{r.get('source')!r}) has {f} {r[f]!r}, the overlay {e[f]!r}")
        if r.get("structure_hash") is None and r.get("timeframe") is None:
            out.append({**r, "structure_hash": e["structure_hash"], "timeframe": e["timeframe"]})
        else:
            out.append(r)  # a native key (possibly half of one) is never completed from the overlay
    return out


def run_protocol_timeframe(root, run_id: str) -> str | None:
    """The canonical timeframe of the protocol `run_id` ran on, read from `root`
    (the strategy-research directory) without resolving or generating anything:
    protocols/<run_id>_generated.json, else the file named by
    runs/<run_id>/artifacts/pre_registration.yaml machine_constraints.protocol_ref,
    else that file's machine_constraints.protocol.timeframe. Only the
    `timeframe` key is read. None when none is readable."""
    import yaml
    root = Path(root)
    tf = read_protocol_timeframe(root / "protocols" / f"{run_id}_generated.json")
    if tf is not None:
        return tf
    pre = root / "runs" / run_id / "artifacts" / "pre_registration.yaml"
    try:
        mc = (yaml.safe_load(pre.read_text(encoding="utf-8")) or {}).get("machine_constraints") or {}
    except Exception:  # noqa: BLE001
        return None
    ref = mc.get("protocol_ref") if isinstance(mc, dict) else None
    if isinstance(ref, str) and ref:
        tf = read_protocol_timeframe(root / ref)
        if tf is not None:
            return tf
    proto = mc.get("protocol") if isinstance(mc, dict) else None
    if isinstance(proto, dict):
        return protocol_timeframe(proto)
    return None
