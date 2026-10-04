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
