"""E-072: ideas are confirmed on data the proposer never saw.

Under orchestrator.explore_confirm.enabled only (run_phase1_research wires it;
nothing here reads a flag). Design: engineering/roadmap/E-072/PHASE_A.md.

  * The split, pre-registered before the backtests (artifacts/explore_confirm.yaml):
    the run's protocol windows in time order, first half = EXPLORATION, second
    half = CONFIRMATION (rule `chronological_half`; an odd count gives the extra
    window to confirmation). It never changes inside a run.
  * The readers see exploration windows only. Code writes their copies under
    artifacts/exploration/: the category reports (build_reports only_windows),
    the grid re-reduced on those windows (exploration_grid: window-source
    criteria only; every pooled criterion and the idea status are withheld),
    the claim digest measured on those windows (exploration_digest), and the
    earlier findings and registry summary with their numbers withheld.
  * After the readers, each side finding is measured on the confirmation
    windows (confirm_findings): a price-only ("pure") finding in the same run,
    with claim_measure.measure_test on that run's base variant bars; a block
    claim (kind forecast/regime), or a pure finding whose config change alters
    the forecast/regime its tests read, is `pending` until the run built from
    it measures its own claim on its own confirmation windows
    (resolve_pending). The result is `confirmation_sign_retained: true | false
    | pending` (null only when nothing could be measured: no usable test, or an
    error -- never a guessed sign).
  * Every confirmation look is counted in campaign_record/confirmations.yaml,
    per confirmation set: n_looks (tests) and n_comparisons (test x horizon).
    The honest bar is "the sign held on unseen windows, counted against the
    looks" -- never "proven".

  * A resolution by the follow-up run is WEAK and recorded so
    (confirmation_basis: follow_up_run, proposer_exposure, weak: true;
    not_comparable when its tests differ): step 1a wrote that run's card after
    reading the all-window knowledge base. The summary counts it apart.

  * E-077 PR-2 (D-087), orchestrator.folds.enabled: the in-run route above and the weak
    follow-up resolution are UNREACHABLE (finding_route(folds=True) has no in_run route;
    run_phase1_research._record_confirmations never calls pending_for / resolve_pending).
    tools/fold_confirm.confirm_on_fold measures the claim on the fold of the run built
    from it, and record_fold_confirmation writes that row under `fold_confirmations`
    in the same ledger, with the same lock and look counting.

INFORMATION ONLY: a confirmation never changes idea_status or the grid, never
routes, stops, parks or ranks anything; and no failure here stops a run (fewer
than 2 windows: `not_applicable`, the run proceeds as flag-off; a missing
readers' copy: the reader is skipped by rule exploration_inputs_unavailable).
"Never saw" means never saw in this pipeline: the confirmation windows are
within the reader model's training period.

WHY THIS CANNOT LEAK (no lookahead): it reads only a completed run's own saved
bars.csv (claim_tests.load_variant_bars; the holdout start is refused by
claim_measure.check_before_holdout) and never a data cache.
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
import uuid
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

SPLIT_ARTIFACT = "explore_confirm.yaml"        # artifacts/, before the backtests
EXPLORATION_DIR = "exploration"                # artifacts/exploration/: the readers' copies
CONFIRMATION_ARTIFACT = "confirmation.yaml"    # artifacts/, after the readers
LEDGER_REL = "campaign_record/confirmations.yaml"
SCHEMA_VERSION = 1
RULE = "chronological_half"
WITHHELD = "withheld"
WITHHELD_REASON = ("withheld under explore_confirm: computed over every window, including the "
                   "confirmation windows the readers do not see")
EARLIER_WITHHELD_REASON = ("withheld under explore_confirm: earlier runs' numbers may come from "
                           "this run's confirmation windows")
HONEST_BAR = ("the sign held (or not) on windows the proposer never saw, counted against the "
              "looks taken on that confirmation set; not proven")
READER_NOTE = ("exploration windows only: every number in this file comes from the windows "
               "listed in windows_shown; the confirmation windows and every aggregate over them "
               "are withheld on purpose")

# routes and statuses of one side finding
IN_RUN = "in_run"
PENDING = "pending"
NOT_MEASURABLE = "not_measurable"
MEASURED = "measured"
ERROR = "error"

LEDGER_NOTE = ("information only: each reader side finding measured on confirmation windows "
               "the proposer never saw; looks counted per confirmation set; not proven")

# the split could not be made (fewer than 2 windows): recorded, and the run
# proceeds as if the flag were off (PR #340 review, finding 2)
NOT_APPLICABLE = "not_applicable"
NOT_APPLICABLE_EFFECT = ("this run proceeds as if orchestrator.explore_confirm were off: the "
                         "readers read the all-window inputs and no side finding is confirmed")

# how a finding's confirmation was obtained (PR #340 review, finding 1)
BASIS_IN_RUN = "in_run"              # this run's readers, who saw the exploration copies only
BASIS_FOLLOW_UP = "follow_up_run"    # the run built from the finding: its card is step 1a's
PROPOSER_EXPOSURE_1A = "step_1a_saw_all_window_knowledge_base"
NOT_COMPARABLE = "not_comparable"    # the follow-up run tested other tests than the finding's
WEAK_BAR = ("WEAK: measured by the run built from this finding, whose card step 1a wrote after "
            "reading campaign_knowledge_base.yaml (every window, these confirmation windows "
            "included) -- so not on windows the proposer pipeline never saw; counted against the "
            "looks taken on that confirmation set; not proven")
# the fields a follow-up resolution overwrites, kept so a re-run of that
# follow-up run can measure it again (finding 6)
_PENDING_STATE_KEYS = ("status", "confirmation_sign_retained", "reason", "confirmation_set", "bar")
_RESOLUTION_KEYS = ("variant", "windows_measured", "tests", "measured_in_run", "looks",
                    "tests_changed_from_finding", "confirmation_basis", "proposer_exposure",
                    "weak", "sign_of_own_tests", "_comparisons")

# The readers' copy of hypothesis_card.yaml (finding 3): a WHITELIST -- the
# claim's statement, kind and tests, and the signal / component spec. Free
# text that may quote earlier all-window numbers (thesis, rationale,
# edge_source, assumptions, failure modes, pass_if/fail_if/rationale of the
# claim) and numeric evidence (power_parameters, library_lookup,
# cost_feasibility) are left out. The free text kept is masked (below).
READER_CARD_KEYS = ("hypothesis_id", "signal_concept", "target_market", "timeframe",
                    "composition", "config", "manifest", "criteria")
READER_CLAIM_KEYS = ("statement", "kind", "tests", "criteria_refs", "missing_block")

# Operator decision 14 (PR #340 review round 2, finding 1): ONE rule for
# every free-text field an AI step wrote that reaches a reader -- its number
# literals (ints, decimals, signed, thousands, percentages, scientific) are
# replaced by NUMBER_MASK, the words kept (run_074's card: "median
# forecast_return_corr=-0.0057", an all-window number, in claim.statement).
# READER_FREE_TEXT lists those fields per readers' copy (artifacts/exploration/
# <name>), as key paths ("*" = every list item); mask_free_text is the one
# function that applies it, called by every builder of such a copy. Never
# masked: the mechanical test specs, component params, the config, window
# labels, ids -- the parameters stay readable there. The other readers'
# copies (the category reports, the grid and the block-registry summary) are
# code-written from results: no AI free text.
NUMBER_MASK = "<n>"
_NUMBER_RE = re.compile(
    r"(?<![\w.])[-+\u2212\u00b1]?"
    r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+)"
    r"(?:[eE][-+\u2212]?\d+)?%?")
_DEVIATION_TEXT = ("clause", "built_instead", "missing", "effect")
READER_FREE_TEXT = {
    # step 1a (or 1b's pass-through manifest)
    "hypothesis_card.yaml": (("signal_concept",), ("target_market",), ("claim", "statement"),
                             ("manifest", "rationale")),
    # step 1b's block manifest
    "block_manifest.yaml": (("rationale",),),
    # the claim statement (1a) and the approximation (1b's deviations)
    "claim_result_digest.yaml": (("statement",), ("approximation", "line"),
                                 *(("approximation", "deviations", "*", k)
                                   for k in _DEVIATION_TEXT)),
    # earlier runs' claim statements (their 1a)
    "findings_summary_for_readers.yaml": (("findings", "*", "statement"),),
}


def mask_numbers(value):
    """`value` with every number literal replaced by NUMBER_MASK: a string
    keeps its words; a number (not a bool) becomes NUMBER_MASK; lists and
    mappings are masked item by item; anything else is returned as is."""
    if isinstance(value, str):
        return _NUMBER_RE.sub(NUMBER_MASK, value)
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return NUMBER_MASK
    if isinstance(value, list):
        return [mask_numbers(v) for v in value]
    if isinstance(value, dict):
        return {k: mask_numbers(v) for k, v in value.items()}
    return value


def _mask_at(node, path: tuple):
    if not path:
        return mask_numbers(node)
    head, rest = path[0], path[1:]
    if head == "*":
        return [_mask_at(x, rest) for x in node] if isinstance(node, list) else node
    if isinstance(node, dict) and head in node:
        node[head] = _mask_at(node[head], rest)
    return node


def mask_free_text(doc, name: str):
    """`doc` (a readers' copy named `name`, changed in place and returned) with
    every READER_FREE_TEXT[name] field passed through mask_numbers."""
    for path in READER_FREE_TEXT[name]:
        doc = _mask_at(doc, path)
    return doc


class SplitError(ValueError):
    """The run's windows cannot be split, or the pre-registered split no longer fits."""


def _load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# The split
# ---------------------------------------------------------------------------

def _protocol_files(arts: Path) -> list:
    vroot = Path(arts) / "variants"
    files = []
    if (vroot / "run_protocol.json").exists():
        files.append(vroot / "run_protocol.json")
    if vroot.is_dir():
        files += sorted(vroot.glob("*/protocol.json"))
    return files


def protocol_windows(arts: Path, extra_files=()) -> list:
    """[{label, start, end}] -- every window named by the run's protocol files
    (`extra_files`, e.g. the resolved run protocol, then
    artifacts/variants/run_protocol.json and artifacts/variants/<vid>/
    protocol.json), one row per label, in time order (start, then label).
    Raises SplitError when there is no protocol file, or when one label has
    two different date ranges."""
    files = [Path(p) for p in extra_files if p is not None and Path(p).exists()]
    files += [p for p in _protocol_files(arts) if p not in files]
    if not files:
        raise SplitError(f"no protocol file under {Path(arts) / 'variants'} -- the windows "
                         f"cannot be split before the backtests")
    by_label = {}
    for path in files:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        for w in (doc or {}).get("windows") or []:
            if not isinstance(w, dict) or not w.get("label"):
                continue
            test = w.get("test") if isinstance(w.get("test"), dict) else {}
            row = {"label": str(w["label"]), "start": str(test.get("start") or ""),
                   "end": str(test.get("end") or "")}
            old = by_label.get(row["label"])
            if old is not None and old != row:
                raise SplitError(f"window {row['label']!r} has two date ranges "
                                 f"({old['start']}..{old['end']} and {row['start']}..{row['end']})")
            by_label[row["label"]] = row
    return sorted(by_label.values(), key=lambda r: (r["start"], r["label"]))


def split_windows(windows: list) -> dict:
    """The pre-registered split of `windows` (protocol_windows' rows): the first
    half in time order is exploration, the rest confirmation. At least two
    windows, else SplitError."""
    if len(windows) < 2:
        raise SplitError(f"{len(windows)} window(s): at least 2 are needed to keep one "
                         f"confirmation window the readers never see")
    k = len(windows) // 2
    return {"rule": RULE, "exploration": [dict(w) for w in windows[:k]],
            "confirmation": [dict(w) for w in windows[k:]]}


def labels(rows: list) -> list:
    return [r["label"] for r in rows]


def ensure_split(arts: Path, run_id: str, extra_files=()) -> dict:
    """artifacts/explore_confirm.yaml, written once per run BEFORE the
    backtests; on a re-run the file on disk is kept (it was pre-registered
    first). Fewer than 2 windows: the file records `status: not_applicable`
    with the reason, and the run proceeds as if the flag were off (it is
    kept on a re-run too). Raises SplitError when it cannot be written, or
    when a window of the current protocol is in neither half of the file on
    disk."""
    import campaign_memory as cm
    arts = Path(arts)
    path = arts / SPLIT_ARTIFACT
    if split_not_applicable(arts):
        return _load_yaml(path)
    windows = protocol_windows(arts, extra_files)
    if not path.exists() and len(windows) < 2:
        doc = {"schema_version": SCHEMA_VERSION, "run_id": run_id, "status": NOT_APPLICABLE,
               "rule": RULE, "windows": [dict(w) for w in windows],
               "reason": (f"{len(windows)} window(s): at least 2 are needed to keep one "
                          f"confirmation window the readers never see"),
               "effect": NOT_APPLICABLE_EFFECT}
        cm._atomic_write(path, doc)
        return doc
    if path.exists():
        doc = load_split(arts)
        known = set(labels(doc["exploration"])) | set(labels(doc["confirmation"]))
        new = [w["label"] for w in windows if w["label"] not in known]
        if new:
            raise SplitError(f"{path}: windows {new} are in neither half of the pre-registered "
                             f"split -- the protocol changed after the split was written")
        return doc
    doc = {"schema_version": SCHEMA_VERSION, "run_id": run_id, **split_windows(windows),
           "note": ("pre-registered before the backtests: the readers see the exploration "
                    "windows only; their side findings are measured on the confirmation "
                    "windows")}
    cm._atomic_write(path, doc)
    return doc


def split_not_applicable(arts: Path) -> bool:
    """True when the run's split file records `status: not_applicable` (fewer
    than 2 windows): the run then proceeds as if the flag were off. False when
    the file is absent or unreadable -- the readers are then skipped by rule
    (never given the all-window files)."""
    path = Path(arts) / SPLIT_ARTIFACT
    try:
        doc = _load_yaml(path) if path.exists() else None
    except (OSError, ValueError, yaml.YAMLError):
        return False
    return isinstance(doc, dict) and doc.get("status") == NOT_APPLICABLE


def load_split(arts: Path) -> dict:
    """The run's split, checked. Raises SplitError when absent, not
    applicable or malformed -- a reader input is never built from a guessed
    split."""
    path = Path(arts) / SPLIT_ARTIFACT
    if not path.exists():
        raise SplitError(f"{path} is missing -- it is written at protocol_execution entry")
    doc = _load_yaml(path)
    if isinstance(doc, dict) and doc.get("status") == NOT_APPLICABLE:
        raise SplitError(f"{path}: not applicable ({doc.get('reason')})")
    ok = isinstance(doc, dict) and all(
        isinstance(doc.get(k), list) and doc[k]
        and all(isinstance(r, dict) and r.get("label") for r in doc[k])
        for k in ("exploration", "confirmation"))
    if not ok:
        raise SplitError(f"{path}: needs non-empty exploration and confirmation window lists")
    if set(labels(doc["exploration"])) & set(labels(doc["confirmation"])):
        raise SplitError(f"{path}: a window is in both halves")
    return doc


def set_key(rows: list) -> str:
    """The confirmation set a look spends: its windows and date ranges."""
    return ",".join(f"{r['label']}[{r.get('start')}..{r.get('end')}]"
                    for r in sorted(rows, key=lambda r: (str(r.get("start")), r["label"])))


def _overlap(a: list, b: list) -> list:
    """Window pairs whose date ranges overlap (ISO dates compare as strings);
    a row without dates overlaps a row with the same label."""
    out = []
    for x in a:
        for y in b:
            if x.get("start") and x.get("end") and y.get("start") and y.get("end"):
                hit = x["start"] <= y["end"] and y["start"] <= x["end"]
            else:
                hit = x["label"] == y["label"]
            if hit:
                out.append(f"{y['label']} overlaps {x['label']}")
    return out


# ---------------------------------------------------------------------------
# The readers' copies (exploration windows only)
# ---------------------------------------------------------------------------

def restrict_protocol_result(pr: dict, windows) -> dict:
    """Only the `results` entries of the given windows; every other key of a
    protocol_result is an aggregate over all windows and is dropped."""
    keep = set(windows)
    return {"results": [r for r in (pr or {}).get("results") or []
                        if isinstance(r, dict) and r.get("window") in keep]}


def exploration_grid(grid_doc: dict, pr_by_variant: dict, pre_registration: dict, menu,
                     windows, *, single_era_inconclusive: bool = False,
                     composition_runs: bool = False,
                     zero_trade_windows_not_computed: bool = False) -> dict:
    """The grid as the readers see it: every criterion x graded variant of
    `grid_doc` (the run's grid_evaluation.yaml); a `window`-source criterion
    re-evaluated by the grid's own cell function on the exploration windows'
    results only, with the keywords the run's own grid call passed
    (`composition_runs`, `single_era_inconclusive`,
    `zero_trade_windows_not_computed` -- CUL-415, the key only when set); any other source
    (pooled, profit bars) WITHHELD, as is the idea status (both read every
    window). Failed/untested/partial variants' reasons are copied (they are
    not results)."""
    import verdict_criteria_evaluator as vce
    shown = sorted(set(windows))
    defs = {c.get("id"): c for c in vce._resolve_grid_criteria(pre_registration or {}, menu)}
    eras = vce._load_campaign_data_policy_eras()
    kw = {"composition_runs": bool(composition_runs),
          **({"single_era_inconclusive": True} if single_era_inconclusive else {}),
          **({"zero_trade_windows_not_computed": True} if zero_trade_windows_not_computed else {})}
    grid = {}
    for cid in grid_doc.get("criteria") or []:
        crit = defs.get(cid)
        row = {}
        for vid in grid_doc.get("variants") or []:
            if crit is None or crit.get("source") != "window":
                row[vid] = {"result": WITHHELD, "reason": WITHHELD_REASON}
            elif vid not in pr_by_variant:
                row[vid] = {"result": WITHHELD, "reason": "no protocol_result for this variant"}
            else:
                row[vid] = vce._evaluate_grid_cell(
                    crit, restrict_protocol_result(pr_by_variant[vid], shown), eras, **kw)
        grid[cid] = row
    out = {"windows_shown": shown, "note": READER_NOTE,
           "criteria": list(grid_doc.get("criteria") or []),
           "variants": list(grid_doc.get("variants") or []), "grid": grid,
           "idea_status": WITHHELD, "idea_status_reason": WITHHELD_REASON}
    for key in ("failed_variants", "untested_variants", "partial_coverage_variants"):
        if grid_doc.get(key):
            out[key] = copy.deepcopy(grid_doc[key])
    return out


def measure_on_windows(run_dir: Path, vid: str, tests: list, windows, eras,
                       holdout_start: str) -> tuple:
    """({test name: claim_measure.measure_test result}, [window labels measured])
    on one variant's saved bars, restricted to `windows`. Raises when the bars
    cannot be read, a bar reaches the holdout start, or no bar is in `windows`."""
    import claim_measure as cmeas
    import claim_tests as ct
    keep = set(windows)
    ws = [w for w in ct.load_variant_bars(Path(run_dir), vid) if w.window in keep]
    if not ws:
        raise ValueError(f"variant {vid!r} has no bars on the windows {sorted(keep)}")
    cmeas.check_before_holdout(ws, holdout_start)
    out = {}
    for t in tests:
        name = str(t.get("name")) if isinstance(t, dict) else "None"
        try:
            out[name] = cmeas.measure_test(ws, t, eras)
        except Exception as exc:  # noqa: BLE001 -- recorded per test
            out[name] = {"name": name, "status": cmeas.NOT_MEASURED, "reason": ERROR,
                         "detail": f"{type(exc).__name__}: {exc}"}
    return out, [w.label for w in ws]


def exploration_digest(run_dir: Path, windows, eras, holdout_start: str) -> dict:
    """artifacts/exploration/claim_result_digest.yaml: the claim digest's
    descriptive part (statement, tests, variant patches, approximation) from
    reader_findings.claim_result_digest -- its AI free text (statement,
    approximation) with numbers masked (mask_free_text) -- and per variant its numbers MEASURED
    AGAIN on the exploration windows only -- for each variant the run-level
    measurement lists as measured in this attempt (the others keep their
    reason, without numbers). Never raises: a failure is `status: error`."""
    import claim_card as cc
    import claim_findings as cf
    import claim_measure as cmeas
    import reader_findings as rf
    run_dir = Path(run_dir)
    shown = sorted(set(windows))
    base = rf.claim_result_digest(run_dir)
    out = mask_free_text({k: v for k, v in base.items()
                          if k not in ("variants", "claim_status", "reason")},
                         "claim_result_digest.yaml")
    out.update({"windows_shown": shown, "windows_note": READER_NOTE})
    if base.get("status") == "error":
        return out
    try:
        arts = run_dir / "artifacts"
        status_path = cmeas.run_file_path(arts)
        if not status_path.exists():
            out.update({"claim_status": "absent", "variants": {}})
            return out
        sdoc = _load_yaml(status_path) or {}
        card = _load_yaml(arts / "hypothesis_card.yaml") or {}
        claim = card.get("claim") if isinstance(card, dict) else None
        res = cc.check_claim(claim, cc.card_criteria_ids(card if isinstance(card, dict) else {}))
        names = {t["name"] for t in res.tests}
        tests = [t for t in (claim or {}).get("tests") or []
                 if isinstance(t, dict) and t.get("name") in names] \
            if isinstance(claim, dict) and isinstance(claim.get("tests"), list) else []
        stats = {str(t["name"]): t.get("statistic") for t in tests}
        variants = {}
        for vid, row in sorted((sdoc.get("variants") or {}).items()):
            vid = str(vid)
            if not isinstance(row, dict) or not row.get("file") or not tests \
                    or row.get("status") not in (cmeas.MEASURED, cmeas.NO_EVENTS):
                variants[vid] = {"status": cmeas.NOT_MEASURED,
                                 "reason": (row or {}).get("reason") if isinstance(row, dict)
                                 else "not in the run's measurement"}
                continue
            try:
                results, _measured = measure_on_windows(run_dir, vid, tests, shown, eras,
                                                        holdout_start)
            except Exception as exc:  # noqa: BLE001 -- recorded
                variants[vid] = {"status": cmeas.NOT_MEASURED, "reason": ERROR,
                                 "detail": f"{type(exc).__name__}: {exc}"}
                continue
            compact = {}
            for n, t in results.items():
                compact[n] = cf._compact_test(t)
                if n in stats:
                    compact[n]["statistic_label"] = rf.statistic_label(stats[n])
            st = [t.get("status") for t in results.values()]
            status = (cmeas.MEASURED if cmeas.MEASURED in st
                      else cmeas.NO_EVENTS if st and all(s == cmeas.NO_EVENTS for s in st)
                      else cmeas.NOT_MEASURED)
            variants[vid] = {"status": status, "tests": compact}
        measured = any(v["status"] == cmeas.MEASURED for v in variants.values())
        out.update({"claim_status": cmeas.MEASURED if measured else cmeas.NOT_MEASURED,
                    "reason": None if measured else "nothing measured on the exploration windows",
                    "variants": variants})
    except Exception as exc:  # noqa: BLE001 -- information only
        out.update({"status": "error", "detail": f"{type(exc).__name__}: {exc}"})
        out.pop("variants", None)
    return out


def withhold_findings_numbers(summary: dict) -> dict:
    """findings_summary_for_readers with every earlier effect withheld: what
    was tested (ids, kind, spec, selector, outcome, status, spec_hash) stays,
    so a reader still does not repeat a test; how it came out does not: the
    code-written `reason` (a result) is dropped, and the claim `statement`
    (1a's free text) has its numbers masked like every AI free text a reader
    gets (mask_free_text, operator decision 14)."""
    out = copy.deepcopy(summary)
    for row in out.get("findings") or []:
        if isinstance(row, dict):
            row.pop("reason", None)
        for t in row.get("tests") or [] if isinstance(row, dict) else []:
            for v in (t.get("by_variant") or {}).values() if isinstance(t, dict) else []:
                if isinstance(v, dict) and "largest_effect" in v:
                    v["largest_effect"] = WITHHELD
    out["numbers"] = {"status": WITHHELD, "reason": EARLIER_WITHHELD_REASON}
    out["statistic_labels"] = {}
    return mask_free_text(out, "findings_summary_for_readers.yaml")


def withhold_registry_numbers(summary: dict) -> dict:
    """The registry summary (block_registry) for the readers: this run's idea status and its
    correlation to the composite (both over every window) and every earlier
    block's residual IC / correlation are withheld; the block inventory and
    types stay."""
    out = copy.deepcopy(summary)
    this = out.get("this_run")
    if isinstance(this, dict):
        if "idea_status" in this:
            this["idea_status"] = WITHHELD
        if "correlation_to_composite" in this:
            this["correlation_to_composite"] = {"status": WITHHELD, "reason": WITHHELD_REASON}
    for b in out.get("blocks") or []:
        if isinstance(b, dict):
            for k in ("residual_ic", "correlation_to_composite"):
                if k in b:
                    b[k] = WITHHELD
    for g in out.get("groups") or []:
        if isinstance(g, dict):
            for k in ("residual_ic_range", "abs_correlation_to_composite_range"):
                if k in g:
                    g[k] = WITHHELD
    out["numbers"] = {"status": WITHHELD, "reason": WITHHELD_REASON}
    return out


def reader_card(card: dict) -> dict:
    """artifacts/exploration/hypothesis_card.yaml: the card the readers get --
    READER_CARD_KEYS and the claim's READER_CLAIM_KEYS only (a whitelist).
    Every other field (free text that may quote an all-window number, numeric
    evidence) is left out and listed under `withheld_fields`; the free text
    kept (signal_concept, target_market, claim.statement, manifest.rationale)
    has its numbers masked (mask_free_text)."""
    if not isinstance(card, dict):
        raise ValueError("hypothesis_card.yaml is not a mapping -- no readers' copy is built")
    out = {k: copy.deepcopy(card[k]) for k in READER_CARD_KEYS if k in card}
    claim = card.get("claim")
    if isinstance(claim, dict):
        out["claim"] = {k: copy.deepcopy(claim[k]) for k in READER_CLAIM_KEYS if k in claim}
    dropped = sorted(k for k in card if k not in READER_CARD_KEYS and k != "claim")
    dropped += sorted(f"claim.{k}" for k in (claim if isinstance(claim, dict) else {})
                      if k not in READER_CLAIM_KEYS)
    out["withheld_fields"] = {"fields": dropped,
                              "reason": ("withheld under explore_confirm: free text or evidence "
                                         "that may quote numbers measured over every window")}
    return mask_free_text(out, "hypothesis_card.yaml")


def reader_manifest(manifest: dict) -> dict:
    """artifacts/exploration/block_manifest.yaml: the block manifest the
    readers get -- the config paths unchanged, the rationale (1b's free text)
    with its numbers masked (mask_free_text)."""
    if not isinstance(manifest, dict):
        raise ValueError("block_manifest.yaml is not a mapping -- no readers' copy is built")
    return mask_free_text(copy.deepcopy(manifest), "block_manifest.yaml")


# ---------------------------------------------------------------------------
# Which attempt wrote the readers' copies (PR #340 review round 2, finding 4)
# ---------------------------------------------------------------------------
# A copy left by an earlier protocol_execution attempt (its removal failed,
# and so did the removal after a failed rewrite) must never pass as this
# attempt's. At protocol_execution entry a fresh attempt id is written to
# artifacts/ATTEMPT_ARTIFACT; after each batch of copies is written,
# COPIES_STAMP (inside artifacts/exploration/, written LAST) lists them under
# that id. A copy not listed under the current id counts as missing.
ATTEMPT_ARTIFACT = "explore_confirm_attempt.yaml"
COPIES_STAMP = "copies_stamp.yaml"


def new_attempt(arts: Path) -> str:
    """A fresh attempt id in artifacts/ATTEMPT_ARTIFACT (protocol_execution
    entry). Raises when it cannot be written."""
    import campaign_memory as cm
    aid = uuid.uuid4().hex
    cm._atomic_write(Path(arts) / ATTEMPT_ARTIFACT,
                     {"schema_version": SCHEMA_VERSION, "attempt_id": aid,
                      "note": ("this protocol_execution attempt; only the readers' copies "
                               f"listed under this id in {EXPLORATION_DIR}/{COPIES_STAMP} are "
                               "current")})
    return aid


def current_attempt(arts: Path):
    """The current attempt id, or None (absent or unreadable). Never raises."""
    try:
        doc = _load_yaml(Path(arts) / ATTEMPT_ARTIFACT)
    except Exception:  # noqa: BLE001 -- absent or unreadable: no current attempt
        return None
    aid = doc.get("attempt_id") if isinstance(doc, dict) else None
    return aid if isinstance(aid, str) and aid else None


def stamp_copies(arts: Path, rels) -> None:
    """Called LAST, after a batch of readers' copies is written: adds `rels`
    (relative to artifacts/exploration/) to COPIES_STAMP under the current
    attempt id (a stamp of another attempt is replaced). Raises when there is
    no current attempt or the stamp cannot be written -- the copies then
    count as missing."""
    import campaign_memory as cm
    aid = current_attempt(arts)
    if aid is None:
        raise ValueError(f"no current attempt id in {Path(arts) / ATTEMPT_ARTIFACT} -- the "
                         f"readers' copies cannot be told apart from an earlier attempt's")
    path = Path(arts) / EXPLORATION_DIR / COPIES_STAMP
    try:
        doc = _load_yaml(path) if path.exists() else None
    except (OSError, ValueError, yaml.YAMLError):
        doc = None
    files = set(doc.get("files") or []) if isinstance(doc, dict) and \
        doc.get("attempt_id") == aid else set()
    cm._atomic_write(path, {"attempt_id": aid, "files": sorted(files | {str(r) for r in rels})})


def current_copies(arts: Path) -> set:
    """The readers' copies (relative to artifacts/exploration/) written by the
    current attempt; empty when there is no current attempt or no stamp of
    it. Never raises."""
    aid = current_attempt(arts)
    if aid is None:
        return set()
    try:
        doc = _load_yaml(Path(arts) / EXPLORATION_DIR / COPIES_STAMP)
    except Exception:  # noqa: BLE001 -- absent or unreadable: nothing is current
        return set()
    if not isinstance(doc, dict) or doc.get("attempt_id") != aid:
        return set()
    return {str(f) for f in doc.get("files") or []}


def exploration_inputs_missing(arts: Path, category: str, required: tuple):
    """None when `category`'s reader has every readers' copy it cannot run
    without (the split, and each path of `required` under
    artifacts/exploration/, `{category}` filled in -- the orchestrator's
    list -- written by the current attempt: current_copies), else the reason
    it has not -- the reader is then skipped by rule
    exploration_inputs_unavailable, never given the all-window files (nor an
    earlier attempt's copy). Never raises."""
    try:
        load_split(arts)
    except Exception as exc:  # noqa: BLE001 -- the reason is recorded
        return (f"the exploration/confirmation split cannot be read "
                f"({type(exc).__name__}: {exc})")
    root = Path(arts) / EXPLORATION_DIR
    current = current_copies(arts)
    missing = [f"{EXPLORATION_DIR}/{rel.format(category=category)}" for rel in required
               if not (root / rel.format(category=category)).is_file()
               or rel.format(category=category) not in current]
    if missing:
        return (f"the readers' exploration copies {missing} could not be written in this "
                f"attempt (absent, or left by an earlier attempt); the all-window files are "
                f"never given instead")
    return None


# ---------------------------------------------------------------------------
# Confirmation of side findings
# ---------------------------------------------------------------------------

FOLD_PENDING_REASON = ("measured by the run built from it, on that run's own fold "
                       "(E-077 confirm_on_fold); never inside the run that inspired it")


def finding_route(item: dict, *, folds: bool = False, trade_tests: bool = False) -> tuple:
    """(route, reason) of one side finding (a flattened reading item).

    `folds` (E-077 PR-2, orchestrator.folds.enabled): the IN_RUN route does not
    exist -- a claim is never confirmed inside the run that inspired it -- so a
    measurable finding (a block claim or a price-only one alike) is PENDING until
    tools/fold_confirm.confirm_on_fold measures it on its child run's fold. A
    refused claim and `tests: none` route as before."""
    import claim_card as cc
    claim = item.get("claim") if isinstance(item, dict) else None
    res = cc.check_claim(claim, **({"folds": True} if folds else {}),
                         **({"trade_tests": True} if trade_tests else {}))
    if res.errors:
        return NOT_MEASURABLE, "its claim is refused by check_claim: " + "; ".join(res.errors)
    if res.tests_none:
        return NOT_MEASURABLE, f"tests: none (missing block {res.missing_block!r})"
    if folds:
        return PENDING, FOLD_PENDING_REASON
    block = cc.KIND_BLOCK.get(claim.get("kind"))
    if block in ("forecast", "regime"):
        return PENDING, (f"a {block} block claim: measured on the confirmation windows of the "
                         f"run built from it")
    if item.get("config_change") and any(cc.signal_columns(t) for t in claim["tests"]
                                         if isinstance(t, dict)):
        return PENDING, ("its config change alters the forecast/regime its tests read: measured "
                         "on the confirmation windows of the run built from it")
    return IN_RUN, "a price-only (pure) finding: measured in this run"


def test_sign(result: dict) -> tuple:
    """(held, reason) of one measure_test result on confirmation windows:
    held True when at least one horizon has a value and every horizon with a
    value has the claimed sign (oriented > 0); False when one does not, or
    when nothing could be measured (no events); None on an error."""
    import claim_measure as cmeas
    status = result.get("status")
    if status == cmeas.NO_EVENTS:
        return False, "no events on the confirmation windows"
    if status != cmeas.MEASURED:
        return None, f"not measured: {result.get('reason')}"
    vals = {str(h): r.get("oriented") for h, r in (result.get("horizons") or {}).items()}
    defined = {h: v for h, v in vals.items() if v is not None}
    if not defined:
        return False, "no horizon has a value on the confirmation windows"
    bad = sorted((h for h, v in defined.items() if not v > 0), key=lambda h: float(h))
    if bad:
        return False, f"claimed sign not held at horizon(s) {bad}"
    return True, f"claimed sign held at every horizon with a value ({sorted(defined, key=float)})"


test_sign.__test__ = False  # not a pytest test


def finding_sign(results: dict) -> tuple:
    """(retained, reason, per-test) from {test name: measure_test result}:
    True only when every test held; None when any test errored; else False."""
    per = {n: test_sign(r) for n, r in results.items()}
    if not per:
        return None, "no test", {}
    if any(h is None for h, _ in per.values()):
        return None, "a test could not be measured", per
    if all(h is True for h, _ in per.values()):
        return True, "every test held its claimed sign", per
    return False, "; ".join(f"{n}: {why}" for n, (h, why) in sorted(per.items()) if not h), per


def _compact_result(r: dict, held) -> dict:
    out = {"status": r.get("status"), "spec_hash": r.get("spec_hash"),
           "statistic": r.get("statistic"), "direction": r.get("direction"),
           "sign_held": held[0], "why": held[1]}
    if r.get("reason"):
        out["reason"] = r.get("reason")
    hz = {}
    for h, row in (r.get("horizons") or {}).items():
        hz[str(h)] = {"effect": row.get("value"), "oriented": row.get("oriented"),
                      "n_events": row.get("n_events"),
                      "windows_claimed_sign": row.get("windows_with_claimed_sign"),
                      "windows_with_value": row.get("windows_with_a_value")}
    if hz:
        out["horizons"] = hz
    return out


def comparisons_of(results: dict) -> list:
    """[{test, spec_hash, n_comparisons}] -- one comparison per horizon of a
    test that was looked at (measured or no events)."""
    import claim_measure as cmeas
    out = []
    for n, r in sorted(results.items()):
        if r.get("status") in (cmeas.MEASURED, cmeas.NO_EVENTS):
            out.append({"test": n, "spec_hash": r.get("spec_hash"),
                        "n_comparisons": max(1, len(r.get("horizons") or {}))})
    return out


def measured_record(results: dict, measured_windows: list, variant: str) -> dict:
    """The confirmation part of a record once measured."""
    retained, why, per = finding_sign(results)
    return {"status": MEASURED if retained is not None else ERROR,
            "confirmation_sign_retained": retained, "reason": why,
            "variant": variant, "windows_measured": list(measured_windows),
            "tests": {n: _compact_result(r, per.get(n, (None, ""))) for n, r in
                      sorted(results.items())}}


def side_finding_items(readings: dict) -> list:
    """[(category, item)] for every side finding of a run's readings."""
    import reader_proposals as rp
    out = []
    for cat, doc in sorted((readings or {}).items()):
        if not isinstance(doc, dict) or "skipped" in doc:
            continue
        for item in rp.flatten_reading(doc):
            if item.get("kind") == rp.SIDE_FINDING:
                out.append((cat, item))
    return out


def confirm_findings(run_dir: Path, run_id: str, readings: dict, split: dict, *,
                     base_variant: str | None, eras, holdout_start: str,
                     merges: dict | None = None, folds: bool = False,
                     trade_tests: bool = False) -> list:
    """One record per side finding of this run's readings: measured in-run on
    the confirmation windows of the base variant (a pure finding), or pending
    / not_measurable with its reason. Never raises: an error is a record.

    `merges` (E-073 step 2, orchestrator.observable_backtest only;
    reader_findings.merge_index of the run's side_finding_merges.yaml): a
    merged duplicate is measured and counted ONCE -- its primary's record
    lists every source (`sources`, `merged_finding_ids`, `merge_note`: not
    agreement), and the other members get no record and no look. None (the
    default): exactly as before.

    `folds` (E-077 PR-2, orchestrator.folds.enabled): finding_route(folds=True) --
    no finding is measured in this run; every measurable one is `pending` for the
    fold of the run built from it (tools/fold_confirm.confirm_on_fold)."""
    conf = split["confirmation"]
    conf_labels = labels(conf)
    records = []
    for cat, item in side_finding_items(readings):
        claim = item.get("claim") or {}
        merged = (merges or {}).get(item.get("proposal_id"))
        if merged and merged["order"]:
            continue  # a merged duplicate: its primary's record is the one measurement
        rec = {"finding_id": item.get("proposal_id"), "category": cat, "source_run": run_id,
               "kind": claim.get("kind"), "statement": claim.get("statement"),
               "proposer_saw": [dict(r) for r in split["exploration"]],
               "confirmation_set": set_key(conf), "bar": HONEST_BAR}
        if merged:
            import reader_findings as _rf
            rec["sources"] = [dict(x) for x in merged["group"].get("sources") or []]
            rec["merged_finding_ids"] = list(merged["group"]["finding_ids"][1:])
            rec["merge_note"] = _rf.MERGE_NOT_AGREEMENT
        try:
            kw = {**({"folds": True} if folds else {}),
                  **({"trade_tests": True} if trade_tests else {})}    # D-091
            route, why = finding_route(item, **kw)
            rec["finding_spec_hashes"] = finding_spec_hashes(item, **kw)
        except Exception as exc:  # noqa: BLE001 -- recorded
            route, why = ERROR, f"{type(exc).__name__}: {exc}"
        rec["route"] = route
        if route == PENDING:
            rec.update({"status": PENDING, "confirmation_sign_retained": PENDING, "reason": why})
        elif route != IN_RUN:
            rec.update({"status": route, "confirmation_sign_retained": None, "reason": why})
        elif base_variant is None:
            rec.update({"status": ERROR, "confirmation_sign_retained": None,
                        "reason": "no graded base variant to measure on"})
        else:
            try:
                results, measured = measure_on_windows(run_dir, base_variant, claim["tests"],
                                                       conf_labels, eras, holdout_start)
                rec.update(measured_record(results, measured, base_variant))
                rec["measured_in_run"] = run_id
                rec["confirmation_basis"] = BASIS_IN_RUN
                rec["_comparisons"] = comparisons_of(results)
            except Exception as exc:  # noqa: BLE001 -- recorded
                rec.update({"status": ERROR, "confirmation_sign_retained": None,
                            "reason": f"{type(exc).__name__}: {exc}"})
        records.append(rec)
    return records


def source_finding_id(arts: Path):
    """The side finding a run was built from (its research_brief.yaml's
    candidate.source.proposal_ref, after '#'), or None."""
    path = Path(arts) / "research_brief.yaml"
    if not path.exists():
        return None
    doc = _load_yaml(path) or {}
    ref = (((doc.get("candidate") or {}).get("source") or {}).get("proposal_ref")
           if isinstance(doc, dict) else None)
    if not isinstance(ref, str) or "#" not in ref:
        return None
    return ref.split("#", 1)[1] or None


def pending_for(findings: dict, source_id, run_id: str):
    """The record THIS run (built from finding `source_id`) should resolve,
    from the ledger's `findings` (read under the ledger's lock), or None: the
    finding while it is pending, or -- on a resume or re-run of this same run
    -- the finding this run already resolved, put back to its pending state so
    it is measured again (artifacts/confirmation.yaml keeps it under
    resolved_pending; its looks are not counted twice)."""
    rec = (findings or {}).get(source_id) if source_id else None
    if rec is None and source_id:
        # E-073 step 2: the run may be built from a merged duplicate; its
        # finding is recorded under the group's primary (merged_finding_ids)
        rec = next((r for r in (findings or {}).values() if isinstance(r, dict)
                    and source_id in (r.get("merged_finding_ids") or [])), None)
    if not isinstance(rec, dict):
        return None
    if rec.get("confirmation_sign_retained") == PENDING:
        return rec
    if rec.get("measured_in_run") == run_id and rec.get("confirmation_basis") == BASIS_FOLLOW_UP:
        out = copy.deepcopy(rec)
        state = out.pop("pending_state", None)
        for k in _RESOLUTION_KEYS:
            out.pop(k, None)
        out.update(state if isinstance(state, dict) else
                   {"status": PENDING, "confirmation_sign_retained": PENDING})
        return out
    return None


def resolve_pending(run_dir: Path, run_id: str, pending: dict, split: dict, *,
                    base_variant: str | None, eras, holdout_start: str) -> dict:
    """A pending record, measured by THIS run (built from it): this run's own
    claim tests (its hypothesis card) on this run's confirmation windows of its
    base variant. Not measured -- and still pending -- when this run's
    confirmation windows overlap the windows the proposer saw. Never raises.

    A resolution is recorded as WEAK (PR #340 review, finding 1):
    `confirmation_basis: follow_up_run`, `proposer_exposure:
    step_1a_saw_all_window_knowledge_base`, `weak: true` -- this run's card
    was written by step 1a, which read the all-window knowledge base. When
    this run's tests differ from the finding's (`tests_changed_from_finding`),
    the result is `not_comparable`: its own sign is kept as
    `sign_of_own_tests`, never counted as the finding held or not held. An
    earlier attempt of this same run is replaced, not appended to."""
    import claim_card as cc
    rec = copy.deepcopy(pending)
    rec["attempts"] = [a for a in rec.get("attempts") or []
                       if not (isinstance(a, dict) and a.get("run_id") == run_id)]
    conf = split["confirmation"]
    overlap = _overlap(rec.get("proposer_saw") or [], conf)
    attempt = {"run_id": run_id, "confirmation_set": set_key(conf)}
    if overlap:
        attempt["result"] = f"not measured: {overlap} (the proposer saw them)"
        rec.setdefault("attempts", []).append(attempt)
        return rec
    try:
        card = _load_yaml(Path(run_dir) / "artifacts" / "hypothesis_card.yaml") or {}
        claim = card.get("claim") if isinstance(card, dict) else None
        res = cc.check_claim(claim, cc.card_criteria_ids(card if isinstance(card, dict) else {}))
        names = {t["name"] for t in res.tests}
        tests = [t for t in (claim or {}).get("tests") or []
                 if isinstance(t, dict) and t.get("name") in names] \
            if isinstance(claim, dict) and isinstance(claim.get("tests"), list) else []
        if res.errors or not tests:
            attempt["result"] = "not measured: this run's card has no usable claim test"
            rec.setdefault("attempts", []).append(attempt)
            return rec
        if base_variant is None:
            attempt["result"] = "not measured: no graded base variant"
            rec.setdefault("attempts", []).append(attempt)
            return rec
        results, measured = measure_on_windows(run_dir, base_variant, tests, labels(conf), eras,
                                               holdout_start)
    except Exception as exc:  # noqa: BLE001 -- recorded, still pending
        attempt["result"] = f"not measured: {type(exc).__name__}: {exc}"
        rec.setdefault("attempts", []).append(attempt)
        return rec
    rec.setdefault("pending_state", {k: pending.get(k) for k in _PENDING_STATE_KEYS})
    rec.update(measured_record(results, measured, base_variant))
    rec.update({"measured_in_run": run_id, "confirmation_set": set_key(conf),
                "_comparisons": comparisons_of(results), "confirmation_basis": BASIS_FOLLOW_UP,
                "proposer_exposure": PROPOSER_EXPOSURE_1A, "weak": True, "bar": WEAK_BAR})
    own = {t.get("spec_hash") for t in res.tests}
    rec["tests_changed_from_finding"] = bool(rec.get("finding_spec_hashes")) and \
        set(rec.get("finding_spec_hashes") or []) != own
    if rec["tests_changed_from_finding"] and rec.get("confirmation_sign_retained") is not None:
        rec["sign_of_own_tests"] = rec["confirmation_sign_retained"]
        rec["confirmation_sign_retained"] = NOT_COMPARABLE
        rec["reason"] = ("not comparable: the run built from this finding measured other tests "
                         "(spec_hash differs from the finding's); its own tests' sign is "
                         "sign_of_own_tests, not this finding's")
    attempt["result"] = rec["status"]
    rec.setdefault("attempts", []).append(attempt)
    return rec


def finding_spec_hashes(item: dict, *, folds: bool = False, trade_tests: bool = False) -> list:
    import claim_card as cc
    res = cc.check_claim(item.get("claim") if isinstance(item, dict) else None,
                         **({"folds": True} if folds else {}),
                         **({"trade_tests": True} if trade_tests else {}))
    return sorted(t["spec_hash"] for t in res.tests if t.get("spec_hash"))


# ---------------------------------------------------------------------------
# The campaign ledger: every finding's latest record, and every look
# ---------------------------------------------------------------------------

def load_ledger(root: Path) -> dict:
    path = Path(root) / LEDGER_REL
    if not path.exists():
        return {}
    doc = _load_yaml(path)
    return doc if isinstance(doc, dict) else {}


def _resolved_elsewhere(old, run_id: str) -> bool:
    """True when the ledger's record `old` was measured by ANOTHER run than
    `run_id` (a follow-up run's resolution, or another run's in-run
    measurement): `run_id` may then not replace it. A pending record, or one
    measured by `run_id` itself, may be replaced."""
    return (isinstance(old, dict) and old.get("confirmation_sign_retained") != PENDING
            and old.get("measured_in_run") not in (None, run_id))


def _count_looks(looks: list, seen: set, run_id: str, rec: dict, comps: list) -> None:
    """Append one look per (run, finding, spec_hash) not seen yet to `looks`
    (idempotent: a resumed stage never counts a look twice). Shared by record()
    and record_fold_confirmation()."""
    for c in comps:
        key = (run_id, rec.get("finding_id"), c.get("spec_hash"))
        if key in seen:
            continue
        seen.add(key)
        looks.append({"run_id": run_id, "finding_id": rec.get("finding_id"),
                      "test": c.get("test"), "spec_hash": c.get("spec_hash"),
                      "n_comparisons": int(c.get("n_comparisons") or 1),
                      "confirmation_set": rec.get("confirmation_set")})


def _looks_on_set(looks: list, rec: dict) -> dict:
    """A record's `looks` field: how many looks and comparisons its confirmation set has now."""
    on_set = [lk for lk in looks if lk.get("confirmation_set") == rec.get("confirmation_set")]
    return {"confirmation_set": rec.get("confirmation_set"),
            "n_looks_on_set": len(on_set),
            "n_comparisons_on_set": sum(lk["n_comparisons"] for lk in on_set)}


def _by_set(looks: list) -> dict:
    by_set = {}
    for lk in looks:
        s = by_set.setdefault(str(lk.get("confirmation_set")),
                              {"n_looks": 0, "n_comparisons": 0})
        s["n_looks"] += 1
        s["n_comparisons"] += int(lk.get("n_comparisons") or 1)
    return dict(sorted(by_set.items()))


def record(root: Path, run_id: str, records: list, *, resolve=None) -> list:
    """Upsert `records` (this run's side findings) into
    campaign_record/confirmations.yaml and count their looks (idempotent per
    run, finding and spec_hash: a resumed stage never counts a look twice).
    Locked, atomic.

    `resolve`: optional callable(findings) -> [resolved records], called
    UNDER the lock with the ledger's findings (the pending lookup reads the
    ledger as it is now, not a copy read before the lock); its records are
    upserted and counted after `records`.

    A re-run of this run REPLACES its own entries: a finding this run proposed
    in an earlier attempt and not in `records` is removed from `findings`
    (listed under `superseded`) -- unless another run already measured it.
    Its looks stay counted: a look measured on a confirmation set was spent,
    whichever attempt took it. A record another run already measured (a
    follow-up run's resolution) is never replaced by a re-run of the source
    run: it is kept, and the re-run's record goes under `superseded`
    (_resolved_elsewhere).

    Returns the records as written (`records` first, then the resolved ones),
    each measured one with its `looks` position on its confirmation set."""
    import campaign_memory as cm
    import campaign_review_retired as crr
    path = Path(root) / LEDGER_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    written = []
    with crr._lock(path, path.name):
        doc = crr._load_mapping(path, {})
        findings = doc.get("findings") if isinstance(doc.get("findings"), dict) else {}
        looks = [lk for lk in doc.get("looks") or [] if isinstance(lk, dict)]
        superseded = [s for s in doc.get("superseded") or [] if isinstance(s, dict)]
        seen = {(lk.get("run_id"), lk.get("finding_id"), lk.get("spec_hash")) for lk in looks}
        resolved = list(resolve(copy.deepcopy(findings)) or []) if resolve is not None else []
        own_now = {str(r.get("finding_id")) for r in records if r.get("finding_id")}
        for fid, old in sorted(findings.items()):
            if (isinstance(old, dict) and old.get("source_run") == run_id
                    and str(fid) not in own_now
                    and old.get("measured_in_run") in (None, run_id)):
                superseded.append({"run_id": run_id, "finding_id": str(fid),
                                   "status": old.get("status"),
                                   "confirmation_sign_retained":
                                       old.get("confirmation_sign_retained"),
                                   "note": "an earlier attempt of this run; its looks stay "
                                           "counted"})
                del findings[fid]
        for rec in list(records) + resolved:
            rec = dict(rec)
            comps = rec.pop("_comparisons", None) or []
            _count_looks(looks, seen, run_id, rec, comps)
            if comps:
                rec["looks"] = _looks_on_set(looks, rec)
            fid = rec.get("finding_id")
            old = findings.get(str(fid)) if fid else None
            if _resolved_elsewhere(old, run_id):
                # review round 2, finding 2: a re-run of the source run never
                # overwrites a result another run measured -- that record is
                # kept, this attempt is listed under `superseded`
                same = set(old.get("finding_spec_hashes") or []) == set(
                    rec.get("finding_spec_hashes") or [])
                superseded.append({
                    "run_id": run_id, "finding_id": str(fid), "status": rec.get("status"),
                    "confirmation_sign_retained": rec.get("confirmation_sign_retained"),
                    "same_spec_hash": same,
                    "note": (f"a re-run of the source run; the record measured by "
                             f"{old.get('measured_in_run')} is kept (a re-run replaces only a "
                             f"pending or same-run record)")})
                rec["ledger"] = f"not written: already measured by {old.get('measured_in_run')}"
            elif fid:
                findings[str(fid)] = rec
            written.append(rec)
        cm._atomic_write(path, {"schema_version": SCHEMA_VERSION, "note": LEDGER_NOTE,
                                "bar": HONEST_BAR, "findings": findings, "looks": looks,
                                "by_set": _by_set(looks),
                                **({"superseded": superseded} if superseded else {}),
                                **_carry_fold_rows(doc)})
    return written


# ---------------------------------------------------------------------------
# E-077 PR-2 (D-087): one row per confirmation on a CHILD RUN's fold
# ---------------------------------------------------------------------------
# tools/fold_confirm.confirm_on_fold builds the row; this module owns the file, so
# the lock, the atomic write and the look counting are the ones above. The rows
# live under their own top-level key, `fold_confirmations`, keyed
# "<source finding id>@<child run id>" (one measurement = one row; a resumed or
# re-run child REPLACES its own row, never adds a second). They are kept apart
# from `findings` on purpose: record() removes "an earlier attempt of this run's"
# findings by source_run, and a child run measuring its parent's finding must not
# be mistaken for that.
FOLD_ROWS_KEY = "fold_confirmations"


def _carry_fold_rows(doc: dict) -> dict:
    """The ledger's fold rows, carried through record()'s rewrite of the file
    ({} when there are none, so a ledger without them is written exactly as before)."""
    rows = doc.get(FOLD_ROWS_KEY)
    return {FOLD_ROWS_KEY: rows} if isinstance(rows, dict) and rows else {}


def fold_row_key(finding_id, run_id) -> str:
    return f"{finding_id}@{run_id}"


def record_fold_confirmation(root: Path, row: dict) -> dict:
    """Upsert one fold-confirmation row (built by fold_confirm.confirm_on_fold;
    `run_id` = the child run that measured it, `finding_id` = the claim's side
    finding) into campaign_record/confirmations.yaml, and count its looks on the
    fold's confirmation set (`_comparisons`, idempotent per child run, finding and
    spec_hash). Locked, atomic. Returns the row as written (`_comparisons`
    removed, `looks` added when it counted any)."""
    import campaign_memory as cm
    import campaign_review_retired as crr
    row = dict(row)
    run_id, fid = row.get("run_id"), row.get("finding_id")
    if not run_id or not fid:
        raise ValueError("a fold-confirmation row needs run_id (the child run) and finding_id")
    comps = row.pop("_comparisons", None) or []
    path = Path(root) / LEDGER_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with crr._lock(path, path.name):
        doc = crr._load_mapping(path, {})
        findings = doc.get("findings") if isinstance(doc.get("findings"), dict) else {}
        looks = [lk for lk in doc.get("looks") or [] if isinstance(lk, dict)]
        superseded = [x for x in doc.get("superseded") or [] if isinstance(x, dict)]
        rows = doc.get(FOLD_ROWS_KEY) if isinstance(doc.get(FOLD_ROWS_KEY), dict) else {}
        seen = {(lk.get("run_id"), lk.get("finding_id"), lk.get("spec_hash")) for lk in looks}
        _count_looks(looks, seen, run_id, row, comps)
        if comps:
            row["looks"] = _looks_on_set(looks, row)
        rows[fold_row_key(fid, run_id)] = row
        cm._atomic_write(path, {"schema_version": SCHEMA_VERSION, "note": LEDGER_NOTE,
                                "bar": HONEST_BAR, "findings": findings, "looks": looks,
                                "by_set": _by_set(looks),
                                **({"superseded": superseded} if superseded else {}),
                                FOLD_ROWS_KEY: dict(sorted(rows.items()))})
    return row


def fold_rows(doc) -> list:
    """The fold rows of a loaded ledger, in key order (a malformed value gives none)."""
    rows = doc.get(FOLD_ROWS_KEY) if isinstance(doc, dict) else None
    if not isinstance(rows, dict):
        return []
    return [r for _k, r in sorted(rows.items()) if isinstance(r, dict)]


def summary_lines(root: Path) -> list:
    """Campaign-summary lines; [] when the ledger does not exist (so a summary
    is unchanged until the flag has recorded something)."""
    path = Path(root) / LEDGER_REL
    if not path.exists():
        return []
    title = ["", "## Side findings on unseen windows (E-072; information only, not proven)", ""]
    try:
        doc = _load_yaml(path) or {}
    except (yaml.YAMLError, OSError, UnicodeDecodeError) as exc:
        return title + [f"- {LEDGER_REL} is unreadable ({type(exc).__name__}); fix or remove it."]
    # review round 2, finding 3: a hand-edited ledger of another shape never
    # breaks the campaign summary (called on the pause/finish paths)
    if not isinstance(doc, dict) or any(doc.get(k) is not None and not isinstance(doc[k], dict)
                                        for k in ("by_set", "findings")):
        return title + [f"- {LEDGER_REL} is unreadable (not the confirmations ledger's shape); "
                        f"fix or remove it."]
    findings = doc.get("findings") or {}
    # E-077 PR-2: a finding a child run measured on its fold is counted in the fold
    # lines below, not as "pending" here (no fold rows: nothing changes).
    fold_done = {str(r.get("finding_id")) for r in fold_rows(doc)}
    findings = {k: v for k, v in findings.items() if str(k) not in fold_done}
    if fold_done and not findings:
        return fold_summary_lines(doc)      # only fold rows: no E-072 block to show
    # The clean counts are the in-run measurements (readers who saw the
    # exploration copies only); a resolution by the run built from a finding
    # is counted on its own line (weak: step 1a saw the all-window knowledge
    # base), and a not_comparable one is never held / not held.
    counts, follow = {}, {}
    for rec in findings.values():
        v = rec.get("confirmation_sign_retained") if isinstance(rec, dict) else None
        if isinstance(rec, dict) and rec.get("confirmation_basis") == BASIS_FOLLOW_UP:
            key = ("held" if v is True else "not held" if v is False
                   else "not comparable" if v == NOT_COMPARABLE else "not measured")
            follow[key] = follow.get(key, 0) + 1
            continue
        key = ("held" if v is True else "not held" if v is False
               else "pending" if v == PENDING else "not measured")
        counts[key] = counts.get(key, 0) + 1
    n_follow = sum(follow.values())
    lines = title + [f"- Side findings: {len(findings)} ("
                     + ", ".join(f"{k} {counts.get(k, 0)}"
                                 for k in ("held", "not held", "pending", "not measured"))
                     + f", resolved by a follow-up run {n_follow})"]
    if n_follow:
        lines.append("  - resolved by the run built from them (weak: step 1a, which wrote that "
                     "run's card, saw the all-window knowledge base): "
                     + ", ".join(f"{k} {follow.get(k, 0)}" for k in
                                 ("held", "not held", "not comparable", "not measured")))
    for s, c in sorted((doc.get("by_set") or {}).items()):
        if isinstance(c, dict):
            lines.append(f"  - confirmation set {s}: {c.get('n_looks')} look(s), "
                         f"{c.get('n_comparisons')} comparison(s)")
    return lines + fold_summary_lines(doc)


FOLD_STATUS_LINES = (("confirmed", "Confirmed"), ("not_confirmed", "Not confirmed"),
                     ("not_measurable", "Not measurable"), ("not_comparable", "Not comparable"))


def fold_summary_lines(doc: dict) -> list:
    """E-077 PR-2: one line per status of the fold confirmations, labelled with the
    fold each count comes from; [] when the ledger holds none (a summary without
    them is unchanged). `not comparable` is shown only when there is one."""
    rows = fold_rows(doc)
    if not rows:
        return []
    by_status = {}
    for r in rows:
        by_status.setdefault(r.get("status"), {}).setdefault(str(r.get("fold")), 0)
        by_status[r.get("status")][str(r.get("fold"))] += 1
    lines = ["", "## Claims measured on a child run's fold (E-077; a noise rule, not proof)", "",
             f"- Claims measured: {len(rows)}. Confirmed = the pooled sign holds at every "
             f"horizon and the claimed sign holds in all but one window (at least 4 windows): "
             f"a noise rule, about an 11% chance per fold under a symmetric null; no cost "
             f"is compared."]
    for status, label in FOLD_STATUS_LINES:
        per_fold = by_status.get(status, {})
        if status == "not_comparable" and not per_fold:
            continue
        lines.append(f"- {label}: {sum(per_fold.values())}"
                     + (" (" + ", ".join(f"fold {f} {n}" for f, n in sorted(per_fold.items())) + ")"
                        if per_fold else ""))
    by_set = doc.get("by_set") if isinstance(doc.get("by_set"), dict) else {}
    for key in sorted({str(r.get("confirmation_set")) for r in rows}):
        c = by_set.get(key)
        if isinstance(c, dict):
            lines.append(f"  - fold windows {key}: {c.get('n_looks')} look(s), "
                         f"{c.get('n_comparisons')} comparison(s)")
    return lines
