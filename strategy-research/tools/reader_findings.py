"""E-068 slice 5 (D-073): readers v3 -- what code writes and checks around them.

Under orchestrator.reader_findings.enabled only (run_phase1_research and
decide_next wire it; nothing here reads a flag). Design:
engineering/roadmap/E-068/DESIGN_PROPOSAL.md sections 6 and 8.

  * skip_rule -- a reader whose report has nothing to read is not called:
    regime_power when block_manifest.yaml lists /regime_detector as
    scaffolding (a deliberately ungated detector, run_070) or the base
    config's detector has no components and no rules (one constant label);
    component_attribution when every graded variant has at most one
    component. A skip is written as a `skipped` reading with its rule --
    never as an empty proposal list -- and counted in
    campaign_record/reader_skips.yaml (the campaign summary reads it).
  * claim_result_digest -- this run's measured claim numbers for the readers
    (artifacts/claim_result_digest.yaml): claim_measurement.yaml's status
    (an older run's claim_status.yaml, D-077) plus,
    per variant, the compact per-horizon numbers of its claim_test.yaml, and
    only when that file was measured on the bars the variant's current
    protocol_result.yaml names (else `stale`, no numbers) -- the binding of
    tools/claim_findings.py.
  * reader_findings_summary -- earlier runs' findings for the readers
    (artifacts/findings_summary_for_readers.yaml): the slice-4 summary over the
    campaign memory WITHOUT this run, compacted, newest 10.
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
 SKIP_OUTPUT_REFUSED, SKIP_EXPLORATION_UNAVAILABLE) = rp.SKIP_RULES
DIGEST_ARTIFACT = "claim_result_digest.yaml"
READER_SUMMARY_ARTIFACT = "findings_summary_for_readers.yaml"
# The two files above that could not be written before the readers ran (the
# readers then run without them); absent when both were written.
INPUT_GAPS_ARTIFACT = "reader_input_gaps.yaml"
READER_SUMMARY_MAX_ROWS = 10
SKIPS_REL = "campaign_record/reader_skips.yaml"
WARN_REPEAT = "repeats_measured_spec"
WARN_BLIND = "block_claim_cannot_see_block"
REGIME_DETECTOR_POINTER = "/regime_detector"
DIGEST_SCHEMA_VERSION = 1
NOTE = ("information only: effect sizes measured on saved bars, no p-value; readers explain "
        "these numbers and propose, they do not grade the claim")
# CUL-413 (D-077): every number in the digest says which statistic it is, so a
# reader never mixes the claim test's rank IC with the forecast_power report's
# Pearson correlation. One label per claim_tests.STATISTICS name (a test pins
# the key set); horizons are in bars of the run's timeframe.
STATISTIC_LABELS = {
    "rank_ic": ("rank IC (Spearman) of the bar-t forecast with the outcome, on the selected "
                "bars -- the claim test's own statistic; horizons in bars"),
    "mean_diff": ("mean outcome on the selected bars minus the baseline's mean (a difference "
                  "of means, not a correlation); horizons in bars"),
    "hit_rate": ("share of selected bars whose outcome has the claimed sign minus the "
                 "baseline's share (a difference of rates, not a correlation); horizons in bars"),
    "decay_curve": ("mean outcome on the selected bars minus the baseline's mean, at each "
                    "horizon (a difference of means, not a correlation); horizons in bars"),
}
STATISTICS_NOTE = ("each test's `effect` is that test's own statistic (its `statistic_label`); "
                   "none of them is the forecast_power report's forecast_return_corr, which is "
                   "a Pearson correlation of the forecast with the next bar's return on active "
                   "bars")


def statistic_label(name) -> str:
    """The digest's label for a claim test's statistic name (unknown: says so)."""
    return STATISTIC_LABELS.get(str(name), f"{name} (no label: not a known statistic)")


def _load(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Skip rules
# ---------------------------------------------------------------------------

def skip_rule(category: str, *, manifest=None, base_config=None, report=None):
    """{rule, reason} when `category`'s reader has nothing to read on this
    run, else None. Pure; any missing or odd input means "do not skip"."""
    if category == "regime_power":
        scaff = manifest.get("scaffolding") if isinstance(manifest, dict) else None
        pointers = [p.rstrip("/") for p in scaff or [] if isinstance(p, str)]
        if REGIME_DETECTOR_POINTER in pointers:
            return {"rule": SKIP_REGIME_SCAFFOLDING,
                    "reason": ("block_manifest.yaml lists /regime_detector as scaffolding: the "
                               "detector is deliberately not part of the idea, so there is no "
                               "regime gate of this idea to read")}
        det = base_config.get("regime_detector") if isinstance(base_config, dict) else None
        if isinstance(det, dict) and not det.get("components") and not det.get("rules"):
            return {"rule": SKIP_REGIME_CONSTANT,
                    "reason": ("the base config's regime detector has no components and no "
                               "rules: every bar gets its default regime, so there is no regime "
                               "signal to read")}
    elif category == "component_attribution":
        variants = report.get("variants") if isinstance(report, dict) else None
        if not isinstance(variants, dict) or not variants:
            return None
        names = {}
        for vid, v in variants.items():
            slices = v.get("slices") if isinstance(v, dict) else None
            overall = slices.get("overall") if isinstance(slices, dict) else None
            comps = overall.get("components_discovered") if isinstance(overall, dict) else None
            if not isinstance(comps, list):
                return None
            names[str(vid)] = len(comps)
        if max(names.values()) <= 1:
            return {"rule": SKIP_SINGLE_COMPONENT,
                    "reason": (f"every graded variant has at most one component "
                               f"({', '.join(f'{k}: {n}' for k, n in sorted(names.items()))}): "
                               f"there is nothing to attribute between components")}
    return None


def skipped_reading(category: str, run_id: str, skip: dict) -> dict:
    """The proposals file of a reader not called (or whose answer was refused
    after its retry): a `skipped` reading with the rule -- never `[]`, which
    would read as "nothing to propose"."""
    doc = {"schema_version": rp.READING_SCHEMA_VERSION, "reading_id": f"{category}-{run_id}",
           "skipped": {"rule": skip["rule"], "reason": skip["reason"]}}
    rp.check_reading(doc, category, "skipped reading")
    return doc


# ---------------------------------------------------------------------------
# This run's claim numbers for the readers
# ---------------------------------------------------------------------------

def _variant_digest(run_dir: Path, vid: str, row, card_hashes: dict, *,
                    run_file: str | None = None, statistics: dict | None = None) -> dict:
    """One variant's digest. `run_file`: the run file's name as read
    (claim_measurement.yaml, or an older run's claim_status.yaml);
    `statistics`: {test name: statistic name} from the card, so each measured
    test carries its `statistic_label` (CUL-413)."""
    import claim_findings as cf
    import claim_measure as cmeas
    if not isinstance(row, dict):
        return {"status": cmeas.NOT_MEASURED,
                "reason": f"not in {run_file or cmeas.RUN_FILE}"}
    if not row.get("file"):
        return {"status": cmeas.NOT_MEASURED, "reason": row.get("reason")}
    path = run_dir / "artifacts" / "variants" / vid / cmeas.VARIANT_FILE
    if not path.exists():
        return {"status": cmeas.NOT_MEASURED, "reason": cf.STALE,
                "detail": f"{cmeas.VARIANT_FILE} absent"}
    doc = _load(path) or {}
    if not doc.get("bars"):
        return {"status": cmeas.NOT_MEASURED, "reason": doc.get("reason")}
    try:
        problem = cf._binding_problem(run_dir, vid, doc, card_hashes)
    except FileNotFoundError as exc:
        problem = f"protocol_result.yaml unreadable ({exc})"
    if problem:
        return {"status": cmeas.NOT_MEASURED, "reason": cf.STALE, "detail": problem}
    if doc.get("status") == cmeas.MEASURED:
        status = cmeas.MEASURED
    elif doc.get("reason") == cmeas.NO_EVENTS:
        status = cmeas.NO_EVENTS
    else:
        return {"status": cmeas.NOT_MEASURED, "reason": doc.get("reason")}
    tests = {}
    for n, t in (doc.get("tests") or {}).items():
        if not isinstance(t, dict):
            continue
        tests[str(n)] = cf._compact_test(t)
        if statistics and str(n) in statistics:
            tests[str(n)]["statistic_label"] = statistic_label(statistics[str(n)])
    return {"status": status, "tests": tests}


VARIANT_PATCHES_FILE = "variant_patches.yaml"
VARIANT_PATCHES_NOTE = ("each variant's exact change to the base config (JSON pointer -> new "
                        "value). Read a variant's settings here, never infer them from its "
                        "name.")


def variant_patches_digest(arts: Path):
    """CUL-410: artifacts/variant_patches.yaml compacted for the readers --
    per variant its id, kind, symbol and patch (no rationale prose) -- or None
    when the file is absent or unreadable."""
    try:
        path = Path(arts) / VARIANT_PATCHES_FILE
        doc = _load(path) if path.exists() else None
    except Exception:  # noqa: BLE001 -- an unreadable file never spoils the digest
        return None
    rows = doc.get("variants") if isinstance(doc, dict) else None
    if not isinstance(rows, list):
        return None
    out = []
    for v in rows:
        if not isinstance(v, dict):
            continue
        patch = v.get("patch") if isinstance(v.get("patch"), list) else []
        out.append({"variant_id": v.get("variant_id"), "kind": v.get("kind"),
                    "symbol": v.get("symbol"),
                    "patch": [{"path": p.get("path"), "value": p.get("value")}
                              for p in patch if isinstance(p, dict)]})
    return {"note": VARIANT_PATCHES_NOTE, "base_config_ref": doc.get("base_config_ref"),
            "variants": out}


def claim_result_digest(run_dir: Path) -> dict:
    """artifacts/claim_result_digest.yaml's content. Never raises: a failure
    is the document's `status: error` (information only)."""
    import claim_card as cc
    import claim_findings as cf
    import claim_measure as cmeas
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    out = {"schema_version": DIGEST_SCHEMA_VERSION, "label": cf.LABEL, "note": NOTE,
           "information_only": True}
    try:
        # E-068 nearest build: a run that tested an approximation says so first
        # (deviations.yaml exists only under orchestrator.nearest_build or for a
        # side finding's start config, CUL-412).
        import nearest_build as nb
        block = nb.approximation_block(nb.load_record(arts))
        if block:
            out["approximation"] = block
        # CUL-410: each variant's exact settings, so a reader never guesses them
        # (run_073: forecast_power stated base period 1 and design period 2;
        # they were 2 and 3).
        patches = variant_patches_digest(arts)
        if patches is not None:
            out["variant_patches"] = patches
        card_path = arts / "hypothesis_card.yaml"
        card = (_load(card_path) or {}) if card_path.exists() else {}
        claim = card.get("claim") if isinstance(card, dict) else None
        tests = cf._tests_of(claim)
        kind_m = cf._manifest_kind(arts)
        out.update({
            "statement": claim.get("statement") if isinstance(claim, dict) else None,
            "kind": claim.get("kind") if isinstance(claim, dict) else None,
            "block_visibility": cc.block_visibility(claim, kind_m),
            "manifest_kind": kind_m,
            "statistics_note": STATISTICS_NOTE,
            "tests": [{"name": t["name"], "spec_hash": t["spec_hash"],
                       "statistic": t["statistic"],
                       "statistic_label": statistic_label(t["statistic"]),
                       "direction": t["direction"],
                       **{k: t["spec"][k] for k in ("selector", "outcome", "baseline")
                          if k in t["spec"]}} for t in tests],
        })
        status_path = cmeas.run_file_path(arts)  # an older run: claim_status.yaml (D-077)
        if not status_path.exists():
            out.update({"claim_status": "absent", "variants": {}})
            return out
        sdoc = _load(status_path) or {}
        out["claim_status"] = sdoc.get("claim_status")
        out["reason"] = sdoc.get("reason")
        card_hashes = {str(t["name"]): t["spec_hash"] for t in tests}
        stats = {str(t["name"]): t["statistic"] for t in tests}
        out["variants"] = {str(vid): _variant_digest(run_dir, str(vid), row, card_hashes,
                                                     run_file=status_path.name,
                                                     statistics=stats)
                           for vid, row in sorted((sdoc.get("variants") or {}).items())}
    except Exception as exc:  # noqa: BLE001 -- information only
        out.update({"status": "error", "detail": f"{type(exc).__name__}: {exc}"})
    return out


# ---------------------------------------------------------------------------
# Earlier runs' findings for the readers
# ---------------------------------------------------------------------------

def _largest(row: dict):
    effects = row.get("effect") or {}
    signs = row.get("claimed_sign_windows") or {}
    best = None
    for h, e in effects.items():
        if e is None:
            continue
        if best is None or abs(e) > abs(effects[best]):
            best = h
    if best is None:
        return None
    return {"horizon": best, "effect": effects[best], "claimed_sign_windows": signs.get(best)}


def reader_findings_summary(memory: dict, run_id: str,
                            max_rows: int = READER_SUMMARY_MAX_ROWS) -> dict:
    """Every finding in `memory` EXCEPT `run_id`'s own (on a resume the
    memory may already hold it), compacted for a prompt: per test its spec
    and, per variant, the status and the horizon with the largest absolute
    effect. Newest first, capped at `max_rows`; deterministic (no clock)."""
    import claim_findings as cf
    runs = {rid: e for rid, e in ((memory or {}).get("runs") or {}).items() if rid != run_id}
    full = cf.findings_summary({"runs": runs}, run_id, max_rows=max_rows)
    rows = []
    for row in full["findings"]:
        finding = (runs.get(row["run_id"]) or {}).get(cf.FINDING_KEY) or {}
        specs = {str(t.get("name")): t.get("spec") or {} for t in finding.get("tests") or []}
        tests = []
        for t in row.get("tests") or []:
            spec = specs.get(str(t.get("name"))) or {}
            tests.append({
                "name": t.get("name"), "spec_hash": t.get("spec_hash"),
                "statistic": t.get("statistic"), "direction": t.get("direction"),
                "selector": spec.get("selector"), "outcome": spec.get("outcome"),
                "by_variant": {vid: {"status": v.get("status"), "largest_effect": _largest(v)}
                               for vid, v in sorted((t.get("by_variant") or {}).items())}})
        compact = {k: row.get(k) for k in ("finding_id", "run_id", "kind", "status", "reason",
                                            "block_visibility", "statement", "scope")}
        if "deviations" in row:  # E-068 nearest build: an approximation, counted first
            compact = {"deviations": row["deviations"], **compact}
        rows.append(compact | {"tests": tests})
    # CUL-413 review: an earlier run's effect is labelled like this run's -- one
    # table for the statistics listed (the rows stay compact)
    stats = sorted({str(t["statistic"]) for r in rows for t in r["tests"]
                    if t.get("statistic") is not None})
    return {"schema_version": 1, "run_id": run_id, "excludes_run": run_id, "label": cf.LABEL,
            "note": NOTE, "information_only": True, "n_findings": full["n_findings"],
            "n_listed": len(rows), "by_status": full["by_status"], "by_kind": full["by_kind"],
            "statistic_labels": {s: statistic_label(s) for s in stats},
            "findings": rows, "same_spec_hash": full["same_spec_hash"]}


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


def side_finding_review(item: dict, *, prior: dict, own: set, run_id: str) -> dict:
    """{errors, tests_none, missing_block, spec_hashes, warnings} for one side
    finding. `errors` are check_claim's refusals (the reader's retry, or the
    candidate's ineligibility); `warnings` never refuse anything:
      - repeats_measured_spec: a test with the same spec_hash as a finding
        already recorded, or as this run's own claim test;
      - block_claim_cannot_see_block: the claim's kind names a block
        (claim_card.KIND_BLOCK) but no test reads that block's output
        (CLAIM_TESTS.md's visibility rule). A kind with no block is a pure
        finding and gets no such warning."""
    import claim_card as cc
    claim = item.get("claim") if isinstance(item, dict) else None
    res = cc.check_claim(claim)
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
# The campaign's skip record and its summary lines
# ---------------------------------------------------------------------------

def record_skips(root: Path, run_id: str, skips: dict) -> None:
    """campaign_record/reader_skips.yaml {runs: {run_id: {category: {rule,
    reason}}}}: this run's latest skips (a run with none is removed). Locked,
    atomic."""
    import campaign_memory as cm
    import campaign_review_retired as crr
    path = Path(root) / SKIPS_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with crr._lock(path, path.name):
        doc = crr._load_mapping(path, {})
        runs = doc.get("runs") if isinstance(doc.get("runs"), dict) else {}
        if skips:
            runs[run_id] = {c: {"rule": s["rule"], "reason": s["reason"]}
                            for c, s in sorted(skips.items())}
        else:
            runs.pop(run_id, None)
        cm._atomic_write(path, {**doc, "runs": runs})


def skip_summary_lines(root: Path) -> list:
    """Campaign-summary lines; [] when the record does not exist (so a summary
    is unchanged until a reader has been skipped)."""
    path = Path(root) / SKIPS_REL
    if not path.exists():
        return []
    title = ["", "## Readers skipped by a code rule (E-068 slice 5, no model call)", ""]
    try:
        doc = _load(path) or {}
    except (yaml.YAMLError, OSError, UnicodeDecodeError) as exc:  # never break the summary
        return title + [f"- {SKIPS_REL} is unreadable ({type(exc).__name__}); fix or remove it."]
    runs = doc.get("runs") if isinstance(doc, dict) and isinstance(doc.get("runs"), dict) else {}
    by_rule = {}
    for rid, cats in sorted(runs.items(), key=lambda kv: str(kv[0])):
        if not isinstance(cats, dict):        # a hand-edited row never breaks the summary
            continue
        for cat, s in sorted(cats.items(), key=lambda kv: str(kv[0])):
            rule = str(s.get("rule")) if isinstance(s, dict) else "unreadable"
            by_rule.setdefault(rule, []).append(f"{cat} in {rid}")
    n = sum(len(v) for v in by_rule.values())
    lines = title + [f"- Reader calls skipped: {n} in {len(runs)} run(s)"]
    for rule, where in sorted(by_rule.items()):
        lines.append(f"  - {rule}: {len(where)} ({', '.join(where)})")
    return lines


# ---------------------------------------------------------------------------
# E-073 step 2 (D-083): in-run dedup of side findings, under
# orchestrator.observable_backtest only (run_phase1_research wires it).
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


def _merge_key(item: dict):
    """(claim kind, spec_hashes, canonical config_change) of one flattened
    side finding, or None when it has no measurable test (refused claim or
    tests: none). The kind is part of the key (review fix 4): the
    confirmation routes by it (explore_confirm.finding_route: a block kind
    is PENDING, a pure kind IN_RUN), so the same tests under two kinds are
    two findings."""
    import json as _json
    import claim_card as cc
    res = cc.check_claim(item.get("claim") if isinstance(item, dict) else None)
    hashes = tuple(sorted({t["spec_hash"] for t in res.tests if t.get("spec_hash")}))
    if res.errors or res.tests_none or not hashes:
        return None
    change = item.get("config_change")
    canon = None
    if change:
        canon = _json.dumps(sorted((_json.dumps(c, sort_keys=True, default=str)
                                    for c in change), key=str), default=str)
    return str(item["claim"].get("kind")), hashes, canon


def side_finding_merges(readings: dict) -> list:
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
            key = _merge_key(item)
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
