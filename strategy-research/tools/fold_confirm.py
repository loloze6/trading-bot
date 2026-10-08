"""E-077 PR-2 (D-087): confirm a claim on the fold of the run built from it.

Under orchestrator.folds.enabled only (run_phase1_research wires it; nothing here
reads a flag). Design: engineering/delivery_plan_readers.md Amendment 1, Step 11 and
A1.11 (final Stage 1, items 2 and 3); engineering/roadmap/E-075/ITERATIVE_PLAN_JUDGEMENT.md
sections 1 (Q1 gaps a-c), 3 (the noise rule) and 4 (PR-2).

A claim is never confirmed inside the run that inspired it. A reader (later an
analyst) proposes a claim with a VEHICLE -- the strategy change its own run
backtests. If decide-next picks it, the CHILD run backtests the source run's config
with the vehicle applied, on the next fold its lineage has not used (PR-1, D-085).
After that backtest `confirm_on_fold` measures the claim's tests -- the SOURCE
proposal's tests, found by the child brief's `candidate.source.proposal_ref` and
identified by spec_hash -- on the child's saved bars over the child's fold, and
writes one row to campaign_record/confirmations.yaml.

How it finds things
-------------------
  source claim    research_brief.yaml candidate.source.proposal_ref
                  ("runs/<src>/artifacts/proposals/<category>.yaml#<proposal id>"), loaded
                  with reader_proposals.load_proposals; only a side finding is a claim
                  (a child built from a patch or a new block returns None: no claim).
  vehicle variant the child variant that carries the vehicle. decide-next gives the
                  child the source run's base config WITH the vehicle applied (step 1b
                  starts from it, candidate.start_config), so that is the child's own
                  `base` variant; callers may name another one.
  base variant    the child's base variant, recorded beside the vehicle variant. No
                  test slot compares one variant with another today (the baselines
                  `complement`, `placebo` and `other_selector` are all inside one
                  variant's bars), so it is passed to a custom `measure` hook and
                  recorded, and the default measurement does not need it.
  the fold        the fold in the child's pre_registration (research_folds); the
                  child's protocol windows must be exactly that fold's blocks.

The statuses
------------
  confirmed       THE NOISE RULE (below) holds for every test of the claim.
  not_confirmed   a test was measured and the rule fails: the claim is refuted on this
                  fold (kept as knowledge).
  not_measurable  no events, an unreadable source or bars, a vehicle variant that was not
                  backtested, or fewer than MIN_WINDOWS windows with a value (a fold of
                  SOL/UNI has almost no 2018-2021 bars). Kept as knowledge; the look is
                  counted when the selector was actually run.
  not_comparable  the child's card tests (spec_hash) are not the source claim's: the run
                  was not built for this claim (the spec-hash rule of explore_confirm's
                  resolve_pending, kept). Nothing is measured.

THE NOISE RULE -- a noise rule, NOT a size rule and NOT a cost rule
-------------------------------------------------------------------
For one test, at EVERY horizon that has a pooled value:
  (1) the pooled oriented effect is > 0 (the claimed sign holds), AND
  (2) the claimed sign (oriented > 0) holds in all but at most ONE window of the fold,
      counted among the windows with a value, of which there must be at least
      MIN_WINDOWS (else not_measurable).
A claim is confirmed only if every one of its tests (at most 3) is confirmed.
Why it exists: a claim with no effect points the right way by luck about half the time
(explore_confirm.test_sign needs only a positive pooled value), so "the sign held" would
put about half of all null claims into the registry as building blocks. With six
windows, under a symmetric null the chance that at least 5 of 6 share the claimed sign
is 7/64 = about 11% per fold, and 6 of 6 about 1.6%; a lineage confirmed on two folds is
near 1%. Windows of one fold share a market phase, so the true chance is somewhat higher,
and a "window" here is one symbol-window cell of claim_measure's per-window values, so
with several coins the rule is stricter than the single-coin figure. Every look is
counted in the ledger. It uses numbers every measurement already has
(claim_measure.measure_test: the pooled oriented value and the per-window values). The
EFFECT SIZE and the agreement count (k of n) are recorded for every horizon of every
claim; NO COST appears anywhere: whether an effect survives costs is judged where a
strategy is assembled, not here.

WHY THIS CANNOT LEAK (no lookahead): the measurement reads only the child run's own saved
bars.csv (claim_measure / claim_tests, unchanged), restricted to the fold's windows, and
refuses any bar at or after the holdout start. The fold's dates come from
config/folds.yaml, which research_folds validates against the data policy (research
period only; never the validation period or the holdout).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

CONFIRMED = "confirmed"
NOT_CONFIRMED = "not_confirmed"
NOT_MEASURABLE = "not_measurable"
NOT_COMPARABLE = "not_comparable"
STATUSES = (CONFIRMED, NOT_CONFIRMED, NOT_MEASURABLE, NOT_COMPARABLE)

BASIS_CHILD_RUN = "child_run"
ROW_ARTIFACT = "fold_confirmation.yaml"      # artifacts/ of the child run
SCHEMA_VERSION = 1

#: THE NOISE RULE's two numbers (see the module docstring).
MIN_WINDOWS = 4          # fewer windows with a value than this: not measurable
WINDOWS_ALLOWED_AGAINST = 1   # the claimed sign may fail in at most this many windows

RULE_NAME = "noise_rule"
RULE_TEXT = ("NOISE RULE, not a size rule and no cost comparison: confirmed when, at every horizon "
             "with a value, the pooled effect has the claimed sign AND the claimed sign holds in "
             f"all but at most {WINDOWS_ALLOWED_AGAINST} window(s) of the fold (at least "
             f"{MIN_WINDOWS} windows with a value, else not measurable). About an 11% chance per "
             "fold for a claim with no effect (6 windows), about 1% after two folds; every look is "
             "counted. Measured on the run built from the claim, on a fold its lineage had not used; "
             "not proven.")

_REF_RE = re.compile(r"runs/(?P<run>[^/]+)/artifacts/proposals/(?P<cat>[^/]+)\.yaml#(?P<pid>.+)")


# ---------------------------------------------------------------------------
# The rule, on one measure_test result
# ---------------------------------------------------------------------------

def grade_test(result: dict) -> dict:
    """{status, reason, horizons} of ONE claim_measure.measure_test result under the
    noise rule. `horizons`: per horizon with a pooled value, {effect, oriented, n_events,
    windows_claimed_sign (k), windows_with_value (n), per_window (oriented value per
    window), pooled_sign_held, windows_rule_held}. Pure."""
    import claim_measure as cmeas
    st = result.get("status")
    if st == cmeas.NO_EVENTS:
        return {"status": NOT_MEASURABLE,
                "reason": "no events: the selector matched no bar on the fold's windows"}
    if st != cmeas.MEASURED:
        why = result.get("detail") or result.get("reason")
        return {"status": NOT_MEASURABLE, "reason": f"not measured: {why}"}
    horizons = {}
    for h, r in sorted((result.get("horizons") or {}).items(), key=lambda kv: float(kv[0])):
        oriented = r.get("oriented")
        if oriented is None:
            continue
        per_window = {str(w): c.get("oriented") for w, c in (r.get("per_window") or {}).items()}
        vals = [v for v in per_window.values() if v is not None]
        k, n = sum(1 for v in vals if v > 0), len(vals)
        horizons[str(h)] = {"effect": r.get("value"), "oriented": oriented,
                            "n_events": r.get("n_events"),
                            "windows_claimed_sign": k, "windows_with_value": n,
                            "per_window": per_window,
                            "pooled_sign_held": oriented > 0,
                            "windows_rule_held": n >= MIN_WINDOWS and k >= n - WINDOWS_ALLOWED_AGAINST}
    if not horizons:
        return {"status": NOT_MEASURABLE, "reason": "no horizon has a pooled value on the fold",
                "horizons": horizons}
    short = {h: x["windows_with_value"] for h, x in horizons.items()
             if x["windows_with_value"] < MIN_WINDOWS}
    if short:
        return {"status": NOT_MEASURABLE, "horizons": horizons,
                "reason": (f"fewer than {MIN_WINDOWS} windows with a value at horizon(s) "
                           f"{short} (windows with a value) -- the fold cannot grade this test")}
    bad = [f"h={h}: pooled {'held' if x['pooled_sign_held'] else 'NOT held'}, windows "
           f"{x['windows_claimed_sign']} of {x['windows_with_value']}"
           for h, x in horizons.items() if not (x["pooled_sign_held"] and x["windows_rule_held"])]
    if bad:
        return {"status": NOT_CONFIRMED, "horizons": horizons,
                "reason": "the noise rule fails: " + "; ".join(bad)}
    return {"status": CONFIRMED, "horizons": horizons,
            "reason": ("the pooled sign held at every horizon and the claimed sign held in all but "
                       "at most one window: " + "; ".join(
                           f"h={h} {x['windows_claimed_sign']} of {x['windows_with_value']}"
                           for h, x in horizons.items()))}


def combine(graded: dict) -> tuple:
    """(status, reason) of a claim from {test name: grade_test(...)}. Confirmed only if
    EVERY test is (claim_tests.combine, D-014); not_confirmed as soon as one measured
    test fails the rule, whatever the others say; else not_measurable."""
    if not graded:
        return NOT_MEASURABLE, "the claim has no test to measure"
    statuses = {n: g["status"] for n, g in graded.items()}
    if all(s == CONFIRMED for s in statuses.values()):
        return CONFIRMED, "every test of the claim passed the noise rule"
    failed = sorted(n for n, s in statuses.items() if s == NOT_CONFIRMED)
    if failed:
        return NOT_CONFIRMED, "; ".join(f"{n}: {graded[n]['reason']}" for n in failed)
    return NOT_MEASURABLE, "; ".join(f"{n}: {graded[n]['reason']}" for n, s in sorted(statuses.items())
                                     if s != CONFIRMED)


# ---------------------------------------------------------------------------
# The source claim
# ---------------------------------------------------------------------------

def source_ref(arts: Path):
    """(source run, category, proposal id) from the brief's candidate.source.proposal_ref,
    or None when the run was not built from a reader proposal."""
    path = Path(arts) / "research_brief.yaml"
    if not path.exists():
        return None
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    ref = (((doc.get("candidate") or {}).get("source") or {}).get("proposal_ref")
           if isinstance(doc, dict) else None)
    m = _REF_RE.fullmatch(ref.replace("\\", "/")) if isinstance(ref, str) else None
    return (m.group("run"), m.group("cat"), m.group("pid")) if m else None


def source_item(root: Path, ref: tuple):
    """The flattened reader proposal the ref names (reader_proposals.load_proposals), or None
    when the file has no such proposal. Raises ProposalError / OSError when unreadable."""
    import reader_proposals as rp
    run, _cat, pid = ref
    items = rp.load_proposals(Path(root) / "runs" / run / "artifacts" / "proposals",
                              list(rp.READER_RUBRIC_VERSIONS))
    for cat_items in items.values():
        for item in cat_items:
            if item.get("proposal_id") == pid:
                return item
    return None


def _spec_hashes(res) -> list:
    return sorted(t["spec_hash"] for t in res.tests if t.get("spec_hash"))


# ---------------------------------------------------------------------------
# confirm_on_fold
# ---------------------------------------------------------------------------

def _row_base(child: str, ref: tuple, item: dict | None, fold: str | None) -> dict:
    claim = (item or {}).get("claim") or {}
    row = {"schema_version": SCHEMA_VERSION, "finding_id": ref[2], "category": ref[1],
           "source_run": ref[0], "run_id": child, "basis": BASIS_CHILD_RUN, "fold": fold,
           "kind": claim.get("kind"), "statement": claim.get("statement"),
           "rule": {"name": RULE_NAME, "min_windows": MIN_WINDOWS,
                    "windows_allowed_against": WINDOWS_ALLOWED_AGAINST, "text": RULE_TEXT}}
    for key in ("vehicle", "combines_as", "fold_observed"):
        if item and key in item:
            row[key] = item[key]
    return row


def _finish(row: dict, status: str, reason: str, **extra) -> dict:
    row.update({"status": status, "reason": reason, **extra})
    return row


def confirm_on_fold(run_dir: Path, run_id: str, *, root: Path, folds_doc: dict | None = None,
                    eras, holdout_start: str, vehicle_variant: str | None = None,
                    base_variant: str | None = None, fresh_variants=None,
                    measure=None, folds_path=None, policy_path=None):
    """Measure the source claim's tests on the child run `run_id`'s vehicle variant over
    its fold, and return the ledger row (explore_confirm.record_fold_confirmation writes
    it). None when the run was not built from a side finding (nothing to confirm). Never
    raises for a content problem: it is a row with a status and a reason.

    `fresh_variants`: the variants backtested in THIS attempt (None: every graded one).
    `measure(run_dir, variant, tests, window_labels, eras, holdout_start) ->
    ({test name: measure_test-shaped result}, [windows measured])`: the generic measurement
    (explore_confirm.measure_on_windows); a trade-level test family plugs in here later by
    returning results of the same shape, and may take the base variant as a keyword."""
    import claim_card as cc
    import claim_tests as ct
    import explore_confirm as ec
    import json_pointer as jp
    import reader_proposals as rp
    import research_folds as rf
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    ref = source_ref(arts)
    if ref is None:
        return None
    try:
        item = source_item(root, ref)
    except Exception as exc:  # noqa: BLE001 -- a row, not a crash
        return _finish(_row_base(run_id, ref, None, None), NOT_MEASURABLE,
                       f"the source proposal cannot be read ({type(exc).__name__}: {exc})")
    if item is None:
        return _finish(_row_base(run_id, ref, None, None), NOT_MEASURABLE,
                       f"the proposal_ref names {ref[2]!r}, which is not in the source run's "
                       f"proposals")
    if item.get("kind") != rp.SIDE_FINDING:
        return None                      # a patch or a new block: no claim to confirm
    try:
        fold = rf.fold_of_run_dir(run_dir)
    except rf.FoldsError as exc:
        fold = None
        fold_error = str(exc)
    else:
        fold_error = None
    row = _row_base(run_id, ref, item, fold)
    if fold is None:
        return _finish(row, NOT_MEASURABLE,
                       fold_error or "this run carries no fold in its pre_registration "
                       "(machine_constraints.protocol.fold): it was not placed on a fold, so "
                       "nothing is measured")
    # the source claim and its tests
    claim = item.get("claim")
    res = cc.check_claim(claim)
    if res.errors:
        return _finish(row, NOT_MEASURABLE, "the source claim is refused by check_claim: "
                       + "; ".join(res.errors))
    if res.tests_none:
        return _finish(row, NOT_MEASURABLE,
                       f"tests: none (missing block {res.missing_block!r}): a trade-level or other "
                       f"test family the slots cannot express yet; recorded as knowledge")
    source_hashes = _spec_hashes(res)
    row["spec_hashes"] = source_hashes
    names = {t["name"] for t in res.tests}
    tests = [t for t in claim["tests"] if isinstance(t, dict) and t.get("name") in names]
    # the spec-hash rule (explore_confirm.resolve_pending, kept): the child's own card must
    # carry the same tests, else it was not built for this claim
    card_path = arts / "hypothesis_card.yaml"
    try:
        card = yaml.safe_load(card_path.read_text(encoding="utf-8")) if card_path.exists() else None
        own = cc.check_claim((card or {}).get("claim") if isinstance(card, dict) else None,
                             cc.card_criteria_ids(card if isinstance(card, dict) else {}))
        own_hashes = [] if own.errors else _spec_hashes(own)
    except Exception as exc:  # noqa: BLE001 -- recorded
        own_hashes = []
        row["own_card_error"] = f"{type(exc).__name__}: {exc}"
    if set(own_hashes) != set(source_hashes):
        return _finish(row, NOT_COMPARABLE,
                       "not comparable: the run built from this claim carries other tests "
                       "(spec_hash differs from the claim's, or its card has none); nothing is "
                       "measured",
                       own_spec_hashes=own_hashes)
    # the fold and the child's protocol must agree
    try:
        doc = folds_doc if folds_doc is not None else rf.load_folds(folds_path, policy_path=policy_path)
        blocks = doc["folds"][fold]
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE, f"config/folds.yaml cannot be used ({type(exc).__name__}: {exc})")
    block_rows = [dict(b) for b in blocks]
    row["fold_blocks"] = [b["label"] for b in block_rows]
    row["confirmation_set"] = ec.set_key(block_rows)
    try:
        proto = {w["label"]: (w["start"], w["end"]) for w in ec.protocol_windows(arts)}
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE,
                       f"the run's protocol windows cannot be read ({type(exc).__name__}: {exc})")
    want = {b["label"]: (b["start"], b["end"]) for b in block_rows}
    if proto != want:
        return _finish(row, NOT_MEASURABLE,
                       f"the run's protocol windows {sorted(proto.items())} are not exactly fold "
                       f"{fold}'s blocks {sorted(want.items())}: the claim is not measured on a "
                       f"fold it was not run on")
    # the variants
    try:
        graded = ct.graded_variants(run_dir)[0]
        base = base_variant or jp.base_variant_id(graded)
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE, f"no graded variant ({type(exc).__name__}: {exc})")
    vehicle_vid = vehicle_variant or base
    row.update({"vehicle_variant": vehicle_vid, "base_variant": base})
    usable = set(graded if fresh_variants is None else fresh_variants) & set(graded)
    if vehicle_vid not in usable:
        return _finish(row, NOT_MEASURABLE,
                       f"the vehicle variant {vehicle_vid!r} was not backtested in this attempt "
                       f"(graded now: {sorted(usable)})")
    # the generic measurement, over the fold's windows only
    measure = measure or ec.measure_on_windows
    try:
        results, measured = measure(run_dir, vehicle_vid, tests, [b["label"] for b in block_rows],
                                    eras, holdout_start)
    except Exception as exc:  # noqa: BLE001 -- recorded
        return _finish(row, NOT_MEASURABLE,
                       f"the bars could not be measured ({type(exc).__name__}: {exc})")
    graded_tests = {n: grade_test(r) for n, r in sorted(results.items())}
    status, reason = combine(graded_tests)
    row["tests"] = {n: {"spec_hash": results[n].get("spec_hash"), **g}
                    for n, g in graded_tests.items()}
    row["windows_measured"] = list(measured)
    # the numbers every row carries, for any status that measured something
    row["effect"] = {n: {h: x["effect"] for h, x in g.get("horizons", {}).items()}
                     for n, g in graded_tests.items() if g.get("horizons")}
    row["agreement"] = {n: {h: f"{x['windows_claimed_sign']} of {x['windows_with_value']}"
                            for h, x in g.get("horizons", {}).items()}
                        for n, g in graded_tests.items() if g.get("horizons")}
    row["_comparisons"] = ec.comparisons_of(results)
    return _finish(row, status, reason)
