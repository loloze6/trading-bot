"""
decide_next -- pick the next idea to run (E-059 S2a, delivery_plan_v26.md
slice 6b "decide-next and the queue"; spec:
engineering/roadmap/E-059/S1_FINDINGS_6B.md and its operator decision of
2026-09-24, which overrides the recommendations above it).

Called by run_campaign._finish_lineage_with_decision under
orchestrator.decide_next.enabled (off by default), when a lineage finishes
(the DONE branch, or the E-030 quarantine path that marks it done), BEFORE the
finished entry is persisted as done (so a failure is retried). Three pure
steps and one loader:

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
  1. If the scheduler (run_campaign._select_entry, passed in) would still run
     an existing entry -- an in_progress one, else the lowest-priority ready
     one, operator or agent -- that entry is `picked` and nothing is minted,
     so the record always names what actually runs next (operator entries go
     first because nothing is minted while one is waiting; decision 4).
  2. Otherwise every reader proposal still in the pool (referenced by a memory
     entry, not yet named by a queue entry's `proposal_ref`) becomes a
     candidate. Its proposal_id must be a safe name '<category>-<run_id>-<n>'
     of its own source run and must not collide with a queue id or brief. A
     patch is resolved against its source run's base config. Gates: novelty
     -- the EXACT match of card K against campaign memory, BINDING (operator
     decision 3), keyed on (config hash, measured symbols, the protocol file's
     timeframe, a content hash of the protocol's windows) -- never the
     per-run protocol path; the legacy exclusion digest's layer 2 is recorded
     for information only and never refuses; its layer 1 is not called.
     Feasibility -- the patch resolves, the manifest still resolves, no
     unknown component class; a regime block is infeasible before slice 7.
  3. Eligible candidates collapse (card I, full novelty key; ineligible ones
     never collapse into them) and are ranked: confidence_real desc,
     distance_to_profitable desc, cost (backtests) asc, candidate_id asc.
     There is NO lineage-depth demotion (operator decision 6, dropped).
  4. Nothing scheduled and nothing eligible -> R2 (E-059 S2b): for every
     brief whose owner entry is `brief_status: open`, ask step 1a for more
     hypotheses -- reuse that brief's waiting request, or mint one
     `<owner>__more_<n>` (origin: brief). Every such request is `ready`, so
     no brief waits behind another; the scheduler's priority order applies.
     Legacy briefs (no `brief_status`, operator decision 7), exhausted ones,
     owners superseded/paused/blocked, and briefs whose last
     BRIEF_MAX_CONSECUTIVE_EMPTY_R2 requests yielded no new card never
     trigger R2 (the caller marks the last kind exhausted).
  5. Nothing scheduled, nothing eligible and no eligible open brief -> stop.

E-059 S2b adds the brief's extra hypotheses (card M, operator decisions 4 and
9) as candidates next to the reader proposals: a `queued` queue entry with
`origin: brief` and a `card_ref` (the card 1a already wrote, so it skips
authoring when picked), ranked on the three anchored scores step 1a wrote
for it (rubric brief-card-v1, runs/<run>/artifacts/queued_hypotheses.yaml),
with the same key as a proposal. Its pick flips it `queued` -> `ready`.

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
  * R1 (composition brief): recorded as a no-op until slice 7.
  * decide a brief is exhausted. Only step 1a says so (brief_status.yaml ->
    the run's completed_brief_exhausted outcome); the caller flips the owner.
  * write trial rows, touch the holdout, or write any file. The caller writes
    (including the one-time "[obsolete]" title on legacy briefs).

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
# A proposal_id is used as a queue id and a file name: letters, digits, '_' and
# '-' only (no '/', '\\', '..', '#', '.').
_SAFE_ID_RE = re.compile(r"[A-Za-z0-9_-]+")
_FIELD_PART_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)((?:\[\d+\])*)$")

# E-059 S2b -- briefs (card M) and R2.
ORIGIN_BRIEF = "brief"
BRIEF_OPEN = "open"
BRIEF_EXHAUSTED = "exhausted"
# The run's terminal pending_stage (and queue outcome) when step 1a reports the
# brief exhausted. Registered in verdict_criteria_evaluator._NON_VERDICT_OUTCOMES.
BRIEF_EXHAUSTED_OUTCOME = "completed_brief_exhausted"
# Operator decision 7: the one-time marker written on a legacy brief's queue
# entry `title` (never in the brief file).
OBSOLETE_TITLE_TAG = "[obsolete]"
# The anchored rubric step 1a scores extra cards on (hypothesis-design
# BRIEF_HYPOTHESES.md, injected only under the flag).
BRIEF_CARD_RUBRIC = "brief-card-v1"
QUEUED_CARDS_DIR = "campaign_record/queued_cards"
QUEUED_HYPOTHESES_FILE = "queued_hypotheses.yaml"
# The run's terminal pending_stage (and queue outcome) when every card step 1a
# wrote repeats a hypothesis this brief already produced (code-review fix 1).
# Non-verdict: registered in verdict_criteria_evaluator._NON_VERDICT_OUTCOMES.
NO_NEW_HYPOTHESIS_OUTCOME = "completed_no_new_hypothesis"
# R2 MUST TERMINATE (code-review fix 1). An open brief is marked exhausted
# (brief_status_reason: no_new_hypothesis) once this many CONSECUTIVE R2
# requests on it ended without a new, eligible card: 1a repeated an old card
# (completed_no_new_hypothesis), the run was quarantined, it failed or was
# paused, or the request was superseded. OPERATOR-ADJUSTABLE: raise it to give
# a brief more tries, never set it below 1.
BRIEF_MAX_CONSECUTIVE_EMPTY_R2 = 2
AUTO_EXHAUSTED_REASON = "no_new_hypothesis"
# Statuses in which an R2 request is still outstanding (not yet run to the end).
_OUTSTANDING_STATUSES = ("queued", "ready", "in_progress")
# Queue outcomes of a finished R2 request that produced no new, eligible card.
_EMPTY_R2_OUTCOMES = frozenset({NO_NEW_HYPOTHESIS_OUTCOME, BRIEF_EXHAUSTED_OUTCOME,
                                "quarantined_engineering_failure"})
# Code-review fix 6: an owner in one of these states never gets an R2 request.
_R2_INELIGIBLE_OWNER_STATUS_PREFIXES = ("superseded", "paused:", "blocked_")


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


def normalize_timeframe(tf):
    """'1H' / ' 1h ' -> '1h'; anything that is not a non-empty string -> None."""
    return tf.strip().lower() if isinstance(tf, str) and tf.strip() else None


def normalize_ref(ref):
    """Path separators normalised ('\\' -> '/'), leading './' dropped."""
    if not isinstance(ref, str) or not ref.strip():
        return None
    out = ref.strip().replace("\\", "/")
    while out.startswith("./"):
        out = out[2:]
    return out


def protocol_spec(root: Path, protocol_ref) -> dict | None:
    """What a protocol file actually tests, independent of its per-run file
    name (generated protocols are protocols/<run_id>_generated.json, so the
    path never repeats): {timeframe (normalised), windows_sha256 (canonical
    JSON of its `windows` list)}. None when the file cannot be read."""
    ref = normalize_ref(protocol_ref)
    if ref is None:
        return None
    path = Path(root) / ref
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    doc = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    if not isinstance(doc, dict) or not isinstance(doc.get("windows"), list):
        return None
    return {"timeframe": normalize_timeframe(doc.get("timeframe")),
            "windows_sha256": _canonical_sha(doc["windows"])}


def novelty_key(forecast_hash, symbols, entry: dict, specs: dict) -> tuple:
    """Card K's exact key: (config hash, symbols, timeframe, window set).
    Symbols come from the measured variant (protocol_result), the timeframe
    and window set from the protocol file the engine ran (the memory entry's
    own `timeframe` is copied from the LLM-written card, so it is only the
    fallback when the protocol file cannot be read, normalised)."""
    ref = normalize_ref(entry.get("protocol_ref"))
    spec = specs.get(ref) if ref else None
    if spec:
        timeframe, window_set = spec["timeframe"], f"windows:{spec['windows_sha256']}"
    else:
        timeframe, window_set = normalize_timeframe(entry.get("timeframe")), f"unresolved:{ref}"
    return (forecast_hash, tuple(sorted(symbols or [])), timeframe, window_set)


def _exact_index(memory: dict, specs: dict) -> dict:
    """{novelty_key: [run_id, ...]} over every TESTED variant in the memory.
    Legacy runs are not in memory, so they can never match (slice 8.1)."""
    index: dict = {}
    for run_id in sorted((memory.get("runs") or {})):
        entry = memory["runs"][run_id]
        if entry.get("engineering_fault"):
            continue
        for v in (entry.get("variants") or {}).values():
            if v.get("status") != "tested" or not v.get("forecast_hash"):
                continue
            key = novelty_key(v["forecast_hash"], v.get("symbols"), entry, specs)
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
# E-059 S2b -- briefs: owners, legacy briefs, extra cards, R2 requests
# ---------------------------------------------------------------------------

def _entries(queue) -> list:
    return [e for e in ((queue or {}).get("queue") or []) if isinstance(e, dict)]


def is_brief_owner(entry: dict) -> bool:
    """The entry that owns a brief carries `brief_status` (open|exhausted).
    Written by `register` while the flag is on; never on an agent entry."""
    return entry.get("brief_status") in (BRIEF_OPEN, BRIEF_EXHAUSTED)


def is_card_entry(entry: dict) -> bool:
    """A brief's extra hypothesis: its card was written by 1a (`card_ref`)."""
    return entry.get("origin") == ORIGIN_BRIEF and bool(entry.get("card_ref"))


def is_r2_request(entry: dict) -> bool:
    """An R2 request: ask 1a for more hypotheses on its owner's brief."""
    return entry.get("origin") == ORIGIN_BRIEF and not entry.get("card_ref")


def is_legacy_brief(entry: dict) -> bool:
    """Operator decision 7: an operator-registered entry (no origin, or
    `external`) with no `brief_status` is a legacy brief. It never triggers R2."""
    return entry.get("origin") in _OPERATOR_ORIGINS and "brief_status" not in entry


def needs_obsolete_tag(entry: dict) -> bool:
    """True for a legacy brief whose `title` does not carry the marker yet,
    so the marker is written exactly once."""
    return is_legacy_brief(entry) and not str(entry.get("title") or "").startswith(
        OBSOLETE_TITLE_TAG)


def obsolete_title(entry: dict, heading) -> str:
    """'[obsolete] <existing title | brief heading | entry id>'."""
    base = entry.get("title") or (heading.strip() if isinstance(heading, str) and heading.strip()
                                  else None) or entry.get("id")
    return f"{OBSOLETE_TITLE_TAG} {base}"


_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def brief_heading(root: Path, brief_path) -> str | None:
    """A human title for a brief (read only; the file is never written).
    Markdown brief: the first '# ' heading of the BODY -- the YAML frontmatter
    (whose '# ' lines are YAML comments) is skipped. Pure-YAML brief
    (.yaml/.yml): its top-level `title`, else `name`. None when there is
    none, or the file is missing/unreadable (the caller falls back to the id)."""
    ref = normalize_ref(brief_path)
    if ref is None:
        return None
    path = Path(root) / ref
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            doc = yaml.safe_load(text)
        except yaml.YAMLError:
            return None
        for key in ("title", "name"):
            val = doc.get(key) if isinstance(doc, dict) else None
            if isinstance(val, str) and val.strip():
                return val.strip()
        return None
    m = _FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    for line in body.splitlines():
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip()
    return None


def brief_owner(entry: dict, entries: list) -> dict | None:
    """The entry owning `entry`'s brief: the entry itself when it carries
    `brief_status`; for an origin-brief entry, the one entry with the same
    brief_path that carries it; else None (a legacy brief or a reader
    candidate). Two owners of one brief file raises."""
    if is_brief_owner(entry):
        return entry
    if entry.get("origin") != ORIGIN_BRIEF:
        return None
    ref = normalize_ref(entry.get("brief_path"))
    owners = [e for e in entries if is_brief_owner(e) and normalize_ref(e.get("brief_path")) == ref]
    if len(owners) > 1:
        raise DecideNextError(f"brief {ref!r} has {len(owners)} owner entries "
                              f"{[e.get('id') for e in owners]} carrying brief_status")
    return owners[0] if owners else None


def validate_card_scores(item, where: str) -> dict:
    """{scores: {<reader_proposals.SCORE_KEYS>: int 0..3}, model_id (non-empty
    string), rubric_version == BRIEF_CARD_RUBRIC}, checked with the reader
    proposals' own score validator. Raises DecideNextError otherwise."""
    if not isinstance(item, dict):
        raise DecideNextError(f"{where}: scores are not a mapping")
    scores = item.get("scores")
    try:
        _rp.check_scores(scores, where)
    except _rp.ProposalError as exc:
        raise DecideNextError(str(exc)) from exc
    if not (isinstance(item.get("model_id"), str) and item["model_id"].strip()):
        raise DecideNextError(f"{where}: model_id must be a non-empty string")
    if item.get("rubric_version") != BRIEF_CARD_RUBRIC:
        raise DecideNextError(f"{where}: rubric_version={item.get('rubric_version')!r} is not "
                              f"{BRIEF_CARD_RUBRIC!r} (the only rubric extra cards are scored on)")
    return {**{k: scores[k] for k in _rp.SCORE_KEYS},
            "model_id": item["model_id"], "rubric_version": item["rubric_version"]}


def _card_source_run(card_ref: str) -> str:
    """runs id from 'campaign_record/queued_cards/<run_id>/<file>'."""
    ref = normalize_ref(card_ref) or ""
    prefix = QUEUED_CARDS_DIR + "/"
    parts = ref[len(prefix):].split("/") if ref.startswith(prefix) else []
    if len(parts) != 2 or not _SAFE_ID_RE.fullmatch(parts[0]):
        raise DecideNextError(f"card_ref {card_ref!r} is not '{QUEUED_CARDS_DIR}/<run_id>/<card>'")
    return parts[0]


def load_queued_card(root: Path, card_ref: str) -> dict:
    """{source_run, hypothesis_id, scores} of one queued card, from its source
    run's artifacts/queued_hypotheses.yaml (written by the split under the
    flag). A card with no record or malformed scores raises: scores are 1a's
    output, and a card that cannot be ranked must stop loudly."""
    run_id = _card_source_run(card_ref)
    path = Path(root) / "runs" / run_id / "artifacts" / QUEUED_HYPOTHESES_FILE
    doc = _load_yaml_opt(path)
    cards = doc.get("cards") if isinstance(doc, dict) else None
    ref = normalize_ref(card_ref)
    match = [c for c in (cards or []) if isinstance(c, dict) and normalize_ref(c.get("card_ref")) == ref]
    if len(match) != 1:
        raise DecideNextError(f"{path}: {len(match)} record(s) for card {ref!r} (expected 1)")
    return {"source_run": run_id, "hypothesis_id": match[0].get("hypothesis_id"),
            "scores": validate_card_scores(match[0], f"{path} card {ref}")}


def brief_protocol_cost(root: Path, brief_path):
    """(backtests, basis) from a brief's pinned protocol file
    (machine_constraints.protocol_ref: its windows x symbols x N_VARIANTS), or
    (None, reason) when it cannot be resolved -- a null cost ranks last."""
    ref = normalize_ref(brief_path)
    path = Path(root) / ref if ref else None
    if path is None or not path.is_file():
        return None, "brief file not found"
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\s*\n(.*?\n)---\s*\n", text, re.DOTALL)
    front = (yaml.safe_load(m.group(1)) or {}) if m else {}
    mc = front.get("machine_constraints") if isinstance(front, dict) else None
    pref = normalize_ref((mc or {}).get("protocol_ref")) if isinstance(mc, dict) else None
    if not pref or not (Path(root) / pref).is_file():
        return None, "the brief pins no readable protocol_ref"
    ptext = (Path(root) / pref).read_text(encoding="utf-8")
    proto = json.loads(ptext) if pref.endswith(".json") else yaml.safe_load(ptext)
    windows = proto.get("windows") if isinstance(proto, dict) else None
    symbols = proto.get("symbols") if isinstance(proto, dict) else None
    if not isinstance(windows, list) or not windows or not isinstance(symbols, list) or not symbols:
        return None, f"{pref} has no windows/symbols list"
    return (len(windows) * N_VARIANTS * len(symbols),
            f"{len(windows)} windows x {N_VARIANTS} variants x {len(symbols)} symbol(s) "
            f"x {SECONDS_PER_BACKTEST} s ({COST_BASIS_SOURCE}; protocol {pref})")


def brief_hypothesis_ids(root: Path, queue, brief_path) -> list:
    """Every hypothesis_id already produced from one brief file: the card of
    each run of every entry sharing that brief_path, and each queued card not
    yet run. Handed to step 1a on an R2 request so it does not repeat them."""
    ref = normalize_ref(brief_path)
    found = set()
    for e in _entries(queue):
        if normalize_ref(e.get("brief_path")) != ref:
            continue
        paths = [Path(root) / "runs" / r / "artifacts" / "hypothesis_card.yaml"
                 for r in (e.get("run_ids") or [])]
        if e.get("card_ref") and not e.get("run_ids"):
            paths.append(Path(root) / normalize_ref(e["card_ref"]))
        for p in paths:
            card = _load_yaml_opt(p)
            hid = card.get("hypothesis_id") if isinstance(card, dict) else None
            if isinstance(hid, str) and hid.strip():
                found.add(hid.strip())
    return sorted(found)


def _request_number(entry: dict, owner_id: str) -> int:
    m = re.fullmatch(re.escape(owner_id) + r"__more_(\d+)", str(entry.get("id")))
    return int(m.group(1)) if m else 0


def r2_request_yielded(entry: dict) -> bool | None:
    """Did a finished R2 request produce a new, eligible card? None while it is
    still outstanding (queued/ready/in_progress). True when it ran to `done`
    with any other outcome than the empty ones, or was parked blocked_on_* or
    paused:waiting_for_* (its card needed an engine piece or data: it WAS a new
    card). False otherwise:
    completed_no_new_hypothesis, completed_brief_exhausted, a quarantine, a
    failure or pause (paused:*), or superseded."""
    status = str(entry.get("status") or "")
    if status in _OUTSTANDING_STATUSES:
        return None
    # Slice 6c S2c: a parked request (paused:waiting_for_component|data) is the
    # retired-routing form of blocked_on_*: its card WAS new, it waits on an
    # engine piece or data.
    if status.startswith(("blocked_on_", "paused:waiting_for_")):
        return True
    if status == "done":
        return entry.get("outcome") not in _EMPTY_R2_OUTCOMES
    return False


def consecutive_empty_r2(owner: dict, entries: list) -> list:
    """The ids of the trailing run of finished R2 requests on `owner`'s brief
    that yielded no new, eligible card (request-number order; outstanding
    requests neither count nor break the run)."""
    mine = sorted((e for e in entries if is_r2_request(e) and brief_owner(e, entries) is owner),
                  key=lambda e: _request_number(e, owner["id"]))
    streak = []
    for e in mine:
        yielded = r2_request_yielded(e)
        if yielded is None:
            continue
        streak = [] if yielded else streak + [e["id"]]
    return streak


def r2_eligible_owner(entry: dict) -> bool:
    """An open brief whose owner entry is not superseded, paused or blocked
    (code-review fix 6)."""
    return (entry.get("brief_status") == BRIEF_OPEN
            and not str(entry.get("status") or "").startswith(_R2_INELIGIBLE_OWNER_STATUS_PREFIXES))


def _next_request_id(owner_id: str, taken: set) -> str:
    n = 1
    while f"{owner_id}__more_{n}" in taken:
        n += 1
    return f"{owner_id}__more_{n}"


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

    specs = {}
    for entry in (memory.get("runs") or {}).values():
        ref = normalize_ref(entry.get("protocol_ref"))
        if ref and ref not in specs:
            specs[ref] = protocol_spec(root, ref)
    briefs_dir = root / CANDIDATE_BRIEFS_DIR
    existing_briefs = (sorted(p.name for p in briefs_dir.iterdir() if p.is_file())
                       if briefs_dir.exists() else [])

    # E-059 S2b: every waiting extra card (queued, origin brief, card_ref).
    brief_cards = {}
    for e in _entries(queue):
        if is_card_entry(e) and e.get("status") == "queued":
            card = load_queued_card(root, e["card_ref"])
            backtests, basis = brief_protocol_cost(root, e.get("brief_path"))
            brief_cards[e["id"]] = {**card, "cost_backtests": backtests, "cost_basis": basis}

    return {
        "brief_cards": brief_cards,
        "memory": memory,
        "protocol_specs": specs,
        "existing_candidate_briefs": existing_briefs,
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
    resolved_sha, novelty, key = None, None, None
    config_for_digest = None
    # The proposal_id becomes a queue id AND a file name: it must be a safe
    # bare name, and its middle segment must be the run it came from.
    if not (_SAFE_ID_RE.fullmatch(pid) and ".." not in pid
            and re.fullmatch(rf"{re.escape(category)}-{re.escape(run_id)}-\d+", pid)):
        reasons.append(f"unsafe_proposal_id: {pid!r} is not a safe '<category>-{run_id}-<n>' name")
    else:
        queue_ids = {e.get("id") for e in (inputs.get("queue") or {}).get("queue") or []
                     if isinstance(e, dict)}
        if pid in queue_ids:
            reasons.append(f"queue_id_collision: a queue entry {pid!r} already exists")
        if f"{pid}.md" in set(inputs.get("existing_candidate_briefs") or []):
            reasons.append(f"brief_collision: {CANDIDATE_BRIEFS_DIR}/{pid}.md already exists")
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
            key = novelty_key(resolved_sha, symbols, entry, inputs.get("protocol_specs") or {})
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
    if p["kind"] == "patch":
        collapse_key = ("patch", key) if key else ("single", pid)
    else:
        blk = p.get("block") or {}
        collapse_key = ("new_block", blk.get("kind"),
                        tuple(sorted(blk.get("config_paths") or [])), run_id)
    return {
        "_collapse_key": collapse_key,
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


def _card_candidate(entry: dict, info: dict, owner) -> dict:
    """A brief's extra hypothesis (card M) as a candidate: its card is already
    written, so there is no config to hash and no novelty key before 1b; its
    feasibility is decided by step 3's data gate, as for a sketch. Always
    eligible: scores only rank (decision 4), they never exclude an idea."""
    backtests = info.get("cost_backtests")
    return {
        "_collapse_key": ("card", entry["id"]),
        "candidate_id": entry["id"],
        "origin": ORIGIN_BRIEF,
        "kind": "card",
        "category": None,
        "source_run": info["source_run"],
        "parent_hypothesis_id": None,
        "hypothesis_id": info.get("hypothesis_id"),
        "proposal_ref": None,
        "card_ref": entry["card_ref"],
        "brief_owner": owner.get("id") if owner else None,
        "collapsed_sources": [],
        "scores": dict(info["scores"]),
        "resolved_config_sha256": None,
        "gates": {
            "novelty": {"exact_match": "NOT_APPLICABLE", "matched_runs": [],
                        "note": "no config until 1b authors it",
                        "digest_advisory": {"outcome": "not_available", "family": None,
                                            "family_confidence": None, "run_ids": []}},
            "feasibility": {"result": "UNKNOWN",
                            "reasons": ["config authored at 1b; step 3's data gate stays binding"]},
        },
        "eligible": True,
        "cost": {
            "backtests": backtests,
            "seconds_estimate": (round(backtests * SECONDS_PER_BACKTEST)
                                 if backtests is not None else None),
            "basis": info.get("cost_basis") or "unresolved",
        },
        "rank": None,
    }


def _r2(entries: list, *, select: bool) -> dict:
    """R2 (S1_FINDINGS_6B.md §4.3). `select` is False when something is
    already scheduled or eligible: the rule is then only recorded. When it
    fires, EVERY eligible open brief (r2_eligible_owner, and fewer than
    BRIEF_MAX_CONSECUTIVE_EMPTY_R2 consecutive empty requests) gets a `ready`
    request -- its waiting one is flipped ready, or a new `<owner>__more_<n>`
    is minted ready -- so no brief waits behind another (code-review fix 3);
    the scheduler's own priority order then picks among them."""
    open_owners = sorted((e for e in entries if e.get("brief_status") == BRIEF_OPEN),
                         key=lambda e: (e.get("priority", 999), e.get("id")))
    spent = {e["id"]: consecutive_empty_r2(e, entries) for e in open_owners}
    spent = {k: v for k, v in spent.items() if len(v) >= BRIEF_MAX_CONSECUTIVE_EMPTY_R2}
    eligible = [e for e in open_owners if r2_eligible_owner(e) and e["id"] not in spent]
    out = {
        "fired": False,
        "open_briefs": [e["id"] for e in open_owners],
        "eligible_briefs": [e["id"] for e in eligible],
        "exhausted_briefs": sorted(e["id"] for e in entries
                                   if e.get("brief_status") == BRIEF_EXHAUSTED),
        "no_new_hypothesis_briefs": sorted(spent),
        "legacy_briefs": sorted(e["id"] for e in entries if is_legacy_brief(e)),
        "max_consecutive_empty_r2": BRIEF_MAX_CONSECUTIVE_EMPTY_R2,
        "enqueued": [],
        "ready": [],
        "reason": "",
    }
    if not select:
        out["reason"] = "not needed: the scheduler has an entry to run, or a candidate is eligible"
        return out
    if not eligible:
        out["reason"] = ("no eligible open brief (exhausted, no new hypothesis after "
                         f"{BRIEF_MAX_CONSECUTIVE_EMPTY_R2} consecutive empty R2 requests, owner "
                         "superseded/paused/blocked, or legacy -- operator decision 7)")
        return out
    taken = {e.get("id") for e in entries}
    requests = []  # (entry_id, owner_id, new)
    for owner in eligible:
        mine = [e for e in entries if is_r2_request(e) and brief_owner(e, entries) is owner]
        waiting = [e for e in mine if e.get("status") in _OUTSTANDING_STATUSES]
        if waiting:
            requests.append((waiting[0]["id"], owner["id"], False))
        else:
            rid = _next_request_id(owner["id"], taken)
            taken.add(rid)
            requests.append((rid, owner["id"], True))
    out.update({
        "fired": True,
        "enqueued": [{"entry_id": rid, "owner": oid, "status": "ready"}
                     for rid, oid, new in requests if new],
        "ready": [rid for rid, _, _ in requests],
        "reason": (f"nothing scheduled and no eligible candidate: ask step 1a for more hypotheses "
                   f"on {len(eligible)} eligible open brief(s)"),
    })
    out["_requests"] = requests
    return out


def _score_key(c: dict) -> tuple:
    return (-c["scores"]["confidence_real"], -c["scores"]["distance_to_profitable"],
            c["candidate_id"])


def _collapse(cands: list) -> list:
    """Card I: ELIGIBLE candidates that are the same thing collapse into one,
    keeping the highest score tuple. Called on eligible candidates only, so an
    ineligible duplicate can never shadow an eligible one. Patches: the FULL
    novelty key (config hash + symbols + timeframe + window set). Sketches:
    identical kind + config_paths from the same source run."""
    groups, order = {}, []
    for c in cands:
        key = c["_collapse_key"]
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


def select_entry_rule(entries: list):
    """A verbatim mirror of run_campaign._select_entry (first in_progress entry,
    else the lowest-priority `ready` one, stable), for callers without the
    campaign runner. run_campaign passes its own _select_entry to decide();
    a test pins the two together."""
    in_progress = [e for e in entries if e.get("status") == "in_progress"]
    if in_progress:
        return in_progress[0]
    ready = [e for e in entries if e.get("status") == "ready"]
    if not ready:
        return None
    ready.sort(key=lambda e: e.get("priority", 999))
    return ready[0]


def decide(inputs: dict, *, now: str, trigger: dict, select_entry=None) -> dict:
    """The decision record. Pure: reads only `inputs`; the same inputs, `now`
    and `trigger` give the same record. `inputs["queue"]` is the queue as it
    will stand once the finished entry is marked done. `select_entry` is the
    scheduler's own rule (run_campaign._select_entry; default: the mirror
    above). `picked` is always what that rule will run next: an existing
    in_progress or ready entry if there is one (nothing is minted), else the
    top candidate -- a reader proposal to mint, or a waiting extra card to
    flip ready (either way the only ready entry, so the rule picks it) --,
    else R2's ready request (E-059 S2b), else a stop (no open brief left)."""
    select_entry = select_entry or select_entry_rule
    memory = inputs["memory"]
    queue = inputs["queue"]
    named = {e.get("proposal_ref") for e in (queue.get("queue") or [])
             if isinstance(e, dict) and e.get("proposal_ref")}
    exact = _exact_index(memory, inputs.get("protocol_specs") or {})

    cands = []
    for run_id in sorted(inputs.get("runs") or {}):
        src = inputs["runs"][run_id]
        entry = memory["runs"][run_id]
        for item in src["proposals"]:
            p, cat = item["proposal"], item["category"]
            ref = f"runs/{run_id}/artifacts/proposals/{cat}.yaml#{p['proposal_id']}"
            if ref in named:
                continue  # already in the queue: out of the pool (§3.7)
            cands.append(_candidate(run_id, entry, src, cat, p, inputs, exact))
    # E-059 S2b: a brief's waiting extra cards, ranked with the proposals.
    entries = _entries(queue)
    brief_cards = inputs.get("brief_cards") or {}
    for e in entries:
        if is_card_entry(e) and e.get("status") == "queued":
            if e["id"] not in brief_cards:
                raise DecideNextError(f"queued card entry {e['id']!r} has no loaded card record "
                                      f"(load_inputs reads {QUEUED_HYPOTHESES_FILE})")
            cands.append(_card_candidate(e, brief_cards[e["id"]], brief_owner(e, entries)))
    # Split by eligibility FIRST; collapse only among eligible candidates.
    eligible = sorted(_collapse([c for c in cands if c["eligible"]]), key=rank_key)
    for i, c in enumerate(eligible, 1):
        c["rank"] = i
    ineligible = sorted((c for c in cands if not c["eligible"]), key=lambda c: c["candidate_id"])
    for c in eligible + ineligible:
        c.pop("_collapse_key", None)

    operator = _operator_entries(queue)
    scheduled = select_entry([e for e in (queue.get("queue") or []) if isinstance(e, dict)])
    picked, stop = None, None
    if scheduled is not None:
        why = (f"the scheduler's own rule (_select_entry) runs this {scheduled.get('status')} "
               f"entry next (priority {scheduled.get('priority')}); nothing is minted")
        if scheduled.get("origin") in _OPERATOR_ORIGINS:
            picked = {"operator_entry": scheduled["id"], "why": why}
        else:
            picked = {"queue_entry_id": scheduled["id"], "why": why}
    elif eligible:
        top = eligible[0]
        why = (f"rank 1 of {len(eligible)} eligible: confidence_real="
               f"{top['scores']['confidence_real']}, distance_to_profitable="
               f"{top['scores']['distance_to_profitable']}, backtests="
               f"{top['cost']['backtests']}")
        if top["origin"] == ORIGIN_BRIEF:
            # A waiting extra card: flipped queued -> ready by the caller.
            picked = {"candidate_id": top["candidate_id"], "queue_entry_id": top["candidate_id"],
                      "card_ref": top["card_ref"], "why": why}
        else:
            picked = {
                "candidate_id": top["candidate_id"],
                "queue_entry_id": top["candidate_id"],
                "brief_path": f"{CANDIDATE_BRIEFS_DIR}/{top['candidate_id']}.md",
                "why": why,
            }
    r2 = _r2(entries, select=scheduled is None and not eligible)
    requests = r2.pop("_requests", None)
    if requests:
        # What the scheduler will actually run: its own rule over the queue
        # with every request ready (waiting ones flipped, new ones appended).
        ready_ids = {rid for rid, _, _ in requests}
        sim = [dict(e, status="ready") if e.get("id") in ready_ids else e for e in entries]
        sim += [{"id": rid, "status": "ready", "priority": AGENT_PRIORITY}
                for rid, _, new in requests if new]
        first = select_entry(sim)["id"]
        rid, oid, new = next(r for r in requests if r[0] == first)
        owner = next(e for e in entries if e.get("id") == oid)
        picked = {"r2_request": rid, "queue_entry_id": rid, "brief_owner": oid,
                  "brief_path": owner.get("brief_path"), "new": new,
                  "why": (f"R2: no entry scheduled and no eligible candidate; ask step 1a for "
                          f"more hypotheses on open brief {oid}")}
    elif picked is None:
        stop = {"reason": "no_eligible_candidate",
                "detail": (f"the scheduler has no in_progress or ready entry to run, 0 of "
                           f"{len(cands)} candidate(s) eligible, and no open brief for R2 "
                           f"({len(r2['exhausted_briefs'])} exhausted, "
                           f"{len(r2['legacy_briefs'])} legacy)")}

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
            "r2": r2,
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
        source["expected_manifest_sha256"] = config_sha256(src["manifest"])
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
