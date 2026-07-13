"""
Shared, degenerate-safe statistics for forecast/signal series.

HARD RULE (2026-07-09, P4_ts_trend incident): a zero-variance input makes a
correlation coefficient mathematically UNDEFINED, not zero. This happens
whenever a signal's forecast is a single constant magnitude across every bar
being correlated against (e.g. a long-only component that outputs exactly
+10.0 whenever active, never varying, never negative -- filtering to
active-bars-only then leaves zero variance to correlate against returns).

Two independent call sites (strategy-research/tools/prescreen_signal.py and
trading-bot/reporting/run_artifact.py::build_core) each hand-rolled their own
correlation with their own degenerate-case handling. prescreen_signal.py's
version correctly returned None. run_artifact.py's version fell back to a
hardcoded corr=0.0, and then computed a p-value FROM that fake 0.0 (p=1.0) --
producing a "corr=0.0, p=1.0, high confidence no-edge" result that is actually
a mathematical artifact of the signal's SHAPE, not evidence about its quality.
This surfaced when the two stages' outputs materially disagreed (prescreen:
pooled_ic=0.0359, p=0.004, significant; full backtest: corr=0.0, p=1.0,
identically across all 24 window-symbol pairs) -- a pattern that should never
coexist silently (see run_protocol.py's prescreen/backtest cross-check).

Every consumer of a forecast-vs-return correlation MUST use these functions
(or another function that composes them) instead of hand-rolling the same
logic a third time:
  - Zero variance in EITHER series -> return None. Never 0.0, never False.
  - No p-value is ever computed from an undefined (None) correlation.
"""
import math
from typing import Optional, Sequence


def has_zero_variance(values: Sequence[float], tol: float = 1e-10) -> bool:
    """True if `values` has no variance (all elements effectively identical,
    or fewer than 2 elements). Works with plain lists or numpy arrays."""
    n = len(values)
    if n < 2:
        return True
    mean = sum(values) / n
    return sum((v - mean) ** 2 for v in values) < tol


def pearson_correlation(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
    """
    Pearson correlation coefficient. Returns None (never a fabricated 0.0)
    when either series has zero variance -- mathematically undefined, not
    "no correlation found."
    """
    n = len(x)
    if n < 2 or len(y) != n:
        return None
    if has_zero_variance(x) or has_zero_variance(y):
        return None

    x_mean = sum(x) / n
    y_mean = sum(y) / n
    xm = [v - x_mean for v in x]
    ym = [v - y_mean for v in y]
    denom = math.sqrt(sum(v * v for v in xm) * sum(v * v for v in ym))
    if denom < 1e-12:
        return None
    corr = sum(a * b for a, b in zip(xm, ym)) / denom
    return max(-1.0, min(1.0, corr))


def spearman_correlation(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
    """
    Spearman rank correlation. Returns None (never a fabricated 0.0) when
    either series is constant in rank space (fewer than 3 points, or all
    values tie into a single rank) -- mathematically undefined.
    """
    n = len(x)
    if n < 3 or len(y) != n:
        return None

    def _rank(vals):
        sorted_i = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and vals[sorted_i[j + 1]] == vals[sorted_i[j]]:
                j += 1
            avg_r = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                ranks[sorted_i[k]] = avg_r
            i = j + 1
        return ranks

    rx = _rank(x)
    ry = _rank(y)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    cov = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n)) / n
    std_rx = math.sqrt(sum((r - mean_rx) ** 2 for r in rx) / n)
    std_ry = math.sqrt(sum((r - mean_ry) ** 2 for r in ry) / n)
    if std_rx < 1e-10 or std_ry < 1e-10:
        return None
    return cov / (std_rx * std_ry)


def t_test_pvalue(corr: Optional[float], n: int) -> Optional[float]:
    """
    Two-tailed t-test p-value for a correlation coefficient computed on n
    paired observations. HARD RULE: if corr is None (undefined), returns None
    -- a p-value is NEVER fabricated from an undefined statistic. Computing
    p=1.0 from a fake corr=0.0 is the same "displaying undefined as measured"
    defect as printing an undefined IC as the literal string "0.0000".
    """
    if corr is None:
        return None
    if abs(corr) >= 1.0:
        return 0.0
    if n <= 2:
        return None
    try:
        from scipy.stats import t as t_dist
    except ImportError:
        return None
    t_stat = corr * math.sqrt((n - 2) / (1.0 - corr ** 2))
    return float(2 * t_dist.sf(abs(t_stat), df=n - 2))
