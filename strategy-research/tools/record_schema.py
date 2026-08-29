"""
record_schema.py -- closed schema for campaign_knowledge_base.yaml findings and
config/campaign_queue.yaml entries (C7-EXT-R2, 2026-07-23).

WHY THIS FILE EXISTS: G6 HAS NOW FAILED THREE TIMES, THE SAME WAY EACH TIME.

  Round 1 (C7-EXT, 0a4d606) gated three field names:
      _VERDICT_FIELDS = ("verdict_c7", "hypothesis_verdict", "verdict")
  The audit wrote `{"outcome": "kill_mechanism_falsified"}` -- the field the KB
  and queue actually use, and the one _write_kb_findings_entry itself emits.
  ACCEPTED.

  Round 2 (C7-EXT-R, 2c8b8d1) added `outcome` and, for renamed fields, replaced
  the three-name denylist with a substring marker: any key containing the
  literal ASCII word "verdict". The commit message called this "New name, same
  gate". The re-audit wrote `status: kill`, `disposition: kill`,
  `resolution: kill`, `result: kill`, `decision: kill`, `conclusion: kill`,
  `urteil: kill`, `veredicto_c7: kill` -- and nested a verdict one level down,
  and inside a list. ALL ACCEPTED.

  The pattern is not that the wrong names were chosen. It is that ENUMERATING
  THE NAMES OF THINGS THAT ARE FORBIDDEN cannot work: the set of names an author
  might use is unbounded, spans languages, and grows every time someone invents
  a synonym. A denylist over an infinite set is a guess, and each round's guess
  was defeated in minutes by the next reader who tried a word nobody had thought
  of. Broadening the guess (round 2) is the same move, not a different one.

WHAT THIS FILE DOES INSTEAD -- a different class of fix.

  Deny by default. A KB finding or queue entry may contain ONLY the fields this
  schema enumerates, and each field's value must match a declared SHAPE. An
  unknown field is rejected wherever it appears -- top level, nested, or inside
  a list -- because no shape in this schema permits an arbitrary key to hold an
  arbitrary structure. `details`, `decisions`, `disposition`, `urteil` are not
  rejected because they are on a list of bad names; they are rejected because
  they are not on the short list of GOOD ones.

  Verdict-bearing content is permitted in EXACTLY ONE designated field --
  `outcome` -- which requires valid provenance (see
  verdict_criteria_evaluator.validate_verdict_provenance). Everywhere else, at
  any depth, a bare verdict token as a VALUE is refused. That second rule is
  name-agnostic on purpose: it catches `urteil: kill` and
  `signal_property.anything: kill` identically, because it looks at the claim,
  not at the label someone chose for it.

  The two rules compose: to smuggle a verdict you would need both a field this
  schema permits AND a value that is not a verdict token -- at which point you
  have written data, not a verdict.

ACCEPTED RISK, STATED EXPLICITLY (operator proportionality ruling, 2026-07-23).
  This schema governs what a RECORD may say. It does not and cannot establish
  that a cited pass_rule_evaluation.yaml was genuinely produced by the evaluator
  rather than hand-authored into a real run's artifacts/ directory. Any
  filesystem-only provenance check has this boundary; closing it needs a
  cryptographic or append-only-log tie, which is out of proportion to a
  single-operator research campaign. Recorded as a standing limitation, not as a
  closed hole. See ledger C7-EXT-R2 and the re-audit's carry-forward 3.

MAINTENANCE. Adding a field here is a deliberate act, and that friction is the
feature -- it is what makes "unknown" mean something. If the pipeline needs a
new field, add it WITH a shape; do not widen a shape to accommodate it.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Value shapes. Depth is constrained by SHAPE, never by a list of nested names:
# no shape below lets an arbitrary key carry an arbitrary structure, which is
# what makes "unknown field at any depth" enforceable without enumerating the
# 66 distinct measurement keys that legitimately appear under signal_property.
# ---------------------------------------------------------------------------
TEXT = "TEXT"  # str or None -- identifier or prose
NUMBER = "NUMBER"  # int/float (bool excluded)
FLAG = "FLAG"  # bool
TEXT_LIST = "TEXT_LIST"  # list[str]
METRICS = "METRICS"  # flat mapping: any key -> scalar | list[scalar]
POWER = "POWER"  # closed sub-keys, or a plain string
HISTORY = "HISTORY"  # list of superseded-outcome records, closed sub-keys
OUTCOME = "OUTCOME"  # THE designated verdict-bearing field
VERDICT_STATUS = "VERDICT_STATUS"
REF = "REF"
QUEUE_STATUS = "QUEUE_STATUS"
GATE_RESULT = "GATE_RESULT"  # LLM validation-stage gate, closed vocabulary
RELATION = "RELATION"  # queue lineage relation, closed vocabulary
SOURCE = "SOURCE"  # brief custody, closed vocabulary
REASON = "REASON"  # prose/label EXPLAINING `outcome` -- see below

_SCALAR = (str, int, float, bool, type(None))

# HISTORY records: closed sub-key set. These are superseded verdicts, retained
# deliberately, so `outcome` here MAY hold a verdict token -- it is a record of
# what was once claimed, explicitly marked as no longer current.
_HISTORY_KEYS = frozenset(
    {"outcome", "recorded_at", "superseded_at", "superseded_reason"}
)

# POWER: sample-adequacy disposition. Its own `verdict` sub-key predates this
# schema and means "was this run adequately powered", not "is the hypothesis
# true" -- so it is permitted, but its VALUE still faces the token rule below,
# which is what stops it being repurposed to carry a real verdict.
_POWER_KEYS = frozenset(
    {
        "status",
        "verdict",
        "expected_n_eff",
        "min_detectable_ic_at_target_power",
        "plausible_ic_range",
    }
)

_VERDICT_STATUS_VALUES = frozenset({"gated", "ungated", "stage_discretion", "void"})

_QUEUE_STATUS_RE = re.compile(
    r"^(ready|done|in_progress|superseded|paused:.+|blocked_on_.+)$"
)

# Three fields whose legitimate values collide with the verdict-token rule below
# -- `validation_gate: PASS` is the LLM validation STAGE's gate, and
# `relation: refine` is a queue LINEAGE link, neither of which is a claim about
# whether a hypothesis is true. They are handled by giving each a closed
# vocabulary of its own, which is tighter than free text, not looser: it is the
# only way the token rule stays absolute everywhere else.
_GATE_RESULT_VALUES = frozenset({"PASS", "FAIL", "NOT_RUN", "SKIPPED", "BLOCKED"})
_RELATION_VALUES = frozenset(
    {
        "new_registration",
        "refine",
        "reframe",
        "escalate",
        "pivot",
        "split",
        "reactivation",
    }
)
_SOURCE_VALUES = frozenset({"agent", "operator_ratified", "user_delivered"})

# A BARE VERDICT TOKEN: a value that IS a verdict, as opposed to prose that
# discusses one. Anchored and whole-value, so a paragraph containing the word
# "kill" is untouched while the value "kill_mechanism_falsified" is not.
# Verified collision-free against every string value in both live stores.
_VERDICT_TOKEN_RE = re.compile(
    r"^(kill|killed|promote|promoted|refine|refined|pass|fail)([ _:\-].*)?$",
    re.IGNORECASE,
)


# THE ONE NAMED EXEMPTION FROM THE TOKEN RULE, and why it is safe.
#
# `outcome_reason` holds the machine `verdict_label` the orchestrator computed --
# legitimately a prescreen ROUTE NAME such as `kill_no_ic` or
# `refine_inverted_ic` (see run_phase1_research._VERDICT_TO_OUTCOME, whose keys
# are exactly these route names). It is also, elsewhere in the live KB, multi-
# paragraph prose. Both are real, so the field cannot take the token rule.
#
# This is safe because `outcome_reason` is SUBORDINATE by construction: it
# explains `outcome`, it is never read as an independent verdict, and it can only
# appear on an entry whose `outcome` was itself gated in the same pass. An entry
# reading `outcome: inconclusive` + `outcome_reason: kill_no_ic` records an
# inconclusive result explained by a prescreen kill route -- which is exactly
# what it means, and is what the pipeline has always written.
#
# It is named here rather than left implicit precisely because an unexamined
# exemption is how the previous three rounds failed.
_TOKEN_RULE_EXEMPT_SHAPES = frozenset({REASON})


def is_bare_verdict_token(value) -> bool:
    """True when a string value asserts a verdict rather than describing one.

    This is the name-agnostic half of the fix. It does not care whether the key
    is `verdict_c7`, `urteil`, `disposition` or `x` -- a value that reads as a
    verdict is refused everywhere except the one designated field."""
    return isinstance(value, str) and bool(_VERDICT_TOKEN_RE.match(value.strip()))


# ---------------------------------------------------------------------------
# The closed field sets, enumerated from the live corpus plus everything the
# orchestrator and campaign runner actually write.
# ---------------------------------------------------------------------------
KB_FINDING_SCHEMA = {
    # identity & linkage
    "id": TEXT,
    "hypothesis_id": TEXT,
    "hypothesis_ids": TEXT_LIST,
    "mechanism": TEXT,
    "edge_source_category": TEXT,
    "evidence_runs": TEXT_LIST,
    "evidence_count": NUMBER,
    "supplementary_evidence": TEXT_LIST,
    "reference": TEXT,
    "run_path": TEXT,
    # THE verdict field, and its provenance
    "outcome": OUTCOME,
    "verdict_status": VERDICT_STATUS,
    "verdict_status_basis": TEXT,
    "verdict_void_reason": TEXT,
    "pass_rule_evaluation_ref": REF,
    "outcome_reason": REASON,
    "outcome_history_superseded": HISTORY,
    # measurement & provenance detail
    "signal_property": METRICS,
    "power_disposition": POWER,
    "protocol_version": TEXT,
    "protocol_version_note": TEXT,
    "detector_version": TEXT,
    "detector_family": TEXT,
    "detector_note": TEXT,
    "root_cause": TEXT,
    "validation_gate": GATE_RESULT,
    "deployable_today": TEXT,
    "venue": TEXT,
    "venue_live_tradability": TEXT,
    # lifecycle
    "exhausted": FLAG,
    "exhausted_basis": TEXT,
    "reactivation_condition": TEXT,
    "reactivation_consumed_by": TEXT,
    "blocked_by_feed": TEXT,
    "research_only": FLAG,
    "closes_ac4": FLAG,
    # annotations
    "a8_4_alignment": TEXT,
    "audit_note": TEXT,
    "autopsy_note": TEXT,
    "closes_ac4_note": TEXT,
    "engine_provenance_caveat": TEXT,
    "policy_consequence": TEXT,
    "signal_property_audit_note": TEXT,
    "strongest_threat_to_validity": TEXT,
}

QUEUE_ENTRY_SCHEMA = {
    "id": TEXT,
    "brief_path": TEXT,
    "notes": TEXT,
    "status": QUEUE_STATUS,
    "priority": NUMBER,
    "source": SOURCE,
    "relation": RELATION,
    "run_ids": TEXT_LIST,
    "outcome": OUTCOME,
    "verdict_status": VERDICT_STATUS,
    "verdict_status_basis": TEXT,
    "verdict_void_reason": TEXT,
    "pass_rule_evaluation_ref": REF,
    "refinement_brief_path": TEXT,
    "refinement_brief_consumed_for": TEXT,
}

# Dated correction families. A correction gets its own dated field so the prior
# text is never overwritten; the DATE varies, the shape does not. Allowlist
# patterns are safe in a way denylist patterns are not -- the shape still binds.
_DATED_FAMILIES = (
    (re.compile(r"^readjudication_\d{8}$"), TEXT),
    (re.compile(r"^outcome_history_superseded_\d{8}$"), HISTORY),
)


class RecordSchemaError(ValueError):
    """An entry contains a field this schema does not permit, or a value that
    does not match the permitted field's declared shape."""


def _shape_for(field: str, schema: dict):
    if field in schema:
        return schema[field]
    for pattern, shape in _DATED_FAMILIES:
        if pattern.match(field):
            return shape
    return None


def _check_scalar_tree(value, path: str, errors: list, allow_verdict_token=False):
    """Recursively verify a data subtree is flat-ish scalars and carries no
    verdict claim. Rejects nested mappings, which is what stops an arbitrary
    structure being smuggled inside a permitted data field."""
    if isinstance(value, dict):
        errors.append(
            f"{path}: nested mapping is not permitted inside a data field "
            f"(only scalars and lists of scalars)"
        )
        return
    if isinstance(value, list):
        for i, item in enumerate(value):
            _check_scalar_tree(item, f"{path}[{i}]", errors, allow_verdict_token)
        return
    if not isinstance(value, _SCALAR):
        errors.append(f"{path}: value of type {type(value).__name__} is not permitted")
        return
    if not allow_verdict_token and is_bare_verdict_token(value):
        errors.append(
            f"{path}: value {value!r} is a bare verdict token; a verdict may "
            f"appear ONLY in the designated `outcome` field, which requires "
            f"provenance"
        )


def _check_value(field: str, shape: str, value, errors: list):
    path = field
    if shape in (TEXT, REF, REASON):
        if value is None:
            return
        if not isinstance(value, str):
            errors.append(f"{path}: expected text, got {type(value).__name__}")
        elif shape not in _TOKEN_RULE_EXEMPT_SHAPES and is_bare_verdict_token(value):
            errors.append(
                f"{path}: value {value!r} is a bare verdict token; a verdict "
                f"may appear ONLY in the designated `outcome` field"
            )
    elif shape == NUMBER:
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float))
        ):
            errors.append(f"{path}: expected a number, got {type(value).__name__}")
    elif shape == FLAG:
        if value is not None and not isinstance(value, bool):
            errors.append(f"{path}: expected a boolean, got {type(value).__name__}")
    elif shape == TEXT_LIST:
        if value is None:
            return
        if not isinstance(value, list):
            errors.append(f"{path}: expected a list, got {type(value).__name__}")
        else:
            for i, item in enumerate(value):
                if not isinstance(item, str):
                    errors.append(
                        f"{path}[{i}]: expected text, got {type(item).__name__}"
                    )
                elif is_bare_verdict_token(item):
                    errors.append(
                        f"{path}[{i}]: value {item!r} is a bare verdict token"
                    )
    elif shape == METRICS:
        if value is None:
            return
        if not isinstance(value, dict):
            errors.append(
                f"{path}: expected a mapping of measurements, got "
                f"{type(value).__name__}"
            )
        else:
            for key, item in value.items():
                _check_scalar_tree(item, f"{path}.{key}", errors)
    elif shape == POWER:
        if value is None or isinstance(value, str):
            _check_value(field, TEXT, value, errors)
        elif isinstance(value, dict):
            for key, item in value.items():
                if key not in _POWER_KEYS:
                    errors.append(
                        f"{path}.{key}: unknown field (permitted: "
                        f"{sorted(_POWER_KEYS)})"
                    )
                else:
                    _check_scalar_tree(item, f"{path}.{key}", errors)
        else:
            errors.append(
                f"{path}: expected text or a mapping, got {type(value).__name__}"
            )
    elif shape == HISTORY:
        if value is None:
            return
        if not isinstance(value, list):
            errors.append(f"{path}: expected a list of superseded-outcome records")
        else:
            for i, record in enumerate(value):
                if not isinstance(record, dict):
                    errors.append(f"{path}[{i}]: expected a mapping")
                    continue
                for key, item in record.items():
                    if key not in _HISTORY_KEYS:
                        errors.append(
                            f"{path}[{i}].{key}: unknown field (permitted: "
                            f"{sorted(_HISTORY_KEYS)})"
                        )
                    else:
                        # a superseded `outcome` is a record of a withdrawn claim,
                        # deliberately retained -- see _HISTORY_KEYS.
                        _check_scalar_tree(
                            item,
                            f"{path}[{i}].{key}",
                            errors,
                            allow_verdict_token=(key == "outcome"),
                        )
    elif shape == OUTCOME:
        if value is not None and not isinstance(value, str):
            errors.append(f"{path}: expected text, got {type(value).__name__}")
    elif shape == VERDICT_STATUS:
        if (
            value is not None
            and str(value).strip().lower() not in _VERDICT_STATUS_VALUES
        ):
            errors.append(
                f"{path}: {value!r} is not a recognised verdict_status "
                f"(permitted: {sorted(_VERDICT_STATUS_VALUES)})"
            )
    elif shape == QUEUE_STATUS:
        if value is not None and not _QUEUE_STATUS_RE.match(str(value).strip()):
            errors.append(f"{path}: {value!r} is not a recognised queue status")
    elif shape in (GATE_RESULT, RELATION, SOURCE):
        permitted = {
            GATE_RESULT: _GATE_RESULT_VALUES,
            RELATION: _RELATION_VALUES,
            SOURCE: _SOURCE_VALUES,
        }[shape]
        if value is not None and str(value).strip() not in permitted:
            errors.append(
                f"{path}: {value!r} is not permitted here "
                f"(closed vocabulary: {sorted(permitted)})"
            )


def validate_record_schema(
    entry: dict, schema: dict, entry_ref: str = "<entry>"
) -> dict:
    """Deny-by-default structural validation. Returns the entry when it conforms;
    raises RecordSchemaError listing every violation otherwise.

    Reports ALL violations rather than the first: a hand-edited entry usually has
    more than one problem, and fixing them one exception at a time is how people
    give up and reach for a workaround."""
    if not isinstance(entry, dict):
        raise RecordSchemaError(
            f"{entry_ref}: expected a mapping, got {type(entry).__name__}"
        )

    errors: list = []
    for field, value in entry.items():
        shape = _shape_for(str(field), schema)
        if shape is None:
            errors.append(
                f"{field}: unknown field. This record type permits only the fields "
                f"enumerated in tools/record_schema.py. If the pipeline genuinely "
                f"needs {field!r}, add it there WITH a declared shape -- deliberately, "
                f"which is the point."
            )
            continue
        _check_value(str(field), shape, value, errors)

    if errors:
        raise RecordSchemaError(
            f"{entry_ref} violates the closed record schema:\n  - "
            + "\n  - ".join(errors)
        )
    return entry


def validate_kb_finding(entry: dict, entry_ref: str = "<KB finding>") -> dict:
    return validate_record_schema(entry, KB_FINDING_SCHEMA, entry_ref)


def validate_queue_entry(entry: dict, entry_ref: str = "<queue entry>") -> dict:
    return validate_record_schema(entry, QUEUE_ENTRY_SCHEMA, entry_ref)
