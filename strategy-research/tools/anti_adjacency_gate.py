"""
anti_adjacency_gate.py -- E-032 S2a, Task 2.

Deterministic tool stage. No LLM call, no token cost -- same class of stage
as tools/prescreen_signal.py (the `signal_prescreen` `tool:` entry in
workflow/stages.yaml): a mechanical pass/fail should not be adjudicated by
prose. See engineering/roadmap/E-032/artifacts/s1_idea_generation.md Task 3
for the full design rationale and the worked calibration case this module
is regression-tested against.

WHAT IT DECIDES
A candidate hypothesis (family, instrument, timeframe) is ADMIT or REFUSE,
using two layers, evaluated IN THIS ORDER and never reversed:

  Layer 1 -- campaign_knowledge_base.yaml, matched at MECHANISM grain (via
  hypothesis_id containment, see _kb_findings_matching_candidate), never at
  FAMILY grain. This distinction is load-bearing, not stylistic: a family
  (e.g. "funding_rate_extreme") can contain several INDEPENDENT KB findings
  that reached different, unrelated verdicts (H-041-A's extreme-threshold
  formulation closed permanently at run_050; FUNDING_RATE_CONTINUOUS_MEAN_
  REVERSION_EXPANDED is a distinct, still-open mechanism). Matching at
  family grain would let H-041-A's closure silently REFUSE a candidate that
  has nothing to do with it -- the exact failure mode this gate exists to
  avoid, just relocated one layer down. Matching is via normalized
  hypothesis_id containment (handles the real-world "_EXPANDED" suffix
  drift between a run's own hypothesis_card.yaml and its KB entry, observed
  on run_044) -- see _normalize_hid().

  Layer 2 -- the exclusion digest (build_exclusion_digest.py), matched at
  FAMILY grain: has THIS family already run at THIS (instrument, timeframe)?
  Only reached when Layer 1 has no opinion (no matching KB finding, or a
  matching finding with no reactivation_condition/exhausted verdict either
  way). Never trust campaign_state.yaml's flat instruments_tried/
  timeframes_tried lists here -- see the digest module's own docstring for
  the measured false-refusal this avoids.

  Default -- ADMIT. Absence of history is not evidence of an unresearched
  idea being bad; it is simply not yet REFUSED by anything on record.

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
  python strategy-research/tools/anti_adjacency_gate.py <candidate.yaml> [--digest ...] [--kb ...] [--out ...]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

from build_exclusion_digest import (
    classify_family,
    extract_instruments,
    extract_timeframes,
)

_HERE = Path(__file__).resolve().parent
_SR = _HERE.parent

DEFAULT_DIGEST_PATH = _SR / "campaign_record" / "exclusion_digest.yaml"
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
    norm_candidate = _normalize_hid(candidate_hid)
    if not norm_candidate:
        return []
    matches = []
    for finding in kb_findings:
        for hid in _kb_finding_hids(finding):
            if _hid_contains_match(norm_candidate, _normalize_hid(hid)):
                matches.append(finding)
                break
    return matches


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

        if consumed_by:
            return REFUSE("kb", f"{fid}: already reactivated by {consumed_by}",
                           kb_finding_id=fid)

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
                return ADMIT(
                    "kb",
                    f"{fid}: matches open, unconsumed branch '{candidate_timeframe}' "
                    f"of an explicit reactivation_condition",
                    kb_finding_id=fid,
                )
            # named branches exist but candidate's timeframe isn't one of them --
            # this finding has no opinion on this specific candidate; keep looking.
            continue

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
# Layer 2 -- exclusion digest, family grain
# ---------------------------------------------------------------------------

def layer2_digest_check(candidate: dict, instrument: str, timeframe: str,
                         digest: dict) -> GateResult:
    family, confidence = classify_family(candidate)
    families = digest.get("families", {})
    entry = families.get(family)
    if entry:
        for triple in entry.get("triples", []):
            if triple["instrument"] == instrument and triple["timeframe"] == timeframe:
                return REFUSE(
                    "digest",
                    f"family '{family}' already run at ({instrument}, {timeframe}) "
                    f"-- run_ids={triple['run_ids']}",
                    family=family, family_confidence=confidence,
                )

    # Never a silent auto-refuse on a bare-string low-detail failed_families
    # entry -- flag it as supporting context only (mirrors S1's Task 3
    # predicate exactly).
    low_detail_flag = any(
        e.get("family") == family and e.get("detail") == "bare_string_low_detail"
        for e in digest.get("failed_families_passthrough", [])
    )
    return ADMIT(
        "default",
        f"no matching family/instrument/timeframe triple in the digest for "
        f"family '{family}'" + (" (weak prior: bare-string failed_families entry "
                                 "exists for this family, not gating)" if low_detail_flag else ""),
        family=family, family_confidence=confidence,
        low_detail_prior_failure=low_detail_flag,
    )


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def evaluate_candidate(candidate: dict, digest: dict, kb: dict, runs_dir: Path,
                        instrument: str | None = None, timeframe: str | None = None) -> GateResult:
    """candidate: a hypothesis_card.yaml-shaped dict (or close enough --
    only hypothesis_id, edge_source, library_lookup, thesis, target_market,
    timeframe are read). instrument/timeframe: override the values that
    would otherwise be derived from candidate['target_market']/['timeframe']
    -- required when a caller is evaluating one variant of a multi-symbol
    card individually (e.g. an expanded_hypothesis_card.yaml variant)."""
    if timeframe is None:
        tfs = extract_timeframes(candidate)
        timeframe = tfs[0] if tfs else None
    if instrument is None:
        instruments = extract_instruments(candidate)
        instrument = instruments[0] if instruments else None

    kb_findings = kb.get("findings", [])
    result = layer1_kb_check(candidate.get("hypothesis_id", ""), timeframe, kb_findings, runs_dir)
    if result is not None:
        return result

    return layer2_digest_check(candidate, instrument, timeframe, digest)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="hypothesis_card.yaml-shaped candidate")
    parser.add_argument("--digest", type=Path, default=DEFAULT_DIGEST_PATH)
    parser.add_argument("--kb", type=Path, default=DEFAULT_KB_PATH)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--instrument", default=None)
    parser.add_argument("--timeframe", default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    candidate = _load_yaml(args.candidate)
    digest = _load_yaml(args.digest)
    kb = _load_yaml(args.kb)

    result = evaluate_candidate(candidate, digest, kb, args.runs_dir,
                                 instrument=args.instrument, timeframe=args.timeframe)

    out_data = dict(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            yaml.safe_dump(out_data, f, sort_keys=False, allow_unicode=True)
        print(f"anti_adjacency_result.yaml written to {args.out}")
    print(f"route={result['route']} layer={result['layer']} reasons={result['reasons']}")
    return 0 if result["route"] == "admit" else 1


if __name__ == "__main__":
    raise SystemExit(main())
