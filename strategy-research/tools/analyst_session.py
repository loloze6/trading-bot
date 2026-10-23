"""E-075 PR-5 (CUL-423, D-092): the analyst session's pure part -- no SDK, no model call.

run_phase1_research wires the session (the seven tools as an in-process MCP server, the
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

import copy
import json
import math
import os
import re
import sys
from decimal import Decimal
from pathlib import Path

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

SR_ROOT = Path(_HERE).parent

import catalogue_section  # noqa: E402

#: lens -> the reader category file it writes (artifacts/proposals/<category>.yaml); the
#: other reader categories are written by code as `skipped` (replaced_by_analyst)
LENS_CATEGORY = {"forecast": "forecast_power", "trade_efficiency": "trade_efficiency"}
LENSES = tuple(LENS_CATEGORY)
REPLACED_RULE = "replaced_by_analyst"
SERVER_NAME = "analyst"
TOOL_NAMES = ("list_columns", "describe", "distribution", "conditional_effect", "trade_slice",
              "event_study", "window_economics")
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


def _window_bars_suffix(window, timeframe) -> str:
    """", <n> bars" for one protocol window: the days of test.start..test.end (end inclusive,
    the engine's convention) times the bars per day of the protocol's timeframe
    (claim_card.window_bars, the one definition of "bars in a test window"); "" when the
    window or the timeframe cannot be read, so the line is then as it was without the count."""
    import claim_card
    step = claim_card.timeframe_seconds(timeframe)
    if not step or step > 86400:
        return ""
    try:
        return f", {claim_card.window_bars([window], step)} bars"
    except (ValueError, KeyError, TypeError):
        return ""


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
                + _window_bars_suffix(w, p.get("timeframe"))
                for w in p.get("windows") or []))
        except ValueError:
            parts.append("run_protocol.json: unreadable")
    out = "\n".join(parts)
    out += _section(f"Base strategy config ({base_config_rel})", _read(run_dir / base_config_rel))
    out += _section("Variant patches (artifacts/variant_patches.yaml)",
                    _read(arts / "variant_patches.yaml"))
    out += _section("Cost model (config/cost_model.yaml; a measurement of this run, evidence never the claim)",
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
    text += _section("The component and op catalogue (what a vehicle may name)",
                     catalogue_section.catalogue_section())
    text += _section("The data dictionary (docs/DATA_DICTIONARY.md)",
                     _read(SR_ROOT / "docs" / "DATA_DICTIONARY.md"))
    for name in ("CLAIM_TESTS.md", "CLAIM_TESTS_TRADE.md", "CLAIM_TESTS_EXECUTION.md"):
        text += _section(f"Claim-test vocabulary: {name}", _read(hs / name))
    text += _section("The memory view (earlier claims; effect numbers only for confirmed ones)",
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
        if float(f"{float(logged):.8g}") == float(f"{c:.8g}"):
            return True
        # D-097 (smoke 2, 2026-10-09: five honest roundings refused): a float cited rounded
        # to the digits it shows, 3 or more; a count (an int) stays exact
        m = _CITED_FLOAT_RE.fullmatch(cited.strip())
        if isinstance(logged, int) or not m:
            return False
        sd = _sig_digits(m.group(1))
        return sd >= CITE_MIN_SIG_DIGITS and _rounds_to(float(logged), c, sd)
    return str(logged) == cited.strip()


CITE_MIN_SIG_DIGITS = 3
# a cited number: optional sign, its mantissa (group 1), optional exponent
_CITED_FLOAT_RE = re.compile(r"[-+]?(\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def check_citations(cites, entries: dict) -> list:
    """Errors of the `evidence` list: each item `q<n>:<dotted path>=<value>`; the id is an `ok`
    entry of this session's log, the path exists in its logged result, and the value equals
    the logged one (numbers at the log's 8 significant digits; since D-097 a float may also
    be cited rounded to 3 or more significant digits, a count stays exact)."""
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
    be present, a list, and name no tool outside the seven (PHASE_A section 1.4 (b): fail
    closed). Not verifiable from the Python source; the smoke session checks it live."""
    if not isinstance(init_tools, list):
        return [f"the session reported no tool list (system/init tools={init_tools!r})"]
    extra = sorted({str(t) for t in init_tools} - set(ALLOWED_TOOLS))
    if extra:
        return [f"the session had tools outside the seven: {extra}"]
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


# Operator, 2026-10-19 (PR-A): a no_claim may record what the session measured but could not
# turn into a claim yet (no strategy change follows from it yet): `observations`, a list of
# mappings with exactly OBSERVATION_KEYS -- `statement` (the behaviour), `test` (the id of the
# ok conditional_effect call of this session that measured it), `evidence` (citations, at
# least one of that call), `floors_met` (true/false: the call cleared its test's floor on
# every horizon; checked where its result can tell). Absent = none: a no_claim without the key
# is checked and recorded exactly as before. Each recorded observation also carries `spec`,
# written by code: the measured test block (its slots, no result) and its spec_hash. The
# regroup_record stage copies an accepted no_claim's observations into the run's
# campaign_memory entry (campaign_memory.analyst_observations); the memory view shows them as
# "observed, no vehicle yet" (analyst_memory_view).
# Operator, 2026-10-19: at most OBSERVATIONS_MAX observations per no_claim, each citing a different
# test (the prompt grows with every recorded observation).
OBSERVATION_KEYS = ("statement", "test", "evidence", "floors_met")
OBSERVATIONS_MAX = 3

# D-178 (operator item D, 2026-10-22). Optional keys of an observation: `mechanism_query` (a
# later query of this session) or `stopped_by` (a named tool limit) -- one of them is required
# when floors_met is true; `floor_lowered_reason` -- required when the observation's test repeats
# an earlier query's selector and outcome on a lower floor (floor_lowered_info).
# `vehicle` (ruling 1, 2026-10-23) -- the strategy change the finding points at, the claim's
# change-list shape; code reads only its path to tag a sizing finding (angle_of).
OBSERVATION_OPTIONAL = ("mechanism_query", "stopped_by", "floor_lowered_reason", "vehicle")
#: the four lines of the next-steps ledger (`claim.next_steps` / `no_claim.next_steps`)
NEXT_STEPS_KEYS = ("opposite_direction", "another_horizon", "all_bars_version", "mechanism")
#: keys a claim may carry for code only: stripped before the claim card sees the claim
CLAIM_CODE_KEYS = ("next_steps", "floor_lowered_reasons", "observations")
NOT_RUN_PREFIX = "not run:"


def _qnum(qid):
    """The number of a query id ("q12" -> 12); None for anything else."""
    m = re.fullmatch(r"q([0-9]+)", qid) if isinstance(qid, str) else None
    return int(m.group(1)) if m else None


def _is_ce_ok(entry) -> bool:
    return isinstance(entry, dict) and entry.get("function") == "conditional_effect" \
        and entry.get("status") == "ok"


def _test_block_of(entry) -> dict:
    res = entry.get("result") if isinstance(entry, dict) else None
    blk = res.get("test") if isinstance(res, dict) else None
    return blk if isinstance(blk, dict) else {}


def _floor_of(entry) -> dict:
    """The numeric floor units of a conditional_effect call's own test block."""
    fl = _test_block_of(entry).get("floor")
    if not isinstance(fl, dict):
        return {}
    return {k: v for k, v in fl.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}


def _same_selector_outcome_key(entry) -> str:
    """The identity D-178 compares when it asks whether a test repeats an earlier one: the
    selector, the outcome kind and the statistic (not the floor, direction, horizons, `by`,
    baseline or variant)."""
    t = _test_block_of(entry)
    out = t.get("outcome")
    kind = out.get("kind") if isinstance(out, dict) else out
    return json.dumps([t.get("selector"), kind, t.get("statistic")], sort_keys=True, default=str)


def _accounted_key(entry) -> str:
    """The identity D-178 (item D3, operator ruling 4) uses for "accounted for": the selector,
    the outcome kind, the statistic AND the direction. The same test at another floor, horizon
    or `by` is the same finding; the opposite direction of the same selector is not."""
    t = _test_block_of(entry)
    return json.dumps([_same_selector_outcome_key(entry), t.get("direction")], default=str)


def _floor_is_lower(this: dict, earlier: dict) -> bool:
    """`this` floor is lower than `earlier`: lower in at least one unit (a unit it leaves out
    counts as 0) and higher in none."""
    keys = set(this) | set(earlier)
    return any(earlier.get(k, 0) > this.get(k, 0) for k in keys) \
        and not any(this.get(k, 0) > earlier.get(k, 0) for k in keys)


def _first_run_of_test(qid: str, entries: dict) -> str:
    """The earliest ok call of the same test block (same spec_hash) as `qid`: where the test
    was first run, hence where its floor was chosen."""
    h = (entries[qid].get("result") or {}).get("spec_hash")
    same = [q for q, e in entries.items() if _is_ce_ok(e) and _qnum(q) is not None
            and h and (e.get("result") or {}).get("spec_hash") == h]
    return min(same, key=_qnum) if same else qid


def floor_lowered_info(qid, entries: dict):
    """D-178 (item D1): None, or {from, to, after} when the test that call `qid` ran repeats the
    selector, outcome kind and statistic of an EARLIER ok conditional_effect call of this session
    on a lower floor. `to` is the floor the test was first run with, `from` the earlier call's
    floor, `after` the latest such earlier call. The reader writes it from the log; the model
    only supplies the reason."""
    if not _is_ce_ok(entries.get(qid)):
        return None
    anchor = _first_run_of_test(qid, entries)
    n = _qnum(anchor)
    key, this = _same_selector_outcome_key(entries[anchor]), _floor_of(entries[anchor])
    best = None
    for q, e in entries.items():
        qn = _qnum(q)
        if qn is None or n is None or qn >= n or not _is_ce_ok(e):
            continue
        if _same_selector_outcome_key(e) == key and _floor_is_lower(this, _floor_of(e)) \
                and (best is None or qn > _qnum(best)):
            best = q
    if best is None:
        return None
    return {"from": _floor_of(entries[best]), "to": this, "after": best}


def met_own_floor(entry):
    """Whether a conditional_effect call's logged result met its own test's floor (D-178, item
    D3): at ANY horizon every floor unit the result reports (n_events, n_windows_with_events,
    n_blocks; a unit the result does not report, as min_eras, is not judged) is at or above its
    minimum, and at least one unit was judged. SKILL.md's no-claim rule says "at any horizon";
    floors_met_in_log (an observation's flag) asks every horizon. None when it cannot tell."""
    import claim_measure as cmeas
    floor = _floor_of(entry)
    hz = (entry.get("result") or {}).get("horizons") if isinstance(entry, dict) else None
    if not floor or not isinstance(hz, dict) or not hz:
        return None
    for row in hz.values():
        if not isinstance(row, dict):
            continue
        judged = []
        for unit, need in floor.items():
            have = row.get(cmeas._FLOOR_KEY.get(unit))
            if isinstance(have, (int, float)) and not isinstance(have, bool):
                judged.append(have >= need)
        if judged and all(judged):
            return True
    return False


def completeness_errors(entries: dict, accounted) -> list:
    """D-178 (item D3, SKILL.md's no-claim rule enforced): every ok conditional_effect call of
    the session that met its own floor must be accounted for -- `accounted` is the set of query
    ids the answer uses (why_query, an observation's `test` under a claim or a no_claim,
    best_rejected.killed_by, a claim test's own calls). A call that has the same selector,
    outcome kind, statistic AND direction as an accounted one (another floor, horizon or `by`)
    is the same finding and counts as accounted; the opposite direction is not."""
    keys = {_accounted_key(entries[q]) for q in accounted
            if isinstance(q, str) and _is_ce_ok(entries.get(q))}
    missing = [q for q, e in entries.items()
               if _is_ce_ok(e) and q not in accounted and met_own_floor(e) is True
               and _accounted_key(e) not in keys]
    if not missing:
        return []
    return [f"query(ies) {', '.join(missing)} cleared the floor of their own test but appear "
            f"nowhere in your answer: every conditional_effect result that cleared its floors, "
            f"in either direction and at any horizon, is written as a claim or recorded as an "
            f"observation (`observations`, `test`, under the claim or the no_claim), or is the "
            f"why_query or the best_rejected killed_by. Record each"]


def next_steps_errors(ns, entries: dict, where: str) -> list:
    """D-178 (item D5b): the four-line ledger is present and every cited query id is one of
    this session's. Nothing else is judged."""
    if not isinstance(ns, dict) or set(ns) != set(NEXT_STEPS_KEYS):
        return [f"{where}.next_steps is required: exactly the four lines "
                f"{list(NEXT_STEPS_KEYS)}, each the id of a query of this session or "
                f"\"{NOT_RUN_PREFIX} <the floor, the tool limit or the budget that stopped it>\""
                + (f" (got {sorted(map(str, ns))})" if isinstance(ns, dict) else "")]
    errors = []
    for k in NEXT_STEPS_KEYS:
        v = ns[k]
        if isinstance(v, str) and v.strip().startswith(NOT_RUN_PREFIX):
            if not v.strip()[len(NOT_RUN_PREFIX):].strip():
                errors.append(f"{where}.next_steps.{k}: \"{NOT_RUN_PREFIX}\" needs the floor, "
                              f"tool limit or budget that stopped it")
        elif not (isinstance(v, str) and _qnum(v.strip()) is not None):
            errors.append(f"{where}.next_steps.{k}={v!r} must be the id of a query of this "
                          f"session or \"{NOT_RUN_PREFIX} <reason>\"")
        elif v.strip() not in entries:
            errors.append(f"{where}.next_steps.{k}={v!r} is not a query of this session")
    return errors


# D-178 (item D4, operator ruling 1 of 2026-10-23): angle tags, written by code, by the vehicle's
# path and the selector's fields only; no text is read. `sizing`: the vehicle changes the sizing
# block (strategies.sizing) or the params of a vol_target op. `regime`: no selector names a
# forecast field. Sizing wins.
ANGLES = ("regime", "sizing")
SIZING_OP = "vol_target"
_SIZING_BLOCK_IDS = ("sizing", "strategies.sizing", "/strategies/sizing")


def _fields_of(node) -> list:
    """Every bar `field` named anywhere in a selector (at any depth)."""
    if isinstance(node, dict):
        out = [node["field"]] if isinstance(node.get("field"), str) else []
        for v in node.values():
            out += _fields_of(v)
        return out
    if isinstance(node, list):
        return [f for v in node for f in _fields_of(v)]
    return []


def _is_forecast_field(field: str) -> bool:
    """The forecast and every forecast-derived column (abs_forecast, forecast_sign_change,
    entry_forecast, ...): any field whose name contains "forecast"."""
    return "forecast" in field


#: statistics that never read the forecast (claim_tests.st_mean_diff / st_hit_rate; decay_curve
#: is mean_diff per horizon). rank_ic correlates the forecast with the outcome: it uses it.
FORECAST_FREE_STATISTICS = ("mean_diff", "hit_rate", "decay_curve")
#: selector kinds a regime tag is never given: all bars, and trade selectors
NON_REGIME_KINDS = ("all", "trade")


def is_regime_selector(selector, statistic=None) -> bool:
    """D-178 (operator 2026-10-23): a regime finding when (1) the selector names at least one
    bar field that is not a forecast field, (2) it names no forecast field and the test's
    statistic does not use the forecast (FORECAST_FREE_STATISTICS), (3) the selector is neither
    kind `all` nor kind `trade`. An unknown or missing statistic is not a regime."""
    if not isinstance(selector, dict) or statistic not in FORECAST_FREE_STATISTICS:
        return False
    if selector.get("kind") in NON_REGIME_KINDS:
        return False
    fields = _fields_of(selector)
    return bool(fields) and not any(_is_forecast_field(f) for f in fields)


def _sizing_ops_of(config) -> dict:
    """{json pointer: params} of every step (a mapping with `op: vol_target`) in a config."""
    out = {}

    def walk(node, path):
        if isinstance(node, dict):
            if node.get("op") == SIZING_OP:
                out[path] = copy.deepcopy(node.get("params"))
            for k, v in node.items():
                walk(v, f"{path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}/{i}")
    walk(config, "")
    return out


def _change_is_sizing(item, base_config) -> bool:
    """One `{component_id, field, before, after}` change: under the sizing block, or on a
    step whose op is vol_target (the field's path resolved in the base config: the component
    by `id`, then every prefix of the field path that is a step mapping)."""
    if not isinstance(item, dict):
        return False
    cid, field = item.get("component_id"), item.get("field")
    in_block = isinstance(field, str) and (
        field == "strategies.sizing" or field.startswith(("strategies.sizing.", "strategies.sizing[")))
    if cid in _SIZING_BLOCK_IDS or in_block:
        return True
    if not isinstance(base_config, dict) or not isinstance(cid, str) or not isinstance(field, str):
        return False
    import decide_next as dn
    import json_pointer as jp
    ptrs = dn._component_pointers(base_config, cid)
    if len(ptrs) != 1:
        return False
    try:
        suffix = dn.field_to_pointer_suffix(field)
    except dn.DecideNextError:
        return False
    parts = suffix.strip("/").split("/")
    for k in range(1, len(parts) + 1):
        try:
            node = jp.resolve_json_pointer(base_config, ptrs[0] + "/" + "/".join(parts[:k]))
        except jp.JsonPointerError:
            return False
        if isinstance(node, dict) and node.get("op") == SIZING_OP:
            return True
    return False


def vehicle_is_sizing(vehicle, base_config=None) -> bool:
    """D-178 (ruling 1): True when a vehicle changes the sizing block or a vol_target op's
    params. A change list is judged item by item; a config vehicle (`kind: config`) by what
    differs from the base config at the sizing block and at its vol_target steps."""
    if isinstance(vehicle, list):
        return any(_change_is_sizing(x, base_config) for x in vehicle)
    if isinstance(vehicle, dict) and isinstance(vehicle.get("config"), dict)             and isinstance(base_config, dict):
        cand, base = vehicle["config"], base_config
        if (cand.get("strategies") or {}).get("sizing") != (base.get("strategies") or {}).get("sizing"):
            return True
        return _sizing_ops_of(cand) != _sizing_ops_of(base)
    return False


def angle_of(selectors, vehicle=None, base_config=None, statistics=None):
    """`sizing` (wins), `regime` (every test passes is_regime_selector with its statistic;
    `statistics` is parallel to `selectors`) or None."""
    if vehicle_is_sizing(vehicle, base_config):
        return "sizing"
    stats = list(statistics) if statistics is not None else [None] * len(selectors)
    pairs = [(s, st) for s, st in zip(selectors, stats) if s is not None]
    return "regime" if pairs and all(is_regime_selector(s, st) for s, st in pairs) else None


def floors_met_in_log(entry: dict):
    """Whether a conditional_effect call's logged result clears its own test block's floor on
    every horizon (claim_measure's floor_not_met rule): False when a unit the result reports
    is below the floor, True when every unit is reported and met, None when it cannot tell
    (min_eras is not in the result, or the result is unreadable)."""
    import claim_measure as cmeas
    res = entry.get("result") if isinstance(entry, dict) else None
    floor = ((res or {}).get("test") or {}).get("floor") if isinstance(res, dict) else None
    hz = res.get("horizons") if isinstance(res, dict) else None
    if not isinstance(floor, dict) or not isinstance(hz, dict) or not hz:
        return None
    known = True
    for unit, need in floor.items():
        field = cmeas._FLOOR_KEY.get(unit)
        for row in hz.values():
            have = row.get(field) if isinstance(row, dict) and field else None
            if not isinstance(have, (int, float)) or isinstance(have, bool) \
                    or not isinstance(need, (int, float)):
                known = False
            elif have < need:
                return False
    return True if known else None


def observation_errors(observations, entries: dict, where: str = "no_claim.observations") -> list:
    """Errors of the `observations` of a no_claim or of a claim (`where` names which;
    OBSERVATION_KEYS); [] for a valid list, `[]` included."""
    if not isinstance(observations, list):
        return [f"{where} must be a list of {{statement, test, evidence, "
                "floors_met} (leave the key out, or write [], when there is none)"]
    errors = []
    if len(observations) > OBSERVATIONS_MAX:
        errors.append(f"{where} has {len(observations)} entries: at "
                      f"most {OBSERVATIONS_MAX} observations are recorded, each citing a different test (keep the "
                      f"{OBSERVATIONS_MAX} that matter most)")
    seen_tests = set()
    for i, o in enumerate(observations):
        w = f"{where}[{i}]"
        if not isinstance(o, dict) or not set(OBSERVATION_KEYS) <= set(o) \
                or set(o) - set(OBSERVATION_KEYS) - set(OBSERVATION_OPTIONAL):
            errors.append(f"{w} must have exactly the keys {list(OBSERVATION_KEYS)}, plus where "
                          f"they apply {list(OBSERVATION_OPTIONAL)}"
                          + (f" (got {sorted(map(str, o))})" if isinstance(o, dict) else ""))
            continue
        if not isinstance(o["statement"], str) or not o["statement"].strip():
            errors.append(f"{w}.statement must be a non-empty text: the behaviour you measured")
        if "vehicle" in o:
            import reader_proposals as _rpm
            try:
                _rpm._check_change_items(o["vehicle"], f"{w}.vehicle")
            except _rpm.ProposalError as exc:
                errors.append(str(exc))
        qid = o["test"]
        is_ce = _ok_call(entries, qid) and entries[qid].get("function") == "conditional_effect"
        if is_ce:
            # one observation per test: the same query, or the same test block run again (the
            # same spec_hash), is the same test
            sh = (entries[qid].get("result") or {}).get("spec_hash")
            key = sh if isinstance(sh, str) and sh else qid
            if key in seen_tests:
                errors.append(f"{w}.test={qid!r} measures the same test as an earlier observation "
                              f"of this answer: each observation cites a different test")
            seen_tests.add(key)
        if not is_ce:
            errors.append(f"{w}.test={qid!r} must be the id of an ok conditional_effect call of "
                          f"this session (the call that measured the behaviour)")
        errors += [f"{w}.{e}" for e in check_citations(o["evidence"], entries)]
        if is_ce and isinstance(o["evidence"], list) \
                and not any(_cite_qid(c) == qid for c in o["evidence"]):
            errors.append(f"{w}.evidence must cite its test's own result "
                          f"(`{qid}:horizons.<h>.<field>=<value>`)")
        if not isinstance(o["floors_met"], bool):
            errors.append(f"{w}.floors_met must be true or false")
        elif is_ce:
            met = floors_met_in_log(entries[qid])
            if met is not None and met != o["floors_met"]:
                errors.append(f"{w}.floors_met is {str(o['floors_met']).lower()}, but {qid}'s "
                              f"result {'clears' if met else 'does not clear'} its test's floor "
                              f"on every horizon (n_events, n_windows_with_events, n_blocks "
                              f"against `floor`)")
        if is_ce:
            errors += _mechanism_errors(o, qid, w, entries)
            if floor_lowered_info(qid, entries) is not None \
                    and not _non_empty_text(o.get("floor_lowered_reason")):
                errors.append(_floor_reason_error(f"{w}.floor_lowered_reason", qid, entries))
    return errors


def _non_empty_text(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _mechanism_errors(o: dict, qid: str, w: str, entries: dict) -> list:
    """D-178 (item D2): an observation with floors_met true cites a LATER query of this session
    as `mechanism_query` (the query its mechanism predicts), or `stopped_by` a named tool limit.
    A `mechanism_query` that is written must be valid, whatever `stopped_by` says."""
    if o.get("floors_met") is not True:
        return []
    mq = o.get("mechanism_query")
    if mq is not None:
        if not (_ok_call(entries, mq) and _qnum(mq) is not None and _qnum(mq) > _qnum(qid)):
            return [f"{w}.mechanism_query={mq!r} must be an ok query of this session LATER than "
                    f"{qid} (the query your mechanism predicts)"]
        return []
    if _non_empty_text(o.get("stopped_by")):
        return []
    return [f"{w}: {qid} cleared its floors, so the observation needs `mechanism_query: q<n>` "
            f"(a query of this session after {qid} that runs what your mechanism predicts) or "
            f"`stopped_by: <the tool limit that stopped it>`; run that query, then record it"]


def _floor_reason_error(where: str, qid: str, entries: dict) -> str:
    info = floor_lowered_info(qid, entries)
    return (f"{where} is required: the test of {qid} repeats the selector and outcome of "
            f"{info['after']} on a lower floor ({info['from']} to {info['to']}); write one "
            f"sentence saying why the floor was lowered")


def _observation_spec(entry: dict) -> dict:
    """The code-written `spec` of a recorded observation: the measured test block's slots
    (selector, outcome, baseline, statistic, direction, floor; no result) and its spec_hash."""
    res = entry.get("result") or {}
    block = res.get("test") if isinstance(res.get("test"), dict) else {}
    # deep copies: two observations citing the same query must not share objects (PyYAML would
    # write the second as an alias, &id001 / *id001, in the record)
    return {"spec_hash": res.get("spec_hash"),
            **{k: copy.deepcopy(block[k]) for k in ("selector", "outcome", "baseline", "statistic",
                                                    "direction", "floor") if k in block}}


def _tests_of(claim) -> list:
    tests = claim.get("tests") if isinstance(claim, dict) else None
    return [t for t in tests if isinstance(t, dict)] if isinstance(tests, list) else []


def _selector_of(entry: dict):
    return (((entry.get("result") or {}).get("test")) or {}).get("selector")


def _clause_set(clauses):
    """A trade filter as a set of (field, op, canonical value): the same clauses in any order are
    one filter. None for anything that is not a list of well-formed clause dicts."""
    if not isinstance(clauses, list):
        return None
    import claim_tests as ct
    out = set()
    for c in clauses:
        if not (isinstance(c, dict) and isinstance(c.get("field"), str)
                and isinstance(c.get("op"), str) and "value" in c):
            return None
        v = c["value"]
        try:    # as the engine's test identity reads it: 5 == 5.0, `in` lists in any order
            v = ct._canon(sorted(v, key=ct._val_key) if isinstance(v, list) else v)
            out.add((c["field"], c["op"], json.dumps(v, sort_keys=True)))
        except (TypeError, ValueError, OverflowError):
            return None
    return frozenset(out)


def _why_filter_set(entry: dict):
    """The trade filter a why_query used, whatever its tool: a conditional_effect's trade
    selector `where`, a trade_slice's `filter`, an event_study's `trade_filter`."""
    fn, params = entry.get("function"), entry.get("params") or {}
    if fn == "conditional_effect":
        sel = _selector_of(entry)
        is_trade = isinstance(sel, dict) and sel.get("kind") == "trade"
        return _clause_set(sel.get("where")) if is_trade else None
    key = {"trade_slice": "filter", "event_study": "trade_filter"}.get(fn)
    return _clause_set(params.get(key)) if key and isinstance(params, dict) else None


def _test_numbers(node, out: set) -> set:
    """The finite numbers written anywhere in `node`: the claim's test blocks (horizons,
    lookbacks, floors, selector values) or, for config_settings, a whole base config. Python
    ints are kept exact (a huge one never overflows)."""
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


def prose_number_errors(fields: dict, evidence, entries: dict, tests=None,
                        settings=None) -> list:
    """The message of each unverified number in the answer's prose (number_hits)."""
    return [h[4] for h in number_hits(fields, evidence, entries, tests, settings)]


def config_settings(config) -> set:
    """D-098: every finite number of a run's base strategy config (its settings: periods,
    spans, factors, weights, lookbacks); empty for anything that is not a config."""
    return _test_numbers(config, set()) if isinstance(config, dict) else set()


def number_hits(fields: dict, evidence, entries: dict, tests=None, settings=None) -> list:
    """Every number written in the answer's prose that the session did not see, as
    (label, start, end, written, message) (review of #359: free-text numbers were never
    checked). Since D-096 such a number is masked and listed, not refused (check_answer).
    `fields`: {label: text}. A number is verified when
      * it is 0 (as written), or 100%;
      * it is a horizon of a cited `horizons.<h>.` path, or a number of the claim's own test
        blocks, written exactly (all its digits, no sign, no %, no exponent). Known gap: a
        unit in words is not read, so "5 bps" passes when 5 is a number of the test;
      * it is a number of the claim's own test blocks in [0, 1] written as a percent, no sign,
        no exponent ("top 20%" for q 0.2; smoke 4, 2026-10-09). Known gap: whether the percent
        reads right is not checked ("forecast above 20%" passes for `forecast > 0.2`);
      * it is a value of the claim's own test blocks or a setting of the run's base config
        (`settings`), written exactly with its own sign ("-5" for `entry_forecast > -5`, "a
        21-bar EMA"; D-098, pilot 2a: 29 of Sonnet's 51 masked numbers were such settings);
        a written "+" is never a setting. Known gap: units are not read, so a number equal
        to a setting passes where it is not one (base configs hold 2 to 5 numbers such as 1,
        2, 10, 20, 21, 50, 500: "500 trades" passes in a run with a 500-bar lookback);
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
    own = _test_numbers(tests, set())
    exact = horizons | own
    own_unit = {n for n in own if 0 <= n <= 1}
    checkable = own | (settings or set())
    hits = []
    for label, text in fields.items():
        if not isinstance(text, str):
            continue
        for m in _PROSE_NUMBER_RE.finditer(text):
            sign, mantissa, exp, pct = m.groups()
            try:
                x = float(mantissa.replace(",", "")) * (10.0 ** int(exp) if exp else 1.0)
            except (ValueError, OverflowError):
                x = math.inf

            def hit(message, m=m, label=label):
                hits.append((label, m.start(), m.end(), m.group(0), message))
            if not math.isfinite(x):
                hit(f"{label} writes {m.group(0)!r}: not a number you cited")
                continue
            negative = sign in ("-", "\u2212")
            if float(mantissa.replace(",", "")) == 0 or (pct and x == 100 and not sign):
                continue
            # a test's own number or a cited horizon: unsigned and exact only (it is a setting
            # of the test, never an effect)
            if not pct and not exp and not sign and "," not in mantissa and x in exact:
                continue
            # D-098: a test value or a config setting the code can check, with its own sign;
            # a written "+" marks an effect, never a setting (review of #375)
            if not pct and not exp and "," not in mantissa and sign != "+" \
                    and (-x if negative else x) in checkable:
                continue
            # a test's own number in [0, 1] as a percent: x/100 computed exactly in decimal
            # (33.3 / 100.0 != 0.333 in floats)
            if pct and not exp and not sign and "," not in mantissa \
                    and float(Decimal(mantissa) / 100) in own_unit:
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
                hit(f"{label} writes {m.group(0)!r}: write your test's number as in "
                    f"the test block ({x / 100.0!r}), not as a percent")
                continue
            hit(f"{label} writes {m.group(0)!r}, which is not a value you cited in "
                f"`evidence` nor a number of your test: cite it (as the decimal the "
                f"tool returned, e.g. 0.0123, or as a percent, 1.23%; bps are not "
                f"read), or say it in words (\"positive\", \"most windows\")")
    return hits


def mask_hits(root, prefix: str, hits: list):
    """A deep copy of `root` (the claim or the no_claim block) with each hit's number replaced
    by explore_confirm.NUMBER_MASK, as the memory view masks earlier statements. A hit's label
    is `<prefix>.<key>[.<key>]` (number_hits' labels)."""
    import copy
    from explore_confirm import NUMBER_MASK
    out = copy.deepcopy(root)
    spans: dict = {}
    for label, start, end, _written, _msg in hits:
        spans.setdefault(label, []).append((start, end))
    for label, where in spans.items():
        keys = label.split(".")[1:] if label.startswith(prefix + ".") else []
        node = out
        for k in keys[:-1]:
            node = node.get(k) if isinstance(node, dict) else None
        if not keys or not isinstance(node, dict) or not isinstance(node.get(keys[-1]), str):
            raise ValueError(f"mask_hits: {label!r} is not a text under {prefix!r}")
        text = node[keys[-1]]
        for start, end in sorted(where, reverse=True):
            text = text[:start] + NUMBER_MASK + text[end:]
        node[keys[-1]] = text
    return out


def _unverified(hits: list) -> list:
    return [{"field": label, "written": written} for label, _s, _e, written, _m in hits]


def exit_selector_own_outcome_hits(claim) -> list[dict]:
    """D-095 (smoke 3, 2026-10-09): one hit per claim test that selects lots by an exit-time
    field (claim_tests.TRADE_EXIT_FIELDS) and measures their own result (any of
    claim_tests.TRADE_OWN_OUTCOMES, operator ruling 2026-10-19). Such a test is near-mechanical
    (a losing lot stays open longer). Claim in, list of {name, fields, outcome, what, core} out,
    in the order of the claim's tests; [] for anything else, a malformed claim included.
    The one source of the refusal's facts (operator ruling D-157, 2026-10-20): every seam
    composes its own text from a hit -- `what` (the test and what it does) and `core` (`what`
    plus what the test cannot tell apart, one sentence) -- so the seams cannot drift:
    the analyst (exit_selector_own_outcome_errors), step 1a (run_phase1_research.
    _check_1a_claim) and the side-finding check (reader_findings.d095_refusals)."""
    import claim_tests as ct
    hits = []
    for i, t in enumerate(_tests_of(claim)):
        sel, out = t.get("selector"), t.get("outcome")
        if not (isinstance(sel, dict) and sel.get("kind") == "trade"
                and isinstance(out, dict) and out.get("kind") in ct.TRADE_OWN_OUTCOMES
                and isinstance(sel.get("where"), list)):
            continue
        fields = sorted({c["field"] for c in sel["where"]
                         if isinstance(c, dict) and c.get("field") in ct.TRADE_EXIT_FIELDS})
        if fields:
            name = t.get("name", i)
            what = (f"claim test {name!r} selects lots by an exit-time field "
                    f"({', '.join(fields)}) and measures their own {out['kind']}")
            # D-097: the core says what this test cannot tell apart
            core = (f"{what}: it cannot tell 'the exit comes too late' from 'a losing lot stays "
                    f"open longer' (a lot closes only when the allocation changes, so long-held "
                    f"lots are the ones the price kept going against).")
            hits.append({"name": name, "fields": fields, "outcome": out["kind"],
                         "what": what, "core": core})
    return hits


def exit_selector_own_outcome_errors(claim) -> list[str]:
    """D-095, the analyst's seam (check_answer): one error per hit
    (exit_selector_own_outcome_hits), its core plus the analyst's advice (D-097: what to do
    instead). Claim in, list of error strings out; [] for anything else."""
    import claim_tests as ct
    return [f"{h['core']} Select on an entry-time field ({', '.join(ct.TRADE_ENTRY_FIELDS)}), "
            f"or measure post_exit_return. 'The exit comes too late' has no claim test yet (it "
            f"needs the return from bar N to the exit): explore it with event_study "
            f"(trade_filter on {h['fields'][0]}) and, if it is your best idea, end with "
            f"no_claim and give it as best_rejected"
            for h in exit_selector_own_outcome_hits(claim)]


def _record_observations(observations: list, entries: dict, evidence, settings, base_config,
                         where: str) -> tuple:
    """(recorded observations, unverified numbers) of a valid `observations` list (a claim's or a
    no_claim's): each masked (D-096), with its code spec, the floor disclosure (D1) and the
    angle tag (D4) written by code."""
    recorded, unverified = [], []
    for i, o in enumerate(observations):
        test = entries[o["test"]]
        block = (test.get("result") or {}).get("test")
        ohits = number_hits(
            {"observation.statement": o["statement"]},
            list(o["evidence"]) + list(evidence), entries,
            tests=[block] if isinstance(block, dict) else None, settings=settings)
        item = {k: v for k, v in mask_hits(o, "observation", ohits).items()
                if k != "floor_lowered_reason"}
        item["spec"] = _observation_spec(test)
        lowered = floor_lowered_info(o["test"], entries)
        if lowered is not None:
            item["floor_lowered"] = {**lowered, "reason": o["floor_lowered_reason"].strip()}
        angle = angle_of([item["spec"].get("selector")], o.get("vehicle"), base_config,
                         [item["spec"].get("statistic")])
        if angle is not None:
            item["angle"] = angle
        recorded.append(item)
        unverified += [{"field": f"{where}.{i}.statement", "written": wr}
                       for _l, _s, _e, wr, _m in ohits]
    return recorded, unverified


def check_answer(text: str, *, lens: str, run_id: str, entries: dict, claim_check,
                 holdout_start: str, fold: str | None, model_id: str,
                 settings=None, base_config=None) -> tuple:
    """(reading, record, errors). `base_config`: the run's base strategy config (a mapping),
    against which a vehicle's path is resolved for the sizing tag (D-178, ruling 1). `entries`: {id: log entry} of this lens's query log.
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
        errors += next_steps_errors(nc.get("next_steps") if isinstance(nc, dict) else None,
                                    entries, "no_claim")
        if isinstance(nc, dict):
            # smoke 5 (2026-10-09): the killing test's own numbers (its threshold, horizons,
            # floor) may be written here, as the claim's own test's are on the claim path.
            # Known gap, as on the claim path: the model names killed_by, and nothing ties the
            # statement to that test, so its numbers are accepted whatever the text says
            kid = br.get("killed_by") if isinstance(br, dict) else None
            killed = entries[kid] if _ok_call(entries, kid) else {}
            res = killed.get("result")
            ktest = res.get("test") if killed.get("function") == "conditional_effect" \
                and isinstance(res, dict) else None
            # D-096: an unverified number is masked and listed, never a refusal
            hits = number_hits(
                {"no_claim.reason": nc.get("reason"),
                 "no_claim.best_rejected.statement": br.get("statement")
                 if isinstance(br, dict) else None}, evidence, entries,
                tests=[ktest] if isinstance(ktest, dict) else None, settings=settings)
            nc = mask_hits(nc, "no_claim", hits)
            record["unverified_numbers"] = _unverified(hits)
            if "observations" in nc:
                # operator, 2026-10-19 (PR-A): absent = none, so a no_claim without the key is
                # unchanged; a valid list is recorded masked (D-096), each with its code spec
                obs_errors = observation_errors(nc["observations"], entries)
                errors += obs_errors
                if not obs_errors:
                    nc["observations"], unv = _record_observations(
                        nc["observations"], entries, evidence, settings, base_config,
                        "no_claim.observations")
                    record["unverified_numbers"] += unv
        # D-178 (item D3): every call that cleared its own floor is accounted for
        accounted = [br.get("killed_by") if isinstance(br, dict) else None]
        accounted += [o.get("test") for o in (nc.get("observations") if isinstance(nc, dict)
                                              and isinstance(nc.get("observations"), list) else [])
                      if isinstance(o, dict)]
        errors += completeness_errors(entries, {q for q in accounted if isinstance(q, str)})
        if isinstance(nc, dict) and isinstance(nc.get("next_steps"), dict):
            record["next_steps"] = copy.deepcopy(nc["next_steps"])
        record["no_claim"] = nc
        reading = {**base, "explanation": str((nc or {}).get("reason") or "no claim"),
                   "evidence": list(evidence), "side_findings": []}
        return reading, record, errors
    claim = doc.get("claim")
    # D-178: `next_steps` and `floor_lowered_reasons` are for code; the claim card never sees them
    claim_extra = {}
    if isinstance(claim, dict):
        claim_extra = {k: claim[k] for k in CLAIM_CODE_KEYS if k in claim}
        claim = {k: v for k, v in claim.items() if k not in CLAIM_CODE_KEYS}
    errors += next_steps_errors(claim_extra.get("next_steps"), entries, "claim")
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
    errors += exit_selector_own_outcome_errors(claim)
    # D-098 (pilot 2a): the forecast's rank IC over all bars is what the run's protocol
    # already tests; restating it spends a fold-B child to learn nothing new
    for i, t in enumerate(_tests_of(claim)):
        sel = t.get("selector")
        if t.get("statistic") == "rank_ic" and isinstance(sel, dict) and sel.get("kind") == "all":
            errors.append(
                f"claim test {t.get('name', i)!r} is the forecast's rank IC over all bars: the "
                f"run's protocol already tests that. Claim where the forecast behaves "
                f"differently: a selector on part of the bars (calendar, regime, event, "
                f"quantile), with a statement that says only what that test measures, or end "
                f"with no_claim")
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
    why_set = _why_filter_set(entries[why]) if _ok_call(entries, why) else None
    claim_sets = [_clause_set((t["selector"]).get("where")) for t in _tests_of(claim)
                  if isinstance(t.get("selector"), dict) and t["selector"].get("kind") == "trade"]
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
    elif why_set is not None and why_set in claim_sets:
        # smoke 3 (2026-10-09): a trade_slice on the claim's own filter, or the same `where`
        # clauses in another order, passed as the "second query"
        errors.append("why_query must use another filter than the claim's own test (the same "
                      "trades split another way, or the same clauses in another order, are the "
                      "same observation)")
    if hashes and not any(_cite_qid(c) in test_qids and _cite_path(c).startswith("horizons.")
                          for c in evidence):
        errors.append("evidence must cite the claim test's own result "
                      "(`q<n>:horizons.<h>.<field>=<value>` of its conditional_effect call)")
    # D-178: floor disclosure (D1), completeness (D3), tags (D4)
    lowered_items = []
    reasons = claim_extra.get("floor_lowered_reasons")
    reasons = reasons if isinstance(reasons, dict) else {}
    for t in (res.tests if hashes else []):
        qids = sorted(ran.get(t["spec_hash"], []), key=_qnum)
        info = floor_lowered_info(qids[0], entries) if qids else None
        if info is None:
            continue
        reason = reasons.get(t.get("name"))
        if not _non_empty_text(reason):
            errors.append(_floor_reason_error(
                f"claim.floor_lowered_reasons.{t.get('name')}", qids[0], entries))
        else:
            lowered_items.append({"test": t.get("name"), **info, "reason": reason.strip()})
    accounted = ([why] if isinstance(why, str) else []) + list(test_qids)
    claim_obs = claim_extra.get("observations")
    claim_obs_ok = False
    if "observations" in claim_extra:
        obs_errors = observation_errors(claim_obs, entries, "claim.observations")
        errors += obs_errors
        claim_obs_ok = not obs_errors
        if claim_obs_ok:
            accounted += [o["test"] for o in claim_obs]
    errors += completeness_errors(entries, {q for q in accounted if isinstance(q, str)})
    angle = None
    if isinstance(claim, dict):
        angle = angle_of([t.get("selector") for t in _tests_of(claim)], doc.get("vehicle"),
                         base_config, [t.get("statistic") for t in _tests_of(claim)])
    if angle == "sizing":
        errors.append("claim: this is a sizing finding (its vehicle changes the sizing block or "
                      "the params of a vol_target op). A sizing finding is recorded as an "
                      "observation (`observations`, under the claim or the no_claim), tagged "
                      "angle: sizing by code; it is never a claim with a vehicle")
    if isinstance(claim, dict):
        # D-096: an unverified number is masked in what is stored and passed on (the reading,
        # the child's pre-filled claim) and listed, never a refusal
        hits = number_hits({f"claim.{k}": claim.get(k) for k in PROSE_KEYS},
                           evidence, entries, tests=claim.get("tests"), settings=settings)
        claim = mask_hits(claim, "claim", hits)
        record["unverified_numbers"] = _unverified(hits)
    # the reading checks (shape, vehicle) need a claim the claim card accepted
    record["claim_card_ok"] = not res.errors
    record.update(why_query=why, test_spec_hashes=hashes)
    scores = {"confidence_real": in_run_score(score_keys, entries) if hashes else 0,
              "distance_to_profitable": FIXED_SCORE, "mechanism_plausibility": FIXED_SCORE}
    record["scores"] = {**scores, "source": "code: in-run window agreement (PR5_DESIGN 11.3)"}
    side = {"proposal_id": f"{rid}-1", "claim": claim,
            "evidence": list(evidence), "scores": scores,
            "vehicle": doc.get("vehicle"), "combines_as": doc.get("combines_as")}
    if lowered_items:      # D-178: written by code from the log; one test -> a mapping
        side["floor_lowered"] = lowered_items[0] if len(lowered_items) == 1 else lowered_items
        record["floor_lowered"] = side["floor_lowered"]
    if angle is not None:
        side["angle"] = angle
        record["angle"] = angle
    if isinstance(claim_extra.get("next_steps"), dict):
        record["next_steps"] = copy.deepcopy(claim_extra["next_steps"])
    if claim_obs_ok and claim_obs:
        record["observations"], unv = _record_observations(
            claim_obs, entries, evidence, settings, base_config, "claim.observations")
        record["unverified_numbers"] = list(record.get("unverified_numbers") or []) + unv
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
    # smoke 5 (2026-10-09): a no_claim refused only for its wording came back as a claim
    lines += ["", "A `no_claim` is an accepted answer as much as a claim. If the errors are about "
              "wording or citations only, fix them and keep your outcome: do not turn a no_claim "
              "into a claim to get past them. End with no_claim when an error says your claim "
              "does not hold (its test was not run, or measured the opposite)."]
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
    never written to). Spends model money: at most the `max_budget_usd` cap per session ($3
    by default), as the SDK's CLI meters it."""
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
