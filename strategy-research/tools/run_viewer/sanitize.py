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

Token shapes masked, when the day (or the month / quarter / half) they spell intersects
the window. One left-to-right pass over the text: at each position the leftmost token
wins (so "5 May YYYY" is read as a day, not as the month "May YYYY"), and a token whose
period does not intersect the window is left as it was.
  * ISO YYYY-MM-DD, also when followed by T or a space and a time (and an optional
    fraction / Z / offset): the whole token is replaced. The only guard before it is
    "not a digit", so it is masked when glued after letters too;
  * YYYY/MM/DD, YYYY.MM.DD, YYYY_MM_DD (one separator used twice);
  * D/M/YYYY, M/D/YYYY, D.M.YYYY, D-M-YYYY (masked when EITHER the day/month reading or
    the month/day reading is inside the window);
  * "D Mon YYYY", "D Month YYYY", "Mon D, YYYY", "Month D, YYYY", "DD-Mon-YYYY" (English
    month names and 3-letter abbreviations, case-insensitive, optional ordinal suffix);
  * compact YYYYMMDD, also when followed by T<time>Z (results stamps like
    YYYYMMDDTHHMMSSZ, with an optional _<hash> suffix): the whole stamp is replaced;
  * months: YYYY-MM, YYYY/MM, MM/YYYY, "Month YYYY", "Mon YYYY";
  * quarter labels (Q1..Q4 with a year, either order, "Q1 YYYY" / "YYYY Q1" / "YYYYQ1" /
    "YYYY-Q1" / "Q1-YYYY") and half labels (H1/H2, same forms).

Known limits, NOT masked: epoch numbers, ISO week dates (YYYY-Www-D), ordinal dates
(YYYY-DDD), two-digit years, and any date spelled in a language other than English.
"""
import sys as _sys

_sys.dont_write_bytecode = True  # before any tools/ import: never write .pyc under the repo

import re as _re  # noqa: E402
from datetime import date as _date  # noqa: E402
from pathlib import Path as _Path  # noqa: E402

__all__ = ["sanitize", "sanitize_text"]

_MASK = "[sealed-window date]"
_FAIL_TEXT = "run viewer: sealed-window policy unreadable; not starting"
_POLICY_PATH = _Path(__file__).resolve().parents[2] / "config" / "campaign_data_policy.yaml"

_TOOLS_DIR = str(_Path(__file__).resolve().parents[1])

_range = None  # (date, date) once loaded; private, never exposed

_MON = (r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|"
        r"sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?![A-Za-z])")
_MON_NUM = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
_ORD = r"(?:st|nd|rd|th)?"
_SP = r"(?:\s+|-)"

_I = _re.IGNORECASE
_P_ISO = _re.compile(
    r"(?<![0-9])([0-9]{4})-([0-9]{2})-([0-9]{2})"
    r"(?:[T ][0-9]{2}:[0-9]{2}(?::[0-9]{2}(?:[.,][0-9]+)?)?(?:Z|[+-][0-9]{2}:?[0-9]{2})?)?(?![0-9])"
)
_P_YMD_SEP = _re.compile(r"(?<![0-9])([0-9]{4})([/._])([0-9]{2})\2([0-9]{2})(?![0-9])")
_P_NUM_DMY = _re.compile(r"(?<![0-9])([0-9]{1,2})([/.\-])([0-9]{1,2})\2([0-9]{4})(?![0-9])")
_P_D_MON_Y = _re.compile(
    r"(?<![0-9A-Za-z])([0-9]{1,2})" + _ORD + _SP + _MON + r"\.?" + _SP + r"([0-9]{4})(?![0-9])", _I)
_P_MON_D_Y = _re.compile(
    r"(?<![A-Za-z])" + _MON + r"\.?\s+([0-9]{1,2})" + _ORD + r",?\s+([0-9]{4})(?![0-9])", _I)
_P_COMPACT = _re.compile(
    r"(?<![0-9A-Za-z])([0-9]{4})([0-9]{2})([0-9]{2})(?:T[0-9]{4,6}(?:\.[0-9]+)?Z?(?:_[0-9a-f]{6,12})?)?(?![0-9])"
)
_P_YM_DASH = _re.compile(r"(?<![0-9-])([0-9]{4})-([0-9]{2})(?![0-9-])")
_P_YM_SLASH = _re.compile(r"(?<![0-9/.\-])([0-9]{4})/([0-9]{2})(?![0-9/])")
_P_MY_SLASH = _re.compile(r"(?<![0-9/.\-])([0-9]{1,2})/([0-9]{4})(?![0-9])")
_P_MON_Y = _re.compile(r"(?<![A-Za-z])" + _MON + r"\.?\s+([0-9]{4})(?![0-9])", _I)
_P_Q_FIRST = _re.compile(r"(?<![0-9A-Za-z])Q([1-4])(?:\s+|[-_])([0-9]{4})(?![0-9])", _I)
_P_Q_LAST = _re.compile(r"(?<![0-9])([0-9]{4})(?:\s+|[-_])?Q([1-4])(?![0-9A-Za-z])", _I)
_P_H_FIRST = _re.compile(r"(?<![0-9A-Za-z])H([12])(?:\s+|[-_])([0-9]{4})(?![0-9])", _I)
_P_H_LAST = _re.compile(r"(?<![0-9])([0-9]{4})(?:\s+|[-_])?H([12])(?![0-9A-Za-z])", _I)


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


# --------------------------------------------------------------------------- period tests


def _day_hit(y, m, d, lo, hi):
    try:
        return lo <= _date(int(y), int(m), int(d)) <= hi
    except ValueError:
        return False


def _span_hit(y, m1, m2, lo, hi):
    """True when months m1..m2 (inclusive) of year y intersect [lo, hi]."""
    try:
        y = int(y)
        first = _date(y, m1, 1)
        last = _date(y + (m2 == 12), 1 if m2 == 12 else m2 + 1, 1).toordinal() - 1
    except ValueError:
        return False
    return first <= hi and _date.fromordinal(last) >= lo


def _month_hit(y, m, lo, hi):
    m = int(m)
    return 1 <= m <= 12 and _span_hit(y, m, m, lo, hi)


def _h_ymd(m, lo, hi):
    return _day_hit(m.group(1), m.group(2), m.group(3), lo, hi)


def _h_ymd_sep(m, lo, hi):
    return _day_hit(m.group(1), m.group(3), m.group(4), lo, hi)


def _h_num_dmy(m, lo, hi):
    a, b, y = m.group(1), m.group(3), m.group(4)
    return _day_hit(y, b, a, lo, hi) or _day_hit(y, a, b, lo, hi)


def _h_d_mon_y(m, lo, hi):
    return _day_hit(m.group(3), _MON_NUM[m.group(2)[:3].lower()], m.group(1), lo, hi)


def _h_mon_d_y(m, lo, hi):
    return _day_hit(m.group(3), _MON_NUM[m.group(1)[:3].lower()], m.group(2), lo, hi)


def _h_ym(m, lo, hi):
    return _month_hit(m.group(1), m.group(2), lo, hi)


def _h_my(m, lo, hi):
    return _month_hit(m.group(2), m.group(1), lo, hi)


def _h_mon_y(m, lo, hi):
    return _month_hit(m.group(2), _MON_NUM[m.group(1)[:3].lower()], lo, hi)


def _h_q_first(m, lo, hi):
    q = int(m.group(1))
    return _span_hit(m.group(2), 3 * q - 2, 3 * q, lo, hi)


def _h_q_last(m, lo, hi):
    q = int(m.group(2))
    return _span_hit(m.group(1), 3 * q - 2, 3 * q, lo, hi)


def _h_h_first(m, lo, hi):
    h = int(m.group(1))
    return _span_hit(m.group(2), 6 * h - 5, 6 * h, lo, hi)


def _h_h_last(m, lo, hi):
    h = int(m.group(2))
    return _span_hit(m.group(1), 6 * h - 5, 6 * h, lo, hi)


# (pattern, handler); on a tie in start position the earlier entry wins
_PATTERNS = [
    (_P_ISO, _h_ymd),
    (_P_YMD_SEP, _h_ymd_sep),
    (_P_NUM_DMY, _h_num_dmy),
    (_P_D_MON_Y, _h_d_mon_y),
    (_P_MON_D_Y, _h_mon_d_y),
    (_P_COMPACT, _h_ymd),
    (_P_YM_DASH, _h_ym),
    (_P_YM_SLASH, _h_ym),
    (_P_MY_SLASH, _h_my),
    (_P_MON_Y, _h_mon_y),
    (_P_Q_FIRST, _h_q_first),
    (_P_Q_LAST, _h_q_last),
    (_P_H_FIRST, _h_h_first),
    (_P_H_LAST, _h_h_last),
]


def sanitize_text(text):
    """Mask every in-window date token in `text`. Non-strings are returned unchanged."""
    if not isinstance(text, str):
        return text
    lo, hi = _load()
    if not any(ch.isdigit() for ch in text):
        return text
    nxt = [p.search(text) for p, _ in _PATTERNS]
    out = []
    pos = 0
    while True:
        best = None
        for i, m in enumerate(nxt):
            if m is not None and (best is None or m.start() < nxt[best].start()):
                best = i
        if best is None:
            break
        m = nxt[best]
        out.append(text[pos:m.start()])
        out.append(_MASK if _PATTERNS[best][1](m, lo, hi) else m.group(0))
        pos = m.end()
        for i, mm in enumerate(nxt):
            if mm is not None and mm.start() < pos:
                nxt[i] = _PATTERNS[i][0].search(text, pos)
    if pos == 0 and not out:
        return text
    out.append(text[pos:])
    return "".join(out)


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
