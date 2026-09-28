"""
replay_repeat_gate -- E-036 S2b (delivery_plan_v26.md slice 8): a READ-ONLY
replay of the 5a exact-match repeat gate (tools/novelty.py via
tools/anti_adjacency_gate.py) over the real past corpus runs/run_*, next to
what the retired family-grain layer 2 (build_exclusion_digest.
legacy_family_lookup) said for the same run. Findings:
engineering/roadmap/E-036/S2B_REPLAY.md.

Nothing here decides anything or writes under the corpus: no backtest, no
market data, no API call, no orchestrator import. The only file written is
the result YAML (CLI --out); the CLI refuses an --out under --runs-dir.

Runs are taken in run-number order, as chronological (run_9 before
run_010). Each run is checked against the memory of EARLIER runs only, with
its own run id excluded as live; its own memory entry is added after.

CANDIDATE AT 5a (run_phase1_research._repeat_gate_context /
_check_variant_repeat). The config is artifacts/candidate_strategy_config.json
(the file the legacy flow writes after F4d's injection, and the file the
trial row is hashed from), hashed with novelty.forecast_hash_of_config. The
protocol is the one the gate would have RESOLVED at 5a -- the live resolver,
tools/protocol_resolution.resolve_protocol_path (what
run_phase1_research._resolve_protocol_path delegates to), called read-only
on the run's own artifacts/run_context.yaml. Its one input the corpus does
not keep is the campaign-wide campaign_state.last_escalation at the time
(the B10 branch, taken by every run whose run_context.yaml names no
run_type). DECLARED APPROXIMATION for that branch: last_escalation is
reconstructed as {protocol_path: E, claimed_by_run: <this run>}, E being the
earliest protocol path the run's own artifacts record resolving:
  1. a protocols/... path quoted in pipeline_state.yaml's last_error by an
     OSError (the resolved path failed to open -- run_027);
  2. prescreen_result.yaml `protocol_version` (prescreen ran right after 5a,
     on the same resolver);
  3. protocol_result.yaml `protocol_file`.
None of them -> UNKEYED (b10_no_evidence): the input is unknown, not bad.
The resolved protocol is then read STRICTLY (novelty.load_protocol /
protocol_spec(strict=True)) and its `symbols` checked, as live. Outcomes:
REPEAT / NOVEL; FAIL_LOUD -- the live gate would raise (resolver error,
NoveltyError, no usable symbols): never keyed on a fallback; UNKEYED -- the
replay cannot build the candidate (no config, variant-loop run, no B10
evidence).
Counterfactual column `executed`: the same check keyed on the protocol the
backtest actually ran (protocol_result.protocol_file, else
prescreen_result.protocol_version) -- NOT what the live gate reads.

MEMORY (what campaign_memory.yaml would hold). Two columns:
  * strict -- the live writer's own rule: component errors
    (campaign_memory.protocol_component_errors, shared with the
    orchestrator) -> campaign_memory.build_fault_entry (never matches);
    otherwise campaign_memory.build_memory_entry exactly as regroup_record
    calls it (categories=[]: the reader proposals are irrelevant to the key).
    Whatever it raises keeps the run out of memory.
  * counterfactual -- the key-relevant helpers of build_memory_entry
    (_variants_block, protocol_ref_of, the card timeframe), with the grid
    requirement waived AND a missing trial-ledger `forecast_hash` BACKFILLED
    from novelty.forecast_hash_of_config of the run's
    candidate_strategy_config.json. A fabricated ledger value: it shows what
    the gate could catch had the memory existed, not what it would catch.
Both use novelty.novelty_key / match_index (no second key), incrementally:
each protocol file is read once, each entry indexed once.

OLD SIDE (information only): the retired 5a caller
(_route_post_variant_selection before E-036 S2a): the hypothesis card merged
with variant_selection.yaml's variant_definition when that artifact exists,
ONE lookup at (selection's instrument(s) and timeframe, else
extract_instruments()[0] / extract_timeframes()[0] -- evaluate_candidate's
defaults), backtest_spec.yaml's `config` for the fingerprint, precedence
repeat > neighbour > first. The digest is scan_run_triples restricted to
earlier runs. "Old refuse" = `repeat` only. Layer 1 (KB) is replayed on
neither side.

Fail loud: an unreadable or malformed campaign_state.yaml (it feeds every
memory entry) aborts the replay; an unreadable run artifact is its own
explicit reason, never treated as absent.

CLI:
  python strategy-research/tools/replay_repeat_gate.py [--runs-dir ...] [--root ...]
      [--campaign-state ...] [--out ...]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import re
from pathlib import Path

import yaml

from abandoned_launch import is_abandoned_launch  # tools/ sibling (E-061 C1.4)
import anti_adjacency_gate as _aag  # tools/ sibling: candidate_key, layer2_digest_check
import build_exclusion_digest as _bed  # tools/ sibling: the retired family digest
import campaign_memory as _cm  # tools/ sibling: the memory writers and helpers
import novelty as _nov  # tools/ sibling: THE exact-match key
import protocol_resolution as _pres  # tools/ sibling: THE protocol resolver

_HERE = Path(__file__).resolve().parent
_SR = _HERE.parent

DEFAULT_RUNS_DIR = _SR / "runs"
DEFAULT_CAMPAIGN_STATE_PATH = _SR / "campaign_record" / "campaign_state.yaml"
DEFAULT_OUT_PATH = _SR / "engineering" / "roadmap" / "E-036" / "s2b_replay_result.yaml"

SCHEMA_VERSION = 2
_RUN_RE = re.compile(r"^run_(\d+)$")
_OLD_RANK = {"repeat": 2, "neighbour": 1, "novel": 0}
# An OSError message quoting the protocol path the resolver produced.
_ERRNO_PROTOCOL_RE = re.compile(r"\[Errno \d+\][^']*'(protocols[\\/][^']+)'")

REPEAT, NOVEL, FAIL_LOUD, UNKEYED = "REPEAT", "NOVEL", "FAIL_LOUD", "UNKEYED"
OUTCOMES = (REPEAT, NOVEL, FAIL_LOUD, UNKEYED)
# "<protocol mode>/<memory mode>". PRIMARY = 5a_live/strict (the live gate,
# the live writer). Every other column is a labelled counterfactual:
#   5a_d3_aside -- the resolver's D-3 promotion guard set aside;
#   executed    -- keyed on the protocol the backtest ran, not the 5a one;
#   counterfactual memory -- grid waived, ledger hash backfilled.
PRIMARY = "5a_live/strict"
COLUMNS = ("5a_live/strict", "5a_live/counterfactual", "5a_d3_aside/strict",
           "5a_d3_aside/counterfactual", "executed/strict", "executed/counterfactual")

# Candidate reasons (the text before the first ':' is the bucket).
CAND_NO_CONFIG = "no_candidate_config"
CAND_CONFIG_UNREADABLE = "candidate_config_unreadable"
CAND_VARIANT_LOOP = "variant_loop_run"
CAND_B10_NO_EVIDENCE = "b10_no_evidence"
CAND_NO_EXECUTED_PROTOCOL = "no_executed_protocol_recorded"
CAND_ARTIFACT_UNREADABLE = "artifact_unreadable"
FAIL_RESOLVER = "resolver_raises"
FAIL_PROMOTION = "promotion_unratified"  # the resolver's D-3 guard (UngatedProtocolError)
FAIL_NOVELTY = "novelty_error"
FAIL_NO_SYMBOLS = "protocol_has_no_symbols"


class ReplayError(ValueError):
    """The replay cannot run honestly (unreadable ledger) or was asked to do
    something unsafe (write under the corpus)."""


class _Unreadable(Exception):
    pass


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

def _run_sort_key(path: Path):
    m = _RUN_RE.match(path.name)
    return (int(m.group(1)), path.name) if m else (10 ** 9, path.name)


def run_dirs_in_order(runs_dir: Path) -> list:
    """Every runs_dir/run_<digits> directory, in run-number order (E-061 C1.4:
    except a run dir a failed launch abandoned)."""
    return sorted((p for p in Path(runs_dir).iterdir()
                   if p.is_dir() and _RUN_RE.match(p.name) and not is_abandoned_launch(p)),
                  key=_run_sort_key)


def _strict_load(path: Path):
    """Plain safe_load (no repair). Raises on unreadable input."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _read(path: Path):
    """The parsed YAML mapping; None when ABSENT; raises _Unreadable when the
    file exists but cannot be parsed or is not a mapping."""
    path = Path(path)
    if not path.exists():
        return None
    try:
        doc = _strict_load(path)
    except (OSError, yaml.YAMLError) as exc:
        raise _Unreadable(f"{path.name}: {type(exc).__name__}") from exc
    if doc is None:
        return {}
    if not isinstance(doc, dict):
        raise _Unreadable(f"{path.name}: not a mapping")
    return doc


def load_trial_sharpes(campaign_state_path) -> list:
    """campaign_state.yaml's trial_sharpes, read strictly. None -> no ledger
    (tests). A missing, unparseable or malformed file raises ReplayError: it
    feeds every memory entry, so it is never treated as empty."""
    if campaign_state_path is None:
        return []
    path = Path(campaign_state_path)
    if not path.exists():
        raise ReplayError(f"{path} does not exist -- the trial ledger feeds every memory entry")
    try:
        doc = _strict_load(path)
    except (OSError, yaml.YAMLError) as exc:
        raise ReplayError(f"{path} is unreadable ({type(exc).__name__}: {exc}) -- refusing to "
                          f"replay against a ledger read as empty") from exc
    if not isinstance(doc, dict):
        raise ReplayError(f"{path}: not a mapping")
    rows = doc.get("trial_sharpes") or []
    if not isinstance(rows, list):
        raise ReplayError(f"{path}: trial_sharpes is not a list")
    return rows


def _read_config(path: Path):
    """(config, reason)."""
    if not path.exists():
        return None, CAND_NO_CONFIG
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"{CAND_CONFIG_UNREADABLE}: {type(exc).__name__}"
    if not isinstance(cfg, dict):
        return None, f"{CAND_CONFIG_UNREADABLE}: not a JSON object"
    return cfg, None


def _anchored_ref(protocol_path, root: Path):
    """campaign_memory.protocol_ref_of, a RELATIVE path (recorded by the engine
    running in strategy-research/, e.g. 'protocols\\\\x.json') anchored at
    `root` first so the result never depends on this process's CWD."""
    if not protocol_path:
        return None
    p = Path(str(protocol_path).replace("\\", "/"))
    return _cm.protocol_ref_of(str(p if p.is_absolute() else Path(root) / p), root)


def _bucket(reason) -> str:
    return str(reason or "").split(":")[0]


# ---------------------------------------------------------------------------
# Memory: one incremental index per column
# ---------------------------------------------------------------------------

class _Memory:
    """Earlier runs' entries: each protocol file read once (non-strict, as
    novelty.protocol_specs does), each entry indexed once."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.specs: dict = {}
        self.index: dict = {}
        self.warnings: list = []
        self.entries = 0
        self.variants = 0

    def add(self, entry: dict) -> tuple | None:
        """Index `entry`; returns its tested variant's key (single-column
        entries), else None."""
        ref = _nov.normalize_ref(entry.get("protocol_ref"))
        if ref and ref not in self.specs:
            self.specs[ref] = _nov.protocol_spec(self.root, ref, warnings=self.warnings)
        self.entries += 1
        self.variants += len(entry.get("variants") or {})
        keys = []
        for key, matches in _nov.match_index({"runs": {entry["run_id"]: entry}}, self.specs).items():
            self.index.setdefault(key, []).extend(matches)
            keys.append(key)
        return keys[0] if len(keys) == 1 else None

    def check(self, key: tuple, run_id: str) -> dict:
        """layer2_digest_check against the earlier runs, this run excluded."""
        matched = [m for m in self.index.get(key) or [] if m["run_id"] != run_id]
        res = _aag.layer2_digest_check(key, {key: matched} if matched else {})
        return {"outcome": REPEAT if res["outcome"] == "repeat" else NOVEL,
                "matched": [f"{m['run_id']}:{m['variant_id']}" for m in res["matched"]]}


def _ledger_rule(run_id: str, trial_sharpes) -> str:
    row = (_cm._trial_rows(run_id, trial_sharpes).get(run_id) or {}).get("backtest")
    if row is None:
        return "no_backtest_row"
    return "backtest_row_with_forecast_hash" if row.get("forecast_hash") else \
        "backtest_row_without_forecast_hash"


def _classify_writer_error(msg: str) -> str:
    for needle, code in (("hypothesis_card.yaml is missing", "no_hypothesis_card"),
                         ("has no hypothesis_id", "no_hypothesis_id"),
                         ("protocol_result.yaml is missing", "no_protocol_result"),
                         ("idea_status.yaml is missing", "no_idea_status"),
                         ("grid_evaluation.yaml is missing", "no_grid_evaluation"),
                         ("has no 'backtest' row", "no_ledger_backtest_row"),
                         ("has no forecast_hash", "ledger_row_without_forecast_hash"),
                         ("unparseable YAML", "artifact_unreadable")):
        if needle in msg:
            return code
    return "other"


def _component_errors(run_dir: Path):
    """(errors, reason): the shared live check; reason when it cannot run."""
    try:
        return _cm.protocol_component_errors(run_dir, load=_strict_load), None
    except FileNotFoundError:
        return None, "no_protocol_result"
    except (OSError, yaml.YAMLError) as exc:
        return None, f"{CAND_ARTIFACT_UNREADABLE}: protocol_result.yaml {type(exc).__name__}"
    except (ValueError, AttributeError) as exc:
        return None, f"component_errors_malformed: {exc}"


def strict_entry(run_dir: Path, run_id: str, *, trial_sharpes, root: Path):
    """(entry, reason): what the live regroup_record would write for this
    run, or None and why it would not (the writer's own exception)."""
    errors, reason = _component_errors(run_dir)
    if errors is None:
        return None, reason
    if errors:
        return _cm.build_fault_entry(run_dir, run_id, errors, recorded_at="replay"), "engineering_fault"
    try:
        return _cm.build_memory_entry(Path(run_dir), run_id, trial_sharpes=trial_sharpes,
                                      categories=[], protocol_root=root,
                                      recorded_at="replay"), None
    except _cm.CampaignMemoryError as exc:
        return None, f"{_classify_writer_error(str(exc))}: {exc}"


def counterfactual_entry(run_dir: Path, run_id: str, *, trial_sharpes, root: Path):
    """(entry, reason, forecast_hash_source): the key-relevant part of a
    memory entry with the grid requirement waived and a missing ledger hash
    backfilled from the config file (see the module docstring)."""
    arts = Path(run_dir) / "artifacts"
    errors, reason = _component_errors(run_dir)
    if errors is None:
        return None, reason, None
    if errors:  # as live: the fault entry needs nothing else
        return (_cm.build_fault_entry(run_dir, run_id, errors, recorded_at="replay"),
                "engineering_fault", None)
    try:
        card = _read(arts / "hypothesis_card.yaml")
        pr = _read(arts / "protocol_result.yaml")
    except _Unreadable as exc:
        return None, f"{CAND_ARTIFACT_UNREADABLE}: {exc}", None
    if card is None:
        return None, "no_hypothesis_card", None
    hyp_id = card.get("hypothesis_id")
    if not isinstance(hyp_id, str) or not hyp_id.strip():
        return None, "no_hypothesis_id", None
    if not (pr.get("results") or []):
        return None, f"not_backtested: {pr.get('source') or 'no results'}", None
    trials = _cm._trial_rows(run_id, trial_sharpes)
    row = (trials.get(run_id) or {}).get("backtest")
    if row is not None and row.get("forecast_hash"):
        fh_source = "trial_ledger"
    else:
        cfg, cfg_reason = _read_config(arts / "candidate_strategy_config.json")
        if cfg is None:
            return None, f"no_forecast_hash: {cfg_reason}", None
        fh_source = ("backfill: ledger row without forecast_hash" if row is not None
                     else "backfill: no ledger row")
        row = {**(row or {"trial_id": run_id, "source": "backtest"}),
               "forecast_hash": _nov.forecast_hash_of_config(cfg)}
        trials = {**trials, run_id: {**(trials.get(run_id) or {}), "backtest": row}}
    try:
        variants = _cm._variants_block(Path(run_dir), run_id, [run_id], trials)
    except _cm.CampaignMemoryError as exc:
        return None, f"memory_helper_raised: {exc}", None
    timeframe = card.get("timeframe") if isinstance(card.get("timeframe"), str) else None
    return ({"run_id": run_id, "hypothesis_id": hyp_id, "legacy": False,
             "engineering_fault": None,
             "protocol_ref": _anchored_ref(pr.get("protocol_file"), root),
             "timeframe": timeframe, "variants": variants}, None, fh_source)


# ---------------------------------------------------------------------------
# Candidate: the config, and the protocol at 5a
# ---------------------------------------------------------------------------

def _b10_evidence(run_dir: Path):
    """(protocol path, source) -- the earliest protocol path this run's own
    artifacts record resolving (module docstring), else (None, None).
    Raises _Unreadable on an unparseable source file."""
    arts = Path(run_dir) / "artifacts"
    state = _read(Path(run_dir) / "pipeline_state.yaml") or {}
    m = _ERRNO_PROTOCOL_RE.search(str(state.get("last_error") or ""))
    if m:
        return m.group(1).replace("\\\\", "\\"), "pipeline_state.last_error"
    ps = _read(arts / "prescreen_result.yaml") or {}
    if ps.get("protocol_version"):
        return str(ps["protocol_version"]), "prescreen_result.protocol_version"
    pr = _read(arts / "protocol_result.yaml") or {}
    if pr.get("protocol_file"):
        return str(pr["protocol_file"]), "protocol_result.protocol_file"
    return None, None


def _executed_protocol(run_dir: Path):
    arts = Path(run_dir) / "artifacts"
    pr = _read(arts / "protocol_result.yaml") or {}
    if pr.get("protocol_file"):
        return str(pr["protocol_file"]), "protocol_result.protocol_file"
    ps = _read(arts / "prescreen_result.yaml") or {}
    if ps.get("protocol_version"):
        return str(ps["protocol_version"]), "prescreen_result.protocol_version"
    return None, None


@contextlib.contextmanager
def _promotion_guard_set_aside():
    """COUNTERFACTUAL ONLY (column 5a_d3_aside): the resolver with its D-3
    promotion-ratification check (protocol_resolution.assert_promotion_ratified,
    a guard added after most of this corpus ran, independent of E-036) made a
    no-op for the duration of one call, so the protocol it SELECTS is visible.
    Process-local; nothing is written; restored in `finally`."""
    real = _pres.assert_promotion_ratified
    _pres.assert_promotion_ratified = lambda _path: None
    try:
        yield
    finally:
        _pres.assert_promotion_ratified = real


def resolve_5a_protocol(run_dir: Path, run_id: str, root: Path, *,
                        promotion_guard: bool = True) -> dict:
    """The protocol the live gate would have resolved at 5a:
    {protocol_path, branch, source} or {outcome: FAIL_LOUD|UNKEYED, reason}.
    promotion_guard=False: the counterfactual with the D-3 guard set aside."""
    if not promotion_guard:
        with _promotion_guard_set_aside():
            return resolve_5a_protocol(run_dir, run_id, root)
    run_dir = Path(run_dir)
    try:
        ctx = _read(run_dir / "artifacts" / "run_context.yaml") or {}
    except _Unreadable as exc:
        return {"outcome": FAIL_LOUD, "reason": f"{FAIL_RESOLVER}: run_context {exc}"}
    run_type = ctx.get("run_type", "")
    branch = run_type if run_type in ("replication_diagnostic", "forced_diagnostic",
                                      "protocol_ref_pinned") else "b10_last_escalation"
    state, source = {}, f"run_context.yaml ({run_type})"
    if branch == "b10_last_escalation":
        try:
            evidence, source = _b10_evidence(run_dir)
        except _Unreadable as exc:
            return {"outcome": UNKEYED, "reason": f"{CAND_ARTIFACT_UNREADABLE}: {exc}"}
        if evidence is None:
            return {"outcome": UNKEYED, "reason": CAND_B10_NO_EVIDENCE}
        # Anchored at root, as the live orchestrator (CWD strategy-research/)
        # would open it -- so the resolver's own promotion check reads the
        # same file whatever this process's CWD is.
        p = Path(str(evidence).replace("\\", "/"))
        state = {"last_escalation": {"protocol_path": str(p if p.is_absolute() else Path(root) / p),
                                     "claimed_by_run": run_id}}
    try:
        path = _pres.resolve_protocol_path(run_dir, run_id, Path(root) / "protocols",
                                           campaign_state=state, on_stale_escalation=None)
    except _pres.UngatedProtocolError as exc:
        return {"outcome": FAIL_LOUD, "reason": f"{FAIL_PROMOTION}: {exc}"}
    except (ValueError, RuntimeError, OSError, yaml.YAMLError) as exc:
        return {"outcome": FAIL_LOUD, "reason": f"{FAIL_RESOLVER}: {type(exc).__name__}: {exc}"}
    return {"protocol_path": str(path), "branch": branch, "source": source}


def candidate_key_on(fh: str, protocol_path, root: Path, card_timeframe) -> dict:
    """The live 5a key on one resolved protocol (_repeat_gate_context +
    _check_variant_repeat): strict read, usable symbols, candidate_key.
    {key (tuple), protocol_ref} or {outcome: FAIL_LOUD, reason, protocol_ref}."""
    ref = _anchored_ref(protocol_path, root)
    try:
        proto = _nov.load_protocol(root, ref)
        spec = _nov.protocol_spec(root, ref, strict=True)
    except _nov.NoveltyError as exc:
        return {"outcome": FAIL_LOUD, "reason": f"{FAIL_NOVELTY}: {exc}", "protocol_ref": ref}
    symbols = proto.get("symbols")
    if not (isinstance(symbols, list) and symbols and all(isinstance(s, str) and s for s in symbols)):
        return {"outcome": FAIL_LOUD, "reason": f"{FAIL_NO_SYMBOLS}: {ref}", "protocol_ref": ref}
    key = _aag.candidate_key(fh, sorted(set(symbols)), ref, {_nov.normalize_ref(ref): spec},
                             card_timeframe=card_timeframe)
    return {"key": key, "protocol_ref": ref}


# ---------------------------------------------------------------------------
# Old side
# ---------------------------------------------------------------------------

def _digest_before(scan: dict, earlier: set) -> dict:
    """The family digest restricted to runs in `earlier`."""
    fams = {}
    for fam, bucket in (scan.get("families") or {}).items():
        triples = []
        for t in bucket.get("triples") or []:
            rids = [r for r in t.get("run_ids") or [] if r in earlier]
            if rids:
                triples.append({**t, "run_ids": rids})
        if triples:
            fams[fam] = {"confidence": bucket.get("confidence"), "triples": triples}
    return {"families": fams}


def old_outcome_for_run(run_dir: Path, digest: dict) -> dict:
    """The retired 5a caller's layer-2 outcome (module docstring)."""
    arts = Path(run_dir) / "artifacts"
    try:
        card = _read(arts / "hypothesis_card.yaml")
        selection = _read(arts / "variant_selection.yaml")
        spec = _read(arts / "backtest_spec.yaml") or {}
    except _Unreadable as exc:
        return {"outcome": "not_evaluable", "reason": f"{CAND_ARTIFACT_UNREADABLE}: {exc}"}
    if card is None:
        return {"outcome": "not_evaluable", "reason": "no_hypothesis_card"}
    candidate = dict(card)
    if selection is not None:
        if isinstance(selection.get("variant_definition"), dict):
            candidate.update(selection["variant_definition"])
        candidate["hypothesis_id"] = selection.get("hypothesis_id") or candidate.get("hypothesis_id")
        inst = selection.get("instrument")
        instruments = inst if isinstance(inst, list) else [inst]
        timeframe = selection.get("timeframe")
        source = "variant_selection.yaml"
    else:
        instruments, timeframe, source = [None], None, "card defaults"
    if timeframe is None:
        tfs = _bed.extract_timeframes(candidate)
        timeframe = tfs[0] if tfs else None
    cfg = spec.get("config") if isinstance(spec.get("config"), dict) else None
    results = []
    for instrument in instruments:
        if instrument is None:
            found = _bed.extract_instruments(candidate)
            instrument = found[0] if found else None
        res = _bed.legacy_family_lookup(candidate, instrument, timeframe, digest,
                                        candidate_config=cfg)
        results.append({**res, "instrument": instrument, "timeframe": timeframe})
    best = (next((r for r in results if r["outcome"] == "repeat"), None)
            or next((r for r in results if r["outcome"] == "neighbour"), None) or results[0])
    return {**best, "selection_source": source,
            "fingerprint_config": "backtest_spec.config" if cfg is not None else None}


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------

def _candidate_row(run_dir: Path, run_id: str, root: Path, mems: dict) -> dict:
    arts = Path(run_dir) / "artifacts"
    unkeyed = None
    if (arts / "variants" / "index.yaml").exists():
        unkeyed = CAND_VARIANT_LOOP
    cfg, cfg_reason = (None, unkeyed) if unkeyed else _read_config(arts / "candidate_strategy_config.json")
    if cfg is None:
        return {"candidate_variants": 0,
                **{c: {"outcome": UNKEYED, "reason": cfg_reason} for c in COLUMNS}}
    fh = _nov.forecast_hash_of_config(cfg)
    try:
        card = _read(arts / "hypothesis_card.yaml") or {}
    except _Unreadable:
        card = {}  # the card timeframe is only the unresolved fallback, never used here
    tf = card.get("timeframe")
    resolved = {"5a_live": resolve_5a_protocol(run_dir, run_id, root),
                "5a_d3_aside": resolve_5a_protocol(run_dir, run_id, root, promotion_guard=False)}
    try:
        executed, source = _executed_protocol(run_dir)
        resolved["executed"] = ({"protocol_path": executed, "source": source} if executed
                                else {"outcome": UNKEYED, "reason": CAND_NO_EXECUTED_PROTOCOL})
    except _Unreadable as exc:
        resolved["executed"] = {"outcome": UNKEYED, "reason": f"{CAND_ARTIFACT_UNREADABLE}: {exc}"}
    keys = {}
    for mode, res in resolved.items():
        if "outcome" in res:
            keys[mode] = dict(res)
        else:
            keys[mode] = {**candidate_key_on(fh, res["protocol_path"], root, tf),
                          "protocol_source": res["source"],
                          **({"protocol_branch": res["branch"]} if "branch" in res else {})}
    row = {"candidate_variants": 1, "_keys": keys}
    for col in COLUMNS:
        mode, mem = col.split("/")
        k = keys[mode]
        if "key" not in k:
            row[col] = dict(k)
        else:
            row[col] = {**mems[mem].check(k["key"], run_id), "key": _nov.key_dict(k["key"]),
                        **{f: v for f, v in k.items() if f != "key"}}
    return row


def replay(runs_dir: Path = DEFAULT_RUNS_DIR, *, root: Path = _SR,
           campaign_state_path: Path | None = DEFAULT_CAMPAIGN_STATE_PATH) -> dict:
    """The full replay, returned as a dict (nothing written)."""
    runs_dir, root = Path(runs_dir), Path(root)
    trial_sharpes = load_trial_sharpes(campaign_state_path)
    dirs = run_dirs_in_order(runs_dir)
    scan = _bed.scan_run_triples(runs_dir)
    mems = {"strict": _Memory(root), "counterfactual": _Memory(root)}
    rows, earlier = [], set()
    for run_dir in dirs:
        run_id = run_dir.name
        row = {"run_id": run_id, **_candidate_row(run_dir, run_id, root, mems),
               "old": old_outcome_for_run(run_dir, _digest_before(scan, earlier))}
        exec_key = (row.pop("_keys", None) or {}).get("executed", {}).get("key")

        s_entry, s_reason = strict_entry(run_dir, run_id, trial_sharpes=trial_sharpes, root=root)
        c_entry, c_reason, fh_source = counterfactual_entry(run_dir, run_id,
                                                            trial_sharpes=trial_sharpes, root=root)
        row["memory"] = {
            "strict": {"entry": s_entry is not None,
                       "fault": bool(s_entry and s_entry.get("engineering_fault")),
                       "reason": s_reason},
            "counterfactual": {"entry": c_entry is not None,
                               "fault": bool(c_entry and c_entry.get("engineering_fault")),
                               "reason": c_reason, "forecast_hash_source": fh_source},
            "ledger_rule": _ledger_rule(run_id, trial_sharpes),
        }
        if s_entry is not None:
            own_s = mems["strict"].add(s_entry)
            if own_s is not None:
                row["memory"]["strict"]["key"] = _nov.key_dict(own_s)
        if c_entry is not None:
            own = mems["counterfactual"].add(c_entry)
            if own is not None:
                row["memory"]["counterfactual"]["key"] = _nov.key_dict(own)
            if own is not None and exec_key is not None:
                # The key a later run finds this entry by == this run's own
                # candidate key on the protocol it EXECUTED (the memory's
                # protocol). Both sides hash the SAME config file, so this
                # checks symbols/timeframe/windows alignment only -- it says
                # nothing about whether the backfilled hash is the ledger's.
                row["memory"]["counterfactual"]["self_consistent"] = own == exec_key
        rows.append(row)
        earlier.add(run_id)

    result = {"schema_version": SCHEMA_VERSION, "primary_column": PRIMARY, "runs": rows,
              "totals": _totals(rows, mems),
              "protocol_warnings": {c: m.warnings for c, m in mems.items()},
              "corpus": {"runs_dir": _display_path(runs_dir, root), "n_run_dirs": len(dirs),
                         "order": "run number (run_<digits>)"}}
    # No machine-specific absolute path in the result (writer/loader error
    # messages quote full paths).
    subs = []
    for base, shown in ((runs_dir, _display_path(runs_dir, root)), (root, _display_path(root, root))):
        for form in {str(Path(base).resolve()), Path(base).resolve().as_posix()}:  # absolute only
            subs.append((form, shown))
    return _scrub(result, sorted(subs, key=lambda s: -len(s[0])))


def _scrub(obj, subs):
    if isinstance(obj, dict):
        return {k: _scrub(v, subs) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub(v, subs) for v in obj]
    if isinstance(obj, str):
        for old, new in subs:
            if old in obj:
                obj = obj.replace(old, new)
    return obj


def _display_path(path: Path, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path(root).resolve().parent).as_posix()
    except ValueError:
        return Path(path).as_posix()


def _count(items) -> dict:
    out: dict = {}
    for it in items:
        out[it] = out.get(it, 0) + 1
    return dict(sorted(out.items()))


def _totals(rows: list, mems: dict) -> dict:
    cols = {}
    for c in COLUMNS:
        outs = [r[c]["outcome"] for r in rows]
        cols[c] = {**{o: outs.count(o) for o in OUTCOMES},
                   "reasons": {o: _count(_bucket(r[c].get("reason")) for r in rows
                                         if r[c]["outcome"] == o)
                               for o in (FAIL_LOUD, UNKEYED)},
                   "repeats": [{"run_id": r["run_id"], "matched": r[c]["matched"]}
                               for r in rows if r[c]["outcome"] == REPEAT]}
    old = [r["old"]["outcome"] for r in rows]
    matrices = {}
    for c in COLUMNS:
        m: dict = {}
        for r in rows:
            m.setdefault(r["old"]["outcome"], {o: 0 for o in OUTCOMES})[r[c]["outcome"]] += 1
        matrices[c] = {k: m[k] for k in ("repeat", "neighbour", "novel", "not_evaluable") if k in m}
    by_hash: dict = {}
    for r in rows:
        key = next((r[c]["key"] for c in COLUMNS if r[c].get("key")), None)
        if key:
            by_hash.setdefault(key["forecast_hash"], []).append(r["run_id"])
    a5, ex = "5a_d3_aside/counterfactual", "executed/counterfactual"
    diverging = [{"run_id": r["run_id"], "at_5a": r[a5].get("protocol_ref"),
                  "executed": r[ex].get("protocol_ref")}
                 for r in rows if r[a5].get("protocol_ref") and r[ex].get("protocol_ref")
                 and r[a5]["protocol_ref"] != r[ex]["protocol_ref"]]
    return {
        "runs": len(rows),
        # counted from the candidates themselves: the legacy flow checks one
        # variant (candidate_strategy_config.json) per run that has a config
        "candidate_variants": sum(r["candidate_variants"] for r in rows),
        "new": cols,
        "old": {**{o: old.count(o) for o in ("repeat", "neighbour", "novel", "not_evaluable")},
                "refuse (repeat)": old.count("repeat"),
                "admit (neighbour + novel)": old.count("neighbour") + old.count("novel"),
                "not_evaluable_by_reason": _count(_bucket(r["old"].get("reason")) for r in rows
                                                  if r["old"]["outcome"] == "not_evaluable")},
        "agreement_old_x_new": matrices,
        "memory": {
            c: {"entries": mems[c].entries, "variants": mems[c].variants,
                "fault_entries": sum(1 for r in rows if r["memory"][c]["fault"]),
                "no_entry_by_reason": _count(_bucket(r["memory"][c]["reason"]) for r in rows
                                             if not r["memory"][c]["entry"])}
            for c in ("strict", "counterfactual")},
        "ledger_rule": _count(r["memory"]["ledger_rule"] for r in rows),
        "counterfactual_self_inconsistent": [r["run_id"] for r in rows
                                             if r["memory"]["counterfactual"].get("self_consistent") is False],
        "protocol_at_5a_differs_from_executed": diverging,
        "config_hash_collisions": [{"forecast_hash": h, "runs": v}
                                   for h, v in by_hash.items() if len(v) > 1],
        "distinct_config_hashes": len(by_hash),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--root", type=Path, default=_SR,
                        help="strategy-research/ (protocol refs are relative to it)")
    parser.add_argument("--campaign-state", type=Path, default=DEFAULT_CAMPAIGN_STATE_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_PATH)
    args = parser.parse_args(argv)
    out = args.out.resolve()
    runs = args.runs_dir.resolve()
    if out == runs or runs in out.parents:
        raise ReplayError(f"--out {args.out} is under --runs-dir {args.runs_dir}: the replay "
                          f"never writes into the corpus")
    result = replay(args.runs_dir, root=args.root, campaign_state_path=args.campaign_state)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)
    t = result["totals"]
    print(f"replay written to {out}")
    for c in COLUMNS:
        n = t["new"][c]
        print(f"  {c}: REPEAT={n[REPEAT]} NOVEL={n[NOVEL]} FAIL_LOUD={n[FAIL_LOUD]} "
              f"UNKEYED={n[UNKEYED]}")
    print(f"  old: repeat={t['old']['repeat']} neighbour={t['old']['neighbour']} "
          f"novel={t['old']['novel']} not_evaluable={t['old']['not_evaluable']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
