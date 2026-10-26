"""E-068 slice 5 (D-073): readings v3 -- what code writes and checks around them.

Nothing here reads a flag (run_phase1_research and decide_next wire it). Design:
engineering/roadmap/E-068/DESIGN_PROPOSAL.md sections 6 and 8. D-198: the five readers and
the orchestrator.reader_findings flag are deleted, and with them the skip rules, the claim
digest and earlier-findings summary the readers received, and the skip record (the analyst,
D-197, writes the readings now).

  * skipped_reading -- the code-written `skipped` reading (never an empty list).
  * side_finding_review -- a side finding's claim block through
    claim_card.check_claim, plus two WARNINGS that never refuse anything: a
    test whose spec_hash is already in the findings (or is this run's own
    claim test), and a block-kind claim whose tests cannot see that block.

INFORMATION ONLY (D-055, D-064): nothing here bans, routes, stops or parks a
run, and no text written here names a verdict on the claim (the grid and
claim_measure measure; readers explain).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import reader_proposals as rp  # noqa: E402

(SKIP_REGIME_SCAFFOLDING, SKIP_REGIME_CONSTANT, SKIP_SINGLE_COMPONENT,
 SKIP_OUTPUT_REFUSED, SKIP_EXPLORATION_UNAVAILABLE, SKIP_REPLACED_BY_ANALYST,
 SKIP_OPERATOR_REFOLD) = rp.SKIP_RULES
WARN_REPEAT = "repeats_measured_spec"
WARN_BLIND = "block_claim_cannot_see_block"


def skipped_reading(category: str, run_id: str, skip: dict) -> dict:
    """The proposals file of a reader not called (or whose answer was refused
    after its retry): a `skipped` reading with the rule -- never `[]`, which
    would read as "nothing to propose"."""
    doc = {"schema_version": rp.READING_SCHEMA_VERSION, "reading_id": f"{category}-{run_id}",
           "skipped": {"rule": skip["rule"], "reason": skip["reason"]}}
    rp.check_reading(doc, category, "skipped reading")
    return doc


# ---------------------------------------------------------------------------
# Side findings
# ---------------------------------------------------------------------------

def prior_spec_hashes(memory: dict, exclude_run: str | None = None) -> dict:
    """{spec_hash: [{run_id, status}, ...]} over every finding in the memory
    (except `exclude_run`'s), in run order."""
    import claim_findings as cf
    out = {}
    for rid in sorted(((memory or {}).get("runs") or {}), key=lambda r: cf._run_order(str(r))):
        if rid == exclude_run:
            continue
        finding = (memory["runs"][rid] or {}).get(cf.FINDING_KEY)
        if not isinstance(finding, dict):
            continue
        for t in finding.get("tests") or []:
            h = t.get("spec_hash") if isinstance(t, dict) else None
            if h and not any(r["run_id"] == rid for r in out.get(h, [])):
                out.setdefault(h, []).append({"run_id": rid, "status": finding.get("status")})
    return out


def own_spec_hashes(card) -> set:
    """The spec_hashes of a run's own card claim tests."""
    import claim_findings as cf
    claim = card.get("claim") if isinstance(card, dict) else None
    return {t["spec_hash"] for t in cf._tests_of(claim) if t.get("spec_hash")}


def d095_refusals(claim) -> list[str]:
    """D-095 at the side-finding check (operator ruling D-157, 2026-10-20: "one short line"):
    one line per hit of analyst_session.exit_selector_own_outcome_hits -- "D-095: " and the
    hit's `what`. It is what decide-next's INFEASIBLE reason carries (next_test_refused: ...)
    and what the reading content check lists; the analyst's longer message is its own
    seam's (exit_selector_own_outcome_errors)."""
    import analyst_session as asm  # tools/ sibling, light
    return [f"D-095: {h['what']}" for h in asm.exit_selector_own_outcome_hits(claim)]


def _check(claim, folds: bool, trade_tests: bool):
    """check_claim with the folds kinds (D-089) and the trade-level test family (D-091),
    each passed only when on, so a call with both off is exactly the original one.
    D-095, extended beyond the analyst (operator, 2026-10-20): with the trade family on, a
    test selecting lots by an exit-time field and measuring their own outcome is refused here
    too, one short line per test (d095_refusals), and the claim's tests are dropped as for any
    refused claim. Not in check_claim: fold confirmation re-checks recorded claims through
    check_claim alone."""
    import claim_card as cc
    kw = {**({"folds": True} if folds else {}), **({"trade_tests": True} if trade_tests else {})}
    res = cc.check_claim(claim, **kw)
    if trade_tests:
        d095 = d095_refusals(claim)     # imports analyst_session only with the family on
        if d095:
            res.errors += d095
            res.tests = []
    return res


def side_finding_review(item: dict, *, prior: dict, own: set, run_id: str,
                        folds: bool = False, trade_tests: bool = False) -> dict:
    """{errors, tests_none, missing_block, spec_hashes, warnings} for one side
    finding. `errors` are check_claim's refusals (the reader's retry, or the
    candidate's ineligibility); `warnings` never refuse anything:
      - repeats_measured_spec: a test with the same spec_hash as a finding
        already recorded, or as this run's own claim test;
      - block_claim_cannot_see_block: the claim's kind names a block
        (claim_card.KIND_BLOCK) but no test reads that block's output
        (CLAIM_TESTS.md's visibility rule). A kind with no block is a pure
        finding and gets no such warning.
    `folds` (D-089, orchestrator.folds.enabled): check_claim with the folds kinds, so a
    claim of kind execution_behaviour is accepted here too; off: exactly as before.
    `trade_tests` (D-091, orchestrator.analyst.enabled): the trade-level family too."""
    import claim_card as cc
    claim = item.get("claim") if isinstance(item, dict) else None
    res = _check(claim, folds, trade_tests)
    out = {"errors": list(res.errors), "tests_none": res.tests_none,
           "missing_block": res.missing_block,
           "spec_hashes": [t["spec_hash"] for t in res.tests], "warnings": []}
    if res.errors or res.tests_none:
        return out
    for h in out["spec_hashes"]:
        if h in own:
            out["warnings"].append({"kind": WARN_REPEAT, "spec_hash": h, "own_claim": True,
                                    "runs": [{"run_id": run_id, "status": None}]})
        elif h in prior:
            out["warnings"].append({"kind": WARN_REPEAT, "spec_hash": h, "own_claim": False,
                                    "runs": list(prior[h])})
    block = cc.KIND_BLOCK.get(claim.get("kind"))
    if block in ("forecast", "regime") and cc.block_visibility(claim, block) == cc.VISIBILITY_BLIND:
        out["warnings"].append({
            "kind": WARN_BLIND, "block_kind": block,
            "message": (f"the claim's kind names a {block} block, but no test reads the block's "
                        f"output ({'forecast' if block == 'forecast' else 'regime'}); "
                        f"CLAIM_TESTS.md: at least one test must read it")})
    return out


def test_request_row(run_id: str, parent_hypothesis_id, category: str, item: dict,
                     review: dict) -> dict:
    """A campaign_record/test_requests.yaml row for a side finding that says
    `tests: none` (same appender and key as step 1a's rows)."""
    claim = item.get("claim") or {}
    return {"run_id": run_id, "stage": "specialist_readers",
            "card": f"proposals/{category}.yaml#{item.get('proposal_id')}",
            "hypothesis_id": f"{parent_hypothesis_id}__{item.get('proposal_id')}",
            "claim_kind": claim.get("kind"), "statement": claim.get("statement"),
            "missing_block": review.get("missing_block")}


test_request_row.__test__ = False  # not a pytest test


# ---------------------------------------------------------------------------
# E-073 step 2 (D-083): in-run dedup of side findings (D-198: the observable_backtest
# flag that wired it is deleted; the functions stay).
# ---------------------------------------------------------------------------

MERGES_ARTIFACT = "side_finding_merges.yaml"
MERGES_SCHEMA_VERSION = 1
MERGE_RULE = ("two side findings of this run are ONE finding when their claims have the same "
              "kind, their claim tests the same set of spec_hashes (claim_tests) and the same "
              "config_change (none, or the same items): the same measurement on the same config, "
              "confirmed the same way. A different kind, a partial overlap, a different change "
              "or `tests: none` is not merged.")
MERGE_NOT_AGREEMENT = ("not agreement and not extra evidence: the readers read the same inputs, "
                       "so a second reader proposing the same test is not an independent "
                       "observation; the merged finding is measured, counted and ranked once, "
                       "with its first source's scores")


def _merge_key(item: dict, folds: bool = False, trade_tests: bool = False):
    """(claim kind, spec_hashes, canonical config_change) of one flattened
    side finding, or None when it has no measurable test (refused claim or
    tests: none). The kind is part of the key (review fix 4): the
    confirmation routes by it (explore_confirm.finding_route: a block kind
    is PENDING, a pure kind IN_RUN), so the same tests under two kinds are
    two findings. D-162: a config vehicle (a mapping `vehicle`, never a
    config_change) is keyed on its canonical config (sorted-key JSON), so two
    findings merge only on the same whole config."""
    import json as _json
    claim = item.get("claim") if isinstance(item, dict) else None
    # D-089: under the folds flag the folds kinds (execution_behaviour) are claims too
    res = _check(claim, folds, trade_tests)
    hashes = tuple(sorted({t["spec_hash"] for t in res.tests if t.get("spec_hash")}))
    if res.errors or res.tests_none or not hashes:
        return None
    change = item.get("config_change")
    canon = None
    vehicle = item.get("vehicle")
    if isinstance(vehicle, dict):
        try:
            canon = "config:" + _json.dumps(vehicle.get("config"), sort_keys=True, default=str)
        except TypeError:          # mixed key types in a model-written mapping
            canon = "config:" + repr(vehicle.get("config"))
    elif change:
        canon = _json.dumps(sorted((_json.dumps(c, sort_keys=True, default=str)
                                    for c in change), key=str), default=str)
    return str(item["claim"].get("kind")), hashes, canon


def reading_structure(doc: dict, folds: bool = False, trade_tests: bool = False) -> list:
    """What a citation retry must keep (D-083): for each item of a v3 reading
    (rp.flatten_reading), (item kind, claim kind, sorted spec_hashes), sorted
    -- the same number of side findings proposing the same tests the same
    way. Wording, evidence and scores are not part of it."""
    out = []
    for item in rp.flatten_reading(doc):
        claim = item.get("claim")
        kind = str(claim.get("kind")) if isinstance(claim, dict) else None
        if claim is None:
            tests = []
        else:      # D-089: folds kinds are claims under the folds flag
            tests = _check(claim, folds, trade_tests).tests
        out.append((item["kind"], kind,
                    tuple(sorted({t["spec_hash"] for t in tests if t.get("spec_hash")}))))
    return sorted(out, key=repr)


def side_finding_merges(readings: dict, folds: bool = False, trade_tests: bool = False) -> list:
    """The duplicate groups among a run's side findings (MERGE_RULE). Pure.
    `readings`: {category: v3 reading}. Order: categories sorted, then each
    reading's side findings in order (the order explore_confirm measures
    them in); the first member of a group is its primary. Returns
    [{finding_id, finding_ids, sources: [{category, finding_id}], spec_hashes,
    config_change}] for groups of two or more only."""
    groups, order = {}, []
    for cat, doc in sorted((readings or {}).items()):
        if not isinstance(doc, dict) or "skipped" in doc:
            continue
        for item in rp.flatten_reading(doc):
            if item.get("kind") != rp.SIDE_FINDING:
                continue
            key = _merge_key(item, **({"folds": True} if folds else {}),
                             **({"trade_tests": True} if trade_tests else {}))
            if key is None:
                continue
            if key not in groups:
                order.append(key)
                groups[key] = {"items": [], "config_change": item.get("config_change")}
            groups[key]["items"].append((cat, item["proposal_id"]))
    out = []
    for key in order:
        members = groups[key]["items"]
        if len(members) < 2:
            continue
        out.append({"finding_id": members[0][1],
                    "finding_ids": [pid for _c, pid in members],
                    "sources": [{"category": c, "finding_id": pid} for c, pid in members],
                    "spec_hashes": list(key[1]),
                    "config_change": groups[key]["config_change"]})
    return out


def merges_doc(run_id: str, merges: list) -> dict:
    """artifacts/side_finding_merges.yaml (written under the flag, `merged: []`
    when nothing repeats, so a reader of the run can see the check ran)."""
    return {"schema_version": MERGES_SCHEMA_VERSION, "run_id": run_id, "rule": MERGE_RULE,
            "note": MERGE_NOT_AGREEMENT, "merged": list(merges)}


def merge_index(doc) -> dict:
    """{finding_id: {"primary": id, "order": n, "group": group}} for every
    member of a merge group in a side_finding_merges.yaml document; {} for
    None or a document of another shape (never raises)."""
    out = {}
    groups = doc.get("merged") if isinstance(doc, dict) else None
    for g in groups if isinstance(groups, list) else []:
        ids = g.get("finding_ids") if isinstance(g, dict) else None
        if not isinstance(ids, list) or len(ids) < 2:
            continue
        for n, fid in enumerate(ids):
            if isinstance(fid, str):
                out[fid] = {"primary": ids[0], "order": n, "group": g}
    return out
