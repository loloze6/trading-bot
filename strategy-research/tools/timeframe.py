"""
Timeframe arithmetic, derived rather than enumerated.

WHY THIS MODULE EXISTS
----------------------
The A8.6 a-priori power gate divides a hypothesis's active sample by an
autocorrelation `block_size` whose meaning is BARS PER DAY (stated verbatim at
tools/power_check.py's own constant: "1h bars per autocorrelation episode
(bars per day)").

That quantity was, until 2026-08-27, held in a two-entry lookup table
`{"1h": 24, "1d": 1}` with a silent `.get(timeframe, 24)` fallback. Any
timeframe not in the table inherited the 1h value. For 4h that made n_eff 4x
too small and min_detectable_ic 2x too large -- biased entirely toward killing
hypotheses. It killed run_060 (the first real campaign launch in 39 days) with
a verdict that was an artifact, not a finding:

    active_n = 2205
    block 24 (wrong) -> n_eff  91.9 -> mde 0.1061 > 0.1 -> insufficient_power
    block  6 (right) -> n_eff 367.5 -> mde 0.0524 < 0.1 -> power_adequate

This had already happened ONCE, for daily bars: see the 2026-07-07 comment in
run_phase1_research.py ("n_eff off by a full 24x"). That fix added `1d` to a
table and kept the silent default -- fixing the instance while guaranteeing the
recurrence. THE TABLE IS THE BUG. Operator ruling 2026-08-27: "think about
something that would cover any timeframe. i do not want to face it again and
again when we try a new timeframe."

So: derive it. `bars_per_day` is arithmetic on the timeframe, not a fact to be
remembered, and a timeframe nobody has tried yet is correct on first use.

SINGLE SOURCE OF TRUTH
----------------------
Three sites previously held their own copy, with only comments ("both must be
updated together") holding them in sync -- a convention, not a mechanism. All
three now import from here:

    workflow/run_phase1_research.py   (the A8.6 gate)
    tools/power_check.py              (the standalone mirror)
    tools/prescreen_signal.py         (the prescreen tool)

Deliberately self-contained: this does NOT import trading-bot's own interval
helper. Making a strategy-research decision gate depend on engine internals
across the tree, for a few lines of parsing, is the worse trade.
"""

import re

_SECONDS_PER_DAY = 86400

# Unit suffixes as used throughout this project's protocols and briefs
# ("1m", "15m", "1h", "4h", "1d", "1w"). Seconds per unit.
_UNIT_SECONDS = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
}

_TIMEFRAME_RE = re.compile(r"^\s*(\d+)\s*([smhdw])\s*$", re.IGNORECASE)


def timeframe_seconds(timeframe) -> int:
    """Seconds in one bar of `timeframe`.

    Accepts the project's standard strings ("5m", "1h", "4h", "1d", "1w") and
    a bare int/float, which is taken to already be seconds.

    RAISES on anything unparseable rather than returning a default. The silent
    default is the exact mechanism behind this module's originating bug: a
    value feeding a kill/no-kill decision must never be quietly assumed.
    """
    if isinstance(timeframe, bool):
        raise ValueError(
            f"timeframe must be a string or number, got bool: {timeframe!r}"
        )
    if isinstance(timeframe, (int, float)):
        if timeframe <= 0:
            raise ValueError(f"timeframe seconds must be positive, got {timeframe!r}")
        return int(timeframe)
    if not isinstance(timeframe, str):
        raise ValueError(
            f"cannot derive a timeframe from {type(timeframe).__name__}: {timeframe!r}"
        )
    m = _TIMEFRAME_RE.match(timeframe)
    if not m:
        raise ValueError(
            f"unrecognised timeframe {timeframe!r}. Expected <number><unit> with unit "
            f"in {sorted(_UNIT_SECONDS)} (e.g. '5m', '1h', '4h', '1d'). Refusing to "
            f"guess -- a silently-defaulted timeframe is what caused the A8.6 "
            f"block_size bug this module exists to prevent."
        )
    count, unit = int(m.group(1)), m.group(2).lower()
    if count <= 0:
        raise ValueError(f"timeframe count must be positive, got {timeframe!r}")
    return count * _UNIT_SECONDS[unit]


def bars_per_day(timeframe) -> int:
    """Autocorrelation block size: how many bars of `timeframe` make one day.

    This is the A8.6 gate's `block_size`. Derived, so a timeframe never used
    before is correct on first use and nothing has to be added to a table.

    Reproduces both values the old table held, which is the check that this is
    the same quantity and not a new convention:
        1h -> 24        1d -> 1

    Floored at 1: for a timeframe of a day or longer (1d, 1w) the ratio is <= 1,
    and a bar that already spans a day or more is at least one independent
    episode. Without the floor, 1w would yield 0.14 and the division downstream
    would inflate n_eff wildly -- failing in the opposite, far more dangerous
    direction (wrongly declaring power).
    """
    return max(1, round(_SECONDS_PER_DAY / timeframe_seconds(timeframe)))
