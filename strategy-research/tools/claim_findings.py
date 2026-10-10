"""E-068 slice 4: the run's FINDING and the findings summary.

Under orchestrator.claim_tests.enabled only (the regroup_record stage in
run_phase1_research wires it; nothing here reads a flag). Design:
engineering/roadmap/E-068/DESIGN_PROPOSAL.md sections 5 and 8.

  * build_finding -- `finding` in the run's campaign_memory.yaml entry: the
    claim (statement, kind, tests with their spec_hash), whether the tests can
    see the block, the scope (venue, symbols, timeframe, period, windows sha),
    the measured effect sizes per variant with their window and coin sign
    counts, the status, the trial ids and the source run. Compact: per-window
    and per-era detail stays in each variant's claim_test.yaml (referenced).
  * findings_summary -- artifacts/findings_summary.yaml: a compact, code-built
    "what we measured so far" view over every finding in the memory
    (deterministic: no clock, so a resume rewrites the same bytes). In this
    slice no prompt reads it.

INFORMATION ONLY (D-055, D-064): a finding never bans, routes, stops or parks
anything and never changes idea_status. Statuses are those claim_measure
writes -- `measured` (labelled "measured, not proven"), `no_events`,
`not_measured` with a reason -- plus `error` when the finding itself could not
be built. There is no verdict: no text written here names one.

SAME ATTEMPT, OR NO NUMBERS: the memory entry describes the variants of the
run's latest protocol_execution attempt. A variant's numbers are attached only
when its claim_test.yaml was measured on exactly the bars that variant's
current protocol_result.yaml names (each backtest writes its bars under a new
timestamped run id, so an earlier attempt's bars have other paths), the
variant is `tested` in the entry, and the card's tests have the same
spec_hash. Anything else is `not_measured` with reason `stale`; old numbers
are never attached.

Pure functions over files the caller names; importable without the
orchestrator.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import claim_card as cc  # noqa: E402
import claim_measure as cmeas  # noqa: E402
import nearest_build as nb  # noqa: E402

FINDING_KEY = "finding"
SUMMARY_ARTIFACT = "findings_summary.yaml"
SUMMARY_SCHEMA_VERSION = 1
SUMMARY_MAX_ROWS = 200
STATEMENT_CHARS = 200
LABEL = cmeas.LABEL                       # "measured, not proven"
MEASURED = cmeas.MEASURED
NOT_MEASURED = cmeas.NOT_MEASURED
NO_EVENTS = cmeas.NO_EVENTS
ERROR = "error"
STALE = "stale"
CLAIM_STATUS_ABSENT = "claim_status_absent"
NOTE = ("information only: effect sizes measured on this run's own bars, no p-value and "
        "no verdict (CUL-394); a finding never bans, routes or stops anything (D-055)")
_TEST_SPEC_KEYS = ("selector", "outcome", "baseline", "statistic", "direction", "floor",
                   "consistency", "eras")


def _load(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _r(v):
    """Six significant digits: compact, and never more precise than useful."""
    return None if v is None else float(f"{float(v):.6g}")


def _ref(run_id: str, rel: str) -> str:
    return f"runs/{run_id}/{rel}"


# ---------------------------------------------------------------------------
# The claim
# ---------------------------------------------------------------------------

def _tests_of(claim) -> list:
    tests = claim.get("tests") if isinstance(claim, dict) else None
    out = []
    for t in tests if isinstance(tests, list) else []:
        if not isinstance(t, dict):
            continue
        try:
            # D-091 review: a trade-level test's hash (the family is only ever in a card
            # under orchestrator.analyst.enabled; acceptance is check_claim's, earlier)
            spec_hash = cmeas.test_spec(t, cmeas._is_trade_test(t))[1]
        except Exception:  # noqa: BLE001 -- an invalid test keeps spec_hash None
            spec_hash = None
        outcome = t.get("outcome")
        out.append({"name": t.get("name"), "spec_hash": spec_hash,
                    "statistic": t.get("statistic"), "direction": t.get("direction"),
                    "outcome": outcome.get("kind") if isinstance(outcome, dict) else None,
                    "spec": {k: t[k] for k in _TEST_SPEC_KEYS if k in t}})
    return out


def _manifest_kind(arts: Path):
    import block_manifest as bm
    manifest = bm.load_manifest_file(arts / bm.MANIFEST_FILENAME)
    return ((manifest or {}).get("block") or {}).get("kind")


# ---------------------------------------------------------------------------
# One variant: bound to the entry's attempt, or stale
# ---------------------------------------------------------------------------

def _expected_bars(run_dir: Path, vid: str) -> list:
    """The bars paths the variant's CURRENT protocol_result.yaml names, as
    claim_tests.load_variant_bars maps them (relative to the run dir)."""
    pr = _load(run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml") or {}
    return sorted(f"variants/{vid}/results/{e['run_id']}/bars.csv"
                  for e in pr.get("results") or [] if isinstance(e, dict) and e.get("run_id"))


def _binding_problem(run_dir: Path, vid: str, doc: dict, card_hashes: dict):
    """None when claim_test.yaml belongs to the attempt the entry describes,
    else a short reason."""
    measured_on = sorted(str(b.get("path")) for b in doc.get("bars") or [] if isinstance(b, dict))
    expected = _expected_bars(run_dir, vid)
    if not expected or measured_on != expected:
        return ("claim_test.yaml was measured on other bars than the variant's current "
                "protocol_result.yaml names")
    for name, t in (doc.get("tests") or {}).items():
        h = t.get("spec_hash") if isinstance(t, dict) else None
        if h is not None and card_hashes.get(str(name)) != h:
            return f"test {name!r}: spec_hash differs from the card's current test"
    return None


def _compact_test(t: dict) -> dict:
    out = {"status": t.get("status"), "spec_hash": t.get("spec_hash")}
    if t.get("status") != MEASURED:
        out["reason"] = t.get("reason")
        return out
    # Compact (detail stays in claim_test.yaml): `oriented` is left out (it is
    # `effect` signed by the test's direction) and `per_coin` only when the
    # variant has more than one coin (with one it repeats the variant's row).
    horizons = {}
    for h, r in (t.get("horizons") or {}).items():
        row = {"effect": _r(r.get("value")), "n_events": r.get("n_events"),
               "windows_claimed_sign": r.get("windows_with_claimed_sign"),
               "windows_with_value": r.get("windows_with_a_value")}
        coins = r.get("per_coin") or {}
        if len(coins) > 1:
            row["per_coin"] = {sym: {"effect": _r(c.get("value")), "n_events": c.get("n_events"),
                                     "windows_claimed_sign": c.get("windows_with_claimed_sign"),
                                     "windows_with_value": c.get("windows_with_a_value")}
                               for sym, c in coins.items()}
        horizons[str(h)] = row
    peak = t.get("peak_horizon")
    out.update({"peak_horizon": None if peak is None else str(peak),  # same type as the keys
                "floor_not_met": list(t.get("floor_not_met") or []), "horizons": horizons})
    return out


def _bars_really_missing(run_dir: Path, vid: str) -> bool:
    """A `bars_missing` claim_test.yaml is shown to describe the current
    attempt only if a bars file the current protocol_result.yaml names is
    missing now."""
    try:
        expected = _expected_bars(run_dir, vid)
    except FileNotFoundError:
        return True
    return not expected or any(not (run_dir / p).exists() for p in expected)


def _not_older_than_result(run_dir: Path, vid: str, path: Path, missing_ok: bool) -> bool:
    """For a claim file that carries no bars to compare: it was written by the
    attempt the entry describes only if it is not older than the variant's
    current protocol_result.yaml (claim_measure writes after the backtests; a
    later attempt rewrites protocol_result.yaml). `missing_ok`: no variant
    protocol_result.yaml at all (variant loop off) counts as consistent.
    Labels only (numbers bind on bars paths, never on file times): in a run
    folder copied without its timestamps the label may be wrong."""
    result = run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml"
    if not result.exists():
        return missing_ok
    return path.exists() and path.stat().st_mtime_ns >= result.stat().st_mtime_ns


def _stale(rec: dict, detail: str) -> tuple:
    return {**rec, "status": NOT_MEASURED, "reason": STALE, "detail": detail}, None


def _variant(run_dir: Path, run_id: str, vid: str, ventry: dict, status_row,
             card_hashes: dict, run_reason=None) -> tuple:
    """(per-variant record, claim_test ref or None). Numbers only when bound.
    `run_reason`: the run file's (claim_measurement.yaml) own not-measured
    reason, if any. A reason without numbers is passed through only when its
    file is shown to belong to this attempt; otherwise `stale`."""
    rec = {"trial_id": ventry.get("trial_id")}
    if ventry.get("status") != "tested":
        return {**rec, "status": NOT_MEASURED, "reason": f"variant_{ventry.get('status')}"}, None
    status_path = cmeas.run_file_path(run_dir / "artifacts")
    if not isinstance(status_row, dict):
        if run_reason and _not_older_than_result(run_dir, vid, status_path, missing_ok=True):
            # nothing was measured in the run (card gap, no graded variants, ...)
            return {**rec, "status": NOT_MEASURED, "reason": run_reason}, None
        return _stale(rec, f"not in {status_path.name}: not measured in this attempt")
    if not status_row.get("file"):
        # skipped by claim_measure (stale_result, backtest_failed, invalidated, ...)
        if _not_older_than_result(run_dir, vid, status_path, missing_ok=False):
            return {**rec, "status": NOT_MEASURED, "reason": status_row.get("reason")}, None
        return _stale(rec, f"{status_path.name} (its reason: {status_row.get('reason')}) is "
                           f"older than the variant's protocol_result.yaml")
    rel = f"artifacts/variants/{vid}/{cmeas.VARIANT_FILE}"
    path = run_dir / rel
    if not path.exists():
        return _stale(rec, f"{cmeas.VARIANT_FILE} absent")
    doc = _load(path) or {}
    if not doc.get("bars"):
        # never measured (bars unreadable, holdout, error): no numbers to attach
        if _not_older_than_result(run_dir, vid, path, missing_ok=False) or (
                doc.get("reason") == cmeas.BARS_MISSING and _bars_really_missing(run_dir, vid)):
            return {**rec, "status": NOT_MEASURED, "reason": doc.get("reason")}, None
        return _stale(rec, f"{cmeas.VARIANT_FILE} names no bars (its reason: "
                           f"{doc.get('reason')}) and is older than the variant's "
                           f"protocol_result.yaml")
    problem = _binding_problem(run_dir, vid, doc, card_hashes)
    if problem:
        return _stale(rec, problem)
    if doc.get("status") == MEASURED:
        st = MEASURED
    elif doc.get("reason") == NO_EVENTS:
        st = NO_EVENTS
    else:
        return {**rec, "status": NOT_MEASURED, "reason": doc.get("reason")}, None
    tests = {str(n): _compact_test(t) for n, t in (doc.get("tests") or {}).items()
             if isinstance(t, dict)}
    return {**rec, "status": st, "tests": tests}, _ref(run_id, rel)


# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------

def _one_or_list(values: list):
    distinct = sorted({repr(v): v for v in values}.values(), key=repr)
    return distinct[0] if len(distinct) == 1 else (distinct or None)


def _scope(run_dir: Path, vids: list, per_variant: dict) -> dict:
    import novelty as nv
    venues, products, proxies, funding, tfs, starts, ends, shas, symbols = ([] for _ in range(9))
    for vid in vids:
        path = run_dir / "artifacts" / "variants" / vid / "protocol.json"
        if not path.exists():
            continue
        p = _load(path) or {}
        venue = p.get("venue") if isinstance(p.get("venue"), dict) else {}
        venues.append(venue.get("venue") or p.get("exchange"))
        products.append(venue.get("product"))
        proxies.append(venue.get("price_proxy"))
        funding.append(venue.get("funding_modelled"))
        tfs.append(p.get("timeframe"))
        symbols += list(p.get("symbols") or [])
        windows = p.get("windows") or []
        for w in windows:
            test = w.get("test") if isinstance(w, dict) else None
            if isinstance(test, dict):
                if test.get("start") is not None:
                    starts.append(str(test["start"]))
                if test.get("end") is not None:
                    ends.append(str(test["end"]))
        if windows:
            sha = nv.windows_fingerprint(windows)
            per_variant[vid]["windows_sha256"] = sha
            shas.append(sha)
    if not tfs:
        return None
    one_sha = len(set(shas)) == 1
    return {"venue": _one_or_list(venues), "product": _one_or_list(products),
            "price_proxy": _one_or_list(proxies), "funding_modelled": _one_or_list(funding),
            "timeframe": _one_or_list(tfs), "symbols": sorted(set(symbols)),
            "period": {"start": min(starts) if starts else None,
                       "end": max(ends) if ends else None},
            "windows_sha256": shas[0] if one_sha else None,
            "windows_vary": (not one_sha) if shas else None}


# ---------------------------------------------------------------------------
# The finding
# ---------------------------------------------------------------------------

def build_finding(run_dir: Path, run_id: str, entry: dict, *, exempt: str | None = None) -> dict:
    """The run's finding, from its card, block manifest, claim_measurement.yaml,
    the variants' claim_test.yaml / protocol_result.yaml / protocol.json and
    the memory entry being written (its variants and trial ids). `exempt`:
    the orchestrator's _claim_check_exempt reason (no 1a-written claim).
    Raises on a malformed file; the caller records that as an error finding."""
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    card_path = arts / "hypothesis_card.yaml"
    card = (_load(card_path) or {}) if card_path.exists() else {}
    claim = card.get("claim") if isinstance(card, dict) else None
    kind_m = _manifest_kind(arts)
    tests = _tests_of(claim)
    card_hashes = {str(t["name"]): t["spec_hash"] for t in tests}
    rev_path = arts / "claim_revision.yaml"
    rev = (_load(rev_path) or {}) if rev_path.exists() else None
    finding = {
        "finding_id": f"F-{run_id}-1", "label": LABEL, "status": None, "reason": None,
        "information_only": True,
        "statement": claim.get("statement") if isinstance(claim, dict) else None,
        "kind": claim.get("kind") if isinstance(claim, dict) else None,
        "block_visibility": (cc.VISIBILITY_NOT_APPLICABLE if exempt
                             else cc.block_visibility(claim, kind_m)),
        "manifest_kind": kind_m,
        "claim_revision": rev.get("status") if isinstance(rev, dict) else None,
        "tests": tests,
    }
    # CUL-409 (review): a block idea whose claim has no test at all says so (a
    # blind claim already reads block_visibility: blind); only then, so every
    # other finding is unchanged.
    if not exempt and cc.block_test_gap(claim, kind_m) == cc.BLOCK_TEST_GAP_NO_TEST:
        finding["block_test_gap"] = cc.BLOCK_TEST_GAP_NO_TEST
    status_path = cmeas.run_file_path(arts)  # an older run: claim_status.yaml (D-077)
    status_doc = (_load(status_path) or {}) if status_path.exists() else None
    variants = entry.get("variants") if isinstance(entry.get("variants"), dict) else {}
    per_variant, refs = {}, {}
    rows = (status_doc or {}).get("variants") or {}
    run_reason = ((status_doc or {}).get("reason")
                  if (status_doc or {}).get("claim_status") != MEASURED else None)
    for vid in sorted(variants):
        rec, ref = _variant(run_dir, run_id, vid, variants[vid], rows.get(vid), card_hashes,
                            run_reason)
        per_variant[vid] = rec
        if ref:
            refs[vid] = ref
    bound = [v for v in sorted(per_variant) if per_variant[v]["status"] in (MEASURED, NO_EVENTS)]
    statuses = [per_variant[v]["status"] for v in bound]
    if status_doc is None:
        status, reason = NOT_MEASURED, CLAIM_STATUS_ABSENT
    elif MEASURED in statuses:
        status, reason = MEASURED, None
    elif statuses:
        status, reason = NO_EVENTS, cmeas.NO_EVENTS_REASON
    else:
        status = NOT_MEASURED
        reasons = sorted({str(r.get("reason")) for r in per_variant.values()})
        if reasons == [STALE]:
            reason = STALE          # the run file itself is not this attempt's
        elif status_doc.get("claim_status") != MEASURED and status_doc.get("reason"):
            reason = status_doc.get("reason")
        elif STALE in reasons:
            reason = STALE
        elif len(reasons) == 1:
            reason = reasons[0]
        else:                       # `error` is kept for a finding that could not be built
            reason = "mixed: " + ", ".join(reasons)
    tested = [v for v in sorted(variants) if variants[v].get("status") == "tested"]
    finding.update({
        "status": status, "reason": reason,
        "scope": _scope(run_dir, bound or tested, per_variant) if (bound or tested) else None,
        "result": {"per_variant": per_variant},
        "trial_ids": [per_variant[v]["trial_id"] for v in bound if per_variant[v]["trial_id"]],
        "source": {"run_id": run_id, "hypothesis_id": entry.get("hypothesis_id"),
                   "claim_status_ref": (_ref(run_id, f"artifacts/{status_path.name}")
                                        if status_doc is not None else None),
                   "claim_test_refs": refs},
    })
    # E-068 nearest build (operator 2026-10-05): a run that tested an approximation
    # says so FIRST. artifacts/deviations.yaml exists only under
    # orchestrator.nearest_build or for a side finding's start config (CUL-412),
    # so a finding without one is unchanged.
    block = nb.approximation_block(nb.load_record(arts))
    if block:
        finding = {"approximation": block, **finding}
    return finding


# ---------------------------------------------------------------------------
# The findings summary
# ---------------------------------------------------------------------------

def _summary_row(run_id: str, f: dict) -> dict:
    scope = f.get("scope") if isinstance(f.get("scope"), dict) else {}
    statement = f.get("statement")
    if isinstance(statement, str):
        statement = " ".join(statement.split())
        if len(statement) > STATEMENT_CHARS:
            statement = statement[:STATEMENT_CHARS - 3] + "..."
    per_variant = ((f.get("result") or {}).get("per_variant") or {})
    tests = []
    for t in f.get("tests") or []:
        name = str(t.get("name"))
        by_variant = {}
        for vid, rec in sorted(per_variant.items()):
            vt = (rec.get("tests") or {}).get(name)
            if not isinstance(vt, dict):
                continue
            row = {"status": vt.get("status")}
            hz = vt.get("horizons") or {}
            if hz:
                row["effect"] = {h: r.get("effect") for h, r in hz.items()}
                row["claimed_sign_windows"] = {
                    h: f"{r.get('windows_claimed_sign')}/{r.get('windows_with_value')}"
                    for h, r in hz.items()}
            by_variant[vid] = row
        tests.append({"name": name, "spec_hash": t.get("spec_hash"),
                      "statistic": t.get("statistic"), "direction": t.get("direction"),
                      "by_variant": by_variant})
    row = {"finding_id": f.get("finding_id"), "run_id": run_id, "kind": f.get("kind"),
           "status": f.get("status"), "reason": f.get("reason"),
           "block_visibility": f.get("block_visibility"), "statement": statement,
           "scope": {k: scope.get(k) for k in ("venue", "timeframe", "symbols", "period")},
           "tests": tests}
    approx = f.get("approximation")
    if isinstance(approx, dict):  # E-068 nearest build: only a finding that has one
        row = {"deviations": approx.get("n_deviations"), **row}
    return row


def _run_order(run_id: str) -> tuple:
    digits = len(run_id) - len(run_id.rstrip("0123456789"))
    if not digits:
        return (run_id, -1)
    return (run_id[:-digits], int(run_id[-digits:]))


def findings_summary(memory: dict, run_id: str, max_rows: int = SUMMARY_MAX_ROWS) -> dict:
    """artifacts/findings_summary.yaml: every finding in the memory, newest
    first (recorded_at, then run_id), capped at `max_rows` (counts cover all).
    `same_spec_hash`: a test spec measured in more than one run -- listed for
    information, never a ban. Deterministic: no clock."""
    entries = [(e.get("recorded_at") or "", rid, e[FINDING_KEY])
               for rid, e in (memory.get("runs") or {}).items()
               if isinstance(e, dict) and isinstance(e.get(FINDING_KEY), dict)]
    # ties on recorded_at: by the run's number (run_100 after run_99 after run_070)
    entries.sort(key=lambda x: (str(x[0]), _run_order(str(x[1]))), reverse=True)
    by_status, by_kind, spec_runs = {}, {}, {}
    for _, rid, f in entries:
        by_status[str(f.get("status"))] = by_status.get(str(f.get("status")), 0) + 1
        by_kind[str(f.get("kind"))] = by_kind.get(str(f.get("kind")), 0) + 1
        if f.get("status") == MEASURED:
            for t in f.get("tests") or []:
                if t.get("spec_hash"):
                    spec_runs.setdefault(t["spec_hash"], set()).add(rid)
    return {
        "schema_version": SUMMARY_SCHEMA_VERSION, "run_id": run_id, "label": LABEL,
        "note": NOTE, "information_only": True,
        "n_findings": len(entries), "n_listed": min(len(entries), max_rows),
        "by_status": dict(sorted(by_status.items())), "by_kind": dict(sorted(by_kind.items())),
        "findings": [_summary_row(rid, f) for _, rid, f in entries[:max_rows]],
        "same_spec_hash": [{"spec_hash": h, "run_ids": sorted(runs)}
                           for h, runs in sorted(spec_runs.items()) if len(runs) > 1],
    }
