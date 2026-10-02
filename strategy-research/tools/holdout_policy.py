"""
holdout_policy.py -- the ONE strict reader of campaign_data_policy.yaml's
holdout_range (CUL-339 review fixes).

Every tool that needs the sealed range parses it here, with one definition of
"a day": a plain "YYYY-MM-DD" string of ASCII digits that is a real calendar
date (or a `datetime.date` -- not a datetime -- which YAML produces from an
unquoted day). A timestamp, a timezone offset, a US-style "M/D/YYYY", padding
whitespace, trailing text or a non-ASCII digit is NOT a day and is refused.

Callers (each keeps its own exception type by catching HoldoutPolicyError):
  * tools/run_protocol.py -- --holdout range, walk-forward training bound,
    holdout_consumed_by check, window pre-flight;
  * workflow/run_phase1_research.py::_load_holdout_range (and so every
    orchestrator/campaign caller of it, composite_cache's caller included);
  * tools/composite_cache.py::check_protocol_outside_holdout (window dates);
  * tools/measure_bar_sigma.py::_holdout_range_from_policy.

Deny by default: a missing, unreadable, unparseable or malformed policy
raises; nothing here returns "no holdout to worry about".

Import-isolated on purpose: stdlib only at import time (yaml is imported
lazily inside load_policy), and this module reads exactly one file -- the
policy -- so an import-pinned caller (measure_bar_sigma) does not widen what
it can reach by depending on it. No wall clock is read anywhere in here: a
range end is never derived from "today".
"""
from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

#: The real policy file. Callers that sandbox the policy in tests pass their
#: own path explicitly; nothing here caches it.
POLICY_PATH = Path(__file__).resolve().parent.parent / "config" / "campaign_data_policy.yaml"

_ISO_DAY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class HoldoutPolicyError(ValueError):
    """The policy, its holdout_range / holdout_consumed_by, or a window checked
    against the range is unusable. Always a refusal, never a default."""


def iso_day(value) -> str | None:
    """`value` as a strict "YYYY-MM-DD" day, or None when it is not one."""
    if isinstance(value, date) and not isinstance(value, datetime):
        return value.isoformat()
    if not isinstance(value, str) or not _ISO_DAY.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        return None


def _pair(hr, where: str) -> tuple:
    if not isinstance(hr, (list, tuple)) or len(hr) != 2:
        raise HoldoutPolicyError(f"{where} {hr!r} is not a [start, end] pair")
    return hr[0], hr[1]


def parse_holdout_start(hr, where: str = "holdout_range") -> str:
    """The START of a [start, end] holdout_range, validated; the END is not
    looked at (a walk-forward training bound needs only the start, so an open
    or not-yet-decided end must not block training)."""
    raw_start, _ = _pair(hr, where)
    start = iso_day(raw_start)
    if start is None:
        raise HoldoutPolicyError(f"{where} start {raw_start!r} is not a YYYY-MM-DD day")
    return start


def parse_holdout_range(hr, where: str = "holdout_range") -> tuple[str, str]:
    """A CLOSED [start, end] holdout_range: both ends strict days, end >= start.
    An open (null / empty) end is refused -- it would read post-holdout data."""
    start = parse_holdout_start(hr, where)
    raw_end = hr[1]
    end = iso_day(raw_end)
    if end is None:
        raise HoldoutPolicyError(
            f"{where} end {raw_end!r} is open or not a YYYY-MM-DD day; the holdout is a "
            f"CLOSED range and an open end would read post-holdout data")
    if end < start:
        raise HoldoutPolicyError(f"{where} ends ({end}) before it starts ({start})")
    return start, end


def load_policy(path=None) -> dict:
    """The whole policy document. Missing, unreadable, unparseable or not a
    mapping -> HoldoutPolicyError."""
    import yaml  # lazy: keeps this module stdlib-only at import (see module doc)

    p = Path(path) if path is not None else POLICY_PATH
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise HoldoutPolicyError(f"cannot read the campaign data policy at {p} "
                                 f"({type(exc).__name__}: {exc})") from exc
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise HoldoutPolicyError(f"cannot parse the campaign data policy at {p} "
                                 f"({type(exc).__name__}: {exc})") from exc
    if not isinstance(doc, dict):
        raise HoldoutPolicyError(f"the campaign data policy at {p} is not a mapping")
    return doc


def holdout_range_of(policy: dict, where: str = "holdout_range") -> tuple[str, str]:
    """The closed holdout_range of an already-loaded policy document."""
    return parse_holdout_range(policy.get("holdout_range"), where)


def holdout_start_of(policy: dict, where: str = "holdout_range") -> str:
    """The holdout_range START of an already-loaded policy document."""
    return parse_holdout_start(policy.get("holdout_range"), where)


def load_holdout_range(path=None) -> tuple[str, str]:
    """(start, end) of the policy's closed holdout_range, both strict days."""
    p = Path(path) if path is not None else POLICY_PATH
    return holdout_range_of(load_policy(p), f"{p} holdout_range")


def consumed_hypothesis_ids(policy: dict) -> frozenset:
    """holdout_consumed_by of an already-loaded policy, as exact ids. The key
    must be present (deny by default: an absent list cannot prove a hypothesis
    unspent); null means none consumed (the writer's own normalisation);
    a list must hold only non-empty strings; a lone string is one id."""
    if "holdout_consumed_by" not in policy:
        raise HoldoutPolicyError("the campaign data policy has no holdout_consumed_by key "
                                 "-- cannot prove the hypothesis has not spent the holdout")
    value = policy["holdout_consumed_by"]
    if value is None:
        return frozenset()
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise HoldoutPolicyError(f"holdout_consumed_by {value!r} is not a list of "
                                 f"hypothesis ids")
    return frozenset(value)


def check_windows_before(windows, holdout_start: str) -> None:
    """Every walk-forward window must carry strict-day test.start/test.end with
    start <= end and end STRICTLY before `holdout_start`. `end` is
    INCLUSIVE-BY-DAY at the engine (load_data(end_date=end) yields that whole
    day's bars), so end == holdout_start would materialise sealed bars.
    Anything missing or malformed refuses (fail closed)."""
    bound = iso_day(holdout_start)
    if bound is None:
        raise HoldoutPolicyError(f"holdout start {holdout_start!r} is not a YYYY-MM-DD day")
    if not isinstance(windows, list) or not windows:
        raise HoldoutPolicyError("protocol has no windows list -- nothing to check, "
                                 "refusing (fail closed)")
    for w in windows:
        test = w.get("test") if isinstance(w, dict) else None
        if not isinstance(test, dict):
            raise HoldoutPolicyError(f"protocol window {w!r} has no test dates -- refusing "
                                     f"(fail closed)")
        label = w.get("label")
        days = {}
        for edge in ("start", "end"):
            raw = test.get(edge)
            days[edge] = iso_day(raw)
            if days[edge] is None:
                raise HoldoutPolicyError(f"window {label!r} test.{edge}={raw!r} is not a "
                                         f"YYYY-MM-DD day -- refusing (fail closed)")
        if days["end"] < days["start"]:
            raise HoldoutPolicyError(f"window {label!r} ends ({days['end']}) before it "
                                     f"starts ({days['start']})")
        if not days["end"] < bound:
            raise HoldoutPolicyError(
                f"window {label!r} ends {days['end']}, at or past holdout_start={bound} -- a "
                f"training window must never reach into the holdout range. NB `end` is "
                f"INCLUSIVE-BY-DAY at the engine, so an end equal to holdout_start still "
                f"materialises that whole day's bars. Fix the protocol's windows before "
                f"proceeding.")


def windows_overlap(windows) -> str | None:
    """CUL-369 (D-058): why these windows share a day, or None. `test.end` is
    the LAST INCLUDED DAY (the engine loads every bar of it), so two windows
    whose day ranges [start, end] intersect backtest those days twice -- the
    pooled records double-count them and the grid's time-ordered fit refuses
    them. Compared on YYYY-MM-DD in start order. A malformed window is skipped
    here: check_windows_before refuses it (run_protocol calls both)."""
    spans = sorted((days["start"], days["end"], w.get("label", "?"))
                   for w in (windows if isinstance(windows, list) else [])
                   if isinstance(w, dict) and isinstance(w.get("test"), dict)
                   for days in [{e: iso_day(w["test"].get(e)) for e in ("start", "end")}]
                   if days["start"] and days["end"])
    for (s1, e1, l1), (s2, e2, l2) in zip(spans, spans[1:]):
        if s2 <= e1:
            return (f"windows {l1!r} [{s1}..{e1}] and {l2!r} [{s2}..{e2}] share day(s) "
                    f"{s2}..{min(e1, e2)}: test.end is the LAST INCLUDED DAY (the engine loads "
                    f"every bar of it), so those days would be backtested twice (CUL-369, D-058). "
                    f"End each window the day before the next one starts.")
    return None
