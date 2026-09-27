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

import re
from pathlib import Path

import yaml

SCORE_KEYS = ("confidence_real", "distance_to_profitable", "mechanism_plausibility")
_PROPOSAL_KEYS = frozenset(
    {"proposal_id", "kind", "patch", "block", "evidence", "scores", "model_id", "rubric_version",
     "requires_feed"})
_PATCH_ITEM_KEYS = frozenset({"component_id", "field", "before", "after"})
_BLOCK_KEYS = frozenset({"kind", "config_paths", "scaffolding", "rationale"})
_PROPOSAL_ID_RE = re.compile(r"^[a-z_]+-.+-[0-9]+$")
# E-035 S2c: the optional `requires_feed` field, orthogonal to `kind`.
REQUIRES_FEED_KEYS = frozenset({"feed", "reason"})
# A feed is named as a strategy config's aux_feeds entry names it (a
# trading-bot FEED_REGISTRY key) -- lowercase snake_case, so it compares
# exactly against the registry's keys.
FEED_NAME_RE = re.compile(r"[a-z][a-z0-9_]*")


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


def _check_proposal(p, cat: str, where: str) -> None:
    if not isinstance(p, dict):
        raise ProposalError(f"{where}: proposal is not a mapping")
    extra = sorted(set(p) - _PROPOSAL_KEYS)
    if extra:
        raise ProposalError(f"{where}: undeclared field(s) {extra} (readers never route or decide)")
    for key in ("model_id", "rubric_version"):
        if not _non_empty_str(p.get(key)):
            raise ProposalError(f"{where}: {key} must be a non-empty string")
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
        blk = p.get("block")
        if not isinstance(blk, dict) or "patch" in p or blk.get("kind") not in ("forecast", "regime"):
            raise ProposalError(f"{where}: kind=new_block requires a `block` mapping with kind "
                                f"forecast|regime, and no `patch`")
        if sorted(set(blk) - _BLOCK_KEYS) or not isinstance(blk.get("rationale"), str):
            raise ProposalError(f"{where}: block must carry a string rationale and no undeclared field")
        paths = blk.get("config_paths")
        if not isinstance(paths, list) or not paths or not all(_non_empty_str(x) for x in paths):
            raise ProposalError(f"{where}: block.config_paths must be a non-empty list of strings")
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


def load_proposals(proposals_dir: Path, categories: list) -> dict:
    """{category: [proposal, ...]} for every category. A missing file and `[]`
    both mean "no proposals" (an honest reader output). Everything else that
    is not a well-formed list of proposals raises ProposalError, including an
    empty/null file, a non-list document, a duplicate or foreign-category
    proposal_id, and an unexpected *.yaml/*.yml in the directory (a mis-named
    file would otherwise be silently skipped). OS/editor litter is ignored."""
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
            _check_proposal(p, cat, f"{path}[{n}]")
            if p["proposal_id"] in seen:
                raise ProposalError(f"{path}[{n}]: duplicate proposal_id {p['proposal_id']!r}")
            seen.add(p["proposal_id"])
        out[cat] = data
    return out
