"""
Single-writer campaign launch lock (E-011 S1b).

WHY THIS EXISTS: `campaign_state.yaml` (cross-run campaign history, including
the trial count `deflate_sharpe.py` needs) is read-modify-written with zero
locking anywhere (`run_phase1_research.py::load_campaign_state()` /
`_save_campaign_state()`). If two people launch a campaign on the shared
culi.to host around the same time, both can read the same stale state and
one's write silently clobbers the other's -- a lost trial, corrupting the
count the whole research protocol's statistical honesty depends on.

DECIDED SCOPE (Jeremy, 2026-09-09): fix this the simple way -- only ONE
campaign may run at a time on the shared host. A second launch while one is
already running refuses to start with a clear message, rather than silently
racing. This is deliberately NOT true concurrent-safe multi-writer support
(letting both run simultaneously with per-write locking on campaign_state.yaml
itself) -- that is real engineering, scoped separately as E-051, only worth
building if this simpler fix turns out to be a real bottleneck in practice.

WHAT THIS MODULE DOES NOT DO: it does not lock individual writes to
campaign_state.yaml, and it does not make concurrent campaigns safe. It only
ensures at most one `run_campaign.py` `run_forever()` loop is active at once,
by way of one lock file on disk.

Lock file contents (JSON): pid, hostname, started_at (UTC ISO8601). Written
atomically (O_CREAT|O_EXCL, so two racing acquires can't both "win" the
create) alongside campaign_state.yaml.

Staleness: a lock is stale (safe to clear) when EITHER (a) its pid was
recorded on THIS host and that pid is no longer alive, OR (b) the lock file's
mtime is older than STALE_LOCK_AGE_SECONDS. Cross-host locks (different
hostname than us) can only be judged by age -- we have no portable way to ask
another machine whether a pid is alive. Never auto-clear on a guess: if
neither condition is confirmed, the lock is treated as held.
"""
from __future__ import annotations

import contextlib
import json
import os
import socket
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOCK_FILENAME = ".campaign.lock"

# Conservative bound: a single campaign step (one LLM-authored stage) can take
# minutes; a whole run_forever() session can run for hours. 6h is well past any
# observed real run but still catches a genuinely abandoned/crashed lock in a
# reasonable time without a human having to intervene for every long session.
STALE_LOCK_AGE_SECONDS = 6 * 60 * 60


class CampaignLockHeld(RuntimeError):
    """Raised when another process appears to hold the campaign lock."""


@dataclass
class LockInfo:
    pid: int
    hostname: str
    started_at: str  # ISO8601 UTC, informational only -- staleness uses file mtime


def lock_path_for(campaign_state_path: Path) -> Path:
    """The lock lives next to campaign_state.yaml (same directory)."""
    return campaign_state_path.parent / LOCK_FILENAME


def _pid_is_alive(pid: int) -> Optional[bool]:
    """Best-effort liveness check for `pid` on THIS host.

    Returns True/False when determinable, None when it cannot be determined
    on this platform -- callers must fall back to age-based staleness rather
    than guess.
    """
    if pid <= 0:
        return False
    if os.name == "posix":
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True  # exists, just not signalable by us -- still alive
        except OSError:
            return None
    else:
        # Windows: os.kill(pid, 0) is not a reliable existence probe (it
        # actually terminates on some Python/OS combos), so use the Win32
        # API via ctypes instead of assuming POSIX semantics.
        try:
            import ctypes

            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = ctypes.windll.kernel32.OpenProcess(  # type: ignore[attr-defined]
                PROCESS_QUERY_LIMITED_INFORMATION, False, pid
            )
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)  # type: ignore[attr-defined]
                return True
            return False
        except Exception:
            return None


def _read_lock(lock_path: Path) -> Optional[LockInfo]:
    """Parse the lock file. Returns None if it's absent, unreadable, or
    malformed -- callers treat that as "can't identify the holder", which
    falls back to age-only staleness rather than "no lock"."""
    try:
        raw = lock_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return LockInfo(
            pid=int(data["pid"]),
            hostname=str(data.get("hostname", "?")),
            started_at=str(data.get("started_at", "?")),
        )
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _is_stale(lock_path: Path, info: Optional[LockInfo]) -> tuple[bool, str]:
    """Decide whether an existing lock is safe to clear. Never guesses:
    confirms via live pid-check (same host) or a hard age threshold."""
    if info is not None and info.hostname == socket.gethostname():
        alive = _pid_is_alive(info.pid)
        if alive is True:
            return False, ""
        if alive is False:
            return True, f"pid {info.pid} on {info.hostname} is no longer running"
        # alive is None (undeterminable on this platform) -- fall through to age.

    try:
        age_seconds = time.time() - lock_path.stat().st_mtime
    except OSError:
        # Can't even stat it (e.g. removed between read and stat) -- treat
        # conservatively as not confirmed stale; the caller's retry loop
        # will re-read on the next attempt.
        return False, ""

    if age_seconds > STALE_LOCK_AGE_SECONDS:
        hours = age_seconds / 3600.0
        threshold_hours = STALE_LOCK_AGE_SECONDS / 3600.0
        return True, f"lock file is {hours:.1f}h old (> {threshold_hours:.0f}h staleness threshold)"
    return False, ""


def _write_lock_exclusive(lock_path: Path) -> bool:
    """Attempt to create the lock file exclusively. Returns True on success,
    False if it already exists (FileExistsError) -- the atomic primitive that
    makes two racing acquires resolve to exactly one winner."""
    payload = {
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    return True


def acquire(lock_path: Path) -> None:
    """Acquire the campaign lock at `lock_path`.

    Raises CampaignLockHeld if another process's lock is present and not
    confirmed stale. Clears a confirmed-stale lock itself (logging why) and
    retries once. Never silently waits, never silently proceeds past a live
    lock.
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    for _attempt in range(2):
        if _write_lock_exclusive(lock_path):
            return

        existing = _read_lock(lock_path)
        stale, reason = _is_stale(lock_path, existing)
        if not stale:
            if existing is not None:
                who = f"pid={existing.pid}, host={existing.hostname}, started={existing.started_at} UTC"
            else:
                who = "contents unreadable/corrupt"
            raise CampaignLockHeld(
                "Another campaign appears to be running -- refusing to start.\n"
                f"  Lock file : {lock_path}\n"
                f"  Held by   : {who}\n"
                "  If you are SURE this is a stale lock from a crashed run, confirm no "
                "run_campaign.py process is actually alive (`ps aux | grep run_campaign` "
                "on Linux/mac, Task Manager / `Get-Process python` on Windows) and then "
                f"delete it manually: rm {lock_path}"
            )

        print(f"[campaign_lock] clearing stale lock ({reason}): {lock_path}")
        with contextlib.suppress(FileNotFoundError):
            lock_path.unlink()
        # loop back and retry the exclusive create

    raise CampaignLockHeld(
        f"Could not acquire the campaign lock at {lock_path}: a new lock appeared "
        "immediately after a stale one was cleared, meaning another process is "
        "racing to launch right now. Retry the launch."
    )


def release(lock_path: Path) -> None:
    """Remove the lock file. Safe to call even if it's already gone."""
    with contextlib.suppress(FileNotFoundError):
        lock_path.unlink()


@contextlib.contextmanager
def held(lock_path: Path):
    """Context manager: acquire on entry, release on exit (including on
    exception) -- use this to bracket exactly one real campaign run."""
    acquire(lock_path)
    try:
        yield
    finally:
        release(lock_path)
