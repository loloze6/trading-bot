"""
Content-aware cache-presence predicate for the shared `_NEEDED_CACHES` guard
convention (test_close_positions_at_end.py, test_regression_backtest.py,
test_warmup_prefetch_bit_identical.py, test_bar_equity_bit_identical.py,
test_commission_rate_param.py).

A bare `.exists()` check treats a 0-byte file, a header-only file, or a file
whose data never reaches the module's window as "present" -- so the guarded
tests RUN on garbage instead of skipping. `cache_skip_reason` closes that: a
cache only counts as usable if it exists, has at least one parseable data
row, and its [first_ts, last_ts] span covers the caller's declared window.

CONTRACT BOUND: this predicate reads only the header, the first data row,
and the last complete tail row of each file (an O(1) head+tail+span check,
not a full scan). Mid-file gaps or corruption (G1-class) are OUT OF
CONTRACT -- that is the engine's own gap-guard problem, already tracked
separately. Two shapes pass this predicate without being a hole, because
they fail LOUDLY at run time rather than going vacuous:
  (a) a last-day-partial cache: the last row lands exactly at `window_end`
      but is missing that day's remaining bars.
  (b) a cache whose data starts exactly at `window_start`: passes the span
      check but lacks the ~120-bar warmup lookback the engine needs, so the
      run proceeds and diverges from the fixture values loudly.
Neither can produce the vacuous all-zeros pass this predicate exists to
prevent, since both leave in-window data for the run to diverge on.

MEMOIZATION: per-file spans are cached in a module-level dict keyed by
resolved path, for the life of the process. This assumes cache files are
immutable within a process -- true for the real caches (unchanged mid
test-session) and true for the unit tests (each case uses its own
tmp_path-scoped file, so paths never collide across cases).

WHY THIS CAN'T HANG OR BLOAT COLLECTION: this predicate runs at import of
every guarded module, including the FAST suite (pytest.ini's
`--timeout=30` applies to collection too). Every read is local-disk only
(no network), and the tail read is a single slice of the file's last 4096
bytes rather than a full scan -- O(1) per file regardless of cache size.
"""

from datetime import date, datetime
from pathlib import Path

_TAIL_READ_BYTES = 4096
_SPAN_CACHE: dict[Path, tuple[date, date] | str] = {}


def _parse_date(value: str) -> date:
    return datetime.fromisoformat(value).date()


def _first_field(line: str) -> str:
    return line.split(",", 1)[0].strip()


def _inspect(path: Path) -> tuple[date, date] | str:
    """Return (first_ts, last_ts) as dates, or a reason string naming the
    failure mode, for the single cache file at `path`."""
    key = path.resolve()
    if key in _SPAN_CACHE:
        return _SPAN_CACHE[key]

    result: tuple[date, date] | str
    try:
        if not path.exists():
            result = "not present"
        else:
            raw = path.read_bytes()
            if not raw:
                result = "empty file"
            else:
                lines = raw.decode("utf-8").splitlines()
                if len(lines) < 2:
                    result = "no data rows"
                else:
                    try:
                        first_ts = _parse_date(_first_field(lines[1]))
                    except ValueError:
                        result = "unparseable first data row"
                    else:
                        tail_lines = [
                            ln
                            for ln in raw[-_TAIL_READ_BYTES:]
                            .decode("utf-8", errors="ignore")
                            .splitlines()
                            if ln.strip()
                        ]
                        last_ts = None
                        if tail_lines:
                            try:
                                last_ts = _parse_date(_first_field(tail_lines[-1]))
                            except ValueError:
                                last_ts = None
                        result = (
                            (first_ts, last_ts)
                            if last_ts is not None
                            else "unparseable final row (truncated?)"
                        )
    except Exception as exc:
        result = f"unreadable ({type(exc).__name__})"

    _SPAN_CACHE[key] = result
    return result


def cache_skip_reason(
    local_data: Path,
    needed: tuple[str, ...],
    window_start: str,
    window_end: str,
) -> str | None:
    """Return None if every cache in `needed` under `local_data` is usable
    for the inclusive [window_start, window_end] window ("YYYY-MM-DD"
    strings), else a reason naming the first offending file and mode.
    """
    start = _parse_date(window_start)
    end = _parse_date(window_end)
    for name in needed:
        outcome = _inspect(local_data / name)
        if isinstance(outcome, str):
            return f"local_data cache {name}: {outcome}"
        first_ts, last_ts = outcome
        if not (first_ts <= start and last_ts >= end):
            return (
                f"local_data cache {name}: does not cover {window_start}..{window_end} "
                f"(span {first_ts.isoformat()}..{last_ts.isoformat()})"
            )
    return None
