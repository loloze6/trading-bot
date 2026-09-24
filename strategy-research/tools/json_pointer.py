"""
Shared RFC 6901 JSON-pointer and variant helpers (E-058 S2b code-review fix 10).

Moved here, behaviour-preserving, from workflow/run_phase1_research.py
(`_split_json_pointer`, `_json_pointer_exists`, `_check_manifest_paths`, and
protocol_execution's base-variant choice), so tools/block_registry.py reads a
block_manifest.yaml's pointers with exactly the code the orchestrator uses to
check them. run_phase1_research keeps its private names as thin wrappers.

NOT moved: block_manifest.yaml loading. The orchestrator's
backtest_specification loads it with its LLM-output-tolerant load_yaml and
treats any shape as "no paths"; block_registry loads it strictly and raises on a
malformed manifest. Unifying them would change one of the two behaviours.
"""
from __future__ import annotations


class JsonPointerError(ValueError):
    """An invalid JSON pointer, or one that does not resolve."""


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
    """The manifest-declared config_paths (STRATEGY_DESIGN_GUIDE.md §7c's
    block.config_paths) that do NOT resolve in variant_config; [] when the
    manifest has no block.config_paths list at all."""
    config_paths = ((manifest or {}).get("block") or {}).get("config_paths") or []
    return [p for p in config_paths if not json_pointer_exists(variant_config, p)]


def base_variant_id(variant_ids) -> str:
    """protocol_execution's base-variant choice: `base` when present, else the
    first id in sorted order. Raises on an empty collection."""
    ids = list(variant_ids)
    if not ids:
        raise ValueError("base_variant_id: no variant ids")
    return "base" if "base" in ids else sorted(ids)[0]
