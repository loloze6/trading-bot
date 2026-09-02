"""Shared cache-availability guard for the sr fast suite (CUL-198).

One canonical skip for untracked-cache reads, replacing the per-file
``@pytest.mark.skipif(not X.exists(), ...)`` boilerplate. Lives in a
uniquely-named module (not conftest.py) so tests import it without the
two-conftest name collision that ``from conftest import`` risks in this tree
(strategy-research/tests/ and tools/recorder/tests/ both hold a conftest.py).
"""

from pathlib import Path

import pytest

_CACHE_MIN_BYTES = 1024  # an empty/header-only OHLCV or funding CSV sits well below this


def cache_is_available(path, *, min_bytes=_CACHE_MIN_BYTES, min_rows=None):
    """True iff ``path`` exists and is not degenerate.

    Degenerate = a regular file smaller than ``min_bytes``, or (when
    ``min_rows`` is given) with fewer than ``min_rows`` lines. A directory
    counts as present on existence alone (the ``runs/`` fixtures are
    directory-shaped). A bare ``.exists()`` is deliberately NOT enough: a
    truncated or header-only cache exists yet cannot back a real backtest --
    the degenerate-cache lesson from CUL-45.
    """
    p = Path(path)
    if not p.exists():
        return False
    if p.is_dir():
        return True
    try:
        if p.stat().st_size < min_bytes:
            return False
    except OSError:
        return False
    if min_rows is not None:
        try:
            with p.open("rb") as fh:
                n_lines = sum(1 for _ in fh)
        except OSError:
            return False
        if n_lines < min_rows:
            return False
    return True


def requires_cache(*paths, min_bytes=_CACHE_MIN_BYTES, min_rows=None, reason=None):
    """A ``skipif`` mark that skips when any named cache file is absent or degenerate.

    Drop-in replacement for the ad-hoc
    ``@pytest.mark.skipif(not X.exists(), reason=...)`` boilerplate. The
    condition is evaluated once at collection time, exactly as ``skipif``
    always is.
    """
    missing = [str(p) for p in paths if not cache_is_available(p, min_bytes=min_bytes, min_rows=min_rows)]
    default = "cache file(s) absent or degenerate: " + (", ".join(missing) or "none")
    return pytest.mark.skipif(bool(missing), reason=reason or default)
