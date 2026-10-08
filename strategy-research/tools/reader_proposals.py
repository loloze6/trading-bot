"""
Load and validate the five specialist readers' proposal files
(runs/<id>/artifacts/proposals/<category>.yaml, shape:
workflow_artifacts/schemas/proposal.schema.json).

E-046a. Readers propose evidence-grounded changes; they never decide an
idea's status (that is the grid, idea_status.yaml) and never route. Their
scores only RANK the next candidate, which is the decide-next step's job
(delivery_plan_v26.md slice 6b) -- this module deliberately stops at
"well-formed proposals in, validated proposals out".

Kept out of workflow/run_phase1_research.py so decide_next can import it
without the orchestrator. jsonschema is not a declared runtime dependency,
so the schema's rules are checked by hand here; a test pins the two
together.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

import yaml

SCORE_KEYS = ("confidence_real", "distance_to_profitable", "mechanism_plausibility")
_PROPOSAL_KEYS = frozenset(
    {"proposal_id", "kind", "patch", "block", "evidence", "scores", "model_id", "rubric_version",
     "requires_feed"})
_PATCH_ITEM_KEYS = frozenset({"component_id", "field", "before", "after"})
_BLOCK_KEYS = frozenset({"kind", "config_paths", "scaffolding", "rationale"})
# CUL-380: the one statement of a new_block's shape -- quoted in every refusal
# and by every reader SKILL.md. `rationale` is required: when decide-next picks
# a new_block it becomes the next idea's research goal (decide_next: "Test a new
# <kind> block ...: <rationale>"); a sketch without it is an empty idea.
NEW_BLOCK_SHAPE = (
    "Required shape: block: {kind: forecast|regime, config_paths: [non-empty list of "
    "JSON-pointer strings], scaffolding: [optional list], rationale: \"<string: what the "
    "new block is and why it should help>\"} -- exactly these keys.")
_PROPOSAL_ID_RE = re.compile(r"^[a-z_]+-.+-[0-9]+$")
# E-035 S2c: the optional `requires_feed` field, orthogonal to `kind`.
REQUIRES_FEED_KEYS = frozenset({"feed", "reason"})
# A feed is named as a strategy config's aux_feeds entry names it (a
# trading-bot FEED_REGISTRY key) -- lowercase snake_case, so it compares
# exactly against the registry's keys.
FEED_NAME_RE = re.compile(r"[a-z][a-z0-9_]*")


# C5.7b-2 (D-048, S2): the closed `rubric_version` set. A reader's rubric is
# fully determined by its category, so each category has exactly one accepted
# value -- the literal its SKILL.md tells the model to write (C2 S2e: all -v2).
# Enforced only under strict_provenance=True (orchestrator.score_provenance);
# tests/test_c5_7b2_rubric_citations.py pins this dict to the five SKILL files,
# so bumping a SKILL to -v3 fails that test until this dict is bumped too.
READER_RUBRIC_VERSIONS = {
    "profitability": "profitability-reader-v2",
    "forecast_power": "forecast_power-reader-v2",
    "regime_power": "regime_power-reader-v3",
    "component_attribution": "component_attribution-reader-v2",
    "trade_efficiency": "trade_efficiency-reader-v2",
}


# ---------------------------------------------------------------------------
# E-068 slice 5 (D-073): reader output v3, written only under
# orchestrator.reader_findings.enabled (the flag is read by the orchestrator,
# never here). A v3 file is a MAPPING -- one reading per reader -- where a v2
# file is a LIST; load_proposals tells them apart by shape, so old v2 files
# still load and the two coexist. A v3 reading explains the measured result
# and proposes: 0..MAX_SIDE_FINDINGS side findings (each a full claim block,
# checked by claim_card.check_claim where it is written and again by
# decide_next, optionally carrying the config change to test it with; the
# stand-alone patch is removed, see below). It carries NO verdict: the closed key
# set below has no field that could say the claim holds or not. Shape only
# here (no claim_card import): load_proposals is used by decide_next and the
# campaign memory, which must keep loading a file whose claim a later grammar
# would refuse -- that refusal is decide_next's, as an ineligibility.
# ---------------------------------------------------------------------------
READING_SCHEMA_VERSION = 3
MAX_SIDE_FINDINGS = 2
SIDE_FINDING = "side_finding"
READER_RUBRIC_VERSIONS_V3 = {cat: f"{cat}-reading-v1" for cat in READER_RUBRIC_VERSIONS}
# E-068 continuation 2, section 9 item 2 (operator, 2026-10-06): ONE kind of reader
# proposal. A config change is proposed only inside a side finding (`config_change`,
# with the claim it tests); the stand-alone `patch` is removed from what a reader
# writes. A v3 file written before that (runs 070-074) may still hold a `patch` key:
# it is accepted when LOADING (from_model=False) and flattened as before, never from
# a model's answer.
_READING_KEYS = frozenset({"schema_version", "reading_id", "model_id", "rubric_version",
                           "explanation", "evidence", "side_findings"})
_LEGACY_READING_KEYS = _READING_KEYS | {"patch"}
_READING_REQUIRED = ("schema_version", "reading_id", "model_id", "rubric_version",
                     "explanation", "evidence", "side_findings")
PATCH_REMOVED_MESSAGE = (
    "the stand-alone `patch` is removed: a reader proposes side findings only. To test a "
    "config change, put it inside a side finding as `config_change: [{component_id, field, "
    "before, after}]`, with the claim that change is expected to show")
_SKIPPED_READING_KEYS = frozenset({"schema_version", "reading_id", "skipped"})
_SKIP_RECORD_KEYS = frozenset({"rule", "reason"})
# Written by code only (tools/reader_findings.py); a model writing `skipped`
# is refused (from_model=True).
SKIP_RULES = ("regime_detector_scaffolding", "regime_detector_constant",
              "single_component", "output_refused_after_retry",
              # E-072 (orchestrator.explore_confirm only): a readers' exploration
              # copy could not be written -- never the all-window file instead
              "exploration_inputs_unavailable")
_SIDE_FINDING_KEYS = frozenset({"proposal_id", "claim", "evidence", "scores", "requires_feed",
                                "config_change"})
_V3_PATCH_KEYS = frozenset({"proposal_id", "patch", "evidence", "scores", "requires_feed"})


class ProposalError(ValueError):
    """A proposal file or entry is malformed. Never caught here: a bad reader
    output must stop loudly, never silently count as 'no proposals'."""


def _load_yaml_strict(path: Path):
    """Plain single-document safe_load -- no LLM-output repair, which would
    turn a malformed reader file into a silently 'repaired' one."""
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ProposalError(f"{path}: unparseable YAML ({exc})") from exc


def _non_empty_str(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_proposal(p, cat: str, where: str, strict_provenance: bool = False) -> None:
    if not isinstance(p, dict):
        raise ProposalError(f"{where}: proposal is not a mapping")
    extra = sorted(set(p) - _PROPOSAL_KEYS)
    if extra:
        raise ProposalError(f"{where}: undeclared field(s) {extra} (readers never route or decide)")
    for key in ("model_id", "rubric_version"):
        if not _non_empty_str(p.get(key)):
            raise ProposalError(f"{where}: {key} must be a non-empty string")
    if strict_provenance:
        expected = READER_RUBRIC_VERSIONS.get(cat)
        if expected is None:
            raise ProposalError(f"{where}: no closed rubric_version is defined for category "
                                f"'{cat}' (known: {sorted(READER_RUBRIC_VERSIONS)})")
        if p["rubric_version"] != expected:
            raise ProposalError(f"{where}: rubric_version={p['rubric_version']!r} is not the "
                                f"'{cat}' reader's rubric; write exactly {expected!r}")
    pid = p.get("proposal_id")
    if not isinstance(pid, str) or not pid.startswith(f"{cat}-") or not _PROPOSAL_ID_RE.match(pid):
        raise ProposalError(f"{where}: proposal_id={pid!r} must match <category>-<run_id>-<n> "
                            f"with category '{cat}'")
    kind = p.get("kind")
    if kind == "patch":
        items = p.get("patch")
        if not isinstance(items, list) or not items or "block" in p:
            raise ProposalError(f"{where}: kind=patch requires a non-empty `patch` list and no `block`")
        for k, item in enumerate(items):
            if not isinstance(item, dict) or set(item) != _PATCH_ITEM_KEYS \
                    or not _non_empty_str(item["component_id"]) or not _non_empty_str(item["field"]):
                raise ProposalError(f"{where}: patch[{k}] must be exactly "
                                    f"{{component_id, field, before, after}} with non-empty "
                                    f"component_id and field")
    elif kind == "new_block":
        # CUL-380: every refusal states the WHOLE required shape, so one retry
        # can fix every field at once (run_065: the retry fixed `kind`, then
        # failed on the missing `rationale`).
        blk = p.get("block")
        if not isinstance(blk, dict) or "patch" in p or blk.get("kind") not in ("forecast", "regime"):
            raise ProposalError(f"{where}: kind=new_block requires a `block` mapping with kind "
                                f"forecast|regime, and no `patch`. {NEW_BLOCK_SHAPE}")
        if sorted(set(blk) - _BLOCK_KEYS) or not isinstance(blk.get("rationale"), str):
            raise ProposalError(f"{where}: block must carry a string rationale and no undeclared "
                                f"field. {NEW_BLOCK_SHAPE}")
        paths = blk.get("config_paths")
        if not isinstance(paths, list) or not paths or not all(_non_empty_str(x) for x in paths):
            raise ProposalError(f"{where}: block.config_paths must be a non-empty list of strings. "
                                f"{NEW_BLOCK_SHAPE}")
    else:
        raise ProposalError(f"{where}: kind={kind!r} not in ['patch', 'new_block']")
    ev = p.get("evidence")
    if not isinstance(ev, list) or not ev or not all(_non_empty_str(e) for e in ev):
        raise ProposalError(f"{where}: evidence must be a non-empty list of non-empty strings")
    check_scores(p.get("scores"), where)
    if "requires_feed" in p:
        _check_requires_feed(p["requires_feed"], where)


def _check_requires_feed(rf, where: str) -> None:
    """E-035 S2c: exactly {feed, reason}; feed a lowercase snake_case name,
    reason a non-empty string. Present-but-null is malformed, not 'absent'."""
    if not isinstance(rf, dict) or set(rf) != REQUIRES_FEED_KEYS:
        raise ProposalError(f"{where}: requires_feed must be exactly {{feed, reason}}")
    if not isinstance(rf["feed"], str) or not FEED_NAME_RE.fullmatch(rf["feed"]):
        raise ProposalError(f"{where}: requires_feed.feed={rf['feed']!r} must be a lowercase "
                            f"snake_case feed name (e.g. funding_rate, open_interest)")
    if not _non_empty_str(rf["reason"]):
        raise ProposalError(f"{where}: requires_feed.reason must be a non-empty string")


def check_scores(scores, where: str) -> None:
    """The anchored score shape: exactly SCORE_KEYS, each an integer 0..3.
    Shared with tools/decide_next.py (E-059 S2b: a brief's extra cards are
    scored on the same shape). Raises ProposalError."""
    if not isinstance(scores, dict) or set(scores) != set(SCORE_KEYS):
        raise ProposalError(f"{where}: scores must have exactly {list(SCORE_KEYS)}")
    for key in SCORE_KEYS:
        v = scores[key]
        if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= 3:
            raise ProposalError(f"{where}: scores.{key}={v!r} is not an integer in 0..3")


def is_reading(doc) -> bool:
    """True for a v3 reading (a mapping with schema_version 3)."""
    return isinstance(doc, dict) and doc.get("schema_version") == READING_SCHEMA_VERSION


def _check_evidence(ev, where: str) -> None:
    if not isinstance(ev, list) or not ev or not all(_non_empty_str(e) for e in ev):
        raise ProposalError(f"{where}: evidence must be a non-empty list of non-empty strings")


def _check_item_id(pid, reading_id: str, where: str) -> None:
    if not (isinstance(pid, str) and pid.startswith(f"{reading_id}-")
            and pid[len(reading_id) + 1:].isdigit() and _PROPOSAL_ID_RE.match(pid)):
        raise ProposalError(f"{where}: proposal_id={pid!r} must be '{reading_id}-<n>' "
                            f"(the reading_id, a dash, a number)")


def check_reading(doc, cat: str, where: str, *, strict_provenance: bool = False,
                  from_model: bool = False) -> None:
    """Shape check of one v3 reading (the claim INSIDE a side finding is
    checked by claim_card.check_claim, not here). `from_model`: the text a
    reader answered -- a `skipped` reading is code's only, so it is refused.
    Raises ProposalError naming the whole required shape where it can."""
    if not is_reading(doc):
        raise ProposalError(f"{where}: a v3 reading must be a mapping with schema_version: "
                            f"{READING_SCHEMA_VERSION}")
    rid = doc.get("reading_id")
    if not (isinstance(rid, str) and rid.startswith(f"{cat}-") and len(rid) > len(cat) + 1):
        raise ProposalError(f"{where}: reading_id={rid!r} must be '{cat}-<run_id>'")
    if "skipped" in doc:
        if from_model:
            raise ProposalError(f"{where}: `skipped` is written by code only; write a reading "
                                f"(explanation, evidence, side_findings)")
        if set(doc) != _SKIPPED_READING_KEYS:
            raise ProposalError(f"{where}: a skipped reading is exactly "
                                f"{sorted(_SKIPPED_READING_KEYS)}")
        skip = doc["skipped"]
        if (not isinstance(skip, dict) or set(skip) != _SKIP_RECORD_KEYS
                or skip.get("rule") not in SKIP_RULES or not _non_empty_str(skip.get("reason"))):
            raise ProposalError(f"{where}: skipped must be {{rule, reason}} with rule in "
                                f"{list(SKIP_RULES)} and a non-empty reason")
        return
    if from_model and doc.get("patch") is not None:
        raise ProposalError(f"{where}: {PATCH_REMOVED_MESSAGE}")
    # review: a model's `patch: null` proposes nothing -- accepted (no retry spent)
    allowed = _READING_KEYS | ({"patch"} if "patch" in doc and doc["patch"] is None else set())
    extra = sorted(set(doc) - (allowed if from_model else _LEGACY_READING_KEYS))
    if extra:
        raise ProposalError(f"{where}: undeclared field(s) {extra}; a reading has exactly "
                            f"{sorted(_READING_KEYS)} (readers explain and propose; they never "
                            f"judge the claim)")
    missing = [k for k in _READING_REQUIRED if k not in doc]
    if missing:
        raise ProposalError(f"{where}: missing {missing}; a reading has exactly "
                            f"{sorted(_READING_KEYS)} (`side_findings: []` when there is none)")
    for key in ("model_id", "rubric_version"):
        if not _non_empty_str(doc.get(key)):
            raise ProposalError(f"{where}: {key} must be a non-empty string")
    if strict_provenance and doc["rubric_version"] != READER_RUBRIC_VERSIONS_V3.get(cat):
        raise ProposalError(f"{where}: rubric_version={doc['rubric_version']!r} is not the "
                            f"'{cat}' reader's v3 rubric; write exactly "
                            f"{READER_RUBRIC_VERSIONS_V3.get(cat)!r}")
    if not _non_empty_str(doc.get("explanation")):
        raise ProposalError(f"{where}: explanation must be a non-empty string")
    _check_evidence(doc.get("evidence"), where)
    sides = doc.get("side_findings")
    if not isinstance(sides, list) or len(sides) > MAX_SIDE_FINDINGS:
        raise ProposalError(f"{where}: side_findings must be a list of at most "
                            f"{MAX_SIDE_FINDINGS} (`[]` for none)")
    seen = set()
    for i, s in enumerate(sides):
        w = f"{where}.side_findings[{i}]"
        if not isinstance(s, dict) or set(s) - _SIDE_FINDING_KEYS \
                or not {"proposal_id", "claim", "evidence", "scores"} <= set(s):
            raise ProposalError(f"{w}: a side finding is exactly {{proposal_id, claim, evidence, "
                                f"scores}} plus an optional requires_feed and an optional "
                                f"config_change")
        _check_item_id(s["proposal_id"], rid, w)
        if not isinstance(s["claim"], dict):
            raise ProposalError(f"{w}: claim must be a claim block mapping (CLAIM_TESTS.md)")
        if "config_change" in s:
            _check_change_items(s["config_change"], f"{w}.config_change")
        _check_evidence(s["evidence"], w)
        check_scores(s["scores"], w)
        if "requires_feed" in s:
            _check_requires_feed(s["requires_feed"], w)
        if s["proposal_id"] in seen:
            raise ProposalError(f"{w}: duplicate proposal_id {s['proposal_id']!r}")
        seen.add(s["proposal_id"])
    patch = doc.get("patch")
    if patch is not None:
        w = f"{where}.patch"
        if not isinstance(patch, dict) or set(patch) - _V3_PATCH_KEYS \
                or not {"proposal_id", "patch", "evidence", "scores"} <= set(patch):
            raise ProposalError(f"{w}: patch is null or exactly {{proposal_id, patch, evidence, "
                                f"scores}} plus an optional requires_feed")
        _check_item_id(patch["proposal_id"], rid, w)
        items = patch["patch"]
        if not isinstance(items, list) or not items:
            raise ProposalError(f"{w}: patch.patch must be a non-empty list of changes")
        for k, item in enumerate(items):
            if not isinstance(item, dict) or set(item) != _PATCH_ITEM_KEYS \
                    or not _non_empty_str(item["component_id"]) or not _non_empty_str(item["field"]):
                raise ProposalError(f"{w}.patch[{k}] must be exactly "
                                    f"{{component_id, field, before, after}} with non-empty "
                                    f"component_id and field")
        _check_evidence(patch["evidence"], w)
        check_scores(patch["scores"], w)
        if "requires_feed" in patch:
            _check_requires_feed(patch["requires_feed"], w)
        if patch["proposal_id"] in seen:
            raise ProposalError(f"{w}: duplicate proposal_id {patch['proposal_id']!r}")


def _check_change_items(items, where: str) -> None:
    """A side finding's config_change: a non-empty list of exactly
    {component_id, field, before, after} (the patch item shape; resolved
    against the real base config where it is written, and by decide-next)."""
    if not isinstance(items, list) or not items:
        raise ProposalError(f"{where}: must be a non-empty list of changes (omit it when the "
                            f"finding needs no config change)")
    for k, item in enumerate(items):
        if not isinstance(item, dict) or set(item) != _PATCH_ITEM_KEYS \
                or not _non_empty_str(item["component_id"]) or not _non_empty_str(item["field"]):
            raise ProposalError(f"{where}[{k}] must be exactly {{component_id, field, before, "
                                f"after}} with non-empty component_id and field")


def flatten_reading(doc: dict) -> list:
    """A checked v3 reading as decide-next items: each side finding as
    {proposal_id, kind: side_finding, claim, evidence, scores, model_id,
    rubric_version[, requires_feed][, config_change]}; a LEGACY v3 file's
    patch (written before continuation 2 removed it) as a v2-shaped
    `kind: patch` item, so old runs load unchanged. A skipped reading has
    none. The explanation is not an item (it proposes nothing)."""
    if "skipped" in doc:
        return []
    prov = {"model_id": doc["model_id"], "rubric_version": doc["rubric_version"]}
    out = []
    for s in doc.get("side_findings") or []:
        item = {"proposal_id": s["proposal_id"], "kind": SIDE_FINDING, "claim": s["claim"],
                "evidence": s["evidence"], "scores": s["scores"], **prov}
        if "requires_feed" in s:
            item["requires_feed"] = s["requires_feed"]
        if "config_change" in s:
            item["config_change"] = s["config_change"]
        out.append(item)
    patch = doc.get("patch")
    if patch is not None:
        item = {"proposal_id": patch["proposal_id"], "kind": "patch", "patch": patch["patch"],
                "evidence": patch["evidence"], "scores": patch["scores"], **prov}
        if "requires_feed" in patch:
            item["requires_feed"] = patch["requires_feed"]
        out.append(item)
    return out


def load_readings(proposals_dir: Path, categories: list) -> dict:
    """{category: v3 reading} for every category whose file is a v3 reading
    (checked); v2 files and missing files are left out."""
    out = {}
    for cat in categories:
        path = Path(proposals_dir) / f"{cat}.yaml"
        if not path.exists():
            continue
        data = _load_yaml_strict(path)
        if is_reading(data):
            check_reading(data, cat, str(path))
            out[cat] = data
    return out


def load_proposals(proposals_dir: Path, categories: list, strict_provenance: bool = False) -> dict:
    """{category: [proposal, ...]} for every category. A missing file and `[]`
    both mean "no proposals" (an honest reader output). Everything else that
    is not a well-formed list of proposals raises ProposalError, including an
    empty/null file, a non-list document, a duplicate or foreign-category
    proposal_id, and an unexpected *.yaml/*.yml in the directory (a mis-named
    file would otherwise be silently skipped). OS/editor litter is ignored.

    `strict_provenance` (C5.7b-2, default False so every existing caller and
    `-v1` fixture is unchanged): also require each proposal's `rubric_version`
    to be exactly READER_RUBRIC_VERSIONS[category]."""
    proposals_dir = Path(proposals_dir)
    if proposals_dir.exists():
        expected = {f"{c}.yaml" for c in categories}
        unexpected = sorted(x.name for x in proposals_dir.iterdir()
                            if x.is_file() and x.name.endswith((".yaml", ".yml"))
                            and not x.name.startswith(".") and x.name not in expected)
        if unexpected:
            raise ProposalError(f"{proposals_dir}: unexpected file(s) {unexpected} -- only "
                                f"{sorted(expected)} are recognised")
    out = {}
    for cat in categories:
        path = proposals_dir / f"{cat}.yaml"
        if not path.exists():
            out[cat] = []
            continue
        data = _load_yaml_strict(path)
        if is_reading(data):
            # E-068 slice 5 (D-073): a v3 reading, flattened into items.
            check_reading(data, cat, str(path), strict_provenance=strict_provenance)
            out[cat] = flatten_reading(data)
            continue
        if not isinstance(data, list):
            raise ProposalError(f"{path}: expected a YAML list of proposals (`[]` for none), "
                                f"got {type(data).__name__}")
        seen = set()
        for n, p in enumerate(data):
            _check_proposal(p, cat, f"{path}[{n}]", strict_provenance)
            if p["proposal_id"] in seen:
                raise ProposalError(f"{path}[{n}]: duplicate proposal_id {p['proposal_id']!r}")
            seen.add(p["proposal_id"])
        out[cat] = data
    return out


# ---------------------------------------------------------------------------
# E-068 PR 4 (D-071): component class names a reader wrote that do not exist.
#
# run_070's regime_power reader proposed "VarianceRatioRegimeComponent"; the
# real class is VarianceRatioComponent. A WARNING ONLY: decide_next records it
# on the candidate (`warnings`) and run_campaign prints it; nothing is refused,
# ranked or excluded on it, and nothing is ever written into proposals/
# (load_proposals refuses unexpected YAML there).
# ---------------------------------------------------------------------------

# A class-like word ending in "Component". A bare "Component" never matches
# (it needs at least one capital letter before the suffix).
COMPONENT_CLASS_NAME_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*Component\b")
# Provenance fields: never prose about the strategy, never scanned.
_CLASS_SCAN_SKIP_KEYS = frozenset({"proposal_id", "model_id", "rubric_version"})
# The base classes in trading-bot/strategies/strategy_base.py whose names match
# COMPONENT_CLASS_NAME_RE: real names, never a typo
# (tests/test_e068_4_approval_cap_warnings.py pins this set to that file).
BASE_COMPONENT_CLASS_NAMES = frozenset({"SubStrategyComponent"})
# difflib.get_close_matches' own default cutoff.
_SUGGESTION_CUTOFF = 0.6


def _string_leaves(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _string_leaves(value)
    elif isinstance(node, list):
        for value in node:
            yield from _string_leaves(value)


def unknown_class_names(proposal, known, card_text=None) -> dict:
    """Component class names in `proposal` that are not real classes. Pure.

    Scans every string leaf of the proposal except proposal_id, model_id and
    rubric_version for COMPONENT_CLASS_NAME_RE. `known`: the known component
    classes (dotted paths, e.g. decide_next.known_component_classes, or bare
    names); BASE_COMPONENT_CLASS_NAMES are always known. `card_text`: the raw
    text of the run's hypothesis_card.yaml, or None -- a name the card itself
    uses is the reader quoting the card, so it is reported under
    `quoted_from_card`, not as unknown.

    Returns {"unknown": [{"name", "suggestion"}], "quoted_from_card": [name]},
    each name once, in first-seen order. `suggestion` is the nearest known
    class name (difflib), or None when nothing is close."""
    known_names = {str(k).rpartition(".")[2] for k in (known or [])}
    real = known_names | BASE_COMPONENT_CLASS_NAMES
    found = []
    if isinstance(proposal, dict):
        for key, value in proposal.items():
            if key in _CLASS_SCAN_SKIP_KEYS:
                continue
            for leaf in _string_leaves(value):
                for name in COMPONENT_CLASS_NAME_RE.findall(leaf):
                    if name not in found:
                        found.append(name)
    on_card = set(COMPONENT_CLASS_NAME_RE.findall(card_text)) if isinstance(card_text, str) else set()
    unknown, quoted = [], []
    for name in found:
        if name in real:
            continue
        if name in on_card:
            quoted.append(name)
            continue
        close = difflib.get_close_matches(name, sorted(known_names), n=1,
                                          cutoff=_SUGGESTION_CUTOFF)
        unknown.append({"name": name, "suggestion": close[0] if close else None})
    return {"unknown": unknown, "quoted_from_card": quoted}


# ---------------------------------------------------------------------------
# C5.7b-2 (D-048, S4): record-only citation resolution.
#
# Each `evidence` item is supposed to cite a field path from the files the
# reader received (its category report, grid_evaluation.yaml,
# the registry summary -- the E-061 C2 S2e artifact, named only in
# block_registry.py / run_phase1_research.py by that test's pin). resolve_evidence_paths() MEASURES how many of those
# paths exist. It is pure, never rejects, and only reports; whether to gate on
# it (A+) or add per-score attribution (B) is decided after C4's first real
# reader output gives a measured unresolved rate (D-048). It reads no file and
# no market data: it walks documents it is handed.
# ---------------------------------------------------------------------------

# Roots the SKILLs cite even when the file they live in is absent; a rooted path
# into an absent file is UNRESOLVED (measured), not ignored. The top-level keys
# of every file actually received are roots too.
CITATION_ROOTS = frozenset({"variants", "this_run", "registry", "blocks", "groups"})
_CITE_BRACKETS = r"(?:\[[^\]\s]*\])*"
_CITE_TOKEN_RE = re.compile(
    rf"(?<![\w.\]\[/])[A-Za-z_][A-Za-z0-9_]*{_CITE_BRACKETS}"
    rf"(?:\.[A-Za-z0-9_]+{_CITE_BRACKETS})+")
_CITE_STEP_RE = re.compile(rf"\.?([A-Za-z0-9_]+)({_CITE_BRACKETS})")


def _cite_steps(token: str) -> list:
    """[(key, [bracket contents...]), ...] for one path token."""
    return [(m.group(1), re.findall(r"\[([^\]\s]*)\]", m.group(2)))
            for m in _CITE_STEP_RE.finditer(token)]


def _cite_get(node, key: str):
    """(found, value) for a mapping key, tolerating non-string YAML keys."""
    if not isinstance(node, dict):
        return False, None
    if key in node:
        return True, node[key]
    for k, v in node.items():
        if str(k) == key:
            return True, v
    return False, None


def _cite_walk(node, steps: list) -> bool:
    if not steps:
        return True
    key, brackets = steps[0]
    found, value = _cite_get(node, key)
    return found and _cite_walk_brackets(value, brackets, steps[1:])


def _cite_walk_brackets(node, brackets: list, rest: list) -> bool:
    """`[*]` and `[]` mean "some element" (the list must exist; with a path
    after it, at least one element must resolve it); `[n]` is that index; any
    other bracket is a mapping key. A name that cannot be resolved is False."""
    if not brackets:
        return _cite_walk(node, rest)
    b, more = brackets[0], brackets[1:]
    if b in ("*", ""):
        if not isinstance(node, list):
            return False
        if not more and not rest:
            return True
        return any(_cite_walk_brackets(el, more, rest) for el in node)
    if b.isdigit():
        i = int(b)
        if not isinstance(node, list) or i >= len(node):
            return False
        return _cite_walk_brackets(node[i], more, rest)
    found, value = _cite_get(node, b)
    return found and _cite_walk_brackets(value, more, rest)


def resolve_evidence_paths(received_files: dict, evidence: list) -> dict:
    """Which field paths cited in one proposal's `evidence` exist in the files
    the reader received.

    `received_files`: {file name: parsed document}; a document that is absent or
    not a mapping (`None`) is an unavailable file. `evidence`: the proposal's
    evidence strings.

    Path tokens are dotted names rooted at a known root (CITATION_ROOTS, or a
    top-level key of a received file), e.g.
    `variants.base.slices.per_symbol.BTCUSDT[*].core.cost_drag_pct`. `[*]` / `[]`
    match any list element, `[n]` an index, and a trailing `=value` (or any
    prose after the path) is dropped -- the value is NOT compared. Returns
    {"resolved": [...], "unresolved": [...], "no_path_items": n}: each distinct
    token once, in first-seen order, as written; no_path_items counts evidence
    items with no rooted path token at all. Never rejects; a malformed argument
    (not a list / not a mapping) raises TypeError for the caller to record."""
    if not isinstance(received_files, dict):
        raise TypeError("received_files must be a mapping of file name -> document")
    if not isinstance(evidence, list):
        raise TypeError("evidence must be a list of strings")
    docs = [d for d in received_files.values() if isinstance(d, dict)]
    roots = set(CITATION_ROOTS) | {str(k) for d in docs for k in d}
    resolved, unresolved, seen, no_path = [], [], set(), 0
    for item in evidence:
        tokens = ([t for t in _CITE_TOKEN_RE.findall(item) if _cite_steps(t)[0][0] in roots]
                  if isinstance(item, str) else [])
        if not tokens:
            no_path += 1
            continue
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            steps = _cite_steps(token)
            ok = any(_cite_walk(d, steps) for d in docs if _cite_get(d, steps[0][0])[0])
            (resolved if ok else unresolved).append(token)
    return {"resolved": resolved, "unresolved": unresolved, "no_path_items": no_path}


# ---------------------------------------------------------------------------
# E-073 step 2 (D-083): value-checked citations, under
# orchestrator.observable_backtest only (the flag is read by the orchestrator,
# never here). resolve_evidence_paths above stays record-only and unchanged;
# check_citation_values also compares the value a reader wrote after a path
# with the value at that path in the file it received.
# ---------------------------------------------------------------------------

CITATION_VALUE_RULE = (
    "A citation is a field path from a file the reader received (rooted at a known root, a "
    "top-level key of that file, or the file's own name, e.g. grid_evaluation.grid.<...>) "
    "followed by `=` or `:` and a value. Keys are written as the file has them (2022-09 "
    "included); a key with spaces or other characters goes in quoted brackets, "
    "x[\"a key\"]. The path must exist, with every level written out: a shortened path is "
    "missing even when its last key exists elsewhere (the nearest real paths are suggested). "
    "Only the first value after the path is checked. A number matches when it is the file's "
    "value rounded to the digits the reader wrote (within half a unit of its last digit) if "
    "the reader wrote at least 2 significant digits; with fewer (0, 0.9, 3k), the file's "
    "value must round to it at 2 decimals as well (a cited 0 matches |x| < 0.005). A trailing "
    "% also matches the value x 100, a k / M suffix multiplies by 1e3 / 1e6, and approx / "
    "about / ~ in front is ignored. Text matches ignoring case: the file's text must start "
    "the cited value, or a cited quote of 20 characters or more must be part of it; booleans "
    "and null match their words. With [*] any element may match. A path rooted at the file "
    "named first, else at the first received file that has it (the reader's own report "
    "first). A path to a mapping or list, or a path with no value after it, is not "
    "value-checked.")
# The data dictionary's relative roots that are not a received file
# (docs/DATA_DICTIONARY_READERS.md: `summary.` / `trades[]` of
# trade_diagnostics.json, which no reader receives, and the report-relative
# `slices.`): a path rooted there is a citation, MISSING unless a received
# file has that top-level key -- with the received file's real path suggested
# (the trade_efficiency report's variants.<v>.slices.overall.* for summary.*).
CITATION_DICTIONARY_ROOTS = frozenset({"summary", "trades", "slices"})
CITATION_MAX_SUGGESTIONS = 3
CITATION_QUOTE_MIN_CHARS = 20
# artifacts/citation_checks/<category>.yaml: the last check of each reading
# (run_phase1_research writes it; decide_next reads the flagged side findings)
CITATION_CHECKS_DIR = "citation_checks"
CITATION_MATCH = "match"
CITATION_MISMATCH = "mismatch"
CITATION_MISSING = "missing"
CITATION_PATH_ONLY = "path_only"          # resolved, no value written after it
CITATION_NOT_A_VALUE = "not_a_value"      # resolved to a mapping or list only
CITATION_BAD = (CITATION_MISMATCH, CITATION_MISSING)
_CITE_SEP_RE = re.compile(r"\s*[=:]\s*")
_CITE_NUMBER_RE = re.compile(
    r"(?:(?:[Aa]pprox(?:imately|\.)?|[Aa]bout)\s*|[~≈]\s*)?"
    r"(?P<num>[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d*)?(?:[eE][-+]?\d+)?"
    r"|[-+−]?\.\d+(?:[eE][-+]?\d+)?)(?P<mult>[kKM](?![A-Za-z0-9_]))?(?P<pct>\s*%)?")
_CITE_MULT = {"k": 3, "K": 3, "M": 6}
_CITE_WORD_RE = re.compile(r"[^\s,;()\[\]{}]+")
_FLOAT_EPS = 1e-9
# The value check's own tokenizer (review fix 2). A key may hold inner hyphens
# (trade_efficiency's YYYY-MM per_window keys, the only non-word key character
# in run_060..run_079's report/grid/config keys); any other key (spaces, dots:
# LLM-written card keys) is cited in quoted brackets, x["a key"]. The
# record-only resolver above keeps _CITE_TOKEN_RE unchanged: its output is
# recorded under another flag (score provenance) and must not move here.
_CITE_V_KEY = r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*"
_CITE_V_BRACKET = r"""\[(?:"[^"\]]*"|'[^'\]]*'|[^\]\s]*)\]"""
_CITE_VALUE_TOKEN_RE = re.compile(
    rf"(?<![\w.\]\[/])[A-Za-z_][A-Za-z0-9_]*(?:{_CITE_V_BRACKET})*"
    rf"(?:\.{_CITE_V_KEY}(?:{_CITE_V_BRACKET})*)+")
_CITE_VALUE_STEP_RE = re.compile(rf"\.?({_CITE_V_KEY})((?:{_CITE_V_BRACKET})*)")
_CITE_V_BRACKET_RE = re.compile(r"""\[("[^"\]]*"|'[^'\]]*'|[^\]\s]*)\]""")
_CITE_V_PLAIN_KEY_RE = re.compile(rf"{_CITE_V_KEY}")
_CITE_V_ROOT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _cite_value_steps(token: str) -> list:
    """[(key, [bracket contents...]), ...] for one value-check path token;
    the quotes of a quoted bracket key are removed."""
    out = []
    for m in _CITE_VALUE_STEP_RE.finditer(token):
        brackets = [b[1:-1] if len(b) >= 2 and b[0] == b[-1] and b[0] in "'\"" else b
                    for b in _CITE_V_BRACKET_RE.findall(m.group(2))]
        out.append((m.group(1), brackets))
    return out


def _cite_values(node, steps: list) -> list:
    """Every value at `steps` below `node` ([] when the path does not exist);
    the value-collecting twin of _cite_walk (same step and bracket rules)."""
    if not steps:
        return [node]
    key, brackets = steps[0]
    found, value = _cite_get(node, key)
    return _cite_values_brackets(value, brackets, steps[1:]) if found else []


def _cite_values_brackets(node, brackets: list, rest: list) -> list:
    if not brackets:
        return _cite_values(node, rest)
    b, more = brackets[0], brackets[1:]
    if b in ("*", ""):
        if not isinstance(node, list):
            return []
        if not more and not rest:
            return [node]
        return [v for el in node for v in _cite_values_brackets(el, more, rest)]
    if b.isdigit() and isinstance(node, list):
        i = int(b)
        return _cite_values_brackets(node[i], more, rest) if i < len(node) else []
    found, value = _cite_get(node, b)  # a mapping key (quoted, or a digit key of a mapping)
    return _cite_values_brackets(value, more, rest) if found else []


def _file_stem(rel: str) -> str:
    name = str(rel).replace("\\", "/").rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[0] if "." in name else name


def _cited_text(item: str, end: int):
    """The value text written after a path token ending at `end`, or None
    when no `=` / `:` follows it (then the path alone is cited)."""
    m = _CITE_SEP_RE.match(item, end)
    if not m:
        return None
    rest = item[m.end():].strip()
    return rest or None


def _strip_quotes(text: str) -> str:
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"`":
        return text[1:-1]
    for q in "'\"`":
        if text.startswith(q) and q in text[1:]:
            return text[1:text.index(q, 1)]
    return text


def value_matches(cited: str, actual) -> bool:
    """Whether the value text a reader wrote matches one scalar `actual` (the
    CITATION_VALUE_RULE). Pure. `cited` is the text after the separator."""
    import math
    from decimal import Decimal, InvalidOperation
    text = cited.strip()
    word_m = _CITE_WORD_RE.match(_strip_quotes(text))
    word = word_m.group(0).rstrip(".") if word_m else ""
    if isinstance(actual, bool):
        return word.lower() == ("true" if actual else "false")
    if actual is None:
        return word.lower() in ("null", "none", "~")
    if isinstance(actual, (int, float)):
        if isinstance(actual, float) and math.isnan(actual):
            return word.lower() in ("nan", ".nan")
        if isinstance(actual, float) and math.isinf(actual):
            return word.lower().lstrip("+-") in ("inf", ".inf", "infinity")
        m = _CITE_NUMBER_RE.match(_strip_quotes(text))
        if not m:
            return False
        raw = m.group("num").replace(",", "").replace("−", "-")
        try:
            dec = Decimal(raw)
        except InvalidOperation:
            return False
        if m.group("mult"):  # 3.3k = 3.3E+3: the reader's precision scales with it
            dec = dec.scaleb(_CITE_MULT[m.group("mult")])
        digits = dec.as_tuple().digits
        tol = 0.5 * 10.0 ** dec.as_tuple().exponent
        significant = len(digits) - next((i for i, d in enumerate(digits) if d), len(digits))
        if significant < 2:
            # 0, 0.9, 3k: too coarse on its own (a cited 0 would match any
            # |x| < 0.5) -- the file's value must also round to it at 2 decimals
            tol = min(tol, 0.005)
        value = float(dec)
        candidates = [float(actual)] + ([float(actual) * 100.0] if m.group("pct") else [])
        return any(abs(c - value) <= tol + _FLOAT_EPS * max(1.0, abs(c)) for c in candidates)
    target = str(actual).casefold()
    body = _strip_quotes(text).casefold()
    if body == target:
        return True
    if len(body) >= CITATION_QUOTE_MIN_CHARS and body in target:
        return True  # a quote of the file's text
    if not body.startswith(target):
        return False
    nxt = body[len(target):len(target) + 1]
    return not (nxt.isalnum() or nxt in "_-.")


def _short(value, limit: int = 80):
    """A value as recorded in a check: scalars as they are, containers named."""
    if isinstance(value, dict):
        return "<mapping>"
    if isinstance(value, list):
        return "<list>"
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + "..."
    return value


def _cite_index(docs: dict) -> list:
    """Every mapping key of every received document, as [{file, path, keys,
    values}] in file then document order: `path` written the way a citation
    is (rooted at the file's top-level key, list elements as [*], a key the
    tokenizer cannot read as x["key"] -- at the top level behind the file
    stem), `keys` the key names along it, `values` the scalars found there
    (every element's, for a [*] path)."""
    index, at = [], {}

    def _entry(rel, path, keys):
        key = (rel, path)
        if key not in at:
            at[key] = {"file": rel, "path": path, "keys": keys, "values": []}
            index.append(at[key])
        return at[key]

    def _walk(rel, node, path, keys):
        if isinstance(node, dict):
            for k, v in node.items():
                name = str(k)
                plain = (_CITE_V_PLAIN_KEY_RE if path else _CITE_V_ROOT_RE).fullmatch(name)
                step = (f"{path}.{name}" if path else name) if plain else \
                    f'{path or _file_stem(rel)}["{name}"]'
                entry = _entry(rel, step, keys + (name,))
                if not isinstance(v, (dict, list)):
                    entry["values"].append(v)
                _walk(rel, v, step, keys + (name,))
        elif isinstance(node, list):
            for el in node:
                if isinstance(el, (dict, list)):
                    _walk(rel, el, f"{path}[*]", keys)
                else:
                    _entry(rel, f"{path}[*]", keys)["values"].append(el)

    for rel, d in docs.items():
        _walk(rel, d, "", ())
    return index


def _cite_suggestions(index: list, steps: list, cited) -> list:
    """The nearest real paths for a missing citation (review fix 1): the
    received fields whose LAST key is the cited path's last key, ranked by
    (the cited value matches there, trailing keys in common, keys in common
    -- the file stem counts --, fewest extra levels, file then document
    order); at most CITATION_MAX_SUGGESTIONS. Generic, no per-field rule;
    never makes the citation valid -- it stays missing until the reader
    corrects it. [] when no received field has that last key."""
    leaf = steps[-1][0]
    wrote = [k for k, _b in steps]
    ranked = []
    for n, e in enumerate(index):
        if not e["keys"] or e["keys"][-1] != leaf:
            continue
        keys = e["keys"]
        common_tail = 0
        for a, b in zip(reversed(wrote), reversed(keys)):
            if a != b:
                break
            common_tail += 1
        shared = len(set(wrote) & (set(keys) | {_file_stem(e["file"])}))
        value_ok = cited is not None and any(value_matches(cited, v) for v in e["values"])
        ranked.append(((not value_ok, -common_tail, -shared, abs(len(keys) - len(wrote)), n),
                       e, value_ok))
    out = []
    for _key, e, value_ok in sorted(ranked, key=lambda r: r[0])[:CITATION_MAX_SUGGESTIONS]:
        s = {"path": e["path"], "file": e["file"], "value_matches": value_ok}
        distinct = {repr(v): v for v in e["values"]}
        if len(distinct) == 1:
            s["value"] = _short(next(iter(distinct.values())))
        out.append(s)
    return out


def _cite_found(docs: dict, stems: dict, steps: list) -> list:
    """[(file, value)] at a cited path, from ONE file (review fix 5): the
    file the path names (its stem as the root) first; else the first
    received file, in the received order (the reader's own report first),
    in which the path resolves. [] when none."""
    found = []
    if not steps[0][1] and len(steps) > 1:  # the file's own name as the root
        for rel in stems.get(steps[0][0], ()):
            found += [(rel, v) for v in _cite_values(docs[rel], steps[1:])]
    if found:
        return found
    for rel, d in docs.items():
        if _cite_get(d, steps[0][0])[0]:
            values = _cite_values(d, steps)
            if values:
                return [(rel, v) for v in values]
    return []


def check_citation_values(received_files: dict, evidence: list) -> dict:
    """E-073 step 2 (D-083): every cited path in `evidence` checked against
    the value at that path in the files the reader received (the
    CITATION_VALUE_RULE). Pure; reads no file and never rejects.

    `received_files`: {file rel path: parsed document}, exactly the files the
    reader was given (under E-072 the exploration copies), IN PREFERENCE
    ORDER: the reader's own report first (as _reader_received_files builds
    it). A path is rooted at CITATION_ROOTS, CITATION_DICTIONARY_ROOTS, a
    top-level key of a received file, or a received file's stem
    (`grid_evaluation.grid.residual_ic.base.value` walks inside
    grid_evaluation.yaml); it is looked up in the file it names, else in the
    first received file where it resolves (_cite_found). Keys may hold inner
    hyphens or be quoted in brackets (_CITE_VALUE_TOKEN_RE). Only the first
    value after the path is compared; with [*] any element may match.
    Returns {"citations": [{path, cited, status, actual?, files?,
    suggestions?}], "bad": [...the mismatch / missing ones...],
    "no_path_items": n}; each (path, cited value) pair once, in first-seen
    order. A missing path carries `suggestions` (_cite_suggestions; [] when
    nothing has its last key) -- still missing. A malformed argument raises
    TypeError for the caller to record."""
    if not isinstance(received_files, dict):
        raise TypeError("received_files must be a mapping of file name -> document")
    if not isinstance(evidence, list):
        raise TypeError("evidence must be a list of strings")
    docs = {str(rel): d for rel, d in received_files.items() if isinstance(d, dict)}
    stems = {}
    for rel, d in docs.items():
        stems.setdefault(_file_stem(rel), []).append(rel)
    roots = (set(CITATION_ROOTS) | set(CITATION_DICTIONARY_ROOTS)
             | {str(k) for d in docs.values() for k in d} | set(stems))
    out, seen, no_path, index = [], set(), 0, None
    for item in evidence:
        matches = ([m for m in _CITE_VALUE_TOKEN_RE.finditer(item)
                    if _cite_value_steps(m.group(0))[0][0] in roots]
                   if isinstance(item, str) else [])
        if not matches:
            no_path += 1
            continue
        for m in matches:
            token = m.group(0)
            cited = _cited_text(item, m.end())
            if (token, cited) in seen:
                continue
            seen.add((token, cited))
            steps = _cite_value_steps(token)
            found = _cite_found(docs, stems, steps)  # (rel, value)
            rec = {"path": token, "cited": cited}
            if not found:
                rec["status"] = CITATION_MISSING
                index = _cite_index(docs) if index is None else index
                rec["suggestions"] = _cite_suggestions(index, steps, cited)
            elif cited is None:
                rec["status"] = CITATION_PATH_ONLY
            else:
                scalars = [(rel, v) for rel, v in found if not isinstance(v, (dict, list))]
                if not scalars:
                    rec["status"] = CITATION_NOT_A_VALUE
                elif any(value_matches(cited, v) for _rel, v in scalars):
                    rec["status"] = CITATION_MATCH
                else:
                    rec["status"] = CITATION_MISMATCH
                    rec["actual"] = [_short(v) for _rel, v in scalars[:3]]
                    rec["files"] = sorted({rel for rel, _v in scalars})
            out.append(rec)
    return {"citations": out, "bad": [r for r in out if r["status"] in CITATION_BAD],
            "no_path_items": no_path}
