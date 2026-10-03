"""E-068 slice 2 (CUL-389): the `claim` block step 1a writes, checked by code.

Under orchestrator.claim_tests.enabled only (run_phase1_research wires it;
nothing here reads a flag). Design: engineering/roadmap/E-068/DESIGN_PROPOSAL.md
sections 2, 2.3 and 4. Pure functions, no I/O except append_test_requests.

The claim block (hypothesis_card.yaml `claim`):

    statement     the claim in plain words
    kind          one of CLAIM_KINDS (O-18's closed list)
    tests         1..MAX_TESTS tests composed from the four slots of
                  tools/claim_tests.py (selector, outcome, baseline, statistic,
                  plus direction, floor, optional consistency, and a unique
                  name); or the string "none" when the slots cannot express it
    criteria_refs optional: ids of criteria in the card's own `criteria` list
                  that test the claim (cost, redundancy, robustness kinds)
    missing_block required with tests: none -- the building block that is missing
    pass_if       plain words restating the code's verdict rule; decides nothing
    fail_if       same
    rationale     why these tests answer this claim

The claim is supported only if every test passes (claim_tests.combine,
D-014). `alpha` and `significance` are fixed by code (claim_tests.TestSpec
defaults); the agent may not write them -- fewer knobs, fewer lucky passes.

Regime selectors (claim_tests.NOT_RECOMPUTABLE_SELECTORS) are accepted as
EFFECT-SIZE ONLY (operator, 2026-10-03, CUL-391): every other slot is checked
with check_spec's own rules, and the test is marked verdict_possible: false
with REGIME_REASON. `verdict_possible: true`
means only that no rule of this file excludes a verdict; a verdict still
needs a calibrated significance method (claim_tests operator rule 3).

A claim is INFORMATION ONLY: no check here ever stops, parks or reroutes a run.
`tests: none` (a genuinely missing building block) is recorded as a test
request; a missing or invalid claim is recorded as a gap (claim_test_status.yaml).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import claim_tests as ct  # noqa: E402

CLAIM_KINDS = (
    "regime_classifier", "regime_transition", "direction_forecast", "volatility_forecast",
    "event_behaviour", "conditional_behaviour", "horizon_decay", "calendar_effect",
    "redundancy", "lead_lag", "data_feed_value", "cost_turnover", "robustness",
)
# 1a's claim kind -> the block kind it could become (section 2.3). None: a
# finding only, never a block. Kinds absent here say nothing about the block.
KIND_BLOCK = {
    "regime_classifier": "regime", "regime_transition": "regime",
    "direction_forecast": "forecast", "volatility_forecast": "forecast",
    "calendar_effect": None,
}
CLAIM_KEYS = {"statement", "kind", "tests", "criteria_refs", "missing_block",
              "pass_if", "fail_if", "rationale"}
TEXT_KEYS = ("statement", "pass_if", "fail_if", "rationale")
TEST_KEYS = {"name", "selector", "outcome", "baseline", "statistic", "direction",
             "floor", "consistency"}
CODE_FIXED_KEYS = ("alpha", "significance")
MAX_TESTS = 3
NO_TEST = "none"
REGIME_REASON = "no calibrated significance method for regime selectors"
TEST_REQUESTS_REL = "campaign_record/test_requests.yaml"


@dataclass
class ClaimCheck:
    errors: list = field(default_factory=list)     # non-empty -> 1a retry
    tests_none: bool = False                        # tests: none (a missing block)
    missing_block: str | None = None
    tests: list = field(default_factory=list)       # per test: name, spec_hash, verdict_possible, reason

    def record(self) -> dict:
        return {"errors": list(self.errors), "tests_none": self.tests_none,
                "missing_block": self.missing_block, "tests": list(self.tests)}


def _text(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _baseline_selector(test: dict):
    """The baseline's own selector -- read only for `other_selector`, the one
    baseline that has one (a stray `selector` on another baseline is ignored
    by the engine, so it must not change the verdict flag either)."""
    base = test.get("baseline")
    if isinstance(base, dict) and base.get("kind") == "other_selector":
        return base.get("selector")
    return None


def _regime_selector_paths(test: dict) -> list:
    """(where, kind) for every selector of this test that is a regime selector,
    with `where` named exactly as claim_tests.check_spec names it."""
    out = []
    sel = test.get("selector")
    if isinstance(sel, dict) and sel.get("kind") in ct.NOT_RECOMPUTABLE_SELECTORS:
        out.append(("selector", sel["kind"]))
    sub = _baseline_selector(test)
    if isinstance(sub, dict) and sub.get("kind") in ct.NOT_RECOMPUTABLE_SELECTORS:
        out.append(("baseline.selector", sub["kind"]))
    return out


def _check_test(test, where: str) -> tuple:
    """(errors, spec_hash or None, verdict_possible)."""
    if not isinstance(test, dict):
        return [f"{where}: a test must be a mapping"], None, False
    errors = []
    fixed = [k for k in CODE_FIXED_KEYS if k in test]
    if fixed:
        errors.append(f"{where}: {fixed} are fixed by code (alpha 0.05, the calibrated "
                      f"significance method); remove them")
    unknown = sorted(set(test) - TEST_KEYS - set(CODE_FIXED_KEYS))
    if unknown:
        errors.append(f"{where}: unknown keys {unknown}; allowed: {sorted(TEST_KEYS)}")
    missing = sorted(k for k in TEST_KEYS - {"consistency", "baseline"} if k not in test)
    if missing:
        errors.append(f"{where}: missing {missing}")
    if errors:
        return errors, None, False
    if not _text(test["name"]):
        return [f"{where}: name must be a non-empty string"], None, False
    spec_dict = {k: test.get(k) for k in TEST_KEYS - {"name"} if k in test}
    spec_dict.setdefault("baseline", None)
    try:
        spec = ct.TestSpec.from_dict(spec_dict)
    except (TypeError, ValueError) as exc:
        return [f"{where}: {exc}"], None, False
    regime = _regime_selector_paths(test)
    # check_spec refuses a regime selector under every method; that one
    # refusal is replaced by verdict_possible: false. Matched on check_spec's
    # own message prefix: if its wording changes, the refusal stays (fail
    # loud) and tests/test_e068_s2_claim_card.py fails.
    allowed = tuple(f"{w}: {k} cannot be graded under " for w, k in regime)
    try:
        # an LLM slip (a list where a scalar belongs, an int where a list
        # belongs) can make check_spec itself raise: a refusal, never a crash
        errs = [e for e in ct.check_spec(spec) if not (allowed and e.startswith(allowed))]
        if errs:
            return [f"{where}: {e}" for e in errs], None, False
        h = ct.spec_hash(spec)
    except (TypeError, ValueError, AttributeError, KeyError) as exc:
        return [f"{where}: malformed test ({type(exc).__name__}: {exc})"], None, False
    return [], h, not regime


def check_claim(claim, criteria_ids=()) -> ClaimCheck:
    """Static checks of 1a's claim block, before any spend. criteria_ids: the
    ids of the card's own `criteria` list (criteria_refs must name them)."""
    res = ClaimCheck()
    e = res.errors
    if not isinstance(claim, dict):
        e.append("claim: a `claim` mapping is required in hypothesis_card.yaml")
        return res
    unknown = sorted(set(claim) - CLAIM_KEYS)
    if unknown:
        e.append(f"claim: unknown keys {unknown}; allowed: {sorted(CLAIM_KEYS)}")
    for k in TEXT_KEYS:
        if not _text(claim.get(k)):
            e.append(f"claim.{k}: a non-empty string is required")
    if claim.get("kind") not in CLAIM_KINDS:
        e.append(f"claim.kind: {claim.get('kind')!r} is not one of {list(CLAIM_KINDS)}")
    tests = claim.get("tests")
    refs = claim.get("criteria_refs")
    if refs is not None:
        known = set(criteria_ids or ())
        if (not isinstance(refs, list) or not refs
                or any(not isinstance(r, str) for r in refs) or len(set(refs)) != len(refs)):
            e.append("claim.criteria_refs: a non-empty list of distinct criterion ids")
        else:
            bad = [r for r in refs if r not in known]
            if bad:
                e.append(f"claim.criteria_refs: {bad} are not in this card's `criteria` "
                         f"list (ids: {sorted(known)})")
    if tests == NO_TEST:
        if refs is not None:
            e.append("claim: tests: none with criteria_refs -- the claim is tested by "
                     "those criteria, so drop `tests: none` (or the refs)")
        if not _text(claim.get("missing_block")):
            e.append("claim.missing_block: required with tests: none -- name the missing "
                     "building block (CLAIM_TESTS.md)")
        if not e:
            res.tests_none = True
            res.missing_block = claim["missing_block"].strip()
        return res
    if "missing_block" in claim:
        e.append("claim.missing_block: only allowed with tests: none")
    if tests is None and refs is not None:
        return res
    if not isinstance(tests, list) or not 1 <= len(tests) <= MAX_TESTS:
        e.append(f"claim.tests: a list of 1 to {MAX_TESTS} tests, or `none` (with "
                 f"missing_block), or omit it and use criteria_refs")
        return res
    names = [t.get("name") for t in tests if isinstance(t, dict)]
    if any(not isinstance(n, str) for n in names):
        e.append("claim.tests: every test name must be a string")
    elif len(set(names)) != len(names):
        e.append("claim.tests: every test needs a unique name")
    for i, t in enumerate(tests):
        errs, h, possible = _check_test(t, f"claim.tests[{i}]")
        e.extend(errs)
        if not errs:
            res.tests.append({"name": t["name"], "spec_hash": h, "verdict_possible": possible,
                              **({} if possible else {"reason": REGIME_REASON})})
    if e:
        res.tests = []
    return res


def card_criteria_ids(card: dict) -> list:
    crit = card.get("criteria") if isinstance(card, dict) else None
    return [c["id"] for c in crit or [] if isinstance(c, dict) and isinstance(c.get("id"), str)]


# ---------------------------------------------------------------------------
# 1a/1b match check (section 2.3): a warning, never a stop
# ---------------------------------------------------------------------------

def _selector_columns(sel) -> set:
    if not isinstance(sel, dict):
        return set()
    if sel.get("kind") in ("regime", "regime_change"):
        return {"regime"}
    if sel.get("kind") in ("event", "quantile") and sel.get("field") == "forecast":
        return {"forecast"}
    return set()


def signal_columns(test: dict) -> set:
    """The block-produced columns a test reads: `forecast` (a selector field,
    or rank_ic, which correlates the forecast) and/or `regime`."""
    cols = _selector_columns(test.get("selector")) | _selector_columns(_baseline_selector(test))
    if test.get("statistic") == "rank_ic":
        cols.add("forecast")
    return cols


def expected_block(columns: set):
    """regime anywhere -> regime block; forecast -> forecast block; neither ->
    None (a finding only)."""
    if "regime" in columns:
        return "regime"
    if "forecast" in columns:
        return "forecast"
    return None


def match_check(claim: dict, manifest_kind) -> list:
    """Warnings (dicts) comparing 1a's claim with 1b's manifest kind. Empty
    when they agree. Never raises on content: this is information only."""
    warnings = []
    tests = claim.get("tests") if isinstance(claim, dict) else None
    for t in tests if isinstance(tests, list) else []:
        if not isinstance(t, dict):
            continue
        cols = sorted(signal_columns(t))
        want = expected_block(set(cols))
        if want != manifest_kind:
            warnings.append({
                "check": "test_reads_vs_block_kind", "test": t.get("name"),
                "test_reads": cols, "expected_block": want, "manifest_kind": manifest_kind,
                "meaning": ("the test does not read this block's output; it measures the "
                            "strategy's signal or price behaviour instead")})
    kind = claim.get("kind") if isinstance(claim, dict) else None
    if kind in KIND_BLOCK and KIND_BLOCK[kind] != manifest_kind:
        warnings.append({
            "check": "claim_kind_vs_block_kind", "claim_kind": kind,
            "expected_block": KIND_BLOCK[kind], "manifest_kind": manifest_kind,
            "meaning": "1a's claim kind and 1b's block kind disagree; 1b's manifest decides"})
    return warnings


# ---------------------------------------------------------------------------
# Power warning (operator, 2026-10-03): can the floor be reached at all?
# ---------------------------------------------------------------------------

_TF_UNIT = {"m": 60, "h": 3600, "d": 86400, "w": 7 * 86400}


def timeframe_seconds(tf) -> int | None:
    """'15m' -> 900, '1h' -> 3600, '4h' -> 14400, '1d' -> 86400; None if unknown."""
    if not isinstance(tf, str) or len(tf) < 2 or tf[-1] not in _TF_UNIT or not tf[:-1].isdigit():
        return None
    return int(tf[:-1]) * _TF_UNIT[tf[-1]]


def window_bars(windows: list, step: int) -> int:
    """Bars in the test windows: each window's days (end inclusive, the
    engine's convention) times bars per day."""
    from datetime import date
    total = 0
    for w in windows:
        t = w.get("test") if isinstance(w, dict) else None
        if not isinstance(t, dict):
            raise ValueError(f"window {w!r} has no test.start/test.end")
        days = (date.fromisoformat(str(t["end"])[:10])
                - date.fromisoformat(str(t["start"])[:10])).days + 1
        total += days * 86400 // step
    return total


def power_warnings(claim: dict, total_bars: int, n_coins: int) -> list:
    """For every test with a min_events floor: the upper bound of separate
    events = (bars in the test windows // the longest horizon) x coins. One
    dict per test whose bound is below its floor (empty: every floor is
    reachable). An upper bound: the selector picks fewer bars, never more."""
    out = []
    tests = claim.get("tests") if isinstance(claim, dict) else None
    for t in tests if isinstance(tests, list) else []:
        floor = (t.get("floor") or {}).get("min_events") if isinstance(t, dict) else None
        hs = ((t.get("outcome") or {}).get("horizons") or []) if isinstance(t, dict) else []
        if not isinstance(floor, int) or not hs:
            continue
        h_max = max(hs)
        bound = (total_bars // h_max) * n_coins
        if bound < floor:
            out.append({"test": t.get("name"), "bound": bound, "floor": floor,
                        "bars": total_bars, "longest_horizon": h_max, "coins": n_coins,
                        "message": (f"test {t.get('name')!r}: at most {bound} separate events "
                                    f"are possible, the floor is {floor}: shorten the horizon "
                                    f"or widen the data")})
    return out


# ---------------------------------------------------------------------------
# test_requests.yaml (card J pattern) and the coverage record -- information
# only: neither ever stops, parks or reroutes a run.
# ---------------------------------------------------------------------------

COVERAGE_REL = "campaign_record/claim_test_coverage.yaml"
# Why a run has no usable claim test (claim_test_status.yaml `reason`).
GAP_REASONS = ("no_claim", "invalid_claim", "tests_none", "criteria_refs_only",
               "exempt", "check_error")


def test_request_key(rec: dict) -> tuple:
    return (rec.get("run_id"), rec.get("hypothesis_id"), rec.get("missing_block"))


test_request_key.__test__ = False  # not a pytest test


def append_test_requests(root: Path, rows: list) -> int:
    """Append-only, locked, idempotent per (run_id, hypothesis_id,
    missing_block): a re-run adds no duplicate row. Same appender as
    data/component requests (tools/campaign_review_retired.append_requests)."""
    import campaign_review_retired as crr
    return crr.append_requests(Path(root) / TEST_REQUESTS_REL, rows, key=test_request_key)


append_test_requests.__test__ = False


def status_of(res, exempt: str | None, power: list) -> dict:
    """The run's claim-test status from its card's check: usable (at least one
    valid slot test) or the gap reason. Information only."""
    if exempt:
        return {"usable": False, "reason": "exempt", "detail": exempt}
    if res is None:
        return {"usable": False, "reason": "check_error", "detail": "no result"}
    if res.errors:
        missing = any("a `claim` mapping is required" in e for e in res.errors)
        return {"usable": False, "reason": "no_claim" if missing else "invalid_claim",
                "detail": "; ".join(res.errors)}
    if res.tests_none:
        return {"usable": False, "reason": "tests_none", "detail": res.missing_block}
    if not res.tests:
        return {"usable": False, "reason": "criteria_refs_only",
                "detail": "the claim is tested only by the card's own menu criteria"}
    out = {"usable": True, "reason": None, "detail": None, "tests": list(res.tests)}
    if power:
        out["power_warnings"] = list(power)
    return out


def record_coverage(root: Path, run_id: str, status: dict) -> None:
    """campaign_record/claim_test_coverage.yaml {runs: {run_id: {...}}}: the
    run's latest claim-test status, so the campaign summary can count the runs
    without a usable claim test and why. Locked, atomic, one row per run."""
    import campaign_memory as cm
    import campaign_review_retired as crr
    path = Path(root) / COVERAGE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with crr._lock(path, path.name):
        doc = crr._load_mapping(path, {})
        runs = doc.get("runs") if isinstance(doc.get("runs"), dict) else {}
        old = runs.get(run_id) if isinstance(runs.get(run_id), dict) else {}
        runs[run_id] = {"usable": bool(status.get("usable")), "reason": status.get("reason"),
                        "power_warning": bool(status.get("power_warnings")),
                        # slice 3's count of measured tests is kept: those looks
                        # were taken, whatever the card check says later
                        **({"measured": old["measured"]} if "measured" in old else {})}
        cm._atomic_write(path, {**doc, "runs": runs})


def coverage_summary_lines(root: Path) -> list:
    """Campaign-summary lines; [] when the coverage file does not exist (so a
    summary is unchanged until a claim-test run has been checked)."""
    path = Path(root) / COVERAGE_REL
    if not path.exists():
        return []
    import yaml
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError, UnicodeDecodeError) as exc:   # never break the summary
        return ["", "## Claim tests (E-068, information only)", "",
                f"- {COVERAGE_REL} is unreadable ({type(exc).__name__}); fix or remove it."]
    runs = doc.get("runs") if isinstance(doc, dict) and isinstance(doc.get("runs"), dict) else {}
    usable = sorted(r for r, v in runs.items() if isinstance(v, dict) and v.get("usable"))
    gaps = {}
    for r, v in sorted(runs.items()):
        # a row holding only a slice-3 measurement (its card check never
        # recorded) is not a card gap
        if isinstance(v, dict) and "usable" in v and not v.get("usable"):
            gaps.setdefault(str(v.get("reason")), []).append(r)
    floor = sorted(r for r, v in runs.items() if isinstance(v, dict) and v.get("power_warning"))
    lines = ["", "## Claim tests (E-068, information only)", "",
             f"- Runs with a usable claim test: {len(usable)}",
             f"- Runs without one: {sum(len(v) for v in gaps.values())}"]
    for reason, rs in sorted(gaps.items()):
        lines.append(f"  - {reason}: {len(rs)} ({', '.join(rs)})")
    if floor:
        lines.append(f"- Runs whose floor cannot be reached (power warning): {len(floor)} "
                     f"({', '.join(floor)})")
    # E-068 slice 3 (CUL-393): the measurements after the backtests (absent
    # until a run has been measured, so the lines above are unchanged until then).
    measured = {r: v["measured"] for r, v in sorted(runs.items())
                if isinstance(v, dict) and isinstance(v.get("measured"), dict)}
    if measured:
        # every test ever measured (looks accumulate across a run's attempts)
        n_tests = sum(int(m.get("n_looks", m.get("n_tests_measured")) or 0)
                      for m in measured.values())
        done = [r for r, m in measured.items() if m.get("claim_status") == "measured"]
        lines.append(f"- Claim tests measured after the backtests (effect sizes, measured, "
                     f"not proven): {n_tests} test(s) in {len(done)} run(s)"
                     + (f" ({', '.join(done)})" if done else "")
                     + f"; runs not measured: {len(measured) - len(done)}")
    return lines
