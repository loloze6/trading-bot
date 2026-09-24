"""
Shared RFC 6901 JSON-pointer and variant helpers (E-058 S2b code-review fix 10).

Moved here, behaviour-preserving, from workflow/run_phase1_research.py
(`_split_json_pointer`, `_json_pointer_exists`, `_check_manifest_paths`, and
protocol_execution's base-variant choice), so tools/block_registry.py reads a
block_manifest.yaml's pointers with exactly the code the orchestrator uses to
check them. run_phase1_research keeps its private names as thin wrappers.

E-059 S2a moved the patch applier here too (`apply_json_pointer_patch`, was
run_phase1_research._apply_json_pointer_patch, and `PatchApplicationError`),
behaviour-preserving, so tools/decide_next.py resolves a reader patch with the
same set semantics 5a applies a variant patch with, without importing the
orchestrator. run_phase1_research re-exports the same exception class and
keeps `_apply_json_pointer_patch` as a thin wrapper.

block_manifest.yaml loading and its contract live in tools/block_manifest.py
(E-056 1b block manifest), shared by the orchestrator's backtest_specification
tool stage and tools/block_registry.py -- both load it strictly and raise on a
malformed or unresolved manifest.
"""
from __future__ import annotations


import copy as _copy


class JsonPointerError(ValueError):
    """An invalid JSON pointer, or one that does not resolve."""


class PatchApplicationError(Exception):
    """Raised by apply_json_pointer_patch on any patch that cannot be
    applied cleanly -- never silently no-opped, per this project's own
    'fail loud, not flattering' rule."""


def split_json_pointer(path, error_cls=JsonPointerError) -> list:
    """RFC 6901 tokenization: '/' splits, '~1' -> '/' and '~0' -> '~' unescaped
    per segment. Raises `error_cls` on anything that isn't a non-empty string
    starting with '/'."""
    if not path or not isinstance(path, str) or not path.startswith("/"):
        raise error_cls(
            f"'{path!r}' is not a valid JSON Pointer -- must be a non-empty string starting with '/'"
        )
    segments = [seg.replace("~1", "/").replace("~0", "~") for seg in path.split("/")[1:]]
    if not segments:
        raise error_cls(f"'{path}' has no segments after the leading '/'")
    return segments


def _walk(config, segments):
    """(True, value) when every segment resolves, else (False, None)."""
    node = config
    for seg in segments:
        if isinstance(node, dict):
            if seg not in node:
                return False, None
            node = node[seg]
        elif isinstance(node, list):
            try:
                idx = int(seg)
            except ValueError:
                return False, None
            if not (0 <= idx < len(node)):
                return False, None
            node = node[idx]
        else:
            return False, None
    return True, node


def json_pointer_exists(config, path) -> bool:
    """True iff the RFC 6901 pointer 'path' resolves inside config. Never
    raises -- an invalid pointer simply does not exist."""
    try:
        segments = split_json_pointer(path)
    except JsonPointerError:
        return False
    return _walk(config, segments)[0]


def resolve_json_pointer(config, path):
    """The value at `path`. Raises JsonPointerError when it is invalid or does
    not resolve (same resolution rules as json_pointer_exists)."""
    found, value = _walk(config, split_json_pointer(path))
    if not found:
        raise JsonPointerError(f"{path!r} does not resolve")
    return value


def manifest_missing_paths(variant_config: dict, manifest) -> list:
    """The manifest-declared block.config_paths (STRATEGY_DESIGN_GUIDE.md
    §7c) that do NOT resolve in variant_config; [] when the manifest has no
    block.config_paths list at all. Block paths only: a variant may change
    scaffolding. tools/block_manifest.unresolved_paths adds scaffolding for
    the base-config check."""
    config_paths = ((manifest or {}).get("block") or {}).get("config_paths") or []
    return [p for p in config_paths if not json_pointer_exists(variant_config, p)]


def base_variant_id(variant_ids) -> str:
    """protocol_execution's base-variant choice: `base` when present, else the
    first id in sorted order. Raises on an empty collection."""
    ids = list(variant_ids)
    if not ids:
        raise ValueError("base_variant_id: no variant ids")
    return "base" if "base" in ids else sorted(ids)[0]


def apply_json_pointer_patch(base_config: dict, patch: list) -> dict:
    """Apply a list of {path, value} JSON-Pointer (RFC 6901) set-operations to
    a DEEP COPY of base_config (base_config itself is never mutated -- every
    variant patches from the same pristine base), returning the patched copy.

    Semantics (E-056 Slice 3b, deliberately chosen): a patch entry SETS the
    value at 'path'. The path's PARENT container must already exist in the
    config -- a patch targeting a path whose parent doesn't exist RAISES
    PatchApplicationError; it never silently creates a new nested chain of
    dicts and never silently no-ops. Only the FINAL segment of a path may be
    new (adding a key that doesn't exist yet under an EXISTING parent dict, or
    appending to a list via the RFC 6901 '-' token). A list segment must be a
    base-10 integer index in range, or (for the final segment only) the
    literal '-'; anything else raises."""
    result = _copy.deepcopy(base_config)
    for i, op in enumerate(patch):
        # CODE-REVIEW FIX (2026-09-21): a malformed patch entry that isn't a
        # dict at all (an LLM authoring slip, e.g. `patch: [21]`) must raise
        # PatchApplicationError, not a bare TypeError, so the caller marks just
        # this one variant not_tested instead of crashing the whole stage.
        if not isinstance(op, dict):
            raise PatchApplicationError(
                f"patch[{i}]: expected a mapping with 'path'/'value' keys, got "
                f"{type(op).__name__} ({op!r})"
            )
        path = op.get("path")
        if "value" not in op:
            raise PatchApplicationError(f"patch[{i}] ({path}): missing required 'value' key")
        segments = split_json_pointer(path, PatchApplicationError)
        parent = result
        for seg in segments[:-1]:
            if isinstance(parent, dict):
                if seg not in parent:
                    raise PatchApplicationError(
                        f"patch[{i}] ({path}): parent segment '{seg}' does not exist in the base "
                        "config -- a patch may only set a NEW leaf key under an EXISTING parent, "
                        "never create a new nested chain."
                    )
                parent = parent[seg]
            elif isinstance(parent, list):
                try:
                    idx = int(seg)
                except ValueError:
                    raise PatchApplicationError(f"patch[{i}] ({path}): '{seg}' is not a valid list index")
                if not (0 <= idx < len(parent)):
                    raise PatchApplicationError(
                        f"patch[{i}] ({path}): list index {idx} out of range (len={len(parent)})"
                    )
                parent = parent[idx]
            else:
                raise PatchApplicationError(
                    f"patch[{i}] ({path}): cannot descend into a {type(parent).__name__} at segment '{seg}'"
                )
        leaf = segments[-1]
        if isinstance(parent, dict):
            parent[leaf] = op["value"]
        elif isinstance(parent, list):
            if leaf == "-":
                parent.append(op["value"])
            else:
                try:
                    idx = int(leaf)
                except ValueError:
                    raise PatchApplicationError(f"patch[{i}] ({path}): '{leaf}' is not a valid list index or '-'")
                if not (0 <= idx < len(parent)):
                    raise PatchApplicationError(
                        f"patch[{i}] ({path}): list index {idx} out of range (len={len(parent)})"
                    )
                parent[idx] = op["value"]
        else:
            raise PatchApplicationError(f"patch[{i}] ({path}): cannot set a key on a {type(parent).__name__}")
    return result
