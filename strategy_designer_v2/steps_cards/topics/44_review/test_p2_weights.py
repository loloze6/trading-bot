"""Checks of topic 44's P2 weight rules on made-up returns."""
import numpy as np
import p2_weights as p


def test_capped_sums_to_one_and_respects_cap():
    w = p.capped([10, 1, 1, 1], 2.0)
    assert abs(w.sum() - 1) < 1e-12 and w.max() <= 0.5 + 1e-12


def test_inverse_swing_halves_weight_for_double_swing():
    rng = np.random.default_rng(0); a = rng.normal(0, 1, 5000)
    w = p.inverse_swing(np.c_[a, 2 * a[::-1]])
    assert abs(w[0] / w[1] - 2) < 1e-9


def test_risk_shared_equals_inverse_swing_when_uncorrelated_and_equalises_contributions():
    rng = np.random.default_rng(1); X = rng.normal(0, 1, (20000, 3)) * [1, 2, 4]
    w = p.risk_shared(X); C = np.cov(X, rowvar=False); rc = w * (C @ w)
    assert np.allclose(rc / rc.sum(), 1 / 3, atol=0.01)
    assert np.allclose(w, p.inverse_swing(X), atol=0.01)


def test_weights_use_only_days_before():
    rng = np.random.default_rng(2); X = rng.normal(0, 0.01, (300, 4)); Y = X.copy(); Y[200:] *= 50
    for rule in ("equal risk", "shared risk"):
        a, b = p.weights(X, rule), p.weights(Y, rule)
        assert np.allclose(a[:201], b[:201]) and not np.allclose(a[201:], b[201:])
