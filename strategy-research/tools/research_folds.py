"""
research_folds -- the three fixed folds of time windows (E-077 PR-1, D-085).

A claim is never confirmed on the bars where it was observed. Each fold is six
exact 4-month blocks (config/folds.yaml). D-123 (operator decision 2026-10-13,
replacing D-085's lineage order): a child run backtests on a fold drawn at random
among the folds (A, B, C and D) its SOURCE run's windows do not overlap, the draw
seeded by the child's id so it is reproducible (`draw_fold`). Everything here is
pure (no wall clock, no market data, no network); the only files read are
config/folds.yaml and the data policy.

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
`load_folds` refuses a block of A-C outside the research period or inside either
range. D-115 (operator decision 2026-10-13): there is no validation stage; fold D
(six contiguous 4-month blocks of 2024-2025, inside the validation range, outside
the holdout) is defined in the folds file but is NOT in `order` A, B, C; since D-123
decide-next's draw includes it; a brief carrying `fold: "D"` is generated only under
orchestrator.folds.enabled. The validation guard (`assert_windows_clear_of_validation`) reads the
same validation range. Under orchestrator.folds.enabled the guard runs at every
place a protocol's windows are fixed or used: the protocol generator, the launch
pre-flight (generated, pinned and run_context-resolved protocols alike), and
tools/run_protocol.py itself, which every backtest goes through -- so a pinned
file such as protocols/baseline_v2.json, a replication_diagnostic run
(baseline_v1.json) and a last_escalation protocol are refused too, not only
generated ones.

Which fold a run is on
----------------------
A run is ON a fold when any of its windows overlaps any block of that fold
(`folds_overlapped`, all four folds): a run on exactly fold B's blocks is on B;
run_065..run_074 (the six 4-month 2022-2023 windows) are on A; a run on other
windows is on whichever folds it overlaps (an overlap of one day counts). If the
source run's windows cannot be read, no fold is drawn: the assignment fails with a
reason (the candidate is infeasible) rather than risk re-using its bars.
"""
from __future__ import annotations

import calendar
import hashlib
import random
import re
from datetime import date, timedelta
from pathlib import Path

import yaml

import holdout_policy as _hp
import novelty as _nov

#: The real file. Tests pass their own path.
FOLDS_PATH = Path(__file__).resolve().parent.parent / "config" / "folds.yaml"

FOLD_ORDER = ("A", "B", "C")
#: D-115: the fold of the 2024-2025 period, defined in the folds file after A, B, C but
#: outside the automatic order (FOLD_ORDER): decide-next never assigns it.
FOLD_D = "D"
#: Every fold the folds file defines, in file order.
ALL_FOLDS = FOLD_ORDER + (FOLD_D,)
BLOCKS_PER_FOLD = 6
BLOCK_MONTHS = 4

_LABEL = re.compile(r"[0-9]{4}-(01|05|09)")


class FoldsError(ValueError):
    """config/folds.yaml or the policy ranges are unusable. A refusal, never a default."""


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
    if not isinstance(raw, dict) or list(raw) != list(ALL_FOLDS):  # D-115: D defined, not ordered
        raise FoldsError(f"{p}: folds must hold exactly the keys {list(ALL_FOLDS)} in order")
    ranges = policy_ranges(policy_path)
    folds, seen = {}, {}
    for fid in ALL_FOLDS:
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
            home = "validation" if fid == FOLD_D else "research"  # D-115: fold D is 2024-2025
            rs, re_ = ranges[home]
            if start < rs or end > re_:
                raise FoldsError(f"{p}: fold {fid} block {label} ({start}..{end}) is outside the {home} "
                                 f"period {rs}..{re_} (read from the data policy)")
            for name in (("holdout",) if fid == FOLD_D else ("validation", "holdout")):
                if _overlaps((start, end), ranges[name]):
                    if name == "holdout":  # D-173: the sealed range and the block's days are withheld
                        raise FoldsError(f"{p}: fold {fid} has a block that overlaps the holdout "
                                         f"period in config/campaign_data_policy.yaml "
                                         f"(holdout_range; dates withheld)")
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
# Which fold a run is on, and the child's fold draw (D-123)
# ---------------------------------------------------------------------------

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


def folds_overlapped(doc: dict, ranges) -> list:
    """D-123: every fold of the file (A, B, C, then D) any of these (start, end) ranges
    overlaps -- the folds a run is on."""
    return [fid for fid in ALL_FOLDS
            if any(_overlaps(r, (b["start"], b["end"])) for r in ranges for b in doc["folds"][fid])]


def draw_seed(key: str) -> int:
    """D-123: the draw's seed, derived from `key` (the child's candidate id), so the same
    candidate draws the same fold at every decision and the draw can be replayed."""
    return int(hashlib.sha256(str(key).encode("utf-8")).hexdigest()[:16], 16)


def draw_fold(doc: dict, *, run_id: str, run_ranges: dict, seed_key: str,
              usable=None) -> dict:
    """D-123 (operator decision 2026-10-13): which fold a child of `run_id` backtests on.

    The source run's folds are the folds its windows overlap (`run_ranges[run_id]`);
    the child's fold is drawn with random.Random(draw_seed(seed_key)) among the other
    folds of ALL_FOLDS (A, B, C, D), keeping only those `usable(fold)` returns None for
    (the caller's data check; None = every fold usable).

    Returns {"fold", "windows_sha256", "source_folds", "drawn_from", "seed", "reason"}.
    `reason` is set (and fold None) when the source run's windows cannot be read
    (`fold_source_unreadable`) or no other fold is usable (`no_other_fold`, naming why
    each one was left out) -- never guessed."""
    seed = draw_seed(seed_key)
    result = {"fold": None, "windows_sha256": None, "source_folds": None, "drawn_from": [],
              "seed": seed, "reason": None}
    ranges = run_ranges.get(run_id)
    if not ranges:
        result["reason"] = (f"fold_source_unreadable: {run_id}'s protocol windows cannot be "
                            f"read, so the fold its claim was found on is unknown")
        return result
    source = folds_overlapped(doc, ranges)
    result["source_folds"] = source
    left_out = []
    for fid in ALL_FOLDS:
        if fid in source:
            continue
        why = usable(fid) if usable is not None else None
        if why:
            left_out.append(f"{fid}: {why}")
        else:
            result["drawn_from"].append(fid)
    if not result["drawn_from"]:
        result["reason"] = (f"no_other_fold: {run_id} is on {source or 'no fold'}; no other fold "
                            f"is usable" + (f" ({'; '.join(left_out)})" if left_out else ""))
        return result
    fold = random.Random(seed).choice(result["drawn_from"])
    result["fold"] = fold
    result["windows_sha256"] = fold_windows_sha256(doc, fold)
    return result


# ---------------------------------------------------------------------------
# The validation-period guard
# ---------------------------------------------------------------------------

class ValidationBoundaryBreach(ValueError):
    """A generated window would materialise bars inside the validation period."""


def assert_windows_clear_of_validation(windows: list, validation_range, fold_d_windows=()) -> None:
    """Refuse any window whose [start, end] overlaps the validation period, unless it is
    exactly one of fold D's blocks (D-115: no validation stage; label, start and end
    must all match).

    `fold_d_windows`: fold D's windows, or a zero-argument function returning them,
    called only when some window overlaps the period (so a protocol clear of 2024-2025
    never reads the folds file); () lets nothing through. Enforced by the callers
    listed in the module docstring; this function is the one check they all share
    (and the one message). `end` is inclusive by day at the engine (D-058), so a window ending
    on a validation day spends that day. Raises, never clamps (a silently trimmed sweep
    no longer matches what was pre-registered)."""
    v_start, v_end = validation_range
    allowed = None
    for w in windows:
        label = w.get("label", "?")
        start, end = str(w["test"]["start"])[:10], str(w["test"]["end"])[:10]
        if not _overlaps((start, end), (v_start, v_end)):
            continue
        if allowed is None:
            blocks = fold_d_windows() if callable(fold_d_windows) else fold_d_windows
            allowed = {(str(b.get("label")), str(b["test"]["start"])[:10],
                        str(b["test"]["end"])[:10]) for b in blocks}
        if (str(label), start, end) not in allowed:
            raise ValidationBoundaryBreach(
                f"window {label!r} ({start}..{end}) overlaps the validation period "
                f"{v_start}..{v_end} and is not one of fold D's blocks. D-115: there is no "
                f"validation stage; under orchestrator.folds.enabled a run may include that "
                f"period only as fold D's exact blocks (config/folds.yaml). Use a fold's "
                f"blocks, or turn the flag off.")


def load_fold_d_windows(*, path=None, policy_path=None) -> list:
    """D-115: fold D's windows, for the validation guard's callers."""
    return load_fold_windows(FOLD_D, path=path, policy_path=policy_path)


#: config/campaign_config.yaml, where orchestrator.folds.enabled lives.
CAMPAIGN_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "campaign_config.yaml"


def folds_flag_enabled(config_path=None) -> bool:
    """orchestrator.folds.enabled read straight from the config file, for the one caller
    that cannot import the orchestrator (tools/run_protocol.py -- a standalone tool every
    backtest passes through). Same reading as run_phase1_research._folds_enabled: False
    when the file, the section or the key is absent; a non-bool value raises FoldsError."""
    path = Path(config_path) if config_path is not None else CAMPAIGN_CONFIG_PATH
    if not path.exists():
        return False
    try:
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise FoldsError(f"{path} cannot be read ({type(exc).__name__}: {exc})") from exc
    folds_cfg = ((cfg.get("orchestrator") or {}).get("folds") or {}) if isinstance(cfg, dict) else {}
    value = folds_cfg.get("enabled", False)
    if not isinstance(value, bool):
        raise FoldsError(f"orchestrator.folds.enabled={value!r} is not a real boolean "
                         f"(got {type(value).__name__})")
    return value


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
    """A fold the folds file defines (D-115: D included, so a fold-D run's memory entry and
    trial rows record it). Whether a brief may run on fold D is decided by the generator
    (run_phase1_research._protocol_windows_from_constraints: flag on only)."""
    if fold not in ALL_FOLDS:
        raise FoldsError(f"fold {fold!r} is not one of {list(ALL_FOLDS)}")
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
