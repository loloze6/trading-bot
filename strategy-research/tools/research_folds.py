"""
research_folds -- the three fixed folds of time windows (E-077 PR-1, D-085).

A claim is never confirmed on the bars where it was observed. Each fold is six
exact 4-month blocks (config/folds.yaml); a child run of an idea backtests on
the next fold its LINEAGE has not used; a lineage that has used all three is
refused. Everything here is pure (no wall clock, no market data, no network);
the only files read are config/folds.yaml and the data policy.

Where the dates come from
-------------------------
folds.yaml names only the blocks. The research period and the two ranges a
block must stay out of are read from config/campaign_data_policy.yaml
(deny by default, strict days via tools/holdout_policy):
  * holdout   = holdout_range                                 (sealed, single-use)
  * validation = [earliest start of burned_ranges,
                  end of walk_forward_extension]              (2024-2025, single-use)
  * research  = backward_extension.BTCUSDT_1h, which must end the day before
                validation starts (checked: a gap or an overlap raises).
`load_folds` refuses a block outside the research period or inside either
range; the generator's validation guard (`assert_windows_clear_of_validation`)
reads the same validation range.

Lineage and "which fold has a run used"
---------------------------------------
Lineage of a run = the run itself plus every run named in its memory entry's
hypothesis_id. decide-next builds a child's hypothesis_id as
`<parent hypothesis_id>__<category>-<source run>-<n>`, so the chain of source
runs is spelled out in the id (`lineage_run_ids`).

A fold is USED by a lineage when any window of any lineage run overlaps any
block of that fold. That single rule covers every case without a special one:
a run on exactly fold B's blocks used B; run_065..run_074 (the six 4-month
2022-2023 windows) overlap only fold A's blocks, so they used A; a run on other
windows (1-month tiles, a different span) used whichever folds it overlaps, and
a run that overlaps no fold (outside 2018-2023) used none. If a lineage run's
windows cannot be read, the fold is NOT guessed: the assignment fails with a
reason (the candidate is infeasible) rather than risk re-using bars.
"""
from __future__ import annotations

import calendar
import re
from datetime import date, timedelta
from pathlib import Path

import yaml

import holdout_policy as _hp
import novelty as _nov

#: The real file. Tests pass their own path.
FOLDS_PATH = Path(__file__).resolve().parent.parent / "config" / "folds.yaml"

FOLD_ORDER = ("A", "B", "C")
BLOCKS_PER_FOLD = 6
BLOCK_MONTHS = 4

_LABEL = re.compile(r"[0-9]{4}-(01|05|09)")
_PID_SEGMENT = re.compile(r"[a-z][a-z_]*-(run_[0-9]+)-[0-9]+")


class FoldsError(ValueError):
    """config/folds.yaml, the policy ranges, or a lineage is unusable. A refusal, never a default."""


# ---------------------------------------------------------------------------
# The policy's ranges
# ---------------------------------------------------------------------------

def _day(value, where: str) -> str:
    d = _hp.iso_day(value)
    if d is None:
        raise FoldsError(f"{where} {value!r} is not a YYYY-MM-DD day")
    return d


def _pair_days(value, where: str) -> tuple:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise FoldsError(f"{where} {value!r} is not a [start, end] pair")
    start, end = _day(value[0], f"{where} start"), _day(value[1], f"{where} end")
    if end < start:
        raise FoldsError(f"{where} ends ({end}) before it starts ({start})")
    return start, end


def validation_range_of(policy: dict) -> tuple:
    """(start, end) of the validation period (2024-2025 in the current policy):
    from the earliest start of `burned_ranges` to the end of
    `walk_forward_extension`. Raises FoldsError when either key is missing or
    malformed -- no default."""
    burned = policy.get("burned_ranges")
    if not isinstance(burned, dict) or not burned:
        raise FoldsError("the data policy has no burned_ranges: cannot derive the validation period")
    start = min(_pair_days(v, f"burned_ranges.{k}")[0] for k, v in burned.items())
    _, end = _pair_days(policy.get("walk_forward_extension"), "walk_forward_extension")
    if end < start:
        raise FoldsError(f"validation period ends ({end}) before it starts ({start})")
    return start, end


def research_range_of(policy: dict) -> tuple:
    """(start, end) of the research period: backward_extension.BTCUSDT_1h, which
    must end the day before the validation period starts."""
    ext = policy.get("backward_extension")
    if not isinstance(ext, dict):
        raise FoldsError("the data policy has no backward_extension: cannot derive the research period")
    start, end = _pair_days(ext.get("BTCUSDT_1h"), "backward_extension.BTCUSDT_1h")
    v_start, _ = validation_range_of(policy)
    if (date.fromisoformat(end) + timedelta(days=1)).isoformat() != v_start:
        raise FoldsError(
            f"the research period ends {end} but the validation period starts {v_start}: "
            f"they must be contiguous (research end + 1 day == validation start)")
    return start, end


def policy_ranges(policy_path=None) -> dict:
    """{"research": (s, e), "validation": (s, e), "holdout": (s, e)} from the policy file."""
    try:
        policy = _hp.load_policy(policy_path)
        holdout = _hp.holdout_range_of(policy)
    except _hp.HoldoutPolicyError as exc:
        raise FoldsError(str(exc)) from exc
    return {"research": research_range_of(policy), "validation": validation_range_of(policy),
            "holdout": holdout}


def _overlaps(a: tuple, b: tuple) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


# ---------------------------------------------------------------------------
# The folds file
# ---------------------------------------------------------------------------

def _block_end(label: str) -> str:
    y, m = int(label[:4]), int(label[5:7])
    last_m = m + BLOCK_MONTHS - 1
    return date(y, last_m, calendar.monthrange(y, last_m)[1]).isoformat()


def load_folds(path=None, *, policy_path=None) -> dict:
    """The validated folds document: {"order": ["A","B","C"], "folds": {"A": [block, ...], ...}}
    where a block is {"label", "start", "end"}.

    Refuses (FoldsError): a file that cannot be read; an order other than A, B, C;
    a fold without exactly six blocks; a block that is not an exact 4-month
    calendar tile (label YYYY-01/05/09, start = its first day, end = its last
    day); the same label in two folds; blocks of one fold out of order; a block
    outside the research period or inside the validation period or the holdout
    (their dates read from the policy at `policy_path`, required)."""
    p = Path(path) if path is not None else FOLDS_PATH
    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise FoldsError(f"cannot read the folds file {p} ({type(exc).__name__}: {exc})") from exc
    if not isinstance(doc, dict) or doc.get("version") != 1:
        raise FoldsError(f"{p}: not a mapping with version: 1")
    if list(doc.get("order") or []) != list(FOLD_ORDER):
        raise FoldsError(f"{p}: order must be exactly {list(FOLD_ORDER)}, got {doc.get('order')!r}")
    raw = doc.get("folds")
    if not isinstance(raw, dict) or list(raw) != list(FOLD_ORDER):
        raise FoldsError(f"{p}: folds must hold exactly the keys {list(FOLD_ORDER)} in order")
    ranges = policy_ranges(policy_path)
    folds, seen = {}, {}
    for fid in FOLD_ORDER:
        blocks = raw[fid]
        if not isinstance(blocks, list) or len(blocks) != BLOCKS_PER_FOLD:
            raise FoldsError(f"{p}: fold {fid} must have exactly {BLOCKS_PER_FOLD} blocks")
        out, prev = [], None
        for b in blocks:
            if not isinstance(b, dict) or set(b) != {"label", "start", "end"}:
                raise FoldsError(f"{p}: fold {fid} block {b!r} must be exactly {{label, start, end}}")
            label = b["label"]
            if not (isinstance(label, str) and _LABEL.fullmatch(label)):
                raise FoldsError(f"{p}: fold {fid} label {label!r} is not YYYY-MM with month 01, 05 or 09 "
                                 f"(a 4-month tile that never crosses a year)")
            start, end = _day(b["start"], f"fold {fid} {label} start"), _day(b["end"], f"fold {fid} {label} end")
            if start != f"{label}-01" or end != _block_end(label):
                raise FoldsError(
                    f"{p}: fold {fid} block {label} must run {label}-01 .. {_block_end(label)} "
                    f"(end = the last INCLUDED day, D-058), got {start} .. {end}")
            if label in seen:
                raise FoldsError(f"{p}: block {label} is in fold {seen[label]} and fold {fid}")
            if prev is not None and label <= prev:
                raise FoldsError(f"{p}: fold {fid} blocks must be in ascending order ({prev} then {label})")
            seen[label], prev = fid, label
            rs, re_ = ranges["research"]
            if start < rs or end > re_:
                raise FoldsError(f"{p}: fold {fid} block {label} ({start}..{end}) is outside the research "
                                 f"period {rs}..{re_} (read from the data policy)")
            for name in ("validation", "holdout"):
                if _overlaps((start, end), ranges[name]):
                    raise FoldsError(f"{p}: fold {fid} block {label} ({start}..{end}) overlaps the "
                                     f"{name} period {ranges[name][0]}..{ranges[name][1]}")
            out.append({"label": label, "start": start, "end": end})
        folds[fid] = out
    return {"order": list(FOLD_ORDER), "folds": folds}


def fold_windows(doc: dict, fold: str) -> list:
    """The fold's windows in the protocol file's own shape --
    [{"label": "YYYY-MM", "test": {"start": ..., "end": ...}}, ...] -- exactly what
    `_generate_monthly_windows(window_months=4)` writes, so a run on a fold has the
    same `windows_sha256` (the novelty key's window part) as any run on those blocks."""
    if fold not in (doc.get("folds") or {}):
        raise FoldsError(f"unknown fold {fold!r} (folds: {list(doc.get('folds') or {})})")
    return [{"label": b["label"], "test": {"start": b["start"], "end": b["end"]}}
            for b in doc["folds"][fold]]


def fold_windows_sha256(doc: dict, fold: str) -> str:
    """The canonical sha256 of fold_windows -- the value tools/novelty.protocol_spec
    reports as `windows_sha256` for a protocol whose windows are those."""
    return _nov.windows_fingerprint(fold_windows(doc, fold))


def fold_span(doc: dict, fold: str) -> tuple:
    """(first block start, last block end) of a fold, for the protocol's start / end keys."""
    blocks = doc["folds"][fold]
    return blocks[0]["start"], blocks[-1]["end"]


def load_fold_windows(fold, *, path=None, policy_path=None) -> list:
    """Load + validate the folds file and return one fold's windows."""
    return fold_windows(load_folds(path, policy_path=policy_path), fold)


# ---------------------------------------------------------------------------
# Lineage and the next fold
# ---------------------------------------------------------------------------

def lineage_run_ids(run_id: str, hypothesis_id) -> list:
    """The run itself, then every run named in its hypothesis_id (decide-next writes
    `<parent id>__<category>-<source run>-<n>` for each generation), first-seen order."""
    out = [run_id]
    for seg in str(hypothesis_id or "").split("__"):
        m = _PID_SEGMENT.fullmatch(seg)
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


def windows_ranges(windows) -> list:
    """[(start, end), ...] of a protocol's `windows` list, or None when it cannot be read."""
    if not isinstance(windows, list) or not windows:
        return None
    out = []
    for w in windows:
        test = w.get("test") if isinstance(w, dict) else None
        if not isinstance(test, dict):
            return None
        s, e = _hp.iso_day(str(test.get("start"))[:10]), _hp.iso_day(str(test.get("end"))[:10])
        if s is None or e is None or e < s:
            return None
        out.append((s, e))
    return out


def folds_used_by(doc: dict, ranges) -> list:
    """The folds (in order) that any of these (start, end) ranges overlaps."""
    return [fid for fid in doc["order"]
            if any(_overlaps(r, (b["start"], b["end"])) for r in ranges for b in doc["folds"][fid])]


def assign_fold(doc: dict, *, run_id: str, memory_runs: dict, run_ranges: dict) -> dict:
    """Which fold a child of `run_id` backtests on.

    `memory_runs`: campaign memory's `runs` mapping. `run_ranges`: {run_id: [(start, end), ...]
    or None} -- each memory run's protocol windows (None = unreadable).

    Returns {"fold": "B" | None, "windows_sha256": ... | None, "lineage": [run ids],
    "used": {run_id: [folds]}, "reason": None | str}. `fold` is the first fold in A, B, C
    order that no lineage run has used. `reason` is set (and fold None) when the lineage
    has used all three (`folds_exhausted`) or when some lineage run is missing from memory
    or has unreadable windows (`fold_lineage_unreadable`) -- the safe direction: never
    guess a fold when the bars a line has seen are unknown."""
    entry = memory_runs.get(run_id)
    lineage = lineage_run_ids(run_id, (entry or {}).get("hypothesis_id"))
    used, unreadable = {}, []
    for rid in lineage:
        if rid not in memory_runs:
            unreadable.append(f"{rid} (not in campaign memory)")
            continue
        ranges = run_ranges.get(rid)
        if not ranges:
            unreadable.append(f"{rid} (its protocol windows cannot be read)")
            continue
        used[rid] = folds_used_by(doc, ranges)
    result = {"fold": None, "windows_sha256": None, "lineage": lineage, "used": used, "reason": None}
    if unreadable:
        result["reason"] = (f"fold_lineage_unreadable: the lineage of {run_id} ({', '.join(lineage)}) "
                            f"cannot be placed on the folds: {'; '.join(unreadable)}")
        return result
    taken = {f for fs in used.values() for f in fs}
    for fid in doc["order"]:
        if fid not in taken:
            result["fold"] = fid
            result["windows_sha256"] = fold_windows_sha256(doc, fid)
            return result
    result["reason"] = (f"folds_exhausted: the lineage of {run_id} ({', '.join(lineage)}) has used every "
                        f"fold ({', '.join(doc['order'])}); the next stage for this idea is validation "
                        f"(single-use), not another child run")
    return result


# ---------------------------------------------------------------------------
# The validation-period guard
# ---------------------------------------------------------------------------

class ValidationBoundaryBreach(ValueError):
    """A generated window would materialise bars inside the validation period."""


def assert_windows_clear_of_validation(windows: list, validation_range) -> None:
    """Refuse any window whose [start, end] overlaps the validation period.

    No validation stage exists yet, so under orchestrator.folds.enabled this refuses
    ALWAYS: the 2024-2025 bars are single-use and only the future validation stage
    may read them. `end` is inclusive by day at the engine (D-058), so a window ending
    on a validation day spends that day. Raises, never clamps (a silently trimmed sweep
    no longer matches what was pre-registered)."""
    v_start, v_end = validation_range
    for w in windows:
        label = w.get("label", "?")
        start, end = str(w["test"]["start"])[:10], str(w["test"]["end"])[:10]
        if _overlaps((start, end), (v_start, v_end)):
            raise ValidationBoundaryBreach(
                f"window {label!r} ({start}..{end}) overlaps the validation period "
                f"{v_start}..{v_end}. The validation period is single-use: only the future "
                f"validation stage may read it, and that stage does not exist yet, so under "
                f"orchestrator.folds.enabled no run may include it. Use a fold from "
                f"config/folds.yaml (research period only), or turn the flag off.")


def load_validation_range(policy_path=None) -> tuple:
    """The validation period read from the policy file (FoldsError when unusable)."""
    try:
        return validation_range_of(_hp.load_policy(policy_path))
    except _hp.HoldoutPolicyError as exc:
        raise FoldsError(str(exc)) from exc


# ---------------------------------------------------------------------------
# The fold a run was pre-registered on
# ---------------------------------------------------------------------------

def check_fold_id(fold) -> str:
    if fold not in FOLD_ORDER:
        raise FoldsError(f"fold {fold!r} is not one of {list(FOLD_ORDER)}")
    return fold


def fold_of_constraints(machine_constraints) -> str | None:
    """`machine_constraints.protocol.fold` (validated), or None when the run carries none."""
    proto = machine_constraints.get("protocol") if isinstance(machine_constraints, dict) else None
    if not isinstance(proto, dict) or "fold" not in proto:
        return None
    return check_fold_id(proto["fold"])


def fold_of_run_dir(run_dir) -> str | None:
    """The fold in the run's pre_registration.yaml (None for every run without one)."""
    p = Path(run_dir) / "artifacts" / "pre_registration.yaml"
    if not p.exists():
        return None
    try:
        pre = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return fold_of_constraints(pre.get("machine_constraints")) if isinstance(pre, dict) else None
