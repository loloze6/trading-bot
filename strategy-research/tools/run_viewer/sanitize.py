"""
sanitize.py -- the run viewer's one output filter (D-180, operator ruling 2026-10-23,
option A for wall-clock dates).

Every string that leaves the viewer (JSON values AND keys, raw file text, error and
reason strings, the static page, the banner, the request log line) passes through
`sanitize` / `sanitize_text`. A date whose day falls inside the sealed holdout window
is replaced by "[sealed-window date]". No exemptions: provenance timestamps are masked
the same as any other date.

The window is read ONCE per process (lazily, on first use), from the policy file next to
this tool -- `Path(__file__).resolve().parents[2] / "config" / "campaign_data_policy.yaml"`
-- through tools/holdout_policy.py, independent of the viewer's --root. It is held in a
private module value only: never logged, never returned by any function, never put in an
exception message or a repr. The public API is exactly `sanitize(obj)` and
`sanitize_text(text)` (a test pins the module's public names).

Fail closed: if the policy is absent or unreadable the module raises a fixed-text error and never
returns unmasked data.

Token shapes masked, when the date they spell falls inside the window:
  * YYYY-MM-DD, also when followed by T or a space and a time (and an optional
    fraction / Z / offset): the whole token is replaced;
  * compact YYYYMMDD, also when followed by T<time>Z (results stamps like
    YYYYMMDDTHHMMSSZ, with an optional _<hash> suffix): the whole stamp is replaced;
  * YYYY-MM month tokens whose month intersects the window.
"""
import re as _re
import sys as _sys
from datetime import date as _date
from pathlib import Path as _Path

__all__ = ["sanitize", "sanitize_text"]

_MASK = "[sealed-window date]"
_FAIL_TEXT = "run viewer: sealed-window policy unreadable; not starting"
_POLICY_PATH = _Path(__file__).resolve().parents[2] / "config" / "campaign_data_policy.yaml"

_TOOLS_DIR = str(_Path(__file__).resolve().parents[1])

_range = None  # (date, date) once loaded; private, never exposed

_FULL = _re.compile(
    r"(?<![0-9A-Za-z])(\d{4})-(\d{2})-(\d{2})"
    r"(?:[T ]\d{2}:\d{2}(?::\d{2}(?:[.,]\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?)?(?![0-9])"
)
_COMPACT = _re.compile(
    r"(?<![0-9A-Za-z])(\d{4})(\d{2})(\d{2})(?:T\d{4,6}(?:\.\d+)?Z?(?:_[0-9a-f]{6,12})?)?(?![0-9])"
)
_MONTH = _re.compile(r"(?<![0-9A-Za-z-])(\d{4})-(\d{2})(?![0-9-])")


class _SanitizeError(RuntimeError):
    """Fixed-text failure: the sealed-window policy could not be read."""

    def __init__(self):
        super().__init__(_FAIL_TEXT)


def _load():
    global _range
    if _range is not None:
        return _range
    try:
        if _TOOLS_DIR not in _sys.path:
            _sys.path.insert(0, _TOOLS_DIR)
        import holdout_policy  # tools/ sibling: the one strict reader of the range

        start, end = holdout_policy.load_holdout_range(_POLICY_PATH)
        lo = _date.fromisoformat(start)
        hi = _date.fromisoformat(end)
    except Exception:  # noqa: BLE001 -- never leak the cause (it can name paths or dates)
        raise _SanitizeError() from None
    _range = (lo, hi)
    return _range


def _ensure_ready() -> None:
    """Server start-up check: raises _SanitizeError (fixed text) when the policy is unreadable."""
    _load()


def _day(y: str, m: str, d: str):
    try:
        return _date(int(y), int(m), int(d))
    except ValueError:
        return None


def _in_window(day, lo, hi) -> bool:
    return day is not None and lo <= day <= hi


def sanitize_text(text):
    """Mask every in-window date token in `text`. Non-strings are returned unchanged."""
    if not isinstance(text, str):
        return text
    lo, hi = _load()
    if not any(ch.isdigit() for ch in text):
        return text

    def full(m):
        return _MASK if _in_window(_day(m.group(1), m.group(2), m.group(3)), lo, hi) else m.group(0)

    def compact(m):
        return _MASK if _in_window(_day(m.group(1), m.group(2), m.group(3)), lo, hi) else m.group(0)

    def month(m):
        y, mo = int(m.group(1)), int(m.group(2))
        if not 1 <= mo <= 12:
            return m.group(0)
        first = _date(y, mo, 1)
        last = _date(y + (mo == 12), 1 if mo == 12 else mo + 1, 1).toordinal() - 1
        if first <= hi and _date.fromordinal(last) >= lo:
            return _MASK
        return m.group(0)

    out = _FULL.sub(full, text)
    out = _COMPACT.sub(compact, out)
    out = _MONTH.sub(month, out)
    return out


def sanitize(obj):
    """Return `obj` with every string (values and mapping keys) masked. Containers are
    rebuilt, never mutated, so cached parsed documents stay untouched."""
    if isinstance(obj, str):
        return sanitize_text(obj)
    if isinstance(obj, dict):
        return {(sanitize_text(k) if isinstance(k, str) else k): sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    return obj

