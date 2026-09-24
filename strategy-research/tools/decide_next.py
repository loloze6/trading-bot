"""
decide_next -- pick the next idea to run (E-059 S2a, delivery_plan_v26.md
slice 6b "decide-next and the queue"; spec:
engineering/roadmap/E-059/S1_FINDINGS_6B.md and its operator decision of
2026-09-24, which overrides the recommendations above it).

Called by run_campaign.process_once's DONE branch under
orchestrator.decide_next.enabled (off by default), after a run's queue entry
is marked done. Three pure steps and one loader:

  load_inputs(root, queue, ...) -> inputs   reads the campaign memory, the block
                                            registry revision, every reader
                                            proposal a memory entry references,
                                            and each source run's base config,
                                            block manifest, pre-registration,
                                            research brief and card.
  decide(inputs, now=, trigger=) -> record  the decision record
                                            (runs/<run>/artifacts/decision_record.yaml).
  candidate_brief(record, inputs) -> (rel_path, text)
                                            the brief file for a picked candidate.

What decides, in order:
  1. An operator-registered `ready` entry (no `origin`, or `origin: external`)
     always goes first, by priority, with no ranking (operator decision 4).
     An agent entry that is already `ready` is picked next (idempotence).
  2. Otherwise every reader proposal still in the pool (referenced by a memory
     entry, not yet named by a queue entry's `proposal_ref`) becomes a
     candidate. A patch is resolved against its source run's base config.
     Gates: novelty -- the EXACT match of card K (config hash + symbols +
     timeframe + protocol) against campaign memory, BINDING (operator decision
     3); the legacy exclusion digest's layer 2 is recorded for information
     only and never refuses; its layer 1 is not called. Feasibility -- the
     patch resolves, the manifest still resolves, no unknown component class;
     a regime block is infeasible before slice 7.
  3. Eligible candidates are ranked: confidence_real desc,
     distance_to_profitable desc, cost (backtests) asc, candidate_id asc.
     There is NO lineage-depth demotion (operator decision 6, dropped).
  4. Nothing eligible and no operator entry -> stop.

What this module deliberately does NOT do:
  * decide or change an idea's status. The status comes only from the grid
    (idea_status.yaml, copied into memory). Proposal scores only RANK; they
    are copied into the decision record and nowhere else.
  * inherit criteria. Operator decision 2: a picked candidate enters step 1a,
    which writes a card and criteria coherent with the proposed idea from the
    criterion menu. The brief therefore carries no pass_rule; it carries
    `candidate.criteria_from: hypothesis_generation`, and the run's
    pre_registration.yaml is written pending at 1a (run_campaign._materialize_run,
    run_phase1_research._write_pass_rule_from_card). A patch's resolved config
    passes through to 1b; a new_block is authored at 1b.
  * refine/pivot/escalate/kill routing, the circuit breaker,
    hypothesis_family, altitude_history, continuation children (retired in
    slice 6c). The record refuses to carry any of them.
  * R1 (composition brief): recorded as a no-op until slice 7. R2 (ask 1a
    for more hypotheses on open briefs), brief exhaustion and multi-card
    briefs: E-059 S2b.
  * write trial rows, touch the holdout, or write any file. The caller writes.

Importable without the orchestrator: every path is passed in by the caller.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import math
import re
from pathlib import Path

import yaml

import block_registry as _br  # tools/ sibling: registry loader (revision for R1)
import campaign_memory as _cm  # tools/ sibling: memory loader + retired-field scan
import json_pointer as _jp  # tools/ sibling: pointer + patch semantics shared with 5a
import reader_proposals as _rp  # tools/ sibling: proposal loader/validator

SCHEMA_VERSION = 1
ORIGIN_READER = "reader"
CRITERIA_FROM_1A = "hypothesis_generation"
CANDIDATE_BRIEFS_DIR = "campaign_record/candidate_briefs"
AGENT_PRIORITY = 999
# Card D: base + design + asset variant.
N_VARIANTS = 3
# E-039 S1_FINDINGS.md L113-121: median 3m45s for 22 backtests (11 windows x 2
# symbols, local-cache 1h protocol) -> ~10.2 s per window-symbol backtest. A
# single constant cannot change the rank; it is recorded for the reader.
SECONDS_PER_BACKTEST = 10.2
COST_BASIS_SOURCE = "E-039 S1_FINDINGS.md L113-121"
# Operator-registered entries: no origin, or an explicit external one.
_OPERATOR_ORIGINS = (None, "external")
_FIELD_PART_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)((?:\[\d+\])*)$")


class DecideNextError(ValueError):
    """An input decide_next needs is malformed. Never caught here."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def config_sha256(config) -> str:
    """The run_phase1_research._compute_forecast_hash canonicalisation
    (json.dumps(..., sort_keys=True), sha256) applied to an in-memory config,
    so a resolved candidate config hashes exactly as its trial row will."""
    return hashlib.sha256(json.dumps(config, sort_keys=True).encode("utf-8")).hexdigest()


def _canonical_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def known_component_classes(trading_bot_root: Path) -> list:
    """Dotted class paths defined at the top level of
    trading-bot/strategies/strategy_components.py, read with ast (no import of
    the engine). The same module 5a's V12 check loads classes from."""
    path = Path(trading_bot_root) / "strategies" / "strategy_components.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return sorted(f"strategies.strategy_components.{n.name}"
                  for n in tree.body if isinstance(n, ast.ClassDef))


def _component_classes(config) -> set:
    out = set()
    if not isinstance(config, dict):
        return out
    for comp in ((config.get("regime_detector") or {}).get("components") or []):
        if isinstance(comp, dict) and comp.get("class"):
            out.add(comp["class"])
    for rcfg in (((config.get("strategies") or {}).get("regimes")) or {}).values():
        for comp in ((rcfg or {}).get("components") or []):
            if isinstance(comp, dict) and comp.get("class"):
                out.add(comp["class"])
    return out


def _escape(seg: str) -> str:
    return str(seg).replace("~", "~0").replace("/", "~1")


def _component_pointers(config, component_id: str) -> list:
    """Every JSON pointer of a component whose `id` is component_id, under
    /strategies/regimes/*/components/* and /regime_detector/components/*."""
    found = []
    if not isinstance(config, dict):
        return found
    for i, comp in enumerate((config.get("regime_detector") or {}).get("components") or []):
        if isinstance(comp, dict) and comp.get("id") == component_id:
            found.append(f"/regime_detector/components/{i}")
    for rname, rcfg in sorted((((config.get("strategies") or {}).get("regimes")) or {}).items()):
        for i, comp in enumerate((rcfg or {}).get("components") or []):
            if isinstance(comp, dict) and comp.get("id") == component_id:
                found.append(f"/strategies/regimes/{_escape(rname)}/components/{i}")
    return found


def field_to_pointer_suffix(field: str) -> str:
    """A reader's dotted `field` (`transforms[2].params.min_abs`) as a JSON
    pointer suffix (`/transforms/2/params/min_abs`). Raises DecideNextError on
    any other syntax."""
    if not isinstance(field, str) or not field:
        raise DecideNextError(f"field {field!r} is not a non-empty string")
    segs = []
    for part in field.split("."):
        m = _FIELD_PART_RE.match(part)
        if not m:
            raise DecideNextError(f"field {field!r}: segment {part!r} is not name or name[i]")
        segs.append(_escape(m.group(1)))
        segs.extend(re.findall(r"\[(\d+)\]", m.group(2)))
    return "/" + "/".join(segs)


def resolve_patch(proposal: dict, base_config: dict) -> tuple:
    """(ops, patched_config, None) when every item of a reader patch resolves,
    else (None, None, reason). Each item needs exactly one component with that
    `id`, a `field` that resolves inside it, and a current value equal to
    `before`; it then becomes {path, value: after}, applied with 5a's own
    semantics (json_pointer.apply_json_pointer_patch)."""
    ops = []
    for k, item in enumerate(proposal.get("patch") or []):
        ptrs = _component_pointers(base_config, item.get("component_id"))
        if len(ptrs) != 1:
            return None, None, (f"patch_unresolvable: patch[{k}] component_id "
                                f"{item.get('component_id')!r} matches {len(ptrs)} components")
        try:
            path = ptrs[0] + field_to_pointer_suffix(item.get("field"))
            current = _jp.resolve_json_pointer(base_config, path)
        except (DecideNextError, _jp.JsonPointerError) as exc:
            return None, None, f"patch_unresolvable: patch[{k}] field {item.get('field')!r}: {exc}"
        if current != item.get("before"):
            return None, None, (f"stale_before: patch[{k}] {path} is {current!r}, "
                                f"the proposal says before={item.get('before')!r}")
        ops.append({"path": path, "value": item.get("after")})
    try:
        patched = _jp.apply_json_pointer_patch(base_config, ops)
    except _jp.PatchApplicationError as exc:
        return None, None, f"patch_unresolvable: {exc}"
    return ops, patched, None


def _base_variant(entry: dict) -> tuple:
    """(variant_id, variant) of a memory entry's base variant: the single
    run_id column when the variant loop was off, else json_pointer's rule."""
    variants = entry.get("variants") or {}
    if not variants:
        return None, None
    run_id = entry.get("run_id")
    vid = run_id if list(variants) == [run_id] else _jp.base_variant_id(variants)
    return vid, variants.get(vid)


def _exact_index(memory: dict) -> dict:
    """{(forecast_hash, symbols, timeframe, protocol_ref): [run_id, ...]} over
    every TESTED variant in the memory. Legacy runs are not in memory, so they
    can never match (slice 8.1)."""
    index: dict = {}
    for run_id in sorted((memory.get("runs") or {})):
        entry = memory["runs"][run_id]
        if entry.get("engineering_fault"):
            continue
        for v in (entry.get("variants") or {}).values():
            if v.get("status") != "tested" or not v.get("forecast_hash"):
                continue
            key = (v["forecast_hash"], tuple(sorted(v.get("symbols") or [])),
                   entry.get("timeframe"), entry.get("protocol_ref"))
            runs = index.setdefault(key, [])
            if run_id not in runs:
                runs.append(run_id)
    return index


def _load_yaml_opt(path: Path):
    path = Path(path)
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_inputs(root: Path, queue: dict, *, categories: list, known_classes=None,
                digest=None) -> dict:
    """Everything decide() reads, from disk under `root` (strategy-research/).
    `queue` is the caller's in-memory queue document (after its own write).
    `known_classes` is the known component class set (known_component_classes)
    or None; `digest` the legacy exclusion digest document or None."""
    root = Path(root)
    mem_path = root / "campaign_record" / "campaign_memory.yaml"
    memory = _cm.load_memory(mem_path)
    registry = _br.load_registry(root / "campaign_record" / "block_registry.yaml")
    runs = {}
    for run_id in sorted(memory.get("runs") or {}):
        entry = memory["runs"][run_id]
        if entry.get("engineering_fault") or not any(
                (p or {}).get("count") for p in (entry.get("proposals") or [])):
            continue
        run_dir = root / "runs" / run_id
        arts = run_dir / "artifacts"
        loaded = _rp.load_proposals(arts / "proposals", list(categories))
        proposals = [{"category": cat, "proposal": p}
                     for cat in categories for p in loaded.get(cat) or []]
        base_vid, base = _base_variant(entry)
        base_config, base_ref = None, None
        if base and base.get("config_ref"):
            base_ref = base["config_ref"]
            cfg_path = root / base_ref
            if cfg_path.exists():
                base_config = json.loads(cfg_path.read_text(encoding="utf-8"))
        runs[run_id] = {
            "proposals": proposals,
            "base_variant": base_vid,
            "base_config": base_config,
            "base_config_ref": base_ref,
            "manifest": _load_yaml_opt(arts / "block_manifest.yaml"),
            "pre_registration": _load_yaml_opt(arts / "pre_registration.yaml"),
            "research_brief": _load_yaml_opt(arts / "research_brief.yaml"),
            "card": _load_yaml_opt(arts / "hypothesis_card.yaml"),
        }

    def _count(name):
        doc = _load_yaml_opt(root / "campaign_record" / name) or {}
        return len(doc.get("requests") or []) if isinstance(doc, dict) else 0

    return {
        "memory": memory,
        "memory_sha256": (hashlib.sha256(mem_path.read_bytes()).hexdigest()
                          if mem_path.exists() else None),
        "registry_revision": registry.get("revision", 0),
        "queue": copy.deepcopy(queue),
        "known_classes": sorted(known_classes) if known_classes is not None else None,
        "digest": digest,
        "runs": runs,
        "component_requests_count": _count("component_requests.yaml"),
        "data_requests_count": _count("data_requests.yaml"),
    }


# ---------------------------------------------------------------------------
# The decision
# ---------------------------------------------------------------------------

def _digest_advisory(card, config, symbols, timeframe, digest) -> dict:
    """Legacy exclusion digest, layer 2 only, INFORMATION ONLY (operator
    decision 3). Its fingerprint ignores transforms, so it would call most
    reader patches a repeat; it never refuses here."""
    if not digest or not isinstance(card, dict):
        return {"outcome": "not_available", "family": None, "family_confidence": None,
                "run_ids": []}
    import anti_adjacency_gate as _aag  # tools/ sibling, imported lazily
    res = _aag.layer2_digest_check(card, (symbols or [None])[0], timeframe, digest,
                                   candidate_config=config)
    run_ids = list(res.get("run_ids") or sorted(
        {r for n in res.get("neighbours") or [] for r in n.get("run_ids") or []}))
    return {"outcome": res.get("outcome"), "family": res.get("family"),
            "family_confidence": res.get("family_confidence"), "run_ids": run_ids}


def _candidate(run_id: str, entry: dict, src: dict, category: str, p: dict, inputs: dict,
               exact: dict) -> dict:
    pid = p["proposal_id"]
    parent = entry.get("hypothesis_id")
    _, base = _base_variant(entry)
    base = base or {}
    symbols = list(base.get("symbols") or [])
    n_windows = base.get("n_windows") or 0
    reasons = []
    resolved_sha, novelty = None, None
    config_for_digest = None
    pre_reg = src.get("pre_registration") or {}
    if not isinstance(pre_reg.get("machine_constraints"), dict):
        reasons.append("source_has_no_protocol_pin: the source pre_registration.yaml carries "
                       "no machine_constraints to pin the candidate's windows")
    if not isinstance(src.get("research_brief"), dict):
        reasons.append("source_brief_missing: the source research_brief.yaml is missing")
    if p["kind"] == "patch":
        if base.get("status") != "tested":
            reasons.append("source_base_variant_not_tested")
        if not isinstance(src.get("base_config"), dict):
            reasons.append("source_config_missing: the source base variant's config is not on disk")
        elif not isinstance(src.get("manifest"), dict):
            reasons.append("source_manifest_missing: a pass-through config needs the source "
                           "block_manifest.yaml")
        else:
            ops, patched, why = resolve_patch(p, src["base_config"])
            if why:
                reasons.append(why)
            else:
                config_for_digest = patched
                resolved_sha = config_sha256(patched)
                missing = _jp.manifest_missing_paths(patched, src["manifest"])
                if missing:
                    reasons.append(f"manifest_unresolved: {missing}")
                new_classes = _component_classes(patched) - _component_classes(src["base_config"])
                if new_classes and inputs.get("known_classes") is not None:
                    unknown = sorted(new_classes - set(inputs["known_classes"]))
                    if unknown:
                        reasons.append(f"unknown_component_class: {unknown}")
                elif new_classes:
                    reasons.append(f"unknown_component_class: {sorted(new_classes)} "
                                   f"(no known class set was supplied)")
        if resolved_sha:
            key = (resolved_sha, tuple(sorted(symbols)), entry.get("timeframe"),
                   entry.get("protocol_ref"))
            matched = list(exact.get(key) or [])
            novelty = {"exact_match": "REPEAT" if matched else "NOVEL", "matched_runs": matched}
        else:
            novelty = {"exact_match": "NOT_EVALUATED", "matched_runs": []}
        feas = "INFEASIBLE" if reasons else "FEASIBLE"
    else:
        blk = p.get("block") or {}
        if blk.get("kind") == "regime":
            reasons.append("regime_block_needs_composition: a regime block is validated only "
                           "as a composition variant (cards A/F, slice 7)")
        novelty = {"exact_match": "NOT_APPLICABLE", "matched_runs": [],
                   "note": "no config until 1b authors it"}
        feas = "INFEASIBLE" if reasons else "UNKNOWN"
        if not reasons:
            reasons.append("config authored at 1b; step 3's data gate stays binding")
    novelty["digest_advisory"] = _digest_advisory(
        src.get("card"), config_for_digest, symbols, entry.get("timeframe"), inputs.get("digest"))
    backtests = n_windows * N_VARIANTS * len(symbols) if (n_windows and symbols) else None
    eligible = novelty["exact_match"] != "REPEAT" and feas != "INFEASIBLE"
    return {
        "candidate_id": pid,
        "origin": ORIGIN_READER,
        "kind": p["kind"],
        "category": category,
        "source_run": run_id,
        "parent_hypothesis_id": parent,
        "hypothesis_id": f"{parent}__{pid}",
        "proposal_ref": f"runs/{run_id}/artifacts/proposals/{category}.yaml#{pid}",
        "collapsed_sources": [],
        "scores": {**{k: p["scores"][k] for k in _rp.SCORE_KEYS},
                   "model_id": p.get("model_id"), "rubric_version": p.get("rubric_version")},
        "resolved_config_sha256": resolved_sha,
        "gates": {"novelty": novelty,
                  "feasibility": {"result": feas, "reasons": reasons}},
        "eligible": eligible,
        "cost": {
            "backtests": backtests,
            "seconds_estimate": (round(backtests * SECONDS_PER_BACKTEST)
                                 if backtests is not None else None),
            "basis": (f"{n_windows} windows x {N_VARIANTS} variants x {len(symbols)} symbol(s) "
                      f"x {SECONDS_PER_BACKTEST} s ({COST_BASIS_SOURCE})"
                      if backtests is not None else "source run has no tested windows/symbols"),
        },
        "rank": None,
    }


def _score_key(c: dict) -> tuple:
    return (-c["scores"]["confidence_real"], -c["scores"]["distance_to_profitable"],
            c["candidate_id"])


def _collapse(cands: list) -> list:
    """Card I: candidates that are the same thing collapse into one, keeping
    the highest score tuple. Patches: identical resolved config hash. Sketches:
    identical kind + config_paths from the same source run."""
    groups, order = {}, []
    for c in cands:
        if c["kind"] == "patch" and c["resolved_config_sha256"]:
            key = ("patch", c["resolved_config_sha256"])
        elif c["kind"] == "new_block":
            key = ("new_block", c["_block_key"])
        else:
            key = ("single", c["candidate_id"])
        if key not in groups:
            order.append(key)
        groups.setdefault(key, []).append(c)
    out = []
    for key in order:
        members = sorted(groups[key], key=_score_key)
        keep = members[0]
        keep["collapsed_sources"] = sorted(m["proposal_ref"] for m in members[1:])
        out.append(keep)
    return out


def rank_key(c: dict) -> tuple:
    """confidence_real desc, distance_to_profitable desc, cost asc (unknown
    cost last), candidate_id asc. mechanism_plausibility is recorded, not
    ranked on (the plan's key). No lineage term (operator decision 6)."""
    cost = c["cost"]["backtests"]
    return (-c["scores"]["confidence_real"], -c["scores"]["distance_to_profitable"],
            cost if cost is not None else math.inf, c["candidate_id"])


def _operator_entries(queue: dict) -> list:
    entries = [e for e in (queue.get("queue") or []) if isinstance(e, dict)
               and e.get("status") == "ready" and e.get("origin") in _OPERATOR_ORIGINS]
    return sorted(entries, key=lambda e: e.get("priority", 999))  # stable, as _select_entry


def decide(inputs: dict, *, now: str, trigger: dict) -> dict:
    """The decision record. Pure: reads only `inputs`; the same inputs, `now`
    and `trigger` give the same record."""
    memory = inputs["memory"]
    queue = inputs["queue"]
    named = {e.get("proposal_ref") for e in (queue.get("queue") or [])
             if isinstance(e, dict) and e.get("proposal_ref")}
    exact = _exact_index(memory)

    cands = []
    for run_id in sorted(inputs.get("runs") or {}):
        src = inputs["runs"][run_id]
        entry = memory["runs"][run_id]
        for item in src["proposals"]:
            p, cat = item["proposal"], item["category"]
            ref = f"runs/{run_id}/artifacts/proposals/{cat}.yaml#{p['proposal_id']}"
            if ref in named:
                continue  # already in the queue: out of the pool (§3.7)
            c = _candidate(run_id, entry, src, cat, p, inputs, exact)
            if p["kind"] == "new_block":
                blk = p.get("block") or {}
                c["_block_key"] = (blk.get("kind"), tuple(sorted(blk.get("config_paths") or [])),
                                   run_id)
            cands.append(c)
    cands = _collapse(cands)
    for c in cands:
        c.pop("_block_key", None)
    eligible = sorted((c for c in cands if c["eligible"]), key=rank_key)
    for i, c in enumerate(eligible, 1):
        c["rank"] = i
    ineligible = sorted((c for c in cands if not c["eligible"]), key=lambda c: c["candidate_id"])

    operator = _operator_entries(queue)
    agent_ready = [e for e in (queue.get("queue") or []) if isinstance(e, dict)
                   and e.get("status") == "ready" and e.get("origin") not in _OPERATOR_ORIGINS]
    picked, stop = None, None
    if operator:
        picked = {"operator_entry": operator[0]["id"],
                  "why": "an operator-registered ready entry goes first, by priority, unranked"}
    elif agent_ready:
        picked = {"queue_entry_id": agent_ready[0]["id"],
                  "why": "an agent entry is already ready; nothing new is minted"}
    elif eligible:
        top = eligible[0]
        picked = {
            "candidate_id": top["candidate_id"],
            "queue_entry_id": top["candidate_id"],
            "brief_path": f"{CANDIDATE_BRIEFS_DIR}/{top['candidate_id']}.md",
            "why": (f"rank 1 of {len(eligible)} eligible: confidence_real="
                    f"{top['scores']['confidence_real']}, distance_to_profitable="
                    f"{top['scores']['distance_to_profitable']}, backtests="
                    f"{top['cost']['backtests']}"),
        }
    else:
        stop = {"reason": "no_eligible_candidate",
                "detail": (f"no operator ready entry, no ready agent entry, and 0 of "
                           f"{len(cands)} candidate(s) eligible")}

    revision = inputs.get("registry_revision") or 0
    known = inputs.get("known_classes")
    record = {
        "schema_version": SCHEMA_VERSION,
        "decided_at": now,
        "trigger": dict(trigger),
        "inputs": {
            "memory_sha256": inputs.get("memory_sha256"),
            "registry_revision": revision,
            "queue_sha256": _canonical_sha(queue),
            "known_component_classes_sha256": _canonical_sha(known) if known is not None else None,
            "component_requests": inputs.get("component_requests_count", 0),
            "data_requests": inputs.get("data_requests_count", 0),
        },
        "rules": {
            "r1": {"registry_revision": revision, "last_composition_revision": None,
                   "would_fire": revision >= 2, "fired": False,
                   "reason": "composition brief writer is slice 7"},
            "r2": {"fired": False, "open_briefs": [], "enqueued": [],
                   "reason": "R2 (1a requests on open briefs) is E-059 S2b"},
        },
        "operator_entries": [e["id"] for e in operator],
        "candidates": eligible + ineligible,
        "picked": picked,
        "stop": stop,
    }
    retired = _cm._find_retired(record)
    if retired:
        raise DecideNextError(f"decision record carries retired field(s) {retired}")
    return record


# ---------------------------------------------------------------------------
# The brief for a picked candidate
# ---------------------------------------------------------------------------

def _find_proposal(inputs: dict, run_id: str, pid: str) -> tuple:
    for item in (inputs["runs"].get(run_id) or {}).get("proposals") or []:
        if item["proposal"]["proposal_id"] == pid:
            return item["category"], item["proposal"]
    raise DecideNextError(f"proposal {pid!r} of {run_id} is not in the inputs")


def candidate_brief(record: dict, inputs: dict, *, decision_ref: str) -> tuple:
    """(rel_path, text) of the brief for record['picked'] (a candidate).
    Frontmatter: the source research brief's six required keys, a research
    goal built from the proposal, the source's machine_constraints (the
    window/protocol pin, which is part of the novelty key) WITHOUT any
    pass_rule, and `candidate` = {config + manifest (patch only), criteria_from:
    hypothesis_generation, source}. No criteria and no `evaluation`: step 1a
    writes them for the proposed idea (operator decision 2)."""
    picked = record.get("picked") or {}
    cid = picked.get("candidate_id")
    cand = next((c for c in record["candidates"] if c["candidate_id"] == cid), None)
    if cand is None:
        raise DecideNextError(f"picked candidate {cid!r} is not in the record")
    run_id = cand["source_run"]
    src = inputs["runs"][run_id]
    category, p = _find_proposal(inputs, run_id, cid)
    brief = src["research_brief"] or {}
    front = {k: brief.get(k) for k in ("strategy_domain", "market_universe", "timeframe",
                                       "venue", "product")}
    evidence = "; ".join(p.get("evidence") or [])
    if p["kind"] == "patch":
        changes = ", ".join(f"{i['component_id']}.{i['field']}: {i['before']!r} -> {i['after']!r}"
                            for i in p["patch"])
        goal = (f"Test a change proposed by the {category} reader after {run_id} on idea "
                f"{cand['parent_hypothesis_id']}: {changes}. Evidence: {evidence}")
    else:
        blk = p.get("block") or {}
        goal = (f"Test a new {blk.get('kind')} block proposed by the {category} reader after "
                f"{run_id}: {blk.get('rationale')} (config paths {blk.get('config_paths')}). "
                f"Evidence: {evidence}")
    front["research_goal"] = goal
    mc = copy.deepcopy((src["pre_registration"] or {}).get("machine_constraints") or {})
    mc.pop("pass_rule", None)  # never inherit criteria (operator decision 2)
    front["machine_constraints"] = mc
    source = {
        "origin": ORIGIN_READER,
        "proposal_ref": cand["proposal_ref"],
        "source_run": run_id,
        "parent_hypothesis_id": cand["parent_hypothesis_id"],
        "hypothesis_id": cand["hypothesis_id"],
        "decision_ref": decision_ref,
        "proposal": {k: copy.deepcopy(p[k]) for k in ("kind", "patch", "block", "evidence")
                     if k in p},
    }
    candidate = {}
    if p["kind"] == "patch":
        ops, patched, why = resolve_patch(p, src["base_config"])
        if why:
            raise DecideNextError(f"picked patch {cid!r} no longer resolves: {why}")
        candidate["config"] = patched
        candidate["manifest"] = copy.deepcopy(src["manifest"])
        source["resolved_patch"] = ops
        source["base_config_ref"] = src["base_config_ref"]
        source["expected_config_sha256"] = config_sha256(patched)
    candidate["criteria_from"] = CRITERIA_FROM_1A
    candidate["source"] = source
    front["candidate"] = candidate
    rel = picked["brief_path"]
    text = ("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n\n"
            f"# {cid}\n\n"
            f"Written by tools/decide_next.py (E-059, slice 6b) from {cand['proposal_ref']}; "
            f"decision record: {decision_ref}.\n\n"
            "This brief carries no pass criteria on purpose (operator decision 2, "
            "2026-09-24): step 1a writes a hypothesis card and criteria coherent with the "
            "proposed idea, from config/criterion_menu.yaml. A patch's resolved config "
            "passes through to 1b (candidate.config), and 5a checks it against "
            "candidate.source.expected_config_sha256.\n")
    return rel, text
