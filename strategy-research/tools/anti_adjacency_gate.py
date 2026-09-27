"""
anti_adjacency_gate.py -- E-032 S2a, Task 2.

Deterministic tool stage. No LLM call, no token cost -- same class of stage
as tools/prescreen_signal.py (the `signal_prescreen` `tool:` entry in
stages.yaml [ARCHIVED 2026-08-24 -> E-033/artifacts/] [ARCHIVED 2026-08-24 -> E-033/artifacts/]): a mechanical pass/fail should not be adjudicated by
prose. See engineering/roadmap/E-032/artifacts/s1_idea_generation.md Task 3
for the full design rationale and the worked calibration case this module
is regression-tested against.

WHAT IT DECIDES (E-036 S2a, delivery_plan_v26.md slice 8.1; spec:
engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md and its operator decision
of 2026-09-27)
A candidate VARIANT -- the exact config a backtest is about to run, on the
protocol it will run -- is ADMIT or REFUSE:

  Layer 2 (binding) -- the exact-match check. The candidate's key
  (tools/novelty.py: config hash, sorted symbols, the protocol file's
  timeframe and a hash of its windows) is looked up in
  campaign_record/campaign_memory.yaml, the one source of truth, through the
  SAME functions tools/decide_next.py uses. REPEAT -> REFUSE, NOVEL ->
  ADMIT. Binary: there is no NEIGHBOUR outcome and nothing here groups by
  family or compares composition fingerprints (the E-036 S2 design was
  rejected 2026-09-02; family machinery is retired, card G). A run with no
  memory entry (every run before the regroup_record stage) or an entry
  marked `legacy: true` can never produce REPEAT.

  Layer 1 (advisory only) -- campaign_knowledge_base.yaml, matched at
  MECHANISM grain (via hypothesis_id containment, see
  _kb_findings_matching_candidate). Its verdict is recorded as
  `layer1_advisory` next to the result and NEVER refuses (operator decision
  4): part of its input is pass_rule_evaluation.yaml's lineage_routing, a
  retired routing field (S1_FINDINGS_6B.md §5.1). The mechanism-grain notes
  and the precedence rule below describe what that warning means.

  Callers (run_phase1_research): _route_post_variant_selection (the legacy
  LLM backtest_specification flow) and _gate_config_direct_variants (the
  config-direct tool-stage 5a, one check per variant), both under
  orchestrator.variant_anti_adjacency_gate.enabled (off by default).

PRECEDENCE RULE (added by the dispatching session's 2026-08-23 review of
S1; not in S1's original design -- see EPIC.md's review log entry).
S1's own worked case (the funding 4h retest) resolves correctly by reading
the KB parent's `reactivation_condition` plus its prose note that a child
finding's closure "does NOT itself close the parent." That is right. But
two binding artifacts can disagree on their face: a registered
`lineage_routing: terminate` (in a run's pass_rule_evaluation.yaml -- the
mechanical, pre-committed B11 verdict) closes the LINEAGE IT NAMES -- i.e.
the one branch that specific run tested -- and nothing else. Only the KB
PARENT entry's own reactivation_condition can keep a SIBLING branch open.
Concretely: run_059's lineage_routing=terminate closes the DAILY branch of
funding_rate_continuous_mean_reversion_expanded_auto. It does not, and
cannot, touch the 4H branch of the SAME parent -- that branch was never
named by run_059's own registration, so nothing terminated it. This rule is
mechanical (_branch_closed_by_lineage_routing), not a KB-authored opinion:
it holds even if a human forgets to set the KB's own
`reactivation_consumed_by` field, and it never closes a branch the
terminating run did not itself test.

CLI:
  python strategy-research/tools/anti_adjacency_gate.py <strategy_config.json> <protocols/x.json> [--memory ...] [--kb ...] [--hypothesis-id ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

import campaign_memory as _cm  # tools/ sibling: the memory loader (the ONE source)
import novelty as _nov  # tools/ sibling: the exact-match key shared with decide_next
from build_exclusion_digest import extract_timeframes  # Layer 1's run-card timeframe reader

_HERE = Path(__file__).resolve().parent
_SR = _HERE.parent

DEFAULT_MEMORY_PATH = _SR / "campaign_record" / "campaign_memory.yaml"
DEFAULT_KB_PATH = _SR / "campaign_record" / "campaign_knowledge_base.yaml"
DEFAULT_RUNS_DIR = _SR / "runs"

_HID_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")
_MIN_HID_MATCH_LEN = 8  # guards against trivial short-token false containment


def _normalize_hid(hid) -> str:
    return _HID_NORMALIZE_RE.sub("_", str(hid or "").strip().lower()).strip("_")


def _hid_contains_match(a: str, b: str) -> bool:
    """True if the shorter normalized id is a real (non-trivial) substring
    of the longer one -- e.g. 'funding_rate_continuous_mean_reversion' is a
    prefix of 'funding_rate_continuous_mean_reversion_expanded'. Guards
    against short/generic ids (e.g. a hypothesis_id of just 'v3') producing
    spurious matches via _MIN_HID_MATCH_LEN."""
    if not a or not b:
        return False
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    if len(shorter) < _MIN_HID_MATCH_LEN:
        return shorter == longer
    return shorter in longer


# ---------------------------------------------------------------------------
# GateResult
# ---------------------------------------------------------------------------

class GateResult(dict):
    """Thin dict wrapper so tests can do result.route / result["route"] and
    so the CLI can yaml.safe_dump(result) directly."""

    def __init__(self, route: str, layer: str, reasons: list[str], **extra):
        assert route in ("admit", "refuse")
        super().__init__(route=route, layer=layer, reasons=reasons, **extra)

    @property
    def route(self):
        return self["route"]


def ADMIT(layer: str, reason: str, **extra) -> GateResult:
    return GateResult("admit", layer, [reason], **extra)


def REFUSE(layer: str, reason: str, **extra) -> GateResult:
    return GateResult("refuse", layer, [reason], **extra)


# ---------------------------------------------------------------------------
# Layer 1 -- KB, mechanism grain
# ---------------------------------------------------------------------------

def _kb_finding_hids(finding: dict) -> list[str]:
    ids = finding.get("hypothesis_ids")
    if ids:
        return [str(x) for x in ids]
    single = finding.get("hypothesis_id")
    return [str(single)] if single else []


def _kb_findings_matching_candidate(candidate_hid: str, kb_findings: list[dict]) -> list[dict]:
    """Findings whose hypothesis_id(s) contain (or are contained by) the
    candidate's, MOST SPECIFIC FIRST.

    FIX 1 (dispatching session's 2026-08-24 review): a candidate can
    legitimately match multiple KB findings (e.g. an _EXPANDED child and its
    base mechanism parent). layer1_kb_check returns on the first REFUSE/ADMIT
    it sees, so the order findings are evaluated in is load-bearing. Sorting
    here -- by the length of the matched hid, longest (most specific) first,
    a stable sort so ties keep their original relative order -- makes that
    order a property of the match itself (an _EXPANDED child's longer hid
    always sorts before its shorter base parent's), never of campaign_
    knowledge_base.yaml's incidental list order. Two findings for the same
    candidate must reach the same verdict regardless of which is listed
    first in the YAML.
    """
    norm_candidate = _normalize_hid(candidate_hid)
    if not norm_candidate:
        return []
    scored = []
    for finding in kb_findings:
        best_len = None
        for hid in _kb_finding_hids(finding):
            norm_hid = _normalize_hid(hid)
            if _hid_contains_match(norm_candidate, norm_hid):
                if best_len is None or len(norm_hid) > best_len:
                    best_len = len(norm_hid)
        if best_len is not None:
            scored.append((best_len, finding))
    scored.sort(key=lambda pair: -pair[0])
    return [finding for _, finding in scored]


# Branch-token vocabulary for parsing KB reactivation_condition PROSE (free
# text like "re-test ... at 4h or daily bars"). Distinct from
# build_exclusion_digest.extract_timeframes, which parses the STRUCTURED
# hypothesis_card.yaml `timeframe` field -- KB prose uses word forms
# ("daily") that field never does.
_KB_BRANCH_RE = re.compile(r"\b(15m|30m|1h|2h|4h|6h|8h|12h|1d|1w|daily|weekly|hourly)\b", re.I)
_KB_BRANCH_WORD_MAP = {"daily": "1d", "weekly": "1w", "hourly": "1h"}


def _extract_named_branches(reactivation_condition: str) -> set[str]:
    if not reactivation_condition:
        return set()
    found = set()
    for tok in _KB_BRANCH_RE.findall(reactivation_condition.lower()):
        found.add(_KB_BRANCH_WORD_MAP.get(tok, tok))
    return found


def _load_yaml(path: Path):
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _timeframe_of_run(run_id: str, runs_dir: Path) -> str | None:
    card_path = runs_dir / run_id / "artifacts" / "hypothesis_card.yaml"
    if not card_path.exists():
        return None
    try:
        card = _load_yaml(card_path)
    except Exception:  # noqa: BLE001
        return None
    tfs = extract_timeframes(card)
    return tfs[0] if tfs else None


def _lineage_routing_of_run(run_id: str, runs_dir: Path) -> str | None:
    """PRECEDENCE RULE input: reads the run's own registered pass_rule
    verdict (pass_rule_evaluation.yaml -- the B11/C7 machine-checkable
    total mapping), never verdict_interpretation.yaml's free-text
    protocol_verdict/status, which the pass_rule mapping is registered to
    OVERRIDE (see campaign_knowledge_base.yaml's funding_mr_daily_retest_killed
    entry for a documented case of exactly this override)."""
    p = runs_dir / run_id / "artifacts" / "pass_rule_evaluation.yaml"
    if not p.exists():
        return None
    try:
        data = _load_yaml(p)
    except Exception:  # noqa: BLE001
        return None
    return data.get("lineage_routing")


def _branches_closed_by_lineage_routing(matching_findings: list[dict], all_kb_findings: list[dict],
                                         runs_dir: Path) -> dict:
    """PRECEDENCE RULE, mechanical form.

    A branch of a matched (parent) finding's reactivation_condition is
    closed by a CHILD finding -- a separate KB entry, elsewhere in the file,
    that (a) explicitly names the parent in its own prose (mechanism /
    exhausted_basis / outcome_reason -- see _finding_references_parent) and
    (b) has at least one evidence run whose registered pass_rule verdict is
    lineage_routing=terminate. That run's OWN timeframe is the closed
    branch -- of the PARENT it named, and only that branch: a run that
    tested the daily branch can never close the 4h branch of the same
    parent, because it never named it.

    This deliberately searches ALL kb findings for children, not just the
    candidate's own matched set -- the candidate matches its PARENT via
    hypothesis_id containment (Layer 1's mechanism-grain match), but the
    CHILD that closes one of the parent's branches is a structurally
    different, separately-registered finding (e.g. funding_mr_daily_retest_
    killed vs. its parent funding_rate_continuous_mean_reversion_expanded_
    auto) that a candidate proposing the 4h branch would never itself match.

    Returns {parent_finding_id: {closed_timeframe, ...}}.
    """
    closed: dict[str, set[str]] = {}
    for parent in matching_findings:
        parent_id = parent.get("id")
        if not parent_id:
            continue
        for child in all_kb_findings:
            if child is parent:
                continue
            if not _finding_references_parent(child, parent_id):
                continue
            for run_id in child.get("evidence_runs", []) or []:
                routing = _lineage_routing_of_run(run_id, runs_dir)
                if routing == "terminate":
                    tf = _timeframe_of_run(run_id, runs_dir)
                    if tf:
                        closed.setdefault(parent_id, set()).add(tf)
    return closed


def _finding_references_parent(child: dict, parent_id: str) -> bool:
    """A child KB entry names its parent only in prose (no structured
    parent_id field exists in this KB's schema today) -- e.g.
    funding_mr_daily_retest_killed's exhausted_basis literally contains the
    substring 'funding_rate_continuous_mean_reversion_expanded_auto'. A
    literal substring check on the fields that carry this kind of
    cross-reference is deliberately conservative: it only fires on an
    EXPLICIT textual reference, never inferred from family/mechanism
    similarity alone."""
    haystack = " ".join(str(child.get(k, "")) for k in
                         ("mechanism", "exhausted_basis", "outcome_reason"))
    return parent_id in haystack


def layer1_kb_check(candidate_hid: str, candidate_timeframe: str,
                     kb_findings: list[dict], runs_dir: Path) -> GateResult | None:
    matching = _kb_findings_matching_candidate(candidate_hid, kb_findings)
    if not matching:
        return None

    closed_by_lineage = _branches_closed_by_lineage_routing(matching, kb_findings, runs_dir)

    for finding in matching:
        fid = finding.get("id")
        consumed_by = finding.get("reactivation_consumed_by")
        reactivation_condition = finding.get("reactivation_condition")
        exhausted = bool(finding.get("exhausted"))

        if reactivation_condition:
            named = _extract_named_branches(reactivation_condition)
            if candidate_timeframe in named:
                # PRECEDENCE RULE: a sibling branch this exact finding
                # named can only be closed by a lineage_routing=terminate
                # run that itself tested THAT branch -- never by a run
                # that tested a different one.
                if candidate_timeframe in closed_by_lineage.get(fid, set()):
                    return REFUSE(
                        "kb",
                        f"{fid}: branch '{candidate_timeframe}' closed by a run "
                        f"registered lineage_routing=terminate (precedence rule: "
                        f"terminate closes only the branch it named)",
                        kb_finding_id=fid,
                    )
                # FIX 2 (dispatching session's 2026-08-24 review):
                # reactivation_consumed_by is a flat, whole-finding field with
                # no branch attribution of its own. It can only unambiguously
                # mean "the branch that was consumed" when reactivation_
                # condition names exactly ONE branch -- with two or more, the
                # only mechanism that can attribute closure to a SPECIFIC
                # branch is the mechanical lineage-routing precedence rule
                # above; consumed_by must not blanket-REFUSE every named
                # branch just because one of them (unspecified which) was
                # consumed.
                if consumed_by and len(named) == 1:
                    return REFUSE("kb", f"{fid}: already reactivated by {consumed_by}",
                                   kb_finding_id=fid)
                return ADMIT(
                    "kb",
                    f"{fid}: matches open, unconsumed branch '{candidate_timeframe}' "
                    f"of an explicit reactivation_condition",
                    kb_finding_id=fid,
                )
            # named branches exist but candidate's timeframe isn't one of them --
            # this finding has no opinion on this specific candidate; keep looking.
            continue

        if consumed_by:
            # No reactivation_condition at all here (handled above when
            # present) -- consumed_by means "the whole finding is closed",
            # unchanged from before FIX 2.
            return REFUSE("kb", f"{fid}: already reactivated by {consumed_by}",
                           kb_finding_id=fid)

        if exhausted:
            # exhausted with NO reactivation_condition = a closed leaf with
            # no open branch at all (e.g. H-041-A's well-powered null).
            # This only fires for THIS finding (matched at hypothesis_id
            # containment grain) -- an unrelated sibling finding in the
            # same family never reaches this branch of the loop for a
            # candidate it wasn't matched to.
            return REFUSE("kb", f"{fid}: closed, no open reactivation clause",
                           kb_finding_id=fid)

        # Neither consumed, nor a reactivation clause, nor exhausted (e.g. an
        # invalidated_artifact placeholder like funding_rate_continuous_mean_
        # reversion_auto) -- this finding has nothing to say. Keep looking.

    return None


# ---------------------------------------------------------------------------
# Layer 2 -- exact match against campaign memory (E-036 S2a, slice 8.1)
# ---------------------------------------------------------------------------

def candidate_key(forecast_hash: str, symbols, protocol_ref, specs: dict,
                  card_timeframe=None) -> tuple:
    """The candidate's exact-match key, built with the SAME function the
    memory side uses (novelty.novelty_key): `forecast_hash` the canonical
    hash of the config file the backtest will run
    (run_phase1_research._compute_forecast_hash /
    novelty.forecast_hash_of_config), `symbols` the protocol's symbols (what
    tools/run_protocol.py iterates, and so what campaign_memory measures),
    `protocol_ref` the protocol file the backtest will run (relative to
    strategy-research/, campaign_memory.protocol_ref_of), `card_timeframe`
    only the unresolved-protocol fallback. The caller must have put the
    candidate's protocol in `specs` strictly (novelty.protocol_spec(...,
    strict=True)), so a candidate key is never "unresolved"."""
    return _nov.novelty_key(forecast_hash, sorted(set(symbols or [])),
                            {"protocol_ref": protocol_ref, "timeframe": card_timeframe}, specs)


def layer2_digest_check(key: tuple, index: dict) -> GateResult:
    """E-036 S2a (slice 8.1, operator decision 2026-09-27): BINARY.

      REPEAT -> REFUSE. A tested variant in campaign_memory.yaml has exactly
      this key (tools/novelty.py: config hash, symbols, the protocol file's
      timeframe, a hash of its windows). `matched`: every such
      {run_id, variant_id}.
      NOVEL -> ADMIT. Nothing in memory has this key.

    `index` is novelty.match_index(memory, specs, exclude_run_id=...), built
    once per run. There is no third outcome: no family, no neighbour, no
    composition fingerprint (the rejected E-036 S2 design is retired). A run
    with no memory entry, or an entry marked `legacy: true`, can never produce
    REPEAT. The name is kept from E-032 for its callers; there is no digest
    behind it any more."""
    matched = list(index.get(key) or [])
    if matched:
        refs = [f"{m['run_id']}:{m['variant_id']}" for m in matched]
        return REFUSE("exact_match",
                      f"exact repeat of tested variant(s) {refs} in campaign_memory.yaml "
                      f"(same config hash, symbols, timeframe and protocol windows)",
                      outcome="repeat", matched=matched)
    return ADMIT("exact_match", "no tested variant in campaign_memory.yaml has this exact key",
                 outcome="novel", matched=[])


def layer1_advisory(candidate_hid, candidate_timeframe, kb: dict | None,
                    runs_dir: Path) -> dict:
    """Layer 1 (KB reactivation) as a WARNING only (operator decision 4,
    2026-09-27): recorded next to the result, never a refusal -- its input
    includes pass_rule_evaluation.yaml's retired lineage_routing field
    (S1_FINDINGS_6B.md §5.1), so it cannot bind. It depends only on the run's
    hypothesis_id and timeframe, so a caller checking several variants of
    one run computes it once. {status: warn | admit | no_opinion |
    not_evaluated, reasons, kb_finding_id}."""
    if kb is None:
        return {"status": "not_evaluated",
                "reasons": ["campaign_knowledge_base.yaml not available"], "kb_finding_id": None}
    res = layer1_kb_check(str(candidate_hid or ""), candidate_timeframe,
                          (kb or {}).get("findings", []) or [], runs_dir)
    if res is None:
        return {"status": "no_opinion", "reasons": [], "kb_finding_id": None}
    return {"status": "warn" if res.route == "refuse" else "admit",
            "reasons": list(res.get("reasons") or []), "kb_finding_id": res.get("kb_finding_id")}


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def evaluate_candidate(key: tuple, memory: dict, specs: dict, *, kb: dict | None = None,
                       candidate_hid=None, candidate_timeframe=None,
                       runs_dir: Path = DEFAULT_RUNS_DIR,
                       exclude_run_id: str | None = None) -> GateResult:
    """One candidate, end to end (the CLI's path): Layer 2's binary exact
    match alone decides the route; Layer 1 is attached as `layer1_advisory`
    and never changes it. A caller checking several variants of one run
    builds novelty.match_index and layer1_advisory once and calls
    layer2_digest_check per variant instead."""
    index = _nov.match_index(memory, specs, exclude_run_id=exclude_run_id)
    result = layer2_digest_check(key, index)
    result["layer1_advisory"] = layer1_advisory(candidate_hid, candidate_timeframe, kb, runs_dir)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="the strategy config file the backtest will run")
    parser.add_argument("protocol", type=Path,
                        help="the protocol file (JSON or YAML) the backtest will run")
    parser.add_argument("--memory", type=Path, default=DEFAULT_MEMORY_PATH)
    parser.add_argument("--kb", type=Path, default=DEFAULT_KB_PATH)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--hypothesis-id", default=None)
    parser.add_argument("--exclude-run-id", default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    forecast_hash = _nov.forecast_hash_of_config(
        json.loads(args.config.read_text(encoding="utf-8")))
    protocol_ref = _cm.protocol_ref_of(str(args.protocol), _SR)
    memory = _cm.load_memory(args.memory)
    specs = _nov.protocol_specs(_SR, memory)
    specs[_nov.normalize_ref(protocol_ref)] = _nov.protocol_spec(_SR, protocol_ref, strict=True)
    proto = _nov.load_protocol(_SR, protocol_ref)
    key = candidate_key(forecast_hash, proto.get("symbols"), protocol_ref, specs)
    kb = _load_yaml(args.kb) if args.kb.exists() else None
    result = evaluate_candidate(key, memory, specs, kb=kb, candidate_hid=args.hypothesis_id,
                                candidate_timeframe=key[2], runs_dir=args.runs_dir,
                                exclude_run_id=args.exclude_run_id)
    out_data = dict(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            yaml.safe_dump(out_data, f, sort_keys=False, allow_unicode=True)
        print(f"anti_adjacency_result.yaml written to {args.out}")
    print(f"route={result['route']} layer={result['layer']} reasons={result['reasons']}")
    return 0 if result["route"] == "admit" else 1


if __name__ == "__main__":
    raise SystemExit(main())
