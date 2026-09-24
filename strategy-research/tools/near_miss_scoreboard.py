"""Near-miss scoreboard generator (E-018 S1).

Produces a ranked table over every tested idea (a `runs/run_*` directory) in
`strategy-research/runs/`. Its sole purpose, per `docs/CAMPAIGN_PROGRAM.md`
Part 1, is to be raw material for the IDEA-GENERATION stage: "failed a
criterion but ground for an idea" is real information this project
under-uses. It is NOT a ranking used, or usable, for promotion.

FIREWALL (doctrine, see the epic and Part 1 verbatim): "The scoreboard
inspires; only the gates decide." Promotion must have no *decision-making*
read on this module or its output -- i.e. no code that computes
hypothesis_verdict/lineage_routing/promote-kill may consult it. This was
previously enforced by a static test (tests/test_near_miss_scoreboard_firewall.py,
removed 2026-09-13, E-018 S2 -- the operator's own call, judged
overengineered for what it was protecting once verdict-interpreter became an
explicit, reviewed exception; see below). There is now no mechanical check
for this doctrine -- it relies on the routing functions in
workflow/run_phase1_research.py (`_resolve_verdict_fields`,
`determine_post_verdict_route`, `_apply_circuit_breaker`, `_dispatch_verdict_route`)
genuinely never importing or reading this module/its output, verified by
inspection rather than by a standing test.

E-018 S2 (2026-09-13): verdict-interpreter/SKILL.md is a reviewed, EXPLICIT
exception to the doctrine above, and workflow/run_phase1_research.py's
verdict_interpreter handoff-construction code (where its optional_inputs are
built) now references this module's output path directly, to actually hand
the file to the LLM. Made safe by a companion change the same session:
routing (`determine_post_verdict_route`) now reads a BINDING
`pass_rule_evaluation.yaml` directly, so verdict_interpreter's own restated
verdict no longer drives promote/kill on any run that has one; the scoreboard
informs only its qualitative writeup (root_cause, proposed_brief,
findings_carryover), never hypothesis_verdict/lineage_routing. The output
artifact is deliberately written under
`engineering/roadmap/E-018/artifacts/`, NOT under `runs/*/artifacts/` or
`campaign_record/` -- neither of which is glob-safe against decision-path
code (run_campaign.py globs `runs/*/artifacts/*` in places, and
`campaign_record/campaign_knowledge_base.yaml` is already a required input of
decision-adjacent skills, e.g. verdict-interpreter). See this file's __main__
docstring output for the by-inspection audit trail.

WHAT THIS DOES NOT DO
    - It does not compute, gate, or influence any pass/fail/promote decision.
    - It never touches `local_data/holdout_sealed/`.
    - It never runs a backtest or campaign; it only reads artifacts already
      on disk under runs/.

HONESTY RULES (per the epic's Done-when and the operator's brief)
    - Every derived count states its denominator (N of how many run dirs).
    - Nothing is imputed. Where a field cannot be recovered for a run, the
      row carries an explicit "not_recorded" marker -- never a guess, never
      a silent drop. A thin record is itself information the idea-generation
      stage needs, so thin runs stay IN the table.
    - Fields extracted via best-effort regex from free text are tagged with
      their source (`structured` vs `text_extracted`) so a consumer can
      weight confidence accordingly.

SCHEMA DIVERSITY (measured 2026-08-23 across all 38 verdict_interpretation.yaml
files, 59 run_* dirs total)
    Two verdict_interpretation.yaml schema families exist:
      1. "protocol" schema (36 of 38 files) -- protocol_verdict, status,
         criteria_summary (list of dicts OR list of free-text strings --
         both forms occur, roughly 19/17 dict/string split), primary_failure_mode,
         root_cause.{mechanism_failure,confidence}.
      2. "prescreen/disposition" schema (run_041, run_042) -- verdict_label,
         disposition, prescreen_summary/prescreen_result_summary with
         structured ic_active_bars/ic_all_bars/p_value/edge_to_cost_ratio.
    21 of 59 run dirs carry NO verdict_interpretation.yaml at all (early/killed
    pipeline runs). For those, `pipeline_state.yaml`'s status/current_stage is
    recorded as the "why thin" explanation where the file exists.

    Two DIFFERENT verdict fields are routinely confused in this project's own
    history and are reported here as SEPARATE columns, never collapsed:
    `protocol_verdict` (26 refine / 10 kill / 2 absent-within-file, of 38) and
    `status` (14 refine / 10 pivot / 7 escalate / 2 kill / 5 absent-within-file,
    of 38). ZERO "promote" appears in either, across the whole history.

GRID ROWS (E-058 S2b, 2026-09-23)
    A run with `artifacts/grid_evaluation.yaml` (the E-046b grid, written by
    protocol_execution) is read from THAT file instead of
    verdict_interpretation.yaml, and its row carries evidence_tier `grid`,
    `legacy: false` and the grid's `idea_status`. Its near miss is the closest
    FAILing cell (per-symbol sub-cells included), from the cell's own `value`
    and `threshold` and the criterion's comparator (resolved from the run's
    pre_registration.yaml against config/criterion_menu.yaml by the
    evaluator's own _resolve_grid_criteria). Every other row is `legacy: true`
    and is built exactly as before. The retired refine/pivot/escalate words
    are never read for a grid row (its `status` stays not_recorded).
    Wired (E-058 S2b): the orchestrator's regroup_record stage
    (orchestrator.regroup_record.enabled, off by default) calls
    build_scoreboard + write_scoreboard with an explicit out_dir after
    recording each run. Nothing on the route reads the output (firewall).

USAGE
    python tools/near_miss_scoreboard.py
    python tools/near_miss_scoreboard.py --runs-dir runs --out-dir engineering/roadmap/E-018/artifacts

REGENERATES (idempotent -- safe to re-run any time; see Task 3 in the S1
dispatch: this is the "standing, not one-shot" mechanism. It is not yet
wired into the campaign loop -- see the script's final printed note and
E-018/EPIC.md's Log for what that wiring would need.)
    <out-dir>/near_miss_scoreboard.yaml   -- structured, machine-readable
    <out-dir>/near_miss_scoreboard.md     -- rendered ranked table + denominators
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

STRATEGY_RESEARCH_ROOT = Path(__file__).resolve().parent.parent

# --- failure-mode buckets, carried forward from
# engineering/roadmap/E-030/artifacts/measure_verdict_repetition.py (same
# regexes, same "first sentence only" discipline -- reused rather than
# reimplemented per the dispatch's instruction). ---------------------------
FAILURE_BUCKETS = [
    ("regime",   r"regime|gat(e|ing)|activation|starvation"),
    ("cost",     r"cost.drag|fee|over-?trad|turnover|sizing/frequency"),
    ("nosignal", r"no (statistically |directional )?(significant )?edge|no informational|no predictive|inversion|uninformative signal"),
    ("sample",   r"insufficient sample|sample size|sparsity|min-?n"),
]


def classify_bucket(text: str) -> list[str]:
    if not text:
        return ["not_recorded"]
    full = " ".join(str(text).split())
    first = re.split(r"(?<=[.;:])\s", full)[0]
    tags = [name for name, pat in FAILURE_BUCKETS if re.search(pat, first, re.I)]
    return tags or ["other"]


# --- generic comparator/number extraction ---------------------------------
CMP_NUM_RE = re.compile(r"(<=|>=|≤|≥|<|>)\s*(-?~?\d+(?:\.\d+)?)\s*%?")
LABEL_NUM_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]{1,40})\s*[=:]\s*(-?~?\d+(?:\.\d+)?)\s*%?")
SYM_PAREN_NUM_RE = re.compile(r"(-?~?\d+(?:\.\d+)?)\s*%?\s*\(([A-Z]{2,10})\)")
SYM_LEAD_NUM_RE = re.compile(r"\b([A-Z]{3,10})\b\s+(-?~?\d+(?:\.\d+)?)\s*%?")
RESULT_RE = re.compile(r"\b(PASS(?:ED)?|FAIL(?:ED)?|UNTESTED)\b", re.IGNORECASE)
_EXCLUDE_SYM = {"PASS", "FAIL", "AND", "AND ", "NOT", "RULE", "ANY", "ALL", "AT", "IC", "AT ", "SE"}
# Labels that restate a REQUIREMENT rather than report an OBSERVATION, seen
# recurring inside the "detail" segment of free-text criteria (e.g. a
# rationale that says "...validation_protocol required=1.5 is a spec
# error..."). Picking these up as the "actual" value silently substitutes
# the threshold for the observation and produces a bogus zero margin.
_REQUIREMENT_LABELS = {"required", "threshold", "target", "min", "max", "expected", "requirement"}

_OP_NORM = {"≤": "<=", "≥": ">=", "<=": "<=", ">=": ">=", "<": "<", ">": ">"}


def _to_float(s):
    try:
        return float(str(s).strip().lstrip("~"))
    except (TypeError, ValueError):
        return None


def _worst(values, op):
    """Given multiple observed values for one criterion (e.g. per-symbol),
    return the one that binds the pass/fail decision -- the hardest to
    satisfy under `op`."""
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    if op in (">", ">="):
        return min(vals)
    if op in ("<", "<="):
        return max(vals)
    return vals[0]


def _margin_frac(op, threshold, actual):
    if threshold is None or actual is None or op not in _OP_NORM.values():
        return None
    base = abs(threshold) if threshold != 0 else 1.0
    if op in (">", ">="):
        return (actual - threshold) / base
    if op in ("<", "<="):
        return (threshold - actual) / base
    return None


class Criterion:
    __slots__ = ("raw", "result", "op", "threshold", "actual", "actual_source",
                 "margin_frac", "compound")

    def __init__(self, raw, result, op, threshold, actual, actual_source, compound):
        self.raw = raw
        self.result = result
        self.op = op
        self.threshold = threshold
        self.actual = actual
        self.actual_source = actual_source
        self.compound = compound
        margin = _margin_frac(op, threshold, actual)
        # SAFETY NET: a derived margin is only trusted when it agrees with the
        # verdict file's OWN stated result. Free-text/unit parsing across this
        # corpus is inconsistent (percent vs fraction, signed drawdowns vs
        # unsigned thresholds, stray digits from embedded dates) and a wrong
        # sign turns a blowout FAIL into an apparent giant PASS margin, which
        # would corrupt the near-miss ranking by promoting garbage to rank 1.
        # This is the cheapest control that catches that whole class: trust
        # the number only when its sign is consistent with the label already
        # given to us (measured against this corpus: caught 2 of 2 known
        # unit/sign artifacts -- run_029's "2024" date-as-trade-count and
        # run_018's percent/fraction mismatch -- without any bespoke
        # date-stripping or unit-normalization logic).
        if margin is not None:
            if self.result == "FAIL" and margin > 1e-9:
                margin = None
                self.actual_source = self.actual_source + "_contradicts_result"
            elif self.result == "PASS" and margin < -1e-9:
                margin = None
                self.actual_source = self.actual_source + "_contradicts_result"
        self.margin_frac = margin

    def to_dict(self):
        return {
            "text": self.raw,
            "result": self.result,
            "comparator": self.op,
            "threshold": self.threshold,
            "actual_binding_value": self.actual,
            "actual_source": self.actual_source,
            "margin_frac": None if self.margin_frac is None else round(self.margin_frac, 4),
            "compound_requirement": self.compound,
        }


def _extract_symbol_values(text: str):
    pairs = SYM_PAREN_NUM_RE.findall(text)
    if not pairs:
        pairs = [(n, s) for s, n in SYM_LEAD_NUM_RE.findall(text) if s.upper() not in _EXCLUDE_SYM]
        pairs = [(n, s) for n, s in pairs]
    else:
        pairs = [(n, s) for n, s in pairs]
    vals = [_to_float(n) for n, _s in pairs]
    return [v for v in vals if v is not None]


def parse_dict_criterion(c: dict) -> Criterion:
    raw = c.get("criterion") or c.get("text") or str(c)
    result = str(c.get("result", "unknown")).upper()
    if result not in ("PASS", "FAIL", "UNTESTED"):
        result = "unknown"
    required_text = str(c.get("required", ""))
    m = CMP_NUM_RE.search(required_text) or CMP_NUM_RE.search(raw)
    op = _OP_NORM.get(m.group(1)) if m else None
    threshold = _to_float(m.group(2)) if m else None
    compound = bool(re.search(r"\bAND\b|\bOR\b", required_text, re.I))

    actual_field = c.get("actual")
    actual_source = "none"
    actual = None
    if isinstance(actual_field, dict):
        vals = [_to_float(v) for v in actual_field.values()]
        vals = [v for v in vals if v is not None]
        if vals:
            actual = _worst(vals, op)
            actual_source = "structured_per_symbol"
    elif isinstance(actual_field, (int, float)):
        actual = float(actual_field)
        actual_source = "structured_scalar"
    elif isinstance(actual_field, str):
        direct = _to_float(actual_field)
        if direct is not None:
            actual = direct
            actual_source = "structured_scalar_text"
        else:
            vals = _extract_symbol_values(actual_field)
            if vals:
                actual = _worst(vals, op)
                actual_source = "text_extracted_per_symbol"

    if actual is None:
        # Some runs split per-symbol actuals into separate keys instead of a
        # nested dict/string (e.g. run_016: actual_btc / actual_eth).
        per_symbol_keys = [k for k in c.keys() if k.lower().startswith("actual") and k != "actual"]
        if per_symbol_keys:
            vals = [_to_float(c.get(k)) for k in per_symbol_keys]
            vals = [v for v in vals if v is not None]
            if vals:
                actual = _worst(vals, op)
                actual_source = "structured_per_symbol_keys"

    return Criterion(raw, result, op, threshold, actual, actual_source, compound)


def _normalize_result_token(tok: str) -> str:
    """FIX 5: RESULT_RE now also matches FAILED/PASSED (past tense) and
    lowercase untested (re.IGNORECASE), so the captured group can arrive as
    e.g. 'FAILED' or 'untested' -- normalize to exactly one of PASS/FAIL/
    UNTESTED before it reaches any consumer (Criterion.result, the safety
    net in Criterion.__init__, build_row's PASS/FAIL/UNTESTED counts), which
    all expect precisely those three tokens, never a variant."""
    t = tok.upper()
    if t.startswith("PASS"):
        return "PASS"
    if t.startswith("FAIL"):
        return "FAIL"
    return "UNTESTED"


def parse_text_criterion(text: str) -> Criterion:
    rm = RESULT_RE.search(text)
    result = _normalize_result_token(rm.group(1)) if rm else "unknown"
    req_seg = text[: rm.start()] if rm else text
    detail_seg = text[rm.end():] if rm else ""

    m = CMP_NUM_RE.search(req_seg)
    op = _OP_NORM.get(m.group(1)) if m else None
    threshold = _to_float(m.group(2)) if m else None
    compound = bool(re.search(r"\bAND\b|\bOR\b", req_seg, re.I))

    actual = None
    actual_source = "none"

    sym_vals = _extract_symbol_values(detail_seg)
    if sym_vals:
        actual = _worst(sym_vals, op)
        actual_source = "text_extracted_per_symbol"
    else:
        pairs = LABEL_NUM_RE.findall(detail_seg)
        pairs = [p for p in pairs if p[0].lower() not in _REQUIREMENT_LABELS]
        # drop pure noise labels that are clearly not the metric (e.g. "p" is
        # a real metric name too, so we don't blanket-exclude -- only exclude
        # if there are >1 candidates and none can be disambiguated).
        if len(pairs) == 1:
            actual = _to_float(pairs[0][1])
            actual_source = "text_extracted_label"
        elif len(pairs) > 1:
            req_norm = re.sub(r"[^a-z0-9]", "", req_seg.lower())
            matches = [p for p in pairs if re.sub(r"[^a-z0-9]", "", p[0].lower()) in req_norm
                       or req_norm[:12] in re.sub(r"[^a-z0-9]", "", p[0].lower())]
            if len(matches) == 1:
                actual = _to_float(matches[0][1])
                actual_source = "text_extracted_label_matched"
        if actual is None:
            am = re.search(r"actual[:=]?\s*~?(-?\d+(?:\.\d+)?)", detail_seg, re.I)
            if am:
                actual = _to_float(am.group(1))
                actual_source = "text_extracted_actual_marker"

    return Criterion(text, result, op, threshold, actual, actual_source, compound)


# --- IC / cost-ratio / era-behavior opportunistic extraction ---------------
IC_TEXT_RE = re.compile(r"\bic_(?:all|active)_bars\s*=\s*(-?\d+(?:\.\d+)?)", re.I)
COST_RATIO_TEXT_RE = re.compile(r"edge_to_cost_ratio\s*[=:]\s*(-?\d+(?:\.\d+)?)", re.I)
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")


def extract_ic_cost(y: dict):
    """Returns (ic, ic_source, cost_ratio, cost_ratio_source)."""
    for key in ("prescreen_result_summary", "prescreen_summary"):
        blk = y.get(key)
        if isinstance(blk, dict):
            ic = blk.get("ic_active_bars", blk.get("ic_all_bars"))
            cost = blk.get("edge_to_cost_ratio")
            if ic is not None or cost is not None:
                return (ic, "structured" if ic is not None else "not_recorded",
                         cost, "structured" if cost is not None else "not_recorded")

    # Fallback: opportunistic regex over the free-text fields most likely to
    # carry these numbers when the run used the "protocol" schema but the
    # underlying evidence still cites IC/cost from an earlier prescreen.
    haystack_parts = []
    rc = y.get("root_cause")
    if isinstance(rc, dict):
        haystack_parts.append(str(rc.get("supporting_evidence", "")))
    haystack_parts.append(str(y.get("primary_failure_mode", "")))
    haystack_parts.append(str(y.get("config_to_failure_map", "")))
    for c in y.get("criteria_summary") or []:
        haystack_parts.append(str(c))
    haystack = " ".join(haystack_parts)

    ic = None
    ic_m = IC_TEXT_RE.search(haystack)
    if ic_m:
        ic = _to_float(ic_m.group(1))
    cost = None
    cost_m = COST_RATIO_TEXT_RE.search(haystack)
    if cost_m:
        cost = _to_float(cost_m.group(1))
    return (ic, "text_extracted" if ic is not None else "not_recorded",
            cost, "text_extracted" if cost is not None else "not_recorded")


def extract_era_behavior(y: dict):
    """Best-effort: only claims era/period behaviour is recoverable when the
    supporting evidence names >=2 distinct 4-digit years (i.e. an actual
    cross-period comparison), never on a single incidental date."""
    rc = y.get("root_cause")
    text = ""
    if isinstance(rc, dict):
        text = str(rc.get("supporting_evidence", ""))
    if len(set(YEAR_RE.findall(text))) < 2:
        alt = str(y.get("primary_failure_mode", ""))
        if len(set(YEAR_RE.findall(alt))) >= 2:
            text = alt
        else:
            return (None, "not_recorded")
    snippet = " ".join(text.split())
    return (snippet[:400], "text_extracted")


# --- per-run row assembly ---------------------------------------------------
def parse_criteria_summary(cs) -> list[Criterion]:
    out = []
    if not cs:
        return out
    for c in cs:
        if isinstance(c, dict):
            out.append(parse_dict_criterion(c))
        else:
            out.append(parse_text_criterion(str(c)))
    return out


def _grid_row(run_dir: Path, grid_path: Path, row: dict, menu_path: Path | None) -> dict:
    """E-058 S2b: a row from grid_evaluation.yaml. A malformed grid raises (a
    thin row would hide a broken artifact)."""
    g = yaml.safe_load(grid_path.read_text(encoding="utf-8"))
    if not isinstance(g, dict) or not isinstance(g.get("grid"), dict) \
            or not isinstance(g.get("criteria"), list) or not isinstance(g.get("variants"), list):
        raise ValueError(f"{grid_path}: not a grid_evaluation document (criteria/variants/grid)")
    row["legacy"] = False
    row["evidence_tier"] = "grid"
    row["idea_status"] = g.get("idea_status") or "not_recorded"
    row["grid_result"] = g.get("result", "not_recorded")
    card_path = run_dir / "artifacts" / "hypothesis_card.yaml"
    if card_path.exists():
        card = yaml.safe_load(card_path.read_text(encoding="utf-8")) or {}
        if isinstance(card, dict) and card.get("hypothesis_id"):
            row["hypothesis_id"] = card["hypothesis_id"]
    reason = g.get("reason")
    if reason:
        row["primary_failure_mode_text"] = " ".join(str(reason).split())[:400]

    comparators = _grid_comparators(run_dir, menu_path)
    counts = {"PASS": 0, "FAIL": 0, "INCONCLUSIVE": 0}
    fails = []
    for crit in g["criteria"]:
        cells = g["grid"].get(crit)
        if not isinstance(cells, dict):
            raise ValueError(f"{grid_path}: grid.{crit} is missing or not a mapping")
        op = comparators.get(crit)
        for variant in g["variants"]:
            cell = cells.get(variant)
            if not isinstance(cell, dict):
                raise ValueError(f"{grid_path}: grid.{crit}.{variant} is missing or not a mapping")
            if cell.get("result") in counts:
                counts[cell["result"]] += 1
            subs = [(f"{variant}/{sym}", c) for sym, c in (cell.get("per_symbol") or {}).items()
                    if isinstance(c, dict)] or [(variant, cell)]
            for where, c in subs:
                if c.get("result") != "FAIL":
                    continue
                value, threshold = _to_float(c.get("value")), _to_float(c.get("threshold"))
                text = (f"{crit} @ {where}: value={c.get('value')} {op or '?'} "
                        f"threshold={c.get('threshold')}")
                fails.append(Criterion(text, "FAIL", op, threshold, value,
                                       "grid" if op else "grid_no_comparator", False))
    # grid CELLS (criterion x variant), not criteria; INCONCLUSIVE cells in "untested"
    row["n_criteria_pass"] = counts["PASS"]
    row["n_criteria_fail"] = counts["FAIL"]
    row["n_criteria_untested"] = counts["INCONCLUSIVE"]
    with_margin = [c for c in fails if c.margin_frac is not None]
    if with_margin:
        worst = max(with_margin, key=lambda c: c.margin_frac)  # closest to 0 = nearest miss
        row["worst_fail_criterion_text"] = worst.raw[:300]
        row["worst_fail_margin_frac"] = round(worst.margin_frac, 4)
        row["worst_fail_margin_source"] = "grid"
    elif fails:
        row["worst_fail_margin_source"] = "grid_cell_without_value_or_comparator"
    return row


def _grid_comparators(run_dir: Path, menu_path: Path | None) -> dict:
    """{criterion_id: comparator} from the run's pre_registration.yaml merged
    against the criterion menu, by the grid evaluator's own resolver."""
    pre_path = run_dir / "artifacts" / "pre_registration.yaml"
    if not pre_path.exists():
        return {}
    import verdict_criteria_evaluator as _vce  # tools/ sibling, lazily for the caller's sys.path
    pre = yaml.safe_load(pre_path.read_text(encoding="utf-8")) or {}
    menu = None
    if menu_path is not None and Path(menu_path).exists():
        menu = yaml.safe_load(Path(menu_path).read_text(encoding="utf-8"))
    out = {}
    for c in _vce._resolve_grid_criteria(pre if isinstance(pre, dict) else {}, menu):
        op = _OP_NORM.get(str(c.get("comparator")))
        if c.get("id") and op:
            out[c["id"]] = op
    return out


def build_row(run_dir: Path, menu_path: Path | None = None) -> dict:
    run_id = run_dir.name
    verdict_path = run_dir / "artifacts" / "verdict_interpretation.yaml"
    grid_path = run_dir / "artifacts" / "grid_evaluation.yaml"
    row = {
        "run_id": run_id,
        "legacy": True,  # E-058 S2b: false only on a grid row
        "idea_status": "not_recorded",
        "hypothesis_id": "not_recorded",
        "hypothesis_family": "not_recorded",
        "evidence_tier": "thin_no_verdict_file",
        "protocol_verdict": "not_recorded",
        "status": "not_recorded",
        "verdict_label_or_disposition": "not_recorded",
        "pipeline_status": "not_recorded",
        "pipeline_stage": "not_recorded",
        "primary_failure_mode_bucket": ["not_recorded"],
        "primary_failure_mode_text": "not_recorded",
        "root_cause_mechanism": "not_recorded",
        "root_cause_confidence": "not_recorded",
        "n_criteria_pass": None,
        "n_criteria_fail": None,
        "n_criteria_untested": None,
        "worst_fail_criterion_text": "not_recorded",
        "worst_fail_margin_frac": None,
        "worst_fail_margin_source": "not_recorded",
        "ic": None,
        "ic_source": "not_recorded",
        "cost_ratio": None,
        "cost_ratio_source": "not_recorded",
        "era_behavior_text": "not_recorded",
        "era_behavior_source": "not_recorded",
    }

    if grid_path.exists():
        return _grid_row(run_dir, grid_path, row, menu_path)

    if not verdict_path.exists():
        ps_path = run_dir / "pipeline_state.yaml"
        if ps_path.exists():
            ps = yaml.safe_load(ps_path.read_text(encoding="utf-8", errors="replace")) or {}
            row["pipeline_status"] = ps.get("status", "not_recorded")
            row["pipeline_stage"] = ps.get("current_stage") or "not_recorded"
        return row

    y = yaml.safe_load(verdict_path.read_text(encoding="utf-8", errors="replace")) or {}

    row["hypothesis_id"] = y.get("hypothesis_id", "not_recorded")
    row["hypothesis_family"] = y.get("hypothesis_family", "not_recorded")
    row["protocol_verdict"] = y.get("protocol_verdict", "not_recorded")
    row["status"] = y.get("status", "not_recorded")

    if "protocol_verdict" in y or "criteria_summary" in y:
        row["evidence_tier"] = "full_protocol"
    elif "verdict_label" in y or "disposition" in y:
        row["evidence_tier"] = "prescreen_only"
        row["verdict_label_or_disposition"] = y.get("verdict_label", y.get("disposition", "not_recorded"))
    else:
        row["evidence_tier"] = "verdict_file_unrecognized_schema"

    pfm = y.get("primary_failure_mode")
    if pfm is None:
        rc = y.get("root_cause") or {}
        pfm = rc.get("mechanism_failure") if isinstance(rc, dict) else None
    if pfm is not None:
        row["primary_failure_mode_text"] = " ".join(str(pfm).split())[:400]
        row["primary_failure_mode_bucket"] = classify_bucket(pfm)
    elif row["evidence_tier"] == "prescreen_only":
        row["primary_failure_mode_text"] = y.get("verdict_label", "not_recorded")
        row["primary_failure_mode_bucket"] = classify_bucket(y.get("verdict_label", ""))

    rc = y.get("root_cause")
    if isinstance(rc, dict):
        row["root_cause_mechanism"] = rc.get("mechanism_failure", "not_recorded")
        row["root_cause_confidence"] = rc.get("confidence", "not_recorded")

    criteria = parse_criteria_summary(y.get("criteria_summary"))
    if criteria:
        row["n_criteria_pass"] = sum(1 for c in criteria if c.result == "PASS")
        row["n_criteria_fail"] = sum(1 for c in criteria if c.result == "FAIL")
        row["n_criteria_untested"] = sum(1 for c in criteria if c.result == "UNTESTED")
        fails_with_margin = [c for c in criteria if c.result == "FAIL" and c.margin_frac is not None]
        if fails_with_margin:
            worst = max(fails_with_margin, key=lambda c: c.margin_frac)  # closest to 0 = nearest miss
            row["worst_fail_criterion_text"] = " ".join(worst.raw.split())[:300]
            row["worst_fail_margin_frac"] = round(worst.margin_frac, 4)
            row["worst_fail_margin_source"] = (
                "text_approx" if worst.compound or "text" in worst.actual_source else "structured"
            )
        elif any(c.result == "FAIL" for c in criteria):
            row["worst_fail_margin_source"] = "unparseable_free_text"

    ic, ic_src, cost, cost_src = extract_ic_cost(y)
    row["ic"] = ic
    row["ic_source"] = ic_src
    row["cost_ratio"] = cost
    row["cost_ratio_source"] = cost_src

    era_text, era_src = extract_era_behavior(y)
    row["era_behavior_text"] = era_text if era_text else "not_recorded"
    row["era_behavior_source"] = era_src

    return row


# --- ranking ----------------------------------------------------------------
_VERDICT_PRIORITY = {"refine": 0, "escalate": 1, "pivot": 2, "kill": 3, "not_recorded": 4}


def _tier_sort_key(row):
    if row["worst_fail_margin_frac"] is not None:
        tier = 0
        key2 = -row["worst_fail_margin_frac"]  # ascending on -margin == descending on margin
    elif row["evidence_tier"] in ("full_protocol", "prescreen_only", "verdict_file_unrecognized_schema",
                                  "grid"):
        tier = 1
        vp = _VERDICT_PRIORITY.get(row["status"], 4)
        key2 = vp
    else:
        tier = 2
        key2 = 0
    ic = row.get("ic")
    ic_key = -(ic if isinstance(ic, (int, float)) else -1e9)
    return (tier, key2, ic_key, row["run_id"])


def rank_rows(rows):
    rows.sort(key=_tier_sort_key)
    for i, r in enumerate(rows, start=1):
        r["rank"] = i


# --- rendering ----------------------------------------------------------------
def _denominator_report(rows):
    n = len(rows)
    lines = [f"Total run dirs scanned: {n}"]
    has_verdict = [r for r in rows if r["evidence_tier"] not in ("thin_no_verdict_file", "grid")]
    lines.append(f"Have a verdict_interpretation.yaml: {len(has_verdict)} of {n}")
    n_grid = sum(1 for r in rows if r["evidence_tier"] == "grid")
    lines.append(f"Have a grid_evaluation.yaml (tier grid, legacy: false): {n_grid} of {n}")
    full = [r for r in rows if r["evidence_tier"] == "full_protocol"]
    prescreen = [r for r in rows if r["evidence_tier"] == "prescreen_only"]
    lines.append(f"  full_protocol schema: {len(full)} of {n}")
    lines.append(f"  prescreen_only schema: {len(prescreen)} of {n}")
    pv_present = sum(1 for r in rows if r["protocol_verdict"] != "not_recorded")
    st_present = sum(1 for r in rows if r["status"] != "not_recorded")
    lines.append(f"protocol_verdict recorded (non-absent, within verdict file): {pv_present} of {n}")
    lines.append(f"status recorded (non-absent, within verdict file): {st_present} of {n}")
    margin = sum(1 for r in rows if r["worst_fail_margin_frac"] is not None)
    lines.append(f"Numeric worst-fail margin recovered: {margin} of {n}")
    ic_n = sum(1 for r in rows if r["ic"] is not None)
    lines.append(f"IC recovered (any source): {ic_n} of {n}")
    cost_n = sum(1 for r in rows if r["cost_ratio"] is not None)
    lines.append(f"Cost ratio recovered (any source): {cost_n} of {n}")
    era_n = sum(1 for r in rows if r["era_behavior_source"] == "text_extracted")
    lines.append(f"Era-behaviour text recovered: {era_n} of {n}")
    return lines


def render_markdown(rows, denom_lines) -> str:
    out = []
    out.append("# Near-miss scoreboard (E-018 S1)")
    out.append("")
    out.append("Ranked table over every tested idea in `runs/`, for the")
    out.append("idea-generation stage to read as raw material only. **Not a")
    out.append("promotion input** -- see `tests/test_near_miss_scoreboard_firewall.py`.")
    out.append("")
    out.append("Ranked BY: numeric near-miss quality first (tier 0 -- FAIL")
    out.append("criteria with a recoverable margin, ordered by the *smallest*")
    out.append("magnitude miss on the run's worst-binding failed criterion --")
    out.append("i.e. the criterion it came closest to passing); then (tier 1)")
    out.append("runs with a verdict but no recoverable numeric margin, ordered")
    out.append("by status (refine > escalate > pivot > kill > absent); then")
    out.append("(tier 2) runs with no verdict file at all, by run_id. Positive")
    out.append("IC is used only as a tie-break within a tier, never as the")
    out.append("primary key.")
    out.append("")
    out.append("## Denominators (MEASURED)")
    out.append("")
    for line in denom_lines:
        out.append(f"- {line}")
    out.append("")
    out.append("## Table")
    out.append("")
    headers = ["rank", "run_id", "hypothesis_family", "evidence_tier", "protocol_verdict",
               "status", "failure_bucket", "worst_fail_margin_frac", "margin_source",
               "root_cause_mechanism", "ic", "cost_ratio", "era_behavior"]
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        bucket = ",".join(r["primary_failure_mode_bucket"]) if isinstance(r["primary_failure_mode_bucket"], list) else r["primary_failure_mode_bucket"]
        era = r["era_behavior_text"]
        if era and era != "not_recorded":
            era = era[:60].replace("|", "/") + ("..." if len(era) > 60 else "")
        cells = [
            r["rank"], r["run_id"], r["hypothesis_family"], r["evidence_tier"],
            r["protocol_verdict"], r["status"], bucket,
            "not_recorded" if r["worst_fail_margin_frac"] is None else r["worst_fail_margin_frac"],
            r["worst_fail_margin_source"],
            r["root_cause_mechanism"],
            "not_recorded" if r["ic"] is None else r["ic"],
            "not_recorded" if r["cost_ratio"] is None else r["cost_ratio"],
            era,
        ]
        out.append("| " + " | ".join(str(c).replace("\n", " ") for c in cells) + " |")
    return "\n".join(out) + "\n"


def build_scoreboard(runs_dir: Path, menu_path: Path | None = None):
    """`menu_path` (config/criterion_menu.yaml) resolves grid comparators;
    default: <runs_dir>/../config/criterion_menu.yaml."""
    runs_dir = Path(runs_dir)
    if menu_path is None:
        menu_path = runs_dir.parent / "config" / "criterion_menu.yaml"
    run_dirs = sorted(
        d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith("run_")
    )
    rows = [build_row(d, menu_path) for d in run_dirs]
    rank_rows(rows)
    return rows


def write_scoreboard(rows, out_dir: Path) -> tuple:
    """Writes <out_dir>/near_miss_scoreboard.{yaml,md}; returns both paths.
    `out_dir` is required -- the regroup_record hook passes it explicitly,
    because STRATEGY_RESEARCH_ROOT is not covered by the test sandbox."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    denom_lines = _denominator_report(rows)
    yaml_path = out_dir / "near_miss_scoreboard.yaml"
    md_path = out_dir / "near_miss_scoreboard.md"
    yaml_doc = {
        "generated_by": "strategy-research/tools/near_miss_scoreboard.py",
        "purpose": "idea-generation raw material ONLY; not a promotion input",
        "denominators": denom_lines,
        "rows": rows,
    }
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(yaml_doc, f, sort_keys=False, allow_unicode=True, width=100)
    md_path.write_text(render_markdown(rows, denom_lines), encoding="utf-8")
    return yaml_path, md_path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs-dir", default=str(STRATEGY_RESEARCH_ROOT / "runs"))
    ap.add_argument("--out-dir", default=str(STRATEGY_RESEARCH_ROOT / "engineering" / "roadmap" / "E-018" / "artifacts"))
    args = ap.parse_args(argv)

    rows = build_scoreboard(Path(args.runs_dir))
    yaml_path, md_path = write_scoreboard(rows, Path(args.out_dir))

    for line in _denominator_report(rows):
        print(line)
    print(f"\nWrote {yaml_path}")
    print(f"Wrote {md_path}")
    print(
        "\nWired (E-058 S2b) into the orchestrator's regroup_record stage, which runs "
        "only under orchestrator.regroup_record.enabled (off by default) and rebuilds "
        "this scoreboard after recording each run. Nothing on the route reads it "
        "(firewall, by review)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
