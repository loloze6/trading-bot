"""CUL-11: opt-in JSON-Schema validation of workflow artifacts at write/read time.

If a schema exists at ``workflow_artifacts/schemas/{path.stem}.schema.json``, validate
the already-parsed ``data`` dict against it. Loader-agnostic: ``data`` is a parsed dict,
so the same helper works whether the caller produced it from ``yaml.safe_load`` or
``json.load`` — the two JSON artifacts (holdout_result, trade_diagnostics) validate
through the identical path as the YAML ones.

Opt-in by schema existence: a save whose stem has no schema file is a no-op.

Rollout is warn-by-default and EXCEPTION-PROOF. In the default (warn) mode every
exception the validation can raise — a real schema violation (``jsonschema.ValidationError``),
a malformed schema file (``jsonschema.SchemaError`` / ``json.JSONDecodeError``), a bug in
this helper, a non-dict ``data`` (``TypeError``/``AttributeError``), or ``jsonschema`` being
absent — is caught, logged once, and swallowed, so a bug in this NEW validation code can
never crash a write path that works today. Only ``WORKFLOW_ARTIFACT_VALIDATION=raise`` lets
a genuine failure propagate (blocking the write); a missing ``jsonschema`` is warned and
swallowed even then, since without the library validation is simply unavailable.

Lives in tools/ (not the workflow orchestrator) so the standalone reusable analyzers
(deflate_sharpe, prescreen_signal, run_protocol, validate_regime_detector) can import it
by bare name without pulling in the agent-SDK-heavy workflow module.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

_SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "workflow_artifacts" / "schemas"

_RAISE_VALUE = "raise"
_ENV_FLAG = "WORKFLOW_ARTIFACT_VALIDATION"


def _raise_mode() -> bool:
    return os.environ.get(_ENV_FLAG, "").strip().lower() == _RAISE_VALUE


def _make_validator(jsonschema, schema):
    """Build a validator with a registry of every schema in ``_SCHEMAS_DIR`` so a
    cross-file ``$ref`` resolves (e.g. protocol_result.schema.json ->
    trade_diagnostics.schema.json#/properties/summary). Without this, jsonschema.validate
    raises Unresolvable on the one schema that carries a $ref — silently skipping real
    validation in warn mode and false-blocking a valid artifact in raise mode.

    Prefers referencing.Registry (jsonschema >= 4.18); falls back to the deprecated
    RefResolver with a base URI at the schemas dir for older jsonschema. A malformed or
    empty sibling schema (e.g. an empty robustness_report.schema.json) is skipped so it
    cannot poison the registry for the artifact actually being validated.
    """
    cls = jsonschema.validators.validator_for(schema)
    try:
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT7
    except ImportError:
        base_uri = _SCHEMAS_DIR.resolve().as_uri() + "/"
        resolver = jsonschema.RefResolver(base_uri=base_uri, referrer=schema)
        return cls(schema, resolver=resolver)

    resources = []
    for p in _SCHEMAS_DIR.glob("*.schema.json"):
        try:
            resources.append(
                (
                    p.name,
                    Resource.from_contents(json.loads(p.read_text(encoding="utf-8")), default_specification=DRAFT7),
                )
            )
        except Exception:
            continue  # skip an empty/malformed sibling schema (not a $ref target)
    registry = Registry().with_resources(resources)
    return cls(schema, registry=registry)


def validate_workflow_artifact(path, data) -> None:
    """Validate ``data`` against ``workflow_artifacts/schemas/{stem}.schema.json`` if present.

    No-op when no matching schema exists. Warn-by-default (never raises); raises only under
    ``WORKFLOW_ARTIFACT_VALIDATION=raise``, and never for a merely-absent ``jsonschema``.
    """
    raise_mode = _raise_mode()
    try:
        schema_path = _SCHEMAS_DIR / f"{Path(path).stem}.schema.json"
        if not schema_path.exists():
            return  # opt-in by schema existence

        try:
            import jsonschema
        except Exception as exc:  # guarded optional dep — cannot validate, must not crash
            logger.warning(
                "workflow artifact validation unavailable for %s (jsonschema import failed): %s",
                schema_path.stem,
                exc,
            )
            return

        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        _make_validator(jsonschema, schema).validate(data)
    except Exception as exc:
        if raise_mode:
            raise
        logger.warning(
            "workflow artifact validation failed for %s: %s: %s",
            path,
            type(exc).__name__,
            exc,
        )
