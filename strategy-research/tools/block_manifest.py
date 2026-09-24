"""
artifacts/block_manifest.yaml -- the ONE implementation of the manifest
contract (docs/STRATEGY_DESIGN_GUIDE.md §7c; E-056 1b block-manifest ticket).

The manifest says which part of a run's base strategy config IS the idea's
block, as opposed to scaffolding. Stage 1b (strategy_config_authoring,
config-direct-authoring flow only) writes it next to the config; two readers
check it with the functions below and nothing else:

  * run_phase1_research's tool-only backtest_specification stage (5a) --
    against the base config 1b wrote, before any variant is built;
  * tools/block_registry.py -- against the tested base config, when a
    validated run registers its block.

A manifest valid for one is valid for the other: both call `check_manifest`
(shape + every pointer resolves) on the same base config (5a's `base`
variant is the registry's base variant, see tools/json_pointer.base_variant_id).
workflow_artifacts/schemas/block_manifest.schema.json documents the same
shape; tests/test_e056_1b_block_manifest.py keeps the schema and this module
in agreement.

Contract (every key required, no other key allowed):

    block:
      kind: forecast | regime
      config_paths: [<JSON pointer>, ...]   # non-empty; the block's config pieces
    scaffolding: [<JSON pointer>, ...]      # may be empty; config the idea needs
                                            # to run but that is not the idea
    rationale: <non-empty string>           # why these paths are the block

Rules beyond the shape:
  * every pointer is RFC 6901 ('/'-prefixed; tools/json_pointer.py) and
    resolves in the base config -- block AND scaffolding;
  * no pointer appears twice, and no pointer lies inside another one's
    subtree (block vs block, block vs scaffolding, scaffolding vs
    scaffolding): each config piece is listed once, as block or scaffolding;
  * kind `forecast` -> at least one block path strictly inside a named
    regime, /strategies/regimes/<name>[/...];
    kind `regime`   -> at least one block path at or under /regime_detector.
    Both are read off `regime_assignment` below -- the same function
    tools/block_registry.py stores as the block's regime_assignment.

Deliberately absent: a coin/symbol/instrument restriction (a validated block
is usable on any coin, card F), `hypothesis_id` (the registry takes the idea's
identity from the run's memory entry -- a second copy could only disagree),
and every retired field (hypothesis_family, refine/pivot/escalate/kill).
"""
from __future__ import annotations

from pathlib import Path

import yaml

import json_pointer as _jp  # tools/ sibling

MANIFEST_FILENAME = "block_manifest.yaml"
MANIFEST_KINDS = ("forecast", "regime")
MANIFEST_KEYS = ("block", "scaffolding", "rationale")
BLOCK_KEYS = ("kind", "config_paths")
# kind -> the regime_assignment() key at least one block path must land in.
KIND_ASSIGNMENT_KEY = {"forecast": "regimes", "regime": "detector_paths"}


class BlockManifestError(ValueError):
    """A malformed manifest, or one whose pointers do not resolve."""


def _is_pointer(p) -> bool:
    try:
        _jp.split_json_pointer(p)
    except _jp.JsonPointerError:
        return False
    return True


def _segments(p: str) -> tuple:
    return tuple(_jp.split_json_pointer(p))


def _nested(a: str, b: str) -> bool:
    """True when a == b or one pointer's subtree contains the other."""
    sa, sb = _segments(a), _segments(b)
    n = min(len(sa), len(sb))
    return sa[:n] == sb[:n]


def regime_assignment(paths: list) -> dict:
    """Derived from the pointer paths only: /strategies/regimes/<name>[/...]
    -> <name> (a bare /strategies/regimes names no regime); a regime block's
    detector pieces are the paths at or under /regime_detector. Stored by
    tools/block_registry.py as the block's regime_assignment and used for the
    kind rule in validate_manifest, so the two can never disagree."""
    regimes = sorted({p.split("/")[3].replace("~1", "/").replace("~0", "~")
                      for p in paths if p.startswith("/strategies/regimes/") and len(p.split("/")) > 3})
    detector = sorted(p for p in paths if p == "/regime_detector" or p.startswith("/regime_detector/"))
    return {"regimes": regimes, "detector_paths": detector}


def validate_manifest(doc, where: str = MANIFEST_FILENAME, error_cls=BlockManifestError) -> dict:
    """Shape check (no config needed). Returns `doc`; raises `error_cls`."""
    if not isinstance(doc, dict) or not isinstance(doc.get("block"), dict):
        raise error_cls(f"{where}: expected {{block: {{kind, config_paths}}, scaffolding, "
                        f"rationale}}, got {doc!r}")
    missing = [k for k in MANIFEST_KEYS if k not in doc]
    extra = sorted(str(k) for k in set(doc) - set(MANIFEST_KEYS))
    if missing or extra:
        raise error_cls(f"{where}: manifest keys missing {missing} / unknown {extra} "
                        f"(allowed: {list(MANIFEST_KEYS)})")
    block = doc["block"]
    b_missing = [k for k in BLOCK_KEYS if k not in block]
    b_extra = sorted(str(k) for k in set(block) - set(BLOCK_KEYS))
    if b_missing or b_extra:
        raise error_cls(f"{where}: block keys missing {b_missing} / unknown {b_extra} "
                        f"(allowed: {list(BLOCK_KEYS)})")
    kind = block["kind"]
    if kind not in MANIFEST_KINDS:
        raise error_cls(f"{where}: block.kind={kind!r} not one of {MANIFEST_KINDS}")
    paths = block["config_paths"]
    if (not isinstance(paths, list) or not paths
            or not all(_is_pointer(p) for p in paths) or len(set(paths)) != len(paths)):
        raise error_cls(f"{where}: block.config_paths must be a non-empty list of distinct "
                        f"JSON pointers ('/...'), got {paths!r}")
    scaffolding = doc["scaffolding"]
    if (not isinstance(scaffolding, list) or not all(_is_pointer(p) for p in scaffolding)
            or len(set(scaffolding)) != len(scaffolding)):
        raise error_cls(f"{where}: scaffolding must be a list (possibly empty) of distinct "
                        f"JSON pointers ('/...'), got {scaffolding!r}")
    rationale = doc["rationale"]
    if not isinstance(rationale, str) or not rationale.strip():
        raise error_cls(f"{where}: rationale must be a non-empty string, got {rationale!r}")
    for i, a in enumerate(paths):
        for b in paths[i + 1:]:
            if _nested(a, b):
                raise error_cls(f"{where}: block.config_paths {a!r} and {b!r} overlap -- list "
                                f"each config piece once")
        for s in scaffolding:
            if _nested(a, s):
                raise error_cls(f"{where}: block path {a!r} and scaffolding path {s!r} overlap "
                                f"-- a config piece is either block or scaffolding, not both")
    for i, a in enumerate(scaffolding):
        for b in scaffolding[i + 1:]:
            if _nested(a, b):
                raise error_cls(f"{where}: scaffolding paths {a!r} and {b!r} overlap -- list "
                                f"each config piece once")
    if not regime_assignment(paths)[KIND_ASSIGNMENT_KEY[kind]]:
        need = ("strictly inside a named regime (/strategies/regimes/<name>[/...])"
                if kind == "forecast" else "at or under /regime_detector")
        raise error_cls(f"{where}: a {kind!r} block needs at least one config_path {need}, "
                        f"got {paths!r}")
    return doc


def unresolved_paths(config, manifest: dict) -> list:
    """Block and scaffolding pointers that do NOT resolve in `config`
    (a shape-valid manifest is assumed). Checked against the base config by
    5a and by the registry. Per variant, 5a checks only the BLOCK paths
    (json_pointer.manifest_missing_paths): a variant may change scaffolding."""
    return _jp.manifest_missing_paths(config, manifest) + [
        p for p in manifest["scaffolding"] if not _jp.json_pointer_exists(config, p)]


def check_manifest(doc, config, where: str = MANIFEST_FILENAME,
                   error_cls=BlockManifestError) -> dict:
    """validate_manifest + every pointer resolves in `config`. Returns `doc`."""
    validate_manifest(doc, where, error_cls)
    missing = unresolved_paths(config, doc)
    if missing:
        raise error_cls(f"{where}: manifest path(s) {missing} do not resolve in the base config")
    return doc


def load_manifest_file(path: Path, error_cls=BlockManifestError):
    """Strict read: None when the file is absent; unparseable YAML or a bad
    shape raises `error_cls`. No LLM-output repair -- a manifest that needs
    repairing is a malformed manifest."""
    path = Path(path)
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise error_cls(f"{path}: unparseable YAML ({exc})") from exc
    return validate_manifest(doc, str(path), error_cls)
