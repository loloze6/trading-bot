"""
Free-space guard — the recorder's own floor, checked while it runs.
===================================================================

WHY THE RECORDER NEEDS ONE AT ALL
---------------------------------
Nothing above this process is watching the disk. The capture writes ~0.115
GB/day in the configured snapshot cadence and ~8.7 GB/day raw in delta mode,
and it is designed to run for twelve months unattended. A full disk does not
announce itself: `write()` starts failing, shards stop growing, and — because
Kraken publishes no sequence numbers — the resulting hole is indistinguishable
from a quiet market to anyone reading the data later. That is the same
announce-success-over-a-hole shape `journal.py` exists to forbid.

So the floor is enforced here, in the process that is doing the writing, and a
breach is **attested**: it writes a `DISK_GUARD_ABORT` record to the coverage
journal before exiting, which closes every open coverage interval at a known
instant. A consumer reading the journal afterwards can tell a guard stop from a
crash, and the supervisor can tell "restart me" from "do not restart me into a
full disk".

CHECKED ON A TIMER, NOT ONLY AT STARTUP
---------------------------------------
A startup-only check answers the wrong question. The disk is not full when a
twelve-month capture begins; it becomes full some weeks in, possibly because of
something else entirely on the same volume. The guard therefore re-reads free
space on a fixed cadence for the whole life of the process.

DENY BY DEFAULT
---------------
If free space cannot be determined — the path is gone, the volume is
unreachable, `disk_usage` raises anything at all — that is a BREACH, not a
pass. An unmeasurable disk is exactly the state in which continuing to write is
least defensible, and a guard that fails open is not a guard. This mirrors
`holdout_date_gate.sh`'s rule that silence is never treated as success.

UNITS
-----
Decimal GB (1e9 bytes), matching the cadence ladder report's GB/day figures and
the storage projections in `campaign_data_policy.yaml`. Not GiB — mixing the two
in an operator-facing floor is how a 5 GB floor silently becomes 5.37.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional

#: Decimal GB, deliberately — see UNITS above.
GB = 1_000_000_000

#: Default floor. Chosen to be several days of headroom in the configured
#: snapshot cadence (~0.115 GB/day) while still leaving the host usable, and to
#: be large enough that the abort lands well before the OS itself starts
#: failing writes. Override with --min-free-gb.
DEFAULT_MIN_FREE_GB = 5.0

#: How often the running recorder re-reads free space.
DEFAULT_CHECK_INTERVAL_S = 30.0

#: Process exit code for an attested guard stop. Distinct from 0 (clean stop)
#: and from 1/2 (crash, unhandled error) precisely so the supervisor can refuse
#: to relaunch on this one without guessing. `supervise.ps1` reads it.
EXIT_DISK_GUARD_ABORT = 3


def probe_free_bytes(path: Path) -> Optional[int]:
    """
    Free bytes on the volume holding `path`, or None if that cannot be
    determined. None is a breach at the call site — see DENY BY DEFAULT.

    Every exception is swallowed into None on purpose: the guard's contract is
    "prove there is room, or stop", and there is no failure of this probe that
    should be allowed to propagate as anything other than "cannot prove it".
    """
    try:
        return int(shutil.disk_usage(str(path)).free)
    except Exception:  # noqa: BLE001 - see docstring
        return None


@dataclass(frozen=True)
class GuardReading:
    """One evaluation of the floor. `ok` False always means stop."""

    ok: bool
    free_bytes: Optional[int]
    min_free_bytes: int
    path: str
    reason: str

    @property
    def free_gb(self) -> Optional[float]:
        return None if self.free_bytes is None else self.free_bytes / GB

    @property
    def min_free_gb(self) -> float:
        return self.min_free_bytes / GB

    def as_journal_fields(self) -> Dict[str, Any]:
        """Fields for the DISK_GUARD_ABORT record — the attestation payload."""
        return {
            "path": self.path,
            "free_bytes": self.free_bytes,
            "free_gb": None if self.free_gb is None else round(self.free_gb, 3),
            "min_free_bytes": self.min_free_bytes,
            "min_free_gb": round(self.min_free_gb, 3),
            "reason": self.reason,
            "determinable": self.free_bytes is not None,
        }

    def summary(self) -> str:
        if self.free_bytes is None:
            return f"free space UNDETERMINABLE at {self.path} ({self.reason})"
        return (
            f"free {self.free_gb:.2f} GB vs floor {self.min_free_gb:.2f} GB "
            f"at {self.path}"
        )


class DiskGuard:
    """
    A floor plus a way to read the disk. `probe` is injectable so the breach
    and undeterminable paths are testable without filling a real volume.
    """

    def __init__(
        self,
        path: Path,
        min_free_gb: float = DEFAULT_MIN_FREE_GB,
        probe: Callable[[Path], Optional[int]] = probe_free_bytes,
    ):
        if min_free_gb <= 0:
            raise ValueError(
                f"min_free_gb must be > 0, got {min_free_gb!r} — a floor of zero "
                "or less is not a guard, and disabling the guard is not offered."
            )
        self.path = Path(path)
        self.min_free_bytes = int(round(min_free_gb * GB))
        self._probe = probe

    def check(self) -> GuardReading:
        free = self._probe(self.path)
        if free is None:
            return GuardReading(
                ok=False,
                free_bytes=None,
                min_free_bytes=self.min_free_bytes,
                path=str(self.path),
                reason="free space could not be determined (deny by default)",
            )
        if free < self.min_free_bytes:
            return GuardReading(
                ok=False,
                free_bytes=free,
                min_free_bytes=self.min_free_bytes,
                path=str(self.path),
                reason="free space below configured floor",
            )
        return GuardReading(
            ok=True,
            free_bytes=free,
            min_free_bytes=self.min_free_bytes,
            path=str(self.path),
            reason="ok",
        )
