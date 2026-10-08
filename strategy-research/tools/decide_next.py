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
     per-run protocol path (tools/novelty.py, shared with the 5a gate since
     E-036 S2a); the legacy exclusion digest's family lookup
     (build_exclusion_digest.legacy_family_lookup) is recorded for
     information only and never refuses; the KB layer is not called.
     Feasibility -- the patch resolves, the manifest still resolves, no
     unknown component class; a regime block is infeasible before slice 7;
     (E-035 S2c) a proposal's `requires_feed` blocks it only while that feed
     is not WIRED and the candidate's config consumes it (requires_feed_gate).
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
  * R1 (composition brief) without orchestrator.composition_runs: recorded as
    the same no-op as before. With it (E-060 S3b, load_inputs(...,
    composition_runs=True)): when an exact timeframe holds >= 2 forecast
    blocks whose set has no composition queue entry yet, R1 picks
    `composition-<tf>-<registry_hash>` -- behind a run in progress and behind
    ready operator entries, ahead of every agent entry, candidate and R2
    (guess 10); once per registry state per timeframe. The caller writes the
    code-made variants + manifest (tools/composition.py), the brief
    (composition_brief) and the queue entry (origin composition). A
    composition's reader patches are accepted with its composition manifest
    as their source (7.5).
  * decide a brief is exhausted. Only step 1a says so (brief_status.yaml ->
    the run's completed_brief_exhausted outcome); the caller flips the owner
    after two consecutive such answers (consecutive_exhausted, O-20).
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
import composition_names as _names  # tools/ sibling: the shared composition names
import campaign_memory as _cm  # tools/ sibling: memory loader + retired-field scan
import json_pointer as _jp  # tools/ sibling: pointer + patch semantics shared with 5a
import novelty as _nov  # tools/ sibling: the exact-match key shared with the 5a gate (E-036 S2a)
import reader_proposals as _rp  # tools/ sibling: proposal loader/validator
import research_folds as _folds  # tools/ sibling: E-077 PR-1 (D-085), the fixed folds + lineage

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
# O-20 (operator, 2026-10-04): step 1a's "exhausted" closes a brief only after this
# many CONSECUTIVE independent answers -- one per queue entry (the owner's own run,
# then its R2 requests); a retry or resume inside one run is never a second answer.
# A single one is recorded on the owner (`brief_exhausted_answers`) and the brief
# stays open. run_067 + run_069: 4 of 6 step-1a calls on one brief proposed new
# ideas, so one "exhausted" draw is not evidence that nothing is left.
BRIEF_EXHAUSTED_ANSWERS_TO_CLOSE = 2
EXHAUSTED_ANSWERS_REASON = "two_exhausted_answers"
# O-20: the operator's reopen marker on an owner entry -- the id of the last entry
# (an R2 request, or the owner's own id) whose answers no longer count. Both the
# exhausted-answer count and the empty-R2 streak start after it, so a reopened brief
# is not closed again by the history that closed it.
REOPENED_AFTER_KEY = "brief_reopened_after"
# Finished queue outcomes that carry no answer from step 1a (the run broke).
_NO_ANSWER_OUTCOMES = frozenset({"quarantined_engineering_failure"})
# Statuses in which an R2 request is still outstanding (not yet run to the end).
_OUTSTANDING_STATUSES = ("queued", "ready", "in_progress")
# CUL-398: a held request (operator hold or component quarantine). Outstanding
# for the streak and never flipped ready by R2. Only an OPERATOR hold freezes
# its whole brief (r2_request_operator_held).
HELD_STATUS_PREFIX = "blocked_on_"
# R9's automatic quarantine (run_campaign: `blocked_on_component:<name>`): held
# for the streak, but it does not freeze the brief (operator, 2026-10-04).
COMPONENT_QUARANTINE_PREFIX = "blocked_on_component:"
# E-068 PR 4 (D-071, review S3b of PR 3a): a quarantine no longer freezes its
# brief, so a brief whose new ideas keep needing missing components had no
# per-brief R2 limit. At this many component-quarantined entries (owner + R2
# requests, after any reopen marker) R2 stops asking it; the brief stays open.
BRIEF_MAX_COMPONENT_QUARANTINES = 3
# E-068 PR 4 (D-071, CUL-399): the status run_campaign gives an entry the agent
# created or would flip ready while orchestrator.operator_approval is on. An
# OPERATOR hold (not COMPONENT_QUARANTINE_PREFIX): it holds its brief, so R2
# never re-mints behind it; run_campaign.py --approve <id> sets it ready.
OPERATOR_APPROVAL_STATUS = "blocked_on_operator_approval"
# Queue outcomes of a finished R2 request that produced no new, eligible card.
_EMPTY_R2_OUTCOMES = frozenset({NO_NEW_HYPOTHESIS_OUTCOME, BRIEF_EXHAUSTED_OUTCOME,
                                "quarantined_engineering_failure"})
# Code-review fix 6: an owner in one of these states never gets an R2 request.
_R2_INELIGIBLE_OWNER_STATUS_PREFIXES = ("superseded", "paused:", "blocked_")
# Slice 6c S2c: a parked queue entry's status prefix (run_campaign.PARKED_STATUS_PREFIX
# mirrors it; a test pins the two). A parked OWNER stays R2-eligible (review fix 6).
PARKED_STATUS_PREFIX = "paused:waiting_for_"


class DecideNextError(ValueError):
    """An input decide_next needs is malformed. Never caught here."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def config_sha256(config) -> str:
    """The run_phase1_research._compute_forecast_hash canonicalisation
    (json.dumps(..., sort_keys=True), sha256) applied to an in-memory config,
    so a resolved candidate config hashes exactly as its trial row will.
    E-036 S2a: one definition, tools/novelty.forecast_hash_of_config."""
    return _nov.forecast_hash_of_config(config)


def _canonical_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()


# The one module component classes live in: the scope of known_component_classes
# AND of component_class_status (slice 6c S2c review fixes 2 + 8 -- one
# definition of "is this component class defined", shared by decide-next's
# feasibility check, 5a parking and --unpark).
COMPONENT_MODULE = "strategies.strategy_components"
_CLASS_PATH_RE = re.compile(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+$")


def _component_module_path(trading_bot_root: Path) -> Path:
    return Path(trading_bot_root).joinpath(*COMPONENT_MODULE.split(".")).with_suffix(".py")


def _top_level_class_names(trading_bot_root: Path) -> list:
    tree = ast.parse(_component_module_path(trading_bot_root).read_text(encoding="utf-8"))
    return [n.name for n in tree.body if isinstance(n, ast.ClassDef)]


def known_component_classes(trading_bot_root: Path) -> list:
    """Dotted class paths defined at the top level of
    trading-bot/strategies/strategy_components.py, read with ast (no import of
    the engine). The same module 5a's V12 check loads classes from."""
    return sorted(f"{COMPONENT_MODULE}.{n}" for n in _top_level_class_names(trading_bot_root))


def component_class_status(trading_bot_root: Path, class_path) -> str:
    """'defined' | 'missing' | 'invalid' for one dotted component class path,
    in known_component_classes' scope, read with ast (never imported):
      * invalid -- not a well-formed dotted path (a dotless name included), a
        module other than COMPONENT_MODULE (a module typo), or that module's
        file absent or unparseable: a config / engineering error;
      * missing -- the module exists and parses, and the class is not defined
        at its top level (the one case a run may wait on);
      * defined -- it is."""
    if not isinstance(class_path, str) or not _CLASS_PATH_RE.match(class_path):
        return "invalid"
    module, _, name = class_path.rpartition(".")
    if module != COMPONENT_MODULE or not _component_module_path(trading_bot_root).is_file():
        return "invalid"
    try:
        names = _top_level_class_names(trading_bot_root)
    except (SyntaxError, ValueError, OSError):
        return "invalid"
    return "defined" if name in names else "missing"


# ---------------------------------------------------------------------------
# E-035 S2c (slice 8.2): feeds a reader proposal may require
# ---------------------------------------------------------------------------
# The layering (one check per step, never duplicated):
#   * HERE, at decide-next: is the feed WIRED -- a key of
#     trading-bot/data/feed_registry.py's FEED_REGISTRY, the registry the
#     engine loads every backtest from -- and does the candidate's config
#     consume it? That is all decide-next can know before a config exists.
#   * At step 3 (tools/data_availability_gate.py, stage 14): does the wired
#     feed actually COVER this run's venue, symbols and windows? A shortfall
#     there parks the run waiting_for_data (slice 6c S2c), as for any feed.
# The classification is the gate's own (check_aux_feed_window): a
# RESERVED_FEED_REGISTRY name is checked first and is declined until a
# committed campaign_data_policy.yaml designation covers it (a DESIGNATION,
# not an acquisition); any other name outside FEED_REGISTRY was never built
# (an ACQUISITION). Both registries are read with ast, like
# known_component_classes: the module imports pandas and the fetchers, which
# decide_next must not need.
FEED_REGISTRY_MODULE = "data.feed_registry"
FEED_REGISTRY_NAME = "FEED_REGISTRY"
RESERVED_FEED_REGISTRY_NAME = "RESERVED_FEED_REGISTRY"
FEED_WIRED, FEED_RESERVED, FEED_UNKNOWN = "wired", "reserved", "unknown"
CONSUMES_FEEDS_ATTR = "consumes_feeds"  # SubStrategyComponent.consumes_feeds


def feed_registry_path(trading_bot_root: Path) -> Path:
    """trading-bot/data/feed_registry.py under `trading_bot_root`."""
    return Path(trading_bot_root).joinpath(*FEED_REGISTRY_MODULE.split(".")).with_suffix(".py")


def _parse_module(path: Path) -> ast.Module:
    try:
        return ast.parse(Path(path).read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError) as exc:
        raise DecideNextError(f"{path}: cannot be read ({type(exc).__name__}: {exc})") from exc


def _module_assignments(tree: ast.Module) -> dict:
    """name -> value node, for every module-level `NAME = <value>`."""
    out = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            out[node.targets[0].id] = node.value
    return out


def _str_sequence(node, assigns: dict):
    """The strings of a tuple/list literal whose items are string constants or
    names bound at module level to one -- or of a name bound to such a
    literal. None for any other shape."""
    if isinstance(node, ast.Name) and isinstance(assigns.get(node.id), (ast.Tuple, ast.List)):
        node = assigns[node.id]
    if not isinstance(node, (ast.Tuple, ast.List)):
        return None
    out = []
    for item in node.elts:
        if isinstance(item, ast.Name):
            item = assigns.get(item.id)
        if not (isinstance(item, ast.Constant) and isinstance(item.value, str)):
            return None
        out.append(item.value)
    return out


def _registry_keys(tree: ast.Module, name: str, path: Path) -> list:
    """Sorted string keys of the module-level `name = {...}` dict literal, or
    of `name = {k: ... for k in <literal tuple/list, or a name bound to one>}`
    (the shape RESERVED_FEED_REGISTRY has). Raises DecideNextError for any
    other shape, or no keys -- a silent empty set would give every
    requires_feed proposal the wrong status."""
    node = _module_assignments(tree).get(name)
    keys = None
    if isinstance(node, ast.Dict):
        if all(isinstance(k, ast.Constant) and isinstance(k.value, str) for k in node.keys):
            keys = [k.value for k in node.keys]
    elif (isinstance(node, ast.DictComp) and len(node.generators) == 1
          and not node.generators[0].ifs and isinstance(node.generators[0].target, ast.Name)
          and isinstance(node.key, ast.Name) and node.key.id == node.generators[0].target.id):
        keys = _str_sequence(node.generators[0].iter, _module_assignments(tree))
    if not keys:
        raise DecideNextError(f"{path}: no module-level {name} dict literal (or comprehension over "
                              f"a literal tuple) with string keys -- cannot classify feeds")
    return sorted(keys)


def known_feeds(trading_bot_root: Path) -> list:
    """Sorted FEED_REGISTRY keys (the WIRED feeds), read with ast (never
    imported). Raises DecideNextError when unreadable."""
    path = feed_registry_path(trading_bot_root)
    return _registry_keys(_parse_module(path), FEED_REGISTRY_NAME, path)


def load_feed_registry(trading_bot_root: Path) -> dict:
    """{"wired": FEED_REGISTRY keys, "reserved": RESERVED_FEED_REGISTRY keys},
    both sorted, read with ast. Raises DecideNextError when the module is
    missing, does not parse, or either registry is not a literal it can read."""
    path = feed_registry_path(trading_bot_root)
    tree = _parse_module(path)
    return {FEED_WIRED: _registry_keys(tree, FEED_REGISTRY_NAME, path),
            FEED_RESERVED: _registry_keys(tree, RESERVED_FEED_REGISTRY_NAME, path)}


def component_consumed_feeds(trading_bot_root: Path) -> dict:
    """{dotted class path: sorted feeds} for every top-level class of
    COMPONENT_MODULE whose `consumes_feeds` (its own, or inherited from a
    class of the same module) is non-empty -- the declaration the engine's
    required_feeds() reads. Read with ast; raises DecideNextError when the
    module is unreadable or a `consumes_feeds` is not a literal tuple/list of
    strings (or of module-level string constants)."""
    path = _component_module_path(trading_bot_root)
    tree = _parse_module(path)
    assigns = _module_assignments(tree)
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    own = {}
    for name, cls in classes.items():
        for node in cls.body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == CONSUMES_FEEDS_ATTR):
                feeds = _str_sequence(node.value, assigns)
                if feeds is None:
                    raise DecideNextError(f"{path}: {name}.{CONSUMES_FEEDS_ATTR} is not a literal "
                                          f"tuple of feed names")
                own[name] = feeds

    def _resolve(name, seen=()):
        if name in own:
            return own[name]
        for base in classes[name].bases:
            if isinstance(base, ast.Name) and base.id in classes and base.id not in seen:
                got = _resolve(base.id, seen + (name,))
                if got is not None:
                    return got
        return None

    out = {}
    for name in classes:
        feeds = _resolve(name)
        if feeds:
            out[f"{COMPONENT_MODULE}.{name}"] = sorted(set(feeds))
    return out


def load_feed_set(trading_bot_root: Path) -> dict:
    """Everything requires_feed_gate needs: load_feed_registry's wired and
    reserved names plus component_consumed_feeds. Fails loud (DecideNextError)
    when either source cannot be read. Callers compute it only when some
    proposal carries requires_feed (load_inputs' `feed_set` callable)."""
    return {**load_feed_registry(trading_bot_root),
            "component_feeds": component_consumed_feeds(trading_bot_root)}


def feed_status(feed: str, feed_set) -> str | None:
    """The gate's own classification of one feed name (check_aux_feed_window
    checks the reserved registry first): 'reserved', 'wired' or 'unknown'.
    None when no feed set was supplied."""
    if feed_set is None:
        return None
    if feed in set(feed_set.get(FEED_RESERVED) or ()):
        return FEED_RESERVED
    if feed in set(feed_set.get(FEED_WIRED) or ()):
        return FEED_WIRED
    return FEED_UNKNOWN


def _aux_feed_name(entry):
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict) and isinstance(entry.get("name"), str):
        return entry["name"]
    return None


def config_feeds(config, component_feeds: dict) -> set:
    """The feeds a strategy config consumes: its `aux_feeds` (what the
    data-availability gate reads, evaluate_variant) plus every feed its
    component classes declare in `consumes_feeds` (what the engine's
    required_feeds() reads)."""
    if not isinstance(config, dict):
        return set()
    out = {n for n in (_aux_feed_name(e) for e in (config.get("aux_feeds") or [])) if n}
    for cls in _component_classes(config):
        out.update((component_feeds or {}).get(cls) or ())
    return out


def requires_feed_gate(p: dict, feed_set, config=None) -> tuple:
    """(record, reason) for one proposal. (None, None) when the proposal has
    no requires_feed -- nothing is recorded, so such candidates are unchanged.

    Otherwise record = {feed, status, consumed, available, reason}:
      status   -- feed_status (None: no feed set supplied);
      consumed -- whether `config` (the candidate's RESOLVED config) consumes
                  the feed (config_feeds); None when there is no resolved
                  config (a new_block before 1b, an unresolved patch) or no
                  feed set;
      available -- status == 'wired'.
    The candidate is blocked (reason not None) unless the feed is wired or its
    resolved config provably does not read it: a patch that leaves the feed
    unread is testable today (its request row is still filed at stage 16).
    Reasons name only the missing feed -- never the registry's contents -- so
    an unrelated registry change never rewrites a waiting candidate's reason:
      requires_feed_reserved:<feed> -- a reserved feed (needs a designation);
      requires_feed:<feed>          -- not wired (needs an acquisition), or no
                                       feed set was supplied."""
    rf = p.get("requires_feed")
    if rf is None:
        return None, None
    feed = rf["feed"]
    status = feed_status(feed, feed_set)
    consumed = (None if config is None or feed_set is None
                else feed in config_feeds(config, feed_set.get("component_feeds")))
    record = {"feed": feed, "status": status, "consumed": consumed,
              "available": status == FEED_WIRED, "reason": rf["reason"]}
    if status == FEED_WIRED or consumed is False:
        return record, None
    if status is None:
        return record, f"requires_feed:{feed} -- no feed set was supplied"
    if status == FEED_RESERVED:
        return record, (f"requires_feed_reserved:{feed} -- a reserved feed: the data-availability "
                        f"gate declines it until a campaign_data_policy.yaml designation covers it")
    return record, f"requires_feed:{feed} -- not wired in {FEED_REGISTRY_MODULE}.{FEED_REGISTRY_NAME}"


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


# E-036 S2a (slice 8.1): the exact-match key and its lookup live in
# tools/novelty.py, extracted verbatim from here, so this module and the 5a
# gate (tools/anti_adjacency_gate.py) share ONE definition of "the same idea".
# Re-exported under their old names. decide_next's behaviour is unchanged
# (tests/test_e036_s2a_exact_match_gate.py pins it against the pre-extraction
# code) except for two DECLARED changes: a memory entry marked `legacy: true`
# can no longer produce a REPEAT (slice 8.1), and a memory entry whose
# protocol file is unparseable now keys "unresolved" (never matches) with a
# warning instead of crashing the decision.
normalize_timeframe = _nov.normalize_timeframe
normalize_ref = _nov.normalize_ref
protocol_spec = _nov.protocol_spec
novelty_key = _nov.novelty_key
_exact_index = _nov.exact_index


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
    still outstanding (queued/ready/in_progress) or held (blocked_on_*, CUL-398:
    it has not run to the end). True when it ran to `done` with any other
    outcome than the empty ones. False otherwise -- a
    retired-routing park (paused:waiting_for_*) included, since it tested
    nothing:
    completed_no_new_hypothesis, completed_brief_exhausted, a quarantine, a
    failure or pause (paused:*), or superseded."""
    status = str(entry.get("status") or "")
    if status in _OUTSTANDING_STATUSES:
        return None
    # CUL-398 (2026-10-04): a held request (blocked_on_*, the operator's hold or a
    # component quarantine) has not run to the end: it neither counts nor breaks
    # the streak. An operator hold also keeps R2 off its brief (r2_held_owner).
    if r2_request_held(entry):
        return None
    # Slice 6c S2c review fix 1: a parked request (paused:waiting_for_*) tested
    # nothing, so it counts as EMPTY (the `paused:` fall-through below): a brief
    # whose cards keep parking auto-exhausts, and R2 terminates. An unparked
    # card still comes back through the queue (--unpark sets it ready).
    if status.startswith(PARKED_STATUS_PREFIX):
        return False
    if status == "done":
        return entry.get("outcome") not in _EMPTY_R2_OUTCOMES
    return False


def _requests_since_reopen(owner: dict, entries: list) -> tuple:
    """(R2 requests on `owner`'s brief in request-number order, whether the
    owner's own run still counts), honouring the operator's reopen marker
    (REOPENED_AFTER_KEY). A marker naming neither the owner nor one of its
    requests raises: a typo must not silently count the whole history."""
    mine = sorted((e for e in entries if is_r2_request(e) and brief_owner(e, entries) is owner),
                  key=lambda e: _request_number(e, owner["id"]))
    cut = owner.get(REOPENED_AFTER_KEY)
    if not cut:
        return mine, True
    if cut == owner["id"]:
        return mine, False
    n = _request_number({"id": cut}, owner["id"])
    if n == 0:
        raise DecideNextError(f"{owner['id']}: {REOPENED_AFTER_KEY}={cut!r} names neither the "
                              f"owner nor one of its {owner['id']}__more_<n> requests")
    return [e for e in mine if _request_number(e, owner["id"]) > n], False


def consecutive_exhausted(owner: dict, entries: list) -> list:
    """O-20: the ids of the trailing run of step-1a "exhausted" answers on
    `owner`'s brief -- the owner's own run first, then its R2 requests in
    request-number order, after any reopen marker. One answer per queue entry.
    A finished entry with any other outcome (a card, a repeat included) resets
    the run; an entry that gave no answer (not finished, held, parked, failed,
    superseded, quarantined) neither counts nor resets it."""
    mine, owner_counts = _requests_since_reopen(owner, entries)
    run = []
    for e in ([owner] if owner_counts else []) + mine:
        if str(e.get("status") or "") != "done":
            continue
        outcome = e.get("outcome")
        if outcome == BRIEF_EXHAUSTED_OUTCOME:
            run.append(e["id"])
        elif outcome is None or outcome in _NO_ANSWER_OUTCOMES:
            continue
        else:
            run = []
    return run


def consecutive_empty_r2(owner: dict, entries: list) -> list:
    """The ids of the trailing run of finished R2 requests on `owner`'s brief
    that yielded no new, eligible card (request-number order; outstanding
    requests neither count nor break the run; only requests after the
    operator's reopen marker count, O-20)."""
    mine, _owner_counts = _requests_since_reopen(owner, entries)
    streak = []
    for e in mine:
        yielded = r2_request_yielded(e)
        if yielded is None:
            continue
        streak = [] if yielded else streak + [e["id"]]
    return streak


def r2_request_held(entry: dict) -> bool:
    """CUL-398: an R2 request on hold (`blocked_on_*`)."""
    return str(entry.get("status") or "").startswith(HELD_STATUS_PREFIX)


def r2_request_operator_held(entry: dict) -> bool:
    """CUL-398 follow-up (operator, 2026-10-04): an OPERATOR hold -- any
    blocked_on_* except R9's automatic `blocked_on_component:<name>` quarantine.
    A quarantined request stays outstanding (r2_request_yielded -> None) but does
    not freeze its brief: R2 may still ask that brief for other ideas."""
    return r2_request_held(entry) and not str(entry.get("status") or "").startswith(
        COMPONENT_QUARANTINE_PREFIX)


def r2_held_owner(owner: dict, entries: list) -> bool:
    """CUL-398: True when the owner entry itself, or any R2 request on
    `owner`'s brief, carries an operator hold. R2 then neither flips a request
    ready nor mints a new one for that brief: the operator's hold holds the
    brief, not only the one entry (review S3a: an owner hold is listed too).
    E-068 PR 4 review (D-071): an operator-held EXTRA CARD of the brief holds it
    too -- e.g. a card waiting in blocked_on_operator_approval is an unrun idea
    of that brief, so R2 must not ask for more behind it. A component-
    quarantined card does not (D-069)."""
    return r2_request_operator_held(owner) or any(
        (is_r2_request(e) or is_card_entry(e)) and r2_request_operator_held(e)
        and brief_owner(e, entries) is owner
        for e in entries)


def r2_eligible_owner(entry: dict) -> bool:
    """An open brief whose owner entry is not superseded, paused or blocked
    (code-review fix 6). Like a parked owner, an owner under R9's automatic
    component quarantine stays eligible (review S3a: only an operator hold
    freezes a brief, decision (i) of 2026-10-04)."""
    status = str(entry.get("status") or "")
    return (entry.get("brief_status") == BRIEF_OPEN
            and (status.startswith(PARKED_STATUS_PREFIX)
                 or status.startswith(COMPONENT_QUARANTINE_PREFIX)
                 or not status.startswith(_R2_INELIGIBLE_OWNER_STATUS_PREFIXES)))


def _card_producer_id(card: dict, entries: list):
    """The id of the queue entry whose run wrote `card` (its card_ref's run is
    in that entry's run_ids), or None when no entry claims the run."""
    try:
        run = _card_source_run(card.get("card_ref"))
    except DecideNextError:
        return None
    return next((e.get("id") for e in entries
                 if run in (e.get("run_ids") or []) and not is_card_entry(e)), None)


def component_quarantines(owner: dict, entries: list) -> list:
    """E-068 PR 4 (D-071, review S3b of PR 3a): the ids of the entries on
    `owner`'s brief that are under R9's automatic component quarantine
    (`blocked_on_component:<name>`) -- the owner's own entry, its R2 requests
    and (review follow-up) its extra cards, which are new ideas of the brief
    too. Counted after the operator's reopen marker (_requests_since_reopen),
    so a reopen resets the count; with a marker, a card counts only when the
    entry that wrote it (_card_producer_id) still counts. A released entry no
    longer counts."""
    mine, owner_counts = _requests_since_reopen(owner, entries)
    counted = {e["id"] for e in mine} | ({owner["id"]} if owner_counts else set())
    cards = [e for e in entries if is_card_entry(e) and brief_owner(e, entries) is owner
             and (not owner.get(REOPENED_AFTER_KEY) or _card_producer_id(e, entries) in counted)]
    return [e["id"] for e in ([owner] if owner_counts else []) + mine + cards
            if str(e.get("status") or "").startswith(COMPONENT_QUARANTINE_PREFIX)]


def r2_quarantine_capped(owner: dict, entries: list) -> bool:
    """At BRIEF_MAX_COMPONENT_QUARANTINES or more, R2 stops asking the brief
    (it is not closed: releasing entries makes it eligible again)."""
    return len(component_quarantines(owner, entries)) >= BRIEF_MAX_COMPONENT_QUARANTINES


def _next_request_id(owner_id: str, taken: set) -> str:
    n = 1
    while f"{owner_id}__more_{n}" in taken:
        n += 1
    return f"{owner_id}__more_{n}"


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def requests_count(doc) -> int:
    """The rows of a {requests: [...]} file (component or data requests) the
    decision record counts. E-068 nearest build (operator 2026-10-05): a
    `kind: deviation` row records a missing piece of a run that continued --
    never a park -- so it is not counted."""
    rows = (doc.get("requests") or []) if isinstance(doc, dict) else []
    return sum(1 for r in rows if not (isinstance(r, dict) and r.get("kind") == "deviation"))


def load_inputs(root: Path, queue: dict, *, categories: list, known_classes=None,
                digest=None, composition_runs: bool = False, dsr_basis: dict | None = None,
                feed_set=None, folds: dict | None = None, fold_data: dict | None = None) -> dict:
    """Everything decide() reads, from disk under `root` (strategy-research/).
    `queue` is the caller's in-memory queue document (after its own write).
    `known_classes` is the known component class set (known_component_classes)
    or None; `digest` the legacy exclusion digest document or None.
    `feed_set` (E-035 S2c): None, a load_feed_set document, or a zero-argument
    callable returning one. It is used -- and a callable is CALLED -- only
    when some loaded proposal carries `requires_feed`; otherwise
    inputs["feed_set"] is None and nothing about feeds is read, so a campaign
    whose readers never ask for a feed does not depend on the feed registry's
    syntax. A callable's DecideNextError propagates (fail loud).
    `composition_runs` (E-060 S3b; the caller passes
    run_phase1_research._composition_runs_enabled()): also read the whole
    block registry, campaign_record/compositions.yaml and each forecast
    block's validating run (inputs["composition"]) -- R1's inputs. Off: no
    such key, nothing more is read, and R1 stays the recorded no-op.
    `folds` (E-077 PR-1, D-085; the caller passes research_folds.load_folds(...) only
    under orchestrator.folds.enabled): the validated folds document. Then every
    memory run's protocol windows are read (inputs["folds"]["run_ranges"]) so a
    candidate's child can be given the next fold its lineage has not used. None:
    no such key, nothing more is read, and every candidate is as before.
    `fold_data` (with `folds`; run_phase1_research._fold_data_context): {layer1, precheck,
    first_symbol_only} -- what `_fold_data_reason` needs to refuse a child that has no data on
    its fold. None: that check is skipped."""
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
            # E-068 PR 4 (D-071): the card's raw text, so a class name the
            # reader quoted from the card is not reported as unknown.
            "card_text": ((arts / "hypothesis_card.yaml").read_text(encoding="utf-8")
                          if (arts / "hypothesis_card.yaml").exists() else None),
        }
        # E-073 step 2 (D-083): written only under orchestrator.observable_backtest;
        # absent files add no key, so every other run's inputs are unchanged.
        runs[run_id].update(_observable_inputs(arts))

    def _count(name):
        return requests_count(_load_yaml_opt(root / "campaign_record" / name) or {})

    # E-036 S2a: the one protocol-spec loop (tools/novelty.protocol_specs). An
    # unreadable memory protocol is None -> that entry keys "unresolved".
    specs = _nov.protocol_specs(root, memory)
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

    needs_feeds = any("requires_feed" in item["proposal"]
                      for src in runs.values() for item in src["proposals"])
    if needs_feeds and callable(feed_set):
        feed_set = feed_set()

    out = {
        "brief_cards": brief_cards,
        "memory": memory,
        "protocol_specs": specs,
        "existing_candidate_briefs": existing_briefs,
        "memory_sha256": (hashlib.sha256(mem_path.read_bytes()).hexdigest()
                          if mem_path.exists() else None),
        "registry_revision": registry.get("revision", 0),
        "queue": copy.deepcopy(queue),
        "known_classes": sorted(known_classes) if known_classes is not None else None,
        "feed_set": copy.deepcopy(feed_set) if needs_feeds else None,
        "digest": digest,
        "runs": runs,
        "component_requests_count": _count("component_requests.yaml"),
        "data_requests_count": _count("data_requests.yaml"),
    }
    if folds is not None:
        out["folds"] = {"doc": copy.deepcopy(folds), "run_ranges": _memory_run_ranges(root, memory),
                        "data": fold_data}
    if composition_runs:
        # E-060 S3b (7.5 + review fix 6): only under the flag -- a composition
        # run's manifest and the check its reader patches must pass. Flag off,
        # a composite's patch has no manifest here: source_manifest_missing.
        comp_inputs = load_composition_inputs(root, registry, memory, queue=queue,
                                              dsr_basis=dsr_basis)
        for run_id, src in runs.items():
            man = _load_yaml_opt(root / "runs" / run_id / "artifacts" / COMPOSITION_MANIFEST_FILE)
            if isinstance(man, dict):
                src["composition_manifest"] = man
                src["composition_check"] = _composition_checker(root, registry, man)
        out["composition"] = comp_inputs
    return out


def _memory_run_ranges(root: Path, memory: dict) -> dict:
    """{run_id: [(start, end), ...] or None} -- the test windows of every memory run's
    protocol (E-077 PR-1). None for a run whose protocol is unnamed, missing or
    unreadable: the lineage check then refuses rather than guess which bars it saw."""
    out = {}
    for run_id, entry in (memory.get("runs") or {}).items():
        ref = _nov.normalize_ref((entry or {}).get("protocol_ref"))
        ranges = None
        if ref:
            try:
                ranges = _folds.windows_ranges(_nov.load_protocol(root, ref).get("windows"))
            except _nov.NoveltyError:
                ranges = None
        out[run_id] = ranges
    return out


def _observable_inputs(arts: Path) -> dict:
    """E-073 step 2 (D-083): the run's in-run merges (side_finding_merges.yaml)
    and its flagged citations (citation_checks/<category>.yaml: {proposal id:
    [bad citations]}), each only when its file exists. Information only: an
    unreadable file counts as absent (a warning is never worth a stop)."""
    import reader_findings as _rf  # tools/ sibling; only E-073 runs need it
    out = {}
    merges_path = arts / _rf.MERGES_ARTIFACT
    if merges_path.exists():
        try:
            out["side_finding_merges"] = _rf.merge_index(_load_yaml_opt(merges_path))
        except (yaml.YAMLError, OSError, UnicodeDecodeError):
            out["side_finding_merges"] = {}
    checks_dir = arts / _rp.CITATION_CHECKS_DIR
    if checks_dir.is_dir():
        flagged = {}
        for path in sorted(checks_dir.glob("*.yaml")):
            try:
                doc = _load_yaml_opt(path)
            except (yaml.YAMLError, OSError, UnicodeDecodeError):
                continue
            items = doc.get("items") if isinstance(doc, dict) else None
            for pid, rec in (items.items() if isinstance(items, dict) else []):
                bad = rec.get("bad") if isinstance(rec, dict) else None
                if isinstance(bad, list) and bad:
                    flagged[str(pid)] = bad
        out["citation_flags"] = flagged
    return out


def _composition_checker(root: Path, registry: dict, manifest: dict):
    """callable(config) -> None | reason: tools/composition.check_composition_config
    against the source composition manifest (base = equal weights) -- the same
    check 5a runs, so a patch decide-next admits is one 1b/5a accept (review
    fix 3)."""
    def check(config):
        import composition as _comp  # lazily: flag-on only
        try:
            _comp.check_composition_config(config, manifest, "base", root=root,
                                           registry_doc=registry)
        except _comp.CompositionError as exc:
            return str(exc)
        return None
    return check


# ---------------------------------------------------------------------------
# E-060 S3b -- R1, the composition trigger (S1_FINDINGS.md §4, guesses 3, 10,
# 11 and operator decisions 3 + 6). Only when inputs carry "composition"
# (orchestrator.composition_runs on); otherwise R1 is the recorded no-op.
# ---------------------------------------------------------------------------

ORIGIN_COMPOSITION = _names.ORIGIN_COMPOSITION
COMPOSITION_MANIFEST_FILE = _names.MANIFEST_FILENAME
COMPOSITIONS_DIR = _names.COMPOSITIONS_DIR
COMPOSITIONS_FILE = _names.COMPOSITIONS_FILE
COMPOSITION_HYPOTHESIS_PREFIX = "COMPOSITION"


def composition_entry_id(timeframe: str, registry_hash: str) -> str:
    """The queue id (and brief / directory name) of the composition of one
    exact timeframe's block set. registry_hash identifies that set
    (composite_cache.composite_registry_hash), so the id is stable for one
    registry state of that timeframe and new when a block joins it -- R1 fires
    ONCE per registry revision per timeframe."""
    tf = normalize_timeframe(timeframe)
    eid = f"composition-{tf}-{registry_hash}"
    if not tf or not _SAFE_ID_RE.fullmatch(eid):
        raise DecideNextError(f"timeframe {timeframe!r} gives an unsafe composition id {eid!r}")
    return eid


def composition_attempt_id(base_id: str, attempt: int) -> str:
    """Attempt 1 is the base id; a re-fire after an inconclusive attempt
    (review fix 1) is `<base>-a<n>`."""
    return base_id if attempt <= 1 else f"{base_id}-a{attempt}"


def _attempts(base_id: str, entries: list) -> list:
    """[(attempt n, entry)] of every queue entry of one block set, oldest first."""
    out = []
    for e in entries:
        eid = str(e.get("id") or "")
        if eid == base_id:
            out.append((1, e))
        else:
            m = re.fullmatch(re.escape(base_id) + r"-a(\d+)", eid)
            if m:
                out.append((int(m.group(1)), e))
    return sorted(out, key=lambda t: t[0])


# The one bar whose NOT_EVALUABLE can clear with time: the deflated Sharpe
# needs >= 2 trials in the ledger (and >= 2 real Sharpe values). The others
# (drawdown / avg daily return coverage, trade counts) are properties of the
# composite's own fixed data, so re-running would give the same answer.
_REFIRABLE_BAR = "deflated_sharpe_threshold"
_MIN_DSR_TRIALS = 2  # run_phase1_research._promotion_dsr_context's own minimum


def load_composition_inputs(root: Path, registry: dict, memory: dict, *, queue=None,
                            dsr_basis: dict | None = None) -> dict:
    """R1's inputs: the registry document, compositions.yaml's entries and
    failure rows, for every forecast block that carries a timeframe its
    validating run's pre_registration.yaml and research_brief.yaml (the
    composition brief's protocol pin and brief keys) and the pinned protocol
    files, and -- for every finished INCONCLUSIVE composition attempt -- its
    last run's profit_bars_evaluation.yaml summary (review fix 1).
    `dsr_basis`: the CURRENT trial-ledger basis {n_dsr_total, n_trials}
    (run_phase1_research._promotion_dsr_context), passed by the caller.
    Read only."""
    import composite_cache as _cc  # tools/ sibling, lazily: flag-on only
    import composition as _comp
    root = Path(root)
    sources, protocols = {}, {}
    for block in registry.get("blocks") or []:
        run_id = block.get("validated_by_run")
        if block.get("kind") != "forecast" or not block.get("timeframe") or run_id in sources:
            continue
        arts = root / "runs" / str(run_id) / "artifacts"
        ref = normalize_ref(((memory.get("runs") or {}).get(run_id) or {}).get("protocol_ref"))
        sources[run_id] = {
            "pre_registration": _load_yaml_opt(arts / "pre_registration.yaml"),
            "research_brief": _load_yaml_opt(arts / "research_brief.yaml"),
            "protocol_ref": ref,
        }
        if ref and ref not in protocols and (root / ref).is_file():
            text = (root / ref).read_text(encoding="utf-8")
            protocols[ref] = json.loads(text) if ref.endswith(".json") else yaml.safe_load(text)
    inconclusive = {}
    for e in _entries(queue):
        if (e.get("origin") == ORIGIN_COMPOSITION and e.get("status") == "done"
                and e.get("outcome") == "inconclusive" and e.get("run_ids")):
            ev = _load_yaml_opt(root / "runs" / e["run_ids"][-1] / "artifacts" /
                                "profit_bars_evaluation.yaml")
            ev = ev if isinstance(ev, dict) else {}
            not_eval = sorted({b.get("name") for v in (ev.get("variants") or {}).values()
                               if isinstance(v, dict) for b in (v.get("bars") or [])
                               if isinstance(b, dict) and b.get("result") == "NOT_EVALUABLE"})
            inconclusive[e["id"]] = {"not_evaluable": not_eval, "dsr_basis": ev.get("dsr_basis")}
    path = root / _names.COMPOSITIONS_FILE
    return {"registry": copy.deepcopy(registry),
            "compositions": _cc.load_compositions(path),
            "failures": _comp.load_composition_failures(path),
            "sources": sources, "protocols": protocols,
            "inconclusive": inconclusive, "dsr_basis": dsr_basis}


def _dsr_computable(basis) -> bool:
    return (isinstance(basis, dict) and (basis.get("n_dsr_total") or 0) >= _MIN_DSR_TRIALS
            and (basis.get("n_trials") or 0) >= _MIN_DSR_TRIALS)


def _classify_block_set(base_id: str, registry_hash: str, entries: list,
                        comp_inputs: dict) -> tuple:
    """(status, entry_id, reason) for one block set with >= 2 blocks:
      * failed_before -- an unresolved failure row in compositions.yaml (a
        preparation fault, review fix 2): never re-fired by code;
      * fired_before  -- an attempt exists and is outstanding, done with a
        binding answer, paused, or inconclusive with its missing input still
        missing;
      * eligible      -- no attempt yet, or (review fix 1) the latest attempt
        ended inconclusive ONLY because the deflated-Sharpe bar was not
        evaluable for want of trials, and the ledger now has them -- a NEW
        attempt id, so a finished attempt is never re-run in a loop."""
    failures = [f for f in comp_inputs.get("failures") or []
                if f.get("registry_hash") == registry_hash and f.get("resolved") is not True]
    if failures:
        return ("failed_before", None,
                f"preparation failed ({failures[-1].get('entry_id')}: "
                f"{str(failures[-1].get('reason'))[:200]}); unresolved in "
                f"{_names.COMPOSITIONS_FILE} -- set resolved: true to allow a new attempt")
    attempts = _attempts(base_id, entries)
    if not attempts:
        return "eligible", base_id, "never composed in this registry state"
    n, last = attempts[-1]
    if last.get("status") != "done" or last.get("outcome") != "inconclusive":
        return ("fired_before", None,
                f"attempt {last.get('id')} is {last.get('status')} "
                f"(outcome {last.get('outcome')!r})")
    info = (comp_inputs.get("inconclusive") or {}).get(last.get("id")) or {}
    not_eval = info.get("not_evaluable") or []
    if not not_eval or set(not_eval) - {_REFIRABLE_BAR}:
        return ("fired_before", None,
                f"attempt {last.get('id')} was inconclusive on {not_eval or 'unknown bars'}: "
                f"properties of its own data, a re-run would give the same answer")
    if isinstance(info.get("dsr_basis"), dict) and "sharpe_basis" in info["dsr_basis"]:
        # E-062 S2b-2b review fix 4: the whole-test DSR (D-046) is never
        # NOT_EVALUABLE for want of trials -- only on the candidate's own data
        # (its stats, a dedup collapse, a ledger mismatch) -- so a re-run gives
        # the same answer; the legacy n_trials rule below does not apply.
        return ("fired_before", None,
                f"attempt {last.get('id')} was inconclusive on the whole-test deflated Sharpe "
                f"({info.get('dsr_basis')}): a property of its own data, not a missing input")
    if _dsr_computable(info.get("dsr_basis")):
        return ("fired_before", None,
                f"attempt {last.get('id')} was inconclusive although the ledger already had "
                f"enough trials ({info.get('dsr_basis')}) -- not a missing input")
    if not _dsr_computable(comp_inputs.get("dsr_basis")):
        return ("fired_before", None,
                f"attempt {last.get('id')} was inconclusive for want of trials "
                f"({info.get('dsr_basis')}); the ledger still has "
                f"{comp_inputs.get('dsr_basis')} -- waits until it has >= {_MIN_DSR_TRIALS}")
    return ("eligible", composition_attempt_id(base_id, n + 1),
            f"attempt {last.get('id')} was inconclusive for want of trials "
            f"({info.get('dsr_basis')}); the ledger now has {comp_inputs.get('dsr_basis')}")


def _r1_timeframes(comp_inputs: dict, entries: list) -> tuple:
    """([per-timeframe row], excluded_blocks). One row per exact bar size
    (in seconds; shortest first) that carries at least one forecast block:
    {timeframe, timeframe_category, block_ids, registry_hash, entry_id,
    status, reason}. status: `single_block` (fewer than 2 -- operator
    decision 3), else _classify_block_set's."""
    import composite_cache as _cc  # lazily: flag-on only
    import timeframe as _tf
    registry = comp_inputs["registry"]
    by_secs: dict = {}
    for block in registry.get("blocks") or []:
        if block.get("kind") == "forecast" and block.get("timeframe"):
            by_secs.setdefault(_tf.timeframe_seconds(block["timeframe"]), block["timeframe"])
    rows, excluded = [], []
    for secs in sorted(by_secs):
        tf = by_secs[secs]
        blocks, excl = _cc.forecast_blocks_on_timeframe(registry, tf)
        excluded = excl
        ids = sorted(b["block_id"] for b in blocks)
        row = {"timeframe": tf, "timeframe_category": _cc.timeframe_category(tf),
               "block_ids": ids, "registry_hash": None, "entry_id": None}
        if len(blocks) < 2:
            row["status"], row["reason"] = "single_block", "fewer than 2 forecast blocks"
        else:
            row["registry_hash"] = _cc.composite_registry_hash(blocks)
            base = composition_entry_id(tf, row["registry_hash"])
            status, eid, reason = _classify_block_set(base, row["registry_hash"], entries,
                                                      comp_inputs)
            row.update(status=status, entry_id=eid or base, reason=reason)
        rows.append(row)
    if not by_secs:
        # every forecast block lacks a timeframe (or there is none): still
        # report the excluded ones, loudly (composite_cache prints them)
        forecast = [b for b in registry.get("blocks") or [] if b.get("kind") == "forecast"]
        if forecast:
            _, excluded = _cc.forecast_blocks_on_timeframe(registry, "1h")
    return rows, excluded


def _r1(inputs: dict, entries: list, *, scheduled, operator: list) -> tuple:
    """(r1 record, request or None). Flag off (no inputs["composition"]): the
    unchanged no-op record. Flag on: the first `eligible` timeframe (shortest
    bar first) fires unless a run is in progress or an operator entry is
    ready (guess 10: behind both); it is then scheduled AHEAD of every agent
    entry (reader candidates, extra cards, R2 requests, reframes) by a
    priority strictly below every ready agent entry's. One composition per
    decision; the next eligible timeframe fires at a later decision."""
    revision = inputs.get("registry_revision") or 0
    comp_inputs = inputs.get("composition")
    if comp_inputs is None:
        return ({"registry_revision": revision, "last_composition_revision": None,
                 "would_fire": revision >= 2, "fired": False,
                 "reason": "composition brief writer is slice 7"}, None)
    rows, excluded = _r1_timeframes(comp_inputs, entries)
    revs = [c.get("registry_revision") for c in comp_inputs.get("compositions") or []
            if isinstance(c, dict) and isinstance(c.get("registry_revision"), int)]
    eligible = [r for r in rows if r["status"] == "eligible"]
    rec = {"registry_revision": revision,
           "last_composition_revision": max(revs) if revs else None,
           "would_fire": bool(eligible), "fired": False, "reason": "",
           "timeframes": rows, "excluded_blocks": excluded}
    if not eligible:
        rec["reason"] = ("no timeframe has a new set of >= 2 forecast blocks (operator decision "
                         "3: same exact bar size only; R1 fires once per registry state)")
        return rec, None
    if scheduled is not None and scheduled.get("status") == "in_progress":
        rec["reason"] = f"deferred: {scheduled.get('id')} is in progress (guess 10)"
        return rec, None
    if operator:
        rec["reason"] = (f"deferred: operator entr{'y' if len(operator) == 1 else 'ies'} "
                         f"{[e['id'] for e in operator]} ready (guess 10: behind operator entries)")
        return rec, None
    row = eligible[0]
    ready_prios = [e.get("priority", AGENT_PRIORITY) for e in entries if e.get("status") == "ready"]
    priority = min([AGENT_PRIORITY] + [p for p in ready_prios if isinstance(p, (int, float))]) - 1
    rec.update(fired=True, entry_id=row["entry_id"], timeframe=row["timeframe"],
               registry_hash=row["registry_hash"], priority=priority,
               reason=(f"the forecast blocks on {row['timeframe']} ({len(row['block_ids'])}) have "
                       f"not been composed in this registry state: composition "
                       f"{row['entry_id']} queued ahead of agent entries"))
    return rec, {"row": row, "priority": priority}


def _composition_pin(comp_inputs: dict, block_ids: list) -> dict:
    """The protocol pin of a composition: the validating runs' most common
    protocol_ref, tie -> the most recently registered block's (S1 §4). Returns
    {run_id, machine_constraints (pass_rule dropped), research_brief}.
    Raises when a block's run has no memory protocol_ref or no pin."""
    registry = comp_inputs["registry"]
    order = [b for b in registry.get("blocks") or [] if b.get("block_id") in set(block_ids)]
    counts: dict = {}
    for b in order:
        src = comp_inputs["sources"].get(b["validated_by_run"]) or {}
        ref = src.get("protocol_ref")
        if not ref:
            raise DecideNextError(f"block {b['block_id']!r}: its run {b['validated_by_run']} has no "
                                  f"protocol_ref in the campaign memory -- no protocol to pin")
        counts[ref] = counts.get(ref, 0) + 1
    top = max(counts.values())
    # registry order is append order: the last block with a top-count ref wins a tie
    run_id = next(b["validated_by_run"] for b in reversed(order)
                  if counts[comp_inputs["sources"][b["validated_by_run"]]["protocol_ref"]] == top)
    src = comp_inputs["sources"][run_id]
    mc = copy.deepcopy(((src.get("pre_registration") or {}).get("machine_constraints")) or {})
    if not mc:
        raise DecideNextError(f"{run_id}: pre_registration.yaml carries no machine_constraints -- "
                              f"the composition's windows cannot be pinned")
    mc.pop("pass_rule", None)  # criteria are the profit bars, never inherited
    if not isinstance(src.get("research_brief"), dict):
        raise DecideNextError(f"{run_id}: research_brief.yaml is missing")
    return {"run_id": run_id, "machine_constraints": mc, "research_brief": src["research_brief"],
            "protocol_ref": src["protocol_ref"], "protocol_counts": counts}


def composition_window_starts(inputs: dict, block_ids: list) -> list:
    """The composite's window test-start dates: the windows of the protocol
    the composition is pinned to (_composition_pin). The per-window weights
    are estimated before each (tools/composition.window_weight_schedule).
    Raises when the pinned protocol file or its window dates are missing."""
    comp = inputs["composition"]
    pin = _composition_pin(comp, block_ids)
    proto = (comp.get("protocols") or {}).get(pin["protocol_ref"])
    windows = proto.get("windows") if isinstance(proto, dict) else None
    starts = [((w or {}).get("test") or {}).get("start") for w in windows or []
              if isinstance(w, dict)]
    if not starts or not all(isinstance(x, str) and x for x in starts):
        raise DecideNextError(f"pinned protocol {pin['protocol_ref']!r} has no window test start "
                              f"dates -- the per-window weights cannot be placed")
    return sorted(set(starts))


def composition_brief(record: dict, inputs: dict, manifest: dict, *, manifest_ref: str,
                      manifest_sha256: str, decision_ref: str) -> tuple:
    """(rel_path, text) of the brief for record['picked'] (an R1 composition).
    Frontmatter: the pinned validating run's brief keys and machine_constraints
    (no pass_rule), a research goal naming the blocks, and `candidate` =
    {criteria_from: hypothesis_generation, composition: {manifest_ref,
    manifest_sha256, registry_revision, registry_hash, timeframe,
    timeframe_category, block_ids}, source: {origin: composition,
    hypothesis_id, decision_ref, base_config_ref, expected_config_sha256}}.
    The configs and the manifest are code-written (tools/composition.py);
    steps 1a / 1b pass them through and author nothing."""
    picked = record.get("picked") or {}
    r1 = record["rules"]["r1"]
    if not picked.get("composition") or picked["composition"] != r1.get("entry_id"):
        raise DecideNextError("composition_brief: the record's pick is not R1's composition")
    if manifest.get("registry_hash") != r1["registry_hash"]:
        raise DecideNextError(f"the written manifest's registry_hash {manifest.get('registry_hash')} "
                              f"is not R1's {r1['registry_hash']}")
    comp = inputs["composition"]
    block_ids = [b["block_id"] for b in manifest["blocks"]]
    pin = _composition_pin(comp, block_ids)
    brief = pin["research_brief"]
    front = {k: brief.get(k) for k in ("strategy_domain", "market_universe", "timeframe",
                                       "venue", "product")}
    front["timeframe"] = manifest["timeframe"]
    front["research_goal"] = (
        f"Composition of the {len(block_ids)} validated forecast blocks on {manifest['timeframe']} "
        f"({', '.join(block_ids)}), each run as validated, standardised past-only and weighted "
        f"three ways (equal, inverse stand-alone volatility, residual IC). Graded on the profit "
        f"bars (card F).")
    front["machine_constraints"] = pin["machine_constraints"]
    base = manifest["variants"]["base"]
    hyp = f"{COMPOSITION_HYPOTHESIS_PREFIX}-{picked['composition'][len('composition-'):]}"
    front["candidate"] = {
        "criteria_from": CRITERIA_FROM_1A,
        "composition": {"manifest_ref": manifest_ref, "manifest_sha256": manifest_sha256,
                        "registry_revision": manifest.get("registry_revision"),
                        "registry_hash": manifest["registry_hash"],
                        "timeframe": manifest["timeframe"],
                        "timeframe_category": manifest["timeframe_category"],
                        "block_ids": block_ids},
        "source": {"origin": ORIGIN_COMPOSITION, "hypothesis_id": hyp,
                   "decision_ref": decision_ref, "protocol_pinned_from": pin["run_id"],
                   "base_config_ref": base["config_ref"],
                   "expected_config_sha256": base["config_sha256"]},
    }
    rel = picked["brief_path"]
    text = ("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n\n"
            f"# {picked['composition']}\n\n"
            f"Written by tools/decide_next.py (E-060 S3b, R1) after "
            f"{record['trigger'].get('after_run')}; decision record: {decision_ref}.\n\n"
            "The three variant configs and the composition manifest were written by code "
            f"({manifest_ref}); step 1a passes this candidate through (criteria = the profit bars) "
            "and step 1b authors nothing. A composite never registers as a block.\n")
    return rel, text


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
    # E-036 S2a: anti_adjacency_gate.layer2_digest_check is now the exact-match
    # check; the family-grain lookup this field records moved, unchanged, to
    # build_exclusion_digest.legacy_family_lookup (information only).
    import build_exclusion_digest as _bed  # tools/ sibling, imported lazily
    return _bed.legacy_family_lookup(card, (symbols or [None])[0], timeframe, digest,
                                     candidate_config=config)


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
    # E-077 PR-1 (D-085): only under orchestrator.folds.enabled (inputs["folds"]).
    fold_assignment = None
    if inputs.get("folds") is not None:
        fold_assignment = _fold_assignment_for(run_id, pre_reg, inputs, src.get("research_brief"))
        if fold_assignment["reason"]:
            reasons.append(fold_assignment["reason"])
    fold_sha = (fold_assignment or {}).get("windows_sha256")
    if p["kind"] == "patch":
        if base.get("status") != "tested":
            reasons.append("source_base_variant_not_tested")
        # E-060 S3b (7.5): a composition run has no block_manifest.yaml; its
        # composition manifest is the source manifest (only such a run has one).
        comp_manifest = src.get("composition_manifest")
        if not isinstance(src.get("base_config"), dict):
            reasons.append("source_config_missing: the source base variant's config is not on disk")
        elif not isinstance(src.get("manifest"), dict) and not isinstance(comp_manifest, dict):
            reasons.append("source_manifest_missing: a pass-through config needs the source "
                           "block_manifest.yaml")
        else:
            ops, patched, why = resolve_patch(p, src["base_config"])
            if why:
                reasons.append(why)
            else:
                config_for_digest = patched
                resolved_sha = config_sha256(patched)
                if isinstance(comp_manifest, dict):
                    # review fix 3: the SAME check 1b/5a run (weights, lookback,
                    # class, source gate, detector, standardisation, scaffolding).
                    check = src.get("composition_check")
                    bad = check(patched) if check else "no composition check was loaded"
                    if bad:
                        reasons.append(f"composition_check_failed: {bad}")
                else:
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
        # E-035 S2c: a patch waits on its feed (INFEASIBLE, recorded, never
        # dropped) only if the resolved config consumes it and it is not wired.
        feed_record, feed_reason = requires_feed_gate(p, inputs.get("feed_set"), config_for_digest)
        if feed_reason:
            reasons.append(feed_reason)
        if resolved_sha:
            key = novelty_key(resolved_sha, symbols, entry, inputs.get("protocol_specs") or {},
                              **({"windows_sha256": fold_sha} if fold_sha else {}))
            matched = list(exact.get(key) or [])
            novelty = {"exact_match": "REPEAT" if matched else "NOVEL", "matched_runs": matched}
        else:
            novelty = {"exact_match": "NOT_EVALUATED", "matched_runs": []}
        feas = "INFEASIBLE" if reasons else "FEASIBLE"
    elif p["kind"] == _rp.SIDE_FINDING:
        # E-068 slice 5 (D-073): a reader's side finding is a claim block; its
        # brief carries that claim pre-filled. No config exists before 1b, so
        # novelty is not applicable (its tests' spec_hashes are recorded) and
        # 1b + step 3's data gate decide feasibility, as for a sketch.
        side_review = _side_finding_review(run_id, src, p, inputs)
        if side_review["errors"]:
            reasons.append("next_test_refused: " + "; ".join(side_review["errors"]))
        elif side_review["tests_none"]:
            reasons.append(f"next_test_none: missing block {side_review['missing_block']!r} "
                           f"(recorded as a test request)")
        if _cc_kind_block((p.get("claim") or {}).get("kind")) == "regime":
            reasons.append("regime_block_needs_composition: a regime block is validated only "
                           "as a composition variant (cards A/F, slice 7)")
        # CUL-412: the finding starts from the source run's config (and its own
        # config change, resolved like a patch), so the claim is tested on the
        # block it is about.
        start = side_finding_start(p, src)
        if start["reason"]:
            reasons.append(start["reason"])
        elif start["ops"]:
            config_for_digest = start["config"]
            resolved_sha = config_sha256(start["config"])
            missing = _jp.manifest_missing_paths(start["config"], start["manifest"])
            if missing:
                reasons.append(f"manifest_unresolved: {missing}")
            new_classes = _component_classes(start["config"]) - _component_classes(
                src["base_config"])
            if new_classes:
                known = inputs.get("known_classes")
                unknown = sorted(new_classes - set(known)) if known is not None \
                    else sorted(new_classes)
                if unknown:
                    reasons.append(f"unknown_component_class: {unknown}")
        elif start["config"] is not None:
            config_for_digest = start["config"]
        # unchanged: a side finding's requires_feed is data its TEST needs, so it
        # waits until the feed is wired whatever the config reads
        feed_record, feed_reason = requires_feed_gate(p, inputs.get("feed_set"))
        if feed_reason:
            reasons.append(feed_reason)
        if resolved_sha:
            # a config change: the changed config has a novelty key like a patch's
            key = novelty_key(resolved_sha, symbols, entry, inputs.get("protocol_specs") or {},
                              **({"windows_sha256": fold_sha} if fold_sha else {}))
            matched = list(exact.get(key) or [])
            novelty = {"exact_match": "REPEAT" if matched else "NOVEL", "matched_runs": matched,
                       "spec_hashes": list(side_review["spec_hashes"])}
        elif start["config"] is not None:
            novelty = {"exact_match": "NOT_APPLICABLE", "matched_runs": [],
                       "note": "the source run's config, unchanged: a new claim on it",
                       "spec_hashes": list(side_review["spec_hashes"])}
        else:
            novelty = {"exact_match": "NOT_APPLICABLE", "matched_runs": [],
                       "note": "no config until 1b authors it",
                       "spec_hashes": list(side_review["spec_hashes"])}
        feas = "INFEASIBLE" if reasons else "UNKNOWN"
        if not reasons:
            reasons.append("starts from the source run's config at 1b; step 3's data gate "
                           "stays binding" if start["config"] is not None else
                           "config authored at 1b; step 3's data gate stays binding")
    else:
        blk = p.get("block") or {}
        if blk.get("kind") == "regime":
            reasons.append("regime_block_needs_composition: a regime block is validated only "
                           "as a composition variant (cards A/F, slice 7)")
        # E-035 S2c: no config exists before 1b, so a sketch needing a feed that
        # is not wired waits for it.
        feed_record, feed_reason = requires_feed_gate(p, inputs.get("feed_set"))
        if feed_reason:
            reasons.append(feed_reason)
        novelty = {"exact_match": "NOT_APPLICABLE", "matched_runs": [],
                   "note": "no config until 1b authors it"}
        feas = "INFEASIBLE" if reasons else "UNKNOWN"
        if not reasons:
            reasons.append("config authored at 1b; step 3's data gate stays binding")
    novelty["digest_advisory"] = _digest_advisory(
        src.get("card"), config_for_digest, symbols, entry.get("timeframe"), inputs.get("digest"))
    backtests = n_windows * N_VARIANTS * len(symbols) if (n_windows and symbols) else None
    eligible = novelty["exact_match"] != "REPEAT" and feas != "INFEASIBLE"
    feasibility = {"result": feas, "reasons": reasons}
    if feed_record is not None:
        feasibility["requires_feed"] = feed_record
    if p["kind"] == "patch":
        collapse_key = ("patch", key) if key else ("single", pid)
    elif p["kind"] == _rp.SIDE_FINDING:
        # two readers proposing the same tests on the same START config are one
        # candidate (review: keyed on the start config even without a change, so
        # the same test from two source runs never collapses onto one block)
        hashes = tuple(sorted(novelty.get("spec_hashes") or []))
        # review round 2: with no start config (a composite source), the run itself
        start_sha = (config_sha256(start["config"]) if start["config"] is not None
                     else f"run:{run_id}")
        collapse_key = ("side_finding", hashes, start_sha) if hashes else ("single", pid)
    else:
        blk = p.get("block") or {}
        collapse_key = ("new_block", blk.get("kind"),
                        tuple(sorted(blk.get("config_paths") or [])), run_id)
    cand = {
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
                  "feasibility": feasibility},
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
    if fold_assignment is not None:
        # E-077 PR-1 (D-085): which fold the child gets and why (the lineage it was
        # read from, and the folds each lineage run used). Only under the flag.
        cand["fold_assignment"] = {k: fold_assignment[k] for k in ("fold", "lineage", "used")}
    warnings = class_name_warnings(p, inputs.get("known_classes"), src.get("card_text"))
    if p["kind"] == _rp.SIDE_FINDING:
        # E-068 slice 5: a repeated spec_hash or a block-kind claim whose tests
        # cannot see the block -- WARNINGS ONLY, never a reason or a rank change
        warnings = warnings + list(side_review["warnings"])
    if p["kind"] == _rp.SIDE_FINDING and pid in (src.get("citation_flags") or {}):
        # E-073 step 2 (D-083): kept, flagged -- a WARNING, never a reason or a rank change
        warnings = warnings + [{"kind": CITATION_WARNING,
                                "bad": copy.deepcopy(src["citation_flags"][pid])}]
    if warnings:  # E-068 PR 4 (D-071): only when non-empty -- other records unchanged
        cand["warnings"] = warnings
    merged = (src.get("side_finding_merges") or {}).get(pid)         if p["kind"] == _rp.SIDE_FINDING else None
    if merged:
        # E-073 step 2: an in-run duplicate (side_finding_merges.yaml) is folded
        # into its primary by _collapse; the primary's scores are kept
        cand["_merge"] = {"primary": merged["primary"], "order": merged["order"]}
    return cand


def _fold_assignment_for(run_id: str, pre_reg: dict, inputs: dict, brief=None) -> dict:
    """E-077 PR-1 (D-085): research_folds.assign_fold for a child of `run_id`, plus the
    two extra refusals that need the source's pre-registration: a source that PINS a
    protocol file (machine_constraints.protocol_ref) has no generated `protocol` block
    to put the fold's windows in, so its child cannot take a fold; and a child that has
    no data on the chosen fold (`_fold_data_reason`) -- INFEASIBLE with
    `fold_<X>_lacks_data`, the fold stays the one the lineage order gave (no skipping
    ahead to a fold the data would fit)."""
    f = inputs["folds"]
    result = _folds.assign_fold(f["doc"], run_id=run_id,
                                memory_runs=(inputs["memory"].get("runs") or {}),
                                run_ranges=f["run_ranges"])
    mc = pre_reg.get("machine_constraints")
    if (result["reason"] is None and isinstance(mc, dict)
            and not isinstance(mc.get("protocol"), dict)):
        result.update(fold=None, windows_sha256=None, reason=(
            "fold_needs_generated_protocol: the source pins a protocol file "
            "(machine_constraints.protocol_ref); a fold's windows can only be written into a "
            "generated machine_constraints.protocol block"))
    if result["reason"] is None and result["fold"] is not None:
        why = _fold_data_reason(result["fold"], mc.get("protocol"), brief, inputs)
        if why:
            result["reason"] = why
    return result


def _fold_data_reason(fold: str, protocol, brief, inputs: dict) -> str | None:
    """E-077 PR-1 review fix (D-085): why the child would have no data on `fold`, else None.

    Without it a fold the child's coin did not exist on (SOL lists 2021-06; fold B has
    blocks in 2018-2020) is assigned, the data-availability gate then declines the
    base, and under the variant loop the run is wasted. This is the gate's own layer-1
    coverage check -- variant_coin.window_coverage over data_availability_gate.layer1_price_precheck
    plus the listing rule (a window counts only when the coin exists for all of it) -- run
    on the fold's blocks for the child's symbols and timeframe, with the venue the
    brief maps to (tools/venue_resolver). Zero network, no market data. It is the
    base's pass/fail: the gate validates the base only when every window passes.
    NOT checked: aux feeds (the gate reads those in layer 2 only: cache/fetch). Skipped
    (None) when the caller supplied no `inputs["folds"]["data"]` (the production caller
    always does, run_phase1_research._fold_data_context). Never raises: an input that
    cannot be judged is a reason, not a crash."""
    ctx = inputs["folds"].get("data")
    if ctx is None or not isinstance(protocol, dict):
        return None
    prefix = f"fold_{fold}_lacks_data"
    try:
        import venue_resolver as _venue
        import variant_coin as _vc
        symbols = list(protocol.get("symbols") or [])
        exchange = "binance"
        keys = _venue.protocol_keys(brief if isinstance(brief, dict) else {}, symbols,
                                    layer1=ctx["layer1"])
        if keys:
            symbols, exchange = list(keys["symbols"]), keys["exchange"]
        if ctx.get("first_symbol_only"):
            symbols = symbols[:1]  # the variant loop backtests the base on symbols[0] only
        windows = _folds.fold_windows(inputs["folds"]["doc"], fold)
        lacking = []
        for symbol in symbols:
            cov = _vc.window_coverage(
                {"windows": windows, "timeframe": protocol.get("timeframe", "1h")},
                exchange=exchange, symbol=symbol, layer1=ctx["layer1"],
                precheck=ctx["precheck"], era_of=lambda ts: "era_unmapped")
            lacking += [f"{symbol} {u['label']}: {u['reason']}" for u in cov["uncovered"]]
    except Exception as e:  # noqa: BLE001 -- a reason, never a crash
        return f"{prefix}: the child's coverage of fold {fold} cannot be judged ({type(e).__name__}: {e})"
    if not lacking:
        return None
    more = f" (+{len(lacking) - 3} more)" if len(lacking) > 3 else ""
    return (f"{prefix}: the child's base would not pass the data-availability gate on fold "
            f"{fold} -- {'; '.join(lacking[:3])}{more}")


def side_finding_start(p: dict, src: dict) -> dict:
    """CUL-412 (operator, 2026-10-06): the config a reader's side finding starts
    from -- the source run's base config, with the finding's `config_change`
    applied (resolve_patch, the patch rules) when it has one -- and the source
    block manifest. {config, manifest, ops, reason}:
      * a composition source: nothing is carried (config None, reason None) --
        a composite has no block config to start from -- and a config_change
        there is a reason (`config_change_on_composition`, review: never
        silently dropped);
      * no base config or no block manifest on disk: reason
        `source_config_missing` (the candidate is INFEASIBLE);
      * a config_change that does not resolve: its resolve_patch reason.
    `ops` lists the resolved changes ([] when the finding carries none)."""
    if isinstance(src.get("composition_manifest"), dict):
        return {"config": None, "manifest": None, "ops": [],
                "reason": ("config_change_on_composition: a composite run has no block config "
                           "to apply the finding's config change to; propose the claim without "
                           "it") if p.get("config_change") else None}
    base, manifest = src.get("base_config"), src.get("manifest")
    if not isinstance(base, dict) or not isinstance(manifest, dict):
        return {"config": None, "manifest": None, "ops": [],
                "reason": ("source_config_missing: a side finding starts from the source "
                           "run's base config and block manifest (CUL-412), and they are "
                           "not on disk")}
    change = p.get("config_change")
    if not change:
        return {"config": copy.deepcopy(base), "manifest": copy.deepcopy(manifest),
                "ops": [], "reason": None}
    ops, patched, why = resolve_patch({"patch": change}, base)
    if why:
        return {"config": None, "manifest": None, "ops": [], "reason": f"config_change: {why}"}
    return {"config": patched, "manifest": copy.deepcopy(manifest), "ops": ops, "reason": None}


def _cc_kind_block(kind):
    import claim_card as _cc  # tools/ sibling; only side findings need it
    return _cc.KIND_BLOCK.get(kind) if isinstance(kind, str) else None


def _side_finding_review(run_id: str, src: dict, p: dict, inputs: dict) -> dict:
    """reader_findings.side_finding_review against the memory's findings
    (every run but the source run) and the source run's own claim tests."""
    import reader_findings as _rf  # tools/ sibling; only side findings need it
    prior = _rf.prior_spec_hashes(inputs.get("memory") or {}, exclude_run=run_id)
    return _rf.side_finding_review(p, prior=prior, own=_rf.own_spec_hashes(src.get("card")),
                                   run_id=run_id)


# E-068 PR 4 (D-071): the one warning kind a candidate can carry.
UNKNOWN_CLASS_WARNING = "unknown_component_class"


# E-073 step 2 (D-083): a side finding whose cited value did not match the file
# its reader read, after the reader's one retry (citation_checks/<category>.yaml)
CITATION_WARNING = "citation_mismatch"
MERGE_NOTE = ("in-run duplicates merged (E-073): the same tests proposed by more than one "
              "reader; not agreement and not extra evidence (the readers share their inputs), "
              "so this candidate keeps its first source's scores")


def class_name_warnings(proposal: dict, known, card_text) -> list:
    """The candidate's `warnings`: one {kind, name, suggestion} per component
    class name the proposal writes that is neither a known class
    (known_component_classes) nor quoted from the run's hypothesis card
    (reader_proposals.unknown_class_names). WARNING ONLY -- never a reason,
    never a change of eligibility or rank. [] without a known class set."""
    if known is None:
        return []
    found = _rp.unknown_class_names(proposal, known, card_text)
    return [{"kind": UNKNOWN_CLASS_WARNING, "name": u["name"], "suggestion": u["suggestion"]}
            for u in found["unknown"]]


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


def quarantine_capped_text(capped: list) -> str:
    """", N capped after 3 component quarantines: <ids>" -- appended to R2's
    reason and to the decide-next stop detail; empty when nothing is capped."""
    if not capped:
        return ""
    return (f", {len(capped)} capped after {BRIEF_MAX_COMPONENT_QUARANTINES} component "
            f"quarantines: {', '.join(capped)}")


def _r2(entries: list, *, select: bool) -> dict:
    """R2 (S1_FINDINGS_6B.md §4.3). `select` is False when something is
    already scheduled or eligible: the rule is then only recorded. When it
    fires, EVERY eligible open brief (r2_eligible_owner, fewer than
    BRIEF_MAX_CONSECUTIVE_EMPTY_R2 consecutive empty requests, no operator
    hold, and fewer than BRIEF_MAX_COMPONENT_QUARANTINES component-quarantined
    entries -- D-071) gets a `ready`
    request -- its waiting one is flipped ready, or a new `<owner>__more_<n>`
    is minted ready -- so no brief waits behind another (code-review fix 3);
    the scheduler's own priority order then picks among them."""
    open_owners = sorted((e for e in entries if e.get("brief_status") == BRIEF_OPEN),
                         key=lambda e: (e.get("priority", 999), e.get("id")))
    spent = {e["id"]: consecutive_empty_r2(e, entries) for e in open_owners}
    spent = {k: v for k, v in spent.items() if len(v) >= BRIEF_MAX_CONSECUTIVE_EMPTY_R2}
    held = sorted(e["id"] for e in open_owners if r2_held_owner(e, entries))
    # a brief both held and capped is listed once, as held (review nit)
    capped = sorted(e["id"] for e in open_owners
                    if e["id"] not in held and r2_quarantine_capped(e, entries))
    eligible = [e for e in open_owners
                if r2_eligible_owner(e) and e["id"] not in spent and e["id"] not in held
                and e["id"] not in capped]
    out = {
        "fired": False,
        "open_briefs": [e["id"] for e in open_owners],
        "eligible_briefs": [e["id"] for e in eligible],
        "held_briefs": held,
        "exhausted_briefs": sorted(e["id"] for e in entries
                                   if e.get("brief_status") == BRIEF_EXHAUSTED),
        "no_new_hypothesis_briefs": sorted(spent),
        "legacy_briefs": sorted(e["id"] for e in entries if is_legacy_brief(e)),
        "max_consecutive_empty_r2": BRIEF_MAX_CONSECUTIVE_EMPTY_R2,
        "enqueued": [],
        "ready": [],
        "reason": "",
    }
    if capped:  # E-068 PR 4 (D-071): only when non-empty -- other records unchanged
        out["quarantine_capped_briefs"] = capped
    if not select:
        out["reason"] = "not needed: the scheduler has an entry to run, or a candidate is eligible"
        return out
    if not eligible:
        out["reason"] = ("no eligible open brief (exhausted, no new hypothesis after "
                         f"{BRIEF_MAX_CONSECUTIVE_EMPTY_R2} consecutive empty R2 requests, owner "
                         "superseded/paused/blocked, a request on hold (CUL-398), or legacy "
                         "-- operator decision 7)" + quarantine_capped_text(capped))
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


def _fold_in_run_merges(cands: list) -> list:
    """E-073 step 2 (D-083): an eligible in-run duplicate (a side finding
    side_finding_merges.yaml lists after its group's primary) is folded into
    that primary when the primary is eligible too: one candidate, the
    PRIMARY's scores (never the higher of the two -- the readers share their
    inputs, so a second proposal is not evidence), every source listed under
    `merged_sources`. A duplicate whose primary is not eligible stays a
    candidate of its own. No-op when no candidate carries `_merge`."""
    by_id = {(c.get("source_run"), c["candidate_id"]): c for c in cands}
    out = []
    for c in cands:
        m = c.get("_merge")
        primary = by_id.get((c.get("source_run"), m["primary"])) if m and m["order"] else None
        if primary is None:
            out.append(c)
            continue
        primary.setdefault("merged_sources", [primary["proposal_ref"]]).append(c["proposal_ref"])
        primary["merge_note"] = MERGE_NOTE
    return out


def _collapse(cands: list) -> list:
    """Card I: ELIGIBLE candidates that are the same thing collapse into one,
    keeping the highest score tuple. Called on eligible candidates only, so an
    ineligible duplicate can never shadow an eligible one. Patches: the FULL
    novelty key (config hash + symbols + timeframe + window set). Sketches:
    identical kind + config_paths from the same source run.
    E-073 step 2: in-run merges are folded first (_fold_in_run_merges)."""
    cands = _fold_in_run_merges(cands)
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
        c.pop("_merge", None)

    operator = _operator_entries(queue)
    scheduled = select_entry([e for e in (queue.get("queue") or []) if isinstance(e, dict)])
    picked, stop = None, None
    # E-060 S3b: R1 (a no-op record unless inputs carry "composition").
    r1, r1_request = _r1(inputs, entries, scheduled=scheduled, operator=operator)
    if r1_request is not None:
        row, prio = r1_request["row"], r1_request["priority"]
        sim = entries + [{"id": row["entry_id"], "status": "ready", "priority": prio}]
        if select_entry(sim)["id"] != row["entry_id"]:
            raise DecideNextError(f"R1: the scheduler would not run {row['entry_id']} (priority "
                                  f"{prio}) first -- refusing a pick that would not run next")
        picked = {"composition": row["entry_id"], "queue_entry_id": row["entry_id"],
                  "brief_path": f"{CANDIDATE_BRIEFS_DIR}/{row['entry_id']}.md",
                  "timeframe": row["timeframe"], "registry_hash": row["registry_hash"],
                  "priority": prio,
                  "why": (f"R1: {len(row['block_ids'])} forecast blocks on {row['timeframe']} "
                          f"not yet composed in this registry state; ahead of agent entries, "
                          f"behind in-progress and operator entries (guess 10)")}
    elif scheduled is not None:
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
    r2 = _r2(entries, select=scheduled is None and not eligible and r1_request is None)
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
                           f"{len(r2['legacy_briefs'])} legacy"
                           # CUL-398 review: a held brief is still open; name it.
                           + (f", {len(r2['held_briefs'])} held by an operator hold: "
                              f"{', '.join(r2['held_briefs'])}" if r2.get("held_briefs") else "")
                           # E-068 PR 4 (D-071): a capped brief is still open; name it.
                           + quarantine_capped_text(r2.get("quarantine_capped_briefs") or [])
                           + ")")}

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
            # E-035 S2c: only when some proposal carried requires_feed.
            **({"feed_set_sha256": _canonical_sha(inputs["feed_set"])}
               if inputs.get("feed_set") is not None else {}),
        },
        "rules": {
            "r1": r1,
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
    elif p["kind"] == _rp.SIDE_FINDING:
        statement = " ".join(str((p.get("claim") or {}).get("statement") or "").split())
        goal = (f"Test a finding the {category} reader noticed after {run_id} on idea "
                f"{cand['parent_hypothesis_id']}: {statement} Its claim block is pre-filled "
                f"(candidate.claim). Evidence: {evidence}")
    else:
        blk = p.get("block") or {}
        goal = (f"Test a new {blk.get('kind')} block proposed by the {category} reader after "
                f"{run_id}: {blk.get('rationale')} (config paths {blk.get('config_paths')}). "
                f"Evidence: {evidence}")
    rf = p.get("requires_feed")
    if rf is not None:
        # E-035 S2c: picked once the feed is wired, or (a patch) when its resolved
        # config does not read the feed (requires_feed_gate); either way 1a sees it.
        goal += f" Needs feed {rf['feed']}: {rf['reason']}"
    front["research_goal"] = goal
    mc = copy.deepcopy((src["pre_registration"] or {}).get("machine_constraints") or {})
    mc.pop("pass_rule", None)  # never inherit criteria (operator decision 2)
    fa = cand.get("fold_assignment")
    if fa is not None:
        # E-077 PR-1 (D-085), orchestrator.folds.enabled: the child's windows are the next
        # unused fold's, not the parent's. Only the window-defining keys change; symbols,
        # timeframe, promotion, holdout, ... are copied as before.
        fold, proto = fa["fold"], mc.get("protocol")
        if fold is None or not isinstance(proto, dict):
            raise DecideNextError(f"picked candidate {cid!r} has no fold to run on "
                                  f"({fa}); it should have been infeasible")
        start, end = _folds.fold_span(inputs["folds"]["doc"], fold)
        proto = {k: v for k, v in proto.items() if k != "per_symbol_start"}
        mc["protocol"] = {**proto, "start": start, "end": end,
                          "window_months": _folds.BLOCK_MONTHS, "fold": fold}
        front["research_goal"] += (
            f" It backtests on fold {fold} ({', '.join(b['label'] for b in inputs['folds']['doc']['folds'][fold])};"
            f" config/folds.yaml), the next fold its lineage ({', '.join(fa['lineage'])}) has not used.")
    front["machine_constraints"] = mc
    source = {
        "origin": ORIGIN_READER,
        "proposal_ref": cand["proposal_ref"],
        "source_run": run_id,
        "parent_hypothesis_id": cand["parent_hypothesis_id"],
        "hypothesis_id": cand["hypothesis_id"],
        "decision_ref": decision_ref,
        "proposal": {k: copy.deepcopy(p[k])
                     for k in ("kind", "patch", "block", "claim", "evidence", "requires_feed",
                               "config_change")
                     if k in p},
    }
    candidate = {}
    if p["kind"] == _rp.SIDE_FINDING:
        # E-068 slice 5: step 1a copies this into the card unchanged
        # (PREFILLED_CLAIM.md); a change is recorded as a warning.
        candidate["claim"] = copy.deepcopy(p["claim"])
        # CUL-412: the block the claim is about -- the source run's base config
        # (its config change applied) and block manifest. NOT `config`/`manifest`:
        # those mark a pass-through patch (1a's pass_through, the CUL-405 hash
        # guard); 1b starts from this one and records any change as a deviation.
        start = side_finding_start(p, src)
        if start["reason"]:
            raise DecideNextError(f"picked side finding {cid!r} has no start config: "
                                  f"{start['reason']}")
        if start["config"] is not None:
            candidate["start_config"] = start["config"]
            candidate["start_manifest"] = start["manifest"]
            source["base_config_ref"] = src["base_config_ref"]
            source["start_config_sha256"] = config_sha256(start["config"])
            if start["ops"]:
                source["config_change_ops"] = start["ops"]
            changes = "".join(f" {op['path']} -> {op['value']!r};" for op in start["ops"])
            front["research_goal"] += (
                f" It starts from {run_id}'s base config (candidate.start_config)"
                + (f" with the finding's config change:{changes}" if changes else "")
                + " -- the block the claim is about.")
    if p["kind"] == "patch":
        ops, patched, why = resolve_patch(p, src["base_config"])
        if why:
            raise DecideNextError(f"picked patch {cid!r} no longer resolves: {why}")
        candidate["config"] = patched
        comp_manifest = src.get("composition_manifest")
        if isinstance(comp_manifest, dict):
            # E-060 S3b (7.5): a patch on a composite is itself a composition-mode
            # run (never a block; criteria = the profit bars; its variants are
            # the source manifest's schemes). No block manifest to pass through.
            candidate["composition"] = {
                "manifest_ref": f"runs/{run_id}/artifacts/{COMPOSITION_MANIFEST_FILE}",
                "manifest_sha256": config_sha256(comp_manifest),
                "registry_revision": comp_manifest.get("registry_revision"),
                "registry_hash": comp_manifest.get("registry_hash"),
                "timeframe": comp_manifest.get("timeframe"),
                "timeframe_category": comp_manifest.get("timeframe_category"),
                "block_ids": [b.get("block_id") for b in comp_manifest.get("blocks") or []],
            }
            source["source_kind"] = ORIGIN_COMPOSITION
        else:
            candidate["manifest"] = copy.deepcopy(src["manifest"])
        source["resolved_patch"] = ops
        source["base_config_ref"] = src["base_config_ref"]
        source["expected_config_sha256"] = config_sha256(patched)
        if not isinstance(comp_manifest, dict):
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
