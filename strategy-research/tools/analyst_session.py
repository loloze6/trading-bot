"""E-075 PR-5 (CUL-423, D-092): the analyst session's pure part -- no SDK, no model call.

run_phase1_research wires the session (the six tools as an in-process MCP server, the
closed-book options, the deny hook, the call); this module holds everything that can be
checked without a model:

  build_prompt(...)      the analyst's prompt: its skill and lens text, the run context, the
                         data dictionary, the claim-test vocabulary, the memory view
  check_answer(...)      the model's answer -> (a v3 reading in the reader-proposal shape,
                         the session record, errors). Code checks the claim, every citation
                         against the query log, that each claim test was really run with
                         conditional_effect, that the "why" query is a call of the session,
                         and that no date at or after the holdout start appears
  in_run_score(...)      the simple code score (operator, 2026-10-08): the claim's in-run
                         window agreement, 0..3; the other two scores fixed at 1

Design: engineering/roadmap/E-075/PR5_DESIGN.md (sections 3-5 and 11).

Why this cannot leak: the analyst reads this run's own bars and trades through
tools/analyst_queries.py only (which refuses any bar at or after the holdout start and any
path outside the run); this module reads the query log the engine wrote, the run's own
config/protocol files, repo docs and the campaign memory view, and refuses an answer naming a
date at or after the holdout start.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

SR_ROOT = Path(_HERE).parent

#: lens -> the reader category file it writes (artifacts/proposals/<category>.yaml); the
#: other reader categories are written by code as `skipped` (replaced_by_analyst)
LENS_CATEGORY = {"forecast": "forecast_power", "trade_efficiency": "trade_efficiency"}
LENSES = tuple(LENS_CATEGORY)
REPLACED_RULE = "replaced_by_analyst"
SERVER_NAME = "analyst"
TOOL_NAMES = ("list_columns", "describe", "distribution", "conditional_effect", "trade_slice",
              "event_study")
ALLOWED_TOOLS = tuple(f"mcp__{SERVER_NAME}__{n}" for n in TOOL_NAMES)
SKILL_DIR = SR_ROOT / "workflow_artifacts" / "skills" / "analyst"
LOG_DIR_REL = "artifacts/analyst_queries"
RECORD_DIR_REL = "artifacts/analyst"
ANSWER_KEYS = {"claim": {"outcome", "claim", "why_query", "evidence", "vehicle", "combines_as"},
               "no_claim": {"outcome", "no_claim", "evidence"}}
_CITE_RE = re.compile(r"^(q[0-9]+):([A-Za-z0-9_.\-/<>]+)=(.+)$")
_DATE_RE = re.compile(r"(?<!\d)(\d{4})-(\d{2})(?:-(\d{2}))?(?!\d)")
FIXED_SCORE = 1            # distance_to_profitable and mechanism_plausibility (no self-score)


def log_rel(lens: str) -> str:
    return f"{LOG_DIR_REL}/{lens}.yaml"


def record_rel(lens: str) -> str:
    return f"{RECORD_DIR_REL}/{lens}.yaml"


def rubric(category: str) -> str:
    import reader_proposals as rp
    return rp.ANALYST_RUBRIC_VERSIONS[category]


# ---------------------------------------------------------------------------
# The prompt
# ---------------------------------------------------------------------------

def _read(path: Path) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return None


def _section(title: str, body: str | None) -> str:
    return f"\n\n## {title}\n\n" + (body.strip() if body else "(absent)")


def run_context(run_dir: Path, base_config_rel: str, fold: str | None) -> str:
    """The run context as text: the base config, the variant patches, the protocol (coins,
    timeframe, windows), the fold, the cost model. Absent files are said to be absent."""
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    parts = [f"Run: {run_dir.name}", f"Fold of this run: {fold or '(none registered)'}"]
    proto = _read(arts / "variants" / "run_protocol.json")
    if proto:
        try:
            p = json.loads(proto)
            parts.append(f"Coins: {p.get('symbols')}; timeframe: {p.get('timeframe')}")
            parts.append("Windows: " + ", ".join(
                f"{w.get('label')} {((w.get('test') or {}).get('start'))}..{((w.get('test') or {}).get('end'))}"
                for w in p.get("windows") or []))
        except ValueError:
            parts.append("run_protocol.json: unreadable")
    out = "\n".join(parts)
    out += _section(f"Base strategy config ({base_config_rel})", _read(run_dir / base_config_rel))
    out += _section("Variant patches (artifacts/variant_patches.yaml)",
                    _read(arts / "variant_patches.yaml"))
    out += _section("Cost model (config/cost_model.yaml; for reference only)",
                    _read(SR_ROOT / "config" / "cost_model.yaml"))
    return out


def build_prompt(lens: str, run_dir: Path, *, base_config_rel: str, fold: str | None,
                 memory_view: dict) -> str:
    """The analyst's whole prompt (the session has no file tool: what it reads is here)."""
    if lens not in LENS_CATEGORY:
        raise ValueError(f"unknown lens {lens!r} (one of {list(LENSES)})")
    hs = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design"
    text = (_read(SKILL_DIR / "SKILL.md") or "") + "\n\n" + (_read(SKILL_DIR / f"{lens}.md") or "")
    text += _section("The run context", run_context(run_dir, base_config_rel, fold))
    text += _section("The data dictionary (docs/DATA_DICTIONARY.md)",
                     _read(SR_ROOT / "docs" / "DATA_DICTIONARY.md"))
    for name in ("CLAIM_TESTS.md", "CLAIM_TESTS_TRADE.md", "CLAIM_TESTS_EXECUTION.md"):
        text += _section(f"Claim-test vocabulary: {name}", _read(hs / name))
    text += _section("The memory view (earlier claims; numbers only for confirmed ones)",
                     yaml.safe_dump(memory_view, sort_keys=False, allow_unicode=True))
    text += _section("Your tools", "\n".join(
        f"- {full} (call it by that name)" for full in ALLOWED_TOOLS))
    return text


# ---------------------------------------------------------------------------
# Reading the answer
# ---------------------------------------------------------------------------

MAX_ANSWER_DEPTH = 40


def _depth(node) -> int:
    """Nesting depth of a parsed answer, without recursion (a deep answer must not crash the
    checks that serialise it)."""
    deepest, stack = 0, [(node, 1)]
    while stack:
        cur, d = stack.pop()
        deepest = max(deepest, d)
        if d > MAX_ANSWER_DEPTH:
            break
        if isinstance(cur, dict):
            stack.extend((v, d + 1) for v in cur.values())
        elif isinstance(cur, list):
            stack.extend((v, d + 1) for v in cur)
    return deepest


_YAML_BLOCK = re.compile(r"```ya?ml[^\n]*\n(.*?)```", re.DOTALL)


def parse_answer(text: str):
    """(answer dict, None) or (None, error): exactly one fenced YAML block, a mapping with an
    `outcome` of claim / no_claim and exactly that outcome's keys."""
    blocks = _YAML_BLOCK.findall(text or "")
    if len(blocks) != 1:
        return None, f"the answer holds {len(blocks)} fenced YAML block(s); write exactly one"
    try:
        doc = yaml.safe_load(blocks[0])
    except (yaml.YAMLError, ValueError, RecursionError) as exc:
        # ValueError: an integer past Python's digit limit; RecursionError: deep nesting
        return None, f"the answer is not readable YAML: {type(exc).__name__}: {str(exc)[:200]}"
    if _depth(doc) > MAX_ANSWER_DEPTH:
        return None, f"the answer nests deeper than {MAX_ANSWER_DEPTH} levels"
    if not isinstance(doc, dict) or not isinstance(doc.get("outcome"), str) \
            or doc["outcome"] not in ANSWER_KEYS:
        return None, "the answer must be a mapping with outcome: claim or outcome: no_claim"
    want = ANSWER_KEYS[doc["outcome"]]
    if set(doc) != want:
        return None, (f"an answer with outcome {doc['outcome']} has exactly the keys "
                      f"{sorted(want)} (got {sorted(doc)})")
    return doc, None


def _walk_path(result, path: str):
    node = result
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
            node = node[int(part)]
        else:
            raise KeyError(part)
    return node


def _same_value(logged, cited: str) -> bool:
    if isinstance(logged, bool) or logged is None:
        return str(logged).lower() == cited.strip().lower()
    if isinstance(logged, (int, float)):
        try:
            c = float(cited)
        except ValueError:
            return False
        if not math.isfinite(c):
            return False
        return float(f"{float(logged):.8g}") == float(f"{c:.8g}")
    return str(logged) == cited.strip()


def check_citations(cites, entries: dict) -> list:
    """Errors of the `evidence` list: each item `q<n>:<dotted path>=<value>`; the id is an `ok`
    entry of this session's log, the path exists in its logged result, and the value equals
    the logged one (numbers at the log's 8 significant digits)."""
    if not isinstance(cites, list) or not cites:
        return ["evidence must be a non-empty list of `q<n>:<path>=<value>` citations"]
    errors = []
    for c in cites:
        m = _CITE_RE.match(str(c).strip()) if isinstance(c, str) else None
        if not m:
            errors.append(f"citation {c!r} is not `q<n>:<path>=<value>`")
            continue
        qid, path, value = m.groups()
        e = entries.get(qid)
        if e is None or e.get("status") != "ok":
            errors.append(f"citation {c!r}: {qid} is not a successful call of this session")
            continue
        try:
            logged = _walk_path(e.get("result"), path)
        except KeyError:
            errors.append(f"citation {c!r}: {qid}'s result has no {path!r}")
            continue
        if not _same_value(logged, value):
            errors.append(f"citation {c!r}: {qid} returned {logged!r} at {path!r}")
    return errors


def sealed_dates(text: str, holdout_start: str) -> list:
    """Dates (YYYY-MM or YYYY-MM-DD) in `text` at or after the holdout start's month."""
    bound = holdout_start[:7]
    return sorted({m.group(0) for m in _DATE_RE.finditer(text or "")
                   if f"{m.group(1)}-{m.group(2)}" >= bound})


def conditional_effect_hashes(entries: dict) -> dict:
    """{spec_hash: [query ids]} of the session's successful conditional_effect calls."""
    out: dict = {}
    for qid, e in entries.items():
        if e.get("function") == "conditional_effect" and e.get("status") == "ok":
            h = (e.get("result") or {}).get("spec_hash")
            if h:
                out.setdefault(h, []).append(qid)
    return out


_UNIT_FLOOR = {"min_events": 1}


def floorless_hash(test) -> str | None:
    """The identity of a test with its floor set aside (D-094): spec_hash with the floor
    replaced by {min_events: 1}, so a run without a floor keeps its own spec_hash. The floor
    never changes a measured number (claim_tests.effect_sizes does not read it; downstream it
    is information, claim_measure's floor_not_met), so runs of one test under different floors
    are one observation. The block is read as claim_card._check_test
    reads it (`baseline` may be left out: None). None when the block does not parse."""
    if not isinstance(test, dict):
        return None
    import claim_tests as ct
    spec = {k: v for k, v in test.items() if k != "name"}
    spec.setdefault("baseline", None)
    spec["floor"] = dict(_UNIT_FLOOR)
    try:
        return ct.spec_hash(ct.TestSpec.from_dict(spec))
    except (TypeError, ValueError, KeyError, OverflowError):
        return None


def runs_by_test(entries: dict) -> dict:
    """{floorless test identity: [query ids]} of the session's successful conditional_effect
    calls (an entry whose block does not parse falls back to its own spec_hash)."""
    out: dict = {}
    for qid, e in entries.items():
        if e.get("function") == "conditional_effect" and e.get("status") == "ok":
            res = e.get("result") or {}
            k = floorless_hash(res.get("test")) or res.get("spec_hash")
            if k:
                out.setdefault(k, []).append(qid)
    return out


def opposite_horizons(entry: dict) -> list:
    """[(horizon, windows_claimed_sign, windows_with_value)] of the horizons of a
    conditional_effect run whose `oriented` effect (positive = the claimed direction) is
    strictly below 0; [] if none (exactly 0 or no value is not opposite; a run with no valued
    horizon is never opposite). ANY horizon, not all: fold B (tools/fold_confirm.py) refuses a
    test whose pooled sign fails at any judged horizon, so the in-run rule matches it.
    Smoke 2 (2026-10-09): a claim written `direction: greater` whose own run measured the
    opposite was accepted, scored 0 and would be graded not confirmed on fold B, yet
    decide-next would still spend a child run."""
    hs = ((entry.get("result") or {}).get("horizons")) or {}
    valued = [(hz, v) for hz, v in hs.items()
              if isinstance(v, dict) and isinstance(v.get("oriented"), (int, float))
              and not isinstance(v.get("oriented"), bool)]
    return [(hz, v.get("windows_claimed_sign"), v.get("windows_with_value"))
            for hz, v in valued if v["oriented"] < 0]


def in_run_score(test_hashes: list, entries: dict) -> int:
    """confidence_real, 0..3 (operator, 2026-10-08): for each claim test, the share of windows
    with the claimed sign in the conditional_effect call that ran that test (its weakest
    horizon, and the lowest over every run of that test); the lowest over the tests; 1.0 -> 3,
    >= 0.8 -> 2, >= 0.6 -> 1, else 0. An
    exploratory number: it only ORDERS candidates, confirmation stays on the unseen fold.
    `test_hashes` are floorless identities (floorless_hash): a run under another floor is
    the same test, so choosing a floor cannot drop a weaker run from the minimum (D-094)."""
    by_hash = runs_by_test(entries)
    shares = []
    for h in test_hashes:
        best = None
        for qid in by_hash.get(h, []):
            hz = ((entries[qid].get("result") or {}).get("horizons") or {}).values()
            # a horizon with no window value counts as no agreement, never as skipped
            vals = [x.get("windows_claimed_sign", 0) / x["windows_with_value"]
                    if x.get("windows_with_value") else 0.0 for x in hz]
            if vals:
                share = min(vals)
                # the lowest over every run of the test (any variant, any `by`): repeating a
                # test cannot raise its score (review of #359)
                best = share if best is None else min(best, share)
        shares.append(best if best is not None else 0.0)
    s = min(shares) if shares else 0.0
    return 3 if s >= 1.0 else 2 if s >= 0.8 else 1 if s >= 0.6 else 0


def tool_list_errors(init_tools) -> list:
    """Errors of the tool list the CLI reported for the session (system/init `tools`): it must
    be present, a list, and name no tool outside the six (PHASE_A section 1.4 (b): fail
    closed). Not verifiable from the Python source; the smoke session checks it live."""
    if not isinstance(init_tools, list):
        return [f"the session reported no tool list (system/init tools={init_tools!r})"]
    extra = sorted({str(t) for t in init_tools} - set(ALLOWED_TOOLS))
    if extra:
        return [f"the session had tools outside the six: {extra}"]
    return []


WHY_FUNCTIONS = ("conditional_effect", "trade_slice", "event_study")
PROSE_KEYS = ("statement", "pass_if", "fail_if", "rationale")
# A number standing on its own: `24h`, `9.9pct`, `.5`, `1,234` and `1.2e-3` count; a number glued
# after a word character (`past_return_24`, `run_074`) is a name. A sign counts when it stands
# at the start or after a non-word character ("-1.2%", not "post-24").
_PROSE_NUMBER_RE = re.compile(
    r"(?<![\w.])([-+\u2212]?)(\d{1,3}(?:,\d{3})+|\d*\.\d+|\d+)(?:[eE]([-+]?\d+))?(%?)")


def _ok_call(entries: dict, qid) -> bool:
    """A successful call of this session (a non-string id is never one)."""
    return isinstance(qid, str) and (entries.get(qid) or {}).get("status") == "ok"


def _cite_parts(c):
    m = _CITE_RE.match(c.strip()) if isinstance(c, str) else None
    return m.groups() if m else (None, "", None)


def _cite_qid(c):
    return _cite_parts(c)[0]


def _cite_path(c) -> str:
    return _cite_parts(c)[1]


def _tests_of(claim) -> list:
    tests = claim.get("tests") if isinstance(claim, dict) else None
    return [t for t in tests if isinstance(t, dict)] if isinstance(tests, list) else []


def _selector_of(entry: dict):
    return (((entry.get("result") or {}).get("test")) or {}).get("selector")


def _test_numbers(node, out: set) -> set:
    """The finite numbers written in the claim's test blocks (horizons, lookbacks, floors,
    selector values). Python ints are kept exact (a huge one never overflows)."""
    if isinstance(node, bool):
        return out
    if isinstance(node, int):
        out.add(node)
    elif isinstance(node, float):
        if math.isfinite(node):
            out.add(node)
    elif isinstance(node, dict):
        for v in node.values():
            _test_numbers(v, out)
    elif isinstance(node, list):
        for v in node:
            _test_numbers(v, out)
    return out


def _sig_digits(mantissa: str) -> int:
    """Significant digits a prose number shows: every digit after the leading zeros
    ("100" shows 3, "0.0120" shows 3, "0" shows 1)."""
    return max(1, len(mantissa.replace(",", "").replace(".", "").lstrip("0")))


def _rounds_to(value: float, shown: float, sd: int) -> bool:
    try:
        return float(f"{value:.{sd}g}") == float(f"{shown:.{sd}g}")
    except (OverflowError, ValueError):
        return False


def prose_number_errors(fields: dict, evidence, entries: dict, tests=None) -> list:
    """Every number written in the answer's prose must be one the session saw (review of
    #359: free-text numbers were never checked, and the claim's rationale or the no-claim
    reason becomes the reading's explanation). `fields`: {label: text}. A number passes when
      * it is 0 (as written), or 100%;
      * it is a horizon of a cited `horizons.<h>.` path, or a number of the claim's own test
        blocks, written exactly (all its digits, no sign, no %, no exponent). Known gap: a
        unit in words is not read, so "5 bps" passes when 5 is a number of the test;
      * or it rounds a value cited in `evidence` (each citation already checked against the
        log) to the digits it shows; `x%` is x/100 (or x); a written sign must match the
        cited sign, an unsigned number is compared without sign ("0.08% lower" for -0.0008).
    """
    cited, horizons = [], set()
    for c in evidence or []:
        qid, path, value = _cite_parts(c)
        if not _ok_call(entries, qid):
            continue
        parts = path.split(".")
        if len(parts) > 2 and parts[0] == "horizons" and parts[1].isdigit() \
                and len(parts[1]) <= 6:
            horizons.add(int(parts[1]))
        try:
            v = float(value) if value is not None else None
        except (ValueError, OverflowError):
            v = None
        if v is not None and math.isfinite(v):
            cited.append(v)
    exact = horizons | _test_numbers(tests, set())
    errors = []
    for label, text in fields.items():
        if not isinstance(text, str):
            continue
        for m in _PROSE_NUMBER_RE.finditer(text):
            sign, mantissa, exp, pct = m.groups()
            try:
                x = float(mantissa.replace(",", "")) * (10.0 ** int(exp) if exp else 1.0)
            except (ValueError, OverflowError):
                x = math.inf
            if not math.isfinite(x):
                errors.append(f"{label} writes {m.group(0)!r}: not a number you cited")
                continue
            negative = sign in ("-", "\u2212")
            if float(mantissa.replace(",", "")) == 0 or (pct and x == 100 and not sign):
                continue
            # a test's own number or a cited horizon: unsigned and exact only (it is a setting
            # of the test, never an effect)
            if not pct and not exp and not sign and "," not in mantissa and x in exact:
                continue
            sd = _sig_digits(mantissa)
            cands = [x / 100.0, x] if pct else [x]
            if sign:
                ok = any(_rounds_to(a, -c if negative else c, sd) for a in cited for c in cands)
            else:
                ok = any(_rounds_to(abs(a), c, sd) for a in cited for c in cands)
            if ok:
                continue
            if pct and x / 100.0 in exact:
                errors.append(f"{label} writes {m.group(0)!r}: write your test's number as in "
                              f"the test block ({x / 100.0!r}), not as a percent")
                continue
            errors.append(f"{label} writes {m.group(0)!r}, which is not a value you cited in "
                          f"`evidence` nor a number of your test: cite it (as the decimal the "
                          f"tool returned, e.g. 0.0123, or as a percent, 1.23%; bps are not "
                          f"read), or say it in words (\"positive\", \"most windows\")")
    return errors


def check_answer(text: str, *, lens: str, run_id: str, entries: dict, claim_check,
                 holdout_start: str, fold: str | None, model_id: str) -> tuple:
    """(reading, record, errors). `entries`: {id: log entry} of this lens's query log.
    `claim_check(claim)`: claim_card.check_claim with the pipeline's keywords (folds and the
    trade family). The reading is the v3 reader-proposal shape decide-next reads unchanged;
    the record holds what the reading cannot (why_query, the no-claim block, what was
    examined). The vehicle, combines_as, fold_observed and the envelope rules are checked
    afterwards by the orchestrator's reading checks (reader_proposals.check_reading and
    _reading_content_errors), exactly as for a reader's side finding. An answer with 2 or more
    blocks is refused whatever they hold; its last block's other errors are listed after the
    block-count error, so one retry can fix them all."""
    category = LENS_CATEGORY[lens]
    doc, err = parse_answer(text)
    record = {"lens": lens, "category": category, "outcome": None,
              "what_was_examined": sorted(conditional_effect_hashes(entries)),
              "looks": {"calls": len(entries),
                        "comparisons": sum(max(0, int(e.get("n_comparisons") or 0))
                                           for e in entries.values() if e.get("status") == "ok")}}
    if err:
        blocks = _YAML_BLOCK.findall(text or "")
        if len(blocks) < 2:
            return None, record, [err]
        # only the sub-check's errors are kept: its reading and record never leave
        last = check_answer("```yaml\n" + blocks[-1] + "```", lens=lens, run_id=run_id,
                            entries=entries, claim_check=claim_check,
                            holdout_start=holdout_start, fold=fold, model_id=model_id)[2]
        last = last or ["passes this answer check (the reading checks run once it is the "
                        "only block): write only that block"]
        return None, record, [err] + [f"(your last block) {e}" for e in last]
    record["outcome"] = doc["outcome"]
    errors = check_citations(doc.get("evidence"), entries)
    evidence = doc["evidence"] if isinstance(doc.get("evidence"), list) else []
    late = sealed_dates(yaml.safe_dump(doc, allow_unicode=True), holdout_start)
    if late:
        errors.append(f"the answer names date(s) {late}: nothing at or after the research "
                      f"period's end may be written")
    rid = f"{category}-{run_id}"
    base = {"schema_version": 3, "reading_id": rid, "model_id": model_id,
            "rubric_version": rubric(category)}
    if doc["outcome"] == "no_claim":
        nc = doc.get("no_claim")
        if not isinstance(nc, dict) or not isinstance(nc.get("reason"), str) or not nc["reason"].strip():
            errors.append("no_claim needs a non-empty `reason`")
        br = (nc or {}).get("best_rejected") if isinstance(nc, dict) else None
        if not isinstance(br, dict) or not isinstance(br.get("statement"), str) \
                or not _ok_call(entries, br.get("killed_by")):
            errors.append("no_claim needs best_rejected {statement, killed_by: an ok query id "
                          "of this session}")
        if isinstance(nc, dict):
            errors += prose_number_errors(
                {"no_claim.reason": nc.get("reason"),
                 "no_claim.best_rejected.statement": br.get("statement")
                 if isinstance(br, dict) else None}, evidence, entries)
        record["no_claim"] = nc
        reading = {**base, "explanation": str((nc or {}).get("reason") or "no claim"),
                   "evidence": list(evidence), "side_findings": []}
        return reading, record, errors
    claim = doc.get("claim")
    try:
        res = claim_check(claim)
    except OverflowError as exc:
        # only a model-written number the claim card cannot hash (an integer past float range,
        # claim_tests._canon) is a refusal; any other exception is a bug of ours: loud
        errors.append(f"claim: a number in it is too large to check ({str(exc)[:120]})")
        return None, record, errors
    if res.errors:
        errors += [f"claim: {e}" for e in res.errors]
    elif res.tests_none:
        errors.append("claim: `tests: none` cannot be confirmed on a fold; write the test in the "
                      "slots or end with no_claim")
    hashes = [t["spec_hash"] for t in res.tests] if not res.errors else []
    ran = conditional_effect_hashes(entries)
    by_test = runs_by_test(entries)
    blocks = {t["name"]: t for t in _tests_of(claim) if isinstance(t.get("name"), str)}
    # the score's keys: each test's floorless identity (its own hash if the block is unknown)
    score_keys = []
    for t in (res.tests if hashes else []):
        h = t["spec_hash"]
        k = floorless_hash(blocks.get(t.get("name"))) or h
        score_keys.append(k)
        if h not in ran:
            msg = (f"claim test {h[:12]}... was never run with conditional_effect in this "
                   f"session: run it first and paste the `test` block it returns")
            other = by_test.get(k, [])
            if other:
                floors = sorted({json.dumps((((entries[q].get("result") or {}).get("test")) or {})
                                            .get("floor"), sort_keys=True) for q in other})
                msg += (f" ({', '.join(other)} ran the same test with floor {', '.join(floors)}, "
                        f"not the claim's: run it again with the claim's floor, the "
                        f"conditional_effect `floor` parameter)")
            errors.append(msg)
        # any run of this test (variant, floor, by) that measured the opposite counts, first
        # offending run in query-id order (q2 before q10)
        for q in sorted(by_test.get(k, []), key=lambda q: (len(q), q)):
            opp = opposite_horizons(entries[q])
            if opp:
                errors.append(
                    f"claim test {h[:12]}... measured the opposite of its direction in {q} ("
                    + "; ".join(f"h={hz}: {ws} of {wv} windows with the claimed sign"
                                for hz, ws, wv in opp)
                    + "): flip `direction` if the opposite is your claim, drop those horizons "
                    "from the test, or end with no_claim (a changed test must be run with "
                    "conditional_effect before you claim it)")
                break
    why = doc.get("why_query")
    test_qids = {q for h in hashes for q in ran.get(h, [])}
    if not _ok_call(entries, why):
        errors.append(f"why_query={why!r} is not a successful call of this session")
    elif why in test_qids or (entries[why].get("function") == "conditional_effect" and
                              floorless_hash(((entries[why].get("result") or {}).get("test")))
                              in score_keys):
        # D-094: the claim's own test under another floor is the same observation
        errors.append("why_query must be the SECOND query your mechanism predicted, not the "
                      "claim's own test")
    elif entries[why].get("function") not in WHY_FUNCTIONS:
        errors.append(f"why_query must be a {'/'.join(WHY_FUNCTIONS)} call (a measured "
                      f"prediction), not {entries[why].get('function')!r}")
    elif entries[why].get("function") == "conditional_effect" and _selector_of(entries[why]) in [
            t.get("selector") for t in _tests_of(claim)]:
        errors.append("why_query must test another selector than the claim's own test (the "
                      "same selector at another horizon or statistic is the same observation)")
    if hashes and not any(_cite_qid(c) in test_qids and _cite_path(c).startswith("horizons.")
                          for c in evidence):
        errors.append("evidence must cite the claim test's own result "
                      "(`q<n>:horizons.<h>.<field>=<value>` of its conditional_effect call)")
    if isinstance(claim, dict):
        errors += prose_number_errors({f"claim.{k}": claim.get(k) for k in PROSE_KEYS},
                                      evidence, entries, tests=claim.get("tests"))
    record.update(why_query=why, test_spec_hashes=hashes)
    scores = {"confidence_real": in_run_score(score_keys, entries) if hashes else 0,
              "distance_to_profitable": FIXED_SCORE, "mechanism_plausibility": FIXED_SCORE}
    record["scores"] = {**scores, "source": "code: in-run window agreement (PR5_DESIGN 11.3)"}
    side = {"proposal_id": f"{rid}-1", "claim": claim,
            "evidence": list(evidence), "scores": scores,
            "vehicle": doc.get("vehicle"), "combines_as": doc.get("combines_as")}
    if fold:
        side["fold_observed"] = fold
    reading = {**base, "explanation": str((claim or {}).get("rationale") or "")
               if isinstance(claim, dict) else "",
               "evidence": list(evidence), "side_findings": [side]}
    return reading, record, errors


RETRY_MAX_CHARS = 40000
_RETRY_ENTRY_MAX = 4000


def retry_section(previous_answer: str, errors: list, entries: dict) -> str:
    """The text appended to the prompt for the one retry: why the answer was refused, the
    refused answer, and the query log so far (a new session does not see the first one's
    tool results, and its citations must quote them). Each entry is compact JSON, its
    result cut at a fixed length; entries past the total cap are named, not shown (re-run
    them: the log, its ids and its comparison budget continue)."""
    lines = ["## Your previous answer was refused", ""]
    lines += [f"- {e}" for e in errors]
    lines += ["", "### The refused answer", "", (previous_answer or "(empty)")[:8000], "",
              "### Your query log so far (same ids, same comparison budget; it continues)", ""]
    used, omitted = sum(len(x) for x in lines), []
    for qid, e in entries.items():
        row = json.dumps({k: e.get(k) for k in ("id", "function", "params", "status", "reason",
                                                 "result")}, sort_keys=True, default=str)
        if len(row) > _RETRY_ENTRY_MAX:
            row = row[:_RETRY_ENTRY_MAX] + " ...(cut)"
        if used + len(row) > RETRY_MAX_CHARS:
            omitted.append(qid)
            continue
        lines.append(row)
        used += len(row)
    if omitted:
        lines.append(f"(not shown, over the length cap: {', '.join(omitted)})")
    lines += ["", "Answer again with exactly one fenced YAML block."]
    return "\n".join(lines)


SMOKE_SUMMARY_MARK = "--- analyst smoke summary ---"


def main(argv=None) -> int:
    """The smoke CLI (runbook, engineering/roadmap/E-075/PR5_RUNBOOK.md): one REAL analyst
    session, with the real stage function, on a COPY of a saved run. Run from
    strategy-research/ (the campaign memory is read from ./campaign_record, read-only):

        python tools/analyst_session.py --run <copy of a run> --lens forecast

    Turns on, in this process only, the two flags the stage reads (analyst and folds); the
    config file is not changed. Refuses a run under this repository's runs/ (saved runs are
    never written to). Spends model money: about $1.50 at most per session."""
    import argparse
    ap = argparse.ArgumentParser(description=main.__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="a COPY of a run directory")
    ap.add_argument("--lens", required=True, choices=LENSES)
    args = ap.parse_args(argv)
    run_dir = Path(args.run).resolve()
    if (SR_ROOT / "runs").resolve() in run_dir.parents or "holdout_sealed" in run_dir.parts:
        print(f"refusing {run_dir}: copy the run outside this repository's runs/ first",
              file=sys.stderr)
        return 2
    if not run_dir.is_dir():
        print(f"no such run directory: {run_dir}", file=sys.stderr)
        return 2
    workflow = str(SR_ROOT / "workflow")
    if workflow not in sys.path:
        sys.path.insert(0, workflow)
    import run_phase1_research as rpr
    saved = rpr._analyst_enabled, rpr._folds_enabled
    rpr._analyst_enabled = rpr._folds_enabled = lambda *a: True
    try:
        dest = rpr.run_analyst_worker(args.lens, run_dir.name, run_dir)
    finally:
        rpr._analyst_enabled, rpr._folds_enabled = saved
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8")) or {}
    audit = {k: v for k, v in (state.get("audit_log") or {}).items()
             if k.startswith(f"specialist_readers_analyst_{args.lens}_")}
    print(SMOKE_SUMMARY_MARK)
    print(yaml.safe_dump({"reading": str(dest), "record": str(run_dir / record_rel(args.lens)),
                          "query_log": str(run_dir / log_rel(args.lens)), "audit_log": audit},
                         sort_keys=False, allow_unicode=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
