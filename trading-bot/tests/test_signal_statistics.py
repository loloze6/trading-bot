"""
Known-answer tests for performance.signal_statistics (2026-07-09).

Hard rule under test: a zero-variance input series makes a correlation
mathematically undefined -- these functions must return None, never a
fabricated 0.0, and must never derive a p-value from an undefined
correlation. See the module's own docstring for the incident this fixes.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from performance.signal_statistics import (
    has_zero_variance,
    pearson_correlation,
    spearman_correlation,
    t_test_pvalue,
)


def test_has_zero_variance_constant_series():
    assert has_zero_variance([10.0, 10.0, 10.0, 10.0]) is True


def test_has_zero_variance_varying_series():
    assert has_zero_variance([1.0, 2.0, 3.0, 4.0]) is False


def test_has_zero_variance_single_element():
    assert has_zero_variance([5.0]) is True


def test_pearson_correlation_none_on_constant_x():
    """The exact P4_ts_trend shape: forecast is always +10.0 when active."""
    x = [10.0] * 20
    y = [0.001, -0.002, 0.003, -0.001] * 5
    assert pearson_correlation(x, y) is None


def test_pearson_correlation_none_on_constant_y():
    x = [1.0, 2.0, 3.0, -1.0, -2.0]
    y = [5.0] * 5
    assert pearson_correlation(x, y) is None


def test_pearson_correlation_real_value_on_varying_input():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    corr = pearson_correlation(x, y)
    assert corr is not None
    assert abs(corr - 1.0) < 1e-9


def test_spearman_correlation_none_on_constant_series():
    x = [10.0] * 20
    y = list(range(20))
    assert spearman_correlation(x, y) is None


def test_t_test_pvalue_none_when_corr_is_none():
    """HARD RULE: never fabricate a p-value from an undefined correlation."""
    assert t_test_pvalue(None, 100) is None


def test_t_test_pvalue_real_value_on_real_correlation():
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    y = [1.1, 2.2, 2.9, 4.1, 5.2, 5.8, 7.3, 7.9, 9.1, 10.2]
    corr = pearson_correlation(x, y)
    pvalue = t_test_pvalue(corr, len(x))
    assert corr is not None and pvalue is not None
    assert pvalue < 0.01  # near-perfect linear relationship, must be highly significant
